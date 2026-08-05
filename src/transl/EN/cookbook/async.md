# Asynchronous Operations

The main purpose of introducing asynchronous operations in JavaScript scripts is to move time-consuming tasks to the background, avoiding JavaScript thread blocking. The tasks processed in the background are mainly I/O-bound operations. Glyphix provides a basic JavaScript asynchronous framework for developers. This framework only makes the necessary abstractions for asynchronous workflows, thus avoiding additional overhead.

## Applicable Scenarios

Applicable scenarios for the asynchronous workflow model:

- A request is initiated by JavaScript code, processed by a native asynchronous processing thread, and the result is returned;
- A request is initiated by JavaScript code, processed by a native asynchronous processing thread, and messages are reported periodically;
  - JavaScript code can actively request to revoke/cancel the request.

## Data Request Pattern

In the data request pattern, JavaScript code calls a C++ API to create a request, executes operations in an asynchronous thread, and returns the result to the JavaScript code. During this process, data is transmitted through an asynchronous queue. The `async::ResultSession` template class provides a general operation framework for this pattern.

### Scenario Description

The following scenarios are typical of the data request pattern:

- **File Read/Write**: When JavaScript initiates a call, it needs to specify the file path, the file offset position, data length, or the data to be written. When the request is sent to the asynchronous thread for execution, the actual file read/write operation is performed, and upon completion, it notifies or returns the result to the JavaScript code.
- **Network Request**: Similar to file read/write, when JavaScript initiates a call, it specifies the request parameters, which are then processed in a background thread and return the result.

The scenarios for the data request pattern have the following characteristics:
- The result returned by a request is single-shot; therefore, sensors or timer listeners that trigger multiple times are not suitable for this pattern;
- A request always yields a result: if the request succeeds, it returns the result; otherwise, it returns an error message. The return of the result is also asynchronous;
- Once initiated, a request cannot be cancelled.

### Example: Getting Battery Level

#### JavaScript API

Suppose we want to implement an asynchronous JavaScript function to get the battery level:
``` ts
getLevel(): Promise<number> // Promise-style API
getLevel(options: { // Callback-style API
    success: (level: number) => void,
    fail: (code: number, msg: string) => void // Battery level reading actually won't fail
}): void
```
Use the `getLevel()` function to asynchronously get the battery level. This function provides two API styles: `Promise` style and callback style. The code for both styles is as follows:
``` js
async function printBatteryLevel() {
    const level = await getLevel() // Asynchronously get the battery level
    console.log(`battery level: ${level}%`)
}
printBatteryLevel() // Print battery level, console output example:
// battery level: 59%

// Below is the callback-style code, which is not recommended:
getLevel({
    success(level) { console.log(`battery level: ${level}%`) }
})
```

#### C++ Native Interface Export

The `getLevel()` function in JavaScript is actually implemented by C++. When JavaScript code calls this function, it initiates an asynchronous request to get the battery level, and upon obtaining the result, returns it to the JavaScript code via a callback function or `Promise`. The C++ function implementing `getLevel()` is as follows:
``` cpp
static JsValue getLevel(const JsCallContext &ctx) {
    typedef async::ResultSession<BatteryGetLevel> Session;
    Session *session = new Session; // Create a Session object
    session->request(ctx.argc() ? ctx.arg(0) : JsValue());
    return session->promise();
}
```

The template class `async::ResultSession` (the `async` namespace is omitted below) implements the framework required for asynchronous data requests. Every asynchronous data request includes the following steps:
1. Create a `ResultSession` object
2. Call the `ResultSession::request()` method to initiate the request
3. Use `ResultSession::promise()` to return the `Promise` object to JavaScript.

This line of code
``` cpp
session->request(ctx.argc() ? ctx.arg(0) : JsValue());
```
In addition to initiating the request, we also pass the $0$-th argument passed by the JavaScript caller to the `ResultSession::request()` method. `ResultSession` automatically chooses between the callback and `Promise` styles based on whether callback functions like `success` / `fail` exist in that argument. If it is the `Promise` style, then
``` cpp
return session->promise();
```
returns a `Promise` object used to get the result of the asynchronous request; otherwise, it returns `undefined` and the callback function handles the result.

#### `ResultSession` Template Class

The declaration of the `ResultSession` template class is as follows:
``` cpp
template<class T, class H = ResultHandler> class ResultSession;
```
The template parameter `T` is a class that implements the specific asynchronous operation. This example will implement a `BatteryGetLevel` class to asynchronously get the battery level. The template parameter `H` determines how to process the result of the asynchronous request. The default `ResultHandler` automatically selects the callback or `Promise` style, and developers generally do not need to modify it.

#### `BatteryGetLevel` Class

The definition of the `BatteryGetLevel` class is as follows:
``` cpp
struct BatteryGetLevel {
    async::Result<int> resolve() const {
        return battery_read_level(); // Get battery level
    }
    // errorMessage() is used to translate error codes into text. However, reading the battery level will not fail, so it can be implemented arbitrarily.
    static const char *errorMessage(Status) {
        return "get battery level failed";
    }
};
```
As can be seen, `BatteryGetLevel` has two member functions. The `resolve()` function is used to execute the specific operation in the asynchronous thread. The return value of the `resolve()` function must be of type `async::Result<T>`, which in this example is `async::Result<int>`.

The template parameter `T` type of the `resolve()` function's return value `async::Result<T>` is consistent with the type of the JavaScript API's callback function parameter or `Promise` data. For example, in this case, `int` corresponds to the JavaScript API as:
``` ts
// The return value type of C++'s BatteryGetLevel::resolve() function
// async::Result<int> corresponds to JavaScript's Promise<number>
getLevel(): Promise<number>
```

In other words, if `resolve()` returns an `async::Result<String>` value, it will correspond to `Promise<string>` in JavaScript, or `{ success(value: string): void }` for callback functions. For details on C++ and JavaScript data type conversion, please refer to [Data Type Conversion](#data-type-conversion).

### Example: Reading a File

#### JavaScript API

Suppose we want to implement an asynchronous JavaScript function for reading files:
``` ts
readfile(url:string): Promise<string> // Promise-style API
readFile(option: {   // Callback-style API
  uri: string,
  success?: (data: string) => void,
  fail?: (code: number, msg: string) => void,
}): void
```
This function will asynchronously read the content of the file and return it through a `Promise` object, with the return value being the file content. The actual JavaScript code looks like this:
``` js
async function printReadFile() {
    const data = await readFile("file.txt") // Asynchronously get file content
    console.log('File read successfully:', data)
}

printReadFile() // Print file content as a string, console output example:
// File read successfully: hello

// Below is the callback-style code
readFile({
    url: "file.txt", 
    success: (data: string) => {  
        console.log('File read successfully:', data);  
    }
})
```

#### C++ Native Interface Export

The `readFile()` function in JavaScript is actually implemented by C++. When JavaScript code calls this function, it initiates an asynchronous request to read a file, and upon obtaining the result, returns it to the JavaScript code via a callback function or `Promise`. The C++ function implementing `readFile()` is as follows:
``` cpp
JsValue readFile(const JsCallContext &ctx) {
    typedef async::ResultSession<ReadFileRequest> Session;
    if (ctx.argc() > 0 && ctx.arg(0).isObject()) { 
        Session *session = new Session;
        // Convert the url field of the JavaScript function parameter to a C++ String 
        session->client().url = ctx.arg(0)["url"].toString(); 
        session->request(ctx.argc() ? ctx.arg(0) : JsValue());
        return JsValue();
    }
}
```
For an explanation of the template class used, refer to [ResultSession Template Class](#resultsession-template-class), and for code explanation, refer to [C++ Native Interface Export](#c-native-interface-export) under Getting Battery Level.

#### ReadFile Class

The definition of the `ReadFileRequest` class is as follows:
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
As can be seen, `ReadFileRequest` has two member functions. The `resolve()` function is used to execute the specific operation in the asynchronous thread. The return value of the `resolve()` function must be of type `async::Result<T>`, which in this case is `async::Result<String>`. Note that JavaScript data types cannot be handled inside the `resolve()` function. The url is converted to a C++ String type inside the `readFile()` function before initiating the asynchronous request; similar data conversions cannot be processed within the `resolve()` function.

## Listening Pattern

In the listening pattern, JavaScript code calls a C++ API to create a request to listen to multiple asynchronous requests (such as sensor data). When the data changes, an asynchronous event is executed to return the result to JavaScript. The `async::ListenSession` and `async::Signal` template classes provide a general operation framework for this pattern.

### Scenario Description

The following scenarios are typical of the listening pattern:

- **Listening to various sensors**: Initiated by JavaScript by calling the C++ API for listening to the corresponding sensor, requiring a callback function. When the sensor reading changes, the asynchronous thread returns the new data to the JavaScript code as a parameter of the callback function.
- **Periodic scheduled tasks**: When JavaScript initiates a call, it needs to set the time for the scheduled task, the callback function after the task times out, and whether it is periodic. When the request is sent, each time a scheduled task times out, the asynchronous thread returns the result to JavaScript, triggering the callback function set by JavaScript.

The scenarios for the listening pattern have the following characteristics:
- Once listening is started, it supports multiple asynchronous requests, so it may not be suitable for single-shot asynchronous events like file reading/writing and network status requests;
- Once listening is started, it must be cancelled when no longer needed, otherwise it will cause a memory leak.

### Example: Listening to Battery Level

#### JavaScript API

Suppose we want to implement an asynchronous JavaScript function to listen to the battery level:
``` ts
subscribe(callback: (level: number) => void): number // Listen to battery level
unsubscribe(subscribeID: number): void // Cancel listening
```

Use the `subscribe()` function to asynchronously listen to the battery level and the `unsubscribe()` function to cancel listening. An example of usage is as follows:
``` js
// Start listening, returns an id used to cancel listening
let id = subscribe(level => {
  // If the battery level changes, the listening callback function is triggered, console print example:
  // now battery level: 59
  console.log(`now battery level: ${level}%`)
})

unsubscribe(id); // Cancel listening
``` 

#### C++ Listening Interface Export

The `subscribe()` function in JavaScript is actually implemented by C++. When JavaScript code calls this function, it listens to the battery level, and every time the level changes, it initiates an asynchronous request, returning the result value to the JavaScript code via a callback function. The C++ function implementing `subscribe()` is as follows:
``` cpp
async::Signal<int> Level; // Create a global object Level

level(45); // Level value changes, send an asynchronous request

static JsValue subscribe(const JsCallContext &ctx) {
    Applet *applet = Applet::current(&ctx.vm());
    if (applet && ctx.argc())  // Check if parameters are passed
        return applet->bindObject(Level.connect(ctx.arg(0)));
    return JsValue();
}
```
A global object `Level` must be created. The template class `async::Signal` used (the `async` namespace is omitted below) implements the listening request framework. A listening request includes the following steps:
1. Before listening, a global `Signal` class object must be created;
2. Use the `Signal::connect()` method to associate the first parameter passed by JavaScript with `Level`;
3. Call `Applet::bindObject` to bind the `Level` object; when the state of `Level` changes, call the callback function to return the result to the JavaScript code.

This line of code
```cpp
level(45);
```
changes the `Level` value to $45$, triggers the listening mechanism to initiate an asynchronous request, uses the changed value as a parameter for the callback function, and finally returns the result to the JavaScript code.

#### C++ Cancel Listening Interface Export

The `unsubscribe()` function in JavaScript is also implemented by C++. When JavaScript code calls this function, it cancels the listening to avoid memory leaks caused by unused listeners. The C++ function implementing `unsubscribe()` is as follows:
``` cpp
static JsValue unsubscribe(const JsCallContext &ctx) {
    Applet *applet = Applet::current(&ctx.vm());
    if (applet && ctx.argc() >= 1 && ctx.arg(0).isNumber()) // Check if the passed parameter is correct
        delete applet->unbindObject<async::Slot>(ctx.arg(0).toInt());   
    return JsValue();
}
```
Canceling a listening request requires calling `Applet::unbindObject` to unbind, passing the ID returned by the `subscribe()` function to determine the object to be unbound.

#### `Signal` Template Class

``` cpp
template<class T, class H = ListenHandler> class Signal;
```
The template parameter `T` is a class that implements the specific asynchronous operation. This example demonstrates using an `int` type to implement battery level listening. The template parameter `H` determines how to process the result of the asynchronous request. The default ResultHandler automatically selects the callback or Promise style, and developers generally do not need to modify it.

## Data Type Conversion

In `ResultSession` or `ListenSession`, data for asynchronous operations must be converted into `JsValue` objects to be used in JavaScript code. For example, [BatteryGetLevel Class](#batterygetlevel-class) defines:
``` cpp
async::Result<int> BatteryGetLevel::resolve() const;
```
This function declaration means that the return data type of the battery level request is `int`, which can be converted to `JsValue`. In fact, the following types can be converted to `JsValue`:
- `bool`: Converted to `boolean` type;
- `int`: Converted to `number` type;
- `float`, `double`: Converted to `number` type;
- `String`: Converted to `string` type.

::: warning
C-style strings are not supported. They will be converted to `boolean` type.
:::

The conversion happens automatically without developer intervention.