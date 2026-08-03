# 平台字体回退

Glyphix 框架内置了一套基于 font-face / font-family 的字体加载与回退机制。但目标平台通常自带完善的字体管线（如 Windows DirectWrite、macOS CoreText），它们已实现系统字体回退与相关优化。

为充分利用平台字体管线，Glyphix 允许你接管字体回退：当框架内字体无法覆盖某个字符时，转交平台去查找并渲染合适的系统字体。本文面向 Glyphix 的系统开发者，带你一步步完成对接。

涉及的公共头文件：
- `gx_unite.h`：含 UniTE 公共接口，以及引擎安装函数 `installEngine()`；
- `gx_shapingadapter.h`：此为主要接口；
- `gx_fontdriver.h`：提供 `FontDriver` 封装机制；
- `gx_fontloader.h`：提供字体加载器接口。

## 整体思路

一段文本要在屏幕上显示，会经过下面这条管线：应用文本交由**段落布局引擎**分行、定位；每段同脚本、同方向的文本被**塑形**成字形；缺字时由**字体回退**补齐；字形再交**字体驱动**渲染成位图；而所有字体都来自**字体管理**层的注册、加载与复用。

<ArchDiagram max-width="560px">
  <div>应用文本<div class="remark">段落 · 字符串 · 样式</div></div>
  <div>
    段落布局引擎
    <div class="group row">
      <div>轻量引擎 LiTE<div class="remark">简单排版（默认引擎）</div></div>
      <div>UniTE 引擎<div class="remark">BiDi · Shape · 复杂脚本</div></div>
    </div>
  </div>
  <div>
    塑形 · 字体回退
    <div class="group row">
      <div>HarfBuzz<div class="remark">GSUB / GPOS</div></div>
      <div>Simple Shape<div class="remark">字符 → 字形</div></div>
      <div class="subject">FontFallbackShaper<div class="remark">family 回退 · 平台系统字体</div></div>
    </div>
  </div>
  <div>
    字体渲染
    <div class="group row">
      <div>FontDriver<div class="remark">TTF / FreeType</div></div>
      <div>FontDriverFamily<div class="remark">多 face 级联</div></div>
      <div class="subject">PlatformFont 包装器<div class="remark">绘制平台回退字形</div></div>
    </div>
    <div>GlyphCache - 字形位图缓存</div>
  </div>
  <div>
    字体管理 FontManager
    <div class="group row">
      <div>注册 / 查找<div class="remark">face · family · 属性</div></div>
      <div class="subject">FontLoader<div class="remark">加载 face，注入包装器</div></div>
    </div>
  </div>
</ArchDiagram>

图中高亮的三部分即本文涉及内容：
1. 回退策略 `FontFallbackShaper`，用于找出缺字并回退塑形；
2. 负责绘制平台回退字体的 `PlatformFont` 包装器，与 `FontFallbackShaper` 配套使用；
3. 用于加载平台回退字体包装器的 `FontLoader`，将注册到 `FontManager` 中。

其余各层框架已实现，文本塑形（`ShapingAdapter`）通常无需重头实现，直接复用参考实现即可。

### 前置条件

按本文档实现平台字体回退功能前，需要：

- 启用 UniTE 文本引擎（相比默认轻量引擎，它支持复杂脚本塑形与多级回退）。
- 目标平台支持完整的字体管线，能提供系统字体的塑形、脚本映射等高级功能。这通常是一个复杂的子系统，大部分 MCU RTOS 平台不具备。

::: important
相比于默认的 LiTE 引擎，启用 UniTE 以及完整的字体管线需要更多的内存和固件空间。且该引擎的性能较轻量的 LiTE 要差，需要评估是否需要为了完整的 Unicode 支持和国际化需求而启用它。
:::

## 复用塑形后端

`ShapingAdapter` 负责把字符塑形成字形。自带的 `HarfBuzzShaper`（`gx_harfbuzz_shaper.cpp`）已实现完整的 OpenType 塑形，它调用 HarfBuzz 塑形，再把字形索引、advance、偏移按目标像素尺寸写入输出。

`HarfBuzzShaper` 依赖 Freetype 读取字体文件，因此需要同时引入 HarfBuzz 和 Freetype 库。若目标平台已经存在这些库，请保证版本一致，否则可能出现链接或运行时错误。

::: tip
和 HarfBuzz 的[职责](https://harfbuzz.github.io/what-harfbuzz-doesnt-do.html)类似，`ShapingAdapter` 也不处理包含不同字体的文本 run，这也包括下文介绍的“字体回退”机制情况。因此，只要 shaping 中使用的字体缺字，`ShapingAdapter` 实现就会返回 `.notdef` 字形（索引 `0`），并由回退策略去处理。
:::

## 实现回退策略

`FontFallbackShaper` 是回退的核心。引擎每塑形一截文本就调用它一次，要求交回一份**不含缺字**的字形序列作为塑形结果。与 `ShapingAdapter` 不同，它不只是针对单一 font-face 的塑形，而是设计用于两级回退。

### 两级回退级联

`FontFallbackShaper::shape()` 回退按“由近及远”分两级：

- **第一级**：在当前 family 内部用其它字体互相补字。框架已实现，你只需调用 `builtinShape()`。
- **第二级**：第一级仍补不上的缺字，交给平台系统字体。这一级由你实现。

缺字在数据里表现为字形索引为 `0`，即 `.notdef`。`shape()` 的返回值 `FallbackResult` 用位标志表达结果：`result & NotNeeded` 为真表示已无缺字、可直接结束；否则常见返回 `FullyResolved`（全部处理完）或 `PartiallyResolved`（仍有残留 `.notdef`）。

### `shape()` 函数骨架

先调用第一级；若已无缺字就返回，否则进入第二级的平台字体回退。`m_shaper` 是这个回退器持有的 `ShapingAdapter`（通常就是 `HarfBuzzShaper`）。

```cpp
FallbackResult shape(GlyphRunBundle &storage,
                     TextSpan text,
                     FontDriver *font) override {
    // 第一级：使用 builtin API 处理 family 内的回退
    auto r = builtinShape(storage, text, font, &m_shaper);
    if (r & NotNeeded)
        return r;                                  // 已无缺字，结束
    return resolveByPlatform(storage, text, font); // 第二级，见下
}
```

`builtinShape()` 是唯一依赖 `ShapingAdapter` 的地方，这种情况下你通常需要将 `PlatformFallbackShaper` 实现如下：
```cpp
class PlatformFallbackShaper : public FontFallbackShaper {
    HarfBuzzShaper m_shaper; // 直接定义成员变量，不需要指针引用

public:
    PlatformFallbackShaper() = default;
    FallbackResult shape(GlyphRunBundle &storage,
                         TextSpan text, FontDriver *font) override;
};
```
请注意，`m_shaper` 仅仅是你的平台回退策略的私有成员变量，完全不需要暴露给外部使用。`shape()` 内部调用 `builtinShape()` 时传入 `&m_shaper` 即可。

::: tip
极端情况下（如初步适配阶段）可以不管 family 内的回退，直接跳过 `builtinShape()`，只处理第二级平台回退。此时可以省去 `m_shaper` 成员变量。

无论如何，`ShaperAdapter` 具体类通常不能定义为局部变量，因为它可能持有 HarfBuzz 的缓存状态，若每次塑形都重新创建会导致严重的性能下降。
:::

### 取得平台字体

第二级要把缺字交给平台，并最终让包装器去渲染。`fallbackFont(font)` 返回注册在 family 末项的那个包装器（见后文）。它的静态类型是 `FontDriver *`，你需要转回自己的包装器类型，才能调用你自定义的登记、查询接口。

```cpp
// 转型也可用 dyn_cast，但如果只有一个包装器类型，static_cast 也安全
auto *wrapper = static_cast<PlatformFont *>(fallbackFont(font));
if (wrapper == nullptr)
    return PartiallyResolved; // family 末项没有包装器，无法继续
```

::: warning 必须成对实现
回退策略与包装器是配套的一对：上面的 `static_cast` 要求 `fallbackFont()` 返回的正是你自己的包装器类型。务必保证安装的回退器与注册的包装器相互匹配。
:::

### 简单回退塑形

最常见且适合起步的情形是：整段 run 都可用同一平台字体塑形（即某一系统字体文件完全覆盖该脚本）。此时按 `storage.run().spec.script` 选定平台字体，对整 run 重塑一次，整段写入同一个 `faceId`，**直接覆盖第一级结果**，无需与已解析字形做合并。

UniTE 按 script 切分 run，同一段文本里的拉丁与 CJK 本就是不同 run。当主字体主打拉丁、遇到 CJK, Arabic, Devanagari 等 script 时，该 run 经 `builtinShape()` 后往往整段都是 `.notdef`，整段重塑并覆盖不会丢失任何已解析字形。所以多语言排版绝大多数走这条路径，并非退化特例。

```cpp
// 按脚本选定平台字体（平台字体句柄，非 FontDriver），登记得 faceId
auto sysFont = platformFontForScript(storage.run().spec.script);
uint32_t faceId = wrapper->registerFont(sysFont);
// 你的塑形步骤产出 glyphCount 个字形（此处以 HarfBuzz 产物演示）
auto &run = storage.resize(glyphCount);
for (int i = 0; i < glyphCount; ++i) {
    run.data.glyphIds[i]   = GlyphIds::encodeFallback(gid[i], faceId);
    run.data.xAdvances[i]  = uint16_t(scale(pos[i].x_advance));
    run.data.xOffsets[i]   = int16_t(scale(pos[i].x_offset));
    run.data.yOffsets[i]   = int16_t(scale(pos[i].y_offset));
    run.data.clusterMap[i] = static_cast<int>(info[i].cluster);
}
```

`pos`, `info`, `gid` 和 `scale` 字段来自你的塑形步骤，上面用 HarfBuzz 的输出作演示。

::: tip 平台塑形能力
平台通常自带塑形能力（如 DirectWrite、CoreText），是否复用 HarfBuzz 按具体平台决定；演示中的 HarfBuzz 产物替换为平台塑形输出即可。RTL run（`spec.bidiLevel & 1`）需把方向传给塑形器。
:::

此方法的前提是整段 run 映射到单一平台字体。它**不适用 Common script**（Emoji、符号等）：同一 run 内不同字符可能分属多种平台字体，需要下文的复杂回退。

### 复杂回退塑形

当一个 run 内需要多种平台字体、或仅部分簇需要回退时，简单方案不再适用。考虑到具体的回退和合并算法取决于平台 API，本文档只约束合并后 `GlyphRun` 必须满足的语义，实现需自行处理：

- 第一级已解析的字形**原样保留**，第二级只替换仍为 `.notdef` 的簇。
- 每个字形槽填齐 `glyphIds`, `xAdvances`, `xOffsets`, `yOffsets`, `clusterMap`；回退字形用 `encodeFallback(gid, faceId)` 标记。
- `clusterMap[i]` 为该字形对应源码点相对**本 run** 的偏移（与 `spec.text` 一致，范围 `[0, text.length())`），供绘制回映与按行裁剪。
- 字形数量可变：用 `storage.resize()/reset()` 调整存储，然后逐槽写入。`GlyphRunBundle` 内部会自动更新 `run().glyphCount`。
- 同一源簇映射到多个字形时，顺序与 advance 之和须正确；GSUB 合簇吞并的码点应产出零 advance 字形，避免空隙或错位。
- `faceId` 须为包装器登记过、全生命周期稳定的 ID；RTL run 的字形顺序与塑形方向须一致。
- 返回值：全部补齐返回 `FullyResolved`，仍有残留返回 `PartiallyResolved`。

只要输出满足上述约束，框架即可正确渲染，具体是分段查询平台 API、还是复用 HarfBuzz 逐字体塑形，可按平台选择。

### 行高与缓存

行高取决于每个字形**实际由哪个字体绘制**。`builtinLineMetrics()` 负责 family 内字形的部分；带回退标记（`isFallback()`）的字形则向包装器查询其系统字体的升降部并入。回退字形在 `GlyphIds` 里由 `encodeFallback` 编码，其 `fontIndex()` 即写入的 `faceId`，据此向包装器取回对应平台字体。

```cpp
VerticalMetrics resolveLineMetrics(const GlyphIds *gids, int count,
                                   FontDriver *font) const override {
    // 处理 family 内的字形
    VerticalMetrics m = builtinLineMetrics(gids, count, font);
    // 处理平台回退字形
    auto *wrapper = static_cast<PlatformFont *>(fallbackFont(font));
    if (wrapper == nullptr)
        return m;
    // 对 gids[i].isFallback() 的字形，向包装器查 asc/descent 并入 m
    for (auto gid : utils::span<const GlyphIds>(gids, count)) {
        if (!gid.isFallback())
            continue; // 只处理回退字形
        uint32_t faceId = gid.fontIndex(); // 回退字形的 fontIndex() 即 faceId
        auto face = wrapper->fontForFaceId(faceId); // 平台字体句柄（非 FontDriver）
        if (face == nullptr)
            continue;
        m.ascent = max(face->ascender(), m.ascent);
        m.descent = min(face->descender(), m.descent);
    }
    return m;
}
```

也可以汇总整行的回退字体并一次性查询它们的 asc/descent，避免循环中逐字形查询。

`flush()` 用来释放包装器缓存的系统字体：

```cpp
void flush(FontDriver *font) override {
    if (auto *w = static_cast<PlatformFont *>(fallbackFont(font)))
        w->releaseFonts();
}
```

::: tip
`flush()` 在段落销毁或内存紧张时由框架调用，请在其中清理包装器持有的平台资源。
:::

## 回退字体 `FontDriver` 包装器

包装器负责把上一步塑形的字形渲染成位图。它继承 `FontDriver`，构造时带上 `PlatformFallback` 标记，这样框架就知道它是回退字体。

```cpp
class PlatformFont : public FontDriver {
public:
    PlatformFont(const String &family, const FontAttribute &attr)
        : FontDriver(family, attr, Vector | PlatformFallback) {}
    // ... bitmapOf / metricsOf ...
protected:
    void requestHandler(int) override {}
};
```

该字体包装器并不用于加载某种字体文件（如 `FontDriverTTF` 那样）。它的作用是把回退字形交给平台字体管线去处理，而内部实现对 Glyphix 是不透明的。

### 双模式查询

包装器收到的 `code` 有两种含义，用 `CodeAsGlyphId` 位区分：

- **带标记**：按字形索引查询，高位携带 `faceId`，低位为字形索引。解出后路由到对应平台字体，再以 `glyphId` 查询对应的 `GlyphBitmap`。
- **不带标记**：Unicode 字符查询，按 codepoint 在已登记平台字体里兜底查找，内部自己转换为字形索引再查询。

常见的 `bitmapOf()` 实现如下：

```cpp
bool bitmapOf(uint32_t code, GlyphBitmap *bitmap) override {
    if (code & CodeAsGlyphId) { // 按字形索引
        uint32_t faceId  = (code >> 16) & 0x3ff;
        uint32_t glyphId =  code & 0xffff;
        auto face = fontForFaceId(faceId); // 平台字体句柄（非 FontDriver）
        return face && face->bitmapOf(glyphId, bitmap);
    }
    // Unicode 字符查找，这里遍历已注册字体，也可以用更高效的映射表
    for (auto *face : registeredFonts()) {
        uint32_t glyphId = face->glyphIndexOf(code);
        if (face->bitmapOf(glyphId, bitmap))
            return true;
    }
    return false;
}
```

::: tip
`fontForFaceId()` 返回的是平台字体句柄，**并非 `FontDriver`**；上述 `face->bitmapOf(...)`、`face->glyphIndexOf(...)` 是对该句柄操作的伪代码，分别表示“按 `glyphId` 取 `GlyphBitmap`”，“按码点取 `glyphId`”。
:::

`metricsOf()` 用同样的双模式逻辑；`advancesOf()`、`baseline()` 等也从平台字体计算。`duplicate()` 复制一份映射表即可。

### `faceId` 映射

包装器维护一张 `faceId` → 平台字体的映射，供回退策略登记、渲染时查回。

`faceId` 是 $10$ 位整数（$[0, 1023]$），含义完全由实现定义，唯一要求是**全生命周期稳定**。有两种常见做法：

- **按脚本固定**：直接用 `Script` 枚举值作 `faceId`，包装器按脚本持有对应平台字体，登记时即按脚本写入，无需运行时分配。
- **按需分配**：每遇到一个新平台字体就分配下一个索引，维护一张增长表。

按脚本固定的例子（`faceId` 即脚本值）：
```cpp
PlatformFontHandle fontForScript(Script script) {
    switch (script) {
    case Script::Han:    return sysHanFont;
    case Script::Arabic: return sysArabicFont;
    case Script::Latin:  return sysLatinFont;
    // ...
    }
    return sysDefaultFont;
}
```
你需要自行处理脚本→字体映射、`faceId` 分配与平台字体对象缓存。

::: tip
`faceId` 是回退策略与包装器之间的契约：`PlatformFallbackShaper` 用它编码字形，`PlatformFont` 用它解码回系统字体。两端对 `faceId` 的解释必须一致，并且要保证可以由 $10\rm bit$ 整数表示。
:::

## 注册包装器

最后让框架把包装器纳入 family 加载。实现 `FontLoader::load()`，对某个通用 family 名返回包装器，再装进 `FontManager`：

```cpp
struct PlatformFontLoader : public FontLoader {
    FontDriver *load(const String &face, const FontAttribute &attr) override {
        if (face == "sans-serif")
            return new PlatformFont(face, attr);
        return nullptr;
    }
};

CoreApp()->fontManager()->install(new PlatformFontLoader);
```

应用以 `"<primary-face>,sans-serif"` 形式请求字体时，框架按逗号顺序把各部分合并进同一个 family，包装器作为最后一项成为兜底 face，`fallbackFont()` 便能取到它。

`PlatformFont` 和 `PlatformFontLoader` 通常只注册为 `sans-serif` 这类通用 family 名的字体，而不是某个具体的系统字体名。这样应用就可以在不同平台上使用同一 family 名，而不需要知道平台的具体字体。

::: warning 功能限制
包装器总在 family 末项目前依赖应用按上述顺序书写 family 名。自动保证该顺序的机制尚在完善中。
:::

## 安装并装配

`gx_unite.h` 的 `installEngine()` 把你的回退策略接入引擎：

```cpp
unite::installEngine(*CoreApp()->typesetCore(),
                     std::make_unique<PlatformFallbackShaper>());
```

完整装配顺序：

1. `fontManager()->install(new PlatformFontLoader)`：注册包装器加载器。
2. `installEngine(...)`：安装持有塑形后端的回退策略。
3. 以 `"<primary-face>,sans-serif"` 形式请求字体，照常布局、绘制。

## 注意事项

- advance / 偏移一律为 Q26.6 定点（值 = 像素 × 64）。
- 仍未补齐的 `.notdef`（字形索引为 $0$）在渲染时被跳过，对应位置会显示空白或豆腐块。
- `faceId` 仅 $10$ 位，单个 family 同时活跃的系统字体上限为 $1024$ 个。
- 回退策略与包装器必须成对实现并保持类型一致（依赖 `static_cast`）。
- 在 `flush()` 中务必释放包装器持有的平台字体缓存。
