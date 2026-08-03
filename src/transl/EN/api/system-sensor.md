# Sensor

## Import Module

```js
import sensor from '@system.sensor';
```

Developers need to declare access to `watch.permission.ACCESS_SENSORS` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

## Interface Definitions

### `subscribeAccelerometer`
<decl method><pre>
(options: { 
  interval?: 'game' | 'ui' | 'normal', 
  callback: (data: AccelerometerValue) => void,
}): number
</pre></decl>

Listens for changes in accelerometer data. The functions of the fields in the `options` parameter are:
- `interval`: Listening frequency, defaults to `'normal'`. Available values are:
  - `'game'`: Game mode, frequency is 20ms/time;
  - `'ui'`: UI mode, frequency is 60ms/time;
  - `'normal'`: Normal mode, frequency is 200ms/time.
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

// Cancel listening
sensor.unsubscribeAccelerometer(id)
```

### `unsubscribeAccelerometer` <decl type="(id: number): void" method/>

Cancels listening for accelerometer data. The `id` parameter is the listening ID returned by the [`subscribeAccelerometer`](#subscribeaccelerometer) method.

### `subscribeCompass`
<decl method><pre>
(options: { 
  callback: (data: CompassValue) => void,
}): number
</pre></decl>

Listens for changes in compass data. Returns the listening ID, which is used to cancel listening. The functions of the fields in the `options` parameter are:
- `callback`: Compass data change callback.

`CompassValue` signature:
``` ts
  type CompassValue = {
    direction: number   // Angle between the y-axis and the geomagnetic North Pole (in radians)
    accuracy: number    // Accuracy
  }
```
- `direction`: The angle in radians between the device's Y-axis and the Earth's magnetic North Pole, with a value range of $(-\pi,\pi]$, where:
  - `0`: True North
  - $\pi$` / 2` (approx. 1.57): True East
  - $\pi$ (approx. 3.14): True South
  - -$\pi$` / 2` (approx. -1.57): True West
- `accuracy`: Accuracy level of the compass data
  - `3`: High accuracy
  - `2`: Medium accuracy
  - `1`: Low accuracy
  - `0`: Unreliable (reason unknown)
  - `-1`: Unreliable (sensor disconnected)

Example:
```js
const id = sensor.subscribeCompass({
  callback(ret) {
    console.log(`direction=${ret.direction}, accuracy=${ret.accuracy}`)
  }
})

// Cancel listening
sensor.unsubscribeCompass(id)
```

### `unsubscribeCompass`<decl type="(id: number): void" method/>

Cancels listening for compass data. The `id` parameter is the listening ID returned by the [`subscribeCompass`](#subscribecompass) method.

### `calibrationCompass` <decl type="(): Promise<void>" method/>

Starts the compass calibration process. When the compass accuracy is low, guide the user to perform actions and call this method to calibrate the compass.

This function returns a Promise object with no result, which is resolved when the system completes the calibration.

### `getCompassValue` <decl type="(): Promise<CompassValue>" method/>

Gets the current compass data. Returns an asynchronous result containing a Promise object of type `CompassValue`, which includes compass direction and accuracy information.

### `subscribeStepCounter`
<decl method><pre>
(options: { 
  callback: (data: StepCounterValue) => void,
}): number
</pre></decl>

Listens for changes in step counter sensor data. The functions of the fields in the `options` parameter are:
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

// Cancel listening
sensor.unsubscribeStepCounter(id)
```

### `unsubscribeStepCounter` <decl type="(id: number): void" method/>

Cancels listening for step counter sensor data. The `id` parameter is the listening ID returned by the [`subscribeStepCounter`](#subscribestepcounter) method.

### `subscribeOnBodyState`
<decl method><pre>
(options: { 
  callback: (data: OnBodyStateValue) => void,
}): number
</pre></decl>

Listens for changes in the device on-body (wearing) state. The functions of the fields in the `options` parameter are:
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

// Cancel listening
sensor.unsubscribeOnBodyState(id)
```

### `unsubscribeOnBodyState` <decl type="(): void" method/>

Cancels listening for the on-body state. The `id` parameter is the listening ID returned by the [`subscribeOnBodyState`](#subscribeonbodystate) method.

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

Listens for changes in gyroscope data. The functions of the fields in the `options` parameter are:
- `callback`: Gyroscope data change callback. The signature of the gyroscope data type `GyroscopeValue` is as follows:
  ``` ts
  type GyroscopeValue = {
    x: number   // Angular velocity around the x-axis
    y: number   // Angular velocity around the y-axis
    z: number   // Angular velocity around the z-axis
  }
  ```

Example:
```js
const id = sensor.subscribeGyroscope({
  callback(ret) {
    console.log(`gyroscope data, x = ${ret.x}, y = ${ret.y}, z = ${ret.z}`)
  }
})

// Cancel listening
sensor.unsubscribeGyroscope(id)
```

### `unsubscribeGyroscope` <decl type="(id: number): void" method/>

Cancels listening for gyroscope data. The `id` parameter is the listening ID returned by the [`subscribeGyroscope`](#subscribegyroscope) method.

### `subscribeBarometer`
<decl method><pre>
(options: { 
  callback: (data: BarometerValue) => void,
}): number
</pre></decl>

Listens for changes in barometer sensor data. The functions of the fields in the `options` parameter are:
- `callback`: Barometer data change callback. The signature of the barometer data type `BarometerValue` is as follows:
  ``` ts
  type BarometerValue = {
    pressure: number   // Air pressure value, unit: Pa
  }
  ```

Example:
```js
sensor.subscribeBarometer({
  callback(ret) {
    console.log("get barometer:", ret.pressure)
  }
})

// Cancel listening
sensor.unsubscribeBarometer(id)
```

### `unsubscribeBarometer` <decl type="(id: number): void" method/>

Cancels listening for the barometer sensor. The `id` parameter is the listening ID returned by the [`subscribeBarometer`](#subscribebarometer) method.

### `subscribeWristLift`
<decl method><pre>
(options: { 
  callback: () => void,
}): number
</pre></decl>

Listens for wrist lift events. The functions of the fields in the `options` parameter are:
- `callback`: Wrist lift event listener callback.

Example:
```js
const id = sensor.subscribeWristLift({
  callback: () => {
    console.log('wrist lift')
  }
});

// Cancel listening
sensor.unsubscribeWristLift(id)
```

### `unsubscribeWristLift` <decl type="(id: number): void" method/>

Cancels listening for wrist lifts. The `id` parameter is the listening ID returned by the [`subscribeWristLift()`](#subscribewristlift) method.

## Usage Limits

When the current device does not support the corresponding sensor capability, calling the interface will directly throw an exception, and the listener will not take effect.
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