# Widget Registration and Framework Integration

In the [Widget Development Guide](./widget.md), we implemented a C++ widget class. However, at that stage, it is merely an ordinary C++ object, and application developers cannot use it directly in page code. This article explains how to register a widget with the framework so that it becomes a component usable within applications. Many concepts in this document relate to the [Object System](./object-system.md); reading that section first is recommended.

## Runtime Environment

Widget registration relies on a set of **runtime environment objects**. These are mandatory dependencies for the reactive framework to run, must be explicitly created in `main()` or platform startup code, and their lifecycles must cover the entire duration of the application's execution:

```cpp
Application app(/* platform */);
JsVM vm;
Window window;
AppletKit kit(&window, "pkgs.db");
```

These objects manage the runtime environment of the entire application:
- `Application` is the framework application object that manages all low-level services and maintains the event loop. At the end of initialization, call `app.exec()` to enter the event loop;
- `JsVM` is the embedded JavaScript engine that hosts the reactive framework, and **must** be created before `AppletKit`;
- `Window` is the top-level window, serving as the rendering output target;
- `AppletKit` is the applet manager, responsible for application lifecycles and widget registration.

::: warning Do Not Omit These Objects
`vm`, `window`, `kit`, and others are RAII objects; the framework manages the runtime environment through their constructors and destructors. Even if there are no direct calls to `vm` in the code, its **very presence** is required—destroying it prematurely or failing to create it will cause the framework to malfunction.
:::

`Window window` can sometimes be replaced with `Widget window`, etc. The difference is that `Window` renders an opaque background by default, whereas `Widget` is transparent by default.

## Registering Widgets

Widget registration is completed via `AppletKit::installWidget<T>()`. This must be called after `AppletKit` is instantiated and **before** `launch()` starts the first application:

```cpp
// Register a custom widget (before launch)
kit.installWidget<ProgressRing>(); // No arguments, registered by class name, written as <progress-ring> in templates
kit.installWidget<MySpecialChart>("SpecialChart"); // Or registered with a custom name (see below)

kit.launch("com.example.app");     // Start the application
return app.exec();                 // Enter the event loop
```

::: tip Built-in Widgets Are Registered by Default
Built-in widgets provided by the framework, such as buttons and labels, are registered by `installBuiltinWidgets()`. As long as the SDK is built with the CMake option `GX_BUILTIN_BINDINGS` enabled (default `ON`), `AppletKit` will **automatically call** it upon construction, requiring no manual handling. You only need to manually call `kit.installBuiltinWidgets()` if you explicitly disable that option.
:::

Upon registration, the framework automatically exports its properties, events, methods, as well as the enum and struct types they use, based on the widget class's `GX_OBJECT` metadata, making them available at the application layer.

### Using Widgets in Application Pages

Once successfully registered, application developers can use the widget in page templates just like built-in widgets:

```xml
<!-- Taking the progress-ring component as an example -->
<progress-ring
  class="ring"
  :value="progress"
  @completed="onDone">
</progress-ring>
```

Here, `:value="progress"` binds the widget's `value` property to the application data `progress`; `@completed` listens to the `completed` event exposed by the widget. The framework automatically handles the bidirectional conversion between JavaScript values and C++ properties, eliminating the need for developers to write any "bridge code."

### Custom Component Names

By default, widgets are registered by their **class name**. If the class name is not suitable to be used directly as a component name, a custom name can be specified during registration:

```cpp
// Register VendorWaveformGraph as WaveformGraph, written as <waveform-graph> in templates
kit.installWidget<VendorWaveformGraph>("WaveformGraph");
```

Custom names should use **PascalCase**, matching the style of C++ class names.

### C++ ↔ UX Naming Conversion

Component tag names correspond to the registration name (by default, the **class name** declared by `GX_OBJECT`, or the custom name specified during registration). It is customary to use kebab-case in templates, **and the ux packaging tool is responsible for name conversion at compile time**:

- Tag names: kebab-case in templates ↔ PascalCase registration names. For example, `<progress-ring>` corresponds to the `ProgressRing` class. The same applies to custom registration names.
- Property names: kebab-case in templates ↔ camelCase in C++. For example, `ring-color` corresponds to the `ringColor` property.

In other words, the runtime framework performs exact matching using the original names declared in C++ (camelCase / PascalCase), while the kebab-case syntax is merely a convention on the template side, which is converted by the ux tool to interface correctly.

UX components can also use the same PascalCase for tags and camelCase for properties as C++, as detailed in the [Component Naming Specification](/tutorials/name-spec.md).

## Property and Event Exporting

Properties declared with `GX_PROPERTY` are automatically exported according to the following rules:

- The property name is directly identical to the property name in the framework component
- Properties with a declared setter (`set xxx`) can be assigned values by the application
- Properties with a declared getter (`get xxx`) can be read by the application
- When a signal is declared (`signal xxxChanged`), signals indicating property changes are forwarded to bindings

For example, consider the following complete property declaration:

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

Properties in templates are written in kebab-case, corresponding to camelCase property names in C++: `ring-color` → `ringColor`, `show-label` → `showLabel` (conversion is handled by the ux packaging tool, see above). `:value` and `:show-label` are dynamic bindings (values are expressions), whereas literals like `ring-color="#409EFF"` are static assignments.

### Event Exporting

Component events are exported through **properties with change signals**, rather than exporting `Signal<>` members directly. Exporting an event takes two steps:

1. Declare a `Signal<...>` member (used internally by C++);
2. Reference it in the `signal` field of a `GX_PROPERTY`.

The key rule is: the event name listened to on the application side is the **property name**, **not** the name of the signal member.

### Value-Bearing Property Change Events

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    int value() const;
    void setValue(int v);

    Signal<int> valueChanged;   // Internal signal, this name is invisible to the application
    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
};
```

The application side listens to changes using `@property-name`, so write `@value` (the property name) here, **not** `@value-changed`: even though the signal member is called `valueChanged`, the event name seen by the application is always the property name `value`.

```xml
<progress-ring :value="progress" @value="onProgressChanged"></progress-ring>
```

This behavior is completely consistent with framework built-in widgets. For example, the `Slider` value change signal member is called `changed`, but the application side still listens to the property name `value` (`@value` or two-way binding `::value`).

### Value-less Pure Events

For events that carry no value and simply indicate "something happened" (such as "completed"), use `invalid_t` as the property type to declare a property that has only a signal and no read/write value:

```cpp
Signal<>  completed;   // Emitted when progress completes
GX_PROPERTY(invalid_t completed, signal completed)
```

The application side can listen to it like this (without an event value):

```xml
<progress-ring @completed="onDone"></progress-ring>
```

You cannot declare a `GX_PROPERTY` with a `void` type, even if it has no `get`/`set` at all; therefore, `invalid_t` must be used as a placeholder type. If you want an event to carry a value, it must be declared as a specific type and provide a `get` method—the parameter type of `Signal<T>` does not automatically become the event value, which always originates from the property's getter.

::: warning `Signal<>` Does Not Automatically Become an Event
Declaring a `Signal<>` member without referencing it via the `signal` field in any `GX_PROPERTY` means this signal **cannot** be listened to on the application side using `@some-event`. The framework only exposes "property change signals"—that is, the `signal` field—as events, and the event name always derives from the property name.
:::

## Method Exporting

Member functions declared with `GX_METHOD` are exported as component methods for applications to call in JavaScript:

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    GX_METHOD void reset();               // Method without parameters
    GX_METHOD void animateTo(int target); // Method with parameters
};
```

Unlike properties and events, methods are not used via template tags. Instead, you first obtain the native component object using [`$element()`](../framework/component/component-apis.md#element), and then call methods on it. This requires setting an `id` for the component in the template:

```xml
<progress-ring id="ring" :value="progress"/>
```

```js
onReady() {
  const ring = this.$element('ring'); // 'ring' is the component id in the template
  ring.reset();
  ring.animateTo(80);
}
```

Method arguments and return values are automatically marshaled by the framework via `Variant`, requiring no manual conversion code (for details on type bridging, see [Object System · Runtime Type System](./object-system.md#运行时类型系统)). Note that `$element()` must be called during or after the [`onReady()`](../framework/component/life-cycle.md#onready) lifecycle, as detailed in [Native Components](../framework/component/native-component.md).

## Enum and Struct Types

When the type of a property or method parameter is a custom C++ enum or struct, annotate it with `GX_ENUM` or `GX_STRUCT` to export it together. When [registering the widget](#注册控件), the framework automatically installs the corresponding type conversions without requiring manual binding code. Enums appear as string constants on the JavaScript side, and structs appear as object literals:

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    // Note: define aliases for values, otherwise JavaScript side will use
    // 'Solid' / 'Dashed' names instead of the expected 'solid' / 'dashed'
    enum GX_ENUM LineStyle {
        Solid GX_ALIAS("solid") = 0,
        Dashed GX_ALIAS("dashed"),
    };
    // Structs should have default values to avoid undefined fields when created on the JavaScript side
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

For complete semantics such as enum aliases, struct field mapping, and nested types, refer to [Object System · Complex Type Reflection](./object-system.md#复杂类型反射), which will not be elaborated further here.

::: warning Do Not Forget Annotations
When custom enums/structs are used in properties or methods, be sure to annotate them with `GX_ENUM` / `GX_STRUCT`; otherwise, they will be unusable on the JavaScript side without any compilation error prompts.
:::

## Accommodating Sub-widgets (Container Widgets)

If a widget needs to contain sub-content declared by the application, simply implement it as a **container widget**: layout of sub-widgets is handled on the C++ side, and the framework automatically creates sub-components nested within the template declarations as sub-widgets and mounts them under it. Glyphix does not have HTML-like named slots; nested tags in templates directly become sub-widgets of that widget.

Container layout can be implemented in two ways (detailed in the "Layout and Sizing" section of the [Widget Development Guide](./widget.md)):

- Use existing framework layout classes, such as `setLayout(new FlexLayout())` in the constructor;
- Or override `layoutEvent()`, iterating through `children()` inside it to manually set the geometry of each sub-widget.

At the application layer, use it just like nesting child tags (here, `card-panel` is a container widget implemented and registered by the developer, and `text` is a built-in widget):

```xml
<card-panel>
  <text>Title</text>
  <progress-ring :value="progress"/>
</card-panel>
```

## A Complete Example

Below is the definition of a simple number display widget, registered as a framework component:

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

    Signal<int> valueChanged;            // Internal signal; application side listens via property name value

    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
    GX_PROPERTY(Color textColor, get textColor, set setTextColor)

protected:
    // Neither paintEvent nor sizeHint are virtual functions, do not add override
    void paintEvent(PaintEvent *event);
    Size sizeHint() const;

    // EventDispatch needs access to protected handler functions
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
    // Dispatch events to paintEvent; declaring PaintEvent allows compile-time checking for omissions
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
    p.setBrush(m_color);   // Text color is determined by the Brush, not the Pen
    p.setFont(Font(20));
    p.drawText(rect(), format("{}", m_value), AlignCenter);
}
```

Registration:

```cpp
kit.installWidget<NumberDisplay>();
```

Application-layer usage:

```xml
<number-display
  :value="count"
  text-color="#333333"
  @value="onCountChanged">
</number-display>
```

With this, the entire workflow from C++ implementation to application usage is complete: the `<number-display>` tag is converted to the registration name `NumberDisplay` by the ux tool and recognized.

Whenever the application data `count` changes, the `:value` binding calls `NumberDisplay::setValue()`; when the widget internally emits the `valueChanged` signal, the framework triggers an event named `value` (taking the event name from the property name), thereby invoking the application's `onCountChanged`. If you want bidirectional synchronization between `count` and the widget, you can use `::value="count"` instead.