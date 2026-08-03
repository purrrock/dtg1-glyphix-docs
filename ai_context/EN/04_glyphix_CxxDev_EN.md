# Context File: 04_glyphix_CxxDev_EN.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/transl/EN/cxxdev/widget.md

---
headerDepth: 2
---
# Widget Development Guide

In Glyphix, all visible UI elements are `Widget`s. The framework comes with built-in common controls such as buttons, labels, images, and scroll areas, but device manufacturers often need to develop customized widgets based on their product features. For example, a smart watch might customize a special list animation due to its small circular screen, while dashboard equipment requires specialized chart widgets. This document explains how to implement a new widget in C++.

## Widget Basics

A `Widget` is a rectangular area that has basic properties such as position, size, visibility, and opacity. It can receive events and is responsible for painting its own content. Widgets are organized in a tree structure: a parent widget contains several child widgets, and the coordinates of a child widget are relative to its parent.

Each widget has a **logical update cycle**: when a widget's state changes (e.g., data updates), calling `update()` marks it as "needs repaint." The framework will uniformly repaint all marked widgets in the next render frame rather than repainting immediately—this avoids duplicate repaints within the same frame.

### Widgets and the Component System

UI widgets are typically implemented as C++ classes inheriting from `Widget` and complying with standard C++ object-oriented design. Glyphix's reactive framework and component system support directly exposing these C++ widgets as native components for use in a templated, declarative manner.

This design allows widget development on the C++ side and component usage on the front-end side to remain relatively independent while preserving their respective habitual development styles. For example, in C++ you can build interfaces in a way similar to LVGL or Qt Widgets without needing to adopt the popular declarative style of front-end frameworks.

### Comparison with Other Frameworks

The Glyphix widget system is designed similarly to traditional C/C++ UI frameworks like Qt Widgets or LVGL. Therefore, you will find that the methods and knowledge system for developing a new widget are very similar to those frameworks:
- Create a new widget class by inheriting from `Widget`;
- Core mechanisms such as layout systems, event systems, and painting systems exist;
- Data binding and event notification are implemented through the property system and signal mechanism;
- Geometric concepts such as coordinate systems and dimensions exist, and nested widget tree structures are supported.

::: tip Developing UI with C++ Widgets is Not Recommended
The original design intention of Glyphix is not to develop UI directly on the C++ side; therefore, we do not provide related documentation and examples.
:::

## Creating Custom Widgets

This section uses a circular progress bar widget (`ProgressRing`) as an example to step-by-step illustrate the essential elements required to develop a custom widget.

::: tip Comprehensive Widget Example
The [slider-demo](./widget-slider-demo.md) example included with the SDK is a complete practice of all the knowledge points in this document, including inheriting existing widgets, painting, event processing, property declaration, `ValueAnimation` animation, and `StyleEngine` customization. It is recommended to read it after reading this document.
:::

### Defining the Widget Class

Create a new widget, inherit from `Widget`, add the `GX_OBJECT` macro at the very beginning of the class definition, and **override the `event()`** virtual function as the entry point for event handling:

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

    // EventDispatch needs access to protected methods; declare it as a friend
    friend struct EventTraits<ProgressRing>;

private:
    int m_value;  // [0, 100]
};
```

`GX_OBJECT` is essential. It triggers the meta-object compiler to generate metadata for this class, allowing the widget to be properly recognized by the framework's property system, animation system, and component system (see [Object System](./object-system.md) for details).

### Painting the Widget

Include `gx_widgetevent.h` in the `.cpp` file and implement `event()` and `paintEvent()`:

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
    // ... See the painting section for details
}
```

Custom painting is accomplished by implementing `paintEvent()`. Passing the `this` pointer when constructing a `Painter` yields the drawing context associated with the current widget, after which various drawing methods can be called to paint. For a complete description of the `Painter` API, refer to the [Painting](./painting.md) section.

### Handling Events

Glyphix's event system **does not rely on virtual function inheritance** to dispatch events. Methods like `paintEvent()` and `gestureEvent()` are not `virtual`, and **do not** add `override` during declaration (doing so will cause a compilation error). The framework routes calls to the correct handler function at **compile time** according to the event type via `EventDispatch`.

The only virtual function that needs to be (and must be) overridden is **`event()`**, in which you delegate to `EventDispatch`:

```cpp
bool ProgressRing::event(Event *event) {
    return EventDispatch<Widget>{}(this, event);
}
```

The first template parameter of `EventDispatch` is usually the **direct base class** (i.e., the class that `ProgressRing` inherits from, which is `Widget` here). It checks at compile time whether the current class directly declares the corresponding handler function. If so, it calls it; otherwise, it automatically falls back to the base class implementation. Returning `bool` from a handler function indicates whether the event was consumed; returning `void` is treated as consumed.

::: tip Base Class Selection Tips
There are some optimization tips for choosing the base class parameter of `EventDispatch`. Usually, you can choose the direct base class, but you can also use a higher-level ancestor class, which will cause subtle differences in code size and performance. Generally, however, you don't need to dwell on it too much, nor do you need to worry about misuse errors—as long as it compiles successfully, event dispatching will work correctly.
:::

::: important
When mentioning "overriding `xxxEvent()`" below, please note that it is merely **declaring** a non-virtual member function in the derived widget class with the same signature as the base class event handler function. This is **not** a virtual function, `override` cannot be added, and it does not rely on the virtual function mechanism to dispatch events.

The IDE may prompt you to change these member functions to virtual; ignore this prompt.
:::

If you need to handle gesture input, declare `gestureEvent()` and implement it in the class:

```cpp
// Add a declaration in the protected area of the header file:
bool gestureEvent(GestureEvent *event);

// Implement in .cpp:
bool ProgressRing::gestureEvent(GestureEvent *event) {
    if (event->type() == Event::Press) {
        // ...
        return true;   // Return true to indicate the event is consumed and will not be passed to the parent widget
    }
    return false;
}
```

Supported event types:

| Method Signature | Trigger Timing |
|---|---|
| `bool gestureEvent(GestureEvent *)` | Gesture events, including Press, Pan, Swipe, etc. |
| `bool wheelEvent(WheelEvent *)` | Wheel or dial input (such as a watch crown) |
| `bool keyEvent(KeyEvent *)` | Physical keys |
| `void resizeEvent(ResizeEvent *)` | Widget size change |
| `void moveEvent(MoveEvent *)` | Widget position change |
| `bool focusEvent(FocusEvent *)` | Focus change |
| `void paintEvent(PaintEvent *)` | Repaint request |
| `bool layoutEvent(LayoutEvent *)` | Layout request |
| `void tickEvent(TickEvent *)` | Frame-by-frame tick (must explicitly call `requestNextTick()` to enable) |

If certain event handler functions are **mandatory** for the current widget, they can be declared in the template parameters of `EventDispatch`. Omissions or signature mismatches will result in compilation errors:

```cpp
bool MyButton::event(Event *event) {
    // Compilation fails if paintEvent or gestureEvent are not correctly declared
    return EventDispatch<Widget, PaintEvent, GestureEvent>{}(this, event);
}
```

::: tip Declaring Necessary Event Handlers
Although `EventDispatch<Widget>` can be used to automatically dispatch all events, it is **strongly recommended** to explicitly declare the event types that the current widget needs to handle. This catches omissions or typos at compile time as much as possible and reduces the burden of manual review.
:::

### Properties and Signals

Expose properties to the framework using the `GX_PROPERTY` macro so that they can be bound by the application layer or serve as targets for property animations:

```cpp
// Declare the value property, with getter value() and setter setValue()
// The signal field associates the change signal for subscription by the reactive framework
GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
```

Once declared, the `value` property can:
- Be directly bound by application-layer templates (e.g., `<progress-ring :value="progress"/>`)
- Be smoothly transitioned by the property animation system (when the property type supports interpolation)

Call `update()` in the setter to trigger a repaint, and emit signals at the appropriate time to notify external observers:

```cpp
void ProgressRing::setValue(int v) {
    if (m_value == v) return;
    m_value = v;
    update();          // Mark for repaint in the next frame
    valueChanged(v);   // Emit signal
}
```

`Signal<T>` is a standard template member variable, emitted directly like a function call. Parameterless signals use `Signal<>` and take no arguments when called. For complete semantics regarding properties and signals, refer to the relevant section in the [Object System](./object-system.md).

### Layout

After instantiating a widget, manually specify its position and size via `setGeometry()`; if the parent widget uses automatic layout, override `sizeHint()` to declare the desired size of the widget:

```cpp
Size ProgressRing::sizeHint() const {
    return Size(80, 80);
}
```

For container widgets that need to manage the layout of their child widgets themselves, complete the geometric calculation of child widgets in `layoutEvent()`, or mount a layout class provided by the framework (such as `FlexLayout`) via `setLayout()`. See the [Layout and Dimensions](#layout-and-dimensions) section for details.

## Painting

### Painter Initialization

Construct a `Painter` inside the widget's `paintEvent()` member function to start painting:

```cpp
void ProgressRing::paintEvent(PaintEvent *event) {
    Painter p(this);
    // All subsequent painting is done via p
}
```

The painting coordinate system has its **origin at the top-left corner of the widget**, with $+x$ to the right and $+y$ downwards, in units of pixels. `rect()` returns the local rectangle `(0, 0, width(), height())` of the current widget, which is the most commonly used reference area during painting.

If the widget has set background colors or other framework-managed style properties through application-layer styles or `StyleModifier`, you can call the base class to handle these backgrounds before painting custom content:

```cpp
void ProgressRing::paintEvent(PaintEvent *event) {
    Widget::paintEvent(event);  // Paint framework-managed background first (if any)
    Painter p(this);
    // ...
}
```

When the base class is not called, framework-managed background styles are ignored, and the widget is entirely responsible for its own visual presentation through its `paintEvent`.

### Drawing States

`Painter` maintains a set of current drawing states. Every drawing call uses the current state until it is modified next time.

#### Brush

The brush determines the colors used for **filling** methods (`fillRect`, `fillRoundedRect`, `fillPath`, etc.) as well as **text**:

```cpp
p.setBrush(Color(200, 200, 200));   // RGB gray
p.setBrush(Color{"#35a7ff"});       // Hexadecimal string
p.setBrush(Color::White);           // Predefined constant
p.setBrush(Color(0xff4486ff));      // ARGB hexadecimal integer (0xff is fully opaque)
```

#### Pen

The pen determines the color and line width used for **stroking** methods (`drawRect`, `drawArc`, `drawLine`, etc.):

```cpp
Pen pen(Color(64, 156, 255));
pen.setSize(6);    // Line width 6px
p.setPen(pen);
```

#### Other States

```cpp
p.setFont(Font(18));     // 18px font size, affects drawText()
p.setOpacity(127);      // Opacity [0, 255], affects all subsequent painting
```

All states only apply to the current `Painter` instance. Painters constructed by different widgets are completely independent and do not interfere with each other.

### Basic Shapes

#### Rectangle

```cpp
p.setBrush(Color::White);
p.fillRect(rect());                    // Fill the entire widget area
p.fillRect(Rect(10, 10, 60, 20));      // Fill the specified rectangle

p.fillRoundedRect(rect(), 8.0f);       // Rounded fill, corner radius 8px
p.drawRoundedRect(rect(), 8.0f);       // Rounded stroke (no fill, uses Pen color)
```

When the corner radius equals half of the smaller of the width and height, the rectangle becomes a capsule shape, which is very common in buttons and progress bars:

```cpp
float radius = min(box.width(), box.height()) * 0.5f;
p.fillRoundedRect(box, radius);
```

#### Straight Line

```cpp
p.drawLine(Point(0, cy), Point(width(), cy));   // Horizontal dividing line
```

#### Arc

`drawArc` specifies an arc by center coordinates and radius. The units for `startAngle`/`endAngle` are degrees, where $0^\circ$ corresponds to the $3\text{ o'clock}$ position and increases clockwise:

```cpp
float cx = width() / 2.0f;
float cy = height() / 2.0f;
float radius = min(cx, cy) - 4.0f;

// Draw full arc (background ring), from -90° (12 o'clock) around a full circle
Pen bgPen(Color(200, 200, 200));
bgPen.setWidth(6);
p.setPen(bgPen);
p.drawArc({cx, cy}, radius, -90.0f, -90.0f + 360.0f);

// Draw progress arc (clockwise from 12 o'clock to the position corresponding to progress)
if (m_value > 0) {
    Pen fgPen(Color(64, 156, 255));
    fgPen.setWidth(6);
    p.setPen(fgPen);
    p.drawArc({cx, cy}, radius, -90.0f, -90.0f + 360.0f * m_value / 100.0f);
}
```

The visual thickness of the arc is determined by the line width of the current `Pen`.

### Vector Path (`VectorPath`)

For complex shapes that cannot be described by rectangles and arcs, use `VectorPath` to build arbitrary outlines, and then render them via `fillPath()` or `drawPath()`.

```cpp
#include "gx_vectorpath.h"
```

`VectorPath` works like a "brush trajectory": it uses `moveTo` to drop the pen, `lineTo` for straight segments, and `arcTo` for circular arc segments to sequentially describe the outline, which is finally rendered uniformly by `Painter`.

#### Straight Segment Path

```cpp
VectorPath path;
path.moveTo(x0, y0);   // Drop pen (no drawing)
path.lineTo(x1, y1);   // Straight line to (x1, y1)
path.lineTo(x2, y2);
path.lineTo(x0, y0);   // Return to start, forming a closed triangle

p.fillPath(path, Color(64, 156, 255)); // Fill closed area
```

`fillPath()` automatically treats the path as a closed area even if it doesn't explicitly return to the start point at the end. `drawPath()` draws the outline of the path using the current `Pen` without filling it.

#### Arc Segment Path

The parameters for `arcTo` are center point, $x/y$ radii (which differ for ellipses), start angle, and sweep angle (in degrees, positive clockwise):

```cpp
// Draw horizontal capsule shape: left semicircle + right semicircle, arcTo automatically connects the two segments with a line
float r  = rect.height() * 0.5f;
float x1 = rect.left() + r;
float x2 = rect.right() - r;
float y  = rect.top() + r;

VectorPath path;
path.arcTo(PointF(x1, y), r, r, 90.0f, 270.0f);    // Left semicircle (counterclockwise from 9 o'clock to 3 o'clock)
path.arcTo(PointF(x2, y), r, r, -90.0f, 90.0f);    // Right semicircle (counterclockwise from 3 o'clock to 9 o'clock)
p.fillPath(path);
```

`arcTo` automatically inserts a straight line between the current end point of the path and the start point of the new arc, so the two arc segments connect naturally head-to-tail without requiring an extra call to `lineTo`.

#### Curves

Use `conicTo` or `cubicTo` to build quadratic or cubic Bézier curve segments, which can be combined with `moveTo` and `lineTo` to describe complex outlines:

```cpp
VectorPath path;
path.moveTo(x0, y0);
// Quadratic Bézier curve, (cx, cy) is the control point
path.conicTo(cx, cy, x1, y1);
// Cubic Bézier curve, (cx1, cy1) and (cx2, cy2) are control points
path.cubicTo(cx1, cy1, cx2, cy2, x2, y2);
// Fill the path using the specified brush
p.fillPath(path, brush);
```

#### Combined Path Example

Combining multiple instructions can build shapes of arbitrary complexity. Taking the wave fill area in `WaveSlider` as an example, the path contains a top wave polyline and a bottom rounded edge:

```cpp
VectorPath path;
path.moveTo(leftX, waveY(leftX));
for (int i = 1; i <= sampleCount; ++i) {
    float x = leftX + (rightX - leftX) * float(i) / sampleCount;
    path.lineTo(x, waveY(x));           // Top wave outline
}
path.lineTo(rightX, bottomEdge(rightX)); // Right drop
for (int i = sampleCount - 1; i >= 0; --i) {
    float x = leftX + (rightX - leftX) * float(i) / sampleCount;
    path.lineTo(x, bottomEdge(x));       // Bottom edge (returns along the bottom of the rounded rectangle)
}
path.lineTo(leftX, waveY(leftX));        // Return to start
p.fillPath(path);
```

### Text

`drawText()` lays out and draws text within a rectangular range. The text color is determined by the current `Brush`, and the font is set by `setFont()`:

```cpp
p.setFont(Font(18));
p.setBrush(Color(50, 50, 50));
p.drawText(rect(), format("{}%", m_value), AlignCenter);
```

::: tip Formatted Strings
`format()` is a formatting function provided by the framework. Its syntax is similar to [`std::format`](https://en.cppreference.com/w/cpp/utility/format/format) and it can be used cross-platform.
:::

Alignment flags can be freely combined:

| Flag | Meaning |
|---|---|
| `AlignLeft` | Horizontal left alignment |
| `AlignHCenter` | Horizontal center alignment |
| `AlignRight` | Horizontal right alignment |
| `AlignTop` | Vertical top alignment |
| `AlignVCenter` | Vertical center alignment |
| `AlignBottom` | Vertical bottom alignment |
| `AlignCenter` | Horizontal + vertical center (equivalent to `AlignHCenter \| AlignVCenter`) |

The `font()` method returns the font currently inherited by the widget from the style system. Using it in painting allows the widget to automatically follow changes in the application font size:

```cpp
p.setFont(font());   // Use the widget's inherited style font instead of a fixed size
```

`drawText()` also supports more complex text layouts, such as multi-line text and automatic wrapping. See the API documentation for details.

### Images

`drawImage()` draws an image into a specified rectangle:

```cpp
Image img{"file://path/to/icon.png"};
p.drawImage(widget->rect(), img); // Draw image to specified area without automatic scaling
```

In actual use, images usually come from the resource system, and the loading method depends on the platform and packaging configuration.

### Complete Example

The following is the complete `paintEvent` of `ProgressRing`, combining the painting capabilities mentioned above:

```cpp
void ProgressRing::paintEvent(PaintEvent *event) {
    // If the widget has a background style managed by the framework, call the base class first
    // Widget::paintEvent(event);

    Painter p(this);

    float cx = width() / 2.0f;
    float cy = height() / 2.0f;
    float radius = min(cx, cy) - 4.0f;
    float startAngle = -90.0f;   // Start from 12 o'clock direction

    // Draw gray background ring
    Pen bgPen(Color(200, 200, 200));
    bgPen.setWidth(6);
    p.setPen(bgPen);
    p.drawArc({cx, cy}, radius, startAngle, startAngle + 360.0f);

    // Draw colored progress arc
    if (m_value > 0) {
        Pen fgPen(Color(64, 156, 255));
        fgPen.setWidth(6);
        p.setPen(fgPen);
        p.drawArc({cx, cy}, radius,
          startAngle, startAngle + 360.0f * m_value / 100.0f);
    }

    // Draw percentage number in the center of the ring
    p.setFont(Font(18));
    p.setBrush(Color(50, 50, 50));
    p.drawText(rect(), format("{}%", m_value), AlignCenter);
}
```

## Layout and Dimensions

Override `sizeHint()` to inform the layout system of the widget's "desired size". When the parent widget uses automatic layout, the layout system will reference this value to allocate space:

```cpp
Size ProgressRing::sizeHint() const {
    return Size(80, 80);  // Recommended display as 80×80px
}
```

If the height of the widget varies with its width (such as an aspect-ratio-scaled image), override `heightForWidth()`:

```cpp
int AspectWidget::heightForWidth(int width) const {
    return width; // Square ratio
}
```

For cases where you need to manually manage the layout of child widgets, override `layoutEvent()` and set the geometry of child widgets within it:

```cpp
bool ContainerWidget::layoutEvent(LayoutEvent *event) {
    // Arrange child widgets from top to bottom
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

You can also use ready-made layout classes provided by the framework (such as `FlexLayout`, `StackLayout`), mounted via `setLayout(new FlexLayout())`.

::: tip Use Ready-made Layout Classes
Unless you are creating a container widget with a special layout, it is recommended to use the layout classes provided by the framework to manage the layout of child widgets. In this case, there is no need to override `layoutEvent()`.

Implementing a complete layout algorithm is relatively complex, requiring handling interactions in multiple aspects such as `sizeHint()`, while also considering performance optimization.
:::

## Animation

The framework provides three types of animation mechanisms: **Style Animation**, **Property Animation**, and **`ValueAnimation`**. Style animation and property animation are mainly used on the **application layer** (i.e., the side using widgets), while when implementing custom widgets, `ValueAnimation` is most commonly used directly.

### ValueAnimation

`ValueAnimation<T>` is an animation class that interpolates any type `T`. Each frame it calculates the interpolation result based on the current progress and emits it via the `value` signal. You simply connect the signal to your own update logic:

```cpp
#include "gx_valueanimation.h"

// Declare an animation object among the widget's members, usually using a pointer for dynamic creation and destruction when needed
ValueAnimation<int> *m_animation = nullptr;
```

```cpp
// Initialize and start somewhere
m_animation = new ValueAnimation<int>;
m_animation->setValueLimits(0, 100);  // Interpolate from 0 to 100
m_animation->setDuration(800);        // 800 milliseconds
m_animation->value.connect(this, &MyWidget::onAnimationValue);
m_animation->start();

// Frame callback: receive the interpolated value calculated each frame
void MyWidget::onAnimationValue(int v) {
    m_currentValue = v;
    update();  // Trigger repaint
}
```

The `finished` signal is emitted when the animation ends. If you don't need to manually manage its lifecycle, you can use the `DeleteOnStop` strategy to automatically destroy the animation after playback completes:

```cpp
// The animation object does not need external access; delete automatically after new
auto *anim = new ValueAnimation<int>;
anim->setValueLimits(0, 100);
anim->setDuration(500);
anim->value.connect(this, &MyWidget::onValue);
anim->start(AbstractAnimation::DeleteOnStop);  // Automatically delete after playback
```

The framework has built-in interpolation support for the following types: `int`, `float` (and other numeric types), `Color`, `Point`, `Pen`, `Brush`, `Length`, `Transform`, etc.

Other common configurations:

```cpp
// Infinite loop playback
anim->setRepeat(AbstractAnimation::Infinity);

// Alternating playback back and forth (forward → backward → forward...)
anim->setDirection(AbstractAnimation::Alternate);

// Set easing curve
#include "gx_easecurve.h"
anim->setEaseCurve(easing::make_curve<easing::Ease>());
```

### Style Animations and Property Animations

**Style Animation** (`StyleAnimation`) defines transition effects in a way similar to CSS transitions, automatically played by the framework when the widget's style state switches, and is mainly used in the style configuration of application-layer components.

**Property Animation** (`PropertyAnimation`) drives properties declared with `GX_PROPERTY` via property name strings, and is often used by the application layer to animate widget properties:

```cpp
#include "gx_propertyanimation.h"

auto *anim = new PropertyAnimation(widget, "value");
anim->setStartValue(Variant{0});
anim->setStopValue(Variant{100});
anim->setDuration(1000);
anim->start(AbstractAnimation::DeleteOnStop);
```

When implementing the widget itself, property animation is usually unnecessary because `ValueAnimation` is more direct and lacks the overhead of looking up properties by name.

## Text Display Widgets

When implementing widgets with text content, besides basic painting logic, you also need to handle issues such as text measurement, layout caching, and style linkage. `Label` is the framework's most typical text widget, and its implementation can serve as a reference template for similar widgets.

### Using `updateLayout()`

`update()` only marks a widget as needing a **repaint** and does not affect the layout system. When text content changes, the desired size of the widget (the return value of `sizeHint()`) usually changes accordingly. At this time, you must call `updateLayout()` simultaneously to trigger the parent widget's layout recalculation:

```cpp
void MyTextWidget::setText(const String &text) {
    if (m_text == text)
        return;
    m_text = text;
    update();        // Trigger repaint
    updateLayout();  // Notify parent layout to recalculate (because sizeHint changed)
}
```

The consequence of calling only `update()` is that the text content has been updated, but the widget size remains the value calculated for the old text, resulting in a messed-up layout.

### Text Measurement and `sizeHint()`

`FontMetrics` is the core tool for text measurement, used to implement `sizeHint()` and `heightForWidth()`:

```cpp
#include "gx_fontmetrics.h"

Size MyTextWidget::sizeHint() const {
    if (m_text.empty())
        return Size{0, int(font().pixelSize() * 1.2f)};
    FontMetrics fm(font());
    // Single-line text: measure width directly
    return Size{fm.width(m_text), int(font().pixelSize() * 1.2f)};
}
```

For multi-line text supporting automatic wrapping, you also need to implement `heightForWidth()` to inform the layout system of the widget's height at a given width:

```cpp
int MyTextWidget::heightForWidth(int width) const {
    if (width == 0) return 0;
    FontMetrics fm(font());
    float lineHeight = font().pixelSize() * 1.2f;
    // boundingRect calculates the actual boundary of text at a given width
    return fm.boundingRect(m_text, width, 1024 * 1024, 0, 0, lineHeight).height();
}
```

If the widget is strictly single-line (does not wrap with width), `heightForWidth()` returns `-1` to indicate that it does not depend on width:

```cpp
int SingleLineWidget::heightForWidth(int) const { return -1; }
```

### Responding to Styles and Size Changes

When style properties like fonts and colors change, text measurement results also change. Override `styleEvent()` to respond to style changes, call the base class implementation to refresh style-related caches, and then trigger layout updates:

```cpp
void MyTextWidget::styleEvent(StyleEvent *event) {
  // Must call base class first; it updates internal style data
    Widget::styleEvent(event);
    // After styles like font change, the return value of sizeHint may change
    updateLayout();
}
```

Similarly, if the widget size changes and there are width-dependent text wrapping calculations, you need to trigger updates in `resizeEvent()`:

```cpp
void MyTextWidget::resizeEvent(ResizeEvent *event) {
    Widget::resizeEvent(event); // Call base class
    update();                   // Repaint content after size change
}
```

::: important
The base class implementations of event handlers like `styleEvent()` and `resizeEvent()` usually have side effects that cannot be omitted and **must be called**. The timing of the call depends on your logic requirements: in most cases, call the base class first, then execute your own logic.
:::

### Overriding `event()`

List all event types that need to be handled, such as `StyleEvent` and `ResizeEvent`, in the template parameters of `EventDispatch` to obtain compile-time checking:

```cpp
bool MyTextWidget::event(Event *event) {
    return EventDispatch<Widget,
        PaintEvent, ResizeEvent, StyleEvent>{}(this, event);
}
```

### Flow Layout and Inline Elements

`setFlowLayout(true)` sets a **container widget** to flow layout mode, with an effect similar to CSS block-level flow. The framework automatically arranges child elements in rows without needing to create independent layout objects via `setLayout()`. `Label` enables this mode in its constructor, allowing itself to act as a `SpanLabel` container (embedding multiple child labels with different styles):

```cpp
Label::Label(Widget *parent) : Widget(parent) {
    setFlowLayout(true);
}
```

`setInlineWidget(true)` is a setting targeted at **child elements**, marking the widget as an inline element so that it embeds into the text stream of the parent container for layout just like text. For example, embedding an icon widget inline within rich text:

```cpp
auto *icon = new ImageBox(label);
// Mixed typesetting with text as an inline element. ImageBox is already inline by default; this is just for illustration.
icon->setInlineWidget(true);
```

When a `Label` is used as a `SpanLabel` container accommodating inline child elements, the layout system automatically coordinates the `Label`'s own text measurement logic and its arrangement of child elements as a container. Both share the same layout mechanism, and developers do not need to manually intervene in this process.

## AbstractScrollArea and Scrollable Widgets

When a widget requires scrolling behavior, you don't need to implement gesture recognition, inertial scrolling, and bounce effects from scratch. Directly inheriting from `AbstractScrollArea` grants these capabilities. Built-in framework controls like `ScrollArea` (list scrolling) and `TextField` (single-line text input) are implemented based on it.

### Basic Structure

Widgets inheriting from `AbstractScrollArea` follow a fixed structure: the widget itself is the "viewport", and inside there is a **content widget** responsible for hosting the actual content. When scrolling, it is the content widget that moves, not the viewport itself.

Complete initialization in the constructor:

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
    setDirection(Horizontal);     // Horizontal scrolling
    setDamping(5);                // Adjust damping (larger value means stronger friction)

    auto *content = new Widget;   // Create content widget
    setContentWidget(content);
}

bool MyTicker::event(Event *event) {
    return EventDispatch<AbstractScrollArea, LayoutEvent>{}(this, event);
}
```

Setting the base class parameter of `EventDispatch` to `AbstractScrollArea` (rather than `Widget`) allows events not handled by the current class (gestures, wheels, resize, etc.) to automatically fall back to `AbstractScrollArea`'s implementation, thereby retaining complete scrolling behavior.

### Configuring Scrolling Parameters

```cpp
setDirection(Vertical);          // Vertical scrolling (default)
setDirection(Horizontal);        // Horizontal scrolling
setDamping(3);                   // Lower damping: stronger inertia, slides further
setDamping(20);                  // Higher damping: weaker inertia, close to no inertia
setScrollBar(true);              // Show scroll bar
setBouncesPolicy(SnapType::SnapEdge);  // Edge bounce policy
```

`AbstractScrollArea` also provides `scrollTo(x, y, behavior)` to programmatically control the scroll position, where `behavior` is `Instant` (jump immediately) or `Smooth` (with animation).

::: tip Inertia Damping
For widgets like `TextField` that require precise control over the scroll position, a higher damping value is usually set to weaken inertia; whereas for widgets like `ScrollArea` focused on browsing, a lower damping can be set for a smoother scrolling experience.

Do not set the damping too low; otherwise, ultra-long-distance scrolling may cause content caching to invalidate, resulting in stuttering.
:::

### Calling the Base Class in Event Dispatch

Sometimes you need to perform extra processing on an event before handing control over to `AbstractScrollArea`'s default implementation. The typical approach is to call the base class method directly inside the handler function:

```cpp
// TextField approach: only forward gestures to the scroll area when there is text
bool TextField::gestureEvent(GestureEvent *event) {
    if (text().empty()) // Ignore directly when there is no text
        return false;
    // Hand over to base class scrolling logic in other cases
    return AbstractScrollArea::gestureEvent(event);
}
```

In this pattern, the base class parameter of `EventDispatch` uses `Widget`, and the current class decides for itself when to call which base class method:

```cpp
bool TextField::event(Event *event) {
    // Use Widget as base class, completely controlling the timing of calls to AbstractScrollArea behaviors by yourself
    return EventDispatch<Widget, GestureEvent, ResizeEvent>{}(this, event);
}
```

### Content Widget Event Filtering

The content widget is responsible for layout and hosting child widgets, but certain events of its own (such as layout requests) sometimes need to be intercepted and customized by the container. Register the container as an event filter for the content widget via `setEventFilter(this)`, and then override `eventFilter()` to handle events of interest:

```cpp
// Register in constructor
content->setEventFilter(this);

// Intercept content widget layout requests
bool MyTicker::eventFilter(Object *receiver, Event *e) {
    if (receiver == contentWidget() && e->type() == Event::Layout) {
        auto *lv = static_cast<LayoutEvent *>(e);
        if (lv->isLayoutRequest()) {
            // Custom layout logic...
            return true; // Return true to prevent the event from propagating further
        }
    }
    // Hand over to base class for other cases
    return AbstractScrollArea::eventFilter(receiver, e);
}
```

::: tip
Unhandled events should be passed back to `AbstractScrollArea::eventFilter()`, which is responsible for interaction with internal mechanisms like scroll bars.
:::

### Setting Inline Widgets

Calling `setInlineWidget(true)` allows a widget to participate in inline layouts, making it suitable for scenarios embedded within text flows. `TextField` is handled this way so it can be embedded inline just like text.

### ScrollArea and Derived Classes

`ScrollArea` is a derived class of `AbstractScrollArea` that adds capabilities such as **index navigation** (`index()`/`setIndex()`), **snap modes**, and **visual effects** on top of scrolling. It is the preferred base class for scenarios like lists and marquees. `Swiper` further adds paging (`pageLength`) and indicators on top of `ScrollArea`, making it suitable for carousel modes and similar scenarios.

These classes usually **do not need further derivation**, and most customization requirements can be met by configuring parameters and mounting peripheral facilities without subclassing.

#### Visual Effects (`VisualEffect`)

`ScrollArea` supports mounting a `VisualEffect` object via `setVisualEffect()`, which applies visual transformations such as opacity, scale, and translation to each child widget before it is painted, thereby achieving dynamic effects during scrolling. The framework has built-in effects:

| Class Name | Effect |
|---|---|
| `FisheyeVisualEffect` | Fisheye effect, center elements enlarged, edges shrunk |
| `FadeVisualEffect` | Edge fade-out, opacity decreases the further it is from the viewport center |
| `CollapseVisualEffect` | Collapse effect, elements gather and shrink towards the top (or bottom) edge |
| `BlendVisualEffect` | Interpolate and transition between two effects by progress |

```cpp
#include "gx_visualeffect.h"

scrollArea->setVisualEffect(make_shared<FisheyeVisualEffect>());
```

To customize effects, inherit from `VisualEffect` and implement the `resolve()` method. `resolve()` receives the target child widget, viewport rectangle, and child widget center point, and returns a `PaintModifier`, in which properties such as `opacity`, `scale`, and `translate` can be set.

Complete parameter descriptions for `ScrollArea` and `Swiper`, as well as how to implement custom `VisualEffects`, are introduced separately in [Scroll Area](./scroll-area.md).

## Widget Tree and Lifecycle

When creating widgets in C++, parent-child relationships are established through the `parent` parameter of the constructor:

```cpp
// When parent is destroyed, child is also destroyed accordingly
auto *parent = new Widget(window);
auto *child  = new ProgressRing(parent);
child->setGeometry(10, 10, 80, 80);
```

Whether you manually `delete` the parent widget or the framework cleans up the widget tree when the application exits, all child widgets are automatically destroyed. You do not need to `delete` child widgets in the destructor.

If delayed destruction is required (for example, inside an event handler function), you can use `deleteLater()`, which destroys the object after the current event handling completes, avoiding issues like "destroying yourself inside a callback."

In the reactive framework, the widget tree is maintained by the component framework, and custom development only requires [registering the widget class](./widget-export.md).

============================================================
FILE_PATH: src/transl/EN/cxxdev/widget-slider-demo.md

# Practical Guide to Custom Widgets

`slider-demo` is a complete example included with the Glyphix SDK, demonstrating how to implement a **custom control**—`WaveSlider`—from scratch in C++. This control adds a wave filling effect and a click ripple animation on top of the standard `Slider`. The example also covers `StyleEngine` customization, building UI interfaces directly in C++, and more.

Using this example as a guide, this article combines the core concepts from the [Widget Development Guide](./widget.md) to fully demonstrate all the steps required to customize a new Widget.

## Example Structure

The file structure of the example is as follows:

```
app/slider-demo/
├── CMakeLists.txt
├── main.cpp           # Application entry point, builds UI directly in C++
├── styleengine.h/.cpp # Custom StyleEngine implementation
└── waveslider.h/.cpp  # WaveSlider control implementation
```

You can directly compile and run the `slider-demo` target to see the effect without needing a frontend project.

### Build Instructions

After [setting up the SDK](sdk-setup.md#preparation), use the following commands to build and run the example:

```bash
mkdir build && cd build
cmake .. && cmake --build . -j
bin/slider-demo
```

::: important Host System
You must build and run this example on a Linux system that supports a desktop environment.
:::

## Building the UI Directly in C++

In `main.cpp`, the application's UI is completely constructed using C++ code within the constructor, in a style similar to Qt Widgets or LVGL: child controls are created via `new` and passed a pointer to their parent control, eliminating the need for declarative templates.

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

`Application` accepts a platform backend object (`BSPPlatform`) and a resolution. `Window` is the root control; when `setFlowLayout(true)` is enabled, its child controls automatically arrange themselves according to a flow layout.

`setStyleEngine` attaches a custom style engine. This is optional (the default style will be used otherwise). You only need to provide your own implementation when you need to customize control appearances (such as the modification of `Switch` described below).

### The `MyWidget` Class

`MyWidget` inherits from `ScrollArea` and creates and adds child controls in its constructor:

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

Child controls are declared as member variables and automatically initialized upon construction (the parent-child relationship is established in `addItem`). The lifecycle of these member variables is managed by `MyWidget`, requiring no manual `delete`.

`ScrollArea` provides out-of-the-box capabilities such as scrolling, momentum, and bouncing, meaning `MyWidget` does not need to implement any custom scrolling logic.

::: tip The Purpose of `addItem()`
In general, you can directly attach a child control to a parent control using `setParent()`. However, `ScrollArea` actually contains a dedicated internal content container (`contentWidget()`). Regular elements cannot be added directly to a `ScrollArea`; instead, they must be added to the content container using `addItem()`.

For simple containers, `setParent()` and `addItem()` have the same effect. However, for specialized containers like `ScrollArea`, you **must** use `addItem()` to add elements.
:::

### Signal Connections

States are synchronized between controls via signal connections:

```cpp
m_slider.changed.connect(this, &MyWidget::onSlider);
m_switch.checked.connect(this, &MyWidget::onSwitch);

// Two-way synchronization of the values of two Sliders
waveSlider->changed.connect<AbstractSlider>(&m_slider, &Slider::setValue);
m_slider.changed.connect<AbstractSlider>(waveSlider, &WaveSlider::setValue);

// Switch toggles the wave mode of WaveSlider
m_switch.checked.connect(waveSlider, &WaveSlider::setWaveMode);
```

::: tip Signal Usage
The syntax for signal connections is `signal.connect(receiver, &Type::method)`. When the signatures of `Slider::setValue` and `WaveSlider::setValue` do not match exactly, you can use template parameters to declare a common base class (`AbstractSlider`) to resolve ambiguity.

When you are unsure of the actual type a slot function belongs to, you can use IDE tooltips to check. For example, when checking `Slider::setValue`, the IDE will typically show:
```cpp
public method
void setValue(int value) in class AbstractSlider 
```
This indicates that `setValue` is actually declared in `AbstractSlider`. During connection, you must specify `AbstractSlider` to resolve the ambiguity:
```cpp
m_slider.changed.connect<AbstractSlider>(waveSlider, &WaveSlider::setValue);
```
:::

### Styling with StyleModifier

`StyleModifier` is a tool for programmatically setting control styles in C++, with an effect equivalent to configuring them via style properties in a template:

```cpp
StyleModifier m(waveSlider);
m->setSize(120, 300);
m->setMargin(Style::Margin{Length::fromAuto(), 20});
m->setColor(Color{"#35a7ff"});
```

`setColor` sets the foreground color for the `WaveSlider`, which is read within `paintEvent` and used to draw the progress fill color.

## Customizing StyleEngine

The built-in [`Switch`](/components/switch.md) is a fully functional switch control, but its default appearance resembles [Fluent 2](https://fluent2.microsoft.design/components/web/react/core/switch/usage), which may not suit the visual style of a specific device or brand.

`StyleEngine` is the mechanism designed to solve this problem. Device manufacturers can implement their own `StyleEngine` to customize the appearance of all built-in controls while retaining their interaction logic, all without modifying framework code.

A customized `Switch` does more than just swap theme colors; instead, the entire switch animation suite (thumb displacement, color transition, press scaling) is achieved through **programmatic interpolation** rather than pre-recorded frame sequences. This means:

- Animations are completely smooth, with frame rates matching the rendering system;
- Colors and dimensions can be overridden by application developers via style properties—`StyleEngine` provides overridable default values;
- There is no need to prepare different image assets for various resolutions.

### Responsibilities of `StyleEngine`

`StyleEngine` is the core of the Glyphix styling system and is responsible for three things:

1. **Providing a palette**: Global color variables, similar to CSS custom properties, which can be read by all built-in and custom controls.
2. **Painting control appearances (`paint`)**: The visual effects of built-in framework controls (such as `Switch`, `Slider`) are entirely delegated to `StyleEngine::paint()`, which developers can override in derived classes to achieve completely different appearances.
3. **Size hints (`sizeHint`)**: Recommended dimensions for controls in various style states, used as a reference by the layout system.

### Defining MyStyleEngine

Inherit from `StyleEngine` and override `sizeHint()` and `paint()`:

```cpp
class MyStyleEngine : public StyleEngine {
public:
    MyStyleEngine();
    Size sizeHint(StyleOption::Type type, const Widget *widget) const override;
    void paint(Painter &painter, Widget *widget, StyleOption &option) override;
};
```

Set the palette in the constructor:

```cpp
MyStyleEngine::MyStyleEngine() {
    setPalette(SwitchDark,  Color(0xff565656));
    setPalette(SwitchLight, Color(0xff2f5cff));
    setPalette(SwitchThumb, Color(0xffffffff));
}
```

`SwitchDark`, `SwitchLight`, and `SwitchThumb` are predefined semantic color keys in the `StyleEngine` enum. Different theme engines can assign different colors to them, and controls always read them by key name rather than hardcoding color values.

### Overriding `sizeHint()`

`sizeHint()` informs the framework of the **recommended size** for built-in controls under a given style state. Taking `Switch` as an example, its width and height should be proportional to the font pixel size:

```cpp
Size MyStyleEngine::sizeHint(StyleOption::Type type, const Widget *widget) const {
    // The proportion of the customized Switch size can differ from the built-in strategy
    if (type == StyleOption::OptionSwitch) {
        float f = widget->font().pixelSize();
        int d = int(round(f));
        return {int(round(f * SwitchAspectRatio)), d};
    }
    return StyleEngine::sizeHint(type, widget); // Fall back to the base class for other types
}
```

Be sure to call `StyleEngine::sizeHint(type, widget)` at the end of the function to fall back to the default implementation, otherwise other types of controls will receive zero dimensions.

### Overriding `paint()`

`paint()` dispatches to the corresponding drawing logic based on the `option()` type of `StyleOption`, falling back for unhandled types as well:

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

`StyleOptionSwitch` is a derived class of `StyleOption` that adds Switch-specific state fields. It carries two key animation progress values:

- `option.transition`: Switch toggle transition progress, where `0.0` is the closed state, `1.0` is the open state, and intermediate values indicate an ongoing animation.
- `option.scale`: The scaling factor when pressed, used to draw press feedback effects.

Using these two values, smooth state transitions can be implemented within `drawSwitch`:

```cpp
// Interpolate between open and closed colors
color = color.blend(checked.background().color(), option.transition);

// The position of the thumb indicator moves with the transition progress
float pos = option.transition * (box.width() - size - len);
```

`StyleEngine` drives the animation, and developers simply need to interpolate based on progress values within `paint()` to achieve complete transition animations.

::: tip Customizing Only Specific Controls
The default `StyleEngine` implements the drawing logic for all built-in controls, some of which are quite complex. If you are only dissatisfied with the appearance of a subset of controls, you should override only the drawing logic for those controls in your derived class, letting other controls fall back directly to the base class implementation.

You should first consider meeting color customization needs via the palette, and only override `paint()` when completely different visual effects are required.
:::

### Drawing Rounded Capsule Shapes with VectorPath

The background and thumb of the default `Switch` are both rounded capsule shapes. The example uses `VectorPath` combined with two arcs to draw this. This is a more flexible approach than `drawRoundedRect`, making it suitable for scenarios where the radii of the two ends need to be controlled separately:

```cpp
static void indicatorBar(Painter &p, const RectF &rect) {
    float radius = rect.height() * 0.5f;
    float x1 = rect.left() + radius;
    float x2 = rect.right() - radius;
    float y = rect.top() + radius;
    VectorPath path;
    path.arcTo(PointF(x1, y), radius, radius, 90, 270);   // Left semicircle
    path.arcTo(PointF(x2, y), radius, radius, -90, 90);   // Right semicircle
    p.fillPath(path);
}
```

The two arcs connect head-to-tail, and `arcTo` automatically draws connecting lines within the path, eliminating the need for extra `lineTo` calls.

## WaveSlider: A Complete Custom Control Practice

`WaveSlider` is the core of this example, demonstrating the complete development workflow for a custom control. Similar to the `StyleEngine` customization above, the design goal of `WaveSlider` is to **overlay** new visual effects without breaking existing capabilities:

- **Wave filling** mode: The progress area is filled with dynamic waves instead of a standard rectangular progress bar;
- **Click ripple** effect: Generates a diffusing oscillation when pressed, causing the waves to briefly intensify before recovering;
- **`waveMode` property**: Allows switching between wave mode and normal mode at runtime, supporting application-layer binding and property animations;
- **Full fallback compatibility**: When wave mode is disabled, `WaveSlider` directly calls `Slider::paintEvent()` to fall back to the default appearance, reusing all capabilities of the parent class such as dragging and `value`/`changed`, requiring zero code changes on the application side.

### Class Definition and Inheritance

`WaveSlider` inherits from `Slider` (rather than directly from `Widget`), allowing it to reuse `Slider`'s existing gesture dragging logic, properties like `value`/`minimum`/`maximum`, and the `changed` signal:

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

`GX_OBJECT` must be placed at the very beginning of the class definition, as it triggers the meta-object compiler to generate metadata for the class. `GX_PROPERTY` exposes `waveMode` to the property system, making it bindable by the application layer (e.g., `<wave-slider :wave-mode="enabled"/>`) and driven by property animations.

### Member Variables

The runtime state of the control is stored in member variables:

```cpp
private:
    bool  m_waveMode = false;       // Whether currently in wave mode
    float m_rippleProgress = 1.0f;  // Ripple progress [0, 1], initially 1 (inactive)
    float m_waveOffset = 0.0f;      // Wave phase offset [0, 1], driven by animation
    ValueAnimation<float> m_animation;        // Wave loop animation
    ValueAnimation<float> m_rippleAnimation;  // Ripple animation
    friend struct EventTraits<WaveSlider>;    // Allows event dispatch to access protected methods
```

`ValueAnimation<float>` is used directly as a member variable (rather than a pointer), and its lifecycle is managed by `WaveSlider`, requiring no manual `delete`.

### Constructor: Initializing Animations

The constructor configures two animations and sets the orientation:

```cpp
WaveSlider::WaveSlider(Widget *parent) : Slider(parent) {
    // Wave animation: Infinite loop, one full cycle per second
    m_animation.setRepeat(AbstractAnimation::Infinity);
    m_animation.setValueLimits(0.f, 1.f);
    m_animation.setDuration(1000);
    m_animation.value.connect(this, &WaveSlider::onWaveAnimation);
    m_animation.start();

    // Ripple animation: Played once on press, duration 800ms
    m_rippleAnimation.setValueLimits(0.f, 1.f);
    m_rippleAnimation.setDuration(800);
    m_rippleAnimation.value.connect(this, &WaveSlider::onRippleAnimation);

    setVertical(true);  // Vertical slider
}
```

`m_animation` runs continuously after starting, advancing `m_waveOffset` from $0$ to $1$ per frame before looping back to $0$. This value is ultimately converted into the phase offset of the waves, causing them to flow continuously.

`m_rippleAnimation` is triggered only when pressed, playing once and then stopping without setting `Infinity`. The callbacks for the two animations each do only one thing: update state variables and call `update()` to request a repaint.

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

### Event Handling

#### Configuring EventDispatch

`event()` uses [`EventDispatch`](widget.md#handling-events) to route events, with template parameters listing the event types actually handled by the current control to provide compile-time checking:

```cpp
bool WaveSlider::event(Event *event) {
    return EventDispatch<Widget,
        GestureEvent, PaintEvent>{}(this, event);
}
```

#### Handling Gestures: Triggering Ripples

`gestureEvent()` intercepts the start of a `Press` gesture to trigger ripples, delegating all other cases to `Slider`'s gesture handling (which implements dragging to adjust values):

```cpp
bool WaveSlider::gestureEvent(GestureEvent *event) {
    if (!event->isHitTest() && event->gesture()->type() == Gesture::Press) {
        auto g = static_cast<PressGesture *>(event->gesture());
        if (g->isStarted())
            startRipple(g->clientPoint());
    }
    return Slider::gestureEvent(event); // Pass the event onward to Slider
}

void WaveSlider::startRipple(const Point &) {
    m_rippleProgress = 0.f;      // Start from the beginning
    m_rippleAnimation.start();   // Replay
}
```

When `isHitTest()` is `true`, it indicates a hit test (used by the framework to detect whether an event falls on this control) rather than true user interaction, and it should be skipped.

::: tip Regarding `isHitTest()`
Hit testing is a preliminary step in event dispatch. `gestureEvent()` is also called during the hit-test phase, but no side effects (such as starting animations) should occur at this time. Always check `!event->isHitTest()` before processing interaction logic.
:::

#### Style Reading Interface

`paintEvent()` reads the style data corresponding to the control. Here are two relevant interfaces introduced:

- `style()` / `style(Styles::Xxx)` returns the `Style` object for a specific style pseudo-class of the current control, from which properties such as colors and backgrounds can be read;
- `se->palette(StyleEngine::Xxx)` reads global palette colors from `StyleEngine`, acting as a fallback when the control has no custom colors set.

Working together, they implement the logic: "use custom configuration if available, otherwise fall back to the theme's default color":

```cpp
auto contentStyle = style(Styles::Content);
p.setBrush(contentStyle.hasProperty(style::Background)
               ? contentStyle.background()
               : se->palette(StyleEngine::ProgressRange));
```

### Painting Implementation

`paintEvent()` is the core of WaveSlider. It decides which rendering path to take based on `m_waveMode`:

```cpp
void WaveSlider::paintEvent(PaintEvent *event) {
    discard(event);  // PaintEvent itself carries no useful info; explicitly discard to eliminate compiler warnings

    if (!isWaveMode())
        return Slider::paintEvent(event);  // Normal mode: directly call parent class painting

    auto se = App()->styleEngine();
    RectF box = rect();
    float radius = min(box.width(), box.height()) * 0.5f;
    float progress = sliderRange ? float(value() - minimum()) / float(sliderRange) : 0.f;

    Painter p(this);

    // Draw background (empty track)
    p.setBrush(/* Background color */);
    p.fillRoundedRect(box, radius);

    // Draw wave fill (progress area)
    p.setBrush(/* Foreground color */);
    VectorPath path;
    buildWaveFillPath(path, box, radius, progress, m_waveOffset, m_rippleProgress);
    if (!path.isEmpty())
        p.fillPath(path);
}
```

The entire rendering is split into two steps: first, draw the full background rounded rectangle using `fillRoundedRect`, then draw the wave fill on top of it using `fillPath`, layering the two to form a "progress bar with waves."

#### Wave Path Generation

`buildWaveFillPath()` is an independent helper function (outside the class) responsible for constructing the wave path under given geometric constraints:

```cpp
static void buildWaveFillPath(VectorPath &path, const RectF &box, float radius,
                              float progress, float waveOffset, float rippleProgress)
```

Its core logic is divided into three steps:

1. **Calculate water level and amplitude**: `waterLevel` rises from the bottom proportionally to `progress`; amplitude depends on the aspect ratio and is constrained to stay far enough away from the top and bottom arcs to prevent the wave from going out of bounds.
2. **Sample the waveform**: Sample uniformly from left to right, calculating the $y$ value for each $x$ coordinate.
   The waveform is composed of three overlapping parts: a regular sine wave (controlled by `m_waveOffset`) + ripple gain (controlled by `m_rippleProgress` for attenuation oscillation) + rounded corner constraints (ensuring the path does not exceed the boundaries of the rounded rectangle).
3. **Close the path**: Return along the bottom edge from the top of the wave to the bottom of the rounded rectangle, forming a closed polygon for `fillPath` to fill.

The algorithm details serve as an educational visual demonstration. In actual products, this can be replaced with any custom path generation logic according to design requirements.

::: tip Efficiency of Path Drawing
The number of sample points (`sampleCount`) is proportional to the control width (approximately one point every `4px`), and the performance cost is acceptable at typical screen resolutions. If the CPU is weaker, you can reduce the sampling density or switch to Bézier curve approximation.
:::

### The `waveMode` Property

The implementation of `setWaveMode()` is simple: update the member value and mark for a repaint when the state changes:

```cpp
void WaveSlider::setWaveMode(bool enabled) {
    if (m_waveMode != enabled) {
        m_waveMode = enabled;
        update();
    }
}
```

The declaration of the `GX_PROPERTY` macro makes `waveMode` a framework-visible property:

```cpp
GX_PROPERTY(bool waveMode, get isWaveMode, set setWaveMode)
```

No `signal` field is declared here because its value is typically driven by the user rather than triggered by interaction.

### Production-Grade Optimizations

The implementation of `WaveSlider` is primarily geared towards educational demonstrations and lacks certain optimizations, such as:
- The wave animation plays continuously, triggering `update()` and repeatedly invoking `paintEvent()` even when `waveMode` is disabled;
- It only supports vertical sliders and is not adapted for horizontal modes (which can be implemented as needed by product requirements);
- It fixedly draws capsule-shaped tracks, whereas actual products might require rounded rectangles or other shapes.

## Component Collaboration

The following shows the runtime collaboration of various components in `slider-demo`:

```
User presses screen
    ├─ WaveSlider::gestureEvent() detects Press.isStarted()
    │       └─ startRipple() resets m_rippleProgress and starts m_rippleAnimation
    └─ Slider::gestureEvent() continues processing, adjusts value based on touch point
            └─ changed signal emitted → MyWidget::onSlider() updates Label text

Per-frame render loop
    ├─ m_animation continuously advances m_waveOffset (0→1 loop)
    │       └─ update() → paintEvent() repaints waves with new offset
    └─ m_rippleAnimation advances m_rippleProgress (0→1 finishes and stops)
            └─ update() → paintEvent() repaints ripple decay with new rippleProgress

Switch toggle
    └─ waveSlider->setWaveMode(true/false)
            └─ update() → paintEvent() switches to normal mode or wave mode
```

Signal connections are established once in `MyWidget`'s constructor. Afterward, execution is entirely driven by events and signals at runtime, with no direct calls between controls.

## Summary of Key Patterns

Through `slider-demo`, we can summarize typical patterns for implementing custom controls in Glyphix:

| Requirement | Approach |
|---|---|
| Inherit an existing control, reuse its interaction logic | Inherit the corresponding base class (e.g., `Slider`), control base class fallback in `EventDispatch` |
| Custom drawing | Implement `paintEvent()`, call `Slider::paintEvent()` as a fallback when `isWaveMode()` is `false` |
| Continuously looping animation | `ValueAnimation::setRepeat(Infinity)` |
| One-shot triggered animation | Store state variables, call `anim.start()` in `gestureEvent()` to replay |
| Expose properties to the application layer | `GX_PROPERTY` macro, paired with getters/setters and optional signals |
| Read user color schemes or theme colors | Check via `style().hasProperty()` and fall back to `se->palette()` |
| Customize global control appearance | Inherit `StyleEngine`, override `paint()` and `sizeHint()` |

These patterns are elaborated in the [Widget Development Guide](widget.md); `slider-demo` serves as their comprehensive practical application.

## Comparison with Other GUI Frameworks

::: important Positioning of C++ Control Development
The mainstream development approach in Glyphix is building interfaces using declarative templates via [`.ux` Single File Components](../tutorials/quick-orientation.md). The purpose of C++ control development is to implement **low-level control libraries on the device side** (such as the vendor-customized `WaveSlider`), which are subsequently used by frontend application layers through templates and data binding. Building complete UIs directly in C++ (like the demonstration in `main.cpp`) is **possible within the framework, but not the recommended workflow**, and related toolchain support (debugging, hot reloading, layout previews) is less mature than at the application layer.

Therefore, when evaluating Glyphix's overall development efficiency, the frontend application layer should serve as the benchmark; the C++ control development experience discussed in this section represents only the development scenario for low-level control libraries.
:::

In its mental model, Glyphix's C++ control development is closer to Qt Widgets than to LVGL: the signal mechanism, property macros, inheritance-based extension, and the naming and division of responsibilities for `paintEvent` all correspond closely to Qt Widgets. Developers with a Qt background can quickly build an intuition.

LVGL developers will need to transition from a C handle-style paradigm to a C++ OOP style, which represents a larger gap. However, core paradigms like control tree organization and triggering repaints via `update()` remain common. Using `slider-demo` as a reference, this section details the similarities and key differences between these frameworks.

### Similarities

Whether Qt Widgets, LVGL, or Glyphix, they share a set of proven UI framework core paradigms:

- **Control Tree**: UIs are organized in a parent-child tree structure, where child control coordinates are relative to the parent control. `MyWidget(&window)` semantically corresponds to Qt's `new QWidget(&parent)` and LVGL's `lv_obj_create(parent)`.
- **Custom Drawing**: Control appearance is implemented by "overriding" drawing methods. Qt overrides `paintEvent(QPaintEvent *)`, LVGL registers an `LV_EVENT_DRAW_MAIN` callback, and Glyphix implements `paintEvent(PaintEvent *)`. The design philosophy across all three is identical.
- **Signal/Slot Mechanism**: State changes are communicated between controls via signals, and receivers respond using member functions.
  - Glyphix: `m_slider.changed.connect(this, &MyWidget::onSlider)`;
  - Qt: `connect(&slider, &QSlider::valueChanged, this, &MyWidget::onSlider)`;
  - LVGL: Achieves similar functionality through event callback functions.
- **Inheritance and Reuse**: Extending existing controls is done via inheritance. `WaveSlider : public Slider` reuses all dragging and value-fetching logic of the parent class, overriding only the drawing portion, which aligns with the design of most OOP GUI frameworks.
- **On-Demand Repainting**: When states change, `update()` is called to mark dirty regions, and the framework performs a unified repaint in the next frame rather than drawing immediately. Mainstream frameworks adopt this strategy to avoid redundant intra-frame drawing.

### Differences from Qt Widgets

#### Event Dispatch

Qt dispatches events through virtual function overrides, where each event method is `virtual` and subclasses override them using `override`:

```cpp
// Qt
class MySlider : public QSlider {
    void paintEvent(QPaintEvent *event) override { ... }
    void mousePressEvent(QMouseEvent *event) override { ... }
};
```

Glyphix's event handling functions like `paintEvent()` and `gestureEvent()` are **not virtual functions** and cannot use `override`. Event routing is completed at compile time by `EventDispatch`:

```cpp
// Glyphix
bool WaveSlider::event(Event *event) {
    return EventDispatch<Widget, GestureEvent, PaintEvent>{}(this, event);
}
// paintEvent and gestureEvent are both regular member functions, without override
```

This avoids the indirect jumps of virtual functions, offering performance advantages in high-frequency event processing on embedded devices. At the same time, the template parameter list serves as compile-time documentation and missing-item checking. If you declare handling for `PaintEvent` but forget to implement `paintEvent()`, the compiler will throw an error instead of silently falling back to the base class.

#### Object and Property Systems

Qt uses the `Q_PROPERTY` macro along with the MOC (Meta-Object Compiler) to generate property metadata; Glyphix uses `GX_PROPERTY` alongside `GX_OBJECT`. The mechanisms are similar, but the generation methods and runtime interfaces differ:

```cpp
// Qt
Q_PROPERTY(int value READ value WRITE setValue NOTIFY valueChanged)
// Glyphix
GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
```

Both support driving animations via property name strings (`QPropertyAnimation` / `PropertyAnimation`). However, when implementing controls themselves, Glyphix more strongly recommends using `ValueAnimation<T>` directly to avoid the overhead of property name lookups and conflicts with application-layer-driven property animations.

#### Signals and Slots

As described in the [Object System](object-system.html#signals-signal), Glyphix also has a signal mechanism, but it is closer to `boost::signals2` and does not rely on MOC-generated code. This is an intentional design choice, as the [build systems](sdk-setup.md#other-build-systems) in the Glyphix ecosystem are somewhat fragmented, and we assume downstream consumers do not use a meta-object compiler at all.

#### Styling and Appearance Customization

Qt provides two paths for customizing control appearances: subclassing `QStyle` (complex) or QSS style sheets (CSS-like strings parsed at runtime). Glyphix uses `StyleEngine`: manufacturers implement a `StyleEngine` subclass, drawing all built-in control appearances in C++ code within `paint()` and providing recommended sizes in `sizeHint()`. This approach is well-suited for global system-level style customization rather than localized style adjustments for individual controls.

For styling individual controls, Glyphix uses the `StyleModifier` helper object to assign values programmatically rather than commonly using CSS strings:

```cpp
StyleModifier m(waveSlider);
m->setSize(120, 300);
m->setColor(Color{"#35a7ff"});

// Inline style strings are also supported
waveSlider->setStyle(Style{"background-color: #35a7ff; color: #cce;"});
```

Glyphix's style and layout properties are set more through style properties than by directly calling control methods. This is because C++ is primarily positioned for low-level control library development rather than directly facing application development.

#### Memory and Lifecycles

Under Qt's parent-child control ownership model, child controls are destroyed by their parent after `new QWidget(parent)`. Glyphix also supports this pattern (`new WaveSlider` followed by `addItem()`), but it also recommends declaring child controls as member variables (such as `m_label` and `m_slider` in `MyWidget`). Their lifecycles are automatically managed along with the host object, requiring no manual `delete` and not relying on parent-child tree destruction mechanisms.

### Differences from LVGL

#### Programming Model

LVGL is a framework implemented in C, where controls are operated via `lv_obj_t *` handles, and function naming typically follows the `lv_<type>_<operation>()` convention:

```c
// LVGL
lv_obj_t *slider = lv_slider_create(parent);
lv_slider_set_value(slider, 50, LV_ANIM_ON);
lv_obj_add_event_cb(slider, my_event_cb, LV_EVENT_VALUE_CHANGED, NULL);
```

Glyphix is a native C++ OOP framework where methods are called through objects, and `this` naturally carries context:

```cpp
// Glyphix
auto *slider = new Slider(parent);
slider->setValue(50);
slider->changed.connect(this, &MyWidget::onSlider);
```

For LVGL developers, the main change here is not capability itself, but expression: whereas previously you called functions outside of object handles, you now organize state, events, and drawing logic inside control classes. The type system also helps you avoid certain handle-type misuses at compile time.

#### Event System

LVGL's event handling typically receives multiple events through a single callback function, using `lv_event_get_code()` inside the callback to branch:

```c
// LVGL
static void event_cb(lv_event_t *e) {
    lv_event_code_t code = lv_event_get_code(e);
    if (code == LV_EVENT_PRESSED) { ... }
    else if (code == LV_EVENT_VALUE_CHANGED) { ... }
}
```

Glyphix dispatches events to independent handler functions based on event type. Different events are completely isolated, and their parameters carry type-correct data:

```cpp
// Glyphix
bool WaveSlider::gestureEvent(GestureEvent *event) { ... }
void WaveSlider::paintEvent(PaintEvent *event) { ... }
```

Furthermore, Glyphix's `isHitTest()` mechanism has no direct equivalent in LVGL. LVGL can handle similar issues via `LV_EVENT_HIT_TEST`, but typically still requires manual branching within the same callback.

::: tip Glyphix's Internal Event Dispatch Mechanism
`EventDispatch` is internally implemented as a switch-case dispatcher, but we do not recommend developers write manual switch branches. Instead, always use the fixed `EventDispatch<Widget, ...>{}(this, event)` pattern to facilitate code review.
:::

#### Animations

LVGL animations are configured via the `lv_anim_t` struct, with target values passed through function pointers and `void *` user data:

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

Glyphix's `ValueAnimation<T>` determines interpolation types at compile time via template parameters, eliminating `void *` casting through signal connections:

```cpp
// Glyphix
m_rippleAnimation.setValueLimits(0.f, 1.f);
m_rippleAnimation.setDuration(800);
m_rippleAnimation.value.connect(this, &WaveSlider::onRippleAnimation);
```

`ValueAnimation<T>` has built-in interpolation support for composite types like `Color`, `Point`, and `Transform`, whereas LVGL natively supports only integer ranges, requiring developers to implement their own interpolation callbacks for composite types.

#### Vector Path Drawing

LVGL's drawing APIs focus primarily on basic primitives like rectangles and arcs. Vector path support (`lv_draw_vector`) is a relatively recent addition, with interfaces that are relatively low-level. Glyphix's `VectorPath` is a standard path-building interface where `moveTo`, `lineTo`, `arcTo`, `conicTo`, and `cubicTo` fully cover common curve types. The waves in `WaveSlider` rely entirely on this interface without requiring additional graphics libraries.

#### Memory and Lifecycles

Both support object tree management: child controls are attached under a parent control, and child objects are destroyed when the parent object is destroyed.

Glyphix also allows child controls, animations, and runtime states to be written directly as class members, managed automatically by C++ RAII. For example, `m_label` and `m_slider` in `MyWidget`, as well as the two `ValueAnimation<float>` instances in `WaveSlider`, can be constructed and destructed along with the host object, freeing you from organizing state around handles, `user_data`, and callback contexts like in LVGL.

============================================================
FILE_PATH: src/transl/EN/cxxdev/sdk-setup.md

# SDK Project Configuration

Glyphix is distributed to device manufacturers in the form of pre-compiled libraries. This article describes how to configure the build environment in an SDK project to develop Native Modules, Native Widgets, or platform adaptation code on top of it.

### Prerequisites

Before you begin, ensure that the following are installed:
- CMake 3.14 or higher
- A C++ compiler supporting C++14 (GCC, Clang, or MSVC)
- The Glyphix meta-object compiler `meta` (must match the SDK version; see below for how to obtain it)
- A cross-compilation toolchain (if building for embedded targets)

::: tip System Requirements
- The MSVC toolchain requires Visual Studio 2022 or higher.
- For Linux, a distribution with a desktop environment, such as Ubuntu 22.04 or higher, is recommended.
- Ubuntu 20.04 is not recommended because its package versions are generally too old, frequently requiring manual installation of newer software.
- Environments without a graphical interface, such as WSL or Docker, will not be able to run simulators and GUI examples.
- Currently, the host environment only provides Linux pre-compiled libraries; pre-compiled libraries for Windows and macOS are not yet ready.
:::

## SDK Package Structure

The extracted SDK contains the following directories:

```
glyphix-sdk/
├── libs/
│   └── <target-triple>/       # Pre-compiled libraries organized by target triple
│       ├── include/           # Glyphix header files (gx_*.h)
│       └── lib/               # Static libraries (libglyphix-core.a, etc.)
├── cmake/
│   ├── GlyphixSDK.cmake       # Main SDK configuration script
│   ├── meta.cmake             # Meta-object compiler integration (glyphix_add_meta_objects)
│   ├── cross-compile.cmake    # Cross-compilation toolchain loading
│   ├── arch/                  # Compilation parameters for various architectures (mips-linux-gnu, cortex-m33, etc.)
│   └── toolchain/             # CMake toolchain files for various toolchains
├── wrapper/                   # Platform adaptation layer (host implementations for network, filesystem, etc.)
├── app/                       # Example application entries (emulator, async, etc.)
└── vendor/                    # Third-party dependency libraries
```

### `libs/<target-triple>/`

The SDK's pre-compiled libraries are distinguished by platform using **target triples** as directory names, for example:

- `x86_64-linux-gnu/`: 64-bit Linux host development/simulation
- `mips-linux-gnu/`: MIPS Linux embedded target
- `cortex_m55-none-gnu/`: Cortex-M55 bare-metal target

The `include/` directory contains all Glyphix public header files, all prefixed with `gx_`. The `lib/` directory contains static libraries, with core libraries including:

| Library File | Description |
|:---|:---|
| `libglyphix-core.a` | Core framework (object system, widget tree, events, etc.) |
| `libglyphix-widgets.a` | Built-in widget library |
| `libglyphix-reactive.a` | Reactive framework (JavaScript bridge layer) |
| `libglyphix-platform.a` | Platform abstraction layer interface |
| `libglyphix-service.a` | System service layer |

::: tip Pre-compiled Vendor Libraries
The SDK distribution package also contains some pre-compiled third-party libraries, such as `libfreetype.a`. For convenience, we do not distribute the source code of these libraries directly, but you can choose to build them directly from source instead of using the pre-compiled libraries.
:::

## Getting Started

### Configuring the Meta-Object Compiler

The `meta` meta-object compiler is distributed separately from the SDK as an independent archive. Extracting it yields two directories: `bin/` and `lib/`. **Both must be kept in the same directory**, as the `meta` executable depends on the runtime libraries in `lib/`.

On Linux and macOS, it is recommended to extract it to `/usr/local` so that `meta` is automatically in your `PATH`:

::: code-tabs#bash

@tab Linux

```bash
sudo tar -xJf glyphix-meta-vX.X-linux-x86_64.tar.xz -C /usr/local
```

@tab macOS

```bash
sudo tar -xJf glyphix-meta-vX.X-darwin-arm64.tar.xz -C /usr/local
```

:::

Alternatively, you can extract it to any directory and add its `bin/` directory to your `PATH`. Once completed, verify that it is available with the following command:

```bash
meta --version
```

If you prefer not to modify your `PATH`, you can explicitly specify the full path to the executable during CMake configuration using `-DGX_META=/path/to/bin/meta`.

## Configuring CMakeLists.txt

### Minimal Configuration

::: tip
The CMake configuration introduced in this section resembles the standard example template of the Glyphix SDK project, which you can refer to directly from the SDK source files.
:::

Below is a minimal runnable `CMakeLists.txt` demonstrating the standard configuration skeleton for a project:

```cmake
cmake_minimum_required(VERSION 3.14)

# Must be loaded before project() so that the toolchain is in place when project() detects compilers
include(cmake/cross-compile.cmake)

project(my_glyphix_app)
set(CMAKE_CXX_STANDARD 14)

# Load the Glyphix SDK (sets header paths, link directories, and the glyphix::sdk target)
include(cmake/GlyphixSDK.cmake)

add_subdirectory(vendor)  # Third-party dependencies (if any)
add_subdirectory(src)     # Your source code
```

In `src/CMakeLists.txt`, create a target and link the SDK:

```cmake
add_executable(my_app
  main.cpp
  my_module.cpp
  my_widget.cpp
)

# Link the Glyphix SDK
target_link_libraries(my_app PRIVATE glyphix::sdk)

# Generate metadata for header files containing GX_OBJECT
glyphix_add_meta_objects(my_app
  my_module.h
  my_widget.h
)
```

### Registering Meta Objects (`glyphix_add_meta_objects`)

As mentioned in the [Object System](./object-system) documentation, any class declaring `GX_OBJECT` must be registered with the build system so that the meta-object compiler can generate the corresponding `*_meta.cpp` file for it. `glyphix_add_meta_objects()` is the CMake function that accomplishes this step:

```cmake
glyphix_add_meta_objects(<target> [header1.h header2.h ...])
```

It accepts the target name and a set of **header file** paths as arguments. For each header file, the `meta` tool generates a corresponding `*_meta.cpp` in the `meta/` subdirectory of the build directory and automatically adds it to the target's source file list for compilation.

**Example:** Suppose your project has the following structure:

```
src/
├── CMakeLists.txt
├── main.cpp
├── sensors/
│   ├── step_counter.h       # Contains GX_OBJECT
│   └── step_counter.cpp
└── widgets/
    ├── activity_ring.h      # Contains GX_OBJECT
    └── activity_ring.cpp
```

The corresponding `CMakeLists.txt`:

```cmake
include(${CMAKE_CURRENT_SOURCE_DIR}/../cmake/meta.cmake)

add_executable(my_app
  main.cpp
  sensors/step_counter.cpp
  widgets/activity_ring.cpp
)
target_link_libraries(my_app PRIVATE glyphix::sdk)

glyphix_add_meta_objects(my_app
  sensors/step_counter.h
  widgets/activity_ring.h
)
```

::: tip Pass Header Files Only, Not .cpp Files
`glyphix_add_meta_objects()` only requires **header files** (`.h`) containing `GX_OBJECT` declarations. The meta-object compiler reads the macro declarations in the header files to generate code and does not need to parse implementation files. Conversely, `.cpp` files must not define classes containing `GX_OBJECT`.
:::

::: warning Do Not Omit Registration
If a class declares `GX_OBJECT` but is not registered via `glyphix_add_meta_objects()`, it will result in a **linker error** (symbols such as `staticMetaObject` cannot be found). Remember to update `CMakeLists.txt` whenever you add a new header file containing `GX_OBJECT`.
:::

### The `glyphix::sdk` Interface Target

`GlyphixSDK.cmake` defines the `glyphix::sdk` CMake interface library target, which encapsulates all linking dependencies of the SDK. In your `CMakeLists.txt`, you only need to link this single target:

```cmake
target_link_libraries(my_target PRIVATE glyphix::sdk)
```

Internally, this is equivalent to:

```cmake
# Pseudo-code — actually managed automatically by GlyphixSDK.cmake
target_include_directories(... ${GLYPHIX_INCLUDE_DIRS} wrapper/include)
target_link_libraries(... -Wl,--start-group ${glyphix-*.a} glyphix-wrapper -Wl,--end-group)
target_link_libraries(... m pthread dl)  # UNIX system libraries
```

Wrapping static libraries with `-Wl,--start-group ... -Wl,--end-group` is done to resolve circular dependency linking issues between static libraries on embedded platforms.

::: tip Link Order Issues
If your project contains its own static libraries (e.g., `add_library(my_module STATIC ...)`), they should be linked **inside** `glyphix::sdk`, otherwise the scope of `--start-group` will not cover them, potentially causing linker errors. The method is to append your static library path after the `GLYPHIX_LIBS` variable in `GlyphixSDK.cmake` is defined and before the `glyphix-sdk` target is created, or directly have the final executable link both `my_module` and `glyphix::sdk` and manually specify `--start-group`.
:::

## Host Build

Host builds are used to run Glyphix example programs on your development machine, allowing you to quickly verify widget and module logic without connecting hardware.

```bash
mkdir build && cd build
cmake -G Ninja ..
cmake --build .
```

The `app/` directory of the SDK contains multiple examples, with each subdirectory corresponding to an independent executable target. For example:

| Subdirectory | Build Artifact | Description |
|:---|:---|:---|
| `app/emulator/` | `demo` | Simulator with GUI, depends on the MiniFB window backend |
| `app/async/` | `async-demo` | Headless asynchronous service example, demonstrating Native Modules and asynchronous callbacks |

`GlyphixSDK.cmake` automatically detects the host compiler's target triple (via `gcc -dumpmachine` or `clang -dumpmachine`) and uses it as a key to look up the corresponding pre-compiled libraries in the `libs/` directory. For example, on an x86_64 Linux development machine, it automatically resolves to `libs/x86_64-linux-gnu/`.

If the automatically detected target triple does not match the actual library directory, you can specify it manually:

```bash
cmake -G Ninja -DTARGET_TRIPLE=x86_64-linux-gnu ..
```

If you only need to build a specific example, you can specify the target name:

```bash
cmake --build . --target demo
cmake --build . --target async-demo
```

## CMake Cross-Compilation

For embedded targets, you need to specify the target architecture using the `-DARCH` parameter. The SDK presets the following architecture configurations:

| `-DARCH` Value | Target Platform | Toolchain Prefix |
|:---:|:---:|:---:|
| `mips-linux-gnu` | MIPS Linux | `mips-linux-gnu-` |
| `cortex_m33-gnu` | ARM Cortex-M33 (GNU) | `arm-none-eabi-` |
| `cortex_m7-gnu` | ARM Cortex-M7 (GNU) | `arm-none-eabi-` |

### MIPS Linux Example

```bash
export MIPS_TOOLCHAIN_DIR="/opt/mips-gcc720-glibc229"

mkdir build-mips && cd build-mips
cmake -G Ninja .. \
  -DARCH=mips-linux-gnu \
  -DMIPS_TOOLCHAIN_DIR="$MIPS_TOOLCHAIN_DIR" \
  -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

If the toolchain is already in your `PATH` (i.e., `mips-linux-gnu-gcc` can be invoked directly), `-DMIPS_TOOLCHAIN_DIR` can be omitted, and CMake will locate it automatically.

### ARM Cortex-M Example

```bash
mkdir build-cm33 && cd build-cm33
cmake -G Ninja .. \
  -DARCH=cortex_m33-gnu \
  -DARM_TOOLCHAIN_DIR="/opt/arm-none-eabi-gcc" \
  -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

During cross-compilation, `GlyphixSDK.cmake` does not attempt to automatically detect the target triple—architecture files (such as `cmake/arch/cortex_m33-gnu.cmake`) directly set `TARGET_TRIPLE`, pointing to the correct library directory.

### Supported Target Architectures

The SDK provides pre-compiled libraries only for the architectures listed in the table above. If your target platform is not among them, you need to contact Glyphix to obtain an SDK package for the corresponding architecture, and you cannot add support on top of the existing SDK by yourself.

## Other Build Systems

While the SDK uses CMake as its primary build system, Glyphix also provides support for other build systems to partner manufacturers. This typically involves just importing the pre-built SDK libraries and header files, and adding porting layer source files.

### Project Limitations

This approach is suitable for projects that only require standard SDK features. Once custom widgets, Native Modules, or other capabilities are needed, you must introduce the `meta` meta-object compiler to generate the necessary binding code. CMake is currently the only supported build system for this.

Several alternative solutions are available:
1. Build custom code using the SDK CMake project, and then link the generated libraries into your main project.
2. Build custom code using the SDK CMake project, and then include the generated source files (`*_meta.cpp`) into your main project.
3. Call the `meta` tool directly within your build system to generate binding code.

Among these, the Glyphix SDK itself is built using Method 1. However, this is not suitable for downstream manufacturers' internal development workflows because it requires maintaining a separate project outside of the main firmware project and linking the generated binary libraries back to the main project, which creates severe version management issues.

Method 3 is also generally undesirable because manufacturers typically do not want to introduce an external tool into their main project's build system.

### Recommended Approach

Therefore, Method 2 is recommended. This approach copies the source code; although it requires manual operations, it is easy to audit and integrate into existing build pipelines. You can build custom code in the SDK's CMake project to generate `*_meta.cpp` files, then copy these files into your main project and compile them within your main project's build system.

Another limitation of this approach is that the custom source files must be able to successfully build within the SDK project environment. Specifically, this requires them to be buildable independently of the main project, which includes:
- Include paths and preprocessor definitions must be set correctly, and the header files of custom components must not include main-project-specific header files.
- It is best if the `.cpp` files of custom components can also compile successfully; while this does not affect the generation of `*_meta.cpp` files, it facilitates rapid iteration and debugging in the host environment.

::: tip
This is generally not an issue for most [custom widgets](widget.md). It may be a bit more cumbersome for [Native Modules](native-module.md), and care should be taken: header files declaring `GX_OBJECT` should not include main-project-specific header files.
:::

============================================================
FILE_PATH: src/transl/EN/cxxdev/applet-install-flow.md

# Application Installation Workflow

Glyphix is an application framework designed for embedded devices. After a device leaves the factory, end users or manufacturers may still need to add applications to it—much like installing apps on a smartphone. However, on resource-constrained MCUs, what "installing an application" specifically means and how the framework finds and launches it is not as universally understood as on mobile phones.

This document covers the complete lifecycle of an application package on a device: Installation $\rightarrow$ Launch $\rightarrow$ Uninstallation, and explains how directory configuration affects app discovery, updates, and uninstallation.

## "Installing an Application" on a Device

A Glyphix application is delivered as a `.pkg` file—a read-only resource container that houses the application's manifest (`manifest.json`), JavaScript code, images, and other assets. The application is not unpacked at runtime; the framework reads files directly from the `.pkg` on demand.

**Installing** an application essentially involves two actions: placing the `.pkg` file into a directory scanned by the framework, and registering its package name in the package database. Once registered, the framework can locate the corresponding `.pkg` by its package name and launch it. **Uninstalling** is the reverse operation: deleting the `.pkg` file, cleaning up data generated by the application, and unregistering it from the database.

::: tip Resource Bundle Format
The runtime uses the complete `.pkg` resource file instead of an extracted directory. This bundle model is also common in game engines because application resource packs are read-only rather than writable. The bundle model reduces file system fragmentation and prevents a large number of small files from excessively consuming file system inodes.
:::

Two roles are involved here, and this tutorial is targeted at the latter:
- **Application Developer**: Writes applications in JavaScript, builds `.pkg` files using the `gx build` command, and delivers them.
- **Platform Developer**: Integrates the Glyphix runtime on the device, configures the directories where applications are stored, and calls installation and launch APIs in C++. You are provided with a `.pkg` file, and your goal is to get it running.

::: tip
This tutorial assumes you already have a running Glyphix platform skeleton (`Application` + `JsVM` + `AppletKit`). If you do not, please refer to the `examples/emulator` sample provided with the SDK.
:::

## Preparation

Before getting started, make sure the following conditions are met:

- A running Glyphix platform. The minimal skeleton is shown below; all subsequent operations will take place within this context.
- A `.pkg` file ready for installation. You can obtain one from an application developer or build a sample app yourself using `gx build`. This tutorial assumes the file name is `com.example.demo.pkg` and the package name is `com.example.demo` (the package name is specified in the app's [`manifest.json`](/framework/application/manifest.md#package)).
- A writable partition on the device to store `.pkg` files and application runtime data. The notation `/data` will be used below to represent this partition.

A simple Glyphix platform skeleton looks like this (this is not pseudo-code, it is really this simple):

```cpp
#include "gx_application.h"
#include "gx_appletkit.h"
#include "gx_jsvm.h"
#include "gx_widget.h"

using namespace gx;

int main() {
    Application app{new MyPlatform}; // Platform adaptation, needs to be connected according to the device
    JsVM vm;                         // JavaScript runtime
    Widget window;                   // Parent window for all applications
    AppletKit kit(&window, "/pkgs.db"); // The second parameter is the package database path
    // ...Configuration and installation code for this tutorial goes here
    return app.exec();
}
```

::: tip The Second Parameter of `AppletKit`
It points to a "package database" file (such as `/pkgs.db`). `AppletKit` uses it to record information about installed applications. You can obtain a `PackageDatabase` object by calling `kit.database(ADBT_Applet)` to query the list of installed apps, which will be used later.
:::

## Telling the Framework Where Applications Are Stored

Before installing any applications, you must inform Glyphix of the locations of two types of directories: **Application Package Directories** (where `.pkg` files are stored) and **Application Data Directories** (where data generated during application runtime is stored). They serve different purposes and must not be confused.

### Application Package Directories

Application package directories are managed by `EnvPath::packages()`. It is a list, where each entry points to a directory containing `.pkg` files. This list serves multiple semantic purposes simultaneously, and understanding them is the foundation for all subsequent configurations:

- **Discovery**: When the framework needs to load resources such as `pkg://com.example.demo/...`, it traverses the list **from front to back**, looking for `com.example.demo.pkg` in each directory. The first match is loaded.
- **Installation**: When the installation API is called, the new package is **always written to the last directory in the list**.
- **Uninstall**: Uninstallation scans **from front to back**, deleting the package from the first directory that contains it.

Because installation always targets the end of the list, while discovery and uninstallation start from the head of the list, the order of directories in the list determines their roles: directories near the front are suitable for "factory-default, read-only" applications; directories near the back are suitable for "user-installed" applications.

::: important Prerequisites
Before calling the installation API, the `packages()` list must contain at least one directory, and the last directory in the list (i.e., the installation target) must exist and be writable. Otherwise, the installation will fail immediately.
:::

Configuration is done by appending directories to the list during the platform initialization phase:

```cpp
#include "gx_environment.h"
using namespace gx;

// Call after Application construction and before installation/launch
EnvPath::packages().emplace_back("/data/apps");
```

### Application Data Directories

Applications require writable space at runtime to store caches, files, temporary data, etc. These directories are configured via `EnvPath::setEntry(role, path)`, where each role corresponds to a specific purpose. Their semantic contracts are as follows:

| Role | Meaning | Typical Path |
|:---|:---|:---|
| `AppletCache` | Writable cache for apps; the framework can clean and rebuild it when space is tight | `/data/cache` |
| `AppletFiles` | Private files for apps, retained persistently and not automatically cleaned | `/data/files` |
| `AppletMass` | Large file storage (such as media assets), large capacity | `/data/mass` |
| `AppletTemp` | Temporary files, can be cleaned after the application exits | `/data/temp` |
| `AppletStorage` | Persistent storage for applications | `/data/storage` |
| `LoggingDirectory` | Framework log directory | `/logs` |

**Data Isolation**: The framework creates independent subdirectories for each application under the above directories based on package names. For example, private files for the application `com.example.demo` reside under `/data/files/com.example.demo/`. You do not need to manage these subdirectories manually; the framework automatically creates and cleans them up during installation and uninstallation.

In addition, there is a special role `GlobalPackage`, which points to a globally shared `.pkg` (such as `/global.pkg`). All applications can read public resources such as fonts and icons from it via the `pkg:///...` protocol. It does not belong to any specific application and is typically flashed along with the firmware.

Configuration example:

```cpp
EnvPath::setEntry(EnvPath::AppletCache,   "/data/cache");
EnvPath::setEntry(EnvPath::AppletFiles,   "/data/files");
EnvPath::setEntry(EnvPath::AppletMass,    "/data/mass");
EnvPath::setEntry(EnvPath::AppletTemp,    "/data/temp");
EnvPath::setEntry(EnvPath::AppletStorage, "/data/storage");
EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
```

::: tip Timing
`Application` resets `EnvPath` to its default configuration upon construction, so custom configurations should be completed immediately after `Application` construction and before any `installPackage`/`launch` calls. Late configuration will lead to unexpected behavior.
:::

### Configuration Example

Combining both types of directories, a minimally viable initialization snippet is as follows:

```cpp
Application app;
// Application package directory: at least one writable directory
EnvPath::packages().emplace_back("/data/apps");
// Application data directories: adjusted according to device actual partitions
EnvPath::setEntry(EnvPath::AppletFiles,   "/data/files");
EnvPath::setEntry(EnvPath::AppletCache,   "/data/cache");
EnvPath::setEntry(EnvPath::AppletTemp,    "/data/temp");
EnvPath::setEntry(EnvPath::AppletStorage, "/data/storage");
EnvPath::setEntry(EnvPath::AppletMass,    "/data/mass");

JsVM vm;
Widget window;
AppletKit kit(&window, "/pkgs.db");
```

## Installing an Application

Before calling `installPackage`, you need to confirm that:

1. The `EnvPath::packages()` list is non-empty, and its last directory exists and is writable.
2. `AppletKit` has been constructed (installation requires writing to the package database it manages).
3. The `.pkg` file to be installed already exists in the device file system (e.g., located at `/tmp/com.example.demo.pkg`).
4. If using the default version verification policy (`NormalVerify`), the device's vendor/product ID must be configured; otherwise, the installation will return `InvalidDevice` due to device ID verification failure.

### Invoking Installation

The installation API is `AppletKit::installPackage(fileUri, policy)`. The first parameter is the `.pkg` file path, and the second is the verification policy, which can be omitted (defaults to `NormalVerify`):

```cpp
auto status = kit.installPackage("/tmp/com.example.demo.pkg");
if (status != AppletKit::ValidPackage) {
    LogError() << "install failed:" << AppletKit::packageStatusMessage(status);
    return;
}
LogInfo() << "install ok";
```

The return value is a `PackageStatus`. Common meanings include:

| Status | Meaning |
|:---|:---|
| `ValidPackage` | Installation successful |
| `FileNotExists` | `.pkg` file path does not exist |
| `InvalidPackage` | Package is corrupted or manifest is unreadable |
| `InvalidVersion` | Version does not meet the verification policy |
| `InvalidDevice` | Device vendor/product ID does not match |
| `FileIOError` | Copy failed, usually because the installation directory is not writable or space is insufficient |

The verification policy `PackageVerify` determines the strictness of the framework towards the installation package:

| Policy | Version Verification | Device ID Verification |
|:---|:---|:---|
| `NormalVerify` (Default) | New version must not be lower than the installed version | Required |
| `UpgradeOnly` | Must be strictly higher than the installed version | Required |
| `IgnoreVersion` | Skipped | Required |
| `NoVerify` | Skipped entirely, as long as the package is legal | Skipped |

::: tip
If you encounter `InvalidDevice` or `InvalidVersion` during initial installation debugging, you can temporarily use `AppletKit::NoVerify` to bypass verification interference, confirm that the installation process itself works properly, and then restore the official policy.
:::

### What Installation Does

`installPackage` guarantees the following effects externally:

- Verifies that the `.pkg` file is legal, and checks the version and device ID according to the selected policy.
- If an application with the same name is currently running, it will be terminated first to avoid file locking or data conflicts.
- Copies the `.pkg` file to the last directory in the `packages()` list, with the file name `<package-name>.pkg`. If a file with the same name already exists, it is overwritten.
- Registers the application in the package database, recording its installation path and the `pkg://<package-name>` access URI.
- If the application manifest declares a URI scheme (e.g., registering itself as a handler for the `ime` input method), it is registered as well.
- Issues a "package changed" notification so other parts of the framework are aware of the new app.

::: important Package Verification Capabilities
`AppletKit::installPackage()` itself lacks file integrity or signature verification capabilities. Device manufacturers need to develop related functions on their own, verify the `.pkg` file before calling `installPackage()`, and ensure consistency through features such as power-fail protection and rollbacks of the file system during the installation process. The framework only guarantees completion of installation assuming the `.pkg` file is legal, readable, and writable.
:::

### Observation Checklist

After installation returns `ValidPackage`, you can verify the results in the following ways:

- The file should be visible in the installation directory: `/data/apps/com.example.demo.pkg`.
- `kit.database(ADBT_Applet)->contains("com.example.demo")` should return `true`.
- The list returned by `kit.installedApplets()` should contain `"com.example.demo"`.

```cpp
EXPECT_TRUE(File::exists("/data/apps/com.example.demo.pkg"));
EXPECT_TRUE(kit.database(ADBT_Applet)->contains("com.example.demo"));
EXPECT_NE(std::find(kit.installedApplets().begin(),
                    kit.installedApplets().end(),
                    "com.example.demo"),
          kit.installedApplets().end());
```

## Launching and Observing

Installation merely puts the package in place. To make the application actually display, you need to call `AppletKit::launch(name)`, where `name` is the package name in the manifest:

```cpp
Applet *applet = kit.launch("com.example.demo");
if (!applet)
    LogError() << "launch failed";
```

`launch` returns a pointer to the application object, or `nullptr` upon failure. Upon success, the application enters the foreground and is displayed.

::: tip Dependency Explanation
Whether `launch()` can actually display the application also depends on whether the JavaScript engine, window system, platform graphics adaptation, and the application's own code are ready. If `launch()` returns a non-null value but the screen remains blank, the issue typically lies in these other systems rather than the installation workflow.
:::

After a successful launch, you can verify that:

- The application interface appears in the window (dependent on the aforementioned systems being ready).
- After the application runs and writes data, its private directory appears: `/data/files/com.example.demo/`.
- Assets within the application package can be accessed via `pkg://com.example.demo/<asset-path>` (manipulable through the `File` class).

## Uninstalling an Application

The uninstallation API is `AppletKit::removePackage(package)`, passing in the package name and returning a `bool` indicating whether the package file was found and deleted:

```cpp
if (!kit.removePackage("com.example.demo"))
    LogError() << "uninstall failed: package not found";
```

Uninstallation guarantees the following effects externally:

- If the application is currently running, it is terminated first.
- Deletes the `.pkg` file from the first directory in the `packages()` list that contains it.
- Deletes the application's subdirectories across all data directories (`<package-name>/` under `AppletCache`/`AppletFiles`/`AppletTemp`/`AppletStorage`).
- Unregisters the application from the package database.

Verification after uninstallation:

- `/data/apps/com.example.demo.pkg` in the installation directory has disappeared.
- Data subdirectories like `/data/files/com.example.demo/` have been cleared.
- `kit.installedApplets()` no longer contains `"com.example.demo"`.

## Advanced: System Pre-installed Application Directories

Many devices need to distinguish between two types of applications: **factory pre-installed, non-uninstallable** system applications, and **user-installed, uninstallable** user applications. By leveraging the order semantics of the `packages()` list, two directories can be used to implement this layering.

### Use Cases

Factory pre-installed applications (such as system watch faces and settings apps) are usually flashed into read-only storage and should not be uninstalled or overwritten by users. User-installed applications should reside in writable partitions and can be added or removed at will. If both are mixed into a single directory, subsequent application updates and uninstallation management become complicated.

### Recommended Layout

Append two directories to `packages()`, sensitive to order, with the pre-installed read-only directory first and the user-writable directory second:

```cpp
EnvPath::packages().emplace_back("/system/apps");  // Read-only pre-installed, placed first
EnvPath::packages().emplace_back("/data/apps");    // Writable user-installed, placed second
```

Looking back at [Application Package Directories](#application-package-directories) in Step 1, the semantics of the three operations under this layout are as follows:

- **Discovery** goes from front to back; the pre-installed directory comes first, and factory applications take priority for a guaranteed stable load.
- **Installation** writes to the last directory in the list, which is the user area. Newly installed applications will not pollute the pre-installed directory.
- **Uninstallation** goes from front to back, deleting from the first directory containing the package.

### Protection Mechanism: Call-side Whitelist

Order semantics only determine the storage path of the application and the startup discovery process; they do not prevent users from uninstalling pre-installed applications. The built-in <code>AppletKit&#8203;::&#8203;removePackage</code> has no concept of "pre-installed" or "protected." Therefore, the device's uninstallation entry point must be implemented by native code, maintaining a whitelist of pre-installed package names and intercepting before calling `removePackage`: if the package hits the whitelist, uninstallation is refused.

The installation side does not require a whitelist. The device manufacturer's installation channels (app stores, preloaded pushes, etc.) are controlled by nature, and the legality of the application package name is guaranteed by the signature mechanism, which falls outside the responsibility of this layer. Furthermore, due to forward-resolve shadowing (see "Known Limitations" below), runtime upgrades of pre-installed applications cannot take effect anyway, so there is no need to additionally prevent overwrite installation. Hence, installation can directly call `kit.installPackage`.

An illustration of a native uninstallation wrapper layer:

```cpp
#include "gx_hashset.h"

class PackageManager {
public:
    PackageManager(AppletKit &kit, HashSet<String> preinstalled)
        : m_kit(kit), m_preinstalled(std::move(preinstalled)) {}

    auto install(const String &packageUri) {
        return m_kit.installPackage(packageUri);
    }

    bool uninstall(const String &packageName) {
        if (m_preinstalled.count(packageName)) {
            LogWarning() << "refuse to uninstall protected package:" << packageName;
            return false;
        }
        return m_kit.removePackage(packageName);
    }

private:
    AppletKit &m_kit;
    HashSet<String> preinstalled;
};
```

::: tip Read-only Mounting and Whitelists
Mounting the pre-installed partition as read-only is still a recommended practice (to prevent accidental writes), but it is not a dependency for uninstallation protection. Even if the pre-installed directory is writable, the whitelist will intercept before `removePackage` is called.

The permission field of `EnvPath::Entry` does not participate in application package directory decisions; it only constrains JavaScript code access to application data directories.
:::

### Factory Reset

By taking advantage of the separation between pre-installed and user directories, a factory reset can be implemented as: deleting all `.pkg` files under the user directory and resetting `pkgs.db`; pre-installed packages in the system directory remain unaffected. Runtime installation always writes to `packages().back()` (the user directory) and never overwrites pre-installed copies in the system directory. Therefore, after clearing the user directory and resetting the database, pre-installed applications can still be normally resolved and loaded via `pkg://`.

Optionally, you can implement "uninstalling updates to pre-installed applications"—meaning deleting the update copy of a pre-installed application in the user directory, causing it to fall back to the factory version in the system directory. This capability is currently only feasible in implementation and is not yet officially supported.

### Known Limitations

The following framework behaviors require proactive avoidance or attention from the native business layer:

1. **App store upgrades for pre-installed applications cannot be implemented**. Currently, resource resolution for `pkg://<name>` traverses the `packages()` list forward, while runtime installation always writes to `packages().back()` (the user directory). If you attempt to upgrade a pre-installed application via runtime installation, the new version will land in the user directory but will be shadowed by the old version in the system directory due to forward matching, and thus will never take effect. This upgrade capability is pending implementation.
2. **Uninstallation has no concept of "protected"**. `removePackage` locates packages solely by "first successful deletion," indiscriminately deleting packages in any directory without any "pre-installed" or "protected" markings. Whitelist interception must be implemented by the native caller; the framework does not provide this judgment.
3. **Watch face package uninstallation does not clean the database**. `removePackage` only unregisters from the application table (`ADBT_Applet`) and does not clean database entries for watch face packages (`ADBT_Dial`), leaving stale records behind. This is a framework TODO item, and native uninstallation logic must handle watch faces manually if support is needed.
4. **The permission field of application package directory entries is ineffective**. The permission of `EnvPath::Entry` does not participate in `packages()` list lookup/installation/uninstallation decisions; it only constrains JavaScript code access to application data directories. It cannot be used to express "installation prohibited in this directory."

## Platform Initialization Templates

Complete `EnvPath` configurations for three typical scenarios are provided below, which can be copied directly and adjusted according to device paths. All configurations must be completed after `Application` construction and before <code>AppletKit&#8203;::&#8203;launch</code>/`installPackage`.

### Host Emulator

Minimalist configuration, single directory for storing applications:

```cpp
os::chroot(".");
EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
EnvPath::packages().emplace_back("/apps");
```

### Embedded Target (Single Partition)

A device with only a single writable partition, where applications and data share the same space:

```cpp
EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
EnvPath::setEntry(EnvPath::AppletCache,   "/data/cache");
EnvPath::setEntry(EnvPath::AppletFiles,   "/data/files");
EnvPath::setEntry(EnvPath::AppletMass,    "/data/mass");
EnvPath::setEntry(EnvPath::AppletTemp,    "/data/temp");
EnvPath::setEntry(EnvPath::AppletStorage, "/data/storage");
EnvPath::packages().emplace_back("/data/apps");
```

### Device with Pre-installed Partitions

Separation between pre-installed read-only partitions and user writable partitions:

```cpp
EnvPath::setEntry(EnvPath::GlobalPackage, "/system/global.pkg");
EnvPath::setEntry(EnvPath::AppletCache,   "/data/cache");
EnvPath::setEntry(EnvPath::AppletFiles,   "/data/files");
EnvPath::setEntry(EnvPath::AppletMass,    "/data/mass");
EnvPath::setEntry(EnvPath::AppletTemp,    "/data/temp");
EnvPath::setEntry(EnvPath::AppletStorage, "/data/storage");

// Order-sensitive: pre-installed read-only directory first, user-writable directory second
EnvPath::packages().emplace_back("/system/apps");
EnvPath::packages().emplace_back("/data/apps");
```

Once configuration is complete, you can install and launch applications according to steps 2 and 3. It is recommended to use `AppletKit::NoVerify` to install a simple sample package during your first successful run, confirm that `.pkg` appears under `/data/apps` and `launch` returns a non-null pointer, and then gradually restore official verification policies and pre-installed layouts.

============================================================
FILE_PATH: src/transl/EN/cxxdev/object-system.md

# Object System

The C++ framework of Glyphix features an object model rooted in `PrimitiveObject`. Understanding this model is the foundation for subsequent development.

The object system consists of three cooperating parts: the **Object Base Class Hierarchy** defines the common capabilities and lifecycle rules for all managed objects; the **Meta-Object System** generates metadata for C++ classes through a compile-time meta compiler, empowering them with reflection, property binding, and JavaScript export capabilities; and the **Memory Safety Mechanism** solves the dangling pointer problem prevalent in GUI frameworks using guarded pointers and reference counting.

<ArchDiagram max-width="540px">
  <div>
    JavaScript Script Layer
    <div class="remark">Property Binding · Method Invocation · Event Response</div>
  </div>
  <div>
    Meta-Object System
    <div class="group row">
      <div>GX_OBJECT<div class="remark">Meta-Compiler Registration</div></div>
      <div>GX_PROPERTY<div class="remark">Property/Method Reflection</div></div>
      <div>Variant<div class="remark">C++ ↔ JS Type Bridging</div></div>
      <div>dyn_cast<div class="remark">Safe Downcasting</div></div>
    </div>
  </div>
  <div class="subject">
    Object Base Class Hierarchy
    <div class="group row">
      <div>PrimitiveObject<div class="remark">Reflection Support · Lifecycle Management</div></div>
      <div>Object<div class="remark">Parent-Child Tree Structure · Cascading Destruction</div></div>
      <div>Widget<div class="remark">UI Control Base Class</div></div>
    </div>
  </div>
  <div>
    Memory Safety Mechanism
    <div class="group row">
      <div>Signal&lt;&gt;<div class="remark">Event Notification · Auto-Disconnection</div></div>
      <div>Pointer&lt;T&gt;<div class="remark">Guarded Weak Reference</div></div>
      <div>SharedRef&lt;T&gt;<div class="remark">Intrusive Shared Reference</div></div>
    </div>
  </div>
</ArchDiagram>

## Reflection and the Meta-Object Compiler

Standard C++ classes are "silent": given an object pointer, you cannot know at runtime what members it has, what they are named, or how to read and write them. This is not an obstacle for static C++ development that does not require scripting.

However, Glyphix works differently. When an application's page template writes `:value="progress"`, the reactive framework needs to find the control's corresponding property by the string `"value"` at runtime, and automatically refresh it when the data changes. This capability of "a program being able to understand its own structure at runtime" is called **Reflection**, which standard C++ does not support.

Glyphix's solution is to introduce a **Meta Compiler** into the build process. It scans the source code before the formal C++ compilation, generating metadata for classes that need to participate in the object system. Developers simply place the **`GX_OBJECT`** macro at the beginning of a class definition, and the meta compiler will process this class—after which the framework can read and write its properties or invoke methods by name, and access it from JavaScript.

You do not need to understand the internal principles of the meta-object system just yet. It is enough to remember one rule: any class that requires reflection capabilities must include the `GX_OBJECT` macro in its definition and inherit from `PrimitiveObject` or `Object`.

## `PrimitiveObject` and `Object`

The framework's object system is divided into two tiers:

**`PrimitiveObject`** is the root base class for all **managed objects**. Classes that inherit from it gain framework capabilities such as property reflection, dynamic casting, and safe delayed destruction. However, `PrimitiveObject` itself **does not** have a parent-child tree structure—it is simply a "C++ object perceivable by the framework." Types such as `AsyncSession` and `BindableObject` inherit from it because these types do not need to form a tree.

**`Object`** inherits from `PrimitiveObject` and additionally adds a **parent-child tree structure**: passing a `parent` pointer during construction causes all child objects to be recursively destroyed when the parent object is destroyed. The Widget Tree is organized through this mechanism.

::: tip Analogy to Other Frameworks
If you have Qt development experience, you can think of Glyphix's meta-object system as analogous to Qt's MOC system: `GX_OBJECT` corresponds to `Q_OBJECT`. However, there are many differences, such as Glyphix splitting the capabilities of Qt's `QObject` into two layers; furthermore, `Signal` is merely a regular template class that does not rely on the meta-object compiler.

Other frameworks, like Unreal Engine's UCLASS, have similar reflection systems.
:::

Choosing which base class to use depends on whether your class needs to be part of a tree:

```cpp
// Needs to participate in the object tree → Inherit from Object
class MySensor : public Object {
    GX_OBJECT
public:
    explicit MySensor(Object *parent = nullptr) : Object(parent) {}
};

// Only needs framework awareness, does not participate in the tree → Inherit from PrimitiveObject
class MyNetworkSession : public PrimitiveObject {
    GX_OBJECT_KINDS(ExplicitDeleteKind)
public:
    MyNetworkSession() = default;
};
```

`GX_OBJECT_KINDS(ExplicitDeleteKind)` in the code is an additional declaration. Like the `GX_OBJECT` macro, it declares the meta-object class, but it informs the framework that this object's lifecycle is managed by the developer and will not be automatically garbage-collected by JavaScript. Lifecycle-sensitive types like `AsyncSession` use it.

## Properties and Signals

The **`GX_PROPERTY`** macro is used to declare a property perceptible by the framework, associating it with the corresponding getter and setter. Once declared, the property can be driven by the framework's reactive system—when its value changes, dependent UIs automatically refresh, and the animation system can interpolate it:

```cpp
class MyWidget : public Widget {
    GX_OBJECT
public:
    int value() const { return m_value; }
    void setValue(int v) { m_value = v; update(); }

    GX_PROPERTY(int value, get value, set setValue)

private:
    int m_value = 0;
};
```

### Signals

**`Signal<>`** is the event notification mechanism, declared directly as a class member. It is "emitted" when an event occurs, and other objects receive notifications by "connecting" to it ([lambda expressions](https://en.cppreference.com/w/cpp/language/lambda) are C++'s anonymous function syntax):

```cpp
class MyWidget : public Widget {
    GX_OBJECT
public:
    Signal<int> valueChanged;

    void setValue(int v) {
        m_value = v;
        valueChanged(v);  // Emit signal
    }
private:
    int m_value = 0;
};

// Connect to a member function
myWidget->valueChanged.connect(this, &MyClass::onValueChanged);

// Or connect to a lambda
auto slot = make_slot([](int v) { /* Respond to change */ });
myWidget->valueChanged.connect(slot);
```

::: tip Comparison with Qt's Signals and Slots
Qt's classic signal-slot mechanism requires MOC-generated code support, but `Signal<>` is a pure C++ template class that does not depend on the meta-object compiler. Therefore, you do not necessarily have to use `Signal<...>` objects in specific classes; you can use them anywhere.

Since `Signal` is a class, it occupies memory space (even when there are no connections). Therefore, it is recommended to use event type enumerations and a single signal member variable to save memory as much as possible, rather than declaring a `Signal` member for every event.
:::

### Full Form of `GX_PROPERTY`

In addition to `get` / `set`, `GX_PROPERTY` also supports declaring an associated change signal (`signal`), which is the standard interface for the reactive system to subscribe to property changes:

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    int value() const { return m_value; }
    void setValue(int v) {
        if (m_value == v) return;
        m_value = v;
        update();
        valueChanged(v);
    }

    Signal<int> valueChanged;

    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)

private:
    int m_value = 0;
};
```

For properties declared with a `signal`, their changes are automatically propagated via the reactive system to JavaScript expressions bound to that property. This is the foundation for two-way synchronization between control properties and application data.

The `signal` field in `GX_PROPERTY` does not depend on the parameter type of `Signal<T>`; the framework only cares whether it exists and when it is emitted. Conversely, the `get` field must be provided in this case to allow the framework to read the property value on the JavaScript side.

## Guarded Pointers and Memory Safety

In GUI frameworks, asynchronous scenarios easily lead to dangling pointer crashes. A typical case:
```cpp
void onNetworkResponse(const String &data) {
    // Network request takes 2 seconds to return
    // But within these 2 seconds, the user may have exited the current page, and label has been destroyed
    this->label->setText(data); // Segmentation Fault!
}
```
Timer callbacks, I/O callbacks, and all other asynchronous scenarios face the exact same risk. In scripted frameworks, such use cases are structurally unavoidable, so a safe lifecycle observation mechanism must be provided.

### `Pointer<T>` Guarded Pointers

Glyphix builds weak reference counting support directly into all derived classes of `PrimitiveObject`. Use `Pointer<T>` to hold non-owning cross-object references. When the target object is destroyed, `Pointer<T>` is automatically nulled out, making it safe to use by checking before dereferencing:

```cpp
Pointer<Label> m_label; // Declare as a member variable

// ...Assign after construction...
m_label = label;

// In any asynchronous callback that might cause the label to be destroyed:
void onNetworkResponse(const String &data) {
    if (!m_label)
        return; // label has been destroyed, exit safely
    m_label->setText(data); // Accessing is safe here
}
```

::: tip When to Use
Use `Pointer<T>` instead of raw pointers `T *` to track lifecycles when holding pointers across objects without owning their lifecycles. `Signal`'s `connect` mechanism also relies on guarded pointers—when the receiver (the object containing the slot) is destroyed, the connection is automatically disconnected, preventing dangling callbacks.
:::

::: warning Thread Restrictions
Guarded pointers do not support cross-thread access; they are essentially restricted to the UI thread. Furthermore, they are not zero-cost abstractions, as every construction involves reference counting operations.
:::

### `SharedRef<T>` Intrusive Reference Counting

For plain value objects that do not inherit from `PrimitiveObject` (such as custom data structures), the framework provides intrusive shared reference counting. By making value types inherit from `SharedValue` and holding them with `SharedRef<T>`, you obtain shared semantics similar to [`std::shared_ptr`](https://en.cppreference.com/w/cpp/memory/shared_ptr) while avoiding extra control block allocations:

```cpp
class MyData : public SharedValue {
public:
    int x = 0;
    String name;
};

auto ref1 = make_shared<MyData>();
ref1->x = 42;

SharedRef<MyData> ref2 = ref1; // Reference count increases, sharing the same object
```

`SharedRef` also supports Copy-on-Write (COW) semantics: before modifying a copied version, an independent replica is created to ensure multiple holders do not interfere with each other. This mechanism achieves thread safety using atomic reference counts.

## Dynamic Type Casting

Standard C++'s [`dynamic_cast`](https://en.cppreference.com/w/cpp/language/dynamic_cast) relies on RTTI (Run-Time Type Information), whereas embedded environments are typically compiled with `-fno-rtti`. `dyn_cast` leverages the meta-object system to provide equivalent runtime-safe downcasting capabilities.

The target type `T` of `dyn_cast<T *>()` must satisfy two conditions:
1. Inherit from `PrimitiveObject`
2. Declare the `GX_OBJECT`/`GX_OBJECT_KINDS` macro

```cpp
PrimitiveObject *obj = getSomeObject();

// Safe downcasting; returns nullptr if the cast fails
auto *btn = dyn_cast<Button *>(obj);
if (btn)
    btn->setText("OK");

// Const versions are also supported
const auto *constBtn = dyn_cast<const Button *>(obj);
```

::: warning `GX_OBJECT` is a Prerequisite
`dyn_cast`'s type checking relies on the target class's static meta-object information (`staticMetaObject`). If the target class does not declare `GX_OBJECT`, it lacks the necessary runtime type information, resulting in a compilation error.
:::

In Native Module development, `dyn_cast` is particularly common: the framework frequently passes objects in as base class pointers (`PrimitiveObject *` or `Object *`), requiring `dyn_cast` to safely restore them to concrete types before operating on them.

Considering that sandbox security policies do not trust object pointers passed from scripts, we cannot assume that the runtime object pointer passed in is of the correct type, so `dyn_cast` must be used to verify the type and safely access its members.

### Memory Leak Trap

A typical `dyn_cast` usage pattern conceals a memory leak risk, such as:
```cpp
auto *session = dyn_cast<Session *>(takeObjectOwnership());
if (session) {
    // Cast successful, access session members and transfer ownership
}
```
The problem is that if the object returned by `takeObjectOwnership()` is not of type `Session`, `dyn_cast` returns `nullptr`, but ownership of the original object has already been transferred—leading to a memory leak if no other mechanism reclaims this object.

When developing Native Module APIs, you may occasionally encounter this issue, and related frameworks provide better APIs to avoid it. However, developers should be aware of this potential risk and not be misled by `dyn_cast`'s safety.

### Is `GX_OBJECT` Necessary?

Not all classes inheriting from `PrimitiveObject` require `GX_OBJECT`. The role of the `GX_OBJECT` macro is to register the class with the meta-object system, enabling capabilities such as reflection, property binding, and `dyn_cast`. If your class:

- Does not need to be exposed to JavaScript
- Does not require reflection mechanisms like `GX_PROPERTY` or `GX_METHOD`
- Does not need to be safely downcast by `dyn_cast`

Then you can omit `GX_OBJECT`, simply inheriting from the base class and using standard C++ features normally:

```cpp
// Internal helper class that does not require any meta-object capabilities; GX_OBJECT is omitted
class InternalBufferManager : public PrimitiveObject {
public:
    explicit InternalBufferManager() = default;
    void flush();
private:
    // ...
};
```

Classes that omit `GX_OBJECT` still retain the basic capabilities of `PrimitiveObject`, including `deleteLater()` and guarded pointer support, but lose reflection and dynamic type identification capabilities.

Another scenario is when your final type requires meta-object capabilities, but certain intermediate base classes do not; in this case, the intermediate base classes can omit `GX_OBJECT`. This loses some runtime type information but reduces code size.

::: tip
If you are unsure whether you need `GX_OBJECT`, it is generally recommended to conservatively include it.
:::

One final important difference is that once marked with `GX_OBJECT`, a class must be located in a header file (`*.h`) and registered to the build system using the `glyphix_add_meta_objects()` CMake macro. Classes without `GX_OBJECT` have no such requirement and can be defined directly in `.cpp` files.

## Runtime Type System

Throughout all the discussions of `GX_PROPERTY` so far, one question has never been answered:

```cpp
GX_PROPERTY(int value, get value, set setValue)
```

How does JavaScript know what an `int` is? When `widget.value = 42` is written on the JavaScript side, this `42` is a JavaScript `number` type. Meanwhile, `setValue(int v)` accepts a C++ `int`. What happens in between? Conversely, how does the `int` returned by `getValue()` become a `number` in JavaScript?

Without any glue code, the framework obviously needs to do some work behind the scenes to bridge C++ static types and dynamic script types. This is a fairly transparent process, and this section will explain what happens in the middle.

### The Universal Type Container `Variant`

The answer lies in `Variant`. It is a type-erased container capable of holding values of arbitrary types and serves as the core bridge connecting the C++ static type system and JavaScript dynamic types.

Whenever the framework needs to cross this boundary, it goes through `Variant`:

1. **Property Read/Write Intermediate Layer**: When properties declared by `GX_PROPERTY` are read and written via reflection APIs, values are passed via `Variant`. The framework converts JavaScript's `JsValue` into a `Variant`, which is then converted by `Variant` into the actual parameter type of the C++ setter; the direction is reversed when reading.
2. **Method Call Parameter Marshalling**: Parameters and return values of `GX_METHOD` are first represented via `Variant` before being passed to C++ .

```cpp
Variant v1;                  // Empty value (null)
Variant v2{42};              // Stores int
Variant v3{3.14};            // Stores double
Variant v4{String("Hello")}; // Stores String
// Variant must be explicitly constructed; implicit conversion is not supported
// Variant v5 = 42; // Error, must write Variant v5{42};

// Type checking
if (v2.is<int>()) { /* ... */ }
// Checking convertibility is not recommended; instead, directly call to<T>() and check if it results in an invalid value
if (v3.convertible<double>()) { /* ... */ }

// Read by reference (fastest, requires exact type match)
int n = v2.as<int>();
// Read by reference, returns default value if types do not match
double d = v2.as<double>(0.0); // int != double, returns 0.0
// Read with type conversion (by value)
int fromDouble = v3.to<int>();   // 3.14 -> 3
String fromInt = v2.to<String>(); // 42 -> "42"
```

::: tip
This is not C++17's [`std::variant`](https://en.cppreference.com/w/cpp/utility/variant), but rather closer to [`std::any`](https://en.cppreference.com/w/cpp/utility/any) with support for runtime type identification and automatic type conversion.

Normally, you do not need to manipulate `Variant` directly in business code; the framework handles all conversions automatically. You will only interact with it directly when implementing low-level framework extensions, writing general utility functions, or needing to operate on runtime reflection APIs directly.
:::

### Built-in Type Mappings

The framework features built-in two-way mappings between common C++ primitive types and JavaScript:

| C++ Type | JavaScript Type | Remarks |
|:---:|:---:|:---:|
| `int`, `float`, `double`, etc. | `number` | Numeric types map directly |
| `bool` | `boolean` | |
| `String` | `string` | |
| Subclasses of `PrimitiveObject *` | JavaScript object reference | Object lifecycle managed by the framework |
| Value types like `Color`, `Length` | `string` | Represented via specific-format strings |

This is why after writing `GX_PROPERTY(int value, ...)`, the JS side can directly do `widget.value = 42`: `int` is in the built-in mapping table, and the framework knows how to convert the type.

::: note Do Not Use C-Strings
`Variant` requires the stored type `T` to have ownership, so non-owning types such as C-strings (`const char *`) and string views (`String::View`) cannot be stored in `Variant`. Always use `String` to represent text data, explicitly converting to `String` before storing in `Variant` when necessary.

Using unsupported string types will result in compilation errors.
:::

::: important
The built-in type mapping table does not register `std::string`-related mappings, so it is also not recommended to store `std::string` in `Variant`. Unmapped types can be stored normally, but they will be treated as opaque C++ objects and cannot be used in JavaScript.
:::

### Complex Type Reflection

For classes declared using `GX_OBJECT`, you can also utilize `GX_ENUM` and `GX_STRUCT` to export enumeration and structure member types, allowing them to be used naturally in JavaScript as well. This type export is automatic and requires no manual writing of additional binding code.

#### Enumeration Reflection `GX_ENUM`

When the parameter type of a property or method is a C++ enumeration, exposing it directly to JavaScript as an integer is neither intuitive nor error-prone. `GX_ENUM` exports enumerations as string constants, allowing JavaScript to operate using readable strings instead of magic numbers:

```cpp
class ScrollArea : public Widget {
    GX_OBJECT
public:
    enum GX_ENUM ScrollBarStyle {
        RemoveScrollBar GX_ALIAS("hidden"),
        LinearScrollBar GX_ALIAS("line"),
        DotsScrollBar   GX_ALIAS("dots")
    };

    GX_PROPERTY(ScrollBarStyle indicator, set setScrollBar)
};
```

`GX_ENUM` is placed after the `enum` keyword to inform the meta compiler that this enumeration needs to be exported. `GX_ALIAS("...")` specifies a JavaScript-visible string name for each enumeration member—if omitted, the original C++ member name is used by default. Application developers use this in JavaScript as follows:

```js
scroll.indicator = "hidden"; // Corresponds to RemoveScrollBar
scroll.indicator = "dots";   // Corresponds to DotsScrollBar
```

When reading the `indicator` property, the framework converts the string `"dots"` into the `DotsScrollBar` enum value before passing it to the setter; when reading out, it converts the enum value back to a string. The entire process is completely transparent to the C++ side, which always operates on concrete enum types.

#### Structure Parameter Reflection `GX_STRUCT`

For method parameters, an operation sometimes requires multiple related configuration items. In such cases, parameters can be encapsulated into a structure and exported using `GX_STRUCT`, allowing the JavaScript side to pass an object literal:

```cpp
class Scroll : public ScrollArea {
    GX_OBJECT
public:
    struct GX_STRUCT ScrollOptions {
        Length left;
        Length top;
        ScrollBehavior behavior;
    };
    struct GX_STRUCT IndexOptions {
        int index;
        ScrollBehavior behavior;
    };

    GX_METHOD void scrollTo(const ScrollOptions &options);
    GX_METHOD void scrollBy(const ScrollOptions &options);
    GX_METHOD void setIndex(const IndexOptions &options);
};
```

`GX_STRUCT` is placed after the `struct` keyword, and each field of the structure is automatically exported according to its type (again via built-in type mappings or nested `GX_ENUM`s). The JS side can pass objects directly:

```js
scroll.scrollTo({ left: 0, top: 200, behavior: "smooth" });
scroll.setIndex({ index: 3, behavior: "instant" });
```

The C++ side's `scrollTo` always receives a strongly-typed `ScrollOptions` object, requiring no parsing on the C++ side.

::: warning Do Not Forget Annotations
When declaring `GX_PROPERTY` or `GX_METHOD`, if the related type is a custom enumeration or structure, be sure to correctly annotate it with `GX_ENUM` or `GX_STRUCT`. Otherwise, these properties or methods will be unusable on the JavaScript side without any compilation error prompts.
:::

### Is There an "Intermediate Representation"?

When using `Variant` to bridge C++ and JavaScript, does the framework convert JavaScript objects into a universal intermediate representation, such as some JSON-like serialization structure?

The answer is no. `Variant` directly stores C++ objects (including `JsValue`), which includes all type information and operation semantics of the object. The system correctly performs type conversions and method invocations based on the runtime type tag of the `Variant` value, without needing any specific intermediate representation or serialization process.

============================================================
FILE_PATH: src/transl/EN/cxxdev/async-examples.md

# Asynchronous Development Examples

If you feel that the chapter on [Asynchronous Feature Development](async.md) is too extensive and not intuitive enough, this document provides some typical and relatively simple examples to help you handle common asynchronous development scenarios.

These scenarios are not extremely complex, but they focus on:
- A typical asynchronous call pattern, emphasizing cross-thread and cross-language call relationships;
- Scenarios that may be more trivial, with a large number of system APIs to interface with, making them sensitive to code bloat;
- Typical C API interaction requirements rather than standard C++ interfaces.

You can find the complete implementations of these scenarios in the SDK samples and simulate running them directly on your PC.

## Scenario: Interfacing with a C Alarm API

A common asynchronous pattern in embedded systems is the "C callback": the caller submits a task and passes a function pointer as a completion notification. Once the operation is complete, a worker thread invokes the callback.

::: important async only supports the thread model
The asynchronous features of the Glyphix framework only support normal thread contexts and cannot be used in interrupts. If your asynchronous context is an interrupt handler, you should provision a thread to act as a relay.
:::

Here, we use an alarm service as an example. Its provided C asynchronous interface looks like this:

```c
// Taking alarm_async_create as an example, other operations have a similar form
void alarm_async_create(AlarmService *svc, uint32_t interval_ms, ...,
                        alarm_create_cb_t done_cb, void *done_ctx);

// Function pointer type for the completion callback, invoked on the worker thread
typedef void (*alarm_create_cb_t)(alarm_err_t err, alarm_id_t id, void *ctx);
```

Next, we explain how to bridge such a typical C callback interface into a JavaScript Promise.

### Multiple Operations Sharing a Session Type

The alarm service has a batch of operations such as `create`, `cancel`, `setEnabled`, `update`, `snooze`, `getInfo`, `list`, and `count`. If you define a separate client class for each operation, it will generate a large amount of template instantiation.

For scenarios where "the actual logic is entirely completed on the C layer, and the C++ side only handles parameter passing," you can define a lightweight client containing only error code mappings and let all operations share a single `ResultSession` instantiation:

```cpp
struct AlarmClient {
    // Maps alarm_err_t from the C layer to a readable error string
    // to pass to catch on the JavaScript side when the Promise is rejected.
    static const char *errorMessage(async::Status status) {
        switch (status.value()) {
        case ALARM_OK:              return "ok";
        case ALARM_ERR_NOT_FOUND:   return "not_found";
        case ALARM_ERR_TABLE_FULL:  return "table_full";
        case ALARM_ERR_INVALID_ARG: return "invalid_arg";
        default:                    return "unknown_error";
        }
    }
};

// All alarm operations share this single Session type
using AlarmSession = async::ResultSession<AlarmClient>;
```

`AlarmClient` does not need to implement the `resolve()` method because the default thread pool executor is not used here; the actual asynchronous operations are completed by the alarm service's worker thread, and the C++ side is only responsible for posting the result back to the UI thread.

### Basic Binding Pattern

Taking `alarm.create()` as an example, here is the complete binding process:

```cpp
static JsValue jsAlarmCreate(JsCtx ctx) {
    auto *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1 || !ctx.arg(0).isObject())
        return JsValue{};

    // Read parameters from the options object passed from JavaScript
    const JsValue &opts = ctx.arg(0);
    uint32_t intervalMs = static_cast<uint32_t>(opts["interval"].toInt());
    String label        = opts["label"].toString();
    alarm_repeat_t mask = parseRepeatMask(opts["repeat"]);

    // Create a session and extract resolve/reject callbacks from the options object (supports both async styles)
    auto *session = async::make<AlarmSession>(applet);
    session->setResolver(opts);

    // C callback: invoked in the worker thread, notifies JavaScript cross-thread via resolve()
    auto done = +[](alarm_err_t err, alarm_id_t id, void *data) {
        auto *s = static_cast<AlarmSession *>(data);
        s->resolve(err == ALARM_OK
            ? async::Result<int>(id) // Success: resolve with the new alarm ID
            : async::Status(err));   // Failure: reject, error message comes from errorMessage()
    };

    // Call the C service's asynchronous alarm creation interface, passing the callback and session pointer
    alarm_async_create(AppletAlarmService::instance(),
                       intervalMs, mask, label.c_str(), /*...*/,
                       onAlarmFired, nullptr, done, session);
    // Return the Promise object to JavaScript; the framework will automatically settle it when resolve() is called
    return session->promise();
}
```

There are a few fixed patterns here that can be copied directly for use:

- `async::make<AlarmSession>(applet)` creates a session and binds it to the current Applet to satisfy lifecycle requirements.
- `session->setResolver(opts)` allows the same code to support both [callback style and Promise style](/api/README.md#快应用异步接口) asynchronous calls.
- `+[](... void *data)` converts the lambda to a regular function pointer via the unary `+` operator, satisfying the type requirements of the C callback.
- Passes `session` as `void *` transparently to the C API, casts it back in the callback, and then calls `resolve()`.
- `resolve()` is thread-safe; it packages the result as an event and posts it back to the UI thread to drive the settlement of the Promise.

::: tip Writing callbacks using lambda expressions
In C, callback functions are typically static functions. You can use C++ lambda expressions to nest and define callback functions directly nearby, for example:
```cpp
auto done = +[](alarm_err_t err, alarm_id_t id, ...) { ... }
alarm_async_create(..., done, session);
```
This avoids defining a large batch of separate static functions, making the code more compact and clearer.
:::

The structure of the remaining operations (`cancel`, `setEnabled`, `snooze`, etc.) is completely identical, differing only in parameter reading and C API calls:

```cpp
static JsValue jsAlarmCancel(JsCtx ctx) {
    auto *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1)
        return JsValue{};

    alarm_id_t id = ctx.arg(0).toInt();

    auto *session = async::make<AlarmSession>(applet);
    session->setResolver(ctx.arg(0));

    auto done = +[](alarm_err_t err, void *data) {
        // When there is no return value, use resolve<void>
        static_cast<AlarmSession *>(data)->resolve<void>(async::Status(err));
    };
    alarm_async_cancel(AppletAlarmService::instance(), id, done, session);

    return session->promise();
}
```

::: important Do not omit parameter checks
`session->setResolver(ctx.arg(0))` relies on checking `ctx.argc()`. If the number of parameters is not checked at the beginning of the function, check it when calling `setResolver()`:
```cpp
session->setResolver(ctx.argc() ? ctx.arg(0) : JsValue{});
```
:::

### Registering Type Conversion for Custom C Structs

`alarm.getInfo()` returns an `alarm_info_t` struct, which needs to be converted into a JavaScript object. To do this, first specialize `js_cast<T>` in the `gx` namespace:

```cpp
template<> JsValue gx::js_cast<alarm_info_t>(const alarm_info_t &info) {
    JsValue obj = JsVM::current().newObject();
    obj["id"]          = info.id;
    obj["label"]       = info.label;
    obj["interval"]    = double(info.interval_ms);
    obj["repeatMask"]  = info.repeat_mask;
    obj["enabled"]     = bool(info.enabled);
    obj["remaining"]   = double(info.remaining_ms);
    obj["fireCount"]   = int(info.fire_count);
    obj["snooze"]      = int(info.snooze_ms);
    obj["snoozed"]     = bool(info.snoozed);
    return obj;
}
```

Once specialization is complete, pass the struct instance directly to `resolve()` in the binding function:

```cpp
auto done = +[](alarm_err_t err, const alarm_info_t *info, void *data) {
    auto *s = static_cast<AlarmSession *>(data);
    if (err != ALARM_OK || !info) {
        // Exception path, return error status to trigger reject; error message comes from errorMessage()
        s->resolve<alarm_info_t>(async::Status(err));
        return;
    }
    s->resolve<alarm_info_t>(*info);  // The framework automatically calls js_cast on the UI thread
};
alarm_async_get_info(AppletAlarmService::instance(), id, done, session);
```

::: tip
`js_cast()` is called by the framework only after the result returns to the UI thread; it does not execute on the worker thread. This means you can safely use UI-thread-exclusive APIs like `JsVM::current()` inside `js_cast()`.
:::

For cases like `alarm.list()` which return arrays, you can construct a `std::vector<int>` directly and resolve it without defining additional type conversions:

```cpp
auto done = +[](alarm_err_t /*err*/, const alarm_id_t *ids, int count, void *data) {
    auto *s = static_cast<AlarmSession *>(data);
    s->resolve<std::vector<int>>(std::vector<int>{ids, ids + count});
};
alarm_async_list(AppletAlarmService::instance(), done, session);
```

### Alarm Trigger Callback: Sending Events Back to JavaScript

When an alarm triggers, the C layer invokes the `alarm_fire_cb_t` callback from the worker thread. This scenario differs somewhat from the previous "query results" and requires a dedicated event notification mechanism.

#### Why Not Use JavaScript Callback Functions

Intuitively, it seems reasonable to let applications pass a callback function when registering an alarm:

```javascript
// ❌ This does not work in the alarm scenario
alarm.create({ interval: 60000, onFired: (event) => { /* ... */ } })
```

The problem is that alarms span the application lifecycle: after an alarm is created, the application may be killed at any time before the alarm triggers; many devices also support triggering alarms after a reboot.

A JavaScript callback function (`JsValue`) is only valid within the JavaScript runtime of the current application instance. Once the application is closed, this runtime along with all `JsValue`s will be destroyed. At this point, the C++ side has no way to retain this JavaScript callback, let alone call it when the alarm triggers.

This is not just a problem for alarms; **any event that may trigger across application lifecycles cannot be solved via JavaScript callbacks**, such as scheduled tasks, offline message pushes, background download completion notifications, etc.

#### Using Conventional Method Names Instead of Callback References

The simplest solution is: instead of the application "registering a callback," the system proactively **launches** the application when an event occurs and invokes a handling method on the application object using a pre-agreed method name.

This aligns with the design philosophy of application lifecycle functions (`onCreate`, `onShow`, etc.)—the system starts the application on demand and calls known entry methods rather than holding onto pre-registered callbacks. The application side implements the corresponding methods by convention:

```javascript
// app.js — Handling method exported by the application model object (implemented by convention)
export default {
  onAlarmFired(event) {
    // event: { id, label, interval, ... }
    console.log('alarm fired:', event)
  }
}
```

The C++ side implementation: first read the snapshot on the worker thread, then switch back to the main thread to start the application and call the method:

```cpp
static void onAlarmFired(alarm_id_t id, void * /*user_data*/) {
    // Read the snapshot on the worker thread to avoid cross-thread access to the alarm table
    alarm_info_t info{};
    alarm_get_info(id, &info);

    // Switch back to the main thread before operating on JavaScript
    App()->postTask([info] {
        auto *svc = AppletAlarmService::instance();
        // Use launch() to start (or wake up) the target app, even if it is not currently running
        auto *applet = AppletKit::instance()->launch(svc->alarmAppletName);
        if (!applet) return;

        auto &vm = JsVM::current();
        // Call the conventional method exported on the app.js object, passing the alarm info JS object as the event parameter
        JsValue event = js_cast(info);
        applet->modelObject().callMethod("onAlarmFired", {event}).reportError();
    });
}
```

Key points:

- **Do not** directly operate on `JsValue` or call any JavaScript APIs on the worker thread; they can only be used on the UI thread.
- Use `App()->postTask()` to post closures into the main event loop for execution. This is the simplest way to switch back to the UI thread.
- Use `AppletKit::launch()` instead of searching for existing instances; `launch()` restarts the application if it does not exist, and returns the existing instance if it is already running.
- `.reportError()` on the return value of `callMethod()` prints any potential JavaScript exceptions to the log rather than silently ignoring them.

::: tip Conventional method names are the simplest event handling approach
You can think of this pattern as: the exported object of `app.js` is the "set of entry points" exposed by the application to the system. The system calls methods within it when needed, just like calling `onCreate` and `onShow`.

This method is less generic, but it is basically sufficient for controlled system applications, and it is simple to implement without requiring complex persistence and callback management mechanisms.
:::

### Registering the Library Loader

Once all binding functions are written, they need to be "assembled" into a [library object](native-module.md#library-loader) that JavaScript can import, and registered with the framework.

A library loader is a C++ function triggered when an application calls `app.loadLibrary('vendor.alarm')`. It is responsible for creating and returning a JavaScript object containing all exported methods:

```cpp
static JsValue libAlarmLoader(Applet *applet) {
    // You can check the application's package name here to deny unauthorized applications access. You can also check fields.
    if (!applet || applet->objectName() != "com.vendor.alarm")
        return JsValue{};

    JsValue lib = JsVM::current().newObject();

    // Mount binding functions onto the library object; property names are the method names called on the JavaScript side
    lib["create"]     = jsAlarmCreate;
    lib["cancel"]     = jsAlarmCancel;
    lib["list"]       = jsAlarmList;
    lib["count"]      = jsAlarmCount;
    // ...
    return lib;
}
```

Then register the loader with `AppletKit` during the initialization stage:

```cpp
AppletKit kit{&window};
kit.setLibraryLoader("vendor.alarm", libAlarmLoader);
```

Import it via `app.loadLibrary()` on the JavaScript side, and the return value will be the library object returned by the loader:

```javascript
const alarm = app.loadLibrary('vendor.alarm')

const id = await alarm.create({ interval: 60000, label: 'Get up' })
```

============================================================
FILE_PATH: src/transl/EN/cxxdev/widget-export.md

# Widget Registration and Framework Integration

In the [Widget Development Guide](./widget.md), we implemented a C++ widget class. However, at that point, it is merely an ordinary C++ object, and application developers cannot use it directly in page code. This article explains how to register a widget with the framework so that it becomes a component usable within applications. Many concepts in this document relate to the [Object System](./object-system.md); reading that section first is recommended.

## Runtime Environment

Widget registration relies on a set of **runtime environment objects**. These are mandatory dependencies required for the reactive framework to run. They must be explicitly created in `main()` or platform startup code, and their lifecycle must span the entire duration of the application:

```cpp
Application app(/* platform */);
JsVM vm;
Window window;
AppletKit kit(&window, "pkgs.db");
```

These objects manage the runtime environment for the entire application:
- `Application`: The framework application object responsible for all underlying services and maintaining the event loop. At the end of initialization, call `app.exec()` to enter the event loop.
- `JsVM`: The embedded JavaScript engine that hosts the execution of the reactive framework. It **must** be created before `AppletKit`.
- `Window`: The top-level window, serving as the rendering output target.
- `AppletKit`: The applet manager responsible for application lifecycle and widget registration.

::: warning Do Not Omit These Objects
`vm`, `window`, `kit`, and others are RAII objects, and the framework manages the runtime environment through their construction and destruction. Even if direct calls to `vm` are not visible in the code, its **very presence** is required—destroying it prematurely or failing to create it will cause the framework to fail.
:::

`Window window` can sometimes be replaced with `Widget window`, etc. The difference is that `Window` renders an opaque background by default, whereas `Widget` is transparent by default.

## Registering Widgets

Widget registration is accomplished via `AppletKit::installWidget<T>()`. It must be called after `AppletKit` is instantiated and **before** `launch()` starts the first application:

```cpp
// Register a custom widget (before launch)
kit.installWidget<ProgressRing>(); // No arguments, registered by class name, written as <progress-ring> in templates
kit.installWidget<MySpecialChart>("SpecialChart"); // Or register with a custom name (see below)

kit.launch("com.example.app");     // Launch the application
return app.exec();                 // Enter the event loop
```

::: tip Built-in Widgets Are Registered by Default
Built-in widgets provided by the framework, such as buttons and labels, are registered by `installBuiltinWidgets()`. As long as the SDK is built with the CMake option `GX_BUILTIN_BINDINGS` enabled (which is `ON` by default), `AppletKit` will **automatically call** it upon construction without requiring manual handling. You only need to manually call `kit.installBuiltinWidgets()` if you explicitly disable this option.
:::

Upon registration, the framework uses the `GX_OBJECT` metadata of the widget class to automatically export its properties, events, methods, as well as any enum and struct types it uses, making them available at the application layer.

### Using Widgets in Application Pages

Once successfully registered, application developers can use the widget in page templates just like built-in controls:

```xml
<!-- Taking the progress-ring component as an example -->
<progress-ring
  class="ring"
  :value="progress"
  @completed="onDone">
</progress-ring>
```

Here, `:value="progress"` binds the widget's `value` property to the application data `progress`; `@completed` listens for the `completed` event exposed by the widget. The framework automatically handles the bidirectional conversion between JavaScript values and C++ properties without requiring developers to write any "bridge code."

### Custom Component Names

By default, a widget is registered using its **class name**. If the class name is not suitable as a component name directly, a custom name can be specified during registration:

```cpp
// Register VendorWaveformGraph as WaveformGraph, written as <waveform-graph> in templates
kit.installWidget<VendorWaveformGraph>("WaveformGraph");
```

Custom names should use **PascalCase**, matching the style of C++ class names.

### C++ ↔ UX Naming Conventions

The component tag name corresponds to the name used during registration (defaulting to the **class name** declared by `GX_OBJECT`, or the custom name specified during registration). Templates conventionally use kebab-case, and **the ux packaging tool handles name conversion at compile time**:

- Tag names: kebab-case in templates ↔ PascalCase registered name. For example, `<progress-ring>` corresponds to the `ProgressRing` class. The same applies to custom registered names.
- Property names: kebab-case in templates ↔ camelCase in C++. For example, `ring-color` corresponds to the `ringColor` property.

In other words, the runtime framework performs exact matching using the original names declared in C++ (camelCase / PascalCase), while the kebab-case syntax is simply a writing convention on the template side, converted by the ux tool for interconnection.

UX components can also use the same PascalCase for tags and camelCase for properties as C++, as detailed in [Component Naming Specifications](/tutorials/name-spec.md).

## Property and Event Export

Properties declared with `GX_PROPERTY` are automatically exported according to the following rules:

- The property name is directly equivalent to the property name in the framework component.
- Properties with a declared setter (`set xxx`) can be assigned values by the application.
- Properties with a declared getter (`get xxx`) can be read by the application.
- When a signal is declared (`signal xxxChanged`), signals indicating property changes are propagated to bindings.

For example, consider the following complete property declarations:

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

Corresponding usage at the application layer:

```xml
<progress-ring
  :value="jobProgress"
  ring-color="#409EFF"
  :show-label="true">
</progress-ring>
```

In templates, properties are written in kebab-case, corresponding to camelCase property names in C++: `ring-color` → `ringColor`, `show-label` → `showLabel` (conversion is handled by the ux packaging tool, as mentioned above). `:value` and `:show-label` are dynamic bindings (where values are expressions), whereas literal assignments like `ring-color="#409EFF"` are static.

### Event Export

Component events are exported via **properties with change signals**, rather than exporting `Signal<>` members directly. Exporting an event takes two steps:

1. Declare a `Signal<...>` member (for internal C++ use);
2. Reference it in the `signal` field of a `GX_PROPERTY`.

The key rule is: the event name listened to on the application side is the **property name**, **not** the name of the signal member.

### Property Change Events with Values

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    int value() const;
    void setValue(int v);

    Signal<int> valueChanged;   // Internal signal; this name is invisible to the application
    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
};
```

The application side listens for changes using `@property-name`, so here we write `@value` (the property name), **not** `@value-changed`: despite the signal member being named `valueChanged`, the event name visible to the application is always the property name `value`.

```xml
<progress-ring :value="progress" @value="onProgressChanged"></progress-ring>
```

This behavior is completely consistent with built-in framework controls. For instance, the value change signal member of `Slider` is named `changed`, but the application side still listens via the property name `value` (`@value` or two-way binding `::value`).

### Value-less Pure Events

For events that do not carry a value and simply indicate "something happened" (such as "completed"), declare a property with no read/write values but only a signal, using `invalid_t` as the property type:

```cpp
Signal<>  completed;   // Emitted when progress completes
GX_PROPERTY(invalid_t completed, signal completed)
```

The application side can listen to it like this (without an event value):

```xml
<progress-ring @completed="onDone"></progress-ring>
```

You cannot declare a `GX_PROPERTY` with a `void` type, even if it has no `get`/`set` methods at all; hence `invalid_t` must be used as a placeholder type. If you want an event to carry a value, you must declare it as a specific type and provide a `get` method—the parameter type of `Signal<T>` does not automatically become the event value; it always originates from the property's getter.

::: warning `Signal<>` Does Not Automatically Become an Event
Simply declaring a `Signal<>` member without referencing it via the `signal` field in any `GX_PROPERTY` makes that signal **impossible** to listen to on the application side using `@some-event`. The framework only exposes "property change signals"—namely those defined in the `signal` field—as events, and the event name is always derived from the property name.
:::

## Method Export

Member functions declared with `GX_METHOD` are exported as component methods for applications to call in JavaScript:

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    GX_METHOD void reset();               // Method with no arguments
    GX_METHOD void animateTo(int target); // Method with arguments
};
```

Unlike properties and events, methods are not used through template tags; instead, you first obtain the native component object using [`$element()`](../framework/component/component-apis.md#element), and then call methods on it. This requires assigning an `id` to the component in the template:

```xml
<progress-ring id="ring" :value="progress"/>
```

```js
onReady() {
  const ring = this.$element('ring'); // 'ring' is the id of the component in the template
  ring.reset();
  ring.animateTo(80);
}
```

Method arguments and return values are automatically marshaled by the framework via `Variant`, eliminating the need to write manual conversion code (for details on type bridging, see [Object System · Runtime Type System](./object-system.md#运行时类型系统)). Note that `$element()` must be called during or after the [`onReady()`](../framework/component/life-cycle.md#onready) lifecycle; see [Native Component](../framework/component/native-component.md) for details.

## Enum and Struct Types

When the type of a property or method parameter is a custom C++ enum or struct, you can annotate it with `GX_ENUM` or `GX_STRUCT` to export it along with the widget. During [widget registration](#注册控件), the framework automatically installs the corresponding type conversions without requiring hand-written binding code. On the JavaScript side, enums appear as string constants, while structs appear as object literals:

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    // Note: Define aliases for values, otherwise JavaScript will use
    // 'Solid' / 'Dashed' names instead of the expected 'solid' / 'dashed'
    enum GX_ENUM LineStyle {
        Solid GX_ALIAS("solid") = 0,
        Dashed GX_ALIAS("dashed"),
    };
    // Note: Provide default values for structs to avoid undefined fields when created on the JavaScript side
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

For complete semantics regarding enum aliases, struct field mappings, nested types, and more, refer to [Object System · Complex Type Reflection](./object-system.md#复杂类型反射) and will not be further expanded here.

::: warning Do Not Forget Annotations
When a property or method uses a custom enum/struct, be sure to annotate it with `GX_ENUM` / `GX_STRUCT`. Otherwise, it will be unusable on the JavaScript side without any compilation errors.
:::

## Accommodating Child Widgets (Container Widgets)

If a widget needs to contain child content declared by the application, simply implement it as a **container widget**: handle child widget layout on the C++ side, and the framework will automatically create sub-components declared inside the template as child widgets and mount them underneath it. Glyphix does not have HTML-like named slots; nested tags in templates directly become child widgets of that control.

Container layout can be implemented in two ways (detailed in the "Layout and Sizing" section of the [Widget Development Guide](./widget.md)):

- Use existing framework layout classes, such as calling `setLayout(new FlexLayout())` in the constructor;
- Or override `layoutEvent()`, iterating through `children()` within it to manually set the geometry of each child widget.

At the application layer, use it just like nesting child tags (where `card-panel` is a container widget implemented and registered by the developer, and `text` is a built-in widget):

```xml
<card-panel>
  <text>Title</text>
  <progress-ring :value="progress"/>
</card-panel>
```

## A Complete Example

Below is the definition of a simple numerical display control, registered as a framework component:

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

    bool event(Event *event) override;   // The only virtual function that needs to be overridden

    Signal<int> valueChanged;            // Internal signal; application side listens via the property name value

    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
    GX_PROPERTY(Color textColor, get textColor, set setTextColor)

protected:
    // Neither paintEvent nor sizeHint are virtual functions and must not have override
    void paintEvent(PaintEvent *event);
    Size sizeHint() const;

    // EventDispatch requires access to protected handlers
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
    // Dispatch events to paintEvent; declaring PaintEvent enables compile-time checks for omissions
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
    p.setBrush(m_color);   // Text color is determined by the brush, not the pen
    p.setFont(Font(20));
    p.drawText(rect(), format("{}", m_value), AlignCenter);
}
```

Registration:

```cpp
kit.installWidget<NumberDisplay>();
```

Application layer usage:

```xml
<number-display
  :value="count"
  text-color="#333333"
  @value="onCountChanged">
</number-display>
```

At this point, the entire workflow—from C++ implementation to application usage—is complete: the `<number-display>` tag is converted by the ux tool into the registered name `NumberDisplay` and successfully recognized.

Whenever application data `count` changes, the `:value` binding calls `NumberDisplay::setValue()`; when the widget internally emits the `valueChanged` signal, the framework triggers an event named `value` (using the property name), thereby invoking the application's `onCountChanged`. If you want bidirectional synchronization between `count` and the widget, you can use `::value="count"` instead.

============================================================
FILE_PATH: src/transl/EN/cxxdev/async.md

# Asynchronous Function Development

In embedded systems, many operations are time-consuming—reading flash memory, accessing the network, and waiting for hardware responses. If these operations are executed on the UI thread (which is also the rendering thread), they will freeze the UI and cause the application to become unresponsive.

Glyphix solves this problem by seamlessly integrating asynchronous operations with JavaScript's `Promise` mechanism. The C++ side handles the actual asynchronous logic (usually in another thread or via event-driven mechanisms), the JavaScript side waits for the result using `async/await` or `.then()`, and the UI remains smooth during the wait.

## Core Mechanism

The core of the asynchronous functionality is the "Session" model. When a JavaScript asynchronous call is initiated, the C++ side creates a **session object** (`AsyncSession`) and immediately returns a `Promise` to JavaScript; when the operation completes, the session drives the resolution (resolve or reject) of the `Promise`, executing the `then/catch` or `await` on the JavaScript side.

The session object is bound to the `Applet` that initiated the call. When the application exits, the session is automatically cleaned up, eliminating the need for developers to manage memory manually.

The diagram below illustrates the position and core components of asynchronous sessions within the framework:

<ArchDiagram max-width="520px">
  <div>
    JavaScript Application Layer
    <div class="group row">
      <div>async/await<div class="remark">Call module functions</div></div>
      <div>Promise<div class="remark">Wait for async results</div></div>
    </div>
  </div>
  <div class="subject">
    Async Session (C++)
    <div class="group row">
      <div>ResultSession<div class="remark">One-shot query · Promise bridge</div></div>
      <div>Signal&lt;T&gt;<div class="remark">Global event broadcast</div></div>
    </div>
    <div class="group row">
      <div>Client Class<div class="remark">Pure C++ · No JS dependency</div></div>
      <div>SingleTimer<div class="remark">Timeout control</div></div>
    </div>
  </div>
  <div>
    Async Executor
    <div class="group row">
      <div>ThreadPool<div class="remark">Default background execution</div></div>
      <div>Custom Context<div class="remark">Hardware driver · Event loop</div></div>
    </div>
  </div>
</ArchDiagram>

The asynchronous framework implementation is located in `gx_async.h` and encapsulated within the `gx::async` namespace. The framework provides several useful facilities:
- **`async::ResultSession`**: Used for one-shot asynchronous queries, suitable for scenarios like reading files or making network requests.
- **`async::make_timeout()`**: Used to create a single-shot timer that attaches timeout functionality to a one-shot session.
- **`async::Signal<T>`**: Used for global event broadcasts, suitable for scenarios such as device state changes and external event notifications.

## One-Shot Query: ResultSession

`async::ResultSession<T>` is suitable for scenarios where you "initiate a query and wait for a single result," such as reading a file or making a network request. It is the most commonly used asynchronous pattern and works much like an asynchronous function call.

### Working Model

The complete lifecycle of a `ResultSession` is as follows:

1. **Creation**: A module function creates a session via `async::make<ResultSession<T>>(applet)`, and the session is automatically bound to the current `Applet`.
2. **Configuration**: Access the client object via `session->client()` to set the pure C++ parameters required by the task.
3. **Submission**: Call `session->request(resolver)` to submit the task, which immediately returns a `Promise` to JavaScript.
4. **Execution**: The framework forwards the client's `resolve()` method to the **asynchronous executor** (defaulting to a background thread pool) for execution.
5. **Callback**: After `resolve()` returns, the result is **automatically dispatched back to the UI thread** to drive the resolution or rejection of the `Promise`.
6. **Cleanup**: The session object is automatically destroyed after the callback completes, or cleaned up automatically when the `Applet` exits.

::: important Client Class Isolation Requirements
The client class (i.e., the template parameter `T`) runs in the asynchronous context and **must not hold or access any objects that interact with JavaScript**, including `JsValue`, `Applet *`, or any other UI-thread-exclusive objects.

The client class should be a **pure C++ data processing unit**, holding only value-type data required to execute the task (such as `String`, `int`, or custom structures), and completing all work within its `resolve()` method. All interactions between the UI thread and the asynchronous thread are handled automatically by the framework.
:::

### Basic Usage

First, define a client class and implement the `resolve()` method. This method is called in the asynchronous context and returns a result wrapped in `async::Result<T>`:

```cpp
#include "gx_async.h"
#include "gx_file.h"

using namespace gx;

// Client class: pure C++ data processing, holds no JS objects
class ReadTextClient {
public:
    void setPath(const String &path) { m_path = path; }

    // Called in the asynchronous context, returns the operation result
    async::Result<String> resolve() {
        File file(m_path);
        if (!file.open(File::ReadOnly | File::Text))
            return async::Status(300);  // IO error
        int size = int(file.size());
        String text(size);
        text.resize(file.read(text.data(), size));
        return text;  // Success: return file content
    }

    // Optional: Custom error message (used when the Promise is rejected)
    static const char *errorMessage(async::Status status) {
        switch (status.value()) {
        case 300: return "io error";
        default:  return "unknown error";
        }
    }

private:
    String m_path;  // Absolute path that has already passed security validation
};
```

Next, create the session within the module function and return the `Promise`. Note: You **must** use `Applet::resolveUri()` to perform security validation on the path passed from JavaScript rather than blindly trusting the string provided by the application:

```cpp
static JsValue readText(JsCtx ctx) {
    Applet *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1 || !ctx.arg(0).isObject())
        return {};

    // ✅ Secure: Validate and convert the path via resolveUri
    auto uri = applet->resolveUri(ctx.arg(0)["uri"].toString());
    if (uri.empty())
        return {};  // URI validation failed, access denied

    using Session = async::ResultSession<ReadTextClient>;
    auto *session = async::make<Session>(applet);
    session->client().setPath(uri);  // Pass the validated secure path

    // Submit the async task, passing the complete options object for QuickApp callback interface compatibility
    session->request(ctx.arg(0));
    return session->promise();
}
```

::: tip Why pass `ctx.arg(0)`?
`request()` receives the entire `options` object passed from the JavaScript side (i.e., `ctx.arg(0)`), which is used to automatically adapt to both [calling styles](/api/README.md#quickapp-asynchronous-interfaces) of QuickApp asynchronous interfaces:

- If `options` contains any of the `success`, `fail`, or `complete` properties, it is determined to be **callback style**, and the corresponding function is called directly. `request()` does not return a meaningful value;
- Otherwise, it is determined to be **Promise style**, creating a new `Promise`, and `session->promise()` returns that object for the caller to `await`.

This allows the exact same C++ implementation to support both standard QuickApp callback interfaces and modern Promise/async-await interfaces without any extra code. If you are certain you only want to support the Promise style, you can also pass an empty value `{}`.
:::

::: danger Do not skip URI validation
Using a string passed directly from JavaScript as a file path is a severe security vulnerability:

```cpp
// ❌ Dangerous! Bypasses the sandbox's path security checks
session->client().setPath(ctx.arg(0)["uri"].toString());
```

Malicious applications can use path traversal (such as `../../etc/passwd`) to access the file system outside the sandbox. All paths coming from JavaScript **must** be sanitized via `Applet::resolveUri()`, which detects path traversal attacks, cross-app unauthorized access, and invalid URI formats, returning an empty string if validation fails.
:::

Usage on the JavaScript side:

```javascript
import file from '@system.file'

async function loadConfig() {
    try {
        const text = await file.readText({
          uri: 'internal://files/config.json'
        })
        console.log('config:', text)
    } catch (err) {
        console.error('read failed:', err.message)
    }
}
```

### Errors and Status Codes

`async::Status` encapsulates an integer status code, where `0` (i.e., `async::OK`) represents success, and other values represent custom business error codes:

```cpp
// Success: Return value directly, status code defaults to OK
return async::Result<String>{std::move(content)};
// Failure: Return status code only, value part is ignored
return async::Status(404);
// Carry both a partial result and a non-OK status (e.g., HTTP 206 Partial Content)
return async::Result<ByteArray>{
  std::move(partialData),
  async::Status(206)
};
```

When `resolve()` returns an error status, the `Promise` is rejected, and JavaScript's `catch` block receives an error object containing `message` and `code` fields. The `message` comes from the `errorMessage()` static method of the client class.

`errorMessage()` supports multiple signatures, which the framework automatically recognizes:

```cpp
// Form 1: Accepts Status (Recommended, concise)
static const char *errorMessage(async::Status status);

// Form 2: Accepts the complete Result, allowing message generation based on both value and status
static String errorMessage(const async::Result<MyType> &result);
```

If the client class does not define `errorMessage()`, the framework defaults to `"unknown async error"`.

### Value Types and JavaScript Conversion

The value returned by `resolve()` is not passed to JavaScript as-is; the framework uses the `js_cast()` function to automatically convert C++ types into `JsValue` before driving the `Promise` resolution. This process happens entirely within the framework and appears "transparent," but it actually relies on a set of **implicit conventions**: only types that implement `js_cast()` specializations can be correctly converted. Custom enums, structs, and other types require explicit conversion relationships to be established, otherwise compilation will fail.

#### Built-in Supported Types

The following types can be used directly as type parameters for `Result<T>` without extra work:

| C++ Type | Corresponding JavaScript Type | Remarks |
| --- | --- | --- |
| `int`, `double`, `float` | `number` | Direct numerical mapping |
| `bool` | `boolean` | Direct boolean mapping |
| `String`, `StringView`, `const char *` | `string` | Direct string mapping |
| `ByteArray` | `ArrayBuffer` | Binary data |
| `JsonValue` | `object` / `array` | JSON object or array |
| [`std::vector<T>`](https://en.cppreference.com/w/cpp/container/vector) | `Array` | Array, elements recursively converted (`T` itself must also be convertible) |
| `JsValue` | Any | Passed directly without conversion |
| `void` (i.e., `Result<void>`) | `undefined` | No return value |

These types all have built-in `js_cast<T>()` specializations in the JsVM framework. Some are types that `JsValue` can construct directly, while others implement conversion logic via specializations.

#### Adding Conversion Support for Custom Types

If the type you are using is not in the list above, the compiler will throw an error indicating that `JsValue` cannot be constructed. There are two ways to resolve this:

**Approach 1: Define an `operator JsValue()` Member Function**

This is suitable for custom structs whose definitions you can modify. The advantage is that the conversion logic is built directly into the type definition, creating tight coupling:

```cpp
struct DeviceInfo {
    String model;
    int version;

    // Convert struct to JavaScript object
    // Note: Conversion runs on the UI thread, where a valid JsVM context exists
    operator JsValue() const {
        JsVM &vm = JsVM::current();
        JsValue obj = vm.newObject();
        obj["model"] = JsValue(model);
        obj["version"] = JsValue(version);
        return obj;
    }
};
```

Once defined, `Result<DeviceInfo>` can be used directly:

```cpp
async::Result<DeviceInfo> resolve() {
    return DeviceInfo{"ModelX", 3};  // Framework automatically calls operator JsValue()
}
```

APIs used inside `operator JsValue()`, such as `JsVM::current()` and `vm.newObject()`, belong to the JsVM bridge layer. For details, see the [Native Module Development Documentation](./native-module.md#creating-and-returning-objects).

**Approach 2: [Specializing](https://en.cppreference.com/w/cpp/language/template_specialization) `js_cast<T>` in the `gx` Namespace**

Suitable for situations where the original type definition cannot be modified (such as externally defined types or enums):

```cpp
// Declare the specialization prior to use if necessary
template<>
JsValue gx::js_cast<ConnectionState>(const ConnectionState &x);

// Specialize within the gx namespace
template<>
JsValue gx::js_cast<ConnectionState>(const ConnectionState &x) {
    switch (x) {
    case ConnectionState::Connected:    return "connected";
    case ConnectionState::Connecting:   return "connecting";
    case ConnectionState::Disconnected: return "disconnected";
    default:                            return "unknown";
    }
}
```

Once specialized, both `Result<ConnectionState>` and `Signal<ConnectionState>` will work normally.

::: tip Simple Approach for Integer Enums
If your enum values directly correspond to integers, manually casting to `int` inside `resolve()` is the easiest method and requires no specializations at all:

```cpp
async::Result<int> resolve() {
    return async::Result<int>{int(myEnum)};
}
```
:::

#### Runtime Conversion Overhead

`js_cast()` is executed **after** the asynchronous result is delivered back to the UI thread, not in the asynchronous thread. The time cost of conversion occurs entirely on the UI thread; for complex structures, you must ensure it is fast enough to avoid frame drops. The actual cost of each type is as follows:

- **Zero-overhead types**: `int`, `double`, `bool`, `String`, and `const char *` are mapped directly via `JsValue` constructors with no extra copies or heap allocations. The `operator JsValue()` approach and `js_cast<T>` specializations are also inlined at compile-time with no virtual calls or indirection layers.
- **Linear-overhead types**: `std::vector<T>` requires calling `setIndex()` element by element, with an overhead proportional to the number of elements. If the returned structure is an object with fixed fields, prefer using `operator JsValue()` to manually construct the JS object, which is more efficient and easier to read than an array.
- **Tree-traversal types**: `JsonValue` recursively traverses the entire tree during conversion, constructing JavaScript nodes one by one, making it the highest-overhead built-in type. If the data structure is known at compile-time, `operator JsValue()` constructing the object directly is usually faster and avoids the construction cost of `JsonValue` itself.
- **Custom structs**: If you use `operator JsValue()` or `js_cast()` specializations, conversion performance depends on the conversion overhead of each member type, i.e., the complexity of constructing the object.

::: tip Simple Decision Criterion
If your asynchronous data structures are simple (numbers, simple struct objects, or small `JsonValue`s), the conversion overhead will generally not impact UI fluidity.
:::

#### No Serialization Intermediary Layer

Some asynchronous frameworks require that when passing data between a worker thread and the UI thread, results must first be serialized into JSON or another self-describing format and then deserialized on the UI thread. This is done to achieve "type-erased" passing between threads, but at the cost of incurring string (or binary data stream) concatenation, transmission, and parsing overhead on every call. Worse still, it may construct multiple copies of the data (such as intermediate serialized data alongside the original data).

The async framework **does not rely on a serialization intermediary layer.** Results are moved across threads as native C++ values via `async::Result<T>`, completely bypassing the serialization process:

```
worker thread                  UI thread
resolve(Result<MyType>{...}) → js_cast(result.value()) → JsValue (JavaScript)
                  ↑
             Direct memory movement, no JSON strings
```

`js_cast()` is only executed after the result has safely returned to the UI thread; its job is to map C++ values to the JavaScript engine's internal representation, not to act as an inter-thread communication protocol.

If you voluntarily choose to use `JsonValue` as the type parameter for `Result<T>` (to mitigate template code bloat), you are introducing the **construction and tree traversal** overhead of `JsonValue`, not string serialization. `JsonValue` itself is also an in-memory tree structure, not a text format.

#### Template Code Size

`ResultSession<T>` is a template class, meaning the compiler generates an independent copy of code for each distinct client type `T`. However, the framework extracts the vast majority of logic unrelated to `T` (such as `Promise` management, event dispatching, and `Applet` lifecycle binding) into the non-template base class `detail::ResultSession`. Therefore, the additional code size generated for each `T` is primarily concentrated in the lightweight `Resolver` adaptation layer.

However, if a project contains **a large number of fine-grained client types used only once**, the accumulated number of instantiations can still lead to a noticeable increase in code size.

A common compression technique is to use `JsonValue` as a type-erasure medium, merging multiple scattered small functions into a single client type:

```cpp
// Before merging: Each operation is an independent client class + independent template instantiation
struct GetVersionClient { ... };   // ResultSession<GetVersionClient>
struct GetModelClient   { ... };   // ResultSession<GetModelClient>
struct GetSerialClient  { ... };   // ResultSession<GetSerialClient>

// After merging: Share the same template instantiation, distinguishing operations at runtime
struct DeviceQueryClient {
    enum Kind { Version, Model, Serial } kind;

    // A switch dispatch is demonstrated here, but function pointers can also be used.
    // However, avoid using BaseClient with derived classes overriding resolve() for polymorphism,
    // as it introduces more vtable bloat than the function pointer approach.
    async::Result<JsonValue> resolve() {
        switch (kind) {
        case Kind::Version: return JsonValue{getVersion()};
        case Kind::Model:   return JsonValue{getModel()};
        case Kind::Serial:  return JsonValue{getSerial()};
        }
    }
};

// Three module functions share a single instantiation of ResultSession<DeviceQueryClient>
static JsValue getVersion(JsCtx ctx) {
    using Session = async::ResultSession<DeviceQueryClient>;
    auto *session = async::make<Session>(applet);
    session->client().kind = DeviceQueryClient::Version;
    return session->request(ctx.arg(0));
}
```

The trade-off of this approach is that the return type degrades to `JsonValue`, incurring extra runtime conversion overhead (see above). Therefore, it is suitable for scenarios with **small data volumes and a high number of functions**, trading a small amount of runtime overhead for meaningful code size savings. For data-intensive or performance-sensitive operations, independent strongly-typed client classes should still be retained.

### Custom Asynchronous Contexts

By default, `session->request()` submits `resolve()` to the framework's **asynchronous executor**—typically a background thread pool. However, some scenarios require using a different asynchronous context, such as a custom event loop or AIO multiplexing mechanism, neither of which wants to consume extra thread resources.

In such cases, you can bypass `request()` and manually control the asynchronous execution flow yourself. The client class does not need to implement a `resolve()` execution function either. The key is: **After completing work in the asynchronous context, call `session->resolve()` to deliver the result back to the UI thread.**

```cpp
// Client class: No need to implement resolve() since the default thread pool is not used
struct FirmwareCheckClient {
    // Only define errorMessage() for error description
    static const char *errorMessage(async::Status status) {
        switch (status.value()) {
        case 1: return "firmware not found";
        case 2: return "check failed";
        default: return "unknown error";
        }
    }
};

static JsValue checkFirmwareUpdate(JsCtx ctx) {
    Applet *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1) return {};

    using Session = async::ResultSession<FirmwareCheckClient>;
    auto *session = async::make<Session>(applet);
    auto version = ctx.arg(0).asString();

    // Manually set resolver (do not call request, do not use default thread pool)
    session->setResolver(ctx.arg(0));
    JsValue promise = session->promise();

    // Submit to a custom hardware driver thread
    HardwareDriver::checkUpdate(
        version,
        // Callbacks may run on any thread—the framework automatically dispatches back to the UI thread
        [session](bool available) {
            session->resolve<bool>(available);
        },
        [session](int errorCode) {
            session->resolve<bool>(async::Status(errorCode));
        }
    );

    return promise;
}
```

The core differences here:
- `request()` performs both "setting the resolver" and "submitting to the async executor" in one step;
- In manual mode, you must call `setResolver()` yourself to set the response target, and then push results or error statuses via `session->resolve()` at any arbitrary time.

`resolve()` is thread-safe; it packages the result as an event, posts it back to the UI thread, and then resolves the `Promise`.

::: tip When to Use Custom Contexts
- The underlying driver already provides a callback interface and you do not want to create extra threads: simply `resolve` directly inside the driver callback.
- You need to integrate with an existing AIO/epoll event loop: `resolve` inside the event completion callback.
- Serialized execution is required (e.g., operations must run in order): schedule using your own task queue and `resolve` when finished.

As long as you ensure `session->resolve()` is eventually called once, the framework does not care which thread the result is posted from.
:::

### Value Type Semantics

Since the `async::Result<T>` value returned by `resolve()` (or proactively posted by a custom async context) is dispatched to the UI thread before being converted to `JsValue`, the data type `T` must be moveable. All built-in supported types satisfy this requirement. For custom types:
- If it is a struct containing only built-in supported type members, the C++ standard guarantees it is moveable.
- If you use raw pointers and manage their ownership yourself, you must correctly implement a [move constructor](https://en.cppreference.com/w/cpp/language/move_constructor).
- [Trivial types](https://en.cppreference.com/w/cpp/named_req/TrivialType) (such as pure C structs and enums) satisfy value type semantics by default.

Note that non-trivial types typically contain resources on the heap, and writing code like this may lead to memory peak issues:

```cpp
auto *session = getFetchLargeDataSession();
std::vector<uint32_t> data = fetchDataFromNetwork(url);
session->resolve<decltype(data)>(data);  // Results in a full copy of data
```
This happens because parameters in `session->resolve()` are passed by value, and passing `data` invokes the [copy constructor](https://en.cppreference.com/w/cpp/language/copy_constructor), resulting in a full copy. If `data` is large, this will double memory usage. When this occurs, the compiler issues a warning:
```
'...' is deprecated:
avoid use copy semantics of Result<T> if T is not trivially copyable
```
The correct approach is to explicitly enable move semantics using [`std::move()`](https://en.cppreference.com/w/cpp/utility/move):

```cpp
auto *session = getFetchLargeDataSession();
std::vector<uint32_t> data = fetchDataFromNetwork(url);
session->resolve<decltype(data)>(std::move(data));  // Uses move semantics
```

### Timeout Control

For asynchronous operations that may hang indefinitely without a response, use `async::make_timeout()` to add timeout protection to the session. Upon timing out, the `Promise` is automatically rejected, preventing the JavaScript side from hanging permanently.

The following code snippet demonstrates a basic example of how to use timeout control in a network request:

```cpp
static JsValue fetchData(JsCtx ctx) {
    Applet *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1) return {};

    String url = ctx.arg(0)["url"].asString();
    int timeoutMs = ctx.arg(0)["timeout"].asInt(5000);

    using Session = async::ResultSession<HttpClient>;
    auto *session = async::make<Session>(applet);
    session->client().setUrl(url);
    session->setResolver(ctx.arg(0));
    JsValue promise = session->promise();

    // Create timeout protection: automatically reject Promise upon timeout
    auto handle = async::make_timeout(session, timeoutMs,
        [](Session *s) {
            // Timeout handling: ongoing async operations should be cancelled here
            s->fulfill(async::Status(408));  // 408 Request Timeout
            
        });

    // Move handle into the asynchronous execution context
    NetworkDriver::fetch(url,
        [handle = std::move(handle)](auto &response) {
            // If timed out, resolve will be safely ignored
            handle->resolve<String>(std::move(response.body));
        });

    return promise;
}
```

#### How It Works

Key workflow of `make_timeout()`:

1. **Moves** the client data of the `session` into an internal class; `session->client()` must not be accessed thereafter.
2. Starts a single-shot timer, returning a `SharedRef<SingleTimer>` handle.
3. **Happy path**: `handle->resolve()` is called before the timeout, atomically taking ownership of the session and dispatching the result event. When the timer subsequently fires, it finds the session empty and takes no action.
4. **Timeout path**: The timer fires, executing the callback **on the UI thread**. The developer calls `session->fulfill()` inside the callback to post an error status; after the callback returns, the timer is responsible for `delete session`.
5. **App exit**: When the `Applet` is destroyed, the timer is automatically unbound, the session is deleted, and the callback is never triggered.

This mechanism is particularly useful for scenarios where underlying asynchronous operations lack built-in timeout mechanisms, such as certain network request implementations. As is well known, implementing timeout protection correctly can be tricky; you must properly handle race conditions and lifecycle safety across all code paths.

`make_timeout()` relies on these preconditions to guarantee safety:
- The client type (i.e., `T` in `ResultSession<T>`) must be **moveable**, which is somewhat of a legacy limitation.
- Asynchronous operations must support safe cancellation on the UI thread, which means removing task listeners and releasing references to `handle`.

#### Callback Thread and `fulfill()`

Timeout callbacks (the third argument to `make_timeout()`) **always run on the UI thread** because they are triggered by a `Timer`, whose events are dispatched by the main event loop.

This dictates that you **must** use `session->fulfill()` inside the callback rather than `session->resolve()`:

| Method | Callable Thread | Impact on Session |
| --- | --- | --- |
| `resolve(result)` | Any thread | Posts a Consume event; session is **deleted** after being processed on the UI thread |
| `fulfill(result)` | **UI Thread Only** | Dispatches results directly **without deleting** the session |

The timeout path of `make_timeout()` is handled by the timer itself, which calls `delete session` after the callback finishes. If you were to call `session->resolve()` inside the callback, it would also post an event to delete the session, creating a **double free** conflict with the timer's `delete`, resulting in undefined behavior. `fulfill()` only dispatches results and does not touch the session's lifecycle, making it the only safe choice inside callbacks.

`fulfill()` accepts `async::Result<R>` or directly accepts an `async::Status` (shorthand when there is no result value):

```cpp
auto handle = async::make_timeout(session, 5000, [](Session *s) {
    s->fulfill(async::Status(408)); // Populate error status only
    // Or carry both value and status:
    s->fulfill(async::Result<String>{"partial", async::Status(206)});
    // ❌ Do not call s->resolve(); it causes a double free with the timer's delete session
});
```

::: tip
The rule of thumb is simple: Where does ownership of the session lie, and who is responsible for deleting it?
- **Happy path**: `handle->resolve()` atomically takes ownership of the session internally, and the session is deleted after the Consume event is processed.
- **Timeout callback**: The timer takes ownership of the session and deletes it after the callback finishes. Therefore, you can only use `fulfill()` to post results inside the callback.
:::

#### Accessing Client Data

If the timeout callback needs to read client data to decide on an error strategy, use the extended callback signature `(Session *, const T &)`. **Do not** call `session->client()` inside the callback—the client has already been moved into the timer:

```cpp
auto handle = async::make_timeout(session, 3000,
    [](Session *s, const HttpClient &client) { // auto &client can also be used
        // ✅ Access client data via the second parameter
        LogWarn() << "request timeout: " << client.url();
        s->fulfill(async::Status(408));
    }
);
```

#### Resource Lifecycle Management

When a timeout occurs, you need to cancel the ongoing asynchronous task inside the callback to release references to `handle`. `SingleTimer` uses reference counting to manage its lifecycle—if an asynchronous task holds a reference to `handle` but never completes, a memory leak will occur:

```cpp
auto task = AioTask::create();
auto handle = async::make_timeout(session, 5000,
    [task](auto *s) {
        task->cancel();     // Cancel the task, releasing the reference to handle
        s->fulfill(async::Status(408)); // reject Promise
    });

// Task completion callback holds a reference to handle
task->start([handle = std::move(handle)](auto &result) {
    handle->resolve(result);
});
```

::: important
The `handle` returned by `make_timeout()` **must** also be referenced by the asynchronous task (captured by the lambda in the example above) to ensure the timer is not destroyed before the task finishes. Otherwise, it will immediately trigger the timeout callback and `Promise` rejection, preventing the task from completing normally.
:::

Such memory leaks are caused by two factors:
1. **Async framework leak**: The `handle` reference is forgotten, preventing related session objects from being released.
2. **Underlying task leak**: The async task itself blocks in an uncompleted state, leaving related resources uncleaned.

### Automatic Cleanup on Application Exit

When an `Applet` is destroyed (e.g., the user closes the app or the system reaps resources), all asynchronous sessions bound to that `Applet` are automatically cleaned up:

- The session's `unbind()` method is called, which closes the session and releases the `Promise` reference.
- If `make_timeout` is being used, the timer is similarly unbound, and the internally held session is deleted.
- The `Promise` on the JavaScript side will never be resolved or rejected—but since the JavaScript environment itself is also being destroyed at this point, this is completely safe.

This means you **do not** need to manually track and cancel asynchronous tasks—the framework guarantees that:
- Posting results to a destroyed `Applet` will not lead to dangling pointer accesses.
- Callbacks will not execute within a released JavaScript environment.
- Asynchronous sessions will not leak after application exit.

Specifically, when a background thread calls `resolve()` to post a result back to the UI thread, the handling function checks whether the `applet()` is still valid. If the `Applet` has already been destroyed, causing `applet()` to return `nullptr`, the framework safely discards the result without executing any JavaScript operations.

::: tip Safe Returns in Asynchronous Contexts
Because `resolve()` is purely data posting (via an event queue), calling `resolve()` in a background thread will not crash even if the `Applet` has already been destroyed. Background threads do not need to care about the liveness state of the `Applet`; that is the framework's responsibility.
:::

The only thing to note is that if you subclass `ResultSession` and introduce additional `JsValue` member variables, you must clean up those members in `unbind()` to avoid memory leaks:

```cpp
class MySession : public async::ResultSession<MyClient> {
public:
    void unbind() override {
        m_callbacks = {}; // Clean up any held JsValue to prevent leaks
        async::ResultSession::unbind(); // Call base class cleanup
    }

private:
    JsValue m_callbacks; // Members that need manual cleanup
};
```

::: important Lifespan Extension of `ResultSession`
If there are still incomplete asynchronous sessions when the app exits, the framework only cleans up resources related to the app (such as `Promise` references and binding relationships), but **does not destroy the session object itself**. This manifests as the lifespan of the `ResultSession` being extended until the asynchronous operation completes.

While this ensures memory safety, it causes some resource releases to be delayed. Therefore, asynchronous tasks must guarantee completion within a finite amount of time and cannot hang indefinitely.
:::

## Multi-Shot Query: ListenSession

This class of APIs is still unstable and is not yet open for public use.

## Global Event Broadcast: async::Signal

If a C++ event needs to be broadcast to **multiple applications** (rather than targeting a single specific caller), use `async::Signal<T>`. It "multicasts" underlying hardware or system events to all JavaScript listeners subscribed to it.

`async::Signal<T>` and `ResultSession` have different positioning:

| Feature | ResultSession | Signal |
| --- | :---: | :---: |
| Communication Direction | One-to-one (Caller → Result) | One-to-many (Event source → All subscribers) |
| Trigger Count | Single-shot | Multi-shot |
| Bound Object | Single Applet | Cross-Applet |
| Use Cases | Async queries, requests | System events, state changes |

### Basic Usage

Suppose there is a battery level change event that needs to be notified to all subscribers:

```cpp
// Define a global signal, typically a member variable of the corresponding service
async::Signal<int> batteryChanged;

// Trigger the signal when a hardware event occurs (can be called on any thread)
void onBatteryLevelChanged(int newLevel) {
    batteryChanged(newLevel);  // Notify all subscribers
}
```

#### Binding & Unbinding

This module function allows the JavaScript side to subscribe to the signal and returns a binding ID for the JavaScript side to unsubscribe:

```cpp
static JsValue subscribeBatteryChange(JsCtx ctx) {
    if (ctx.argc() < 1 || !ctx.arg(0).isFunction())
        return {};
    // Must be in a valid applet environment to subscribe
    auto *applet = Applet::current(ctx.vm());
    if (applet == nullptr) return {};

    // Bind the slot to the app, automatically unsubscribing when the app exits
    auto *slot = batteryChanged.connect(ctx.arg(0));
    return applet->bindObject(slot); // Return slot ID for JavaScript to cancel
}
```

You also need to implement a module function for unbinding. Regardless of the `async::Signal` type, the implementation of the unbind function is very standardized:

```cpp
static JsValue unsubscribeBatteryChange(JsCtx ctx) {
    auto *applet = Applet::current(ctx.vm());
    if (applet && ctx.argc()) {
        // slotId defaults to 0 and can be safely ignored without performing any operation
        auto slotId = ctx.arg(0).toInt();
        // Unbind the slot from the applet and then delete the slot object
        delete applet->unbindObject<async::Slot>(slotId);
    }
    return {};
}
```

#### JavaScript Export

You simply need to define a [Native Module](./native-module.md) to export these functions:

```cpp
static JsModule *createBatteryModule(JsVM &vm) {
    auto mod = vm.newObject();
    // The battery module usually has other functions like getLevel(), omitted here
    mod["subscribe"] = subscribeBatteryChange;
    mod["unsubscribe"] = unsubscribeBatteryChange;
    return mod;
}
// Don't forget to import the module using GX_JSVM_MODULE
GX_JSVM_MODULE(vendor_battery, "vendor.battery", createBatteryModule)
```

::: tip Reusing the `unsubscribe` Function
Since the implementation of the unbind function is very general, you can define a single general `unsubscribe` function and import it into multiple modules.
:::

On the JavaScript side:

```js
import battery from '@vendor.battery'

const sid = battery.subscribe((level) => {
  console.log('battery level:', level)
})

// Call when you need to unsubscribe
battery.unsubscribe(sid)
```

### Signal Delivery Modes

`Signal` supports two delivery modes, controlled by the second argument:

```cpp
// Normal mode (default): Notify all subscribers
batteryChanged(newLevel, async::NormalSignal);

// Skip invisible apps: Only notify foreground visible apps to reduce unnecessary resource consumption
batteryChanged(newLevel, async::SkipInvisible);
```

The `SkipInvisible` mode is suitable for events that only make sense when the UI is visible (such as interface refresh notifications). For events that require background awareness (such as low battery warnings), the default `NormalSignal` should be used.

### Signal Value Types

The type parameter `T` in `Signal<T>` follows the exact same conversion rules as `ResultSession`: when a signal is triggered, the framework converts C++ values into JavaScript callback parameters via the same `js_cast()` mechanism. Built-in types like `int`, `bool`, `String`, and `JsonValue` can be used directly. To pass custom structs or enums, refer to the methods in [Value Types and JavaScript Conversion](#value-types-and-javascript-conversion).

## Thread Safety Notes

The thread safety model of the asynchronous framework follows these rules:

- **`resolve()` is thread-safe**: `ResultSession::resolve()` and `SingleTimer::resolve()` can be called on any thread. They post results to the UI thread via the event system and do not operate on JavaScript objects directly.
- **`JsValue` is not thread-safe**: `JsValue` manages its lifecycle via reference counting, and its reference-counting operations are not atomic. You must not create, copy, destroy, or access `JsValue` instances in asynchronous threads. This is precisely why client classes must not hold `JsValue` objects.
- **`Promise` resolution executes on the UI thread**: Regardless of which thread `resolve()` is called from, the final JavaScript `Promise` callback always executes on the UI thread, ensuring UI operation safety.
- **`async::Signal` notifications are dispatched on the UI thread**: Although `async::Signal::operator()` can be called cross-thread, JavaScript callbacks always execute on the UI thread.

If a client class needs to share state with the UI thread (such as providing a cancellation flag), use atomic operations like [`std::atomic`](https://en.cppreference.com/w/cpp/atomic/atomic) or mutexes to protect the shared data:

```cpp
class CancellableClient {
public:
    void cancel() { m_cancelled.store(true); }

    async::Result<String> resolve() {
        for (int i = 0; i < 100 && !m_cancelled.load(); ++i) {
            // Execute step-by-step tasks, periodically checking the cancellation flag
            processChunk(i);
        }
        if (m_cancelled.load())
            return async::Status(499);  // Client cancelled
        return std::move(m_result);
    }

private:
    std::atomic_bool m_cancelled{false};
    String m_result;
};
```

Notably, many value types in the Glyphix framework **can** be safely passed across threads **within this asynchronous framework**, such as:
- `String`: Can be directly assigned and accessed across multi-threads without extra synchronization mechanisms.
- `JsonValue`: This class is also a value type and possesses the same thread-safety characteristics as `String`.
- `ByteArray`: Similar to `String`, supporting cross-thread usage.
- `SharedRef<T>`: The reference-counted smart pointer itself can be passed across threads, but the thread safety of the managed object `T` depends on its own definition.
- Non-owning types like `String::View` **cannot** be used across threads.

This is why, in all the preceding examples, we always directly capture and pass types like `String` across asynchronous contexts without needing special handling, nor do we need to use mutexes or other synchronization mechanisms to protect them.

::: important
The thread safety of the aforementioned types actually relies on the specific memory model of the asynchronous framework, meaning they are **not automatically thread-safe** in all scenarios. The asynchronous framework described in this document guarantees this behavior, but it cannot be generalized to every context.
:::

============================================================
FILE_PATH: src/transl/EN/cxxdev/global-assets-migrate.md

# Global Resource Migration Guide

This document is intended for downstream Glyphix integration projects, helping you upgrade global resource loading methods from legacy projects to the latest scheme. This provides an easily manageable and editable global resource layout, eliminating the dependency on vendor packaging or conversion tools.

In the early days, Glyphix used the `global.pkg` binary archive package to manage global resources (font files, font mapping tables, etc.). Later, it gradually evolved to directly use unpackaged resource files, and finally, the format of the font mapping file was transitioned from binary to standard JSON <version-badge since="0.9" />. If the entry code you maintain still uses the old syntax, you can follow this article to upgrade.

::: tip
Using the old mode brings maintenance hassles and difficulties in managing and editing global resources. It is strongly recommended to upgrade immediately.
:::

## Removing `global.pkg`

### Characteristics of Old Code

If your entry code contains either of the following patterns, it means you are using `global.pkg`:

```cpp
EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
static String globalUri(const String &path) { return "pkg:///" + path; }
```

The effect of these two lines is to route all resource requests with the `pkg:///` protocol to files inside the `/global.pkg` binary archive package.

Why it needs to be removed:
- Every time fonts or other resources are changed, the packaging tool must be re-run to generate the `.pkg` file.
- Individual files inside `.pkg` cannot be directly viewed or replaced during debugging, making content verification difficult.
- The packaging workflow depends on dedicated tools, increasing communication and maintenance costs.

### Migration Steps

**Step 1: Extract resources from `global.pkg`.**

If you no longer have the source `.pkg` file, you can extract the contents from `global.pkg` (using the Glyphix command-line tool or by requesting the original resource files). Typically, you need to extract the following:

```
fonts/
    NotoSans-Regular.ttf
    NotoSansSC-Regular.ttf
    ...
    font-faces          ← Font mapping file (will be upgraded to JSON later)
```

Place the extracted directory into your project's resource directory, for example, `/fonts/`.

**Step 2: Remove code related to `global.pkg`.**

1. Delete the entire line `EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg")`.
2. Delete wrapper functions like `globalUri()`.
3. Change all resource references of `pkg:///xxx` to direct file paths, i.e., `/xxx`.

**Step 3: Modify font loading code.**

Assuming your initialization code originally looked like this:

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

Change it to use direct file paths (without the `globalUri()` function and `GlobalPackage` registration):

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

At this stage, the resource layout becomes:

```
/fonts/
    font-faces          ← Binary format
    NotoSans-Regular.ttf
    ...
```

At this phase, you are still using the binary `font-faces` file. The next section upgrades it to JSON.

## Switching to JSON Font Mapping Files

### Characteristics of Old Code

```cpp
FontFaceMap &map = App()->fontManager()->faces();
map.readFile("/fonts/font-faces");
```

`readFile` reads a custom binary format file. This binary file cannot be edited manually and must be converted and generated from a CSS file using a packaging tool.

### JSON Format Description

Now we describe font mapping relationships directly using a JSON file. You only need to create a `font-faces.json` file with the following format:

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

Field Descriptions:

| Field | Type | Required | Default Value | Description |
|------|------|------|--------|------|
| `family` | String | Yes | - | Font family name, e.g., `sans-serif`, `serif` |
| `weight` | Integer | No | 400 | CSS font weight value (100-900), 400 is regular, 700 is bold |
| `style` | String | No | normal | Font style, options are `italic` or `oblique` |
| `urls` | Array of strings | Yes | - | Font file path, relative to the directory where the JSON file is located |

Further explanations for key fields are provided below.

**The `weight` Field**

For `weight`, input the CSS font weight numerical value directly, which will be rounded to the nearest standard value:

- `100` Thin
- `400` Regular (default value, can be omitted)
- `700` Bold
- `900` Black

**`urls` Path Resolution**

Paths in `urls` are resolved relative to the directory where the JSON file is located. For example, if the JSON file is located at `/fonts/font-faces.json`, writing `"fonts/NotoSans-Regular.ttf"` in `urls` will ultimately resolve to `/fonts/fonts/NotoSans-Regular.ttf`.

Therefore, it is recommended to place the JSON file directly in the same directory as the font files so that URLs can just use the file names. For example, the directory layout:

```
/fonts/
    font-faces.json
    NotoSans-Regular.ttf
    NotoSansSC-Regular.ttf
    NotoSans-Bold.ttf
```

In this case, the JSON content is as shown in the code above.

### Code Modifications

Replace `readFile` in the initialization code with `readJSON`:

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

This is the only API call change; the rest of the code remains unchanged. Afterward, you can directly edit `font-faces.json` to add/remove fonts or adjust mapping relationships, without needing any conversion tools.

## FAQ

**How to handle multiple variants (like Regular, Bold, Italic) for the same family?**

Add independent entries for each variant in the `font-faces` array, distinguished by `weight` and `style`:

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

MCU projects typically only use the Regular `sans-serif` font with `normal` weight, and the system will fall back automatically.

**Can the `urls` array contain multiple files? When is it needed?**

Yes. When a font family needs to cover multi-language characters, put multiple font files into the same `urls` array. For example, `sans-serif` needs to support Latin letters, CJK characters, and Arabic simultaneously:

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

When rendering text, the engine will look up character glyphs in these files sequentially, and the first matched glyph will be used.

**Must the font files be in the same directory as the JSON?**

No. Paths in `urls` are resolved relative to the directory where the JSON file is located, so you can use relative paths to place fonts in subdirectories. Absolute paths can also be used, in which case they are unaffected by the JSON directory.

**Can a JSON string be passed directly in the code?**

Yes. Use the two-parameter overloaded version:

```cpp
map.readJSON("/fonts/", R"({
  "font-faces": [
    {"family": "sans-serif", "urls": ["NotoSans-Regular.ttf"]}
  ]
})");
```

The first parameter is `baseUri`, used to resolve relative paths in `urls`.

============================================================
FILE_PATH: src/transl/EN/cxxdev/cpp-guide.md

# C++ Learning Recommendations

This document is not a C++ tutorial, but rather a set of quick learning recommendations to provide prerequisite knowledge for developers preparing to read the documents in this directory.

It assumes that you have long-term experience using C, and are familiar with MCUs, RTOS, drivers, LVGL, or similar embedded frameworks; you should have extensive programming experience, but may not be familiar with the subset of C++ required by Glyphix.

::: tip
If your goal is to develop Native Modules, asynchronous features, or Native Widgets, please read this article first before proceeding to the [Object System](./object-system.md) and other chapters. This will help you avoid many issues where "the code makes sense, but you just can't write it."
:::

## C++ Feature Subset

The Glyphix project disables certain C++ features, so developers do not need to learn them at all:

- **RTTI** is disabled: You cannot use `dynamic_cast`, `typeid`, or other runtime type identification mechanisms. When you need a safe downcast, use [`dyn_cast`](object-system.md#动态类型转换) directly.
- **Exceptions** are disabled: There is no need to learn `try` / `catch` / `throw` as a primary path. For error handling, prioritize return values, status codes, object states, and explicit checks. This is similar to C error-handling habits.


In addition, the Glyphix runtime has some special constraints, mainly caused by the fragmentation and compatibility limitations of MCU systems:
1. Concurrency tools from the C++ standard library, such as `std::thread` and `std::mutex`, are not available on MCUs.
2. Time libraries such as `std::chrono` are also not available on MCUs.
3. Do not use function-local static variables. The atomic initialization guaranteed since C++11 is **highly likely to be unreliable** on MCUs.
4. Do not use global variables (objects) that rely on heap allocation, because the global construction phase on MCUs may be uncontrolled, and heap memory may not be available.

Among these, points 3 and 4 are very common scenarios and require special attention.

## C++ Knowledge to Master

The following content is sufficient to support most of the documentation in this directory.

### Classes and Object-Oriented Programming

You should at least be able to read and write code like this:

```cpp
class MyWidget : public Widget {
public:
    explicit MyWidget(Widget *parent = nullptr)
        : Widget(parent) {}

    void setValue(int value);
    int value() const;
};
```

You need to understand:

- The difference between classes and structs (not much difference, mainly default access permissions)
- The meaning of public inheritance (generally only public inheritance is used)
- Constructors and initialization lists
- Member functions, **`const` member functions**
- When you are overriding a base class interface versus just declaring a regular member function

This knowledge will appear directly in the [Object System](./object-system.md), [Widget Development Guide](./widget.md), and [Widget Registration and Export](./widget-export.md).

### Pointers, References, and `const`

If you are familiar with C, this part is the easiest to "assume you already know," but C++ usage is stricter than C.

Key points that must be truly mastered:

- The difference between `T *` and `T &`
- When to pass by pointer vs. when to pass by reference
- The meanings of **`const T *`**, `T *const`, and **`const T &`**
- Why `const` member functions are very common
- Why objects should not be arbitrarily processed byte by byte like in C

In Glyphix, this knowledge is directly related to interface design and lifecycle safety.

### Lifecycles and Resource Management

This is the most important section when migrating from C to C++.

You need to build the following habits:

- Objects are automatically destructed when they go out of scope.
- Constructors are responsible for establishing a valid state.
- Destructors are responsible for releasing resources.
- Do not put "resource cleanup" at the end of a function for manual handling.
- Do not treat complex objects as ordinary memory blocks to `memset` / `memcpy`.


A large number of Glyphix facilities and features are built on top of C++'s object lifecycle model, which includes topics such as RAII.

### Basics of Templates

You don't need to understand this deeply, but you must at least be able to read:

- `Signal<int>`
- `Pointer<Label>`
- `SharedRef<MyData>`
- `async::ResultSession<Client>`
- `std::vector<T>`

And know that "templates are code generation mechanisms with type parameters," rather than some advanced trick that only library authors touch.

In Glyphix documentation, templates mainly appear in two forms:

- **Generic containers/utility types**, such as `Signal<T>`, `Pointer<T>`
- **Specialization points**, such as supplying `js_cast<T>` for custom types

Developers should at least understand basic terminology such as "template parameters," "instantiation," and "specialization," and be able to read template type declarations and usages. However, defining your own template classes or functions is not required.

### Lambda Expressions

In modern C++, lambdas are a very practical way to write one-off functions. You should at least be able to read:

```cpp
mod["double"] = [](JsCtx ctx) -> JsValue {
    return ctx.arg(0).asInt(0) * 2;
};
```

And:

```cpp
int factor = readScaleFactorFromConfig();
mod["scale"] = [factor](JsCtx ctx) -> JsValue {
    return ctx.arg(0).asInt(0) * factor;
};
```

You should first become familiar with the basic syntax and capture mechanisms of lambdas, and focus on understanding:

- A lambda is an anonymous function object.
- A captureless lambda can often be used as a regular function pointer.
- A lambda with captures carries state.
- Once a lambda is held asynchronously, the lifecycle of the captured objects becomes critically important.

This directly affects code safety in [Native Module Development](./native-module.md) and [Async Development Examples](./async-examples.md).

::: tip Lambdas are very common
Lambdas effectively occupy the entire ecosystem of callback functions, meaning they are everywhere. To some extent, lambdas may be the most important C++ grammar point.

**Captureless** lambda expressions are almost equivalent to C function pointers, except for the syntax and the ability to alleviate "naming fatigue."
:::

### Minimum Working Set of the Standard Library

You don't need to systematically study the entire STL, but it is recommended to familiarize yourself with these most common parts:

- `std::vector`
- `std::array`
- `std::move`
- Basic algorithms `<algorithm>`, iterators, and range-based `for` loops

::: tip Associative Containers
Glyphix implements its own `HashMap` and `HashSet`, which are very similar to `std::unordered_map`. However, using associative containers like `std::map` and `std::unordered_map` is not recommended because their performance is poor, and `std::map` suffers from significant code bloat.
:::

### C and C++ Interoperability

If you are interfacing with underlying SDKs, you will almost certainly use this part.

You should at least know:

- The purpose of `extern "C"`
- C callback function pointers
- `void *` context parameters, and the implicit conversion limitations of `void *` in C++
- The division of labor between C structs and C++ wrapper layers

You will see a very typical pattern in the [Async Development Examples](./async-examples.md): the C API handles the actual asynchronous execution, while the C++ layer only handles parameter wrapping, lifecycle management, and result passing.

::: tip Difficulty Expectation
This part is not difficult, but it is very prone to link errors. You may need to learn how to resolve issues caused by `extern "C"` and others when mixing C and C++ headers.
:::

## Recommended Learning Order

It is recommended to fill in the gaps in the following order rather than reading a thick textbook from page one.

### First, Establish a "From C to C++" Migration Perspective

[ISO C++ FAQ](https://isocpp.org/faq)
- Prioritize reading entries related to "Learning C++ if you already know C" and "How to mix C and C++".
- This content is well-suited for experienced C developers because it assumes you already understand memory, interfaces, building, and underlying constraints.

### Quickly Build an Impression of Modern C++

[A Tour of C++](https://www.stroustrup.com/Tour.html)
- If you are willing to accept a short book, this is the most worthwhile one to invest time in.
- It is not a "zero-based programming tutorial," but a modern C++ overview for experienced developers.
- The goal is not to memorize everything, but to know what the main components of C++ are and what problems each solves.

### Syntax and Standard Library Reference Manual

[cppreference](https://en.cppreference.com/w/cpp)
- Suitable for looking things up as you go, not for reading sequentially from cover to cover.
- When you encounter syntax or library names like `override`, lambdas, initialization lists, template specialization, or `std::vector` while reading the Glyphix documentation, you can look them up here directly.
- If you need to review certain details of the C language, you can also look them up here.

### Switch Coding Habits to Modern C++

[C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- This is not a tutorial, but an engineering practice guide (there is also a published book version).
- Reading it cover-to-cover sequentially is not recommended; prioritize these sections:
  - `P`: Philosophy
  - `I`: Interfaces
  - `F`: Functions
  - `C`: Classes and class hierarchies
  - `R`: Resource management
  - `ES`: Expressions and statements
  - `CPL`: Interfacing with C
  - `SF`: Source files
  - `SL`: The Standard Library
  - `CP`: Concurrency (read as needed)

[Embedded Artistry's C++ Articles](https://embeddedartistry.com/blog/tag/cpp/)
- Better suited for topical reading rather than a systematic course.
- More noteworthy topics include: how to use C++ without the heap, strongly-typed register encapsulation, and what happens before `main()`.

## Recommended Way to Utilize These Resources

A more efficient approach is not to "learn C++ for a while before looking at Glyphix," but to do it in parallel:

1. Read this article first to know which knowledge needs to be supplemented.
2. Read [A Tour of C++](https://www.stroustrup.com/Tour.html) or the sections in the FAQ related to C migration.
3. Start reading the [Object System](./object-system.md) and [Native Module Development](./native-module.md).
4. When you encounter syntax you don't understand, use [cppreference](https://en.cppreference.com/w/cpp) for precise queries.
5. When you encounter questions like "Why does modern C++ tend to be written this way?", refer to the corresponding chapters in the [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).

This learning rhythm is closer to real work and better suited for developers with existing embedded experience.

## Mapping This Article to the cxxdev Documentation

If you are ready to continue reading, you can map the important knowledge points as follows:

- [Object System](./object-system.md): Classes, inheritance, lifecycles, references, template basics
- [SDK Project Configuration](./sdk-setup.md): Header files, source files, build systems, basic class declaration knowledge
- [Native Module Development](./native-module.md): Function interfaces, lambdas, object lifecycles, C/C++ interoperability
- [Async Feature Development](./async.md): Templates, threading models, object ownership, callback constraints
- [Widget Development Guide](./widget.md): Inheritance, member functions, event handling, object trees, and the rendering pipeline

============================================================
FILE_PATH: src/transl/EN/cxxdev/README.md

# C++ Native Development

Glyphix is an application framework designed for embedded devices, providing a JavaScript-first application development experience with a Vue Options API-like style. However, the core runtime of the framework is implemented in C++, allowing hardware vendors to extend and customize framework features using C++ — which is where "C++ Native Development" comes into play.

This document is intended for C++ developers with embedded development experience, aiming to help you understand Glyphix's C++ extension mechanism and enable you to implement the following two types of features:

- **Native Module**: Encapsulates C++ features into APIs that can be called by JavaScript, such as file access, hardware sensor reading, Bluetooth communication, and other system capabilities.
- **Native Widget**: Implements custom UI controls using C++ and registers them as framework [components](/framework/component/native-component.md) so that applications can directly use them in the user interface, just like using built-in `div`, `image`, and `button` components.

::: tip
In application development, we use "component" to refer to UI elements, while at the C++ layer, we use "widget" to refer to UI elements. This document distinguishes between these two terms: **Widget** is a concept at the C++ layer, and **component** is a concept in the reactive framework.
:::

## Framework Runtime Model

The Glyphix runtime consists of multiple layers. The diagram below illustrates the complete layered architecture:

<ArchDiagram max-width="560px">
  <div>
    Application Sandbox (Applet × N)
    <div class="remark">Independent JavaScript Realm · Lifecycle Isolation</div>
  </div>
  <div>
    Reactive Framework (C++)
    <div class="group row">
      <div>AppletKit<div class="remark">App Routing · Background Management</div></div>
      <div>Component System<div class="remark">Template · Reactive Render</div></div>
      <div>JsVM Bridge Layer<div class="remark">JerryScript / QuickJS</div></div>
    </div>
    <div class="group row">
      <div>Applet<div class="remark">C++ ↔ JavaScript Sandbox</div></div>
      <div>Async Session<div class="remark">ResultSession · Signals</div></div>
      <div>Native Module<div class="remark">System API Extension</div></div>
    </div>
  </div>
  <div>
    C++ Core Framework
    <div class="group row">
      <div>Widget System<div class="remark">Object · Widget</div></div>
      <div>Layout Engine<div class="remark">Flex · Flow · Stack</div></div>
      <div>Style Engine<div class="remark">CSS · Transition</div></div>
    </div>
    <div class="group row">
      <div>Event System<div class="remark">Touch · Key · Wheel</div></div>
      <div>Painter<div class="remark">2D Drawing</div></div>
      <div>Animation Engine<div class="remark">Property · Ease</div></div>
      <div>Signal / Slot</div>
    </div>
  </div>
  <div>
    Platform Abstraction Layer
    <div class="group row">
      <div>Graphics Backend<div class="remark">Framebuffer · GPU</div></div>
      <div>Input Driver<div class="remark">Touch · Key · Wheel</div></div>
      <div>File System<span class="remark">File · Dir</span></div>
      <div>IO / Time<span class="remark">Logger · Time</span></div>
    </div>
  </div>
  <div>
    Hardware / OS
    <div class="remark">RTOS · Linux · WASM</div>
  </div>
</ArchDiagram>

The bottom layer is the **Platform Abstraction Layer**, which is responsible for platform-related abstractions such as graphics rendering, input events, and the file system. This layer is typically implemented by the device vendor or provided as a reference implementation for the corresponding platform by Glyphix.

Above it is the **C++ Core Framework**, which includes a complete widget system (`Widget`), event dispatching, animation engine, layout system, and style engine. All UI elements are ultimately organized and rendered in the form of a C++ widget tree.

The next layer up is the **Reactive Framework**, which is responsible for bridging C++ core capabilities to JavaScript applications. It embeds a JavaScript engine (JerryScript or QuickJS) and implements bidirectional interaction between C++ and JavaScript through the `JsVM` and `JsValue` classes. AppletKit manages the complete lifecycle of applications (Applets), the component system implements reactive data binding and template rendering, and the asynchronous session framework maps C++ asynchronous operations to JavaScript Promises. The reactive framework itself is also implemented in C++.

The topmost layer is the **Application Sandbox**. Each running application (Applet) has an independent JavaScript execution environment (Realm) that is completely isolated from others. When an application exits, all resources within its sandbox are automatically reclaimed.

### System Collaboration Principles

The architecture diagram presents the module divisions but intentionally hides the collaboration and coupling relationships between modules. In fact, the entire framework operates through a set of shared underlying mechanisms. Understanding these mechanisms will help you know "what you are doing and why you are doing it" in practice.

The entire framework is penetrated by an **Object System**, which endows classes with runtime perception capabilities, including property reflection and event notification capabilities of C++ classes, as well as necessary lifecycle safety. Widgets, Native Modules, application frameworks, and asynchronous sessions all rely on this same foundation, as detailed in [Object System](./object-system.md).

**Widgets** form the UI skeleton through an object tree combined with drawing and event dispatching; the JavaScript application layer uses a **componentized** declarative programming model, and the two are naturally connected through reflection capabilities such as object properties. Complex functions such as **asynchronous sessions** also rely on the object system's lifecycle model to ensure correctness.

Through the **Meta-Object Compiler** and other abstraction mechanisms, Glyphix does not require developers to manually write binding code to expose C++ developed widget classes for JavaScript use. At the same time, functional completeness is retained on the C++ side; theoretically, you can directly develop a complete application using C++ (although this is not recommended).

### Programming Model

The Glyphix project does not restrict specific programming paradigms. For example, the object system is a classic object-oriented model, but the reactive framework provides application developers with a declarative, component-based development experience.

We do not encourage developers to practice "everything is an object," deliberately force design patterns, or pursue unnecessary abstractions. Our design principles lean more toward **pragmatism**, prioritizing the **resource constraints** and development efficiency of embedded systems.

## Documentation Conventions

### What is this document?

This is the guide document for Glyphix C++ native development, **not** an API reference document. It introduces the framework's design philosophy, core mechanisms, and development workflow to help you understand how to extend framework features, and demonstrates specific implementation details through sample code.

During actual development, be sure to refer to the API documentation, which is distributed alongside the SDK. Please contact your vendor to get access.

### Sample Code Description

All C++ code in the Glyphix framework is under the `gx` namespace. The documentation assumes `using namespace gx;` by default, so class names and function names do not have the `gx::` prefix. For example:

```cpp
#include "gx_widget.h"

using namespace gx; // Assumed to be imported by default in the documentation

class MyWidget : public Widget {
    // ...
};
```

Here, `Widget` is actually `gx::Widget`, but for simplicity, we omit the namespace prefix.

::: tip C++ Learning Resources
If you primarily use C and are familiar with MCUs, RTOS, drivers, or LVGL, but have not systematically studied C++, it is recommended to read [C++ Learning Guide](./cpp-guide.md) first. It covers only the subset of C++ truly needed to enter Glyphix native development and organizes external resources suitable for embedded developers.
:::

## Development Path

Regardless of your goal, it is recommended to first thoroughly read the basic usage of `GX_OBJECT`, `GX_PROPERTY`, and `Signal` in [Object System](./object-system) — they are used in all development scenarios.

Depending on your goal, choose the appropriate document to continue reading:

- [SDK Project Configuration](./sdk-setup): How to configure the build environment for an SDK project, including `glyphix_add_meta_objects()` registration, host build, and cross-compilation.
- [Native Module Development](./native-module): How to provide new system APIs for applications, such as fetching sensor data and calling underlying SDK functions.
- [Asynchronous Feature Development](./async): How to extend asynchronous features for applications, such as network requests, file IO, time-consuming calculations, etc.
- [Widget Development Guide](./widget.md): How to implement new UI controls (such as custom charts, special animation lists, etc.).
- [Widget Registration and Export](./widget-export.md): Registering custom controls as framework components for direct application use.

============================================================
FILE_PATH: src/transl/EN/cxxdev/native-module.md

# Developing Native Modules

A Native Module serves as the bridge between C++ and application-layer JavaScript code. Whenever you need to expose system capabilities to your application—such as reading sensor data, calling third-party SDKs, or accessing system features—you need to write a Native Module.

The Glyphix framework has already implemented numerous built-in modules using this mechanism, such as the File System (`@system.file`) and Router (`@system.router`). You can use the same approach to add custom capabilities to your own device.

The diagram below illustrates the position of a Native Module within the framework: it sits at the reactive framework layer, bridging upwards to JavaScript applications via the JsVM bridge layer to provide system APIs, and calling downwards into the C++ core framework or platform capabilities:

<ArchDiagram max-width="480px">
  <div>
    Application Sandbox (Applet × N)
    <div class="remark">Independent JavaScript Realm · Lifecycle Isolation</div>
  </div>
  <div>
    Reactive Framework (C++)
    <div class="group row">
      <div>JsVM Bridge Layer<div class="remark">JsValue · JsCallContext</div></div>
      <div class="subject">Native Module<div class="remark">System API Extensions</div></div>
      <div>Applet<div class="remark">Sandbox · Lifecycle</div></div>
    </div>
  </div>
  <div>
    C++ Core Framework / Platform Adaptation Layer
    <div class="remark">Drivers · SDKs · Hardware Abstraction</div>
  </div>
</ArchDiagram>

Writing a Native Module involves three sets of concepts: the **JsVM Bridge Layer** provides type conversion and function invocation capabilities between C++ and JavaScript; **Module Registration Macros** assemble C++ code into modules that can be `import`ed by JavaScript; and the **Applet Sandbox** provides application-level context and resource lifecycle management for the module. This chapter unfolds in this exact order.

::: warning Security Risks
When you plan to develop "system-level extensions" for Glyphix, do not overlook the fact that this also implies high security risks. The slightest oversight may introduce vulnerabilities, allowing malicious applications to exploit these capabilities to attack the system or other applications. Please strictly follow secure coding guidelines, limit the module's permissions and access scope, and conduct thorough security testing.
:::

## JsVM Bridge Layer

Before writing specific modules, you need to understand the interaction tools between C++ and JavaScript. The JsVM Bridge Layer is the infrastructure of the entire Native Module, providing the `JsValue` type system and the `JsCallContext` invocation context, enabling C++ code to create, read, and manipulate JavaScript values.

### `JsValue` Type System

`JsValue` is the C++ type representing JavaScript values within the framework, covering all fundamental JavaScript types. It manages its lifecycle using reference counting and can be directly assigned and copied like C++ value types such as `int` or `String`.

Creating JavaScript values from C++:

```cpp
JsValue undefined;               // undefined
JsValue boolVal{true};           // boolean
JsValue intVal{42};              // number (integer)
JsValue floatVal{3.14};          // number (float)
JsValue strVal{"hello"};         // string
```

These constructor functions are all implicit, so module functions can directly `return "hello"` or `return 42` without manual packaging.

When reading C++ values from a `JsValue`, use the `as*` series of methods. They return specified default values when types do not match, avoiding manual type checking:

```cpp
int    count  = value.asInt(0);       // Returns 0 if not a number
double ratio  = value.asNumber(1.0);  // Returns 1.0 if not a number
String label  = value.asString();     // Returns an empty string if not a string
```

If you need to perform type coercion according to JavaScript semantics (e.g., converting an arbitrary value to a boolean), use the `to*` series of methods:

```cpp
bool   enable = value.toBoolean();    // Any value can be converted to a bool
int    num    = value.toInt();        // Converted to an integer according to the ECMAScript specification
String str    = value.toString();     // Converted to a string according to the ECMAScript specification
```

When you need to determine the specific type of a value, use the `is*` series of methods:

```cpp
value.isUndefined()   // Whether it is undefined
value.isNumber()      // Whether it is a number
value.isString()      // Whether it is a string
value.isObject()      // Whether it is an object
value.isArray()       // Whether it is an array
value.isFunction()    // Whether it is a function
```

### `JsCallContext` Context

Every C++ function called by JavaScript has a fixed signature:

```cpp
JsValue myFunction(JsCtx ctx);
```

`JsCtx` is an alias for `const JsCallContext &`. `JsCallContext` provides three core capabilities:

- **`ctx.argc()`**: Gets the number of arguments passed by JavaScript;
- **`ctx.arg(index)`**: Gets the `index`-th argument (returns `const JsValue &`);
- **`ctx.vm()`**: Gets the current JavaScript engine instance (`JsVM &`).

A typical parameter reading pattern:

```cpp
static JsValue setVolume(JsCtx ctx) {
    // Always check the argument count first, then validate the type, otherwise ctx.arg(0) might go out of bounds
    if (ctx.argc() < 1 || !ctx.arg(0).isNumber())
        return JsValue();  // Invalid argument, return undefined

    int level = ctx.arg(0).asInt(0);
    level = std::max(0, std::min(100, level));
    audioSetVolume(level);
    return JsValue(true);  // Return success flag
}
```

Many built-in module functions accept an object parameter. This is a flexible convention that allows parameters to have default values and facilitates future extensions:

```js
// Called from the JavaScript side
setConfig({ brightness: 80, contrast: 50 })
```

Read object properties on the C++ side using `operator[]`:

```cpp
static JsValue setConfig(JsCtx ctx) {
    if (ctx.argc() < 1) return {}; // Remember to check the argument count

    JsValue params = ctx.arg(0);
    int brightness = params["brightness"].asInt(100);
    int contrast   = params["contrast"].asInt(50);
    // ...
    return {}; // Returns undefined
}
```

### Exporting Functions as `JsValue`

Module functions do not have to be named static functions. A `JsValue` can be constructed from any callable object: **captureless lambdas** are automatically resolved into function pointers with efficiency equivalent to named functions; **lambdas with captures** are wrapped into callable objects, making them suitable for closing over module-level runtime state within factory functions:

```cpp
static JsValue createMathModule(JsVM &vm) {
    JsValue mod = vm.newObject();

    // Captureless lambda: Automatically decays to a function pointer with no extra overhead
    mod["double"] = +[](JsCtx ctx) -> JsValue {
        return ctx.arg(0).asInt(0) * 2;
    };

    // Lambda with captures: Reads configuration once when the module is created and uses it directly in subsequent calls
    int factor = readScaleFactorFromConfig();
    mod["scale"] = [factor](JsCtx ctx) -> JsValue {
        return ctx.arg(0).asInt(0) * factor;
    };

    return mod;
}
```

The advantage of using lambdas is that related logic can be written close together within factory functions, preventing a large number of short named functions from being scattered across files. For functions with simple logic that do not need to be reused on the C++ side, lambdas are highly recommended.

### Creating and Returning Objects

In many scenarios, you need to return a result object containing multiple fields. Use `JsVM::newObject()` to create a new JavaScript object, and then set properties via `operator[]`:

```cpp
static JsValue getSystemInfo(JsCtx ctx) {
    JsValue result = ctx.vm().newObject();
    result["model"] = "GX-Watch-2";
    result["firmware"] = "2.1.0";
    result["memory"] = 512; // KB
    return result;
}
```

`JsVM` also provides other factory methods, such as `newArray()`, `newArrayBuffer()`, `newPromise()`, etc., to create various JavaScript types as needed.

### Exceptions and Error Handling

If a module function encounters an error, it can throw a JavaScript exception via `JsVM::newError()`:

```cpp
static JsValue setConfig(JsCtx ctx) {
    if (ctx.argc() < 1)
        return ctx.vm().newError("missing parameters");
    // ...
}
```

However, we generally avoid using exceptions in simple scenarios like parameter checking, because exception message text consumes code size. For non-critical errors, returning `undefined` or `false` is usually more appropriate.

### Function Interoperability

If you need to proactively execute JavaScript functions or object methods within C++, you can use `JsValue::call()` or `callMethod()`. This is as simple as calling JavaScript functions directly in C++, where arguments can be passed via initializer lists and return values can be retrieved:

```cpp
static JsValue printDemo(JsCtx ctx) {
    JsVM &vm = ctx.vm();
    JsValue obj = vm.newObject();
    obj["value"] = 42;
    
    // Calls a method of the console object, equivalent to console.log("Object is:", obj) in JS
    auto result = vm.globalObject()["console"]
                    .callMethod("log", {"Object is:", obj});
    
    // print() can be used to directly output the contents of a JsValue to the console for debugging
    result.print(); // undefined 
    
    // If you only care about the execution process without needing a return value, and wish to print a warning if an error occurs:
    result.reportError(); // Returns a bool indicating whether an exception occurred
    
    return {}; // Returns undefined
}
```

If you are calling an independent function object passed as an argument (rather than a method attached to an object), you need to use `call()` and specify the `this` binding object, which can usually be the global object `globalObject()`:

```cpp
static JsValue doMathAndCallback(JsCtx ctx) {
    if (ctx.argc() < 1 || !ctx.arg(0).isFunction()) return JsValue();
    
    auto &callback = ctx.arg(0); // References can be used here to avoid reference counting overhead
    // This is the this object during JS function calling; if {} it is equivalent to undefined
    JsValue thisObj = ctx.vm().globalObject();
    // Equivalent to callback.call(globalThis, 10, 20) in JS
    JsValue result = callback.call(thisObj, { 10, 20 });
    
    return result;
}
```

::: warning Dangerous Anti-Pattern: Asynchronous Callback Leaks
If your initial intention is to persistently store a `callback` passed from JavaScript—such as passing it to underlying hardware to subscribe to events—please be extremely careful:

```cpp
// ❌ Incorrect pattern: Will cause a memory leak!
static JsValue onButtonPress(JsCtx ctx) {
    auto callback = ctx.arg(0);
    // Directly obtaining the JavaScript callback from arguments and capturing it in a lambda, passed to the underlying driver
    HardwareButton::onPress([callback]() mutable {
        callback.call({}, {...});
    });
    return {};
}
```

This is a classic **severe trap**: `JsValue` relies on reference-counting lifecycle management. Once this closure is persistently held by the underlying driver alongside global state without providing an explicit cancellation mechanism (such as a corresponding `offPress` method to unbind), this JavaScript callback and its entire bound application sandbox context will be **permanently leaked**!

To implement long-lived callbacks across event loops (such as event subscriptions), you must combine them with the lifecycle mechanism of the **Application Sandbox** to manage C++ objects, safely unbinding them when no longer needed, or directly use the dedicated `AsyncSession` facilities (please refer to [Asynchronous Feature Development](./async.md)).
:::

For more complex asynchronous scenarios (such as returning a Promise or requiring multiple callbacks), please refer to [Asynchronous Feature Development](./async).

::: tip Complete API Reference
This section covers only the most frequently used capabilities of the JsVM bridge layer. `JsVM` and `JsValue` also provide many interfaces not covered in this section, such as JSON parsing and serialization (`parseJSON()`, `stringifyJSON()`), property enumeration (`properties()`), Promise operations (`newPromise()`, `promiseResolve()`/`promiseReject()`), and direct execution of JS code (`eval()`, `importModule()`), etc. For complete interface descriptions, please refer to the API documentation distributed with the SDK.
:::

### Exporting C++ Objects

Previous examples focused on "functions returning basic types or ordinary JavaScript objects," which fundamentally operate on JavaScript via C++ APIs. However, sometimes you need to **export a C++ object to JavaScript** so that scripts can continuously operate on the same underlying instance.

There are several different implementation approaches:

- **`vm.newMetaObject(object)`**: The most direct method, automatically exposing `GX_PROPERTY` / `GX_METHOD` to JavaScript;
- **`vm.newObject(object)` + manually attaching functions**: Closer to an "ordinary JS object with a native handle";
- **`vm.newProxy()`**: The most flexible, but property interception logic is scattered and maintenance cost is the highest.

In most business scenarios, using `newMetaObject()` is recommended first. Only consider other methods when you explicitly need to manually write a JavaScript shape or intercept highly dynamic property accesses.

#### Exporting via `newMetaObject()`

This is the simplest approach. First, define a native object type, and then directly wrap it into a reflectable JavaScript object.

The following example exports a readable and writable counter object. It must inherit from `PrimitiveObject` and be declared to the meta-object system using `GX_OBJECT`:

```cpp
#include "gx_jsvm.h"
#include "gx_object.h"

using namespace gx;

class NativeCounter final : public PrimitiveObject {
    GX_OBJECT

public:
    explicit NativeCounter(int initial = 0) : m_value(initial) {}

    int value() const { return m_value; }
    void setValue(int value) { m_value = value; }

    GX_METHOD void reset() { m_value = 0; }

    // Needs to be exposed to JavaScript as a "constructor".
    static JsValue constructor(JsCtx ctx) {
        int initial = ctx.argc() ? ctx.arg(0).asInt(0) : 0;
        auto *counter = new NativeCounter(initial);
        return ctx.vm().newMetaObject(counter);
    }

    GX_PROPERTY(int value, get value, set setValue)

private:
    int m_value = 0;
};
```

::: tip GX_METHOD Types
Functions marked with `GX_METHOD` can accept and return any managed `Variant` types that can interoperate with `JsValue`, including references, such as `int`, `const String &`, etc.

Remember that `JsValue` itself can also be used.
:::

Then export this "constructor" in the module factory function:

```cpp
static JsValue createCounterModule(JsVM &vm) {
    JsValue mod = vm.newObject();
    mod["createCounter"] = NativeCounter::constructor;
    return mod;
}
```

Usage on the JavaScript side:

```js
import counter from '@vendor.counter'

const c = counter.createCounter(10)
console.log(c.value) // 10
c.value = 42
c.reset()
console.log(c.value) // 0
```

Here, `c` looks like an ordinary JavaScript object, but underneath it is actually associated with a `NativeCounter` instance. Because `newMetaObject()` is used, JavaScript can directly read and write properties declared with `GX_PROPERTY` and call methods exposed by `GX_METHOD`.

If you only need to "naturally expose a C++ object as a JavaScript object" (including properties and methods), this is usually sufficient.

#### Handling Applet Contexts

`newMetaObject()` has a common limitation: `GX_METHOD`s exported through the meta-object system are ordinary C++ member functions, meaning they do not receive `JsCtx` / `JsCallContext` and therefore cannot directly write `Applet::current(ctx.vm())` like module functions can.

If your object methods need to access the current application context, for example:

- Resolving application-private URIs;
- Reading application permissions or configurations;
- Binding other resources to the current sandbox from within object methods;

The more appropriate approach is to have the object inherit from `BindableObject`, binding it to the current `Applet` when the object is created. This allows subsequent `GX_METHOD` implementations to access the host application directly via `applet()`.

Example:

```cpp
#include "gx_applet.h"
#include "gx_bindableobject.h"
#include "gx_jsvm.h"

using namespace gx;

class NativeFile final : public BindableObject {
    GX_OBJECT_KINDS(NoneKind)

public:
    NativeFile(Applet *applet, const String &uri)
        : BindableObject(applet), m_uri(uri) {}

    GX_METHOD String resolvedUri() const {
        auto *host = applet();
        return host ? host->resolveUri(m_uri) : String();
    }

    static JsValue constructor(JsCtx ctx) {
        auto *applet = Applet::current(ctx.vm());
        if (!applet) return {};

        String uri = ctx.argc() ? ctx.arg(0).toString() : String();
        return ctx.vm().newMetaObject(new NativeFile(applet, uri));
    }

private:
    String m_uri;
};
```

::: warning Sandbox Security
Do not actually implement features like `resolvedUri()` that directly expose underlying resource paths; this is merely an example. In actual development, ensure proper permission checks and access controls are in place to avoid leaking sensitive information to the JavaScript side.
:::

Usage on the JavaScript side is identical to ordinary `newMetaObject()` objects:

```js
const file = native.createFile('internal://files/config.json')
console.log(file.resolvedUri())
```

In this example, `resolvedUri()` does not take a `JsCtx` argument, yet it can still access `applet()` because the object was bound to the current application upon creation.

::: warning Two Prerequisites for `BindableObject`
Pay extra attention to two points when using `BindableObject`:

- `BindableObject` defaults to `ExplicitDeleteKind`. This means it **will not** be automatically destroyed when the JavaScript object is garbage collected. If you want it to behave like an ordinary Native Object under GC, you can override this default value using `GX_OBJECT_KINDS(NoneKind)` as shown in the example above.
- `BindableObject` must be bound to an `Applet`; otherwise, `applet()` will always be a null pointer, making context access impossible. The simplest practice is to call `BindableObject(applet)` in the constructor or bind to the current `Applet` immediately after creation.
:::

::: important Legacy Behavior
Prior to the v0.8.0 official release, the behavior of `PrimitiveObject::objectKinds()` differed from this documentation. Do not reference implementation details of older versions.
:::

`BindableObject` is not a replacement for [Exporting via `newMetaObject()`](#exporting-via-newmetaobject), but a specialized solution for "when object methods need to remember their owning application context." Introduce this concept only when you genuinely need to access `Applet` inside a `GX_METHOD`.

#### Using `newObject()` and Manually Exporting Methods

Sometimes you do not want to expose the entire meta-object interface, but simply want to attach a C++ object as an opaque handle to a JavaScript object, manually deciding which methods can be called. In this case, you can use `vm.newObject()` to export the object.

With this approach, `GX_PROPERTY` and `GX_METHOD` are **not** automatically exposed, so you must manually attach methods to the object:

```cpp
class CounterCore final : public PrimitiveObject {
    GX_OBJECT

public:
    explicit CounterCore(int initial = 0) : m_value(initial) {}

    int value() const { return m_value; }
    void add(int delta) { m_value += delta; }

private:
    int m_value = 0;
};

static JsValue createManualCounter(JsCtx ctx) {
    int initial = ctx.argc() > 0 ? ctx.arg(0).asInt(0) : 0;

    JsVM &vm = ctx.vm();
    JsValue obj = vm.newObject(new CounterCore(initial));

    obj["add"] = [](JsCtx ctx) -> JsValue {
        auto *counter = dyn_cast<CounterCore *>(ctx.thisObject().object());
        if (!counter)
            return {};
        counter->add(ctx.arg(0).asInt(0));
        return {};
    };

    obj["get"] = [](JsCtx ctx) -> JsValue {
        auto *counter = dyn_cast<CounterCore *>(ctx.thisObject().object());
        if (!counter)
            return {};
        return counter->value();
    };

    return obj;
}
```

The JavaScript side sees an ordinary object:

```js
const c = counter.createManualCounter(10)
c.add(5)
console.log(c.get()) // 15
```

The characteristic of this writing style is that you completely decide the shape of the JavaScript API, but inside each method, you must manually retrieve the underlying C++ pointer from the `this` object and verify its type using `dyn_cast`. Compared to `newMetaObject()`, this involves more boilerplate code and is more prone to missing checks.

However, it also has a direct advantage: these manually attached functions are essentially ordinary `JsCtx` callbacks, meaning they can directly access the current application context via `Applet::current(ctx.vm())` just like module functions. This is an important distinction between them and `GX_METHOD`.

This method also cannot export property accessors (getters/setters), only fixed property values.

#### Exporting Objects Using `newProxy()`

If you need to take over property reading and writing, method lookup, lazy field generation, and other behaviors entirely, you can also use `vm.newProxy()`. This approach enables highly dynamic interfaces, such as forwarding arbitrary property accesses to an underlying dictionary, generating sub-objects on demand, or intercepting writes for validation.

However, it comes with clear costs:

- The behaviors of reading properties, writing properties, and method calls are scattered across proxy logic;
- The API shape is no longer directly expressed by class definitions as it is with `newMetaObject()`;
- Once the behavior becomes complex, troubleshooting issues becomes cumbersome.

Therefore, `newProxy()` is more suitable for a small number of highly dynamic bridging scenarios rather than replacing conventional object exports.

#### Lifecycle Rules

The destruction rules for Native Objects are not determined solely by `newMetaObject()`, but by the `objectKinds()` of the C++ object:

- If the object contains `RootKind` and **does not** have `ExplicitDeleteKind`, then when the corresponding JavaScript object is garbage collected, the C++ object will also be automatically destroyed;
- If the object is a child node of another object or declares `ExplicitDeleteKind`, its lifecycle remains managed by the C++ side.

For most "standalone wrapper objects," directly inheriting from `PrimitiveObject` without additionally declaring `ExplicitDeleteKind` will yield the appropriate default behavior—automatic destruction alongside GC.

If you are not familiar with these object lifecycle flags, it is recommended to read the chapter on `PrimitiveObject` in [Object System](./object-system.md) before deciding whether to hand the object over to JavaScript GC management.

#### Retrieving Native Objects from `JsValue`

Sometimes another Native Module function will receive this object as a parameter. In this case, you can temporarily retrieve the underlying C++ pointer from the `JsValue`:

```cpp
static JsValue getCounterValue(JsCtx ctx) {
    if (ctx.argc() < 1 || !ctx.arg(0).isObject())
        return {};

    auto *counter = dyn_cast<NativeCounter *>(ctx.arg(0).object());
    if (!counter)
        return {};
    return counter->value();
}
```

`object()` provides **temporary access only** and does not transfer ownership. If you actually need to "take" the object away from the JavaScript side, you should use the templated form `moveObject<T>()`:

```cpp
auto *counter = value.moveObject<NativeCounter>();
```

**Do not** write it like this:

```cpp
auto *counter = dyn_cast<NativeCounter *>(value.moveObject());
```

If the type does not match, this code will lose object ownership after a failed cast, causing a leak. The API documentation also explicitly recommends prioritizing `moveObject<T>()` to combine "type checking" and "ownership transfer" into a single step.

::: warning When NOT to Export Native Objects
If you only need to return a simple result dataset, such as device information, a one-time calculation result, or a configuration snapshot, prioritize returning ordinary JavaScript objects constructed via `newObject()`. Only when JavaScript needs to continuously operate on the same C++ instance over time is it worth introducing Native Objects.
:::

## Module Definition and Registration

Having mastered the basic tools of the JsVM bridge layer, you can assemble C++ functions into a complete Native Module. A module consists of two parts: a **factory function** responsible for creating the module object and attaching C++ functions to it; and a **registration macro** responsible for registering the factory function into the framework's module system.

::: tip
If you are developing non-standard system extensions, it is recommended to prioritize the [Library Loader](#library-loader) mechanism.
:::

### Module Structure

Taking the implementation of a device information module `@vendor.device` as an example:

```cpp
#include "gx_jsvm.h"

using namespace gx;

// C++ functions in the module
static JsValue getDeviceName(JsCtx ctx) {
    return "MyDevice-Pro";
}

static JsValue getBatteryLevel(JsCtx ctx) {
    int level = /* Read battery level from driver */ 85;
    return level;
}

// Factory function: Build and return the module object
static JsValue createDeviceModule(JsVM &vm) {
    JsValue mod = vm.newObject();
    mod["getDeviceName"] = getDeviceName;
    mod["getBatteryLevel"] = getBatteryLevel;
    return mod;
}

// Register the module so it is accessible in JavaScript via the @vendor.device path
GX_JSVM_MODULE(vendor_device, "vendor.device", createDeviceModule)
```

The `GX_JSVM_MODULE` macro accepts three parameters: the C++ variable name, the JavaScript module path (without the `@` prefix), and the factory function. The factory function is called when the module is first `import`ed, and the returned `JsValue` object is what the JavaScript side receives.

On the JavaScript side, applications use this module as follows:

```js
import device from '@vendor.device'

const name = device.getDeviceName()
const battery = device.getBatteryLevel()
```

::: tip This is a Demo!
This looks simple enough, except for one major issue: most APIs are asynchronous! We should practically never read battery levels in the JavaScript execution context (i.e., the UI thread) unless we are genuinely building a demo. For asynchronous APIs, please refer to the [Asynchronous Feature Development](./async.md) chapter, which provides more appropriate patterns and examples.
:::

### Enabling Modules

Declaring a module alone is not enough; you also need to "install" it into the JavaScript engine during framework initialization. This is accomplished using the `GX_JSVM_MODULE_IMPORT` macro:

```cpp
GX_JSVM_MODULE_IMPORT(vendor_device)
```

`GX_JSVM_MODULE` declares a global variable at file scope, and `GX_JSVM_MODULE_IMPORT` finds and calls the `install()` method of this variable. The name parameters (the first parameter) of both macros must match.

A common practice is to centralize all `GX_JSVM_MODULE_IMPORT` calls in a single function for easy management:

```cpp
void installVendorModules() {
    GX_JSVM_MODULE_IMPORT(vendor_device)
    GX_JSVM_MODULE_IMPORT(vendor_sensor)
    GX_JSVM_MODULE_IMPORT(vendor_bluetooth)
}
```

Call `installVendorModules()` after `AppletKit` initialization to ensure modules are available when the application starts.

## Library Loader

Native Modules are suitable for implementing framework-level system APIs universally available to all applications. However, for **non-standard system customization features**, such as vendor-exclusive data accesses, private SDK encapsulations, or capabilities exposed only to specific authorized applications, the **Library Loader** mechanism is strongly recommended.

The Library Loader loads modules by name via the [`loadLibrary()`](/api/system-app.md#loadlibrary) method provided by the `@system.app` module:

```js
import app from '@system.app'

const lib = app.loadLibrary('custom-library')
lib.someFunction()
```

Compared to Native Modules, the Library Loader has two distinct advantages:

- **No global registration required**: Does not depend on the `GX_JSVM_MODULE` macro and `GX_JSVM_MODULE_IMPORT`; module objects are created on demand when called;
- **Easy simulator fallback**: The application side can gracefully fall back to script-implemented stubs in general simulator environments by checking whether the return value of `loadLibrary()` is `undefined`, whereas stub tricks for module imports like `import lib from '...'` are rather hacky and anti-pattern.

```js
import app from '@system.app'

// Attempt to load the native library, falling back to a script stub in simulators
const nativeLib = app.loadLibrary('custom-library')
const lib = nativeLib || {
    someFunction() { /* Simulator implementation */ }
}
```

Apart from the registration method and usage on the JavaScript side, the Library Loader is largely identical to Native Modules in all other respects.

### Registering a Library Loader

On the C++ side, register a loader function via `AppletKit::setLibraryLoader()`. The loader receives the calling `Applet` instance and returns a library object (a `JsValue`):

```cpp
#include "gx_appletkit.h"
#include "gx_jsvm.h"

using namespace gx;

static JsValue getDeviceName(JsCtx ctx) {
    return "MyDevice-Pro";
}

void installLibraries() {
    AppletKit::instance()->setLibraryLoader(
        "custom-library",
        [](Applet *applet) -> JsValue {
            JsVM &vm = JsVM::current();
            JsValue lib = vm.newObject();
            lib["someFunction"] = getDeviceName;
            return lib;
        }
    );
}
```

`setLibraryLoader()` can be called after `AppletKit` initialization without needing to re-register every time an application starts.

Since the Library Loader's loader receives an `Applet *`, it can directly perform **application permission verification** at the entry point, denying features to unauthorized applications without repeatedly checking inside each module function:

```cpp
AppletKit::instance()->setLibraryLoader(
    "custom-library",
    [](Applet *applet) -> JsValue {
        // Permission check: Intercept unauthorized access uniformly at the entry point
        if (!applet || !applet->permission(vendor::Permission::AccessCustomLib))
            return vm.newError("permissions denied"); // Returns undefined

        JsVM &vm = JsVM::current();
        JsValue lib = vm.newObject();
        lib["someFunction"] = getDeviceName;
        return lib;
    }
);
```

If the loader returns `undefined` (i.e., a default-constructed `JsValue()`), `app.loadLibrary()` also evaluates to `undefined` on the JavaScript side, allowing applications to perform fallback processing accordingly.

::: tip
It is recommended that the loader function return `undefined` rather than throwing an exception when permission checks fail. In addition to enabling simple downgrades on the JavaScript side, this prevents leaking information about the library's existence (if you prefer unauthorized applications not to know the library exists).
:::

## Collaborating with Application Sandboxes

The module functions introduced in previous sections are stateless—taking arguments, returning results, and holding no context. However, many practical scenarios require modules to interact with the currently running application: reading application resource paths, language settings, or hosting a long-lived C++ object within the application sandbox. This requires capabilities provided by `Applet`.

### Obtaining the Current Application Context

Use `Applet::current()` to get the application instance belonging to the caller:

```cpp
#include "gx_applet.h"

static JsValue readPreference(JsCtx ctx) {
    auto applet = Applet::current(ctx.vm());
    // Since subsequent operations depend on applet, make sure to check if the context was successfully acquired
    if (!applet) return JsValue();

    // Read the application's private storage path
    String storagePath = applet->resolveUri("internal://files/preferences.json");
    // ...
}
```

`Applet` instances are automatically managed by the framework, with each application running in its own independent JavaScript Realm. `Applet::current()` infers the corresponding application instance from the current Realm, ensuring that when the same module function is called across different applications, each obtains its own isolated context.

### Resource Lifecycle Management

If a module function needs to allocate a long-lived C++ object (such as a background task continuously listening to hardware status), **never** use global variables or raw pointers to hold resources across calls—this allows resources to escape sandbox tracking, resulting in resources failing to release after the application exits and stripping away the crucial security guarantees provided by the sandbox.

A strict security requirement exists here: **Native Modules must guarantee that all access paths to C++ objects undergo strict ownership and type validation**, rather than merely providing a "legal path" with the possibility of bypassing it. The correct way to achieve this is to delegate object lifecycle management entirely to the `Applet` sandbox and **mandatorily** use `takeObject<T>()` for validation in **every** module function that accepts integer handles—an indispensable invariant expanded upon below.

Taking the function of continuously listening to sensor states as an example, we demonstrate this secure lifecycle-binding mechanism.

::: tip
The code in this section is actually a rudimentary conceptual substitute for the `AsyncSession` mechanism in the [Asynchronous Feature Development](./async.md) chapter, used solely for conceptual demonstration. In actual business development, it is strongly recommended to directly use mature `AsyncSession` related facilities to handle asynchronous tasks, as they are built upon the methods introduced in this section under the hood.
:::

Suppose we have a sensor. The application needs to start listening during initialization, read the latest data multiple times subsequently, and manually stop listening when no longer needed. First, we define the carrier for this background task:

```cpp
class SensorListener : public PrimitiveObject {
    GX_OBJECT
public:
    SensorListener() {
        // Start sensor, request underlying driver hardware resources...
    }
    ~SensorListener() override {
        // Stop sensor, release related hardware resources...
    }
    int latestValue() const { return m_value; }

private:
    int m_value = 0;
};
```

#### Binding Objects to the Sandbox

Use `Applet::bindObject()` to bind the instance to the current application sandbox, returning an integer handle for the JavaScript side to hold:

```cpp
static JsValue startSensor(JsCtx ctx) {
    auto applet = Applet::current(ctx.vm());
    if (!applet) return {};

    auto *listener = new SensorListener();
    // Hand over the object management to Applet and obtain an integer handle (ID)
    int bindId = applet->bindObject(listener);

    // Return the ID to JavaScript as a unique credential for subsequent operations on this object
    return bindId;
}
```

Because the object is now **managed** by the sandbox, even if the application exits midway or is forcefully terminated by the system, the sandbox will automatically clean up all bound objects upon destruction, preventing resource leaks.

#### Securely Retrieving Objects

When the JavaScript side needs to operate on a previously created object, it **must** retrieve the instance via `Applet::takeObject<T>()` using the handle, rather than performing any form of "raw casting":

```cpp
static JsValue readSensor(JsCtx ctx) {
    auto applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1) return {};

    int bindId = ctx.arg(0).asInt();
    auto *listener = applet->takeObject<SensorListener>(bindId);
    if (!listener) return {}; // Returns nullptr if ID is invalid or type mismatches

    return listener->latestValue();
}
```

`applet->takeObject<T>()` only accesses IDs belonging to the **current sandbox** (preventing cross-application unauthorized access) and then validates **type matching** via object meta-information. A non-null pointer is returned only if both layers pass.

::: danger Must Access Objects via `takeObject<T>()`
Integer IDs originating from JavaScript are completely untrustworthy on the C++ side—they could be forged or represent expired references. Omitting validation leads to severe security vulnerabilities:

```cpp
// ❌ Absolutely do not do this!
static JsValue readSensor(JsCtx ctx) {
    auto bindId = ctx.arg(0).asInt();
    // Using only the non-template version of takeObject + static_cast bypasses type checks and sandbox boundary checks
    auto *binded = applet->takeObject(bindId);
    // Danger: static_cast has no runtime checks; binded here might not be a SensorListener at all!
    auto *listener = static_cast<SensorListener *>(binded);
    return listener->latestValue(); // Can lead to arbitrary memory read/write
}
```
:::

#### Unbinding and Destruction

When you need to actively terminate tasks from the C++ side and completely release resources, first retrieve and validate the type using `takeObject<T>()`, unbind management via `unbindObject()`, and finally destroy manually:

```cpp
static JsValue stopSensor(JsCtx ctx) {
    Applet *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1) return {};

    int bindId = ctx.arg(0).asInt();
    auto *listener = applet->takeObject<SensorListener>(bindId);
    if (listener) {
        applet->unbindObject(listener); // Unbind from the automatic management list
        delete listener;                // Destroy manually
    }
    return {};
}
```

Complete usage workflow on the JavaScript frontend side:

```javascript
import sensor from '@vendor.sensor'

// Start and cache the credential
const id = sensor.startSensor()
// ...Read multiple times
const value = sensor.readSensor(id)
// Task finished, release resources
sensor.stopSensor(id)
```

Thanks to the safety net provided by `bindObject`, even if the application forgets to call `stopSensor()`, the sandbox will automatically release all bound objects when it exits.


::: important Mandatory Automatic Unbinding
Because JavaScript code cannot be trusted, one cannot assume it will call resource-releasing functions. For malicious applications, sandbox leaks caused by JavaScript reference leaks are viable attack vectors. Therefore, **all objects bound to the sandbox must automatically unbind when the sandbox is destroyed**, ensuring that regardless of how JavaScript operates, resource leaks will not occur.

Any design that requires the JavaScript side to unbind is dangerous and must be avoided.
:::

### Security Safeguards

Despite the many security requirements emphasized earlier, they may still be insufficient to eliminate all risks. To further reinforce your security defenses, we recommend directly restricting extension module access to trusted applications. You can check the permission flags or identity information of the `Applet` directly in the module factory function, rejecting non-compliant access:

```cpp
static JsValue createDeviceModule(JsVM &vm) {
    auto applet = Applet::current(vm);
    if (!applet || !applet->permission(
                    vendor::Permission::AccessDeviceInfo)) {
        // Return an empty object or throw an exception if permissions are lacking
        return vm.newError("permissions denied");
    }

    // Only create module objects and expose functionality after authorization
    JsValue mod = vm.newObject();
    mod["getDeviceName"] = getDeviceName;
    // ...
    return mod;
}
```

This strategy effectively blocks unauthorized access at the entry point. Even if the module function itself is not sufficiently robust, attackers cannot exploit it to obtain sensitive information or execute malicious operations.

Library Loader entry permission checks have already been introduced in related documentation.

============================================================
FILE_PATH: src/transl/EN/cxxdev/platform-font-fallback.md

# Platform Font Fallback

The Glyphix framework has a built-in font loading and fallback mechanism based on `font-face` / `font-family`. However, target platforms usually come with comprehensive font pipelines (such as Windows DirectWrite and macOS CoreText) that have already implemented system font fallback and related optimizations.

To make full use of the platform font pipeline, Glyphix allows you to take over font fallback: when the fonts within the framework cannot cover a certain character, the task is handed over to the platform to find and render a suitable system font. This article is intended for Glyphix system developers and will guide you step-by-step through the integration process.

Involved public header files:
- `gx_unite.h`: Contains UniTE public interfaces and the engine installation function `installEngine()`;
- `gx_shapingadapter.h`: This is the primary interface;
- `gx_fontdriver.h`: Provides the `FontDriver` encapsulation mechanism;
- `gx_fontloader.h`: Provides the font loader interface.

## General Concept

For a piece of text to be displayed on the screen, it goes through the following pipeline: Application text is handed over to the **paragraph layout engine** for line breaking and positioning; text with the same script and direction in each paragraph is **shaped** into glyphs; missing characters are filled in by **font fallback**; glyphs are then rendered into bitmaps by the **font driver**; and all fonts originate from the registration, loading, and reuse of the **font management** layer.

<ArchDiagram max-width="560px">
  <div>Application Text<div class="remark">Paragraph · String · Style</div></div>
  <div>
    Paragraph Layout Engine
    <div class="group row">
      <div>Lightweight Engine LiTE<div class="remark">Simple typesetting (Default engine)</div></div>
      <div>UniTE Engine<div class="remark">BiDi · Shape · Complex script</div></div>
    </div>
  </div>
  <div>
    Shaping · Font Fallback
    <div class="group row">
      <div>HarfBuzz<div class="remark">GSUB / GPOS</div></div>
      <div>Simple Shape<div class="remark">Character → Glyph</div></div>
      <div class="subject">FontFallbackShaper<div class="remark">family fallback · platform system font</div></div>
    </div>
  </div>
  <div>
    Font Rendering
    <div class="group row">
      <div>FontDriver<div class="remark">TTF / FreeType</div></div>
      <div>FontDriverFamily<div class="remark">Multi-face cascading</div></div>
      <div class="subject">PlatformFont Wrapper<div class="remark">Render platform fallback glyphs</div></div>
    </div>
    <div>GlyphCache - Glyph bitmap cache</div>
  </div>
  <div>
    Font Manager FontManager
    <div class="group row">
      <div>Registration / Lookup<div class="remark">face · family · properties</div></div>
      <div class="subject">FontLoader<div class="remark">Load face, inject wrapper</div></div>
    </div>
  </div>
</ArchDiagram>

The three highlighted parts in the diagram are covered in this article:
1. Fallback strategy `FontFallbackShaper`, used to find missing characters and perform fallback shaping;
2. `PlatformFont` wrapper responsible for rendering platform fallback fonts, used in conjunction with `FontFallbackShaper`;
3. `FontLoader` used to load the platform fallback font wrapper, which will be registered into the `FontManager`.

The remaining layers of the framework are already implemented. Text shaping (`ShapingAdapter`) generally does not need to be implemented from scratch; you can directly reuse the reference implementation.

### Prerequisites

Before implementing the platform font fallback feature according to this document, you need to:

- Enable the UniTE text engine (compared to the default lightweight engine, it supports complex script shaping and multi-level fallback).
- The target platform must support a complete font pipeline capable of providing advanced features such as system font shaping and script mapping. This is typically a complex subsystem that most MCU RTOS platforms lack.

::: important
Compared to the default LiTE engine, enabling UniTE and the complete font pipeline requires more memory and firmware space. Additionally, the performance of this engine is lower than that of the lightweight LiTE, so you need to evaluate whether it is necessary to enable it for full Unicode support and internationalization requirements.
:::

## Reusing the Shaping Backend

`ShapingAdapter` is responsible for shaping characters into glyphs. The built-in `HarfBuzzShaper` (`gx_harfbuzz_shaper.cpp`) implements full OpenType shaping by calling HarfBuzz, and then writes glyph indexes, advances, and offsets into the output based on target pixel sizes.

`HarfBuzzShaper` relies on FreeType to read font files, so both HarfBuzz and FreeType libraries must be included simultaneously. If these libraries already exist on the target platform, ensure version consistency; otherwise, linking or runtime errors may occur.

::: tip
Similar to HarfBuzz's [responsibilities](https://harfbuzz.github.io/what-harfbuzz-doesnt-do.html), `ShapingAdapter` does not handle text runs containing different fonts, which also includes the "font fallback" mechanism discussed below. Therefore, as long as the font used in shaping lacks a character, the `ShapingAdapter` implementation will return the `.notdef` glyph (index `0`), leaving it to be handled by the fallback strategy.
:::

## Implementing the Fallback Strategy

`FontFallbackShaper` is the core of the fallback mechanism. The engine calls it once for every shaped piece of text, requiring a glyph sequence **free of missing characters** as the shaping result. Unlike `ShapingAdapter`, it is not just for shaping a single font-face, but is designed for two-level fallback.

### Two-Level Fallback Cascading

`FontFallbackShaper::shape()` performs fallback in two levels from near to far:

- **Level 1**: Fill in missing characters within the current family using other fonts. This is already implemented by the framework; you only need to call `builtinShape()`.
- **Level 2**: Missing characters that cannot be resolved by Level 1 are handed over to the platform system fonts. This level is implemented by you.

Missing characters are represented in the data by a glyph index of `0`, i.e., `.notdef`. The return value of `shape()`, `FallbackResult`, uses bit flags to express the outcome: `result & NotNeeded` being true indicates that there are no more missing characters and processing can end directly; otherwise, common returns are `FullyResolved` (all processed) or `PartiallyResolved` (some `.notdef` characters remain).

### Skeleton of the `shape()` Function

First, call Level 1; return if there are no missing characters, otherwise proceed to Level 2 platform font fallback. `m_shaper` is the `ShapingAdapter` held by this fallback shaper (usually `HarfBuzzShaper`).

```cpp
FallbackResult shape(GlyphRunBundle &storage,
                     TextSpan text,
                     FontDriver *font) override {
    // Level 1: Use builtin API to handle fallback within the family
    auto r = builtinShape(storage, text, font, &m_shaper);
    if (r & NotNeeded)
        return r;                                  // No missing characters, finish
    return resolveByPlatform(storage, text, font); // Level 2, see below
}
```

`builtinShape()` is the only place that depends on `ShapingAdapter`. In this case, you typically implement `PlatformFallbackShaper` as follows:
```cpp
class PlatformFallbackShaper : public FontFallbackShaper {
    HarfBuzzShaper m_shaper; // Directly define as a member variable, no pointer reference needed

public:
    PlatformFallbackShaper() = default;
    FallbackResult shape(GlyphRunBundle &storage,
                         TextSpan text, FontDriver *font) override;
};
```
Note that `m_shaper` is merely a private member variable of your platform fallback strategy and does not need to be exposed to the outside. Inside `shape()`, simply pass `&m_shaper` when calling `builtinShape()`.

::: tip
In extreme cases (such as the initial adaptation phase), you can ignore fallback within the family, skip `builtinShape()`, and only handle Level 2 platform fallback. In this case, the `m_shaper` member variable can be omitted.

Regardless, specific `ShapingAdapter` classes generally cannot be defined as local variables because they may hold HarfBuzz cache states; recreating them on every shaping operation would cause severe performance degradation.
:::

### Obtaining Platform Fonts

Level 2 hands over missing characters to the platform and ultimately lets the wrapper render them. `fallbackFont(font)` returns the wrapper registered at the end of the family (see below). Its static type is `FontDriver *`, and you need to cast it back to your own wrapper type in order to call your custom registration and query interfaces.

```cpp
// Casting can also be done using dyn_cast, but if there is only one wrapper type, static_cast is also safe
auto *wrapper = static_cast<PlatformFont *>(fallbackFont(font));
if (wrapper == nullptr)
    return PartiallyResolved; // No wrapper at the end of the family, cannot continue
```

::: warning Must Be Implemented in Pairs
The fallback strategy and the wrapper are a matched pair: the `static_cast` above requires that `fallbackFont()` returns precisely your own wrapper type. Make sure that the installed fallback shaper matches the registered wrapper.
:::

### Simple Fallback Shaping

The most common and starter-friendly scenario is: an entire run can be shaped using a single platform font (i.e., a certain system font file completely covers the script). In this case, select the platform font according to `storage.run().spec.script`, reshape the entire run, write the entire run with the same `faceId`, and **directly overwrite the Level 1 result** without merging with already resolved glyphs.

UniTE splits runs by script, and Latin and CJK within the same text are naturally different runs. When the primary font focuses on Latin and encounters scripts like CJK, Arabic, or Devanagari, the run after `builtinShape()` is often entirely `.notdef`; reshaping and overwriting the entire run does not lose any already resolved glyphs. Therefore, the vast majority of multilingual typesetting follows this path and it is not a degenerate special case.

```cpp
// Select platform font according to script (platform font handle, not FontDriver), register to get faceId
auto sysFont = platformFontForScript(storage.run().spec.script);
uint32_t faceId = wrapper->registerFont(sysFont);
// Your shaping step yields glyphCount glyphs (demonstrated here with HarfBuzz output)
auto &run = storage.resize(glyphCount);
for (int i = 0; i < glyphCount; ++i) {
    run.data.glyphIds[i]   = GlyphIds::encodeFallback(gid[i], faceId);
    run.data.xAdvances[i]  = uint16_t(scale(pos[i].x_advance));
    run.data.xOffsets[i]   = int16_t(scale(pos[i].x_offset));
    run.data.yOffsets[i]   = int16_t(scale(pos[i].y_offset));
    run.data.clusterMap[i] = static_cast<int>(info[i].cluster);
}
```

The `pos`, `info`, `gid`, and `scale` fields come from your shaping steps, demonstrated above using HarfBuzz output.

::: tip Platform Shaping Capabilities
Platforms usually come with built-in shaping capabilities (such as DirectWrite, CoreText); whether to reuse HarfBuzz depends on the specific platform. The HarfBuzz output in the demonstration can be replaced with platform shaping output. For RTL runs (`spec.bidiLevel & 1`), the direction must be passed to the shaper.
:::

The prerequisite for this method is that the entire run maps to a single platform font. It is **not applicable to Common scripts** (Emojis, symbols, etc.): different characters within the same run may belong to multiple platform fonts, requiring the complex fallback described below.

### Complex Fallback Shaping

When multiple platform fonts are needed within a run, or only some clusters need fallback, the simple approach is no longer applicable. Considering that specific fallback and merging algorithms depend on platform APIs, this document only specifies the semantics that the merged `GlyphRun` must satisfy, and the implementation must handle them accordingly:

- Glyphs already resolved in Level 1 are **retained as-is**, and Level 2 only replaces clusters that are still `.notdef`.
- Fill every glyph slot with `glyphIds`, `xAdvances`, `xOffsets`, `yOffsets`, and `clusterMap`; fallback glyphs are marked using `encodeFallback(gid, faceId)`.
- `clusterMap[i]` is the offset of the source code point corresponding to this glyph relative to **this run** (consistent with `spec.text`, range `[0, text.length())`), used for drawing remapping and line clipping.
- Glyph count is variable: use `storage.resize()/reset()` to adjust storage, and then write slot by slot. `GlyphRunBundle` will automatically update `run().glyphCount`.
- When a single source cluster maps to multiple glyphs, the order and the sum of advances must be correct; code points swallowed by GSUB clustering should yield zero-advance glyphs to avoid gaps or misalignments.
- `faceId` must be a wrapper-registered ID that is stable throughout its lifecycle; the glyph order and shaping direction of RTL runs must be consistent.
- Return value: return `FullyResolved` if all are filled, or `PartiallyResolved` if residuals remain.

As long as the output satisfies the above constraints, the framework can render correctly. Whether to query platform APIs section by section or reuse HarfBuzz to shape font-by-font can be chosen based on the platform.

### Line Height and Caching

Line height depends on **which font actually draws** each glyph. `builtinLineMetrics()` handles parts of the glyphs within the family; glyphs with fallback marks (`isFallback()`) query the wrapper for their system fonts' ascents and descents to be incorporated. Fallback glyphs are encoded in `GlyphIds` by `encodeFallback`, and their `fontIndex()` is the written `faceId`, based on which the corresponding platform font is retrieved from the wrapper.

```cpp
VerticalMetrics resolveLineMetrics(const GlyphIds *gids, int count,
                                   FontDriver *font) const override {
    // Handle glyphs within the family
    VerticalMetrics m = builtinLineMetrics(gids, count, font);
    // Handle platform fallback glyphs
    auto *wrapper = static_cast<PlatformFont *>(fallbackFont(font));
    if (wrapper == nullptr)
        return m;
    // For glyphs where gids[i].isFallback(), query asc/descent from the wrapper and incorporate into m
    for (auto gid : utils::span<const GlyphIds>(gids, count)) {
        if (!gid.isFallback())
            continue; // Process fallback glyphs only
        uint32_t faceId = gid.fontIndex(); // fontIndex() of fallback glyph is faceId
        auto face = wrapper->fontForFaceId(faceId); // Platform font handle (not FontDriver)
        if (face == nullptr)
            continue;
        m.ascent = max(face->ascender(), m.ascent);
        m.descent = min(face->descender(), m.descent);
    }
    return m;
}
```

You can also aggregate the fallback fonts of the entire line and query their asc/descent in one go to avoid querying glyph-by-glyph inside a loop.

`flush()` is used to release system fonts cached by the wrapper:

```cpp
void flush(FontDriver *font) override {
    if (auto *w = static_cast<PlatformFont *>(fallbackFont(font)))
        w->releaseFonts();
}
```

::: tip
`flush()` is called by the framework when a paragraph is destroyed or memory is low; please clean up platform resources held by the wrapper inside it.
:::

## Fallback Font `FontDriver` Wrapper

The wrapper is responsible for rendering the glyphs shaped in the previous step into bitmaps. It inherits from `FontDriver` and carries the `PlatformFallback` flag during construction, allowing the framework to recognize it as a fallback font.

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

This font wrapper is not used to load some font file (like `FontDriverTTF` does). Its role is to hand over fallback glyphs to the platform font pipeline for processing, while its internal implementation is opaque to Glyphix.

### Dual-Mode Query

The `code` received by the wrapper has two meanings, distinguished by the `CodeAsGlyphId` bit:

- **With mark**: Queried by glyph index, with the high bits carrying `faceId` and the low bits being the glyph index. Once decoded, it is routed to the corresponding platform font, and then `glyphId` is used to query the corresponding `GlyphBitmap`.
- **Without mark**: Unicode character query, fallback lookup by codepoint among registered platform fonts, converting internally to a glyph index before querying.

A common implementation of `bitmapOf()` is as follows:

```cpp
bool bitmapOf(uint32_t code, GlyphBitmap *bitmap) override {
    if (code & CodeAsGlyphId) { // By glyph index
        uint32_t faceId  = (code >> 16) & 0x3ff;
        uint32_t glyphId =  code & 0xffff;
        auto face = fontForFaceId(faceId); // Platform font handle (not FontDriver)
        return face && face->bitmapOf(glyphId, bitmap);
    }
    // Unicode character lookup; iterate registered fonts here, or use a more efficient mapping table
    for (auto *face : registeredFonts()) {
        uint32_t glyphId = face->glyphIndexOf(code);
        if (face->bitmapOf(glyphId, bitmap))
            return true;
    }
    return false;
}
```

::: tip
`fontForFaceId()` returns a platform font handle, **not a `FontDriver`**; `face->bitmapOf(...)` and `face->glyphIndexOf(...)` above are pseudo-code for operations on that handle, representing "getting `GlyphBitmap` by `glyphId`" and "getting `glyphId` by codepoint" respectively.
:::

`metricsOf()` uses the same dual-mode logic; `advancesOf()`, `baseline()`, etc., are also calculated from platform fonts. `duplicate()` only needs to copy a mapping table.

### `faceId` Mapping

The wrapper maintains a mapping from `faceId` to platform fonts for use by the fallback strategy during registration and lookup during rendering.

`faceId` is a $10$-bit integer ($[0, 1023]$), and its meaning is entirely defined by the implementation. The only requirement is that it is **stable throughout its lifecycle**. There are two common approaches:

- **Fixed by script**: Directly use the `Script` enum value as `faceId`. The wrapper holds corresponding platform fonts by script, and registers them by script upon startup without runtime allocation.
- **Allocated on demand**: Allocate the next index whenever a new platform font is encountered, maintaining a growing table.

Example of fixing by script (`faceId` is the script value):
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
You need to handle script-to-font mapping, `faceId` allocation, and platform font object caching yourself.

::: tip
`faceId` is the contract between the fallback strategy and the wrapper: `PlatformFallbackShaper` uses it to encode glyphs, and `PlatformFont` uses it to decode back to system fonts. Both ends must interpret `faceId` consistently, and it must be representable by a $10\rm bit$ integer.
:::

## Registering the Wrapper

Finally, let the framework incorporate the wrapper into family loading. Implement `FontLoader::load()`, return a wrapper for a certain generic family name, and install it into the `FontManager`:

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

When an application requests a font in the form of `"<primary-face>,sans-serif"`, the framework merges the parts into the same family in comma-separated order, with the wrapper acting as the fallback face at the end, allowing `fallbackFont()` to retrieve it.

`PlatformFont` and `PlatformFontLoader` are usually only registered as fonts for generic family names like `sans-serif`, rather than specific system font names. This allows applications to use the same family name across different platforms without needing to know the specific fonts of the platform.

::: warning Functional Limitation
The wrapper relies on the application writing family names in the order described above, positioned as the last item in the family. Mechanisms to automatically guarantee this order are still under development.
:::

## Installation and Assembly

`installEngine()` in `gx_unite.h` connects your fallback strategy to the engine:

```cpp
unite::installEngine(*CoreApp()->typesetCore(),
                     std::make_unique<PlatformFallbackShaper>());
```

Complete assembly sequence:

1. `fontManager()->install(new PlatformFontLoader)`: Register the wrapper loader.
2. `installEngine(...)`: Install the fallback strategy holding the shaping backend.
3. Request fonts in the form of `"<primary-face>,sans-serif"`, layout, and draw as usual.

## Notes

- Advances / offsets are uniformly Q26.6 fixed-point (value = pixels × 64).
- Unresolved `.notdef` characters (glyph index $0$) are skipped during rendering, displaying blank spaces or tofu blocks at their corresponding positions.
- `faceId` is only $10$ bits, limiting the maximum number of simultaneously active system fonts in a single family to $1024$.
- The fallback strategy and the wrapper must be implemented in pairs and maintain type consistency (relying on `static_cast`).
- Be sure to release platform font caches held by the wrapper inside `flush()`.

