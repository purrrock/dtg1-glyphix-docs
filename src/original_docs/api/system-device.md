# 设备信息

## 导入模块

``` js
import device from '@system.device'
```

开发者需要在 [`manifest.json`](/framework/application/manifest.md#permissions) 文件中声明应用对 `watch.permission.DEVICE_INFO` 的访问权限。

## 接口定义

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

获取设备的基本信息。返回对象的属性字段含义为：
- `brand`：设备的品牌名。
- `manufacturer`：设备生产商。
- `model`：设备型号。
- `product`：设备代号。
- `osType`：操作系统名称。
- `osVersionName`：操作系统版本名称。
- `platformVersionName`：运行平台版本名称。
- `platformVersionCode`：运行平台版本号。
- `language`：系统语言。
- `region`：系统地区。
- `deviceName`：设备名称。

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

批量获取设备标识信息，参数 `types` 指定需要获取的信息类别，是一个由 `'device'`、`'mac'`、`'user'` 或 `'advertising'` 元素构成的 Array 对象。根据 `types` 值的不同，返回对象的属性各字段含义为：
- `type`: 。
- `device`: 设备唯一标识，仅当 `types` 包含 `'device'` 元素时存在。
- `mac`: 设备的 MAC 地址，仅当 `types` 包含 `'mac'` 元素时存在。
- `user`: 用户唯一标识，仅当 `types` 包含 `'user'` 元素时存在。
- `advertising`: 广告唯一标识，仅当 `types` 包含 `'advertising'` 元素时存在。

### `getDeviceId` <decl type="(): Promise<{deviceId: string}>" method />

获取设备唯一标识。

### `getSerial` <decl type="(): Promise<{serial: string}>" method />

获取设备序列号。

### `getTotalStorage` <decl type="(): Promise<{totalStorage: number}>" method />

获取存储空间的总大小，单位是字节。

### `getAvailableStorage` <decl type="(): Promise<{availableStorage: number}>" method />

获取存储空间的可用大小，单位是字节。

::: tip
模拟器上 `getTotalStorage()` 和 `getAvailableStorage()` 方法返回的值可能不准确，并且不会随着存储空间的变化而变化。
:::

### `screenWidth` <decl type="number" get />

设备的屏幕宽度，单位为像素。

### `screenHeight` <decl type="number" get />

设备的屏幕高度，单位为像素。

### `screenDensity` <decl type="number" get />

设备的屏幕像素密度，单位为 $\rm PPI$。

### `screenShape` <decl type="'rect' | 'circle'" get />

设备的屏幕形状，值的含义如下：
- `'rect'`: 设备具有矩形屏幕。
- `'circle'`: 设备具有圆形屏幕。

### `memoryProfile` <decl type="number" get />

获取设备的内存配置文件属性。这个属性是 [`memory-profile`](/framework/render/media-query.md#memory-profile) 媒体查询属性的 JavaScript API 版本，具体请参考媒体查询属性的文档。

与 `memory-profile` 媒体查询属性不同，`memoryProfile` 属性的值是一个整数，单位固定为 $\rm KiB$。
