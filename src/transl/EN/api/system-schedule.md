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
