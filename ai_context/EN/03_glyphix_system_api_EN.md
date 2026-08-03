# Context File: 03_glyphix_system_api_EN.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/transl/EN/api/system-test.md

# Test Framework

## Importing Modules

``` js
import test from '@system.test'
```

## Introduction

The `system.test` module is an end-to-end testing framework that allows you to programmatically simulate user operations and check whether the UI behavior matches expectations.

Here is a simple example of code that simulates user operations:
``` js
await test.getByClass('play-button').click()
await test.getByClass('more-button').click()
await test.getByClass('download-button').click()
await test.getByClass('close-button').click()
await test.getByClass('menu-button').click()
await test.getHasText('下载列表').click()
await test.getByTag('Scroll').scroll(0, -200, 0.3)
await test.getHasText(/[a-z]/).click()
```
This code automatically waits for elements in the UI to be rendered, brings occluded elements into the visible area via scrolling gestures, and then performs gestures such as clicking or scrolling on them.

## API

### Helper Functions

These functions provide auxiliary features in tests, such as delays.

#### `wait` <decl method type="(duration: number): Promise<void>" />

Asynchronously delays for a specified time, used to wait for certain operations in tests or to simulate user pauses.

### Locators

Locators find elements (native components) from the top-level page of the application, such as by element tag or ID. For more information about locators, please refer to the [`Locator` Object](#locator-object).

#### `getByTag` <decl method type="(tag: string): Locator" />

Locates elements by `tag`. Currently, only UpperCamelCase is supported, such as `'P'`, `'Swiper'`, etc.

#### `getByClass` <decl method type="(class: string): Locator" />

Locates elements by the `class` attribute.

#### `getById` <decl method type="(id: string): Locator" />

Locates elements by the `id` attribute.

#### `getHasText` <decl method type="(text: RegExp | string): <Locator>" />

Locates elements based on whether their `text` attribute matches the `text` parameter. The `text` parameter is a regular expression, for example:
- `/hello/` tests whether the `text` attribute value of the element contains the substring `'hello'`;
- `/^hello/` tests whether the `text` attribute value of the element starts with `'hello'`;
- `/^hello$/` tests whether the `text` attribute value of the element is `'hello'`.

The matching rules for the `text` parameter are the same as [`RegExp.test()`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/RegExp/test).

### `Locator` Object

`Locator` objects are returned by locator APIs and can be used for further operations. All locator operations attempt to automatically wait for the element to appear and bring it into the visible area.

#### `click` <decl method type="(): Promise<void>" />

Simulates a click gesture at the element's position after the element exists and has been scrolled into the visible area.

#### `scroll` <decl method type="(dx: number, dy: number, duration?: number): Promise<void>" />

Simulates a scroll gesture at the element's position after the element exists and has been scrolled into the visible area. `dx` and `dy` are the $(x, y)$ scroll offsets in pixels; the optional `duration` is the duration of the gesture in seconds, with a default value of $0.5 \rm s$.

This method waits for the element's `scrolled` property to become `false` before resolving the Promise object returned. Therefore, for components such as `scroll` and `swiper`, the `scroll()` method will trigger the next operation only after the inertia animation of these components has stopped.

#### `wait` <decl method type="(): Promise<void>" />

Waits for the element to exist and be scrolled into the visible area, without simulating any gestures or other operations.

============================================================
FILE_PATH: src/transl/EN/api/system-path.md

# Path Operations

This module provides interfaces for path operations, including path concatenation, splitting, and normalization.

## Import Module

``` js
import path from '@system.path'
```

## Interface Definitions

#### `path.basename` <decl type="(path: string, suffix?: string): string" method />

Returns the file name portion of the `path`. The specified file name suffix can also be removed by specifying the `suffix` parameter. For example:
``` js
path.basename('/foo/bar/baz.txt') // 'baz.txt'
path.basename('/foo/bar/baz.txt', '.txt') // 'baz'
```

#### `path.dirname` <decl type="(path:string): string" method />

Returns the directory name portion of the `path` (opposite of `basename()`, which discards the file name portion). For example:
``` js
path.dirname('/foo/bar/baz') // '/foo/bar'
```

#### `path.extname` <decl type="(path: string): string" method />

Gets the file extension in the `path`. For example:
``` js
path.extname('table.json') // '.json'
path.extname('/images/icon.png') // '.png'
```

#### `path.isAbsolute` <decl type="(path: string): boolean" method />

Determines whether the `path` is an absolute path. For example:
``` js
path.isAbsolute('/foo/bar'); // true
path.isAbsolute('/baz/..');  // true
path.isAbsolute('qux/');     // false
path.isAbsolute('.');        // false
```

#### `path.join` <decl type="(...paths: string[]): string" method />

Concatenates multiple paths together and normalizes the result. For example:
``` js
path.join('/foo', 'bar', 'baz/asdf', 'quux', '..') // '/foo/bar/baz/asdf'
```

#### `path.normalize` <decl type="(path: string): string" method />

Normalizes the given `path`, resolving `..` and `.`, and removing redundant path separators `/`.

``` js
path.normalize('/foo///bar/.././/baz') // '/foo/baz'
```

#### `path.relative` <decl type="(from: string, to: string): string" method />

Calculates the relative path from `from` to `to`.

``` js
path.relative('/data/orandea/test/aaa', '/data/orandea/impl/bbb') // '../../impl/bbb'
```

============================================================
FILE_PATH: src/transl/EN/api/system-schedule.md

# Scheduled Tasks

## Import Module

``` js
import schedule from "@system.schedule"
// Or
const schedule = require("@system.schedule")
```

Developers need to declare access permission for `watch.permission.SCHEDULE` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

## API

### `scheduleJob`
<decl method><pre>
(options: {
  type: number,
  timeout: number,
  triggerMethod: String,
  interval?: number,
  params?: Object,
}): number
</pre></decl>

Sets a scheduled task. The fields of the `options` parameter are defined as follows:
- `type`:	
  - 1: Hardware time. Modifying the system time can trigger `triggerMethod`.
  - 2: Real elapsed time. Time is calculated even in sleep mode.
- `timeout`:
  - If `type` is 1, this is the timestamp of the first execution time, which is the number of milliseconds from 1970/01/01 00:00:00 GMT to the current time.
  - If `type` is 2, this is the interval between the current time and the first execution time, in milliseconds.
- `triggerMethod`: The method name defined in `app.js`, which is called by the background when the timeout is reached and the app is awakened.
- `interval`: The interval for periodic execution, in milliseconds. If not passed, it will not execute repeatedly.
- `params`: Task parameters.

::: tip
Although the precision of `timeout` and `interval` is in milliseconds, the timing is accurate to the second. The first execution time and the periodic execution interval cannot be less than 60 seconds, otherwise the interface will throw an exception.
:::

The return value is the task ID used to cancel the task. A return value of `-1` indicates that creation failed.

``` js
let id = schedule.scheduleJob({
  type: 1,
  timeout: new Date('2025-03-14T23:00:00').getTime(),  // Timestamp of the first execution time
  interval: 60000,     // Periodic execution interval cannot be less than 60 seconds
  triggerMethod: 'scheduleFunc',
  params: {
    food: 'apple',
  },
})

// app.js
export default {
  scheduleFunc(params) {
    console.log('scheduleFunc', params)
  },
}
```

### `cancel` <decl type="(id: number): void" method/>

Cancels a scheduled task.

``` js
schedule.cancel(id)
```

============================================================
FILE_PATH: src/transl/EN/api/system-launch.md

# App Launch

## Import Module

``` js
import launch from '@system.launch'
```

## API Definition

### `launch` <decl type="(app: string): Promise<bool>" method/>

Launches the specified application and brings it to the foreground. `app` is a string representing the ID of an installed application. The returned Promise indicates whether the application was loaded successfully.

### `inactive` <decl type="(app?: string): Promise<void>" method/>

Switches the application to the background. `app` is the ID of a launched application. If no parameter is specified, the current application is switched to the background. Only foreground applications can be switched to the background.

### `exit` <decl type="(app?: string): Promise<void>" method />

Exits an application. The `app` parameter is the ID of a launched application. If no parameter is specified, the current application is exited.

### `getRunning` <decl type="(): string[]" method />

Gets the list of running application package names, including those in the background.

============================================================
FILE_PATH: src/transl/EN/api/system-prompt.md

# Pop-up

## Import Module

``` js
import prompt from '@system.prompt'
```

## Interface Definition

#### `showToast`
<decl method><pre>
(options: {
  message: string,
  duration?: number,
  important?: boolean
}): void
</pre></decl>

Displays a toast pop-up. A toast is a text pop-up placed at the top layer of the interface. Only one toast instance is displayed in the interface at a time; when there are multiple toast contents, they will be queued and displayed sequentially.

Description of `options` parameter fields:
- `message`: The text to be displayed.
- `duration`: The display duration of the toast in milliseconds (ms). The toast will automatically hide after reaching this timeout.
- `important`: Whether it is an important toast. The default is `false`. If set to `true`, the application is allowed to pop up this toast while in the background.

The display style of the toast (font, color, etc.) is determined by the firmware and cannot be modified within the application. There is also a limit on the display duration of the toast, which ranges from $200$ to $5000$ milliseconds.

#### `showPopup` <decl type="(options: { uri: string, params?: Object }): Promise<any>" method />

Displays a floating page pop-up. Description of `options` parameter fields:
- `uri`: The name of the target page, which needs to be registered in `router` of `manifest.json`.
- `params`: Data to be passed during navigation. The properties of the `params` parameter will replace the `data` property values of the target page.

A floating page is a system-level pop-up (similar to a toast or dialog box), but it is a fully functional page with the highest level of customizability. Unlike general pages, a floating page is displayed in the system's floating page stack rather than the application's own page stack. Therefore, APIs such as `router.back()` in the [page routing](api/system-router) mechanism cannot operate on floating pages. To close a floating page, you can use the [`router.close()`](system-router.md#close) method.

The display hierarchy of a pop-up is higher than that of the application, so floating pages will be displayed above all application pages. All applications share the same floating page stack, and the display hierarchy of floating pages is determined by their pop-up order, meaning that earlier popped-up pages are located at the top. The display hierarchy of a floating page is the same as that of a dialog box, and lower than that of a toast.

Just like `router.push()`, `showPopup()` also returns a Promise object, which will be fulfilled and return a custom result after the floating page exits. For details, please refer to [`router.push()`](system-router.md#push) and [`router.close()`](system-router.md#close).

============================================================
FILE_PATH: src/transl/EN/api/system-exchange.md

# Exchange Data

The data exchange module `system.exchange` is used to store shared data across applications. This data is not persistently stored and will be lost once the device is powered off. Data stored in `system.exchange` can be accessed across all applications, so this module can be used to store some application configuration information, but is not suitable for storing sensitive data.

`system.exchange` stores data in the form of key-value pairs, where the key must be a string, and the value is a JSON value (or a JavaScript value that can be serialized to JSON).

## Import Module

``` js
import exchange from '@system.exchange'
```

## API

### `get` <decl type="(key: string): any" method />

Gets the value corresponding to the key `key` in the storage. Returns `undefined` if the key-value pair does not exist.

### `set` <decl type="(key: string, value: any): void" method />

This method accepts a key `key` and a value `value` as parameters and adds this key-value pair to the storage. If the key already exists, its corresponding value is updated.

### `delete` <decl type="(key: string): boolean" method />

Deletes the key-value pair corresponding to the key `key` from the storage. Returns `true` if the key-value pair exists and is successfully deleted.

### `watch` <decl type="(key: string, callback: (value: any) => void): number" method />

Listens for changes to the data value of the key `key` in the storage, and calls the `callback` function when the value changes. The parameter `value` of the callback function is the new data value. The `watch()` method returns a `watcher ID`, which can be used in the [`unwatch()`](#unwatch) method to stop listening.

::: tip
When listening is no longer needed, the [`unwatch()`](#unwatch) method should be used to stop listening, otherwise it may cause a memory leak.
:::

### `unwatch` <decl type="(watcherID: number): void" method />

Cancels a listener for the key in the storage. The parameter `watcherID` is the `watcher ID` returned when the listener was created by the [`watch()`](#watch) method.

============================================================
FILE_PATH: src/transl/EN/api/system-interconnect.md

# Device Interconnection

## Import Module

``` ts
import interconnect from '@system.interconnect'
```

## Interface Definitions

### `instance` <decl type="(options: {package: string, fingerprint: string}): Connect" method/>

Creates a [`Connect`](#connect-interface) instance.

```js
const connect = interconnect.instance({
  package: "com.xxxx.xxx",
  fingerprint: "xxxxx"
})
```

- package: The package name of the mobile application.
- fingerprint: Fingerprint information, which must be consistent with the fingerprint information passed when creating the connection in the mobile application.

## `Connect` Interface

### `onopen` <decl type="?: () => void" set />

Used to specify the callback when the connection is opened.

```js
connect.onopen = () => {
  console.info("onopen")
}
```

### `onclose` <decl type="?: () => void" set />

Used to specify the callback when the connection is closed.

```js
connect.onclose = () => {
  console.info("onclose")
}
```

### `onerror` <decl type="?: () => void" set />

Used to specify the callback after a connection failure.

```js
connect.onerror = (data: any) => {
  console.info("onerror", data)
}
```

### `onmessage` <decl type="?: () => " set />

Used to specify the callback for receiving data from the mobile App side.

```js
connect.onmessage = (msg => {
  if (msg.isFileType) {
    this.msg = "recv a file " + msg.fileUri
  } else {
    this.msg = "recv a text message " + msg.data
  }
})
```

### `send` <decl type="(options: {data: any}): Promise<any>" method />

Sends data to the mobile App side.

```js
connect.send({
  data: {
    name: "zhangsan"
  }
})
```

============================================================
FILE_PATH: src/transl/EN/api/system-device.md

# Device Information

## Import Module

``` js
import device from '@system.device'
```

Developers need to declare the application's access permission to `watch.permission.DEVICE_INFO` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

## Interface Definition

### `getInfo`
<decl method><pre>
(): Promise<{
  brand: string,
  manufacturer: string,
  model: string,
  product: string,
  osType: string,
  osVersionName: string,
  platformVersionName: string,
  platformVersionCode: number,
  language: string,
  region: string,
  deviceName: string
}>
</pre></decl>

Gets the basic information of the device. The meanings of the property fields in the returned object are:
- `brand`: Device brand name.
- `manufacturer`: Device manufacturer.
- `model`: Device model.
- `product`: Device product code.
- `osType`: Operating system name.
- `osVersionName`: Operating system version name.
- `platformVersionName`: Runtime platform version name.
- `platformVersionCode`: Runtime platform version code.
- `language`: System language.
- `region`: System region.
- `deviceName`: Device name.

### `getId`
<decl method><pre>
(types: ('device' | 'mac' | 'user' | 'advertising')[])
: Promise<{
  device?: string,
  mac?: string,
  user?: string,
  advertising?: string
}>
</pre></decl>

Batch gets device identification information. The `types` parameter specifies the categories of information to be obtained, which is an Array object consisting of elements `'device'`, `'mac'`, `'user'`, or `'advertising'`. Depending on the values in `types`, the meanings of the property fields in the returned object are:
- `type`: .
- `device`: Unique device identifier, present only when `types` contains the `'device'` element.
- `mac`: Device MAC address, present only when `types` contains the `'mac'` element.
- `user`: Unique user identifier, present only when `types` contains the `'user'` element.
- `advertising`: Unique advertising identifier, present only when `types` contains the `'advertising'` element.

### `getDeviceId` <decl type="(): Promise<{deviceId: string}>" method />

Gets the unique device identifier.

### `getSerial` <decl type="(): Promise<{serial: string}>" method />

Gets the device serial number.

### `getTotalStorage` <decl type="(): Promise<{totalStorage: number}>" method />

Gets the total size of the storage space, in bytes.

### `getAvailableStorage` <decl type="(): Promise<{availableStorage: number}>" method />

Gets the available size of the storage space, in bytes.

::: tip
The values returned by `getTotalStorage()` and `getAvailableStorage()` on the simulator may not be accurate and will not change as the storage space changes.
:::

### `screenWidth` <decl type="number" get />

The screen width of the device, in pixels.

### `screenHeight` <decl type="number" get />

The screen height of the device, in pixels.

### `screenDensity` <decl type="number" get />

The screen pixel density of the device, in $\rm PPI$.

### `screenShape` <decl type="'rect' | 'circle'" get />

The screen shape of the device. The values mean the following:
- `'rect'`: The device has a rectangular screen.
- `'circle'`: The device has a circular screen.

### `memoryProfile` <decl type="number" get />

Gets the memory profile property of the device. This property is the JavaScript API version of the [`memory-profile`](/framework/render/media-query.md#memory-profile) media query property. For details, please refer to the documentation of media query properties.

Unlike the `memory-profile` media query property, the value of the `memoryProfile` property is an integer with a fixed unit of $\rm KiB$.

============================================================
FILE_PATH: src/transl/EN/api/system-devtools.md

# Debugging Interface

## Import Module

``` js
import devtools from '@system.devtools'
```

## API

### `command` <decl type="(cmd: string, fn: (argv: string[]) => void): void" method />

Registers a function `fn` as a shell command named `cmd`. Once registered, it can be invoked using the `dev` command on the device terminal. For example:
``` bash
dev cmd arg1 arg2
```
will invoke the command named `'cmd'` with the argument list `['arg1', 'arg2']`.

============================================================
FILE_PATH: src/transl/EN/api/system-geolocation.md

# Geolocation

## Import Module

```js
import geolocation from '@system.geolocation';
```

Developers need to declare the application's access permission to `watch.permission.LOCATION` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

## Interface Definitions

### `getLocation` 
<decl method><pre>
(options: {
  mode?: string
  timeout?: number
}): Promise&lt;Location>
</pre></decl>

Obtain the latitude and longitude of the current location once, returning an asynchronous [Location](#location) object.

`options` Parameter Description
- `mode`: Declares the positioning accuracy. `fine` represents precise positioning, and `coarse` represents rough positioning. The default value is `coarse`.
- `timeout`: Positioning timeout in `ms`, with a default value of 30000.

### `subscribe` <decl type="(callback: (location: Location) => void): number" method/>

Listen for location changes. The `location` parameter of the `callback` is the current [Location](#location) information. The ID returned by this method can be used with the [`unsubscribe()`](#unsubscribe) method to stop listening.

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancel listening for location changes.

## Type Definitions

### `Location`

Used to represent the location information data obtained from positioning.

```ts
ts
type Location = {
  code: number; // Positioning status code, indicating whether the current location information is valid
  msg: string; // Positioning error message
  data: {
    // Location information data
    longitude: number; // Latitude value
    latitude: number; // Longitude value
    coordType: string; // Coordinate system type, such as 'WGS84', 'GCJ02', etc.
  };
};
```

The positioning status codes for the `code` field are as follows:

- `200`: Current location information is valid;
- `1002`: Currently not connected to the mobile phone's Bluetooth network;
- `1300`: The mobile phone cannot obtain positioning services;
- `1301`: Positioning services are not enabled on the mobile phone;
- `1302`: Location permission is not granted to the mobile application;
- `1399`: Unknown error.

============================================================
FILE_PATH: src/transl/EN/api/system-compass.md

# Compass

The `@system.compass` module provides the ability to access the device's compass sensor, allowing you to obtain the device's orientation relative to the Earth's magnetic North Pole.

## Import Module

``` js
import compass from '@system.compass'
```

## Interface Definitions

### `subscribe` <decl type="(callback: (data: Value) => void): number" method/>

Subscribes to compass data changes. When the device orientation changes, the callback function is automatically invoked. The `callback` function receives compass data of type [`Value`](#value).

Returns a subscription ID used for unsubscribing.

### `unsubscribe` <decl type="(subscribeId: number): void" method/>

Unsubscribes from compass data. The `subscribeId` parameter is the subscription ID returned by the [`subscribe()`](#subscribe) method.

This method should be called to cancel the `subscribe()` subscription when the page or component is destroyed:
``` js
const subscribeId = compass.subscribe((data) => {
  console.log(`Direction: ${data.direction} rad`)
  console.log(`Accuracy: ${data.accuracy}`)
})

// Unsubscribe
compass.unsubscribe(subscribeId)
```


### `calibration` <decl type="(): Promise<void>" method/>

Starts the compass calibration process. When the compass accuracy is low, guide the user to perform actions and call this method to calibrate the compass.

This function returns a Promise object with no result, which is resolved when the system completes the calibration.

### `getValue` <decl type="(): Promise<Value>" method/>

Gets the current compass data. Returns an asynchronous result as a Promise object containing compass direction and accuracy information (of type [`Value`](#value)).

Example:
``` js
// Using Promise
compass.getValue().then((data) => {
  console.log(`Direction: ${data.direction} rad`)
  console.log(`Accuracy level: ${data.accuracy}`)
})

// Using async/await
async function getCompassData() {
  const data = await compass.getValue()
  console.log(`Direction: ${data.direction} rad`)
  console.log(`Accuracy level: ${data.accuracy}`)
}
```

::: note
Due to implementation limitations, this method does not support callback-style calls (such as `{ success: (data) => {...} }`); please use Promise or async/await instead.
:::

## Type Definitions

### `Value`

The signature of the compass data type `Value` is as follows:
``` ts
type Value = {
  direction: number  // Compass direction (in radians)
  accuracy: number   // Compass accuracy level
}
```
Property descriptions:
- `direction`: The angle in radians between the device's Y-axis and the Earth's magnetic North Pole, with a value range of $[0,2\pi]$, where:
  - `0`: Due North
  - `Math.PI / 2` (approx. 1.57): Due East
  - `Math.PI` (approx. 3.14): Due South
  - `3 * Math.PI / 2` (approx. 4.71): Due West
- `accuracy`: The accuracy level of the compass data
  - `3`: High accuracy
  - `2`: Medium accuracy
  - `1`: Low accuracy
  - `0`: Unreliable (reason unknown)
  - `-1`: Unreliable (sensor disconnected)

Example:
``` js
// Determine direction
const data = await compass.getValue()
const degrees = data.direction * 180 / Math.PI // Convert to degrees

console.log(`Direction: ${degrees}°`)
if (degrees >= 337.5 || degrees < 22.5) {
  console.log('Facing North')
} else if (degrees >= 22.5 && degrees < 67.5) {
  console.log('Facing Northeast')
} else if (degrees >= 67.5 && degrees < 112.5) {
  console.log('Facing East')
}
// ... Other direction checks

// Check accuracy
if (data.accuracy >= 2) {
  console.log('Compass accuracy is good')
} else if (data.accuracy === 1) {
  console.log('Compass accuracy is low, calibration recommended')
  compass.calibration()
} else {
  console.log('Compass data is unreliable')
}
```

============================================================
FILE_PATH: src/transl/EN/api/system-router.md

# Page Routing

## Importing Modules

``` js
import router from '@system.router'
```

## Interface Definitions

### `push` <decl type="(options: {uri: string, params?: Object}): Promise<any>" method />

Navigates to a specified page within the application. Description of `options` parameter properties:
- `uri`: The name of the target page, which must be configured in `manifest.json`;
- `params`: Data to be passed during navigation. The properties of the `params` parameter will replace the `data` property value of the target page.

`push()` returns a Promise object, which is fulfilled after the target page is closed and returns a custom result. For example:
```js
const result = await router.push({ uri: 'PageName' })
console.log("the page 'PageName' was closed with the result:", result)
```
Here, `result` is the page return value specified by the [`close()`](#close) method, which you can obtain using the method above.

::: warning
The return time of a page typically depends on user actions, so `await router.push()` may wait for a long time. If you do not need to get the return value of the page, it is not recommended to use `await` to wait for the page return.
:::

When the page is in the `singleTask` launch mode, navigating to an already opened page is similar to [`back('<page-name>')`](#back). See [`launchMode`](/framework/application/manifest.md#launchmode) <version-badge since="0.8" />.

### `replace` <decl type="(options: {uri: string, params?: Object}): Promise<boolean>" method />

Navigates to a specified page within the application and closes the current page. Description of `options` parameter properties:
- `uri`: The name of the target page, which must be configured in `manifest.json`;
- `params`: Data to be passed during navigation. The properties of the `params` parameter will replace the `data` property value of the target page.

Like [`push()`](#push) and [`back()`](#back), calling `replace()` always plays the standard page transition animation. Even if `replace()` is called **immediately** in the code, as long as the current page has entered the rendering stage, the user may still briefly see a single frame of the current page before entering the target page. Therefore, `replace()` is more suitable for scenarios where "the current page itself is part of the user flow," rather than as a means for "silent redirection" or "completely hiding the entry page."

If the current page was popped via the [`push()`](#push) method, calling `replace()` will replace the current page, which causes the Promise object returned by [`push()`](#push) to be fulfilled.

::: tip
Do not use the [`push()`](#push) method to navigate to a new page and immediately [`close()`](#close) the current page to achieve page replacement, as this will interrupt the interaction animation and may even cause screen flickering. Always use the `replace()` method to replace pages to ensure a smooth page transition experience.

In addition, if you want a certain entry page (such as the `router.entry` page configured in `manifest.json`, a privacy check page used only for dispatching, etc.) to **not be displayed at all** in certain scenarios, do not call `replace()` inside that page in an attempt to "jump away immediately." Such requirements should be handled by [replacing the default page](#replacing-the-default-page), directly pushing (`push()`) the actual first screen page early in the application startup phase (such as `onCreate()` / `onRoute()`).
:::

`replace()` is commonly used in scenarios such as [splash screen navigation](#splash-screen-navigation).

When the page is in the `singleTask` launch mode, navigating to an already opened page is similar to [`back('<page-name>')`](#back). See [`launchMode`](/framework/application/manifest.md#launchmode) <version-badge since="0.8" />.

### `back` <decl type="(name?: string): Promise<boolean>" method />

Returns to the page named `name`. If `name` is empty or omitted, `router.back()` returns to the previous page.

Calling the `back()` method causes the Promise returned by the [`push()`](#push) method of the relevant page to be fulfilled.

### `close` <decl type="(page: Component, result?: any): Promise<void>" method />

Closes the specified page. `page` is the view-model object of a page. For example:
``` js
router.close(this.$page)
```

The `router.close()` method can close any page within the application. If the target page is at the top of the page stack, `router.close()` is equivalent to `router.back()`. `router.close()` can also correctly close floating pages.

The optional parameter `result` is used to specify the return value of the page, which is the result when the Promise returned by [`router.push()`](#push) or [`prompt.showPopup()`](system-prompt.md#showpopup) that popped the page is fulfilled. Considering that there are many ways to exit a page (such as user swiping, the `router.back()` method, etc.), you can explicitly call the `close()` method in the [`onDestroy()`](/framework/component/life-cycle.md#ondestroy) lifecycle hook of the page component to ensure the page return value is passed:
```js
import router from '@system.router'

export default {
  // This is a component object ...
  onDestroy() {
    router.close(this.$page, this.pageResult)
  },
  // Assume a certain method sets the page return value
  someMethod() {
    this.pageResult = { message: 'some page result' }
  },
}
```

::: tip
If `router.close()` is called multiple times on a page before `onDestroy()` returns **with the `result` parameter passed**, only the last call will take effect as the return value of the page. This is why it is recommended to return values via the `close()` method in the `onDestroy()` lifecycle hook.
:::

### `clear` <decl type="(): Promise<void>" method />

Clears all underlying pages, leaving only the top-level page. Calling the `clear()` method does not play page transition animations. The Promise object returned by this method is fulfilled after all underlying pages are exited.

### `getPages` <decl type="(): Component[]" method />

Gets the page components of all pages in the current application page stack.

### `getLength` <decl type="(): number" method />

Gets the number of pages in the current application page stack.

### `getPagesName` <decl type="(): String[]" method />

Gets the names of all pages in the current application page stack.

### `getPage` <decl type="(index: number): Component | undefined" method />

Gets the page component specified by `index` in the current application. `index` is the index of the page (i.e., its position in the page stack). Returns `undefined` if the searched page does not exist.

### `getIndex` <decl type="(component: Component): number | undefined" />

Gets the page index specified by the page component `component` in the current application. Returns `undefined` if the searched page does not exist.

### `queryPage` <decl type="(name: string): Component[]" />

Gets a list of all pages named `name` in the page stack. The order of the page list is the same as that of the page stack.

### `queryIndex` <decl type="(name: string): number[]" />

Gets the indices of all pages named `name` in the page stack. The order of the page index values is the same as that of the page stack.

## Development Notes

### Repeated Page Pushing

Incorrect use of the `router.push()` method may lead to repeatedly pushing the same page. Consider such an element:
``` html
<p on:click="onClick">Click Me!</p>
```
There is no issue when the component's `onClick()` event callback method simply pushes a new page:
``` js
export default{
  onClick() {
    router.push({ uri: 'CoverPage' })
  }
}
```
Because the page does not respond to gestures while playing transition animations (if any), `router.push()` will not be called repeatedly. However, if `onClick()` calls `router.push()` after an asynchronous operation, issues may arise, for example:
``` js
export default{
  async onClick() {
    // A one-second timer is used here to simulate an asynchronous operation. Real asynchronous operations,
    // such as file read/write or network status queries, will encounter the same issue
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    // Call router.push() after the asynchronous operation
    router.push({ uri: 'CoverPage' })
  }
}
```
If the user clicks the "Click Me!" button multiple times during the asynchronous operation (the timer in the example), the page will be pushed repeatedly. You can try the following demo to verify it:

<glyphix id="api-router-push-repeat-1" height="100" inline>

``` html
<div class="window">
  <p class="button" on:click="onClick">Click Me!</p>
</div>
```

``` css
.window {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #e5e5e5;
  border-radius: 12px;
}

.button {
  border: 2px solid gray;
  border-radius: 20%;
  padding: 8px;
}
```

``` js
import router from '@system.router'

export default {
  async onClick() {
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    router.push({ uri: 'CoverPage' })
  }
}
```

</glyphix>

First, click the "Click Me!" button rapidly multiple times within one second. This will cause the Cover Page to be pushed repeatedly, and you can observe the number of repeated pushes through the counter displayed on that page.

Next, click the Cover Page or swipe right to return to the previous page. At this point, you will find that no matter how fast or continuously you click, the pages always return one by one without duplicate operations, because gestures are not responded to during transition animations.

#### Avoiding Asynchronous Operations

If you need to navigate pages within the callback function of a gesture operation (such as a click gesture), asynchronous operations should be avoided, as this not only easily leads to repeated page pushing, but also increases gesture response latency. In particular, note that the latency of certain asynchronous operations is uncontrollable, such as checking online status in a poor network environment, which may take a long time.

Therefore, in scenarios where page navigation needs to be triggered by a click, it is best to move potential network accesses to the new page and present a busy state via loading animations.

#### Workarounds

If asynchronous operations must be performed before a gesture-triggered page navigation, be sure to use a specific flag to prevent repeated page navigation. Taking the `onClick()` callback above as an example:
``` js
export default {
  async onClick() {
    // Add an isClicked flag to skip duplicate operations; does not need to be a reactive property
    if (this.isClicked)
      return
    // Mark isClicked before executing gesture response logic
    this.isClicked = true
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    router.push({ uri: 'CoverPage' })
    // Clear isClicked after executing gesture response logic
    this.isClicked = false
  }
}
```
Using the same method to continuously click the "Click Me!" button will no longer repeatedly push the Cover Page:

<glyphix id="api-router-push-repeat-2" height="100" inline>

``` html
<div class="window">
  <p class="button" on:click="onClick">Click Me!</p>
</div>
```

``` css
.window {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #e5e5e5;
  border-radius: 12px;
}

.button {
  border: 2px solid gray;
  border-radius: 20%;
  padding: 8px;
}
```

``` js
import router from '@system.router'

export default {
  async onClick() {
    if (this.isClicked)
      return
    this.isClicked = true
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    router.push({ uri: 'CoverPage' })
    this.isClicked = false
  }
}
```

</glyphix>

This example also confirms that asynchronous operations indeed increase page navigation latency—users cannot see any return during the one-second wait for the timer to time out!

### Replacing the Default Page

Developers may not want the application to enter the [`router.entry`](/framework/application/manifest.md#entry) page of `manifest.json` upon startup. A typical scenario is when starting the application via a deeplink, where it should navigate to a specific page based on specific request parameters instead of entering the entry page.

In addition to deeplinks, applications during cold startup often need to select different first screens based on local state, such as deciding whether to enter the login page or home page based on the login state, or entering the privacy page or functional home page based on the locally stored privacy agreement consent flag. If one of these pages is directly configured as `router.entry` and then [`router.replace()`](#replace) is used inside that page to navigate, unwanted pages will be briefly displayed in certain scenarios, looking like the page "flashed."

To solve this, you only need to push (`router.push()`) the page you actually want to display before the [`onShow()`](/framework/component/life-cycle.md#onshow-1) lifecycle hook is called during the application startup phase. Typically, local state checks and home page navigation can be completed in the [`onCreate()`](/framework/component/life-cycle.md#oncreate) or [`onRoute()`](/framework/component/life-cycle.md#onroute) lifecycle hooks of the application. For example, synchronously read the stored privacy agreement state in `onCreate()` of `app.ux`/`app.js`, and then directly navigate to the privacy page or home page:
```js
// app.js
import router from '@system.router'
import storage from '@system.storage'

export default {
  onCreate() {
    const agreed = storage.get('privacyAgreed')
    if (agreed) // User has agreed to the privacy policy, enter the functional home page directly
      router.push({ uri: 'MainPage' })
    else // User has not yet agreed to the privacy policy, display the privacy page on the first screen
      router.push({ uri: 'PrivacyPage' })
  }
}
```
Once the developer manually navigates pages early in the application startup, the actual **first screen page** displayed to the user for this startup is the target page pushed via `router.push()`. `router.entry` in `manifest.json` is used only as an internal entry and will not flash briefly on the interface.

### Splash Screen Navigation

Many applications display a splash logo page when first entered, and then navigate to the actual functional home page. A typical routing structure is: `router.entry` points to the logo page, and the logo page navigates to the home page via [`router.replace()`](#replace) upon initialization. Thus, after the application starts, the user first sees a brief splash screen, followed by the animation transitioning from the splash page to the home page, and the splash page is removed from the page stack after navigation.
``` js
// Assuming this is the index.ux script of the logo page
export default {
  onInit() {
    // Navigate after a delay on the splash logo page
    setTimeout(() => {
      router.replace({ uri: 'MainPage' })
    }, 1000)
  },
}
```
Under this structure, the logo page itself is part of the product design, so users briefly seeing the logo and then transitioning to the home page is expected behavior. Note that `replace()` can only ensure that the transition animation from the logo page to the home page is smooth; the first frame of the logo page will still appear on the screen and cannot be skipped "silently."

If the application is not designed with a separate logo or splash page, but still adopts the "entry page + `replace()` navigation" approach—such as configuring the privacy agreement page as `router.entry` and switching to the home page via `replace()` inside it—the user will see that entry page "flash" when cold-starting the application, and then switch to `MainPage` via a transition animation.

::: tip
This phenomenon is determined by the routing mechanism itself. If you do not want users to observe "page switching," you should prioritize incorporating the approach in the [Replacing the Default Page](#replacing-the-default-page) section, directly selecting the final first screen via `router.push()` during the application startup phase, rather than replacing itself inside the entry page using `replace()`.
:::

============================================================
FILE_PATH: src/transl/EN/api/system-app.md

# Application Context

## Import Module

```js
import app from '@system.app'
```

## Interface Definition

### `getInfo` <decl type="(): Manifest" method/>

Gets the context information of the current application and returns a [`Manifest` object](./system-package.md#manifest-object), which contains basic application information such as package name and version number.

### `terminate` <decl type="(): void" method version="0.8"/>

Terminates the execution of the current application. After calling this method, the application will be closed, and the user needs to restart it to continue use.

::: note Compatibility Risk
This API is not supported on all platforms. You can temporarily use the [`launch.exit()`](./system-launch.md#exit) method as an alternative.
:::

### `loadLibrary` <decl type="(name: string): object | undefined" method/>

Loads a Library Loader registered by native implementation by name, and returns the corresponding library object. If the library with the specified name is not registered, `undefined` is returned.

Typically, it is recommended to mount the library object onto the APP object:
```js
// app.js
import app from '@system.app'

export default {
  customLib: app.loadLibrary('custom-library'),
  onCreate() {
    if (!this.customLib) {
      // Handle library loading failure, e.g., fall back to script implementation
      this.customLib = someStubImplementation();
    } else {
      // Use the library object normally
      this.customLib.someFunction()
    }
  }
}
```
In this way, components can directly use `this.$app.customLib` to access the library object.

`loadLibrary()` is suitable for accessing non-standard system functions. Applications can check whether the return value is `undefined` to determine whether the current platform supports the library, thereby degrading to a scripted stub implementation in a general simulator environment without relying on the simulator's special handling of specific module paths.

If the application needs to support both standard Quick App APIs and system-customized features, it can decide whether to fall back based on the return result of `loadLibrary()`.

### `keepForeground` <decl type="(options: { enable: boolean }): void" method/>

Sets whether the application should stay in the foreground. If the `enable` property in the `options` parameter is `true`, the application will attempt to stay in the foreground.

Using this method requires declaring the permission for `watch.permission.FOREGROUND_SERVICE` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

This method is only a hint for system behavior rather than a mandatory guarantee. The application may still be switched to the background due to user operations or other high-priority policies. When using this method to keep the application in the foreground, the device can still enter low-power mode:

- If the AOD (Always on Display) mode is enabled, the UI refresh rate will be reduced.
- Otherwise, the screen will turn off after a period of time, but the application will still keep running in the foreground.

After the device enters low-power mode (including turning off the screen), foreground applications will still be scheduled and executed at a lower frequency instead of going completely to sleep. Therefore, this can be used for navigation or fitness applications.

============================================================
FILE_PATH: src/transl/EN/api/system-file.md

# File System Operations

This module provides Promise-style file system operation APIs. Compared to the callback style, the Promise style avoids callback hell and reduces code complexity.

::: warning
Since callback-style file APIs are extremely prone to pitfalls in timing, concurrency, and error handling, it is strongly recommended to use the [Promise/`await` API](./README.md#quickapp-asynchronous-interfaces). For detailed suggestions, please refer to [Common Pitfalls and Recommendations](#common-pitfalls-and-recommendations).

The APIs in `@system.file` are all [asynchronous file operations](#asynchronous-file-operations), which are fundamentally different from synchronous I/O access. Please make sure you understand the basic concepts of asynchronous programming and are familiar with the usage of Promises and `async/await`.
:::

## Importing the Module

``` js
import file from '@system.file'
```

## Instructions

### Error Codes

The meanings of the returned error codes are:
- `202`: Invalid parameter;
- `300`: I/O operation failed;
- `400`: Insufficient permissions;

## API Definitions

### `readText`
<decl method><pre>
(params: {
  uri: string
}): Promise&lt;string>
</pre></decl>

Reads the contents of a text file. Description of `params` fields:
- `uri`: The URI of the file to be read.

### `writeText`
<decl method><pre>
(params: {
  uri: string,
  text: string,
  append?: boolean
}): Promise&lt;void>
</pre></decl>

Writes text to a file. If the file does not exist, a new file will be created. This function also automatically creates parent directories. `params` fields:
- `uri`: The URI of the file to be written.
- `text`: The text content to be written to the file.
- `append`: If `true`, the data is appended to the end of the file; if `false`, it overwrites the original content. Defaults to `false`.

### `read`
<decl method><pre>
(params: {
  uri: string,
  position?: number,
  length?: number
}): Promise&lt;ArrayBuffer>
</pre></decl>

Reads file contents into an `ArrayBuffer` object. `params` fields:
- `uri`: The URI of the file to be read.
- `position`: The offset position for reading the file, defaulting to $0$.
- `length`: The number of bytes expected to be read. If not specified, it reads to the end of the file.

### `write`
<decl method><pre>
(params: {
  uri: string,
  data: ArrayBuffer,
  position?: number,
  append?: boolean
}): Promise&lt;void>
</pre></decl>

Writes byte data from an `ArrayBuffer` into a file. If the file does not exist, a new file will be created. This function also automatically creates parent directories.

Description of `params` fields:
- `uri`: The URI of the file to be written.
- `data`: The data to be written.
- `position`: The offset position for writing to the file, defaulting to $0$.
- `append`: If `true`, appends the data to the end of the file and ignores the `position` parameter.

### `copy`
<decl method><pre>
(params: {
  srcUri: string,
  dstUri: string
}): Promise&lt;void>
</pre></decl>

Copies a source file to a specified location, automatically creating the target directory. `params` fields:
- `srcUri`: The URI of the source file.
- `dstUri`: The URI of the target file.

### `rename`
<decl method><pre>
(params: {
  oldUri: string,
  newUri: string
}): Promise&lt;void>
</pre></decl>

Renames a file or directory, automatically creating the target directory. `params` fields:
- `oldUri`: The URI of the file or directory before renaming.
- `newUri`: The URI after renaming.

### `list`
<decl method><pre>
(params: {
  uri: string,
}): Promise&lt;Array>
</pre></decl>

Lists all items (files or directories) under a specified directory. `params` fields:
- `uri`: The URI of the directory to list. Files within the application resource package do not support listing.

The parameter of the `Promise` is an array containing file information, structured like this:
``` js
[
  {
    uri: 'fonts'
  },
  {
    uri: 'font-faces'
  },
]
```

::: tip
You cannot list files inside the application resource package. Therefore, usages that directly use [paths](/framework/application/resource.md#uri-and-paths), such as `await file.list({ uri: "/assets/images" })`, are invalid. In fact, various [`internal`](/framework/application/resource.md#internal) URI schemes should be used instead.
:::

### `access`
<decl method><pre>
(params: {
  uri: string
}): Promise&lt;boolean>
</pre></decl>

Checks whether a file exists. `params` fields:
- `uri`: The URI of the file to check.

### `mkdir`
<decl method><pre>
(params: {
  uri: string,
  recursive?: boolean
}): Promise&lt;void>
</pre></decl>

Creates a directory. `params` fields:
- `uri`: The URI of the directory to be created.
- `recursive`: Whether to create recursively (if the parent directory does not exist, create the parent directory first). Defaults to `false`.

### `remove`
<decl method><pre>
(params: {
  uri: string,
  recursive?: boolean
}): Promise&lt;void>
</pre></decl>

Deletes a directory or file. `params` fields:
- `uri`: The URI of the directory to be deleted.
- `recursive`: Whether to delete recursively. Defaults to `false`. When non-recursive, it can only delete files or empty directories.

### `stat`
<decl method><pre>
(options: {
  uri: string
}): Promise&lt;{size: number}>
</pre></decl>

Gets the attribute information of a file. The fields of the `options` parameter are described as follows:
- `uri`: The URI of the file whose attributes are to be retrieved.

`stat()` asynchronously returns an object containing the following file attributes:
- `size`: The size of the file in bytes.

## Common Pitfalls and Recommendations

The following examples are based on typical problems of the "callback-style" approach, demonstrating why they easily fail or become hard to maintain in file I/O, and providing equivalent rewrites using Promise/`await`.

### Asynchronous File Operations

All APIs in the `@system.file` module are **asynchronous operations**. This means that when you call a file operation function, it will **return immediately** without waiting for the actual I/O operation to complete. File read and write operations are performed in the background, and you will be notified of the result via a Promise once the operation completes.

::: danger Must-Read for Beginners
If you are not familiar with asynchronous programming, please carefully read this section. **Ignoring the return value of an asynchronous operation** or **failing to wait for the Promise to complete** will lead to serious program errors. These errors may not manifest in the simulator, but on real devices, they will cause data loss or program errors.
:::

#### What is an Asynchronous Operation?

In synchronous programming, code executes sequentially, and each line of code finishes executing before the next one starts:

```js
// Synchronous code example (pseudocode, the file API does not provide synchronous versions): blocks and waits for file reading
const text = file.readTextSync({ uri: 'internal://files/data.txt' });
console.log(text); // Will definitely output the file content
console.log('Read completed');
```

However, in asynchronous programming, I/O operations do not block code execution. When you call an asynchronous function, it immediately returns a Promise object, while the actual file operation takes place in the background:

```js
// Error: Ignoring the Promise, not waiting for the operation to complete (returns immediately)
file.readText({ uri: 'internal://files/data.txt' });
console.log('This line of code executes immediately, at which point the file may not have finished reading yet!');

// Correct: Using await to wait for the operation to complete
const text = await file.readText({ uri: 'internal://files/data.txt' });
console.log(text); // At this point the file has been read and can be safely used
console.log('Read completed');
```

#### Why Must You Use `await`?

Failing to use `await` to wait for asynchronous operations to complete leads to the following serious problems.

Data being used before it is ready:
```js
// Error example: Ignoring the return value
function loadConfig() {
  let config = null;
  file.readText({ uri: 'internal://files/config.json' })
    .then(text => config = JSON.parse(text)); // This callback function will execute at some point in the future
  // Here config is still null because file reading is not finished yet!
  console.log(config.theme); // Error: Trying to access null.theme, will crash
  return config; // Returns null
}

// Correct example: Waiting for data to be ready
async function loadConfig() {
  const text = await file.readText({ uri: 'internal://files/config.json' });
  const config = JSON.parse(text);
  console.log(config.theme); // Correct: File is read, safe to access
  return config; // Returns the actual configuration object
}
```

Disordered operation sequences:
```js
// Error example: Not waiting for the write to complete
async function saveAndLoad() {
  // Writes new data, but does not wait for completion
  file.writeText({ uri: 'internal://files/score.txt', text: '100' });
  
  // Reads immediately; at this point, the write may not be finished, and old data might be read!
  const score = await file.readText({ uri: 'internal://files/score.txt' });
  console.log(score); // May output the old value instead of '100'
}

// Correct example: Waiting for the write to complete before reading
async function saveAndLoad() {
  // Use await to wait for the write to finish
  await file.writeText({ uri: 'internal://files/score.txt', text: '100' });
  
  // Now read, ensuring the newly written data is retrieved
  const score = await file.readText({ uri: 'internal://files/score.txt' });
  console.log(score); // Outputs '100'
}
```

Race conditions and data corruption:

```js
// Error example: Multiple concurrent writes to the same file
async function appendLog(message) {
  const log = await file.readText({ uri: 'internal://files/log.txt' });
  // Continuing execution without using await to wait for the write to complete
  file.writeText({ uri: 'internal://files/log.txt', text: log + message + '\n' });
}

// Concurrent calls: not awaiting appendLog
appendLog('Event A'); // Read -> Write A
appendLog('Event B'); // Read -> Write B
// Result: Both reads may fetch the exact same old content, and the later write will overwrite the earlier one, causing 'Event A' to be lost.

// Correct example: Waiting for each write to complete
async function appendLog(message) {
  const log = await file.readText({ uri: 'internal://files/log.txt' });
  await file.writeText({ uri: 'internal://files/log.txt', text: log + message + '\n' });
}

// Sequential calls
await appendLog('Event A'); // Complete Read -> Write -> Finish
await appendLog('Event B'); // Complete Read -> Write -> Finish
// Result: Both events are correctly recorded.
```

#### Simulator Pitfalls

::: warning The Simulator Cannot Expose All Asynchronous Issues
In the development simulator, due to the extremely fast I/O speed of the computer, file operations complete almost instantaneously. Therefore, even if code does not correctly use `await`, it may still appear to "work normally" in the simulator.
:::

File system I/O on real embedded devices has the following limitations:
- Flash storage read and write speeds are relatively slow;
- File system caching capability is weak, and reading/writing files typically accesses the storage medium directly;
- System resources are limited, and I/O operations are queued and delayed.

Code that fails to use `await` will **almost certainly fail** on real devices! Do not ignore asynchronous programming standards just because testing passes in the simulator.

#### Rules for Correctly Using `async/await`

1. Any function that calls a file API should be declared as `async`:
   ```js
   async function saveData(data) {
     await file.writeText({ uri: 'internal://files/data.txt', text: data });
   }
   ```
2. Add the `await` keyword before all file operations:
   ```js
   const content = await file.readText({ uri: 'internal://files/data.txt' });
   ```
3. Use `try/catch` to handle potential errors:
   ```js
   try {
     await file.writeText({ uri: 'internal://files/data.txt', text: 'hello' });
   } catch (err) {
     console.error('Write failed:', err);
   }
   ```
4. Operations that need to be executed sequentially must be `await`ed in order:
   ```js
   // Correct: Write first, then read to verify
   await file.writeText({ uri: 'internal://files/data.txt', text: 'test' });
   const verify = await file.readText({ uri: 'internal://files/data.txt' });
   console.log(verify === 'test' ? 'Verification successful' : 'Verification failed');
   ```
5. Unrelated operations can be executed in parallel, but you must wait for all of them to complete:
   ```js
   // Correct: Read multiple files in parallel, but wait for all to complete
   const [file1, file2, file3] = await Promise.all([
     file.readText({ uri: 'internal://files/a.txt' }),
     file.readText({ uri: 'internal://files/b.txt' }),
     file.readText({ uri: 'internal://files/c.txt' })
   ]);
   ```

#### Complete Example: User Configuration Management

```js
import file from '@system.file'

const CONFIG_URI = 'internal://files/user-config.json';

// Correct asynchronous configuration management
class ConfigManager {
  async load() {
    try {
      const text = await file.readText({ uri: CONFIG_URI });
      return JSON.parse(text);
    } catch (err) {
      // File does not exist or format error, return default configuration
      console.warn('Failed to load config, using default values:', err.message);
      return { theme: 'dark', language: 'zh-CN' };
    }
  }

  async save(config) {
    try {
      const text = JSON.stringify(config, null, 2);
      await file.writeText({ uri: CONFIG_URI, text });
      console.log('Configuration saved');
    } catch (err) {
      console.error('Failed to save configuration:', err.message);
      throw err; // Re-throw to let the caller know saving failed
    }
  }

  async update(changes) {
    // Complete read -> modify -> save workflow
    const config = await this.load();
    Object.assign(config, changes);
    await this.save(config);
    return config;
  }
}

// Usage example
async function main() {
  const manager = new ConfigManager();
  // Load configuration
  const config = await manager.load();
  console.log('Current theme:', config.theme);
  // Update configuration
  await manager.update({ theme: 'light' });
  console.log('Theme updated');
}

// Note: main is also asynchronous and needs to be called correctly
main().catch(err => {
  console.error('Program execution error:', err);
});
```

#### Summary

- All `@system.file` APIs are asynchronous and must use `await` to wait for completion.
- Failing to use `await` leads to severe issues such as unprepared data, out-of-order operations, lost errors, and data corruption.
- Passing tests in the simulator does not mean the code is correct; I/O is slower on real devices, which will expose the problems.
- Using `async/await` + `try/catch` is the correct and most concise writing style.
- Never ignore the return value of a Promise.

### Callback Pitfalls

#### Callback Order Illusion and Race Condition Overwrites

This scenario involves a sequence of operations where a set of files is read, modified, and written. This is problematic code using callback parameters to trigger callback style:
```js
// Expected to increment a counter file by 1, but two concurrent calls might overwrite each other
function increment(uri, done) {
  file.readText({
    uri,
    success(text) {
      const n = Number(text || '0') + 1;
      console.log(`read ${text}, write ${n}`);
      // Nesting write file operation inside readText() success callback
      file.writeText({
        uri,
        text: String(n),
        success() { done && done(); },
        fail(msg, code) { done && done(new Error(`${msg}:${code}`)); }
      });
    },
    fail(msg, code) { done && done(new Error(`${msg}:${code}`)); }
  });
}

// Create counter file first, then trigger two increments concurrently
file.writeText({
  uri: 'internal://files/counter',
  text: '0',
  success() {
    // Trigger two increments concurrently without any synchronization
    increment('internal://files/counter');
    increment('internal://files/counter');
  }
})
```
After running this script, you may only see two `read 0, write 1` logs, and the final `counter` file content will be `1` instead of the expected `2`. The failure mechanism is: both reads fetch the same old value, and the later write overwrites the earlier one, resulting in the result only incrementing by 1.

::: note
The script above looks extremely complex and makes it hard to correctly pass the `done` callback function, which easily induces incorrect implementations. In fact, when rewritten using `async/await`, the code becomes very concise and easy to understand.
:::

A complex technique is to use mutual exclusion + serialization techniques, which can completely preserve the original concurrent `increment` semantics and ensure the atomicity of the entire read file + increment counter operation:
```js
// Key-based mutual exclusion execution using Promise chains
const lock = new Map();

/**
 * Serially executes asynchronous tasks for the same key. This is a utility function.
 * @param {string} key
 * @param {() => Promise<any>} fn
 * @returns {Promise<any>} Returns the result of fn
 */
function withLock(key, fn) {
  // Get the previous "tail" for this key (or an already resolved Promise if none)
  const prev = lock.get(key) || Promise.resolve();
  // Even if prev fails, we must continue the subsequent queue, so .catch(() => {}) first
  const p = prev.catch(() => {}).then(async () => {
    try {
      return await fn(); // The actual task only runs when it's its turn
    } finally {
      // If we are still the current tail, it means no new tasks have come in, so we can clean up
      if (lock.get(key) === p) lock.delete(key);
    }
  });
  lock.set(key, p); // Hang the new tail on
  return p;
}

// Now, the actual I/O inside increment is serialized by withLock:
async function increment(uri) {
  await withLock(uri, async () => {
    const n = Number(await file.readText({ uri })) || 0;
    console.log(`read ${n}, write ${n + 1}`);
    await file.writeText({ uri, text: `${n + 1}` });
  });
}

file.writeText({
  uri: 'internal://files/counter',
  text: '0'
}).then(() => {
  // Trigger two increments concurrently without any synchronization
  increment('internal://files/counter');
  increment('internal://files/counter');
});
```
After running this script, the `counter` file content will definitely be `2`, and the log sequence will definitely be `read 0, write 1` → `read 1, write 2`.

However, such code looks quite complex. The simplest approach is to call `await increment()` directly (manifesting as `await` propagation):
```js
async function increment(uri) {
  const n = Number(await file.readText({ uri })) || 0;
  console.log(`read ${n}, write ${n + 1}`);
  await file.writeText({ uri, text: `${n + 1}` });
}

file.writeText({
  uri: 'internal://files/counter',
  text: '0'
}).then(async () => {
  // Use await to wait for increment to ensure order
  await increment('internal://files/counter');
  await increment('internal://files/counter');
})
```

#### Callback Nesting Levels and Resource Leaks

The following example shows resource leaks and logic errors caused by multi-level nesting and too many branches in callback-style code:

```js
function exportReport(uri, cb) {
  startBusyIndicator();
  file.readText({
    uri,
    success(t) {
      transformCb(t, (err2, out) => {
        if (err2) {
          stopBusyIndicator();
          return cb && cb(err2);
        }
        file.writeText({
          uri: `${uri}.bak`,
          text: out,
          complete() {
            // Some branches forget stopBusyIndicator() or cb()
          }
        });
        // This is also wrong because writeText() is asynchronous and may not have completed yet
        stopBusyIndicator();
        cb && cb(null);
      });
    },
    fail(msg, code) {
      stopBusyIndicator();
      cb && cb(new Error(`${msg}:${code}`));
    }
  });
}
```

Due to overly deep callback nesting levels, `stopBusyIndicator()` and `cb()` are easily omitted or misused:
- Omitting cleanup logic, causing the "busy indicator" to never stop, or the caller to never receive a callback;
- Calling cleanup logic prematurely, causing the caller to mistakenly believe the write has completed.

Recommended writing style (structured cleanup):

```js
async function exportReport(uri) {
  startBusyIndicator();
  try {
    const t = await file.readText({ uri });
    const out = await transform(t);
    await file.writeText({ uri: `${uri}.bak`, text: out });
  } finally {
    stopBusyIndicator(); // Always called after file I/O completes (or throws an exception)
  }
}
```

#### Mixing `await` and Callbacks Causing Style Switching (`await` Invalidation)

No callback handler function returns a Promise object, rendering `await` invalid:

```js
// Because the complete callback is passed, this call enables callback style and does not return a Promise
await file.writeText({
  uri: 'internal://files/a.txt',
  text: 'x',
  complete() {}, // Do not pass success/fail/complete parameter fields
});
// The line above will not truly wait for the write to complete, and subsequent code may execute prematurely
```

Recommended writing style:

```js
// Do not pass success/fail/complete when using await
await file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
```

### Best Practices

#### Clear Ordering and Error Handling

```js
import file from '@system.file'

export async function updateConfig(uri, patch) {
  try {
    const text = await file.readText({ uri });
    const json = JSON.parse(text || '{}');
    Object.assign(json, patch);
    await file.writeText({ uri, text: JSON.stringify(json, null, 2) });
  } catch (err) {
    // Handle/log errors uniformly; do not swallow them
    console.error('updateConfig failed:', uri, err);
    throw err;
  }
}
```

The key points are making sequential timing explicit via `await`; using `try/catch` to ensure errors are perceived and re-thrown. If errors are completely ignored, the runtime will record exception logs and interrupt the entire call chain.

#### Avoiding TOCTTOU (Time-of-Check to Time-of-Use Race Conditions)

Do not call `access()` followed by `write*()` while relying on the state between them to remain unchanged. For example, code like this:

```js
file.access({
  uri: 'internal://files/a.txt',
  success(exists) {
    if (exists) {
      file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
    } else {
      // If the file does not exist, mkdir first then write file
      file.mkdir({
        uri: '/data',
        recursive: true,
        complete() {
          file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
        }
      });
    }
  }
});
```

The recommended approach is to attempt writing directly, and the runtime will automatically create the parent directories:
```js
async function safeWriteText(uri, text) {
  try {
    await file.writeText({ uri, text });
  } catch (e) {
    // Errors should be handled here, and there is no need for mkdir before writing files
  }
}
```

#### Half-Writes and Crash Interruptions

On MCU devices, system exceptions usually result in a direct reset, and the application does not continue executing in a "half-crashed" state. Even if the application is killed, file write operations that have already been submitted will not be interrupted (though they might not execute at all), so there is generally no need to worry about "half-written files":
```js
// Direct overwrite write; power interruption / system crash may leave a half-written file
file.writeText({ uri: '/data/config.json', text: bigJson });
```

For critical configuration file updates, you can use the "temporary file + same-directory rename" pattern to reinforce stability:
```js
async function atomicWriteText(uri, text) {
  const tmp = `${uri}.tmp`;
  await file.writeText({ uri: tmp, text });
  await file.rename({ oldUri: tmp, newUri: uri });
}
```

============================================================
FILE_PATH: src/transl/EN/api/system-network.md

# Network Status

## Import Module

```js
import network from '@system.network';
```

## Interface Definition

### `subscribe` <decl type="(callback: (status: NetworkState) => void): number" method/>

Listens for changes in network status. The `status` parameter of the `callback` is the new [Network State](#networkstate). The ID returned by this method can be used with the [`unsubscribe()`](#unsubscribe) method to stop listening.

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancels network status listening. `subscribeID` is the ID value returned by the [`subscribe()`](#subscribe) method.

### `getType` <decl type="(): Promise<NetworkState>" method/>

Gets the current network status and returns a [`NetworkState`](#networkstate) value.

## Type Definitions

### `NetworkState`

This object is used to represent the current network status, with the following type signature:

```ts
type NetworkState = {
  device: string; // The name of the network device
  type: string; // The type of the network device
  linkUp: boolean; // Whether the network device is turned on
  online: boolean; // Whether the device is online (whether the internet can be accessed)
};
```

Typically, the `online` property of `NetworkState` can be used to check whether the device has internet access.

============================================================
FILE_PATH: src/transl/EN/api/system-internal.md

# Internal Interfaces

The `system.internal` module provides internal interfaces for system use. This module can only be used in the launcher application.

## Import Module

``` js
import internal from '@system.internal'
```

## API

### `globalComponent` <decl type="(name: string, uri: string): void" method />

Registers a [global component](/framework/component/README.md#全局组件), which can be imported in all applications. The `name` parameter is the name of the global component, and the `uri` parameter is the relative path or URI of the global component UX file to the current source file. For example:
``` js
internal.globalComponent('TopBar', '/global/TopBar.ux')
```
Afterwards, the global component `TopBar` can be referenced in all applications using `<import name="TopBar" />`.

It is best to execute the `globalComponent()` method during the execution phase of the launcher application's `app.js`, so that global component information can be registered before any interface is loaded.

### `setDefaultKeyHandler` <decl type="(handler: (event: KeyEvent) => void): void" method />

Registers the system's default key handler. The `handler` parameter is a callback function. The prototype of the `KeyEvent` type is:
``` ts
interface KeyEvent  {
  type: 'keydown' | 'keyup', // Type of the key event
  key: string, // Name of the key
  timestamp: number, // Timestamp when the key event was reported, in milliseconds
}
```
The default key handler can only be registered once, as multiple registrations will overwrite previous operations.

============================================================
FILE_PATH: src/transl/EN/api/system-battery.md

# Battery Status

## Importing Modules

``` js
import battery from '@system.battery'
```

## API

### `getStatus` <decl type="(): Promise<{charge: ChargeState, level: number}>" method />

Gets the battery charging state `charge` (of type [`ChargeState`](#chargestate)) and the battery level `level`. The battery level is an integer between $[0, 100]$.

## Types

### `ChargeState`

`ChargeState` enumerates all battery charging states, defined as follows:
``` ts
type ChargeState = 'charging' | 'discharging' | 'not-charging' | 'full'
```
The meanings of each value are:
- `'charging'`: The battery is charging;
- `'discharging'`: The battery is discharging (disconnected from power);
- `'not-charging'`: The battery is not charging;
- `'full'`: The battery is fully charged.

============================================================
FILE_PATH: src/transl/EN/api/system-calendar.md

# Calendar

## Import Module

``` js
import calendar from '@system.calendar'
```

## Interface Definition

### `getLunar` <decl method type="(date: Date): LunarDate" />

Obtains the lunar date information for a given `Date` object, and returns a lunar date description of type [`LunarDate`](#lunardate).

### `getLunar` <decl method type="(year: number, month: number, day: number): LunarDate" />

Obtains the lunar information corresponding to the specified Gregorian year, month, and day, and returns a lunar date description of type [`LunarDate`](#lunardate). The parameters are defined as follows:
- `year`: Full year number, for example, `2024`;
- `month`: Month number, starting from `0`, where December is numbered $11$;
- `day`: Day number, starting from `1`.

## Type Definition

### `LunarDate`

``` ts
type LunarDate = {
  month: string,    // Lunar month name
  day: string,      // Lunar day name
  festival?: string // Festival name, may be undefined
}
```

- `month`: Name of the lunar month, for example, `'正月'`, `'二月'`.
- `day`: Name of the lunar day, for example, `'初一'`, `'十五'`.
- `festival`: Name of the festival. If there is no festival, this property is undefined.

============================================================
FILE_PATH: src/transl/EN/api/system-fetch.md

# Data Request fetch

## Import Module

``` js
import fetch from '@system.fetch'
```

## API

### `fetch`
<decl method><pre>
(options: {
  url: string,
  method?: 'GET' | 'POST' | 'PUT',
  header?: {[key: string]: string},
  params?: {[key: string]: string | number},
  data?: string | ArrayBuffer | {[key: string]: any},
  responseType?: 'text' | 'json' | 'arraybuffer',
  timeout?: number
}): Promise<{
  code: number,
  headers: {[key: string]: string},
  data: string | ArrayBuffer | any,
}>
</pre></decl>

Initiates an asynchronous network data request. The fields of the `options` parameter are described as follows:
- `url`: The URL of the website to access.
- `method`: Supports `'GET'`, `'POST'`, and `'PUT'`, with `'GET'` as the default.
- `header`: An object containing HTTP request header information, with keys and values as strings. Typical HTTP header fields can be `Authorization`, `Content-Type`, etc.
- `params`: Request parameters, all properties of which will be appended to the URL part of the request.
- `data`: The body content in an HTTP POST request.
- `responseType`: The response data type in the HTTP request, defaulting to `'text'`, with the following possible values:
  - `'text'`: The response returns text data, meaning the `data` property of the returned data is of type `string`.
  - `'json'`: The response returns JSON data, and the returned `data` property parses this JSON data into the corresponding JavaScript value.
  - `arraybuffer`: The response returns binary data, meaning the returned data is stored using an `ArrayBuffer` object.
- `timeout`: The timeout period for the request response in milliseconds, with a default value of $6000 \rm ms$.

#### `data` Parameter

`data` is the request body, used only in POST requests. It typically comes in three types: a string, an `ArrayBuffer` object, or a JSON object. When `data` is a string or an `ArrayBuffer` object, the request body will be text or binary data respectively. When the body is a JSON object, it will be serialized into text format. The serialization format is determined by the `Content-Type` field of the request method (`method` parameter):
- When `Content-Type` is `application/json`, the `data` parameter object is serialized into a JSON string and used as the request body;
- In other cases, the `data` parameter object is serialized into the `application/x-www-form-urlencoded` format.

::: warning
Many HTTP APIs use JSON format for POST request bodies. Please ensure that the request header's `Content-Type` is correctly set to `application/json`. For details, please refer to this [example](#post-request-json-body).
:::

#### Return Value

Returns a `Promise` object. After the request completes, the properties of the fulfilled value are as follows:
- [`code`](#code-response-code) is the server response code. A successful request typically has a response code of `200`.
- `header` is the server response header.
- `data` is the return value of the requested data, and its specific content is determined by the `options.responseType` parameter.

When the request fails, the returned `Promise` object is rejected.

## Instructions

### `code` Response Code

The meanings of the response codes returned by the server are:
- `200`: Indicates a successful request;
- `1002`: Parameter validation error;
- `1005`: Incomplete input parameters;
- `5000`: Request failed, response error;
- `5001`: Failed to read data buffer;
- `5002`: Request failed, response error;
- Others: Other HTTP/HTTPS response codes, such as `404`, etc.

When the response code returned by [`fetch`](#fetch) is `200`, it indicates that the network request was successful. Other values indicate that an error occurred during the request.

### Precautions

## Examples

### GET Request

This is a basic GET request example:

``` js
const res = await fetch.fetch({
  url: 'http://www.rt-thread.com/service/rt-thread.txt',
  method: 'GET', // Since GET is the default mode, method is optional here
  responseType: 'text'
})
console.log(`the status code of the response: ${res.code}`)
console.log(`the data of the response: ${res.data}`)
```

### POST Request

``` js
const res = await fetch.fetch({
  url: 'https://www.rt-thread.com/service/echo',
  method: 'POST',
  data: {
    key1: 'hello',
    key2: 'world'
  },
  responseType: 'text'
})
console.log(`the status code of the response: ${res.code}`)
console.log(`the data of the response: ${res.data}`)
```

### POST Request (JSON Body)

============================================================
FILE_PATH: src/transl/EN/api/system-request.md

# Upload and Download request

## Import Module

``` js
import request from '@system.request'
```

## API

### `download`
<decl method><pre>
(options: {
  url: string,
  header?: {[key: string]: string},
  filename?: string,
  callback: (progress: number) => void
}): DownloadTask
</pre></decl>

Downloads a file via the HTTP/HTTPS protocol. The fields of the `options` parameter are described as follows:
- `url`: The URL of the website to access;
- `header`: An object containing HTTP request header information, with keys and values as strings. Typical HTTP header fields can be `Authorization`, `Content-Type`, etc.;
- `filename`: The URI for storing the downloaded file, e.g., `internal://files/download.txt`;
- `callback`: The download progress callback function. This function will be called multiple times during the download, where `progress` is the download progress value ranging from $[0, 100]$.

The `download()` method returns a [`DownloadTask`](#downloadtask) object, which can be used to wait for the download to complete or to control the download task.

::: warning
Please do not use the download progress reaching $100\%$ in the `callback` function as the trigger condition for operations after the download is complete. For details, please refer to [Waiting for Download Completion](#waiting-for-download-completion).

The current implementation does not automatically resolve the `filename` parameter property based on the `url`, so please make sure to fill in `filename`.
:::

## Types

### `DownloadTask`

`DownloadTask` is the return type of the `download` method, and its signature is:

``` ts
interface DownloadTask {
  complete: Promise<void>,
  cancel(): void
}
```

The `complete` property is a `Promise` object that can be used to wait for the download to complete. The `cancel()` method is used to cancel an ongoing download task. If the download has already completed, the `cancel()` method has no effect.

#### Waiting for Download Completion

Use `DownloadTask.complete` to wait for the download to complete. When this `Promise` is fulfilled, it guarantees that the file has been completely written, making it safe to proceed to the next step. In contrast, the download progress reaching $100\%$ in `callback` does not mean the file writing is complete; it is only suitable for requirements such as UI progress display.

In practical use, considering that downloads may fail, it is recommended to use a `try...catch` statement to handle download errors. The example below demonstrates the usage.

## Examples

Here is a simple example of downloading a file from the network:

``` js
request.download({
  url: "http://www.rt-thread.com/service/rt-thread.txt",
  filename: "internal://tmp/rt-thread.txt",
})
```

You can use the `complete` property of the return value of `download()` to wait for the download to complete:
``` js
try {
  await request.download({
    url: "http://www.rt-thread.com/service/rt-thread.txt",
    filename: "internal://tmp/rt-thread.txt"
  }).complete // When complete is rejected, it indicates that the download failed
  console.log('download finished.')
} catch (e) {
  console.error('download failed:', e)
}
```

The `try...catch` block here is used to catch exceptions caused by download failures. This exception is actually the error thrown when `DownloadTask.complete` is rejected, so `await` must be used with the `complete` property, otherwise the exception cannot be caught.

============================================================
FILE_PATH: src/transl/EN/api/system-package.md

# Package Management

This module provides resource package installation and uninstallation functions.

## Importing the Module

``` js
import pkg from '@system.package'
```

Since `package` is a JavaScript keyword and cannot be used as a variable name, we can export the `"@system.package"` module to the `pkg` variable.

## Interface Definitions

### `install` <decl function type="(options: { src: string }): Promise<void>" />

Installs an application or watch face package from the file system. The `src` property of the `options` parameter is the URI of the resource package file to be installed.

If the resource package is an application resource package, it can be launched using [`launch()`](system-launch.md#launch-launch-app) after installation with `pkg.install({ src: 'package-uri' })`, and the contents within the package can be accessed using the [`app`](/framework/application/resource.md#app) URI protocol.

`src` is the URI of the resource package file to be installed. The installed package must be a valid application or watch face package, meaning it must have a [`manifest.json`](/framework/application/manifest.md) file. The package name after installation is determined by [`manifest.package`](/framework/application/manifest.md#package).

After installation, resources within the package can be accessed using the [`prc`](/framework/application/resource.md#prc) protocol, and application resource packages can also be accessed using the `app` protocol.

If the package to be installed already exists, an upgrade operation will be performed. If the application being upgraded is currently running, it will be exited first, and can be launched again later by calling [`launch()`](system-launch.md#launch-launch-app).

The installed package can be deleted using the [`remove()`](#remove) API.

### `remove`<decl type="(options: { package: string }): Promise<void>" function />

Deletes the resource package installed by [`install()`](#install). The `package` property of the `options` parameter is the name of the resource package to be deleted, which is the [`manifest.package`](/framework/application/manifest.md#package) field.

Related resources should be closed before deleting the resource package, such as destroying related components and closing related pages. The `remove()` function will automatically close the application corresponding to the resource package (if it is an application resource package).

::: warning
You must use `remove()` instead of directly using file system APIs to delete the resource package, because the latter will not clear the resource cache and cannot correctly delete the installation information.
:::

### `getInfo` <decl type="(query?: string | Query): Manifest | undefined" method/>

Gets the manifest information of an application package. The optional parameter `query` can be a package name string or a more complex `Query` object:
``` ts
type Query = {
  package: string,                 // Package name to query
  options?: ('dial' | 'widgets')[] // Optional query fields
}
```
If the package specified by the `package` field exists, `getInfo()` will return the `Manifest` information of the package, otherwise it returns `undefined`. When the `query` parameter is not specified, `getInfo()` will return the manifest information of the current application.

#### `Manifest` Object

The returned `Manifest` object is basically a subset of [`manifest.json`](/framework/application/manifest.md):
``` ts
type Query = {
  type: 'app' | 'dial', // Package type, can be an application or watch face package
  name: string,         // Package name
  versionName: string,  // Version name
  versionCode: number,  // Version code
  icon?: string,        // Application image path, this field only exists for application packages
  dial?: {              // Optional field: watch face information, only present in watch face packages
    component: string,  // Path to the watch face component
    preview: string     // Path to the watch face preview image
  },
  widgets?: {           // Optional field: widget and gadget information
    name: string,       // Widget/gadget name
    component: string,  // Widget/gadget path
    preview: string     // Widget/gadget preview image path
  }[]
}
```
The `dial` and `widgets` fields of the `Manifest` object are optional, and their presence is determined by the contents of `Query.options`. For example:
``` js
pkg.getInfo({
  package: 'com.example.app',
  options: ['dial', 'widgets']
})
```
will cause the resulting `Manifest` to include the `dial` and `widgets` fields (although application packages never include the `dial` field).

When the `query` parameter is a string, it is equivalent to an empty `options` option, meaning:
``` ts
pkg.getInfo('com.example.app')
pkg.getInfo({ package: 'com.example.app' })
```
yield the same results. In this case, the returned `Manifest` object does not contain optional fields.

When the `query` parameter is not specified, information about the current application can be returned via `getInfo()`:
``` js
let manifest = pkg.getInfo()
console.log(manifest)
```

### `list` <decl function type="(type?: 'app' | 'dial'): string[]" />

Gets a list of all installed application or watch face package names.

### `countOf` <decl function type="(type?: 'app' | 'dial'): string[]" />

Gets the number of installed applications or watch faces.

============================================================
FILE_PATH: src/transl/EN/api/system-vibrator.md

# Vibration

## Import Module

``` js
import vibrator from '@system.vibrator'
```

## API

### `vibrate`
<decl method><pre>
(options: {
  mode: string
}): bool
</pre></decl> 

Triggers vibration. The fields of the `options` parameter are described as follows:
- `mode`: Vibration mode. `long` indicates a long vibration, and `short` indicates a short vibration. The default value is `long`.

============================================================
FILE_PATH: src/transl/EN/api/system-notification.md

# Message Notification

## Import Module

``` js
import notification from '@system.notification'
```

Developers need to declare the application's access permission for `watch.permission.NOTIFICATION` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

## API

### `publish`
<decl method><pre>
(options: {
  icon: string,
  id?: number,
  contentType: number,
  content: object,
  deliveryTime: number,
  actionUri: string
}): void
</pre></decl>

Publishes a message notification. The fields in the `options` parameter are described as follows:
- `icon`: URI of the notification icon;
- `id`: Unique ID of the application notification;
- `contentType`: Content type. 1: Plain text notification type. 2: Image notification type; image notifications are not currently supported;
- `content`: Used in conjunction with `contentType` to represent the content of the notification;
  - When `contentType` is 1, it represents the content of a plain text notification; object type, containing the following fields:
    - `title`: Title of the plain text notification; string type;
    - `text`: Content of the plain text notification; string type;
- `deliveryTime`: Notification delivery time;
- `actionUri`: URI to navigate to when the notification is clicked.

### `remove` 
<decl method><pre>
(options: {
  query:{
    id?: number
  }
}): void
</pre></decl>

Clears message notifications. The `options` parameter contains the following fields:
- query: Query conditions for clearing,
  - id: Clears the message notification with the specified ID. If no ID is passed, all message notifications are cleared.

============================================================
FILE_PATH: src/transl/EN/api/system-audiokit.md

# Audio Player Manager

## Import Module

``` ts
import audiokit from '@system.audiokit'
```

## Interface Definitions

### `getPlayers` <decl type="(): AudioPlayer" method />

Queries the list of available audio player [`AudioPlayer`](#AudioPlayer) objects in the system.

### `getActivePlayer` <decl type="(): AudioPlayer" method />

Queries the active audio player [`AudioPlayer`](#AudioPlayer) object in the system.

### `subscribe` <decl type="(callback: (PlayerEvent) => void): number" method/>

Listens for changes to audio players in the system. The `PlayerEvent` parameter of `callback` is a [notification event](#PlayerEvent). The ID returned by this method can be used with the [`unsubscribe()`](#unsubscribe) method to stop listening.

Type signature of `PlayerEvent`:

```ts
type PlayerEvent = {
  notify: string; // Change event type
  player: string; // Name of the changed player
}
```

Change event types:

- `active`: The currently active player in the system has changed.  
- `append`: A player has been added to the system.
- `remove`: A player has been removed from the system.

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancels the player change listener. `subscribeID` is the ID value returned by the [`subscribe()`](#subscribe) method.

## `AudioPlayer` Object

::: details Type Signature
``` ts
interface AudioPlayer {
  src: string,
  name: string,
  icon: string,
  mode: string,
  status: string,
  duration: number,
  position: number,
  songAttribute: object,
  volume: number,
  nextAvailable: bool,
  prevAvailable: bool,

  play(): void,
  pause(): void,
  stop(): void,
  release(): void,
  next(): void,
  previous(): void,
  requestFocus({acquireType: string, volumeType: string}): void,
  releaseFocus(): void,

  onplay?: () => void,
  onpause?: () => void,
  onstop?: () => void,
  onended?: () => void,
  onerror?: (err: {msg: string})=> void,
  ontimeupdate?: () => void,
  oninterrupt?: (action: {interruptHint: number}) => void,
  onnext?: () => void,
  onprevious?: () => void,
  onrequestplay?: () => void,
  onrequestpause?: () => void,
  onrequeststop?: () => void,
  onsongattribute?: () => void,
  onposition?: () => void,
  onrequestfocus?: () => void,
  onreleasefocus?: () => void,
  onmodechanged?: () => void,
  onvolumechange?: () => void,
}
```
:::

- The `AudioPlayer` object (hereinafter referred to as `audiokit.Player`) and the `AudioPlayer` object created in the `system.media` module (hereinafter referred to as `media.Player`) are different JS objects, but they manage the same player. Additionally, the `audiokit.Player` object provides more features than the `media.Player` object, such as `next()`, `previous()`, etc. Operations like `play()` executed by the user through the `audiokit.Player` object will also trigger notifications to the listeners of the `media.Player` object.

### `src` <decl type="string" set get />

Sets or reads the URL of the audio to be played. Supports [local resource paths](/framework/application/resource.md#uri-和路径) and network resource paths using HTTP and HTTPS protocols (e.g., `https://www.rt-thread.com/service/test/001.mp3`). Below is a simple example of setting `src` and starting playback:

```ts
import audiokit from '@system.audiokit'
// Query the active audio player in the system
let player = audiokit.getActivePlayer()
if (player != null) {
  // First, stop the currently playing audio
  player.stop()
  // Set the audio URL to play
  player.src = 'https://www.rt-thread.com/service/test/001.mp3'
  // Start playing audio
  player.play()
}
```

### `name` <decl type="string" set get />

The name of the player object. If not set, defaults to the name of the application that created the player. Note that the player object's name is not guaranteed to be globally unique and cannot be used to uniquely identify a player object.

### `icon` <decl type="string" set get />

The icon URL of the player object. Supports [local resource paths](/framework/application/resource.md#uri-和路径).

### `mode` <decl type="string" set get />

Playback mode. The functionality corresponding to this property should be implemented by the player application; the player object does not process it by default and only provides the property.

- `sequential`: Sequential playback  
- `random`: Random playback  
- `singleloop`: Single-track loop  
- `listloop`: Playlist loop  

### `status` <decl type="string" get />

Reads the current playback status.

- `play`: Playing status  
- `pause`: Paused status  
- `stop`: Stopped status  
- `ended`: Playback ended status  
- `error`: Playback error status  

### `duration` <decl type="number" get />

Total duration of the audio, in seconds.

### `position` <decl type="number" set get />

Current playback time position of the audio, in seconds.

### `songAttribute` <decl type="songAttribute" set get />

Song attribute object.

::: details Type Signature
```ts
type songAttribute = {
  title: string; // Title of the song
  artist: string; // Name of the performer, can be an individual or a band
  album: string; // Name of the album the song belongs to
  year: string; // Release year of the song
  genre: string; // Genre of the song, such as pop, rock, classical, etc.
  track: string; // Track number in the album, e.g., "1/12" means track 1 of 12
  coverArt: string; // URL of the song cover image
  lyrics: string; // URL of the lyrics text
  comments: string; // Additional information, such as copyright notes
}
```
:::

Like the `AudioPlayer` object, the `songAttribute` object is a Proxy object, meaning it cannot be serialized/deserialized with JSON, nor can it be referenced in a reactive framework. Below is a simple usage example:

```ts
// Set the song title
this.player.songAttribute.title = "Unknown"
// Set the song artist
this.player.songAttribute.artist = "Unknown"
// View the song title
console.dir(this.player.songAttribute.title)
```

### `volume` <decl type="number" set get />

Current volume of the player, range: [0.0, 1.0].

### `nextAvailable` <decl type="bool" set get />

Sets or queries whether switching to the next track is available.

### `prevAvailable` <decl type="bool" set get />

Sets or queries whether switching to the previous track is available.

### `play` <decl type="(): void" method />

Starts playing the audio specified in the `src` property.

- If the `src` property is not set before calling this method, playback will fail and trigger the `onerror` event.
- This method is synchronous. After executing this interface, you need to wait for the `onplay` event or `onerror` event to determine whether playback succeeded or failed. Any other operations performed before the event is triggered will be ignored.  

Below is a simple example of calling the `play()` interface:

```ts
import audiokit from '@system.audiokit'
// Query the active audio player in the system
let player = audiokit.getActivePlayer()
if (player != null) {
  // First, stop the currently playing audio
  player.stop()
  // Set the audio URL to play
  player.src = 'https://www.rt-thread.com/service/test/001.mp3'
  // Set the onplay event
  player.onplay = () => { console.dir("Started playing") }
  // Set the onerror event
  player.onerror = () => { console.dir("Playback error") }
  // Start playing audio
  player.play()
}
```

### `pause` <decl type="(): void" method />

Pauses the playback of the current audio.  

- This method is synchronous. After executing this interface, you need to wait for the `onpause` event or `onerror` event to determine whether pausing succeeded or failed. Any other operations performed before the event is triggered will be ignored.  

### `stop` <decl type="(): void" method />

Stops audio playback. Playback can be resumed using `play`.  

- This method is synchronous. After executing this interface, you need to wait for the `onstop` event or `onerror` event to determine whether stopping succeeded or failed. Any other operations performed before the event is triggered will be ignored.  

### `release` <decl type="(): void" method />

Releases audio resources.  

- Executing this interface will stop the playback of the current audio. You need to wait for the `onstop` event or `onerror` event to determine whether stopping succeeded or failed. Any other operations performed before the event is triggered will be ignored.   

### `next` <decl type="(): void" method />

Notifies the player application to play the next track. Executing this interface will trigger the `onnext` event to notify the player application listening to this event, which then executes the song-switching logic.

### `previous` <decl type="(): void" method />

Notifies the player application to play the previous track. Executing this interface will trigger the `onprevious` event to notify the player application listening to this event, which then executes the song-switching logic.

### `requestFocus` <decl type="({acquireType: string, volumeType: string}): void" method />

Requests audio focus. Executing this interface will notify the underlying system to request or release audio focus, allowing the underlying system to control switching and interruption logic for different types of audio.

The `acquireType` parameter indicates the request type:
- `gain`: Request audio focus
- `loss`: Release audio focus

The `volumeType` parameter indicates the audio type:
- `system`: System prompts
- `media`: Media music
- `tts`: Voice broadcasts

The following example demonstrates how to use `requestFocus` to request audio focus:
``` ts
import audiokit from '@system.audiokit'
// Query the active audio player in the system
let player = audiokit.getActivePlayer()
if (player != null) {
  // Acquire audio focus for media music type
  player.requestFocus({ volumeType: 'media', acquireType: 'gain' });
}
```

### `releaseFocus` <decl type="(): void" method />

Releases audio focus. Executing this interface will notify the underlying system to release audio focus, allowing the underlying system to control switching and interruption logic for different types of audio.

### `onplay` <decl type="?: () => void" set />

Callback event triggered when audio `play` succeeds.

### `onpause` <decl type="?: () => void" set />

Callback event triggered when audio `pause` succeeds.

### `onstop` <decl type="?: () => void" set />

Callback event triggered when audio `stop` succeeds.

### `onended` <decl type="?: () => void" set />

Callback event triggered when audio playback ends.

### `onerror` <decl type="?: () => void" set />

Callback event triggered when errors occur during interfaces such as `play`, `pause`, `stop`, or `position`. When an error occurs, corresponding events like `onplay` will not be triggered.

### `ontimeupdate` <decl type="?: () => void" set />

Callback event triggered when the `position` property updates. This event is only triggered when the application is in the foreground and will stop dispatching when the application enters the background.

### `oninterrupt` <decl type="?: (action: {interruptHint: number}) => void" set />

Callback function when an audio interruption event occurs, notifying temporary or permanent interruption when the current audio is preempted by audio of the same or another type.

The `interruptHint` parameter of `action` indicates the type of interruption event:
- `1`: Transient interruption (can recover automatically, e.g., music being interrupted by a notification)
- `2`: Permanent interruption (cannot recover automatically, e.g., NetEase Cloud Music being interrupted by Ximalaya)

The following example demonstrates how to register the `oninterrupt` callback function, which will be called when the event occurs:
``` js
player.oninterrupt = (action) => {
  console.log(action.interruptHint)
}
```

### `onnext` <decl type="?: () => void" set />

Callback event when the next track needs to be played.

### `onprevious` <decl type="?: () => void" set />

Callback event when the previous track needs to be played.

### `onrequestplay` <decl type="?: () => void" set />

Callback event triggered when the underlying system needs to start playback, notifying the JS application to execute the start playback logic.

### `onrequestpause` <decl type="?: () => void" set />

Callback event triggered when the underlying system needs to pause playback, notifying the JS application to execute the pause playback logic.

### `onrequeststop` <decl type="?: () => void" set />

Callback event triggered when the underlying system needs to stop playback, notifying the JS application to execute the stop playback logic.

### `onsongattribute` <decl type="?: () => void" set />

Callback event when the song attribute object changes.

### `onposition` <decl type="?: () => void" set />

Callback event when setting the current audio playback time position via `position` succeeds.

### `onrequestfocus` <decl type="?: () => void" set />

Callback event when requesting audio focus succeeds.

### `onreleasefocus` <decl type="?: () => void" set />

Callback event when releasing audio focus succeeds.

### `onmodechanged` <decl type="?: () => void" set />

Callback event when the playback mode changes.

### `onvolumechange` <decl type="?: () => void" set />

Callback event when the player volume changes.

============================================================
FILE_PATH: src/transl/EN/api/system-media.md

# Multimedia

## Import Module

``` ts
import media from '@system.media'
```

## Interface Definitions

### `createAudioPlayer` <decl type="(): AudioPlayer" method />

Creates an [`AudioPlayer`](#audioplayer-object) object.

### `createAudioRecord` <decl type="(): AudioRecorder" method />

Creates an [`AudioRecorder`](#audiorecorder-object) object.

Developers need to declare the access permission for `watch.permission.RECORD` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

### `setVolume` <decl type="(volume: number): void" method />

Sets the system media volume. The `volume` parameter is a value between $[0.0, 1.0]$. This property is used to control the system media volume, and its specific functionality depends on the platform implementation. Adjusting the volume should preferably use the `volume` property of the `AudioPlayer` object.

### `getVolume` <decl type="(): number" method />

Gets the system media volume. The result is a value between $[0.0, 1.0]$. This property is used to get the system media volume, and its specific functionality depends on the platform implementation. Getting the volume should preferably use the `volume` property of the `AudioPlayer` object.

## `AudioPlayer` Object

::: details Type Signature
``` ts
interface AudioPlayer {
  src: string,
  name: string,
  icon: string,
  mode: string,
  status: string,
  duration: number,
  position: number,
  openSystemNotification: bool,
  songAttribute: object,
  volume: number,
  nextAvailable: bool,
  prevAvailable: bool,

  play(): void,
  pause(): void,
  stop(): void,
  release(): void,
  next(): void,
  previous(): void,
  requestFocus({acquireType: string, volumeType: string}): void,
  releaseFocus(): void,

  onplay?: () => void,
  onpause?: () => void,
  onstop?: () => void,
  onended?: () => void,
  onerror?: (err: {msg: string})=> void,
  ontimeupdate?: () => void,
  oninterrupt?: (action: {interruptHint: number}) => void,
  onnext?: () => void,
  onprevious?: () => void,
  onrequestplay?: () => void,
  onrequestpause?: () => void,
  onrequeststop?: () => void,
  onsongattribute?: () => void,
  onposition?: () => void,
  onrequestfocus?: () => void,
  onreleasefocus?: () => void,
  onmodechanged?: () => void,
  onvolumechange?: () => void,
}
```
:::

### `src` <decl type="string" set get />

Sets or reads the URL of the audio to be played. Supports [local resource paths](/framework/application/resource.md#uri-and-paths) and network resource paths using http and https protocols (e.g., `https://www.rt-thread.com/service/test/001.mp3`). Below is a simple example of setting the src and starting playback:

```ts
import media from '@system.media'
// Create an audio player
let player = media.createAudioPlayer()
// Set the audio URL to be played
player.src = 'https://www.rt-thread.com/service/test/001.mp3'
// Start playing audio
player.play()
```

### `name` <decl type="string" set get />

The name of the player object. If not set, it defaults to the name of the application that created the player. Note that the name of the player object is not globally unique, and you cannot use the name to identify a player object.

### `icon` <decl type="string" set get />

The icon URL of the player object. Supports [local resource paths](/framework/application/resource.md#uri-and-paths).

### `mode` <decl type="string" set get />

Playback mode. The functionality corresponding to this property should be implemented by the player application. The player object does not handle it by default and only provides this property.

- `sequential`: Sequential playback  
- `random`: Shuffle playback  
- `singleloop`: Single track loop  
- `listloop`: List loop  

### `status` <decl type="string" get />

Reads the current player status.

- `play`: Playing status  
- `pause`: Paused playback status  
- `stop`: Stopped playback status 
- `ended`: Playback ended status  
- `error`: Playback error status  

### `duration` <decl type="number" get />

Total duration of the audio, in seconds.

### `position` <decl type="number" set get />

Current audio playback time position, in seconds.

### `openSystemNotification` <decl type="bool" set get />

Whether to enable system notifications. Disabled by default. Once enabled, this player object can be queried by the [Audio Player Manager](/framework/application/system-audioPlayerManager.md#audio-player-manager).

### `songAttribute` <decl type="songAttribute" set get />

Song attribute object.

::: details Type Signature
```ts
type songAttribute = {
  title: string; // Name of the song
  artist: string; // Name of the performer, can be an individual or a band
  album: string; // Name of the album the song belongs to
  year: string; // Release year of the song
  genre: string; // Genre of the song, e.g., pop, rock, classical, etc.
  track: string; // Current song number in the album, e.g., "1/12" means track 1 of 12
  coverArt: string; // URL of the song cover image
  lyrics: string; // URL of the lyrics text
  comments: string; // Additional information, such as copyright notes
}
```
:::

Like the AudioPlayer object, the songAttribute object is a Proxy object, meaning it cannot be serialized or deserialized using JSON, nor can it be referenced within a reactive framework. Below is a simple usage example:

```ts
// Set the song title
this.player.songAttribute.title = "Unknown"
// Set the song artist
this.player.songAttribute.artist = "Unknown"
// View the song title
console.dir(this.player.songAttribute.title)
```

### `volume` <decl type="number" set get />

Current volume of the player, range: [0.0, 1.0].

### `nextAvailable` <decl type="bool" set get />

Sets or queries whether switching to the next track is available.

### `prevAvailable` <decl type="bool" set get />

Sets or queries whether switching to the previous track is available.

### `play` <decl type="(): void" method />

Starts playing the audio specified in the src property.

- If the src property is not set before calling this method, playback will fail and trigger the onerror event;
- This method is a synchronous interface. After executing this interface, you need to wait for the onplay event or onerror event to determine whether the playback succeeded or failed. Any other operations performed before the event is triggered will be ignored;  

Below is a simple example of calling the play() interface:

```ts
import media from '@system.media'
// Create an audio player
let player = media.createAudioPlayer()
// Set the audio URL to be played
player.src = 'https://www.rt-thread.com/service/test/001.mp3'
// Set the onplay event
player.onplay = () => { console.dir("Started playing") }
// Set the onerror event
player.onerror = () => { console.dir("Playback error") }
// Start playing audio
player.play()
```

### `pause` <decl type="(): void" method />

Pauses the playback of the current audio.  

- This method is a synchronous interface. After executing this interface, you need to wait for the onpause event or onerror event to determine whether the pause succeeded or failed. Any other operations performed before the event is triggered will be ignored;  

### `stop` <decl type="(): void" method />

Stops audio playback. You can resume playback using play.  

- This method is a synchronous interface. After executing this interface, you need to wait for the onstop event or onerror event to determine whether stopping succeeded or failed. Any other operations performed before the event is triggered will be ignored;  

### `release` <decl type="(): void" method />

Releases audio resources.  

- Executing this interface will stop the current audio playback. You need to wait for the onstop event or onerror event to determine whether stopping succeeded or failed. Any other operations performed before the event is triggered will be ignored;   

### `next` <decl type="(): void" method />

Notifies the player application to play the next track. Executing this interface triggers the onnext event to notify the player application listening to this event, and the player application executes the song switching logic.

### `previous` <decl type="(): void" method />

Notifies the player application to play the previous track. Executing this interface triggers the onprevious event to notify the player application listening to this event, and the player application executes the song switching logic.

### `requestFocus` <decl type="({acquireType: string, volumeType: string}): void" method />

Requests audio focus. Executing this interface notifies the underlying system to request or release audio focus, and the underlying system controls the switching and interruption logic for different types of audio.

The `acquireType` parameter indicates the request type:
- `gain`: Request audio focus
- `loss`: Release audio focus

The `volumeType` parameter indicates the audio type:
- `system`: System prompts
- `media`: Media music
- `tts`: Voice broadcast

The following example demonstrates how the `requestFocus` function requests audio focus:
``` ts
import media from '@system.media'
// Create an audio player
let player = media.createAudioPlayer()
// Acquire audio focus for media music type
player.requestFocus({ volumeType: 'media', acquireType: 'gain' });
```

### `releaseFocus` <decl type="(): void" method />

Releases audio focus. Executing this interface notifies the underlying system to release audio focus, and the underlying system controls the switching and interruption logic for different types of audio.

### `onplay` <decl type="?: () => void" set />

Callback event when audio play succeeds.

### `onpause` <decl type="?: () => void" set />

Callback event when audio pause succeeds.

### `onstop` <decl type="?: () => void" set />

Callback event when audio stop succeeds.

### `onended` <decl type="?: () => void" set />

Callback event when audio playback ends.

### `onerror` <decl type="?: () => void" set />

Callback event when errors occur during interfaces such as `play`, `pause`, `stop`, `position`. When an error occurs, corresponding events like onplay will not be triggered.

### `ontimeupdate` <decl type="?: () => void" set />

Callback event triggered when the position property is updated. This event is only triggered when the application is in the foreground and stops dispatching when the application is in the background.

### `oninterrupt` <decl type="?: (action: {interruptHint: number}) => void" set />

Callback function when an audio interruption event occurs, notifying temporary or permanent interruption when the current audio is preempted by audio of the same or another type.

The `interruptHint` in the `action` parameter indicates the type of interruption event:
- `1`: Brief interruption (can recover automatically, e.g., music being interrupted)
- `2`: Complete interruption (cannot recover automatically, e.g., NetEase Cloud Music interrupted by Ximalaya)

The following example demonstrates how to register the `oninterrupt` callback function, which is called when the event occurs:
``` js
player.oninterrupt = (action) => {
  console.log(action.interruptHint)
}
```

### `onnext` <decl type="?: () => void" set />

Callback event when the next track needs to be played.

### `onprevious` <decl type="?: () => void" set />

Callback event when the previous track needs to be played.

### `onrequestplay` <decl type="?: () => void" set />

Callback event triggered when the underlying system needs to start playback, notifying the JS application to execute the start playback logic.

### `onrequestpause` <decl type="?: () => void" set />

Callback event triggered when the underlying system needs to pause playback, notifying the JS application to execute the pause playback logic.

### `onrequeststop` <decl type="?: () => void" set />

Callback event triggered when the underlying system needs to stop playback, notifying the JS application to execute the stop playback logic.

### `onsongattribute` <decl type="?: () => void" set />

Callback event when the song attribute object changes.

### `onposition` <decl type="?: () => void" set />

Callback event when setting the current audio playback position via `position` succeeds.

### `onrequestfocus` <decl type="?: () => void" set />

Callback event when requesting audio focus succeeds.

### `onreleasefocus` <decl type="?: () => void" set />

Callback event when releasing audio focus succeeds.

### `onmodechanged` <decl type="?: () => void" set />

Callback event when the playback mode changes.

### `onvolumechange` <decl type="?: () => void" set />

Callback event when the player volume changes.


## `AudioRecorder` Object

::: details Type Signature
``` ts
interface AudioRecorder {
    start({
      uri: string, 
      sample?: 8000 | 16000 | 44100 | 48000,
      layout?: 8 | 16 | 32,
      channel?: 1 | 2,
      bitrate?: 16 | 32 | 64,
      codec?: "pcm" | "mp3" | "opus" | "silk",
      format?: "ogg",
    }): Promise<void>,
    read({callback: (ArrayBuffer) => void}): void,
    stop(): void,
    release(): void,
    onstart?: () => void,
    onstop?: () => void,
    onrelease?: () => void,
    onavailable?: (ArrayBuffer) => void,
    onerror?: ({error: string})=> void
}
```
:::

### `start`
<decl method><pre>
(options: {
  uri: string,
  sample?: 8000 | 16000 | 44100 | 48000,
  layout?: 8 | 16 | 32,
  channel?: 1 | 2,
  bitrate?: 16 | 32 | 64,
  codec?: "pcm" | "mp3" | "opus" | "silk",
  format?: "ogg",
}): Promise&lt;void>
</pre></decl>

Starts recording audio. The functions of the fields in the `options` parameter are:
- `uri`: The URI of the recording file to be stored. Only the `internal` protocol is supported, and directories will be created automatically;
- `sample`: Audio sampling rate in $\rm Hz$, defaults to $8000$;
- `layout`: Audio data bit depth, defaults to $16$;
- `channel`: Number of audio channels, defaults to $1$;
- `bitrate`: Audio bitrate in $\rm kbps$, defaults to $16$. Higher bitrates yield better sound quality but larger file sizes.
- `codec`: Audio encoding format as a string. If left blank, a suitable encoding is automatically matched based on the `format` parameter;
- `format`: Audio container/封装 format as a string. If left blank, a suitable container is automatically matched based on the suffix of the `uri` parameter;

  The support relationships for common recording formats, encoding formats, and container formats are as follows (an empty value in the table indicates that the corresponding parameter can be left blank):

  | Common Recording Formats | codec (Encoding Format) | format (Container Format) |
  | ------------------------ | ----------------------- | ------------------------- |
  | pcm                      | None                    | None                      |
  | mp3                      | mp3                     | None                      |
  | opus                     | opus                    | None                      |
  | opus-ogg                 | opus                    | ogg                       |
  | silk                     | silk                    | None                      |

Here is sample code to start recording:

``` js
let recorder = media.createAudioRecord()
recorder.start({
  uri: "internal://tmp/media_test.mp3",
  sample: 16000,
  layout: 16,
  channel: 1,
  bitrate: 16
})
```

::: info
For more descriptions regarding the `internal` URI protocol, please refer to the [Resource Access](/framework/application/resource.md) documentation.
:::

After recording is complete, please call the [stop()](#stop-1) method to end the recording.

### `read`
<decl method><pre>
(options: {
  callback: (buffer: ArrayBuffer) => void,
}): void
</pre></decl>

Reads the recorded audio data (each read retrieves all available data from the end of the previous read up to the current moment).

### `stop` <decl type="(): void" method />

Stops recording audio. After calling this interface, other modules can read the audio file recorded by the [`start()`](#start) method (specified by the `uri` parameter).

### `release` <decl type="(): void" method />

Releases audio recording resources.

### `onstart` <decl type="?: () => void" set />

Callback event after recording starts.

### `onstop` <decl type="?: () => void" set />

Callback event after recording stops.

### `onrelease` <decl type="?: () => void" set />

Callback event after recording is released.

### `onavailable` <decl type="(data: ArrayBuffer) => void" set />

Callback event when new data is generated after recording starts.

### `onerror` <decl type="?: () => void" set />

Callback event when errors occur during `start`, `stop`, or `release` events. When an error occurs, corresponding events like onstart will not be triggered.

## Examples

### Recording

The following code demonstrates a simple example of recording audio for 3 seconds:
``` js
import media from "@system.media"

async function record() {
  // Create a recording object
  let record = media.createAudioRecord()
  console.log('start record')
  // Only the uri parameter is provided; other parameters use default values
  await record.start({
    uri: 'internal://tmp/test.mp3'
  })
  setTimeout(() => {
    console.log('stop record')
    record.stop() // Stop recording after a 3-second delay
  }, 3000)
}

record()
```

When the `record()` function is called, it creates a recording object, starts recording, and stops recording after 3 seconds. The recording will be saved to the `internal://tmp/test.mp3` file and encoded in MP3 format.

This example only passes the `uri` parameter to the [`AudioPlayer.start()`](#start) method; `sample`, `layout`, `channel`, and `bitrate` all use their default configurations.

::: tip
When using the simulator, you can find and play the recording file in the application's data directory. The file path corresponding to `internal://tmp/test.mp3` is `.glyphix-work/image/{device}/data/temp/{app-id}/test.mp3`, where `{device}` and `{app-id}` are the device name and application name during simulation.
:::

============================================================
FILE_PATH: src/transl/EN/api/i18n.md

# Internationalization

This module provides in-app internationalization features.

## Import Module

``` js
import i18n from '@system.i18n'
```

## API

### `getLanguage` <decl type="(): string" method></decl>

Gets the current language setting of the application. The return value is a string representing the current language code, such as `'zh-CN'`, `'en-US'`, etc.

============================================================
FILE_PATH: src/transl/EN/api/system-cipher.md

# Cipher Algorithm

## Import Module

``` js
import cipher from '@system.cipher'
```

## API

### `aes`
<decl method><pre>
(options: {
  action: string,
  text: string,
  key: string,
  transformation?: string,
  iv?: string,
  ivOffset?: number,
  ivLen?: number
  }): Promise&lt;{ text: string }>
</pre></decl>

`aes` encryption and decryption. The functions of each field in the `options` parameter are as follows:
- `action`: The type of encryption or decryption, with two optional values: `'encrypt'` for encryption, and `'decrypt'` for decryption;
- `text`: The text content to be encrypted or decrypted. Text to be encrypted should be plain text, and text to be decrypted should be binary data encoded in `base64`;
- `key`: The key used for encryption or decryption, generated as a string after `base64` encoding. Before being decoded from `base64`, the key must be a multiple of $16$ bytes;
- `transformation`: The encryption mode (`'ECB'`, `'CBC'`, `'CFB'`, `'CTR'`, `'OFB'`) and padding scheme for the `AES` algorithm, defaulting to `'AES/CBC/PKCS5Padding'`. The available AES padding options are:
  - `'PKCS5Padding'`
  - `'PKCS7Padding'`
  - `'NoPadding'`
  - `'OneAndZerosPadding'`
  - `'ZerosAndLenPadding'`
  - `'ZerosPadding'` 
- `iv`: The initialization vector (IV) for AES encryption/decryption, as a Base64-encoded string, defaulting to the value of the `key` field;
- `ivOffset`: The initialization vector offset for AES encryption/decryption, defaulting to $0$;
- `ivLen`: The byte length of the initialization vector for AES encryption/decryption, defaulting to $16$;

::: details Sample Code

``` js
let signKey = "TkQRXv9xfAU65sxGmx4Xz2tQP7fwwdyxAGIZ9HMtc+c="

async function AesTest() {
  const encrypt = await cipher.aes({
    action: "encrypt",
    text: "this is a test project!",
    key: signKey,
    iv: "MTIzNDU2NzgxMjM0NTY3OA==",
    transformation:"AES/CBC/ZerosAndLenPadding",
    ivOffset: 0,
    ivLen: 16
  })
  console.log(`encrypt text: ${encrypt.text}`)

  const decrypt = await cipher.aes({
    action: "decrypt",
    text: encrypt.text,
    key: signKey,
    iv: "MTIzNDU2NzgxMjM0NTY3OA==",
    transformation:"AES/CBC/ZerosAndLenPadding",
    ivOffset: 0,
    ivLen: 16
  })
  console.log(`decrypto text: ${decrypt.text}`)
}

AesTest() // Print the encrypted and decrypted text, console output
// encrypt text: yI4dWJzQNCQfXq5P8du1dtYWZuBvbl9F9Vh15Fh9qjg=
// decrypto text: this is a test project!
```
:::

### `rsa`
<decl method><pre>
(options: {
  action: string,
  text: string,
  key: string,
  transformation?: string
}): Promise&lt;{ text: string }>
</pre></decl>

`rsa` encryption and decryption. The functions of the fields in the `options` parameter are as follows:
- `action`: The type of encryption or decryption, with two optional values: `'encrypt'` for encryption, and `'decrypt'` for decryption;
- `text`: The text content to be encrypted or decrypted. The text to be decrypted should be binary data encoded in Base64;
- `key`: The `RSA` key, which is a string generated after `base64` encoding. When encrypting, `key` is the public key; when decrypting, `key` is the private key;
- `transformation`: The padding scheme of the RSA algorithm, defaulting to `RSA/None/OAEPwithSHA-256andMGF1Padding`. The available RSA padding options are:
  - `'PKCS_v15andMGF1Padding'`
  - `'OAEPwithMD5andMGF1Padding'`
  - `'OAEPwithSHA-1andMGF1Padding'`
  - `'OAEPwithSHA-256andMGF1Padding'`

::: details Sample Code
``` js
let publicKey =
  'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCirfSt9f49F/BtPqextDlyoUEQ' +
  'qN+NUNxkYB5DY4FmJuI0gQSaK8hlGvnoA5T/seTGylHn95/PPTl5hW+riYtWaKfM' +
  'CXI2scstXA0S5vcYfc9917tRsrFzrDfJW+WD/HmmcvgI6rcbivokDikep3gVX0df' +
  'ktYtsAs158kMs4bBpwIDAQAB'

let privateKey = 
  'MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAKKt9K31/j0X8G0+' +
  'p7G0OXKhQRCo341Q3GRgHkNjgWYm4jSBBJoryGUa+egDlP+x5MbKUef3n889OXmF' +
  'b6uJi1Zop8wJcjaxyy1cDRLm9xh9z33Xu1GysXOsN8lb5YP8eaZy+AjqtxuK+iQO' +
  'KR6neBVfR1+S1i2wCzXnyQyzhsGnAgMBAAECgYAuH23w6H7FqYTkJFB9RKDJDEkb' +
  'RRXkxhlGaC4MYyjr4nhd9Hpuj51IdSaHjoRvHmvDpNcmEoH/ytcBykBH/T5As68M' +
  'L1OmzuJsD3BYMZpOOSFC9m7o6VMRf/T/ZTG6EDMtQekxlBV66QpiFmhQMjDs3jJY' +
  'TyR3OnZN9BWNBNotWQJBAOnLUpMT53HbFtw9vCRtVgAJ8JFjL4ZzYzrHj4mloKF3' +
  'P/r6faYUjgULoaHiD+BZB/Avru2h74Ghhr26CD3gMR0CQQCyIXzjSCrQiyCEdg1I' +
  '//IWLAALsfVITrlCN0rVeMkjTbc0KFEDUKG9y6MGAGX4AJNnos7y+zLpi6PcgwlU' +
  'zWaTAkBx5+fRVK88n5uhrkpODR8LYcxdaU+sV+eOqc/bJmD+ihUX+JbjJbyT5LjZ' +
  'IETP71CYywKVMIJ6S/JT2aFOVD5ZAkEAsfqFtu2fYbjw54iwY3TfpEmYThcj9Xg6' +
  '4C8wxTQm+/AlkaaKs144DNPPciqpt26T2WOxlNNqHjFYqvX+N832owJAaM5d4x2a' +
  'SDfC5GQFNfZ3WjATXkDE86q3m/88RBFFy8fWByyGiXtp4z5LCtMzI63X3ao0asVK' +
  'mjZxB+T+lMqa3w=='

async function rsaTest() {
  const res = await cipher.rsa({
    action: "encrypt",
    text: "this is a Rsa test.",
    key: publicKey,
    transformation: "RSA/None/OAEPwithSHA-256andMGF1Padding"
  })
  console.log(`encrypt text: ${res.text}`)

  const decrypt = await cipher.rsa({
    action: "decrypt",
    text: res.text,
    key: privateKey,
    transformation: "RSA/None/OAEPwithSHA-256andMGF1Padding"
  })
  console.log(`decrypt text: ${decrypt.text}`)
}

rsaTest() // Print the encrypted and decrypted text, console output sample
// encrypt text: FF+4R3iJ9pjeozZ6/Oulz9LUBH/uGQbIesJ7JbYRWvxGIHpJKNiEB+4MT/JcKs8ddN/ZQ4ts+YWMgUeglRBugRx+T4kqq0rKBdQrYdiMP58deCViSJjXJS+joPppwLDPL1Lg0VxpW89B+gA1jfC+9N8tvEHPhcX+nF8uAKRcW0M=
// decrypt text: this is a Rsa test.
```
:::

### `sign`
<decl method><pre>
(options: {
  text: string,
  key: string,
  algorithm?: string,
}): Promise&lt;{ sign: string }>
</pre></decl>

`sign` signature. The functions of each field in the `options` parameter are as follows:
- `text`: The content to be signed;
- `key`: The RSA private key;
- `algorithm`: The signature algorithm, defaulting to `'SHA256withRSA'`. The available signature algorithms are:
  - `'MD5withRSA'`
  - `'SHA1withRSA'`
  - `'SHA256withRSA'`
  - `'SHA512withRSA'`

::: details Sample Code

``` js
let signKey1 = "-----BEGIN RSA PRIVATE KEY-----\n" +
  "MIIEpAIBAAKCAQEA5hoGkpvqxJdssvqAYuvCWdTRrOdzZyx/ZyMev5Qyt2JKLy1C\n" +
  "7DuKrFGF5T5BDxN81o/OK+AQ6G1ASmwWfv5C1mk7sv6/glibPt9Gyr1OFMxviauy\n" +
  "ZMF8sgHVGkFyy1GsCsaM9anT1OEPoNeqrTHt+xB3Pq6FdH9RLMVbY0QNem5zv816\n" +
  "Hb6AJvMSnbGqMdd9fI1ARithrqnr9p+achP+Hc2Pj61PRviKJpFGLzBrU1BgBEbN\n" +
  "hscGRPebn4kTSy8flYau9lnDyLs5yyy0MHKBhot5Ja3tWTKhaqymFyJL2K6gE6Xn\n" +
  "bDAT6YFvo1TE9R7r9y+8prOR8oznJP19yxEWCQIDAQABAoIBAEbolkXvznUuxMyS\n" +
  "7aWOSaItN0A1Qxb0W36JEByxqr9ghsPrCsiJwL5BkSWH/byLoNjuD/btYch+gmVs\n" +
  "0bHo4Of6He+XGaUtcQn6/HHVzI4UQfsG8j6ica7ZabZhnOKTFJVtglriLulXQd2r\n" +
  "GGmvDUtlU5n5Zh70bSuC1hrNCepEMbJWqRZ4dvrdVqZ5RtARd3PYUAiPzwisQF9q\n" +
  "ZPAayyqmDUBReXS71RKRGn47RST+d50fZ3USP1jTAXMxf+X41ml3l7G1zd90IsWL\n" +
  "aIeHIaxi8BVkQogxqfZH8PAzmqtgLEWDfMgWU879qicBW4FB/PoBkP0P6Qlis/50\n" +
  "yY/80UECgYEA+zAkOshLUSJ4MDRMpkpf1WIZABH2lZhhIFw2A/VYnrmCJj3kxJYJ\n" +
  "ELNm82nFVIJGadSarOpownKUteHcJ7Zzv65WoEEZwZBO453I9tL6Fbh64hPp8VdB\n" +
  "4WMvK+0XqhzBL67ehghFNXc9ud4ZIQOXz6KUASxb+Iz0L02iqWIj+RUCgYEA6oJ5\n" +
  "Sh6Ez1lnWDKI5ZEQ1jn+kgcVHObV1o8sB5/5V0/Lihgma+Lpkei333sQsYImWQMD\n" +
  "8BT4JMCpPph5AwM0ZehUF7d2RCtQ+r0A/pUyiXjtMYHDrmAX94zDtf35QUJOL17z\n" +
  "don0weI/vZ71VYX3saa3EvVJLERwpSr0TswfPiUCgYEArLo8D5fwAsjbMPqlwqve\n" +
  "HpOocV3o3JG+KEyAcFRkLjGOh9GD4JLzhOJ45uVS5nv3A4tJGaLPivbTwAaiJ0TV\n" +
  "b3fo5aYemfYr6WV07hXCFvGWvqPG+UhxaxWTOHd/EGFZjvqG1lAVl2B5t7g8O3GH\n" +
  "ESbQ88WXMOFsgKK4OhXceskCgYEA0W/JJvruncg41bn8LRpLsSeGRaBxqKg33jFr\n" +
  "nzuuEd4/54r99WhoNVljrgFYvU+BNAnPYIE5xIkUHcVKffhEuaauQ6gjxWnyHpzh\n" +
  "4Hwa8E/Bdm9v9bH4dauPtl+mVjQDY6cnRHyczPNk/dKTRNgqiMxdwF60BQbym3Ar\n" +
  "VJxUYskCgYA6HWzf+9uHS98Hhr9zW0akjSZbcZclKR53wFMOjE1mFIxp/dC+d6mf\n" +
  "uVcUDTyo/LygzRBA5sd1euBhm5lXPyEHxIHZvwfBhIZWKlCZWlio1UvDbUp1f32u\n" +
  "JMT6q3KeJFJXp7nf5YmrPOKlh1Lm53hiXLSKF/q6Lcnn2lzRD2JDFw==\n" +
  "-----END RSA PRIVATE KEY-----"

async function signTest() {
  let res = await cipher.sign({
    text: "this is a sign test project.",
    key: signKey1
  })

  console.log(`sign text: ${res.sign}`)
}

signTest() 

```
:::

### `hash`
<decl method><pre>
(options: {
  data: string | ArrayBuffer,
  algorithm: string,
  encode?: string
}): Promise&lt;string | ArrayBuffer>
</pre></decl>

`hash` encryption. The functions of each field in the `options` parameter are as follows:
- `data`: The raw data used to generate the digest;
- `algorithm`: The digest algorithm, with optional values `'md5'`, `'sha1'`, `'sha224'`, `'sha256'`, `'sha384'`, `'sha512'`;
- `encode`: The encoding and type of the returned data, with optional values:
  - `'hex'`: Default value, returns a hex-encoded string;
  - `'base64'`: Returns a Base64-encoded string of the encryption result;
  - `'arraybuffer'`: Returns data of type ArrayBuffer;

::: details Sample Code

``` js
async function md5Test(){
  const res = await cipher.hash({
    algorithm: 'md5',
    data: 'hello'
  })
  console.log(res)
}
md5Test() // Print the generated digest, console output
// output：5d41402abc4b2a76b9719d911017c592
```
:::

### `hmac`
<decl method><pre>
(options: {
  data: string | ArrayBuffer,
  algorithm: string,
  key: string | ArrayBuffer,
  encode?: string
}): Promise&lt;string | ArrayBuffer>
</pre></decl>

Generates a keyed-hash message authentication code (HMAC) using the HMAC algorithm. The functions of each field in the `options` parameter are as follows:
- `data`: The raw data used to generate the digest;
- `algorithm`: The digest algorithm, with optional values `'md5'`, `'sha1'`, `'sha224'`, `'sha256'`, `'sha384'`, `'sha512'`;
- `key`: The key;
- `encode`: The encoding and type of the returned data, with optional values:
  - `'hex'`: Default value, returns a hex-encoded string;
  - `'base64'`: Returns a Base64-encoded string of the encryption result;
  - `'arraybuffer'`: Returns data of type `ArrayBuffer`;

::: details Sample Code

``` js
async function hmacTest() {
  let res = await cipher.hmac({
    data: 'hello',
    algorithm: 'sha1',
    key: '1234567890'
  })
  console.log(res)
}
hmacTest() // Print the generated digest, console output
// output：6fce0a55cf8bae80e2cf479b50035f773491c5ad
```
:::

### `base64Encode` <decl type="(data: string | ArrayBuffer): Promise&lt;string>" method />

Performs Base64 encoding on the input data.

### `base64Decode` <decl type="(data: string | ArrayBuffer): Promise&lt;ArrayBuffer>" method />

Performs Base64 decoding on the input data.

::: details Sample Code

``` js
async function base64Test() {
  const originalData = 'Hello, World!';
  const encodedData = await cipher.base64Encode(originalData); // Encode data

  console.log('Encoded Data:', encodedData);

  const decodedArrayBuffer = await cipher.base64Decode(encodedData); // Decode data

  const uint8Array = new Uint8Array(decodedArrayBuffer);
  let decodedData = '';

  for (let i = 0; i < uint8Array.length; i++) {
    decodedData += String.fromCharCode(uint8Array[i]);
  }

  console.log('Decoded Data:', decodedData);
}

base64Test()  // Print the results of encoding and decoding
// Encoded Data: SGVsbG8sIFdvcmxkIQ==
// Decoded Data: Hello, World!
```
:::

============================================================
FILE_PATH: src/transl/EN/api/system-brightness.md

# Brightness Management

## Import Module

``` js
import brightness from '@system.brightness'
```

## API

### `getValue` <decl type="(): number" method />

Gets the screen brightness value, ranging from $[0, 1]$.

### `setValue` <decl type="(value: number): void" method />

Sets the screen brightness value. The range of `value` is $[0, 1]$.

### `getMode` <decl type="(): string" method />

Gets the screen brightness mode.

### `setMode` <decl type="(mode: number): void" method />

Sets the screen brightness mode. When `number` is set to `0`, it is standard mode; when `number` is set to `1`, it is automatic mode.

### `setKeepScreenOn` <decl type="(mode: Boolean): void" method />

Sets whether to keep the screen on. When `mode` is set to `true`, the screen stays on; when `mode` is set to `false`, the screen is no longer kept on.

### `wakeScreenOn`
<decl method><pre>
(options: { 
  screenOn: boolean, 
  timeout?: number,
}): void
</pre></decl>

Turns the screen on or off. The fields of the `options` parameter are as follows:
- `screenOn`: Whether to turn on the screen
- `timeout`: Automatic screen-off time, leaving it blank means no time limit

============================================================
FILE_PATH: src/transl/EN/api/README.md

# API

Glyphix provides a full set of runtime JavaScript APIs, including browser-like APIs such as [`setInterval`](timer.md) and [`console`](console.md), as well as various system capability interfaces essential for building the entire application.

However, unlike the browser environment, Glyphix does not provide DOM interfaces. Therefore, it lacks objects like `window` and `document`, and cannot perform any DOM operations.

## QuickApp Asynchronous Interfaces

Glyphix supports the Watch QuickApp standard, but we primarily use Promise-style asynchronous interfaces rather than callback-style ones. For example, the callback pattern for the `file.readText()` interface in Watch QuickApp is used like this:
``` js
import file from '@system.file'

file.readText({
  uri: 'internal://files/test.txt',
  success(data) {
    console.log(data)
  },
  fail(data, code) {
    console.log(`read text failed: ${code}`)
  }
})
```
However, the Promise style is commonly used in Glyphix:
``` js
import file from '@system.file'

// Assuming inside an async function
try {
  const content = await file.readText({ uri: 'internal://files/test.txt' })
  console.log(content)
} catch (e) {
  console.error('read text failed:', e)
}
```
Since Promise-style APIs better align with modern usage habits established after the ES6 standard, this documentation only retains the type signatures for the Promise version.

### Promise vs. Callback Interfaces

Unless otherwise specified, all interfaces with a return type of `Promise<...>` support both callback functions (older QuickApp standards) and Promise asynchronous interface styles. Callback-style asynchronous interfaces typically have the following type:
``` ts
type CallbackAPI = (options: {
  success: (data: any) => void,
  fail: (data: any, code: number) => void,
  complete: () => void,
  // Other parameters...
}) => void
```
Whereas Promise-style asynchronous interfaces have the following type:
``` ts
type PromiseAPI = (options: any) => Promise<any>
```

When any `success`, `fail`, or `complete` property is present in the `options` parameter, the API will automatically use the callback function style (with no return value); otherwise, it will use the Promise return value style.

::: warning
When using the callback function style, asynchronous APIs do not return any value, so the `await` syntax cannot be used. Therefore, make sure not to pass any `success`, `fail`, or `complete` callback functions when using the Promise/`await` syntax.
:::

### API Examples

Taking the [`system.file`](system-file.md) module as an example, all of its functions support both Promise and callback styles of asynchronous invocation modes. The code snippet below provides a comparison of the two API usages.

::: code-tabs#js

@tab async/await

``` js
import file from '@system.file'

// async/await is actually syntactic sugar for Promises
async function readFile() {
  let text = await file.readText({ uri: '/app.js' })
  console.log(text)
}

readFile()
```

@tab Promise

``` js
import file from '@system.file'

file.readText({ uri: '/app.js' })
  .then(console.log) // Tip: The type of console.log() matches Promise.then(), so arrow functions are not required
  .fail((error) => console.log(`${error.message}: ${error.code}`))
```

@tab callback

``` js
import file from '@system.file'

file.readText({
  uri: '/app.js',
  success(data) {
    console.log(data)
  },
  fail(msg, code) {
    console.log(`${msg}: ${code}`)
  },
  complete() {
    console.log("complete")
  }
})
```

:::

This documentation will only provide Promise-style API types, and examples of asynchronous operations will exclusively use the await/async syntax.

::: tip
Developers are not recommended to additionally wrap Glyphix APIs, especially manually wrapping their callback-compatible styles into Promise modes. This practice requires writing extra code and will hurt performance.
:::

## Subscription Interfaces

Subscription-style APIs register a callback function with a module instead of returning a result directly. Unlike general asynchronous interfaces, the callback function of a subscription interface can be executed multiple times. All subscription interfaces support registering multiple subscription callback functions, return a subscription ID, and allow unsubscribing using the corresponding interface.

Glyphix currently does not support QuickApp-style subscription `fail` callback functions, but may throw exceptions directly when a subscription fails.

============================================================
FILE_PATH: src/transl/EN/api/system-storage.md

# Data Storage

The data storage module `system.storage` allows applications to store their own data, which is persistently saved in the application's storage object. Data stored in `system.storage` will be cleared when the application is uninstalled.

`system.storage` stores data in the form of key-value pairs, where the key must be a string, and the value is a JSON value (or a JavaScript value that can be serialized to JSON).

## Import Module

``` js
import storage from '@system.storage'
```

## API

### `get` <decl type="(key: string): any" method />

Gets the value corresponding to the key `key` in the storage. Returns `undefined` if the key-value pair does not exist.

### `set` <decl type="(key: string, value: any): void" method />

This method accepts a key `key` and a value `value` as parameters and adds this key-value pair to the storage. If the key already exists, its corresponding value is updated.

### `delete` <decl type="(key: string): boolean" method />

Deletes the key-value pair corresponding to the key `key` from the storage. Returns `true` if the key-value pair exists and is successfully deleted.

### `clear` <decl type="(): void" method />

Clears all stored data in the application.

============================================================
FILE_PATH: src/transl/EN/api/global.md

# Global Objects

## Global Functions

### `encodeURIComponent` <decl type="(str: string): string" function />

The `encodeURIComponent()` global function is used to encode a URI component `str`. It escapes certain special characters into their corresponding UTF-8 percentage (`%`) escape sequences, ensuring that the component can be correctly interpreted when used as part of a URL, particularly in query string parameters, paths, or fragments.

Letters, numbers, and `- _ . ! ~ * ' ( )` are not encoded. Other characters are encoded into percentage escape sequences (for example, a space is encoded as `%20`).

The behavior of `encodeURIComponent()` is consistent with the [function of the same name](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent) in the Web.

Example:
```js
console.log(encodeURIComponent("https://example.com/page?id=100"));
// output: https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100
```

### `decodeURIComponent` <decl type="(str: string): string" function />

The `decodeURIComponent()` global function is used to decode a URI component `str` encoded by `encodeURIComponent()`. It converts percentage (`%`)-encoded sequences back to their original character forms, thereby restoring the original URI component. For example, it converts `%20` back to a space.

The behavior of `decodeURIComponent()` is consistent with the [function of the same name](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/decodeURIComponent) in the Web.

Example:
```js
console.log(decodeURIComponent("https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100"));
// output: https://example.com/page?id=100
```

### `URI` <decl type="(uri: string | Uri): Uri" function />

This function takes a string and parses it into a `Uri` object for subsequent processing. The `uri` parameter is the URI string to be parsed.

The return value is an object containing the following fields:
- `scheme: string`: The scheme field parsed from the parameter;
- `authority: string`: The authority field parsed from the parameter;
- `path: string`: The path field parsed from the parameter;
- `query: string`: The query field parsed from the parameter;
- `origin: string`: The original URI string from the parameter;
- `toString: () => string`: This method can re-encode the object back into a URI string.

For example:
``` js
console.log(URI("https://app-name/icon.png"))
// {
//   scheme: 'https',
//   authority: 'app-name',
//   path: '/icon.png',
//   query: '',
//   origin: 'https://app-name/icon.png',
//   toString: <function>
// }
```

The `URI` function also accepts an object as a parameter. In this case, the `URI` function adds a `toString` method to the parameter object, which can be used to encode the URI object into a string:
``` js
let uri = {
  scheme: 'https',
  authority: 'app-name',
  path: '/icon.png',
  query: ''
}
console.log(URI(uri).toString()) // 'https://app-name/icon.png'
```

============================================================
FILE_PATH: src/transl/EN/api/console.md

# Console Module

The functionality of the `console` module is similar to the `console` feature in browsers and is used for logging. This module can be used directly without importing, and all properties are bound to the `console` global variable, for example:
``` js
console.log('Hello world!')
```


## Interface Definitions

### `backtrace` <decl type="boolean" />

When `backtrace` is set to `true`, all log outputs will include call stack information. The default value is `false`, in which case only `console.warn()` and higher-level APIs will output the call stack.

### `log` <decl type="(...data: any[]): void" method />

### `dir` <decl type="(...data: any[]): void" method />

### `debug` <decl type="(...data: any[]): void" method />

### `info` <decl type="(...data: any[]): void" method />

### `warn` <decl type="(...data: any[]): void" method />

### `error` <decl type="(...data: any[]): void" method />

## Log Filtering Level

The log filtering level of the `console` module is determined by the underlying system's log filtering mechanism and cannot be configured in JavaScript code.

============================================================
FILE_PATH: src/transl/EN/api/system-sensor.md

# Sensor

## Import Module

```js
import sensor from '@system.sensor';
```

Developers need to declare access to `watch.permission.ACCESS_SENSORS` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

## Interface Definitions

### `subscribeAccelerometer`
<decl method><pre>
(options: { 
  interval?: 'game' | 'ui' | 'normal', 
  callback: (data: AccelerometerValue) => void,
}): number
</pre></decl>

Listens for changes in accelerometer data. The functions of the fields in the `options` parameter are:
- `interval`: Listening frequency, defaults to `'normal'`. Available values are:
  - `'game'`: Game mode, frequency is 20ms/time;
  - `'ui'`: UI mode, frequency is 60ms/time;
  - `'normal'`: Normal mode, frequency is 200ms/time.
- `callback`: Accelerometer data update callback. The signature of the accelerometer data type `AccelerometerValue` is as follows:
  ``` ts
  type AccelerometerValue = {
    x: number   // Acceleration along the x-axis
    y: number   // Acceleration along the y-axis
    z: number   // Acceleration along the z-axis
  }
  ```

Example:
```js
const id = sensor.subscribeAccelerometer({
  interval: 'normal',
  callback(ret) {
    console.log(`gyroscope data, x = ${ret.x}, y = ${ret.y}, z = ${ret.z}`)
  }
})

// Cancel listening
sensor.unsubscribeAccelerometer(id)
```

### `unsubscribeAccelerometer` <decl type="(id: number): void" method/>

Cancels listening for accelerometer data. The `id` parameter is the listening ID returned by the [`subscribeAccelerometer`](#subscribeaccelerometer) method.

### `subscribeCompass`
<decl method><pre>
(options: { 
  callback: (data: CompassValue) => void,
}): number
</pre></decl>

Listens for changes in compass data. Returns the listening ID, which is used to cancel listening. The functions of the fields in the `options` parameter are:
- `callback`: Compass data change callback.

`CompassValue` signature:
``` ts
  type CompassValue = {
    direction: number   // Angle between the y-axis and the geomagnetic North Pole (in radians)
    accuracy: number    // Accuracy
  }
```
- `direction`: The angle in radians between the device's Y-axis and the Earth's magnetic North Pole, with a value range of $(-\pi,\pi]$, where:
  - `0`: True North
  - $\pi$` / 2` (approx. 1.57): True East
  - $\pi$ (approx. 3.14): True South
  - -$\pi$` / 2` (approx. -1.57): True West
- `accuracy`: Accuracy level of the compass data
  - `3`: High accuracy
  - `2`: Medium accuracy
  - `1`: Low accuracy
  - `0`: Unreliable (reason unknown)
  - `-1`: Unreliable (sensor disconnected)

Example:
```js
const id = sensor.subscribeCompass({
  callback(ret) {
    console.log(`direction=${ret.direction}, accuracy=${ret.accuracy}`)
  }
})

// Cancel listening
sensor.unsubscribeCompass(id)
```

### `unsubscribeCompass`<decl type="(id: number): void" method/>

Cancels listening for compass data. The `id` parameter is the listening ID returned by the [`subscribeCompass`](#subscribecompass) method.

### `calibrationCompass` <decl type="(): Promise<void>" method/>

Starts the compass calibration process. When the compass accuracy is low, guide the user to perform actions and call this method to calibrate the compass.

This function returns a Promise object with no result, which is resolved when the system completes the calibration.

### `getCompassValue` <decl type="(): Promise<CompassValue>" method/>

Gets the current compass data. Returns an asynchronous result containing a Promise object of type `CompassValue`, which includes compass direction and accuracy information.

### `subscribeStepCounter`
<decl method><pre>
(options: { 
  callback: (data: StepCounterValue) => void,
}): number
</pre></decl>

Listens for changes in step counter sensor data. The functions of the fields in the `options` parameter are:
- `callback`: Step counter data change callback. The signature of the step counter data type `StepCounterValue` is as follows:
  ``` ts
  type StepCounterValue = {
    steps: number     // Current accumulated steps (starts from 0 after reboot)
  }
  ```

Example:
```js
const id = sensor.subscribeStepCounter({
  callback(ret) {
    console.log(`steps=${ret.steps}`)
  }
})

// Cancel listening
sensor.unsubscribeStepCounter(id)
```

### `unsubscribeStepCounter` <decl type="(id: number): void" method/>

Cancels listening for step counter sensor data. The `id` parameter is the listening ID returned by the [`subscribeStepCounter`](#subscribestepcounter) method.

### `subscribeOnBodyState`
<decl method><pre>
(options: { 
  callback: (data: OnBodyStateValue) => void,
}): number
</pre></decl>

Listens for changes in the device on-body (wearing) state. The functions of the fields in the `options` parameter are:
- `callback`: Device on-body state change callback. The signature of the device on-body state data type `OnBodyStateValue` is as follows:
  ``` ts
  type OnBodyStateValue = {
    value: boolean  // Whether the device is worn
  }
  ```

Example:
```js
const id = sensor.subscribeOnBodyState({
  callback(ret) {
    console.log(`onBody=${ret.value}`)
  }
})

// Cancel listening
sensor.unsubscribeOnBodyState(id)
```

### `unsubscribeOnBodyState` <decl type="(): void" method/>

Cancels listening for the on-body state. The `id` parameter is the listening ID returned by the [`subscribeOnBodyState`](#subscribeonbodystate) method.

### `getOnBodyState` <decl type="(): Promise<OnBodyStateValue>" method/>

Gets the current device on-body state.

Example:
``` js
async function getOnBodyStat() {
  const data = await sensor.getOnBodyState()
  console.log(`onBody: ${data.value}`)
}
```

### `subscribeGyroscope`
<decl method><pre>
(options: { 
  callback: (data: GyroscopeValue) => void,
}): number
</pre></decl>

Listens for changes in gyroscope data. The functions of the fields in the `options` parameter are:
- `callback`: Gyroscope data change callback. The signature of the gyroscope data type `GyroscopeValue` is as follows:
  ``` ts
  type GyroscopeValue = {
    x: number   // Angular velocity around the x-axis
    y: number   // Angular velocity around the y-axis
    z: number   // Angular velocity around the z-axis
  }
  ```

Example:
```js
const id = sensor.subscribeGyroscope({
  callback(ret) {
    console.log(`gyroscope data, x = ${ret.x}, y = ${ret.y}, z = ${ret.z}`)
  }
})

// Cancel listening
sensor.unsubscribeGyroscope(id)
```

### `unsubscribeGyroscope` <decl type="(id: number): void" method/>

Cancels listening for gyroscope data. The `id` parameter is the listening ID returned by the [`subscribeGyroscope`](#subscribegyroscope) method.

### `subscribeBarometer`
<decl method><pre>
(options: { 
  callback: (data: BarometerValue) => void,
}): number
</pre></decl>

Listens for changes in barometer sensor data. The functions of the fields in the `options` parameter are:
- `callback`: Barometer data change callback. The signature of the barometer data type `BarometerValue` is as follows:
  ``` ts
  type BarometerValue = {
    pressure: number   // Air pressure value, unit: Pa
  }
  ```

Example:
```js
sensor.subscribeBarometer({
  callback(ret) {
    console.log("get barometer:", ret.pressure)
  }
})

// Cancel listening
sensor.unsubscribeBarometer(id)
```

### `unsubscribeBarometer` <decl type="(id: number): void" method/>

Cancels listening for the barometer sensor. The `id` parameter is the listening ID returned by the [`subscribeBarometer`](#subscribebarometer) method.

### `subscribeWristLift`
<decl method><pre>
(options: { 
  callback: () => void,
}): number
</pre></decl>

Listens for wrist lift events. The functions of the fields in the `options` parameter are:
- `callback`: Wrist lift event listener callback.

Example:
```js
const id = sensor.subscribeWristLift({
  callback: () => {
    console.log('wrist lift')
  }
});

// Cancel listening
sensor.unsubscribeWristLift(id)
```

### `unsubscribeWristLift` <decl type="(id: number): void" method/>

Cancels listening for wrist lifts. The `id` parameter is the listening ID returned by the [`subscribeWristLift()`](#subscribewristlift) method.

## Usage Limits

When the current device does not support the corresponding sensor capability, calling the interface will directly throw an exception, and the listener will not take effect.
Example of exception log: `the device does not support accelerometer sensor`

Example of catching exception information:

```js
try {
  const id = sensor.subscribeCompass({
    callback(ret) {
      console.log(`direction=${ret.direction}, accuracy=${ret.accuracy}`)
    }
  })
} catch (e) {
  console.error(e.message)
}
```

## Precautions

It is recommended to unsubscribe promptly when sensor data is no longer needed. Especially when the page is destroyed (in the `onDestroy` callback), unsubscribing helps avoid unnecessary performance degradation and power consumption.

============================================================
FILE_PATH: src/transl/EN/api/system-configuration.md

# App Configuration

## Import Module

```js
import configuration from '@system.configuration'
```

## Interface Definition

### `getLocale`
<decl method><pre>
(): {
  language: string,
  countryOrRegion: string,
}
</pre></decl>

Gets the current locale of the application. The system locale is used by default and may change due to settings or system locale changes.
 - `language` represents the current language, such as 'zh', 'en', etc.
 - `countryOrRegion` represents the current country or region, such as 'CN', 'US', etc.

============================================================
FILE_PATH: src/transl/EN/api/system-ble.md

# Low Energy Bluetooth Module

This module provides Bluetooth capabilities based on Bluetooth Low Energy (BLE) technology, supporting BLE scanning initiation as well as connections and data transmission based on the Generic Attribute Profile (GATT) (currently, only creating a `GattClient` is supported; creating a `GattServer` is not yet supported).

::: warning
Most APIs in `@system.bluetooth.ble` are [Promise asynchronous operations](#Promise异步操作), which are fundamentally different from synchronous IO access. Please make sure you understand the basic concepts of asynchronous programming and are familiar with the usage of Promises and `async/await`.
:::

## Importing the Module

``` js
import ble from '@system.bluetooth.ble'
```

## Permissions

::: tip
Applications using this module need to declare the permission: `watch.permission.BLUETOOTH`
:::

## ble Interface Definition

### `ResultCode`

Result enumeration returned in Promises

- `0`: Success;
- `1`: BLE is not enabled;
- `2`: Parameter error;
- `3`: Failed to enable BLE;
- `4`: No available Bluetooth adapter;
- `5`: Connection failed;
- `6`: Disconnection failed;
- `7`: Setting this property is not currently supported;
- `8`: Unknown error;

### `startBLEScan`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

Starts scanning, using a Promise asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

Here is an example of starting a scan:
```ts
import ble from '@system.bluetooth.ble'
export default {
    async scanStart() {
        // Start scanning
        await ble.startBLEScan().then(async (result) => {
            if (result == 0) {
                console.dir('startBLEScan success')
            } else {
                console.dir('startBLEScan failed' + result)
            }
        }).catch((error) => {
            console.dir('startBLEScan error:' + JSON.stringify(error))
        })
    },
}
```

### `stopBLEScan`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

Stops scanning, using a Promise asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

Here is an example of stopping a scan:
```ts
import ble from '@system.bluetooth.ble'
export default {
    async scanStop() {
        // Stop scanning
        await ble.stopBLEScan().then(async (result) => {
            if (result == 0) {
                console.dir('stopBLEScan success')
            } else {
                console.dir('stopBLEScan failed' + result)
            }
        }).catch((error) => {
            console.dir('stopBLEScan error:' + JSON.stringify(error))
        })
    },
}
```

### `ScanResult`

This object is used to represent the reported scan results. Its type signature is as follows:

```ts
/**
 * Scan result object definition
 */
type ScanResult = {
    deviceId: string; // Device ID (e.g., "AA:BB:CC:DD:EE:FF")
    rssi: number; // Signal strength in dBm
    data: ArrayBuffer; // Advertisement packet raw data
    deviceName: string; // Device name (if available)
    connectable: boolean; // Whether connectable, true means connectable
}
```

### `getBLEScanResults`
<decl method><pre>
(): Promise&lt;Array&lt;ScanResult&gt;&gt;
</pre></decl>

Queries scan results, using a Promise asynchronous callback. This interface asynchronously returns an array containing [`ScanResult`](#scanresult) objects (i.e., `Array<`[`ScanResult`](#scanresult)`>`).

::: warning
Since the underlying Bluetooth adapter is a singleton, multiple applications may operate Bluetooth devices simultaneously. This can lead to a situation where: App A starts scanning for a period of time, and then App B starts scanning again. In this case, the scan results listened to by App B will be incomplete. To handle this scenario, it is recommended that all applications query the current scan results immediately after starting a scan.
:::

Here is an example of querying scan results after starting a scan:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        scanList: [],
    },
    async scanStart() {
        // Start scanning
        await ble.startBLEScan().then(async (result) => {
            console.dir('startBLEScan success')
            // Query scan results
            await ble.getBLEScanResults().then((results) => {
                this.scanList = results
            });
        }).catch((error) => {
            console.dir('startBLEScan error:' + JSON.stringify(error))
        })
    },
}
```

### `subscribeScanStatus`
<decl type="(callback: Callback<{ scan: boolean }> => void): number" method/>

Subscribes to scan status changes, using a Callback asynchronous callback. When the scan status changes, the `callback` function is automatically invoked. This interface synchronously returns a subscription ID used for unsubscription.

Description of callback function parameter fields:
- `scan`: Current scan status. `true` indicates scanning is in progress, `false` indicates scanning has stopped.

Here is an example of subscribing to scan status changes:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        
    },
    scanListener: null,
    async onInit() {
        if (!this.scanListener) {
            this.scanListener = ble.subscribeScanStatus((result) => {
                console.dir('scan status:' + JSON.stringify(result))
            })
        }
    },
}
```

### `unsubscribeScanStatus` <decl type="(subscribeId: number): void" method/>

Unsubscribes from scan status changes. The `subscribeId` parameter is the subscription ID returned by the [`subscribeScanStatus`](#subscribescanstatus) method.

Here is an example of unsubscribing from scan status changes:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        
    },
    scanListener: null,
    async onInit() {
        if (!this.scanListener) {
            ble.unsubscribeScanStatus(this.scanListener)
            this.scanListener = null
        }
    },
}
```

### `subscribeBLEDeviceFind`
<decl type="(callback: Callback<ScanResult> => void): number" method/>

Subscribes to scan result reporting events, using a Callback asynchronous callback. Whenever a new device is scanned, the `callback` function is automatically invoked. This interface synchronously returns a subscription ID used for unsubscription.

::: tip
Scan results are reported in incremental mode, meaning one device is reported as soon as it is discovered. After listening to this event, users need to store the scan results themselves.
:::

Description of callback function parameter fields:
- [`ScanResult`](#scanresult): The newly discovered device object.

Here is an example of subscribing to scan result reporting events:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        scanList: [],
    },
    scanListener: null,
    async onInit() {
        this.scanList = []
        if (!this.scanListener) {
            this.scanListener = ble.subscribeBLEDeviceFind((result) => {
                console.dir('scan found:' + JSON.stringify(result))
                this.scanList.push(result)
            })
        }
    },
}
```

### `unsubscribeBLEDeviceFind` <decl type="(subscribeId: number): void" method/>

Unsubscribes from scan result reporting events. The `subscribeId` parameter is the subscription ID returned by the [`subscribeBLEDeviceFind`](#subscribebledevicefind) method.

Here is an example of unsubscribing from scan result reporting events:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    scanListener: null,
    onHide() {
        if (this.scanListener) {
            ble.unsubscribeBLEDeviceFind(this.scanListener)
            this.scanListener = null
        }
    },
}
```

### `GattClientDevice`

This object is used to represent the Client object in the GATT protocol. Its type signature is as follows:

```ts
/**
 * GattClientDevice object type definition
 */
type GattClientDevice = {
    connect(): Promise<number>,
    disconnect(): Promise<number>,
    close(): Promise<number>,
    getDeviceName(): Promise<string>,
    getServices(): Promise<Array<GattService>>,
    readCharacteristicValue(BLECharacteristic): Promise<BLECharacteristic>,
    writeCharacteristicValue(BLECharacteristic, GattWriteType): Promise<number>,
    readDescriptorValue(BLEDescriptor): Promise<BLEDescriptor>,
    writeDescriptorValue(BLEDescriptor): Promise<number>,
    getRssiValue(): Promise<number>,
    getBLEMtuSize(): Promise<number>,
    setBLEMtuSize(number): Promise<number>,
    setCharacteristicChangeNotification(BLECharacteristic): Promise<number>,
    setCharacteristicChangeIndication(BLECharacteristic): Promise<number>,
    subscribeBLECharacteristicChange(callback: (BLECharacteristic) => void): number,
    unsubscribeBLECharacteristicChange(number): void,
    subscribeBLEConnectionStateChange(callback: (BLEConnectionChangeState) => void): number,
    unsubscribeBLEConnectionStateChange(number): void,
    subscribeBLEMtuChange(callback: (number) => void): number,
    unsubscribeBLEMtuChange(number): void,
}
```

### `createGattClientDevice` <decl type="(deviceId: string): GattClientDevice" method />

Creates a [`GattClientDevice`](#gattclientdevice) instance representing the client side in a GATT connection. This interface synchronously returns a [`GattClientDevice`](#gattclientdevice) instance.

 - Through this instance, you can operate client-side behaviors, such as calling [`connect`](#connect) to initiate a connection to the peer device, and calling [`getServices`](#getservices) to retrieve all service capabilities supported by the peer device.
 - The `deviceId` (device address) required to create this instance represents the server-side device address. You can obtain the server-side device address via the [`startBLEScan`](#startblescan) interface, and you must ensure that the server-side device's BLE advertisement is connectable.

Here is an example of creating a [`GattClientDevice`](#gattclientdevice) instance:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    create() {
        // Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
    },
}
```

## GattClientDevice Interface Definition

### `connect`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

The client actively initiates a GATT protocol connection with the server Bluetooth device, using a Promise asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

 - Before using the methods of this class, you need to construct an instance of this class via the [`createGattClientDevice`](#creategattclientdevice) method.
 - By creating different instances of this class, you can manage multiple GATT connections.

Here is an example of initiating a GATT protocol connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async connect() {
        // Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
    },
}
```

### `disconnect`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

The client actively disconnects the GATT protocol connection with the server Bluetooth device, using a Promise asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

Here is an example of disconnecting a GATT protocol connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        address: null,
    },
    gattClient: null,
    async connect() {
        // Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.address = 'XX:XX:XX:XX:XX:XX'
        this.gattClient = ble.createGattClientDevice(this.address)
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
    },
    async disconnect() { 
        if (this.gattClient) {
            await this.gattClient.disconnect().then((result) => {
                if (result == 0) {
                    console.log('disconnect from' + this.address);
                } else {
                    console.dir('disconnect failed:' + JSON.stringify(result))
                }
            }).catch((error) => {
                console.log('disconnect error:' + JSON.stringify(error));
            });
        }
    },
}
```

### `close`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

Closes the client instance, using a Promise asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

### `getDeviceName`
<decl method><pre>
(): Promise&lt;string&gt;
</pre></decl>

The client retrieves the name of the remote BLE device, using a Promise asynchronous callback. This interface asynchronously returns a device name of type `<string>`.

Here is an example of retrieving the device name after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async name() {
        let clientName = 'N/A'
        // Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
        if (this.gattClient) {
            await this.gattClient.getDeviceName().then((name) => {
                clientName = name || 'N/A'
                console.dir('device name:' + name)
            })
        }
    },
}
```

### `GattService`

This object is used to represent the GATT service structure. Its type signature is as follows:

```ts
/**
 * GATT service structure definition, which can contain multiple BLECharacteristic values and other dependent services.
 */
type GattService = {
    serviceUuid: string; // Service UUID, identifying a GATT service. Example: 00001888-0000-1000-8000-00805f9b34fb.
    isPrimary: boolean; // Whether it is a primary service. true means primary service, false means secondary service.
    characteristics: Array<BLECharacteristic>; // List of characteristics contained in the current service.
    includeServices: Array<GattService>; // Other services depended upon by the current service.
}
```

### `getServices`
<decl method><pre>
(): Promise&lt;Array&lt;GattService&gt;&gt;
</pre></decl>

The client retrieves all services of the BLE device (service discovery), using a Promise asynchronous callback. This interface asynchronously returns an array of type `Array<`[`GattService`](#gattservice)`>` containing all services.

Here is an example of retrieving all services of the device after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    async onShow() {
        // Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
        if (this.gattClient) {
            await this.gattClient.getServices().then((result) => {
                this.services = result;
            }).catch((error) => {
                console.dir('gatt services error: ' + JSON.stringify(error))
            });
        }
    },
}
```

### `GattProperties`

This object is used to represent the properties supported by a GATT characteristic. Its type signature is as follows:

```ts
/**
 * Describes the properties supported by a GATT characteristic. Determines how the characteristic content and descriptors are used and accessed.
 */
type GattProperties = {
    write: boolean; // Whether the characteristic supports write operations. true means supported, and a response from the peer device is required when written; false means not supported.
    writeNoResponse: boolean; // Whether the characteristic supports write operations. true means supported, and no response from the peer device is required when written; false means not supported.
    read: boolean; // Whether the characteristic supports read operations. true means supported, false means not supported.
    notify: boolean; // Whether the characteristic supports actively notifying the peer device of its content. true means supported, and the peer device does not need to reply with a confirmation; false means not supported.
    indicate: boolean; // Whether the characteristic supports indicating its content to the peer device. true means supported, and the peer device needs to reply with a confirmation; false means not supported.
    broadcast: boolean; // Whether the characteristic supports being sent by the server as broadcast content. true means supported, and the server can carry the characteristic content in the advertisement packet as ServiceData; false means not supported.
    authenticatedSignedWrite: boolean; // Whether the characteristic supports authenticated signed write operations, replacing encryption with signature verification of the written content. true means supported, false means not supported.
    extendedProperties: boolean; // Whether the characteristic has extended properties. true means extended properties exist, false means they do not.
}
```

### `BLECharacteristic`

This object is used to represent a GATT characteristic. Its type signature is as follows:

```ts
/**
 * GATT characteristic type definition, the core data unit of the GattService
 */
type BLECharacteristic = {
    serviceUuid: string; // Service UUID to which the characteristic belongs, e.g., 00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // Characteristic UUID, e.g., 00002a11-0000-1000-8000-00805f9b34fb
    characteristicValue: ArrayBuffer; // Data content of the characteristic, used when reading/writing data
    descriptors: Array<BLEDescriptor>; // List of descriptors contained in the characteristic
    properties: GattProperties; // Properties supported by the characteristic
    characteristicValueHandle: number; // Unique identifier handle of the characteristic. When the server BLE device provides multiple characteristics with the same UUID, this handle can be used to distinguish between them
}
```

### `readCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic): Promise&lt;BLECharacteristic&gt;
</pre></decl>

The client reads data from a specified server characteristic, using a Promise asynchronous callback. This interface asynchronously returns an object of type [`BLECharacteristic`](#blecharacteristic).

 - This interface requires passing an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic needs to be read.

Here is an example of reading data from a specified characteristic after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async read() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, get the characteristic to read
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // Test tries to read only the first characteristic of the first service; modify as needed if reading other characteristics
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Read the specified characteristic
        if (this.gattClient && this.characteristic) {
            await this.gattClient.readCharacteristicValue(this.characteristic).then((result) => {
                console.log('characteristic read result:' + JSON.stringify(result))
            }).catch((error) => {
                console.dir('characteristic read error:' + JSON.stringify(error))
            })
        }
    },
}
```

### `GattWriteType`

Characteristic write type enumeration

- `1`: After writing to the characteristic, the peer Bluetooth device is required to reply with a confirmation.
- `2`: After writing to the characteristic, the peer Bluetooth device is not required to reply.

### `writeCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic, writeType: GattWriteType): Promise&lt;number&gt;
</pre></decl>

The client writes data to a specified server characteristic, using a Promise asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

 - This interface requires passing an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic needs to be written.
 - This interface requires passing a [`GattWriteType`](#gattwritetype) enumeration value to indicate the data write mode.

Here is an example of writing data to a specified characteristic after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    
    randomArrayBuffer(length) {
        const randomArray = new Array(length)
        for (let i = 0; i < length; i++) {
            randomArray[i] = Math.floor(Math.random() * 256);
        }
        return new Uint8Array(randomArray).buffer
    },

    async write() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, get the characteristic to operate on
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // Test tries to operate only on the first characteristic of the first service; modify as needed if operating on other characteristics
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Write to the specified characteristic
        if (this.gattClient && this.characteristic) {
            // Generate an ArrayBuffer of the specified length carrying random numbers
            let value = this.randomArrayBuffer(15)
            this.characteristic.characteristicValue = value
            await this.gattClient.writeCharacteristicValue(this.characteristic, 1).then((result) => {
                if (result === 0) {
                    console.log('characteristic write success')
                } else {
                    console.log('characteristic write failed:' + result)
                }
            }).catch((error) => {
                console.dir('characteristic write error:' + JSON.stringify(error))
            })
        }
    },
}
```

### `BLEDescriptor`

This object represents a GATT descriptor, and its type is defined as follows:

```ts
/**
 * GATT descriptor type definition, a data unit of the BLECharacteristic, used to describe additional information and properties of the characteristic
 */
type BLEDescriptor = {
    serviceUuid: string; // Service UUID to which the characteristic belongs, e.g., 00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // Characteristic UUID, e.g., 00002a11-0000-1000-8000-00805f9b34fb
    descriptorUuid: string; // Descriptor UUID, e.g., 00002902-0000-1000-8000-00805f9b34fb
    descriptorValue: ArrayBuffer; // Data content of the descriptor, used when reading/writing data
    descriptorHandle: number; // Unique identifier handle of the descriptor. When the server BLE device provides multiple descriptors with the same UUID, this handle can be used to distinguish between them.
}
```

### `readDescriptorValue`
<decl method><pre>
(descriptor: BLEDescriptor): Promise&lt;BLEDescriptor&gt;
</pre></decl>

The client reads data from a specified server descriptor, using a Promise asynchronous callback. This interface asynchronously returns an object of type [`BLEDescriptor`](#bledescriptor).

 - This interface requires passing an object of type [`BLEDescriptor`](#bledescriptor) to indicate which descriptor needs to be read.

Here is an example of reading data from a specified descriptor after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    descriptor: null,
    async read() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, get the characteristic to read
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        console.dir("gatt client found:" + JSON.stringify(this.services))
        if (this.services.length > 0) {
            // Test tries to read only the first descriptor of the first characteristic of the first service; modify as needed if reading other descriptors.
            // Note that not all characteristics have descriptors. You can adjust this yourself to select a service with descriptors and read/write permissions for testing.
            this.descriptor = this.services[0].characteristics[0].descriptors[0];
        }
        // 4. Read the specified descriptor
        if (this.gattClient && this.descriptor) {
            await this.gattClient.readDescriptorValue(this.descriptor).then((result) => {
                console.log('descriptor read result:' + JSON.stringify(result))
            }).catch((error) => {
                console.dir('descriptor read error:' + JSON.stringify(error))
            })
        }
    },
}
```

### `writeDescriptorValue`
<decl method><pre>
(descriptor: BLEDescriptor): Promise&lt;number&gt;
</pre></decl>

The client writes data to a specified server descriptor, using a Promise asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

 - This interface requires passing an object of type [`BLEDescriptor`](#bledescriptor) to indicate which descriptor needs to be written.

Here is an example of writing data to a specified descriptor after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    descriptor: null,
        
    randomArrayBuffer(length) {
        const randomArray = new Array(length)
        for (let i = 0; i < length; i++) {
            randomArray[i] = Math.floor(Math.random() * 256);
        }
        return new Uint8Array(randomArray).buffer
    },

    async write() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, get the characteristic to read
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        console.dir("gatt client found:" + JSON.stringify(this.services))
        if (this.services.length > 0) {
            // Test tries to operate only on the first descriptor of the first characteristic of the first service; modify as needed if operating on other descriptors.
            // Note that not all characteristics have descriptors. You can adjust this yourself to select a service with descriptors and read/write permissions for testing.
            this.descriptor = this.services[0].characteristics[0].descriptors[0];
        }
        // 4. Write to the specified descriptor
        if (this.gattClient && this.descriptor) {
            let value = randomArrayBuffer(15)
            this.descriptor.descriptorValue = value
            await this.gattClient.writeDescriptorValue(this.descriptor).then((result) => {
                if (result === 0) {
                    console.log('descriptor write success')
                } else {
                    console.log('descriptor write failed:' + result)
                }
            }).catch((error) => {
                console.dir('descriptor write error:' + JSON.stringify(error))
            })
        }
    },
}
```

### `getRssiValue`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

The client retrieves the Received Signal Strength Indication (RSSI) of the GATT connection link, using a Promise asynchronous callback. This interface asynchronously returns a signal strength of type `<string>` in units of dBm.

Here is an example of retrieving the device signal strength after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async rssi() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        if (this.gattClient) {
            await this.gattClient.getRssiValue().then((rssi) => {
                console.dir('device rssi:' + rssi)
            })
        }
    },
}
```

### `getBLEMtuSize`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

The client retrieves the MTU (Maximum Transmission Unit) size of the GATT connection link, using a Promise asynchronous callback. This interface asynchronously returns a length of type `<number>` in units of bytes.

Here is an example of retrieving the GATT connection link MTU (Maximum Transmission Unit) size after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async mtu() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        if (this.gattClient) {
            await this.gattClient.getBLEMtuSize().then((mtu) => {
                console.dir('device mtu:' + mtu)
            })
        }
    },
}
```

### `setBLEMtuSize`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

The client negotiates the MTU (Maximum Transmission Unit) size with the server, using a Promise asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

### `setCharacteristicChangeNotification`
<decl method><pre>
(characteristic: BLECharacteristic, enable: boolean): Promise&lt;number&gt;
</pre></decl>

The client enables or disables the capability to receive server characteristic value change notifications, using a Promise asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

 - This interface requires passing an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic needs to be operated on.
 - This interface requires passing a boolean value to indicate whether to enable or disable the content change notification capability (`true` to enable, `false` to disable).

Here is an example of enabling characteristic value change notifications after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async notify() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, get the characteristic to read
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // Test tries to operate only on the first characteristic of the first service; modify as needed if operating on other characteristics
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Operate on the specified characteristic
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeNotification(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Notification success')
                } else {
                    console.log('This characteristic does not allow enabling notifications, ResultCode:' + result);
                }
            }).catch((error) => {
                console.error('set characteristic Notification error: ' + JSON.stringify(error))
            })
        }
    },
}
```

### `setCharacteristicChangeIndication`
<decl method><pre>
(characteristic: BLECharacteristic, enable: boolean): Promise&lt;number&gt;
</pre></decl>

The client enables or disables the capability to receive server characteristic value change indications, using a Promise asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

 - This interface requires passing an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic needs to be operated on.
 - This interface requires passing a boolean value to indicate whether to enable or disable the content change indication capability (`true` to enable, `false` to disable).

Here is an example of enabling characteristic value change indications after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async indication() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, get the characteristic to read
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // Test tries to operate only on the first characteristic of the first service; modify as needed if operating on other characteristics
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Write to the specified characteristic
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeIndication(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Indication success')
                } else {
                    console.log('This characteristic does not allow enabling indications, ResultCode:' + result);
                }
            }).catch((error) => {
                console.error('set characteristic Indication error:' + JSON.stringify(error))
            })
        }
    },
}
```

### `subscribeBLECharacteristicChange`
<decl method><pre>
(callback: Callback(characteristic: BLECharacteristic) => void): number
</pre></decl>

The client subscribes to server characteristic change events. When a characteristic changes, the `callback` function is automatically invoked. This interface synchronously returns a subscription ID used for unsubscription.

Description of callback function parameter fields:
- [`BLECharacteristic`](#blecharacteristic): The characteristic object that changed.

Here is an example of subscribing to characteristic changes after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Subscribe to characteristic changes
        this.listener = this.gattClient.subscribeBLECharacteristicChange((result) => {
            let characteristicUuid = result.characteristicUuid
            let hexString = arrayBufferToHex(result.characteristicValue)
            console.log('characteristic changed uuid:' + characteristicUuid + ' value:' + hexString)
        })
    },
}
```

### `unsubscribeBLECharacteristicChange`
<decl method><pre>
(subscribeId: number): void
</pre></decl>

The client unsubscribes from server characteristic change events. The `subscribeId` parameter is the subscription ID returned by the [`subscribeBLECharacteristicChange`](#subscribeblecharacteristicchange) method.

Here is an example of unsubscribing from characteristic changes after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Unsubscribe from characteristic changes
        if (this.listener) {
            this.gattClient.unsubscribeBLECharacteristicChange(this.listener)
            this.listener = null
        }
    },
}
```

### `ConnectionState`

Bluetooth connection state enumeration

- `0`: Disconnected
- `1`: Connecting
- `2`: Connected
- `3`: Disconnecting

### `GattDisconnectReason`

GATT link disconnection reason enumeration

- `0`: Reason not available
- `1`: Connection timeout
- `2`: Peer device actively disconnected
- `3`: Local device actively disconnected
- `4`: Unknown disconnection reason

### `BLEConnectionChangeState`

This object is used to represent the Bluetooth connection state. Its type signature is as follows:

```ts
/**
 * Bluetooth connection state type definition
 */
type BLEConnectionChangeState = {
    deviceId: string; // Device ID (e.g., "AA:BB:CC:DD:EE:FF")
    state: ConnectionState; // Bluetooth connection state
    reason: GattDisconnectReason; // Reason for GATT link disconnection
}
```

### `subscribeBLEConnectionStateChange` 
<decl method><pre>
(callback: Callback(connectionChangeState: BLEConnectionChangeState) => void): number
</pre></decl>

The client subscribes to GATT protocol connection state change events. When the connection state changes, the `callback` function is automatically invoked. This interface synchronously returns a subscription ID used for unsubscription.

Description of callback function parameter fields:
- [`BLEConnectionChangeState`](#bleconnectionchangestate): Connection state.

Here is an example of subscribing to connection state changes after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Subscribe to connection state changes
        this.listener = this.gattClient.subscribeBLEConnectionStateChange((result) => {
            console.log('connect changed:' + JSON.stringify(result))
        })
    },
}
```

### `unsubscribeBLEConnectionStateChange`
<decl method><pre>
(subscribeId: number): void
</pre></decl>

The client unsubscribes from GATT protocol connection state change events. The `subscribeId` parameter is the subscription ID returned by the [`subscribeBLEConnectionStateChange`](#subscribebleconnectionstatechange) method.

Here is an example of unsubscribing from connection state changes:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Subscribe to connection state changes
        this.listener = this.gattClient.subscribeBLEConnectionStateChange((result) => {
            console.log('connect changed:' + JSON.stringify(result))
        })
        // 4. Unsubscribe from connection state changes
        if (this.gattClient && this.listener) {    
            this.gattClient.unsubscribeBLEConnectionStateChange(this.listener)
            this.listener = null
        }
    },
}
```

### `subscribeBLEMtuChange`
<decl method><pre>
(callback: Callback(mtu: number) => void): number
</pre></decl>

The client subscribes to MTU (Maximum Transmission Unit) size change events. When the MTU changes, the `callback` function is automatically invoked. This interface synchronously returns a subscription ID used for unsubscription.

Description of callback function parameter fields:
- `mtu`: MTU (Maximum Transmission Unit) size.

Here is an example of subscribing to MTU changes after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Subscribe to MTU changes
        this.listener = this.gattClient.subscribeBLEMtuChange((mtu) => {
            console.log('mtu changed:' + mtu)
        })
    },
}
```

### `unsubscribeBLEMtuChange`
<decl method><pre>
(subscribeId: number): void
</pre></decl>

The client unsubscribes from MTU (Maximum Transmission Unit) size change events. The `subscribeId` parameter is the subscription ID returned by the [`subscribeBLEMtuChange`](#subscribeblemtuchange) method.

Here is an example of unsubscribing from MTU changes:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Construct the gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Subscribe to MTU changes
        this.listener = this.gattClient.subscribeBLEMtuChange((mtu) => {
            console.log('mtu changed:' + mtu)
        })
        // 3. Unsubscribe from MTU changes
        if (this.gattClient && this.listener) {    
            this.gattClient.unsubscribeBLEMtuChange(this.listener)
            this.listener = null
        }
    },
}
```

============================================================
FILE_PATH: src/transl/EN/api/timer.md

# Timers

This module provides timer functionality for delayed or periodic code execution. The timer API can be used directly without importing.

## Interface Definitions

### `setTimeout` <decl type="(callback: () => void, duration: number): number" />

Sets a timer that executes a callback function after a specified delay. Parameter descriptions:
- `callback`: The callback function to execute when the delay time is reached;
- `duration`: The delay time in milliseconds.

Returns a timer ID, which can be used to cancel the timer via the [`clearTimeout()`](#cleartimeout) method.

Example:
``` js
// Execute the callback function after 1 second
const timerId = setTimeout(() => {
  console.log('1 second has passed')
}, 1000)
```

### `setInterval` <decl type="(callback: () => void, duration: number): number" />

Sets a timer that repeatedly executes a callback function at specified intervals. Parameter descriptions:
- `callback`: The callback function to execute every time the timer triggers;
- `duration`: The execution interval in milliseconds.

Returns a timer ID, which can be used to cancel the timer via the [`clearInterval()`](#clearinterval) method.

Example:
``` js
// Execute the callback function every 500 milliseconds
const timerId = setInterval(() => {
  console.log('Another 500 milliseconds have passed')
}, 500)
```

### `clearTimeout` <decl type="(timerId: number): void" />

Cancels a timer set by the [`setTimeout()`](#settimeout) method. The `timerId` parameter is the ID of the timer to cancel.

::: warning
Unlike web environments, the timer ID pool in this implementation **may be reused**. Therefore, **do not** call `clearTimeout()` repeatedly on the same valid timer ID, as this may accidentally stop other running timers.

It is recommended to set the timer ID to `null` after clearing it to avoid repeated clearing. `clearTimeout()` can safely accept invalid IDs such as `null` or `0`, and these calls will not produce side effects.
:::

Example:
``` js
const timerId = setTimeout(() => {
  console.log('This message will not be printed')
}, 1000)

// Cancel the timer before it triggers
clearTimeout(timerId)
```

The recommended practice is to set the timer ID to null after clearing it to avoid repeatedly clearing a valid ID:
``` js
export default {
  onInit() {
    this.timerId = setTimeout(() => {
      console.log('Timer triggered')
      this.timerId = null // Clear the ID after execution
    }, 1000)
  },
  onDestroy() {
    // Safe to clear even if timerId is null
    clearTimeout(this.timerId)
  },
  someMethod() {
    // Clear the timer and set to null
    clearTimeout(this.timerId)
    this.timerId = null
  },
}
```

### `clearInterval` <decl type="(timerId: number): void" />

Cancels a timer set by the [`setInterval()`](#setinterval) method. The `timerId` parameter is the ID of the timer to cancel.

::: warning
Unlike web environments, the timer ID pool in this implementation **may be reused**. Therefore, **do not** call `clearInterval()` repeatedly on the same valid timer ID, as this may accidentally stop other running timers.

It is recommended to set the timer ID to `null` after clearing it to avoid repeated clearing. `clearInterval()` can safely accept invalid IDs such as `null` or `0`, and these calls will not produce side effects.
:::

Example:
``` js
let count = 0
const timerId = setInterval(() => {
  count++
  console.log(`Execution count: ${count}`)
  if (count >= 5)
    clearInterval(timerId) // Stop after 5 executions
}, 500)
```

::: tip
`clearInterval` and `clearTimeout` are actually two aliases for the same function, but it is recommended to use the corresponding method to keep the code clear.
:::

## Development Notes

### Timer ID Reuse

There is an important difference between this implementation and standard web environments: **Timer IDs may be reused**.

In web browsers and Node.js, every call to `setTimeout()` or `setInterval()` returns a unique, monotonically increasing ID that is never reused. Therefore, in a web environment, calling `clearTimeout()` or `clearInterval()` on an already cleared or invalid timer ID is safe and has no side effects.

However, in this implementation, timer IDs come from a limited pool. When a timer is cleared or finishes execution, its ID may be reused by a newly created timer. This means that if you repeatedly clear the same ID (i.e., the number returned by `setTimeout()` or `setInterval()`), you might accidentally stop another running timer.

`clearTimeout()` and `clearInterval()` can safely accept non-timer ID values such as `null`, `0`, and `undefined`, and these calls will not produce side effects.

Therefore, **be sure to follow these best practices**:
1. Clear each timer ID only once;
2. Set the timer ID to `null`, `0`, or `undefined` after clearing to prevent accidental repeated clearing.

`clearTimeout()` and `clearInterval()` can safely accept non-timer ID values such as `null` and `0`, so there is no need to check for validity before calling them.

The examples in the API documentation above demonstrate the recommended practices.

An exception is that you can clear a timer ID within its own `setTimeout` callback:
``` js
let timer = setTimeout(() => {
  clearTimeout(timer) // This will not affect other timers, nor will it trigger warning logs
}, 1000)
```

### Timer Precision Issues

Timer APIs **do not guarantee precise time intervals**, and actual execution times may vary. This is because:
- System scheduling and performance constraints may cause timer trigger times to be inaccurate;
- The minimum timer interval is subject to system limitations and is constantly affected by low-power policies.

Therefore, **do not** use timer APIs for precise timing. If you need to measure time intervals or implement timer functionality, you should use the `Date` object to obtain actual timestamps.

#### Incorrect Example: Using Timer Counts for Timing

The code below attempts to calculate elapsed time by accumulating timer trigger counts, which is incorrect:
``` js
export default {
  data: {
    elapsedTime: 0, // Calculate elapsed time by accumulation
  },
  onInit() {
    // Incorrect: Assumes the timer triggers precisely once per second
    this.timerId = setInterval(() => {
      this.elapsedTime += 1000
    }, 1000)
  },
  onDestroy() {
    clearInterval(this.timerId)
  },
}
```

The problem with this approach is that even if the set interval is $1000\rm ms$, the actual trigger interval might be $1010\rm ms$ or even longer. Cumulative errors will make the timing increasingly inaccurate. After the device enters low-power mode, timers may run with second-level precision or be suspended directly.

#### Correct Example: Timing Using the `Date` Object

The correct approach is to record the start timestamp and calculate the difference from the current time on each update:
``` js
export default {
  data: {
    elapsedTime: 0, // Elapsed time in milliseconds
  },
  onInit() {
    // Record the start timestamp
    this.startTime = Date.now()
    // Use a timer to periodically update the display
    this.timerId = setInterval(() => {
      // Get the actual elapsed time by calculating the timestamp difference
      this.elapsedTime = Date.now() - this.startTime
    }, 100) // A shorter update interval can be set to improve display smoothness
  },
  onDestroy() {
    clearInterval(this.timerId)
  },
}
```

### Complete Stopwatch Example

Below is a complete stopwatch component example demonstrating how to correctly implement start, pause, and reset functions:

<glyphix id="api-timer-stopwatch" height="200" width="410">

``` html
<div class="container">
  <text class="timer">{{ formatTime(elapsedTime) }}</text>
  <div class="buttons">
    <text class="button" on:click="start">Start</text>
    <text class="button" on:click="pause">Pause</text>
    <text class="button" on:click="reset">Reset</text>
  </div>
</div>
```

``` js
export default {
  data: {
    elapsedTime: 0,     // Elapsed time (milliseconds)
    isRunning: false,   // Whether the stopwatch is running
  },
  onInit() {
    this.startTime = 0       // Timestamp of the current start
    this.accumulatedTime = 0 // Accumulated time (used to resume after pausing)
    this.timerId = null
  },
  onDestroy() {
    // Clear the timer
    clearInterval(this.timerId)
  },
  start() {
    if (this.isRunning)
      return // Already running, avoid restarting

    this.isRunning = true
    // Record the timestamp of the current start
    this.startTime = Date.now()

    // Periodically update the display
    this.timerId = setInterval(() => {
      // Accumulated time + (Current time - Start time)
      this.elapsedTime = this.accumulatedTime + (Date.now() - this.startTime)
    }, 20)
  },
  pause() {
    if (!this.isRunning)
      return // Already paused, no action needed

    this.isRunning = false
    // Stop the timer
    clearInterval(this.timerId)
    this.timerId = null // Set to null after clearing

    // Save accumulated time for resumption later
    this.accumulatedTime = this.elapsedTime
  },
  reset() {
    // Stop the timer
    this.isRunning = false
    clearInterval(this.timerId)
    this.timerId = null // Set to null after clearing

    // Reset all states
    this.elapsedTime = 0
    this.accumulatedTime = 0
    this.startTime = 0
  },
  formatTime(ms) {
    // Convert milliseconds to "Minutes:Seconds.Milliseconds" format
    const totalSeconds = Math.floor(ms / 1000)
    const minutes = Math.floor(totalSeconds / 60)
    const seconds = totalSeconds % 60
    const milliseconds = Math.floor((ms % 1000) / 10)

    return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(milliseconds).padStart(2, '0')}`
  },
}
```

``` css
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.timer {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 30px;
}

.buttons {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.button {
  padding: 10px 20px;
  margin: 0 10px;
  background-color: #007AFF;
  color: #FFFFFF;
  border-radius: 8px;
  font-size: 0.8rem;
}
```


</glyphix>

This example demonstrates:
- Using `Date.now()` to get accurate timestamps and calculating the actual elapsed time via timestamp differences;
- Using `setInterval()` solely for periodically updating the UI display;
- Correctly handling state transitions for start, pause, and reset;
- Cleaning up timer resources when the component is destroyed.

### Preventing Memory Leaks

Be sure to clear timers promptly when using them; otherwise, it may lead to memory leaks or access to already destroyed components. Clear all timers in the component's [`onDestroy()`](/framework/component/life-cycle.md) lifecycle function:
``` js
export default {
  onInit() {
    this.timerId = setTimeout(() => {
      // Perform some operations
      this.timerId = null // Set to null after execution
    }, 5000)
  },
  onDestroy() {
    // Clear the timer to prevent memory leaks
    clearTimeout(this.timerId)
  },
}
```

This is especially important for periodic timers created with `setInterval()`, as they will continue to run until explicitly cancelled.

