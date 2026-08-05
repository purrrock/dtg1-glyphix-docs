# Object System

The C++ framework of Glyphix features an object model rooted in `PrimitiveObject`, which forms the foundation for subsequent development.

The object system consists of three complementary parts: the **Object Base Class Hierarchy** defines the common capabilities and lifecycle rules for all managed objects; the **Meta-Object System** uses a compile-time meta-compiler to generate metadata for C++ classes, endowing them with reflection, property binding, and JavaScript export capabilities; and the **Memory Safety Mechanism** solves the ubiquitous dangling pointer problem in GUI frameworks through guarded pointers and reference counting.

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

However, Glyphix works differently. When an application's page template writes `:value="progress"`, the reactive framework needs to find the property corresponding to the control by the string `"value"` at runtime, and automatically refresh when the data changes. This capability of a program to understand its own structure at runtime is called **Reflection**, which standard C++ does not support.

Glyphix's solution is to introduce a **Meta Compiler** into the build pipeline. It scans the source code before standard C++ compilation, generating metadata for classes that need to participate in the object system. Developers simply place the **`GX_OBJECT`** macro at the beginning of a class definition, and the meta compiler processes the class—after which the framework can read and write its properties or call methods by name, and access it from JavaScript.

You don't need to understand the internal workings of the meta-object system just yet. Just remember one rule: any class requiring reflection capabilities must include the `GX_OBJECT` macro in its definition and inherit from `PrimitiveObject` or `Object`.

## `PrimitiveObject` and `Object`

The framework's object system is divided into two tiers:

**`PrimitiveObject`** is the root base class for all **managed objects**. Classes inheriting from it gain framework capabilities such as property reflection, dynamic casting, and safe delayed destruction. However, `PrimitiveObject` itself **does not** have a parent-child tree structure—it is simply a "C++ object perceptible to the framework." Types like `AsyncSession` and `BindableObject` inherit from it because these classes do not need to form trees.

**`Object`** inherits from `PrimitiveObject` and adds a **parent-child tree structure**: a `parent` pointer is passed during construction, and when the parent object is destroyed, all child objects are also recursively destroyed. The Widget Tree is organized through this mechanism.

::: tip Analogy to Other Frameworks
If you have Qt development experience, you can analogize Glyphix's meta-object system to Qt's MOC system: `GX_OBJECT` corresponds to `Q_OBJECT`. However, there are many differences, such as Glyphix splitting the capabilities of Qt's `QObject` into two layers; `Signal` is also just a regular template class that does not rely on the meta-object compiler.

Other frameworks, such as Unreal Engine's UCLASS, have similar reflection systems.
:::

Choosing which base class to use depends on whether your class needs to be part of a tree:

```cpp
// Needs to participate in the object tree → inherit from Object
class MySensor : public Object {
    GX_OBJECT
public:
    explicit MySensor(Object *parent = nullptr) : Object(parent) {}
};

// Only needs framework awareness, does not participate in the tree → inherit from PrimitiveObject
class MyNetworkSession : public PrimitiveObject {
    GX_OBJECT_KINDS(ExplicitDeleteKind)
public:
    MyNetworkSession() = default;
};
```

`GX_OBJECT_KINDS(ExplicitDeleteKind)` in the code is an additional declaration. Like the `GX_OBJECT` macro, it declares the meta-object class, but informs the framework that the object's lifecycle is managed by the developer and will not be automatically reclaimed by JavaScript. Lifecycle-sensitive types like `AsyncSession` use this.

## Properties and Signals

The **`GX_PROPERTY`** macro is used to declare a framework-perceptible property, associating it with its getter and setter. Once declared, the property can be driven by the framework's reactive system—UI depending on it automatically refreshes when the value changes, and the animation system can interpolate it:

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

**`Signal<>`** is an event notification mechanism, declared directly as a class member. It is "emitted" when an event occurs, and other objects receive notifications by "connecting" to it ([lambda expressions](https://en.cppreference.com/w/cpp/language/lambda) are C++'s anonymous function syntax):

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
auto slot = make_slot([](int v) { /* Handle change */ });
myWidget->valueChanged.connect(slot);
```

::: tip Comparison with Qt's Signals and Slots
Qt's classic signals and slots mechanism requires MOC-generated code support, but `Signal<>` is a pure C++ template class that does not depend on the meta-object compiler. Therefore, you do not necessarily have to use `Signal<...>` objects in specific classes; you can use them anywhere.

Since `Signal` is a class, it consumes memory space (even when unconnected). Therefore, it is recommended to use event type enumerations and single signal member variables to save memory, rather than declaring a `Signal` member for every single event.
:::

### Complete Form of `GX_PROPERTY`

In addition to `get` / `set`, `GX_PROPERTY` supports declaring an associated change signal (`signal`), which is the standard interface for reactive frameworks to subscribe to property changes:

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

For properties with a declared `signal`, changes are automatically propagated through the reactive framework to JavaScript expressions bound to that property. This is the basis for two-way synchronization between control properties and application data.

The `signal` field in `GX_PROPERTY` does not depend on the parameter type of `Signal<T>`; the framework only cares whether it exists and when it is emitted. Conversely, the `get` field must be provided in this case to allow the framework to read property values on the JavaScript side.

## Guarded Pointers and Memory Safety

In GUI frameworks, asynchronous scenarios easily lead to dangling pointer crashes. A typical case:
```cpp
void onNetworkResponse(const String &data) {
    // Network request takes 2 seconds to return
    // But within these 2 seconds, the user may have exited the current page, and the label has been destroyed
    this->label->setText(data); // Segmentation Fault!
}
```
Timer callbacks, I/O callbacks, and all other asynchronous scenarios face the same risk. In scripted frameworks, such use cases are structurally unavoidable, so a safe lifecycle observation mechanism must be provided.

### `Pointer<T>` Guarded Pointers

Glyphix builds weak reference counting support into all derived classes of `PrimitiveObject`. Use `Pointer<T>` to hold non-owning cross-object references. When the target object is destroyed, `Pointer<T>` is automatically set to null, and you can safely use it by checking before dereferencing:

```cpp
Pointer<Label> m_label; // Declare as member variable

// ...Assign after construction...
m_label = label;

// In any asynchronous callback that might cause the label to be destroyed:
void onNetworkResponse(const String &data) {
    if (!m_label)
        return; // Label has been destroyed, safely exit
    m_label->setText(data); // Access is safe here
}
```

::: tip When to Use
Use `Pointer<T>` instead of raw pointers `T *` to track lifecycles when holding pointers across objects without owning their lifecycles. `Signal`'s `connect` mechanism also relies on guarded pointers—when the receiver (the object containing the slot) is destroyed, the connection is automatically severed, preventing dangling callbacks.
:::

### Thread Limitations
Guarded pointers do not support cross-thread access; they are essentially limited to use on the UI thread. Furthermore, they are not zero-cost abstractions, as every construction involves reference counting operations.

### `SharedRef<T>` Intrusive Reference Counting

For ordinary value objects that do not inherit from `PrimitiveObject` (such as custom data structures), the framework provides intrusive shared reference counting. Make the value type inherit from `SharedValue`, and then hold it with `SharedRef<T>` to obtain shared semantics similar to [`std::shared_ptr`](https://en.cppreference.com/w/cpp/memory/shared_ptr) while avoiding additional control block allocations:

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

`SharedRef` also supports Copy-On-Write (COW) semantics: before modifying a copied version, an independent copy is created to ensure multiple holders do not interfere with each other. This mechanism uses atomic reference counting to achieve thread safety.

## Dynamic Type Casting

Standard C++'s [`dynamic_cast`](https://en.cppreference.com/w/cpp/language/dynamic_cast) relies on RTTI (Run-Time Type Information), whereas embedded environments are typically compiled with `-fno-rtti`. `dyn_cast` leverages the meta-object system to provide equivalent runtime-safe downcasting capabilities.

The target type `T` of `dyn_cast<T *>()` must satisfy two conditions:
1. Inherit from `PrimitiveObject`
2. Declare the `GX_OBJECT`/`GX_OBJECT_KINDS` macro

```cpp
PrimitiveObject *obj = getSomeObject();

// Safe downcasting; returns nullptr if casting fails
auto *btn = dyn_cast<Button *>(obj);
if (btn)
    btn->setText("OK");

// Const versions are also supported
const auto *constBtn = dyn_cast<const Button *>(obj);
```

::: warning `GX_OBJECT` is a Prerequisite
`dyn_cast`'s type checking relies on the target class's static meta-object information (`staticMetaObject`). If the target class does not declare `GX_OBJECT`, it lacks the necessary runtime type information, resulting in a compilation error.
:::

`dyn_cast` is particularly commonly used in Native Module development: the framework frequently passes objects in as base class pointers (`PrimitiveObject *` or `Object *`), requiring `dyn_cast` to safely restore them to concrete types before operating on them.

Considering that sandbox security policies do not trust objects passed from scripts, we cannot assume that runtime object pointers passed in are of the correct type, and therefore must use `dyn_cast` to verify types and safely access their members.

### Memory Leak Traps

A typical `dyn_cast` usage pattern implies a risk of memory leaks, such as:
```cpp
auto *session = dyn_cast<Session *>(takeObjectOwnership());
if (session) {
    // Successfully cast, access session members and transfer ownership
}
```
The problem is that if the object returned by `takeObjectOwnership()` is not of type `Session`, `dyn_cast` returns `nullptr`, but ownership of the original object has already been transferred—leading to a memory leak if no other mechanism reclaims the object.

When developing Native Module APIs, you may occasionally encounter this issue, and related frameworks provide better APIs to avoid it. However, developers should be aware of this potential risk and not be misled by the safety of `dyn_cast`.

### Is `GX_OBJECT` Necessary?

Not all classes inheriting from `PrimitiveObject` require `GX_OBJECT`. The purpose of the `GX_OBJECT` macro is to register the class with the meta-object system, enabling capabilities such as reflection, property binding, and `dyn_cast`. If your class:

- Does not need to be exposed to JavaScript
- Does not require reflection mechanisms like `GX_PROPERTY` or `GX_METHOD`
- Does not need to be safely cast via `dyn_cast`

Then you can omit `GX_OBJECT`, simply inheriting from the base class and using C++ features normally:

```cpp
// Internal helper class requiring no meta-object capabilities, omit GX_OBJECT
class InternalBufferManager : public PrimitiveObject {
public:
    explicit InternalBufferManager() = default;
    void flush();
private:
    // ...
};
```

Classes omitting `GX_OBJECT` still retain the basic capabilities of `PrimitiveObject`, including `deleteLater()` and guarded pointer support, but lose reflection and dynamic type recognition capabilities.

Another scenario is when your final type requires meta-object capabilities, but certain intermediate base classes do not; in this case, the intermediate base classes can omit `GX_OBJECT`. This loses some runtime type information but reduces code size.

::: tip
If you are unsure whether you need `GX_OBJECT`, it is generally recommended to conservatively include it.
:::

One final important difference: once marked with `GX_OBJECT`, the class must be located in a header file (`*.h`) and registered with the build system using the `glyphix_add_meta_objects()` CMake macro. Classes without `GX_OBJECT` have no such requirement and can be defined directly in `.cpp` files.

## Runtime Type System

Throughout all previous discussions of `GX_PROPERTY`, one question remained unanswered:

```cpp
GX_PROPERTY(int value, get value, set setValue)
```

How does JavaScript know what an `int` is? When `widget.value = 42` is written on the JavaScript side, `42` is JavaScript's `number` type, whereas `setValue(int v)` accepts a C++ `int`. What happens in between? Conversely, how does the `int` returned by `getValue()` become a `number` in JavaScript?

Without any glue code, the framework obviously needs to do some work behind the scenes to bridge C++ static types and dynamic script types. This is a fairly transparent process, and this section explains what happens in the middle.

### The General-Purpose Type Container `Variant`

The answer lies in `Variant`. It is a type-erased container capable of holding values of arbitrary types, serving as the core bridge connecting C++'s static type system with JavaScript's dynamic types.

Whenever the framework needs to cross this boundary, it goes through `Variant`:

1. **Property Read/Write Intermediate Layer**: When properties declared with `GX_PROPERTY` are read and written via reflection APIs, values are passed via `Variant`. The framework converts JavaScript's `JsValue` into a `Variant`, which is then converted by `Variant` into the actual argument type of the C++ setter; the direction is reversed when reading.
2. **Method Call Argument Marshaling**: Parameters and return values of `GX_METHOD` are represented via `Variant` before being passed to C++ .

```cpp
Variant v1;                  // Empty value (null)
Variant v2{42};              // Stores int
Variant v3{3.14};            // Stores double
Variant v4{String("Hello")}; // Stores String
// Variant must be explicitly constructed, implicit conversion is not supported
// Variant v5 = 42; // Error, must write Variant v5{42};

// Type checking
if (v2.is<int>()) { /* ... */ }
// Checking convertibility is not recommended; instead, directly to<T>() and check if it's an invalid value
if (v3.convertible<double>()) { /* ... */ }

// Read by reference (fastest, requires exact type match)
int n = v2.as<int>();
// Read by reference, returns default value on type mismatch
double d = v2.as<double>(0.0); // int != double, returns 0.0
// Read with type conversion (by value)
int fromDouble = v3.to<int>();   // 3.14 -> 3
String fromInt = v2.to<String>(); // 42 -> "42"
```

::: tip
This is not C++17's [`std::variant`](https://en.cppreference.com/w/cpp/utility/variant), but rather closer to [`std::any`](https://en.cppreference.com/w/cpp/utility/any) with support for runtime type identification and automatic type conversion.

Generally, you do not need to directly manipulate `Variant` in business code; the framework automatically handles all conversions. You will only interact with it directly when implementing low-level framework extensions, writing general utility functions, or needing to manipulate runtime reflection APIs directly.
:::

### Built-in Type Mappings

The framework has built-in bidirectional mappings to JavaScript for common C++ primitive types:

| C++ Type | JavaScript Type | Remarks |
|:---:|:---:|:---:|
| `int`, `float`, `double`, etc. | `number` | Numerical types mapped directly |
| `bool` | `boolean` | |
| `String` | `string` | |
| Subclasses of `PrimitiveObject *` | JavaScript object reference | Object lifecycle managed by framework |
| Value types like `Color`, `Length` | `string` | Represented via specifically formatted strings |

This is why after writing `GX_PROPERTY(int value, ...)`, the JS side can directly do `widget.value = 42`: `int` is in the built-in mapping table, and the framework knows how to convert the type.

::: note Do Not Use C-Strings
`Variant` requires the stored type `T` to have ownership, so non-owning types such as C-strings (`const char *`) and string views (`String::View`) cannot be stored in `Variant`. Always use `String` to represent text data, and explicitly convert to `String` before storing in `Variant` when necessary.

Using an unsupported string type will result in a compilation error.
:::

::: important
The built-in type mapping table does not register `std::string`-related mappings, so storing `std::string` in `Variant` is also not recommended. Unmapped types can be stored normally, but they will be treated as opaque C++ objects and cannot be used in JavaScript.
:::

### Complex Type Reflection

For classes declared using `GX_OBJECT`, you can also utilize `GX_ENUM` and `GX_STRUCT` to export enumeration and structure member types, allowing them to be used naturally in JavaScript as well. This type export is automatic and requires no manual writing of additional binding code.

#### Enumeration Reflection `GX_ENUM`

When a property or method parameter type is a C++ enumeration, exposing it to JavaScript directly as an integer is neither intuitive nor error-prone. `GX_ENUM` exports enumerations as string constants, allowing JavaScript to operate using readable strings rather than magic numbers:

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

`GX_ENUM` is placed after the `enum` keyword, telling the meta compiler that this enumeration needs to be exported. `GX_ALIAS("...")` specifies a JavaScript-visible string name for each enumeration member—if omitted, the original name of the C++ member is used by default. Application developers use this in JavaScript as follows:

```js
scroll.indicator = "hidden"; // Corresponds to RemoveScrollBar
scroll.indicator = "dots";   // Corresponds to DotsScrollBar
```

When reading the `indicator` property, the framework converts the string `"dots"` into the `DotsScrollBar` enumeration value before passing it to the setter; when reading, it converts the enumeration value back to a string. The entire process is completely transparent to the C++ side, which always operates on concrete enumeration types.

#### Structure Parameter Reflection `GX_STRUCT`

For method parameters, an operation sometimes requires multiple related configuration options. In such cases, parameters can be encapsulated into structures and exported with `GX_STRUCT`, allowing the JavaScript side to pass an object literal:

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

`GX_STRUCT` is placed after the `struct` keyword, and each field of the structure is automatically exported according to its type (again via built-in type mappings or nested `GX_ENUM`s). Objects can be passed directly on the JS side:

```js
scroll.scrollTo({ left: 0, top: 200, behavior: "smooth" });
scroll.setIndex({ index: 3, behavior: "instant" });
```

The `scrollTo` method on the C++ side always receives strongly typed `ScrollOptions` objects, requiring no parsing whatsoever on the C++ side.

::: warning Do Not Forget Annotations
When declaring `GX_PROPERTY` or `GX_METHOD`, if the related type is a custom enumeration or structure, make sure to correctly annotate it with `GX_ENUM` or `GX_STRUCT`. Otherwise, these properties or methods cannot be used on the JavaScript side, and no compilation error prompts will be given.
:::

### Is There an "Intermediate Representation"?

When using `Variant` to bridge C++ and JavaScript, does the framework convert JavaScript objects into a general intermediate representation, such as some JSON-like serialized structure?

The answer is no. `Variant` directly stores C++ objects (including `JsValue`), which includes all type information and operation semantics of the object. The system correctly performs type conversions and method invocations based on the runtime type tags of the `Variant` value, without requiring a specific intermediate representation or serialization process.