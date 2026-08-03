# 异步操作

在 JavaScript 脚本中引入异步操作的目的主要是将耗时的工作放到后台执行，避免 JavaScript 线程阻塞，放到后台处理的工作主要是 IO 密集型操作。Glyphix 提供一个基本的 JavaScript 异步框架供开发者使用，该框架只对异步工作流做必要的抽象，因此不会引入额外的开销。

## 适用场景

异步工作流模型适用场景

- 由 JavaScript 代码发起请求，原生异步处理线程处理后返回结果；
- 由 JavaScript 代码发起请求，原生异步处理线程处理后定时上报消息；
  - JavaScript 代码可主动要求撤销/取消请求。

## 数据请求模式

在数据请求模式中，JavaScript 代码调用 C++ API 创建请求，并在异步线程中执行操作后将结果返回给 JavaScript 代码。在这个过程中数据会通过异步队列进行传输，`async::ResultSession` 模板类提供了该模式的通用操作框架。

### 场景说明

以下场景是典型的数据请求模式：

- **文件读写**：JavaScript 发起调用时需要指定文件的路径，读写的文件偏移位置、数据长度或要写入的数据；请求发送到异步线程执行时会进行真正的文件读写操作，并在操作完成后通知或将结果返回到 JavaScript 代码。
- **网络请求**：和文件读写类似，JavaScript 发起调用时要制定请求参数，然后在后台线程处理并返回结果。

数据请求模式的场景具有以下特点：
- 请求返回的结果是单次的，因此可能多次触发的传感器或者定时器监听不适用这种模式；
- 请求总是会有结果：如果请求成功则返回结果，否则返回错误信息，结果的返回也是异步的；
- 请求一旦发起无法撤销。

### 实例：电量值获取

#### JavaScript API

假设要实现一个获取电池电量的异步 JavaScript 函数：
``` ts
getLevel(): Promise<number> // Promise 风格 API
getLevel(options: { // 回调风格 API
    success: (level: number) => void,
    fail: (code: number, msg: string) => void // 电池电量读取实际上不会 fail
}): void
```
使用 `getLevel()` 函数异步地获取电池电量，该函数提供两种 API 风格：`Promise` 风格和回调风格。这两种风格的代码如下：
``` js
async function printBatteryLevel() {
    const level = await getLevel() // 异步获取电量值
    console.log(`battery level: ${level}%`)
}
printBatteryLevel() // 打印电量值，控制台输出示例:
// battery level: 59%

// 下面是回调风格的代码，不建议使用：
getLevel({
    success(level) { console.log(`battery level: ${level}%`) }
})
```

#### C++ 原生接口导出

JavaScript 中的 `getLevel()` 函数实际上是由 C++ 实现的，JavaScript 代码调用这个函数时会发起一个获取电池电量的异步请求，并在得到结果后通过回调函数或者 `Promise` 将结果值返回给 JavaScript 代码。实现 `getLevel()` 的 C++ 函数如下：
``` cpp
static JsValue getLevel(const JsCallContext &ctx) {
    typedef async::ResultSession<BatteryGetLevel> Session;
    Session *session = new Session; // 创建 Session 对象
    session->request(ctx.argc() ? ctx.arg(0) : JsValue());
    return session->promise();
}
```

模板类 `async::ResultSession` （下文省略 `async` 命名空间）实现了异步数据请求所需的框架，每个异步数据请求都包含下列步骤：
1. 创建一个 `ResultSession` 对象
2. 调用 `ResultSession::request()` 方法发起请求
3. 使用 `ResultSession::promise()` 将 `Promise` 对象返回到 JavaScript。

这行代码
``` cpp
session->request(ctx.argc() ? ctx.arg(0) : JsValue());
```
除了发起请求外，我们还将 JavaScript 调用方传入的第 $0$ 个参数传递给 `ResultSession::request()` 方法，`ResultSession` 会自动根据该参数是否存在 `success` / `fail` 等回调函数选择回调和 `Promise` 风格。如果是 `Promise` 风格，那么
``` cpp
return session->promise();
```
会返回一个 `Promise` 对象用于获取异步请求的结果，否则会返回 `undefined` 并由回调函数来处理结果。

#### `ResultSession` 模板类

`ResultSession` 模板类的声明如下：
``` cpp
template<class T, class H = ResultHandler> class ResultSession;
```
模板参数 `T` 是一个类，它实现具体的异步操作，本示例会实现一个 `BatteryGetLevel` 类来实现电池电量的异步获取。模板参数 `H` 决定怎样处理异步请求的结果，默认的 `ResultHandler` 会自动选择回调或者 `Promise` 风格，开发者一般不需要修改。

#### `BatteryGetLevel` 类

`BatteryGetLevel` 类的定义如下：
``` cpp
struct BatteryGetLevel {
    async::Result<int> resolve() const {
        return battery_read_level(); // 获取电池电量
    }
    // errorMessage() 用于将错误码翻译成文本。不过电量读取不会出错，可以随意实现。
    static const char *errorMessage(Status) {
        return "get battery level failed";
    }
};
```
可以看到，`BatteryGetLevel` 有两个成员函数。`resolve()` 函数用于在异步线程中执行具体的操作。`resolve()` 函数的返回值必须是一个 `async::Result<T>` 类型，在本例中则是 `async::Result<int>`。

`resolve()` 函数的返回值 `async::Result<T>` 的模板参数 `T` 类型和 JavaScript API 的回调函数参数或 `Promise` 数据的类型是一致的，例如本例中 `int` 对应到 JavaScript API 为
``` ts
// C++ 的 BatteryGetLevel::resolve() 函数返回值类型
// async::Result<int> 对应 JavaScript 的 Promise<number>
getLevel(): Promise<number>
```

换言之，如果 `resolve()` 返回 `async::Result<String>` 值，那么对应到 JavaScript 中会返回 `Promise<string>`，对于回调函数来说则是 `{ success(value: string): void }`。关于 C++ 和 JavaScript 数据类型的转换细节请参考[数据类型转换](#数据类型转换)。

### 实例：文件读取

#### JavaScript API

假设要实现一个文件读取的异步 JavaScript 函数：
``` ts
readfile(url:string): Promise<string> // Promise 风格 API
readFile(option: {   // 回调风格API
  uri: string,
  success?: (data: string) => void,
  fail?: (code: number, msg: string) => void,
}): void
```
该函数会异步读取文件的内容并通过 `Promise` 对象返回，返回值是文件内容是。实际的 JavaScript 代码是这样的；
``` js
async function printReadFile() {
    const data = await readFile("file.txt") // 异步获取电量值
    console.log('文件读取成功：', data)
}

printReadFile() // 以字符串的形式打印文件内容，控制台输出示例:
// 文件读取成功：hello

// 下面是回调风格的代码
readFile({
    url: "file.txt", 
    success: (data: string) => {  
        console.log('文件读取成功：', data);  
    }
})
```

#### C++ 原生接口导出

JavaScript 中的 `readFile()` 函数实际上是由 C++ 实现的，JavaScript 代码调用这个函数时会发起一个读取文件的异步请求，并在得到结果后通过回调函数或者 `Promise` 将结果值返回给 JavaScript 代码。实现 `readFile()` 的 C++ 函数如下：
``` cpp
JsValue readFile(const JsCallContext &ctx) {
    typedef async::ResultSession<ReadFileRequest> Session;
    if (ctx.argc() > 0 && ctx.arg(0).isObject()) { 
        Session *session = new Session;
        // 将JavaScript 函数参数的 url 字段转换为 C++ String 
        session->client().url = ctx.arg(0)["url"].toString(); 
        session->request(ctx.argc() ? ctx.arg(0) : JsValue());
        return JsValue();
    }
}
```
使用的模板类解释参考 [resultsession-模板类](#resultsession-模板类) 和代码解释参考 电量值获取的 [c-原生接口导出](#c-原生接口导出)。

#### readFile类

`ReadFileRequest` 类的定义如下：
``` cpp
struct ReadFileRequest {
    String url; // 待读取文件的 url。
    Result<String> resolve() {
        ByteArray array = File::read(url); // 通过 url 读取文件内容
        return String(array.charData(), array.size());
    }
    // errorMessage() 用于将错误码翻译成文本
    const char *errorMessage(Status) { return "read file error"; }
};
```
可以看到，`ReadFileRequest` 有两个成员函数。`resolve()` 函数用于在异步线程中执行具体的操作。`resolve()` 函数的返回值必须是一个 `async::Result<T>` 类型，在本例中则是 `async::Result<String>`。需要注意的是 `resolve()` 函数中不能处理 JavaScript 中的数据类型，url 是在 `readFile()` 函数中转换成 C++ 的 String 类型才发起的异步请求，不能在 `resolve()` 函数中处理类似的数据转换。

## 监听模式

在监听模式中，JavaScript 代码调用了 C++ API 创建请求，对多次的异步请求例如传感器数据的监听，在数据发生改变时会执行异步事件将结果返回给 JavaScript，`async::ListenSession` 和 `async::Signal` 模板类提供了该模式的通用操作框架。

### 场景说明

以下场景是典型的监听模式：

- **各种传感器的监听**：由 JavaScript 发起调用，调用监听对应传感器的 C++ API，需要指定回调函数，当传感器读取数据发送改变时，通过异步线程将会将新数据返回到 JavaScript 代码中，作为回调函数的形参。
- **周期性定时任务**：JavaScript 发起调用时需要设置定时任务的时间，任务超时后的回调函数，是否为周期性；当发送请求后每一次定时任务超时后，异步线程会将结果返回到 JavaScript 中，触发 JavaScript 设置的回调函数。

监听模式的场景具有以下特点：
- 启动监听后，支持多次的异步请求，因此可能不适用单次对文件读写和网络状态请求的异步事件；
- 启动监听后，不用时必须要取消监听，不然会造成内存泄漏。

### 实例：监听电池电量值

#### JavaScript API

假如要实现一个监听电池电量的异步 JavaScript 函数：
``` ts
subscribe(callback: (Level: number) => void): number // 监听电池电量值
unsubscribe(subscribeID: number): void // 取消监听
```

使用 `subscribe()` 函数异步地监听电池电量值和 `unsubscribe()` 函数取消监听，使用实例如下：
``` js
// 启动监听，返回一个 id 用来取消监听
let id = subscribe(level => {
  // 若电池电量值发生改变，就会触发监听的回调函数，控制台打印示例：
  // now battery level: 59
  console.log(`now battery level: ${level}%`)
})

unsubscribe(id); // 取消监听
``` 

#### C++ 监听接口导出

JavaScript 中的 `subscribe()` 函数实际上是由 C++ 实现的，JavaScript 代码调用这个函数时会监听电池电量值，每当电量值改变后都会发起一个异步请求，通过回调函数将结果值返回给 JavaScript 代码。实现 `subscribe()` 的 C++ 函数如下：
``` cpp
async::Signal<int> Level; // 创建一个全局的对象 Level

level(45); // Level 数值改变，发送异步请求

static JsValue subscribe(const JsCallContext &ctx) {
    Applet *applet = Applet::current(&ctx.vm());
    if (applet && ctx.argc())  // 检查是否传入的参数
        return applet->bindObject(Level.connect(ctx.arg(0)));
    return JsValue();
}
```
必须要创建了一个全局的对象 `Level`，使用到的模板类 `sync::Signal`（下文省略 `async` 命名空间）实现了监听请求的框架，监听请求包含下列步骤：
1. 在监听之前，必须创建一个全局 `Siganal` 类的对象；
2. 使用`Signal::connect()` 方法将 JavaScript 传入的第一个参数和 `Level` 关联起来；
3. 调用 `Applet::bindObject` 绑定 `Level` 对象；当 `Level` 的状态发生改变时，调用回调函数将结果返回 JavaScript 代码。

这行代码
```cpp
level(45);
```
`Level` 数值变 $45$ ,触发监听机制将会发起一个异步请求，变化后的值作为回调函数的形参，最后将结果返回给 JavaScript 代码。

#### C++ 取消监听接口导出

JavaScript 中的 `unsubscribe()` 函数也是由 C++ 实现的，JavaScript 代码调用这个函数时取消监听。避免不使用监听时造成的内存泄漏。实现 `unsubscribe()` 的 C++ 函数如下：
``` cpp
static JsValue unsubscribe(const JsCallContext &ctx) {
    Applet *applet = Applet::current(&ctx.vm());
    if (applet && ctx.argc() >= 1 && ctx.arg(0).isNumber()) // 检查传递的参数是否正确
        delete applet->unbindObject<async::Slot>(ctx.arg(0).toInt());   
    return JsValue();
}
```
取消监听请求需要调用 `Applet::unbindObject` 解除绑定，需要传入 `subscribe()` 函数的返回 ID 来确定解绑的对象。

#### `Signal` 模板类

``` cpp
template<class T, class H = ListenHandler> class Signal;
```
模板参数 T 是一个类，它实现具体的异步操作，本示例展示一个 `int` 类型来实现电池电量的监听。模板参数 H 决定怎样处理异步请求的结果，默认的 ResultHandler 会自动选择回调或者 Promise 风格，开发者一般不需要修改。

## 数据类型转换

在 `ResultSession` 或者 `ListenSession` 中，异步操作的数据必须要转换成 `JsValue` 对象才能在 JavaScript 代码中使用。例如 [BatteryGetLevel](#batterygetlevel-类) 中定义了
``` cpp
async::Result<int> BatteryGetLevel::resolve() const;
```
函数，这个函数声明意味着电池电量请求的返回数据类型是 `int`，该数据类型是可以转换成 `JsValue` 的，事实上以下类型都可以转换为 `JsValue`：
- `bool`：转换为 `boolean` 类型；
- `int`：转换为 `number` 类型；
- `float` 、`double`：转换为 `number` 类型；
- `String`：转换为 `string` 类型。

::: warning
不支持 C 风格字符串。它会转换换成 `boolean` 类型。
:::

转换的时机是自动的，无需开发者介入。
