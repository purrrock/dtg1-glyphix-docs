# 定时器

本模块提供定时器功能，用于延迟执行或周期性执行代码。定时器 API 无需导入即可直接使用。

## 接口定义

### `setTimeout` <decl type="(callback: () => void, duration: number): number" />

设置一个定时器，在指定的延迟时间之后执行回调函数。参数说明：
- `callback`：延迟时间到达后要执行的回调函数；
- `duration`：延迟的时间，单位为毫秒。

返回一个定时器 ID，可用于通过 [`clearTimeout()`](#cleartimeout) 方法取消该定时器。

示例：
``` js
// 1 秒后执行回调函数
const timerId = setTimeout(() => {
  console.log('1 秒已过')
}, 1000)
```

### `setInterval` <decl type="(callback: () => void, duration: number): number" />

设置一个定时器，按照指定的周期重复执行回调函数。参数说明：
- `callback`：每次定时器触发时要执行的回调函数；
- `duration`：执行周期，单位为毫秒。

返回一个定时器 ID，可用于通过 [`clearInterval()`](#clearinterval) 方法取消该定时器。

示例：
``` js
// 每隔 500 毫秒执行一次回调函数
const timerId = setInterval(() => {
  console.log('又过了 500 毫秒')
}, 500)
```

### `clearTimeout` <decl type="(timerId: number): void" />

取消由 [`setTimeout()`](#settimeout) 方法设置的定时器。`timerId` 参数是要取消的定时器 ID。

::: warning
与 Web 环境不同，本实现中的定时器 ID 池**有可能被复用**。因此，**不要**对同一个有效的定时器 ID 重复调用 `clearTimeout()`，否则可能会意外停止其他正在运行的定时器。

推荐在清理定时器后将其 ID 置为 `null`，以避免重复清理。`clearTimeout()` 可以安全地接受 `null`、`0` 等无效 ID，这些调用不会产生副作用。
:::

示例：
``` js
const timerId = setTimeout(() => {
  console.log('这条消息不会输出')
}, 1000)

// 在定时器触发之前取消它
clearTimeout(timerId)
```

推荐的做法是在清理后将定时器 ID 置空，避免重复清理有效 ID：
``` js
export default {
  onInit() {
    this.timerId = setTimeout(() => {
      console.log('定时器触发')
      this.timerId = null // 执行后清空 ID
    }, 1000)
  },
  onDestroy() {
    // 可以安全地清理，即使 timerId 为 null
    clearTimeout(this.timerId)
  },
  someMethod() {
    // 清理定时器并置空
    clearTimeout(this.timerId)
    this.timerId = null
  },
}
```

### `clearInterval` <decl type="(timerId: number): void" />

取消由 [`setInterval()`](#setinterval) 方法设置的定时器。`timerId` 参数是要取消的定时器 ID。

::: warning
与 Web 环境不同，本实现中的定时器 ID 池**有可能被复用**。因此，**不要**对同一个有效的定时器 ID 重复调用 `clearInterval()`，否则可能会意外停止其他正在运行的定时器。

推荐在清理定时器后将其 ID 置为 `null`，以避免重复清理。`clearInterval()` 可以安全地接受 `null`、`0` 等无效 ID，这些调用不会产生副作用。
:::

示例：
``` js
let count = 0
const timerId = setInterval(() => {
  count++
  console.log(`执行次数: ${count}`)
  if (count >= 5)
    clearInterval(timerId) // 执行 5 次后停止
}, 500)
```

::: tip
`clearInterval` 和 `clearTimeout` 实际上是同一个函数的两个别名，但建议使用对应的方法以保持代码清晰。
:::

## 开发笔记

### 定时器 ID 复用

本实现与 Web 标准环境存在一个重要区别：**定时器 ID 可能会被复用**。

在 Web 浏览器和 Node.js 中，每次调用 `setTimeout()` 或 `setInterval()` 都会返回一个唯一的、单调递增的 ID，这些 ID 不会被复用。因此在 Web 环境中，对已清理或无效的定时器 ID 调用 `clearTimeout()` 或 `clearInterval()` 是安全的，不会产生副作用。

然而，在本实现中，定时器 ID 来自一个有限的 ID 池，当定时器被清理或执行完成后，其 ID 可能会被新创建的定时器复用。这意味着如果重复清理同一个 ID（即由 `setTimeout()` 或 `setInterval()` 返回的数字），就可能会意外停止另一个正在运行的定时器。

`clearTimeout()` 和 `clearInterval()` 可以安全地接受 `null`、`0`、`undefined` 等非定时器 ID 的值，这些调用不会产生副作用。

因此，**务必遵循以下最佳实践**：
1. 每个定时器 ID 仅清理一次；
2. 清理后将定时器 ID 置为 `null`、`0` 或 `undefined`，避免意外地重复清理。

`clearTimeout()` 和 `clearInterval()` 可以安全地接受 `null`、`0` 等非定时器 ID 的值，因此无需在调用前进行有效性判断。

前面 API 文档中的示例展示了推荐的做法。

例外情况是，你可以在 `setTimeout` 的回调函数中清理自身的定时器 ID：
``` js
let timer = setTimeout(() => {
  clearTimeout(timer) // 这不会影响其他定时器，也不会触发警告日志
}, 1000)
```

### 定时器精度问题

定时器 API **不保证精确的时间间隔**，实际执行时间可能会有偏差。这是因为：
- 系统调度和性能限制可能导致定时器触发时间不准确；
- 定时器的最小间隔受到系统限制，并随时受到低功耗策略影响。

因此，**不要**使用定时器 API 来进行精确计时。如果需要测量时间间隔或实现计时器功能，应该使用 `Date` 对象来获取实际的时间戳。

#### 错误示例：使用定时器计数来计时

下面的代码试图通过累加定时器触发次数来计算经过的时间，这是不正确的做法：
``` js
export default {
  data: {
    elapsedTime: 0, // 通过累加来计算经过时间
  },
  onInit() {
    // 错误：假设定时器每秒精确触发一次
    this.timerId = setInterval(() => {
      this.elapsedTime += 1000
    }, 1000)
  },
  onDestroy() {
    clearInterval(this.timerId)
  },
}
```

这种方法的问题在于，即使设置的间隔是 $1000\rm ms$，实际触发间隔可能是 $1010\rm ms$ 甚至更长。累计误差会导致计时越来越不准确。在设备进入低功耗模式后，定时器可能以秒级别的精度运行，或被直接挂起。

#### 正确示例：使用 Date 对象计时

正确的做法是记录起始时间戳，然后在每次更新时计算与当前时间的差值：
``` js
export default {
  data: {
    elapsedTime: 0, // 经过的时间（毫秒）
  },
  onInit() {
    // 记录起始时间戳
    this.startTime = Date.now()
    // 使用定时器定期更新显示
    this.timerId = setInterval(() => {
      // 通过计算时间戳差值来获取实际经过的时间
      this.elapsedTime = Date.now() - this.startTime
    }, 100) // 可以设置较短的更新间隔以提高显示流畅度
  },
  onDestroy() {
    clearInterval(this.timerId)
  },
}
```

### 完整的计时器示例

下面是一个完整的计时器组件示例，展示了如何正确实现开始、暂停和重置功能：

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
    elapsedTime: 0,     // 已经过的时间（毫秒）
    isRunning: false,   // 计时器是否正在运行
  },
  onInit() {
    this.startTime = 0       // 本次启动的时间戳
    this.accumulatedTime = 0 // 累计的时间（用于暂停后继续）
    this.timerId = null
  },
  onDestroy() {
    // 清理定时器
    clearInterval(this.timerId)
  },
  start() {
    if (this.isRunning)
      return // 已经在运行，避免重复启动

    this.isRunning = true
    // 记录本次启动的时间戳
    this.startTime = Date.now()

    // 定期更新显示
    this.timerId = setInterval(() => {
      // 累计时间 + (当前时间 - 本次启动时间)
      this.elapsedTime = this.accumulatedTime + (Date.now() - this.startTime)
    }, 20)
  },
  pause() {
    if (!this.isRunning)
      return // 已经暂停，无需操作

    this.isRunning = false
    // 停止定时器
    clearInterval(this.timerId)
    this.timerId = null // 清理后置空

    // 保存累计时间，以便下次继续
    this.accumulatedTime = this.elapsedTime
  },
  reset() {
    // 停止计时器
    this.isRunning = false
    clearInterval(this.timerId)
    this.timerId = null // 清理后置空

    // 重置所有状态
    this.elapsedTime = 0
    this.accumulatedTime = 0
    this.startTime = 0
  },
  formatTime(ms) {
    // 将毫秒转换为 "分:秒.毫秒" 格式
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

这个示例展示了：
- 使用 `Date.now()` 获取准确的时间戳，并通过时间戳差值计算实际经过的时间；
- `setInterval()` 仅用于定期更新界面显示；
- 正确处理开始、暂停和重置的状态转换；
- 在组件销毁时清理定时器资源。

### 内存泄漏预防

使用定时器时务必注意及时清理，否则可能导致内存泄漏或者访问已经销毁的组件。在组件的 [`onDestroy()`](/framework/component/life-cycle.md) 生命周期函数中清理所有定时器：
``` js
export default {
  onInit() {
    this.timerId = setTimeout(() => {
      // 执行某些操作
      this.timerId = null // 执行后置空
    }, 5000)
  },
  onDestroy() {
    // 清理定时器，防止内存泄漏
    clearTimeout(this.timerId)
  },
}
```

对于 `setInterval()` 创建的周期性定时器，这一点尤为重要，因为它们会持续运行直到被显式取消。
