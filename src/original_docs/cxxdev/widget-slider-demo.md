# 自定义 Widget 实战

`slider-demo` 是 Glyphix SDK 附带的一个完整示例，展示了如何用 C++ 从头实现一个**定制控件**：`WaveSlider`。这个控件在标准 `Slider` 的基础上增加了水波纹填充效果和点击涟漪动效，同时示例还涉及 `StyleEngine` 定制、直接用 C++ 构建 UI 界面等内容。

本文以此示例为线索，结合[控件开发指南](./widget.md)中的核心概念，完整地演示定制一个新 Widget 所需的全部步骤。

## 示例结构

示例的文件结构如下：

```
app/slider-demo/
├── CMakeLists.txt
├── main.cpp           # 应用入口，用 C++ 直接构建 UI
├── styleengine.h/.cpp # 定制 StyleEngine
└── waveslider.h/.cpp  # WaveSlider 控件的实现
```

直接编译运行 `slider-demo` 目标即可看到效果，无需配合前端项目。

### 构建说明

[配置好 SDK](sdk-setup.md#准备工作) 后，使用以下命令构建并运行示例：

```bash
mkdir build && cd build
cmake .. && cmake --build . -j
bin/slider-demo
```

::: important 宿主系统
必须在支持桌面环境的 Linux 系统上构建和运行此示例。
:::

## 用 C++ 直接构建 UI

在 `main.cpp` 中，应用的 UI 完全在构造函数中用 C++ 代码搭建，风格类似 Qt Widgets 或 LVGL：通过 `new` 创建子控件并传入父控件指针，无需声明式模板。

```cpp
int main() {
    Application app(new BSPPlatform(500, 500));
    app.setFont(Font(GX_EXAMPLE_ASSETS "/roboto.ttf", 32));
    app.setStyleEngine(new MyStyleEngine);

    Window window;
    window.setFlowLayout(true);

    MyWidget widget(&window);
    StyleModifier(&widget)->setSize(
      Length::fromPercent(100), Length::fromPercent(100));
    StyleModifier(&widget)->setMargin(Margin(10));
    return app.exec();
}
```

`Application` 接收一个平台后端对象（`BSPPlatform`）和分辨率。`Window` 是根控件，启用 `setFlowLayout(true)` 后，其子控件将按照流式布局自动排列。

`setStyleEngine` 挂载自定义的样式引擎，这不是必须的（否则使用默认样式）。只有当你需要定制控件外观（如下文中对 `Switch` 的改造）时才需要提供自己的实现。

### `MyWidget` 类

`MyWidget` 继承 `ScrollArea`，在构造函数中创建并添加子控件：

```cpp
class MyWidget : public ScrollArea {
public:
    explicit MyWidget(Widget *parent = nullptr) : ScrollArea(parent) {
        addItem(&m_switch);
        addItem(&m_label);
        addItem(&m_slider);
        // ...
    }
    // ...
private:
    Label  m_label;
    Switch m_switch;
    Slider m_slider;
};
```

子控件作为成员变量声明，构造时自动初始化（父控件在 `addItem` 中建立）。成员变量的生命周期由 `MyWidget` 管理，无需手动 `delete`。

`ScrollArea` 提供开箱即用的滚动、惯性、回弹等能力，`MyWidget` 不需要手写任何滚动逻辑。

::: tip `addItem()` 的作用
一般情况下，可以直接将子控件通过 `setParent()` 挂到父控件上，但 `ScrollArea` 内部实际上还有一个专门的内容容器（`contentWidget()`），普通元素不能直接添加到 `ScrollArea` 上，而是要通过 `addItem()` 添加到内容容器中。

对于简单的容器，`setParent()` 和 `addItem()` 的效果相同；但对于 `ScrollArea` 这类特殊容器，则**必须**使用 `addItem()` 添加元素。
:::

### 信号连接

控件之间通过信号连接同步状态：

```cpp
m_slider.changed.connect(this, &MyWidget::onSlider);
m_switch.checked.connect(this, &MyWidget::onSwitch);

// 双向同步两个 Slider 的值
waveSlider->changed.connect<AbstractSlider>(&m_slider, &Slider::setValue);
m_slider.changed.connect<AbstractSlider>(waveSlider, &WaveSlider::setValue);

// 开关切换 WaveSlider 的波形模式
m_switch.checked.connect(waveSlider, &WaveSlider::setWaveMode);
```

::: tip Signal 用法
信号连接的语法是 `signal.connect(receiver, &Type::method)`。当 `Slider::setValue` 和 `WaveSlider::setValue` 签名不完全一致时，可以通过模板参数声明公共基类（`AbstractSlider`）来消歧义。

当你不确定某个槽函数的实际所属类型时，可以通过 IDE 提示来检查，例如检查 `Slider::setValue` 时，IDE 通常会提示：
```cpp
public method
void setValue(int value) in class AbstractSlider 
```
这说明 `setValue` 实际上是声明在 `AbstractSlider` 中的。在连接时就需要指定 `AbstractSlider` 以消除歧义：
```cpp
m_slider.changed.connect<AbstractSlider>(waveSlider, &WaveSlider::setValue);
```
:::

### 用 StyleModifier 设置样式

`StyleModifier` 是在 C++ 中以编程方式设置控件样式的工具，效果等价于在模板中通过样式属性配置：

```cpp
StyleModifier m(waveSlider);
m->setSize(120, 300);
m->setMargin(Style::Margin{Length::fromAuto(), 20});
m->setColor(Color{"#35a7ff"});
```

`setColor` 为 `WaveSlider` 设置前景颜色，它会被 `paintEvent` 中读取并用于绘制进度填充色。

## 定制 StyleEngine

内置的 [`Switch`](/components/switch.md) 是一个功能完整的开关控件，但其默认外观类似 [Fluent 2](https://fluent2.microsoft.design/components/web/react/core/switch/usage)，可能不适合特定设备或品牌的视觉风格。

`StyleEngine` 是解决这个问题的机制。设备厂商可以实现自己的 `StyleEngine`，定制所有内置控件的外观，同时保留它们的交互逻辑，无需修改框架代码。

定制后的 `Switch` 不仅仅是换了主题颜色，相反，整套开关动效（滑块位移、颜色过渡、按压缩放）均可以通过**程序化插值**实现，而非预录序列帧图片。这意味着：

- 动效完全流畅，帧率与渲染系统一致；
- 颜色、尺寸可以被应用开发者通过样式属性覆盖，`StyleEngine` 提供的是可被覆盖的默认值；
- 无需为每种分辨率准备不同的图片素材。

### `StyleEngine` 的职责

`StyleEngine` 是 Glyphix 样式系统的核心，负责三件事：

1. **提供调色板**（palette）：全局颜色变量，类似 CSS 自定义属性，供所有内置控件和自定义控件读取。
2. **绘制控件外观**（paint）：框架内置控件（如 `Switch`、`Slider`）的视觉效果全部委托给 `StyleEngine::paint()` 绘制，开发者可以在派生类中重写，实现完全不同的外观。
3. **推荐尺寸**（size hint）：控件在不同样式状态下的推荐尺寸，供布局系统参考。

### 定义 MyStyleEngine

继承 `StyleEngine` 并重写 `sizeHint()` 和 `paint()`：

```cpp
class MyStyleEngine : public StyleEngine {
public:
    MyStyleEngine();
    Size sizeHint(StyleOption::Type type, const Widget *widget) const override;
    void paint(Painter &painter, Widget *widget, StyleOption &option) override;
};
```

构造函数中设置调色板：

```cpp
MyStyleEngine::MyStyleEngine() {
    setPalette(SwitchDark,  Color(0xff565656));
    setPalette(SwitchLight, Color(0xff2f5cff));
    setPalette(SwitchThumb, Color(0xffffffff));
}
```

`SwitchDark`、`SwitchLight`、`SwitchThumb` 是 `StyleEngine` 枚举中预定义的语义颜色键。不同的主题引擎可以赋予它们不同的颜色，控件始终通过键名读取而不是硬编码颜色值。

### 重写 `sizeHint()`

`sizeHint()` 告知框架内置控件在给定样式状态下的**推荐尺寸**。以 `Switch` 为例，其宽高应与字体像素大小成比例：

```cpp
Size MyStyleEngine::sizeHint(StyleOption::Type type, const Widget *widget) const {
    // 定制的 Switch 尺寸比例可以与内置策略不同
    if (type == StyleOption::OptionSwitch) {
        float f = widget->font().pixelSize();
        int d = int(round(f));
        return {int(round(f * SwitchAspectRatio)), d};
    }
    return StyleEngine::sizeHint(type, widget); // 其余类型交给基类
}
```

在函数末尾务必调用 `StyleEngine::sizeHint(type, widget)` 回退到默认实现，否则其他类型的控件会得到零尺寸。

### 重写 `paint()`

`paint()` 通过 `StyleOption` 的 `option()` 类型分发到对应的绘制逻辑，未处理的类型同样要回退：

```cpp
void MyStyleEngine::paint(Painter &painter, Widget *widget, StyleOption &option) {
    switch (option.option()) {
    case StyleOption::OptionSwitch:
        drawSwitch(this, painter, widget, static_cast<StyleOptionSwitch &>(option));
        break;
    default:
        StyleEngine::paint(painter, widget, option);
    }
}
```

`StyleOptionSwitch` 是 `StyleOption` 的派生类，添加了 Switch 特有的状态字段。它携带了两个关键的动画进度值：

- `option.transition`：Switch 开关过渡进度，`0.0` 为关闭状态，`1.0` 为打开状态，中间值表示动画进行中。
- `option.scale`：按下时的缩放系数，用于绘制按压反馈效果。

利用这两个值可以在 `drawSwitch` 中实现平滑的状态过渡：

```cpp
// 在打开和关闭颜色之间插值
color = color.blend(checked.background().color(), option.transition);

// thumb 指示器的位置随过渡进度移动
float pos = option.transition * (box.width() - size - len);
```

`StyleEngine` 负责动画的驱动，开发者只需在 `paint()` 中根据进度值插值，即可得到完整的过渡动效。

::: tip 仅定制部分控件
默认的 `StyleEngine` 实现了所有内置控件的绘制逻辑，其中一部分相当复杂。如果你只对其中一部分控件的外观不满意，应当在派生类中仅重写这些控件的绘制逻辑，其他控件直接回退到基类实现。

应优先考虑通过调色板来满足定制颜色，只有在需要完全不同的视觉效果时才重写 `paint()`。
:::

### VectorPath 绘制圆角胶囊形

默认的 `Switch` 的背景和 thumb 都是圆角胶囊形状。示例中使用 `VectorPath` 配合两段圆弧来绘制，这是一种比 `drawRoundedRect` 更灵活的方式，适合需要对两端分别控制弧度的场景：

```cpp
static void indicatorBar(Painter &p, const RectF &rect) {
    float radius = rect.height() * 0.5f;
    float x1 = rect.left() + radius;
    float x2 = rect.right() - radius;
    float y = rect.top() + radius;
    VectorPath path;
    path.arcTo(PointF(x1, y), radius, radius, 90, 270);   // 左端半圆
    path.arcTo(PointF(x2, y), radius, radius, -90, 90);   // 右端半圆
    p.fillPath(path);
}
```

两段圆弧首尾相接，`arcTo` 在路径中自动连线，无需额外 `lineTo`。

## WaveSlider：自定义控件完整实践

`WaveSlider` 是本示例的核心，展示了定制控件的完整开发流程。与上文中的 `StyleEngine` 定制类似，`WaveSlider` 的设计目标也是在不破坏已有能力的前提下**叠加**新的视觉效果：

- **波浪填充**模式：进度区域以动态波浪填充，而不是普通的矩形进度条；
- **点击涟漪**效果：按下时产生扩散振荡，使波浪短暂增强再恢复；
- **`waveMode` 属性**：可在运行时切换波形模式和普通模式，并支持应用层绑定和属性动画；
- **完整回退兼容**：波形模式关闭时，`WaveSlider` 直接调用 `Slider::paintEvent()` 回退到默认外观，复用父类的拖拽、`value`/`changed` 等全部能力，应用侧无需改动任何代码。

### 类定义与继承

`WaveSlider` 继承自 `Slider`（而非直接继承 `Widget`），可以复用 `Slider` 已有的手势拖拽逻辑、`value`/`minimum`/`maximum` 等属性，以及 `changed` 信号：

```cpp
// waveslider.h
#include "gx_slider.h"
#include "gx_valueanimation.h"

class WaveSlider : public Slider {
    GX_OBJECT
public:
    explicit WaveSlider(Widget *parent = nullptr);
    ~WaveSlider() override = default;

    GX_NODISCARD bool isWaveMode() const { return m_waveMode; }
    void setWaveMode(bool enabled);
    bool event(Event *event) override;

    GX_PROPERTY(bool waveMode, get isWaveMode, set setWaveMode)
    // ...
};
```

`GX_OBJECT` 必须放在类定义最开始，它触发元对象编译器为此类生成元数据。`GX_PROPERTY` 将 `waveMode` 暴露给属性系统，使其可被应用层绑定（如 `<wave-slider :wave-mode="enabled"/>`）和属性动画驱动。

### 成员变量

控件的运行时状态保存在成员变量中：

```cpp
private:
    bool  m_waveMode = false;       // 当前是否为波形模式
    float m_rippleProgress = 1.0f;  // 涟漪进度 [0, 1]，初始为 1（表示未激活）
    float m_waveOffset = 0.0f;      // 波形相位偏移 [0, 1]，由动画驱动
    ValueAnimation<float> m_animation;        // 波浪循环动画
    ValueAnimation<float> m_rippleAnimation;  // 涟漪动画
    friend struct EventTraits<WaveSlider>;    // 允许事件分发访问 protected 方法
```

`ValueAnimation<float>` 直接作为成员变量（而非指针），生命周期由 `WaveSlider` 管理，无需手动 `delete`。

### 构造函数：初始化动画

构造函数配置两个动画并设置方向：

```cpp
WaveSlider::WaveSlider(Widget *parent) : Slider(parent) {
    // 波浪动画：无限循环，每秒一个完整周期
    m_animation.setRepeat(AbstractAnimation::Infinity);
    m_animation.setValueLimits(0.f, 1.f);
    m_animation.setDuration(1000);
    m_animation.value.connect(this, &WaveSlider::onWaveAnimation);
    m_animation.start();

    // 涟漪动画：按下时一次性播放，持续 800ms
    m_rippleAnimation.setValueLimits(0.f, 1.f);
    m_rippleAnimation.setDuration(800);
    m_rippleAnimation.value.connect(this, &WaveSlider::onRippleAnimation);

    setVertical(true);  // 竖向滑动条
}
```

`m_animation` 在启动后一直运行，每帧将 `m_waveOffset` 从 $0$ 推进到 $1$，再循环回 $0$。这个值最终转换为波形的相位偏移，使波浪持续流动。

`m_rippleAnimation` 仅在按下时触发，播放一遍即停止，不设置 `Infinity`。两个动画的回调分别只做一件事：更新状态变量并调用 `update()` 请求重绘。

```cpp
void WaveSlider::onWaveAnimation(float value) {
    m_waveOffset = value;
    update();
}
void WaveSlider::onRippleAnimation(float value) {
    m_rippleProgress = value;
    update();
}
```

### 事件处理

#### 配置 EventDispatch

`event()` 中使用 [`EventDispatch`](widget.md#处理事件) 路由事件，模板参数列出了当前控件实际处理的事件类型，起到编译期检查的作用：

```cpp
bool WaveSlider::event(Event *event) {
    return EventDispatch<Widget,
        GestureEvent, PaintEvent>{}(this, event);
}
```

#### 处理手势：触发涟漪

`gestureEvent()` 拦截 `Press` 手势的开始时刻来触发涟漪，其余情况委托给 `Slider` 的手势处理（实现拖拽调值）：

```cpp
bool WaveSlider::gestureEvent(GestureEvent *event) {
    if (!event->isHitTest() && event->gesture()->type() == Gesture::Press) {
        auto g = static_cast<PressGesture *>(event->gesture());
        if (g->isStarted())
            startRipple(g->clientPoint());
    }
    return Slider::gestureEvent(event); // 将事件继续交给 Slider 处理
}

void WaveSlider::startRipple(const Point &) {
    m_rippleProgress = 0.f;      // 从头开始
    m_rippleAnimation.start();   // 重新播放
}
```

`isHitTest()` 为 `true` 时表示这是一次命中测试（框架用于检测事件是否应该落在此控件上），不代表真正的用户交互，应跳过。

::: tip 关于 `isHitTest()`
命中测试是事件分发的前置步骤，`gestureEvent()` 在命中测试阶段也会被调用，但此时不应有任何副作用（如启动动画）。永远先判断 `!event->isHitTest()` 再处理交互逻辑。
:::

#### 样式读取接口

`paintEvent()` 中会读取控件对应的样式数据，这里先介绍两个涉及的接口：

- `style()` / `style(Styles::Xxx)` 返回当前控件某个样式伪类的 `Style` 对象，可以从中读取颜色、背景等属性；
- `se->palette(StyleEngine::Xxx)` 从 `StyleEngine` 读取全局调色板颜色，当控件未设置自定义颜色时作为默认值。

两者配合实现“有自定义配置时用自定义颜色，否则回退到主题默认色”的逻辑：

```cpp
auto contentStyle = style(Styles::Content);
p.setBrush(contentStyle.hasProperty(style::Background)
               ? contentStyle.background()
               : se->palette(StyleEngine::ProgressRange));
```

### 绘制实现

`paintEvent()` 是 WaveSlider 的核心。根据 `m_waveMode` 决定走哪条绘制路径：

```cpp
void WaveSlider::paintEvent(PaintEvent *event) {
    discard(event);  // PaintEvent 本身不携带有用信息，明确丢弃以消除编译警告

    if (!isWaveMode())
        return Slider::paintEvent(event);  // 普通模式：直接调用父类绘制

    auto se = App()->styleEngine();
    RectF box = rect();
    float radius = min(box.width(), box.height()) * 0.5f;
    float progress = sliderRange ? float(value() - minimum()) / float(sliderRange) : 0.f;

    Painter p(this);

    // 绘制背景（空轨道）
    p.setBrush(/* 背景色 */);
    p.fillRoundedRect(box, radius);

    // 绘制波浪填充（进度区域）
    p.setBrush(/* 前景色 */);
    VectorPath path;
    buildWaveFillPath(path, box, radius, progress, m_waveOffset, m_rippleProgress);
    if (!path.isEmpty())
        p.fillPath(path);
}
```

整个绘制分两步：先用 `fillRoundedRect` 画出完整的背景圆角矩形，再用 `fillPath` 在其上方画出波形填充，两层叠加形成“有波纹的进度条”。

#### 波形路径生成

`buildWaveFillPath()` 是一个独立的辅助函数（不在类内），负责在给定几何约束下构造波形路径：

```cpp
static void buildWaveFillPath(VectorPath &path, const RectF &box, float radius,
                              float progress, float waveOffset, float rippleProgress)
```

其核心逻辑分三步：

1. **计算水位和振幅**：`waterLevel` 从底部按 `progress` 比例上升；振幅取决于宽高比例，并被限制在离顶底圆弧足够远的范围内，避免波形越界。
2. **采样波形**：从左到右均匀采样，对每个 $x$ 坐标计算 $y$ 值。
   波形由三部分叠加：常规正弦波（`m_waveOffset` 控制相位）+ 涟漪增益（`m_rippleProgress` 控制衰减振荡）+ 圆角约束（确保路径不超出圆角矩形的边界）。
3. **封闭路径**：从波形顶部到圆角矩形底部沿底边返回，形成封闭多边形，供 `fillPath` 填充。

算法细节属于教学性质的效果演示，实际产品中可以根据设计需求替换为任意自定义的路径生成逻辑。

::: tip 路径绘制的效率
采样点数量（`sampleCount`）与控件宽度成正比（约每 `4px` 一个点），在典型屏幕分辨率下性能消耗可以接受。如果 CPU 较弱，可以降低采样密度或换用贝塞尔曲线近似。
:::

### waveMode 属性

`setWaveMode()` 的实现很简单：状态变化时更新成员值并标记重绘：

```cpp
void WaveSlider::setWaveMode(bool enabled) {
    if (m_waveMode != enabled) {
        m_waveMode = enabled;
        update();
    }
}
```

`GX_PROPERTY` 宏的声明使 `waveMode` 成为框架可见属性：

```cpp
GX_PROPERTY(bool waveMode, get isWaveMode, set setWaveMode)
```

此处没有声明 `signal` 字段，因为它通常由使用方驱动值变化，而非交互触发。

### 生产级优化

`WaveSlider` 的实现主要面向教学演示，并缺少一些优化，例如：
- 波形动画始终播放，即使 `waveMode` 关闭时也在 `update()`，这会反复触发 `paintEvent()`；
- 仅支持竖向滑动条，未对水平模式进行适配（按产品需求自行决定）；
- 固定绘制胶囊形轨道，实际产品可能需要使用圆角矩形或其他形状。

## 各部分协作关系

以下是 `slider-demo` 中各组件在运行时的协作关系：

```
用户按下屏幕
    ├─ WaveSlider::gestureEvent() 检测到 Press.isStarted()
    │       └─ startRipple() 重置 m_rippleProgress 并启动 m_rippleAnimation
    └─ Slider::gestureEvent() 继续处理，根据触点位置调整 value
            └─ changed 信号发射 → MyWidget::onSlider() 更新 Label 文字

每帧渲染循环
    ├─ m_animation 持续推进 m_waveOffset (0→1 循环)
    │       └─ update() → paintEvent() 用新 offset 重绘波形
    └─ m_rippleAnimation 推进 m_rippleProgress (0→1 播完停止)
            └─ update() → paintEvent() 用新 rippleProgress 重绘涟漪衰减

Switch 切换
    └─ waveSlider->setWaveMode(true/false)
            └─ update() → paintEvent() 切换为普通模式或波形模式
```

各信号连接在 `MyWidget` 的构造函数中一次性建立，之后运行时完全由事件和信号驱动，控件之间没有直接调用。

## 关键模式总结

通过 `slider-demo`，可以归纳出在 Glyphix 中实现定制控件的典型模式：

| 需求 | 做法 |
|---|---|
| 继承现有控件，复用其交互逻辑 | 继承对应基类（如 `Slider`），在 `EventDispatch` 中控制回退基类 |
| 自定义绘制 | 实现 `paintEvent()`，`isWaveMode()` 为 `false` 时调用 `Slider::paintEvent()` 回退 |
| 持续循环的动画 | `ValueAnimation::setRepeat(Infinity)` |
| 一次性触发动画 | 保存状态变量，在 `gestureEvent()` 中调用 `anim.start()` 重新播放 |
| 向应用层暴露属性 | `GX_PROPERTY` 宏，配合 getter/setter 和可选的信号 |
| 读取用户配色或主题色 | `style().hasProperty()` 检查后回退到 `se->palette()` |
| 自定义全局控件外观 | 继承 `StyleEngine`，重写 `paint()` 和 `sizeHint()` |

这些模式在[控件开发指南](widget.md)中均有详细阐述，`slider-demo` 是它们的综合实践。

## 与其他 GUI 框架的对比

::: important C++ 控件开发的定位
Glyphix 的主流开发方式是通过 [`.ux` 单文件组件](../tutorials/quick-orientation.md)以声明式模板构建界面。C++ 控件开发的用途是实现**设备端的底层控件库**（例如设备厂商定制的 `WaveSlider`），这些控件随后会被前端应用层通过模板和数据绑定使用。直接用 C++ 搭建完整 UI（如 `main.cpp` 中的示范）在框架中是**可以实现的，但并非推荐工作流**，相关工具链支持（调试、热更新、布局预览）也不如应用层完善。

因此，评估 Glyphix 的整体开发效率时，应以前端应用层为基准；本节讨论的 C++ 控件开发体验仅代表底层控件库的开发场景。
:::

Glyphix 的 C++ 控件开发在心智模型上更接近 Qt Widgets 而非 LVGL：信号机制、属性宏、继承式扩展、`paintEvent` 的命名和职责划分都与 Qt Widgets 基本对应，有 Qt 背景的开发者可以快速建立直觉。

LVGL 开发者则需要从 C 句柄风格向 C++ OOP 风格转换，差距相对更大，但控件树组织、`update()` 重绘触发等核心范式是共通的。本节以 `slider-demo` 为参照，具体说明各框架之间的相似之处与关键差异。

### 相似之处

无论是 Qt Widgets、LVGL 还是 Glyphix，它们共享一套经过验证的 UI 框架核心范式：

- **控件树**：UI 以父子树形结构组织，子控件的坐标相对于父控件。`MyWidget(&window)` 和 Qt 的 `new QWidget(&parent)`、LVGL 的 `lv_obj_create(parent)` 在语义上对应。
- **自定义绘制**：通过“覆写”绘制方法实现控件外观。Qt 重写 `paintEvent(QPaintEvent *)`，LVGL 注册 `LV_EVENT_DRAW_MAIN` 回调，Glyphix 实现 `paintEvent(PaintEvent *)`，三者设计思路一致。
- **信号/槽机制**：控件间通过信号传递状态变化，接收方以成员函数响应。
  - Glyphix：`m_slider.changed.connect(this, &MyWidget::onSlider)`；
  - Qt：`connect(&slider, &QSlider::valueChanged, this, &MyWidget::onSlider)`；
  - LVGL：通过事件回调函数实现类似功能。
- **继承复用**：扩展现有控件时通过继承实现。`WaveSlider : public Slider` 复用了父类的所有拖拽和取值逻辑，只重写绘制部分，与大部分 OOP GUI 框架的设计一致。
- **按需重绘**：状态变化时调用 `update()` 标记脏区，由框架在下一帧统一重绘，而非立即绘制。主流框架均采用此策略以避免帧内重复绘制。

### 与 Qt Widgets 的差异

#### 事件分发

Qt 通过虚函数重写来分发事件，每个事件方法都是 `virtual`，子类用 `override` 覆盖：

```cpp
// Qt
class MySlider : public QSlider {
    void paintEvent(QPaintEvent *event) override { ... }
    void mousePressEvent(QMouseEvent *event) override { ... }
};
```

Glyphix 的 `paintEvent()`、`gestureEvent()` 等事件处理函数**不是虚函数**，不能加 `override`，事件路由由 `EventDispatch` 在编译期完成：

```cpp
// Glyphix
bool WaveSlider::event(Event *event) {
    return EventDispatch<Widget, GestureEvent, PaintEvent>{}(this, event);
}
// paintEvent 和 gestureEvent 均为普通成员函数，无 override
```

这是为了避免了虚函数的间接跳转，在嵌入式设备的高频事件处理中有性能优势；同时模板参数列表起到编译期文档和漏项检查的作用。如果你声明了处理 `PaintEvent` 但忘记实现 `paintEvent()`，编译器会报错，而不是静默回退到基类。

#### 对象和属性系统

Qt 使用 `Q_PROPERTY` 宏配合 MOC（元对象编译器）生成属性元数据；Glyphix 使用 `GX_PROPERTY` 配合 `GX_OBJECT`，机制类似，但生成方式和运行时接口不同：

```cpp
// Qt
Q_PROPERTY(int value READ value WRITE setValue NOTIFY valueChanged)
// Glyphix
GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
```

两者都支持通过属性名字符串进行动画驱动（`QPropertyAnimation` / `PropertyAnimation`）。但在实现控件自身时，Glyphix 更推荐直接使用 `ValueAnimation<T>`，避免属性名查找的开销，并避免与应用层驱动的属性动画产生冲突。

#### 信号和槽

如[对象系统](object-system.html#信号-signal)描述，Glyphix 也有信号机制，但是它更接近 boost::signals2，不依赖 MOC 生成代码。这是有意为之的设计，因为 Glyphix 生态的[构建系统](sdk-setup.md#其他构建系统)较为碎片化，我们假设下游完全不使用元对象编译器。

#### 样式与外观定制

Qt 的控件外观定制有两条路：`QStyle` 子类化（较复杂）或 QSS 样式表（类 CSS 字符串，运行时解析）。Glyphix 使用 `StyleEngine`：厂商实现 `StyleEngine` 子类，在 `paint()` 中以 C++ 代码绘制全部内置控件的外观，在 `sizeHint()` 中提供推荐尺寸。这种方式适用于全局的系统级样式定制，而非单个控件的局部样式调整。

在单个控件的样式设置上，Glyphix 使用 `StyleModifier` 辅助对象以编程方式赋值，而不常用 CSS 字符串：

```cpp
StyleModifier m(waveSlider);
m->setSize(120, 300);
m->setColor(Color{"#35a7ff"});

// 也支持 inline style 字符串
waveSlider->setStyle(Style{"background-color: #35a7ff; color: #cce;"});
```

Glyphix 的样式和布局属性更多地通过样式属性来设置，而非直接调用控件方法。这是因为 C++ 主要定位于底层控件库开发，并不直接面向应用开发。

#### 内存与生命周期

Qt 的父子控件所有权模型下，`new QWidget(parent)` 后由父控件负责销毁子控件。Glyphix 同样支持这种模式（`new WaveSlider` 后 `addItem()`），也推荐将子控件声明为成员变量（如 `MyWidget` 中的 `m_label`、`m_slider`），生命周期随宿主对象自动管理，无需手动 `delete`，也不依赖父子树销毁机制。

### 与 LVGL 的差异

#### 编程模型

LVGL 是以 C 实现的框架，控件通过 `lv_obj_t *` 句柄操作，函数命名通常遵循 `lv_<类型>_<操作>()` 约定：

```c
// LVGL
lv_obj_t *slider = lv_slider_create(parent);
lv_slider_set_value(slider, 50, LV_ANIM_ON);
lv_obj_add_event_cb(slider, my_event_cb, LV_EVENT_VALUE_CHANGED, NULL);
```

Glyphix 是原生 C++ OOP 框架，方法通过对象调用，`this` 天然携带上下文：

```cpp
// Glyphix
auto *slider = new Slider(parent);
slider->setValue(50);
slider->changed.connect(this, &MyWidget::onSlider);
```

对 LVGL 开发者来说，这里的主要变化不是能力本身，而是表达方式：以前你是在对象句柄外部调用函数，现在则是在控件类内部组织状态、事件和绘制逻辑。类型系统也会在编译期帮助你避免一部分句柄类型误用。

#### 事件系统

LVGL 的事件处理通常通过单一回调函数接收多种事件，在回调内用 `lv_event_get_code()` 枚举分支：

```c
// LVGL
static void event_cb(lv_event_t *e) {
    lv_event_code_t code = lv_event_get_code(e);
    if (code == LV_EVENT_PRESSED) { ... }
    else if (code == LV_EVENT_VALUE_CHANGED) { ... }
}
```

Glyphix 则按事件类型分发到独立的处理函数，不同事件之间完全隔离，参数也各自携带类型正确的数据：

```cpp
// Glyphix
bool WaveSlider::gestureEvent(GestureEvent *event) { ... }
void WaveSlider::paintEvent(PaintEvent *event) { ... }
```

此外，Glyphix 的 `isHitTest()` 机制在 LVGL 中没有完全等价的对应物。LVGL 可以通过 `LV_EVENT_HIT_TEST` 处理相近问题，但通常仍需要在同一回调中自行分支。

::: tip Glyphix 内部的事件分发机制
`EventDispatch` 内部也是一个 switch-case 分发，但是我们不建议开发者手写 switch 分支，而是总是使用固定的 `EventDispatch<Widget, ...>{}(this, event)` 模式，方便代码审核。
:::

#### 动画

LVGL 的动画通过 `lv_anim_t` 结构体配置，目标值通过函数指针和 `void *` 用户数据传递：

```c
// LVGL
lv_anim_t a;
lv_anim_init(&a);
lv_anim_set_exec_cb(&a, anim_cb);
lv_anim_set_var(&a, obj);
lv_anim_set_values(&a, 0, 100);
lv_anim_set_time(&a, 800);
lv_anim_start(&a);
```

Glyphix 的 `ValueAnimation<T>` 通过模板参数在编译期确定插值类型，通过信号连接消除 `void *` 转型：

```cpp
// Glyphix
m_rippleAnimation.setValueLimits(0.f, 1.f);
m_rippleAnimation.setDuration(800);
m_rippleAnimation.value.connect(this, &WaveSlider::onRippleAnimation);
```

`ValueAnimation<T>` 内置了对 `Color`、`Point`、`Transform` 等复合类型的插值支持，而 LVGL 原生只支持整数范围，复合类型需要自行实现插值回调。

#### 矢量路径绘制

LVGL 的绘制 API 以矩形、弧形等基础图元为主，矢量路径支持（`lv_draw_vector`）是较新加入的能力，接口相对底层。Glyphix 的 `VectorPath` 是标准的路径构建接口，`moveTo`、`lineTo`、`arcTo`、`conicTo`、`cubicTo` 完整覆盖常见曲线类型，`WaveSlider` 中的波形即完全依赖此接口实现，无需引入额外的图形库。

#### 内存与生命周期

两者都支持对象树管理：子控件挂在父控件下，父对象销毁时子对象也会一起销毁。

Glyphix 还可以把子控件、动画和运行时状态直接写成类成员，交给 C++ 的 RAII 自动管理。例如 `MyWidget` 中的 `m_label`、`m_slider`，以及 `WaveSlider` 中的两个 `ValueAnimation<float>`，都可以随宿主对象构造和析构，而不必像 LVGL 那样主要围绕句柄、`user_data` 和回调上下文来组织状态。
