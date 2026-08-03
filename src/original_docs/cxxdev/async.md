# 异步功能开发

在嵌入式系统中，许多操作都是耗时的——读取闪存、访问网络、等待硬件响应。如果这些操作在 UI 线程（同时也是渲染线程）执行，就会冻结 UI，导致应用无响应。

Glyphix 通过将异步操作与 JavaScript 的 `Promise` 机制无缝对接来解决这个问题。C++ 侧负责真正的异步逻辑（通常在另一个线程或通过事件驱动），JavaScript 侧通过 `async/await` 或 `.then()` 等待结果，而 UI 在等待期间保持流畅。

## 核心机制

异步功能的核心是“会话（Session）”模型。当一个 JavaScript 异步调用发起时，C++ 侧创建一个**会话对象**（`AsyncSession`），立即返回一个 `Promise` 给 JavaScript；当操作完成时，会话驱动 `Promise` 的决议（resolve 或 reject），JavaScript 侧的 `then/catch` 或 `await` 随之得到执行。

会话对象绑定到发起调用的 `Applet`，当应用退出时会话会自动清理，开发者无需手动管理内存。

下图展示了异步会话在框架中的位置和核心组件：

<ArchDiagram max-width="520px">
  <div>
    JavaScript 应用层
    <div class="group row">
      <div>async/await<div class="remark">调用模块函数</div></div>
      <div>Promise<div class="remark">等待异步结果</div></div>
    </div>
  </div>
  <div class="subject">
    异步会话（C++）
    <div class="group row">
      <div>ResultSession<div class="remark">单次查询 · Promise 桥接</div></div>
      <div>Signal&lt;T&gt;<div class="remark">全局事件广播</div></div>
    </div>
    <div class="group row">
      <div>Client 类<div class="remark">纯 C++ · 无 JS 依赖</div></div>
      <div>SingleTimer<div class="remark">超时控制</div></div>
    </div>
  </div>
  <div>
    异步执行器
    <div class="group row">
      <div>线程池<div class="remark">默认后台执行</div></div>
      <div>自定义上下文<div class="remark">硬件驱动 · 事件循环</div></div>
    </div>
  </div>
</ArchDiagram>

异步框架的实现在 `gx_async.h` 中，并封装在 `gx::async` 命名空间内。该框架提供几种有用的设施：
- **`async::ResultSession`**：用于单次异步查询，适合读取文件、发起网络请求等场景。
- **`async::make_timeout()`**：用于创建一个单次定时器，为单次会话附加超时功能。
- **`async::Signal<T>`**：用于全局事件广播，适合设备状态变化、外部事件通知等场景。

## 单次查询 ResultSession

`async::ResultSession<T>` 适合“发起查询，等待单个结果”的场景，例如读取一个文件、发起一次网络请求。它是最常用的异步模式，工作方式类似于异步函数调用。

### 工作模型

一个 `ResultSession` 的完整生命周期如下：

1. **创建**：模块函数通过 `async::make<ResultSession<T>>(applet)` 创建会话，会话自动绑定到当前 `Applet`。
2. **配置**：通过 `session->client()` 访问客户端对象，设置任务所需的纯 C++ 参数。
3. **提交**：调用 `session->request(resolver)` 提交任务，立即返回一个 `Promise` 给 JavaScript。
4. **执行**：框架将客户端的 `resolve()` 方法转发到**异步执行器**（默认为后台线程池）执行。
5. **回报**：`resolve()` 返回后，结果被**自动调度回 UI 线程**，驱动 `Promise` 的 resolve 或 reject。
6. **清理**：会话对象在回报完成后自动销毁，或随 `Applet` 退出时自动清理。

::: important Client 类的隔离要求
客户端类（即模板参数 `T`）运行在异步上下文中，**不得持有或访问任何与 JavaScript 交互的对象**，包括 `JsValue`、`Applet *` 等任何 UI 线程专属对象。

客户端类应当是一个**纯 C++ 数据处理单元**，只持有执行任务所需的值类型数据（如 `String`、`int`、或自定义结构等），并在 `resolve()` 方法中完成全部工作。UI 线程与异步线程之间的所有交互由框架自动处理。
:::

### 基本用法

首先，定义一个客户端类，实现 `resolve()` 方法。该方法在异步上下文中被调用，返回 `async::Result<T>` 包装的结果：

```cpp
#include "gx_async.h"
#include "gx_file.h"

using namespace gx;

// 客户端类：纯 C++ 数据处理，不持有任何 JS 对象
class ReadTextClient {
public:
    void setPath(const String &path) { m_path = path; }

    // 在异步上下文中调用，返回操作结果
    async::Result<String> resolve() {
        File file(m_path);
        if (!file.open(File::ReadOnly | File::Text))
            return async::Status(300);  // IO 错误
        int size = int(file.size());
        String text(size);
        text.resize(file.read(text.data(), size));
        return text;  // 成功：返回文件内容
    }

    // 可选：自定义错误消息（当 Promise 被 reject 时使用）
    static const char *errorMessage(async::Status status) {
        switch (status.value()) {
        case 300: return "io error";
        default:  return "unknown error";
        }
    }

private:
    String m_path;  // 已经过安全校验的绝对路径
};
```

然后，在模块函数中创建会话并返回 `Promise`。注意：**必须**使用 `Applet::resolveUri()` 对 JavaScript 传入的路径进行安全校验，而不是直接信任应用提供的字符串：

```cpp
static JsValue readText(JsCtx ctx) {
    Applet *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1 || !ctx.arg(0).isObject())
        return {};

    // ✅ 安全：通过 resolveUri 校验并转换路径
    auto uri = applet->resolveUri(ctx.arg(0)["uri"].toString());
    if (uri.empty())
        return {};  // URI 校验失败，拒绝访问

    using Session = async::ResultSession<ReadTextClient>;
    auto *session = async::make<Session>(applet);
    session->client().setPath(uri);  // 传入校验后的安全路径

    // 提交异步任务，传入完整的 options 对象以兼容快应用回调接口
    session->request(ctx.arg(0));
    return session->promise();
}
```

::: tip 为什么传入 `ctx.arg(0)`？
`request()` 接收 JavaScript 侧传入的整个 `options` 对象，即 `ctx.arg(0)`，用于自动适配快应用异步接口的两种[调用风格](/api/README.md#快应用异步接口)：

- 若 `options` 中包含 `success`、`fail` 或 `complete` 任意属性，判定为**回调风格**，直接调用对应函数，`request()` 不返回有意义的值；
- 否则判定为 **Promise 风格**，将创建一个新的 `Promise`，`session->promise()` 返回该对象供调用方 `await`。

这使得同一个 C++ 实现无需任何额外代码，就能同时支持快应用标准的回调接口和现代 Promise/async-await 接口。如果确定只支持 Promise 风格，也可以传入空值 `{}`。
:::

::: danger 不要跳过 URI 校验
直接使用 JavaScript 传入的字符串作为文件路径是严重的安全漏洞：

```cpp
// ❌ 危险！绕过了沙箱的路径安全检查
session->client().setPath(ctx.arg(0)["uri"].toString());
```

恶意应用可以通过路径穿越（如 `../../etc/passwd`）访问沙箱外的文件系统。所有来自 JavaScript 的路径**必须**经过 `Applet::resolveUri()` 消毒，它会检测路径穿越攻击、跨应用越权访问和非法 URI 格式，校验失败时返回空字符串。
:::

JavaScript 侧的用法：

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

### 错误与状态码

`async::Status` 封装了一个整数状态码，`0`（即 `async::OK`）表示成功，其他值为业务自定义错误码：

```cpp
// 成功：直接返回值，状态码自动为 OK
return async::Result<String>{std::move(content)};
// 失败：仅返回状态码，值部分被忽略
return async::Status(404);
// 同时携带部分结果和非 OK 状态（例如 HTTP 206 Partial Content）
return async::Result<ByteArray>{
  std::move(partialData),
  async::Status(206)
};
```

当 `resolve()` 返回错误状态时，`Promise` 会被 reject，JavaScript 的 `catch` 块会收到一个包含 `message` 和 `code` 字段的错误对象。`message` 来自客户端类的 `errorMessage()` 静态方法。

`errorMessage()` 支持多种签名，框架会自动识别：

```cpp
// 形式一：接收 Status（推荐，简洁）
static const char *errorMessage(async::Status status);

// 形式二：接收完整的 Result，可根据值和状态生成消息
static String errorMessage(const async::Result<MyType> &result);
```

若客户端类没有定义 `errorMessage()`，框架会使用默认的 `"unknown async error"`。

### 值类型与 JavaScript 转换

`resolve()` 返回的值不会原样传给 JavaScript，框架通过 `js_cast()` 函数将 C++ 类型自动转换为 `JsValue`，再驱动 `Promise` 的 resolve。这个过程在框架内部完成，看起来“透明”，但实际上依赖一套**隐式约定**：只有实现了 `js_cast()` 特化的类型才能正确转换，对于自定义的枚举、结构体等类型，需要显式建立转换关系，否则编译将会失败。

#### 内置支持的类型

下列类型可以直接作为 `Result<T>` 的类型参数，无需额外工作：

| C++ 类型 | 对应的 JavaScript 类型 | 备注 |
| --- | --- | --- |
| `int`、`double`、`float` | `number` | 数值直接映射 |
| `bool` | `boolean` | 布尔值直接映射 |
| `String`、`StringView`、`const char *` | `string` | 字符串直接映射 |
| `ByteArray` | `ArrayBuffer` | 二进制数据 |
| `JsonValue` | `object` / `array` | JSON 对象或数组 |
| [`std::vector<T>`](https://en.cppreference.com/w/cpp/container/vector) | `Array` | 数组，元素递归转换（`T` 本身也需可转换） |
| `JsValue` | 任意 | 直接传递，不做转换 |
| `void`（即 `Result<void>`） | `undefined` | 无返回值 |

这些类型均在 JsVM 框架中内置了 `js_cast<T>()` 特化，它们一部分是 `JsValue` 可直接构造的类型，一部分则通过特化实现了转换逻辑。

#### 为自定义类型添加转换支持

如果使用的类型不在上述列表中，编译器会报错提示无法构造 `JsValue`。有两种方式解决：

**方式一：定义 `operator JsValue()` 成员函数**

这适合可以修改定义的自定义结构体，好处是转换逻辑内置在类型定义中，紧密耦合：

```cpp
struct DeviceInfo {
    String model;
    int version;

    // 将结构体转换为 JavaScript 对象
    // 注意：转换在 UI 线程执行，此时有合法的 JsVM 上下文
    operator JsValue() const {
        JsVM &vm = JsVM::current();
        JsValue obj = vm.newObject();
        obj["model"] = JsValue(model);
        obj["version"] = JsValue(version);
        return obj;
    }
};
```

定义后，`Result<DeviceInfo>` 可以直接使用：

```cpp
async::Result<DeviceInfo> resolve() {
    return DeviceInfo{"ModelX", 3};  // 框架自动调用 operator JsValue()
}
```

`operator JsValue()` 内部使用的 `JsVM::current()`、`vm.newObject()` 等 API 属于 JsVM 桥接层，详见 [Native Module 开发文档](./native-module.md#创建与返回对象)。

**方式二：在 `gx` 命名空间中[特化](https://en.cppreference.com/w/cpp/language/template_specialization) `js_cast<T>`**

适合不能修改原始类型定义的情况（例如来自外部定义的类型或枚举）：

```cpp
// 必要时在使用前声明该特化
template<>
JsValue gx::js_cast<ConnectionState>(const ConnectionState &x);

// 在 gx 命名空间内特化
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

特化完成后，`Result<ConnectionState>` 和 `Signal<ConnectionState>` 均可正常工作。

::: tip 整数枚举的简便做法
如果枚举值直接对应整数，在 `resolve()` 中手动转换为 `int` 是最省力的方式，无需任何特化：

```cpp
async::Result<int> resolve() {
    return async::Result<int>{int(myEnum)};
}
```
:::

#### 运行时转换开销

`js_cast()` 在异步结果投递回 UI 线程**之后**才执行，不在异步线程中运行。转换的时间开销完全发生在 UI 线程，对于复杂结构需要确保足够快以避免卡帧。各类型的实际代价如下：

- **零开销类型**：`int`、`double`、`bool`、`String`、`const char *` 通过 `JsValue` 构造函数直接映射，无额外拷贝或堆分配。`operator JsValue()` 方式和 `js_cast<T>` 特化同样在编译期内联，没有虚调用或间接层。
- **线性开销类型**：`std::vector<T>` 需要逐元素调用 `setIndex()`，开销与元素数量成正比。如果返回结构是固定字段的对象，优先用 `operator JsValue()` 手动构造 JS 对象，比数组更高效也更易读。
- **树形遍历类型**：`JsonValue` 在转换时递归遍历整棵树，逐一构造 JavaScript 节点，是内置类型中开销最大的。如果数据结构在编译期已知，`operator JsValue()` 直接构造对象通常更快，且没有 `JsonValue` 本身的构建成本。
- **自定义结构体**：如果使用 `operator JsValue()` 或 `js_cast()` 特化，转换性能取决于各成员类型的转换开销，即构造对象的复杂度。

::: tip 简单判定标准
如果你的异步数据结构简单（数值、简单结构体对象，或小的 `JsonValue`），那么转换开销通常不会影响 UI 流畅性。
:::

#### 无序列化中间层

某些异步框架要求在 worker 线程和 UI 线程之间传递数据时，必须先将结果序列化为 JSON 或其他自描述格式，再在 UI 线程反序列化，这是为了实现线程间的“类型擦除”传递，但代价是每次调用都要承担字符串（或二进制数据流）的拼接、传输和解析开销。更糟的是可能构造多份数据副本（序列化的中间数据和原始数据等）。

async 框架**不依赖序列化中间层。** 结果通过 `async::Result<T>` 以 C++ 原生值的形式在线程间移动，完全绕过序列化过程：

```
worker thread                  UI thread
resolve(Result<MyType>{...}) → js_cast(result.value()) → JsValue (JavaScript)
                  ↑
             直接内存移动，无 JSON 字符串
```

`js_cast()` 仅在结果已经安全地回到 UI 线程之后才执行，它的职责是将 C++ 值映射为 JavaScript 引擎的内部表示，而不是充当线程间的通信协议。

如果你主动选择将 `JsonValue` 作为 `Result<T>` 的类型参数（用于缓解模板代码膨胀），那么你引入的是 `JsonValue` 的**构建和树遍历**开销，而不是字符串序列化，`JsonValue` 本身也是一种内存中的树形结构，不是文本格式。

#### 模板代码体积

`ResultSession<T>` 是模板类，编译器会为每个不同的客户端类型 `T` 生成一份独立的代码。不过框架已将绝大多数与 `T` 无关的逻辑（如 `Promise` 管理、事件投递、`Applet` 生命周期绑定）提取到非模板基类 `detail::ResultSession` 中，因此每个 `T` 实际额外增加的代码量主要集中在薄薄的 `Resolver` 适配层。

但如果项目中存在**大量仅使用一次的细粒度客户端类型**，累积的实例化数量仍会带来可观的代码量增长。

一种常见的压缩手段是以 `JsonValue` 作为类型擦除媒介，将多个零散的小函数合并到单一的客户端类型中：

```cpp
// 合并前：每个操作都是独立的客户端类 + 独立的模板实例化
struct GetVersionClient { ... };   // ResultSession<GetVersionClient>
struct GetModelClient   { ... };   // ResultSession<GetModelClient>
struct GetSerialClient  { ... };   // ResultSession<GetSerialClient>

// 合并后：共享同一个模板实例化，仅在运行时区分操作
struct DeviceQueryClient {
    enum Kind { Version, Model, Serial } kind;

    // 这里演示用 switch 分派，实际也可以用函数指针。但是不要用 BaseClient
    // 配合派生类重写 resolve() 来实现多态，会比函数指针方案多一些虚表膨胀。
    async::Result<JsonValue> resolve() {
        switch (kind) {
        case Kind::Version: return JsonValue{getVersion()};
        case Kind::Model:   return JsonValue{getModel()};
        case Kind::Serial:  return JsonValue{getSerial()};
        }
    }
};

// 三个模块函数共用 ResultSession<DeviceQueryClient> 这一个实例化
static JsValue getVersion(JsCtx ctx) {
    using Session = async::ResultSession<DeviceQueryClient>;
    auto *session = async::make<Session>(applet);
    session->client().kind = DeviceQueryClient::Version;
    return session->request(ctx.arg(0));
}
```

这种做法的代价是：返回类型退化为 `JsonValue`，需要承担额外的转换运行时开销（见上文）。因此它适合**数据量小、函数数量多**的场景，用少量运行时开销换取有意义的代码体积收益。对于数据量较大或性能敏感的操作，仍应保留独立的强类型客户端类。

### 自定义异步上下文

默认情况下，`session->request()` 将 `resolve()` 提交到框架的**异步执行器**——通常是一个后台线程池。但有些场景需要使用不同的异步上下文，例如自定义事件循环或 AIO 多路复用机制，它们均不希望占用额外的线程资源。

这时可以跳过 `request()`，直接手动控制异步执行流程，客户端类也不需要实现 `resolve()` 执行函数。关键是：**在异步上下文中完成工作后，调用 `session->resolve()` 将结果投递回 UI 线程**。

```cpp
// 客户端类：不需要实现 resolve()，因为不使用默认线程池
struct FirmwareCheckClient {
    // 仅定义 errorMessage() 用于错误描述
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

    // 手动设置 resolver（不调用 request，不使用默认线程池）
    session->setResolver(ctx.arg(0));
    JsValue promise = session->promise();

    // 提交到自定义的硬件驱动线程
    HardwareDriver::checkUpdate(
        version,
        // 回调可能在任意线程——框架会自动调度回 UI 线程
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

这里的核心区别：
- `request()` 同时完成“设置 resolver”和“提交到异步执行器”两个动作；
- 手动模式下，你需要自己调用 `setResolver()` 设置响应目标，然后在任意时机通过 `session->resolve()` 推送结果或者错误状态。

`resolve()` 是线程安全的，它将结果封装为事件投递回 UI 线程，再完成 `Promise` 的决议。

::: tip 何时使用自定义上下文
- 底层驱动已提供回调接口，你不想再创建额外的线程：直接在驱动回调中 `resolve`。
- 需要与现有的 AIO/epoll 事件循环集成：在事件完成回调中 `resolve`。
- 需要串行化执行（如操作必须按顺序）：用自己的任务队列调度，完成后 `resolve`。

只要保证最终调用一次 `session->resolve()` 即可，框架不关心结果是从哪个线程投递的。
:::

### 值类型语义

由于 `resolve()` 返回（或自定义异步上下文主动投递）的 `async::Result<T>` 值会被投递到 UI 线程再转换为 `JsValue`，因此数据类型 `T` 必须是可移动的。内置支持的类型均满足这一要求，对于自定义类型：
- 如果是一个仅包含内置支持类型成员的结构体，那么 C++ 标准保证它是可移动的。
- 如果使用了裸指针并自己控制其所有权，那么你需要正确实现[移动构造函数](https://en.cppreference.com/w/cpp/language/move_constructor)。
- [平凡类型](https://en.cppreference.com/w/cpp/named_req/TrivialType)（如纯 C 结构体、枚举等）默认满足值类型语义。

需要注意的是，非平凡类型通常包含堆上的资源，以下写法可能面临内存峰值问题：

```cpp
auto *session = getFetchLargeDataSession();
std::vector<uint32_t> data = fetchDataFromNetwork(url);
session->resolve<decltype(data)>(data);  // 会有一次 data 的完整复制
```
这是因为 `session->resolve()` 的参数是按值传递的，传入 `data` 时会调用[复制构造函数](https://en.cppreference.com/w/cpp/language/copy_constructor)，导致完整复制一份。如果 `data` 数据量很大，这会导致内存使用量翻倍。此时会出现这类编译警告：
```
'...' is deprecated:
avoid use copy semantics of Result<T> if T is not trivially copyable
```
正确的做法是使用 [`std::move()`](https://en.cppreference.com/w/cpp/utility/move) 显式启用移动语义：

```cpp
auto *session = getFetchLargeDataSession();
std::vector<uint32_t> data = fetchDataFromNetwork(url);
session->resolve<decltype(data)>(std::move(data));  // 使用移动语义
```

### 超时控制

对于可能长时间无响应的异步操作，使用 `async::make_timeout()` 为会话添加超时保护。超时后会自动 reject `Promise`，避免 JavaScript 侧永久挂起。

以下代码片段展示了一个基本示例，演示如何在网络请求中使用超时控制：

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

    // 创建超时保护：超时后自动 reject Promise
    auto handle = async::make_timeout(session, timeoutMs,
        [](Session *s) {
            // 超时处理：应当在此取消正在进行的异步操作
            s->fulfill(async::Status(408));  // 408 Request Timeout
            
        });

    // 将 handle 移动到异步执行上下文
    NetworkDriver::fetch(url,
        [handle = std::move(handle)](auto &response) {
            // 若已超时，resolve 会被安全忽略
            handle->resolve<String>(std::move(response.body));
        });

    return promise;
}
```

#### 工作原理

`make_timeout()` 的关键工作流程：

1. 将 `session` 的客户端数据**移动**到一个内部类中，此后不得再访问 `session->client()`。
2. 启动一个单次定时器，返回 `SharedRef<SingleTimer>` 句柄。
3. **正常路径**：在超时前调用 `handle->resolve()`，内部原子地取走 session 所有权并投递结果事件，之后定时器触发时发现 session 已为空便不作处理。
4. **超时路径**：定时触发，**在 UI 线程**执行回调，开发者在回调中调用 `session->fulfill()` 投递错误状态；回调返回后，timer 负责 `delete session`。
5. **应用退出**：`Applet` 被销毁时，timer 自动解绑，session 被删除，回调不会被触发。

该机制特别适用于异步操作没有内置超时机制的场景，如某些网络请求的实现。众所周知，正确地实现超时保护有些棘手，你必须正确处理所有路径的竞争条件和生命周期安全问题。

`make_timeout()` 依赖这些前提来保证安全性：
- 客户端类型（也就是 `ResultSession<T>` 中的 `T`）必须是**可移动的**，这算是一个历史遗留限制。
- 异步操作必须支持在 UI 线程中安全地取消，这意味着删除任务监听器并释放对 `handle` 的引用。

#### 回调线程与 `fulfill()`

超时回调（`make_timeout()` 的第三个参数）**始终在 UI 线程执行**，因为它由定时器（`Timer`）触发，而定时器事件由主事件循环分发。

这一点决定了回调中**只能**使用 `session->fulfill()` 而不能使用 `session->resolve()`：

| 方法 | 可调用线程 | 对 session 的影响 |
| --- | --- | --- |
| `resolve(result)` | 任意线程 | 投递 Consume 事件，session 在 UI 线程处理后**被删除** |
| `fulfill(result)` | **仅限 UI 线程** | 直接分发结果，**不删除** session |

`make_timeout()` 的超时路径由 timer 自身负责在回调结束后 `delete session`。如果在回调中调用 `session->resolve()`，它会同样投递一个删除 session 的事件，与 timer 的 `delete` 形成**双重释放（double free）**，导致未定义行为。`fulfill()` 只投递结果、不触及 session 生命周期，因此是回调中唯一安全的选择。

`fulfill()` 接受 `async::Result<R>` 或直接接受 `async::Status`（无结果值时的简写）：

```cpp
auto handle = async::make_timeout(session, 5000, [](Session *s) {
    s->fulfill(async::Status(408)); // 仅填充错误状态
    // 或携带值和状态：
    s->fulfill(async::Result<String>{"partial", async::Status(206)});
    // ❌ 不要调用 s->resolve()，会与 timer 的 delete session 形成双重释放
});
```

::: tip
判断规则很简单：session 的所有权在哪里，由谁负责删除？
- **正常路径**：`handle->resolve()` 内部原子地接管 session 所有权，session 随 Consume 事件处理后删除。
- **超时回调**：timer 接管 session 所有权，回调结束后删除。因此回调中只能用 `fulfill()` 投递结果。
:::

#### 访问客户端数据

如果超时回调需要读取客户端数据来决定错误策略，使用扩展回调签名 `(Session *, const T &)`。**不要**在回调中调用 `session->client()`——客户端已被移动到 timer 中：

```cpp
auto handle = async::make_timeout(session, 3000,
    [](Session *s, const HttpClient &client) { // 也可用 auto &client
        // ✅ 通过第二个参数访问客户端数据
        LogWarn() << "request timeout: " << client.url();
        s->fulfill(async::Status(408));
    }
);
```

#### 资源生命周期管理

超时发生时，你需要在回调中取消正在进行的异步任务，以释放对 `handle` 的引用。`SingleTimer` 使用引用计数管理生命周期——如果异步操作持有 `handle` 的引用但永远不会完成，就会产生内存泄漏：

```cpp
auto task = AioTask::create();
auto handle = async::make_timeout(session, 5000,
    [task](auto *s) {
        task->cancel();     // 取消任务，释放对 handle 的引用
        s->fulfill(async::Status(408)); // reject Promise
    });

// 任务完成回调持有 handle 引用
task->start([handle = std::move(handle)](auto &result) {
    handle->resolve(result);
});
```

::: important
`make_timeout()` 返回的 `handle` 还**必须**被异步任务引用（上例中由 lambda 捕获），以确保在任务完成前定时器不会被销毁。否则会立即触发超时回调和 Promise reject，导致任务无法正常完成。
:::

这种内存泄漏由两种原因导致：
1. **async 框架泄漏**：`handle` 引用被遗忘，导致相关会话对象无法释放。
2. **底层任务泄漏**：异步任务本身阻塞在未完成的状态，相关资源也不会被清理。

### 应用退出时的自动清理

当 `Applet` 被销毁时（例如用户关闭应用、系统回收资源），所有绑定到该 `Applet` 的异步会话会被自动清理：

- 会话的 `unbind()` 方法被调用，它会关闭会话并释放 `Promise` 引用。
- 如果正在使用 `make_timeout`，timer 同样会被解绑，内部持有的 session 被删除。
- JavaScript 侧的 `Promise` 将永远不会被 resolve 或 reject——但此时 JavaScript 环境本身也在被销毁，所以这是安全的。

这意味着你**不需要**手动跟踪和取消异步任务——框架保证不会出现以下情况：
- 向已销毁的 `Applet` 投递结果导致访问悬空指针。
- 在已释放的 JavaScript 环境中执行回调。
- 异步会话在应用退出后泄漏。

具体来说，当后台线程调用 `resolve()` 投递结果到 UI 线程后，处理函数会检查 `applet()` 是否仍然有效。如果 `Applet` 已被销毁导致 `applet()` 返回 `nullptr`，框架会安全地丢弃结果，不执行任何 JavaScript 操作。

::: tip 异步上下文中的安全返回
由于 `resolve()` 是纯数据投递（通过事件队列），即使 `Applet` 已经销毁，在后台线程中调用 `resolve()` 也不会崩溃。后台线程不需要关心 `Applet` 的存活状态，这是框架的职责。
:::

唯一需要注意的是，如果你派生了 `ResultSession` 并引入了其他 `JsValue` 成员变量，则需要在 `unbind()` 中清理这些成员，以避免内存泄漏：

```cpp
class MySession : public async::ResultSession<MyClient> {
public:
    void unbind() override {
        m_callbacks = {}; // 清理任何持有的 JsValue，避免泄漏
        async::ResultSession::unbind(); // 调用基类清理
    }

private:
    JsValue m_callbacks; // 需要手动清理的成员
};
```

::: important `ResultSession` 的生命周期延长
如果应用退出时仍有未完成的异步会话，框架仅会清理与应用相关的资源（如 `Promise` 引用、绑定关系等），但**不会销毁会话对象本身**，这表现为 `ResultSession` 的生命周期被延长到异步操作完成为止。

这本身是为了保证内存安全，但会造成部分资源释放不及时。因此异步任务必须保证在有限的时间内完成，不能无限期地挂起。
:::

## 多次查询 ListenSession

该类 API 尚不稳定，暂不开放使用。

## 全局事件广播 async::Signal

如果一个 C++ 事件需要广播给**多个应用**（而不是针对某一个特定的调用方），使用 `async::Signal<T>`。它将底层的硬件或系统事件“多播”给所有订阅了它的 JavaScript 监听者。

`async::Signal<T>` 和 `ResultSession` 的定位不同：

| 特性 | ResultSession | Signal |
| --- | :---: | :---: |
| 通信方向 | 一对一（调用方 → 结果） | 一对多（事件源 → 所有订阅者） |
| 触发次数 | 单次 | 多次 |
| 绑定对象 | 单个 Applet | 跨 Applet |
| 适用场景 | 异步查询、请求 | 系统事件、状态变化 |

### 基本用法

假设有一个电池点亮变化的事件需要通知所有订阅者：

```cpp
// 定义一个全局信号，通常为对应服务的成员变量
async::Signal<int> batteryChanged;

// 当硬件事件发生时触发信号（可在任意线程调用）
void onBatteryLevelChanged(int newLevel) {
    batteryChanged(newLevel);  // 通知所有订阅者
}
```

#### 绑定 & 解绑

该模块函数允许 JavaScript 侧订阅该信号，它还返回一个绑定 ID 供 JavaScript 侧取消订阅：

```cpp
static JsValue subscribeBatteryChange(JsCtx ctx) {
    if (ctx.argc() < 1 || !ctx.arg(0).isFunction())
        return {};
    // 必须在有效的 applet 环境中才能订阅
    auto *applet = Applet::current(ctx.vm());
    if (applet == nullptr) return {};

    // 将 slot 绑定到应用，随应用退出而自动取消订阅
    auto *slot = batteryChanged.connect(ctx.arg(0));
    return applet->bindObject(slot); // 返回 slot ID 供 JavaScript 取消
}
```

还需要实现一个取消订阅的模块函数。无论何种 `async::Signal` 类型，解绑函数的实现都是非常固定的：

```cpp
static JsValue unsubscribeBatteryChange(JsCtx ctx) {
    auto *applet = Applet::current(ctx.vm());
    if (applet && ctx.argc()) {
        // slotId 默认为 0，可以被安全地忽略而不执行任何操作
        auto slotId = ctx.arg(0).toInt();
        // 将 slot 与 applet 解绑后还需要删除 slot 对象
        delete applet->unbindObject<async::Slot>(slotId);
    }
    return {};
}
```

#### JavaScript 导出

只需要定义一个 [Native Module](./native-module.md) 来导出这些函数即可：

```cpp
static JsModule *createBatteryModule(JsVM &vm) {
    auto mod = vm.newObject();
    // battery 模块通常还有 getLevel() 之类的函数，这里不展开
    mod["subscribe"] = subscribeBatteryChange;
    mod["unsubscribe"] = unsubscribeBatteryChange;
    return mod;
}
// 别忘了用 GX_JSVM_MODULE_IMPORT 导入模块
GX_JSVM_MODULE(vendor_battery, "vendor.battery", createBatteryModule)
```

::: tip 复用 `unsubscribe` 函数
由于解绑函数的实现非常通用，你可以定义一个通用的 `unsubscribe` 函数，然后多次导入到各个模块中使用。
:::

JavaScript 侧：

```js
import battery from '@vendor.battery'

const sid = battery.subscribe((level) => {
  console.log('battery level:', level)
})

// 需要取消订阅时调用
battery.unsubscribe(sid)
```

### 信号传递模式

`Signal` 支持两种传递模式，通过第二个参数控制：

```cpp
// 普通模式（默认）：通知所有订阅者
batteryChanged(newLevel, async::NormalSignal);

// 跳过不可见应用：仅通知前台可见的应用，减少不必要的消耗
batteryChanged(newLevel, async::SkipInvisible);
```

`SkipInvisible` 模式适用于仅在 UI 可见时才有意义的事件（如界面刷新通知）。对于需要后台感知的事件（如电池低电量警告），应使用默认的 `NormalSignal`。

### 信号值类型

`Signal<T>` 的类型参数 `T` 与 `ResultSession` 遵循完全相同的转换规则：触发信号时，框架通过相同的 `js_cast()` 机制将 C++ 值转换为 JavaScript 回调的参数。`int`、`bool`、`String`、`JsonValue` 等内置类型可以直接使用；如需传递自定义结构体或枚举，请参阅[值类型与 JavaScript 转换](#值类型与-javascript-转换) 一节中的方法。

## 线程安全说明

异步框架的线程安全模型遵循以下规则：

- **`resolve()` 是线程安全的**：`ResultSession::resolve()` 和 `SingleTimer::resolve()` 可以在任意线程调用。它们通过事件系统将结果投递到 UI 线程，不直接操作 JavaScript 对象。
- **`JsValue` 不是线程安全的**：`JsValue` 基于引用计数管理生命周期，其引用计数操作非原子性。不得在异步线程中创建、拷贝、销毁或访问 `JsValue`。这正是客户端类不得持有 `JsValue` 的原因。
- **`Promise` 决议在 UI 线程执行**：无论 `resolve()` 从哪个线程调用，最终的 JavaScript `Promise` 回调总是在 UI 线程执行，保证 UI 操作的安全性。
- **`async::Signal` 通知在 UI 线程分发**：`async::Signal::operator()` 虽然可以跨线程调用，但 JavaScript 回调始终在 UI 线程执行。

如果客户端类需要与 UI 线程共享状态（例如提供取消标志），使用 [`std::atomic`](https://en.cppreference.com/w/cpp/atomic/atomic) 等原子操作或互斥量保护共享数据：

```cpp
class CancellableClient {
public:
    void cancel() { m_cancelled.store(true); }

    async::Result<String> resolve() {
        for (int i = 0; i < 100 && !m_cancelled.load(); ++i) {
            // 执行分步任务，定期检查取消标志
            processChunk(i);
        }
        if (m_cancelled.load())
            return async::Status(499);  // 客户端取消
        return std::move(m_result);
    }

private:
    std::atomic_bool m_cancelled{false};
    String m_result;
};
```

特别的，Glyphix 框架的许多值类型在**本异步框架中**是可以安全地跨线程传递的，如：
- `String`：可以直接在多线程中赋值、访问，无需额外同步机制。
- `JsonValue`：该类也是值类型，并具有与 `String` 同等的线程安全特性。
- `ByteArray`：与 `String` 类似，支持跨线程使用。
- `SharedRef<T>`：引用计数智能指针本身可以跨线程传递，但托管对象 `T` 的线程安全性取决于其定义。
- `String::View` 等非拥有类型**不能**跨线程使用。

这也是前面所有示例中我们总是直接跨异步上下文捕获和传递 `String` 等类型，使用它们不需要特别处理。也不需要使用 mutex 等同步机制来保护。

::: important
上述类型的线程安全性实际上依赖于具体的异步框架内存模型，这意味着它们在所有场景中**并不是自动线程安全**的。本文档中的异步框架保证了这一点，但不能推广到任何情况。
:::
