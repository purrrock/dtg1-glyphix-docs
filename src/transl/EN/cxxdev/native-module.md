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