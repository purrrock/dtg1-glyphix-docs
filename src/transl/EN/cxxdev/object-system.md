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