# Context File: 03_glyphix_system_api_EN.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/transl/EN/api/console.md

# Console module

The function of the `console` module is similar to the `console` function in the browser and is used to implement logging. This module can be used directly without importing. All properties are bound to the `console` global variable, for example:
``` js
console.log('Hello world!')
```


## Interface definition

### `backtrace` <decl type="boolean" />

After setting `backtrace` to `true`, all log printouts will carry call stack information. The default value is `false`, at which time only `console.warn()` and higher-level APIs will output the call stack.

### `log` <decl type="(...data: any[]): void" method />

### `dir` <decl type="(...data: any[]): void" method />

### `debug` <decl type="(...data: any[]): void" method />

### `info` <decl type="(...data: any[]): void" method />

### `warn` <decl type="(...data: any[]): void" method />

### `error` <decl type="(...data: any[]): void" method />

## Log filtering level

The log filtering level of the `console` module is determined by the underlying log filtering mechanism of the system and cannot be configured in JavaScript code.


============================================================
FILE_PATH: src/transl/EN/api/global.md

# global object

## Global function

### `encodeURIComponent` <decl type="(str: string): string" function />

The `encodeURIComponent()` global function is used to encode the URI component `str`. It escapes certain special characters to their UTF-8 encoded equivalent percent sign (`%`) escape sequences, which ensures that the component is interpreted correctly when used as part of a URL, especially within a query string parameter, path, or fragment.

Letters, numbers, `- _ . ! ~ * ' ( )` will not be encoded. Other characters are encoded as percent sign escape sequences (e.g. spaces are encoded as `%20`).

`encodeURIComponent()` behaves the same as the function of the same name in Web.

Example:
```js
console.log(encodeURIComponent("https://example.com/page?id=100"));
// output: https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100
```

### `decodeURIComponent` <decl type="(str: string): string" function />

The `decodeURIComponent()` global function is used to decode the URI component `str` encoded by `encodeURIComponent()`. It converts percent sign (`%`) escape sequences back to their original character forms, thereby restoring the original URI components. For example, it will convert `%20` back to a space.

`decodeURIComponent()` behaves the same as the function of the same name in Web.

Example:
```js
console.log(decodeURIComponent("https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100"));
// output: https://example.com/page?id=100
```

### `URI` <decl type="(uri: string | Uri): Uri" function />

This function accepts a string and parses it into a `Uri` object for subsequent processing. The parameter `uri` is the URI string to be parsed.

The return value is an object with the following fields:
- `scheme: string`: the scheme field parsed from the parameter;
- `authority: string`: the authority field parsed from the parameter;
- `path: string`: the path field parsed from the parameter;
- `query: string`: query field parsed from the parameter;
- `origin: string`: the original URI string in the parameter
- `toString: (string`: This method can re-encode this object into a URI string.

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

The `URI` function also accepts an object as a parameter. In this case, the `URI` function will add a `toString` method to the parameter object, through which the URI object can be encoded into a string:
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
FILE_PATH: src/transl/EN/api/i18n.md

# internationalization

This module provides international operation functions within the application.

## Import module

``` js
import i18n from '@system.i18n'
```

## API

### `getLanguage` <decl type="(): string" method></decl>

Get the currently applied language settings. The return value is a string representing the current language code, such as `'zh-CN'`, `'en-US'`, etc.


============================================================
FILE_PATH: src/transl/EN/api/README.md

# API

Glyphix provides a complete set of runtime JavaScript APIs, including [`setInterval`](timer.md), [`console`](console.md) and other APIs similar to the browser environment, as well as various system capability interfaces used to implement the entire application.

However, unlike the browser environment, Glyphix does not provide a DOM interface, so there are no `window`, `document` and other objects, and no DOM operations can be performed.

## Quick App asynchronous interface

Glyphix supports the watch Quick App standard, but we mainly use the Promise style asynchronous interface instead of the callback function style. For example, the callback mode of the `file.readText()` interface in the watch quick app is used like this:
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
But Promise style is often used in Glyphix:
``` js
import file from '@system.file'

// Assume that in an asynchronous function
try {
  const content = await file.readText({ uri: 'internal://files/test.txt' })
  console.log(content)
} catch (e) {
  console.error('read text failed:', e)
}
```
Since the Promise style API is more in line with usage habits after the ES6 standard, this document only retains the type signature of the Promise version.

### Promise vs. callback interface

Unless otherwise specified, all interfaces with a return type of `Promise<...>` support callback functions (lower versions of Quick App standards) and Promise asynchronous interface styles. Callback function-style asynchronous interfaces typically have the following types:
``` ts
type CallbackAPI = (options: {
  success: (data: any) => void,
  fail: (data: any, code: number) => void,
  complete: () => void,
  // Other parameters...
}) => void
```
The asynchronous interface in Promise style is of the following types:
``` ts
type PromiseAPI = (options: any) => Promise<any>
```

When any `success`, `fail` or `complete` attribute exists in the parameter `options`, the API will automatically use the callback function style (no return value), otherwise it will use the Promise return value style.

::: warning
When using the callback function style, the asynchronous API does not return any value, so the `await` syntax cannot be used. So make sure you don't pass in any `success`/`fail` or `complete` callback functions when using Promise/`await` syntax.
:::

### API Example

Taking the [`system.file`](system-file.md) module as an example, all its functions support both Promise and callback-style asynchronous calling modes. The code snippet below gives a comparison of the two API usages.

::: code-tabs#js

@tab async/await

``` js
import file from '@system.file'

// async/await is actually syntactic sugar for Promise
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
  .then(console.log) // Tip: The console.log() type matches Promise.then() and there is no need to use arrow functions.
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

This document will only give Promise-style API types, and examples of asynchronous operations only use await/async syntax.

::: tip
It is not recommended that developers additionally encapsulate the Glyphix API, especially manually encapsulate its callback function compatibility style into Promise mode. This practice requires writing additional code and hurts performance.
:::

## Subscription interface

The API of the subscription class registers a callback function with a module instead of returning the result directly. Unlike general asynchronous interfaces, the callback function of the subscription interface can be executed multiple times. All subscription interfaces support the registration of multiple subscription callback functions, and will return a subscription ID, and you can use the corresponding interface to cancel the subscription.

Glyphix currently does not support the quick app style subscription `fail` callback function, but it may directly throw an exception when the subscription fails.


============================================================
FILE_PATH: src/transl/EN/api/system-app.md

# Application context

## Import module

```js
import app from '@system.app'
```

## Interface definition

### `getInfo` <decl type="(): Manifest" method/>

Get the context information of the current application and return a [`Manifest` object](./system-package.md#manifest-object), which contains the basic information of the application, such as package name, version number, etc.

### `terminate` <decl type="(): void" method version="0.8"/>

Terminate the current application. After calling this method, the app will be closed and the user will need to restart the app to continue using it.

::: note Compatibility Risk
This API is not supported on all platforms, the [`launch.exit()`](./system-launch.md#exit) method may be used as an alternative.
:::

### `loadLibrary` <decl type="(name: string): object | undefined" method/>

Loads a Library Loader registered by the native implementation by name and returns the corresponding library object. If the library with the specified name is not registered, `undefined` is returned.

Typically, it is recommended to mount the library object to the APP object:
```js
// app.js
import app from '@system.app'

export default {
  customLib: app.loadLibrary('custom-library'),
  onCreate() {
    if (!this.customLib) {
      // Handle library loading failure, such as falling back to script implementation
      this.customLib = someStubImplementation();
    } else {
      //Use library objects normally
      this.customLib.someFunction()
    }
  }
}
```
In this way, the component can directly use `this.$app.customLib` to access the library object.

`loadLibrary()` is suitable for accessing non-standard system functions. The application can detect whether the return value is `undefined` to determine whether the current platform supports the library, thereby downgrading to the piling implementation of the script in a general simulator environment without relying on the simulator's special processing of specific module paths.

If your application needs to support both standard quick app APIs and system customization functions, you can decide whether to roll back based on the return result of `loadLibrary()`.

### `keepForeground` <decl type="(options: { enable: boolean }): void" method/>

Sets whether the application remains in the foreground. If the `enable` attribute in the `options` parameter is `true`, the application will try to remain in the foreground.

Using this method requires declaring the application's permissions for `watch.permission.FOREGROUND_SERVICE` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

This method is just a reminder for system behavior and is not mandatory. The application may be switched to the background due to user operations or other high-priority policies. While using this method to keep the app in the foreground, the device can still enter low-power mode:

- If AOD (Always on Display) mode is turned on, the UI refresh rate will be reduced.
- Otherwise, the screen turns off after a while but the app remains running in the foreground.

When the device enters low-power mode (including turning off the screen), the foreground application will still be scheduled and executed at a lower frequency instead of completely sleeping. Therefore it can be used for navigation or fitness applications.


============================================================
FILE_PATH: src/transl/EN/api/system-audiokit.md

# Audio player manager

## Import module

``` ts
import audiokit from '@system.audiokit'
```

## Interface definition

### `getPlayers` <decl type="(): AudioPlayer" method />

Query the list of audio player [`AudioPlayer`](#AudioPlayer) objects available in the system.

### `getActivePlayer` <decl type="(): AudioPlayer" method />

Query the active audio player [`AudioPlayer`](#AudioPlayer) object in the system.

### `subscribe` <decl type="(callback: (PlayerEvent) => void): number" method/>

Listen for changes in the audio player on the system. The parameter `PlayerEvent` of `callback` is [notification event](#PlayerEvent). The ID returned by this method can be used to unsubscribe using the [`unsubscribe()`](#unsubscribe) method.

Type signature of `PlayerEvent`:

```ts
type PlayerEvent = {
  notify: string; // Change event type
  player: string; // Change player name
}
```

Change event type

- `active`: The currently active player in the system has changed
- `append`: The player is added to the system
- `remove`: The player has been removed from the system

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancel player change monitoring. `subscribeID` is the ID value returned by the [`subscribe()`](#subscribe) method.

## `AudioPlayer` object

::: details type signature
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

- The `AudioPlayer` object (hereinafter referred to as: `audiokit.Player`) and the `AudioPlayer` object (hereinafter referred to as: `media.Player`) created in the `system.media` module are different js objects, but they manage the same player. At the same time, the `audiokit.Player` object has more functions than the `media.Player` object, such as: `next()`, `previous()` and other methods. Users can use Operations such as `play()` performed by the `audiokit.Player` object will also be notified to the listener of the `media.Player` object.

### `src` <decl type="string" set get />

Set or read the url that needs to play audio. Supports [local resource path](/framework/application/resource.md#uri-and path) and network resource path using http and https protocols (for example: `https://www.rt-thread.com/service/test/001.mp3`). Here's a simple example of setting src and then starting playback:

```ts
import audiokit from '@system.audiokit'
//Query the active audio players in the system
let player = audiokit.getActivePlayer()
if (player != null) {
  //First stop the currently playing audio
  player.stop()
  //Set the audio url to be played
  player.src = 'https://www.rt-thread.com/service/test/001.mp3'
  // Start playing audio
  player.play()
}
```

### `name` <decl type="string" set get />

The name of the player object. If not set, it defaults to the name of the application that created the player. It should be noted that the name of the player object is not globally unique, and the name cannot be used to identify the player object.

### `icon` <decl type="string" set get />

The player object's icon url. Support [local resource path](/framework/application/resource.md#uri-and path)

### `mode` <decl type="string" set get />

playback mode. The function corresponding to this attribute should be implemented by the player application. The player object does not process it by default and only provides this attribute.

- `sequential`: play sequentially
- `random`: play randomly
- `singleloop`: single loop
- `listloop`: list loop

### `status` <decl type="string" get />

Read the current playback status

- `play`: playing status
- `pause`: Pause playback state
- `stop`: Stop playing status
- `ended`: playback end status
- `error`: playback error status

### `duration` <decl type="number" get />

Total audio duration, unit: seconds

### `position` <decl type="number" set get />

The time position of the current audio playback, unit: seconds

### `songAttribute` <decl type="songAttribute" set get />

Song property object

::: details type signature
```ts
type songAttribute = {
  title: string; // The name of the song
  artist: string; //The name of the performer, which can be an individual or a band
  album: string; // The name of the album to which the song belongs
  year: string; // The year the song was released
  genre: string; // The type of song, such as pop, rock, classical, etc.
  track: string; // The number of the current song in the album, for example: "1/12" means the 1st song, a total of 12 songs
  coverArt: string; // URL of the song cover image
  lyrics: string; // URL of lyrics text
  comments: string; // Additional information, such as copyright remarks, etc.
}
```
:::

The songAttribute object is a Proxy object like the AudioPlayer object. It cannot be serialized and deserialized using JSON, and cannot be referenced in the responsive framework. Here's a simple usage example:

```ts
//Set the name of the song
this.player.songAttribute.title = "Unknown"
//Set the singer of the song
this.player.songAttribute.artist = "Unknown"
// Check the name of the song
console.dir(this.player.songAttribute.title)
```

### `volume` <decl type="number" set get />

The volume of the current player, range: [0.0, 1.0]

### `nextAvailable` <decl type="bool" set get />

Set or query whether the next song can be switched

### `prevAvailable` <decl type="bool" set get />

Set or query whether the previous song can be switched

### `play` <decl type="(): void" method />

Start playing the audio specified in the src attribute

- If the src attribute is not set before calling this method, playback will fail and the onerror event will be triggered;
- This method is a synchronous interface. After executing this interface, you need to wait for the onplay event or onerror event to determine whether the playback is successful or failed. Before the event is triggered, other operations performed will be ignored;

The following is a simple example of calling the play() interface:

```ts
import audiokit from '@system.audiokit'
//Query the active audio players in the system
let player = audiokit.getActivePlayer()
if (player != null) {
  //First stop the currently playing audio
  player.stop()
  //Set the audio url to be played
  player.src = 'https://www.rt-thread.com/service/test/001.mp3'
  //Set onplay event
  player.onplay = () => { console.dir("Start playing") }
  //Set onerror event
  player.onerror = () => { console.dir("Playback error") }
  // Start playing audio
  player.play()
}
```

### `pause` <decl type="(): void" method />

Pause the current audio

- This method is a synchronous interface. After executing this interface, you need to wait for the onpause event or onerror event to determine whether the pause is successful or failed. Before the event is triggered, other operations performed will be ignored;

### `stop` <decl type="(): void" method />

Stop audio playback and replay the audio via play

- This method is a synchronous interface. After executing this interface, you need to wait for the onstop event or onerror event to determine whether the stop is successful or failed. Before the event is triggered, other operations performed will be ignored;

### `release` <decl type="(): void" method />

Release audio resources

- Executing this interface will stop playing the current audio. You need to wait for the onstop event or onerror event to determine whether the stop is successful or failed. Before the event is triggered, other operations performed will be ignored;

### `next` <decl type="(): void" method />

Notify the player application to play the next song. After executing this interface, the onnext event will be triggered to notify the player application that listens to this event, and the player application will execute the logic of song switching.

### `previous` <decl type="(): void" method />

Notify the player application to play the next song. After executing this interface, the onprevious event will be triggered to notify the player application that listens to this event, and the player application will execute the song switching logic.

### `requestFocus` <decl type="({acquireType: string，volumeType: string}): void" method />

Request audio focus. After executing this interface, the underlying layer will be notified to request or release the audio focus, and the underlying layer will control the switching and interruption logic of different types of audio.

The `acquireType` parameter indicates the request type:
- `gain`: Request audio focus
- `loss`: Release audio focus

The `volumeType` parameter indicates the audio type:
- `system`: system prompt
- `media`: media music
- `tts`: voice broadcast

The following example demonstrates how the `requestFocus` function requests audio focus:
``` ts
import audiokit from '@system.audiokit'
//Query the active audio players in the system
let player = audiokit.getActivePlayer()
if (player != null) {
  // Get the audio focus of the media music type
  player.requestFocus({ volumeType: 'media', acquireType: 'gain' });
}
```

### `releaseFocus` <decl type="(): void" method />

Release audio focus. After executing this interface, the bottom layer will be notified to release the audio focus, and the bottom layer will control the switching and interruption logic of different types of audio.

### `onplay` <decl type="?: () => void" set />

Callback event after audio play is successful

### `onpause` <decl type="?: () => void" set />

Callback event after audio pause is successful

### `onstop` <decl type="?: () => void" set />

Callback event after audio stop is successful

### `onended` <decl type="?: () => void" set />

Callback event after audio playback ends

### `onerror` <decl type="?: () => void" set />

Execute callback events for interface errors such as `play` `pause` `stop` `position` and other interfaces. When an error occurs, the corresponding onplay and other events will not be triggered.

### `ontimeupdate` <decl type="?: () => void" set />

A callback event that will be triggered when the position property is updated. This event will only be triggered when the application is in the foreground, and will stop dispatching when the application is in the background.

### `oninterrupt` <decl type="?: (action: {interruptHint: number}) => void" set />

The callback function when an audio interruption event occurs. When the current audio is snatched by audio of the same audio type or other audio types, it will be notified that it is temporarily interrupted or completely interrupted.

The `interruptHint` of the `action` parameter indicates the type of interrupt event:
- `1`: brief interruption (can be automatically restored, such as: music is interrupted)
- `2`: Completely interrupted (cannot be automatically restored, such as: NetEase Cloud was interrupted by Himalaya)

The following example demonstrates how to register an `oninterrupt` callback function, which is called when an event occurs:
``` js
player.oninterrupt = (action) => {
  console.log(action.interruptHint)
}
```

### `onnext` <decl type="?: () => void" set />

Callback event when the next song needs to be played

### `onprevious` <decl type="?: () => void" set />

Callback event when the previous song needs to be played

### `onrequestplay` <decl type="?: () => void" set />

When the bottom layer needs to start playback, the callback event is triggered to notify the js application, and the js application executes the logic of starting playback.

### `onrequestpause` <decl type="?: () => void" set />

When the bottom layer needs to pause playback, the callback event is triggered to notify the js application, and the js application executes the logic of pausing playback.

### `onrequeststop` <decl type="?: () => void" set />

When the bottom layer needs to stop playing, the callback event is triggered to notify the js application, and the js application executes the logic of stopping the playback.

### `onsongattribute` <decl type="?: () => void" set />

Callback event when the song attribute object changes

### `onposition` <decl type="?: () => void" set />

Execute `position` to set the time and position of the current audio playback. The callback event is successful.

### `onrequestfocus` <decl type="?: () => void" set />

Callback event when requesting audio focus successfully

### `onreleasefocus` <decl type="?: () => void" set />

Callback event when audio focus is released successfully

### `onmodechanged` <decl type="?: () => void" set />

Callback event when playback mode changes

### `onvolumechange` <decl type="?: () => void" set />

Callback event when player volume changes


============================================================
FILE_PATH: src/transl/EN/api/system-battery.md

# Battery status

## Import module

``` js
import battery from '@system.battery'
```

## API

### `getStatus` <decl type="(): Promise<{charge: ChargeState, level: number}>" method />

Get the battery's charge state `charge` ([`ChargeState`](#chargestate) type) and power value `level`. The power value is an integer between $[0, 100]$.

## type

### `ChargeState`

`ChargeState` enumerates all battery charging states, which are defined as follows:
``` ts
type ChargeState = 'charging' | 'discharging' | 'not-charging' | 'full'
```
The meaning of each value is:
- `'charging'`: The battery is in charging state;
- `'discharging'`: Disconnect charging state;
- `'not-charging'`: not in charging state;
- `'full'`: The battery is fully charged.


============================================================
FILE_PATH: src/transl/EN/api/system-ble.md

# Low power Bluetooth module

This module provides Bluetooth capabilities based on Bluetooth Low Energy (BLE) technology, supports initiating BLE scans, and connects and transmits data based on the Generic Attribute Profile (GATT) (currently only the creation of GattClient is supported, and the creation of GattServer is not supported at the moment).

::: warning
Most of the APIs in `@system.bluetooth.ble` are [Promise asynchronous operations](#Promise asynchronous operations), which are essentially different from synchronous IO access. Be sure to understand the basic concepts of asynchronous programming and be familiar with the use of Promise and `async/await`.
:::

## Import module

``` js
import ble from '@system.bluetooth.ble'
```

## Permissions

::: tip
Applications using this module need to declare permission: watch.permission.BLUETOOTH
:::

## ble interface definition

### `ResultCode`

Result enumeration returned in Promise

- `0`: success;
- `1`: Bluetooth Low Energy is not turned on;
- `2`: Parameter error;
- `3`: Failed to enable Bluetooth Low Energy;
- `4`: No Bluetooth adapter available;
- `5`: Connection failed;
- `6`: Failed to disconnect;
- `7`: Setting this attribute is not supported yet;
- `8`: unknown error;

### `startBLEScan`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

Start scanning and use Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

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

Stop scanning and use Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

Here's an example of stopping a scan:
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

This object is used to represent the reported scan results. The type signature is as follows:

```ts
/**
 * Scan result object definition
 */
type ScanResult = {
    deviceId: string; // Device ID (for example: "AA:BB:CC:DD:EE:FF")
    rssi: number; // signal strength in dBm
    data: ArrayBuffer; // Original data of broadcast message
    deviceName: string; // device name (if any)
    connectable: boolean; // Whether it can be connected, true means it can be connected
}
```

### `getBLEScanResults`
<decl method><pre>
(): Promise&lt;Array&lt;ScanResult&gt;&gt;
</pre></decl>

Query the scan results and use Promise asynchronous callback. This interface asynchronously returns an array containing [`ScanResult`](#scanresult) objects (i.e. Array&lt;[`ScanResult`](#scanresult)&gt;).

::: warning
Because the underlying Bluetooth adapter is a singleton, multiple applications may operate Bluetooth devices at the same time. It will exist: After application A starts scanning for a period of time, application B starts scanning again. At this time, the scan results monitored by application B are incomplete. In order to handle this situation, it is recommended that all applications immediately query the current scan results after starting scanning.
:::

Here is an example of querying the scan results after starting the scan:
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
            //Query scan results
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

Subscribe to scan status changes and use Callback asynchronous callback. When the scan status changes, the `callback` callback function is automatically called. This interface synchronously returns a subscription ID, which is used to cancel the subscription.

Callback function parameter field description:
- `scan`: current scanning status. true means scanning is in progress, false means scanning has stopped.

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

Unsubscribe from scanning status changes. The parameter `subscribeId` is the subscription ID returned by the [`subscribeScanStatus`](#subscribescanstatus) method.

Here is an example of unsubscribing from a scan status change:
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

Subscribe to scan result reporting events and use Callback asynchronous callback. Whenever a new device is scanned, the `callback` callback function is automatically called. This interface synchronously returns a subscription ID, which is used to cancel the subscription.

::: tip
The scanning results are reported in incremental mode. Each discovery is reported one by one. After monitoring this event, the user needs to store the scanning results himself.
:::

Callback function parameter field description:
- [`ScanResult`](#scanresult): The new device object scanned.

The following is an example of subscribing to scan result reporting events:
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

Unsubscribe from scanning result reporting events. The parameter `subscribeId` is the subscription ID returned by the [`subscribeBLEDeviceFind`](#subscribebledevicefind) method.

The following is an example of unsubscribing from scanning result reporting events:
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

This object is used to represent the Client object in the Gatt protocol. The type signature is as follows:

```ts
/**
 *GattClientDevice object type definition
 */
typeGattClientDevice = {
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

Create a [`GattClientDevice`](#gattclientdevice) instance to represent the client in the GATT connection. This interface synchronously returns a [`GattClientDevice`](#gattclientdevice) instance.

- Through this instance, you can operate the client-side behavior, such as calling [`connect`](#connect) to initiate a connection to the peer device, and calling [`getServices`](#getservices) to obtain all service capabilities supported by the peer device.
 - The deviceId (device address) required to create this instance represents the server-side device address. You can obtain the server device address through the [`startBLEScan`](#startblescan) interface, and you must ensure that the BLE broadcast of the server device is connectable.

Here is an example of creating an instance of [`GattClientDevice`](#gattclientdevice):
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    create() {
        // Please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
    },
}
```

## GattClientDevice interface definition

### `connect`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

The client actively initiates a GATT protocol connection with the server Bluetooth device and uses Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

- Before using the methods of this class, you need to construct an instance of this class through the [`createGattClientDevice`](#creategattclientdevice) method.
 - Multiple GATT connections can be managed by creating different instances of this class.

The following is an example of initiating a GATT protocol connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async connect() {
        // Please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

The client actively disconnects the GATT protocol connection with the server Bluetooth device and uses Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

Here is an example of disconnecting the GATT protocol:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        address: null,
    },
    gattClient: null,
    async connect() {
        // Please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

Close the client instance and use Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

### `getDeviceName`
<decl method><pre>
(): Promise&lt;string&gt;
</pre></decl>

The client obtains the name of the remote Bluetooth low energy device and uses Promise asynchronous callback. This interface asynchronously returns a device name of type &lt;string&gt;.

The following is an example of obtaining the device name after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async name() {
        let clientName = 'N/A'
        // Please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

This object is used to represent the GATT service structure, with the following type signature:

```ts
/**
 * GATT service structure definition, which can contain multiple characteristic values BLECharacteristic and other dependent services.
 */
type GattService = {
    serviceUuid: string; // Service UUID, identifies a GATT service. For example: 00001888-0000-1000-8000-00805f9b34fb.
    isPrimary: boolean; // Whether it is the primary service. true means it is the primary service, false means it is the secondary service.
    characteristics: Array<BLECharacteristic>; // List of characteristic values ​​contained in the current service.
    includeServices: Array<GattService>; // Other services that the current service depends on.
}
```

### `getServices`
<decl method><pre>
(): Promise&lt;Array&lt;GattService&gt;&gt;
</pre></decl>

The client side obtains all services of Bluetooth low energy devices, that is, service discovery, using Promise asynchronous callback. This interface asynchronously returns an array of type Array&lt;[`GattService`](#gattservice)&gt; containing all services.

The following is an example of obtaining all services of the device after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    async onShow() {
        // Please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

This object is used to represent the attributes supported by GATT characteristic values. The type signature is as follows:

```ts
/**
 * Describes the attributes supported by GATT eigenvalues. Determines how characteristic value contents and descriptors are used and accessed.
 */
type GattProperties = {
    write: boolean; // Whether this characteristic value supports writing operations. true means it is supported and needs to reply to the peer device when being written, false means it is not supported.
    writeNoResponse: boolean; // Whether this characteristic value supports writing operations. true means it is supported, and there is no need to reply to the peer device when being written, false means it is not supported.
    read: boolean; // Whether this characteristic value supports read operations. true means supported, false means not supported.
    notify: boolean; //Whether this characteristic value supports actively notifying the peer device of the characteristic value content. true means it is supported and the peer device does not need to reply to confirm, false means it is not supported.
    indicate: boolean; // Whether this characteristic value supports indicating the characteristic value content to the peer device. true means it is supported and the peer device needs to reply to confirm, false means it is not supported.
    broadcast: boolean; // Whether this characteristic value supports being sent as broadcast content by the server. true means it is supported, the server can carry the characteristic value content in the broadcast message as ServiceData type, false means it is not supported.
    authenticatedSignedWrite: boolean; //Whether this characteristic value supports signed writing operations, replacing the encryption process by performing signature verification on the written content. true means supported, false means not supported.
    extendedProperties: boolean; //Whether there are extended properties for this characteristic value. true indicates that the extended attribute exists, false indicates that it does not exist.
}
```

### `BLECharacteristic`

This object is used to represent GATT characteristic values. The type signature is as follows:

```ts
/**
 * GATT characteristic value type definition, which is the core data unit of service GattService
 */
type BLECharacteristic = {
    serviceUuid: string; // The service UUID to which the characteristic value belongs, for example: 00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // Characteristic value UUID, for example: 00002a11-0000-1000-8000-00805f9b34fb
    characteristicValue: ArrayBuffer; //The data content of the characteristic value, used when reading and writing data
    descriptors: Array<BLEDescriptor>; // List of descriptors contained in the characteristic value
    properties: GattProperties; // Properties supported by characteristic values
    characteristicValueHandle: number; // The unique identification handle of the characteristic value. When the server-side BLE Bluetooth device provides multiple identical UUID feature values, you can use this handle to distinguish different feature values.
}
```

### `readCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic): Promise&lt;BLECharacteristic&gt;
</pre></decl>

The client side reads data from the specified server side characteristic value and uses Promise asynchronous callback. This interface asynchronously returns an object of type [`BLECharacteristic`](#blecharacteristic).

- This interface needs to pass in an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic value needs to be read.

The following is an example of reading data from a specified characteristic value after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async read() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, obtain what needs to be read: characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // The test only attempts to read the first characteristic value of the first service. If you need to read other characteristic values, please modify it yourself.
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Read the specified characteristic value
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

Characteristic value writing method enumeration

- `1`: After writing the characteristic value, the peer Bluetooth device needs to reply with confirmation.
- `2`: After writing the characteristic value, the peer Bluetooth device does not need to reply.

### `writeCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic, writeType: GattWriteType): Promise&lt;number&gt;
</pre></decl>

The client writes data to the specified server-side characteristic value and uses Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

- This interface needs to pass in an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic value needs to be written
 - This interface needs to pass in a [`GattWriteType`](#gattwritetype) enumeration value to indicate the way to write data.

下面是一个GATT连接成功后，从指定的特征值写入数据的示例：
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
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 调用: connect 接口发起连接
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. 服务发现，获取需要操作的：characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // 测试只尝试操作第一个服务的第一个特征值，如果需要操作其它特征值，请自行修改
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. 写指定特征值
        if (this.gattClient && this.characteristic) {
            // 生成指定长度且携带随机数的 ArrayBuffer
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

This object represents a GATT descriptor and its type is defined as follows:

```ts
/**
 * GATT descriptor type definition, which is the data unit of the characteristic value BLECharacteristic, is used to describe the additional information and attributes of the characteristic value
 */
type BLEDescriptor = {
    serviceUuid: string; // The service UUID to which the characteristic value belongs, for example: 00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // Characteristic value UUID, for example: 00002a11-0000-1000-8000-00805f9b34fb
    descriptorUuid: string; // Descriptor UUID, for example: 00002902-0000-1000-8000-00805f9b34fb
    descriptorValue: ArrayBuffer; //The data content of the descriptor, used when reading and writing data
    descriptorHandle: number; // The unique identification handle of the descriptor. When the server-side BLE Bluetooth device provides multiple same UUID descriptors, this handle can be used to distinguish different descriptors.
}
```

### `readDescriptorValue`
<decl method><pre>
(descriptor: BLEDescriptor): Promise&lt;BLEDescriptor&gt;
</pre></decl>

The client reads data from the specified server descriptor and uses Promise asynchronous callback. This interface asynchronously returns an object of type [`BLEDescriptor`](#bledescriptor).

- This interface needs to pass in an object of type [`BLEDescriptor`](#bledescriptor) to indicate which descriptor needs to be read.

The following is an example of reading data from the specified descriptor after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    descriptor: null,
    async read() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, obtain what needs to be read: characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        console.dir("gatt client found:" + JSON.stringify(this.services))
        if (this.services.length > 0) {
            // The test only tries to read the first descriptor of the first characteristic value of the first service. If you need to read other descriptors, please modify it yourself.
            // It should be noted that not all characteristic values have descriptors. You can adjust it yourself and select a service test that has descriptors and read and write permissions.
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

The client writes data to the specified server descriptor and uses Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

- This interface needs to pass in an object of type [`BLEDescriptor`](#bledescriptor) to indicate which descriptor needs to be written.

The following is an example of writing data from a specified characteristic value after a successful GATT connection:
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
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 调用: connect 接口发起连接
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. 服务发现，获取需要读取的：characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        console.dir("gatt client found:" + JSON.stringify(this.services))
        if (this.services.length > 0) {
            // 测试只尝试操作第一个服务的第一个特征值的第一个描述符，如果需要操作其它描述符，请自行修改
            // 需要注意的是，不是所有的特征值都有描述符，这里可以自行调整，选取有描述符且有读写权限的服务测试
            this.descriptor = this.services[0].characteristics[0].descriptors[0];
        }
        // 4. 写指定描述符
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

The client side obtains the GATT connection link signal strength (Received Signal Strength Indication, RSSI) and uses Promise asynchronous callback. This interface asynchronously returns a signal strength of type &lt;number&gt;, unit: dBm

The following is an example of obtaining the device signal strength after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    asyncrssi() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

The client side obtains the MTU (maximum transmission unit) size of the GATT connection link and uses Promise asynchronous callback. This interface asynchronously returns the length of a &lt;number&gt; type, unit: byte

The following is the method to obtain the MTU (maximum transmission unit) size of the GATT connection link after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async mtu() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

The client negotiates the MTU (maximum transmission unit) size with the server and uses Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

### `setCharacteristicChangeNotification`
<decl method><pre>
(characteristic: BLECharacteristic, enable: boolean): Promise&lt;number&gt;
</pre></decl>

The client side enables or disables the ability to receive server side feature value content change notifications, using Promise asynchronous callbacks. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

- This interface needs to pass in an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic value needs to be operated
 - This interface needs to pass a boolean value, indicating whether to turn on or off the content change notification capability. true means turned on, false means turned off.

The following is an example of turning on feature value content change notification after the GATT connection is successful:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async notify() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, obtain what needs to be read: characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // The test only attempts to operate the first characteristic value of the first service. If you need to operate other characteristic values, please modify it yourself.
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Operate the specified characteristic value
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeNotification(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Notification success')
                } else {
                    console.log('This characteristic value does not allow setting to enable monitoring, ResultCode:' + result);
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

The client side enables or disables the ability to receive server side characteristic value content change instructions, using Promise asynchronous callbacks. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

- This interface needs to pass in an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic value needs to be operated
 - This interface needs to pass a boolean value, indicating whether to turn on or off the ability to indicate content change. True means turned on, false means turned off.

The following is an example of turning on the characteristic value content change indication after the GATT connection is successful:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async indication() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, obtain what needs to be read: characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // The test only attempts to operate the first characteristic value of the first service. If you need to operate other characteristic values, please modify it yourself.
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Write the specified feature value
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeIndication(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Indication success')
                } else {
                    console.log('This characteristic value does not allow setting to enable monitoring, ResultCode:' + result);
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

The client subscribes to server-side characteristic value change events. When the characteristic value changes, the `callback` callback function is automatically called. This interface synchronously returns a subscription ID, which is used to cancel the subscription.

Callback function parameter field description:
- [`BLECharacteristic`](#blecharacteristic): The changed characteristic value object.

The following is an example of turning on the characteristic value content change indication after the GATT connection is successful:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Subscribe to feature value changes
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

The client unsubscribes from the server-side characteristic value change event. The parameter `subscribeId` is the subscription ID returned by the [`subscribeBLECharacteristicChange`](#subscribeblecharacteristicchange) method.

The following is an example of turning on the characteristic value content change indication after the GATT connection is successful:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Unsubscribe from feature value changes
        if (this.listener) {
            this.gattClient.unsubscribeBLECharacteristicChange(this.listener)
            this.listener = null
        }
    },
}
```

### `ConnectionState`

Bluetooth connection status enumeration

- `0`: disconnected
- `1`: Connecting
- `2`: Connected
- `3`: Disconnecting

### `GattDisconnectReason`

GATT link disconnection reason enumeration

- `0`: Reason is not available
- `1`: connection timeout
- `2`: The peer device actively disconnects
- `3`: The local device actively disconnects
- `4`: Unknown reason for disconnection

### `BLEConnectionChangeState`

This object is used to represent the Bluetooth connection status, and its type signature is as follows:

```ts
/**
 * Bluetooth connection status type definition
 */
type BLEConnectionChangeState = {
    deviceId: string; // Device ID (for example: "AA:BB:CC:DD:EE:FF")
    state: ConnectionState; // Bluetooth connection status
    reason: GattDisconnectReason; //The reason why the GATT link is disconnected
}
```

### `subscribeBLEConnectionStateChange`
<decl method><pre>
(callback: Callback(connectionChangeState: BLEConnectionChangeState) => void): number
</pre></decl>

The client subscribes to the connection status change event of the GATT protocol. When the connection status changes, the `callback` callback function is automatically called. This interface synchronously returns a subscription ID, which is used to cancel the subscription.

Callback function parameter field description:
- [`BLEConnectionChangeState`](#bleconnectionchangestate): connection state.

The following is an example of subscribing to the connection status after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Subscribe to changes in connection status
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

The client unsubscribes from the connection status change event of the GATT protocol. The parameter `subscribeId` is the subscription ID returned by the [`subscribeBLEConnectionStateChange`](#subscribebleconnectionstatechange) method.

Here's an example of unsubscribing from a connection state:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Subscribe to changes in connection status
        this.listener = this.gattClient.subscribeBLEConnectionStateChange((result) => {
            console.log('connect changed:' + JSON.stringify(result))
        })
        // 4. Unsubscribe from changes in connection status
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

The client subscribes to MTU (Maximum Transmission Unit) size change events. When the MTU changes, the `callback` callback function is automatically called. This interface synchronously returns a subscription ID, which is used to cancel the subscription.

Callback function parameter field description:
- mtu: MTU (maximum transmission unit) size.

The following is an example of subscribing to MTU changes after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

The client unsubscribes from the MTU (Maximum Transmission Unit) size change event. The parameter `subscribeId` is the subscription ID returned by the [`subscribeBLEMtuChange`](#subscribeblemtuchange) method.

Here is an example of unsubscribing from MTU changes:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 订阅MTU的变化
        this.listener = this.gattClient.subscribeBLEMtuChange((mtu) => {
            console.log('mtu changed:' + mtu)
        })
        // 3. 取消订阅MTU的变化
        if (this.gattClient && this.listener) {
            this.gattClient.unsubscribeBLEMtuChange(this.listener)
            this.listener = null
        }
    },
}
```


============================================================
FILE_PATH: src/transl/EN/api/system-brightness.md

# Brightness management

## Import module

``` js
import brightness from '@system.brightness'
```

## API

### `getValue` <decl type="(): number" method />

Get the brightness value of the screen, the range is $[0, 1]$.

### `setValue` <decl type="(value: number): void" method />

Set the brightness value of the screen. The range of `value` is $[0, 1]$.

### `getMode` <decl type="(): string" method />

Get the brightness mode of the screen.

### `setMode` <decl type="(mode: number): void" method />

Set the screen brightness mode. When `number` is set to `0`, it is standard mode. When `number` is set to $1$, it is automatic mode.

### `setKeepScreenOn` <decl type="(mode: Boolean): void" method />

Set whether to keep the screen always on. When `mode` is set to `true`, the screen is always on. When `mode` is set to `false`, the screen is always on.

### `wakeScreenOn`
<decl method><pre>
(options: {
  screenOn: boolean,
  timeout?: number,
}): void
</pre></decl>

Turn the screen on or off. The functions of each field of the options parameter are:
- `screenOn`: whether to light up the screen
- `timeout`: automatic extinguishing time, no time limit if not filled in


============================================================
FILE_PATH: src/transl/EN/api/system-calendar.md

# calendar

## Import module

``` js
import calendar from '@system.calendar'
```

## Interface definition

### `getLunar` <decl method type="(date: Date): LunarDate" />

Get the lunar date information of a `Date` object and return the lunar date description of type [`LunarDate`](#lunardate).

### `getLunar` <decl method type="(year: number, month: number, day: number): LunarDate" />

Get the lunar calendar information corresponding to the specified Gregorian calendar year, month, and day, and return the lunar calendar date description of type [`LunarDate`](#lunardate). The parameter meanings are as follows:
- `year`: the complete number of the year, such as `2024`;
- `month`: month number, starting from `0`, the number of December is $11$;
- `day`: date number, starting from `1`.

## Type definition

### `LunarDate`

``` ts
type LunarDate = {
  month: string, // lunar month name
  day: string, // Lunar date name
  festival?: string // Festival name, may be undefined
}
```

- `month`: The name of the lunar month, such as `'first month'`, `'February'`.
- `day`: The name of the lunar calendar date, such as `'the first day of the lunar month'`, `'the fifteenth day'`.
- `festival`: Festival name, if there is no festival, the attribute is undefined.


============================================================
FILE_PATH: src/transl/EN/api/system-cipher.md

# Password algorithm

## Import module

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

`aes` encryption and decryption, the functions of each field of the `options` parameter are:
- `action`: type of encryption and decryption, two optional values: `'encrypt'`: encryption, `'decrypt'`: decryption;
- `text`: the text content to be encrypted or decrypted. The text to be encrypted should be a piece of ordinary text, and the text to be decrypted should be a piece of binary value encoded by `base64`;
- `key`: the key used for encryption or decryption, a string generated after `base64` encoding. The key must be a multiple of $16$ bytes before being decoded by `bsae64`;
- `transformation`: encryption mode (`ECB'`, `'CBC'`, `'CFB'`, `'CTR'`, `'OFB'`) and padding of `AES` algorithm, default is `'AES/CBC/PKCS5Padding'`. AES Padding Optional padding options are:
  - `'PKCS5Padding''`
  - `'PKCS7Padding''`
  - `'NoPadding''`
  - `'OneAndZerosPadding''`
  - `'ZerosAndLenPadding''`
  - `'ZerosPadding'`
- `iv`: initial vector for AES encryption and decryption, a string encoded by Base64, the default value is the value of the `key` field;
- `ivOffset`: initial vector offset for AES encryption and decryption, the default value is $0$;
- `ivLen`: The length of the initial vector in bytes for AES encryption and decryption, the default value is $16$;

::: details sample code

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

AesTest() //Print encrypted and decrypted text, console output
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

`rsa` encryption and decryption, the field functions of the `options` parameter are:
- `action`: type of encryption and decryption, two optional values: `'encrypt'`: encryption, `'decrypt'`: decryption;
- `text`: The text content to be encrypted or decrypted. The text content to be decrypted should be a binary value encoded by Base64;
- `key`: `RSA` key, a string generated after `base64` encoding, `key` is the public key when encrypting, and `key` is the private key when decrypting;
- `transformation`: Padding item of RSA algorithm, default is `RSA/None/OAEPwithSHA-256andMGF1Padding`. RSA optional padding is:
  - `'PKCS_v15andMGF1Padding'`
  - `'OAEPwithMD5andMGF1Padding''`
  - `'OAEPwithSHA-1andMGF1Padding'`
  - `'OAEPwithSHA-256andMGF1Padding''`

::: details sample code
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

rsaTest() // 打印加解密的文本，控制台输出样例
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

`sign` signature, the functions of each field of the `options` parameter are:
- `text`: signature content;
- `key`: RSA private key;
- `algorithm`: signature algorithm, default is `'SHA256withRSA'`. Optional signature algorithms are:
  - `'MD5withRSA'`
  - `'SHA1withRSA'`
  - `'SHA256withRSA''`
  - `'SHA512withRSA''`

::: details sample code

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

`hash` encryption, the functions of each field of the `options` parameter are:
- `data`: the original data to generate the summary;
- `algorithm`: Digest algorithm, optional values ​​are `'md5'`, `'sha1'`, `'sha224''`, `'sha256''`, `'sha384''`, `'sha512'';
- `encode`: The encoding and type of the returned data, the values are:
  - `'hex'`: Default value, returns hex encoded string;
  - `'base64'`: The return value is the Base64-encoded string of the encryption result;
  - `'arraybuffer'`: The return value is ArrayBuffer type data;

::: details sample code

``` js
async function md5Test(){
  const res = await cipher.hash({
    algorithm: 'md5',
    data: 'hello'
  })
  console.log(res)
}
md5Test() // Print the generated summary and console output
// output: 5d41402abc4b2a76b9719d911017c592
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

Use the HMAC algorithm to generate a keyed message authentication code. The functions of each field of the `options` parameter are:
- `data`: the original data to generate the summary;
- `algorithm`: digest algorithm, optional `'md5'`, `'sha1'`, `'sha224''`, `'sha256''`, `'sha384'`, `'sha512'';
- `key`: key;
- `encode`: The encoding and type of the returned data, the values are:
  - `'hex'`: Default value, returns hex encoded string;
  - `'base64'`: The return value is the Base64-encoded string of the encryption result;
  - `'arraybuffer'`: The return value is of `ArrayBuffer` type;

::: details sample code

``` js
async function hmacTest() {
  let res = await cipher.hmac({
    data: 'hello',
    algorithm: 'sha1',
    key: '1234567890'
  })
  console.log(res)
}
hmacTest() // Print the generated summary and console output
// output: 6fce0a55cf8bae80e2cf479b50035f773491c5ad
```
:::

### `base64Encode` <decl type="(data: string | ArrayBuffer): Promise&lt;string>" method />

Base64 encode the input data.

### `base64Decode` <decl type="(data: string | ArrayBuffer): Promise&lt;ArrayBuffer>" method />

Base64 decode the input data.

::: details sample code

``` js
async function base64Test() {
  const originalData = 'Hello, World!';
  const encodedData = await cipher.base64Encode(originalData); // 编码数据

  console.log('Encoded Data:', encodedData);

  const decodedArrayBuffer = await cipher.base64Decode(encodedData); // 解码数据

  const uint8Array = new Uint8Array(decodedArrayBuffer);
  let decodedData = '';

  for (let i = 0; i < uint8Array.length; i++) {
    decodedData += String.fromCharCode(uint8Array[i]);
  }

  console.log('Decoded Data:', decodedData);
}

base64Test()  //打印编码和解码的结果
// Encoded Data: SGVsbG8sIFdvcmxkIQ==
// Decoded Data: Hello, World!
```
:::


============================================================
FILE_PATH: src/transl/EN/api/system-compass.md

# compass

The `@system.compass` module provides the ability to access the device's compass sensor, which can obtain information about the device's orientation relative to Earth's magnetic North Pole.

## Import module

``` js
import compass from '@system.compass'
```

## Interface definition

### `subscribe` <decl type="(callback: (data: Value) => void): number" method/>

Subscribe to Compass data changes. The callback function is automatically called when the device orientation changes. The `callback` callback function receives compass data of type [`Value`](#value).

Returns a subscription ID for unsubscribing.

### `unsubscribe` <decl type="(subscribeId: number): void" method/>

Cancel Compass data subscription. The parameter `subscribeId` is the subscription ID returned by the [`subscribe()`](#subscribe) method.

This method should be called when the page or component is destroyed to cancel the subscription of `subscribe()`:
``` js
const subscribeId = compass.subscribe((data) => {
  console.log(`Direction: ${data.direction} radians`)
  console.log(`Accuracy: ${data.accuracy}`)
})

// Unsubscribe
compass.unsubscribe(subscribeId)
```


### `calibration` <decl type="(): Promise<void>" method/>

Start the compass calibration process. When the compass accuracy is low, guide the user to operate and call this method to calibrate the compass.

This function returns a resultless Promise object, which will be resolved when the system completes calibration.

### `getValue` <decl type="(): Promise<Value>" method/>

Get current compass data. Returns an asynchronous result, a Promise object containing compass direction and accuracy information (of type [`Value`](#value)).

Example:
``` js
// Use Promise
compass.getValue().then((data) => {
  console.log(`Direction: ${data.direction} radians`)
  console.log(`Accuracy level: ${data.accuracy}`)
})

// Use async/await
async function getCompassData() {
  const data = await compass.getValue()
  console.log(`Direction: ${data.direction} radians`)
  console.log(`Accuracy level: ${data.accuracy}`)
}
```

::: note
Due to implementation flaws, this method does not support callback-style calls (such as `{ success: (data) => {...} }`), please use Promise or async/await.
:::

## Type definition

### `Value`

The signature of the compass data type `Value` is as follows:
``` ts
type Value = {
  direction: number // Compass direction (radians)
  accuracy: number // Compass accuracy level
}
```
Property description:
- `direction`: The angle in radians between the Y-axis of the device and the Earth's magnetic north pole, the value range is $[0,2\pi]$, where:
  - `0`: due north direction
  - `Math.PI/2` (about 1.57): due east
  - `Math.PI` (about 3.14): due south direction
  - `3 * Math.PI / 2` (approximately 4.71): due west
- `accuracy`: accuracy level of compass data
  - `3`: high accuracy
  - `2`: medium accuracy
  - `1`: low precision
  - `0`: Untrustworthy (unknown reason)
  - `-1`: Untrusted (sensor lost connection)

Example:
``` js
// Determine direction
const data = await compass.getValue()
const degrees = data.direction * 180 / Math.PI // Convert to angle

console.log(`Direction: ${degrees}°`)
if (degrees >= 337.5 || degrees < 22.5) {
  console.log('Towards north')
} else if (degrees >= 22.5 && degrees < 67.5) {
  console.log('Towards the northeast')
} else if (degrees >= 67.5 && degrees < 112.5) {
  console.log('Towards the east')
}
// ...judgment in other directions

// Check accuracy
if (data.accuracy >= 2) {
  console.log('Compass accuracy is good')
} else if (data.accuracy === 1) {
  console.log('Compass accuracy is low, calibration is recommended')
  compass.calibration()
} else {
  console.log('Compass data is not trustworthy')
}
```


============================================================
FILE_PATH: src/transl/EN/api/system-configuration.md

# Apply configuration

## Import module

```js
import configuration from '@system.configuration'
```

## Interface definition

### `getLocale`
<decl method><pre>
(): {
  language: string,
  countryOrRegion: string,
}
</pre></decl>

Get the current locale of the application. By default, the system locale is used, which may change due to settings or system locale changes.
 - `language` represents the current language, such as 'zh', 'en', etc.,
 - `countryOrRegion` represents the current country or region, such as 'CN', 'US', etc.


============================================================
FILE_PATH: src/transl/EN/api/system-device.md

# Device information

## Import module

``` js
import device from '@system.device'
```

Developers need to declare the application's access permissions to `watch.permission.DEVICE_INFO` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

## Interface definition

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

Get basic information about the device. The meaning of the attribute fields of the returned object is:
- `brand`: The brand name of the device.
- `manufacturer`: Equipment manufacturer.
- `model`: device model.
- `product`: device code name.
- `osType`: operating system name.
- `osVersionName`: operating system version name.
- `platformVersionName`: running platform version name.
- `platformVersionCode`: running platform version number.
- `language`: system language.
- `region`: system region.
- `deviceName`: device name.

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

Obtain device identification information in batches. The parameter `types` specifies the type of information to be obtained. It is an Array object composed of `'device'`, `'mac'`, `'user'` or `'advertising'` elements. Depending on the `types` value, the meaning of each field of the returned object's properties is:
- `type`: .
- `device`: unique identifier of the device, only exists when `types` contains the `'device''` element.
- `mac`: MAC address of the device, present only if `types` contains a `'mac'` element.
- `user`: The user's unique identifier, only exists when `types` contains the `'user'` element.
- `advertising`: A unique identifier for advertising, present only when `types` contains an `'advertising'` element.

### `getDeviceId` <decl type="(): Promise<{deviceId: string}>" method />

Get the unique identifier of the device.

### `getSerial` <decl type="(): Promise<{serial: string}>" method />

Get the device serial number.

### `getTotalStorage` <decl type="(): Promise<{totalStorage: number}>" method />

Get the total size of storage space in bytes.

### `getAvailableStorage` <decl type="(): Promise<{availableStorage: number}>" method />

Get the available size of storage space in bytes.

::: tip
The values ​​returned by the `getTotalStorage()` and `getAvailableStorage()` methods on the emulator may be inaccurate and do not change as the storage space changes.
:::

### `screenWidth` <decl type="number" get />

The device's screen width in pixels.

### `screenHeight` <decl type="number" get />

The device's screen height in pixels.

### `screenDensity` <decl type="number" get />

The device's screen pixel density in $\rm PPI$.

### `screenShape` <decl type="'rect' | 'circle'" get />

The screen shape of the device. The meaning of the values is as follows:
- `'rect'`: The device has a rectangular screen.
- `'circle'`: The device has a circular screen.

### `memoryProfile` <decl type="number" get />

Gets the device's memory profile properties. This attribute is the JavaScript API version of the [`memory-profile`](/framework/render/media-query.md#memory-profile) media query attribute. For details, please refer to the documentation of the media query attribute.

Unlike the `memory-profile` media query attribute, the value of the `memoryProfile` attribute is an integer, with the unit fixed at $\rm KiB$.


============================================================
FILE_PATH: src/transl/EN/api/system-devtools.md

# Debug interface

## Import module

``` js
import devtools from '@system.devtools'
```

## API

### `command` <decl type="(cmd: string, fn: (argv: string[]) => void): void" method />

Register a function `fn` as a shell command named `cmd`. After registration, you can use the `dev` command on the device terminal to call it. For example
``` bash
dev cmd arg1 arg2
```
A command named `'cmd'` is called with the argument list `['arg1', 'arg2']`.


============================================================
FILE_PATH: src/transl/EN/api/system-exchange.md

# Exchange data

The exchange data module `system.exchange` is used to store shared data across applications. This data is not stored persistently and will be lost once the device is powered off. . The data stored in `system.exchange` can be accessed in all applications, so this module can be used to store some configuration information of the application, but it is not suitable for storing sensitive data.

`system.exchange` stores data as key-value pairs, where the key must be a string and the value is a JSON value (or a JavaScript value that can be serialized to JSON).

## Import module

``` js
import exchange from '@system.exchange'
```

## API

### `get` <decl type="(key: string): any" method />

Get the value corresponding to the key name `key` in the storage. Returns `undefined` if the key-value pair does not exist.

### `set` <decl type="(key: string, value: any): void" method />

This method accepts a key name `key` and a value `value` as parameters and adds this key-value pair to the storage. If the key name already exists, update its corresponding value.

### `delete` <decl type="(key: string): boolean" method />

Delete the key-value pair corresponding to the key name `key` in the storage. Returns `true` if the key-value pair exists and is successfully deleted.

### `watch` <decl type="(key: string, callback: (value: any) => void): number" method />

Monitor changes in the data value of the key named `key` in the storage, and call the `callback` callback function when the value changes. The parameter `value` of the callback function is the new data value. The `watch()` method returns a `wtacher ID`, which can be used with the [`unwatch()`](#unwatch) method to unwatch.

::: tip
When monitoring is no longer needed, the [`unwatch()`](#unwatch) method should be used to unblock monitoring, otherwise memory leaks may occur.
:::

### `unwatch` <decl type="(watcherID: number): void" method />

Cancel a listener on the key named `key` in the storage. The parameter `watcherID` is the `wtacher ID` returned when the [`watch()`](#watch) method creates a watcher.


============================================================
FILE_PATH: src/transl/EN/api/system-fetch.md

# Data request fetch

## Import module

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

Initiate an asynchronous network data request. The functions of each field of the `options` parameter are:
- `url`: The URL of the website to be accessed.
- `method`: supports `'GET'`, `'POST'` and `'PUT'`, the default is `'GET'`.
- `header`: an object containing HTTP request header information, the key and value are strings. Typical HTTP header fields can be `Authorization`, `Content-Type`, etc.
- `params`: The parameters of the request, which will set all its properties to the URL part of the request.
- `data`: The body part of the HTTP POST request.
- `responseType`: The response data type in the HTTP request. The default is `'text'`, which can have the following values.
  - `'text'`: The response returns text data, that is, the `data` attribute of the returned data is of type `string`.
  - `'json'`: The response returns JSON data, and the returned `data` attribute will parse the JSON data into the corresponding JavaScript value.
  - `arraybuffer`: The response returns binary data, that is, the returned data is stored in an `ArrayBuffer` object.
- `timeout`: request response timeout, in milliseconds, the default value is $6000 \rm ms$.

#### `data` parameter

`data` is the body of the request and is only used in POST requests. It is usually of three types: string, `ArrayBuffer` object or JSON object. When `data` is a string or an `ArrayBuffer` object, the body of the request will be text or binary data respectively. When the body is a JSON object, it is serialized into text form. The format of the serialization is determined by the `Content-Type` field of the request method (`method` parameter):
- When `Content-Type` is `application/json`, serialize the `data` parameter object into a JSON string as the request body;
- Serialize the `data` parameter object to the format of `application/x-www-form-urlencoded` in other cases.

::: warning
Many HTTP APIs use the POST request body in JSON format. Please note that the `Content-Type` of the request header must be correctly set to `application/json`. Please refer to this [example](#post-request-json-body) for details.
:::

#### Return value

Returns a `Promise` object whose properties are as follows:
- [`code`](#code-response code) is the server response code. The response code for a successful request is generally `200`.
- `header` is the response header of the server.
- `data` is the return value of the request data, and the specific content is determined by the `options.responseType` parameter.

When the request fails, the returned `Promise` object will be rejected.

## Instructions for use

### `code` response code

The response code returned by the server means:
- `200`: indicates that the request is successful;
- `1002`: Parameter verification error;
- `1005`: The input parameters are incomplete;
- `5000`: Request failed, response error;
- `5001`: Failed to read data buffer;
- `5002`: Request failed, response error;
- Others: Other HTTP/HTTPS response codes, such as `404`, etc.

When the response code returned by [`fetch`](#fetch) is `200`, it means that the network request is successful, and if it is other values, it means that there is an error in the request.

### Notes

## Example

### GET request

Here is a basic GET request example:

``` js
const res = await fetch.fetch({
  url: 'http://www.rt-thread.com/service/rt-thread.txt',
  method: 'GET', // Since the default mode is GET, method is optional at this time
  responseType: 'text'
})
console.log(`the status code of the response: ${res.code}`)
console.log(`the data of the response: ${res.data}`)
```

### POST request

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

### POST request (JSON Body)


============================================================
FILE_PATH: src/transl/EN/api/system-file.md

# File system operations

This module provides a Promise-style file system operation API. Compared with callback style, Promise style can avoid callback hell and reduce code complexity.

::: warning
Since the callback file API is prone to pitfalls in timing, concurrency and error handling, it is strongly recommended to use [Promise/`await` API](./README.md#Quick Application Asynchronous Interface); for detailed suggestions, please refer to [Common Traps and Suggestions](#Common Traps and Suggestions).

The APIs in `@system.file` are all [asynchronous file operations](#asynchronous file operations), which are essentially different from synchronous IO access. Be sure to understand the basic concepts of asynchronous programming and be familiar with the use of Promise and `async/await`.
:::

## Import module

``` js
import file from '@system.file'
```

## Instructions for use

### Error code

The error code returned means:
- `202`: Parameter error;
- `300`: IO operation failed;
- `400`: Insufficient permissions;

## Interface definition

### `readText`
<decl method><pre>
(params: {
  uri: string
}): Promise&lt;string>
</pre></decl>

Read the contents of a text file. `params` parameter field description:
- `uri`: URI of the file to be read.

### `writeText`
<decl method><pre>
(params: {
  uri: string,
  text: string,
  append?: boolean
}): Promise&lt;void>
</pre></decl>

Writes text to a file, or creates a new file if it does not exist. This function also automatically creates the parent directory. `params` parameter field:
- `uri`: URI of the file to be written.
- `text`: The text content to be written to the file.
- `append`: The value is `true` to append data to the end of the file, the value is `false` to overwrite the original content. Default `false`.

### `read`
<decl method><pre>
(params: {
  uri: string,
  position?: number,
  length?: number
}): Promise&lt;ArrayBuffer>
</pre></decl>

Read the contents of the file into an `ArrayBuffer` object. `params` parameter field:
- `uri`: URI of the file to be read.
- `position`: the offset of the file reading position, the default is $0$.
- `length`: The number of bytes expected to be read. If not specified, it will be read to the end of the file.

### `write`
<decl method><pre>
(params: {
  uri: string,
  data: ArrayBuffer,
  position?: number,
  append?: boolean
}): Promise&lt;void>
</pre></decl>

Writes the bytes in the `ArrayBuffer` to a file, or creates a new file if it does not exist. This function also automatically creates the parent directory.

`params` parameter field description:
- `uri`: URI of the file to be written.
- `data`: data to be written.
- `position`: the offset of the file writing position, default is $0$.
- `append`: A value of `true` will append the data to the end of the file and ignore the `position` parameter.

### `copy`
<decl method><pre>
(params: {
  srcUri: string,
  dstUri: string
}): Promise&lt;void>
</pre></decl>

Copy the source file to the specified location and the target directory will be automatically created. `params` parameter field:
- `srcUri`: URI of the source file.
- `dstUri`: URI of the target file.

### `rename`
<decl method><pre>
(params: {
  oldUri: string,
  newUri: string
}): Promise&lt;void>
</pre></decl>

Renaming a file or directory will automatically create the target directory. `params` parameter field:
- `oldUri`: URI of the file or directory before renaming.
- `newUri`: URI after renaming.

### `list`
<decl method><pre>
(params: {
  uri: string,
}): Promise&lt;Array>
</pre></decl>

List all items (files or directories) in the specified directory. `params` parameter field:
- `uri`: Directory URI with enumeration. Files in the application resource package do not support enumeration.

The parameter of `Promise` is an array containing file information, in the form
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
You cannot enumerate files in the application resource package, so `await file.list({ uri: "/assets/images" })` and other methods that directly use [path](/framework/application/resource.md#uri-and path) are invalid. In fact, various [`internal`](/framework/application/resource.md#internal) URI protocols should be used.
:::

### `access`
<decl method><pre>
(params: {
  uri: string
}): Promise&lt;boolean>
</pre></decl>

Check if a file exists. `params` parameter field:
- `uri`: URI of the file to be detected.

### `mkdir`
<decl method><pre>
(params: {
  uri: string,
  recursive?: boolean
}): Promise&lt;void>
</pre></decl>

Create a directory. `params` parameter field:
- `uri`: URI of the directory to be created.
- `recursive`: Whether to create recursively (if the parent directory does not exist, create the parent directory first), the default is `false`.

### `remove`
<decl method><pre>
(params: {
  uri: string,
  recursive?: boolean
}): Promise&lt;void>
</pre></decl>

Delete a directory or file. `params` parameter field:
- `uri`: URI of the directory to be created.
- `recursive`: Whether to delete recursively, the default is `false`. Without recursive deletion, only files or empty directories can be deleted.

### `stat`
<decl method><pre>
(options: {
  uri: string
}): Promise&lt;{size: number}>
</pre></decl>

Get the attribute information of the file. Each field of the `options` parameter is described as follows:
- `uri`: the file URI of the attribute to be obtained.

`stat()` returns an object asynchronously containing the following file attributes:
- `size`: The size of the file, in bytes.

## Common pitfalls and suggestions

The following examples are all based on the typical problems of "callback-style" writing, showing why it is easily invalid or difficult to maintain in file IO, and provide equivalent rewriting of Promise/`await`.

### Asynchronous file operations

All APIs in the `@system.file` module are **asynchronous operations**. This means that when you call a file operation function, the function returns immediately without waiting for the actual I/O operation to complete. The read and write operations of the file will be performed in the background, and you will be notified of the result through Promise after the operation is completed.

:::danger A must-read for newbies
If you are new to asynchronous programming, be sure to read this section carefully. **Ignoring the return value of an asynchronous operation** or **Not waiting for a Promise to complete** can lead to serious program errors that may not manifest in the simulator, but can result in data loss or program errors on a real device.
:::

#### What is an asynchronous operation?

In synchronous programming, code is executed sequentially, and each line of code is executed before the next line is executed:

```js
// Synchronous code example (pseudocode, file API does not provide a synchronous version): blocking waiting for file reading
const text = file.readTextSync({ uri: 'internal://files/data.txt' });
console.log(text); // The file content will definitely be output
console.log('Reading completed');
```

But in asynchronous programming, I/O operations do not block code execution. When you call an asynchronous function, it returns a Promise object immediately, and the actual file operations occur in the background:

```js
// Error: Ignore Promise, do not wait for operation to complete (call returns immediately)
file.readText({ uri: 'internal://files/data.txt' });
console.log('This line of code will be executed immediately, and the file may not be finished reading at this time!');

// Correct: use await to wait for the operation to complete
const text = await file.readText({ uri: 'internal://files/data.txt' });
console.log(text); // At this point the file has been read and can be used safely
console.log('Reading completed');
```

#### Why must we use await?

Not using `await` to wait for an asynchronous operation to complete can lead to the following serious problems.

Data is used before it is ready:
```js
// Error example: ignore return value
function loadConfig() {
  let config = null;
  file.readText({ uri: 'internal://files/config.json' })
    .then(text => config = JSON.parse(text)); // This callback function will be executed at some point in the future
  // Here config is still null because the file reading has not been completed yet!
  console.log(config.theme); // Error: Trying to access null.theme will crash
  return config; // return null
}

// Correct example: wait for data to be ready
async function loadConfig() {
  const text = await file.readText({ uri: 'internal://files/config.json' });
  const config = JSON.parse(text);
  console.log(config.theme); // Correct: the file has been read and is safe to access
  return config; // Return the actual configuration object
}
```

The order of operations is confusing:
```js
// Error example: Not waiting for write to complete
async function saveAndLoad() {
  //Write new data, but don't wait for completion
  file.writeText({ uri: 'internal://files/score.txt', text: '100' });

  // Read immediately. The writing may not be completed at this time, and the old data may be read!
  const score = await file.readText({ uri: 'internal://files/score.txt' });
  console.log(score); // Might output the old value instead of '100'
}

// Correct example: wait for writing to complete before reading
async function saveAndLoad() {
  // Use await to wait for writing to complete
  await file.writeText({ uri: 'internal://files/score.txt', text: '100' });

  // Now read, make sure you read the data just written
  const score = await file.readText({ uri: 'internal://files/score.txt' });
  console.log(score); // Output '100'
}
```

Resource contention and data corruption:

```js
//Error example: multiple concurrent writes to the same file
async function appendLog(message) {
  const log = await file.readText({ uri: 'internal://files/log.txt' });
  // No need to wait for writing to complete, continue execution
  file.writeText({ uri: 'internal://files/log.txt', text: log + message + '\n' });
}

// Concurrent calls: no await appendLog
appendLog('Event A'); // Read -> Write A
appendLog('Event B'); // Read -> Write B
// Result: Two reads may read the same old content, and the later write will overwrite the previous one, causing 'event A' to be lost

// Correct example: wait for each write to complete
async function appendLog(message) {
  const log = await file.readText({ uri: 'internal://files/log.txt' });
  await file.writeText({ uri: 'internal://files/log.txt', text: log + message + '\n' });
}

// serial call
await appendLog('Event A'); // Complete read -> write -> complete
await appendLog('Event B'); // Complete read -> write -> complete
// Result: Both events were logged correctly
```

#### Emulator trap

::: warning The simulator cannot expose all asynchronous issues
In a development simulator, file operations are almost instantaneous due to the extremely fast I/O speed of the computer. Therefore, code may appear to "just work" in the simulator even if it does not use `await` correctly.
:::

File system I/O on real embedded devices has the following limitations:
- The read and write speed of Flash memory is slow;
- The file system cache capability is weak, and reading and writing files usually directly accesses the storage medium;
- System resources are limited and I/O operations will be queued and delayed.

Code that does not use `await` will almost certainly break on a real device! Don't ignore asynchronous programming conventions just because the simulator tests pass.

#### Rules for correct use of async/await

1. Any function calling the file API should be declared as `async`:
   ```js
   async function saveData(data) {
     await file.writeText({ uri: 'internal://files/data.txt', text: data });
   }
   ```
2. Add the `await` keyword before all file operations:
   ```js
   const content = await file.readText({ uri: 'internal://files/data.txt' });
   ```
3. Use `try/catch` to handle possible errors:
   ```js
   try {
     await file.writeText({ uri: 'internal://files/data.txt', text: 'hello' });
   } catch (err) {
     console.error('Writing failed:', err);
   }
   ```
4. Operations that need to be performed sequentially must `await` in order:
   ```js
   // Correct: write first, then read and verify
   await file.writeText({ uri: 'internal://files/data.txt', text: 'test' });
   const verify = await file.readText({ uri: 'internal://files/data.txt' });
   console.log(verify === 'test' ? 'Verification successful' : 'Verification failed');
   ```
5. Irrelevant operations can be executed in parallel, but wait for all to complete:
   ```js
   // Correct: read multiple files in parallel, but wait for them all to complete
   const [file1, file2, file3] = await Promise.all([
     file.readText({ uri: 'internal://files/a.txt' }),
     file.readText({ uri: 'internal://files/b.txt' }),
     file.readText({ uri: 'internal://files/c.txt' })
   ]);
   ```

#### Complete example: User configuration management

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
      //The file does not exist or has a wrong format, return to the default configuration
      console.warn('Failed to load configuration, use default value:', err.message);
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
      throw err; // Rethrow to let the caller know the save failed
    }
  }

  async update(changes) {
    // Read -> Modify -> Save the complete process
    const config = await this.load();
    Object.assign(config, changes);
    await this.save(config);
    return config;
  }
}

// Usage example
async function main() {
  const manager = new ConfigManager();
  //Load configuration
  const config = await manager.load();
  console.log('Current theme:', config.theme);
  //Update configuration
  await manager.update({ theme: 'light' });
  console.log('Theme has been updated');
}

// Note: main itself is also asynchronous and needs to be called correctly
main().catch(err => {
  console.error('Program execution error:', err);
});
```

#### Summary

- All `@system.file` APIs are asynchronous and must use `await` to wait for completion.
- Not using `await` can lead to serious problems, such as unprepared data, out-of-order operations, lost errors, and data corruption.
- Passing the simulator test does not mean that the code is correct. I/O on the real device is slower and problems will be exposed.
- Using `async/await` + `try/catch` is the correct and most concise way of writing.
- Never ignore the return value of a Promise.

### Callback trap

#### Callback order illusion and race coverage

This type of scenario involves a sequence of operations in which a set of files are read-modified-written. Here is the code in question using callback parameters to trigger the callback style:
```js
// Expect +1 to count file, but two concurrent calls may overwrite each other
function increment(uri, done) {
  file.readText({
    uri,
    success(text) {
      const n = Number(text || '0') + 1;
      console.log(`read ${text}, write ${n}`);
      // Nested file writing operation in readText() success callback
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

//Create the counter file first, and then trigger it twice concurrently +1
file.writeText({
  uri: 'internal://files/counter',
  text: '0',
  success() {
    //Trigger increment twice concurrently, but without any synchronization
    increment('internal://files/counter');
    increment('internal://files/counter');
  }
})
```
After running the script, you may only see two `read 0, write 1` logs, and the final `counter` file content is `1` instead of the expected `2`. The failure mechanism is: both reads read the same old value, and the later write overwrites the first write, resulting in a result of only +1.

::: note
The above script looks very complicated, and it is difficult to pass the `done` callback function correctly, which can easily lead to incorrect implementation. In fact, after rewriting it using `async/await`, the code becomes very concise and easy to understand.
:::

A complex trick is to use mutual exclusion + serialization technology, which can completely retain the original concurrency `increment` semantics and ensure the atomicity of the entire read file + increment count operation:
```js
// Mutually exclusive execution by key based on Promise chain
const lock = new Map();

/**
 * Execute asynchronous tasks for the same key serially. This is a utility function.
 * @param {string} key
 * @param {() => Promise<any>} fn
 * @returns {Promise<any>} returns the result of fn
 */
function withLock(key, fn) {
  // Get the "tail" before the key (if not, use the completed Promise)
  const prev = lock.get(key) || Promise.resolve();
  // Even if prev fails, the subsequent queue must continue, so first .catch(() => {})
  const p = prev.catch(() => {}).then(async () => {
    try {
      return await fn(); // The real task is only executed when it is its turn
    } finally {
      // If you are still the current tail, it means that no new tasks have come in and you can clean it up.
      if (lock.get(key) === p) lock.delete(key);
    }
  });
  lock.set(key, p); // Hang the new tail
  return p;
}

// Now, the actual IO inside the increment is serialized by withLock:
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
  // Trigger increment twice concurrently without any synchronization
  increment('internal://files/counter');
  increment('internal://files/counter');
});
```
After running this script, the content of the `counter` file must be `2`, and the log sequence must be `read 0, write 1` → `read 1, write 2`.

But such code looks very complicated. The simplest way is to call `await increment()` directly (shown as `await` infection):
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

#### Callback levels and resource leaks

The following example shows resource leaks and logic errors caused by multiple levels of nesting and too many branches in callback writing:

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

Because the callback nesting level is too deep, `stopBusyIndicator()` and `cb()` are prone to omission or misuse:
- Missing cleanup logic, causing the "busy indicator" to never stop, or the caller never getting a callback;
- The cleanup logic was called prematurely, causing the caller to mistakenly believe that the write was completed.

Recommended writing method (structured cleaning):

```js
async function exportReport(uri) {
  startBusyIndicator();
  try {
    const t = await file.readText({ uri });
    const out = await transform(t);
    await file.writeText({ uri: `${uri}.bak`, text: out });
  } finally {
    stopBusyIndicator(); // Always called after file IO is completed (or abnormal)
  }
}
```

#### Mixing await and callback leads to style switching (await fails)

Any callback handler function will not return a Promise object, making `await` wait invalid:

```js
// Because the complete callback is passed in, this call will enable the callback style and will not return a Promise
await file.writeText({
  uri: 'internal://files/a.txt',
  text: 'x',
  complete() {}, // Do not pass in the success/fail/complete parameter field
});
//The above line will not actually wait for the writing to complete, and subsequent code may be executed in advance
```

Recommended writing method:

```js
// Do not pass in success/fail/complete when using await
await file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
```

### Best Practices

#### Clear order and error handling

```js
import file from '@system.file'

export async function updateConfig(uri, patch) {
  try {
    const text = await file.readText({ uri });
    const json = JSON.parse(text || '{}');
    Object.assign(json, patch);
    await file.writeText({ uri, text: JSON.stringify(json, null, 2) });
  } catch (err) {
    // Handle/record errors uniformly, don't swallow them
    console.error('updateConfig failed:', uri, err);
    throw err;
  }
}
```

The key point is to use `await` to clarify the serial timing; use `try/catch` to ensure that errors are sensed and thrown up. If the error is not handled at all, the runtime will log the exception and interrupt the entire call chain.

#### Avoid TOCTTOU (check-use race conditions)

Don't do `access()` first and then `write*()` and then rely on the state between the two to remain unchanged. For example this code:

```js
file.access({
  uri: 'internal://files/a.txt',
  success(exists) {
    if (exists) {
      file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
    } else {
      // If the file does not exist, mkdir first and then write the file
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

The recommended way to write is to directly try to write, and the parent directory will be automatically created when running:
```js
async function safeWriteText(uri, text) {
  try {
    await file.writeText({ uri, text });
  } catch (e) {
    // Errors should be handled here and there is no need to write files after mkdir
  }
}
```

#### Half-write and crash interrupt

On MCU devices, system exceptions are usually directly reset and the application will not continue executing in a "semi-crash" state. Even if the app is killed, already committed file writes will not be interrupted (but may not be executed at all), so you generally don't need to worry about the "half-written file" problem:
```js
// Direct overwrite, which may leave half-written files in case of power interruption/system crash
file.writeText({ uri: '/data/config.json', text: bigJson });
```

For critical configuration file updates, you can use the "temporary file + same directory rename" mode to enhance stability:
```js
async function atomicWriteText(uri, text) {
  const tmp = `${uri}.tmp`;
  await file.writeText({ uri: tmp, text });
  await file.rename({ oldUri: tmp, newUri: uri });
}
```


============================================================
FILE_PATH: src/transl/EN/api/system-geolocation.md

# location

## Import module

```js
import geolocation from '@system.geolocation';
```

Developers need to declare the application's access permissions to `watch.permission.LOCATION` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

## Interface definition

### `getLocation`
<decl method><pre>
(options: {
  mode?: string
  timeout?: number
}): Promise&lt;Location>
</pre></decl>

Get the longitude and latitude of the current location once and return an asynchronous [location information](#location).

`options` parameter description
- `mode`: declare the positioning accuracy, `fine` is precise positioning, `coarse` is fuzzy positioning, the default value is `coarse`
- `timeout`: positioning timeout, unit is `ms`, default is 30000

### `subscribe` <decl type="(callback: (location: Location) => void): number" method/>

Listen for location changes. The parameter `location` of `callback` is the current [location information](#location). The ID returned by this method can be used to unsubscribe using the [`unsubscribe()`](#unsubscribe) method.

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancel listening for location changes.

## Type definition

### `Location`

Location information data used to represent positioning.

```ts
type Location = {
  code: number; // Positioning status code, indicating whether the current location information is valid
  msg: string; // Positioning error message
  data: {
    //Data of location information
    longitude: number; // latitude value
    latitude: number; // longitude value
    coordType: string; //Coordinate system type, such as 'WGS84', 'GCJ02', etc.
  };
};
```

The positioning status code of the `code` field is as follows:

- `200`: The current positioning information is valid;
- `1002`: Currently not connected to the mobile phone Bluetooth network
- `1300`: The mobile phone cannot obtain location services
- `1301`: Location service is not enabled on the phone
- `1302`: The mobile application does not grant location permission
- `1399`: unknown error


============================================================
FILE_PATH: src/transl/EN/api/system-interconnect.md

# Device interconnection

## Import module

``` ts
import interconnect from '@system.interconnect'
```

## Interface definition

### `instance` <decl type="(options: {package: string, fingerprint: string}): Connect" method/>

Create a [`Connect`](#connect-interface) instance

```js
const connect = interconnect.instance({
  package: "com.xxxx.xxx",
  fingerprint: "xxxxx"
})
```

- package: the package name of the mobile application
- fingerprint: fingerprint information, which needs to be consistent with the fingerprint information passed in when the mobile application creates a connection.

## `Connect` interface

### `onopen` <decl type="?: () => void" set />

Used to specify a callback when the connection is opened

```js
connect.onopen = () => {
  console.info("onopen")
}
```

### `onclose` <decl type="?: () => void" set />

Used to specify a callback when the connection is closed

```js
connect.onclose = () => {
  console.info("onclose")
}
```

### `onerror` <decl type="?: () => void" set />

Used to specify a callback after a connection failure

```js
connect.onerror = (data: any) => {
  console.info("onerror", data)
}
```

### `onmessage` <decl type="?: () => " set />

Used to specify the callback for receiving data from the mobile app

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

Send data to mobile app

```js
connect.send({
  data: {
    name: "zhangsan"
  }
})
```


============================================================
FILE_PATH: src/transl/EN/api/system-internal.md

# Internal interface

The `system.internal` module provides some internal interfaces for use by the system. This module can only be used in launcher applications.

## Import module

``` js
import internal from '@system.internal'
```

## API

### `globalComponent` <decl type="(name: string, uri: string): void" method />

Register a [global component](/framework/component/README.md#global component). Global components can be introduced in all applications. The parameter `name` is the name of the global component, and `uri` is the path or URI of the global component UX file relative to the current source file. For example
``` js
internal.globalComponent('TopBar', '/global/TopBar.ux')
```
You can then use `<import name="TopBar" />` to reference the global component `TopBar` in all applications.

The `globalComponent()` method is best executed in the `app.js` execution phase of the launcher application, so that global component information can be registered before any interface is loaded.

### `setDefaultKeyHandler` <decl type="(handler: (event: KeyEvent) => void): void" method />

Register the system's default key handler. The parameter `handler` is a callback function. The `KeyEvent` type prototype is:
``` ts
interface KeyEvent {
  type: 'keydown' | 'keyup', // Type of key event
  key: string, // key name
  timestamp: number, // timestamp of key event reporting, unit is milliseconds
}
```
The default key handler can only be registered once, because multiple registrations will overwrite previous operations.


============================================================
FILE_PATH: src/transl/EN/api/system-launch.md

# Application jump

## Import module

``` js
import launch from '@system.launch'
```

## Interface definition

### `launch` <decl type="(app: string): Promise<bool>" method/>

Start the specified application and switch to the foreground. `app` is an installed application ID string. The returned Promise indicates whether the application is loaded successfully.

### `inactive` <decl type="(app?: string): Promise<void>" method/>

Switch the app to the background. `app` is the ID of a started application. If no parameters are specified, the current application will be switched to the background. Only foreground applications can be switched to the background.

### `exit` <decl type="(app?: string): Promise<void>" method />

Quit an application. The parameter `app` is the ID of a started application. If no parameter is specified, the current application will be exited.

### `getRunning` <decl type="(): string[]" method />

Get a list of running application package names, including those in the background.


============================================================
FILE_PATH: src/transl/EN/api/system-media.md

# multimedia

## Import module

``` ts
import media from '@system.media'
```

## Interface definition

### `createAudioPlayer` <decl type="(): AudioPlayer" method />

Create an [`AudioPlayer`](#audioplayer-object) object.

### `createAudioRecord` <decl type="(): AudioRecorder" method />

Create an [`AudioRecorder`](#audiorecorder-object) object.

Developers need to declare the application's access permissions to `watch.permission.RECORD` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

### `setVolume` <decl type="(volume: number): void" method />

Set the system media volume. The parameter `volume` is a volume value between $[0.0, 1.0]$. This property is used to control the system media volume. The specific function depends on the platform implementation. To adjust the volume, the `volume` property of the `AudioPlayer` object should be used first.

### `getVolume` <decl type="(): number" method />

Get the system media volume, the result is a volume value between $[0.0, 1.0]$. This attribute is used to obtain the system media volume. The specific function depends on the platform implementation. To obtain the volume, the `volume` attribute of the `AudioPlayer` object should be used first.

## `AudioPlayer` object

::: details type signature
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

Set or read the url that needs to play audio. Supports [local resource path](/framework/application/resource.md#uri-and path) and network resource path using http and https protocols (for example: `https://www.rt-thread.com/service/test/001.mp3`). Here's a simple example of setting src and then starting playback:

```ts
import media from '@system.media'
//Create audio player
let player = media.createAudioPlayer()
//Set the audio url to be played
player.src = 'https://www.rt-thread.com/service/test/001.mp3'
// Start playing audio
player.play()
```

### `name` <decl type="string" set get />

The name of the player object. If not set, it defaults to the name of the application that created the player. It should be noted that the name of the player object is not globally unique, and the name cannot be used to identify the player object.

### `icon` <decl type="string" set get />

The player object's icon url. Support [local resource path](/framework/application/resource.md#uri-and path)

### `mode` <decl type="string" set get />

playback mode. The function corresponding to this attribute should be implemented by the player application. The player object does not process it by default and only provides this attribute.

- `sequential`: play sequentially
- `random`: play randomly
- `singleloop`: single loop
- `listloop`: list loop

### `status` <decl type="string" get />

Read the current player status

- `play`: playing status
- `pause`: Pause playback state
- `stop`: Stop playing status
- `ended`: playback end status
- `error`: playback error status

### `duration` <decl type="number" get />

Total audio duration, unit: seconds

### `position` <decl type="number" set get />

The time position of the current audio playback, unit: seconds

### `openSystemNotification` <decl type="bool" set get />

Whether to turn on system notifications, not turned on by default. After it is turned on, this player object can be queried by [Audio Player Manager](/framework/application/system-audioPlayerManager.md#Audio Player Manager).

### `songAttribute` <decl type="songAttribute" set get />

Song property object

::: details type signature
```ts
type songAttribute = {
  title: string; // The name of the song
  artist: string; //The name of the performer, which can be an individual or a band
  album: string; // The name of the album to which the song belongs
  year: string; // The year the song was released
  genre: string; // The type of song, such as pop, rock, classical, etc.
  track: string; // The number of the current song in the album, for example: "1/12" means the 1st song, a total of 12 songs
  coverArt: string; // URL of the song cover image
  lyrics: string; // URL of lyrics text
  comments: string; // Additional information, such as copyright remarks, etc.
}
```
:::

The songAttribute object is a Proxy object like the AudioPlayer object. It cannot be serialized and deserialized using JSON, and cannot be referenced in the responsive framework. Here's a simple usage example:

```ts
//Set the name of the song
this.player.songAttribute.title = "Unknown"
//Set the singer of the song
this.player.songAttribute.artist = "Unknown"
// Check the name of the song
console.dir(this.player.songAttribute.title)
```

### `volume` <decl type="number" set get />

The volume of the current player, range: [0.0, 1.0]

### `nextAvailable` <decl type="bool" set get />

Set or query whether the next song can be switched

### `prevAvailable` <decl type="bool" set get />

Set or query whether the previous song can be switched

### `play` <decl type="(): void" method />

Start playing the audio specified in the src attribute

- If the src attribute is not set before calling this method, playback will fail and the onerror event will be triggered;
- This method is a synchronous interface. After executing this interface, you need to wait for the onplay event or onerror event to determine whether the playback is successful or failed. Before the event is triggered, other operations performed will be ignored;

The following is a simple example of calling the play() interface:

```ts
import media from '@system.media'
//Create audio player
let player = media.createAudioPlayer()
//Set the audio url to be played
player.src = 'https://www.rt-thread.com/service/test/001.mp3'
//Set onplay event
player.onplay = () => { console.dir("Start playing") }
//Set onerror event
player.onerror = () => { console.dir("Playback error") }
// Start playing audio
player.play()
```

### `pause` <decl type="(): void" method />

Pause the current audio

- This method is a synchronous interface. After executing this interface, you need to wait for the onpause event or onerror event to determine whether the pause is successful or failed. Before the event is triggered, other operations performed will be ignored;

### `stop` <decl type="(): void" method />

Stop audio playback and replay the audio via play

- This method is a synchronous interface. After executing this interface, you need to wait for the onstop event or onerror event to determine whether the stop is successful or failed. Before the event is triggered, other operations performed will be ignored;

### `release` <decl type="(): void" method />

Release audio resources

- Executing this interface will stop playing the current audio. You need to wait for the onstop event or onerror event to determine whether the stop is successful or failed. Before the event is triggered, other operations performed will be ignored;

### `next` <decl type="(): void" method />

Notify the player application to play the next song. After executing this interface, the onnext event will be triggered to notify the player application that listens to this event, and the player application will execute the logic of song switching.

### `previous` <decl type="(): void" method />

Notify the player application to play the next song. After executing this interface, the onprevious event will be triggered to notify the player application that listens to this event, and the player application will execute the song switching logic.

### `requestFocus` <decl type="({acquireType: string，volumeType: string}): void" method />

Request audio focus. After executing this interface, the underlying layer will be notified to request or release the audio focus, and the underlying layer will control the switching and interruption logic of different types of audio.

The `acquireType` parameter indicates the request type:
- `gain`: Request audio focus
- `loss`: Release audio focus

The `volumeType` parameter indicates the audio type:
- `system`: system prompt
- `media`: media music
- `tts`: voice broadcast

The following example demonstrates how the `requestFocus` function requests audio focus:
``` ts
import media from '@system.media'
//Create audio player
let player = media.createAudioPlayer()
// Get the audio focus of the media music type
player.requestFocus({ volumeType: 'media', acquireType: 'gain' });
```

### `releaseFocus` <decl type="(): void" method />

Release audio focus. After executing this interface, the bottom layer will be notified to release the audio focus, and the bottom layer will control the switching and interruption logic of different types of audio.

### `onplay` <decl type="?: () => void" set />

Callback event after audio play is successful

### `onpause` <decl type="?: () => void" set />

Callback event after audio pause is successful

### `onstop` <decl type="?: () => void" set />

Callback event after audio stop is successful

### `onended` <decl type="?: () => void" set />

Callback event after audio playback ends

### `onerror` <decl type="?: () => void" set />

Execute callback events for interface errors such as `play` `pause` `stop` `position` and other interfaces. When an error occurs, the corresponding onplay and other events will not be triggered.

### `ontimeupdate` <decl type="?: () => void" set />

A callback event that will be triggered when the position property is updated. This event will only be triggered when the application is in the foreground, and will stop dispatching when the application is in the background.

### `oninterrupt` <decl type="?: (action: {interruptHint: number}) => void" set />

The callback function when an audio interruption event occurs. When the current audio is snatched by audio of the same audio type or other audio types, it will be notified that it is temporarily interrupted or completely interrupted.

The `interruptHint` of the `action` parameter indicates the type of interrupt event:
- `1`: brief interruption (can be automatically restored, such as: music is interrupted)
- `2`: Completely interrupted (cannot be automatically restored, such as: NetEase Cloud was interrupted by Himalaya)

The following example demonstrates how to register an `oninterrupt` callback function, which is called when an event occurs:
``` js
player.oninterrupt = (action) => {
  console.log(action.interruptHint)
}
```

### `onnext` <decl type="?: () => void" set />

Callback event when the next song needs to be played

### `onprevious` <decl type="?: () => void" set />

Callback event when the previous song needs to be played

### `onrequestplay` <decl type="?: () => void" set />

When the bottom layer needs to start playback, the callback event is triggered to notify the js application, and the js application executes the logic of starting playback.

### `onrequestpause` <decl type="?: () => void" set />

When the bottom layer needs to pause playback, the callback event is triggered to notify the js application, and the js application executes the logic of pausing playback.

### `onrequeststop` <decl type="?: () => void" set />

When the bottom layer needs to stop playing, the callback event is triggered to notify the js application, and the js application executes the logic of stopping the playback.

### `onsongattribute` <decl type="?: () => void" set />

Callback event when the song attribute object changes

### `onposition` <decl type="?: () => void" set />

Execute `position` to set the time and position of the current audio playback. The callback event is successful.

### `onrequestfocus` <decl type="?: () => void" set />

Callback event when requesting audio focus successfully

### `onreleasefocus` <decl type="?: () => void" set />

Callback event when audio focus is released successfully

### `onmodechanged` <decl type="?: () => void" set />

Callback event when playback mode changes

### `onvolumechange` <decl type="?: () => void" set />

Callback event when player volume changes


## `AudioRecorder` object

::: details type signature
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

Start recording audio. The functions of each field of the `options` parameter are:
- `uri`: URI of the recording file that needs to be stored, only supports the `internal` protocol, and the directory will be automatically created;
- `sample`: audio sampling rate, unit is $\rm Hz$, default is $8000$;
- `layout`: audio data bit depth, default is $16$;
- `channel`: number of audio channels, default is $1$;
- `bitrate`: Audio bitrate, the unit is $\rm kbps$, the default is $16$, the higher the bitrate, the better the sound quality but the larger the file.
- `codec`: audio encoding format, string type, if not filled in, a suitable code will be automatically matched according to the `format` parameter;
- `format`: audio encapsulation format, string type, if not filled in, a suitable encapsulation will be automatically matched based on the suffix name of the `uri` parameter;

The support relationships for commonly used recording formats, encoding formats and encapsulation formats are as follows (None in the table means that the corresponding parameters do not need to be filled in):

| Commonly used recording formats | codec (encoding format) | format (encapsulation format) |
  | -------------- | --------------- | ------------- |
  | pcm | None | None |
  | mp3 | mp3 | none |
  | opus | opus | none |
  | opus-ogg | opus | ogg |
  | silk | silk | none |

The following example code starts recording:

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
For more information on the `internal` URI protocol, please refer to the [Resource Access](/framework/application/resource.md) document.
:::

After the recording is completed, call the [stop()](#stop-1) method to end the recording.

### `read`
<decl method><pre>
(options: {
  callback: (buffer: ArrayBuffer) => void,
}): void
</pre></decl>

Read the recorded audio data (the data read each time is all available data so far from the end of the last read)

### `stop` <decl type="(): void" method />

Stop recording audio. After calling this interface, the audio file recorded by the [`start()`](#start) method (specified by the `uri` parameter) can be read by other modules.

### `release` <decl type="(): void" method />

Release recording audio resources

### `onstart` <decl type="?: () => void" set />

Callback event after recording start

### `onstop` <decl type="?: () => void" set />

Callback event after recording stop

### `onrelease` <decl type="?: () => void" set />

Callback event after recording release

### `onavailable` <decl type="(data: ArrayBuffer) => void" set />

Callback event generated when new data is generated after recording starts

### `onerror` <decl type="?: () => void" set />

The callback event when an error occurs in the `start`, `stop` or `release` event. When an error occurs, the corresponding onstart, etc. will not be triggered.

## Example

### Recording

The following code demonstrates the simplest example of recording 3 seconds of audio:
``` js
import media from "@system.media"

async function record() {
  //Create recording object
  let record = media.createAudioRecord()
  console.log('start record')
  //Only fill in the uri parameter, other parameters use default values
  await record.start({
    uri: 'internal://tmp/test.mp3'
  })
  setTimeout(() => {
    console.log('stop record')
    record.stop() // Stop recording after a delay of 3 seconds
  }, 3000)
}

record()
```

When the `record()` function is called, a recording object is created, then starts recording, and stops recording after 3 seconds. The recording will be recorded to the file `internal://tmp/test.mp3` and encoded in MP3 format.

This example only passes the `uri` parameter to the [`AudioPlayer.start()`](#start) method, and `sample`, `layout`, `channel` and `bitrate` all use the default configuration.

::: tip
When using the simulator, you can find the recording file in the application's data directory and play it. The corresponding file path of `internal://tmp/test.mp3` is `.glyphix-work/image/{device}/data/temp/{app-id}/test.mp3` where `{device}` and `{app-id}` are the device name and application name during simulation.
:::


============================================================
FILE_PATH: src/transl/EN/api/system-network.md

# Network status

## Import module

```js
import network from '@system.network';
```

## Interface definition

### `subscribe` <decl type="(callback: (status: NetworkState) => void): number" method/>

Monitor changes in network status. The parameter `status` of `callback` is the new [network state](#networkstate). The ID returned by this method can be used to unsubscribe using the [`unsubscribe()`](#unsubscribe) method.

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancel network status monitoring. `subscribeID` is the ID value returned by the [`subscribe()`](#subscribe) method.

### `getType` <decl type="(): Promise<NetworkState>" method/>

Get the current network status and return a [`NetworkState`](#networkstate) value.

## Type definition

### `NetworkState`

This object is used to represent the current network status. The type signature is as follows:

```ts
type NetworkState = {
  device: string; //The name of the network device
  type: string; // Type of network device
  linkUp: boolean; // Whether the network device has been opened
  online: boolean; // Whether the device is online (whether it can access the Internet)
};
```

You can usually use the `online` property of `NetworkState` to check whether the device can access the Internet.


============================================================
FILE_PATH: src/transl/EN/api/system-notification.md

# Message notification

## Import module

``` js
import notification from '@system.notification'
```

Developers need to declare their application's access permissions to `watch.permission.NOTIFICATION` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

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

Post a message notification. The functions of each field of the `options` parameter are:
- `icon`: the URI of the message icon;
- `id`: the unique id of the application notification;
- `contentType`: text type. 1: Ordinary text notification type. 2: Picture notification type; picture notification is not supported temporarily;
- `content`: used in conjunction with `contentType` to represent the text content of the notification;
  - When `contentType` is 1, it represents the body content of a normal text notification; object type, including the following fields:
    - `title`: ordinary text notification title; string type;
    - `text`: ordinary text notification content; string type;
- `deliveryTime`: notification sending time;
- `actionUri`: URI to jump to when clicking the notification.

### `remove`
<decl method><pre>
(options: {
  query:{
    id?: number
  }
}): void
</pre></decl>

Clear message notification. The `options` parameter contains the following fields:
- query: cleared query conditions,
  - id: Clear the message notification with the specified id. If no id is passed in, all message notifications will be cleared.


============================================================
FILE_PATH: src/transl/EN/api/system-package.md

# Package management

This module provides the installation and uninstallation functions of resource packages.

## Import module

``` js
import pkg from '@system.package'
```

Since `package` is a JavaScript keyword and cannot be used as a variable name, we can export the `"@system.package"` module to the `pkg` variable.

## Interface definition

### `install` <decl function type="(options: { src: string }): Promise<void>" />

Install an app or watch face package from the file system. The `src` attribute of the `options` parameter is the URI of the resource package file to be installed.

If the resource package is an application resource package, then after installing the resource package using `pkg.install({ src: 'package-uri' })` it can be launched by [`launch()`](system-launch.md#launch-launch-app) and the contents of the package can be accessed using the [`app`](/framework/application/resource.md#app) URI protocol.

`src` is the URI of the resource package file to be installed. The installed package must be a valid application or watch face package, that is, it must have a [`manifest.json`](/framework/application/manifest.md) file. The package name after installation is determined by [`manifest.package`](/framework/application/manifest.md#package).

After installation, you can use the [`prc`](/framework/application/resource.md#prc) protocol to access the resources in the resource package. For application resource packages, you can also use the `app` protocol.

If the package to be installed already exists, the upgrade operation will be performed. If the upgraded application is running, it will be exited first, and then you can call [`launch()`](system-launch.md#launch-launch-app) to start it again.

Installed packages can be removed by the [`remove()`](#remove) API.

### `remove`<decl type="(options: { package: string }): Promise<void>" function />

Remove resource packages installed by [`install()`](#install). The `package` attribute of the parameter `options` is the name of the resource package to be deleted, that is, the [`manifest.package`](/framework/application/manifest.md#package) field.

Before deleting the resource package, you should close related resources first, such as destroying related components and closing related pages. The `remove()` function will automatically close the application corresponding to the resource package (if it is an application resource package).

::: warning
Resource bundles must be removed using `remove()` rather than directly using the file system API, as the latter does not clear the resource cache and does not properly remove installation information.
:::

### `getInfo` <decl type="(query?: string | Query): Manifest | undefined" method/>

Get the manifest information of the application package. The optional parameter `query` can be a package name string or a more complex `Query` object:
``` ts
type Query = {
  package: string, // package name to be queried
  options?: ('dial' | 'widgets')[] // Optional query fields
}
```
If the package specified by the `package` field exists, `getInfo()` will return the `Manifest` information of the package, otherwise it will return `undefined`. When the `query` parameter is not specified, `getInfo()` will return the manifest information of the current application.

#### `Manifest` object

The returned `Manifest` object is basically a subset of [`manifest.json`](/framework/application/manifest.md):
``` ts
type Query = {
  type: 'app' | 'dial', // Package type, may be application or dial package
  name: string, // package name
  versionName: string, // version name
  versionCode: number, // version number
  icon?: string, // Application image path, this field only exists in application packages
  dial?: { // Optional field: dial information, only the dial package has this information
    component: string, //The path to the watch face component
    preview: string // Path to the watch face preview image
  },
  widgets?: { // Optional fields: widget and widget information
    name: string, //Pendant/widget name
    component: string, // widget/widget path
    preview: string // Preview image of widget/widget
  }[]
}
```
The `dial` and `widgets` of the `Manifest` object are optional fields, and their presence or absence is determined by the contents of `Query.options`. For example
``` js
pkg.getInfo({
  package: 'com.example.app',
  options: ['dial', 'widgets']
})
```
Will cause the resulting `Manifest` to contain the `dial` and `widgets` fields (however, application packages always do not contain the `dial` field).

When the `query` parameter is a string, it is equivalent to the `options` option being empty, that is
``` ts
pkg.getInfo('com.example.app')
pkg.getInfo({ package: 'com.example.app' })
```
The result is the same, in which case the returned `Manifest` object does not contain optional fields.

When the `query` parameter is not specified, the application information can be returned through `getInfo()`:
``` js
let manifest = pkg.getInfo()
console.log(manifest)
```

### `list` <decl function type="(type?: 'app' | 'dial'): string[]" />

Get a list of all installed apps or watch face package names.

### `countOf` <decl function type="(type?: 'app' | 'dial'): string[]" />

Get the number of installed apps or watch faces.


============================================================
FILE_PATH: src/transl/EN/api/system-path.md

# Path operations

This module provides an interface for path operations. Including path splicing, segmentation and simplification functions.

## Import module

``` js
import path from '@system.path'
```

## Interface definition

#### `path.basename` <decl type="(path: string, suffix?: string): string" method />

Returns the file name part of path `path`. The specified file name suffix can also be removed by specifying the `suffix` parameter. For example
``` js
path.basename('/foo/bar/baz.txt') // 'baz.txt'
path.basename('/foo/bar/baz.txt', '.txt') // 'baz'
```

#### `path.dirname` <decl type="(path:string): string" method />

Returns the path part of `path` (as opposed to `basename()`, which discards the filename part). For example
``` js
path.dirname('/foo/bar/baz') // '/foo/bar'
```

#### `path.extname` <decl type="(path: string): string" method />

Get the file suffix in `path`. For example
``` js
path.extname('table.json') // '.json'
path.extname('/images/icon.png') // '.png'
```

#### `path.isAbsolute` <decl type="(path: string): boolean" method />

Determine whether `path` is an absolute path. For example
``` js
path.isAbsolute('/foo/bar'); // true
path.isAbsolute('/baz/..');  // true
path.isAbsolute('qux/');     // false
path.isAbsolute('.');        // false
```

#### `path.join` <decl type="(...paths: string[]): string" method />

Splice and simplify multiple paths, for example
``` js
path.join('/foo', 'bar', 'baz/asdf', 'quux', '..') // '/foo/bar/baz/asdf'
```

#### `path.normalize` <decl type="(path: string): string" method />

Reduce path `path` to its simplest form, parsing `..` and `.` and removing redundant path separators `/`.

``` js
path.normalize('/foo///bar/.././/baz') // '/foo/baz'
```

#### `path.relative` <decl type="(from: string, to: string): string" method />

Computes the relative path from `from` to `to`.

``` js
path.relative('/data/orandea/test/aaa', '/data/orandea/impl/bbb') // '../../impl/bbb'
```


============================================================
FILE_PATH: src/transl/EN/api/system-prompt.md

# Pop-up window

## Import module

``` js
import prompt from '@system.prompt'
```

## Interface definition

#### `showToast`
<decl method><pre>
(options: {
  message: string,
  duration?: number,
  important?: boolean
}): void
</pre></decl>

Display a toast pop-up box. Toast is a text pop-up box placed on top of the interface. Only one instance of toast is displayed in the interface. If there are multiple toast contents, they will be queued and displayed in sequence.

Description of the `options` parameter field:
- `message`: requires realistic text.
- `duration`: the display duration of the toast, in ms. The toast will be automatically hidden after the timeout period is reached.
- `important`: Whether it is an important toast, the default is `false`. If set to `true`, allows this toast to pop up when the app is in the background.

The toast display style (font, color, etc.) is determined by the firmware and cannot be modified in the application. There is also a limit on how long a toast can be displayed, ranging from $200$ to $5000$ milliseconds.

#### `showPopup` <decl type="(options: { uri: string, params?: Object }): Promise<any>" method />

Display a floating page pop-up window. `options` parameter field description:
- `uri`: The name of the target page, which needs to be registered in `router` of `mainfest.json`.
- `params`: The data that needs to be passed when jumping. The attribute of the `params` parameter will replace the `data` attribute value of the target page.

A floating page is a system-level pop-up window (similar to a toast or a dialog box), but a floating page is a fully functional page with the highest customizability. Unlike ordinary pages, floating pages are displayed in the system's floating page stack instead of applying their own page stack. Therefore, APIs such as `router.back()` in the [Page Routing](api/system-router) mechanism cannot operate floating pages. If you want to close the floating page, you can use the [`router.close()`](system-router.md#close) method.

The display level of the pop-up window is higher than that of the application, so the floating page will be displayed on top of all application pages. All applications use the same floating page stack. The display level of floating pages is determined by the pop-up order, that is, the page that popped up earlier is at the top. The display level of the floating page is the same as the dialog box, lower than the toast.

Like `router.push()`, `showPopup()` also returns a Promise object, which will be honored and return a custom result after the floating page exits. Please refer to [`router.push()`](system-router.md#push) and [`router.close()`](system-router.md#close) for details.


============================================================
FILE_PATH: src/transl/EN/api/system-request.md

# Upload download request

## Import module

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

Download files through the HTTP/HTTPS protocol. The functions of each field of the `options` parameter are:
- `url`: the URL of the website to be accessed;
- `header`: an object containing HTTP request header information, the key and value are strings. Typical HTTP header fields can be `Authorization`, `Content-Type`, etc.;
- `filename`: URI that stores downloaded files, such as: `internal://files/download.txt`;
- `callback`: Download progress callback function. This function will be called multiple times during downloading. `progress` is the progress value of the download, ranging from $[0, 100]$.

The `download()` method returns a [`DownloadTask`](#downloadtask) object, which can be used to wait for the download to complete or control the download task.

::: warning
Please do not use the download progress to reach $100\%$ in the `callback` function as the trigger condition for the operation after the download is completed. For details, please refer to [Waiting for downloading to complete](#Waiting for downloading to complete).

The current implementation does not automatically parse the `filename` parameter attribute based on `url`. Please be sure to fill in `filename`.
:::

## type

### `DownloadTask`

`DownloadTask` is the return type of the `download` method, and its signature is:

``` ts
interface DownloadTask {
  complete: Promise<void>,
  cancel(): void
}
```

The `complete` property is a `Promise` object that can be used to wait for the download to complete. The `cancel()` method is used to cancel the ongoing download task. If the download has been completed, the `cancel()` method has no effect.

#### Wait for download to complete

Use `DownloadTask.complete` to wait for the download to complete. When the `Promise` is fulfilled, it will ensure that the file has been written, so it is safe to proceed to the next step. In contrast, when the download progress of `callback` reaches $100\%$, it does not mean that the file writing is completed. It is only suitable for UI progress display and other needs.

In actual use, considering that the download may fail, it is recommended to use the `try...catch` statement to handle download errors. The following examples will introduce usage.

## Example

Here is a simple example of downloading a file from the network:

``` js
request.download({
  url: "http://www.rt-thread.com/service/rt-thread.txt",
  filename: "internal://tmp/rt-thread.txt",
})
```

You can wait for the download to complete through the `complete` attribute of the `download()` method return value:
``` js
try {
  await request.download({
    url: "http://www.rt-thread.com/service/rt-thread.txt",
    filename: "internal://tmp/rt-thread.txt"
  }).complete // When complete is rejected, it means the download failed
  console.log('download finished.')
} catch (e) {
  console.error('download failed:', e)
}
```

The `try...catch` block here is used to catch exceptions when the download fails. This exception is actually an error thrown when `DownloadTask.complete` is rejected, so you should use `awiat` to wait for the `complete` attribute, otherwise the exception cannot be caught.


============================================================
FILE_PATH: src/transl/EN/api/system-router.md

# Page routing

## Import module

``` js
import router from '@system.router'
```

## Interface definition

### `push` <decl type="(options: {uri: string, params?: Object}): Promise<any>" method />

Jump to the specified page within the application. `options` parameter attribute description:
- `uri`: the name of the target page, which must be configured in `mainfest.json`;
- `params`: The data that needs to be passed when jumping. The attribute of the `params` parameter will replace the `data` attribute value of the target page.

`push()` returns a Promise object that will be honored and return a custom result after the target page exits. For example:
```js
const result = await router.push({ uri: 'PageName' })
console.log("the page 'PageName' was closed with the result:", result)
```
Where `result` is the page return value specified by the [`close()`](#close) method, which you can obtain through the above method.

::: warning
The return time of the page usually depends on user actions, so `await router.push()` may wait for a long time. If you do not need to obtain the return value of the page, it is not recommended to wait for the page to return through `await`.
:::

When the page is in `singleTask` launch mode, jumping to an already opened page is similar to [`back('<page-name>')`](#back), see [`launchMode`](/framework/application/manifest.md#launchmode) <version-badge since="0.8" />.

### `replace` <decl type="(options: {uri: string, params?: Object}): Promise<boolean>" method />

Jump to the specified page in the application and close the current page. `options` parameter attribute description:
- `uri`: the name of the target page, which must be configured in `mainfest.json`;
- `params`: The data that needs to be passed when jumping. The attribute of the `params` parameter will replace the `data` attribute value of the target page.

Like [`push()`](#push) and [`back()`](#back) , calling `replace()` always plays the standard page transition animation. Even if `replace()` is called **immediately** in the code, as long as the current page has entered the rendering stage, the user may still briefly see a frame of the current page before entering the target page. Therefore, `replace()` is more suitable for use in scenarios where "the current page itself is part of the user flow", rather than as a means of "silent redirection" or "complete hiding of the entry page".

If the current page is popped up through the [`push()`](#push) method, since the `replace()` method will replace the current page, this will cause the Promise object returned by [`push()`](#push) to be fulfilled.

::: tip
Do not use the [`push()`](#push) method to jump to a new page and immediately [`close()`](#close) the current page to replace the page. This will interrupt the interactive effect and even cause the screen to flicker. Please always use the `replace()` method to replace pages to ensure a smooth page transition experience.

In addition, if you want an entry page (such as the `router.entry` page configured in `manifest.json`, the privacy check page only for distribution, etc.) to be **not displayed at all** in some scenarios, do not call `replace()` inside the page in an attempt to "jump away immediately". For such requirements, you should use [Replace Default Page](#Replace Default Page) to directly `push()` the real first-screen page early in the application startup (such as `onCreate()` / `onRoute()`).
:::

`replace()` is often used in scenarios such as [Jump to the screen-opening interface](#Jump to the screen-opening interface).

When the page is in `singleTask` launch mode, jumping to an already opened page is similar to [`back('<page-name>')`](#back), see [`launchMode`](/framework/application/manifest.md#launchmode) <version-badge since="0.8" />.

### `back` <decl type="(name?: string): Promise<boolean>" method />

Return to the page named `name`. If `name` is empty or this parameter is not passed, `router.back()` will return to the previous page.

Calling the `back()` method will cause the Promise returned by the [`push()`](#push) method to pop up the relevant page to be fulfilled.

### `close` <decl type="(page: Component, result?: any): Promise<void>" method />

Close the specified page. `page` is the view-model object of a page. For example:
``` js
router.close(this.$page)
```

The `router.close()` method can close any page within the application. If the target page is at the top of the page stack, then `router.close()` and `router.back()` are equivalent. `router.close()` can also correctly close floating pages.

The optional parameter `result` is used to specify the return value of the page, that is, the result of the Promise returned by [`router.push()`](#push) or [`prompt.showPopup()`](system-prompt.md#showpopup) that pops up the page. Considering that there are many ways to exit the page (such as user sliding, `router.back()` method, etc.), you can explicitly call the `close()` method in the [`onDestroy()`](/framework/component/life-cycle.md#ondestroy) life cycle function of the page component to ensure that the page return value is passed:
```js
import router from '@system.router'

export default {
  // This is a component object...
  onDestroy() {
    router.close(this.$page, this.pageResult)
  },
  // Assume that a method will set the page return value
  someMethod() {
    this.pageResult = { message: 'some page result' }
  },
}
```

::: tip
When the `router.close()` method** is called multiple times on the page before the page `onDestroy()` returns and the `result` parameter** is passed, only the last call will take effect as the return value of the page. This is why it is recommended to return values ​​through the `close()` method in the `onDestroy()` life cycle function.
:::

### `clear` <decl type="(): Promise<void>" method />

Clear all bottom-level pages, leaving only the top-level pages. Calling the `clear()` method will not play the page transition animation. The Promise object returned by this method is honored after exiting all underlying pages.

### `getPages` <decl type="(): Component[]" method />

Get the page components of all pages in the current application page stack.

### `getLength` <decl type="(): number" method />

Get the number of pages in the current application page stack.

### `getPagesName` <decl type="(): String[]" method />

Get the names of all pages in the current application page stack.

### `getPage` <decl type="(index: number): Component | undefined" method />

Get the page component specified by `index` in the current application. `index` is the index of the page (i.e. the position in the page stack). If the page being searched does not exist, `undefined` is returned.

### `getIndex` <decl type="(component: Component): number | undefined" />

Get the page index specified by the page component `component` in the current application. If the page being searched does not exist, `undefined` is returned.

### `queryPage` <decl type="(name: string): Component[]" />

Get a list of all pages named `name` in the page stack. The order of the page list and the page stack is the same.

### `queryIndex` <decl type="(name: string): number[]" />

Get all page indexes named `name` in the page stack. The order of page index values ​​​​is the same as the order of the page stack.

## Development Notes

### Repeat pop-up page

Improper use of the `router.push()` method may cause the same page to pop up repeatedly. Consider an element like this:
``` html
<p on:click="onClick">Click Me!</p>
```
There is no problem when the component's `onClick()` event callback method simply pops up the new page:
``` js
export default{
  onClick() {
    router.push({ uri: 'CoverPage' })
  }
}
```
Because the page does not respond to gestures while the transition animation (if any) is playing, `router.push()` is not called repeatedly. However, problems may occur if `onClick()` is called after an asynchronous operation and then called `router.push()`, for example:
``` js
export default{
  async onClick() {
    //A one-second timer is used here to simulate asynchronous operations. True asynchronous operation,
    // The same problem will also occur when reading and writing files and querying network status.
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    // Call router.push() after the asynchronous operation
    router.push({ uri: 'CoverPage' })
  }
}
```
If the user clicks the "Click Me!" button multiple times during an asynchronous operation (a timer in the example), the page will pop up repeatedly. You can try the following demo to verify it:

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

First, please click the "Click Me!" button quickly and multiple times within one second, which will cause the Cover Page to pop up repeatedly. You can observe the number of repeated popups through the count displayed on the page.

Next, click Cover Page or swipe right to return to the previous page. At this point you will find that no matter how quickly and continuously you click, the pages will always return one by one without repeating the operation, because the gesture will not respond during the transition animation.

#### Avoid asynchronous operations

If you want to jump to a page in the callback function of a gesture operation (such as a click gesture), you should avoid asynchronous operations, because this will not only easily cause the page to pop up repeatedly, but also increase the delay of gesture response. In particular, please note that the delay of some asynchronous operations is uncontrollable. For example, checking the online status may take a long time in a weak network environment.

Therefore, in scenarios where page jumps need to be triggered by clicks, it is best to transfer possible network access to the new page and present the busy status through loading animation.

#### Avoidance methods

If an asynchronous operation must be performed before a gesture-triggered page jump, be sure to use a specific flag to avoid repeated page jumps. Take the previous `onClick()` callback as an example:
``` js
export default {
  async onClick() {
    // Add isClicked flag to skip repeated operations, does not need to be a reactive attribute
    if (this.isClicked)
      return
    // Mark isClicked before starting to execute gesture response logic
    this.isClicked = true
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    router.push({ uri: 'CoverPage' })
    // Clear isClicked after finishing executing gesture response logic
    this.isClicked = false
  }
}
```
Using the same method to continuously click the "Click Me!" button will not pop up the Cover Page repeatedly:

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

This example also confirms that asynchronous operations will indeed increase the delay of page jumps. The user will not see any return within one second of waiting for the timer to expire!

### Replace default page

Developers may not want the application to enter the [`router.entry`](/framework/application/manifest.md#entry) page of `manifest.json` when it starts. A typical scenario is when starting an application through deeplink, jumping to a specific page based on specific request parameters instead of entering the entry page.

In addition to deeplink, applications often need to select different home screens based on local status during cold start, such as deciding to enter the login page or home page based on the login status, or deciding to enter the privacy page or functional home page based on the locally stored privacy agreement consent mark. If you directly configure one of these pages as `router.entry`, and then jump within the page through [`router.replace()`](#replace), the unnecessary page will be displayed briefly in some cases, and it will look like the page "flashes".

To do this, you only need to pop up the page you really want to display through [`router.push()`](#push) before calling the [`onShow()`](/framework/component/life-cycle.md#onshow-1) life cycle function in the application startup phase. You can usually complete the local status check and jump to the homepage in the application's [`onCreate()`](/framework/component/life-cycle.md#oncreate) or [`onRoute()`](/framework/component/life-cycle.md#onroute) life cycle function. For example, in `onCreate()` of `app.ux`/`app.js`, the stored privacy agreement status is synchronously read, and then jumps directly to the privacy page or home page:
```js
// app.js
import router from '@system.router'
import storage from '@system.storage'

export default {
  onCreate() {
    const agreed = storage.get('privacyAgreed')
    if (agreed) // The user has agreed to the privacy agreement and goes directly to the function homepage
      router.push({ uri: 'MainPage' })
    else // The user has not agreed to the privacy agreement, and the privacy page is displayed on the first screen
      router.push({ uri: 'PrivacyPage' })
  }
}
```
Once the developer manually jumps to the page in the early stage of application startup, the **first screen page** actually displayed to the user during this startup is the target page popped up through `router.push()`. `router.entry` in `manifest.json` is only used as an internal entry and will not flash briefly on the interface.

### Jump to the opening screen interface

Many apps will display an opening logo page when first entering, and then jump to the actual functional homepage. The typical routing structure is: `router.entry` points to the logo page, and the logo page jumps to the homepage through [`router.replace()`](#replace) during initialization. In this way, after the application is launched, the user first sees a brief opening screen, and then sees an animation transitioning from the opening page to the homepage. The opening page will be removed from the page stack after the jump.
``` js
// Assume this is the index.ux script of the logo page
export default {
  onInit() {
    // Jump to the opening logo page after a period of delay
    setTimeout(() => {
      router.replace({ uri: 'MainPage' })
    }, 1000)
  },
}
```
Under this structure, the logo page itself is part of the product design, so it is expected behavior for users to briefly see the logo and then transition to the homepage. It should be noted that `replace()` can only ensure a smooth transition animation from the logo page to the homepage. The first frame of the logo page will still appear on the screen and cannot be "silently" skipped.

If the application does not design a separate logo or opening page, but still uses the "entry page + `replace()` jump" method, for example, configure the privacy agreement page as `router.entry` and switch to the homepage through `replace()`, the user will see the entry page "flash" when cold starting the application, and then switch to `MainPage` through a transition animation.

::: tip
This phenomenon is due to the routing mechanism itself. If you don't want users to observe "page switching". Priority should be given to combining the practices in the [Replace Default Page](#Replace Default Page) section to directly select the final first screen through `router.push()` during the application startup phase, instead of using `replace()` to replace yourself inside the entry page.
:::


============================================================
FILE_PATH: src/transl/EN/api/system-schedule.md

# Scheduled tasks

## Import module

``` js
import schedule from "@system.schedule"
// or
const schedule = require("@system.schedule")
```

Developers need to declare the application's access permissions to `watch.permission.SCHEDULE` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

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

Set up scheduled tasks. The functions of each field of the `options` parameter are:
- `type`:
  - 1: Hardware time, `triggerMethod` can be triggered by modifying the system time;
  - 2: Real time elapses, time will be calculated even in sleep state;
- `timeout`:
  - If type is 1, it is the timestamp of the first execution time, that is, the number of milliseconds from 1970/01/01 00:00:00 GMT to the current time;
  - If type is 2, it is the interval between the current time and the first execution time, in milliseconds;
- `triggerMethod`: The method name defined in app.js, which is called when the timeout is reached and is started from the background;
- `interval`: The interval for periodic execution, in milliseconds. If not passed, it will not be executed repeatedly;
- `params`: task parameters;

::: tip
While `timeout` and `interval` are accurate to milliseconds, timing is accurate to seconds. The interval between the first execution time and the periodic execution time cannot be less than 60 seconds, otherwise the interface will throw an exception.
:::

The return value is the task ID, which is used to cancel the task. The return value is -1, indicating that the creation failed.

``` js
let id = schedule.scheduleJob({
  type: 1,
  timeout: new Date('2025-03-14T23:00:00').getTime(), // timestamp of first execution time
  interval: 60000, // The periodic execution interval is not less than 60 seconds
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

Cancel scheduled tasks.

``` js
schedule.cancel(id)
```


============================================================
FILE_PATH: src/transl/EN/api/system-sensor.md

# sensor

## Import module

```js
import sensor from '@system.sensor';
```

Developers need to declare the application's access permissions to `watch.permission.ACCESS_SENSORS` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

## Interface definition

### `subscribeAccelerometer`
<decl method><pre>
(options: {
  interval?: 'game' | 'ui' | 'normal',
  callback: (data: AccelerometerValue) => void,
}): number
</pre></decl>

Monitor acceleration sensor data changes. The functions of each field of the `options` parameter are:
- `interval`: listening frequency, default `'normal'`, its optional values are as follows
  - `''game'': game mode, frequency is 20ms/time;
  - `'ui'`: UI mode, frequency is 60ms/time;
  - `'normal'`: normal mode, frequency is 200ms/time
- `callback`: Acceleration data update callback, the signature of acceleration data type `AccelerometerValue` is as follows:
  ``` ts
  type AccelerometerValue = {
    x: number // x-axis acceleration
    y: number // y-axis acceleration
    z: number // z-axis acceleration
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

//Cancel listening
sensor.unsubscribeAccelerometer(id)
```

### `unsubscribeAccelerometer` <decl type="(id: number): void" method/>

Cancel monitoring of acceleration sensor data. The parameter `id` is the listening ID returned by the [`subscribeAccelerometer`](#subscribeaccelerometer) method.

### `subscribeCompass`
<decl method><pre>
(options: {
  callback: (data: CompassValue) => void,
}): number
</pre></decl>

Monitor compass data changes. The return value is the listening ID, which is used to cancel listening. The functions of each field of the `options` parameter are:
- `callback`: Compass data change callback.

`CompassValue` signature:
``` ts
  type CompassValue = {
    direction: number // The angle between the y-axis and magnetic north pole (radians)
    accuracy: number // accuracy
  }
```
- `direction`: The angle in radians between the Y-axis of the device and the Earth's magnetic north pole, the value range is $(-\pi,\pi]$, where:
  - `0`: due north direction
  - $\pi$` / 2` (approximately 1.57): Due east direction
  - $\pi$ (about 3.14): due south direction
  - -$\pi$` / 2` (approximately -1.57): due west direction
- `accuracy`: accuracy level of compass data
  - `3`: high accuracy
  - `2`: medium accuracy
  - `1`: low precision
  - `0`: Untrustworthy (unknown reason)
  - `-1`: Untrusted (sensor lost connection)

Example:
```js
const id = sensor.subscribeCompass({
  callback(ret) {
    console.log(`direction=${ret.direction}, accuracy=${ret.accuracy}`)
  }
})

//Cancel listening
sensor.unsubscribeCompass(id)
```

### `unsubscribeCompass`<decl type="(id: number): void" method/>

Cancel monitoring of compass data. The parameter `id` is the listening id returned by the [`subscribeCompass`](#subscribecompass) method.

### `calibrationCompass` <decl type="(): Promise<void>" method/>

Start the compass calibration process. When the compass accuracy is low, guide the user to operate and call this method to calibrate the compass.

This function returns a resultless Promise object, which will be resolved when the system completes calibration.

### `getCompassValue` <decl type="(): Promise<CompassValue>" method/>

Get current compass data. Returns an asynchronous result, a Promise object of type `CompassValue` containing compass direction and accuracy information.

### `subscribeStepCounter`
<decl method><pre>
(options: {
  callback: (data: StepCounterValue) => void,
}): number
</pre></decl>

Monitor changes in pedometer sensor data. The functions of each field of the `options` parameter are:
- `callback`: Step counting data change callback, the signature of the step counting data type `StepCounterValue` is as follows:
  ``` ts
  type StepCounterValue = {
    steps: number // Current cumulative number of steps (starts from 0 after restart)
  }
  ```

Example:
```js
const id = sensor.subscribeStepCounter({
  callback(ret) {
    console.log(`steps=${ret.steps}`)
  }
})

//Cancel listening
sensor.unsubscribeStepCounter(id)
```

### `unsubscribeStepCounter` <decl type="(id: number): void" method/>

Cancel monitoring of pedometer sensor data. The parameter `id` is the listening id returned by the [`subscribeStepCounter`](#subscribestepcounter) method.

### `subscribeOnBodyState`
<decl method><pre>
(options: {
  callback: (data: OnBodyStateValue) => void,
}): number
</pre></decl>

Monitor device wearing status changes. The functions of each field of the `options` parameter are:
- `callback`: callback for device wearing state changes. The signature of the device wearing state data type `OnBodyStateValue` is as follows:
  ``` ts
  type OnBodyStateValue = {
    value: boolean // Whether it has been worn
  }
  ```

Example:
```js
const id = sensor.subscribeOnBodyState({
  callback(ret) {
    console.log(`onBody=${ret.value}`)
  }
})

//Cancel listening
sensor.unsubscribeOnBodyState(id)
```

### `unsubscribeOnBodyState` <decl type="(): void" method/>

Cancel monitoring of wearing status. The parameter `id` is the listening id returned by the [`subscribeOnBodyState`](#subscribeonbodystate) method.

### `getOnBodyState` <decl type="(): Promise<OnBodyStateValue>" method/>

Get the current device wearing status.

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

Monitor gyroscope data changes. The functions of each field of the `options` parameter are:
- `callback`: gyroscope data change callback, the signature of the gyroscope data type `GyroscopeValue` is as follows:
  ``` ts
  type GyroscopeValue = {
    x: number // x-axis angular velocity
    y: number // y-axis angular velocity
    z: number // z-axis angular velocity
  }
  ```

Example:
```js
const id = sensor.subscribeGyroscope({
  callback(ret) {
    console.log(`gyroscope data, x = ${ret.x}, y = ${ret.y}, z = ${ret.z}`)
  }
})

//Cancel listening
sensor.unsubscribeGyroscope(id)
```

### `unsubscribeGyroscope` <decl type="(id: number): void" method/>

Cancel monitoring of gyroscope data. The parameter `id` is the listening id returned by the [`subscribeGyroscope`](#subscribegyroscope) method.

### `subscribeBarometer`
<decl method><pre>
(options: {
  callback: (data: BarometerValue) => void,
}): number
</pre></decl>

Monitor changes in air pressure sensor data. The functions of each field of the `options` parameter are:
- `callback`: Barometer data change callback, the signature of barometer data type `BarometerValue` is as follows:
  ``` ts
  type BarometerValue = {
    pressure: number // Air pressure value, unit: Pa
  }
  ```

Example:
```js
sensor.subscribeBarometer({
  callback(ret) {
    console.log("get barometer:", ret.pressure)
  }
})

//Cancel listening
sensor.unsubscribeBarometer(id)
```

### `unsubscribeBarometer` <decl type="(id: number): void" method/>

Cancel monitoring of air pressure sensor. The parameter `id` is the listening id returned by the [`subscribeBarometer`](#subscribebarometer) method.

### `subscribeWristLift`
<decl method><pre>
(options: {
  callback: () => void,
}): number
</pre></decl>

Monitor wrist-raising events. The functions of each field of the `options` parameter are:
- `callback`: monitor wrist-raising event callback.

Example:
```js
const id = sensor.subscribeWristLift({
  callback: () => {
    console.log('wrist lift')
  }
});

//Cancel listening
sensor.unsubscribeWristLift(id)
```

### `unsubscribeWristLift` <decl type="(id: number): void" method/>

To cancel monitoring, raise your wrist. The parameter `id` is the listening ID returned by the [`subscribeWristLift()`](#subscribewristlift) method.

## Usage restrictions

When the current device does not support the corresponding sensor capability, the calling interface will directly throw an exception and the monitoring will not take effect.
Exception information log example: `the device does not support accelerometer sensor`

Example of capturing exception information:

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
## Notes

It is recommended to cancel the subscription in time when sensor data is not needed. Especially unsubscribe when the page is destroyed (`onDestroy` callback) to avoid unnecessary performance loss and power consumption overhead.


============================================================
FILE_PATH: src/transl/EN/api/system-storage.md

# Data storage

The data storage module `system.storage` allows an application to store its own data. This data will be persisted in the application's storage object. When the application is uninstalled, the data stored in `system.storage` will be cleared.

`system.storage` stores data as key-value pairs, where the key must be a string and the value is a JSON value (or a JavaScript value that can be serialized to JSON).

## Import module

``` js
import storage from '@system.storage'
```

## API

### `get` <decl type="(key: string): any" method />

Get the value corresponding to the key name `key` in the storage. Returns `undefined` if the key-value pair does not exist.

### `set` <decl type="(key: string, value: any): void" method />

This method accepts a key name `key` and a value `value` as parameters and adds this key-value pair to the storage. If the key name already exists, update its corresponding value.

### `delete` <decl type="(key: string): boolean" method />

Delete the key-value pair corresponding to the key name `key` in the storage. Returns `true` if the key-value pair exists and is successfully deleted.

### `clear` <decl type="(): void" method />

Clear all stored data in the app.


============================================================
FILE_PATH: src/transl/EN/api/system-test.md

# Test framework

## Import module

``` js
import test from '@system.test'
```

## Introduction

The `system.test` module is an end-to-end testing framework that can simulate user operations through programming and check whether the interface behavior is as expected.

A simple code to simulate user operations is as follows:
``` js
await test.getByClass('play-button').click()
await test.getByClass('more-button').click()
await test.getByClass('download-button').click()
await test.getByClass('close-button').click()
await test.getByClass('menu-button').click()
await test.getHasText('Download list').click()
await test.getByTag('Scroll').scroll(0, -200, 0.3)
await test.getHasText(/[a-z]/).click()
```
This code will automatically wait for the elements in the interface to be rendered, use scrolling gestures to bring the occluded elements into the visible area, and then perform gestures such as clicking or scrolling on them.

## API

### Auxiliary functions

These functions provide auxiliary functions in testing, such as delays, etc.

#### `wait` <decl method type="(duration: number): Promise<void>" />

The time specified by the asynchronous delay is used to wait for certain operations in the test, or to simulate user pauses.

### Locator

The locator finds elements (native components) from the top-level page of the application, for example, based on the element's tag or id. For further introduction to locators, please refer to [`Locator` object](#locator-object).

#### `getByTag` <decl method type="(tag: string): Locator" />

Locate elements via `tag`. Currently, only big camel case names are supported, such as `'P'`, `'Swiper'`, etc.

#### `getByClass` <decl method type="(class: string): Locator" />

Locate elements via the `class` attribute.

#### `getById` <decl method type="(id: string): Locator" />

Locate elements via the `id` attribute.

#### `getHasText` <decl method type="(text: RegExp | string): <Locator>" />

Locate elements by whether their `text` attribute matches the `text` parameter. The `text` parameter is a regular expression, for example:
- `/hello/` tests whether the `text` attribute value of the element contains the `'hello'' string;
- `/^hello/` tests whether the value of the element's `text` attribute starts with `'hello'';
- `/^hello$/` tests whether the element's `text` attribute value is `'hello'`.

The matching rules for the `text` parameter are the same as [`RegExp.test()`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/RegExp/test).

### `Locator` object

`Locator` objects are returned by the locator API and can be used for further operations. All locator operations attempt to automatically wait for the element to appear and move it into view.

#### `click` <decl method type="(): Promise<void>" />

When the element exists and has been scrolled into the visible area, simulate a click gesture at the element's position.

#### `scroll` <decl method type="(dx: number, dy: number, duration?: number): Promise<void>" />

When the element exists and has been scrolled into the visible area, simulate a scroll gesture at the element's position. `dy` and `dy` are the $(x, y)$ offset of the scrolling, in pixels; the optional `duration` is the duration of the gesture, in seconds, and the default value is $0.5 \rm s$.

This method will wait for the element's `scrolled` attribute to become `false` before polyfilling the returned Promise object. Therefore, for components such as `scroll` and `swiper`, the `scroll()` method will not trigger the next operation until the inertial animation of these components has stopped.

#### `wait` <decl method type="(): Promise<void>" />

Waits for the element to exist and scroll into view, but does not simulate any gestures or other operations.


============================================================
FILE_PATH: src/transl/EN/api/system-vibrator.md

# vibration

## Import module

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

Trigger vibration. The functions of each field of the `option` parameter are:
- `mode`: vibration mode, `long` means long vibration, `short` means short vibration. The default value is `long`.


============================================================
FILE_PATH: src/transl/EN/api/timer.md

# 定时器

本模块提供定时器功能，用于延迟执行或周期性执行代码。定时器 API 无需导入即可直接使用。

## 接口定义

### `setTimeout` <decl type="(callback: () => void, duration: number): number" />

设置一个定时器，在指定的延迟时间之后执行回调函数。参数说明：
- `callback`：延迟时间到达后要执行的回调函数；
- `duration`：延迟的时间，单位为毫秒。

返回一个定时器 ID，可用于通过 [`clearTimeout()`](#cleartimeout) 方法取消该定时器。

示例：
``` js
// 1 秒后执行回调函数
const timerId = setTimeout(() => {
  console.log('1 秒已过')
}, 1000)
```

### `setInterval` <decl type="(callback: () => void, duration: number): number" />

设置一个定时器，按照指定的周期重复执行回调函数。参数说明：
- `callback`：每次定时器触发时要执行的回调函数；
- `duration`：执行周期，单位为毫秒。

返回一个定时器 ID，可用于通过 [`clearInterval()`](#clearinterval) 方法取消该定时器。

示例：
``` js
// 每隔 500 毫秒执行一次回调函数
const timerId = setInterval(() => {
  console.log('又过了 500 毫秒')
}, 500)
```

### `clearTimeout` <decl type="(timerId: number): void" />

取消由 [`setTimeout()`](#settimeout) 方法设置的定时器。`timerId` 参数是要取消的定时器 ID。

::: warning
与 Web 环境不同，本实现中的定时器 ID 池**有可能被复用**。因此，**不要**对同一个有效的定时器 ID 重复调用 `clearTimeout()`，否则可能会意外停止其他正在运行的定时器。

推荐在清理定时器后将其 ID 置为 `null`，以避免重复清理。`clearTimeout()` 可以安全地接受 `null`、`0` 等无效 ID，这些调用不会产生副作用。
:::

示例：
``` js
const timerId = setTimeout(() => {
  console.log('这条消息不会输出')
}, 1000)

// 在定时器触发之前取消它
clearTimeout(timerId)
```

推荐的做法是在清理后将定时器 ID 置空，避免重复清理有效 ID：
``` js
export default {
  onInit() {
    this.timerId = setTimeout(() => {
      console.log('定时器触发')
      this.timerId = null // 执行后清空 ID
    }, 1000)
  },
  onDestroy() {
    // 可以安全地清理，即使 timerId 为 null
    clearTimeout(this.timerId)
  },
  someMethod() {
    // 清理定时器并置空
    clearTimeout(this.timerId)
    this.timerId = null
  },
}
```

### `clearInterval` <decl type="(timerId: number): void" />

取消由 [`setInterval()`](#setinterval) 方法设置的定时器。`timerId` 参数是要取消的定时器 ID。

::: warning
与 Web 环境不同，本实现中的定时器 ID 池**有可能被复用**。因此，**不要**对同一个有效的定时器 ID 重复调用 `clearInterval()`，否则可能会意外停止其他正在运行的定时器。

推荐在清理定时器后将其 ID 置为 `null`，以避免重复清理。`clearInterval()` 可以安全地接受 `null`、`0` 等无效 ID，这些调用不会产生副作用。
:::

示例：
``` js
let count = 0
const timerId = setInterval(() => {
  count++
  console.log(`执行次数: ${count}`)
  if (count >= 5)
    clearInterval(timerId) // 执行 5 次后停止
}, 500)
```

::: tip
`clearInterval` 和 `clearTimeout` 实际上是同一个函数的两个别名，但建议使用对应的方法以保持代码清晰。
:::

## 开发笔记

### 定时器 ID 复用

本实现与 Web 标准环境存在一个重要区别：**定时器 ID 可能会被复用**。

在 Web 浏览器和 Node.js 中，每次调用 `setTimeout()` 或 `setInterval()` 都会返回一个唯一的、单调递增的 ID，这些 ID 不会被复用。因此在 Web 环境中，对已清理或无效的定时器 ID 调用 `clearTimeout()` 或 `clearInterval()` 是安全的，不会产生副作用。

然而，在本实现中，定时器 ID 来自一个有限的 ID 池，当定时器被清理或执行完成后，其 ID 可能会被新创建的定时器复用。这意味着如果重复清理同一个 ID（即由 `setTimeout()` 或 `setInterval()` 返回的数字），就可能会意外停止另一个正在运行的定时器。

`clearTimeout()` 和 `clearInterval()` 可以安全地接受 `null`、`0`、`undefined` 等非定时器 ID 的值，这些调用不会产生副作用。

因此，**务必遵循以下最佳实践**：
1. 每个定时器 ID 仅清理一次；
2. 清理后将定时器 ID 置为 `null`、`0` 或 `undefined`，避免意外地重复清理。

`clearTimeout()` 和 `clearInterval()` 可以安全地接受 `null`、`0` 等非定时器 ID 的值，因此无需在调用前进行有效性判断。

前面 API 文档中的示例展示了推荐的做法。

例外情况是，你可以在 `setTimeout` 的回调函数中清理自身的定时器 ID：
``` js
let timer = setTimeout(() => {
  clearTimeout(timer) // 这不会影响其他定时器，也不会触发警告日志
}, 1000)
```

### 定时器精度问题

定时器 API **不保证精确的时间间隔**，实际执行时间可能会有偏差。这是因为：
- 系统调度和性能限制可能导致定时器触发时间不准确；
- 定时器的最小间隔受到系统限制，并随时受到低功耗策略影响。

因此，**不要**使用定时器 API 来进行精确计时。如果需要测量时间间隔或实现计时器功能，应该使用 `Date` 对象来获取实际的时间戳。

#### 错误示例：使用定时器计数来计时

下面的代码试图通过累加定时器触发次数来计算经过的时间，这是不正确的做法：
``` js
export default {
  data: {
    elapsedTime: 0, // 通过累加来计算经过时间
  },
  onInit() {
    // 错误：假设定时器每秒精确触发一次
    this.timerId = setInterval(() => {
      this.elapsedTime += 1000
    }, 1000)
  },
  onDestroy() {
    clearInterval(this.timerId)
  },
}
```

这种方法的问题在于，即使设置的间隔是 $1000\rm ms$，实际触发间隔可能是 $1010\rm ms$ 甚至更长。累计误差会导致计时越来越不准确。在设备进入低功耗模式后，定时器可能以秒级别的精度运行，或被直接挂起。

#### 正确示例：使用 Date 对象计时

正确的做法是记录起始时间戳，然后在每次更新时计算与当前时间的差值：
``` js
export default {
  data: {
    elapsedTime: 0, // 经过的时间（毫秒）
  },
  onInit() {
    // 记录起始时间戳
    this.startTime = Date.now()
    // 使用定时器定期更新显示
    this.timerId = setInterval(() => {
      // 通过计算时间戳差值来获取实际经过的时间
      this.elapsedTime = Date.now() - this.startTime
    }, 100) // 可以设置较短的更新间隔以提高显示流畅度
  },
  onDestroy() {
    clearInterval(this.timerId)
  },
}
```

### 完整的计时器示例

下面是一个完整的计时器组件示例，展示了如何正确实现开始、暂停和重置功能：

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
    elapsedTime: 0,     // 已经过的时间（毫秒）
    isRunning: false,   // 计时器是否正在运行
  },
  onInit() {
    this.startTime = 0       // 本次启动的时间戳
    this.accumulatedTime = 0 // 累计的时间（用于暂停后继续）
    this.timerId = null
  },
  onDestroy() {
    // 清理定时器
    clearInterval(this.timerId)
  },
  start() {
    if (this.isRunning)
      return // 已经在运行，避免重复启动

    this.isRunning = true
    // 记录本次启动的时间戳
    this.startTime = Date.now()

    // 定期更新显示
    this.timerId = setInterval(() => {
      // 累计时间 + (当前时间 - 本次启动时间)
      this.elapsedTime = this.accumulatedTime + (Date.now() - this.startTime)
    }, 20)
  },
  pause() {
    if (!this.isRunning)
      return // 已经暂停，无需操作

    this.isRunning = false
    // 停止定时器
    clearInterval(this.timerId)
    this.timerId = null // 清理后置空

    // 保存累计时间，以便下次继续
    this.accumulatedTime = this.elapsedTime
  },
  reset() {
    // 停止计时器
    this.isRunning = false
    clearInterval(this.timerId)
    this.timerId = null // 清理后置空

    // 重置所有状态
    this.elapsedTime = 0
    this.accumulatedTime = 0
    this.startTime = 0
  },
  formatTime(ms) {
    // 将毫秒转换为 "分:秒.毫秒" 格式
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

这个示例展示了：
- 使用 `Date.now()` 获取准确的时间戳，并通过时间戳差值计算实际经过的时间；
- `setInterval()` 仅用于定期更新界面显示；
- 正确处理开始、暂停和重置的状态转换；
- 在组件销毁时清理定时器资源。

### 内存泄漏预防

使用定时器时务必注意及时清理，否则可能导致内存泄漏或者访问已经销毁的组件。在组件的 [`onDestroy()`](/framework/component/life-cycle.md) 生命周期函数中清理所有定时器：
``` js
export default {
  onInit() {
    this.timerId = setTimeout(() => {
      // 执行某些操作
      this.timerId = null // 执行后置空
    }, 5000)
  },
  onDestroy() {
    // 清理定时器，防止内存泄漏
    clearTimeout(this.timerId)
  },
}
```

对于 `setInterval()` 创建的周期性定时器，这一点尤为重要，因为它们会持续运行直到被显式取消。


