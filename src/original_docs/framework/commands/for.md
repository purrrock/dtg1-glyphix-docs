---
icon: format-list-bulleted
---
# for 指令

`for` 指令用于列表渲染。

## 语法

``` html
<div for="expr"></div> <!-- 不定义下标和迭代变量 -->
<div for="value in expr"></div> <!-- 不定义下标变量 -->
<div for="index, value in expr"></div>
<div for="(index, value) in expr"></div>
```
`expr` 表达的值是一个 [`Array` 对象](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)或者数值，`for` 指令会遍历整个列表并在迭代过程中传递下标值和迭代项的值。如果不定义下标变量或迭代变量，那么下标变量的默认名称为 `$idx`，迭代变量的默认名称为 `$item`。

当 `for` 指令和 `if` 指令同时存在时，`if` 指令的优先级更高。这意味着如果 `if` 指令值为假，整个列表都不会渲染。

`for` 指令的属性值支持[指令属性值](/framework/component/template.md#指令属性值)语法，因此也可以使用双大括号包围表达式。

::: warning
不推荐同时使用 `if` 和 `for` 指令以提升代码可读性。
:::

## 列表渲染

通过 `for` 指令将一个 [JavaScript 数组](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/First_steps/Arrays)渲染为列表。它通常用于 [`scroll`](/components/scroll.md) 的子组件上，例如：
``` html
<scroll :damping="damping">
  <p for="item in items" class="item">
    {{ item.message }}
  </p>
</scroll>
```
`p` 组件上的 `for` 指令会遍历 `items` 数组并为每个迭代项生成一个 `p` 组件节点。`item` 是迭代项的变量名，在 `{{ item.message }}` [插值表达式](/framework/component/template.md#插值表达式)中访问了它的 `message` 属性。

`items` 是一个类型为数组的[组件对象属性](/framework/component/component-object.md)，例如：
``` js
export default {
  data: {
    items: [
      { message: 'Foo' },
      { message: 'Bar' },
      { message: 'Baz' },
    ]
  }
}
```

此代码会渲染出以下界面：

<glyphix id="commands-for-1" height="200" width="360" inline>

``` html
<scroll :damping="damping">
  <p for="item in items" class="item">
    {{ item.message }}
  </p>
</scroll>
```

``` js
export default {
  data: {
    items: [
      { message: 'Foo' },
      { message: 'Bar' },
      { message: 'Baz' },
    ]
  }
}
```

``` css
scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
}

.item {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 40px 10px;
  margin: 10px;
  border-radius: 16px;
}
```

</glyphix>

渲染结果是一个包含三个表项的可滚动列表，内容为 “Foo”，“Bar” 和 “Baz”。你可以在原生[组件](/framework/component/README.md)或者自定义组件上使用 `for` 指令来实现列表渲染。

也可以使用默认的 `$item` 迭代变量名：
``` html
<scroll :damping="damping">
  <p for="items" class="item">
    {{ $item.message }}
  </p>
</scroll>
```
这样的渲染结果和上面是一样的。

## 嵌套和作用域

在同一个标签中，下标和迭代变量必须在 `for` 指令之后才可以访问，因此需要注意相关属性的顺序：
``` html
<panel for="value in expr" title="value.title"></panel> <!-- 正确 -->
<panel title="value.title" for="value in expr"></panel> <!-- 错误 -->
```
错误的顺序不会导致编译报错，而是尝试在 `this` 作用域中查找 `value` 属性。换言之，`for` 指令中定义的变量会隐藏外层作用域的名字，这包括：
- 组件的 view-model（即通过 `this` 的属性访问）
- 全局对象

考虑到变量作用域和指令优先级的问题，`if` 指令应位于 `for` 指令之前，否则可能会引起令人困惑的行为。

对于当前组件节点，`for` 指令中定义的变量只在其之后的属性中可见。也在静态的子组件中可以见，例如
``` html
<panel for="value in expr" title="value.title">
  <p>message: {{value.message}}</p>
</panel>
<p>{{value.message}}</p> <!-- 此时访问 this.value.message -->
```
除最后一个 `{{value.message}}` 表达式以外，其他几处 `value` 均在 `for` 指令的作用域内。

`for` 指令可以嵌套使用，此时的作用域规则同上。注意，同名下标和迭代变量的作用域会被内层的 `for` 指令隐藏，因此需要显式地定义这些变量。

## 数组变化侦测

`for` 指令可以检测[响应式](/framework/component/component-object.md#响应式编程)数组的变化并更新界面。以下操作都会触发 `for` 渲染更新：
- 替换一个新数组；
- 调用数组更新方法，如 [`push()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/push)，[`pop()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/pop)，[`shift()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/shift)，[`unshift()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/unshift)，[`splice()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/splice)，[`sort()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/sort) 和 [`reverse()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/reverse)。

### 替换一个数组

可以将用于列表渲染的响应式属性替换为一个新的数组来触发界面更新。例如：
``` js
this.items = this.items.filter((item) => item.message.match(/Foo/))
```
这样，`this.items` 被赋值为一个新的数组，`for` 指令会在该操作之后重新渲染新的列表。

::: tip
数组有一些不可变 (immutable) 方法，例如 `filter()`，`concat()` 和 `slice()`，这些都不会更改原数组，而总是**返回一个新数组**。当遇到不可变方法时，需要用上面的方法将旧的数组替换为新的。
:::

### 数组更新方法

使用数组的更新方法也可以触发视图更新，例如：
``` js
// 在原有的列表底部插入一个内容为 Grault 的新元素
this.items.push({ message: 'Grault' })
```

还可以直接修改数组长度来截断数组，如：
``` js
// 删除列表中第三项之后的元素
this.items.length = 2
```

还可以更改列表的元素：
``` js
// 将第二个元素内容更改为 Grault
this.items[1] = { message: 'Grault' }
```

::: warning
`for` 指令目前无法追踪列表元素的属性更改，详见[列表元素更新](#列表元素更新)。
:::

## 缺陷和限制

### 列表元素更新

`for` 指令无法监听数组项目的深层属性更新，这意味着
``` js
this.items[1].message = 'Grault'
```
将不能正确地触发界面更新。为了解决这种问题，必须将数组项目替换为一个新的对象：
``` js
this.items[1] = { message: 'Grault' }
```

当项目对象的属性比较多，但只希望更新其中少数属性的时候，建议先使用[展开语法（`...`）](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Spread_syntax) 拷贝对象，然后再更新属性：
``` js
this.items[1] = {
  ...this.items[1], // 拷贝第二个元素的所有属性
  message: 'Grault' // 更新 message 属性
}
```

::: warning
数组项目对象的属性数量会对性能造成影响，当你发现列表更新卡顿时，请参阅[不必要的更新](#不必要的更新)。

由于界面中的其他元素一起更新等原因，直接更改项目的深层属性后界面也许会更新，但是这并不稳定，请不要这样使用。
:::

### 列表下标问题

`for` 指令虽然支持在渲染时获取项目下标，如：
``` html
<p for="index, value in items">
  {{ index }} - {{ value }}
</p>
```
但是目前并不支持响应式地更新下标，对 `items` 数组的修改可能会导致显示错乱。更新整个数组可以避免这个问题。

但由于某些优化机制，开发者很难保证**真正地**更新整个 `items` 数组，这会导致奇怪的非预期下标错乱问题。

### 不必要的更新

列表渲染可能是流畅性和性能的瓶颈之一，尤其是长列表的渲染速度可能较慢。减少不必要的列表更新可能是一种有效的优化手段。

#### 直接更新列表

考虑这样的一个列表：
``` html
<div for="(idx, task) in tasks" on:click="process(idx)">
  <p>{{ task.name }}</p>
  <p>{{ task.progress }}%</p>
</div>
```
这是一个任务处理界面，它显示一个任务列表并在用户点击时处理某个任务。简单起见，我们这样初始化这个任务列表：
``` js
this.tasks = Array.from({ length: 10 },
  (_, i) => ({ name: `Task #${i + 1}`, progress: 0 }))
```
此时你会看到一个包含 10 个项目的任务清单。以下的 `process()` 方法简单地实现了任务进度的更新：
``` js
process(idx) { // idx 是点击的任务项目下标
  this.tasks[idx].progress = 0
  // 创建一个定时器来模拟处理进度
  let timer = setInterval(() => {
    // 由于 for 指令不支持深层属性更新，所以先拷贝一个对象
    let task = {...this.tasks[idx]}
    task.progress += 10
    this.tasks[idx] = task
    if (task.progress >= 100)
      clearInterval(timer) // 处理完成时删除定时器
  }, 100)
}
```
如下所示，这个实现是可以正常交互的。

<glyphix id="commands-for-tasklist-1" height="360" width="360" title="任务清单列表">

``` html
<scroll>
  <div for="(idx, task) in tasks" on:click="process(idx)">
    <p>{{ task.name }}</p>
    <p>{{ task.progress }}%</p>
  </div>
</scroll>
```

``` js
export default {
  data: {
    tasks: []
  },
  onInit() {
    this.tasks = Array.from({ length: 10 },
      (_, i) => ({ name: `Task #${i + 1}`, progress: 0 }))
  },
  process(idx) {
    this.tasks[idx].progress = 0
    let timer = setInterval(() => {
      let task = {...this.tasks[idx]}
      task.progress += 10
      this.tasks[idx] = task
      if (task.progress >= 100)
        clearInterval(timer)
    }, 100)
  }
}
```

``` css
scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
}

div {
  color: #fafafa;
  background-color: #bdbdbd;
  display: flex;
  justify-content: space-between;
  padding: 40px 10px;
  margin: 10px;
  border-radius: 16px;
}
```

</glyphix>

这种简单的方法在复杂且较长的列表界面中可能会变得很卡顿，此时你可能会观察到：
- 界面中的进度等动画出现掉帧；
- 在列表中上下滚动会变得明显卡顿。

#### 通过子组件优化

一种优化方法是将项目拆分成一个独立的组件，在本示例中可以添加一个 `Task` 组件：
``` html
<div on:click="process">
  <p>{{ name }}</p>
  <p>{{ progress }}%</p>
</div>
```
`Task` 组件的 JavaScript 脚本中可以处理自己的 `process()` 操作：
``` js
export default {
  data: {
    name: null, // 任务名字要在外层传入
    progress: 0
  },
  // 每个 Task 组件对象会处理自己的 process 操作，
  // 并通过 this 访问自己的响应式属性。
  process() {
    this.progress = 0
    let timer = setInterval(() => {
      this.progress += 10
      if (this.progress >= 100)
        clearInterval(timer)
    }, 100)
  }
}
```

相比于之前的方法，新的方案在[引入 `Task` 组件](/framework/component/README.md#引入组件)之后直接使用即可：
``` html
<task for="task in tasks" :name="task.name" />
```
而父组件的 JavaScript 代码也可以更简单：
``` js
export default {
  data: {
    tasks: []
  },
  onInit() {
    for (let i = 0; i < 10; ++i)
      this.tasks.push({ name: `Task #${i + 1}` })
  }
}
```
这相比于直接更新列表有以下变化：
- 插入的数组项目没有 `progress` 属性，因为它只需要在 `Task` 子组件中处理；
- `process()` 方法被删除并移动到了 `Task` 组件内；
- 不需要使用 `idx` 下标变量来区分不同的项目。

这种方式可以实现相同的任务列表界面，只是将 `progress` 的处理移动到了 `Task` 子组件内，从而避免在修改进度时更新任务数组。使用这种方法可以优化列表元素内部界面更新的问题，同时可以降低代码复杂度。
