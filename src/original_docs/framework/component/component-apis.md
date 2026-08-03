# 组件内置接口

Glyphix 框架为组件内置了一些属性，这些属性都使用 `this.$xxx` 的格式来访问。这些内置属性为组件提供了一些响应式框架以外的功能。

所有的内置属性都是只读的。

## 属性

### `$app` <decl type="Applet" get />

通过 `$app` 属性可以访问 `app.js` 中导出的应用对象。

### `$page` <decl type="Component" get />

通过 `$page` 属性可以访问组件所属页面的组件对象。对于页面组件来说，`this.$page` 的值就是 `this`。

### `$valid` <decl type="boolean" get />

判断组件对象是否有效。值为 `false` 表示组件已经被销毁。

::: tip
对于已经销毁的组件，访问 `$valid` 属性以外的所有操作都是非法的。
:::

#### 已销毁组件

组件的生命周期是由渲染框架控制的，合理编写的代码通常不会访问已经销毁的组件，但是如果忘记在销毁组件时取消定时器或者监听，例如：

``` js
setInterval(() => {
  this.secondCounter += 1
}, 1000)
```

如果组件对象被销毁，你可能遇到这种报错：

```
the component object has been destroyed
  stack backtrace:
    at <anonymous> (pkg://com.example.app/main/index.js:50)
TypeError: proxy: cannot set property
  stack backtrace:
    at <anonymous> (pkg://com.example.app/main/index.js:52)
```

如果确实难以在组件销毁时删除定时器或者取消监听，那么可以通过 `$valid` 属性安全地判断组件是否销毁，以下示例就可以抑制上述运行时错误：

``` js
let timer = setInterval(() => {
  if (this.$valid) {
    this.secondCounter += 1
  } else {
    clearTimeout(timer) // 组件销毁后删除定时器
  }
})
```
这类场景（如多次定时器、事件监听函数）一般有固定的代码结构：
1. 在访问组件属性之前使用 `this.$valid` 判断组件是否有效；
2. 有效分支中执行正常的组件属性访问操作；
3. 无效分支中清理定时器或取消监听，并**立即返回**以保证不再访问组件属性。

::: warning
在使用 `$valid` 属性判断组件是否被销毁时，需要特别注意监听函数的闭包可能导致内存泄漏。未正确取消事件监听或定时器可能导致组件销毁后该闭包仍被系统引用，进而无法被垃圾回收。
:::

#### 内存泄漏风险

在 JavaScript 中，闭包指的是一个函数与其外部作用域的变量之间的关联。当一个函数被创建时，它会捕获外部作用域中的变量，并保持对这些变量的引用，即使外部作用域已经不再执行。这意味着，在闭包内部引用的变量依然存在于内存中，直到闭包本身被垃圾回收。

在组件框架中，当你注册事件监听器或启动定时器时，通常会传入一个回调函数，并可能会捕获组件的某些属性或上下文（例如 `this`）。

虽然组件对象本身会被框架正确销毁并释放内存，但这些闭包函数不会被清除。如果事件监听器或定时器回调没有被主动移除，这些闭包可能会依旧存在，并且会随着时间的推移积累，从而导致内存泄漏，特别是在长时间运行的应用中。这种泄漏可能难以察觉。

以下的示例演示了可能的内存泄漏：
``` js
let timer = setInterval(() => {
  if (this.$valid) {
    this.secondCounter += 1;
  }
}, 1000)
```
虽然在回调函数内通过 `if (this.$valid)` 判断了组件是否仍然有效，从而避免了在组件销毁后抛出错误，但这种做法并不能避免内存泄漏的问题。原因在于 `$valid` 只是判断有效性，判断该属性可以避免访问已经销毁的组件对象。但是问题在于，由于定时器未关闭，回调函数的闭包本身依然被引用，该闭包无法被垃圾回收。

::: tip
为了避免这种隐蔽的内存泄漏，应该在组件[销毁](./life-cycle.md#ondestroy)时，主动取消定时器或移除事件监听器，而不是单纯依赖 `$valid 判断`。即使 `$valid` 可以防止在组件销毁后执行不当操作，但它无法清理回调函数本身的闭包。

应用退出后会释放所有 JavaScript 内存，因此这种内存泄漏不会长期累积。
:::

## 方法

### `$component` <decl type="(name: string, url: string): void" method />

动态地导入一个组件（`<import>` 标签只能静态地导入组件），例如：
``` js
this.$component("Name", "url")
```
字符串 `"Name"` 是被导入组件的名字，必须使用大驼峰命名；字符串 `"url"` 是被导入组件的 URI。

### `$element` <decl type="(id: string): Element | undefined" method />

返回组件中指定 ID 的[原生子组件](native-component.md#原生组件对象)对象，如果不存在这样的子组件则返回 `undefined`。`$element()` 方法会遍历组件的所有子节点，因此其他 UX 文件的组件实例也可以被找到。

`$element()` 方法会在渲染后的整个子组件树上匹配 ID，并不局限于当前[组件模板](template.md)中的子组件。有时候要特别小心这个特性，例如对于以下模板：
``` html
<scroll>
  <MyComponent />
  <div id="panel">...</div>
</scroll>
```
当自定义组件 `MyComponent` 中也存在 `id="panel"` 的元素时，使用 `this.$element('panel')` 将会找到 `MyComponent` 中的子元素，而不是示例中的 `div` 元素。

::: tip
`$element()` 方法无法用于自定义组件，即使为自定义组件设置 `id` 属性也不行。由于 `$element()` 访问渲染后的组件树，因此必须在 [`onReady()`](life-cycle.md#onready) 生命周期函数及之后使用，而不能在 [`onInit()`](life-cycle.md#oninit) 中使用。
:::

请参考[此文档](README.md#组件对象和方法)了解如何访问 `$element()` 方法返回的组件对象。

### `$emit` <decl type="(event: string, value: any): void" method />

详见[组件间通信](communicate)。
