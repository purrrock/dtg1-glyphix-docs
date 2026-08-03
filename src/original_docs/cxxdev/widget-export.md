# 控件注册与框架集成

在[控件开发指南](./widget.md)中，我们实现了一个 C++ 控件类。但此时它还只是一个普通的 C++ 对象，应用开发者无法在页面代码中直接使用。本文介绍如何将控件注册到框架，使其成为可在应用中使用的组件。本文档的许多概念涉及[对象系统](./object-system.md)，建议先阅读相关内容。

## 运行环境

控件注册依赖一组**运行环境对象**。它们是响应式框架运行所必需的依赖，必须在 `main()` 或平台启动代码中显式创建，并且其生命周期要覆盖整个应用运行期间：

```cpp
Application app(/* platform */);
JsVM vm;
Window window;
AppletKit kit(&window, "pkgs.db");
```

这几个对象负责整个应用的运行环境：
- `Application` 框架应用对象负责所有底层服务并维护事件循环，在初始化的最后调用 `app.exec()` 进入事件循环；
- `JsVM` 是内嵌的 JavaScript 引擎，承载响应式框架的运行，**必须**在 `AppletKit` 之前创建；
- `Window` 是顶层窗口，作为渲染输出目标；
- `AppletKit` 是应用（Applet）管理器，负责应用生命周期与控件注册。

::: warning 不要省略这些对象
`vm`、`window`、`kit` 等是 RAII 对象，框架通过它们的构造/析构来管理运行环境。即使代码里看不到对 `vm` 的直接调用，它的**存在本身**就是必需的——提前销毁或不创建会导致框架无法工作。
:::

`Window window` 有时候也可以替换成 `Wigdet window` 等，区别在于 `Window` 默认绘制不透明背景，而 `Widget` 默认透明。

## 注册控件

控件的注册通过 `AppletKit::installWidget<T>()` 完成，在 `AppletKit` 实例化之后、`launch()` 启动第一个应用**之前**调用：

```cpp
// 注册自定义控件（在 launch 之前）
kit.installWidget<ProgressRing>(); // 无参数，以类名注册，模板中写作 <progress-ring>
kit.installWidget<MySpecialChart>("SpecialChart"); // 或用自定义名称注册（见下文）

kit.launch("com.example.app");     // 启动应用
return app.exec();                 // 进入事件循环
```

::: tip 内置控件默认已注册
框架自带的按钮、标签等内置控件由 `installBuiltinWidgets()` 注册。只要 SDK 构建时启用了 CMake 选项 `GX_BUILTIN_BINDINGS`（默认 `ON`），`AppletKit` 构造时就会**自动调用**它，无需手动处理。仅当显式关闭该选项时，才需要自己调用 `kit.installBuiltinWidgets()`。
:::

注册后，框架会根据控件类的 `GX_OBJECT` 元数据，自动导出其属性、事件、方法，以及它们用到的枚举、结构体类型，使其在应用层可用。

### 在应用页面中使用

注册成功后，应用开发者可以在页面模板中像使用内置控件那样使用它：

```xml
<!-- 以 progress-ring 组件为例 -->
<progress-ring
  class="ring"
  :value="progress"
  @completed="onDone">
</progress-ring>
```

这里 `:value="progress"` 把控件的 `value` 属性绑定到应用数据 `progress`；`@completed` 监听控件暴露的 `completed` 事件。框架自动完成 JavaScript 值与 C++ 属性的互相转换，开发者无需写任何"桥接代码"。

### 自定义组件名称

默认情况下，控件以**类名**注册。如果类名不适合直接作为组件名，可以在注册时指定一个自定义名称：

```cpp
// 将 VendorWaveformGraph 以 WaveformGraph 注册，模板中写作 <waveform-graph>
kit.installWidget<VendorWaveformGraph>("WaveformGraph");
```

自定义名称要使用**大驼峰（PascalCase）**形式，与 C++ 类名风格一致。

### C++ ↔ UX 命名转换

组件标签名对应注册时的名称（默认为 `GX_OBJECT` 声明的**类名**，或注册时指定的自定义名称）。模板里习惯用短横线（kebab-case）书写，**ux 打包工具在编译期负责名称转换**：

- 标签名：模板中的 kebab-case ↔ 注册名的大驼峰（PascalCase）。如 `<progress-ring>` 对应类 `ProgressRing`。自定义注册名也如此。
- 属性名：模板中的 kebab-case ↔ C++ 中的 camelCase。如 `ring-color` 对应属性 `ringColor`。

也就是说，运行时框架按 C++ 中声明的原始名称（camelCase / PascalCase）精确匹配，而短横线写法只是模板侧的书写习惯，由 ux 工具转换后对接。

ux 组件中也可以使用与 C++ 相同的标签 PascalCase 和属性 camelCase，参见[组件命名规范](/tutorials/name-spec.md)。

## 属性和事件导出

`GX_PROPERTY` 声明的属性会被自动导出，规则如下：

- 属性名即框架组件中的属性名，二者直接对应
- 声明了 setter 的属性（`set xxx`）可以被应用赋值
- 声明了 getter 的属性（`get xxx`）可以被应用读取
- 声明了 signal（`signal xxxChanged`）时，属性变化的信号会被传递给绑定

例如以下完整的属性声明：

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
    GX_PROPERTY(Color ringColor, get ringColor, set setRingColor)
    GX_PROPERTY(bool showLabel, get showLabel, set setShowLabel)
    // ...
};
```

在应用层对应的用法：

```xml
<progress-ring
  :value="jobProgress"
  ring-color="#409EFF"
  :show-label="true">
</progress-ring>
```

模板里属性以短横线（kebab-case）书写，对应 C++ 中的 camelCase 属性名：`ring-color` → `ringColor`，`show-label` → `showLabel`（转换由 ux 打包工具完成，见上文）。`:value`、`:show-label` 是动态绑定（值为表达式），而 `ring-color="#409EFF"` 这样的字面量则是静态赋值。

### 事件导出

组件事件是通过**带变化信号的属性**导出的，而不是直接导出 `Signal<>` 成员。导出一个事件需要两步：

1. 声明一个 `Signal<...>` 成员（C++ 内部使用）；
2. 在某个 `GX_PROPERTY` 的 `signal` 字段中引用它。

关键规则是：应用侧监听的事件名是**属性名**，而**不是**信号成员的名字。

### 带值的属性变化事件

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    int value() const;
    void setValue(int v);

    Signal<int> valueChanged;   // 内部信号，这个名字对应用不可见
    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
};
```

应用侧用 `@属性名` 监听变化，因此这里写 `@value`（属性名），而**不是** `@value-changed`：尽管信号成员叫 `valueChanged`，应用看到的事件名始终是属性名 `value`。

```xml
<progress-ring :value="progress" @value="onProgressChanged"></progress-ring>
```

这一点和框架内置控件完全一致。例如 `Slider` 的值变化信号成员叫 `changed`，但应用侧监听的仍是属性名 `value`（`@value` 或双向绑定 `::value`）。

### 无值的纯事件

对于不携带数值、只表示“某件事发生了”的事件（如“完成”），用 `invalid_t` 作为属性类型声明一个只有信号、没有读写值的属性：

```cpp
Signal<>  completed;   // 进度完成时发射
GX_PROPERTY(invalid_t completed, signal completed)
```

应用侧可以这样监听（没有事件值）：

```xml
<progress-ring @completed="onDone"></progress-ring>
```

你无法将一个 `GX_PROPERTY` 声明为 `void` 类型，即便它根本没有 `get`/`set`，因此要用 `invalid_t` 作为占位类型。如果你希望事件携带值，必须声明为一个具体类型，并提供 `get` 方法——`Signal<T>` 的参数类型不会自动成为事件值，而是始终来自属性的 getter。

::: warning `Signal<>` 不会自动成为事件
只声明一个 `Signal<>` 成员、却不在任何 `GX_PROPERTY` 中用 `signal` 字段引用它，这个信号是**无法**在应用侧用 `@some-event` 监听的。框架只会把“属性的变化信号”，也就是 `signal` 字段暴露为事件，事件名始终来自属性名。
:::

## 方法导出

用 `GX_METHOD` 声明的成员函数会作为组件方法导出，供应用在 JavaScript 中调用：

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    GX_METHOD void reset();               // 无参方法
    GX_METHOD void animateTo(int target); // 带参方法
};
```

与属性、事件不同，方法不通过模板标签使用，而是先用 [`$element()`](../framework/component/component-apis.md#element) 取得原生组件对象，再在其上调用。对应模板需要给组件设置 `id`：

```xml
<progress-ring id="ring" :value="progress"/>
```

```js
onReady() {
  const ring = this.$element('ring'); // 'ring' 为模板中组件的 id
  ring.reset();
  ring.animateTo(80);
}
```

方法的参数与返回值由框架经 `Variant` 自动编组，无需手写转换代码（类型桥接的细节见[对象系统](./object-system.md#运行时类型系统)）。注意 `$element()` 须在 [`onReady()`](../framework/component/life-cycle.md#onready) 生命周期及之后调用，详见[原生组件](../framework/component/native-component.md)。

## 枚举与结构体类型

当属性或方法参数的类型是自定义的 C++ 枚举或结构体时，用 `GX_ENUM` / `GX_STRUCT` 标注即可一并导出，[注册控件](#注册控件)时框架会自动安装相应的类型转换，无需手写绑定代码。枚举在 JavaScript 侧表现为字符串常量，结构体表现为对象字面量：

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    // 注意为值定义别名，否则 JavaScript 侧会使用
    // 'Solid' / 'Dashed' 名称，而不是预期的 'solid' / 'dashed'
    enum GX_ENUM LineStyle {
        Solid GX_ALIAS("solid") = 0,
        Dashed GX_ALIAS("dashed"),
    };
    // 结构体注意写默认值，以免在 JavaScript 侧创建时出现未定义字段
    struct GX_STRUCT Range { int min = 0; int max = 100; };

    GX_METHOD void setRange(const Range &range);

    GX_PROPERTY(LineStyle lineStyle, get lineStyle, set setLineStyle)
};
```

```xml
<progress-ring line-style="dashed"/>
```

```js
this.$element('ring').setRange({ min: 0, max: 100 });
```

枚举别名、结构体字段映射、嵌套类型等完整语义见[对象系统 · 复杂类型反射](./object-system.md#复杂类型反射)，此处不再展开。

::: warning 不要遗忘标注
属性或方法用到自定义枚举/结构体时，务必标注 `GX_ENUM` / `GX_STRUCT`，否则 JavaScript 侧无法使用，且没有任何编译错误提示。
:::

## 容纳子控件（容器型控件）

如果控件需要容纳应用声明的子内容，只需把它实现为一个**容器型控件**：在 C++ 侧负责子控件的布局，框架会自动把模板里嵌套声明的子组件创建为子控件并挂载到它下面。Glyphix 没有 HTML 那样的具名插槽（slot），模板中嵌套的标签会直接成为该控件的子控件。

容器的布局有两种实现方式（详见[控件开发指南](./widget.md)的「布局与尺寸」一节）：

- 使用框架现成的布局类，例如在构造函数中 `setLayout(new FlexLayout())`；
- 或覆写 `layoutEvent()`，在其中遍历 `children()` 手动设置每个子控件的几何。

在应用层，像嵌套子标签一样使用即可（这里 `card-panel` 是开发者实现并注册的容器控件，`text` 为内置控件）：

```xml
<card-panel>
  <text>标题</text>
  <progress-ring :value="progress"/>
</card-panel>
```

## 一个完整的例子

以下定义一个简单的数字显示控件，并将其注册为框架组件：

```cpp
// number_display.h
#pragma once
#include "gx_widget.h"
#include "gx_color.h"

class NumberDisplay : public Widget {
    GX_OBJECT
public:
    explicit NumberDisplay(Widget *parent = nullptr);

    int value() const { return m_value; }
    Color textColor() const { return m_color; }

    void setValue(int v);
    void setTextColor(const Color &c);

    bool event(Event *event) override;   // 唯一需要覆写的虚函数

    Signal<int> valueChanged;            // 内部信号；应用侧通过属性名 value 监听

    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
    GX_PROPERTY(Color textColor, get textColor, set setTextColor)

protected:
    // paintEvent / sizeHint 都不是虚函数，不能加 override
    void paintEvent(PaintEvent *event);
    Size sizeHint() const;

    // EventDispatch 需要访问 protected 处理函数
    friend struct EventTraits<NumberDisplay>;

private:
    int m_value = 0;
    Color m_color{0, 0, 0};
};
```

```cpp
// number_display.cpp
#include "number_display.h"
#include "gx_format.h"
#include "gx_painter.h"
#include "gx_widgetevent.h"   // EventDispatch

NumberDisplay::NumberDisplay(Widget *parent)
    : Widget(parent) {}

bool NumberDisplay::event(Event *event) {
    // 把事件分发给 paintEvent；声明 PaintEvent 可在编译期检查遗漏
    return EventDispatch<Widget, PaintEvent>{}(this, event);
}

void NumberDisplay::setValue(int v) {
    if (m_value == v) return;
    m_value = v;
    update();
    valueChanged(v);
}

void NumberDisplay::setTextColor(const Color &c) {
    if (m_color == c) return;
    m_color = c;
    update();
}

Size NumberDisplay::sizeHint() const {
    return Size(60, 30);
}

void NumberDisplay::paintEvent(PaintEvent *) {
    Painter p(this);
    p.setBrush(m_color);   // 文本颜色由画刷（Brush）决定，而非画笔
    p.setFont(Font(20));
    p.drawText(rect(), format("{}", m_value), AlignCenter);
}
```

注册：

```cpp
kit.installWidget<NumberDisplay>();
```

应用层使用：

```xml
<number-display
  :value="count"
  text-color="#333333"
  @value="onCountChanged">
</number-display>
```

至此，从 C++ 实现到应用使用，整个流程完整：`<number-display>` 标签经 ux 工具转换为注册名 `NumberDisplay` 而被识别。

每当应用数据 `count` 变化时，`:value` 绑定会调用 `NumberDisplay::setValue()`；当控件内部发射 `valueChanged` 信号时，框架触发名为 `value` 的事件（事件名取属性名），从而调用应用的 `onCountChanged`。若希望 `count` 与控件双向同步，可改用 `::value="count"`。
