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
