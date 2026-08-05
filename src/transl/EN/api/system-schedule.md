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
  - If `type` is 1, this is the timestamp for the first execution, i.e., the number of milliseconds from 1970/01/01 00:00:00 GMT to the current time.
  - If `type` is 2, this is the interval between the current time and the first execution time, in milliseconds.
- `triggerMethod`: The method name defined in `app.js`, which is called when the timeout is reached and the app is awakened by the background.
- `interval`: The interval for periodic execution in milliseconds. If not passed, it will not execute repeatedly.
- `params`: Task parameters.

::: tip
Although the precision of `timeout` and `interval` is in milliseconds, the timing is accurate to the second. The first execution time and the periodic execution interval cannot be less than 60 seconds; otherwise, the interface will throw an exception.
:::

The return value is the task ID used for canceling the task. A return value of `-1` indicates that the creation failed.

``` js
let id = schedule.scheduleJob({
  type: 1,
  timeout: new Date('2025-03-14T23:00:00').getTime(),  // Timestamp of the first execution time
  interval: 60000,     // The periodic execution interval must not be less than 60 seconds
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