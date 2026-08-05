# Device Information

## Import Module

``` js
import device from '@system.device'
```

Developers need to declare access to the `watch.permission.DEVICE_INFO` permission for the application in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

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

Gets basic device information. The meanings of the properties in the returned object are as follows:
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

Gets device identification information in batches. The `types` parameter specifies the categories of information to retrieve, which is an Array object consisting of elements `'device'`, `'mac'`, `'user'`, or `'advertising'`. Depending on the values in `types`, the meanings of the properties in the returned object are as follows:
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

Unlike the `memory-profile` media query property, the value of the `memoryProfile` property is an integer, with a fixed unit of $\rm KiB$.