# 组件对象

位于 UX 文件内的 `<script>` 标签定义并导出了一个组件对象。一个典型的组件对象定义如下：
``` js
export default {
  data: {
    text: "Hello world"
  },
  onInit() {
    console.log("component onInit()")
  },
  clicked(event) {
    console.log(`clicked: ${event}`)
  }
}
```
组件框架允许开发者为组件对象填写一些属性来实现功能，本文档将介绍这些属性。

## 响应式编程

**响应式编程**是一种用于动态更新界面和数据状态的编程范式。通过**响应式属性**，开发者可以自动追踪数据的变化并更新界面，无需手动触发和管理这些更新。这使得数据与界面始终保持同步，实现简洁高效的 UI 编程体验。

### 响应式属性

组件对象的 [`data` 属性](#data-属性)和 [`computed` 属性](#computed-属性)对象中定义的属性都是组件的**响应式属性**，也称为 view-model 属性：
- **`data` 属性**：直接反映组件的状态。例如，温度值、显示文本或按钮状态等都可以定义在 `data` 中。当这些属性值发生变化时，框架会自动同步到视图中。
- **`computed` 属性**：用于定义基于 `data` 或其他 `computed` 属性计算得到的派生属性。计算属性会自动随依赖数据的变化而更新，使得复杂的逻辑表达更直观、简洁。

总而言之，当组件的响应式属性值发生变化时，依赖这些属性的内容会自动更新并进行渲染，从而保证显示的内容与数据保持一致。

### 自动数据绑定

**自动数据绑定**是响应式编程的核心概念，它使得数据的变化能够直接反映到界面上，而无需开发者手动处理。

由于每个响应式属性与界面的相关部分是自动绑定的，当属性值发生变化时，界面会自动更新，无需调用特定元素的属性更新函数。

例如定义一个名为 `counter` 的响应式属性：
``` js
export default {
  data: { // 将 counter 响应式属性定义在 data 对象中
    counter: 0 // 初始值为 0
  }
}
```

每当 `counter` 的值发生变化，引用该属性的界面也会自动更新。下面的[模板](template)代码演示了这个机制：
``` html
<p on:click="counter += 1">
  counter: {{ counter }}
</p>
```
此示例演示了点击 `<p>` 标签时会使 `counter` 显示值加 1 的计数器。你可以点击下面的在线 demo 来测试它：

<glyphix id="component-object-reactive" height="50" width="200" inline>

``` html
<p on:click="counter += 1">
  counter: {{ counter }}
</p>
```

``` js
export default {
  data: {
    counter: 0
  }
}
```

``` css
p {
  border: 2px solid gray;
  border-radius: 16px;
  padding: 2px 8px;
  text-align: center;
  height: 100%;
}
```

</glyphix>

`<p>` 标签内的 `{{ counter }}` 是一个模板[插值表达式](template.md#插值表达式)，它对 `counter` 的依赖是自动绑定的。而 `<p>` 标签中的 [`on:click` 监听](/framework/commands/on.md)在点击时修改 `counter` 属性值。可以看到，通过自动数据绑定的方式，消除了传统 GUI 开发中的手动**数据**-**界面**更新的操作，使界面逻辑更加简洁明了。

## `data` 属性

`data` 属性用于声明组件的响应式数据属性。该属性是一个对象，例如：
``` js
export default {
  data: {
    text: "Hello world"
  }
}
```
`data` 属性的值要能通过 `JSON.stringify()` 进行序列化，准确来说必须满足下列条件：
- 简单类型的值：`number`、`string`、`boolean`、`null` 或 `undefined`
- 具有递归结构的 `Object` 和 `Array` 中，最深层元素的值必须属于上述中的一种

这意味着源代码中 `data` 对象的属性不能有函数或其他特殊类型的值，这也包括 `Date` 这样的对象。

::: note
`data` 对象不支持非 JSON 兼容的数据类型，例如 `Date`、`Proxy` 对象等等，这是一个已知的限制。如果需要使用这些类型的数据，可以将它们定义为[自定义属性](#自定义属性)，否则会导致不可预期的行为。
:::

`data` 属性都是组件的 view-model 属性，因此其中数据可用于响应式编程。在组件对象中使用 `this.prop` 的写法可以直接访问 `data` 对象中的属性。因此，在下面的组件对象中
``` js
export default {
  data: {
    onInit: true
  },
  onInit() {}
}
```
代码 `this.onInit` 将会访问 `data` 对象中的 `onInit` 属性，而不是生命周期函数 `onInit`。

::: tip
为了优化性能，仅将用于 UI 呈现和状态管理的数据定义在 `data` 对象中。对于不需要响应式的数据，可以将它们定义为[自定义属性](#自定义属性)。例如：定时器 ID（`setTimeout()` 的返回值）、[音频播放器](/api/system-media.md#createaudioplayer)句柄、WebSocket 连接对象等。这类对象通常没有必要作为响应式属性，并且无法正常工作。
:::

## `computed` 属性

组件对象的 `computed` 属性对象对象声明组件中的计算属性。相比于 `data` 中的响应式属性，计算属性可以实现需要一些计算才能得到结果的属性。例如
``` html
<text> reversed message: {{ reversedMessage }}
```

``` js
export default {
  data: {
    message: "hello"
  },
  computed: {
    reversedMessage() { // 这是 reversedMessage 计算属性的 getter 方法
      return this.message.split('').reverse().join('')
    }
  }
}
```
这里声明了一个 `reversedMessage` 计算属性，该属性实现了一个 getter 函数用于获取属性值。直接使用 `this.reversedMessage`（在模板中可以省略 `this.`）即可获取该计算属性的值。

计算属性也是组件的 view-model 属性。计算属性的值会被缓存，因此多次获取计算属性的值也不会重复计算。另一方面，计算属性会所依赖的 view-model 属性变化后会自动更新。在这个例子中，计算属性的值是由 `message` 属性计算得出的，因此 `message` 属性变化时，`reversedMessage` 属性的值会自动更新。

### 计算属性的 setter 方法

默认的计算属性只有 getter 方法，但你还可以为计算属性提供 setter 方法：
``` js
export default {
  data: {
    message: "hello"
  },
  computed: {
    reversedMessage: {
      get() { // 这是 reversedMessage 计算属性的 getter 方法
        return this.message.split('').reverse().join('')
      },
      set(value) {
        this.message = value.split('').reverse().join('')
      }
    }
  }
}
```
此时，计算属性 `reversedMessage` 的值不再是一个函数，而是一个对象，后者有两个方法：getter 方法 `get` 和 setter 方法 `set`。`set` 方法的参数就是计算属性需要被设置的新值。

## `watch` 属性

`watch` 对象方法用于监听 view-model 属性的变化，例如：
``` js
export default {
  data: {
    value: 0
  },
  watch: {
    value(newValue, oldValue) {
      console.log(`value change: ${oldValue} -> ${newValue}`)
    }
  }
}
```
`watch` 对象的方法会监听同名 view-model 属性的变化，因此 `watch.value()` 监听 `value` 属性变化。计算属性的变化也可以由 `watch` 监听。

## 生命周期函数

详见[生命周期](life-cycle.md)文档。

## 自定义属性

用户还可以在组件对象中定义自定义属性，这些属性不在 view-model 中（即不在 `data` 或者 `computed` 对象中），因此不是是响应式的。开发者可以将方法定义为自定义属性，还可以使用自定义属性存储一些不需要响应式的数据。例如：
``` html
<p on:click="onClick()">{{ text }}</p>
```

``` js
export default {
  data: {
    text: "some text"
  },
  // 自定义属性不在 data 或者 computed 对象中，直接定义在组件对象内
  timer: null, // 存储定时器句柄，可以不事先定义，this.timer 赋值时会自动创建此属性
  onInit() {
    // 对 this 赋值的新属性是自定义属性
    this.timer = setInterval(() => this.text += "?", 1000)
  },
  onDestroy() {
    clearInterval(this.timer)
  },
  onClick() {
    this.text += "." // 在自定义方法中操作 view-model 属性
  }
}
```

例子中的 `text` 属性是响应式的，而 `timer` 是非响应式的自定义属性。`timer` 属性用于存储定时器句柄，这个值和界面视图没有关系，因此不需要作为 view-model 属性。考虑到代码的规范性，也可以在组件对象中事先定义自定义属性：
``` js
export default {
  data: {
    text: "some text"
  },
  timer: null, // 自定义属性是组件对象的直接属性
  // ...
}
```
如例子中所示，自定义属性直接定义在组件对象内即可。每个组件的自定义属性都是不同的实例而不会共享。

::: warning
自定义属性、`data` 对象、 `computed` 对象、生命周期函数等属性都不能出现重名，否则会使某些属性被覆盖而无法访问。
:::

### 方法

自定义属性和方法都是组件对象的直接属性，两者本质上是等价的。当你把一个函数赋值给组件对象的属性时，这个属性就变成了一个方法。本节通过两个例子展示这种等价性。

方式一：直接定义方法，这是最常见且推荐的写法。
``` js
export default {
  data: {
    count: 0
  },
  increment() {
    this.count++
  }
}
```

方式二：定义属性并赋值为函数。
``` js
export default {
  data: {
    count: 0
  },
  increment: function() {
    this.count++
  }
}
```
两种写法在功能上完全一致，都可以通过 `this.increment()` 调用。在模板中使用时也是相同的：
``` html
<button on:click="increment()">Count: {{ count }}</button>
```

::: tip
推荐使用方式一的写法，这是 ES6+ 标准支持的对象方法语法，更加简洁明了。
:::

### 动态赋值方法

除了在组件对象中直接定义方法外，还可以在组件实例化后（如在 `onInit` 生命周期中）动态赋值方法。这种方式的关键特点是：每个组件实例的动态方法是独立的，可以通过闭包捕获和保持不同的状态。

考虑一个定时器组件，每个实例都有自己的计数器，并且可以独立停止。这是动态赋值方法的典型应用场景：
``` html
<div>
  <text>timeout: {{ counter }}</text>
  <button on:click="stopTimer">Stop</button>
</div>
```

``` js
export default {
  data: {
    counter: 0,
  },
  stopTimer: null, // 可选：预定义 stopTimer 方法
  onInit() {
    const timer = setInterval(() => {
      this.counter++
    }, 1000)
    // 动态创建 stopTimer 方法，通过闭包捕获 timer 变量
    this.stopTimer = () => {
      clearInterval(timer)
      this.stopTimer = null // 停止后将方法置空
    }
  },
}
```

下面的示例同时实例化了 4 个定时器组件，你可以尝试独立停止其中任意一个：

<glyphix id="component-object-dynamic-method" height="200" width="300" inline>
</glyphix>

这种动态赋值方法的实现依赖于以下几个关键点：
- **闭包捕获**：在 `onInit` 中创建的 `timer` 常量是一个局部变量，`stopTimer` 方法通过闭包捕获了这个变量
- **实例独立性**：每个组件实例调用 `onInit` 时都会创建自己的 `timer` 和 `stopTimer`，它们互不干扰
- **状态隔离**：点击某个实例的 "Stop" 按钮只会停止该实例的定时器，不影响其他实例

当然，对于本示例来说，更常见的做法是将 `stopTimer` 方法直接定义在组件对象中：
``` js
export default {
  data: {
    counter: 0,
  },
  timer: null,
  onInit() {
    // 这种情况下需要将 timer 作为自定义属性存储
    this.timer = setInterval(() => {
      this.counter++
    }, 1000)
  },
  stopTimer() {
    // stopTimer 方法访问 this.timer 以停止定时器
    clearInterval(this.timer)
    this.timer = null // 清除 timer 引用
  }
}
```
这对于定时器来说通常更加直观，但是在一些带有复杂上下文，并需要动态分发策略时，可以使用动态赋值方法来实现更灵活的逻辑。下表展示了动态方法 vs 直接定义方法的区别：

| 特性 | 直接定义方法 | 动态赋值方法 |
|------|------------|------------|
| 共享性 | 所有实例共享同一个函数对象 | 每个实例有独立的函数副本 |
| 闭包捕获 | 不捕获作用域中的局部变量 | 可以捕获作用域中的局部变量 |
| 内存占用 | 更少（共享） | 稍多（每实例一份） |
| 适用场景 | 通用的、无状态的操作 | 需要捕获局部状态的操作 |

