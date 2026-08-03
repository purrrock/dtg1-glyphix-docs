---
headerDepth: 2
---
# 控件开发指南

在 Glyphix 中，所有可见的 UI 元素都是 `Widget`（控件）。框架内置了按钮、标签、图片、滚动区域等常用控件，但设备厂商往往需要根据自己的产品特色开发定制化的控件。例如，智能手表可能因为较小的圆形屏幕而定制特殊的列表动效，仪表设备则需要定制专门的图表控件。这篇文档介绍如何用 C++ 实现一个新控件。

## 控件基础

`Widget` 是一个矩形区域，它有位置、大小、可见性、透明度等基本属性，可以接收事件，并负责绘制自身的内容。控件以树形结构组织：一个父控件包含若干子控件，子控件的坐标相对于父控件。

每个控件都有一个**逻辑更新周期**：当控件的状态发生变化（例如数据更新了），调用 `update()` 标记为"需要重绘"，框架会在下一个渲染帧统一重绘所有已标记的控件，而不是立即重绘——这避免了同一帧内多次重复绘制。

### 控件与组件系统

UI 控件通常实现为一个 C++ 类，继承自 `Widget`，并符合标准的 C++ 面向对象设计。Glyphix 的响应式框架和组件系统则支持将这些 C++ 控件直接暴露为原生组件，并以模板化、声明式的方式来使用。

这种设计使得 C++ 侧的控件开发和前端组件使用可以相对独立，并保持双方习惯的开发方式。例如，在 C++ 中，你可以使用类似 LVGL 或者 Qt Widgets 的方式来构建界面，而完全不需要接受前端框架流行的声明式风格。

### 与其他框架的对比

Glyphix 控件系统在设计上类似于 Qt Widgets 或 LVGL 等传统 C/C++ UI 框架。所以你会发现开发一个新控件的方式和知识体系与这些框架非常相似：
- 通过继承 `Widget` 来创建新控件类；
- 存在布局系统、事件系统、绘制系统等核心机制；
- 通过属性系统和信号机制实现数据绑定和事件通知；
- 具有坐标系、尺寸等几何概念，并且支持嵌套的控件树结构。

::: tip 不建议使用 C++ 控件开发 UI
Glyphix 的设计初衷并非直接在 C++ 侧开发 UI，因此我们不会提供相关的文档和示例。
:::

## 创建自定义控件

本节以一个环形进度条控件（`ProgressRing`）为例，逐步说明开发一个自定义控件所需的各个要素。

::: tip 控件综合示例
SDK 附带的 [slider-demo](./widget-slider-demo.md) 示例是本文档所有知识点的完整实践，包括继承现有控件、绘制、事件处理、属性声明、`ValueAnimation` 动画，以及 `StyleEngine` 定制。建议在阅读完本文档后参阅。
:::

### 定义控件类

新建一个控件，继承 `Widget`，在类定义最开始加上 `GX_OBJECT` 宏，并**覆写 `event()`** 虚函数作为事件处理的入口：

```cpp
// progressring.h
#include "gx_widget.h"

class ProgressRing : public Widget {
    GX_OBJECT
public:
    explicit ProgressRing(Widget *parent = nullptr)
        : Widget(parent), m_value(0) {}

    int value() const { return m_value; }
    void setValue(int v);
    bool event(Event *event) override;

    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
    Signal<int> valueChanged;

protected:
    void paintEvent(PaintEvent *event);

    // EventDispatch 需要访问 protected 方法，声明友元
    friend struct EventTraits<ProgressRing>;

private:
    int m_value;  // [0, 100]
};
```

`GX_OBJECT` 是必不可少的，它触发元对象编译器为此类生成元数据，使控件可以被框架的属性系统、动画系统和组件系统正确感知（详见[对象系统](./object-system.md)）。

### 绘制控件

在 `.cpp` 文件中包含 `gx_widgetevent.h`，实现 `event()` 和 `paintEvent()`：

```cpp
// progressring.cpp
#include "progressring.h"
#include "gx_widgetevent.h"

bool ProgressRing::event(Event *event) {
    return EventDispatch<Widget>{}(this, event);
}

void ProgressRing::paintEvent(PaintEvent *event) {
    Widget::paintEvent(event);
    Painter p(this);
    // ... 详见绘制章节
}
```

自定义绘制通过实现 `paintEvent()` 完成；构造 `Painter` 时传入 `this` 指针，即可获得与当前控件关联的绘图上下文，然后调用各类绘制方法进行绘制。有关 `Painter` API 的完整说明，参见[绘制](./painting.md)章节。

### 处理事件

Glyphix 的事件系统**并不依赖虚函数继承**来分发事件，`paintEvent()`、`gestureEvent()` 等方法都不是 `virtual` 的，**不要**在声明时加 `override`（会编译报错）。框架通过 `EventDispatch` 在**编译期**按事件类型将调用路由到正确的处理函数。

唯一需要（也必须）覆写的虚函数是 **`event()`**，在其中委托给 `EventDispatch`：

```cpp
bool ProgressRing::event(Event *event) {
    return EventDispatch<Widget>{}(this, event);
}
```

`EventDispatch` 的第一个模板参数通常是**直接基类**（也就是 `ProgressRing` 继承的那个类，此处为 `Widget`）。它会在编译期检查当前类是否直接声明了对应的处理函数，有则调用，否则自动回退到基类实现。处理函数的返回值为 `bool` 时表示是否消费了该事件；返回 `void` 时视为已消费。

::: tip 基类选择技巧
`EventDispatch` 的基类参数选择有一些优化技巧，通常可以选择直接基类，但也可以用更高层的祖先类，这会造成细微的代码大小和性能差异。但一般不需要过于纠结，也不用担心误用出错——只要编译通过了，事件分发就会正确工作。
:::

::: important
下文中提到“覆写 `xxxEvent()`”的说法时，请注意仅仅是在派生控件类中**声明**了一个与基类事件处理函数签名相同但**非虚**的成员函数。这**不是**虚函数，不能加 `override`，也不依赖虚函数机制来分发事件。

IDE 可能提示将这些成员函数改为虚函数，不要理会这个提示。
:::

如果要处理手势输入，声明 `gestureEvent()` 并在类中实现：

```cpp
// 在头文件 protected 区域增加声明：
bool gestureEvent(GestureEvent *event);

// 在 .cpp 中实现：
bool ProgressRing::gestureEvent(GestureEvent *event) {
    if (event->type() == Event::Press) {
        // ...
        return true;   // 返回 true 表示事件已消费，不再向父控件传递
    }
    return false;
}
```

可处理的事件类型：

| 方法签名 | 触发时机 |
|---|---|
| `bool gestureEvent(GestureEvent *)` | 手势事件，包括 Press、Pan、Swipe 等 |
| `bool wheelEvent(WheelEvent *)` | 滚轮或旋钮输入（如表冠） |
| `bool keyEvent(KeyEvent *)` | 实体按键 |
| `void resizeEvent(ResizeEvent *)` | 控件尺寸变化 |
| `void moveEvent(MoveEvent *)` | 控件位置变化 |
| `bool focusEvent(FocusEvent *)` | 焦点变化 |
| `void paintEvent(PaintEvent *)` | 重绘请求 |
| `bool layoutEvent(LayoutEvent *)` | 布局请求 |
| `void tickEvent(TickEvent *)` | 逐帧 tick（需主动调用 `requestNextTick()` 启用） |

如果某些事件处理函数对当前控件是**必须实现**的，可以在 `EventDispatch` 的模板参数中声明，遗漏或签名不匹配时编译报错：

```cpp
bool MyButton::event(Event *event) {
    // 若未正确声明 paintEvent 或 gestureEvent，编译失败
    return EventDispatch<Widget, PaintEvent, GestureEvent>{}(this, event);
}
```

::: tip 声明必要事件处理函数
尽管可以使用 `EventDispatch<Widget>` 来自动分发所有事件，但是**强烈建议**显式声明当前控件需要处理的事件类型，这样可以在编译期尽可能地检查遗漏或笔误，并减少人工审核的负担。
:::

### 属性与信号

使用 `GX_PROPERTY` 宏向框架暴露属性，使其可被应用层绑定、也可作为属性动画的目标：

```cpp
// 声明 value 属性，getter 为 value()，setter 为 setValue()
// signal 字段关联变化信号，供响应式框架订阅
GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
```

声明后，`value` 属性可以：
- 被应用层模板直接绑定（如 `<progress-ring :value="progress"/>`）
- 被属性动画系统平滑过渡（当属性类型支持插值时）

在 setter 中调用 `update()` 触发重绘，在合适时机发射信号通知外部：

```cpp
void ProgressRing::setValue(int v) {
    if (m_value == v) return;
    m_value = v;
    update();          // 标记下一帧重绘
    valueChanged(v);   // 发射信号
}
```

`Signal<T>` 是普通的模板成员变量，直接像函数调用一样发射。无参信号使用 `Signal<>`，调用时不传参数。关于属性与信号的完整语义，参见[对象系统](./object-system.md)中的相关章节。

### 布局

控件实例化后，通过 `setGeometry()` 手动指定位置和大小；如果父控件使用自动布局，则覆写 `sizeHint()` 来声明控件的期望大小：

```cpp
Size ProgressRing::sizeHint() const {
    return Size(80, 80);
}
```

对于自身需要管理子控件布局的容器控件，在 `layoutEvent()` 中完成子控件的几何计算，或通过 `setLayout()` 挂载框架提供的布局类（如 `FlexLayout`）。详见[布局与尺寸](#布局与尺寸)章节。

## 绘制

### Painter 初始化

在控件的 `paintEvent()` 成员函数中构造 `Painter` 即可开始绘制：

```cpp
void ProgressRing::paintEvent(PaintEvent *event) {
    Painter p(this);
    // 后续所有绘制通过 p 完成
}
```

绘制坐标系以**控件左上角为原点**，向右为 $+x$，向下为 $+y$，单位为像素。`rect()` 返回当前控件的本地矩形 `(0, 0, width(), height())`，是绘制时最常用的参考区域。

如果控件通过应用层样式或 `StyleModifier` 设置了背景色等框架管理的样式属性，可以在绘制自定义内容之前先调用基类来处理这些背景：

```cpp
void ProgressRing::paintEvent(PaintEvent *event) {
    Widget::paintEvent(event);  // 先绘制框架管理的背景（如有）
    Painter p(this);
    // ...
}
```

不调用基类时，框架管理的背景样式将被忽略，控件完全由自己的 `paintEvent` 负责全部视觉呈现。

### 绘制状态

`Painter` 维护一组当前绘制状态，每次绘制调用都使用当前状态，直到下次修改。

#### 画刷（Brush）

画刷决定**填充类**方法（`fillRect`、`fillRoundedRect`、`fillPath` 等），以及**文本**使用的颜色：

```cpp
p.setBrush(Color(200, 200, 200));   // RGB 灰色
p.setBrush(Color{"#35a7ff"});       // 十六进制字符串
p.setBrush(Color::White);           // 预定义常量
p.setBrush(Color(0xff4486ff));      // ARGB 十六进制整数（0xff 为完全不透明）
```

#### 画笔（Pen）

画笔决定**描边类**方法（`drawRect`、`drawArc`、`drawLine` 等）使用的颜色和线宽：

```cpp
Pen pen(Color(64, 156, 255));
pen.setSize(6);    // 线宽 6px
p.setPen(pen);
```

#### 其他状态

```cpp
p.setFont(Font(18));     // 18px 字号，影响 drawText()
p.setOpacity(127);      // 透明度 [0, 255]，影响此后所有绘制
```

所有状态仅作用于当前 `Painter` 实例，不同控件各自构造的 `Painter` 完全独立，互不干扰。

### 基础形状

#### 矩形

```cpp
p.setBrush(Color::White);
p.fillRect(rect());                    // 填充整个控件区域
p.fillRect(Rect(10, 10, 60, 20));      // 填充指定矩形

p.fillRoundedRect(rect(), 8.0f);       // 圆角填充，圆角半径 8px
p.drawRoundedRect(rect(), 8.0f);       // 圆角描边（不填充，使用 Pen 颜色）
```

圆角半径等于宽高较小值的一半时，矩形变成胶囊形状，这在按钮和进度条中非常常见：

```cpp
float radius = min(box.width(), box.height()) * 0.5f;
p.fillRoundedRect(box, radius);
```

#### 直线

```cpp
p.drawLine(Point(0, cy), Point(width(), cy));   // 水平分隔线
```

#### 圆弧

`drawArc` 以圆心坐标和半径指定弧形，`startAngle`/`endAngle` 单位为度数，$0°$ 对应 $3$ 点钟方向，顺时针增大：

```cpp
float cx = width() / 2.0f;
float cy = height() / 2.0f;
float radius = min(cx, cy) - 4.0f;

// 绘制完整圆弧（背景圆环），从 -90°（12 点钟）绕一圈
Pen bgPen(Color(200, 200, 200));
bgPen.setWidth(6);
p.setPen(bgPen);
p.drawArc({cx, cy}, radius, -90.0f, -90.0f + 360.0f);

// 绘制进度弧（从 12 点钟顺时针到 progress 对应位置）
if (m_value > 0) {
    Pen fgPen(Color(64, 156, 255));
    fgPen.setWidth(6);
    p.setPen(fgPen);
    p.drawArc({cx, cy}, radius, -90.0f, -90.0f + 360.0f * m_value / 100.0f);
}
```

弧的视觉粗细由当前 `Pen` 的线宽决定。

### 矢量路径 `VectorPath`

对于矩形和圆弧无法描述的复杂形状，使用 `VectorPath` 构建任意轮廓，再通过 `fillPath()` 或 `drawPath()` 渲染。

```cpp
#include "gx_vectorpath.h"
```

`VectorPath` 的工作方式类似“画笔轨迹”：用 `moveTo` 落笔、`lineTo` 直线段、`arcTo` 圆弧段依次描述轮廓，最后由 `Painter` 统一渲染。

#### 直线段路径

```cpp
VectorPath path;
path.moveTo(x0, y0);   // 落笔（不绘制）
path.lineTo(x1, y1);   // 直线到 (x1, y1)
path.lineTo(x2, y2);
path.lineTo(x0, y0);   // 回到起点，形成封闭三角形

p.fillPath(path, Color(64, 156, 255)); // 填充封闭区域
```

`fillPath()` 自动将路径作为封闭区域处理，即使最后没有显式回到起点。`drawPath()` 则用当前 `Pen` 绘制路径轮廓而不填充。

#### 圆弧段路径

`arcTo` 参数为圆心、$x/y$ 半径（椭圆时两者不等）、起始角度和扫过角度（角度制，顺时针为正）：

```cpp
// 绘制水平胶囊形：左端半圆 + 右端半圆，arcTo 自动用连线衔接两段
float r  = rect.height() * 0.5f;
float x1 = rect.left() + r;
float x2 = rect.right() - r;
float y  = rect.top() + r;

VectorPath path;
path.arcTo(PointF(x1, y), r, r, 90.0f, 270.0f);    // 左端半圆（从 9 点到 3 点逆时针）
path.arcTo(PointF(x2, y), r, r, -90.0f, 90.0f);    // 右端半圆（从 3 点到 9 点逆时针）
p.fillPath(path);
```

`arcTo` 会在路径当前终点和新圆弧起点之间自动插入一条直线，因此两段圆弧首尾自然衔接，无需额外调用 `lineTo`。

#### 曲线

使用 `conicTo` 或 `cubicTo` 可以构建二次或三次贝塞尔曲线段，配合 `moveTo` 和 `lineTo` 可以描述复杂的轮廓：

```cpp
VectorPath path;
path.moveTo(x0, y0);
// 二次贝塞尔曲线，(cx, cy) 为控制点
path.conicTo(cx, cy, x1, y1);
// 三次贝塞尔曲线，(cx1, cy1) 和 (cx2, cy2) 为控制点
path.cubicTo(cx1, cy1, cx2, cy2, x2, y2);
// 使用指定画刷填充路径
p.fillPath(path, brush);
```

#### 组合路径示例

将多段指令组合，可以构建任意复杂的形状。以 `WaveSlider` 中波浪填充区域为例，路径包含顶部波形折线和底部圆角边：

```cpp
VectorPath path;
path.moveTo(leftX, waveY(leftX));
for (int i = 1; i <= sampleCount; ++i) {
    float x = leftX + (rightX - leftX) * float(i) / sampleCount;
    path.lineTo(x, waveY(x));           // 顶部波浪轮廓
}
path.lineTo(rightX, bottomEdge(rightX)); // 右侧下降
for (int i = sampleCount - 1; i >= 0; --i) {
    float x = leftX + (rightX - leftX) * float(i) / sampleCount;
    path.lineTo(x, bottomEdge(x));       // 底边（沿圆角矩形底部返回）
}
path.lineTo(leftX, waveY(leftX));        // 回到起点
p.fillPath(path);
```

### 文字

`drawText()` 在矩形范围内排列并绘制文本，文字颜色由当前 `Brush` 决定，字体由 `setFont()` 设置：

```cpp
p.setFont(Font(18));
p.setBrush(Color(50, 50, 50));
p.drawText(rect(), format("{}%", m_value), AlignCenter);
```

::: tip 格式化字符串
`format()` 是框架提供的格式化函数，语法类似 [`std::format`](https://en.cppreference.com/w/cpp/utility/format/format)，可跨平台使用。
:::

对齐标志可自由组合：

| 标志 | 含义 |
|---|---|
| `AlignLeft` | 水平左对齐 |
| `AlignHCenter` | 水平居中 |
| `AlignRight` | 水平右对齐 |
| `AlignTop` | 垂直顶对齐 |
| `AlignVCenter` | 垂直居中 |
| `AlignBottom` | 垂直底对齐 |
| `AlignCenter` | 水平 + 垂直居中（等同于 `AlignHCenter \| AlignVCenter`）|

`font()` 方法返回控件当前从样式系统继承的字体，在绘制中使用它可以使控件自动跟随应用字号变化：

```cpp
p.setFont(font());   // 使用控件继承的样式字体，而非固定字号
```

`drawText()` 还支持更复杂的文本布局，例如多行文本、自动换行等，详见 API 文档。

### 图片

`drawImage()` 将图片绘制到指定矩形内：

```cpp
Image img{"file://path/to/icon.png"};
p.drawImage(widget->rect(), img); // 将图片绘制到指定区域，不会自动缩放
```

实际使用中图片通常来自资源系统，加载方式取决于平台和打包配置。

### 完整示例

以下是 `ProgressRing` 的完整 `paintEvent`，综合运用了上述绘制能力：

```cpp
void ProgressRing::paintEvent(PaintEvent *event) {
    // 若控件有背景样式由框架管理，先调用基类
    // Widget::paintEvent(event);

    Painter p(this);

    float cx = width() / 2.0f;
    float cy = height() / 2.0f;
    float radius = min(cx, cy) - 4.0f;
    float startAngle = -90.0f;   // 从 12 点钟方向开始

    // 绘制灰色背景圆环
    Pen bgPen(Color(200, 200, 200));
    bgPen.setWidth(6);
    p.setPen(bgPen);
    p.drawArc({cx, cy}, radius, startAngle, startAngle + 360.0f);

    // 绘制彩色进度弧
    if (m_value > 0) {
        Pen fgPen(Color(64, 156, 255));
        fgPen.setWidth(6);
        p.setPen(fgPen);
        p.drawArc({cx, cy}, radius,
          startAngle, startAngle + 360.0f * m_value / 100.0f);
    }

    // 在圆环中心绘制百分比数字
    p.setFont(Font(18));
    p.setBrush(Color(50, 50, 50));
    p.drawText(rect(), format("{}%", m_value), AlignCenter);
}
```

## 布局与尺寸

覆写 `sizeHint()` 告知布局系统控件的"期望大小"。当父控件使用自动布局时，布局系统会参考这个值来分配空间：

```cpp
Size ProgressRing::sizeHint() const {
    return Size(80, 80);  // 建议显示为 80×80px
}
```

如果控件是高度随宽度变化的（例如等比缩放的图片），覆写 `heightForWidth()`：

```cpp
int AspectWidget::heightForWidth(int width) const {
    return width; // 正方形比例
}
```

对于需要手动管理子控件布局的情况，覆写 `layoutEvent()` 并在其中设置子控件的几何：

```cpp
bool ContainerWidget::layoutEvent(LayoutEvent *event) {
    // 将子控件从上往下排列
    int y = 0;
    for (auto *child : children()) {
        auto *w = dyn_cast<Widget *>(child);
        if (w && w->isVisible()) {
            w->setGeometry(0, y, width(), w->sizeHint().height());
            y += w->height();
        }
    }
    return true;
}
```

也可以使用框架提供的现成布局类（如 `FlexLayout`、`StackLayout`），通过 `setLayout(new FlexLayout())` 挂载。

::: tip 使用现成的布局类
除非你要制作特殊布局的容器控件，否则建议使用框架提供的布局类来管理子控件的布局，这种情况下不需要覆写 `layoutEvent()`。

实现一个完整的布局算法是比较复杂的，需要处理 `sizeHint()` 等多个方面的交互，并且还要考虑性能优化。
:::

## 动画

框架提供了三类动画机制：**样式动画**、**属性动画**和 **`ValueAnimation`**。样式动画和属性动画主要用于**应用层**（即使用控件的一侧），而在实现自定义控件时，最常直接用到的是 `ValueAnimation`。

### ValueAnimation

`ValueAnimation<T>` 是一个对任意类型 `T` 进行插值的动画类。每一帧它会根据当前进度计算出插值结果，并通过 `value` 信号发射出来。你只需将信号连接到自己的更新逻辑即可：

```cpp
#include "gx_valueanimation.h"

// 在控件成员中声明动画对象，一般使用指针以便在需要时动态创建和销毁
ValueAnimation<int> *m_animation = nullptr;
```

```cpp
// 在某处初始化并启动
m_animation = new ValueAnimation<int>;
m_animation->setValueLimits(0, 100);  // 从 0 插值到 100
m_animation->setDuration(800);        // 800 毫秒
m_animation->value.connect(this, &MyWidget::onAnimationValue);
m_animation->start();

// 帧回调：接收每帧计算出的插值
void MyWidget::onAnimationValue(int v) {
    m_currentValue = v;
    update();  // 触发重绘
}
```

动画结束时发射 `finished` 信号。如果不需要手动管理生命周期，可以用 `DeleteOnStop` 策略让动画在播放完毕后自动销毁：

```cpp
// 动画对象不需要外部访问，直接 new 后自动销毁
auto *anim = new ValueAnimation<int>;
anim->setValueLimits(0, 100);
anim->setDuration(500);
anim->value.connect(this, &MyWidget::onValue);
anim->start(AbstractAnimation::DeleteOnStop);  // 播完自动 delete
```

框架内置了以下类型的插值支持：`int`、`float`（以及其他数值类型）、`Color`、`Point`、`Pen`、`Brush`、`Length`、`Transform` 等。

其他常用配置：

```cpp
// 无限循环播放
anim->setRepeat(AbstractAnimation::Infinity);

// 来回交替播放（正放→倒放→正放……）
anim->setDirection(AbstractAnimation::Alternate);

// 设置缓动曲线
#include "gx_easecurve.h"
anim->setEaseCurve(easing::make_curve<easing::Ease>());
```

### 样式动画与属性动画

**样式动画**（`StyleAnimation`）通过类似 CSS transition 的方式定义过渡效果，当控件的样式状态切换时由框架自动播放，主要在应用层组件的样式配置中使用。

**属性动画**（`PropertyAnimation`）通过属性名字符串驱动 `GX_PROPERTY` 声明的属性，常用于应用层对控件属性做动画：

```cpp
#include "gx_propertyanimation.h"

auto *anim = new PropertyAnimation(widget, "value");
anim->setStartValue(Variant{0});
anim->setStopValue(Variant{100});
anim->setDuration(1000);
anim->start(AbstractAnimation::DeleteOnStop);
```

在实现控件本身时，通常不需要使用属性动画，因为 `ValueAnimation` 更直接，也没有按名称查找属性的开销。

## 文本显示控件

实现带有文本内容的控件时，除了基本的绘制逻辑外，还需要处理文本测量、布局缓存、样式联动等问题。`Label` 是框架最典型的文本控件，其实现可以作为类似控件的参考模板。

### 使用 `updateLayout()`

`update()` 仅标记控件需要**重绘**，不影响布局系统。而文本内容变化时，控件的期望大小（`sizeHint()` 返回值）通常也会随之改变，此时必须同时调用 `updateLayout()` 来触发父控件的布局重新计算：

```cpp
void MyTextWidget::setText(const String &text) {
    if (m_text == text)
        return;
    m_text = text;
    update();        // 触发重绘
    updateLayout();  // 通知父布局重新计算（因为 sizeHint 变了）
}
```

仅调用 `update()` 的后果是：文本内容已更新，但控件大小仍是旧文本计算出来的值，排版会错乱。

### 文本测量与 `sizeHint()`

`FontMetrics` 是文本测量的核心工具，用它来实现 `sizeHint()` 和 `heightForWidth()`：

```cpp
#include "gx_fontmetrics.h"

Size MyTextWidget::sizeHint() const {
    if (m_text.empty())
        return Size{0, int(font().pixelSize() * 1.2f)};
    FontMetrics fm(font());
    // 单行文本：直接测量宽度
    return Size{fm.width(m_text), int(font().pixelSize() * 1.2f)};
}
```

对于支持自动换行的多行文本，还需要实现 `heightForWidth()`，告知布局系统在给定宽度下控件的高度：

```cpp
int MyTextWidget::heightForWidth(int width) const {
    if (width == 0) return 0;
    FontMetrics fm(font());
    float lineHeight = font().pixelSize() * 1.2f;
    // boundingRect 计算给定宽度下文本的实际边界
    return fm.boundingRect(m_text, width, 1024 * 1024, 0, 0, lineHeight).height();
}
```

如果控件是严格的单行（不随宽度换行），`heightForWidth()` 返回 `-1` 表示不依赖宽度：

```cpp
int SingleLineWidget::heightForWidth(int) const { return -1; }
```

### 响应样式与尺寸变化

字体、颜色等样式属性变化时，文本的测量结果也会改变。覆写 `styleEvent()` 来响应样式变化，调用基类实现后刷新与样式相关的缓存，再触发布局更新：

```cpp
void MyTextWidget::styleEvent(StyleEvent *event) {
  // 必须先调用基类，它会更新内部样式数据
    Widget::styleEvent(event);
    // 字体等样式改变后，sizeHint 的返回值可能变化
    updateLayout();
}
```

同样，控件尺寸变化时如果有依赖宽度的文本换行计算，需要在 `resizeEvent()` 中触发更新：

```cpp
void MyTextWidget::resizeEvent(ResizeEvent *event) {
    Widget::resizeEvent(event); // 调用基类
    update();                   // 尺寸变化后重绘内容
}
```

::: important
`styleEvent()`、`resizeEvent()` 等事件处理函数的基类实现通常有不可省略的副作用，**必须调用**。调用时机取决于你的逻辑需要：大多数情况下先调用基类，再执行自己的逻辑。
:::

### 覆写 `event()`

将 `StyleEvent`、`ResizeEvent` 等需要处理的事件类型全部列入 `EventDispatch` 的模板参数，以获得编译期检查：

```cpp
bool MyTextWidget::event(Event *event) {
    return EventDispatch<Widget,
        PaintEvent, ResizeEvent, StyleEvent>{}(this, event);
}
```

### 流式布局与行内元素

`setFlowLayout(true)` 将**容器控件**设置为流式布局（flow layout）模式，效果类似 CSS 的块级流，框架会自动将子元素按行排布，无需通过 `setLayout()` 创建独立的布局对象。`Label` 在构造函数中就启用了这一模式，从而使自己可以作为 `SpanLabel` 容器（内嵌多个带不同样式的子标签）：

```cpp
Label::Label(Widget *parent) : Widget(parent) {
    setFlowLayout(true);
}
```

`setInlineWidget(true)` 则是针对**子元素**的设置，将该控件标记为行内（inline）元素，使其像文字一样嵌入父容器的文本流中参与排版。例如，在富文本行内嵌入一个图标控件：

```cpp
auto *icon = new ImageBox(label);
// 作为行内元素与文字混排。ImageBox 默认已经是行内的了，这里只是示例说明。
icon->setInlineWidget(true);
```

当 `Label` 作为容纳行内子元素的 `SpanLabel` 容器使用时，布局系统会自动协调 `Label` 自身的文本测量逻辑和作为容器时对子元素的排布。两者共用同一套布局机制，开发者不需要手动干预这一过程。

## AbstractScrollArea 与可滚动控件

当控件需要滚动行为时，不必从头实现手势识别、惯性滚动和回弹效果，直接继承 `AbstractScrollArea` 即可获得这些能力。框架内置的 `ScrollArea`（列表滚动）和 `TextField`（单行文本输入）都基于它实现。

### 基本结构

继承 `AbstractScrollArea` 的控件遵循一个固定的结构：控件本身是"视口"，内部有一个**内容控件**（content widget）负责承载实际内容，滚动时移动的是内容控件而非视口本身。

构造函数中完成初始化：

```cpp
// myticker.h
#include "gx_abstractscorllarea.h"

class MyTicker : public AbstractScrollArea {
    GX_OBJECT
public:
    explicit MyTicker(Widget *parent = nullptr);
    bool event(Event *event) override;

protected:
    bool layoutEvent(LayoutEvent *event);
    friend struct EventTraits<MyTicker>;
};
```

```cpp
// myticker.cpp
#include "myticker.h"
#include "gx_widgetevent.h"

MyTicker::MyTicker(Widget *parent) : AbstractScrollArea(parent) {
    setDirection(Horizontal);     // 水平滚动
    setDamping(5);                // 调整阻尼（数值越大摩擦越强）

    auto *content = new Widget;   // 创建内容控件
    setContentWidget(content);
}

bool MyTicker::event(Event *event) {
    return EventDispatch<AbstractScrollArea, LayoutEvent>{}(this, event);
}
```

将 `EventDispatch` 的基类参数设为 `AbstractScrollArea`（而非 `Widget`），可以让未被当前类处理的事件（手势、滚轮、resize 等）自动回退到 `AbstractScrollArea` 的实现，从而保留完整的滚动行为。

### 配置滚动参数

```cpp
setDirection(Vertical);          // 垂直滚动（默认）
setDirection(Horizontal);        // 水平滚动
setDamping(3);                   // 较低阻尼：惯性更强，滑行更远
setDamping(20);                  // 较高阻尼：惯性较弱，接近无惯性
setScrollBar(true);              // 显示滚动条
setBouncesPolicy(SnapType::SnapEdge);  // 边缘回弹策略
```

`AbstractScrollArea` 还提供了 `scrollTo(x, y, behavior)` 来以编程方式控制滚动位置，`behavior` 为 `Instant`（立即跳转）或 `Smooth`（带动画）。

::: tip 惯性阻尼
对于 `TextField` 这类需要精确控制滚动位置的控件，通常会设置较高的阻尼值以弱化惯性；而对于 `ScrollArea` 这类以浏览为主的控件，则可以设置较低的阻尼以获得更流畅的滚动体验。

阻尼不要设置得太低，否则超长距离的滚动可能导致内容缓存失效，出现卡顿。
:::

### 在事件分发中调用基类

有时需要对某事件做额外处理，再将控制权交给 `AbstractScrollArea` 的默认实现。典型的做法是在处理函数中直接调用基类方法：

```cpp
// TextField 的做法：只在有文字时才转发手势给滚动区
bool TextField::gestureEvent(GestureEvent *event) {
    if (text().empty()) // 无文字时直接忽略
        return false;
    // 其余情况交给基类滚动逻辑
    return AbstractScrollArea::gestureEvent(event);
}
```

这种模式下，`EventDispatch` 的基类参数使用 `Widget`，当前类自行决定何时调用哪个基类方法：

```cpp
bool TextField::event(Event *event) {
    // 用 Widget 作为基类，完全由自己控制 AbstractScrollArea 行为的调用时机
    return EventDispatch<Widget, GestureEvent, ResizeEvent>{}(this, event);
}
```

### 内容控件的事件过滤

内容控件负责布局和承载子控件，但它的某些事件（如布局请求）有时需要容器来拦截和自定义处理。通过 `setEventFilter(this)` 将容器注册为内容控件的事件过滤器，然后覆写 `eventFilter()` 处理感兴趣的事件：

```cpp
// 在构造函数中注册
content->setEventFilter(this);

// 拦截内容控件的布局请求
bool MyTicker::eventFilter(Object *receiver, Event *e) {
    if (receiver == contentWidget() && e->type() == Event::Layout) {
        auto *lv = static_cast<LayoutEvent *>(e);
        if (lv->isLayoutRequest()) {
            // 自定义布局逻辑……
            return true; // 返回 true 阻止事件继续传递
        }
    }
    // 其余情况交给基类
    return AbstractScrollArea::eventFilter(receiver, e);
}
```

::: tip
未被处理的事件应回退给 `AbstractScrollArea::eventFilter()`，它负责与滚动条等内部机制的交互。
:::

### 设置行内控件

调用 `setInlineWidget(true)` 可以让控件参与行内布局（inline layout），适合嵌入文本流中的场景，`TextField` 就是这样处理使其可以像文字一样嵌入行内。

### ScrollArea 及派生类

`ScrollArea` 是 `AbstractScrollArea` 的一个派生类，在滚动基础上增加了**索引导航**（`index()`/`setIndex()`）、**吸附模式**（snap）和**视觉特效**（visual effect）等能力，是列表、走马灯等场景的首选基类。`Swiper` 则在 `ScrollArea` 之上进一步增加了分页（`pageLength`）和指示点（indicator）等功能，适合轮播图等模式。

这些类通常**不需要进一步派生**，大多数定制需求可以通过配置参数和挂载周边设施来实现，而无需子类化。

#### 视觉特效 VisualEffect

`ScrollArea` 支持通过 `setVisualEffect()` 挂载一个 `VisualEffect` 对象，在绘制每个子控件之前对其施加透明度、缩放、位移等视觉变换，从而实现滚动时的动态效果。框架内置了以下几种效果：

| 类名 | 效果 |
|---|---|
| `FisheyeVisualEffect` | 鱼眼效果，中心元素放大，边缘缩小 |
| `FadeVisualEffect` | 边缘渐隐，距离视口中心越远透明度越低 |
| `CollapseVisualEffect` | 折叠效果，元素向上（或向下）边缘聚拢缩小 |
| `BlendVisualEffect` | 在两种效果之间按进度插值过渡 |

```cpp
#include "gx_visualeffect.h"

scrollArea->setVisualEffect(make_shared<FisheyeVisualEffect>());
```

如需自定义效果，继承 `VisualEffect` 并实现 `resolve()` 方法。`resolve()` 接收目标子控件、视口矩形和子控件中心点，返回一个 `PaintModifier`，其中可设置 `opacity`、`scale`、`translate` 等属性。

有关 `ScrollArea` 和 `Swiper` 的完整参数说明，以及如何实现自定义 `VisualEffect`，将在[滚动区域](./scroll-area.md)中单独介绍。

## 控件树与生命周期

在 C++ 中创建控件时，通过构造函数的 `parent` 参数建立父子关系：

```cpp
// parent 销毁时，child 也会随之销毁
auto *parent = new Widget(window);
auto *child  = new ProgressRing(parent);
child->setGeometry(10, 10, 80, 80);
```

无论是手动 `delete` 父控件，还是框架在应用退出时清理控件树，所有子控件都会被自动销毁。你不需要在析构函数中 `delete` 子控件。

如果需要延迟销毁（例如在事件处理函数内部），可以使用 `deleteLater()`，它会在当前事件处理完成后再销毁对象，避免"在回调中销毁自己"这类问题。

在响应式框架中，控件树由组件框架维护，定制开发时只需要[注册控件类](./widget-export.md)。
