# compass

The `@system.compass` module provides the ability to access the device's compass sensor, which can obtain information about the device's orientation relative to Earth's magnetic North Pole.

## Import module

``` js
import compass from '@system.compass'
```

## Interface definition

### `subscribe` <decl type="(callback: (data: Value) => void): number" method/>

Subscribe to Compass data changes. The callback function is automatically called when the device orientation changes. The `callback` callback function receives compass data of type [`Value`](#value).

Returns a subscription ID for unsubscribing.

### `unsubscribe` <decl type="(subscribeId: number): void" method/>

Cancel Compass data subscription. The parameter `subscribeId` is the subscription ID returned by the [`subscribe()`](#subscribe) method.

This method should be called when the page or component is destroyed to cancel the subscription of `subscribe()`:
``` js
const subscribeId = compass.subscribe((data) => {
  console.log(`Direction: ${data.direction} radians`)
  console.log(`Accuracy: ${data.accuracy}`)
})

// Unsubscribe
compass.unsubscribe(subscribeId)
```


### `calibration` <decl type="(): Promise<void>" method/>

Start the compass calibration process. When the compass accuracy is low, guide the user to operate and call this method to calibrate the compass.

This function returns a resultless Promise object, which will be resolved when the system completes calibration.

### `getValue` <decl type="(): Promise<Value>" method/>

Get current compass data. Returns an asynchronous result, a Promise object containing compass direction and accuracy information (of type [`Value`](#value)).

Example:
``` js
// Use Promise
compass.getValue().then((data) => {
  console.log(`Direction: ${data.direction} radians`)
  console.log(`Accuracy level: ${data.accuracy}`)
})

// Use async/await
async function getCompassData() {
  const data = await compass.getValue()
  console.log(`Direction: ${data.direction} radians`)
  console.log(`Accuracy level: ${data.accuracy}`)
}
```

::: note
Due to implementation flaws, this method does not support callback-style calls (such as `{ success: (data) => {...} }`), please use Promise or async/await.
:::

## Type definition

### `Value`

The signature of the compass data type `Value` is as follows:
``` ts
type Value = {
  direction: number // Compass direction (radians)
  accuracy: number // Compass accuracy level
}
```
Property description:
- `direction`: The angle in radians between the Y-axis of the device and the Earth's magnetic north pole, the value range is $[0,2\pi]$, where:
  - `0`: due north direction
  - `Math.PI/2` (about 1.57): due east
  - `Math.PI` (about 3.14): due south direction
  - `3 * Math.PI / 2` (approximately 4.71): due west
- `accuracy`: accuracy level of compass data
  - `3`: high accuracy
  - `2`: medium accuracy
  - `1`: low precision
  - `0`: Untrustworthy (unknown reason)
  - `-1`: Untrusted (sensor lost connection)

Example:
``` js
// Determine direction
const data = await compass.getValue()
const degrees = data.direction * 180 / Math.PI // Convert to angle

console.log(`Direction: ${degrees}°`)
if (degrees >= 337.5 || degrees < 22.5) {
  console.log('Towards north')
} else if (degrees >= 22.5 && degrees < 67.5) {
  console.log('Towards the northeast')
} else if (degrees >= 67.5 && degrees < 112.5) {
  console.log('Towards the east')
}
// ...judgment in other directions

// Check accuracy
if (data.accuracy >= 2) {
  console.log('Compass accuracy is good')
} else if (data.accuracy === 1) {
  console.log('Compass accuracy is low, calibration is recommended')
  compass.calibration()
} else {
  console.log('Compass data is not trustworthy')
}
```
