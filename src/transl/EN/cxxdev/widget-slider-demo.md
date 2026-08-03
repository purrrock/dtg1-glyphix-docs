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