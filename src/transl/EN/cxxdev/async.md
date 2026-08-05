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