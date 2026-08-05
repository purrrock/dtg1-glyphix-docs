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