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
