# Compass

The `@system.compass` module provides the ability to access the device's compass sensor, allowing you to obtain the device's orientation relative to the Earth's magnetic North Pole.

## Import Module

``` js
import compass from '@system.compass'
```

## Interface Definitions

### `subscribe` <decl type="(callback: (data: Value) => void): number" method/>

Subscribes to compass data changes. When the device orientation changes, the callback function is automatically invoked. The `callback` function receives compass data of type [`Value`](#value).

Returns a subscription ID used for unsubscribing.

### `unsubscribe` <decl type="(subscribeId: number): void" method/>

Unsubscribes from compass data. The `subscribeId` parameter is the subscription ID returned by the [`subscribe()`](#subscribe) method.

This method should be called to cancel the `subscribe()` subscription when the page or component is destroyed:
``` js
const subscribeId = compass.subscribe((data) => {
  console.log(`Direction: ${data.direction} rad`)
  console.log(`Accuracy: ${data.accuracy}`)
})

// Unsubscribe
compass.unsubscribe(subscribeId)
```


### `calibration` <decl type="(): Promise<void>" method/>

Starts the compass calibration process. When the compass accuracy is low, guide the user to perform actions and call this method to calibrate the compass.

This function returns a Promise object with no result, which is resolved when the system completes the calibration.

### `getValue` <decl type="(): Promise<Value>" method/>

Gets the current compass data. Returns an asynchronous result as a Promise object containing compass direction and accuracy information (of type [`Value`](#value)).

Example:
``` js
// Using Promise
compass.getValue().then((data) => {
  console.log(`Direction: ${data.direction} rad`)
  console.log(`Accuracy level: ${data.accuracy}`)
})

// Using async/await
async function getCompassData() {
  const data = await compass.getValue()
  console.log(`Direction: ${data.direction} rad`)
  console.log(`Accuracy level: ${data.accuracy}`)
}
```

::: note
Due to implementation limitations, this method does not support callback-style calls (such as `{ success: (data) => {...} }`); please use Promise or async/await instead.
:::

## Type Definitions

### `Value`

The signature of the compass data type `Value` is as follows:
``` ts
type Value = {
  direction: number  // Compass direction (in radians)
  accuracy: number   // Compass accuracy level
}
```
Property descriptions:
- `direction`: The angle in radians between the device's Y-axis and the Earth's magnetic North Pole, with a value range of $[0,2\pi]$, where:
  - `0`: Due North
  - `Math.PI / 2` (approx. 1.57): Due East
  - `Math.PI` (approx. 3.14): Due South
  - `3 * Math.PI / 2` (approx. 4.71): Due West
- `accuracy`: The accuracy level of the compass data
  - `3`: High accuracy
  - `2`: Medium accuracy
  - `1`: Low accuracy
  - `0`: Unreliable (reason unknown)
  - `-1`: Unreliable (sensor disconnected)

Example:
``` js
// Determine direction
const data = await compass.getValue()
const degrees = data.direction * 180 / Math.PI // Convert to degrees

console.log(`Direction: ${degrees}°`)
if (degrees >= 337.5 || degrees < 22.5) {
  console.log('Facing North')
} else if (degrees >= 22.5 && degrees < 67.5) {
  console.log('Facing Northeast')
} else if (degrees >= 67.5 && degrees < 112.5) {
  console.log('Facing East')
}
// ... Other direction checks

// Check accuracy
if (data.accuracy >= 2) {
  console.log('Compass accuracy is good')
} else if (data.accuracy === 1) {
  console.log('Compass accuracy is low, calibration recommended')
  compass.calibration()
} else {
  console.log('Compass data is unreliable')
}
```