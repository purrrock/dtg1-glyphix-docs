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