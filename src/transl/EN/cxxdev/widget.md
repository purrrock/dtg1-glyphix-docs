---
headerDepth: 2
---
# Widget Development Guide

In Glyphix, all visible UI elements are `Widget` instances. The framework includes built-in common controls such as buttons, labels, images, and scroll areas, but device manufacturers often need to develop customized widgets tailored to their product features. For example, a smartwatch might customize special list animations due to a small circular screen, while dashboard equipment might require specialized chart widgets. This document describes how to implement a new widget using C++.

## Widget Basics

A `Widget` represents a rectangular area with basic properties such as position, size, visibility, and opacity. It can receive events and is responsible for rendering its own content. Widgets are organized in a tree structure: a parent widget contains multiple child widgets, and the coordinates of a child widget are relative to its parent widget.

Each widget has a **logical update cycle**: when a widget's state changes (for example, data is updated), calling `update()` marks it as "needs redraw". The framework then unifies the redrawing of all marked widgets on the next render frame rather than redrawing immediately—this prevents multiple redundant redraws within the same frame.

### Widgets vs. Component Systems

UI widgets are typically implemented as C++ classes inheriting from `Widget`, conforming to standard C++ object-oriented design. Glyphix's reactive framework and component system allow these C++ widgets to be directly exposed as native components and used in a templated, declarative manner.

This design allows C++-side widget development and front-end component usage to remain relatively independent while preserving the customary development practices of both sides. For example, in C++ you can build interfaces using an approach similar to LVGL or Qt Widgets, without needing to adopt the popular declarative style of front-end frameworks.

### Comparison with Other Frameworks

The design of the Glyphix widget system is similar to traditional C/C++ UI frameworks such as Qt Widgets or LVGL. Therefore, you will find that the methodology and knowledge system for developing a new widget are very similar to those frameworks:
- Create a new widget class by inheriting from `Widget`;
- Core mechanisms such as layout systems, event systems, and painting systems exist;
- Data binding and event notifications are achieved through property systems and signal mechanisms;
- They possess geometric concepts such as coordinate systems and dimensions, and support nested widget tree structures.

::: tip Developing UIs with C++ Widgets is Not Recommended
The original design intent of Glyphix is not to develop UIs directly on the C++ side; therefore, we do not provide related documentation and examples.
:::

## Creating Custom Widgets

This section uses a progress ring widget (`ProgressRing`) as an example to step through the elements required to develop a custom widget.

::: tip Comprehensive Widget Example
The [slider-demo](./widget-slider-demo.md) example included with the SDK is a complete implementation of all the knowledge points in this document, including inheriting existing widgets, painting, event handling, property declarations, `ValueAnimation` animations, and `StyleEngine` customization. It is recommended to review it after reading this document.
:::

### Defining the Widget Class

Create a new widget class inheriting from `Widget`, add the `GX_OBJECT` macro at the very beginning of the class definition, and **override the `event()`** virtual function as the entry point for event handling:

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

    // EventDispatch needs to access protected methods, declare friend
    friend struct EventTraits<ProgressRing>;

private:
    int m_value;  // [0, 100]
};
```

`GX_OBJECT` is essential; it triggers the meta-object compiler to generate metadata for the class, allowing the widget to be properly recognized by the framework's property system, animation system, and component system (see [Object System](./object-system.md) for details).

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
    // ... see painting section for details
}
```

Custom painting is accomplished by implementing `paintEvent()`. Constructing a `Painter` by passing the `this` pointer provides the drawing context associated with the current widget, after which various drawing methods can be called to perform rendering. For a complete description of the `Painter` API, refer to the [Painting](./painting.md) section.

### Handling Events

The Glyphix event system **does not rely on virtual function inheritance** to dispatch events. Methods like `paintEvent()` and `gestureEvent()` are not `virtual`, and you **must not** add `override` when declaring them (doing so will cause a compilation error). Instead, the framework routes calls to the correct handling functions at **compile time** based on event types via `EventDispatch`.

The only virtual function that needs to be (and must be) overridden is **`event()`**, within which you delegate to `EventDispatch`:

```cpp
bool ProgressRing::event(Event *event) {
    return EventDispatch<Widget>{}(this, event);
}
```

The first template parameter of `EventDispatch` is typically the **direct base class** (i.e., the class that `ProgressRing` inherits from, which here is `Widget`). It checks at compile time whether the current class directly declares the corresponding handling function. If so, it calls it; otherwise, it automatically falls back to the base class implementation. A return value of `bool` for a handling function indicates whether the event was consumed; a return value of `void` is treated as consumed.

::: tip Base Class Selection Tips
There are some optimization techniques for selecting the base class parameter of `EventDispatch`. Typically you can choose the direct base class, but you can also use higher-level ancestor classes, which results in subtle code size and performance differences. Generally, however, you do not need to overthink this or worry about misuse—as long as it compiles, event dispatch will work correctly.
:::

::: important
When references are made below to "overriding `xxxEvent()`", please note that this simply means **declaring** a non-virtual member function in the derived widget class that shares the same signature as the base class event handling function. This is **not** a virtual function, `override` cannot be added, and event dispatch does not rely on virtual function mechanisms.

The IDE may suggest changing these member functions to virtual; ignore this prompt.
:::

If you need to handle gesture inputs, declare `gestureEvent()` and implement it in the class:

```cpp
// Add declaration in the protected area of the header file:
bool gestureEvent(GestureEvent *event);

// Implement in the .cpp file:
bool ProgressRing::gestureEvent(GestureEvent *event) {
    if (event->type() == Event::Press) {
        // ...
        return true;   // Returning true indicates the event is consumed and will not propagate to the parent widget
    }
    return false;
}
```

Handled event types:

| Method Signature | Trigger Timing |
|---|---|
| `bool gestureEvent(GestureEvent *)` | Gesture events, including Press, Pan, Swipe, etc. |
| `bool wheelEvent(WheelEvent *)` | Wheel or dial input (such as a crown) |
| `bool keyEvent(KeyEvent *)` | Physical keys |
| `void resizeEvent(ResizeEvent *)` | Widget size change |
| `void moveEvent(MoveEvent *)` | Widget position change |
| `bool focusEvent(FocusEvent *)` | Focus change |
| `void paintEvent(PaintEvent *)` | Redraw request |
| `bool layoutEvent(LayoutEvent *)` | Layout request |
| `void tickEvent(TickEvent *)` | Per-frame tick (requires calling `requestNextTick()` to enable) |

If certain event handling functions are **mandatory** for the current widget, you can declare them in the template parameters of `EventDispatch`, causing a compilation error if omitted or if signatures do not match:

```cpp
bool MyButton::event(Event *event) {
    // Fails to compile if paintEvent or gestureEvent are not correctly declared
    return EventDispatch<Widget, PaintEvent, GestureEvent>{}(this, event);
}
```

::: tip Declaring Necessary Event Handling Functions
Although you can use `EventDispatch<Widget>` to automatically dispatch all events, it is **strongly recommended** to explicitly declare the event types that the current widget needs to handle. This catches omissions or typos at compile time as much as possible and reduces manual review burdens.
:::

### Properties and Signals

Use the `GX_PROPERTY` macro to expose properties to the framework so they can be bound by the application layer and targeted by property animations:

```cpp
// Declare the value property, with getter value(), setter setValue(),
// and signal field associated with change signals for reactive framework subscription
GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
```

Once declared, the `value` property can:
- Be directly bound by application-layer templates (e.g., `<progress-ring :value="progress"/>`)
- Be smoothly transitioned by the property animation system (when the property type supports interpolation)

Call `update()` in the setter to trigger a redraw, and emit signals at the appropriate time to notify external observers:

```cpp
void ProgressRing::setValue(int v) {
    if (m_value == v) return;
    m_value = v;
    update();          // Mark for redraw on the next frame
    valueChanged(v);   // Emit signal
}
```

`Signal<T>` is an ordinary templated member variable, emitted directly like a function call. Parameterless signals use `Signal<>` and take no arguments when invoked. For complete semantics regarding properties and signals, refer to the relevant section in [Object System](./object-system.md).

### Layout

After a widget is instantiated, its position and size can be manually specified via `setGeometry()`. If the parent widget uses automatic layout, override `sizeHint()` to declare the widget's desired size:

```cpp
Size ProgressRing::sizeHint() const {
    return Size(80, 80);
}
```

For container widgets that need to manage child widget layouts themselves, complete the child widget's geometry calculations in `layoutEvent()`, or mount layout classes provided by the framework (such as `FlexLayout`) via `setLayout()`. For details, see the [Layout and Dimensions](#layout-and-dimensions) section.

## Painting

### Painter Initialization

Construct a `Painter` inside the widget's `paintEvent()` member function to begin drawing:

```cpp
void ProgressRing::paintEvent(PaintEvent *event) {
    Painter p(this);
    // All subsequent drawing is accomplished via p
}
```

The drawing coordinate system uses the **top-left corner of the widget as the origin**, with $+x$ pointing right and $+y$ pointing down, in units of pixels. `rect()` returns the local rectangle of the current widget `(0, 0, width(), height())`, which is the most commonly used reference area during painting.

If the widget has framework-managed style properties such as background color set via application-layer styles or `StyleModifier`, you can call the base class to handle these backgrounds before drawing custom content:

```cpp
void ProgressRing::paintEvent(PaintEvent *event) {
    Widget::paintEvent(event);  // Draw framework-managed background first (if any)
    Painter p(this);
    // ...
}
```

When the base class is not called, framework-managed background styles are ignored, and the widget is entirely responsible for its own visual presentation via `paintEvent`.

### Painting States

`Painter` maintains a set of current painting states. Every drawing call uses the current state until it is modified again.

#### Brush

The brush determines the color used by **filling** methods (`fillRect`, `fillRoundedRect`, `fillPath`, etc.) as well as **text**:

```cpp
p.setBrush(Color(200, 200, 200));   // RGB gray
p.setBrush(Color{"#35a7ff"});       // Hexadecimal string
p.setBrush(Color::White);           // Predefined constant
p.setBrush(Color(0xff4486ff));      // ARGB hex integer (0xff is fully opaque)
```

#### Pen

The pen determines the color and line width used by **stroking** methods (`drawRect`, `drawArc`, `drawLine`, etc.):

```cpp
Pen pen(Color(64, 156, 255));
pen.setSize(6);    // Line width 6px
p.setPen(pen);
```

#### Other States

```cpp
p.setFont(Font(18));     // 18px font size, affects drawText()
p.setOpacity(127);      // Opacity [0, 255], affects all subsequent drawing
```

All states apply only to the current `Painter` instance. Painters constructed by different widgets are completely independent and do not interfere with each other.

### Basic Shapes

#### Rectangle

```cpp
p.setBrush(Color::White);
p.fillRect(rect());                    // Fill the entire widget area
p.fillRect(Rect(10, 10, 60, 20));      // Fill the specified rectangle

p.fillRoundedRect(rect(), 8.0f);       // Rounded rectangle fill, radius 8px
p.drawRoundedRect(rect(), 8.0f);       // Rounded rectangle stroke (no fill, uses Pen color)
```

When the corner radius equals half of the smaller of the width and height, the rectangle becomes a capsule shape, which is very common in buttons and progress bars:

```cpp
float radius = min(box.width(), box.height()) * 0.5f;
p.fillRoundedRect(box, radius);
```

#### Straight Line

```cpp
p.drawLine(Point(0, cy), Point(width(), cy));   // Horizontal separator line
```

#### Arc

`drawArc` specifies an arc by center coordinates and radius. The units for `startAngle`/`endAngle` are degrees, where $0°$ corresponds to the $3$ o'clock position and increases clockwise:

```cpp
float cx = width() / 2.0f;
float cy = height() / 2.0f;
float radius = min(cx, cy) - 4.0f;

// Draw complete arc (background ring), from -90° (12 o'clock) for a full circle
Pen bgPen(Color(200, 200, 200));
bgPen.setWidth(6);
p.setPen(bgPen);
p.drawArc({cx, cy}, radius, -90.0f, -90.0f + 360.0f);

// Draw progress arc (from 12 o'clock clockwise to the position corresponding to progress)
if (m_value > 0) {
    Pen fgPen(Color(64, 156, 255));
    fgPen.setWidth(6);
    p.setPen(fgPen);
    p.drawArc({cx, cy}, radius, -90.0f, -90.0f + 360.0f * m_value / 100.0f);
}
```

The visual thickness of the arc is determined by the line width of the current `Pen`.

### Vector Paths (`VectorPath`)

For complex shapes that cannot be described by rectangles and arcs, use `VectorPath` to construct arbitrary contours, and then render them via `fillPath()` or `drawPath()`.

```cpp
#include "gx_vectorpath.h"
```

`VectorPath` works like a "pen trajectory": contours are described sequentially using `moveTo` to place the pen, `lineTo` for straight segments, and `arcTo` for circular arc segments, and finally rendered uniformly by `Painter`.

#### Straight Segment Path

```cpp
VectorPath path;
path.moveTo(x0, y0);   // Place pen (no drawing)
path.lineTo(x1, y1);   // Line to (x1, y1)
path.lineTo(x2, y2);
path.lineTo(x0, y0);   // Return to start, forming a closed triangle

p.fillPath(path, Color(64, 156, 255)); // Fill closed region
```

`fillPath()` automatically treats the path as a closed region even if it does not explicitly return to the start at the end. `drawPath()` draws the path outline using the current `Pen` without filling.

#### Arc Segment Path

The parameters for `arcTo` are the center point, $x/y$ radii (which differ for ellipses), start angle, and sweep angle (in degrees, positive clockwise):

```cpp
// Draw horizontal capsule shape: left semicircle + right semicircle; arcTo automatically connects the two segments with a line
float r  = rect.height() * 0.5f;
float x1 = rect.left() + r;
float x2 = rect.right() - r;
float y  = rect.top() + r;

VectorPath path;
path.arcTo(PointF(x1, y), r, r, 90.0f, 270.0f);    // Left semicircle (counter-clockwise from 9 to 3 o'clock)
path.arcTo(PointF(x2, y), r, r, -90.0f, 90.0f);    // Right semicircle (counter-clockwise from 3 to 9 o'clock)
p.fillPath(path);
```

`arcTo` automatically inserts a straight line between the current end point of the path and the start point of the new arc, so the two arc segments connect naturally without requiring an explicit call to `lineTo`.

#### Curves

Quadratic or cubic Bezier curve segments can be constructed using `conicTo` or `cubicTo`, which, combined with `moveTo` and `lineTo`, can describe complex contours:

```cpp
VectorPath path;
path.moveTo(x0, y0);
// Quadratic Bezier curve, with (cx, cy) as control point
path.conicTo(cx, cy, x1, y1);
// Cubic Bezier curve, with (cx1, cy1) and (cx2, cy2) as control points
path.cubicTo(cx1, cy1, cx2, cy2, x2, y2);
// Fill path using specified brush
p.fillPath(path, brush);
```

#### Combined Path Example

Combining multiple instructions can build shapes of arbitrary complexity. Taking the wave-filled area in `WaveSlider` as an example, the path consists of a top wave polyline and a bottom rounded edge:

```cpp
VectorPath path;
path.moveTo(leftX, waveY(leftX));
for (int i = 1; i <= sampleCount; ++i) {
    float x = leftX + (rightX - leftX) * float(i) / sampleCount;
    path.lineTo(x, waveY(x));           // Top wave contour
}
path.lineTo(rightX, bottomEdge(rightX)); // Right descent
for (int i = sampleCount - 1; i >= 0; --i) {
    float x = leftX + (rightX - leftX) * float(i) / sampleCount;
    path.lineTo(x, bottomEdge(x));       // Bottom edge (returning along the rounded rectangle bottom)
}
path.lineTo(leftX, waveY(leftX));        // Return to start
p.fillPath(path);
```

### Text

`drawText()` lays out and renders text within a rectangular range. The text color is determined by the current `Brush`, and the font is set via `setFont()`:

```cpp
p.setFont(Font(18));
p.setBrush(Color(50, 50, 50));
p.drawText(rect(), format("{}%", m_value), AlignCenter);
```

::: tip Formatted Strings
`format()` is a formatting function provided by the framework with syntax similar to [`std::format`](https://en.cppreference.com/w/cpp/utility/format/format), usable cross-platform.
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
| `AlignCenter` | Horizontal + Vertical center (equivalent to `AlignHCenter | AlignVCenter`) |

The `font()` method returns the current font inherited by the widget from the style system. Using it during painting allows the widget to automatically follow application font size changes:

```cpp
p.setFont(font());   // Use the widget's inherited style font rather than a fixed size
```

`drawText()` also supports more complex text layouts, such as multi-line text and auto-wrapping. See the API documentation for details.

### Images

`drawImage()` draws an image into a specified rectangle:

```cpp
Image img{"file://path/to/icon.png"};
p.drawImage(widget->rect(), img); // Draw image to specified area without automatic scaling
```

In actual usage, images typically come from the resource system, and the loading method depends on the platform and packaging configuration.

### Complete Example

The following is the complete `paintEvent` for `ProgressRing`, combining the painting capabilities discussed above:

```cpp
void ProgressRing::paintEvent(PaintEvent *event) {
    // If the widget has a background style managed by the framework, call the base class first
    // Widget::paintEvent(event);

    Painter p(this);

    float cx = width() / 2.0f;
    float cy = height() / 2.0f;
    float radius = min(cx, cy) - 4.0f;
    float startAngle = -90.0f;   // Start from 12 o'clock position

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
    return Size(80, 80);  // Recommended display size 80×80px
}
```

If the widget's height varies with its width (such as an aspect-ratio-scaled image), override `heightForWidth()`:

```cpp
int AspectWidget::heightForWidth(int width) const {
    return width; // Square ratio
}
```

For cases where you need to manually manage child widget layouts, override `layoutEvent()` and set the geometry of child widgets within it:

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

You can also use ready-made layout classes provided by the framework (such as `FlexLayout` or `StackLayout`), mounted via `setLayout(new FlexLayout())`.

::: tip Using Ready-Made Layout Classes
Unless you are building a container widget with a special layout, it is recommended to use the layout classes provided by the framework to manage child widget layouts. In such cases, there is no need to override `layoutEvent()`.

Implementing a complete layout algorithm is relatively complex, requiring handling of interactions across aspects like `sizeHint()`, along with performance optimizations.
:::

## Animations

The framework provides three categories of animation mechanisms: **Style Animations**, **Property Animations**, and **`ValueAnimation`**. Style animations and property animations are primarily used on the **application layer** (i.e., the side consuming widgets), whereas when implementing custom widgets, `ValueAnimation` is most commonly used directly.

### ValueAnimation

`ValueAnimation<T>` is an animation class that interpolates any type `T`. Each frame, it calculates the interpolation result based on the current progress and emits it via the `value` signal. You simply need to connect the signal to your own update logic:

```cpp
#include "gx_valueanimation.h"

// Declare the animation object among the widget's members, typically using a pointer for dynamic creation/destruction when needed
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
    update();  // Trigger redraw
}
```

A `finished` signal is emitted when the animation ends. If manual lifecycle management is unnecessary, you can use the `DeleteOnStop` strategy to automatically destroy the animation after playback completes:

```cpp
// Animation object does not require external access, automatically deleted after new
auto *anim = new ValueAnimation<int>;
anim->setValueLimits(0, 100);
anim->setDuration(500);
anim->value.connect(this, &MyWidget::onValue);
anim->start(AbstractAnimation::DeleteOnStop);  // Automatically delete after playing
```

The framework has built-in interpolation support for the following types: `int`, `float` (and other numeric types), `Color`, `Point`, `Pen`, `Brush`, `Length`, `Transform`, etc.

Other common configurations:

```cpp
// Infinite loop playback
anim->setRepeat(AbstractAnimation::Infinity);

// Alternating playback back and forth (forward → reverse → forward...)
anim->setDirection(AbstractAnimation::Alternate);

// Set easing curve
#include "gx_easecurve.h"
anim->setEaseCurve(easing::make_curve<easing::Ease>());
```

### Style Animations and Property Animations

**Style Animations** (`StyleAnimation`) define transition effects in a way similar to CSS transitions, automatically played by the framework when a widget's style state switches, primarily used in style configurations for application-layer components.

**Property Animations** (`PropertyAnimation`) drive properties declared with `GX_PROPERTY` via property name strings, commonly used at the application layer to animate widget properties:

```cpp
#include "gx_propertyanimation.h"

auto *anim = new PropertyAnimation(widget, "value");
anim->setStartValue(Variant{0});
anim->setStopValue(Variant{100});
anim->setDuration(1000);
anim->start(AbstractAnimation::DeleteOnStop);
```

When implementing the widget itself, property animations are usually unnecessary because `ValueAnimation` is more direct and lacks the overhead of looking up properties by name.

## Text Display Widgets

When implementing widgets containing text content, in addition to basic painting logic, you must also handle issues such as text measurement, layout caching, and style linkage. `Label` is the framework's most typical text widget, and its implementation can serve as a reference template for similar widgets.

### Using `updateLayout()`

`update()` only marks a widget as needing a **redraw** and does not affect the layout system. When text content changes, the widget's desired size (the return value of `sizeHint()`) typically changes accordingly. In this case, you must call `updateLayout()` simultaneously to trigger the parent widget's layout recalculation:

```cpp
void MyTextWidget::setText(const String &text) {
    if (m_text == text)
        return;
    m_text = text;
    update();        // Trigger redraw
    updateLayout();  // Notify parent layout to recalculate (because sizeHint changed)
}
```

The consequence of calling only `update()` is that the text content is updated, but the widget size remains what was calculated for the old text, leading to disorganized layouting.

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

For multi-line text that supports auto-wrapping, you also need to implement `heightForWidth()`, informing the layout system of the widget's height at a given width:

```cpp
int MyTextWidget::heightForWidth(int width) const {
    if (width == 0) return 0;
    FontMetrics fm(font());
    float lineHeight = font().pixelSize() * 1.2f;
    // boundingRect calculates the actual boundaries of text at a given width
    return fm.boundingRect(m_text, width, 1024 * 1024, 0, 0, lineHeight).height();
}
```

If the widget is strictly single-line (does not wrap with width), `heightForWidth()` returns `-1` to indicate no dependency on width:

```cpp
int SingleLineWidget::heightForWidth(int) const { return -1; }
```

### Responding to Style and Size Changes

When style properties such as font and color change, text measurement results also change. Override `styleEvent()` to respond to style changes, call the base class implementation to refresh style-related caches, and then trigger layout updates:

```cpp
void MyTextWidget::styleEvent(StyleEvent *event) {
    // Must call base class first; it updates internal style data
    Widget::styleEvent(event);
    // After styles such as fonts change, the return value of sizeHint may change
    updateLayout();
}
```

Similarly, if there are width-dependent text wrapping calculations when the widget size changes, you need to trigger updates in `resizeEvent()`:

```cpp
void MyTextWidget::resizeEvent(ResizeEvent *event) {
    Widget::resizeEvent(event); // Call base class
    update();                   // Redraw content after size change
}
```

::: important
Base class implementations of event handling functions like `styleEvent()` and `resizeEvent()` typically have non-omissible side effects and **must be called**. The timing of the call depends on your logic requirements: in most cases, call the base class first, then execute your own logic.
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

`setFlowLayout(true)` sets a **container widget** to flow layout mode, producing an effect similar to CSS block-level flow. The framework automatically arranges child elements row by row without needing to create independent layout objects via `setLayout()`. `Label` enables this mode in its constructor, allowing itself to act as a `SpanLabel` container (embedding multiple sub-labels with different styles):

```cpp
Label::Label(Widget *parent) : Widget(parent) {
    setFlowLayout(true);
}
```

`setInlineWidget(true)` is a setting targeted at **child elements**, marking the widget as an inline element so that it embeds into the parent container's text flow like text to participate in layouting. For example, embedding an icon widget inline within rich text:

```cpp
auto *icon = new ImageBox(label);
// Mixed-layout with text as an inline element. ImageBox is already inline by default; this is just for illustration.
icon->setInlineWidget(true);
```

When `Label` is used as a `SpanLabel` container accommodating inline child elements, the layout system automatically coordinates `Label`'s own text measurement logic and its arrangement of child elements as a container. Both share the same layout mechanism, and developers do not need to manually intervene in this process.

## `AbstractScrollArea` and Scrollable Widgets

When a widget requires scrolling behavior, there is no need to implement gesture recognition, inertial scrolling, and bounce effects from scratch. Directly inheriting from `AbstractScrollArea` provides these capabilities. The framework's built-in `ScrollArea` (list scrolling) and `TextField` (single-line text input) are both implemented based on it.

### Basic Structure

Widgets inheriting from `AbstractScrollArea` follow a fixed structure: the widget itself is the "viewport", and inside there is a **content widget** responsible for carrying the actual content. When scrolling, it is the content widget that moves, not the viewport itself.

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
    setDamping(5);                // Adjust damping (higher value means stronger friction)

    auto *content = new Widget;   // Create content widget
    setContentWidget(content);
}

bool MyTicker::event(Event *event) {
    return EventDispatch<AbstractScrollArea, LayoutEvent>{}(this, event);
}
```

Setting the base class parameter of `EventDispatch` to `AbstractScrollArea` (instead of `Widget`) allows events not handled by the current class (gestures, wheels, resizes, etc.) to automatically fall back to `AbstractScrollArea`'s implementation, preserving complete scrolling behavior.

### Configuring Scroll Parameters

```cpp
setDirection(Vertical);          // Vertical scrolling (default)
setDirection(Horizontal);        // Horizontal scrolling
setDamping(3);                   // Lower damping: stronger inertia, slides farther
setDamping(20);                  // Higher damping: weaker inertia, close to no inertia
setScrollBar(true);              // Show scrollbar
setBouncesPolicy(SnapType::SnapEdge);  // Edge bounce policy
```

`AbstractScrollArea` also provides `scrollTo(x, y, behavior)` to control the scroll position programmatically, where `behavior` is `Instant` (jump immediately) or `Smooth` (animated).

::: tip Inertia Damping
For widgets like `TextField` that require precise control over the scroll position, a higher damping value is typically set to weaken inertia; whereas for widgets like `ScrollArea` centered around browsing, a lower damping value can be set for a smoother scrolling experience.

Do not set the damping too low; otherwise, ultra-long-distance scrolling may cause content cache invalidation and stuttering.
:::

### Calling Base Class in Event Dispatch

Sometimes you need to perform extra processing on an event before handing control over to `AbstractScrollArea`'s default implementation. A typical approach is to call the base class method directly inside the handler:

```cpp
// Approach in TextField: forward gestures to scroll area only when there is text
bool TextField::gestureEvent(GestureEvent *event) {
    if (text().empty()) // Ignore directly when text is empty
        return false;
    // Hand over to base class scrolling logic in other cases
    return AbstractScrollArea::gestureEvent(event);
}
```

Under this pattern, `Widget` is used as the base class parameter for `EventDispatch`, and the current class decides for itself when and which base class method to call:

```cpp
bool TextField::event(Event *event) {
    // Use Widget as base class, fully controlling when AbstractScrollArea behavior is invoked
    return EventDispatch<Widget, GestureEvent, ResizeEvent>{}(this, event);
}
```

### Event Filtering of Content Widgets

The content widget is responsible for layout and carrying child widgets, but certain events (such as layout requests) sometimes need to be intercepted and custom-processed by the container. Register the container as an event filter for the content widget via `setEventFilter(this)`, and then override `eventFilter()` to handle events of interest:

```cpp
// Register in the constructor
content->setEventFilter(this);

// Intercept content widget layout requests
bool MyTicker::eventFilter(Object *receiver, Event *e) {
    if (receiver == contentWidget() && e->type() == Event::Layout) {
        auto *lv = static_cast<LayoutEvent *>(e);
        if (lv->isLayoutRequest()) {
            // Custom layout logic...
            return true; // Return true to prevent event from continuing to propagate
        }
    }
    // Hand over to base class in other cases
    return AbstractScrollArea::eventFilter(receiver, e);
}
```

::: tip
Unhandled events should be fallen back to `AbstractScrollArea::eventFilter()`, which is responsible for interaction with internal mechanisms like scrollbars.
:::

### Setting Inline Widgets

Calling `setInlineWidget(true)` allows a widget to participate in inline layouts, making it suitable for scenarios embedded in text streams. `TextField` handles things this way so it can be embedded inline like text.

### `ScrollArea` and Derived Classes

`ScrollArea` is a derived class of `AbstractScrollArea` that adds capabilities such as **index navigation** (`index()`/`setIndex()`), **snap modes** (snap), and **visual effects** on top of scrolling. It is the preferred base class for scenarios like lists and tickers. `Swiper`, on top of `ScrollArea`, further adds features like pagination (`pageLength`) and indicator dots, making it suitable for carousel modes and similar patterns.

These classes generally **do not need further subclassing**; most customization requirements can be met by configuring parameters and mounting surrounding facilities without subclassing.

#### Visual Effects (`VisualEffect`)

`ScrollArea` supports mounting a `VisualEffect` object via `setVisualEffect()`. This applies visual transformations such as opacity, scaling, and translation to each child widget before painting it, thereby achieving dynamic effects during scrolling. The framework includes several built-in effects:

| Class Name | Effect |
|---|---|
| `FisheyeVisualEffect` | Fisheye effect: center elements scale up, edges scale down |
| `FadeVisualEffect` | Edge fade-out: opacity decreases the further an element is from the viewport center |
| `CollapseVisualEffect` | Collapse effect: elements gather and shrink towards the top (or bottom) edges |
| `BlendVisualEffect` | Interpolated transition between two effects based on progress |

```cpp
#include "gx_visualeffect.h"

scrollArea->setVisualEffect(make_shared<FisheyeVisualEffect>());
```

If a custom effect is required, inherit from `VisualEffect` and implement the `resolve()` method. `resolve()` receives the target child widget, viewport rectangle, and child widget center point, returning a `PaintModifier` where properties like `opacity`, `scale`, and `translate` can be set.

Complete parameter descriptions for `ScrollArea` and `Swiper`, along with how to implement custom `VisualEffect`s, are covered separately in [Scroll Area](./scroll-area.md).

## Widget Trees and Lifecycles

When creating widgets in C++, parent-child relationships are established through the `parent` parameter of the constructor:

```cpp
// When parent is destroyed, child is also destroyed accordingly
auto *parent = new Widget(window);
auto *child  = new ProgressRing(parent);
child->setGeometry(10, 10, 80, 80);
```

Whether you manually `delete` the parent widget or the framework cleans up the widget tree upon application exit, all child widgets are automatically destroyed. You do not need to `delete` child widgets in the destructor.

If delayed destruction is required (for example, inside an event handling function), you can use `deleteLater()`, which destroys the object after the current event handling completes, avoiding issues like "destroying oneself within a callback".

In the reactive framework, widget trees are maintained by the component framework. Customized development only requires [registering widget classes](./widget-export.md).