# Asynchronous Development Examples

If you feel that the chapter on [Asynchronous Feature Development](async.md) is too extensive and not intuitive enough, this document provides some typical and relatively simple examples to help you handle common asynchronous development scenarios.

These scenarios are not extremely complex, but they focus on:
- A typical asynchronous call pattern, emphasizing cross-thread and cross-language call relationships;
- Scenarios that may be more trivial, with a large number of system APIs to interface with, making them sensitive to code bloat;
- Typical C API interaction requirements rather than standard C++ interfaces.

You can find the complete implementations of these scenarios in the SDK samples and simulate running them directly on your PC.

## Scenario: Interfacing with a C Alarm API

A common asynchronous pattern in embedded systems is the "C callback": the caller submits a task and passes a function pointer as a completion notification. Once the operation is complete, a worker thread invokes the callback.

::: important async only supports the thread model
The asynchronous features of the Glyphix framework only support normal thread contexts and cannot be used in interrupts. If your asynchronous context is an interrupt handler, you should provision a thread to act as a relay.
:::

Here, we use an alarm service as an example. Its provided C asynchronous interface looks like this:

```c
// Taking alarm_async_create as an example, other operations have a similar form
void alarm_async_create(AlarmService *svc, uint32_t interval_ms, ...,
                        alarm_create_cb_t done_cb, void *done_ctx);

// Function pointer type for the completion callback, invoked on the worker thread
typedef void (*alarm_create_cb_t)(alarm_err_t err, alarm_id_t id, void *ctx);
```

Next, we explain how to bridge such a typical C callback interface into a JavaScript Promise.

### Multiple Operations Sharing a Session Type

The alarm service has a batch of operations such as `create`, `cancel`, `setEnabled`, `update`, `snooze`, `getInfo`, `list`, and `count`. If you define a separate client class for each operation, it will generate a large amount of template instantiation.

For scenarios where "the actual logic is entirely completed on the C layer, and the C++ side only handles parameter passing," you can define a lightweight client containing only error code mappings and let all operations share a single `ResultSession` instantiation:

```cpp
struct AlarmClient {
    // Maps alarm_err_t from the C layer to a readable error string
    // to pass to catch on the JavaScript side when the Promise is rejected.
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

`AlarmClient` does not need to implement the `resolve()` method because the default thread pool executor is not used here; the actual asynchronous operations are completed by the alarm service's worker thread, and the C++ side is only responsible for posting the result back to the UI thread.

### Basic Binding Pattern

Taking `alarm.create()` as an example, here is the complete binding process:

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

    // Create a session and extract resolve/reject callbacks from the options object (supports both async styles)
    auto *session = async::make<AlarmSession>(applet);
    session->setResolver(opts);

    // C callback: invoked in the worker thread, notifies JavaScript cross-thread via resolve()
    auto done = +[](alarm_err_t err, alarm_id_t id, void *data) {
        auto *s = static_cast<AlarmSession *>(data);
        s->resolve(err == ALARM_OK
            ? async::Result<int>(id) // Success: resolve with the new alarm ID
            : async::Status(err));   // Failure: reject, error message comes from errorMessage()
    };

    // Call the C service's asynchronous alarm creation interface, passing the callback and session pointer
    alarm_async_create(AppletAlarmService::instance(),
                       intervalMs, mask, label.c_str(), /*...*/,
                       onAlarmFired, nullptr, done, session);
    // Return the Promise object to JavaScript; the framework will automatically settle it when resolve() is called
    return session->promise();
}
```

There are a few fixed patterns here that can be copied directly for use:

- `async::make<AlarmSession>(applet)` creates a session and binds it to the current Applet to satisfy lifecycle requirements.
- `session->setResolver(opts)` allows the same code to support both [callback style and Promise style](/api/README.md#快应用异步接口) asynchronous calls.
- `+[](... void *data)` converts the lambda to a regular function pointer via the unary `+` operator, satisfying the type requirements of the C callback.
- Passes `session` as `void *` transparently to the C API, casts it back in the callback, and then calls `resolve()`.
- `resolve()` is thread-safe; it packages the result as an event and posts it back to the UI thread to drive the settlement of the Promise.

::: tip Writing callbacks using lambda expressions
In C, callback functions are typically static functions. You can use C++ lambda expressions to nest and define callback functions directly nearby, for example:
```cpp
auto done = +[](alarm_err_t err, alarm_id_t id, ...) { ... }
alarm_async_create(..., done, session);
```
This avoids defining a large batch of separate static functions, making the code more compact and clearer.
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
        // When there is no return value, use resolve<void>
        static_cast<AlarmSession *>(data)->resolve<void>(async::Status(err));
    };
    alarm_async_cancel(AppletAlarmService::instance(), id, done, session);

    return session->promise();
}
```

::: important Do not omit parameter checks
`session->setResolver(ctx.arg(0))` relies on checking `ctx.argc()`. If the number of parameters is not checked at the beginning of the function, check it when calling `setResolver()`:
```cpp
session->setResolver(ctx.argc() ? ctx.arg(0) : JsValue{});
```
:::

### Registering Type Conversion for Custom C Structs

`alarm.getInfo()` returns an `alarm_info_t` struct, which needs to be converted into a JavaScript object. To do this, first specialize `js_cast<T>` in the `gx` namespace:

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

Once specialization is complete, pass the struct instance directly to `resolve()` in the binding function:

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
`js_cast()` is called by the framework only after the result returns to the UI thread; it does not execute on the worker thread. This means you can safely use UI-thread-exclusive APIs like `JsVM::current()` inside `js_cast()`.
:::

For cases like `alarm.list()` which return arrays, you can construct a `std::vector<int>` directly and resolve it without defining additional type conversions:

```cpp
auto done = +[](alarm_err_t /*err*/, const alarm_id_t *ids, int count, void *data) {
    auto *s = static_cast<AlarmSession *>(data);
    s->resolve<std::vector<int>>(std::vector<int>{ids, ids + count});
};
alarm_async_list(AppletAlarmService::instance(), done, session);
```

### Alarm Trigger Callback: Sending Events Back to JavaScript

When an alarm triggers, the C layer invokes the `alarm_fire_cb_t` callback from the worker thread. This scenario differs somewhat from the previous "query results" and requires a dedicated event notification mechanism.

#### Why Not Use JavaScript Callback Functions

Intuitively, it seems reasonable to let applications pass a callback function when registering an alarm:

```javascript
// ❌ This does not work in the alarm scenario
alarm.create({ interval: 60000, onFired: (event) => { /* ... */ } })
```

The problem is that alarms span the application lifecycle: after an alarm is created, the application may be killed at any time before the alarm triggers; many devices also support triggering alarms after a reboot.

A JavaScript callback function (`JsValue`) is only valid within the JavaScript runtime of the current application instance. Once the application is closed, this runtime along with all `JsValue`s will be destroyed. At this point, the C++ side has no way to retain this JavaScript callback, let alone call it when the alarm triggers.

This is not just a problem for alarms; **any event that may trigger across application lifecycles cannot be solved via JavaScript callbacks**, such as scheduled tasks, offline message pushes, background download completion notifications, etc.

#### Using Conventional Method Names Instead of Callback References

The simplest solution is: instead of the application "registering a callback," the system proactively **launches** the application when an event occurs and invokes a handling method on the application object using a pre-agreed method name.

This aligns with the design philosophy of application lifecycle functions (`onCreate`, `onShow`, etc.)—the system starts the application on demand and calls known entry methods rather than holding onto pre-registered callbacks. The application side implements the corresponding methods by convention:

```javascript
// app.js — Handling method exported by the application model object (implemented by convention)
export default {
  onAlarmFired(event) {
    // event: { id, label, interval, ... }
    console.log('alarm fired:', event)
  }
}
```

The C++ side implementation: first read the snapshot on the worker thread, then switch back to the main thread to start the application and call the method:

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
        // Call the conventional method exported on the app.js object, passing the alarm info JS object as the event parameter
        JsValue event = js_cast(info);
        applet->modelObject().callMethod("onAlarmFired", {event}).reportError();
    });
}
```

Key points:

- **Do not** directly operate on `JsValue` or call any JavaScript APIs on the worker thread; they can only be used on the UI thread.
- Use `App()->postTask()` to post closures into the main event loop for execution. This is the simplest way to switch back to the UI thread.
- Use `AppletKit::launch()` instead of searching for existing instances; `launch()` restarts the application if it does not exist, and returns the existing instance if it is already running.
- `.reportError()` on the return value of `callMethod()` prints any potential JavaScript exceptions to the log rather than silently ignoring them.

::: tip Conventional method names are the simplest event handling approach
You can think of this pattern as: the exported object of `app.js` is the "set of entry points" exposed by the application to the system. The system calls methods within it when needed, just like calling `onCreate` and `onShow`.

This method is less generic, but it is basically sufficient for controlled system applications, and it is simple to implement without requiring complex persistence and callback management mechanisms.
:::

### Registering the Library Loader

Once all binding functions are written, they need to be "assembled" into a [library object](native-module.md#library-loader) that JavaScript can import, and registered with the framework.

A library loader is a C++ function triggered when an application calls `app.loadLibrary('vendor.alarm')`. It is responsible for creating and returning a JavaScript object containing all exported methods:

```cpp
static JsValue libAlarmLoader(Applet *applet) {
    // You can check the application's package name here to deny unauthorized applications access. You can also check fields.
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

Then register the loader with `AppletKit` during the initialization stage:

```cpp
AppletKit kit{&window};
kit.setLibraryLoader("vendor.alarm", libAlarmLoader);
```

Import it via `app.loadLibrary()` on the JavaScript side, and the return value will be the library object returned by the loader:

```javascript
const alarm = app.loadLibrary('vendor.alarm')

const id = await alarm.create({ interval: 60000, label: 'Get up' })
```