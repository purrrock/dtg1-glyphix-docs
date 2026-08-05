# Sensor

## Import Module

```js
import sensor from '@system.sensor';
```

Developers need to declare the application's access permission to `watch.permission.ACCESS_SENSORS` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

## Interface Definitions

### `subscribeAccelerometer`
<decl method><pre>
(options: { 
  interval?: 'game' | 'ui' | 'normal', 
  callback: (data: AccelerometerValue) => void,
}): number
</pre></decl>

Listens for changes in accelerometer sensor data. The functions of the fields in the `options` parameter are as follows:
- `interval`: Listening frequency, defaults to `'normal'`. Available values are:
  - `'game'`: Game mode, with a frequency of 20ms/time;
  - `'ui'`: UI mode, with a frequency of 60ms/time;
  - `'normal'`: Normal mode, with a frequency of 200ms/time.
- `callback`: Accelerometer data update callback. The signature of the accelerometer data type `AccelerometerValue` is as follows:
  ``` ts
  type AccelerometerValue = {
    x: number   // Acceleration along the x-axis
    y: number   // Acceleration along the y-axis
    z: number   // Acceleration along the z-axis
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

// Unsubscribe
sensor.unsubscribeAccelerometer(id)
```

### `unsubscribeAccelerometer` <decl type="(id: number): void" method/>

Cancels listening to accelerometer sensor data. The `id` parameter is the listening ID returned by the [`subscribeAccelerometer`](#subscribeaccelerometer) method.

### `subscribeCompass`
<decl method><pre>
(options: { 
  callback: (data: CompassValue) => void,
}): number
</pre></decl>

Listens for changes in compass data. Returns the listening ID, which is used to cancel listening. The functions of the fields in the `options` parameter are as follows:
- `callback`: Compass data change callback.

`CompassValue` signature:
``` ts
  type CompassValue = {
    direction: number   // Angle between the y-axis and the geomagnetic north pole (in radians)
    accuracy: number    // Accuracy
  }
```
- `direction`: The angle in radians between the device's Y-axis and the Earth's magnetic north pole, with a value range of $(-\pi,\pi]$, where:
  - `0`: True North
  - $\pi$` / 2` (approx. 1.57): True East
  - $\pi$ (approx. 3.14): True South
  - -$\pi$` / 2` (approx. -1.57): True West
- `accuracy`: Accuracy level of the compass data
  - `3`: High accuracy
  - `2`: Medium accuracy
  - `1`: Low accuracy
  - `0`: Unreliable (reason unknown)
  - `-1`: Unreliable (sensor lost connection)

Example:
```js
const id = sensor.subscribeCompass({
  callback(ret) {
    console.log(`direction=${ret.direction}, accuracy=${ret.accuracy}`)
  }
})

// Unsubscribe
sensor.unsubscribeCompass(id)
```

### `unsubscribeCompass`<decl type="(id: number): void" method/>

Cancels listening to compass data. The `id` parameter is the listening ID returned by the [`subscribeCompass`](#subscribecompass) method.

### `calibrationCompass` <decl type="(): Promise<void>" method/>

Starts the compass calibration process. When the compass accuracy is low, guide the user to operate and call this method to calibrate the compass.

This function returns a Promise object with no result, which is resolved when the system completes the calibration.

### `getCompassValue` <decl type="(): Promise<CompassValue>" method/>

Gets the current compass data. Returns an asynchronous result containing a Promise object of type `CompassValue` with compass direction and accuracy information.

### `subscribeStepCounter`
<decl method><pre>
(options: { 
  callback: (data: StepCounterValue) => void,
}): number
</pre></decl>

Listens for changes in step counter sensor data. The functions of the fields in the `options` parameter are as follows:
- `callback`: Step counter data change callback. The signature of the step counter data type `StepCounterValue` is as follows:
  ``` ts
  type StepCounterValue = {
    steps: number     // Current accumulated steps (starts from 0 after reboot)
  }
  ```

Example:
```js
const id = sensor.subscribeStepCounter({
  callback(ret) {
    console.log(`steps=${ret.steps}`)
  }
})

// Unsubscribe
sensor.unsubscribeStepCounter(id)
```

### `unsubscribeStepCounter` <decl type="(id: number): void" method/>

Cancels listening to step counter sensor data. The `id` parameter is the listening ID returned by the [`subscribeStepCounter`](#subscribestepcounter) method.

### `subscribeOnBodyState`
<decl method><pre>
(options: { 
  callback: (data: OnBodyStateValue) => void,
}): number
</pre></decl>

Listens for changes in the device on-body state. The functions of the fields in the `options` parameter are as follows:
- `callback`: Device on-body state change callback. The signature of the device on-body state data type `OnBodyStateValue` is as follows:
  ``` ts
  type OnBodyStateValue = {
    value: boolean  // Whether the device is worn
  }
  ```

Example:
```js
const id = sensor.subscribeOnBodyState({
  callback(ret) {
    console.log(`onBody=${ret.value}`)
  }
})

// Unsubscribe
sensor.unsubscribeOnBodyState(id)
```

### `unsubscribeOnBodyState` <decl type="(): void" method/>

Cancels listening to the on-body state. The `id` parameter is the listening ID returned by the [`subscribeOnBodyState`](#subscribeonbodystate) method.

### `getOnBodyState` <decl type="(): Promise<OnBodyStateValue>" method/>

Gets the current device on-body state.

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

Listens for changes in gyroscope data. The functions of the fields in the `options` parameter are as follows:
- `callback`: Gyroscope data change callback. The signature of the gyroscope data type `GyroscopeValue` is as follows:
  ``` ts
  type GyroscopeValue = {
    x: number   // Angular velocity along the x-axis
    y: number   // Angular velocity along the y-axis
    z: number   // Angular velocity along the z-axis
  }
  ```

Example:
```js
const id = sensor.subscribeGyroscope({
  callback(ret) {
    console.log(`gyroscope data, x = ${ret.x}, y = ${ret.y}, z = ${ret.z}`)
  }
})

// Unsubscribe
sensor.unsubscribeGyroscope(id)
```

### `unsubscribeGyroscope` <decl type="(id: number): void" method/>

Cancels listening to gyroscope data. The `id` parameter is the listening ID returned by the [`subscribeGyroscope`](#subscribegyroscope) method.

### `subscribeBarometer`
<decl method><pre>
(options: { 
  callback: (data: BarometerValue) => void,
}): number
</pre></decl>

Listens for changes in barometer sensor data. The functions of the fields in the `options` parameter are as follows:
- `callback`: Barometer data change callback. The signature of the barometer data type `BarometerValue` is as follows:
  ``` ts
  type BarometerValue = {
    pressure: number   // Barometric pressure value, unit: Pa
  }
  ```

Example:
```js
sensor.subscribeBarometer({
  callback(ret) {
    console.log("get barometer:", ret.pressure)
  }
})

// Unsubscribe
sensor.unsubscribeBarometer(id)
```

### `unsubscribeBarometer` <decl type="(id: number): void" method/>

Cancels listening to the barometer sensor. The `id` parameter is the listening ID returned by the [`subscribeBarometer`](#subscribebarometer) method.

### `subscribeWristLift`
<decl method><pre>
(options: { 
  callback: () => void,
}): number
</pre></decl>

Listens for wrist lift events. The functions of the fields in the `options` parameter are as follows:
- `callback`: Wrist lift event listener callback.

Example:
```js
const id = sensor.subscribeWristLift({
  callback: () => {
    console.log('wrist lift')
  }
});

// Unsubscribe
sensor.unsubscribeWristLift(id)
```

### `unsubscribeWristLift` <decl type="(id: number): void" method/>

Cancels listening to wrist lifts. The `id` parameter is the listening ID returned by the [`subscribeWristLift()`](#subscribewristlift) method.

## Usage Limits

If the current device does not support the corresponding sensor capability, calling the interface will directly throw an exception, and the listener will not take effect.
Example of exception log: `the device does not support accelerometer sensor`

Example of catching exception information:

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

## Precautions

It is recommended to unsubscribe promptly when sensor data is no longer needed. Especially when the page is destroyed (in the `onDestroy` callback), unsubscribing helps avoid unnecessary performance degradation and power consumption.