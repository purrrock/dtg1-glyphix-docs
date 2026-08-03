# 异步开发示例

如果你感觉[异步功能开发](async.md)的章节内容过多且不够直观，本文档将提供一些典型的、较为简单的示例，帮助你应对一些常见的异步开发场景。

这些场景并不极端复杂，但侧重于：
- 一个典型的异步调用模式，重点在于跨线程、跨语言的调用关系；
- 这些场景可能更琐碎，存在一大批需要对接的系统 API，对代码膨胀较为敏感；
- 存在典型的 C API 交互需求，而不是标准的 C++ 接口。

你可以在 SDK 示例中找到这些场景的完整实现，并可以直接在 PC 上模拟运行。

## 场景：对接 C 闹钟接口

嵌入式系统中常见的异步模式是“C 回调”：调用方提交一个任务，并传入一个函数指针作为完成通知，操作完成后由 worker 线程调用该回调。

::: important async 只支持线程模型
Glyphix 框架的异步功能只支持普通的线程上下文，不能在中断中使用。如果你的异步上下文是中断处理程序，那么应该配备一个线程来中转。
:::

这里以一个闹钟服务为例。它提供的 C 异步接口是这样的：

```c
// 以 alarm_async_create 为例，其他操作的形式类似
void alarm_async_create(AlarmService *svc, uint32_t interval_ms, ...,
                        alarm_create_cb_t done_cb, void *done_ctx);

// 完成回调的函数指针类型，在 worker 线程被调用
typedef void (*alarm_create_cb_t)(alarm_err_t err, alarm_id_t id, void *ctx);
```

接下来说明如何将这类典型的 C 回调接口桥接到 JavaScript 的 Promise。

### 多个操作共用 Session 类型

闹钟服务有 `create`、`cancel`、`setEnabled`、`update`、`snooze`、`getInfo`、`list`、`count` 等一批操作。如果为每个操作单独定义一个客户端类（client），会产生大量模板实例化。

对于这类“实际逻辑均在 C 层完成，C++ 侧只做参数传递”的场景，可以定义一个只包含错误码映射的轻量客户端，让所有操作共用一个 `ResultSession` 实例化：

```cpp
struct AlarmClient {
    // 将 C 层的 alarm_err_t 转换为可读的错误字符串，
    // 供 Promise 被 reject 时传给 JavaScript 侧的 catch。
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

// 所有闹钟操作共用这一个 Session 类型
using AlarmSession = async::ResultSession<AlarmClient>;
```

`AlarmClient` 不需要实现 `resolve()` 方法，因为这里不使用默认的线程池执行器，实际的异步操作由闹钟服务的 worker 线程完成，C++ 侧只负责将结果投递回 UI 线程。

### 基本绑定模式

以 `alarm.create()` 为例，展示完整的绑定流程：

```cpp
static JsValue jsAlarmCreate(JsCtx ctx) {
    auto *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1 || !ctx.arg(0).isObject())
        return JsValue{};

    // 从 JavaScript 传入的 options 对象中读取参数
    const JsValue &opts = ctx.arg(0);
    uint32_t intervalMs = static_cast<uint32_t>(opts["interval"].toInt());
    String label        = opts["label"].toString();
    alarm_repeat_t mask = parseRepeatMask(opts["repeat"]);

    // 创建会话，并从 options 对象中提取 resolve/reject 回调（支持两种异步风格）
    auto *session = async::make<AlarmSession>(applet);
    session->setResolver(opts);

    // C 回调：在 worker 线程中被调用，通过 resolve() 跨线程通知 JavaScript
    auto done = +[](alarm_err_t err, alarm_id_t id, void *data) {
        auto *s = static_cast<AlarmSession *>(data);
        s->resolve(err == ALARM_OK
            ? async::Result<int>(id) // 成功：resolve 新建的闹钟 ID
            : async::Status(err));   // 失败：reject，错误消息来自 errorMessage()
    };

    // 调用 C 服务的异步闹钟创建接口，传入回调和会话指针
    alarm_async_create(AppletAlarmService::instance(),
                       intervalMs, mask, label.c_str(), /*...*/,
                       onAlarmFired, nullptr, done, session);
    // 返回 Promise 对象给 JavaScript，框架会在 resolve() 被调用时自动决议它
    return session->promise();
}
```

这里有几个固定的套路，可以直接复制使用：

- `async::make<AlarmSession>(applet)` 创建会话并绑定到当前 Applet，以满足生命周期要求。
- `session->setResolver(opts)` 让同一套代码同时支持[回调风格和 Promise 风格](/api/README.md#快应用异步接口)的异步调用。
- `+[](... void *data)` 通过一元 `+` 将 lambda 转换为普通函数指针，满足 C 回调的类型要求。
- 将 `session` 作为 `void *` 透传给 C API，在回调中转型回来再调用 `resolve()`。
- `resolve()` 是线程安全的，它将结果封装为事件投递回 UI 线程，再驱动 Promise 的决议。

::: tip 利用 lambda 表达式写回调
在 C 中，回调函数通常是一个静态函数，可以使用 C++ 的 lambda 表达式直接就近嵌套定义回调函数，例如：
```cpp
auto done = +[](alarm_err_t err, alarm_id_t id, ...) { ... }
alarm_async_create(..., done, session);
```
这样可以避免定义一大批单独的静态函数，代码更紧凑清晰。
:::

其余操作（`cancel`、`setEnabled`、`snooze` 等）的结构完全相同，只有参数读取和 C API 调用不同：

```cpp
static JsValue jsAlarmCancel(JsCtx ctx) {
    auto *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1)
        return JsValue{};

    alarm_id_t id = ctx.arg(0).toInt();

    auto *session = async::make<AlarmSession>(applet);
    session->setResolver(ctx.arg(0));

    auto done = +[](alarm_err_t err, void *data) {
        // 没有返回值时，用 resolve<void> 即可
        static_cast<AlarmSession *>(data)->resolve<void>(async::Status(err));
    };
    alarm_async_cancel(AppletAlarmService::instance(), id, done, session);

    return session->promise();
}
```

::: important 不要遗漏参数检查
`session->setResolver(ctx.arg(0))` 依赖对 `ctx.argc()` 的检查。如果函数开头没有检查参数数量，那么要在调用 `setResolver()` 时检查参数数量：
```cpp
session->setResolver(ctx.argc() ? ctx.arg(0) : JsValue{});
```
:::

### 注册自定义 C 结构体的类型转换

`alarm.getInfo()` 返回一个 `alarm_info_t` 结构体，需要将它转换为 JavaScript 对象。为此，先在 `gx` 命名空间中特化 `js_cast<T>`：

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

特化完成后，在绑定函数中直接将结构体实例传给 `resolve()` 即可：

```cpp
auto done = +[](alarm_err_t err, const alarm_info_t *info, void *data) {
    auto *s = static_cast<AlarmSession *>(data);
    if (err != ALARM_OK || !info) {
        // 异常路径，返回错误状态触发 reject，错误消息来自 errorMessage()
        s->resolve<alarm_info_t>(async::Status(err));
        return;
    }
    s->resolve<alarm_info_t>(*info);  // 框架在 UI 线程自动调用 js_cast
};
alarm_async_get_info(AppletAlarmService::instance(), id, done, session);
```

::: tip
`js_cast()` 由框架在结果回到 UI 线程之后才调用，不在 worker 线程中执行。这意味着在 `js_cast()` 内部可以安全地使用 `JsVM::current()` 等 UI 线程专属 API。
:::

对于 `alarm.list()` 这种返回数组的情况，可以直接构造 `std::vector<int>` 并 resolve，无需定义额外的类型转换：

```cpp
auto done = +[](alarm_err_t /*err*/, const alarm_id_t *ids, int count, void *data) {
    auto *s = static_cast<AlarmSession *>(data);
    s->resolve<std::vector<int>>(std::vector<int>{ids, ids + count});
};
alarm_async_list(AppletAlarmService::instance(), done, session);
```

### 闹钟触发回调：将事件送回 JavaScript

闹钟触发时，C 层会从 worker 线程调用 `alarm_fire_cb_t` 回调。这个场景和前面的“查询结果”有些不同，需要专门设计事件通知机制。

#### 为什么不用 JavaScript 回调函数

直觉上，让应用在注册闹钟时传入一个回调函数似乎合理：

```javascript
// ❌ 这在闹钟场景下行不通
alarm.create({ interval: 60000, onFired: (event) => { /* ... */ } })
```

问题是，闹钟是跨越应用生命周期的：闹钟创建后，应用可能会在闹钟触发之前的任意时刻被杀死；许多设备还支持重启后触发闹钟。

一个 JavaScript 回调函数（`JsValue`）只在当前应用实例的 JavaScript 运行时中有效。一旦应用被关闭，这个运行时连同所有 `JsValue` 都会被销毁。此时 C++ 侧没办法继续保留这个 JavaScript 回调，更别说在闹钟触发时调用它了。

这不只是闹钟的问题，**任何可能在跨应用存活期触发的事件，都无法通过 JavaScript 回调解决**，例如定时任务、离线消息推送、后台下载完成通知等。

#### 使用约定方法名代替回调引用

最简单的解决方法是：不由应用“注册回调”，而是系统在事件发生时主动**启动**应用，并以约定好的方法名调用应用对象上的处理方法。

这与应用生命周期函数（`onCreate`、`onShow` 等）的思路一致——系统按需启动应用，调用已知的入口方法，而不是持有事先注册的回调。应用侧按约定实现对应方法即可：

```javascript
// app.js — 应用模型对象导出的处理方法（按约定实现）
export default {
  onAlarmFired(event) {
    // event: { id, label, interval, ... }
    console.log('alarm fired:', event)
  }
}
```

C++ 侧的实现：先在 worker 线程读取快照，再切回主线程启动应用并调用方法：

```cpp
static void onAlarmFired(alarm_id_t id, void * /*user_data*/) {
    // 在 worker 线程读取快照，避免跨线程访问闹钟表
    alarm_info_t info{};
    alarm_get_info(id, &info);

    // 切换回主线程再操作 JavaScript
    App()->postTask([info] {
        auto *svc = AppletAlarmService::instance();
        // 用 launch() 启动（或唤醒）目标应用，即使它当前不在运行
        auto *applet = AppletKit::instance()->launch(svc->alarmAppletName);
        if (!applet) return;

        auto &vm = JsVM::current();
        // 调用 app.js 导出对象上的约定方法，事件参数为闹钟信息的 JavaScript 对象
        JsValue event = js_cast(info);
        applet->modelObject().callMethod("onAlarmFired", {event}).reportError();
    });
}
```

几个要点：

- **不要**在 worker 线程中直接操作 `JsValue` 或调用任何 JavaScript API，它们只能在 UI 线程中使用。
- 使用 `App()->postTask()` 将闭包投递到主事件循环中执行，这是切回主线程最简单的方式。
- 用 `AppletKit::launch()` 而不是查找现有实例；`launch()` 在应用不存在时会重新启动它，在应用已经运行时则返回现有实例。
- `callMethod()` 返回值上的 `.reportError()` 会将可能发生的 JavaScript 异常打印到日志，而不是静默忽略。

::: tip 约定方法名是最简单的事件处理方式
可以将这种模式理解为：app.js 的导出对象就是应用暴露给系统的“入口点集合”，系统在需要时调用其中的方法，就像调用 `onCreate`、`onShow` 一样。

这种方法不太通用，但对受控的系统应用来说基本够用，且实现简单，不需要复杂的持久化和回调管理机制。
:::

### 注册库加载器

所有绑定函数编写完成后，还需要将它们“装配”成一个 JavaScript 可以导入的[库对象](native-module.md#library-loader)，并注册到框架中。

库加载器是一个在应用调用 `app.loadLibrary('vendor.alarm')` 时被触发的 C++ 函数，它负责创建并返回一个包含所有导出方法的 JavaScript 对象：

```cpp
static JsValue libAlarmLoader(Applet *applet) {
    // 可以在这里检查应用的包名，拒绝未授权的应用访问。也可以检查字段。
    if (!applet || applet->objectName() != "com.vendor.alarm")
        return JsValue{};

    JsValue lib = JsVM::current().newObject();

    // 将绑定函数挂载到库对象上，属性名就是 JavaScript 侧调用的方法名
    lib["create"]     = jsAlarmCreate;
    lib["cancel"]     = jsAlarmCancel;
    lib["list"]       = jsAlarmList;
    lib["count"]      = jsAlarmCount;
    // ...
    return lib;
}
```

然后在初始化阶段将加载器注册到 `AppletKit`：

```cpp
AppletKit kit{&window};
kit.setLibraryLoader("vendor.alarm", libAlarmLoader);
```

JavaScript 侧通过 `app.loadLibrary()` 导入，返回值就是加载器返回的库对象：

```javascript
const alarm = app.loadLibrary('vendor.alarm')

const id = await alarm.create({ interval: 60000, label: '起床' })
```
