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
