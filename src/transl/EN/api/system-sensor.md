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
