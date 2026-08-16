# Context File: 03_glyphix_system_api_ZH.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/original_docs/api/system-notification.md

# 消息通知

## 导入模块

``` js
import notification from '@system.notification'
```

开发者需要在 [`manifest.json`](/framework/application/manifest.md#permissions) 文件中声明应用对 `watch.permission.NOTIFICATION` 的访问权限。

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

发布消息通知。`options` 参数的各字段功能为：
- `icon`：消息图标的 URI；
- `id`：应用通知的唯一 id；
- `contentType`：正文类型。 1：普通文本通知类型。 2：图片通知类型；暂时不支持图片通知；
- `content`：与 `contentType` 配合使用，表示通知的正文内容；
  - 当 `contentType` 为 1 时，表示普通文本通知的正文内容；object 类型，包含以下字段：
    - `title`：普通文本通知标题；string 类型；
    - `text`：普通文本通知内容；string 类型；
- `deliveryTime`：通知发送时间；
- `actionUri`：点击通知时跳转的 URI。

### `remove` 
<decl method><pre>
(options: {
  query:{
    id?: number
  }
}): void
</pre></decl>

清除消息通知。`options` 参数包含以下字段：
- query：清除的查询条件，
  - id：清除指定 id 的消息通知，如果不传入 id，则清除所有消息通知。


============================================================
FILE_PATH: src/original_docs/api/system-vibrator.md

# 震动

## 导入模块

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

触发震动。`option` 参数的各字段功能为：
- `mode`：振动模式，`long` 表示长振动，`short` 表示短振动。默认值为 `long`。


============================================================
FILE_PATH: src/original_docs/api/system-launch.md

# 应用跳转

## 导入模块

``` js
import launch from '@system.launch'
```

## 接口定义

### `launch` <decl type="(app: string): Promise<bool>" method/>

启动指定应用并切换到前台。`app` 是一个已经安装的应用 ID 字符串。返回的 Promise 表示应用是否加载成功。

### `inactive` <decl type="(app?: string): Promise<void>" method/>

将应用切换到后台。`app` 是一个已启动应用的 ID，不指定参数时会将当前应用切换到后台。只有前台应用可以切换到后台。

### `exit` <decl type="(app?: string): Promise<void>" method />

退出一个应用。参数 `app` 是一个已启动应用的 ID，不指定参数时会退出当前应用。

### `getRunning` <decl type="(): string[]" method />

获取正在运行的应用包名列表，包括那些在后台的应用。


============================================================
FILE_PATH: src/original_docs/api/system-calendar.md

# 日历

## 导入模块

``` js
import calendar from '@system.calendar'
```

## 接口定义

### `getLunar` <decl method type="(date: Date): LunarDate" />

获取一个 `Date` 对象的农历日期信息，返回 [`LunarDate`](#lunardate) 类型的农历日期描述。

### `getLunar` <decl method type="(year: number, month: number, day: number): LunarDate" />

获取指定公历年、月、日对应的农历信息，返回 [`LunarDate`](#lunardate) 类型的农历日期描述。参数含义如下：
- `year`：年份的完整编号，例如 `2024`；
- `month`：月份编号，从 `0` 开始，12 月的编号为 $11$；
- `day`：日期编号，从 `1` 开始。

## 类型定义

### `LunarDate`

``` ts
type LunarDate = {
  month: string,    // 农历月份名称
  day: string,      // 农历日期名称
  festival?: string // 节日名称，可能未定义
}
```

- `month`：农历月份的名称，例如 `'正月'`，`'二月'`。
- `day`：农历日期的名称，例如 `'初一'`，`'十五'`。
- `festival`：节日名称，如果没有节日则属性未定义。


============================================================
FILE_PATH: src/original_docs/api/system-interconnect.md

# 设备互联

## 导入模块

``` ts
import interconnect from '@system.interconnect'
```

## 接口定义

### `instance` <decl type="(options: {package: string, fingerprint: string}): Connect" method/>

创建 [`Connect`](#connect-接口) 实例

```js
const connect = interconnect.instance({
  package: "com.xxxx.xxx",
  fingerprint: "xxxxx"
})
```

- package: 手机应用的的包名
- fingerprint: 指纹信息，需要与手机应用创建连接时传入的指纹信息一致

## `Connect` 接口

### `onopen` <decl type="?: () => void" set />

用于指定连接打开时的回调

```js
connect.onopen = () => {
  console.info("onopen")
}
```

### `onclose` <decl type="?: () => void" set />

用于指定连接关闭时回调

```js
connect.onclose = () => {
  console.info("onclose")
}
```

### `onerror` <decl type="?: () => void" set />

用于指定连接失败后的回调

```js
connect.onerror = (data: any) => {
  console.info("onerror", data)
}
```

### `onmessage` <decl type="?: () => " set />

用于指定接收手机 App 端数据的回调

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

发送数据到手机 App 端

```js
connect.send({
  data: {
    name: "zhangsan"
  }
})
```


============================================================
FILE_PATH: src/original_docs/api/system-sensor.md

# 传感器

## 导入模块

```js
import sensor from '@system.sensor';
```

开发者需要在 [`manifest.json`](/framework/application/manifest.md#permissions) 文件中声明应用对 `watch.permission.ACCESS_SENSORS` 的访问权限。

## 接口定义

### `subscribeAccelerometer`
<decl method><pre>
(options: { 
  interval?: 'game' | 'ui' | 'normal', 
  callback: (data: AccelerometerValue) => void,
}): number
</pre></decl>

监听加速度传感器数据变化。`options` 参数的各字段功能为：
- `interval`：监听频率，默认 `'normal'`，其可选值如下
  - `'game'`：游戏模式，频率为 20ms/次；
  - `'ui'`：UI 模式，频率为 60ms/次；
  - `'normal'`：普通模式，频率为 200ms/次
- `callback`：加速度数据更新回调，加速度数据类型 `AccelerometerValue` 的签名如下：
  ``` ts
  type AccelerometerValue = {
    x: number   // x 轴加速度
    y: number   // y 轴加速度
    z: number   // z 轴加速度
  }
  ```

示例：
```js
const id = sensor.subscribeAccelerometer({
  interval: 'normal',
  callback(ret) {
    console.log(`gyroscope data, x = ${ret.x}, y = ${ret.y}, z = ${ret.z}`)
  }
})

// 取消监听
sensor.unsubscribeAccelerometer(id)
```

### `unsubscribeAccelerometer` <decl type="(id: number): void" method/>

取消监听加速度传感器数据。参数 `id` 为 [`subscribeAccelerometer`](#subscribeaccelerometer) 方法返回的监听 ID。

### `subscribeCompass`
<decl method><pre>
(options: { 
  callback: (data: CompassValue) => void,
}): number
</pre></decl>

监听指南针数据变化。返回值为监听 ID，用于取消监听。`options` 参数的各字段功能为：
- `callback`：指南针数据变化回调。

`CompassValue` 签名：
``` ts
  type CompassValue = {
    direction: number   // y 轴与地磁北极夹角（弧度）
    accuracy: number    // 精度
  }
```
- `direction`：设备 Y 轴与地球磁北极之间的弧度制夹角，取值范围为 $(-\pi,\pi]$，其中：
  - `0`：正北方向
  - $\pi$` / 2`（约 1.57）：正东方向
  - $\pi$（约 3.14）：正南方向
  - -$\pi$` / 2`（约 -1.57）：正西方向
- `accuracy`：指南针数据的精度级别
  - `3`：高精度
  - `2`：中等精度
  - `1`：低精度
  - `0`：不可信（原因未知）
  - `-1`：不可信（传感器失去连接）

示例：
```js
const id = sensor.subscribeCompass({
  callback(ret) {
    console.log(`direction=${ret.direction}, accuracy=${ret.accuracy}`)
  }
})

// 取消监听
sensor.unsubscribeCompass(id)
```

### `unsubscribeCompass`<decl type="(id: number): void" method/>

取消监听罗盘数据。参数 `id` 为 [`subscribeCompass`](#subscribecompass) 方法返回的监听 id。

### `calibrationCompass` <decl type="(): Promise<void>" method/>

启动指南针校准流程。当指南针精度较低时，引导用户操作并调用此方法校准指南针。

该函数返回一个无结果的 Promise 对象，当系统完成校准后，Promise 会被解析。

### `getCompassValue` <decl type="(): Promise<CompassValue>" method/>

获取当前指南针数据。返回一个异步的结果，包含指南针方向和精度信息 `CompassValue` 类型的 Promise 对象。

### `subscribeStepCounter`
<decl method><pre>
(options: { 
  callback: (data: StepCounterValue) => void,
}): number
</pre></decl>

监听计步传感器数据变化。`options` 参数的各字段功能为：
- `callback`：计步数据变化回调，计步数据类型 `StepCounterValue` 的签名如下：
  ``` ts
  type StepCounterValue = {
    steps: number     // 当前累计步数（重启后从 0 开始）
  }
  ```

示例：
```js
const id = sensor.subscribeStepCounter({
  callback(ret) {
    console.log(`steps=${ret.steps}`)
  }
})

// 取消监听
sensor.unsubscribeStepCounter(id)
```

### `unsubscribeStepCounter` <decl type="(id: number): void" method/>

取消监听计步传感器数据。参数 `id` 为 [`subscribeStepCounter`](#subscribestepcounter) 方法返回的监听 id。

### `subscribeOnBodyState`
<decl method><pre>
(options: { 
  callback: (data: OnBodyStateValue) => void,
}): number
</pre></decl>

监听设备佩戴状态变化。`options` 参数的各字段功能为：
- `callback`：设备佩戴状态变化回调，设备佩戴状态数据类型 `OnBodyStateValue` 的签名如下：
  ``` ts
  type OnBodyStateValue = {
    value: boolean  // 是否已佩戴
  }
  ```

示例：
```js
const id = sensor.subscribeOnBodyState({
  callback(ret) {
    console.log(`onBody=${ret.value}`)
  }
})

// 取消监听
sensor.unsubscribeOnBodyState(id)
```

### `unsubscribeOnBodyState` <decl type="(): void" method/>

取消监听佩戴状态。参数 `id` 为 [`subscribeOnBodyState`](#subscribeonbodystate) 方法返回的监听 id。

### `getOnBodyState` <decl type="(): Promise<OnBodyStateValue>" method/>

获取当前设备佩戴状态。

示例：
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

监听陀螺仪数据变化。`options` 参数的各字段功能为：
- `callback`：陀螺仪数据变化回调，陀螺仪数据类型 `GyroscopeValue` 的签名如下：
  ``` ts
  type GyroscopeValue = {
    x: number   // x 轴角速度
    y: number   // y 轴角速度
    z: number   // z 轴角速度
  }
  ```

示例：
```js
const id = sensor.subscribeGyroscope({
  callback(ret) {
    console.log(`gyroscope data, x = ${ret.x}, y = ${ret.y}, z = ${ret.z}`)
  }
})

// 取消监听
sensor.unsubscribeGyroscope(id)
```

### `unsubscribeGyroscope` <decl type="(id: number): void" method/>

取消监听陀螺仪数据。参数 `id` 为 [`subscribeGyroscope`](#subscribegyroscope) 方法返回的监听 id。

### `subscribeBarometer`
<decl method><pre>
(options: { 
  callback: (data: BarometerValue) => void,
}): number
</pre></decl>

监听气压传感器数据变化。`options` 参数的各字段功能为：
- `callback`：气压数据变化回调，气压数据类型 `BarometerValue` 的签名如下：
  ``` ts
  type BarometerValue = {
    pressure: number   // 气压值，单位：Pa
  }
  ```

示例：
```js
sensor.subscribeBarometer({
  callback(ret) {
    console.log("get barometer:", ret.pressure)
  }
})

// 取消监听
sensor.unsubscribeBarometer(id)
```

### `unsubscribeBarometer` <decl type="(id: number): void" method/>

取消监听气压传感器。参数 `id` 为 [`subscribeBarometer`](#subscribebarometer) 方法返回的监听 id。

### `subscribeWristLift`
<decl method><pre>
(options: { 
  callback: () => void,
}): number
</pre></decl>

监听抬腕事件。`options` 参数的各字段功能为：
- `callback`：监听抬腕事件回调。

示例：
```js
const id = sensor.subscribeWristLift({
  callback: () => {
    console.log('wrist lift')
  }
});

// 取消监听
sensor.unsubscribeWristLift(id)
```

### `unsubscribeWristLift` <decl type="(id: number): void" method/>

取消监听抬腕。参数 `id` 为 [`subscribeWristLift()`](#subscribewristlift) 方法返回的监听 ID。

## 使用限制

当前设备不支持对应的传感器能力时，调用接口将直接抛出异常，监听不会生效。
异常信息日志示例：`the device does not support accelerometer sensor`

捕获异常信息示例：

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
## 注意事项

建议在不需要传感器数据时，及时取消订阅。尤其是在页面销毁（`onDestroy` 回调）时取消订阅，以避免不必要的性能损耗和功耗开销。


============================================================
FILE_PATH: src/original_docs/api/system-compass.md

# 指南针

`@system.compass` 模块提供了访问设备指南针传感器的能力，可以获取设备相对于地球磁北极的方向信息。

## 导入模块

``` js
import compass from '@system.compass'
```

## 接口定义

### `subscribe` <decl type="(callback: (data: Value) => void): number" method/>

订阅指南针数据变化。当设备方向改变时，会自动调用回调函数。`callback` 回调函数接收 [`Value`](#value) 类型的指南针数据。

返回一个订阅 ID，用于取消订阅。

### `unsubscribe` <decl type="(subscribeId: number): void" method/>

取消指南针数据订阅。参数 `subscribeId` 为 [`subscribe()`](#subscribe) 方法返回的订阅 ID。

应当在页面或者组件销毁时调用此方法取消 `subscribe()` 的订阅：
``` js
const subscribeId = compass.subscribe((data) => {
  console.log(`方向: ${data.direction} 弧度`)
  console.log(`精度: ${data.accuracy}`)
})

// 取消订阅
compass.unsubscribe(subscribeId)
```


### `calibration` <decl type="(): Promise<void>" method/>

启动指南针校准流程。当指南针精度较低时，引导用户操作并调用此方法校准指南针。

该函数返回一个无结果的 Promise 对象，当系统完成校准后，Promise 会被解析。

### `getValue` <decl type="(): Promise<Value>" method/>

获取当前指南针数据。返回一个异步的结果，包含指南针方向和精度信息（[`Value`](#value) 类型）的 Promise 对象。

示例：
``` js
// 使用 Promise
compass.getValue().then((data) => {
  console.log(`方向: ${data.direction} 弧度`)
  console.log(`精度级别: ${data.accuracy}`)
})

// 使用 async/await
async function getCompassData() {
  const data = await compass.getValue()
  console.log(`方向: ${data.direction} 弧度`)
  console.log(`精度级别: ${data.accuracy}`)
}
```

::: note
由于实现缺陷，该方法不支持回调风格的调用（如 `{ success: (data) => {...} }`），请使用 Promise 或 async/await。
:::

## 类型定义

### `Value`

指南针数据类型 `Value` 的签名如下：
``` ts
type Value = {
  direction: number  // 指南针方向（弧度）
  accuracy: number   // 指南针精度级别
}
```
属性说明：
- `direction`：设备 Y 轴与地球磁北极之间的弧度制夹角，取值范围为 $[0,2\pi]$，其中：
  - `0`：正北方向
  - `Math.PI / 2`（约 1.57）：正东方向
  - `Math.PI`（约 3.14）：正南方向
  - `3 * Math.PI / 2`（约 4.71）：正西方向
- `accuracy`：指南针数据的精度级别
  - `3`：高精度
  - `2`：中等精度
  - `1`：低精度
  - `0`：不可信（原因未知）
  - `-1`：不可信（传感器失去连接）

示例：
``` js
// 判断方向
const data = await compass.getValue()
const degrees = data.direction * 180 / Math.PI // 转换为角度

console.log(`方向：${degrees}°`)
if (degrees >= 337.5 || degrees < 22.5) {
  console.log('朝向北方')
} else if (degrees >= 22.5 && degrees < 67.5) {
  console.log('朝向东北方')
} else if (degrees >= 67.5 && degrees < 112.5) {
  console.log('朝向东方')
}
// ... 其他方向判断

// 检查精度
if (data.accuracy >= 2) {
  console.log('指南针精度良好')
} else if (data.accuracy === 1) {
  console.log('指南针精度较低，建议校准')
  compass.calibration()
} else {
  console.log('指南针数据不可信')
}
```


============================================================
FILE_PATH: src/original_docs/api/system-device.md

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


============================================================
FILE_PATH: src/original_docs/api/system-app.md

# 应用上下文

## 导入模块

```js
import app from '@system.app'
```

## 接口定义

### `getInfo` <decl type="(): Manifest" method/>

获取当前应用的上下文信息，返回一个 [`Manifest` 对象](./system-package.md#manifest-对象)，包含应用的基本信息，例如包名、版本号等。

### `terminate` <decl type="(): void" method version="0.8"/>

终止当前应用的运行。调用此方法后，应用将被关闭，用户需要重新启动应用才能继续使用。

::: note 兼容性风险
该 API 未在所有平台上支持，可暂时使用 [`launch.exit()`](./system-launch.md#exit) 方法作为替代。
:::

### `loadLibrary` <decl type="(name: string): object | undefined" method/>

按名称加载一个由原生实现注册的 Library Loader，返回对应的库对象。若指定名称的库未注册，则返回 `undefined`。

典型情况下，建议将库对象挂载到 APP 对象上：
```js
// app.js
import app from '@system.app'

export default {
  customLib: app.loadLibrary('custom-library'),
  onCreate() {
    if (!this.customLib) {
      // 处理库加载失败的情况，例如回退到脚本实现
      this.customLib = someStubImplementation();
    } else {
      // 正常使用库对象
      this.customLib.someFunction()
    }
  }
}
```
这样，组件中可以直接使用 `this.$app.customLib` 来访问库对象。

`loadLibrary()` 适用于非标准系统功能的接入，应用可以检测返回值是否为 `undefined` 来判断当前平台是否支持该库，从而在通用模拟器环境中降级到脚本的打桩实现，而不依赖模拟器对特定模块路径的特殊处理。

如果应用需要同时支持标准快应用 API 和系统定制功能，可以根据 `loadLibrary()` 的返回结果决定是否回退。

### `keepForeground` <decl type="(options: { enable: boolean }): void" method/>

设置应用是否保持在前台显示，如果 `options` 参数中的 `enable` 属性为 `true`，则应用会试图保持在前台。

使用该方法需要在 [`manifest.json`](/framework/application/manifest.md#permissions) 文件中声明应用对 `watch.permission.FOREGROUND_SERVICE` 的权限。

该方法只是一个针对系统行为的提示，并不是强制性的，可能因用户操作或其他高优先级策略将应用切换到后台。使用该方法将应用保持在前台时，设备依然可以进入低功耗模式：

- 如果开启 AOD（Always on Display）模式，那么会降低 UI 刷新率。
- 否则，屏幕会在一段时间后关闭，但应用仍然保持在前台运行。

当设备进入低功耗模式后（包括关闭屏幕），前台应用依然会以较低的频率调度并执行，而不是完全休眠。因此可以用于导航或者健身类的应用。


============================================================
FILE_PATH: src/original_docs/api/system-fetch.md

# 数据请求 fetch

## 导入模块

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

发起异步的网络数据请求。`options` 参数的各字段功能为：
- `url`：要访问的网站的网址 URL。
- `method`：支持 `'GET'` 、`'POST'` 和 `'PUT'`，默认是 `'GET'`。
- `header`：一个包含 HTTP 请求头信息的对象，键和值为字符串。典型的 HTTP 头部字段可以是 `Authorization`、`Content-Type` 等。
- `params`：请求的参数，会将其所有属性设置到请求的 URL 部分。
- `data`：HTTP POST 请求中的主体（body）部分内容。
- `responseType`：HTTP 请求中的响应数据类型，默认是 `'text'`，可以有以下取值。
  - `'text'`：响应返回文本数据，即返回数据的 `data` 属性为 `string` 类型。
  - `'json'`：响应返回 JSON 数据，返回的 `data` 属性会将该 JSON 数据解析为对应的 JavaScript 值。
  - `arraybuffer`：响应返回二进制数据，即返回的数据是，以 `ArrayBuffer` 对象来存储的。
- `timeout`: 请求响应的超时时间，单位为毫秒，默认值为 $6000 \rm ms$。

#### `data` 参数

`data` 是请求的主体（body），仅在 POST 请求中使用。它通常是三种类型：字符串、`ArrayBuffer` 对象或者 JSON 对象。当 `data` 为字符串或者 `ArrayBuffer` 对象时，请求的主体将分别是文本或者二进制数据。当主体是一个 JSON 对象时，它会被序列化为文本形式。序列化的格式由请求方法（`method` 参数）的 `Content-Type` 字段决定：
- `Content-Type` 为 `application/json` 时，将 `data` 参数对象序列化为 JSON 字符串后作为请求主体；
- 其他情况下将 `data` 参数对象序列化为 `application/x-www-form-urlencoded` 的格式。

::: warning
很多 HTTP API 使用 JSON 格式的 POST 请求主体，请注意要正确设置请求头的 `Content-Type` 为 `application/json`，具体请参考此[示例](#post-请求-json-body)。
:::

#### 返回值

返回一个 `Promise` 对象，它在请求完后兑现值的属性如下：
- [`code`](#code-响应代码) 为服务器响应代码，请求成功的响应代码一般是 `200`。
- `header` 为服务器的响应头。
- `data` 为请求数据的返回值，具体的内容由 `options.responseType` 参数决定。

当请求失败后，返回的 `Promise` 对象会被拒绝。

## 使用说明

### `code` 响应代码

服务器返回的响应代码含义为：
- `200`：表示请求成功；
- `1002`：参数校验错误；
- `1005`：输入的参数不完整；
- `5000`：请求失败，响应错误；
- `5001`：读取数据缓冲区失败；
- `5002`：请求失败，响应错误；
- 其他：其他 HTTP/HTTPS 响应代码，如 `404` 等。

当 [`fetch`](#fetch) 返回的响应代码为 `200` 时表示网络请求成功，为其他值时表示请求出现错误。

### 注意事项

## 示例

### GET 请求

这是一个基本的 GET 请求示例：

``` js
const res = await fetch.fetch({
  url: 'http://www.rt-thread.com/service/rt-thread.txt',
  method: 'GET', // 由于默认的模式就是 GET，此时 method 是可选的
  responseType: 'text'
})
console.log(`the status code of the response: ${res.code}`)
console.log(`the data of the response: ${res.data}`)
```

### POST 请求

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

### POST 请求（JSON Body）


============================================================
FILE_PATH: src/original_docs/api/system-path.md

# 路径操作

本模块提供路径操作的接口。包括路径拼接、分割以及化简等功能。

## 导入模块

``` js
import path from '@system.path'
```

## 接口定义

#### `path.basename` <decl type="(path: string, suffix?: string): string" method />

返回路径 `path` 的文件名部分，通过指定 `suffix` 参数还可以去除指定的文件名后缀。例如
``` js
path.basename('/foo/bar/baz.txt') // 'baz.txt'
path.basename('/foo/bar/baz.txt', '.txt') // 'baz'
```

#### `path.dirname` <decl type="(path:string): string" method />

返回 `path` 的路径部分（和 `basename()` 相反，它会丢弃文件名部分）。例如
``` js
path.dirname('/foo/bar/baz') // '/foo/bar'
```

#### `path.extname` <decl type="(path: string): string" method />

获取 `path` 中的文件后缀。例如
``` js
path.extname('table.json') // '.json'
path.extname('/images/icon.png') // '.png'
```

#### `path.isAbsolute` <decl type="(path: string): boolean" method />

判定 `path` 是否为绝对路径。例如
``` js
path.isAbsolute('/foo/bar'); // true
path.isAbsolute('/baz/..');  // true
path.isAbsolute('qux/');     // false
path.isAbsolute('.');        // false
```

#### `path.join` <decl type="(...paths: string[]): string" method />

将多个路径进行拼接并化简，例如
``` js
path.join('/foo', 'bar', 'baz/asdf', 'quux', '..') // '/foo/bar/baz/asdf'
```

#### `path.normalize` <decl type="(path: string): string" method />

将路径 `path` 化为最简，会解析 `..` 和 `.`，并移除多余的路径分隔符 `/`。

``` js
path.normalize('/foo///bar/.././/baz') // '/foo/baz'
```

#### `path.relative` <decl type="(from: string, to: string): string" method />

计算从 `from` 到 `to` 的相对路径。

``` js
path.relative('/data/orandea/test/aaa', '/data/orandea/impl/bbb') // '../../impl/bbb'
```


============================================================
FILE_PATH: src/original_docs/api/system-audiokit.md

# 音频播放器管理器

## 导入模块

``` ts
import audiokit from '@system.audiokit'
```

## 接口定义

### `getPlayers` <decl type="(): AudioPlayer" method />

查询系统中可用的音频播放器 [`AudioPlayer`](#AudioPlayer) 对象列表。

### `getActivePlayer` <decl type="(): AudioPlayer" method />

查询系统中处于活跃状态的音频播放器 [`AudioPlayer`](#AudioPlayer) 对象。

### `subscribe` <decl type="(callback: (PlayerEvent) => void): number" method/>

监听系统中音频播放器的变化。`callback` 的参数 `PlayerEvent` 为[通知事件](#PlayerEvent)，此方法返回的 ID 可使用 [`unsubscribe()`](#unsubscribe) 方法来解除监听。

`PlayerEvent` 的类型签名：

```ts
type PlayerEvent = {
  notify: string; // 变化事件类型
  player: string; // 变化播放器名字
}
```

变化事件类型

- `active`：系统当前活跃的播放器发生改变  
- `append`：系统中添加了播放器
- `remove`：系统中移除了播放器

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

取消播放器变化监听，`subscribeID` 是 [`subscribe()`](#subscribe) 方法返回的 ID 值。

## `AudioPlayer` 对象

::: details 类型签名
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

- `AudioPlayer` 对象（以下简称：`audiokit.Player`）与 `system.media` 模块中创建的 `AudioPlayer` 对象（以下简称：`media.Player`），为不同的js对象，但是它们管理同一个播放器，同时 `audiokit.Player` 对象较 `media.Player` 对象多一些功能，例如：`next()`、`previous()` 等方法，用户通过 `audiokit.Player` 对象执行的 `play()` 等操作，也会通知给 `media.Player` 对象的监听。

### `src` <decl type="string" set get />

设置或读取需要播放音频的 url。支持[本地资源路径](/framework/application/resource.md#uri-和路径)与使用http、https协议的网络资源路径（例如：`https://www.rt-thread.com/service/test/001.mp3`）。下面是一个设置 src 然后开始播放的简单示例：

```ts
import audiokit from '@system.audiokit'
// 查询系统中处于活跃状态的音频播放器
let player = audiokit.getActivePlayer()
if (player != null) {
  // 首先停止当前正在播放的音频
  player.stop()
  // 设置需要播放的音频url
  player.src = 'https://www.rt-thread.com/service/test/001.mp3'
  // 开始播放音频
  player.play()
}
```

### `name` <decl type="string" set get />

播放器对象的名字，如果不设置，默认为创建播放器的应用名。需要注意的是，播放器对象的名字并不是全局不唯一，并不能使用名字来标识播放器对象。

### `icon` <decl type="string" set get />

播放器对象的图标 url。支持[本地资源路径](/framework/application/resource.md#uri-和路径)

### `mode` <decl type="string" set get />

播放模式。该属性对应的功能应由播放器应用实现，播放器对象默认不处理，只提供该属性。

- `sequential`：顺序播放  
- `random`：随机播放  
- `singleloop`：单曲循环  
- `listloop`：列表循环  

### `status` <decl type="string" get />

读取当前播放状态

- `play`：正在播放状态  
- `pause`：暂停播放状态  
- `stop`：停止播放状态 
- `ended`：播放结束状态  
- `error`：播放错误状态  

### `duration` <decl type="number" get />

音频总时长，单位：秒

### `position` <decl type="number" set get />

当前音频播放的时间位置，单位：秒

### `songAttribute` <decl type="songAttribute" set get />

歌曲属性对象

::: details 类型签名
```ts
type songAttribute = {
  title: string; // 歌曲的名称
  artist: string; // 表演者的名称，可以是个人或者乐队
  album: string; // 歌曲所属的专辑名称
  year: string; // 歌曲的发行年份
  genre: string; // 歌曲的类型，例如流行、摇滚、古典等
  track: string; // 当前歌曲在专辑中的编号，例如："1/12" 表示第1首，共12首
  coverArt: string; // 歌曲封面图片的url
  lyrics: string; // 歌词文本的 url
  comments: string; // 额外信息，如版权备注等
}
```
:::

songAttribute对象与AudioPlayer对象一样是一个Proxy对象，即不能使用JSON序列化与反序列化，也不能在响应式框架中引用。下面是一个简单的使用示例：

```ts
// 设置歌曲的名字
this.player.songAttribute.title = "未知"
// 设置歌曲演唱者
this.player.songAttribute.artist = "未知"
// 查看歌曲的名字
console.dir(this.player.songAttribute.title)
```

### `volume` <decl type="number" set get />

当前播放器的音量，范围：[0.0, 1.0]

### `nextAvailable` <decl type="bool" set get />

设置或查询是否可以切换下一曲

### `prevAvailable` <decl type="bool" set get />

设置或查询是否可以切换上一曲

### `play` <decl type="(): void" method />

开始播放在 src 属性中指定的音频

- 如果在调用此方法之前未设置 src 属性，会导致播放失败，触发 onerror 事件；
- 此方法为同步接口，执行此接口后，需要等待 onplay 事件或者 onerror 事件来判定播放成功或失败，在事件未触发之前，执行的额其它操作会被忽略；  

下面是一个调用play() 接口的简单示例：

```ts
import audiokit from '@system.audiokit'
// 查询系统中处于活跃状态的音频播放器
let player = audiokit.getActivePlayer()
if (player != null) {
  // 首先停止当前正在播放的音频
  player.stop()
  // 设置需要播放的音频url
  player.src = 'https://www.rt-thread.com/service/test/001.mp3'
  // 设置 onplay 事件
  player.onplay = () => { console.dir("开始播放") }
  // 设置 onerror 事件
  player.onerror = () => { console.dir("播放错误") }
  // 开始播放音频
  player.play()
}
```

### `pause` <decl type="(): void" method />

暂停播放当前音频  

- 此方法为同步接口，执行此接口后，需要等待 onpause 事件或者 onerror 事件来判定暂停成功或失败，在事件未触发之前，执行的额其它操作会被忽略；  

### `stop` <decl type="(): void" method />

停止音频播放，可以通过 play 重新播放音频  

- 此方法为同步接口，执行此接口后，需要等待 onstop 事件或者 onerror 事件来判定停止成功或失败，在事件未触发之前，执行的额其它操作会被忽略；  

### `release` <decl type="(): void" method />

释放音频资源  

- 执行此接口会停止播放当前音频，需要等待 onstop 事件或者 onerror 事件来判定停止成功或失败，在事件未触发之前，执行的额其它操作会被忽略；   

### `next` <decl type="(): void" method />

通知播放器应用，播放下一首。执行此接口后，会触发 onnext 事件通知监听此事件的播放器应用，由播放器应用执行歌曲切换的逻辑。

### `previous` <decl type="(): void" method />

通知播放器应用，播放下一首。执行此接口后，会触发 onprevious 事件通知监听此事件的播放器应用，由播放器应用执行歌曲切换的逻辑。

### `requestFocus` <decl type="({acquireType: string，volumeType: string}): void" method />

请求音频焦点。执行此接口后，会通知底层请求或者释放音频焦点，由底层控制不同类型音频的切换与打断逻辑。

`acquireType` 参数指示请求类型：
- `gain`：请求音频焦点
- `loss`：释放音频焦点

`volumeType` 参数指示音频类型：
- `system`：系统提示
- `media`：媒体音乐
- `tts`：语音播报

以下示例演示 `requestFocus` 函数请求音频焦点的方法：
``` ts
import audiokit from '@system.audiokit'
// 查询系统中处于活跃状态的音频播放器
let player = audiokit.getActivePlayer()
if (player != null) {
  // 获取媒体音乐类型的音频焦点
  player.requestFocus({ volumeType: 'media', acquireType: 'gain' });
}
```

### `releaseFocus` <decl type="(): void" method />

释放音频焦点。执行此接口后，会通知底层释放音频焦点，由底层控制不同类型音频的切换与打断逻辑。

### `onplay` <decl type="?: () => void" set />

在音频 play 成功后的回调事件

### `onpause` <decl type="?: () => void" set />

在音频 pause 成功后的回调事件

### `onstop` <decl type="?: () => void" set />

在音频 stop 成功后的回调事件

### `onended` <decl type="?: () => void" set />

在音频播放结束后的回调事件

### `onerror` <decl type="?: () => void" set />

执行`play` `pause` `stop` `position`等接口发生错误的回调事件，发生错误时， 对应的 onplay 等事件不会被触发

### `ontimeupdate` <decl type="?: () => void" set />

在 position 属性更新时会触发的回调事件，此事件只有应用处于前台时才会触发，当应用处于后台时会停止派发。

### `oninterrupt` <decl type="?: (action: {interruptHint: number}) => void" set />

发生音频打断事件时的回调函数，当前音频被相同音频类型或其它音频类型的音频抢夺时，被暂时打断或彻底打断的通知。

`action` 参数的 `interruptHint` 指示打断事件的类型：
- `1`：短暂打断 （可以自动恢复，如：音乐被打断）
- `2`：彻底打断 （不可自动恢复，如：网易云被喜马拉雅打断）

以下示例演示注册 `oninterrupt` 回调函数的方法，该函数会在事件发生时调用：
``` js
player.oninterrupt = (action) => {
  console.log(action.interruptHint)
}
```

### `onnext` <decl type="?: () => void" set />

需要播放下一曲时的回调事件

### `onprevious` <decl type="?: () => void" set />

需要播放上一曲时的回调事件

### `onrequestplay` <decl type="?: () => void" set />

底层需要启动播放时触发该回调事件通知js应用，由js应用执行启动播放的逻辑

### `onrequestpause` <decl type="?: () => void" set />

底层需要暂停播放时触发该回调事件通知js应用，由js应用执行暂停播放的逻辑

### `onrequeststop` <decl type="?: () => void" set />

底层需要停止播放时触发该回调事件通知js应用，由js应用执行停止播放的逻辑

### `onsongattribute` <decl type="?: () => void" set />

歌曲属性对象发生变化时的回调事件

### `onposition` <decl type="?: () => void" set />

执行 `position` 设置当前音频播放的时间位置成功的回调事件

### `onrequestfocus` <decl type="?: () => void" set />

请求音频焦点成功时的回调事件

### `onreleasefocus` <decl type="?: () => void" set />

释放音频焦点成功时的回调事件

### `onmodechanged` <decl type="?: () => void" set />

播放模式发生变化时的回调事件

### `onvolumechange` <decl type="?: () => void" set />

播放器音量发生变化时的回调事件


============================================================
FILE_PATH: src/original_docs/api/system-brightness.md

# 亮度管理

## 导入模块

``` js
import brightness from '@system.brightness'
```

## API

### `getValue` <decl type="(): number" method />

获取屏幕的亮度值，范围为 $[0, 1]$。

### `setValue` <decl type="(value: number): void" method />

设置屏幕的亮度值。`value` 的范围为 $[0, 1]$。

### `getMode` <decl type="(): string" method />

获取屏幕的亮度模式。

### `setMode` <decl type="(mode: number): void" method />

设置屏幕的亮度模式。设置 `number` 为 `0` 时，为标准模式，设置 `number` 为 $1$ 时，为自动模式。

### `setKeepScreenOn` <decl type="(mode: Boolean): void" method />

设置是否保持屏幕常亮。设置 `mode` 为 `true` 时，屏幕常亮，设置 `mode` 为 `false` 时，取消屏幕常亮。

### `wakeScreenOn`
<decl method><pre>
(options: { 
  screenOn: boolean, 
  timeout?: number,
}): void
</pre></decl>

点亮或熄灭屏幕。options 参数的各字段功能为：
- `screenOn`：是否点亮屏幕
- `timeout`：自动熄灭时间，不填则不限时间


============================================================
FILE_PATH: src/original_docs/api/system-ble.md

# 低功耗蓝牙模块

本模块提供了基于低功耗蓝牙（Bluetooth Low Energy，BLE）技术的蓝牙能力，支持发起BLE扫描、以及基于通用属性协议（Generic Attribute Profile，GATT）的连接和传输数据（目前仅支持创建 GattClient，暂不支持创建 GattServer）。

::: warning
`@system.bluetooth.ble` 中的 API 大部分都是[Promise异步操作](#Promise异步操作)，这和同步的 IO 访问有本质区别。请务必理解异步编程的基本概念，并且熟悉 Promise 和 `async/await` 的用法。
:::

## 导入模块

``` js
import ble from '@system.bluetooth.ble'
```

## 权限

::: tip
使用该模块应用需要声明权限：watch.permission.BLUETOOTH 
:::

## ble接口定义

### `ResultCode`

Promise中返回的结果枚举

- `0`：成功；
- `1`：低功耗蓝牙未开启；
- `2`：参数错误；
- `3`：低功耗蓝牙开启失败；
- `4`：没有可用的蓝牙适配器；
- `5`：连接失败；
- `6`：断开连接失败；
- `7`：暂不支持设置此属性；
- `8`：未知错误；

### `startBLEScan`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

启动扫描，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

下面是一个启动扫描的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    async scanStart() {
        // 启动扫描
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

停止扫描，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

下面是一个停止扫描的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    async scanStop() {
        // 停止扫描
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

此对象用于表示上报的扫描结果，类型签名如下：

```ts
/**
 * 扫描结果对象定义
 */
type ScanResult = {
    deviceId: string; // 设备 ID（例如："AA:BB:CC:DD:EE:FF"）
    rssi: number; // 信号强度，单位 dBm
    data: ArrayBuffer; // 广播报文原始数据
    deviceName: string; // 设备名称（如果有）
    connectable: boolean; // 是否可连接，true 表示可连接
}
```

### `getBLEScanResults`
<decl method><pre>
(): Promise&lt;Array&lt;ScanResult&gt;&gt;
</pre></decl>

查询扫描结果，使用Promise异步回调。该接口异步返回一个包含 [`ScanResult`](#scanresult) 对象的数组（即Array&lt;[`ScanResult`](#scanresult)&gt;）。

::: warning
因为底层的蓝牙适配器是单例的，所以可能会出现多个应用同时操作蓝牙设备的情况。就会存在：应用A 开启扫描一段时间后之后，应用B 再次开启扫描，此时 应用B 监听到的扫描结果是不完整的。为了处理这种情况，建议所有应用开启扫描之后，立即查询一下当前的扫描结果。
:::

下面是一个启动扫描后查询扫描结果的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        scanList: [],
    },
    async scanStart() {
        // 启动扫描
        await ble.startBLEScan().then(async (result) => {
            console.dir('startBLEScan success')
            // 查询扫描结果
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

订阅扫描状态变化，使用Callback异步回调。当扫描状态改变时，会自动调用 `callback` 回调函数。该接口同步返回一个订阅ID，用于取消订阅。

回调函数参数字段说明：
- `scan`：当前扫描状态。true表示正在扫描，false表示已经停止扫描。

下面是一个订阅扫描状态变化的示例：
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

取消订阅扫描状态变化。参数 `subscribeId` 为 [`subscribeScanStatus`](#subscribescanstatus) 方法返回的订阅ID。

下面是一个取消订阅扫描状态变化的示例：
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

订阅扫描结果上报事件，使用Callback异步回调。每当扫描到一个新的设备时，都会自动调用 `callback` 回调函数。该接口同步返回一个订阅ID，用于取消订阅。

::: tip
扫描结果上报为增量模式，既发现一个上报一个，监听此事件后需要用户自己存储扫描结果。
:::

回调函数参数字段说明：
- [`ScanResult`](#scanresult) ：扫描到的新设备对象。

下面是一个订阅扫描结果上报事件的示例：
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

取消订阅扫描结果上报事件。参数 `subscribeId` 为 [`subscribeBLEDeviceFind`](#subscribebledevicefind) 方法返回的订阅 ID。

下面是一个取消订阅扫描结果上报事件的示例：
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

此对象用于表示 Gatt 协议中的 Client 对象，类型签名如下：

```ts
/**
 * GattClientDevice对象类型定义
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

创建 [`GattClientDevice`](#gattclientdevice) 实例，表示GATT连接中的client端，该接口同步返回一个 [`GattClientDevice`](#gattclientdevice) 实例。

 - 通过该实例可以操作client端行为，如调用 [`connect`](#connect) 向对端设备发起连接，调用 [`getServices`](#getservices) 获取对端设备支持的所有服务能力。
 - 创建该实例所需要的 deviceId(设备地址) 表示server端设备地址。可以通过 [`startBLEScan`](#startblescan) 接口获取server端设备地址，且需保证server端设备的BLE广播是可连接的。

下面是一个创建 [`GattClientDevice`](#gattclientdevice) 实例的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    create() {
        // 请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
    },
}
```

## GattClientDevice接口定义

### `connect`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

client端主动发起和server蓝牙设备的GATT协议连接，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

 - 使用该类的方法前，需通过 [`createGattClientDevice`](#creategattclientdevice) 方法构造该类的实例。
 - 通过创建不同的该类实例，可以管理多路GATT连接。

下面是一个发起GATT协议连接的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async connect() {
        // 请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
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

client端主动断开和server蓝牙设备的GATT协议连接，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

下面是一个断开GATT协议连接的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        address: null,
    },
    gattClient: null,
    async connect() {
        // 请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
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

关闭client端实例，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

### `getDeviceName`
<decl method><pre>
(): Promise&lt;string&gt;
</pre></decl>

client获取远端蓝牙低功耗设备的名称，使用Promise异步回调。该接口异步返回一个&lt;string&gt;类型的设备名。

下面是一个GATT连接成功后，获取设备名字的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async name() {
        let clientName = 'N/A'
        // 请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
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

此对象用于表示 GATT 服务结构，类型签名如下：

```ts
/**
 * GATT服务结构定义，可包含多个特征值BLECharacteristic和依赖的其他服务。
 */
type GattService = {
    serviceUuid: string; // 服务UUID，标识一个GATT服务。例如：00001888-0000-1000-8000-00805f9b34fb。
    isPrimary: boolean; // 是否是主服务。true表示是主服务，false表示是次要服务。
    characteristics: Array<BLECharacteristic>; // 当前服务包含的特征值列表。
    includeServices: Array<GattService>; // 当前服务依赖的其它服务。
}
```

### `getServices`
<decl method><pre>
(): Promise&lt;Array&lt;GattService&gt;&gt;
</pre></decl>

client端获取蓝牙低功耗设备的所有服务，即服务发现，使用Promise异步回调。该接口异步返回一个包含所有服务的Array&lt;[`GattService`](#gattservice)&gt;类型的数组。

下面是一个GATT连接成功后，获取该设备所有服务的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    async onShow() {
        // 请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
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

此对象用于表示GATT特征值支持的属性，类型签名如下：

```ts
/**
 * 描述GATT特征值支持的属性。决定了特征值内容和描述符如何被使用和访问。
 */
type GattProperties = {
    write: boolean; // 该特征值是否支持写入操作。true表示支持，且被写入时需要回复对端设备，false表示不支持。
    writeNoResponse: boolean; // 该特征值是否支持写入操作。true表示支持，且被写入时无需回复对端设备，false表示不支持。
    read: boolean; // 该特征值是否支持读取操作。true表示支持，false表示不支持。
    notify: boolean; // 该特征值是否支持主动向对端设备通知特征值内容。true表示支持，且对端设备不需要回复确认，false表示不支持。
    indicate: boolean; // 该特征值是否支持向对端设备指示特征值内容。true表示支持，对端设备需要回复确认，false表示不支持。
    broadcast: boolean; // 该特征值是否支持作为广播内容由server端发送。true表示支持，server端可将特征值内容以ServiceData类型在广播报文中携带，false表示不支持。
    authenticatedSignedWrite: boolean; // 该特征值是否支持签名写入操作，通过对写入内容进行签名校验替代加密流程。true表示支持，false表示不支持。
    extendedProperties: boolean; //该特征值是否存在扩展属性。true表示存在扩展属性，false表示不存在。
}
```

### `BLECharacteristic`

此对象用于表示GATT特征值，类型签名如下：

```ts
/**
 * GATT特征值类型定义, 是服务GattService的核心数据单元
 */
type BLECharacteristic = {
    serviceUuid: string; // 特征值所属的服务UUID, 例如：00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // 特征值UUID, 例如：00002a11-0000-1000-8000-00805f9b34fb
    characteristicValue: ArrayBuffer; // 特征值的数据内容, 读取写数据时使用
    descriptors: Array<BLEDescriptor>; // 特征值包含的描述符列表
    properties: GattProperties; // 特征值支持的属性
    characteristicValueHandle: number; // 特征值的唯一标识句柄。当server端BLE蓝牙设备提供了多个相同UUID特征值时，可以通过此句柄区分不同的特征值
}
```

### `readCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic): Promise&lt;BLECharacteristic&gt;
</pre></decl>

client端从指定的server端特征值读取数据，使用Promise异步回调。该接口异步返回一个 [`BLECharacteristic`](#blecharacteristic) 类型的对象。

 - 该接口需要传入一个 [`BLECharacteristic`](#blecharacteristic) 类型的对象，表示需要读取哪一个特征值

下面是一个GATT连接成功后，从指定的特征值读取数据的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async read() {
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
        if (this.services.length > 0) {
            // 测试只尝试读取第一个服务的第一个特征值，如果需要读取其它特征值，请自行修改
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. 读取指定特征值
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

特征值写入方式枚举

- `1`：写入特征值后，对端蓝牙设备需要回复确认。
- `2`：写入特征值后，对端蓝牙设备不需要回复。

### `writeCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic, writeType: GattWriteType): Promise&lt;number&gt;
</pre></decl>

client端向指定的server端特征值写入数据，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

 - 该接口需要传入一个 [`BLECharacteristic`](#blecharacteristic) 类型的对象，表示需要写哪一个特征值
 - 该接口需要传入一个 [`GattWriteType`](#gattwritetype) 枚举值，用来表示数据的写入方式

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

此对象表示GATT描述符，其类型定义如下：

```ts
/**
 * GATT描述符类型定义, 是特征值BLECharacteristic的数据单元，用于描述特征值的附加信息和属性
 */
type BLEDescriptor = {
    serviceUuid: string; // 特征值所属的服务UUID, 例如：00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // 特征值UUID, 例如：00002a11-0000-1000-8000-00805f9b34fb
    descriptorUuid: string; // 描述符UUID, 例如：00002902-0000-1000-8000-00805f9b34fb
    descriptorValue: ArrayBuffer; // 描述符的数据内容, 读取写数据时使用
    descriptorHandle: number; // 描述符的唯一标识句柄, 当server端BLE蓝牙设备提供了多个相同UUID描述符时，可以通过此句柄区分不同的描述符。
}
```

### `readDescriptorValue`
<decl method><pre>
(descriptor: BLEDescriptor): Promise&lt;BLEDescriptor&gt;
</pre></decl>

client端从指定的server端描述符读取数据，使用Promise异步回调。该接口异步返回一个 [`BLEDescriptor`](#bledescriptor) 类型的对象。

 - 该接口需要传入一个 [`BLEDescriptor`](#bledescriptor) 类型的对象，表示需要读取哪一个描述符

下面是一个GATT连接成功后，从指定的描述符中读取数据的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    descriptor: null,
    async read() {
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
            // 测试只尝试读取第一个服务的第一个特征值的第一个描述符，如果需要读取其它描述符，请自行修改
            // 需要注意的是，不是所有的特征值都有描述符，这里可以自行调整，选取有描述符且有读写权限的服务测试
            this.descriptor = this.services[0].characteristics[0].descriptors[0];
        }
        // 4. 读取指定描述符
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

client端向指定的server端描述符写入数据，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

 - 该接口需要传入一个 [`BLEDescriptor`](#bledescriptor) 类型的对象，表示需要写哪一个描述符

下面是一个GATT连接成功后，从指定的特征值写入数据的示例：
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

client端获取GATT连接链路信号强度 (Received Signal Strength Indication, RSSI)，使用Promise异步回调。该接口异步返回一个&lt;number&gt;类型的信号强度，单位：dBm

下面是一个GATT连接成功后，获取设备信号强度的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async rssi() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
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

client端获取GATT连接链路MTU（最大传输单元）大小，使用Promise异步回调。该接口异步返回一个&lt;number&gt;类型的长度，单位：byte

下面是一个GATT连接成功后，获取GATT连接链路MTU（最大传输单元）大小：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async mtu() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
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

client端同server端协商MTU（最大传输单元）大小，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

### `setCharacteristicChangeNotification`
<decl method><pre>
(characteristic: BLECharacteristic, enable: boolean): Promise&lt;number&gt;
</pre></decl>

client端启用或者禁用接收server端特征值内容变更通知的能力，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

 - 该接口需要传入一个 [`BLECharacteristic`](#blecharacteristic) 类型的对象，表示需要操作哪一个特征值
 - 该接口需要传日一个 boolean 值，表示开启还是关闭内容变更通知能力，true表示开启，false表示关闭

下面是一个GATT连接成功后，开启特征值内容变更通知的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async notify() {
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
        if (this.services.length > 0) {
            // 测试只尝试操作第一个服务的第一个特征值，如果需要操作其它特征值，请自行修改
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. 操作指定特征值
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeNotification(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Notification success')
                } else {
                    console.log('该特征值不允许设置开启监听，ResultCode:' + result);
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

client端启用或者禁用接收server端特征值内容变更指示的能力，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

 - 该接口需要传入一个 [`BLECharacteristic`](#blecharacteristic) 类型的对象，表示需要操作哪一个特征值
 - 该接口需要传日一个 boolean 值，表示开启还是关闭内容变更指示的能力，true表示开启，false表示关闭

下面是一个GATT连接成功后，开启特征值内容变更指示的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async indication() {
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
        if (this.services.length > 0) {
            // 测试只尝试操作第一个服务的第一个特征值，如果需要操作其它特征值，请自行修改
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. 写指定特征值
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeIndication(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Indication success')
                } else {
                    console.log('该特征值不允许设置开启监听，ResultCode:' + result);
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

client端订阅server端特征值变化事件。当特征值发生变化时，会自动调用 `callback` 回调函数。该接口同步返回一个订阅ID，用于取消订阅。

回调函数参数字段说明：
- [`BLECharacteristic`](#blecharacteristic) ：发生变化的特征值对象。

下面是一个GATT连接成功后，开启特征值内容变更指示的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
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
        // 3. 订阅特征值变化
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

client端取消订阅server端特征值变化事件。参数 `subscribeId` 为 [`subscribeBLECharacteristicChange`](#subscribeblecharacteristicchange) 方法返回的订阅ID。

下面是一个GATT连接成功后，开启特征值内容变更指示的示例：
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
        // 3. 取消订阅特征值变化
        if (this.listener) {
            this.gattClient.unsubscribeBLECharacteristicChange(this.listener)
            this.listener = null
        }
    },
}
```

### `ConnectionState`

蓝牙连接状态枚举

- `0`：已断开连接
- `1`：正在连接
- `2`：已连接
- `3`：正在断开连接 

### `GattDisconnectReason`

GATT链路断开原因枚举

- `0`：原因不可用
- `1`：连接超时
- `2`：对端设备主动断开连接
- `3`：本端设备主动断开连接
- `4`：未知断连原因

### `BLEConnectionChangeState`

此对象用于表示蓝牙连接状态，其类型签名如下：

```ts
/**
 * 蓝牙连接状态类型定义
 */
type BLEConnectionChangeState = {
    deviceId: string; // 设备 ID（例如："AA:BB:CC:DD:EE:FF"）
    state: ConnectionState; // 蓝牙连接状态
    reason: GattDisconnectReason; // GATT链路断开的原因
}
```

### `subscribeBLEConnectionStateChange` 
<decl method><pre>
(callback: Callback(connectionChangeState: BLEConnectionChangeState) => void): number
</pre></decl>

client端订阅GATT协议的连接状态变化事件。当连接状态发生变化时，会自动调用 `callback` 回调函数。该接口同步返回一个订阅ID，用于取消订阅。

回调函数参数字段说明：
- [`BLEConnectionChangeState`](#bleconnectionchangestate) ：连接状态。

下面是一个GATT连接成功后，订阅连接状态的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
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
        // 3. 订阅连接状态的变化
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

client端取消订阅GATT协议的连接状态变化事件。参数 `subscribeId` 为 [`subscribeBLEConnectionStateChange`](#subscribebleconnectionstatechange) 方法返回的订阅ID。

下面是一个取消订阅连接状态的示例：
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
        // 3. 订阅连接状态的变化
        this.listener = this.gattClient.subscribeBLEConnectionStateChange((result) => {
            console.log('connect changed:' + JSON.stringify(result))
        })
        // 4. 取消订阅连接状态的变化
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

client端订阅MTU（最大传输单元）大小变更事件。当MTU发生变化时，会自动调用 `callback` 回调函数。该接口同步返回一个订阅ID，用于取消订阅。

回调函数参数字段说明：
- mtu ：MTU（最大传输单元）大小。

下面是一个GATT连接成功后，订阅MTU变化的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 订阅MTU的变化
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

client端取消订阅MTU（最大传输单元）大小变更事件。参数 `subscribeId` 为 [`subscribeBLEMtuChange`](#subscribeblemtuchange) 方法返回的订阅ID。

下面是一个取消订阅MTU变化的示例：
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
FILE_PATH: src/original_docs/api/system-router.md

# 页面路由

## 导入模块

``` js
import router from '@system.router'
```

## 接口定义

### `push` <decl type="(options: {uri: string, params?: Object}): Promise<any>" method />

跳转到应用内的指定页面。`options` 参数属性说明：
- `uri`：目标页面的名字，必须在 `mainfest.json` 中配置；
- `params`：跳转时需要传递的数据，`params` 参数的属性会替换目标页面的 `data` 属性值。

`push()` 返回一个 Promise 对象，它会在目标页面退出之后兑现并返回自定义的结果。例如：
```js
const result = await router.push({ uri: 'PageName' })
console.log("the page 'PageName' was closed with the result:", result)
```
其中 `result` 是由 [`close()`](#close) 方法指定的页面返回值，你可以通过上面的方法来获取。

::: warning
页面的返回时间通常取决于用户操作，所以 `await router.push()` 可能会等待很长时间。如果不需要获取页面的返回值则不建议通过 `await` 等待页面返回。
:::

当页面为 `singleTask` 启动模式时，跳转到一个已经打开的页面类似于 [`back('<page-name>')`](#back)，见 [`launchMode`](/framework/application/manifest.md#launchmode) <version-badge since="0.8" />。

### `replace` <decl type="(options: {uri: string, params?: Object}): Promise<boolean>" method />

跳转到应用内的指定页面并关闭当前页面。`options` 参数属性说明：
- `uri`：目标页面的名字，必须在 `mainfest.json` 中配置；
- `params`：跳转时需要传递的数据，`params` 参数的属性会替换目标页面的 `data` 属性值。

与 [`push()`](#push) 和 [`back()`](#back) 一样，调用 `replace()` 总是会播放标准的页面转场动画。即使在代码中**立即**调用 `replace()`，只要当前页面已经进入渲染阶段，用户仍然有可能短暂地看到当前页面的一帧画面，然后再进入目标页面。因此，`replace()` 更适合用于“当前页面本身就是用户流程的一部分”的场景，而不适合作为“静默重定向”、“完全隐藏入口页”的手段。

如果当前页面是通过 [`push()`](#push) 方法弹出的，由于 `replace()` 方法会替换当前页面，这会导致 [`push()`](#push) 返回的 Promise 对象兑现。

::: tip
不要使用 [`push()`](#push) 方法跳转到新页面并立即 [`close()`](#close) 当前页面来实现页面替换，这样会打断交互动效，甚至出现画面闪烁。请始终用 `replace()` 方法来替换页面，以保证平滑的页面转场体验。

此外，如果希望某个入口页（例如 `manifest.json` 中配置的 `router.entry` 页面、仅用于分发的隐私检查页等）在部分场景下**完全不展示**，不要在该页面内部调用 `replace()` 试图“立刻跳走”。这类需求应当通过[替换默认页面](#替换默认页面)的方式，在应用启动早期（如 `onCreate()` / `onRoute()`）直接 `push()` 出真正的首屏页面。
:::

`replace()` 常用于[开屏界面跳转](#开屏界面跳转)等场景。

当页面为 `singleTask` 启动模式时，跳转到一个已经打开的页面类似于 [`back('<page-name>')`](#back)，见 [`launchMode`](/framework/application/manifest.md#launchmode) <version-badge since="0.8" />。

### `back` <decl type="(name?: string): Promise<boolean>" method />

返回到名为 `name` 的页面，如果 `name` 为空或者不传递这个参数，`router.back()` 就返回到上一级页面。

调用 `back()` 方法会导致弹出相关页面的 [`push()`](#push) 方法所返回的 Promise 兑现。

### `close` <decl type="(page: Component, result?: any): Promise<void>" method />

关闭指定页面。`page` 是一个页面的 view-model 对象。例如：
``` js
router.close(this.$page)
```

`router.close()` 方法可以关闭应用内的任意页面。如果目标页面位于页面栈顶端，那么 `router.close()` 和 `router.back()` 等效。`router.close()` 还可以正确关闭悬浮页面。

可选参数 `result` 用于指定页面的返回值，即弹出该页面的 [`router.push()`](#push) 或 [`prompt.showPopup()`](system-prompt.md#showpopup) 返回的 Promise 兑现时的结果。考虑到有很多种方法退出页面（如用户侧滑、`router.back()` 方法等），你可以在页面组件的 [`onDestroy()`](/framework/component/life-cycle.md#ondestroy) 生命周期函数中显式调用 `close()` 方法以确保传递页面返回值：
```js
import router from '@system.router'

export default {
  // 这是一个组件对象 ...
  onDestroy() {
    router.close(this.$page, this.pageResult)
  },
  // 假设某个方法会设置页面返回值
  someMethod() {
    this.pageResult = { message: 'some page result' }
  },
}
```

::: tip
在页面 `onDestroy()` 返回前多次对页面调用 `router.close()` 方法**并传递了 `result` 参数**时，仅最后一次调用会生效为页面的返回值。这也是建议在 `onDestroy()` 生命周期函数中通过 `close()` 方法来返回值的原因。
:::

### `clear` <decl type="(): Promise<void>" method />

清空所有底层页面，仅保留顶层页面。调用 `clear()` 方法不会播放页面转场动画。在退出所有底层页面之后兑现本方法返回的 Promise 对象。

### `getPages` <decl type="(): Component[]" method />

获取当前应用页面栈中所有页面的页面组件。

### `getLength` <decl type="(): number" method />

获取当前应用页面栈中页面数量。

### `getPagesName` <decl type="(): String[]" method />

获取当前应用页面栈中所有页面的名称。

### `getPage` <decl type="(index: number): Component | undefined" method />

获取当前应用中由 `index` 指定的页面组件。`index` 是页面的索引（即在页面栈中的位置）。如果查找的页面不存在则返回 `undefined`。

### `getIndex` <decl type="(component: Component): number | undefined" />

获取当前应用中由页面组件 `component` 指定的页面索引。如果查找的页面不存在则返回 `undefined`。

### `queryPage` <decl type="(name: string): Component[]" />

获取页面栈中名为 `name` 的所有页面列表，页面列表和页面栈的顺序相同。

### `queryIndex` <decl type="(name: string): number[]" />

获取页面栈中名为 `name` 的所有页面索引，页面索引值的顺序和页面栈的顺序相同。

## 开发笔记

### 重复弹出页面

错误地使用 `router.push()` 方法可能导致重复弹出同一个页面。考虑这样一个元素：
``` html
<p on:click="onClick">Click Me!</p>
```
当组件的 `onClick()` 事件回调方法只是简单地弹出新页面时不会有任何问题：
``` js
export default{
  onClick() {
    router.push({ uri: 'CoverPage' })
  }
}
```
因为页面在播放转场动画（如果有的话）时不会响应手势，因此不会重复调用 `router.push()`。但是，如果 `onClick()` 在异步操作之后再调用 `router.push()` 就可能出问题，例如：
``` js
export default{
  async onClick() {
    // 这里使用一秒钟的定时器模拟异步操作。真实的异步操作，
    // 如文件读写、网络状态查询也会出现相同的问题
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    // 在异步操作之后再调用 router.push()
    router.push({ uri: 'CoverPage' })
  }
}
```
如果用户在异步操作（示例中为定时器）期间多次点击 “Click Me!” 按钮就会重复弹出页面。你可以尝试下面的 demo 来验证它：

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

首先，请在一秒钟内迅速多次点击 “Click Me!” 按钮，这会导致重复弹出 Cover Page，你可以通过该页面显示的计数来观察重复弹出的次数。

接下来，点击 Cover Page 或者右滑即可返回到上一级页面。此时你会发现：无论怎样快速、连续地点击，页面总是逐个返回，而不会重复操作，因为转场动画期间不会响应手势。

#### 避免异步操作

如果要在手势操作（如 click 手势）的回调函数中跳转页面，应当避免异步操作，因为这不仅容易导致重复弹出页面，还会增加手势响应的延迟。尤其是要注意某些异步操作的延迟是不可控的，例如弱网环境下检查在线状态可能要很长时间。

因此，在需要通过点击触发页面跳转的场景中，最好将可能的网络访问转移到新页面中，并通过加载动画来呈现忙状态。

#### 规避方法

如果必须在手势触发的页面跳转之前进行异步操作，请务必通过特定的标志位来避免重复跳转页面。以前面的 `onClick()` 回调为例：
``` js
export default {
  async onClick() {
    // 添加 isClicked 标志来跳过重复操作，不需要是响应式属性
    if (this.isClicked)
      return
    // 开始执行手势响应逻辑之前标记 isClicked
    this.isClicked = true
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    router.push({ uri: 'CoverPage' })
    // 结束执行手势响应逻辑之后清除 isClicked
    this.isClicked = false
  }
}
```
使用相同的方式连续点击 “Click Me!” 按钮将不会重复弹出 Cover Page：

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

这个示例也证实了异步操作确实会增加页面跳转的延迟，在等待定时器超时的一秒钟内用户看不到任何返回！

### 替换默认页面

开发者可能不希望应用在启动时进入 `manifest.json` 的 [`router.entry`](/framework/application/manifest.md#entry) 页面。典型的场景是在通过 deeplink 启动应用时，根据具体的请求参数跳转到特定页面，而不是进入 entry 页面。

除了 deeplink 以外，应用在冷启动时还经常需要根据本地状态选择不同的首屏，例如根据登录态决定进入登录页或首页，或者根据本地存储的隐私协议同意标记决定进入隐私页或功能首页。如果直接把这些页面之一配置为 `router.entry`，再在该页面内部通过 [`router.replace()`](#replace) 跳转，就会在某些情况下短暂显示出不需要的页面，看起来像是页面“闪了一下”。

为此，你只需要在应用启动阶段的 [`onShow()`](/framework/component/life-cycle.md#onshow-1) 生命周期函数调用之前，通过 [`router.push()`](#push) 弹出你真正想要展示的页面即可。通常可以在应用的 [`onCreate()`](/framework/component/life-cycle.md#oncreate) 或 [`onRoute()`](/framework/component/life-cycle.md#onroute) 生命周期函数中完成本地状态检查并跳转首页。例如，`app.ux`/`app.js` 的 `onCreate()` 中同步读取存储的隐私协议状态，然后直接跳转到隐私页或首页：
```js
// app.js
import router from '@system.router'
import storage from '@system.storage'

export default {
  onCreate() {
    const agreed = storage.get('privacyAgreed')
    if (agreed) // 用户已同意隐私协议，直接进入功能首页
      router.push({ uri: 'MainPage' })
    else // 用户尚未同意隐私协议，首屏展示隐私页面
      router.push({ uri: 'PrivacyPage' })
  }
}
```
一旦开发者在应用启动早期手动跳转了页面，本次启动实际显示给用户的**首屏页面**就是通过 `router.push()` 弹出的目标页面，`manifest.json` 中的 `router.entry` 仅作为内部入口使用，不会在界面上短暂闪现。

### 开屏界面跳转

许多应用在首次进入时会显示一个开屏 logo 页面，然后再跳转到实际的功能首页。典型的路由结构是：`router.entry` 指向 logo 页面，logo 页面在初始化时通过 [`router.replace()`](#replace) 跳转到首页。这样，应用启动后用户首先看到短暂的开屏画面，随后看到从开屏页过渡到首页的动画，开屏页在跳转后会从页面栈中移除。
``` js
// 假设这是 logo 页面的 index.ux 脚本
export default {
  onInit() {
    // 在开屏 logo 页面延时一段时间之后跳转
    setTimeout(() => {
      router.replace({ uri: 'MainPage' })
    }, 1000)
  },
}
```
在这种结构下，logo 页面本身就是产品设计的一部分，因此用户短暂看到 logo 再过渡到首页是预期行为。需要注意的是，`replace()` 只能保证从 logo 页面到首页的过渡动画平滑，logo 页面的首帧仍然会出现在屏幕上，无法被“静默”跳过。

如果应用没有设计单独的 logo 或开屏页面，却仍然采用“入口页面 + `replace()` 跳转”的方式，例如将隐私协议页配置为 `router.entry` 并在其中通过 `replace()` 切换到首页，用户就会在冷启动应用时看到该入口页面“闪一下”，然后通过过渡动画切换到 `MainPage`。

::: tip
这种现象是由于路由机制本身决定的，如果你不希望用户观察到“页面切换”。应优先结合[替换默认页面](#替换默认页面)一节中的做法，在应用启动阶段通过 `router.push()` 直接选择最终首屏，而不是在入口页面内部用 `replace()` 把自己替换掉。
:::


============================================================
FILE_PATH: src/original_docs/api/system-configuration.md

# 应用配置

## 导入模块

```js
import configuration from '@system.configuration'
```

## 接口定义

### `getLocale`
<decl method><pre>
(): {
  language: string,
  countryOrRegion: string,
}
</pre></decl>

获取应用当前的语言环境。默认会使用系统的语言环境，可能因为设置或系统语言环境改变而发生变化。
 - `language` 表示当前的语言，如 'zh'、'en' 等, 
 - `countryOrRegion` 表示当前国家或地区，如 'CN'、'US' 等。


============================================================
FILE_PATH: src/original_docs/api/system-file.md

# 文件系统操作

本模块提供 Promise 风格的文件系统操作 API。相比于 callback 风格，Promise 风格可避免回调地狱以降低代码复杂度。

::: warning
由于回调式文件 API 在时序、并发和错误处理上极易埋坑，强烈建议使用 [Promise/`await` API](./README.md#快应用异步接口)；详细建议请参考[常见陷阱和建议](#常见陷阱和建议)。

`@system.file` 中的 API 都是[异步文件操作](#异步文件操作)，这和同步的 IO 访问有本质区别。请务必理解异步编程的基本概念，并且熟悉 Promise 和 `async/await` 的用法。
:::

## 导入模块

``` js
import file from '@system.file'
```

## 使用说明

### 错误码

返回的错误码含义为：
- `202`：参数错误；
- `300`：IO 操作失败；
- `400`：权限不足；

## 接口定义

### `readText`
<decl method><pre>
(params: {
  uri: string
}): Promise&lt;string>
</pre></decl>

读取文本文件的内容。`params` 参数字段描述：
- `uri`：待读取文件的 URI。

### `writeText`
<decl method><pre>
(params: {
  uri: string,
  text: string,
  append?: boolean
}): Promise&lt;void>
</pre></decl>

将文本写入到文件中，如果文件不存在则会创建新文件。此函数还会自动创建父级目录。`params` 参数字段：
- `uri`：待写入文件的 URI。
- `text`：要写入文件的文本内容。
- `append`：值为 `true` 将数据追加写入到文件的尾部，值为 `false` 覆盖原有内容。默认 `false`。

### `read`
<decl method><pre>
(params: {
  uri: string,
  position?: number,
  length?: number
}): Promise&lt;ArrayBuffer>
</pre></decl>

读取文件内容到一个 `ArrayBuffer` 对象中。`params` 参数字段：
- `uri`：待读取文件的 URI。
- `position`：文件读取位置的偏移量，默认为 $0$。
- `length`：期望读取的字节数，如果不指定则读取到文件尾部。

### `write`
<decl method><pre>
(params: {
  uri: string,
  data: ArrayBuffer,
  position?: number,
  append?: boolean
}): Promise&lt;void>
</pre></decl>

将 `ArrayBuffer` 中的字节数据写入到文件中，如果文件不存在则会创建新文件。此函数还会自动创建父级目录。

`params` 参数字段说明：
- `uri`：待写入文件的 URI。
- `data`：待写入的数据。
- `position`：文件写入位置的偏移量，默认为 $0$。
- `append`：值为 `true` 将数据追加写入到文件尾部并忽略 `position` 参数。

### `copy`
<decl method><pre>
(params: {
  srcUri: string,
  dstUri: string
}): Promise&lt;void>
</pre></decl>

将源文件复制到指定位置，会自动创建目标目录。`params` 参数字段：
- `srcUri`：源文件的 URI。
- `dstUri`：目标文件的 URI。

### `rename`
<decl method><pre>
(params: {
  oldUri: string,
  newUri: string
}): Promise&lt;void>
</pre></decl>

重命名文件或者目录，会自动创建目标目录。`params` 参数字段：
- `oldUri`：重命名之前文件或者目录的 URI。
- `newUri`：重命名之后的 URI。

### `list`
<decl method><pre>
(params: {
  uri: string,
}): Promise&lt;Array>
</pre></decl>

列出指定目录下的所有项目（文件或目录）列表。`params` 参数字段：
- `uri`：带列举的目录 URI，应用资源包中的文件不支持列举。

`Promise` 的参数是一个包含文件信息的数组，形如
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
你不能列举应用资源包内的文件，因此 `await file.list({ uri: "/assets/images" })` 等直接使用[路径](/framework/application/resource.md#uri-和路径)的用法都是无效的。事实上，应该使用各种 [`internal`](/framework/application/resource.md#internal) URI 协议。
:::

### `access`
<decl method><pre>
(params: {
  uri: string
}): Promise&lt;boolean>
</pre></decl>

检查一个文件是否存在。`params` 参数字段：
- `uri`：待检测的文件 URI。

### `mkdir`
<decl method><pre>
(params: {
  uri: string,
  recursive?: boolean
}): Promise&lt;void>
</pre></decl>

创建一个目录。`params` 参数字段：
- `uri`：待创建目录的 URI。
- `recursive`：是否要递归创建（如果父级目录不存在则先创建父级目录），默认为 `false`。

### `remove`
<decl method><pre>
(params: {
  uri: string,
  recursive?: boolean
}): Promise&lt;void>
</pre></decl>

删除一个目录或文件。`params` 参数字段：
- `uri`：待创建目录的 URI。
- `recursive`：是否要递归删除，默认为 `false`。不递归删除时只能删除文件或者空的目录。

### `stat`
<decl method><pre>
(options: {
  uri: string
}): Promise&lt;{size: number}>
</pre></decl>

获取文件的属性信息。`options` 参数各字段描述如下：
- `uri`：待获取属性的文件 URI。

`stat()` 异步返回一个对象，包含以下文件属性：
- `size`：文件的尺寸，单位为字节。

## 常见陷阱和建议

以下示例均基于“回调式”写法的典型问题，展示其在文件 IO 中为何极易失效或难以维护，并给出 Promise/`await` 的等价重写。

### 异步文件操作

`@system.file` 模块中的所有 API 都是**异步操作**。这意味着当你调用文件操作函数时，函数会**立即返回**，而不会等待实际的 I/O 操作完成。文件的读写操作会在后台进行，操作完成后会通过 Promise 通知你结果。

::: danger 新手必读
如果你不熟悉异步编程，请务必认真阅读本节内容。**忽略异步操作的返回值**或**不等待 Promise 完成**会导致严重的程序错误，这些错误在模拟器中可能不会表现出来，但在真实设备上会导致数据丢失或程序错误。
:::

#### 什么是异步操作？

在同步编程中，代码按顺序执行，每一行代码执行完毕后才会执行下一行：

```js
// 同步代码示例（伪代码，file API 不提供同步版本）：阻塞等待文件读取
const text = file.readTextSync({ uri: 'internal://files/data.txt' });
console.log(text); // 必然会输出文件内容
console.log('读取完成');
```

但在异步编程中，I/O 操作不会阻塞代码执行。当你调用异步函数时，它会立即返回一个 Promise 对象，实际的文件操作在后台进行：

```js
// 错误：忽略 Promise，不等待操作完成（调用立即返回）
file.readText({ uri: 'internal://files/data.txt' });
console.log('这行代码会立即执行，此时文件可能还没读完！');

// 正确：使用 await 等待操作完成
const text = await file.readText({ uri: 'internal://files/data.txt' });
console.log(text); // 此时文件已经读取完成，可以安全使用
console.log('读取完成');
```

#### 为什么必须使用 await？

不使用 `await` 等待异步操作完成会导致以下严重问题。

数据尚未准备好就被使用：
```js
// 错误示例：忽略返回值
function loadConfig() {
  let config = null;
  file.readText({ uri: 'internal://files/config.json' })
    .then(text => config = JSON.parse(text)); // 这个回调函数会在未来某个时刻执行
  // 这里 config 仍然是 null，因为文件读取还没完成！
  console.log(config.theme); // 错误：试图访问 null.theme，会崩溃
  return config; // 返回 null
}

// 正确示例：等待数据准备好
async function loadConfig() {
  const text = await file.readText({ uri: 'internal://files/config.json' });
  const config = JSON.parse(text);
  console.log(config.theme); // 正确：文件已读取，可以安全访问
  return config; // 返回实际的配置对象
}
```

操作顺序混乱：
```js
// 错误示例：不等待写入完成
async function saveAndLoad() {
  // 写入新数据，但不等待完成
  file.writeText({ uri: 'internal://files/score.txt', text: '100' });
  
  // 立即读取，此时写入可能还没完成，读到的可能是旧数据！
  const score = await file.readText({ uri: 'internal://files/score.txt' });
  console.log(score); // 可能输出旧值，而不是 '100'
}

// 正确示例：等待写入完成后再读取
async function saveAndLoad() {
  // 用 await 等待写入完成
  await file.writeText({ uri: 'internal://files/score.txt', text: '100' });
  
  // 现在读取，确保读到的是刚写入的数据
  const score = await file.readText({ uri: 'internal://files/score.txt' });
  console.log(score); // 输出 '100'
}
```

资源竞争和数据损坏：

```js
// 错误示例：多次并发写入同一个文件
async function appendLog(message) {
  const log = await file.readText({ uri: 'internal://files/log.txt' });
  // 不用 await 等待写入完成，继续执行
  file.writeText({ uri: 'internal://files/log.txt', text: log + message + '\n' });
}

// 并发调用：不 await appendLog
appendLog('事件A'); // 读取 -> 写入 A
appendLog('事件B'); // 读取 -> 写入 B
// 结果：两次读取可能都读到同样的旧内容，后一次写入会覆盖前一次，导致 '事件A' 丢失

// 正确示例：等待每次写入完成
async function appendLog(message) {
  const log = await file.readText({ uri: 'internal://files/log.txt' });
  await file.writeText({ uri: 'internal://files/log.txt', text: log + message + '\n' });
}

// 串行调用
await appendLog('事件A'); // 完整的读取 -> 写入 -> 完成
await appendLog('事件B'); // 完整的读取 -> 写入 -> 完成
// 结果：两个事件都被正确记录
```

#### 模拟器陷阱

::: warning 模拟器无法暴露所有异步问题
在开发用的模拟器中，由于电脑的 I/O 速度极快，文件操作几乎是瞬间完成的。因此，即使代码没有正确使用 `await`，在模拟器中也可能看起来“正常工作”。
:::

真实的嵌入式设备上的文件系统 I/O 则存在以下限制：
- Flash 存储器的读写速度较慢；
- 文件系统缓存能力弱，读写文件通常直接访问存储介质；
- 系统资源有限，I/O 操作会被排队延迟。

没有使用 `await` 的代码在真实设备上**几乎必然会出错**！ 不要因为模拟器测试通过就忽略异步编程规范。

#### 正确使用 async/await 的规则

1. 任何调用文件 API 的函数都应该声明为 `async`：
   ```js
   async function saveData(data) {
     await file.writeText({ uri: 'internal://files/data.txt', text: data });
   }
   ```
2. 所有文件操作前都加上 `await` 关键字：
   ```js
   const content = await file.readText({ uri: 'internal://files/data.txt' });
   ```
3. 使用 `try/catch` 处理可能的错误：
   ```js
   try {
     await file.writeText({ uri: 'internal://files/data.txt', text: 'hello' });
   } catch (err) {
     console.error('写入失败:', err);
   }
   ```
4. 需要顺序执行的操作必须依次 `await`：
   ```js
   // 正确：先写入，再读取验证
   await file.writeText({ uri: 'internal://files/data.txt', text: 'test' });
   const verify = await file.readText({ uri: 'internal://files/data.txt' });
   console.log(verify === 'test' ? '验证成功' : '验证失败');
   ```
5. 不相关的操作可以并行执行，但要等待全部完成：
   ```js
   // 正确：并行读取多个文件，但等待全部完成
   const [file1, file2, file3] = await Promise.all([
     file.readText({ uri: 'internal://files/a.txt' }),
     file.readText({ uri: 'internal://files/b.txt' }),
     file.readText({ uri: 'internal://files/c.txt' })
   ]);
   ```

#### 完整示例：用户配置管理

```js
import file from '@system.file'

const CONFIG_URI = 'internal://files/user-config.json';

// 正确的异步配置管理
class ConfigManager {
  async load() {
    try {
      const text = await file.readText({ uri: CONFIG_URI });
      return JSON.parse(text);
    } catch (err) {
      // 文件不存在或格式错误，返回默认配置
      console.warn('加载配置失败，使用默认值:', err.message);
      return { theme: 'dark', language: 'zh-CN' };
    }
  }

  async save(config) {
    try {
      const text = JSON.stringify(config, null, 2);
      await file.writeText({ uri: CONFIG_URI, text });
      console.log('配置已保存');
    } catch (err) {
      console.error('保存配置失败:', err.message);
      throw err; // 重新抛出，让调用者知道保存失败
    }
  }

  async update(changes) {
    // 读取 -> 修改 -> 保存的完整流程
    const config = await this.load();
    Object.assign(config, changes);
    await this.save(config);
    return config;
  }
}

// 使用示例
async function main() {
  const manager = new ConfigManager();
  // 加载配置
  const config = await manager.load();
  console.log('当前主题:', config.theme);
  // 更新配置
  await manager.update({ theme: 'light' });
  console.log('主题已更新');
}

// 注意：main 本身也是异步的，需要正确调用
main().catch(err => {
  console.error('程序执行出错:', err);
});
```

#### 小结

- 所有 `@system.file` API 都是异步的，必须使用 `await` 等待完成。
- 不使用 `await` 会导致严重问题，例如数据未准备、操作乱序、错误丢失、数据损坏。
- 模拟器测试通过不等于代码正确，真实设备上 I/O 更慢，问题会暴露。
- 使用 `async/await` + `try/catch` 是正确且最简洁的写法。
- 永远不要忽略 Promise 的返回值。

### 回调陷阱

#### 回调顺序错觉与竞态覆盖

该类场景涉及一组文件被读-改-写的操作序列。这是使用回调参数触发回调风格的问题代码：
```js
// 期望对计数文件 +1，但两个并发调用可能相互覆盖
function increment(uri, done) {
  file.readText({
    uri,
    success(text) {
      const n = Number(text || '0') + 1;
      console.log(`read ${text}, write ${n}`);
      // readText() 成功回调中嵌套写文件操作
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

// 先建 counter 文件，然后并发触发两次 +1
file.writeText({
  uri: 'internal://files/counter',
  text: '0',
  success() {
    // 并发触发两次 increment，但是不做任何同步
    increment('internal://files/counter');
    increment('internal://files/counter');
  }
})
```
运行该脚本后，可能只会看到两条 `read 0, write 1` 日志，并且最终 `counter` 文件内容为 `1`，而不是期望的 `2`。失败机制为：两次 read 都读到相同旧值，后写覆盖先写，导致结果只 +1。

::: note
上面的脚本看起来十分复杂，难以正确地传递 `done` 回调函数，这很容易诱导为错误的实现。实际上，使用 `async/await` 重写后，代码会变得非常简洁且易于理解。
:::

一个复杂的技巧是使用互斥 + 串行化技术，这可以完全保留原有的并发 `increment` 语义，并保证整个读文件 + 递增计数操作的原子性：
```js
// 基于 Promise 链的按 key 互斥执行
const lock = new Map();

/**
 * 串行地执行同一个 key 的异步任务。这是一个工具函数。
 * @param {string} key
 * @param {() => Promise<any>} fn
 * @returns {Promise<any>} 返回 fn 的结果
 */
function withLock(key, fn) {
  // 取到该 key 之前的“尾巴”（没有则用已完成的 Promise）
  const prev = lock.get(key) || Promise.resolve();
  // 即便 prev 失败，也要继续后续队列，所以先 .catch(() => {})
  const p = prev.catch(() => {}).then(async () => {
    try {
      return await fn(); // 真正的任务只在轮到它时才执行
    } finally {
      // 如果自己仍是当前尾巴，说明没有新的任务进来，可以清理
      if (lock.get(key) === p) lock.delete(key);
    }
  });
  lock.set(key, p); // 把新的尾巴挂上去
  return p;
}

// 现在，increment 内部的实际 IO 由 withLock 串行化：
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
  // 并发触发两次 increment，同样不做任何同步
  increment('internal://files/counter');
  increment('internal://files/counter');
});
```
运行该脚本后，`counter` 文件内容必然为 `2`，且日志顺序必然为 `read 0, write 1` → `read 1, write 2`。

但是这样的代码看起来十分复杂，最简单的办法是直接 `await increment()` 调用（表现为 `await` 传染）：
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
  // 使用 await 等待 increment，保证顺序
  await increment('internal://files/counter');
  await increment('internal://files/counter');
})
```

#### 回调层级与资源泄漏

以下示例展示了回调式写法中，因多层嵌套和分支过多而导致的资源泄漏和逻辑错误：

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
            // 某些分支忘记 stopBusyIndicator() 或 cb()
          }
        });
        // 这也是错的，因为 writeText() 是异步的，并可能尚未完成
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

由于回调嵌套层级太深，`stopBusyIndicator()` 和 `cb()` 容易出现遗漏或误用：
- 遗漏清理逻辑，导致“忙指示器”永远不停止，或者调用方永远得不到回调；
- 过早调用了清理逻辑，导致调用方误以为写入已完成。

推荐写法（结构化清理）：

```js
async function exportReport(uri) {
  startBusyIndicator();
  try {
    const t = await file.readText({ uri });
    const out = await transform(t);
    await file.writeText({ uri: `${uri}.bak`, text: out });
  } finally {
    stopBusyIndicator(); // 总是在文件 IO 都完成（或异常）后调用
  }
}
```

#### 混用 await 与回调导致风格切换（await 失效）

任何回调处理函数都不会返回 Promise 对象，使 `await` 等待失效：

```js
// 因为传入了 complete 回调，该调用会启用回调风格，不会返回 Promise
await file.writeText({
  uri: 'internal://files/a.txt',
  text: 'x',
  complete() {}, // 不要传入 success/fail/complete 参数字段
});
// 上面这行不会真正等待写入完成，后续代码可能提前执行
```

推荐写法：

```js
// 使用 await 时不要传入 success/fail/complete
await file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
```

### 最佳实践

#### 明确的顺序与错误处理

```js
import file from '@system.file'

export async function updateConfig(uri, patch) {
  try {
    const text = await file.readText({ uri });
    const json = JSON.parse(text || '{}');
    Object.assign(json, patch);
    await file.writeText({ uri, text: JSON.stringify(json, null, 2) });
  } catch (err) {
    // 统一处理/记录错误，不要吞没
    console.error('updateConfig failed:', uri, err);
    throw err;
  }
}
```

要点是通过 `await` 明确串行时序；用 `try/catch` 保证错误被感知与上抛。如果完全不处理错误，运行时会记录异常日志，并中断整个调用链。

#### 避免 TOCTTOU（检查-使用竞态）

不要先 `access()` 后 `write*()` 再依赖两者之间的状态不变。例如这样的代码：

```js
file.access({
  uri: 'internal://files/a.txt',
  success(exists) {
    if (exists) {
      file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
    } else {
      // 如果文件不存在，先 mkdir 再写文件
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

推荐的写法是直接尝试写入，运行时会自动创建父目录：
```js
async function safeWriteText(uri, text) {
  try {
    await file.writeText({ uri, text });
  } catch (e) {
    // 这里应该处理错误，并且不需要 mkdir 后写文件
  }
}
```

#### 半写与崩溃中断

在 MCU 设备上，系统异常通常直接复位，应用不会在“半崩溃”状态下继续执行。即使应用被杀死，已经提交的文件写入操作也不会中断（但可能完全不执行），因此通常不需要担心“写一半文件”的问题：
```js
// 直接覆盖写，在电源中断/系统崩溃可能留下半写文件
file.writeText({ uri: '/data/config.json', text: bigJson });
```

对于关键的配置文件更新，可以使用“临时文件 + 同目录 rename”模式来加固稳定性：
```js
async function atomicWriteText(uri, text) {
  const tmp = `${uri}.tmp`;
  await file.writeText({ uri: tmp, text });
  await file.rename({ oldUri: tmp, newUri: uri });
}
```



============================================================
FILE_PATH: src/original_docs/api/system-media.md

# 多媒体

## 导入模块

``` ts
import media from '@system.media'
```

## 接口定义

### `createAudioPlayer` <decl type="(): AudioPlayer" method />

创建一个 [`AudioPlayer`](#audioplayer-对象) 对象。

### `createAudioRecord` <decl type="(): AudioRecorder" method />

创建一个 [`AudioRecorder`](#audiorecorder-对象) 对象。

开发者需要在 [`manifest.json`](/framework/application/manifest.md#permissions) 文件中声明应用对 `watch.permission.RECORD` 的访问权限。

### `setVolume` <decl type="(volume: number): void" method />

设置系统媒体音量，参数 `volume` 是 $[0.0, 1.0]$ 之间的音量值。此属性用于系统媒体音量的控制，具体功能取决于平台实现，调整音量应优先使用`AudioPlayer`对象的`volume`属性。

### `getVolume` <decl type="(): number" method />

获取系统媒体音量，结果是 $[0.0, 1.0]$ 之间的音量值。此属性用于系统媒体音量的获取，具体功能取决于平台实现，获取音量应优先使用`AudioPlayer`对象的`volume`属性。

## `AudioPlayer` 对象

::: details 类型签名
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

设置或读取需要播放音频的 url。支持[本地资源路径](/framework/application/resource.md#uri-和路径)与使用http、https协议的网络资源路径（例如：`https://www.rt-thread.com/service/test/001.mp3`）。下面是一个设置 src 然后开始播放的简单示例：

```ts
import media from '@system.media'
// 创建音频播放器
let player = media.createAudioPlayer()
// 设置需要播放的音频url
player.src = 'https://www.rt-thread.com/service/test/001.mp3'
// 开始播放音频
player.play()
```

### `name` <decl type="string" set get />

播放器对象的名字，如果不设置，默认为创建播放器的应用名。需要注意的是，播放器对象的名字并不是全局不唯一，并不能使用名字来标识播放器对象。

### `icon` <decl type="string" set get />

播放器对象的图标 url。支持[本地资源路径](/framework/application/resource.md#uri-和路径)

### `mode` <decl type="string" set get />

播放模式。该属性对应的功能应由播放器应用实现，播放器对象默认不处理，只提供该属性。

- `sequential`：顺序播放  
- `random`：随机播放  
- `singleloop`：单曲循环  
- `listloop`：列表循环  

### `status` <decl type="string" get />

读取当前播放器状态

- `play`：正在播放状态  
- `pause`：暂停播放状态  
- `stop`：停止播放状态 
- `ended`：播放结束状态  
- `error`：播放错误状态  

### `duration` <decl type="number" get />

音频总时长，单位：秒

### `position` <decl type="number" set get />

当前音频播放的时间位置，单位：秒

### `openSystemNotification` <decl type="bool" set get />

是否开启系统通知，默认不开启。开启后，此播放器对象才可以被[音频播放器管理器](/framework/application/system-audioPlayerManager.md#音频播放器管理器)查询到。

### `songAttribute` <decl type="songAttribute" set get />

歌曲属性对象

::: details 类型签名
```ts
type songAttribute = {
  title: string; // 歌曲的名称
  artist: string; // 表演者的名称，可以是个人或者乐队
  album: string; // 歌曲所属的专辑名称
  year: string; // 歌曲的发行年份
  genre: string; // 歌曲的类型，例如流行、摇滚、古典等
  track: string; // 当前歌曲在专辑中的编号，例如："1/12" 表示第1首，共12首
  coverArt: string; // 歌曲封面图片的url
  lyrics: string; // 歌词文本的 url
  comments: string; // 额外信息，如版权备注等
}
```
:::

songAttribute对象与AudioPlayer对象一样是一个Proxy对象，即不能使用JSON序列化与反序列化，也不能在响应式框架中引用。下面是一个简单的使用示例：

```ts
// 设置歌曲的名字
this.player.songAttribute.title = "未知"
// 设置歌曲演唱者
this.player.songAttribute.artist = "未知"
// 查看歌曲的名字
console.dir(this.player.songAttribute.title)
```

### `volume` <decl type="number" set get />

当前播放器的音量，范围：[0.0, 1.0]

### `nextAvailable` <decl type="bool" set get />

设置或查询是否可以切换下一曲

### `prevAvailable` <decl type="bool" set get />

设置或查询是否可以切换上一曲

### `play` <decl type="(): void" method />

开始播放在 src 属性中指定的音频

- 如果在调用此方法之前未设置 src 属性，会导致播放失败，触发 onerror 事件；
- 此方法为同步接口，执行此接口后，需要等待 onplay 事件或者 onerror 事件来判定播放成功或失败，在事件未触发之前，执行的额其它操作会被忽略；  

下面是一个调用play() 接口的简单示例：

```ts
import media from '@system.media'
// 创建音频播放器
let player = media.createAudioPlayer()
// 设置需要播放的音频url
player.src = 'https://www.rt-thread.com/service/test/001.mp3'
// 设置 onplay 事件
player.onplay = () => { console.dir("开始播放") }
// 设置 onerror 事件
player.onerror = () => { console.dir("播放错误") }
// 开始播放音频
player.play()
```

### `pause` <decl type="(): void" method />

暂停播放当前音频  

- 此方法为同步接口，执行此接口后，需要等待 onpause 事件或者 onerror 事件来判定暂停成功或失败，在事件未触发之前，执行的额其它操作会被忽略；  

### `stop` <decl type="(): void" method />

停止音频播放，可以通过 play 重新播放音频  

- 此方法为同步接口，执行此接口后，需要等待 onstop 事件或者 onerror 事件来判定停止成功或失败，在事件未触发之前，执行的额其它操作会被忽略；  

### `release` <decl type="(): void" method />

释放音频资源  

- 执行此接口会停止播放当前音频，需要等待 onstop 事件或者 onerror 事件来判定停止成功或失败，在事件未触发之前，执行的额其它操作会被忽略；   

### `next` <decl type="(): void" method />

通知播放器应用，播放下一首。执行此接口后，会触发 onnext 事件通知监听此事件的播放器应用，由播放器应用执行歌曲切换的逻辑。

### `previous` <decl type="(): void" method />

通知播放器应用，播放下一首。执行此接口后，会触发 onprevious 事件通知监听此事件的播放器应用，由播放器应用执行歌曲切换的逻辑。

### `requestFocus` <decl type="({acquireType: string，volumeType: string}): void" method />

请求音频焦点。执行此接口后，会通知底层请求或者释放音频焦点，由底层控制不同类型音频的切换与打断逻辑。

`acquireType` 参数指示请求类型：
- `gain`：请求音频焦点
- `loss`：释放音频焦点

`volumeType` 参数指示音频类型：
- `system`：系统提示
- `media`：媒体音乐
- `tts`：语音播报

以下示例演示 `requestFocus` 函数请求音频焦点的方法：
``` ts
import media from '@system.media'
// 创建音频播放器
let player = media.createAudioPlayer()
// 获取媒体音乐类型的音频焦点
player.requestFocus({ volumeType: 'media', acquireType: 'gain' });
```

### `releaseFocus` <decl type="(): void" method />

释放音频焦点。执行此接口后，会通知底层释放音频焦点，由底层控制不同类型音频的切换与打断逻辑。

### `onplay` <decl type="?: () => void" set />

在音频 play 成功后的回调事件

### `onpause` <decl type="?: () => void" set />

在音频 pause 成功后的回调事件

### `onstop` <decl type="?: () => void" set />

在音频 stop 成功后的回调事件

### `onended` <decl type="?: () => void" set />

在音频播放结束后的回调事件

### `onerror` <decl type="?: () => void" set />

执行`play` `pause` `stop` `position`等接口发生错误的回调事件，发生错误时， 对应的 onplay 等事件不会被触发

### `ontimeupdate` <decl type="?: () => void" set />

在 position 属性更新时会触发的回调事件，此事件只有应用处于前台时才会触发，当应用处于后台时会停止派发。

### `oninterrupt` <decl type="?: (action: {interruptHint: number}) => void" set />

发生音频打断事件时的回调函数，当前音频被相同音频类型或其它音频类型的音频抢夺时，被暂时打断或彻底打断的通知。

`action` 参数的 `interruptHint` 指示打断事件的类型：
- `1`：短暂打断 （可以自动恢复，如：音乐被打断）
- `2`：彻底打断 （不可自动恢复，如：网易云被喜马拉雅打断）

以下示例演示注册 `oninterrupt` 回调函数的方法，该函数会在事件发生时调用：
``` js
player.oninterrupt = (action) => {
  console.log(action.interruptHint)
}
```

### `onnext` <decl type="?: () => void" set />

需要播放下一曲时的回调事件

### `onprevious` <decl type="?: () => void" set />

需要播放上一曲时的回调事件

### `onrequestplay` <decl type="?: () => void" set />

底层需要启动播放时触发该回调事件通知js应用，由js应用执行启动播放的逻辑

### `onrequestpause` <decl type="?: () => void" set />

底层需要暂停播放时触发该回调事件通知js应用，由js应用执行暂停播放的逻辑

### `onrequeststop` <decl type="?: () => void" set />

底层需要停止播放时触发该回调事件通知js应用，由js应用执行停止播放的逻辑

### `onsongattribute` <decl type="?: () => void" set />

歌曲属性对象发生变化时的回调事件

### `onposition` <decl type="?: () => void" set />

执行 `position` 设置当前音频播放的时间位置成功的回调事件

### `onrequestfocus` <decl type="?: () => void" set />

请求音频焦点成功时的回调事件

### `onreleasefocus` <decl type="?: () => void" set />

释放音频焦点成功时的回调事件

### `onmodechanged` <decl type="?: () => void" set />

播放模式发生变化时的回调事件

### `onvolumechange` <decl type="?: () => void" set />

播放器音量发生变化时的回调事件


## `AudioRecorder` 对象

::: details 类型签名
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

开始录制音频，`options` 参数的各字段功能为：
- `uri`：需要存储的录音文件 URI，只支持 `internal` 协议，会自动创建目录；
- `sample`：音频采样率，单位为 $\rm Hz$，默认为 $8000$；
- `layout`：音频数据位深度，默认为 $16$；
- `channel`：音频声道数，默认为 $1$；
- `bitrate`：音频码率，单位为 $\rm kbps$，默认为 $16$，码率越高，音质越好但文件也越大。
- `codec`：音频编码格式，字符串类型，如果不填写，则根据`format`参数自动匹配一个合适的编码；
- `format`：音频封装格式，字符串类型，如果不填写，则根据`uri`参数的后缀名自动匹配一个合适的封装；

  常用的录音格式、编码格式以及封装格式的支持关系如下（表格中的无，表示对应的参数可以不用填写）：

  | 常用的录音格式 | codec(编码格式) | format(封装格式) |
  | -------------- | --------------- | ---------------- |
  | pcm            | 无              | 无               |
  | mp3            | mp3             | 无               |
  | opus           | opus            | 无               |
  | opus-ogg       | opus            | ogg              |
  | silk           | silk            | 无               |

以下启动录音的示例代码：

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
关于 `internal` URI 协议的更多说明请参考[资源访问](/framework/application/resource.md)文档。
:::

在录制完成后，请调用 [stop()](#stop-1) 方法来结束录制。

### `read`
<decl method><pre>
(options: {
  callback: (buffer: ArrayBuffer) => void,
}): void
</pre></decl>

读取录制的音频数据（每次读取到的数据为从上次读取结束的位置开始到目前为止所有可用的数据）

### `stop` <decl type="(): void" method />

停止录制音频。调用此接口后，可以由其他模块读取 [`start()`](#start) 方法录制的音频文件（由 `uri` 参数指定）。

### `release` <decl type="(): void" method />

释放录制音频资源

### `onstart` <decl type="?: () => void" set />

在录制 start 后的回调事件

### `onstop` <decl type="?: () => void" set />

在录制 stop 后的回调事件

### `onrelease` <decl type="?: () => void" set />

在录制 release 后的回调事件

### `onavailable` <decl type="(data: ArrayBuffer) => void" set />

在录制开始后有新数据产生的回调事件

### `onerror` <decl type="?: () => void" set />

`start`、`stop` 或 `release` 事件发生错误的回调事件，发生错误时，对应的 onstart 等不会被触发

## 示例

### 录音

以下代码演示了录制 3 秒钟音频的最简单示例：
``` js
import media from "@system.media"

async function record() {
  // 创建录音对象
  let record = media.createAudioRecord()
  console.log('start record')
  // 只填写了 uri 参数，其他参数使用默认值
  await record.start({
    uri: 'internal://tmp/test.mp3'
  })
  setTimeout(() => {
    console.log('stop record')
    record.stop() // 延时 3 秒后停止录音
  }, 3000)
}

record()
```

调用 `record()` 函数时会创建一个录音对象，然后开始录音，并在 3 秒钟之后停止录音。录音会被记录到 `internal://tmp/test.mp3` 文件中，并以 MP3 格式编码。

该示例只为 [`AudioPlayer.start()`](#start) 方法传入了 `uri` 参数，`sample`、`layout` 、 `channel` 和 `bitrate` 均使用默认配置。

::: tip
使用模拟器时，可以到应用的数据目录找到录音文件并播放。`internal://tmp/test.mp3` 对应的文件路径是 `.glyphix-work/image/{device}/data/temp/{app-id}/test.mp3` 其中 `{device}` 和 `{app-id}` 是模拟时的设备名称和应用名称。
:::


============================================================
FILE_PATH: src/original_docs/api/system-cipher.md

# 密码算法

## 导入模块

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

`aes` 加解密，`options` 参数的各字段功能为：
- `action`：加解密的类型，两个可选值：`'encrypt'`：加密，`'decrypt'`：解密；
- `text`：待加密或解密的文本内容，待加密的文本应该是一段普通文本，待解密的文本应该是经过 `base64` 编码的一段二进制值；
- `key`：加密或解密使用到的密钥，经过 `base64` 编码后生成的字符串，密钥没有经过 `bsae64` 解码之前必须是 $16$ 字节的倍数；
- `transformation`：`AES` 算法的加密模式 (`ECB'`, `'CBC'`, `'CFB'`, `'CTR'`, `'OFB'`) 和填充项，默认为 `'AES/CBC/PKCS5Padding'`。AES 填充项可选填充项为：
  - `'PKCS5Padding'`
  - `'PKCS7Padding'`
  - `'NoPadding'`
  - `'OneAndZerosPadding'`
  - `'ZerosAndLenPadding'`
  - `'ZerosPadding'` 
- `iv`：AES 加解密的初始向量，经过 Base64 编码后的字符串，默认值为 `key` 字段的值；
- `ivOffset`：AES 加解密的初始向量偏移，默认值为 $0$；
- `ivLen`：AES 加解密的初始向量字节长度，默认值为 $16$；

::: details 示例代码

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

AesTest() // 打印加解密的文本，控制台输出
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

`rsa` 加解密，`options` 参数的字段功能为：
- `action`：加解密的类型，两个可选值：`'encrypt'`：加密，`'decrypt'`：解密；
- `text`：待加密或解密的文本内容，待解密的文本内容应该是经过 Base64 编码的一段二进制值；
- `key`：`RSA` 密钥，经过 `base64` 编码后生成的字符串，加密时 `key` 为公钥，解密时 `key` 为私钥；
- `transformation`：RSA 算法的填充项，默认为 `RSA/None/OAEPwithSHA-256andMGF1Padding`。RSA 可选填充项为：
  - `'PKCS_v15andMGF1Padding'`
  - `'OAEPwithMD5andMGF1Padding'`
  - `'OAEPwithSHA-1andMGF1Padding'`
  - `'OAEPwithSHA-256andMGF1Padding'`

::: details 示例代码
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

`sign` 签名，`options` 参数的各字段功能为：
- `text`：签名内容；
- `key`：RSA 私钥；
- `algorithm`：签名算法，默认为 `'SHA256withRSA'`。可选签名算法为:
  - `'MD5withRSA'`
  - `'SHA1withRSA'`
  - `'SHA256withRSA'`
  - `'SHA512withRSA'`

::: details 示例代码

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

`hash` 加密，`options` 参数的各字段功能为：
- `data`：生成摘要的原数据；
- `algorithm`：摘要算法，可选值有 `'md5'`，`'sha1'`，`'sha224'`，`'sha256'`，`'sha384'`，`'sha512'`；
- `encode`：返回数据的编码和类型，取值有：
  - `'hex'`：默认值，返回 hex 编码的字符串；
  - `'base64'`：返回值为加密结果经过 Base64 编码的字符串；
  - `'arraybuffer'`：返回值为 ArrayBuffer 类型数据；

::: details 示例代码

``` js
async function md5Test(){
  const res = await cipher.hash({
    algorithm: 'md5',
    data: 'hello'
  })
  console.log(res)
}
md5Test() // 打印生成的摘要，控制台输出
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

使用 HMAC 算法生成带密钥的消息认证码，`options` 参数的各字段功能为：
- `data`：生成摘要的原数据；
- `algorithm`：摘要算法，可选 `'md5'`，`'sha1'`，`'sha224'`，`'sha256'`，`'sha384'`，`'sha512'`；
- `key`：密钥；
- `encode`：返回数据的编码和类型，取值有：
  - `'hex'`：默认值，返回 hex 编码的字符串；
  - `'base64'`：返回值为加密结果经过 Base64 编码的字符串；
  - `'arraybuffer'`：返回值为 `ArrayBuffer` 类型；

::: details 示例代码

``` js
async function hmacTest() {
  let res = await cipher.hmac({
    data: 'hello',
    algorithm: 'sha1',
    key: '1234567890'
  })
  console.log(res)
}
hmacTest() // 打印生成的摘要，控制台输出
// output：6fce0a55cf8bae80e2cf479b50035f773491c5ad
```
:::

### `base64Encode` <decl type="(data: string | ArrayBuffer): Promise&lt;string>" method />

将输入数据进行 Base64 编码。

### `base64Decode` <decl type="(data: string | ArrayBuffer): Promise&lt;ArrayBuffer>" method />

将输入数据进行 Base64 解码。

::: details 示例代码

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
FILE_PATH: src/original_docs/api/system-package.md

# 包管理

本模块提供资源包的安装和卸载功能。

## 导入模块

``` js
import pkg from '@system.package'
```

由于 `package` 是 JavaScript 的关键字且不能作为作为变量名，我们可以将 `"@system.package"` 模块导出到 `pkg` 变量。

## 接口定义

### `install` <decl function type="(options: { src: string }): Promise<void>" />

从文件系统中安装一个应用或者表盘包。参数 `options` 的 `src` 属性是即将安装的资源包文件 URI。

如果资源包是一个应用资源包，那么在使用 `pkg.install({ src: 'package-uri' })` 安装该资源包之后可以由 [`launch()`](system-launch.md#launch-launch-app) 启动，并可以使用 [`app`](/framework/application/resource.md#app) URI 协议来访问包中的内容。

`src` 是即将安装的资源包文件的 URI。安装的包必须是有效的应用或者表盘包，也就是要有 [`manifest.json`](/framework/application/manifest.md) 文件。安装之后的包名由 [`manifest.package`](/framework/application/manifest.md#package) 决定。

安装后可以使用 [`prc`](/framework/application/resource.md#prc) 协议访问来访问资源包中的资源，对于应用资源包还可以用 `app` 协议来访问。

如果待安装的包已经存在，那么会进行升级操作。如果升级的应用正在运行，那么会先退出该应用，此后也可以调用 [`launch()`](system-launch.md#launch-launch-app) 再次启动。

安装的包可以由 [`remove()`](#remove) API 删除。

### `remove`<decl type="(options: { package: string }): Promise<void>" function />

删除由 [`install()`](#install) 安装的资源包。参数 `options` 的 `package` 属性为待删除的资源包名，即 [`manifest.package`](/framework/application/manifest.md#package) 字段。

在删除资源包之前应先关闭相关的资源，例如销毁相关组件并关闭相关页面等。`remove()` 函数会自动关闭资源包对应的应用（如果是应用资源包）。

::: warning
必须用 `remove()` 而不要直接使用文件系统 API 删除资源包，因为后者不会清理资源缓存并且无法正确删除安装信息。
:::

### `getInfo` <decl type="(query?: string | Query): Manifest | undefined" method/>

获取应用包的 manifest 信息。可选参数 `query` 可以是一个包名字符串，也可以是更复杂的 `Query` 对象：
``` ts
type Query = {
  package: string,                 // 待查询的包名
  options?: ('dial' | 'widgets')[] // 可选查询字段
}
```
如果 `package` 字段所指定的包存在 `getInfo()` 将返回包的 `Manifest` 信息，否则返回 `undefined`。当不指定 `query` 参数时，`getInfo()` 将返回当前应用的 manifest 信息。

#### `Manifest` 对象

返回的 `Manifest` 对象基本上是 [`manifest.json`](/framework/application/manifest.md) 的子集：
``` ts
type Query = {
  type: 'app' | 'dial', // 包类型，可能是应用或者表盘包
  name: string,         // 包名
  versionName: string,  // 版本名
  versionCode: number,  // 版本编号
  icon?: string,        // 应用图片路径，只有应用包才存在此字段
  dial?: {              // 可选字段：表盘信息，只有表盘包才有此信息
    component: string,  // 表盘组件的路径
    preview: string     // 表盘预览图的路径
  },
  widgets?: {           // 可选字段：挂件和小组件信息
    name: string,       // 挂件/小组件名字
    component: string,  // 挂件/小组件路径
    preview: string     // 挂件/小组件预览图
  }[]
}
```
`Manifest` 对象的 `dial` 和 `widgets` 是可选字段，他们是否存在由 `Query.options` 的内容决定。例如
``` js
pkg.getInfo({
  package: 'com.example.app',
  options: ['dial', 'widgets']
})
```
将会使结果的 `Manifest` 包含 `dial` 和 `widgets` 字段（不过应用包总是不包含 `dial` 字段）。

当 `query` 参数是一个字符串时等效于 `options` 选项为空，即
``` ts
pkg.getInfo('com.example.app')
pkg.getInfo({ package: 'com.example.app' })
```
的结果都一样，这种情况下返回的 `Manifest` 对象不包含可选字段。

当不指定 `query` 参数时，可以通过 `getInfo()` 返回本应用的信息：
``` js
let manifest = pkg.getInfo()
console.log(manifest)
```

### `list` <decl function type="(type?: 'app' | 'dial'): string[]" />

获取所有已安装的应用或表盘包名列表。

### `countOf` <decl function type="(type?: 'app' | 'dial'): string[]" />

获取已经安装的应用或者表盘数量。


============================================================
FILE_PATH: src/original_docs/api/README.md

# API

Glyphix 提供一整套运行时 JavaScript API，包括与浏览器环境类似的 [`setInterval`](timer.md)、[`console`](console.md) 等 API，也有用于实现整个应用必须的各种系统能力接口。

但是与浏览器环境不同，Glyphix 不提供 DOM 接口，因此没有 `window`、`document` 等对象，也不能进行任何 DOM 操作。

## 快应用异步接口

Glyphix 支持手表快应用标准，但我们主要使用 Promise 风格的异步接口，而不是回调函数风格。例如手表快应用中的 `file.readText()` 接口的回调模式是这样使用的：
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
但是在 Glyphix 中常使用 Promise 风格：
``` js
import file from '@system.file'

// 假设在某个异步函数中
try {
  const content = await file.readText({ uri: 'internal://files/test.txt' })
  console.log(content)
} catch (e) {
  console.error('read text failed:', e)
}
```
由于 Promise 风格 API 更符合 ES6 标准之后的使用习惯，所以本文档只保留 Promise 版本的类型签名。

### Promise vs. 回调接口

如无特别说明，所以返回类型为 `Promise<...>` 的接口都支持回调函数（低版本快应用标准），以及 Promise 两种异步接口风格。回调函数风格的异步接口通常具有以下类型：
``` ts
type CallbackAPI = (options: {
  success: (data: any) => void,
  fail: (data: any, code: number) => void,
  complete: () => void,
  // 其他参数...
}) => void
```
而 Promise 风格下的异步接口则是以下类型：
``` ts
type PromiseAPI = (options: any) => Promise<any>
```

当参数 `options` 中存在任意 `success`、`fail` 或 `complete` 属性时，API 会自动使用回调函数风格（没有返回值），否则使用 Promise 返回值风格。

::: warning
使用回调函数风格时，异步 API 不会返回任何值，因此无法使用 `await` 语法。所以要确保使用 Promise/`await` 语法时，不要传入任何 `success`/`fail` 或 `complete` 回调函数。
:::

### API 示例

以 [`system.file`](system-file.md) 模块为例，的所有函数同时支持 Promise 和回调风格的异步调用模式。下面的代码片段给出了两种 API 用法对比。

::: code-tabs#js

@tab async/await

``` js
import file from '@system.file'

// async/await 实际上是 Promise 的语法糖
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
  .then(console.log) // 提示：console.log() 类型和 Promise.then() 是匹配的，不需要使用箭头函数
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

本文档只会给出 Promise 风格的 API 类型，并且异步操作的示例只用 await/async 语法。

::: tip
不建议开发者额外对 Glyphix API 进行封装，尤其是手动将其回调函数兼容风格封装成 Promise 模式。这种做法需要编写额外的代码，并会损害性能。
:::

## 订阅接口

订阅类的 API 向某个模块注册一个回调函数，而不是直接返回结果。与一般的异步接口不同，订阅接口的回调函数可以被多次执行。所有的订阅接口都支持注册多个订阅回调函数，并且会返回一个订阅 ID，并可以用对应的接口取消订阅。

Glyphix 目前不支持快应用风格的订阅 `fail` 回调函数，但可能在订阅失败时直接抛出异常。


============================================================
FILE_PATH: src/original_docs/api/system-request.md

# 上传下载 request

## 导入模块

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

通过 HTTP/HTTPS 协议下载文件，`options` 参数的各字段功能为：
- `url`：要访问的网站的网址 URL；
- `header`：一个包含 HTTP 请求头信息的对象，键和值为字符串。典型的 HTTP 头部字段可以是 `Authorization`、`Content-Type` 等；
- `filename`：存储下载文件的 URI，如：`internal://files/download.txt`；
- `callback`：下载进度回调函数，下载时会多次调用此函数，`progress` 为下载的进度值，范围为 $[0, 100]$。

`download()` 方法返回一个 [`DownloadTask`](#downloadtask) 对象，可用于等待下载完成或控制下载任务。

::: warning
请不要在 `callback` 函数中以下载进度达到 $100\%$ 作为下载完成后的操作触发条件，详情请参考[等待下载完成](#等待下载完成)。

当前实现没有自动根据 `url` 解析 `filename` 参数属性，请务必填写 `filename`。
:::

## 类型

### `DownloadTask`

`DownloadTask` 是 `download` 方法的返回类型，它的签名为：

``` ts
interface DownloadTask {
  complete: Promise<void>,
  cancel(): void
}
```

`complete` 属性是一个 `Promise` 对象，可用于等待下载完成。`cancel()` 方法用于取消正在进行的下载任务，如果下载已经完成，`cancel()` 方法没有效果。

#### 等待下载完成

使用 `DownloadTask.complete` 等待下载完成，该 `Promise` 兑现（fulfilled）时会保证文件已写入完成，因此可以安全地进行下一步操作。相比之下，`callback` 的下载进度达到 $100\%$ 也并不意味着文件写入完成，它仅适合用于 UI 进度显示等需求。

实际使用时，考虑到下载可能会失败，建议使用 `try...catch` 语句来处理下载错误。下面的实例会介绍用法。

## 示例

这是从网络中下载一个文件的简单示例：

``` js
request.download({
  url: "http://www.rt-thread.com/service/rt-thread.txt",
  filename: "internal://tmp/rt-thread.txt",
})
```

可以通过 `download()` 方法返回值的 `complete` 属性来等待下载完成：
``` js
try {
  await request.download({
    url: "http://www.rt-thread.com/service/rt-thread.txt",
    filename: "internal://tmp/rt-thread.txt"
  }).complete // complete 被拒绝时表示下载失败
  console.log('download finished.')
} catch (e) {
  console.error('download failed:', e)
}
```

这里的 `try...catch` 块用于捕获下载失败的异常。该异常实际是 `DownloadTask.complete` 被拒绝时抛出的错误，所以应该用 `awiat` 等待 `complete` 属性，否则无法捕获到异常。


============================================================
FILE_PATH: src/original_docs/api/console.md

# Console 模块

`console` 模块的功能和浏览器中的 `console` 功能类似，用于实现日志记录。本模块无需导入就可以直接使用，所有属性都绑定到 `console` 全局变量，例如：
``` js
console.log('Hello world!')
```


## 接口定义

### `backtrace` <decl type="boolean" />

把 `backtrace` 设置为 `true` 之后，所有的日志打印将携带调用栈信息。默认值为 `false`，此时只有 `console.warn()` 及更高级的 API 会输出调用栈。

### `log` <decl type="(...data: any[]): void" method />

### `dir` <decl type="(...data: any[]): void" method />

### `debug` <decl type="(...data: any[]): void" method />

### `info` <decl type="(...data: any[]): void" method />

### `warn` <decl type="(...data: any[]): void" method />

### `error` <decl type="(...data: any[]): void" method />

## 日志过滤级别

`console` 模块的日志过滤级别由系统底层的日志过滤机制决定，无法在 JavaScript 代码中配置。


============================================================
FILE_PATH: src/original_docs/api/system-storage.md

# 数据存储

数据存储模块 `system.storage` 允许应用存储自己的数据，这些数据会持久化地保存在应用的存储对象中，当应用卸载后存储在 `system.storage` 中的数据会被清除。

`system.storage` 以键值对的形式存储数据，其中键必须是字符串，而值是一个 JSON 值（也可以是可以序列化为 JSON 的 JavaScript 值）。

## 导入模块

``` js
import storage from '@system.storage'
```

## API

### `get` <decl type="(key: string): any" method />

获取存储中键名 `key` 所对应的值。如果键值对不存在则返回 `undefined`。

### `set` <decl type="(key: string, value: any): void" method />

该方法接受一个键名 `key` 和值 `value` 作为参数并将此键值对添加到存储中。如果键名已经存在则更新其对应的值。

### `delete` <decl type="(key: string): boolean" method />

删除存储中键名 `key` 对应的键值对。键值对存在且删除成功后返回 `true`。

### `clear` <decl type="(): void" method />

清空应用中的所有存储数据。


============================================================
FILE_PATH: src/original_docs/api/system-prompt.md

# 弹窗

## 导入模块

``` js
import prompt from '@system.prompt'
```

## 接口定义

#### `showToast`
<decl method><pre>
(options: {
  message: string,
  duration?: number,
  important?: boolean
}): void
</pre></decl>

显示一个 toast 弹框，toast 是一种置于界面顶层的文本弹框。toast 在界面中只显示一个实例，有多个 toast 内容时会依次排队显示。

`options` 参数字段的描述：
- `message`：需要现实的文本。
- `duration`：toast 的显示时长，单位为 ms，达到超时时长后 toast 会自动隐藏。
- `important`：是否为重要的 toast，默认为 `false`。如果设置为 `true`，则允许应用在后台时弹出该 toast。

toast 的显示样式（字体、颜色等）由固件决定，无法在应用中修改。toast 的显示时长也有限制，为 $200$ 到 $5000$ 毫秒。

#### `showPopup` <decl type="(options: { uri: string, params?: Object }): Promise<any>" method />

显示一个悬浮页面弹窗。`options` 参数字段描述：
- `uri`：目标页面的名字，需要在 `mainfest.json` 的 `router` 中注册。
- `params`：跳转时需要传递的数据，`params` 参数的属性会替换目标页面的 `data` 属性值。

悬浮页面是一种系统级的弹窗（类似于 toast 或者对话框），但悬浮页面是功能完整的页面，具有最高的可定制性。和一般的页面不同，悬浮页面在系统的悬浮页面栈中显示而不是应用自己的页面栈，因此[页面路由](api/system-router)机制中的 `router.back()` 等 API 无法操作悬浮页面。想要关闭悬浮页面，可以使用 [`router.close()`](system-router.md#close) 方法。

弹窗的显示层级比应用高，因此悬浮页面会显示在所有应用的页面之上。所有的应用都使用同一个悬浮页面栈，悬浮页面按照弹出顺序决定显示层级，即早弹出的页面位于顶部。悬浮页面的显示层级和对话框相同，低于 toast。

和 `router.push()` 一样，`showPopup()` 也返回一个 Promise 对象，它会在悬浮页面退出之后兑现并返回自定义的结果。详情请参考 [`router.push()`](system-router.md#push) 和 [`router.close()`](system-router.md#close)。


============================================================
FILE_PATH: src/original_docs/api/global.md

# 全局对象

## 全局函数

### `encodeURIComponent` <decl type="(str: string): string" function />

`encodeURIComponent()` 全局函数用于对 URI 组件 `str` 进行编码。它会将某些特殊字符转义成 UTF-8 编码后对应的百分号（`%`）转义序列，这可确保组件在用作 URL 的一部分时可被正确解释，特别是在查询字符串参数、路径或片段中。 

字母、数字、`- _ . ! ~ * ' ( )` 不会被编码。其他字符会被编码成百分号的转义序列（例如空格被编码为 `%20`）。

`encodeURIComponent()` 与 Web 中的[同名函数](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent)行为一致。

示例：
```js
console.log(encodeURIComponent("https://example.com/page?id=100"));
// output: https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100
```

### `decodeURIComponent` <decl type="(str: string): string" function />

`decodeURIComponent()` 全局函数用于解码由 `encodeURIComponent()` 编码的 URI 组件 `str`。它会将百分号（`%`）转义序列转换回其原始字符形式，从而恢复原始的 URI 组件。例如，它会将 `%20` 转换回空格。

`decodeURIComponent()` 与 Web 中的[同名函数](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/decodeURIComponent)行为一致。

示例：
```js
console.log(decodeURIComponent("https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100"));
// output: https://example.com/page?id=100
```

### `URI` <decl type="(uri: string | Uri): Uri" function />

此函数接受一个字符串，并将其解析为 `Uri` 对象用于后续处理。参数 `uri` 是待解析的 URI 字符串。

返回值是一个对象，包含以下字段：
- `scheme: string`：从参数中解析到的 scheme 字段；
- `authority: string`：从参数中解析到的 authority 字段；
- `path: string`：从参数中解析到的 path 字段；
- `query: string`：从参数中解析到的 query 字段；
- `origin: string`：参数中的原始 URI 字符串
- `toString: ( string`：此方法可以将本对象重新编码为 URI 字符串。

例如：
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

`URI` 函数还接受对象作为参数，这种情况下 `URI` 函数会给参数对象增加一个 `toString` 方法，通过该方法可以将 URI 对象编码为字符串：
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
FILE_PATH: src/original_docs/api/system-internal.md

# 内部接口

`system.internal` 模块提供一些供系统使用的内部接口，该模块只能在 launcher 应用中使用。

## 导入模块

``` js
import internal from '@system.internal'
```

## API

### `globalComponent` <decl type="(name: string, uri: string): void" method />

注册一个[全局组件](/framework/component/README.md#全局组件)，全局组件可以在所有应用中引入。参数 `name` 是全局组件的名字，`uri` 是全局组件 UX 文件相对于当前源文件的路径或 URI。例如
``` js
internal.globalComponent('TopBar', '/global/TopBar.ux')
```
之后在所有应用中都可以用 `<import name="TopBar" />` 来引用全局组件 `TopBar`。

`globalComponent()` 方法最好在 launcher 应用的 `app.js` 执行阶段执行，这样可以在任何界面加载之前就注册全局组件信息。

### `setDefaultKeyHandler` <decl type="(handler: (event: KeyEvent) => void): void" method />

注册系统的默认按键处理程序，参数 `handler` 是一个回调函数。`KeyEvent` 类型原型为：
``` ts
interface KeyEvent  {
  type: 'keydown' | 'keyup', // 按键事件的类型
  key: string, // 按键名称
  timestamp: number, // 按键事件上报的时间戳，单位是毫秒
}
```
默认按键处理程序只能注册一次，因为多次注册会覆盖前面的操作。


============================================================
FILE_PATH: src/original_docs/api/i18n.md

# 国际化

本模块提供应用内的国际化操作功能。

## 导入模块

``` js
import i18n from '@system.i18n'
```

## API

### `getLanguage` <decl type="(): string" method></decl>

获取当前应用的语言设置。返回值为一个字符串，表示当前的语言代码，如 `'zh-CN'`、`'en-US'` 等。


============================================================
FILE_PATH: src/original_docs/api/timer.md

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


============================================================
FILE_PATH: src/original_docs/api/system-battery.md

# 电池状态

## 导入模块

``` js
import battery from '@system.battery'
```

## API

### `getStatus` <decl type="(): Promise<{charge: ChargeState, level: number}>" method />

获取电池的充电状态 `charge` （[`ChargeState`](#chargestate) 类型）和电量值 `level`。电量值是 $[0, 100]$ 间的整数。

## 类型

### `ChargeState`

`ChargeState` 枚举所有的电池充电状态，其定义如下：
``` ts
type ChargeState = 'charging' | 'discharging' | 'not-charging' | 'full'
```
各个值的含义为：
- `'charging'`：电池处于充电状态；
- `'discharging'`：断开充电状态；
- `'not-charging'`：未处于充电状态；
- `'full'`：电池已经充满电。


============================================================
FILE_PATH: src/original_docs/api/system-exchange.md

# 交换数据

交换数据模块 `system.exchange` 用于存储跨应用的共享数据，这些数据不会持久化存储，一旦设备断电即会丢失。。`system.exchange` 中存储的数据可以在所有应用中访问，因此该模块可用于存储应用的一些配置信息，但不适合存储敏感数据。

`system.exchange` 以键值对的形式存储数据，其中键必须是字符串，而值是一个 JSON 值（也可以是可以序列化为 JSON 的 JavaScript 值）。

## 导入模块

``` js
import exchange from '@system.exchange'
```

## API

### `get` <decl type="(key: string): any" method />

获取存储中键名 `key` 所对应的值。如果键值对不存在则返回 `undefined`。

### `set` <decl type="(key: string, value: any): void" method />

该方法接受一个键名 `key` 和值 `value` 作为参数并将此键值对添加到存储中。如果键名已经存在则更新其对应的值。

### `delete` <decl type="(key: string): boolean" method />

删除存储中键名 `key` 对应的键值对。键值对存在且删除成功后返回 `true`。

### `watch` <decl type="(key: string, callback: (value: any) => void): number" method />

监听存储中键名为 `key` 的数据值变化，并在值变化时调用 `callback` 回调函数。回调函数的参数 `value` 为新的数据值。`watch()` 方法返回一个 `wtacher ID`，该 ID 可用于 [`unwatch()`](#unwatch) 方法来解除监听。

::: tip
不再需要监听时应使用 [`unwatch()`](#unwatch) 方法解除监听，否则可能造成内存泄漏。
:::

### `unwatch` <decl type="(watcherID: number): void" method />

取消存储中对键名为 `key` 的一个监听。参数 `watcherID` 是 [`watch()`](#watch) 方法创建监听时返回的 `wtacher ID`。


============================================================
FILE_PATH: src/original_docs/api/system-network.md

# 网络状态

## 导入模块

```js
import network from '@system.network';
```

## 接口定义

### `subscribe` <decl type="(callback: (status: NetworkState) => void): number" method/>

监听网络状态的变化。`callback` 的参数 `status` 为新的[网络状态](#networkstate)，此方法返回的 ID 可使用 [`unsubscribe()`](#unsubscribe) 方法来解除监听。

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

取消网络状态监听，`subscribeID` 是 [`subscribe()`](#subscribe) 方法返回的 ID 值。

### `getType` <decl type="(): Promise<NetworkState>" method/>

获取当前的网络状态，返回一个 [`NetworkState`](#networkstate) 值。

## 类型定义

### `NetworkState`

此对象用于表示当前的网络状态，类型签名如下：

```ts
type NetworkState = {
  device: string; // 网络设备的名字
  type: string; // 网络设备的类型
  linkUp: boolean; // 网络设备是否已经打开
  online: boolean; // 设备是否在线（是否可以访问互联网）
};
```

通常可以使用 `NetworkState` 的 `online` 属性来检查设备是否可以上网。


============================================================
FILE_PATH: src/original_docs/api/system-geolocation.md

# 地理位置

## 导入模块

```js
import geolocation from '@system.geolocation';
```

开发者需要在 [`manifest.json`](/framework/application/manifest.md#permissions) 文件中声明应用对 `watch.permission.LOCATION` 的访问权限。

## 接口定义

### `getLocation` 
<decl method><pre>
(options: {
  mode?: string
  timeout?: number
}): Promise&lt;Location>
</pre></decl>

单次获取当前位置经纬度，返回一个异步的[位置信息](#location)。

`options` 参数说明
- `mode` : 声明定位精度， `fine` 为精确定位， `coarse` 为模糊定位，默认值为  `coarse`
- `timeout` : 定位超时时间， 单位为 `ms` ，默认为 30000

### `subscribe` <decl type="(callback: (location: Location) => void): number" method/>

监听位置变化。 `callback` 的参数 `location` 为当前[位置信息](#location)，此方法返回的 ID 可使用 [`unsubscribe()`](#unsubscribe) 方法来解除监听。

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

取消监听位置变化。

## 类型定义

### `Location`

用于表示定位的位置信息数据。

```ts
type Location = {
  code: number; // 定位状态代码，表示当前位置信息是否有效
  msg: string; // 定位错误信息
  data: {
    // 位置信息的数据
    longitude: number; // 纬度值
    latitude: number; // 经度值
    coordType: string; // 坐标系类型，例如 'WGS84'、'GCJ02' 等
  };
};
```

`code` 字段的定位状态代码如下：

- `200`: 当前定位信息有效；
- `1002`: 当前未连接手机蓝牙网络
- `1300`: 手机无法获取定位服务
- `1301`: 手机未开启定位服务
- `1302`: 手机应用未授予定位权限
- `1399`: 未知错误


============================================================
FILE_PATH: src/original_docs/api/system-test.md

# 测试框架

## 导入模块

``` js
import test from '@system.test'
```

## 简介

`system.test` 模块是一个端到端测试框架，可以通过编程来模拟用户操作，并检查界面行为是否符合预期。

一个简单的模拟用户操作的代码如下：
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
这段代码会自动等待界面中的元素被渲染，并通过滚动手势让被遮挡的元素进入可视区域内，然后对其执行点击或滚动等手势。

## API

### 辅助函数

这些函数在测试中提供辅助功能，如延时等。

#### `wait` <decl method type="(duration: number): Promise<void>" />

异步延时指定的时间，用来在测试中等待某些操作，或者模拟用户的停顿。

### 定位器

定位器从应用的顶层页面查找元素（原生组件），例如根据元素的 tag 或者 id 来查找。定位器的进一步介绍请参考 [`Locator` 对象](#locator-对象)。

#### `getByTag` <decl method type="(tag: string): Locator" />

通过 `tag` 定位元素。目前只支持大驼峰命名，如 `'P'`、`'Swiper'` 等。

#### `getByClass` <decl method type="(class: string): Locator" />

通过 `class` 属性定位元素。

#### `getById` <decl method type="(id: string): Locator" />

通过 `id` 属性定位元素。

#### `getHasText` <decl method type="(text: RegExp | string): <Locator>" />

通过元素的 `text` 属性是否与 `text` 参数匹配来定位元素。`text` 参数是一个正则表达式，例如：
- `/hello/` 测试元素的 `text` 属性值中是否包含 `'hello'` 字串；
- `/^hello/` 测试元素的 `text` 属性值的开头是否为 `'hello'`；
- `/^hello$/` 测试元素 `text` 属性值是否为 `'hello'`。

`text` 参数的匹配规则和 [`RegExp.test()`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/RegExp/test) 相同。

### `Locator` 对象

`Locator` 对象由定位器 API 返回，可用于进一步的操作。所有的定位器操作都会尝试自动等待元素出现并会将其移动到可视范围内。

#### `click` <decl method type="(): Promise<void>" />

当元素存在并已经滚动到可视区域内后，后在元素的位置上模拟一个点击手势。

#### `scroll` <decl method type="(dx: number, dy: number, duration?: number): Promise<void>" />

当元素存在并已经滚动到可视区域内后，后在元素的位置上模拟一个滚动手势。`dy` 和 `dy` 是滚动的 $(x, y)$ 偏移量，单位为像素；可选的 `duration` 为手势的时间，单位为秒，默认值为 $0.5 \rm s$。

该方法会等待元素的 `scrolled` 属性变为 `false` 才会 polyfill 返回的 Promise 对象。因此对于 `scroll`、`swiper` 等组件来说，`scroll()` 方法会在这些组件的惯性动画已经停止之后才会触发下一步操作。

#### `wait` <decl method type="(): Promise<void>" />

等待元素存在并滚动到可视区域内，但是不模拟任何手势或其他操作。


============================================================
FILE_PATH: src/original_docs/api/system-devtools.md

# 调试接口

## 导入模块

``` js
import devtools from '@system.devtools'
```

## API

### `command` <decl type="(cmd: string, fn: (argv: string[]) => void): void" method />

将一个函数 `fn` 注册为名为 `cmd` 的 shell 命令。注册后可以在设备终端上使用 `dev` 命令来调用。例如
``` bash
dev cmd arg1 arg2
```
会调用名为 `'cmd'` 的命令，而参数列表为 `['arg1', 'arg2']`。



============================================================
FILE_PATH: src/original_docs/api/system-schedule.md

# 定时任务

## 导入模块

``` js
import schedule from "@system.schedule"
// 或者
const schedule = require("@system.schedule")
```

开发者需要在 [`manifest.json`](/framework/application/manifest.md#permissions) 文件中声明应用对 `watch.permission.SCHEDULE` 的访问权限。

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

设置定时任务。`options` 参数的各字段功能为：
- `type`：	
  - 1：硬件时间，可以通过修改系统时间触发 `triggerMethod`；
  - 2：真实时间流逝，即使在休眠状态，时间也会被计算；
- `timeout`：
  - 若 type 为 1，则为首次执行时间的时间戳，即从 1970/01/01 00:00:00 GMT 到当前时间的毫秒数；
  - 若 type 为 2，则为当前时间距离首次执行时间的间隔，单位毫秒；
- `triggerMethod`：app.js 中定义的方法名，达到超时时间，由后台拉起时调用；
- `interval`：周期性执行的间隔，毫秒为单位，不传就不重复执行；
- `params`：任务参数；

::: tip
虽然 `timeout` 和 `interval` 的精度为毫秒，但定时精确到秒。首次执行时间和周期执行时间间隔不能小于 60 秒，否则接口会抛出异常。
:::

返回值为任务 ID，用于取消任务，返回值为 -1，表示创建失败。

``` js
let id = schedule.scheduleJob({
  type: 1,
  timeout: new Date('2025-03-14T23:00:00').getTime(),  // 首次执行时间的时间戳
  interval: 60000,     // 周期执行间隔不小于 60 秒
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

取消定时任务。

``` js
schedule.cancel(id)
```


