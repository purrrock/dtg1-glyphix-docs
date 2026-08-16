# Context File: 04_glyphix_CxxDev_EN.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/transl/EN/cxxdev/native-module.md

# Native Module Development

A Native Module is the bridge connecting C++ and application-layer JavaScript code. Whenever you need to expose system capabilities to the application—such as reading sensor data, calling third-party SDKs, or accessing system features—you need to write a Native Module.

The Glyphix framework has already implemented numerous built-in modules through this mechanism, such as the File System (`@system.file`) and Router (`@system.router`). You can use the exact same approach to add custom capabilities to your own device.

The diagram below illustrates the position of a Native Module within the framework: it sits at the reactive framework layer, bridging upwards to JavaScript applications via the JsVM bridge layer to provide system APIs, and calling downwards into the C++ core framework or platform adaptation layer:

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

Writing a Native Module requires three sets of concepts: the **JsVM Bridge Layer** provides type conversion and function invocation capabilities between C++ and JavaScript; **Module Registration Macros** assemble C++ code into modules that can be `import`ed by JavaScript; and the **Applet Sandbox** provides application-level context and resource lifecycle management for the module. This chapter unfolds step by step in this order.

::: warning Security Risks
When you plan to develop "system-level extensions" for Glyphix, do not overlook the fact that this also implies high security risks. Even a slight carelessness may introduce vulnerabilities, allowing malicious applications to exploit these capabilities to attack the system or other applications. Please be sure to follow secure coding standards, restrict module permissions and access scopes, and conduct thorough security testing.
:::

## JsVM Bridge Layer

Before writing specific modules, you need to understand the interaction tools between C++ and JavaScript. The JsVM bridge layer is the infrastructure of the entire Native Module, providing the `JsValue` type system and the `JsCallContext` invocation context, enabling C++ code to create, read, and manipulate JavaScript values.

### `JsValue` Type System

`JsValue` is the C++ type in the framework representing JavaScript values, covering all basic JavaScript types. It uses reference counting to manage its lifecycle and can be directly assigned and copied like C++ value types such as `int` and `String`.

Creating JavaScript values from C++:

```cpp
JsValue undefined;               // undefined
JsValue boolVal{true};           // boolean
JsValue intVal{42};              // number (integer)
JsValue floatVal{3.14};          // number (float)
JsValue strVal{"hello"};         // string
```

These constructors are all implicit, so module functions can directly `return "hello"` or `return 42` without manual wrapping.

When reading C++ values from a `JsValue`, use the `as*` series of methods. They return specified default values when types do not match, avoiding manual type checking:

```cpp
int    count  = value.asInt(0);       // Returns 0 if not a number
double ratio  = value.asNumber(1.0);  // Returns 1.0 if not a number
String label  = value.asString();     // Returns an empty string if not a string
```

If you need to perform forced type conversion according to JavaScript semantics (such as converting any value to a boolean), use the `to*` series of methods:

```cpp
bool   enable = value.toBoolean();    // Any value can be converted to bool
int    num    = value.toInt();        // Converted to an integer according to ECMAScript specs
String str    = value.toString();     // Converted to a string according to ECMAScript specs
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
    // Always check the parameter count first, then validate the type, otherwise ctx.arg(0) might go out of bounds
    if (ctx.argc() < 1 || !ctx.arg(0).isNumber())
        return JsValue();  // Invalid parameter, return undefined

    int level = ctx.arg(0).asInt(0);
    level = std::max(0, std::min(100, level));
    audioSetVolume(level);
    return JsValue(true);  // Return success flag
}
```

Many built-in module functions receive an object parameter. This is a flexible convention that allows parameters to have default values and facilitates future extensions:

```js
// JavaScript side invocation
setConfig({ brightness: 80, contrast: 50 })
```

Read object properties on the C++ side using `operator[]`:

```cpp
static JsValue setConfig(JsCtx ctx) {
    if (ctx.argc() < 1) return {}; // Remember to check the parameter count

    JsValue params = ctx.arg(0);
    int brightness = params["brightness"].asInt(100);
    int contrast   = params["contrast"].asInt(50);
    // ...
    return {}; // Return undefined
}
```

### Exporting Functions as `JsValue`

Module functions do not have to be named static functions. `JsValue` can be constructed from any callable object: **capturing-free lambdas** are automatically resolved to function pointers with efficiency equivalent to named functions; **capturing lambdas** are wrapped as callable objects, making them suitable for enclosing module-level runtime state inside factory functions:

```cpp
static JsValue createMathModule(JsVM &vm) {
    JsValue mod = vm.newObject();

    // Capturing-free lambda: automatically decays to a function pointer with zero extra overhead
    mod["double"] = +[](JsCtx ctx) -> JsValue {
        return ctx.arg(0).asInt(0) * 2;
    };

    // Capturing lambda: reads configuration once during module creation and uses it directly in subsequent calls
    int factor = readScaleFactorFromConfig();
    mod["scale"] = [factor](JsCtx ctx) -> JsValue {
        return ctx.arg(0).asInt(0) * factor;
    };

    return mod;
}
```

The advantage of the lambda form is that related logic can be written close to the factory function, avoiding a large number of short, named functions scattered across files. For logic that is simple and does not need to be reused on the C++ side, lambdas are recommended.

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

If a module function encounters an error, you can throw a JavaScript exception via `JsVM::newError()`:

```cpp
static JsValue setConfig(JsCtx ctx) {
    if (ctx.argc() < 1)
        return ctx.vm().newError("missing parameters");
    // ...
}
```

However, we generally do not use exceptions in simple scenarios such as parameter checks, because exception message text consumes code size. For non-critical errors, returning `undefined` or `false` is usually more appropriate.

### Function Interoperability

If you need to proactively execute JavaScript functions or object methods within C++, you can use `JsValue::call()` or `callMethod()`. This is as simple as directly calling JavaScript functions in C++, passing parameters via initializer lists and obtaining return values:

```cpp
static JsValue printDemo(JsCtx ctx) {
    JsVM &vm = ctx.vm();
    JsValue obj = vm.newObject();
    obj["value"] = 42;
    
    // Call a method on the console object, equivalent to console.log("Object is:", obj) in JS
    auto result = vm.globalObject()["console"]
                    .callMethod("log", {"Object is:", obj});
    
    // print() can be used to directly output the content of a JsValue to the console for debugging
    result.print(); // undefined 
    
    // If you only care about the execution process without needing a return value, and want to print a warning if an error occurs:
    result.reportError(); // Returns a bool value indicating whether an exception occurred
    
    return {}; // Return undefined
}
```

If you are calling an independent function object passed in as an argument (rather than a method attached to an object), you need to use `call()` and specify the `this` binding object, which is usually the global object `globalObject()`:

```cpp
static JsValue doMathAndCallback(JsCtx ctx) {
    if (ctx.argc() < 1 || !ctx.arg(0).isFunction()) return JsValue();
    
    auto &callback = ctx.arg(0); // References can be used here to avoid reference counting overhead
    // This is the this object during JS function calling; {} is equivalent to undefined
    JsValue thisObj = ctx.vm().globalObject();
    // Equivalent to callback.call(globalThis, 10, 20) in JS
    JsValue result = callback.call(thisObj, { 10, 20 });
    
    return result;
}
```

::: warning Dangerous Anti-Pattern: Asynchronous Callback Leaks
If your original intention is to store a `callback` passed from JavaScript long-term, such as passing it to underlying hardware to subscribe to events, please be very careful:

```cpp
// ❌ Incorrect usage: leads to memory leaks!
static JsValue onButtonPress(JsCtx ctx) {
    auto callback = callback = ctx.arg(0);
    // Directly getting the JavaScript callback from arguments and capturing it in a lambda, passing it to the underlying driver
    HardwareButton::onPress([callback]() mutable {
        callback.call({}, {...});
    });
    return {};
}
```

This is a classic **severe trap**: `JsValue` has a lifecycle management based on reference counting. Once this closure is persistently held by the underlying driver along with global state without providing a clear unsubscription mechanism (such as a corresponding `offPress` method to unbind), this JavaScript callback and the entire application sandbox context it binds to will be **permanently leaked**!

To implement long-lifecycle callbacks across event loops (such as event subscriptions), you must combine the lifecycle mechanism of the **Applet Sandbox** to manage C++ objects and safely unbind them when no longer needed, or directly use dedicated `AsyncSession` facilities (refer to [Asynchronous Feature Development](./async.md)).
:::

For more complex asynchronous scenarios (such as needing to return a Promise or requiring multiple callbacks), please refer to [Asynchronous Feature Development](./async).

::: tip Complete API Reference
This section only covers the most commonly used capabilities of the JsVM bridge layer. `JsVM` and `JsValue` also provide many interfaces not covered in this section, such as JSON parsing and serialization (`parseJSON()`, `stringifyJSON()`), property enumeration (`properties()`), Promise operations (`newPromise()`, `promiseResolve()`/`promiseReject()`), and direct execution of JS code (`eval()`, `importModule()`), etc. For complete interface descriptions, please refer to the API documentation distributed with the SDK.
:::

### Exporting C++ Objects

Previous examples all "returned basic types or ordinary JavaScript objects from functions," which is essentially manipulating JavaScript via C++ APIs. However, sometimes you need to **export a C++ object to JavaScript** so that scripts can continue to manipulate the same underlying instance subsequently.

There are a few different implementation approaches:

- **`vm.newMetaObject(object)`**: The most straightforward, automatically exposes `GX_PROPERTY` / `GX_METHOD` to JavaScript;
- **`vm.newObject(object)` + manual function attachment**: Closer to "ordinary JS objects with native handles";
- **`vm.newProxy()`**: The most flexible, but property interception logic is scattered and maintenance costs are highest.

In most business scenarios, using `newMetaObject()` is recommended first. Only when you explicitly need to write a JavaScript shape by hand, or need to intercept highly dynamic property accesses, should you consider the other two methods.

#### Exporting via `newMetaObject()`

This is the simplest approach. First, define a native object type, and then directly wrap it into a reflectable JavaScript object.

The following example exports a read-write counter object. It must inherit from `PrimitiveObject` and be declared to the meta-object system using `GX_OBJECT`:

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
Functions marked with `GX_METHOD` can have any `Variant` hostable type parameters and return values that can be converted to and from `JsValue`, and can be references. For example: `int`, `const String &`, etc.

Remember, `JsValue` itself can also be used.
:::

Then export this "constructor" in the module factory function:

```cpp
static JsValue createCounterModule(JsVM &vm) {
    JsValue mod = vm.newObject();
    mod["createCounter"] = NativeCounter::constructor;
    return mod;
}
```

Used on the JavaScript side like this:

```js
import counter from '@vendor.counter'

const c = counter.createCounter(10)
console.log(c.value) // 10
c.value = 42
c.reset()
console.log(c.value) // 0
```

Here `c` looks like an ordinary JavaScript object, but underneath it actually corresponds to a `NativeCounter` instance. Thanks to `newMetaObject()`, JavaScript can directly read and write properties declared with `GX_PROPERTY` and call methods exposed by `GX_METHOD`.

If you only need to "naturally expose a C++ object as a JavaScript object" (including properties and methods), doing this is usually sufficient.

#### Handling Applet Context

`newMetaObject()` has a common limitation: `GX_METHOD`s exported through the meta-object system are ordinary C++ member functions, meaning they cannot access `JsCtx` / `JsCallContext` and therefore cannot directly write `Applet::current(ctx.vm())` like module functions do.

If your object methods need to access the current application context, for example:

- Resolving application private URIs;
- Reading application permissions or configurations;
- Binding other resources to the current sandbox inside object methods;

Then a more appropriate approach is to make this object inherit from `BindableObject`, binding it to the current `Applet` when the object is created. This allows subsequent `GX_METHOD`s to directly access the host application via `applet()`.

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
Do not actually implement features like `resolvedUri()` that directly expose underlying resource paths; this is merely an example. In actual development, please make sure to perform permission checks and access controls to avoid leaking sensitive information to the JavaScript side.
:::

Used on the JavaScript side, it is indistinguishable from ordinary `newMetaObject()` objects:

```js
const file = native.createFile('internal://files/config.json')
console.log(file.resolvedUri())
```

In this example, `resolvedUri()` has no `JsCtx` parameter, but it can still access `applet()` because the object was bound to the current application upon creation.

::: warning Two Prerequisites for `BindableObject`
Pay extra attention to two points when using `BindableObject`:

- `BindableObject` comes with `ExplicitDeleteKind` by default. This means it **will not** be automatically destroyed when the JavaScript object is garbage collected. If you want it to revert to ordinary Native Object GC behavior, you can override this default value using `GX_OBJECT_KINDS(NoneKind)` as shown in the example above.
- `BindableObject` must be bound to an `Applet`, otherwise `applet()` will forever be a null pointer, and context will be out of the question. The simplest approach is to call `BindableObject(applet)` in the constructor, or bind it to the current `Applet` immediately after creation.
:::

::: important Legacy Behavior
Prior to the v0.8.0 official release, the behavior of `PrimitiveObject::objectKinds()` differed from this document; please do not refer to implementation details of older versions.
:::

`BindableObject` is not a replacement for [`newMetaObject()` exports](#exporting-via-newmetaobject), but a specialized solution for "when object methods need to remember their owning application context." Only introduce this concept when you genuinely need to access `Applet` inside a `GX_METHOD`.

#### Exporting Methods Manually via `newObject()`

Sometimes you do not want to expose the entire meta-object interface, but simply want to attach a C++ object as an opaque handle to a JavaScript object, manually deciding which methods can be called. In this case, you can use `vm.newObject()` to export the object.

With this approach, `GX_PROPERTY` and `GX_METHOD` are **not** automatically exposed, so you need to attach methods to the object yourself:

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

The characteristic of this writing style is: the shape of the JavaScript API is entirely up to you, but inside each method, you must retrieve the underlying C++ pointer from the `this` object yourself and check the type using `dyn_cast`. Compared to `newMetaObject()`, there is more boilerplate code and it is easier to miss checks.

However, it also has one direct advantage: these manually attached functions are essentially ordinary `JsCtx` callbacks, so they can directly obtain the current application context via `Applet::current(ctx.vm())` just like module functions. This is also an important distinction from `GX_METHOD`.

This method cannot export property accessors (getters/setters), but can only export fixed property values.

#### Exporting Objects Using `newProxy()`

If you need to take over property reading/writing, method searching, lazy generation of fields, and other behaviors entirely, you can also use `vm.newProxy()`. This approach can implement highly dynamic interfaces, such as forwarding arbitrary property access to an underlying dictionary, generating sub-objects on demand, or intercepting writes for validation.

However, it also comes with obvious costs:

- The behaviors of reading properties, writing properties, and method calls are scattered across the proxy logic;
- The API shape is no longer directly expressed by class definitions like `newMetaObject()`;
- Once behaviors become complex, troubleshooting issues becomes cumbersome.

Therefore, `newProxy()` is more suitable for a small number of highly dynamic bridging scenarios rather than replacing routine object exports.

#### Lifecycle Rules

The destruction rules for Native Objects are not determined solely by `newMetaObject()`, but rather by the `objectKinds()` of the C++ object:

- If the object includes `RootKind` and **does not** have `ExplicitDeleteKind`, then when the corresponding JavaScript object is garbage collected, the C++ object will also be automatically destroyed;
- If the object is a child node of another object or has declared `ExplicitDeleteKind`, its lifecycle remains managed by the C++ side.

For most "standalone wrapped objects," directly inheriting from `PrimitiveObject` without additionally declaring `ExplicitDeleteKind` will usually yield the appropriate default behavior, which is automatic destruction upon GC.

If you are not familiar with these object lifecycle flags, it is recommended to read the chapter on `PrimitiveObject` in the [Object System](./object-system.md) first, before deciding whether to hand the object over to JavaScript GC management.

#### Retrieving Native Objects from `JsValue`

Sometimes another Native Module function receives this object as a parameter, at which point the underlying C++ pointer can be temporarily retrieved from `JsValue`:

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

`object()` provides **temporary access only** and does not transfer ownership. If you genuinely need to "take away" the object from the JavaScript side, you should use the templated form `moveObject<T>()`:

```cpp
auto *counter = value.moveObject<NativeCounter>();
```

**Do not** write it in the following form:

```cpp
auto *counter = dyn_cast<NativeCounter *>(value.moveObject());
```

Once the types do not match, this code will lose object ownership after a failed cast, causing a leak. The API documentation also explicitly recommends prioritizing `moveObject<T>()`, combining "type checking" and "ownership transfer" into a single step.

::: warning When NOT to Export Native Objects
If you only want to return a simple result data structure, such as device information, a one-time calculation result, or a configuration snapshot, prioritize returning ordinary JavaScript objects constructed via `newObject()`. Only when JavaScript needs to continuously manipulate the same C++ instance subsequently is it worth introducing a Native Object.
:::

## Module Definition and Registration

Having mastered the basic tools of the JsVM bridge layer, you can now assemble C++ functions into a complete Native Module. A module consists of two parts: a **factory function**, responsible for creating the module object and attaching C++ functions to it; and a **registration macro**, responsible for registering the factory function into the framework's module system.

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

// Factory function: builds the module object and returns it
static JsValue createDeviceModule(JsVM &vm) {
    JsValue mod = vm.newObject();
    mod["getDeviceName"] = getDeviceName;
    mod["getBatteryLevel"] = getBatteryLevel;
    return mod;
}

// Register the module so it is accessible in JavaScript via the @vendor.device path
GX_JSVM_MODULE(vendor_device, "vendor.device", createDeviceModule)
```

The `GX_JSVM_MODULE` macro accepts three parameters: the C++ variable name, the JavaScript module path (excluding the `@` prefix), and the factory function. The factory function is called when the module is first `import`ed, and the returned `JsValue` object is what the JavaScript side receives.

On the JavaScript side, applications use this module as follows:

```js
import device from '@vendor.device'

const name = device.getDeviceName()
const battery = device.getBatteryLevel()
```

::: tip This is a Demo!
This looks quite simple, except it overlooks a major issue: most APIs are asynchronous! We should not be reading battery levels in the JavaScript execution context—meaning the UI thread—unless we are truly building a demo. For asynchronous APIs, please refer to the [Asynchronous Feature Development](./async.md) chapter, which provides more appropriate patterns and examples.
:::

### Enabling Modules

Simply declaring a module is not enough; it also needs to be "installed" into the JavaScript engine during framework initialization. This is accomplished via the `GX_JSVM_MODULE_IMPORT` macro:

```cpp
GX_JSVM_MODULE_IMPORT(vendor_device)
```

`GX_JSVM_MODULE` declares a global variable at file scope, and `GX_JSVM_MODULE_IMPORT` finds and invokes that variable's `install()` method. The name parameters (the first parameter) of both macros must match.

A common practice is to centralize all `GX_JSVM_MODULE_IMPORT` calls into a single function for easy management:

```cpp
void installVendorModules() {
    GX_JSVM_MODULE_IMPORT(vendor_device)
    GX_JSVM_MODULE_IMPORT(vendor_sensor)
    GX_JSVM_MODULE_IMPORT(vendor_bluetooth)
}
```

Call `installVendorModules()` after `AppletKit` initializes to ensure modules are available when the application starts.

## Library Loader

Native Modules are suitable for implementing framework-level system APIs universally available to all applications. However, for **non-standard system customization features**, such as vendor-exclusive data access, private SDK encapsulations, or capabilities open only to specific authorized applications, the **Library Loader** mechanism is strongly recommended.

Library Loaders are loaded by name using the [`loadLibrary()`](/api/system-app.md#loadlibrary) method provided by the `@system.app` module:

```js
import app from '@system.app'

const lib = app.loadLibrary('custom-library')
lib.someFunction()
```

Compared to Native Modules, Library Loaders have two distinct advantages:

- **No Global Registration Required**: They do not rely on the `GX_JSVM_MODULE` and `GX_JSVM_MODULE_IMPORT` macros; module objects are created on-demand when invoked;
- **Easy Simulator Fallback**: The application side can detect whether the return value of `loadLibrary()` is `undefined`, gracefully downgrading to a script-implemented stub in generic simulator environments, whereas stubbing module imports like `import lib from '...'` is hacky and anti-pattern.

```js
import app from '@system.app'

// Attempt to load the native library, falling back to a script stub in the simulator
const nativeLib = app.loadLibrary('custom-library')
const lib = nativeLib || {
    someFunction() { /* Simulator implementation */ }
}
```

Except for registration methods and usage on the JavaScript side, Library Loaders are otherwise identical to Native Modules.

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

`setLibraryLoader()` can be called after `AppletKit` initializes; there is no need to re-register it every time an application starts.

Since the Library Loader's loader receives an `Applet *`, it can perform **application permission verification** right at the entry point, denying features to unauthorized applications without repeatedly checking inside every module function:

```cpp
AppletKit::instance()->setLibraryLoader(
    "custom-library",
    [](Applet *applet) -> JsValue {
        // Permission check: uniformly intercept unauthorized access at the entry point
        if (!applet || !applet->permission(vendor::Permission::AccessCustomLib))
            return vm.newError("permissions denied"); // Returns undefined

        JsVM &vm = JsVM::current();
        JsValue lib = vm.newObject();
        lib["someFunction"] = getDeviceName;
        return lib;
    }
);
```

If the loader returns `undefined` (i.e., a default-constructed `JsValue()`), `app.loadLibrary()` also yields `undefined` on the JavaScript side, allowing the application to perform fallback processing accordingly.

::: tip
It is not recommended for loader functions to throw exceptions when permission checks fail; instead, returning `undefined` by default is preferred. Besides allowing the JavaScript side to gracefully downgrade, this also prevents leaking information about the module's existence (if you do not want unauthorized apps to know the library exists).
:::

## Collaborating with Application Sandboxes

The module functions introduced in previous sections are stateless—they receive parameters, return results, and hold no context. However, many real-world scenarios require modules to interact with the currently running application: reading application resource paths or language settings, or hosting a long-lived C++ object within the application sandbox. This requires capabilities provided by `Applet`.

### Obtaining the Current Application Context

Use `Applet::current()` to obtain the application instance belonging to the caller:

```cpp
#include "gx_applet.h"

static JsValue readPreference(JsCtx ctx) {
    auto applet = Applet::current(ctx.vm());
    // Since subsequent operations depend on applet, make sure to check if the context was successfully retrieved
    if (!applet) return JsValue();

    // Read application-private storage paths
    String storagePath = applet->resolveUri("internal://files/preferences.json");
    // ...
}
```

`Applet` instances are automatically managed by the framework, with each application running in its own independent JavaScript Realm. `Applet::current()` derives the corresponding application instance through the current Realm, meaning that when the same module function is called in different applications, each obtains its own independent context.

### Resource Lifecycle Management

If a module function needs to allocate a long-lived C++ object (such as a background task continuously listening to hardware status), **never** use global variables or raw pointers to hold resources across calls—this allows resources to escape application sandbox tracking, causing both memory leaks when applications exit and the loss of critical security guarantees provided by the sandbox.

A serious security requirement exists here: **Native Modules must guarantee that all access paths to C++ objects undergo strict ownership and type validation**, rather than merely providing a "legal path" that leaves open possibilities to bypass it. The correct way to achieve this is to completely delegate object lifecycle management to the `Applet` sandbox, and **compulsorily** use `takeObject<T>()` for validation in **every** module function that receives integer handles—this is an indispensable invariant, as expanded below.

The following uses continuous sensor state monitoring as an example to demonstrate this secure lifecycle-binding mechanism.

::: tip
The code in this section is essentially a crude substitute for the `AsyncSession` principle covered in the [Asynchronous Feature Development](./async.md) chapter, used solely for concept demonstration. In actual business development, it is strongly recommended to directly use mature `AsyncSession`-related facilities to handle asynchronous tasks, which are also built on top of the methods introduced in this section under the hood.
:::

Suppose we have a sensor. The application needs to start listening upon initialization, subsequently read the latest data multiple times, and manually stop listening when no longer needed. First, we define the carrier of this background task:

```cpp
class SensorListener : public PrimitiveObject {
    GX_OBJECT
public:
    SensorListener() {
        // Start the sensor, requesting underlying driver hardware resources...
    }
    ~SensorListener() override {
        // Stop the sensor, releasing related hardware resources...
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

    // Return the ID to JavaScript as the unique credential for subsequent operations on this object
    return bindId;
}
```

Because the object is now **managed** by the sandbox, even if the application exits midway or is forcibly killed by the system, the sandbox will automatically clean up all bound objects upon destruction, thereby preventing resource leaks.

#### Safely Retrieving Objects

When the JavaScript side needs to operate on a previously created object, it **must** retrieve the instance via `Applet::takeObject<T>()` based on the handle, rather than performing any form of "raw casting":

```cpp
static JsValue readSensor(JsCtx ctx) {
    auto applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1) return {};

    int bindId = ctx.arg(0).asInt();
    auto *listener = applet->takeObject<SensorListener>(bindId);
    if (!listener) return {}; // Returns nullptr if ID is invalid or types mismatch

    return listener->latestValue();
}
```

`applet->takeObject<T>()` only accesses IDs belonging to the **current sandbox** (preventing cross-app unauthorized access), and then verifies **type matching** via object metadata. A non-null pointer is returned only if both layers pass.

::: danger Must Access Objects via `takeObject<T>()`
Integer IDs originating from JavaScript are completely untrustworthy on the C++ side—they could be forged or expired references. Lacking validation leads to severe security vulnerabilities:

```cpp
// ❌ Absolutely do not do this!
static JsValue readSensor(JsCtx ctx) {
    auto bindId = ctx.arg(0).asInt();
    // Using only the non-templated takeObject + static_cast bypasses type checking and sandbox boundary checks
    auto *binded = applet->takeObject(bindId);
    // Dangerous: static_cast has no runtime checks; 'binded' here might not be a SensorListener at all!
    auto *listener = static_cast<SensorListener *>(binded);
    return listener->latestValue(); // Can lead to arbitrary memory read/write
}
```
:::

#### Unbinding and Destruction

When you need to proactively terminate a task and completely release resources from the C++ side, first retrieve and validate the type using `takeObject<T>()`, then unbind management via `unbindObject()`, and finally destroy it manually:

```cpp
static JsValue stopSensor(JsCtx ctx) {
    Applet *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1) return {};

    int bindId = ctx.arg(0).asInt();
    auto *listener = applet->takeObject<SensorListener>(bindId);
    if (listener) {
        applet->unbindObject(listener); // Unbind from automatic management list
        delete listener;                // Destroy manually
    }
    return {};
}
```

Complete usage workflow on the JavaScript front-end side:

```javascript
import sensor from '@vendor.sensor'

// Start and temporarily store the credential
const id = sensor.startSensor()
// ... Read multiple times
const value = sensor.readSensor(id)
// Task ends, release resources
sensor.stopSensor(id)
```

Thanks to the safety net provided by `bindObject`, even if the application forgets to call `stopSensor()`, the sandbox will automatically release all bound objects upon exiting.

::: important Must Unbind Automatically
Because JavaScript code cannot be trusted, one cannot assume it will call resource-releasing functions. For malicious applications, sandbox leaks caused by JavaScript reference leaks are valid attack vectors. Therefore, **all objects bound to the sandbox must automatically unbind when the sandbox is destroyed**, ensuring that no matter how JavaScript behaves, resource leaks will not occur.

Any design that requires the JavaScript side to unbind is dangerous and must be avoided.
:::

### Security Protections

Despite the numerous security requirements emphasized earlier, this may still not be enough to eliminate all risks. To further strengthen security defenses, we recommend directly restricting extension module access permissions to trusted applications. You can check Applet permission flags or identity information directly in the module factory function, rejecting non-compliant access:

```cpp
static JsValue createDeviceModule(JsVM &vm) {
    auto applet = Applet::current(vm);
    if (!applet || !applet->permission(
                    vendor::Permission::AccessDeviceInfo)) {
        // If lacking permissions, return an empty object or throw an exception
        return vm.newError("permissions denied");
    }

    // Only after authorization can you create module objects and expose features
    JsValue mod = vm.newObject();
    mod["getDeviceName"] = getDeviceName;
    // ...
    return mod;
}
```

This strategy effectively blocks unauthorized access at the entry point. Even if the module function itself is not sufficiently robust, attackers cannot exploit it to obtain sensitive information or execute malicious operations.

Library Loader entry permission checks have already been introduced in related documentation.

============================================================
FILE_PATH: src/transl/EN/cxxdev/sdk-setup.md

# SDK Project Configuration

Glyphix is distributed to device manufacturers in the form of pre-compiled libraries. This article introduces how to configure the build environment in the SDK project in order to develop Native Modules, Native Widgets, or platform adaptation code based on it.

### Prerequisites

Before you begin, make sure you have installed:
- CMake 3.14 or higher
- A C++ compiler supporting C++14 (GCC, Clang, or MSVC)
- The Glyphix meta-object compiler `meta` (matches the SDK; see below for how to obtain it)
- A cross-compilation toolchain (if building for embedded targets)

::: tip System Requirements
- The MSVC toolchain requires Visual Studio 2022 or later.
- For Linux, a distribution with a desktop environment, such as Ubuntu 22.04 or later, is recommended.
- Ubuntu 20.04 is not recommended because its package versions are usually too old, often requiring manual installation of newer software.
- Environments without graphical interfaces like WSL or Docker will not be able to run the simulator and GUI examples.
- Currently, the host environment only provides Linux pre-compiled libraries; pre-compiled libraries for Windows and macOS are not yet available.
:::

## SDK Package Structure

The extracted SDK contains the following directories:

```
glyphix-sdk/
├── libs/
│   └── <target-triple>/       # Pre-compiled libraries categorized by target triple
│       ├── include/           # Glyphix header files (gx_*.h)
│       └── lib/               # Static libraries (libglyphix-core.a, etc.)
├── cmake/
│   ├── GlyphixSDK.cmake       # Main SDK configuration script
│   ├── meta.cmake             # Meta-object compiler integration (glyphix_add_meta_objects)
│   ├── cross-compile.cmake    # Cross-compilation toolchain loading
│   ├── arch/                  # Compilation parameters for each architecture (mips-linux-gnu, cortex-m33, etc.)
│   └── toolchain/             # CMake toolchain files for each toolchain
├── wrapper/                   # Platform adaptation layer (host implementations for network, file system, etc.)
├── app/                       # Sample application entry points (emulator, async, etc.)
└── vendor/                    # Third-party dependency libraries
```

### `libs/<target-triple>/`

The pre-compiled libraries of the SDK are categorized by platform using **target triples**, for example:

- `x86_64-linux-gnu/`: 64-bit Linux host development/simulation
- `mips-linux-gnu/`: MIPS Linux embedded target
- `cortex_m55-none-gnu/`: Cortex-M55 bare-metal target

The `include/` directory contains all Glyphix public header files, all prefixed with `gx_`. The `lib/` directory contains static libraries. The core libraries include:

| Library File | Description |
|:---|:---|
| `libglyphix-core.a` | Core framework (object system, widget tree, events, etc.) |
| `libglyphix-widgets.a` | Built-in widget library |
| `libglyphix-reactive.a` | Reactive framework (JavaScript bridge layer) |
| `libglyphix-platform.a` | Platform abstraction layer interface |
| `libglyphix-service.a` | System service layer |

::: tip Pre-compiled Vendor Libraries
The SDK distribution package also includes some pre-compiled third-party libraries, such as `libfreetype.a`. For convenience, we do not directly distribute the source code of these libraries, but you can choose to build using the source code directly instead of using the pre-compiled libraries.
:::

## Preparation

### Configuring the Meta-Object Compiler

The `meta` meta-object compiler is distributed separately from the SDK as an independent archive. Extracting it yields two directories: `bin/` and `lib/`. **Both must be kept in the same directory**; the `meta` executable depends on the runtime libraries in `lib/`.

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

Alternatively, you can extract it to any directory and add its `bin/` directory to your `PATH`. Once done, verify that it is available with the following command:

```bash
meta --version
```

If you do not wish to modify your `PATH`, you can explicitly specify the full path to the executable during CMake configuration using `-DGX_META=/path/to/bin/meta`.

## Configuring CMakeLists.txt

### Minimal Configuration

::: tip
The CMake configuration introduced in this section resembles the standard sample template of the Glyphix SDK project, and you can refer directly to the SDK's source files.
:::

Below is a minimally runnable `CMakeLists.txt` illustrating the standard configuration skeleton of a project:

```cmake
cmake_minimum_required(VERSION 3.14)

# Must be loaded before project() so the toolchain is in place when project() probes compilers
include(cmake/cross-compile.cmake)

project(my_glyphix_app)
set(CMAKE_CXX_STANDARD 14)

# Load the Glyphix SDK (sets up include paths, link directories, and the glyphix::sdk target)
include(cmake/GlyphixSDK.cmake)

add_subdirectory(vendor)  # Third-party dependencies (if any)
add_subdirectory(src)     # Your source code
```

Create a target in `src/CMakeLists.txt` and link the SDK:

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

As mentioned in the [Object System](./object-system) documentation, any class declaring `GX_OBJECT` must be registered with the build system so the meta-object compiler can generate the `*_meta.cpp` files for it. `glyphix_add_meta_objects()` is the CMake function that accomplishes this:

```cmake
glyphix_add_meta_objects(<target> [header1.h header2.h ...])
```

It takes the target name and a set of **header file** paths as arguments. For each header file, the `meta` tool generates a corresponding `*_meta.cpp` in the `meta/` subdirectory within the build directory, and automatically adds it to the target's source file list for compilation.

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
If a class declares `GX_OBJECT` but is not registered via `glyphix_add_meta_objects()`, it will result in a **link error** (symbols like `staticMetaObject` cannot be found). Remember to update `CMakeLists.txt` whenever you add a new header file containing `GX_OBJECT`.
:::

### The `glyphix::sdk` Interface Target

`GlyphixSDK.cmake` defines the `glyphix::sdk` CMake interface library target, which encapsulates all link dependencies of the SDK. You only need to link this single target in your `CMakeLists.txt`:

```cmake
target_link_libraries(my_target PRIVATE glyphix::sdk)
```

Internally, this is equivalent to:

```cmake
# Pseudocode — actually managed automatically by GlyphixSDK.cmake
target_include_directories(... ${GLYPHIX_INCLUDE_DIRS} wrapper/include)
target_link_libraries(... -Wl,--start-group ${glyphix-*.a} glyphix-wrapper -Wl,--end-group)
target_link_libraries(... m pthread dl)  # UNIX system libraries
```

Wrapping static libraries with `-Wl,--start-group ... -Wl,--end-group` is done to resolve circular dependency linking issues among static libraries on embedded platforms.

::: tip Link Order Issue
If your project has its own static libraries (such as `add_library(my_module STATIC ...)`), they should be linked **inside** `glyphix::sdk`, otherwise the scope of `--start-group` will not cover them, which may trigger link errors. The approach is to append your static library path after the `GLYPHIX_LIBS` variable in `GlyphixSDK.cmake` is defined and before the `glyphix-sdk` target is created, or directly have the final executable link both `my_module` and `glyphix::sdk` and manually specify `--start-group`.
:::

## Host Build

Host builds are used to run Glyphix sample programs on your development machine, allowing you to quickly verify widget and module logic without connecting hardware.

```bash
mkdir build && cd build
cmake -G Ninja ..
cmake --build .
```

The `app/` directory of the SDK contains multiple examples, with each subdirectory corresponding to an independent executable target. For example:

| Subdirectory | Build Output | Description |
|:---|:---|:---|
| `app/emulator/` | `demo` | Simulator with GUI, depends on the MiniFB window backend |
| `app/async/` | `async-demo` | Headless asynchronous service example, demonstrating Native Modules and asynchronous callbacks |

`GlyphixSDK.cmake` automatically detects the compiler target triple of the host (via `gcc -dumpmachine` or `clang -dumpmachine`), and uses it as a key to look up the corresponding pre-compiled libraries in the `libs/` directory. For example, on an x86_64 Linux development machine, it will automatically resolve to `libs/x86_64-linux-gnu/`.

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

If the toolchain is already in your `PATH` (meaning `mips-linux-gnu-gcc` can be called directly), you can omit `-DMIPS_TOOLCHAIN_DIR`, and CMake will locate it automatically.

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

The SDK only provides pre-compiled libraries for the architectures listed in the table above. If your target platform is not among them, you need to contact Glyphix to obtain an SDK package for the corresponding architecture; you cannot add support yourself on top of the existing SDK.

## Other Build Systems

While the SDK uses CMake as its primary build system, Glyphix also provides support for other build systems to partner manufacturers. This typically just involves importing the pre-built SDK libraries and header files, and adding the porting layer source files.

### Project Limitations

This approach is suitable for projects that only require standard SDK features. Once custom widgets, Native Modules, or other capabilities are needed, you must introduce the `meta` meta-object compiler to generate the necessary binding code. Currently, CMake is the only supported build system.

There are several available alternatives:
1. Build custom code using the SDK CMake project, and then link the generated libraries into your main project.
2. Build custom code using the SDK CMake project, and then include the generated source files (`*_meta.cpp`) into your main project.
3. Directly invoke the `meta` tool in your build system to generate binding code.

Among these, the Glyphix SDK itself is built using Method 1. However, this is not suitable for downstream manufacturers' internal development workflows because it requires maintaining a separate project outside of the main firmware project and linking the generated binary libraries back to the main project, which introduces severe version management issues.

Method 3 is also usually undesirable because manufacturers generally do not want to introduce an external tool into their main project's build system.

### Recommended Approach

Therefore, Method 2 is recommended. This approach copies the source code; although it requires manual operation, it is easy to audit and integrate into existing build pipelines. You can build custom code in the SDK's CMake project to generate the `*_meta.cpp` files, then copy these files into your main project and compile them within your main project's build system.

Another limitation of this method is that the custom source files must successfully build within the SDK project environment. Specifically, this requires them to be buildable independently of the main project, which includes:
- Include paths and preprocessor definitions must be set correctly, and the header files of custom components must not include header files specific to the main project.
- It is best if the `.cpp` files of custom components can also compile successfully; although this does not affect the generation of `*_meta.cpp` files, it facilitates rapid iteration and debugging in the host environment.

::: tip
For most [custom widgets](widget.md), this is not an issue. It can be slightly more cumbersome for [Native Modules](native-module.md), and you should note: header files declaring `GX_OBJECT` should not include header files specific to the main project.
:::

============================================================
FILE_PATH: src/transl/EN/cxxdev/widget-export.md

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

============================================================
FILE_PATH: src/transl/EN/cxxdev/platform-font-fallback.md

# Platform Font Fallback

The Glyphix framework has a built-in font loading and fallback mechanism based on `font-face` / `font-family`. However, target platforms usually come with comprehensive font pipelines (such as Windows DirectWrite or macOS CoreText) that already implement system font fallback and related optimizations.

To make full use of the platform font pipeline, Glyphix allows you to take over font fallback: when a font within the framework cannot cover a certain character, the task is handed over to the platform to find and render the appropriate system font. This article is intended for Glyphix system developers and guides you step-by-step through the integration process.

Public header files involved:
- `gx_unite.h`: Contains the UniTE public interface and the engine installation function `installEngine()`;
- `gx_shapingadapter.h`: This is the primary interface;
- `gx_fontdriver.h`: Provides the `FontDriver` encapsulation mechanism;
- `gx_fontloader.h`: Provides the font loader interface.

## Overall Architecture

For a piece of text to be displayed on the screen, it goes through the following pipeline: application text is handed over to the **paragraph layout engine** for line breaking and positioning; text segments with the same script and direction are **shaped** into glyphs; missing characters are filled in by **font fallback**; glyphs are then handed over to the **font driver** to be rendered into bitmaps; and all fonts come from the registration, loading, and reuse of the **font management** layer.

<ArchDiagram max-width="560px">
  <div>Application Text<div class="remark">Paragraph · String · Style</div></div>
  <div>
    Paragraph Layout Engine
    <div class="group row">
      <div>Lightweight Engine LiTE<div class="remark">Simple typesetting (Default engine)</div></div>
      <div>UniTE Engine<div class="remark">BiDi · Shape · Complex scripts</div></div>
    </div>
  </div>
  <div>
    Shaping · Font Fallback
    <div class="group row">
      <div>HarfBuzz<div class="remark">GSUB / GPOS</div></div>
      <div>Simple Shape<div class="remark">Character → Glyph</div></div>
      <div class="subject">FontFallbackShaper<div class="remark">Family fallback · Platform system fonts</div></div>
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
    Font Management (FontManager)
    <div class="group row">
      <div>Registration / Lookup<div class="remark">Face · Family · Attributes</div></div>
      <div class="subject">FontLoader<div class="remark">Load face, inject wrapper</div></div>
    </div>
  </div>
</ArchDiagram>

The three highlighted parts in the diagram are covered in this article:
1. The fallback strategy `FontFallbackShaper`, used to identify missing characters and perform fallback shaping;
2. The `PlatformFont` wrapper responsible for rendering platform fallback fonts, used in tandem with `FontFallbackShaper`;
3. The `FontLoader` used to load the platform fallback font wrapper, which will be registered into `FontManager`.

The rest of the framework layers are already implemented. Text shaping (`ShapingAdapter`) usually does not need to be implemented from scratch; you can directly reuse the reference implementation.

### Prerequisites

Before implementing the platform font fallback feature according to this document, you need:

- Enable the UniTE text engine (compared to the default lightweight engine, it supports complex script shaping and multi-level fallback).
- The target platform must support a complete font pipeline capable of advanced features such as system font shaping and script mapping. This is usually a complex subsystem that most MCU RTOS platforms lack.

::: important
Compared to the default LiTE engine, enabling UniTE and the complete font pipeline requires more memory and firmware space. Moreover, the performance of this engine is lower than the lightweight LiTE, so you need to evaluate whether it is necessary to enable it for complete Unicode support and internationalization requirements.
:::

## Reusing the Shaping Backend

`ShapingAdapter` is responsible for shaping characters into glyphs. The built-in `HarfBuzzShaper` (`gx_harfbuzz_shaper.cpp`) already implements complete OpenType shaping. It calls HarfBuzz for shaping, and then writes glyph indices, advances, and offsets into the output based on the target pixel size.

`HarfBuzzShaper` relies on FreeType to read font files, so both HarfBuzz and FreeType libraries must be included simultaneously. If these libraries already exist on the target platform, make sure their versions match, otherwise link or runtime errors may occur.

::: tip
Similar to HarfBuzz's [responsibility](https://harfbuzz.github.io/what-harfbuzz-doesnt-do.html), `ShapingAdapter` does not handle text runs containing different fonts, which includes the "font fallback" mechanism described below. Therefore, as long as the font used in shaping is missing a character, the `ShapingAdapter` implementation will return the `.notdef` glyph (index `0`), leaving it to the fallback strategy to handle.
:::

## Implementing the Fallback Strategy

`FontFallbackShaper` is the core of the fallback mechanism. The engine calls it every time it shapes a section of text, requiring a glyph sequence **free of missing characters** to be returned as the shaping result. Unlike `ShapingAdapter`, it is not just shaping for a single font-face, but is designed for a two-tier fallback.

### Two-Tier Fallback Cascade

`FontFallbackShaper::shape()` performs fallback in two tiers from nearest to farthest:

- **First tier**: Use other fonts within the current family to complement each other. This is already implemented by the framework; you only need to call `builtinShape()`.
- **Second tier**: Missing characters that cannot be resolved by the first tier are handed over to the platform system fonts. This tier is implemented by you.

Missing characters are represented in the data by a glyph index of `0`, i.e., `.notdef`. The return value `FallbackResult` of `shape()` uses bit flags to express the result: `result & NotNeeded` being true indicates that there are no more missing characters and can end directly; otherwise, common returns are `FullyResolved` (all processed) or `PartiallyResolved` (some `.notdef` still remain).

### `shape()` Function Skeleton

First call the first tier; return if there are no missing characters, otherwise proceed to the second-tier platform font fallback. `m_shaper` is the `ShapingAdapter` held by this fallback processor (usually `HarfBuzzShaper`).

```cpp
FallbackResult shape(GlyphRunBundle &storage,
                     TextSpan text,
                     FontDriver *font) override {
    // First tier: Use builtin API to handle fallback within the family
    auto r = builtinShape(storage, text, font, &m_shaper);
    if (r & NotNeeded)
        return r;                                  // No missing characters, finish
    return resolveByPlatform(storage, text, font); // Second tier, see below
}
```

`builtinShape()` is the only place that depends on `ShapingAdapter`. In this case, you typically need to implement `PlatformFallbackShaper` as follows:
```cpp
class PlatformFallbackShaper : public FontFallbackShaper {
    HarfBuzzShaper m_shaper; // Directly define as a member variable, no pointer reference needed

public:
    PlatformFallbackShaper() = default;
    FallbackResult shape(GlyphRunBundle &storage,
                         TextSpan text, FontDriver *font) override;
};
```
Please note that `m_shaper` is merely a private member variable of your platform fallback strategy and does not need to be exposed externally at all. When calling `builtinShape()` inside `shape()`, simply pass `&m_shaper`.

::: tip
In extreme cases (such as the initial adaptation phase), you can ignore the fallback within the family and directly skip `builtinShape()`, only handling the second-tier platform fallback. In this case, the `m_shaper` member variable can be omitted.

Regardless, specific `ShaperAdapter` classes generally cannot be defined as local variables because they may hold HarfBuzz cache states, and recreating them on every shaping operation would cause severe performance degradation.
:::

### Obtaining Platform Fonts

The second tier hands over missing characters to the platform and ultimately lets the wrapper render them. `fallbackFont(font)` returns the wrapper registered at the end of the family (see below). Its static type is `FontDriver *`, and you need to cast it back to your own wrapper type in order to call your custom registration and query interfaces.

```cpp
// Casting can also use dyn_cast, but if there is only one wrapper type, static_cast is also safe
auto *wrapper = static_cast<PlatformFont *>(fallbackFont(font));
if (wrapper == nullptr)
    return PartiallyResolved; // No wrapper at the end of the family, cannot continue
```

::: warning Must Be Implemented in Pairs
The fallback strategy and the wrapper are a matched pair: the `static_cast` above requires that `fallbackFont()` returns precisely your own wrapper type. Make sure that the installed fallback processor matches the registered wrapper.
:::

### Simple Fallback Shaping

The most common and starter-friendly scenario is: the entire run can be shaped using a single platform font (i.e., a certain system font file completely covers the script). In this case, select the platform font according to `storage.run().spec.script`, re-shape the entire run, write the entire section into the same `faceId`, **directly overwriting the first-tier result**, without needing to merge with already resolved glyphs.

UniTE splits runs by script, and Latin and CJK within the same text segment are inherently different runs. When the main font focuses on Latin and encounters scripts such as CJK, Arabic, or Devanagari, the entire run after `builtinShape()` is often `.notdef`, and re-shaping and overwriting the entire run will not lose any resolved glyphs. Therefore, multilingual typesetting almost entirely follows this path and is not a degenerated special case.

```cpp
// Select platform font based on script (platform font handle, not FontDriver), register to get faceId
auto sysFont = platformFontForScript(storage.run().spec.script);
uint32_t faceId = wrapper->registerFont(sysFont);
// Your shaping step produces glyphCount glyphs (demonstrated here with HarfBuzz output)
auto &run = storage.resize(glyphCount);
for (int i = 0; i < glyphCount; ++i) {
    run.data.glyphIds[i]   = GlyphIds::encodeFallback(gid[i], faceId);
    run.data.xAdvances[i]  = uint16_t(scale(pos[i].x_advance));
    run.data.xOffsets[i]   = int16_t(scale(pos[i].x_offset));
    run.data.yOffsets[i]   = int16_t(scale(pos[i].y_offset));
    run.data.clusterMap[i] = static_cast<int>(info[i].cluster);
}
```

The fields `pos`, `info`, `gid`, and `scale` come from your shaping steps, demonstrated above using HarfBuzz output.

::: tip Platform Shaping Capabilities
Platforms usually come with their own shaping capabilities (such as DirectWrite, CoreText). Whether to reuse HarfBuzz depends on the specific platform; the HarfBuzz output in the demonstration can be replaced with the platform's shaping output. For RTL runs (`spec.bidiLevel & 1`), the direction must be passed to the shaper.
:::

The premise of this method is that the entire run maps to a single platform font. It **does not apply to Common scripts** (Emojis, symbols, etc.): different characters within the same run may belong to multiple platform fonts, requiring the complex fallback described below.

### Complex Fallback Shaping

When multiple platform fonts are needed within a run, or only some clusters need fallback, the simple solution no longer applies. Considering that specific fallback and merging algorithms depend on platform APIs, this document only constrains the semantics that the merged `GlyphRun` must satisfy, and the implementation must handle it accordingly:

- Glyphs already resolved in the first tier are **retained as is**, and the second tier only replaces clusters that are still `.notdef`.
- Fill every glyph slot with `glyphIds`, `xAdvances`, `xOffsets`, `yOffsets`, and `clusterMap`; fallback glyphs are marked using `encodeFallback(gid, faceId)`.
- `clusterMap[i]` is the offset of the source code point corresponding to this glyph relative to **this run** (consistent with `spec.text`, range `[0, text.length())`), used for drawing mapping and per-line clipping.
- Glyph count is variable: use `storage.resize()/reset()` to adjust storage, then write slot by slot. `GlyphRunBundle` will automatically update `run().glyphCount`.
- When a single source cluster maps to multiple glyphs, the order and sum of advances must be correct; code points swallowed by GSUB cluster merging should produce zero-advance glyphs to avoid gaps or misalignments.
- `faceId` must be a stable ID registered in the wrapper and valid throughout its lifecycle; the glyph order and shaping direction of RTL runs must be consistent.
- Return value: return `FullyResolved` if all are filled, or `PartiallyResolved` if residuals remain.

As long as the output satisfies the above constraints, the framework can render correctly. Whether to query platform APIs segment by segment or reuse HarfBuzz to shape font by font can be chosen according to the platform.

### Line Height and Caching

Line height depends on **which font actually draws each glyph**. `builtinLineMetrics()` is responsible for parts of the glyphs within the family; glyphs with fallback marks (`isFallback()`) query the wrapper for their system font's ascender and descender and incorporate them. Fallback glyphs are encoded in `GlyphIds` by `encodeFallback`, and their `fontIndex()` is the written `faceId`, based on which the corresponding platform font is retrieved from the wrapper.

```cpp
VerticalMetrics resolveLineMetrics(const GlyphIds *gids, int count,
                                   FontDriver *font) const override {
    // Handle glyphs within the family
    VerticalMetrics m = builtinLineMetrics(gids, count, font);
    // Handle platform fallback glyphs
    auto *wrapper = static_cast<PlatformFont *>(fallbackFont(font));
    if (wrapper == nullptr)
        return m;
    // For glyphs where gids[i].isFallback(), query asc/descent from wrapper and incorporate into m
    for (auto gid : utils::span<const GlyphIds>(gids, count)) {
        if (!gid.isFallback())
            continue; // Process fallback glyphs only
        uint32_t faceId = gid.fontIndex(); // The fontIndex() of a fallback glyph is its faceId
        auto face = wrapper->fontForFaceId(faceId); // Platform font handle (not FontDriver)
        if (face == nullptr)
            continue;
        m.ascent = max(face->ascender(), m.ascent);
        m.descent = min(face->descender(), m.descent);
    }
    return m;
}
```

You can also aggregate the fallback fonts of the entire line and query their asc/descent all at once to avoid per-glyph queries in a loop.

`flush()` is used to release system fonts cached by the wrapper:

```cpp
void flush(FontDriver *font) override {
    if (auto *w = static_cast<PlatformFont *>(fallbackFont(font)))
        w->releaseFonts();
}
```

::: tip
`flush()` is called by the framework when a paragraph is destroyed or memory is tight. Please clean up platform resources held by the wrapper inside it.
:::

## Fallback Font `FontDriver` Wrapper

The wrapper is responsible for rendering the glyphs shaped in the previous step into bitmaps. It inherits from `FontDriver` and carries the `PlatformFallback` flag upon construction, letting the framework know it is a fallback font.

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

This font wrapper is not used to load some font file (like `FontDriverTTF` does). Its role is to hand over fallback glyphs to the platform font pipeline for processing, while the internal implementation is opaque to Glyphix.

### Dual-Mode Query

The `code` received by the wrapper has two meanings, distinguished by the `CodeAsGlyphId` bit:

- **Tagged**: Query by glyph index, with the high bits carrying `faceId` and the low bits being the glyph index. After decoding, it is routed to the corresponding platform font, and then queried for the corresponding `GlyphBitmap` using `glyphId`.
- **Untagged**: Unicode character query, fallback lookup among registered platform fonts by code point, which internally converts to a glyph index before querying.

A typical `bitmapOf()` implementation is as follows:

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
`fontForFaceId()` returns a platform font handle, **not a `FontDriver`**; `face->bitmapOf(...)` and `face->glyphIndexOf(...)` above are pseudo-code operating on that handle, representing "getting `GlyphBitmap` by `glyphId`" and "getting `glyphId` by code point" respectively.
:::

`metricsOf()` uses the same dual-mode logic; `advancesOf()`, `baseline()`, etc., are also calculated from platform fonts. `duplicate()` only needs to copy a mapping table.

### `faceId` Mapping

The wrapper maintains a mapping of `faceId` → platform font for the fallback strategy to register and look up during rendering.

`faceId` is a $10$-bit integer ($[0, 1023]$), and its meaning is entirely defined by the implementation, with the only requirement being **stability throughout its lifecycle**. There are two common approaches:

- **Fixed by script**: Directly use the `Script` enum value as `faceId`. The wrapper holds the corresponding platform font by script, and registers it by script upon creation without runtime allocation.
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
`faceId` is the contract between the fallback strategy and the wrapper: `PlatformFallbackShaper` uses it to encode glyphs, and `PlatformFont` uses it to decode back to system fonts. Both ends must interpret `faceId` consistently, and it must be representable by a $10\text{-bit}$ integer.
:::

## Registering the Wrapper

Finally, let the framework incorporate the wrapper into family loading. Implement `FontLoader::load()`, return the wrapper for a certain generic family name, and then install it into `FontManager`:

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

When an application requests a font in the form of `"<primary-face>,sans-serif"`, the framework merges each part into the same family in comma-separated order, with the wrapper acting as the last item to become the fallback face, allowing `fallbackFont()` to retrieve it.

`PlatformFont` and `PlatformFontLoader` are usually only registered as fonts for generic family names like `sans-serif`, rather than any specific system font name. This allows applications to use the same family name across different platforms without knowing the platform's specific fonts.

::: warning Functional Limitation
The wrapper must always be placed as the last item in the family, and applications must write family names in the order described above. The mechanism to automatically guarantee this order is still under development.
:::

## Installation and Assembly

`installEngine()` in `gx_unite.h` plugs your fallback strategy into the engine:

```cpp
unite::installEngine(*CoreApp()->typesetCore(),
                     std::make_unique<PlatformFallbackShaper>());
```

Complete assembly sequence:

1. `fontManager()->install(new PlatformFontLoader)`: Register the wrapper loader.
2. `installEngine(...)`: Install the fallback strategy holding the shaping backend.
3. Request fonts in the form of `"<primary-face>,sans-serif"`, and lay out and render as usual.

## Notes

- Advances / offsets are uniformly Q26.6 fixed-point (value = pixels × 64).
- Unresolved `.notdef` (glyph index $0$) are skipped during rendering, displaying blank spaces or tofu blocks at their corresponding positions.
- `faceId` is only $10$ bits, meaning the upper limit of simultaneously active system fonts in a single family is $1024$.
- The fallback strategy and the wrapper must be implemented in pairs and maintain type consistency (relying on `static_cast`).
- Be sure to release the platform font caches held by the wrapper inside `flush()`.

============================================================
FILE_PATH: src/transl/EN/cxxdev/widget-slider-demo.md

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

============================================================
FILE_PATH: src/transl/EN/cxxdev/global-assets-migrate.md

# Global Resource Migration Guide

This document is intended for Glyphix downstream integration projects, helping you upgrade global resource loading methods from older projects to the latest scheme. This achieves an easily manageable and editable global resource layout without relying on vendor-supplied packaging or conversion tools.

Early versions of Glyphix used `global.pkg` binary archive packages to manage global resources (font files, font mapping tables, etc.). Later, it gradually evolved to directly using unpacked resource files, and finally, the font mapping file format transitioned from binary to standard JSON <version-badge since="0.9" />. If your maintained entry code still uses the old syntax, you can follow this guide to upgrade.

::: tip
Using the old mode introduces maintenance hassles, making it difficult to manage and edit global resources. Upgrading immediately is strongly recommended.
:::

## Removing `global.pkg`

### Old Code Characteristics

If your entry code contains any of the following patterns, it means you are using `global.pkg`:

```cpp
EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
static String globalUri(const String &path) { return "pkg:///" + path; }
```

The effect of these two lines is to route all resource requests with the `pkg:///` protocol to the files inside the `/global.pkg` binary archive package.

Why it needs to be removed:
- Every time fonts or other resources are replaced, the packaging tool must be re-run to generate the `.pkg` file.
- Individual files inside `.pkg` cannot be directly viewed or replaced during debugging, making it difficult to verify contents.
- The packaging process relies on dedicated tools, increasing communication and maintenance costs.

### Migration Steps

**Step 1: Extract resources from `global.pkg`.**

If you no longer have the `.pkg` source files, you can extract the contents from `global.pkg` (using the Glyphix command-line tool or by requesting the original resource files). Typically, you need to extract the following:

```
fonts/
    NotoSans-Regular.ttf
    NotoSansSC-Regular.ttf
    ...
    font-faces          ← Font mapping file (will be upgraded to JSON later)
```

Place the extracted directory into your project's resource directory, for example, `/fonts/`.

**Step 2: Remove `global.pkg` related code.**

1. Delete the entire line `EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg")`.
2. Delete wrapper functions like `globalUri()`.
3. Change all resource references from `pkg:///xxx` to direct file paths, i.e., `/xxx`.

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

Change it to use file paths directly (without the `globalUri()` function and `GlobalPackage` registration):

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

You are still using the binary `font-faces` file at this stage; the next section will upgrade it to JSON.

## Switching to JSON Font Mapping Files

### Old Code Characteristics

```cpp
FontFaceMap &map = App()->fontManager()->faces();
map.readFile("/fonts/font-faces");
```

`readFile` reads a custom binary format file. This binary file cannot be edited manually and must be converted and generated from CSS files using a packaging tool.

### JSON Format Description

Now, we use a JSON file directly to describe the font mapping relationships. You only need to create a `font-faces.json` file with the following format:

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
| `urls` | String Array | Yes | - | Font file paths, relative to the directory where the JSON file is located |

Further explanations for key fields are provided below.

**The `weight` Field**

For `weight`, directly enter the CSS font weight numerical value, which will be rounded to the nearest standard value:

- `100` Thin
- `400` Regular (default value, can be omitted)
- `700` Bold
- `900` Black

**`urls` Path Resolution**

Paths in `urls` are resolved relative to the directory where the JSON file is located. For example, if the JSON file is located at `/fonts/font-faces.json`, writing `"fonts/NotoSans-Regular.ttf"` in `urls` will ultimately be resolved as `/fonts/fonts/NotoSans-Regular.ttf`.

Therefore, it is recommended to place the JSON file directly in the same directory as the font files, allowing URLs to be written simply as file names. For example, the directory layout:

```
/fonts/
    font-faces.json
    NotoSans-Regular.ttf
    NotoSansSC-Regular.ttf
    NotoSans-Bold.ttf
```

The JSON content at this point matches the code snippet above.

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

Only this single API call needs to be changed; no other code needs to be modified. Afterwards, you can directly edit `font-faces.json` to add/remove fonts or adjust mapping relationships without needing any conversion tools.

## FAQ

**How to handle multiple variants (Regular, Bold, Italic, etc.) for the same family?**

Add an independent entry for each variant in the `font-faces` array, distinguishing them using `weight` and `style`:

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

MCU projects typically only use the Regular `sans-serif` font with `normal` weight, and the system will automatically fall back.

**Can multiple files be placed in the `urls` array? When is it needed?**

Yes. When a font family needs to cover multi-language characters, put multiple font files into the same `urls` array. For example, if `sans-serif` needs to support Latin letters, CJK characters, and Arabic simultaneously:

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

When rendering text, the engine will search for character glyphs in these files sequentially, and the first matched glyph will be used.

**Must the font files and JSON be in the same directory?**

No. Paths in `urls` are resolved relative to the JSON file's directory; you can use relative paths to place fonts in subdirectories. Absolute paths can also be used, in which case they are unaffected by the JSON directory.

**Can a JSON string be passed directly in code?**

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

This document is not a C++ tutorial; rather, it provides quick learning recommendations and prerequisite knowledge for developers preparing to read the documentation in this directory.

It assumes that you have long-term experience using C, and are familiar with MCUs, RTOS, drivers, LVGL, or similar embedded frameworks. You should have a wealth of programming experience, but may not be familiar with the subset of C++ required by Glyphix.

::: tip
If your goal is to develop Native Modules, asynchronous features, or Native Widgets, please read this document first before proceeding to the [Object System](./object-system.md) and other chapters. This will help you avoid many "I can understand the code, but I just can't write it" issues.
:::

## C++ Feature Subset

The Glyphix project disables certain C++ features, so developers do not need to learn them at all:

- **RTTI is disabled**: You cannot use `dynamic_cast`, `typeid`, or other runtime type identification mechanisms. When you need a safe downcast, use [`dyn_cast`](object-system.md#dynamic-type-casting) directly.
- **Exceptions are disabled**: You do not need to learn `try` / `catch` / `throw` as a primary path. Error handling should prioritize return values, status codes, object states, and explicit checks. This is similar to C error-handling conventions.


Additionally, the Glyphix runtime has some special constraints, which are mainly caused by the fragmentation and compatibility limitations of MCU systems:
1. Concurrency tools from the C++ standard library, such as `std::thread` and `std::mutex`, are not available on MCUs.
2. Time libraries like `std::chrono` are also not available on MCUs.
3. Do not use function-local static variables; the atomic initialization guaranteed since C++11 is **highly likely to be unreliable** on MCUs.
4. Do not use global variables (objects) that rely on heap allocation, because the global construction phase on MCUs may be uncontrolled, and heap memory might be unavailable.

Points 3 and 4 are very common scenarios and require special attention.

## C++ Knowledge to Master

The following content is sufficient to support most of the documentation in this directory.

### Classes and Object-Oriented Programming

You need to be able to at least read and write code like this:

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

- The difference between classes and structs (very little difference; mainly default access permissions)
- The meaning of public inheritance (generally, only public inheritance is used)
- Constructors and initialization lists
- Member functions, **`const` member functions**
- When a base class interface is being overridden versus when a normal member function is simply being declared

This knowledge will appear directly in the [Object System](./object-system.md), [Widget Development Guide](./widget.md), and [Widget Registration & Export](./widget-export.md).

### Pointers, References, and `const`

If you are familiar with C, this part is the easiest to "assume you already know," but C++ usage is stricter than C.

Key points that must be truly mastered:

- The difference between `T *` and `T &`
- When to pass by pointer versus when to pass by reference
- The meanings of **`const T *`**, `T *const`, and **`const T &`**
- Why `const` member functions are very common
- Why objects should not be arbitrarily manipulated byte-by-byte like in C

In Glyphix, this knowledge is directly related to interface design and lifecycle safety.

### Lifecycles and Resource Management

This is the most important section when migrating from C to C++.

You need to build the following habits:

- Objects are automatically destructed when they go out of scope.
- Constructors are responsible for establishing a valid state.
- Destructors are responsible for releasing resources.
- Do not manually clean up resources at the end of a function.
- Do not treat complex objects as ordinary memory blocks to be `memset` / `memcpy`'d.


A large number of Glyphix facilities and features are built on top of C++'s object lifecycle model, including topics such as RAII.

### Basic Usage of Templates

You don't need to understand this in depth, but you should at least be able to read:

- `Signal<int>`
- `Pointer<Label>`
- `SharedRef<MyData>`
- `async::ResultSession<Client>`
- `std::vector<T>`

And know that "templates are code generation mechanisms with type parameters," rather than some advanced trickery that only library authors touch.

In the Glyphix documentation, templates mainly appear in two forms:

- **Generic containers / utility types**, such as `Signal<T>`, `Pointer<T>`
- **Specialization points**, such as supplying `js_cast<T>` for custom types

Developers should at least understand basic terms like "template parameters," "instantiation," and "specialization," and be able to read template type declarations and usage. However, defining your own template classes or functions is not required.

### Lambda Expressions

In modern C++, lambdas are a very practical way to write one-off functions. You should at least be able to read:

```cpp
mod["double"] = [](JsCtx ctx) -> JsValue {
    return ctx.arg(0).asInt(0) * 2;
};
```

As well as:

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
Lambdas essentially completely occupy the niche of callback functions, meaning they are everywhere. To some extent, lambdas may be the most important C++ syntax point.

A **captureless** lambda expression is almost identical to a C function pointer, differing only in syntax and alleviating the "naming things is hard" problem.
:::

### Minimum Working Set of the Standard Library

You do not need to systematically study the entire STL, but it is recommended to first become familiar with these most common components:

- `std::vector`
- `std::array`
- `std::move`
- Basic algorithms from `<algorithm>`, iterators, and range-based `for` loops

::: tip Associative Containers
Glyphix implements its own `HashMap` and `HashSet`, which are very similar to `std::unordered_map`. However, using associative containers like `std::map` and `std::unordered_map` is not recommended due to their poor performance, and `std::map` suffers from noticeable code bloat.
:::

### C and C++ Interoperability

If you are interfacing with underlying SDKs, you will almost certainly use this part.

At a minimum, you should know:

- The purpose of `extern "C"`
- C callback function pointers
- `void *` context parameters, and the implicit conversion limitations of `void *` in C++
- The division of labor between C structs and C++ wrapper layers

You will see a very typical pattern in the [Async Development Examples](./async-examples.md): the C API handles the actual asynchronous execution, while the C++ layer only handles parameter wrapping, lifecycle management, and result passing.

::: tip Difficulty Expectation
This part is not difficult, but it is prone to linking errors. You may need to learn how to resolve issues caused by `extern "C"` and other factors when mixing C and C++ headers.
:::

## Recommended Learning Order

It is recommended to fill in the gaps in the following order, rather than reading a thick textbook from page one.

### First, Establish a "C to C++" Migration Perspective

[ISO C++ FAQ](https://isocpp.org/faq)
- Prioritize reading entries related to "Learning C++ if you already know C" and "How to mix C and C++."
- This material is well-suited for experienced C developers because it assumes you already understand memory, interfaces, building, and low-level constraints.

### Quickly Build an Impression of Modern C++

[A Tour of C++](https://www.stroustrup.com/Tour.html)
- If you are willing to read a short book, this is the one most worth investing time in.
- It is not a "zero-based programming tutorial," but rather a modern C++ overview for experienced developers.
- The goal is not to memorize everything, but to know what the main components of C++ are and what problems each solves.

### Syntax and Standard Library Reference Manual

[cppreference](https://en.cppreference.com/w/cpp)
- Suitable for looking things up as you go, rather than reading sequentially from cover to cover.
- When you encounter syntax or library names like `override`, lambdas, initialization lists, template specialization, or `std::vector` while reading the Glyphix documentation, you can look them up directly here.
- If you need to review certain details of the C language, you can also look them up here.

### Switch Your Coding Habits to Modern C++

[C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- This is not a tutorial, but rather a guide to engineering practices (also available in book form).
- Reading it sequentially from start to finish is not recommended; prioritize these chapters:
  - `P`: Philosophy
  - `I`: Interfaces
  - `F`: Functions
  - `C`: Classes and class hierarchies
  - `R`: Resource management
  - `ES`: Expressions and statements
  - `CPL`: Interop
  - `SF`: Source files
  - `SL`: The Standard Library
  - `CP`: Concurrency (read as needed)

[Embedded Artistry's C++ Articles](https://embeddedartistry.com/blog/tag/cpp/)
- Better suited for topical reading rather than a systematic course.
- Notable topics include how to use C++ without the heap, strong-type register encapsulation, and what happens before `main()`.

## How to Apply These Resources

A relatively efficient approach is not to "learn C++ for a while before starting Glyphix," but to proceed in parallel:

1. Read this document first to understand what knowledge needs to be supplemented.
2. Read [A Tour of C++](https://www.stroustrup.com/Tour.html) or the C-migration-related parts of the FAQ.
3. Start reading the [Object System](./object-system.md) and [Native Module Development](./native-module.md).
4. When you encounter syntax you don't understand, use [cppreference](https://en.cppreference.com/w/cpp) to look it up precisely.
5. When you encounter questions like "Why does modern C++ tend to be written this way?", refer to the corresponding chapters in the [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).

This learning rhythm is closer to real-world work and is better suited for developers who already have embedded experience.

## Mapping This Document to the cxxdev Documentation

If you are ready to continue reading, you can map the important knowledge points as follows:

- [Object System](./object-system.md): Classes, inheritance, lifecycles, references, template basics
- [SDK Project Setup](./sdk-setup.md): Header files, source files, build systems, basic class declaration knowledge
- [Native Module Development](./native-module.md): Function interfaces, lambdas, object lifecycles, C/C++ interop
- [Asynchronous Feature Development](./async.md): Templates, threading models, object ownership, callback constraints
- [Widget Development Guide](./widget.md): Inheritance, member functions, event handling, object trees, and the rendering pipeline

============================================================
FILE_PATH: src/transl/EN/cxxdev/applet-install-flow.md

# Application Installation Process

Glyphix is an application framework designed for embedded devices. After a device leaves the factory, end users or manufacturers still need to be able to add applications to it—just like installing an app on a smartphone. However, on resource-constrained MCUs, what "installing an application" actually means and how the framework finds and launches it is not as widely understood as on mobile phones.

This document introduces the complete lifecycle of an application package on a device: Installation → Launch → Uninstallation, and explains how directory configuration affects app discovery, updates, and uninstallation.

## "Installing an Application" on a Device

A Glyphix application is delivered as a `.pkg` file—a read-only resource container that houses the application's manifest (`manifest.json`), JavaScript code, images, and other assets. The application is not unpacked at runtime; the framework reads files directly from the `.pkg` on demand.

**Installing** an app essentially involves two actions: placing this `.pkg` file into a directory scanned by the framework, and registering its package name in the package database. Once registered, the framework can locate the corresponding `.pkg` via the package name and launch it. **Uninstalling** is the reverse operation: deleting the `.pkg` file, cleaning up data generated by the app, and unregistering it from the database.

::: tip Resource Bundle Format
The runtime uses the complete `.pkg` resource file instead of an extracted directory. This bundle pattern is also common in game engines. Because application resource packages are only read from and never written to, the bundle pattern reduces file system fragmentation and prevents a multitude of small files from excessively consuming file system inodes.
:::

Two roles are involved here, and this tutorial is targeted at the latter:
- **Application Developer**: Writes the application in JavaScript, builds it into a `.pkg` file using the `gx build` command, and delivers it.
- **Platform Developer**: Integrates the Glyphix runtime on the device, configures the directories for storing applications, and calls the installation and startup APIs in C++. You are provided with a `.pkg` file, and your goal is to make it run.

::: tip
This tutorial assumes you already have a functional Glyphix platform skeleton (`Application` + `JsVM` + `AppletKit`). If you do not, please refer to the `examples/emulator` sample provided with the SDK.
:::

## Preparation

Before getting started, please ensure the following conditions are met:

- A running Glyphix platform. The minimal skeleton is shown below; all subsequent operations will take place within this context.
- A `.pkg` file to be installed. You can obtain one from an application developer or build a sample app yourself using `gx build`. This tutorial assumes the filename is `com.example.demo.pkg` and the package name is `com.example.demo` (the package name is defined in the app's [`manifest.json`](/framework/application/manifest.md#package)).
- A writable partition on the device to store the `.pkg` file and application runtime data. Below, `/data` represents this partition.

A simple Glyphix platform skeleton looks like this (this is not pseudo-code; it is just this simple):

```cpp
#include "gx_application.h"
#include "gx_appletkit.h"
#include "gx_jsvm.h"
#include "gx_widget.h"

using namespace gx;

int main() {
    Application app{new MyPlatform}; // Platform adaptation, implement according to the device
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

Before installing any applications, you must inform Glyphix of the locations of two categories of directories: **Application Package Directories** (where `.pkg` files are stored) and **Application Data Directories** (where data generated during application runtime is stored). They serve different purposes and must not be confused.

### Application Package Directories

Application package directories are managed by `EnvPath::packages()`. It is a list, where each entry points to a directory containing `.pkg` files. This list serves multiple semantic purposes simultaneously, and understanding them is the foundation for all subsequent configurations:

- **Discovery**: When the framework needs to load a resource such as `pkg://com.example.demo/...`, it traverses the list **from front to back**, looking for `com.example.demo.pkg` in each directory. The first match is loaded.
- **Installation**: When the installation API is called, the new package is **always written to the last directory in the list**.
- **Uninstallation**: Uninstallation scans **from front to back**, deleting from the first directory that contains the package.

Since installation always targets the end of the list, while discovery and uninstallation start from the head of the list, the position of a directory in the list determines its role: directories near the front are suitable for "factory-default applications that should not be overwritten"; directories near the rear are suitable for "applications installed subsequently by the user."

::: important Prerequisite
Before calling the installation API, the `packages()` list must contain at least one directory, and the last directory in the list (i.e., the installation target) must exist and be writable. Otherwise, the installation will fail immediately.
:::

Configuration is performed by appending directories to the list during the platform initialization phase:

```cpp
#include "gx_environment.h"
using namespace gx;

// Call after Application construction and before installation/launch
EnvPath::packages().emplace_back("/data/apps");
```

### Application Data Directories

Applications require writable space at runtime to store caches, files, temporary data, etc. These directories are configured via `EnvPath::setEntry(role, path)`, with each role corresponding to a specific purpose. Their semantic contracts are as follows:

| Role | Meaning | Typical Path |
|:---|:---|:---|
| `AppletCache` | Writable cache for apps; the framework can clear and rebuild it when space is tight | `/data/cache` |
| `AppletFiles` | Private files of the app, retained persistently and not automatically cleared | `/data/files` |
| `AppletMass` | Large file storage (such as media assets), high capacity | `/data/mass` |
| `AppletTemp` | Temporary files, can be cleared after the app exits | `/data/temp` |
| `AppletStorage` | Persistent storage for the app | `/data/storage` |
| `LoggingDirectory` | Framework logging directory | `/logs` |

**Data Isolation**: The framework creates independent subdirectories for each application under the above directories based on the package name. For example, the private files for the application `com.example.demo` reside under `/data/files/com.example.demo/`. You do not need to manage these subdirectories manually; the framework automatically creates and cleans them up during installation and uninstallation.

In addition, there is a special role called `GlobalPackage`, which points to a globally shared `.pkg` (such as `/global.pkg`). All applications can read public resources such as fonts and icons from it via the `pkg:///...` protocol. It does not belong to any specific application and is typically flashed along with the firmware.

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
The `Application` constructor resets `EnvPath` to its default configuration, so custom configurations should be completed immediately after `Application` construction and before any `installPackage`/`launch` calls. Late configuration will lead to unexpected behavior.
:::

### Configuration Example

Combining both types of directories, a minimally viable initialization snippet looks like this:

```cpp
Application app;
// Application package directory: at least one writable directory
EnvPath::packages().emplace_back("/data/apps");
// Application data directories: adjust according to actual device partitions
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

1. The `EnvPath::packages()` list is not empty, and its last directory exists and is writable.
2. `AppletKit` has been constructed (installation requires writing to the package database it manages).
3. The `.pkg` file to be installed already exists in the device's file system (for example, located at `/tmp/com.example.demo.pkg`).
4. If using the default version verification policy (`NormalVerify`), the device's vendor/product ID must be configured; otherwise, the installation will return `InvalidDevice` due to device ID verification failure.

### Triggering Installation

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
| `FileIOError` | Copy failed, typically because the installation directory is not writable or space is insufficient |

The verification policy `PackageVerify` determines how strictly the framework scrutinizes the installation package:

| Policy | Version Verification | Device ID Verification |
|:---|:---|:---|
| `NormalVerify` (Default) | New version must not be lower than the installed version | Required |
| `UpgradeOnly` | Must be strictly higher than the installed version | Required |
| `IgnoreVersion` | Skipped | Required |
| `NoVerify` | All skipped, as long as the package is valid | Skipped |

::: tip
If you encounter `InvalidDevice` or `InvalidVersion` during initial installation debugging, you can temporarily use `AppletKit::NoVerify` to bypass verification interference. Once you confirm the installation process itself works properly, restore the formal policy.
:::

### What Installation Does

`AppletKit::installPackage` guarantees the following effects externally:

- Verifies that the `.pkg` file is legal, and checks the version and device ID according to the selected policy.
- If an application with the same name is currently running, it is terminated first to avoid file locks or data conflicts.
- Copies the `.pkg` file to the last directory in the `packages()` list, with the filename `<package-name>.pkg`. If a file with the same name already exists, it is overwritten.
- Registers the application in the package database, recording its installation path and the `pkg://<package-name>` access URI.
- If the application manifest declares a URI scheme (for example, registering itself as a handler for the `ime` input method), it is registered as well.
- Emits a "package changed" notification so other parts of the framework are aware of the new application.

::: important Package Verification Capabilities
`AppletKit::installPackage()` itself lacks file integrity or signature verification capabilities. Device manufacturers need to develop related functionality independently, verify the `.pkg` file before calling `installPackage()`, and ensure consistency through file system power-loss protection and rollback mechanisms during the installation process. The framework only guarantees completion of the installation on the premise that the `.pkg` file is legal, readable, and writable.
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

Installation merely puts the package in place. To make the application actually appear and run, you need to call `AppletKit::launch(name)`, where `name` is the package name defined in the manifest:

```cpp
Applet *applet = kit.launch("com.example.demo");
if (!applet)
    LogError() << "launch failed";
```

`launch` returns a pointer to the application object, or `nullptr` upon failure. Upon success, the application enters the foreground and is displayed.

::: tip Dependency Note
Whether `launch()` can successfully display the application also depends on whether the JavaScript engine, window system, platform graphics adaptation, and the application's own code are ready. If `launch()` returns a non-null value but the screen remains blank, the issue typically lies within these other systems rather than the installation process.
:::

Once launched successfully, you can verify:

- The application interface appears in the window (dependent on the aforementioned systems being ready).
- After the application runs and writes data, its private directory appears: `/data/files/com.example.demo/`.
- Resources inside the application package can be accessed via `pkg://com.example.demo/<asset-path>` (operations can be performed via the `File` class).

## Uninstalling an Application

The uninstallation API is `AppletKit::removePackage(package)`. You pass in the package name, and it returns a `bool` indicating whether the package file was found and deleted:

```cpp
if (!kit.removePackage("com.example.demo"))
    LogError() << "uninstall failed: package not found";
```

Uninstallation guarantees the following effects externally:

- If the application is currently running, it is terminated first.
- Deletes the `.pkg` file from the first directory in the `packages()` list that contains it.
- Deletes the application's subdirectories under each data directory (`<package-name>/` under `AppletCache`/`AppletFiles`/`AppletTemp`/`AppletStorage`).
- Unregisters the application from the package database.

Verification after uninstallation:

- `/data/apps/com.example.demo.pkg` in the installation directory has disappeared.
- Data subdirectories such as `/data/files/com.example.demo/` have been cleared.
- `kit.installedApplets()` no longer contains `"com.example.demo"`.

## Advanced: System Pre-installed Application Directories

Many devices need to distinguish between two types of applications: **factory pre-installed, non-uninstallable** system applications, and **user-installed, uninstallable** user applications. By leveraging the sequential semantics of the `packages()` list, you can implement this layering using two directories.

### Use Cases

Factory pre-installed applications (such as system watch faces and settings apps) are typically flashed into read-only flash memory and should not be uninstallable or overwritable by the user. User-installed applications should reside in a writable partition and can be added or removed at any time. If both types are mixed into a single directory, subsequent application updates and uninstallation management become complex.

### Recommended Layout

Append two directories to `packages()`. Order matters: the pre-installed read-only directory comes first, followed by the user-writable directory:

```cpp
EnvPath::packages().emplace_back("/system/apps");  // Read-only pre-installed, placed first
EnvPath::packages().emplace_back("/data/apps");    // Writable user-installed, placed second
```

Looking back at the [Application Package Directories](#application-package-directories) in the first step, under this layout the semantics of the three operations are as follows:

- **Discovery** proceeds from front to back. Since the pre-installed directory comes first, factory apps take precedence, ensuring stable loading.
- **Installation** writes to the last directory in the list (the user area), ensuring newly installed apps do not pollute the pre-installed directory.
- **Uninstallation** proceeds from front to back, deleting from the first directory containing the package.

### Protection Mechanism: Call-side Whitelist

Sequential semantics only determine the storage path and startup discovery process for applications; they cannot prevent users from uninstalling pre-installed applications. The built-in <code>AppletKit&#8203;::&#8203;removePackage</code> has no concept of "pre-installed" or "protected." Therefore, the device's uninstallation entry point must be implemented by native code, which maintains a whitelist of pre-installed package names and intercepts calls before invoking `removePackage`: if a package hits the whitelist, uninstallation is refused.

The installation side does not require a whitelist. The device manufacturer's installation channels (app stores, preloaded pushes, etc.) are controlled by nature, and the legitimacy of application package names is guaranteed by the signature mechanism, which falls outside the scope of this layer. Furthermore, due to the masking effect of forward resolution (see "Known Limitations" below), runtime upgrades of pre-installed applications cannot take effect anyway, eliminating the need to additionally block overwrite installations. Thus, installation can directly call `kit.installPackage`.

A schematic of a native uninstallation wrapper layer:

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
    HashSet<String> m_preinstalled;
};
```

::: tip Read-only Mounting and Whitelists
Mounting the pre-installed partition as read-only is still recommended practice (to prevent accidental writes), but it is not a dependency for uninstallation protection. Even if the pre-installed directory is writable, the whitelist will intercept before `removePackage` is called.

The permission field of `EnvPath::Entry` does not participate in application package directory decisions; it only restricts JavaScript code access to application data directories.
:::

### Factory Reset

By leveraging the separation of pre-installed and user directories, a factory reset can be implemented by deleting all `.pkg` files in the user directory and resetting `pkgs.db`; pre-installed packages in the system directory remain unaffected. Runtime installations are hardcoded to write to `packages().back()` (the user directory) and never overwrite pre-installed copies in the system directory. Therefore, clearing the user directory and resetting the database allows pre-installed apps to still be parsed and loaded normally via `pkg://`.

Optionally, you can implement "uninstalling updates to pre-installed applications"—that is, deleting the updated copy of a pre-installed app in the user directory, causing it to fall back to the factory version in the system directory. This capability is currently only conceptually feasible and is not yet officially supported.

### Known Limitations

The following framework behaviors require active avoidance or attention from the native business layer:

1. **App store upgrades for pre-installed applications cannot be realized**. The current `pkg://<name>` resource resolution performs a forward traversal of the `packages()` list, while runtime installations are hardcoded to write to `packages().back()` (the user directory). If you attempt to upgrade a pre-installed app via runtime installation, the new version will land in the user directory but will be shadowed by the older version in the system directory due to forward matching, meaning it will never take effect. This upgrade capability is pending implementation.
2. **Uninstallation lacks the concept of "protected"**. `removePackage` locates packages solely via "first successful deletion," deleting packages from any directory indiscriminately without any "pre-installed" or "protected" markings. Whitelist interception must be implemented by the native caller; the framework does not provide this judgment.
3. **Uninstallation of watch face packages does not clean up the database**. `removePackage` only unregisters apps from the application table (`ADBT_Applet`) and does not clean up database entries for watch face packages (`ADBT_Dial`), leaving behind stale records. This is a framework todo item; native uninstallation logic must handle watch faces independently if support is required.
4. **The permission field of application package directory entries is ineffective**. The permission field of `EnvPath::Entry` does not participate in `packages()` list lookup/installation/uninstallation decisions; it only restricts JavaScript code access to application data directories. It cannot be used to express "installation prohibited in this directory."

## Platform Initialization Templates

Complete `EnvPath` configurations for three typical scenarios are provided below and can be copied directly and adjusted according to device paths. All configurations must be completed after `Application` construction and before <code>AppletKit&#8203;::&#8203;launch</code>/`installPackage`.

### Host Emulator

Minimal configuration, single directory for storing apps:

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

Separation of the pre-installed read-only partition and the user writable partition:

```cpp
EnvPath::setEntry(EnvPath::GlobalPackage, "/system/global.pkg");
EnvPath::setEntry(EnvPath::AppletCache,   "/data/cache");
EnvPath::setEntry(EnvPath::AppletFiles,   "/data/files");
EnvPath::setEntry(EnvPath::AppletMass,    "/data/mass");
EnvPath::setEntry(EnvPath::AppletTemp,    "/data/temp");
EnvPath::setEntry(EnvPath::AppletStorage, "/data/storage");

// Order-sensitive: pre-installed read-only directory first, user writable directory second
EnvPath::packages().emplace_back("/system/apps");
EnvPath::packages().emplace_back("/data/apps");
```

Once configured, you can install and launch applications according to steps two and three. We recommend using `AppletKit::NoVerify` to install a simple sample package during your first successful run, confirming that `.pkg` appears under `/data/apps` and `launch` returns a non-null value, before gradually restoring formal verification policies and pre-installed layouts.

============================================================
FILE_PATH: src/transl/EN/cxxdev/object-system.md

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

============================================================
FILE_PATH: src/transl/EN/cxxdev/README.md

# Native C++ Development

Glyphix is an application framework designed for embedded devices, providing a JavaScript-centric application development experience with a Vue Options API-like style. However, the core runtime of the framework is implemented in C++, allowing hardware vendors to extend and customize framework features using C++ — and this is where "Native C++ Development" comes into play.

This documentation is intended for C++ developers with embedded development experience. It aims to help you understand Glyphix's C++ extension mechanism and enable you to implement the following two types of features:

- **Native Module**: Encapsulates C++ functionalities into JavaScript-callable APIs, such as file access, hardware sensor reading, Bluetooth communication, and other system capabilities.
- **Native Widget**: Implements custom UI widgets using C++ and registers them as framework [components](/framework/component/native-component.md) for applications to use directly in their user interfaces, just like the built-in `div`, `image`, and `button` components.

::: tip
In application development, we use "component" to refer to UI elements, while at the C++ layer, we use "widget" to refer to UI elements. This documentation distinguishes between these two terms: **widgets** are concepts at the C++ layer, and **components** are concepts within the reactive framework.
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
      <div>Asynchronous Session<div class="remark">ResultSession · Signals</div></div>
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
      <div>IO/Time<span class="remark">Logger · Time</span></div>
    </div>
  </div>
  <div>
    Hardware / OS
    <div class="remark">RTOS · Linux · WASM</div>
  </div>
</ArchDiagram>

The bottom layer is the **Platform Abstraction Layer**, which is responsible for platform-dependent abstractions such as graphics rendering, input events, and the file system. This layer is typically implemented by device vendors or provided as a reference implementation for the corresponding platform by Glyphix.

Above it is the **C++ Core Framework**, containing the complete widget system (`Widget`), event dispatching, animation engine, layout system, and style engine. All UI elements are ultimately organized and rendered in the form of a C++ widget tree.

The next layer up is the **Reactive Framework**, which is responsible for bridging C++ core capabilities to JavaScript applications. It embeds a JavaScript engine (JerryScript or QuickJS) and implements bidirectional interaction between C++ and JavaScript via the `JsVM` and `JsValue` classes. AppletKit manages the complete lifecycle of applications (Applets), the component system implements reactive data binding and template rendering, and the asynchronous session framework maps C++ asynchronous operations to JavaScript Promises. The reactive framework itself is also implemented in C++.

The top layer is the **Application Sandbox**. Each running application (Applet) has an independent JavaScript execution environment (Realm) that is completely isolated from others. When an application exits, all resources within its sandbox are automatically reclaimed.

### System Collaboration Principles

The architectural diagram illustrates module partitioning but intentionally conceals the collaboration and coupling relationships between modules. In reality, the entire framework operates through a set of shared underlying mechanisms. Understanding these mechanisms helps you know "what you are doing and why you are doing it" in practice.

The entire framework is underpinned by a **Object System** that endows classes with runtime perception capabilities, including C++ class property reflection and event notification capabilities, as well as necessary lifecycle safety. Widgets, Native Modules, application frameworks, and asynchronous sessions all rely on this same foundation. For details, see the [Object System](./object-system.md).

**Widgets** form the UI skeleton through an object tree combined with drawing and event dispatching; the JavaScript application layer uses a **componentized** declarative programming model, and the two are naturally connected via object reflection capabilities such properties. Complex features like **Asynchronous Sessions** also rely on the object system's lifecycle model to ensure correctness.

Through the **Meta-Object Compiler** and other abstraction mechanisms, Glyphix does not require developers to handwrite binding code to expose C++-developed widget classes for JavaScript usage. At the same time, functional completeness is retained on the C++ side; theoretically speaking, you can develop a complete application directly in C++ (although it is not recommended).

### Programming Model

The Glyphix project does not restrict specific programming paradigms. For example, the object system is a classic object-oriented model, while the reactive framework provides application developers with a declarative, component-based development experience.

We do not encourage developers to practice "everything is an object," deliberately force design patterns, or pursue unnecessary abstractions. Our design principles lean more toward **pragmatism**, prioritizing the **resource constraints** and development efficiency of embedded systems.

## Documentation Conventions

### What is this document?

This is a guide for Glyphix Native C++ Development, **not** an API reference document. It introduces the framework's design philosophy, core mechanisms, and development workflow to help you understand how to extend framework capabilities, demonstrating specific implementation details through sample code.

During actual development, please be sure to refer to the API documentation distributed alongside the SDK; please contact your vendor for access.

### Sample Code Notes

All C++ code within the Glyphix framework resides under the `gx` namespace. The documentation assumes `using namespace gx;` by default, so class and function names do not carry the `gx::` prefix. For example:

```cpp
#include "gx_widget.h"

using namespace gx; // Assumed to be imported by default in documentation

class MyWidget : public Widget {
    // ...
};
```

Here, `Widget` is actually `gx::Widget`, but for brevity, we omit the namespace prefix.

::: tip C++ Learning Resources
If you primarily use C, are familiar with MCUs, RTOS, drivers, or LVGL, but have not systematically studied C++, we recommend reading the [C++ Learning Guide](./cpp-guide.md) first. It covers only the subset of C++ truly needed to enter Glyphix native development and organizes external resources suitable for embedded developers.
:::

## Development Path

Regardless of your goal, it is recommended to first thoroughly read the basic usage of `GX_OBJECT`, `GX_PROPERTY`, and `Signal` in the [Object System](./object-system) — they are used across all development scenarios.

Choose the appropriate documentation to continue reading based on your goals:

- [SDK Project Configuration](./sdk-setup): How to configure the build environment for an SDK project, including `glyphix_add_meta_objects()` registration, host building, and cross-compilation.
- [Native Module Development](./native-module): How to provide new system APIs for applications, such as fetching sensor data or calling underlying SDK functions.
- [Asynchronous Feature Development](./async): How to extend asynchronous features for applications, such as network requests, file IO, and time-consuming computations.
- [Widget Development Guide](./widget.md): How to implement new UI widgets (such as custom charts, special animation lists, etc.).
- [Widget Registration and Export](./widget-export.md): Registering custom widgets as framework components for direct application usage.

============================================================
FILE_PATH: src/transl/EN/cxxdev/async.md

# Asynchronous Feature Development

In embedded systems, many operations are time-consuming—such as reading flash memory, accessing the network, or waiting for hardware responses. If these operations are executed on the UI thread (which is also the rendering thread), it will freeze the UI and cause the application to become unresponsive.

Glyphix solves this problem by seamlessly integrating asynchronous operations with JavaScript's `Promise` mechanism. The C++ side handles the actual asynchronous logic (typically on another thread or via event-driven mechanisms), the JavaScript side waits for the result using `async/await` or `.then()`, and the UI remains smooth during the wait.

## Core Mechanism

The core of the asynchronous functionality is the "Session" model. When a JavaScript asynchronous call is initiated, the C++ side creates a **session object** (`AsyncSession`) and immediately returns a `Promise` to JavaScript. When the operation completes, the session drives the resolution (resolve or reject) of the `Promise`, and the `then/catch` or `await` on the JavaScript side is executed accordingly.

The session object is bound to the `Applet` that initiated the call. When the application exits, the session is automatically cleaned up, so developers do not need to manage memory manually.

The following diagram illustrates the position of the asynchronous session within the framework and its core components:

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
      <div>ResultSession<div class="remark">Single query · Promise bridging</div></div>
      <div>Signal&lt;T&gt;<div class="remark">Global event broadcasting</div></div>
    </div>
    <div class="group row">
      <div>Client Class<div class="remark">Pure C++ · No JS dependency</div></div>
      <div>SingleTimer<div class="remark">Timeout control</div></div>
    </div>
  </div>
  <div>
    Async Executor
    <div class="group row">
      <div>ThreadPool<div class="remark">Background execution by default</div></div>
      <div>Custom Context<div class="remark">Hardware driver · Event loop</div></div>
    </div>
  </div>
</ArchDiagram>

The asynchronous framework implementation is located in `gx_async.h` and encapsulated within the `gx::async` namespace. The framework provides several useful facilities:
- **`async::ResultSession`**: Used for single asynchronous queries, suitable for scenarios such as reading files and initiating network requests.
- **`async::make_timeout()`**: Used to create a one-shot timer to attach timeout functionality to a single session.
- **`async::Signal<T>`**: Used for global event broadcasting, suitable for scenarios such as device state changes and external event notifications.

## Single-Query ResultSession

`async::ResultSession<T>` is suitable for scenarios where you "initiate a query and wait for a single result," such as reading a file or making a network request. It is the most commonly used asynchronous pattern and works similarly to an asynchronous function call.

### Working Model

The complete lifecycle of a `ResultSession` is as follows:

1. **Creation**: The module function creates a session via `async::make<ResultSession<T>>(applet)`, and the session is automatically bound to the current `Applet`.
2. **Configuration**: Access the client object via `session->client()` to set the pure C++ parameters required for the task.
3. **Submission**: Call `session->request(resolver)` to submit the task, which immediately returns a `Promise` to JavaScript.
4. **Execution**: The framework forwards the client's `resolve()` method to the **asynchronous executor** (defaults to a background thread pool) for execution.
5. **Reporting**: After `resolve()` returns, the result is **automatically scheduled back to the UI thread** to drive the resolution or rejection of the `Promise`.
6. **Cleanup**: The session object is automatically destroyed after reporting is complete, or automatically cleaned up when the `Applet` exits.

::: important Client Class Isolation Requirements
The client class (i.e., the template parameter `T`) runs in the asynchronous context and **must not hold or access any objects that interact with JavaScript**, including `JsValue`, `Applet *`, or any other UI-thread-exclusive objects.

The client class should be a **pure C++ data processing unit**, holding only value-type data required to execute the task (such as `String`, `int`, or custom structures), and completing all work within the `resolve()` method. All interactions between the UI thread and the asynchronous thread are handled automatically by the framework.
:::

### Basic Usage

First, define a client class and implement the `resolve()` method. This method is called in the asynchronous context and returns a result wrapped in `async::Result<T>`:

```cpp
#include "gx_async.h"
#include "gx_file.h"

using namespace gx;

// Client class: Pure C++ data processing, holding no JS objects
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

Next, create a session in the module function and return a `Promise`. Note: You **must** use `Applet::resolveUri()` to perform security validation on the path passed from JavaScript, rather than blindly trusting the string provided by the application:

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

    // Submit the async task, passing the complete options object for quick-app callback compatibility
    session->request(ctx.arg(0));
    return session->promise();
}
```

::: tip Why pass `ctx.arg(0)`?
`request()` receives the entire `options` object passed from the JavaScript side (i.e., `ctx.arg(0)`), which is used to automatically adapt to both [calling styles](/api/README.md#快应用异步接口) of quick-app asynchronous interfaces:

- If `options` contains any of the `success`, `fail`, or `complete` properties, it is determined to be **callback style**, and the corresponding function is called directly. `request()` does not return a meaningful value;
- Otherwise, it is determined to be **Promise style**, creating a new `Promise`, and `session->promise()` returns this object for the caller to `await`.

This allows the exact same C++ implementation to simultaneously support both standard quick-app callback interfaces and modern Promise/async-await interfaces without any extra code. If you are certain that only the Promise style is supported, you can also pass an empty value `{}`.
:::

::: danger Do not skip URI validation
Directly using strings passed from JavaScript as file paths is a severe security vulnerability:

```cpp
// ❌ Dangerous! Bypasses sandbox path security checks
session->client().setPath(ctx.arg(0)["uri"].toString());
```

Malicious applications can access the file system outside the sandbox via path traversal (e.g., `../../etc/passwd`). All paths originating from JavaScript **must** be sanitized via `Applet::resolveUri()`, which detects path traversal attacks, cross-application unauthorized access, and illegal URI formats, returning an empty string when validation fails.
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

`async::Status` encapsulates an integer status code. `0` (i.e., `async::OK`) indicates success, and other values represent custom business error codes:

```cpp
// Success: Return value directly, status code is automatically OK
return async::Result<String>{std::move(content)};
// Failure: Return status code only, value part is ignored
return async::Status(404);
// Carry both partial results and a non-OK status (e.g., HTTP 206 Partial Content)
return async::Result<ByteArray>{
  std::move(partialData),
  async::Status(206)
};
```

When `resolve()` returns an error status, the `Promise` is rejected, and the JavaScript `catch` block receives an error object containing `message` and `code` fields. The `message` comes from the client class's `errorMessage()` static method.

`errorMessage()` supports multiple signatures, which the framework will automatically recognize:

```cpp
// Form 1: Accepts Status (recommended, concise)
static const char *errorMessage(async::Status status);

// Form 2: Accepts the complete Result, allowing message generation based on both value and status
static String errorMessage(const async::Result<MyType> &result);
```

If the client class does not define `errorMessage()`, the framework will use the default `"unknown async error"`.

### Value Types and JavaScript Conversion

The value returned by `resolve()` is not passed to JavaScript as-is. The framework uses the `js_cast()` function to automatically convert C++ types to `JsValue`, which then drives the resolution of the `Promise`. This process happens internally within the framework and appears "transparent," but it actually relies on a set of **implicit conventions**: only types that implement `js_cast()` specializations can be correctly converted. For custom enums, structs, and other types, conversion relationships must be explicitly established, otherwise compilation will fail.

#### Built-in Supported Types

The following types can be used directly as type parameters for `Result<T>` without extra work:

| C++ Type | Corresponding JavaScript Type | Remarks |
| --- | --- | --- |
| `int`, `double`, `float` | `number` | Direct numeric mapping |
| `bool` | `boolean` | Direct boolean mapping |
| `String`, `StringView`, `const char *` | `string` | Direct string mapping |
| `ByteArray` | `ArrayBuffer` | Binary data |
| `JsonValue` | `object` / `array` | JSON object or array |
| [`std::vector<T>`](https://en.cppreference.com/w/cpp/container/vector) | `Array` | Array, elements are recursively converted (`T` itself must also be convertible) |
| `JsValue` | Any | Passed directly without conversion |
| `void` (i.e., `Result<void>`) | `undefined` | No return value |

These types all have built-in `js_cast<T>()` specializations within the JsVM framework. Some of them are types that `JsValue` can construct directly, while others implement conversion logic via specializations.

#### Adding Conversion Support for Custom Types

If the type you are using is not in the above list, the compiler will throw an error indicating that `JsValue` cannot be constructed. There are two ways to resolve this:

**Approach 1: Define an `operator JsValue()` member function**

This is suitable for custom structs whose definitions you can modify. The advantage is that the conversion logic is built directly into the type definition, maintaining tight coupling:

```cpp
struct DeviceInfo {
    String model;
    int version;

    // Convert the struct into a JavaScript object
    // Note: Conversion executes on the UI thread, where a valid JsVM context is present
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

APIs such as `JsVM::current()` and `vm.newObject()` used inside `operator JsValue()` belong to the JsVM bridging layer. See [Native Module Development Documentation](./native-module.md#创建与返回对象) for details.

**Approach 2: [Specialize](https://en.cppreference.com/w/cpp/language/template_specialization) `js_cast<T>` in the `gx` namespace**

This is suitable for cases where you cannot modify the original type definition (such as types or enums defined externally):

```cpp
// Declare the specialization beforehand if necessary
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

::: tip Easy approach for integer enums
If enum values directly correspond to integers, manually converting them to `int` inside `resolve()` is the easiest way without needing any specialization:

```cpp
async::Result<int> resolve() {
    return async::Result<int>{int(myEnum)};
}
```
:::

#### Runtime Conversion Overhead

`js_cast()` is executed **after** the asynchronous result is delivered back to the UI thread, not in the asynchronous thread. The time overhead of conversion occurs entirely on the UI thread. For complex structures, you must ensure it is fast enough to avoid dropped frames. The actual costs for various types are as follows:

- **Zero-overhead types**: `int`, `double`, `bool`, `String`, and `const char *` are mapped directly via `JsValue` constructors with no extra copying or heap allocation. The `operator JsValue()` approach and `js_cast<T>` specializations are also inlined at compile time, with no virtual calls or layers of indirection.
- **Linear-overhead types**: `std::vector<T>` requires calling `setIndex()` element by element, with overhead proportional to the number of elements. If the returned structure is an object with fixed fields, prefer manually constructing a JS object using `operator JsValue()`, which is more efficient and readable than an array.
- **Tree-traversal types**: `JsonValue` recursively traverses the entire tree during conversion to construct JavaScript nodes one by one, representing the highest overhead among built-in types. If the data structure is known at compile time, `operator JsValue()` to construct the object directly is usually faster and avoids the construction cost of `JsonValue` itself.
- **Custom structs**: If you use `operator JsValue()` or `js_cast()` specializations, conversion performance depends on the conversion overhead of each member type, i.e., the complexity of constructing the object.

::: tip Simple heuristic rule
If your asynchronous data structure is simple (numeric values, simple struct objects, or small `JsonValues`), the conversion overhead typically will not affect UI smoothness.
:::

#### No Intermediate Serialization Layer

Some asynchronous frameworks require data passed between the worker thread and the UI thread to first be serialized into JSON or another self-describing format, and then deserialized on the UI thread. This is done to achieve thread-safe "type-erased" transmission, but at the cost of incurring string (or binary data stream) concatenation, transmission, and parsing overhead on every call. Worse still, it may construct multiple data copies (intermediate serialized data and raw data, etc.).

The async framework **does not rely on an intermediate serialization layer.** Results are moved across threads as native C++ values via `async::Result<T>`, completely bypassing the serialization process:

```
worker thread                  UI thread
resolve(Result<MyType>{...}) → js_cast(result.value()) → JsValue (JavaScript)
                  ↑
             Direct memory movement, no JSON strings
```

`js_cast()` is only executed after the result has safely returned to the UI thread. Its responsibility is to map C++ values to the JavaScript engine's internal representation, rather than acting as a communication protocol between threads.

If you proactively choose to use `JsonValue` as the type parameter for `Result<T>` (to mitigate template code bloat), you are introducing the overhead of `JsonValue`'s **construction and tree traversal**, not string serialization. `JsonValue` itself is also an in-memory tree structure, not a text format.

#### Template Code Size

`ResultSession<T>` is a template class, and the compiler generates a separate copy of code for each distinct client class type `T`. However, the framework extracts the vast majority of logic unrelated to `T` (such as `Promise` management, event delivery, and `Applet` lifecycle binding) into the non-template base class `detail::ResultSession`. Therefore, the actual extra code added per `T` is primarily concentrated in the thin `Resolver` adapter layer.

However, if there are **a large number of fine-grained client types used only once** in a project, the cumulative number of instantiations can still lead to significant code size growth.

A common mitigation technique is to use `JsonValue` as a type-erasure medium, combining multiple scattered small functions into a single client class:

```cpp
// Before combination: Each operation is an independent client class + independent template instantiation
struct GetVersionClient { ... };   // ResultSession<GetVersionClient>
struct GetModelClient   { ... };   // ResultSession<GetModelClient>
struct GetSerialClient  { ... };   // ResultSession<GetSerialClient>

// After combination: Share the same template instantiation, distinguishing operations at runtime
struct DeviceQueryClient {
    enum Kind { Version, Model, Serial } kind;

    // A switch dispatch is shown here for demonstration; function pointers can also be used.
    // However, do not use BaseClient combined with derived classes overriding resolve() 
    // for polymorphism, as it introduces more vtable bloat than the function pointer approach.
    async::Result<JsonValue> resolve() {
        switch (kind) {
        case Kind::Version: return JsonValue{getVersion()};
        case Kind::Model:   return JsonValue{getModel()};
        case Kind::Serial:  return JsonValue{getSerial()};
        }
    }
};

// Three module functions share the single ResultSession<DeviceQueryClient> instantiation
static JsValue getVersion(JsCtx ctx) {
    using Session = async::ResultSession<DeviceQueryClient>;
    auto *session = async::make<Session>(applet);
    session->client().kind = DeviceQueryClient::Version;
    return session->request(ctx.arg(0));
}
```

The tradeoff of this approach is that the return type degenerates to `JsonValue`, incurring additional runtime conversion overhead (see above). Therefore, it is suitable for scenarios with **small data volumes and many functions**, trading a small amount of runtime overhead for meaningful code size gains. For data-intensive or performance-sensitive operations, independent strongly-typed client classes should still be retained.

### Custom Asynchronous Contexts

By default, `session->request()` submits `resolve()` to the framework's **asynchronous executor**—typically a background thread pool. However, some scenarios require using a different asynchronous context, such as a custom event loop or AIO multiplexing mechanism, which do not want to consume extra thread resources.

In this case, you can bypass `request()` and manually control the asynchronous execution flow directly. The client class also does not need to implement the `resolve()` execution function. The key is: **after completing work in the asynchronous context, call `session->resolve()` to deliver the result back to the UI thread**.

```cpp
// Client class: No need to implement resolve(), as the default thread pool is not used
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
        // The callback may run on any thread—the framework automatically schedules it back to the UI thread
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
- `request()` performs both "setting the resolver" and "submitting to the async executor" in one go;
- In manual mode, you need to call `setResolver()` yourself to set the response target, and then push the result or error status via `session->resolve()` at any arbitrary time.

`resolve()` is thread-safe; it packages the result as an event, delivers it back to the UI thread, and then completes the resolution of the `Promise`.

::: tip When to use custom contexts
- The underlying driver already provides a callback interface, and you do not want to create extra threads: `resolve` directly inside the driver callback.
- You need to integrate with an existing AIO/epoll event loop: `resolve` inside the event completion callback.
- You need sequential execution (e.g., operations must be ordered): dispatch via your own task queue and `resolve` upon completion.

As long as you ensure `session->resolve()` is eventually called once, the framework does not care which thread the result is delivered from.
:::

### Value Type Semantics

Since the `async::Result<T>` value returned by `resolve()` (or actively posted by a custom async context) is posted to the UI thread and then converted to `JsValue`, the data type `T` must be movable. Built-in supported types all meet this requirement. For custom types:
- If it is a struct containing only members of built-in supported types, the C++ standard guarantees it is movable.
- If raw pointers are used and you manage their ownership yourself, you need to correctly implement the [move constructor](https://en.cppreference.com/w/cpp/language/move_constructor).
- [Trivial types](https://en.cppreference.com/w/cpp/named_req/TrivialType) (such as pure C structs, enums, etc.) satisfy value type semantics by default.

Note that non-trivial types typically contain resources on the heap, and the following pattern may face peak memory issues:

```cpp
auto *session = getFetchLargeDataSession();
std::vector<uint32_t> data = fetchDataFromNetwork(url);
session->resolve<decltype(data)>(data);  // Results in a full copy of data
```
This is because the parameter of `session->resolve()` is passed by value, and passing `data` invokes the [copy constructor](https://en.cppreference.com/w/cpp/language/copy_constructor), resulting in a full copy. If `data` is large, this will double memory usage. In such cases, you will encounter compilation warnings like this:
```
'...' is deprecated:
avoid use copy semantics of Result<T> if T is not trivially copyable
```
The correct approach is to explicitly enable move semantics using [`std::move()`](https://en.cppreference.com/w/cpp/utility/move):

```cpp
auto *session = getFetchLargeDataSession();
std::vector<uint32_t> data = fetchDataFromNetwork(url);
session->resolve<decltype(data)>(std::move(data));  // Use move semantics
```

### Timeout Control

For asynchronous operations that may remain unresponsive for a long time, use `async::make_timeout()` to add timeout protection to the session. Upon timeout, the `Promise` is automatically rejected, preventing the JavaScript side from hanging indefinitely.

The following code snippet shows a basic example demonstrating how to use timeout control in a network request:

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

#### Working Principle

The key workflow of `make_timeout()`:

1. **Moves** the client data of `session` into an internal class; `session->client()` must not be accessed after this.
2. Starts a one-shot timer, returning a `SharedRef<SingleTimer>` handle.
3. **Normal Path**: Call `handle->resolve()` before the timeout. This atomically takes ownership of the session and posts the result event. When the timer subsequently triggers, it sees the session is already empty and takes no action.
4. **Timeout Path**: The timer triggers and executes the callback **on the UI thread**. The developer calls `session->fulfill()` in the callback to post the error status. After the callback returns, the timer is responsible for `delete session`.
5. **App Exit**: When the `Applet` is destroyed, the timer is automatically unbound, the session is deleted, and the callback is not triggered.

This mechanism is particularly useful for scenarios where asynchronous operations lack built-in timeout mechanisms, such as certain network request implementations. As is well known, correctly implementing timeout protection can be tricky, as you must correctly handle race conditions and lifecycle safety issues across all execution paths.

`make_timeout()` relies on these prerequisites to guarantee safety:
- The client type (i.e., `T` in `ResultSession<T>`) must be **movable**, which is somewhat of a legacy restriction.
- Asynchronous operations must support safe cancellation on the UI thread, which means removing task listeners and releasing references to `handle`.

#### Callback Thread and `fulfill()`

The timeout callback (the third parameter of `make_timeout()`) **always executes on the UI thread** because it is triggered by a timer (`Timer`), and timer events are dispatched by the main event loop.

This dictates that you **must only** use `session->fulfill()` rather than `session->resolve()` within the callback:

| Method | Callable Thread | Impact on Session |
| --- | --- | --- |
| `resolve(result)` | Any thread | Posts a Consume event; session is **deleted** after being processed on the UI thread |
| `fulfill(result)` | **UI Thread Only** | Dispatches the result directly **without deleting** the session |

The timeout path of `make_timeout()` is handled by the timer itself, which executes `delete session` after the callback finishes. If you call `session->resolve()` inside the callback, it will also post an event to delete the session, creating a **double free** conflict with the timer's `delete`, leading to undefined behavior. `fulfill()` only posts the result without touching the session lifecycle, making it the only safe choice inside the callback.

`fulfill()` accepts an `async::Result<R>` or directly accepts an `async::Status` (shorthand when there is no result value):

```cpp
auto handle = async::make_timeout(session, 5000, [](Session *s) {
    s->fulfill(async::Status(408)); // Populate error status only
    // Or carry both value and status:
    s->fulfill(async::Result<String>{"partial", async::Status(206)});
    // ❌ Do not call s->resolve(), as it will form a double free with the timer's delete session
});
```

::: tip
The decision rule is simple: Where does the session ownership lie, and who is responsible for deletion?
- **Normal Path**: `handle->resolve()` atomically takes ownership of the session internally, and the session is deleted after the Consume event is processed.
- **Timeout Callback**: The timer takes ownership of the session and deletes it after the callback finishes. Therefore, you can only use `fulfill()` to post results inside the callback.
:::

#### Accessing Client Data

If the timeout callback needs to read client data to determine the error strategy, use the extended callback signature `(Session *, const T &)`. **Do not** call `session->client()` inside the callback—the client has already been moved into the timer:

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

When a timeout occurs, you need to cancel ongoing asynchronous tasks within the callback to release references to `handle`. `SingleTimer` manages its lifecycle using reference counting—if an asynchronous operation holds a reference to `handle` but never completes, a memory leak will occur:

```cpp
auto task = AioTask::create();
auto handle = async::make_timeout(session, 5000,
    [task](auto *s) {
        task->cancel();     // Cancel task, releasing reference to handle
        s->fulfill(async::Status(408)); // reject Promise
    });

// Task completion callback holds a reference to handle
task->start([handle = std::move(handle)](auto &result) {
    handle->resolve(result);
});
```

::: important
The `handle` returned by `make_timeout()` **must** also be referenced by the asynchronous task (captured by the lambda in the example above) to ensure the timer is not destroyed before the task completes. Otherwise, it will immediately trigger the timeout callback and `Promise` rejection, preventing the task from completing normally.
:::

Such memory leaks are caused by two reasons:
1. **Async framework leak**: The `handle` reference is forgotten, causing the related session object to remain unreleased.
2. **Underlying task leak**: The asynchronous task itself blocks in an uncompleted state, leaving related resources uncleaned.

### Automatic Cleanup on Application Exit

When an `Applet` is destroyed (e.g., the user closes the app, or the system reclaims resources), all asynchronous sessions bound to that `Applet` are automatically cleaned up:

- The session's `unbind()` method is called, which closes the session and releases the `Promise` reference.
- If `make_timeout` is being used, the timer is similarly unbound, and the internally held session is deleted.
- The `Promise` on the JavaScript side will never be resolved or rejected—but since the JavaScript environment itself is being destroyed at this point, this is safe.

This means you **do not** need to manually track and cancel asynchronous tasks—the framework guarantees that the following will not happen:
- Delivering results to a destroyed `Applet`, causing access to dangling pointers.
- Executing callbacks in a released JavaScript environment.
- Asynchronous sessions leaking after application exit.

Specifically, when a background thread calls `resolve()` to post a result to the UI thread, the handling function checks whether `applet()` is still valid. If the `Applet` has already been destroyed, causing `applet()` to return `nullptr`, the framework safely discards the result without executing any JavaScript operations.

::: tip Safe Return in Asynchronous Contexts
Since `resolve()` is pure data posting (via the event queue), calling `resolve()` in a background thread will not crash even if the `Applet` has already been destroyed. The background thread does not need to care about the survival state of the `Applet`; that is the framework's responsibility.
:::

The only thing to note is that if you derive from `ResultSession` and introduce other `JsValue` member variables, you need to clean up these members in `unbind()` to avoid memory leaks:

```cpp
class MySession : public async::ResultSession<MyClient> {
public:
    void unbind() override {
        m_callbacks = {}; // Clean up any held JsValues to avoid leaks
        async::ResultSession::unbind(); // Call base class cleanup
    }

private:
    JsValue m_callbacks; // Members that need manual cleanup
};
```

::: important `ResultSession` Lifecycle Extension
If there are still incomplete asynchronous sessions when the application exits, the framework only cleans up application-related resources (such as `Promise` references, binding relationships, etc.), but **does not destroy the session object itself**. This manifests as the lifetime of the `ResultSession` being extended until the asynchronous operation completes.

While this is meant to guarantee memory safety, it causes some resources to be released less promptly. Therefore, asynchronous tasks must ensure they complete within a finite time and cannot hang indefinitely.
:::

## Multi-Query ListenSession

This category of APIs is still unstable and is not yet open for use.

## Global Event Broadcasting async::Signal

If a C++ event needs to be broadcast to **multiple applications** (rather than targeting a specific caller), use `async::Signal<T>`. It "multicasts" underlying hardware or system events to all JavaScript listeners subscribed to it.

`async::Signal<T>` and `ResultSession` have different positioning:

| Feature | ResultSession | Signal |
| --- | :---: | :---: |
| Communication Direction | One-to-one (Caller → Result) | One-to-many (Event Source → All Subscribers) |
| Trigger Count | Single | Multiple |
| Bound Object | Single Applet | Cross-Applet |
| Applicable Scenarios | Asynchronous queries, requests | System events, state changes |

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

This module function allows the JavaScript side to subscribe to the signal, and it returns a binding ID for the JavaScript side to unsubscribe:

```cpp
static JsValue subscribeBatteryChange(JsCtx ctx) {
    if (ctx.argc() < 1 || !ctx.arg(0).isFunction())
        return {};
    // Must be in a valid applet environment to subscribe
    auto *applet = Applet::current(ctx.vm());
    if (applet == nullptr) return {};

    // Bind slot to the applet, automatically unsubscribing when the app exits
    auto *slot = batteryChanged.connect(ctx.arg(0));
    return applet->bindObject(slot); // Return slot ID for JavaScript to cancel
}
```

You also need to implement a module function for unbinding. Regardless of the `async::Signal` type, the implementation of the unbind function is very fixed:

```cpp
static JsValue unsubscribeBatteryChange(JsCtx ctx) {
    auto *applet = Applet::current(ctx.vm());
    if (applet && ctx.argc()) {
        // slotId defaults to 0, which can be safely ignored without performing any operation
        auto slotId = ctx.arg(0).toInt();
        // After unbinding the slot from the applet, the slot object must also be deleted
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
    // The battery module typically has functions like getLevel(), omitted here
    mod["subscribe"] = subscribeBatteryChange;
    mod["unsubscribe"] = unsubscribeBatteryChange;
    return mod;
}
// Don't forget to import the module using GX_JSVM_MODULE_IMPORT
GX_JSVM_MODULE(vendor_battery, "vendor.battery", createBatteryModule)
```

::: tip Reusing the `unsubscribe` function
Since the implementation of the unbinding function is very generic, you can define a general `unsubscribe` function and import it into multiple modules for use.
:::

On the JavaScript side:

```js
import battery from '@vendor.battery'

const sid = battery.subscribe((level) => {
  console.log('battery level:', level)
})

// Call when unsubscribing is needed
battery.unsubscribe(sid)
```

### Signal Delivery Modes

`Signal` supports two delivery modes, controlled by the second parameter:

```cpp
// Normal mode (default): Notify all subscribers
batteryChanged(newLevel, async::NormalSignal);

// Skip invisible apps: Only notify foreground visible apps, reducing unnecessary consumption
batteryChanged(newLevel, async::SkipInvisible);
```

The `SkipInvisible` mode is suitable for events that only make sense when the UI is visible (such as interface refresh notifications). For events that require background awareness (such as low battery warnings), the default `NormalSignal` should be used.

### Signal Value Types

The type parameter `T` of `Signal<T>` follows the exact same conversion rules as `ResultSession`: when a signal is triggered, the framework converts C++ values to JavaScript callback parameters via the same `js_cast()` mechanism. Built-in types such as `int`, `bool`, `String`, and `JsonValue` can be used directly; if you need to pass custom structs or enums, refer to the methods in the [Value Types and JavaScript Conversion](#value-types-and-javascript-conversion) section.

## Thread Safety Notes

The thread safety model of the asynchronous framework follows these rules:

- **`resolve()` is thread-safe**: `ResultSession::resolve()` and `SingleTimer::resolve()` can be called on any thread. They post results to the UI thread via the event system and do not directly manipulate JavaScript objects.
- **`JsValue` is not thread-safe**: `JsValue` manages its lifecycle using reference counting, and its reference counting operations are non-atomic. You must not create, copy, destroy, or access `JsValue` in an asynchronous thread. This is precisely why client classes must not hold `JsValue`.
- **`Promise` resolution executes on the UI thread**: Regardless of which thread `resolve()` is called from, the final JavaScript `Promise` callback always executes on the UI thread, ensuring UI operation safety.
- **`async::Signal` notifications are dispatched on the UI thread**: Although `async::Signal::operator()` can be called across threads, JavaScript callbacks always execute on the UI thread.

If the client class needs to share state with the UI thread (such as providing a cancellation flag), use atomic operations like [`std::atomic`](https://en.cppreference.com/w/cpp/atomic/atomic) or mutexes to protect shared data:

```cpp
class CancellableClient {
public:
    void cancel() { m_cancelled.store(true); }

    async::Result<String> resolve() {
        for (int i = 0; i < 100 && !m_cancelled.load(); ++i) {
            // Execute step-by-step task, periodically checking the cancellation flag
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

Notably, many value types in the Glyphix framework **are** safe to pass across threads **within this asynchronous framework**, such as:
- `String`: Can be assigned and accessed directly across multiple threads without extra synchronization mechanisms.
- `JsonValue`: This class is also a value type and possesses the same thread-safety characteristics as `String`.
- `ByteArray`: Similar to `String`, supports cross-thread usage.
- `SharedRef<T>`: The reference-counted smart pointer itself can be passed across threads, but the thread safety of the managed object `T` depends on its definition.
- Non-owning types such as `String::View` **cannot** be used across threads.

This is why in all the preceding examples we always directly capture and pass types like `String` across asynchronous contexts without special handling, and without needing to use synchronization mechanisms like mutexes.

::: important
The thread safety of the aforementioned types actually relies on the specific asynchronous framework memory model, meaning they are **not automatically thread-safe** in all scenarios. The asynchronous framework in this document guarantees this, but it cannot be generalized to any situation.
:::

============================================================
FILE_PATH: src/transl/EN/cxxdev/widget.md

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

============================================================
FILE_PATH: src/transl/EN/cxxdev/async-examples.md

# Asynchronous Development Examples

If you feel that the chapter on [Asynchronous Feature Development](async.md) is too lengthy and not intuitive enough, this document provides some typical and simpler examples to help you handle common asynchronous development scenarios.

These scenarios are not extremely complex, but they focus on:
- A typical asynchronous call pattern, with an emphasis on cross-thread and cross-language calling relationships;
- Scenarios that may be more trivial, involving a large batch of system APIs that need to be integrated, making them sensitive to code bloat;
- Typical C API interaction requirements rather than standard C++ interfaces.

You can find complete implementations of these scenarios in the SDK samples and simulate running them directly on your PC.

## Scenario: Interfacing with a C Alarm Interface

A common asynchronous pattern in embedded systems is the "C callback": the caller submits a task, passes a function pointer as a completion notification, and the worker thread calls the callback once the operation is complete.

::: important async only supports the thread model
The asynchronous features of the Glyphix framework only support normal thread contexts and cannot be used in interrupts. If your asynchronous context is an interrupt service routine, you should provide a thread to act as a bridge.
:::

Here, we take an alarm service as an example. Its provided C asynchronous interface looks like this:

```c
// Taking alarm_async_create as an example; other operations have similar forms
void alarm_async_create(AlarmService *svc, uint32_t interval_ms, ...,
                        alarm_create_cb_t done_cb, void *done_ctx);

// Function pointer type for the completion callback, called on the worker thread
typedef void (*alarm_create_cb_t)(alarm_err_t err, alarm_id_t id, void *ctx);
```

Next, we will explain how to bridge such typical C callback interfaces to JavaScript Promises.

### Multiple Operations Sharing a Session Type

The alarm service has a batch of operations such as `create`, `cancel`, `setEnabled`, `update`, `snooze`, `getInfo`, `list`, and `count`. Defining a separate client class for each operation would generate a large number of template instantiations.

For such scenarios where "the actual logic is completed in the C layer, and the C++ side only handles parameter passing," you can define a lightweight client containing only error code mapping, allowing all operations to share a single `ResultSession` instantiation:

```cpp
struct AlarmClient {
    // Converts the C layer's alarm_err_t to a readable error string
    // to be passed to the JavaScript side's catch when the Promise is rejected.
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

`AlarmClient` does not need to implement the `resolve()` method because the default thread pool executor is not used here; the actual asynchronous operations are completed by the alarm service's worker thread, and the C++ side is only responsible for posting the results back to the UI thread.

### Basic Binding Pattern

Taking `alarm.create()` as an example, this demonstrates the complete binding process:

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

    // Create a session and extract resolve/reject callbacks from the options object (supporting both async styles)
    auto *session = async::make<AlarmSession>(applet);
    session->setResolver(opts);

    // C callback: called in the worker thread, notifying JavaScript across threads via resolve()
    auto done = +[](alarm_err_t err, alarm_id_t id, void *data) {
        auto *s = static_cast<AlarmSession *>(data);
        s->resolve(err == ALARM_OK
            ? async::Result<int>(id) // Success: resolve the newly created alarm ID
            : async::Status(err));   // Failure: reject, with the error message coming from errorMessage()
    };

    // Call the C service's asynchronous alarm creation interface, passing the callback and session pointer
    alarm_async_create(AppletAlarmService::instance(),
                       intervalMs, mask, label.c_str(), /*...*/,
                       onAlarmFired, nullptr, done, session);
    // Return the Promise object to JavaScript; the framework will automatically settle it when resolve() is called
    return session->promise();
}
```

There are a few fixed patterns here that you can copy and use directly:

- `async::make<AlarmSession>(applet)` creates a session and binds it to the current Applet to meet lifecycle requirements.
- `session->setResolver(opts)` enables the same codebase to support both [callback style and Promise style](/api/README.md#快应用异步接口) asynchronous calls.
- `+[](... void *data)` converts the lambda into a normal function pointer via the unary `+` operator, satisfying the type requirements of C callbacks.
- Pass `session` as `void *` transparently to the C API, cast it back in the callback, and then call `resolve()`.
- `resolve()` is thread-safe; it encapsulates the result as an event and posts it back to the UI thread to drive the resolution of the Promise.

::: tip Writing callbacks using lambda expressions
In C, callback functions are typically static functions. You can use C++ lambda expressions to define callback functions locally and nested nearby, for example:
```cpp
auto done = +[](alarm_err_t err, alarm_id_t id, ...) { ... }
alarm_async_create(..., done, session);
```
This avoids defining a large batch of separate static functions, making the code more compact and clear.
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
        // When there is no return value, resolve<void> can be used
        static_cast<AlarmSession *>(data)->resolve<void>(async::Status(err));
    };
    alarm_async_cancel(AppletAlarmService::instance(), id, done, session);

    return session->promise();
}
```

::: important Do not omit parameter checks
`session->setResolver(ctx.arg(0))` relies on checking `ctx.argc()`. If the function does not check the parameter count at the beginning, you must check it when calling `setResolver()`:
```cpp
session->setResolver(ctx.argc() ? ctx.arg(0) : JsValue{});
```
:::

### Registering Type Conversions for Custom C Structs

`alarm.getInfo()` returns an `alarm_info_t` struct, which needs to be converted into a JavaScript object. To achieve this, first specialize `js_cast<T>` within the `gx` namespace:

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

Once specialization is complete, you can directly pass the struct instance to `resolve()` within the binding function:

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
`js_cast()` is called by the framework only after the result returns to the UI thread, not executed in the worker thread. This means you can safely use UI-thread-exclusive APIs such as `JsVM::current()` inside `js_cast()`.
:::

For cases like `alarm.list()` which return an array, you can directly construct a `std::vector<int>` and resolve it without defining additional type conversions:

```cpp
auto done = +[](alarm_err_t /*err*/, const alarm_id_t *ids, int count, void *data) {
    auto *s = static_cast<AlarmSession *>(data);
    s->resolve<std::vector<int>>(std::vector<int>{ids, ids + count});
};
alarm_async_list(AppletAlarmService::instance(), done, session);
```

### Alarm Trigger Callback: Sending Events Back to JavaScript

When an alarm triggers, the C layer calls the `alarm_fire_cb_t` callback from the worker thread. This scenario differs somewhat from the previous "query results" pattern and requires a specially designed event notification mechanism.

#### Why Not Use JavaScript Callback Functions

Intuitively, it might seem reasonable to let the application pass a callback function when registering an alarm:

```javascript
// ❌ This does not work for the alarm scenario
alarm.create({ interval: 60000, onFired: (event) => { /* ... */ } })
```

The problem is that alarms span the application's lifecycle: after an alarm is created, the application may be killed at any time before the alarm fires; many devices also support triggering alarms after a reboot.

A JavaScript callback function (`JsValue`) is only valid within the JavaScript runtime of the current application instance. Once the application is closed, this runtime along with all `JsValue`s will be destroyed. At that point, the C++ side has no way to retain this JavaScript callback, let alone call it when the alarm fires.

This is not just a problem for alarms; **any event that may trigger across application lifecycles cannot be solved via JavaScript callbacks**, such as scheduled tasks, offline message push, background download completion notifications, etc.

#### Using Convention Method Names Instead of Callback References

The simplest solution is: instead of the application "registering a callback," the system actively **launches** the application when an event occurs and calls a processing method on the application object using a pre-arranged method name.

This aligns with the approach of application lifecycle functions (`onCreate`, `onShow`, etc.)—the system starts the application on demand and calls a known entry method rather than holding onto a pre-registered callback. The application side implements the corresponding method by convention:

```javascript
// app.js — Processing method exported by the application model object (implemented by convention)
export default {
  onAlarmFired(event) {
    // event: { id, label, interval, ... }
    console.log('alarm fired:', event)
  }
}
```

C++ side implementation: first read the snapshot on the worker thread, then switch back to the main thread to start the application and call the method:

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
        // Call the convention method on the exported object of app.js, with the event parameter being the JS object of the alarm info
        JsValue event = js_cast(info);
        applet->modelObject().callMethod("onAlarmFired", {event}).reportError();
    });
}
```

Key points:

- **Do not** directly operate on `JsValue` or call any JavaScript APIs in the worker thread; they can only be used on the UI thread.
- Use `App()->postTask()` to post closures to the main event loop for execution. This is the simplest way to switch back to the UI thread.
- Use `AppletKit::launch()` instead of searching for an existing instance; `launch()` restarts the application if it does not exist, and returns the existing instance if it is already running.
- `.reportError()` on the return value of `callMethod()` prints potential JavaScript exceptions to the log rather than silently ignoring them.

::: tip Convention method names are the simplest event handling method
You can think of this pattern as: the exported object of app.js is simply the "set of entry points" exposed by the application to the system. The system calls methods within it when needed, just like calling `onCreate` or `onShow`.

This method is not universally applicable, but it is basically sufficient for controlled system applications, and it is simple to implement without requiring complex persistence and callback management mechanisms.
:::

### Registering the Library Loader

Once all binding functions are written, they need to be "assembled" into a [library object](native-module.md#library-loader) that JavaScript can import, and registered into the framework.

A library loader is a C++ function triggered when an application calls `app.loadLibrary('vendor.alarm')`. It is responsible for creating and returning a JavaScript object containing all exported methods:

```cpp
static JsValue libAlarmLoader(Applet *applet) {
    // You can check the application's package name here to reject unauthorized apps, or check fields.
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

Then register the loader into `AppletKit` during the initialization stage:

```cpp
AppletKit kit{&window};
kit.setLibraryLoader("vendor.alarm", libAlarmLoader);
```

Import it on the JavaScript side via `app.loadLibrary()`, and the return value will be the library object returned by the loader:

```javascript
const alarm = app.loadLibrary('vendor.alarm')

const id = await alarm.create({ interval: 60000, label: 'Get up' })
```

