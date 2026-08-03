# Asynchronous operations


The main purpose of introducing asynchronous operations in JavaScript scripts is to execute time-consuming work in the background to avoid JavaScript thread blocking. The work placed in the background for processing is mainly IO-intensive operations. Glyphix provides a basic JavaScript asynchronous framework for developers to use, which only makes necessary abstractions for asynchronous workflows, so it does not introduce additional overhead.


## Applicable scenarios


Applicable scenarios for asynchronous workflow models


- The request is initiated by JavaScript code, and the result is returned after processing by the native asynchronous processing thread;
- The request is initiated by JavaScript code, and the native asynchronous processing thread reports the message regularly after processing;
  - JavaScript code can proactively ask for revocation/cancellation requests.


## Data request pattern


In the data request pattern, JavaScript code calls a C++ API to create a request and returns the result to the JavaScript code after performing the operation in an asynchronous thread. In this process, data will be transmitted through an asynchronous queue. The `async::ResultSession` template class provides a general operation framework for this mode.


### Scene description


The following scenarios are typical data request patterns:


- **File reading and writing**: When JavaScript initiates a call, you need to specify the path of the file, the offset position of the file to be read and written, the data length, or the data to be written; when the request is sent to the asynchronous thread for execution, the actual file read and write operation will be performed, and after the operation is completed, the result will be notified or returned to the JavaScript code.
- **Network Request**: Similar to file reading and writing, request parameters must be specified when JavaScript initiates a call, and then the background thread processes and returns the result.


The scenario of data request mode has the following characteristics:
- The result returned by the request is a single time, so sensors or timer monitoring that may be triggered multiple times are not suitable for this mode;
- The request always has a result: if the request is successful, the result is returned, otherwise an error message is returned, and the result is returned asynchronously;
- Once a request is made it cannot be revoked.


### Example: Obtaining power value


#### JavaScript API


Suppose you want to implement an asynchronous JavaScript function to get the battery level:
``` ts
getLevel(): Promise<number> // Promise style API
getLevel(options: { // Callback style API
    success: (level: number) => void,
    fail: (code: number, msg: string) => void // Battery level reading does not actually fail
}): void
```
Use the `getLevel()` function to obtain the battery level asynchronously, which provides two API styles: `Promise` style and callback style. The code for these two styles is as follows:
``` js
async function printBatteryLevel() {
    const level = await getLevel() // Get battery value asynchronously
    console.log(`battery level: ${level}%`)
}
printBatteryLevel() // Print the power value, console output example:
// battery level: 59%

// The following is callback style code, which is not recommended:
getLevel({
    success(level) { console.log(`battery level: ${level}%`) }
})
```


#### C++ native interface export


The `getLevel()` function in JavaScript is actually implemented in C++. When the JavaScript code calls this function, it will initiate an asynchronous request to obtain the battery power, and after getting the result, the result value will be returned to the JavaScript code through the callback function or `Promise`. The C++ function that implements `getLevel()` is as follows:
``` cpp
static JsValue getLevel(const JsCallContext &ctx) {
    typedef async::ResultSession<BatteryGetLevel> Session;
    Session *session = new Session; // Create Session object
    session->request(ctx.argc() ? ctx.arg(0) : JsValue());
    return session->promise();
}
```


The template class `async::ResultSession` (the `async` namespace is omitted below) implements the framework required for asynchronous data requests. Each asynchronous data request includes the following steps:
1. Create a `ResultSession` object
2. Call the `ResultSession::request()` method to initiate a request
3. Use `ResultSession::promise()` to return the `Promise` object to JavaScript.


this line of code
``` cpp
session->request(ctx.argc() ? ctx.arg(0) : JsValue());
```
In addition to initiating the request, we also pass the $0$th parameter passed in by the JavaScript caller to the `ResultSession::request()` method. `ResultSession` will automatically select the callback and `Promise` style based on whether the parameter exists `success` / `fail` and other callback functions. If it is `Promise` style, then
``` cpp
return session->promise();
```
A `Promise` object will be returned to obtain the result of the asynchronous request, otherwise `undefined` will be returned and the callback function will handle the result.


#### `ResultSession` template class


The declaration of `ResultSession` template class is as follows:
``` cpp
template<class T, class H = ResultHandler> class ResultSession;
```
The template parameter `T` is a class that implements specific asynchronous operations. This example will implement a `BatteryGetLevel` class to achieve asynchronous acquisition of battery power. The template parameter `H` determines how to handle the results of asynchronous requests. The default `ResultHandler` will automatically select the callback or `Promise` style, and developers generally do not need to modify it.


#### `BatteryGetLevel` class


The `BatteryGetLevel` class is defined as follows:
``` cpp
struct BatteryGetLevel {
    async::Result<int> resolve() const {
        return battery_read_level(); // Get battery level
    }
    // errorMessage() is used to translate error codes into text. However, the power reading will not go wrong and can be implemented at will.
    static const char *errorMessage(Status) {
        return "get battery level failed";
    }
};
```
As you can see, `BatteryGetLevel` has two member functions. The `resolve()` function is used to perform specific operations in an asynchronous thread. The return value of a `resolve()` function must be of type `async::Result<T>`, in this case `async::Result<int>`.


The `resolve()` function's return value `async::Result<T>`'s template parameter `T` type is consistent with the JavaScript API's callback function parameter or `Promise` data type. For example, in this example, `int` corresponds to the JavaScript API's
``` ts
// C++ BatteryGetLevel::resolve() function return value type
// async::Result <int> corresponds to JavaScript's Promise <number>
getLevel(): Promise<number>
```


In other words, if `resolve()` returns the `async::Result<String>` value, then it will return `Promise<string>` in JavaScript, which is `{ success(value: string): void }` for the callback function. Please refer to [数据类型转换](#数据类型转换) for details on conversion between C++ and JavaScript data types.


### Example: file reading


#### JavaScript API


Suppose you want to implement an asynchronous JavaScript function for file reading:
``` ts
readfile(url:string): Promise<string> // Promise style API
readFile(option: {   // Callback style API
  uri: string,
  success?: (data: string) => void,
  fail?: (code: number, msg: string) => void,
}): void
```
This function will read the content of the file asynchronously and return it through the `Promise` object. The return value is the file content. The actual JavaScript code looks like this;
``` js
async function printReadFile() {
    const data = await readFile("file.txt") // Get battery value asynchronously
    console.log('File read successfully:', data)
}

printReadFile() // Print the file contents as a string, console output example:
// File read successfully: hello

// Below is the callback style code
readFile({
    url: "file.txt",
    success: (data: string) => {
        console.log('File read successfully:', data);
    }
})
```


#### C++ native interface export


The `readFile()` function in JavaScript is actually implemented in C++. When the JavaScript code calls this function, it will initiate an asynchronous request to read the file, and after getting the result, the result value will be returned to the JavaScript code through the callback function or `Promise`. The C++ function that implements `readFile()` is as follows:
``` cpp
JsValue readFile(const JsCallContext &ctx) {
    typedef async::ResultSession<ReadFileRequest> Session;
    if (ctx.argc() > 0 && ctx.arg(0).isObject()) {
        Session *session = new Session;
        // Convert JavaScript function parameter url field to C++ String
        session->client().url = ctx.arg(0)["url"].toString();
        session->request(ctx.argc() ? ctx.arg(0) : JsValue());
        return JsValue();
    }
}
```
For explanation of the template class used, refer to [resultsession-模板类](#resultsession-模板类) and for code explanation, refer to [c-原生接口导出](#c-原生接口导出) for obtaining the electric power value.


#### readFile class


The `ReadFileRequest` class is defined as follows:
``` cpp
struct ReadFileRequest {
    String url; // The url of the file to be read.
    Result<String> resolve() {
        ByteArray array = File::read(url); // Read file content via url
        return String(array.charData(), array.size());
    }
    // errorMessage() is used to translate error codes into text
    const char *errorMessage(Status) { return "read file error"; }
};
```
As you can see, `ReadFileRequest` has two member functions. The `resolve()` function is used to perform specific operations in an asynchronous thread. The return value of a `resolve()` function must be of type `async::Result<T>`, in this case `async::Result<String>`. It should be noted that the `resolve()` function cannot process data types in JavaScript. The url is an asynchronous request that is converted to the C++ String type in the `readFile()` function. Similar data conversion cannot be processed in the `resolve()` function.


## Listen mode


In the listening mode, the JavaScript code calls the C++ API to create a request. For multiple asynchronous requests such as monitoring of sensor data, an asynchronous event will be executed when the data changes and the results will be returned to JavaScript. The `async::ListenSession` and `async::Signal` template classes provide a common operation framework for this mode.


### Scene description


The following scenarios are typical monitoring modes:


- **Monitoring of various sensors**: Initiated by JavaScript, calling the C++ API for monitoring the corresponding sensor requires specifying a callback function. When the sensor reads data and sends changes, the new data will be returned to the JavaScript code through the asynchronous thread as a formal parameter of the callback function.
- **Periodic scheduled tasks**: When JavaScript initiates a call, you need to set the time of the scheduled task, the callback function after the task times out, and whether it is periodic; when each timed task times out after sending a request, the asynchronous thread will return the result to JavaScript, triggering the callback function set by JavaScript.


The monitoring mode scenario has the following characteristics:
- After the monitoring is started, multiple asynchronous requests are supported, so asynchronous events for a single file read and write and network status request may not be applicable;
- After starting the monitoring, you must cancel the monitoring when not in use, otherwise it will cause a memory leak.


### Example: Monitor battery power value


#### JavaScript API


If you want to implement an asynchronous JavaScript function that monitors battery power:
``` ts
subscribe(callback: (Level: number) => void): number // Monitor battery power level
unsubscribe(subscribeID: number): void // Cancel monitoring
```


Use the `subscribe()` function to asynchronously monitor the battery power value and the `unsubscribe()` function to cancel monitoring. The usage examples are as follows:
``` js
// Start monitoring and return an id to cancel monitoring.
let id = subscribe(level => {
  // If the battery power value changes, the listening callback function will be triggered. Example of console printing:
  // now battery level: 59
  console.log(`now battery level: ${level}%`)
})

unsubscribe(id); // Cancel monitoring
```


#### C++ listening interface export


The `subscribe()` function in JavaScript is actually implemented in C++. When the JavaScript code calls this function, it will monitor the battery power value. Whenever the power value changes, an asynchronous request will be initiated and the result value will be returned to the JavaScript code through the callback function. The C++ function that implements `subscribe()` is as follows:
``` cpp
async::Signal<int> Level; // Create a global object Level

level(45); // The Level value changes and an asynchronous request is sent.

static JsValue subscribe(const JsCallContext &ctx) {
    Applet *applet = Applet::current(&ctx.vm());
    if (applet && ctx.argc())  // Check whether the parameters passed in
        return applet->bindObject(Level.connect(ctx.arg(0)));
    return JsValue();
}
```
A global object `Level` must be created. The template class `sync::Signal` used (the `async` namespace is omitted below) implements the framework for monitoring requests. Monitoring requests includes the following steps:
1. Before listening, an object of the global `Siganal` class must be created;
2. Use the `Signal::connect()` method to associate the first parameter passed in by JavaScript with `Level`;
3. Call `Applet::bindObject` to bind the `Level` object; when the state of `Level` changes, call the callback function and return the result to JavaScript code.


this line of code
```cpp
level(45);
```
The value of `Level` changes to $45$, triggering the listening mechanism and will initiate an asynchronous request. The changed value is used as the formal parameter of the callback function, and finally the result is returned to the JavaScript code.


#### C++ Cancel export of listening interface


The `unsubscribe()` function in JavaScript is also implemented in C++. When the JavaScript code calls this function, the listening function is cancelled. Avoid memory leaks caused when not using listeners. The C++ function that implements `unsubscribe()` is as follows:
``` cpp
static JsValue unsubscribe(const JsCallContext &ctx) {
    Applet *applet = Applet::current(&ctx.vm());
    if (applet && ctx.argc() >= 1 && ctx.arg(0).isNumber()) // Check whether the passed parameters are correct
        delete applet->unbindObject<async::Slot>(ctx.arg(0).toInt());
    return JsValue();
}
```
To cancel the listening request, you need to call `Applet::unbindObject` to unbind, and you need to pass in the return ID of the `subscribe()` function to determine the unbound object.


#### `Signal` template class


``` cpp
template<class T, class H = ListenHandler> class Signal;
```
Template parameter T is a class that implements specific asynchronous operations. This example shows a `int` type to monitor battery power. Template parameter H determines how to handle the results of asynchronous requests. The default ResultHandler will automatically choose callback or Promise style, and developers generally do not need to modify it.


## Data type conversion


In `ResultSession` or `ListenSession`, the data of asynchronous operations must be converted into `JsValue` objects before they can be used in JavaScript code. For example, [BatteryGetLevel](#batterygetlevel-类) defines
``` cpp
async::Result<int> BatteryGetLevel::resolve() const;
```
Function, this function declaration means that the return data type of the battery power request is `int`, which can be converted to `JsValue`. In fact, the following types can be converted to `JsValue`:
- `bool`: converted to `boolean` type;
- `int`: converted to `number` type;
- `float`, `double`: converted to `number` type;
- `String`: converted to `string` type.


::: warning

C-style strings are not supported. It will be converted to type `boolean`.
:::



The timing of the conversion is automatic and does not require developer intervention.