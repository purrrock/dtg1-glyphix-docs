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