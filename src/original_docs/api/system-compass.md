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
