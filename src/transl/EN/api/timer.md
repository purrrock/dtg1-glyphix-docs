# Timers

This module provides timer functionality for delayed or periodic code execution. The timer API can be used directly without importing.

## Interface Definitions

### `setTimeout` <decl type="(callback: () => void, duration: number): number" />

Sets a timer that executes a callback function after a specified delay. Parameter descriptions:
- `callback`: The callback function to execute when the delay time is reached;
- `duration`: The delay time in milliseconds.

Returns a timer ID, which can be used to cancel the timer via the [`clearTimeout()`](#cleartimeout) method.

Example:
``` js
// Execute the callback function after 1 second
const timerId = setTimeout(() => {
  console.log('1 second has passed')
}, 1000)
```

### `setInterval` <decl type="(callback: () => void, duration: number): number" />

Sets a timer that repeatedly executes a callback function at specified intervals. Parameter descriptions:
- `callback`: The callback function to execute every time the timer triggers;
- `duration`: The execution interval in milliseconds.

Returns a timer ID, which can be used to cancel the timer via the [`clearInterval()`](#clearinterval) method.

Example:
``` js
// Execute the callback function every 500 milliseconds
const timerId = setInterval(() => {
  console.log('Another 500 milliseconds have passed')
}, 500)
```

### `clearTimeout` <decl type="(timerId: number): void" />

Cancels a timer set by the [`setTimeout()`](#settimeout) method. The `timerId` parameter is the ID of the timer to cancel.

::: warning
Unlike web environments, the timer ID pool in this implementation **may be reused**. Therefore, **do not** call `clearTimeout()` repeatedly on the same valid timer ID, as this may accidentally stop other running timers.

It is recommended to set the timer ID to `null` after clearing it to avoid repeated clearing. `clearTimeout()` can safely accept invalid IDs such as `null` or `0`, and these calls will not produce side effects.
:::

Example:
``` js
const timerId = setTimeout(() => {
  console.log('This message will not be printed')
}, 1000)

// Cancel the timer before it triggers
clearTimeout(timerId)
```

The recommended practice is to set the timer ID to null after clearing it to avoid repeatedly clearing a valid ID:
``` js
export default {
  onInit() {
    this.timerId = setTimeout(() => {
      console.log('Timer triggered')
      this.timerId = null // Clear the ID after execution
    }, 1000)
  },
  onDestroy() {
    // Safe to clear even if timerId is null
    clearTimeout(this.timerId)
  },
  someMethod() {
    // Clear the timer and set to null
    clearTimeout(this.timerId)
    this.timerId = null
  },
}
```

### `clearInterval` <decl type="(timerId: number): void" />

Cancels a timer set by the [`setInterval()`](#setinterval) method. The `timerId` parameter is the ID of the timer to cancel.

::: warning
Unlike web environments, the timer ID pool in this implementation **may be reused**. Therefore, **do not** call `clearInterval()` repeatedly on the same valid timer ID, as this may accidentally stop other running timers.

It is recommended to set the timer ID to `null` after clearing it to avoid repeated clearing. `clearInterval()` can safely accept invalid IDs such as `null` or `0`, and these calls will not produce side effects.
:::

Example:
``` js
let count = 0
const timerId = setInterval(() => {
  count++
  console.log(`Execution count: ${count}`)
  if (count >= 5)
    clearInterval(timerId) // Stop after 5 executions
}, 500)
```

::: tip
`clearInterval` and `clearTimeout` are actually two aliases for the same function, but it is recommended to use the corresponding method to keep the code clear.
:::

## Development Notes

### Timer ID Reuse

There is an important difference between this implementation and standard web environments: **Timer IDs may be reused**.

In web browsers and Node.js, every call to `setTimeout()` or `setInterval()` returns a unique, monotonically increasing ID that is never reused. Therefore, in a web environment, calling `clearTimeout()` or `clearInterval()` on an already cleared or invalid timer ID is safe and has no side effects.

However, in this implementation, timer IDs come from a limited pool. When a timer is cleared or finishes execution, its ID may be reused by a newly created timer. This means that if you repeatedly clear the same ID (i.e., the number returned by `setTimeout()` or `setInterval()`), you might accidentally stop another running timer.

`clearTimeout()` and `clearInterval()` can safely accept non-timer ID values such as `null`, `0`, and `undefined`, and these calls will not produce side effects.

Therefore, **be sure to follow these best practices**:
1. Clear each timer ID only once;
2. Set the timer ID to `null`, `0`, or `undefined` after clearing to prevent accidental repeated clearing.

`clearTimeout()` and `clearInterval()` can safely accept non-timer ID values such as `null` and `0`, so there is no need to check for validity before calling them.

The examples in the API documentation above demonstrate the recommended practices.

An exception is that you can clear a timer ID within its own `setTimeout` callback:
``` js
let timer = setTimeout(() => {
  clearTimeout(timer) // This will not affect other timers, nor will it trigger warning logs
}, 1000)
```

### Timer Precision Issues

Timer APIs **do not guarantee precise time intervals**, and actual execution times may vary. This is because:
- System scheduling and performance constraints may cause timer trigger times to be inaccurate;
- The minimum timer interval is subject to system limitations and is constantly affected by low-power policies.

Therefore, **do not** use timer APIs for precise timing. If you need to measure time intervals or implement timer functionality, you should use the `Date` object to obtain actual timestamps.

#### Incorrect Example: Using Timer Counts for Timing

The code below attempts to calculate elapsed time by accumulating timer trigger counts, which is incorrect:
``` js
export default {
  data: {
    elapsedTime: 0, // Calculate elapsed time by accumulation
  },
  onInit() {
    // Incorrect: Assumes the timer triggers precisely once per second
    this.timerId = setInterval(() => {
      this.elapsedTime += 1000
    }, 1000)
  },
  onDestroy() {
    clearInterval(this.timerId)
  },
}
```

The problem with this approach is that even if the set interval is $1000\rm ms$, the actual trigger interval might be $1010\rm ms$ or even longer. Cumulative errors will make the timing increasingly inaccurate. After the device enters low-power mode, timers may run with second-level precision or be suspended directly.

#### Correct Example: Timing Using the `Date` Object

The correct approach is to record the start timestamp and calculate the difference from the current time on each update:
``` js
export default {
  data: {
    elapsedTime: 0, // Elapsed time in milliseconds
  },
  onInit() {
    // Record the start timestamp
    this.startTime = Date.now()
    // Use a timer to periodically update the display
    this.timerId = setInterval(() => {
      // Get the actual elapsed time by calculating the timestamp difference
      this.elapsedTime = Date.now() - this.startTime
    }, 100) // A shorter update interval can be set to improve display smoothness
  },
  onDestroy() {
    clearInterval(this.timerId)
  },
}
```

### Complete Stopwatch Example

Below is a complete stopwatch component example demonstrating how to correctly implement start, pause, and reset functions:

<glyphix id="api-timer-stopwatch" height="200" width="410">

``` html
<div class="container">
  <text class="timer">{{ formatTime(elapsedTime) }}</text>
  <div class="buttons">
    <text class="button" on:click="start">Start</text>
    <text class="button" on:click="pause">Pause</text>
    <text class="button" on:click="reset">Reset</text>
  </div>
</div>
```

``` js
export default {
  data: {
    elapsedTime: 0,     // Elapsed time (milliseconds)
    isRunning: false,   // Whether the stopwatch is running
  },
  onInit() {
    this.startTime = 0       // Timestamp of the current start
    this.accumulatedTime = 0 // Accumulated time (used to resume after pausing)
    this.timerId = null
  },
  onDestroy() {
    // Clear the timer
    clearInterval(this.timerId)
  },
  start() {
    if (this.isRunning)
      return // Already running, avoid restarting

    this.isRunning = true
    // Record the timestamp of the current start
    this.startTime = Date.now()

    // Periodically update the display
    this.timerId = setInterval(() => {
      // Accumulated time + (Current time - Start time)
      this.elapsedTime = this.accumulatedTime + (Date.now() - this.startTime)
    }, 20)
  },
  pause() {
    if (!this.isRunning)
      return // Already paused, no action needed

    this.isRunning = false
    // Stop the timer
    clearInterval(this.timerId)
    this.timerId = null // Set to null after clearing

    // Save accumulated time for resumption later
    this.accumulatedTime = this.elapsedTime
  },
  reset() {
    // Stop the timer
    this.isRunning = false
    clearInterval(this.timerId)
    this.timerId = null // Set to null after clearing

    // Reset all states
    this.elapsedTime = 0
    this.accumulatedTime = 0
    this.startTime = 0
  },
  formatTime(ms) {
    // Convert milliseconds to "Minutes:Seconds.Milliseconds" format
    const totalSeconds = Math.floor(ms / 1000)
    const minutes = Math.floor(totalSeconds / 60)
    const seconds = totalSeconds % 60
    const milliseconds = Math.floor((ms % 1000) / 10)

    return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(milliseconds).padStart(2, '0')}`
  },
}
```

``` css
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.timer {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 30px;
}

.buttons {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.button {
  padding: 10px 20px;
  margin: 0 10px;
  background-color: #007AFF;
  color: #FFFFFF;
  border-radius: 8px;
  font-size: 0.8rem;
}
```


</glyphix>

This example demonstrates:
- Using `Date.now()` to get accurate timestamps and calculating the actual elapsed time via timestamp differences;
- Using `setInterval()` solely for periodically updating the UI display;
- Correctly handling state transitions for start, pause, and reset;
- Cleaning up timer resources when the component is destroyed.

### Preventing Memory Leaks

Be sure to clear timers promptly when using them; otherwise, it may lead to memory leaks or access to already destroyed components. Clear all timers in the component's [`onDestroy()`](/framework/component/life-cycle.md) lifecycle function:
``` js
export default {
  onInit() {
    this.timerId = setTimeout(() => {
      // Perform some operations
      this.timerId = null // Set to null after execution
    }, 5000)
  },
  onDestroy() {
    // Clear the timer to prevent memory leaks
    clearTimeout(this.timerId)
  },
}
```

This is especially important for periodic timers created with `setInterval()`, as they will continue to run until explicitly cancelled.