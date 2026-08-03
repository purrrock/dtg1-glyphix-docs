# 全局资源迁移指南

本文面向 Glyphix 下游集成项目，帮助你将历史项目中的全局资源加载方式升级到最新方案，获得易于管理、编辑的全局资源布局，不再依赖厂商的打包或转换工具支持。

早期 Glyphix 采用 `global.pkg` 二进制归档包管理全局资源（字体文件、字体映射表等），后来逐步演进为直接使用未打包资源文件，最终字体映射文件的格式也从二进制转为标准 JSON <version-badge since="0.9" /> 。如果你维护的入口代码仍沿用旧写法，可以按本文升级。

::: tip
使用旧模式存在维护麻烦、难以管理和编辑全局资源的问题，建议立即升级。
:::

## 去除 `global.pkg`

### 旧代码特征

如果你的入口代码中存在类似以下任一模式，说明你正在使用 `global.pkg`：

```cpp
EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
static String globalUri(const String &path) { return "pkg:///" + path; }
```

这两行的效果是：将所有 `pkg:///` 协议的资源请求路由到 `/global.pkg` 这个二进制归档包内部的文件。

为什么需要去除：
- 每次更换字体等资源，都必须重新运行打包工具生成 `.pkg` 文件
- 调试时无法直接查看或替换 `.pkg` 内部的单个文件，也难以核对内容
- 打包流程依赖专用工具，增加沟通和维护成本

### 迁移操作

**第一步：解出 `global.pkg` 中的资源。**

如果你已经没有 `.pkg` 源文件，可以从 `global.pkg` 中解出内容（使用 Glyphix 命令行工具或索取原始资源文件）。通常需要解出以下内容：

```
fonts/
    NotoSans-Regular.ttf
    NotoSansSC-Regular.ttf
    ...
    font-faces          ← 字体映射文件（后续会升级为 JSON）
```

将解出的目录放置到你的项目资源目录中，例如 `/fonts/`。

**第二步：移除 `global.pkg` 相关代码。**

1. 删除 `EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg")` 整行
2. 删除 `globalUri()` 这类包装函数
3. 将所有 `pkg:///xxx` 的资源引用改为直接文件路径，即 `/xxx`

**第三步：修改字体加载代码。**

假设你的初始化代码原本类似：

```cpp
static String globalUri(const String &path) { return "pkg:///" + path; }

static void setupFont(const String &fontMap) {
    String uri = globalUri(fontMap);
    FontFaceMap &map = App()->fontManager()->faces();
    if (!map.readFile(uri))
        LogError() << "Failed to load font face map: " << fontMap;
}

int main() {
    Application app;
    EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
    setupFont("font-faces");
    // ...
}
```

改为直接使用文件路径（没有 `globalUri()` 函数和 `GlobalPackage` 注册）：

```cpp
static void setupFont(const String &fontMap) {
    auto &map = App()->fontManager()->faces();
    if (!map.readFile(fontMap))
        LogError() << "Failed to load font face map: " << fontMap;
}

int main() {
    Application app;
    setupFont("/fonts/font-faces");
    // ...
}
```

此时资源布局变为：

```
/fonts/
    font-faces          ← 二进制格式
    NotoSans-Regular.ttf
    ...
```

这个阶段你仍然使用二进制的 `font-faces` 文件，下一节将其升级为 JSON。

## 改用 JSON 字体映射文件

### 旧代码特征

```cpp
FontFaceMap &map = App()->fontManager()->faces();
map.readFile("/fonts/font-faces");
```

`readFile` 读取的是自定义二进制格式文件，这个二进制文件不能手工编辑，必须从 CSS 文件用打包工具转换生成。

### JSON 格式说明

现在我们直接用 JSON 文件描述字体映射关系。你只需要创建一个 `font-faces.json` 文件，格式如下：

```json
{
  "font-faces": [
    {
      "family": "sans-serif",
      "weight": 400,
      "style": "normal",
      "urls": [
        "NotoSans-Regular.ttf",
        "NotoSansSC-Regular.ttf",
        "NotoSansJP-Regular.ttf"
      ]
    },
    {
      "family": "sans-serif",
      "weight": 700,
      "style": "normal",
      "urls": [
        "NotoSans-Bold.ttf"
      ]
    },
    {
      "family": "serif",
      "weight": 400,
      "style": "normal",
      "urls": [
        "NotoSerif-Regular.ttf"
      ]
    }
  ]
}
```

字段说明：

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `family` | 字符串 | 是 | - | 字体族名，如 `sans-serif`、`serif` |
| `weight` | 整数 | 否 | 400 | CSS 字重值（100-900），400 为常规，700 为加粗 |
| `style` | 字符串 | 否 | normal | 字体样式，可选 `italic` 或 `oblique` |
| `urls` | 字符串数组 | 是 | - | 字体文件路径，相对于 JSON 文件所在目录 |

下面对关键字段做进一步说明。

**weight 字段**

weight 直接填 CSS 字重数值，会舍入到最近的标准值：

- `100` Thin
- `400` Regular（默认值，不填即可）
- `700` Bold
- `900` Black

**urls 路径解析**

`urls` 中的路径相对于 JSON 文件所在的目录解析。例如 JSON 文件位于 `/fonts/font-faces.json`，则 `urls` 中写 `"fonts/NotoSans-Regular.ttf"` 最终解析为 `/fonts/fonts/NotoSans-Regular.ttf`。

因此建议 JSON 文件直接放置在字体文件同级目录，这样 URL 可以直接写文件名。例如目录布局为：

```
/fonts/
    font-faces.json
    NotoSans-Regular.ttf
    NotoSansSC-Regular.ttf
    NotoSans-Bold.ttf
```

此时 JSON 内容如上述代码所示。

### 代码修改

将初始化代码中的 `readFile` 替换为 `readJSON`：

```cpp
#include "gx_fontmanager.h"

static void setupFont() {
    auto &map = App()->fontManager()->faces();
    if (!map.readJSON("/fonts/font-faces.json"))
        LogError() << "Failed to load font-faces.json";
    App()->setFont(Font("sans-serif", 24));
}

int main() {
    Application app;
    setupFont();
    // ...
}
```

就这一处 API 调用变更，其余代码无需修改。之后你可以直接编辑 `font-faces.json` 来增删字体或调整映射关系，不再需要任何转换工具。

## FAQ

**如何处理同一个 family 有 Regular、Bold、Italic 等多个变体？**

在 `font-faces` 数组中为每个变体添加独立条目，用 `weight` 和 `style` 区分：

```json
{
  "font-faces": [
    {
      "family": "sans-serif",
      "weight": 400,
      "style": "normal",
      "urls": ["NotoSans-Regular.ttf"]
    },
    {
      "family": "sans-serif",
      "weight": 700,
      "style": "normal",
      "urls": ["NotoSans-Bold.ttf"]
    },
    {
      "family": "sans-serif",
      "weight": 400,
      "style": "italic",
      "urls": ["NotoSans-Italic.ttf"]
    }
  ]
}
```

MCU 项目通常只使用 `normal` 字重的 Regular `sans-serif` 字体，系统会自动回退。

**`urls` 数组里可以放多个文件吗？什么时候需要？**

可以。当一个字体族需要覆盖多语种字符时，将多个字体文件放入同一个 `urls` 数组。例如 `sans-serif` 需要同时支持拉丁字母、中日韩文字、阿拉伯文：

```json
{
  "family": "sans-serif",
  "weight": 400,
  "style": "normal",
  "urls": [
    "NotoSans-Regular.ttf",
    "NotoSansSC-Regular.ttf",
    "NotoSansJP-Regular.ttf",
    "NotoSansArabic.ttf"
  ]
}
```

引擎渲染文本时会按顺序在这些文件中查找字符字形，第一个匹配到的字形将被使用。

**字体文件必须和 JSON 放在同一目录吗？**

不是。`urls` 中的路径相对于 JSON 文件所在目录解析，你可以使用相对路径将字体放在子目录中。也可以使用绝对路径，此时不受 JSON 目录影响。

**可以直接在代码中传入 JSON 字符串吗？**

可以。使用两参数重载版本：

```cpp
map.readJSON("/fonts/", R"({
  "font-faces": [
    {"family": "sans-serif", "urls": ["NotoSans-Regular.ttf"]}
  ]
})");
```

第一个参数是 baseUri，用于解析 `urls` 中的相对路径。
