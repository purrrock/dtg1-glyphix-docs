# Practical Guide to Custom Widgets

`slider-demo` is a complete example included with the Glyphix SDK, demonstrating how to implement a **custom control**—`WaveSlider`—from scratch in C++. This control adds a wave-fill effect and a click-ripple motion effect on top of the standard `Slider`. The example also covers `StyleEngine` customization and building UI interfaces directly in C++.

Using this example as a guideline, and combining it with the core concepts from the [Widget Development Guide](./widget.md), this article demonstrates the complete steps required to customize a new Widget.

## Example Structure

The file structure of the example is as follows:

```
app/slider-demo/
├── CMakeLists.txt
├── main.cpp           # Application entry point, building the UI directly in C++
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

In `main.cpp`, the application's UI is entirely constructed using C++ code within the constructor, styled similarly to Qt Widgets or LVGL: child controls are created via `new` and passed a pointer to their parent control, without declarative templates.

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

`Application` receives a platform backend object (`BSPPlatform`) and a resolution. `Window` is the root control. When `setFlowLayout(true)` is enabled, its child controls automatically arrange themselves according to a flow layout.

`setStyleEngine` mounts a custom style engine. This is optional (the default style is used otherwise). You only need to provide your own implementation when you need to customize the appearance of controls (such as modifying the `Switch` as shown below).

### The `MyWidget` Class

`MyWidget` inherits from `ScrollArea`, creating and adding child controls in its constructor:

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

Child controls are declared as member variables and initialized automatically upon construction (the parent-child relationship is established in `addItem`). The lifecycle of these member variables is managed by `MyWidget`, requiring no manual `delete`.

`ScrollArea` provides out-of-the-box scrolling, inertia, and bounce-back capabilities, allowing `MyWidget` to operate without writing any custom scrolling logic.

::: tip Role of `addItem()`
In general, you can attach child controls directly to a parent control using `setParent()`. However, `ScrollArea` internally contains a dedicated content container (`contentWidget()`). Regular elements cannot be added directly to a `ScrollArea`; instead, they must be added to the content container via `addItem()`.

For simple containers, `setParent()` and `addItem()` have the same effect. But for special containers like `ScrollArea`, you **must** use `addItem()` to add elements.
:::

### Signal Connections

States are synchronized between controls using signal connections:

```cpp
m_slider.changed.connect(this, &MyWidget::onSlider);
m_switch.checked.connect(this, &MyWidget::onSwitch);

// Bidirectionally synchronize the values of two Sliders
waveSlider->changed.connect<AbstractSlider>(&m_slider, &Slider::setValue);
m_slider.changed.connect<AbstractSlider>(waveSlider, &WaveSlider::setValue);

// Toggle the wave mode of WaveSlider using the switch
m_switch.checked.connect(waveSlider, &WaveSlider::setWaveMode);
```

::: tip Signal Usage
The syntax for signal connection is `signal.connect(receiver, &Type::method)`. When the signatures of `Slider::setValue` and `WaveSlider::setValue` do not match exactly, you can declare a common base class (`AbstractSlider`) via template parameters to resolve ambiguity.

If you are unsure of the actual type to which a slot function belongs, you can check it using IDE hints. For example, when inspecting `Slider::setValue`, the IDE typically suggests:
```cpp
public method
void setValue(int value) in class AbstractSlider 
```
This indicates that `setValue` is actually declared in `AbstractSlider`. Therefore, you must specify `AbstractSlider` during connection to resolve ambiguity:
```cpp
m_slider.changed.connect<AbstractSlider>(waveSlider, &WaveSlider::setValue);
```
:::

### Styling with StyleModifier

`StyleModifier` is a tool for programmatically setting control styles in C++, functionally equivalent to configuring style properties in a template:

```cpp
StyleModifier m(waveSlider);
m->setSize(120, 300);
m->setMargin(Style::Margin{Length::fromAuto(), 20});
m->setColor(Color{"#35a7ff"});
```

`setColor` sets the foreground color for the `WaveSlider`, which is read in `paintEvent` and used to render the progress fill color.

## Customizing StyleEngine

The built-in [`Switch`](/components/switch.md) is a fully functional toggle control, but its default appearance resembles [Fluent 2](https://fluent2.microsoft.design/components/web/react/core/switch/usage), which might not suit the visual style of a specific device or brand.

`StyleEngine` is the mechanism designed to solve this. Device manufacturers can implement their own `StyleEngine` to customize the appearance of all built-in controls while retaining their interaction logic, without modifying framework code.

A customized `Switch` is not just a change in theme color; rather, the entire set of switch animations (thumb translation, color transition, press scaling) is achieved through **programmatic interpolation** rather than pre-recorded frame sequences. This means:

- Animations are completely smooth, with frame rates matching the rendering system;
- Colors and sizes can be overridden by application developers through style properties, as `StyleEngine` provides overridable default values;
- No need to prepare different image assets for various resolutions.

### Responsibilities of `StyleEngine`

`StyleEngine` is the core of the Glyphix styling system, responsible for three tasks:

1. **Providing a palette**: Global color variables, similar to CSS custom properties, which can be read by all built-in and custom controls.
2. **Painting control appearance**: The visual effects of built-in framework controls (such as `Switch`, `Slider`) are entirely delegated to `StyleEngine::paint()`, which developers can override in derived classes to achieve completely different appearances.
3. **Recommending sizes (size hint)**: The recommended size of a control under different style states, used as a reference for the layout system.

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

`sizeHint()` informs the framework of the **recommended size** of built-in controls under a given style state. Taking `Switch` as an example, its width and height should be proportional to the font pixel size:

```cpp
Size MyStyleEngine::sizeHint(StyleOption::Type type, const Widget *widget) const {
    // The size ratio of the customized Switch can differ from the built-in strategy
    if (type == StyleOption::OptionSwitch) {
        float f = widget->font().pixelSize();
        int d = int(round(f));
        return {int(round(f * SwitchAspectRatio)), d};
    }
    return StyleEngine::sizeHint(type, widget); // Fall back to base class for other types
}
```

Be sure to call `StyleEngine::sizeHint(type, widget)` at the end of the function to fall back to the default implementation, otherwise controls of other types will receive zero dimensions.

### Overriding `paint()`

`paint()` dispatches to the corresponding rendering logic based on the `option()` type of `StyleOption`, falling back unhandled types similarly:

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

`StyleOptionSwitch` is a derived class of `StyleOption`, adding state fields specific to the Switch. It carries two key animation progress values:

- `option.transition`: Switch toggle transition progress, `0.0` for closed state, `1.0` for open state, and intermediate values indicating the animation is in progress.
- `option.scale`: Scaling factor when pressed, used to render press feedback effects.

Using these two values, smooth state transitions can be achieved within `drawSwitch`:

```cpp
// Interpolate between open and closed colors
color = color.blend(checked.background().color(), option.transition);

// The position of the thumb indicator moves with the transition progress
float pos = option.transition * (box.width() - size - len);
```

`StyleEngine` drives the animation, and developers only need to interpolate based on progress values within `paint()` to obtain complete transition effects.

::: tip Customizing Only Specific Controls
The default `StyleEngine` implements the rendering logic for all built-in controls, some of which are quite complex. If you are only dissatisfied with the appearance of certain controls, you should override the rendering logic for those specific controls in your derived class, letting other controls fall back directly to the base class implementation.

You should prioritize satisfying custom color requirements via the palette, and only override `paint()` when completely different visual effects are needed.
:::

### Drawing Rounded Capsule Shapes with VectorPath

The background and thumb of the default `Switch` are both rounded capsule shapes. The example uses `VectorPath` combined with two arcs to draw this, which is a more flexible approach than `drawRoundedRect`, suitable for scenarios requiring independent control over the radiuses of both ends:

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

The two arcs connect end-to-end, and `arcTo` automatically connects lines within the path without requiring an extra `lineTo`.

## WaveSlider: Complete Practice for Custom Controls

`WaveSlider` is the core of this example, demonstrating the complete development workflow for a custom control. Similar to the `StyleEngine` customization above, the design goal of `WaveSlider` is to **overlay** new visual effects without disrupting existing capabilities:

- **Wave fill** mode: The progress area is filled with dynamic waves instead of a regular rectangular progress bar;
- **Click ripple** effect: Generates a diffusing oscillation when pressed, temporarily enhancing and then recovering the waves;
- **`waveMode` property**: Allows switching between wave mode and regular mode at runtime, supporting application-layer binding and property animations;
- **Full fallback compatibility**: When wave mode is disabled, `WaveSlider` directly calls `Slider::paintEvent()` to fall back to the default appearance, reusing all parent capabilities such as dragging, `value`, and `changed`, with zero code changes required on the application side.

### Class Definition and Inheritance

`WaveSlider` inherits from `Slider` (rather than directly from `Widget`), allowing it to reuse `Slider`'s existing gesture-dragging logic, properties like `value`/`minimum`/`maximum`, and the `changed` signal:

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

`GX_OBJECT` must be placed at the very beginning of the class definition; it triggers the meta-object compiler to generate metadata for this class. `GX_PROPERTY` exposes `waveMode` to the property system, making it bindable by the application layer (e.g., `<wave-slider :wave-mode="enabled"/>`) and drivable by property animations.

### Member Variables

The runtime state of the control is stored in member variables:

```cpp
private:
    bool  m_waveMode = false;       // Whether currently in wave mode
    float m_rippleProgress = 1.0f;  // Ripple progress [0, 1], initially 1 (inactive)
    float m_waveOffset = 0.0f;      // Waveform phase offset [0, 1], driven by animation
    ValueAnimation<float> m_animation;        // Wave loop animation
    ValueAnimation<float> m_rippleAnimation;  // Ripple animation
    friend struct EventTraits<WaveSlider>;    // Allow event dispatching to access protected methods
```

`ValueAnimation<float>` is used directly as a member variable (rather than a pointer), with its lifecycle managed by `WaveSlider`, requiring no manual `delete`.

### Constructor: Initializing Animations

The constructor configures two animations and sets the orientation:

```cpp
WaveSlider::WaveSlider(Widget *parent) : Slider(parent) {
    // Wave animation: infinite loop, one full cycle per second
    m_animation.setRepeat(AbstractAnimation::Infinity);
    m_animation.setValueLimits(0.f, 1.f);
    m_animation.setDuration(1000);
    m_animation.value.connect(this, &WaveSlider::onWaveAnimation);
    m_animation.start();

    // Ripple animation: plays once when pressed, duration 800ms
    m_rippleAnimation.setValueLimits(0.f, 1.f);
    m_rippleAnimation.setDuration(800);
    m_rippleAnimation.value.connect(this, &WaveSlider::onRippleAnimation);

    setVertical(true);  // Vertical slider
}
```

`m_animation` runs continuously after starting, advancing `m_waveOffset` from $0$ to $1$ every frame before looping back to $0$. This value is eventually converted into the phase offset of the waveform, causing the waves to flow continuously.

`m_rippleAnimation` is triggered only upon being pressed, playing once and then stopping without setting `Infinity`. The callbacks for both animations do only one thing: update state variables and call `update()` to request a redraw.

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

`event()` uses [`EventDispatch`](widget.md#handling-events) to route events, with template parameters listing the event types actually handled by the current control, providing compile-time checking:

```cpp
bool WaveSlider::event(Event *event) {
    return EventDispatch<Widget,
        GestureEvent, PaintEvent>{}(this, event);
}
```

#### Handling Gestures: Triggering Ripples

`gestureEvent()` intercepts the start of the `Press` gesture to trigger a ripple, delegating all other cases to `Slider`'s gesture handling (implementing drag-to-adjust-value):

```cpp
bool WaveSlider::gestureEvent(GestureEvent *event) {
    if (!event->isHitTest() && event->gesture()->type() == Gesture::Press) {
        auto g = static_cast<PressGesture *>(event->gesture());
        if (g->isStarted())
            startRipple(g->clientPoint());
    }
    return Slider::gestureEvent(event); // Pass the event further to Slider for processing
}

void WaveSlider::startRipple(const Point &) {
    m_rippleProgress = 0.f;      // Start from the beginning
    m_rippleAnimation.start();   // Replay
}
```

When `isHitTest()` is `true`, it indicates that this is a hit-test (used by the framework to detect whether an event should fall onto this control), not actual user interaction, and should be skipped.

::: tip Regarding `isHitTest()`
Hit-testing is a prerequisite step in event dispatching. `gestureEvent()` is also called during the hit-test phase, but no side effects (such as starting animations) should occur at this time. Always check `!event->isHitTest()` before processing interaction logic.
:::

#### Style Reading Interface

`paintEvent()` reads the style data corresponding to the control. Two relevant interfaces are introduced here:

- `style()` / `style(Styles::Xxx)` returns the `Style` object for a certain style pseudo-class of the current control, from which properties such as color and background can be read;
- `se->palette(StyleEngine::Xxx)` reads the global palette color from the `StyleEngine`, acting as a default when the control has no custom color set.

The two are used together to implement the logic of "using custom colors when custom configurations exist, otherwise falling back to theme default colors":

```cpp
auto contentStyle = style(Styles::Content);
p.setBrush(contentStyle.hasProperty(style::Background)
               ? contentStyle.background()
               : se->palette(StyleEngine::ProgressRange));
```

### Rendering Implementation

`paintEvent()` is the core of WaveSlider. It decides which rendering path to take based on `m_waveMode`:

```cpp
void WaveSlider::paintEvent(PaintEvent *event) {
    discard(event);  // PaintEvent itself carries no useful info; explicitly discard to eliminate compiler warnings

    if (!isWaveMode())
        return Slider::paintEvent(event);  // Normal mode: directly call parent rendering

    auto se = App()->styleEngine();
    RectF box = rect();
    float radius = min(box.width(), box.height()) * 0.5f;
    float progress = sliderRange ? float(value() - minimum()) / float(sliderRange) : 0.f;

    Painter p(this);

    // Draw background (empty track)
    p.setBrush(/* background color */);
    p.fillRoundedRect(box, radius);

    // Draw wave fill (progress area)
    p.setBrush(/* foreground color */);
    VectorPath path;
    buildWaveFillPath(path, box, radius, progress, m_waveOffset, m_rippleProgress);
    if (!path.isEmpty())
        p.fillPath(path);
}
```

The entire rendering is split into two steps: first, draw the complete background rounded rectangle using `fillRoundedRect`, then draw the waveform fill on top using `fillPath`, overlaying the two layers to form a "progress bar with ripples."

#### Waveform Path Generation

`buildWaveFillPath()` is an independent helper function (not inside the class) responsible for constructing the waveform path under given geometric constraints:

```cpp
static void buildWaveFillPath(VectorPath &path, const RectF &box, float radius,
                              float progress, float waveOffset, float rippleProgress)
```

Its core logic is divided into three steps:

1. **Calculate water level and amplitude**: `waterLevel` rises from the bottom according to the `progress` ratio; amplitude depends on the aspect ratio and is constrained within limits far enough from the top and bottom arcs to prevent the waveform from going out of bounds.
2. **Sample the waveform**: Sample uniformly from left to right, calculating the $y$ value for each $x$ coordinate.
   The waveform is a superposition of three parts: a regular sine wave (controlled by `m_waveOffset`) + ripple gain (decay oscillation controlled by `m_rippleProgress`) + rounded corner constraints (ensuring the path does not exceed the boundaries of the rounded rectangle).
3. **Close the path**: Return along the bottom edge from the top of the waveform to the bottom of the rounded rectangle to form a closed polygon for `fillPath` to fill.

The algorithmic details are for educational demonstration purposes; in actual products, they can be replaced with any custom path generation logic according to design requirements.

::: tip Efficiency of Path Drawing
The number of sample points (`sampleCount`) is proportional to the width of the control (approximately one point every `4px`), and performance overhead is acceptable at typical screen resolutions. If the CPU is weaker, you can reduce the sampling density or switch to cubic Bézier curve approximations.
:::

### The waveMode Property

The implementation of `setWaveMode()` is simple: update the member value when the state changes and mark for a redraw:

```cpp
void WaveSlider::setWaveMode(bool enabled) {
    if (m_waveMode != enabled) {
        m_waveMode = enabled;
        update();
    }
}
```

The declaration of the `GX_PROPERTY` macro makes `waveMode` a property visible to the framework:

```cpp
GX_PROPERTY(bool waveMode, get isWaveMode, set setWaveMode)
```

No `signal` field is declared here because it is typically driven by the consumer to change values rather than triggered by interaction.

### Production-Grade Optimizations

The implementation of `WaveSlider` is primarily geared towards educational demonstrations and lacks some optimizations, such as:
- The wave animation plays continuously even when `waveMode` is disabled, calling `update()` repeatedly and triggering unnecessary `paintEvent()` calls;
- It only supports vertical sliders and is not adapted for horizontal modes (which can be handled according to product requirements);
- It fixedly draws capsule-shaped tracks, whereas actual products might require rounded rectangles or other shapes.

## Collaboration Between Components

Here is how the components in `slider-demo` collaborate at runtime:

```
User presses the screen
    ├─ WaveSlider::gestureEvent() detects Press.isStarted()
    │       └─ startRipple() resets m_rippleProgress and starts m_rippleAnimation
    └─ Slider::gestureEvent() continues processing, adjusting value based on touch point
            └─ changed signal emitted → MyWidget::onSlider() updates Label text

Per-frame rendering loop
    ├─ m_animation continuously advances m_waveOffset (0→1 loop)
    │       └─ update() → paintEvent() redraws wave with new offset
    └─ m_rippleAnimation advances m_rippleProgress (0→1 plays and stops)
            └─ update() → paintEvent() redraws ripple decay with new rippleProgress

Switch toggle
    └─ waveSlider->setWaveMode(true/false)
            └─ update() → paintEvent() switches to normal or wave mode
```

Signal connections are established once in `MyWidget`'s constructor. Afterward, runtime execution is entirely driven by events and signals, with no direct calls between controls.

## Summary of Key Patterns

Through `slider-demo`, we can summarize typical patterns for implementing custom controls in Glyphix:

| Requirement | Approach |
|---|---|
| Inherit an existing control and reuse its interaction logic | Inherit from the corresponding base class (e.g., `Slider`), and control fallback to the base class inside `EventDispatch` |
| Custom rendering | Implement `paintEvent()`, falling back to `Slider::paintEvent()` when `isWaveMode()` is `false` |
| Continuous looping animation | `ValueAnimation::setRepeat(Infinity)` |
| One-shot triggered animation | Save state variables, and call `anim.start()` in `gestureEvent()` to replay |
| Expose properties to the application layer | `GX_PROPERTY` macro, paired with getters/setters and optional signals |
| Read user color schemes or theme colors | Check using `style().hasProperty()` and fall back to `se->palette()` |
| Customize global control appearance | Inherit from `StyleEngine`, overriding `paint()` and `sizeHint()` |

These patterns are elaborated in the [Widget Development Guide](widget.md), and `slider-demo` serves as a comprehensive practical application of them.

## Comparison with Other GUI Frameworks

::: important Positioning of C++ Control Development
The mainstream development approach in Glyphix is building interfaces via declarative templates using [`.ux Single File Components](../tutorials/quick-orientation.md). C++ control development is used for implementing **low-level control libraries on the device side** (such as the device-manufacturer-customized `WaveSlider`), which are subsequently used by frontend application layers through templates and data bindings. Building complete UIs directly in C++ (like the demonstration in `main.cpp`) is **possible within the framework, but not the recommended workflow**, and related toolchain support (debugging, hot-reloading, layout preview) is less mature compared to the application layer.

Therefore, when evaluating Glyphix's overall development efficiency, the frontend application layer should be used as the benchmark; the C++ control development experience discussed in this section only represents the development scenario for low-level control libraries.
:::

In terms of mental models, Glyphix's C++ control development is closer to Qt Widgets than to LVGL: the signal mechanism, property macros, inheritance-based extension, and the naming and division of responsibilities for `paintEvent` all largely correspond to Qt Widgets. Developers with a Qt background can quickly build intuition.

LVGL developers will need to transition from a C handle-style paradigm to a C++ OOP paradigm, which represents a slightly larger gap. However, core paradigms such as control tree organization and `update()` redraw triggering are common. This section uses `slider-demo` as a reference to specifically explain the similarities and key differences between frameworks.

### Similarities

Whether Qt Widgets, LVGL, or Glyphix, they share a set of proven UI framework core paradigms:

- **Control Tree**: UIs are organized in a parent-child tree structure, where child control coordinates are relative to their parent. `MyWidget(&window)` corresponds semantically to Qt's `new QWidget(&parent)` and LVGL's `lv_obj_create(parent)`.
- **Custom Rendering**: Control appearance is achieved by "overriding" rendering methods. Qt overrides `paintEvent(QPaintEvent *)`, LVGL registers the `LV_EVENT_DRAW_MAIN` callback, and Glyphix implements `paintEvent(PaintEvent *)`. The design philosophy across all three is consistent.
- **Signal/Slot Mechanism**: State changes are communicated between controls via signals, with receivers responding using member functions.
  - Glyphix: `m_slider.changed.connect(this, &MyWidget::onSlider)`;
  - Qt: `connect(&slider, &QSlider::valueChanged, this, &MyWidget::onSlider)`;
  - LVGL: Achieves similar functionality via event callback functions.
- **Inheritance and Reuse**: Extending existing controls is achieved via inheritance. `WaveSlider : public Slider` reuses all dragging and value-fetching logic of the parent class, overriding only the rendering part, which is consistent with the design of most OOP GUI frameworks.
- **On-Demand Redrawing**: When state changes, `update()` is called to mark dirty areas, and the framework uniformly redraws them in the next frame rather than drawing immediately. Mainstream frameworks all adopt this strategy to avoid redundant drawing within the same frame.

### Differences from Qt Widgets

#### Event Dispatching

Qt dispatches events through virtual function overrides, where each event method is `virtual` and overridden in subclasses using `override`:

```cpp
// Qt
class MySlider : public QSlider {
    void paintEvent(QPaintEvent *event) override { ... }
    void mousePressEvent(QMouseEvent *event) override { ... }
};
```

Event handling functions in Glyphix, such as `paintEvent()` and `gestureEvent()`, are **not virtual functions** and cannot use `override`. Event routing is done at compile-time by `EventDispatch`:

```cpp
// Glyphix
bool WaveSlider::event(Event *event) {
    return EventDispatch<Widget, GestureEvent, PaintEvent>{}(this, event);
}
// Both paintEvent and gestureEvent are regular member functions without override
```

This avoids the indirect jumps of virtual functions, providing performance advantages in high-frequency event handling on embedded devices. At the same time, the template parameter list acts as compile-time documentation and omission checks. If you declare that you handle `PaintEvent` but forget to implement `paintEvent()`, the compiler will throw an error rather than silently falling back to the base class.

#### Object and Property Systems

Qt uses the `Q_PROPERTY` macro along with MOC (Meta-Object Compiler) to generate property metadata; Glyphix uses `GX_PROPERTY` alongside `GX_OBJECT`. The mechanisms are similar, but the generation methods and runtime interfaces differ:

```cpp
// Qt
Q_PROPERTY(int value READ value WRITE setValue NOTIFY valueChanged)
// Glyphix
GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
```

Both support driving animations via property name strings (`QPropertyAnimation` / `PropertyAnimation`). However, when implementing controls themselves, Glyphix recommends using `ValueAnimation<T>` directly to avoid property name lookup overhead and prevent conflicts with application-layer-driven property animations.

#### Signals and Slots

As described in the [Object System](object-system.html#signal), Glyphix also has a signal mechanism, but it is closer to `boost::signals2` and does not rely on MOC to generate code. This is an intentional design choice because the [build system](sdk-setup.md#other-build-systems) of the Glyphix ecosystem is relatively fragmented, and we assume that downstream users do not use the meta-object compiler at all.

#### Styling and Appearance Customization

Qt provides two paths for customizing control appearance: `QStyle` subclassing (complex) or QSS stylesheets (CSS-like strings parsed at runtime). Glyphix uses `StyleEngine`: manufacturers implement a `StyleEngine` subclass, rendering the appearance of all built-in controls in C++ code within `paint()`, and providing recommended sizes in `sizeHint()`. This approach is suitable for global system-level style customization rather than local style adjustments of individual controls.

For styling individual controls, Glyphix uses the `StyleModifier` helper object for programmatic assignment instead of relying heavily on CSS strings:

```cpp
StyleModifier m(waveSlider);
m->setSize(120, 300);
m->setColor(Color{"#35a7ff"});

// Inline style strings are also supported
waveSlider->setStyle(Style{"background-color: #35a7ff; color: #cce;"});
```

Glyphix's style and layout properties are set more through style properties than by directly calling control methods. This is because C++ is primarily positioned for low-level control library development and does not directly target application development.

#### Memory and Lifecycles

Under Qt's parent-child control ownership model, child controls are destroyed by their parent after `new QWidget(parent)`. Glyphix also supports this model (`new WaveSlider` followed by `addItem()`), and additionally recommends declaring child controls as member variables (such as `m_label` and `m_slider` in `MyWidget`), where lifecycles are automatically managed alongside the host object without manual `delete` and without depending on parent-child tree destruction mechanisms.

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

For LVGL developers, the main change here is not the capabilities themselves, but the expression: previously you called functions outside of object handles, whereas now you organize state, events, and rendering logic inside the control class. The type system also helps you avoid certain handle-type misuses at compile time.

#### Event System

LVGL's event handling typically receives multiple events through a single callback function, branching using `lv_event_get_code()` inside the callback:

```c
// LVGL
static void event_cb(lv_event_t *e) {
    lv_event_code_t code = lv_event_get_code(e);
    if (code == LV_EVENT_PRESSED) { ... }
    else if (code == LV_EVENT_VALUE_CHANGED) { ... }
}
```

Glyphix dispatches events to independent handling functions by event type, completely isolating different events, with each carrying type-correct data:

```cpp
// Glyphix
bool WaveSlider::gestureEvent(GestureEvent *event) { ... }
void WaveSlider::paintEvent(PaintEvent *event) { ... }
```

In addition, Glyphix's `isHitTest()` mechanism does not have an exact equivalent in LVGL. LVGL can handle similar issues via `LV_EVENT_HIT_TEST`, but typically still requires manual branching within the same callback.

::: tip Glyphix's Internal Event Dispatch Mechanism
`EventDispatch` is also implemented internally via a switch-case dispatch, but we do not recommend developers write manual switch branches. Instead, always use the fixed `EventDispatch<Widget, ...>{}(this, event)` pattern to facilitate code auditing.
:::

#### Animations

LVGL animations are configured via the `lv_anim_t` structure, with target values passed through function pointers and `void *` user data:

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

Glyphix's `ValueAnimation<T>` determines the interpolation type at compile time via template parameters, eliminating `void *` casting through signal connections:

```cpp
// Glyphix
m_rippleAnimation.setValueLimits(0.f, 1.f);
m_rippleAnimation.setDuration(800);
m_rippleAnimation.value.connect(this, &WaveSlider::onRippleAnimation);
```

`ValueAnimation<T>` has built-in interpolation support for composite types such as `Color`, `Point`, and `Transform`, whereas LVGL natively supports only integer ranges, requiring developers to implement custom interpolation callbacks for composite types.

#### Vector Path Rendering

LVGL's rendering API focuses primarily on basic primitives like rectangles and arcs, and vector path support (`lv_draw_vector`) is a relatively recent addition with a lower-level interface. Glyphix's `VectorPath` is a standard path-building interface, where `moveTo`, `lineTo`, `arcTo`, `conicTo`, and `cubicTo` fully cover common curve types. The waveforms in `WaveSlider` rely entirely on this interface without requiring additional graphics libraries.

#### Memory and Lifecycles

Both support object tree management: child controls are attached under parent controls, and when the parent object is destroyed, child objects are destroyed alongside it.

Glyphix also allows child controls, animations, and runtime states to be written directly as class members, managed automatically via C++ RAII. For example, `m_label` and `m_slider` in `MyWidget`, as well as the two `ValueAnimation<float>` instances in `WaveSlider`, can be constructed and destructed along with the host object, eliminating the need to organize states primarily around handles, `user_data`, and callback contexts like in LVGL.