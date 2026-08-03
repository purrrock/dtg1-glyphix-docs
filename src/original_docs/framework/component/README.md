# 组件框架

组件是 Glyphix 中实现 App 界面开发功能重用的技术。通过类似嵌套 HTML 元素的方式可以组合多个组件并形成界面整体的外观和功能。另一方面，每个组件内封装了一定的内容和逻辑，通过合理地运用可以降低代码复杂度和维护成本。

组件分为内置的[**原生组件**](../render/native-component.md)和由开发者实现的**自定义组件**。原生组件一般都是 UI 元素的封装，可用于显示特性的 UI 内容或用于布局和交互，如 text、image 以及 div、list 等。而自定义组件则侧重于逻辑实现和功能封装，因为在自定义组件中实现的界面最终实际上是由原生组件承载的。

## 定义组件

每个自定义组件都定义在一个单独的 `.ux` 文件中：

``` html
<template>
  <p>{{text}}</p>
</template>

<style>
  * {
    font-size: 48;
    text-align: center;
  }
</style>

<script>
  export default {
    data: {
      text: "Hello, World!"
    }
  }
</script>
```

由此可见，一个组件由样式、JavaScript 脚本和描述界面的“模板”组成。

## UX 文件

UX（UI XML）文件是一种使用 XML 格式的组件描述。每一个 UX 文件定义一个组件，页面也是一种组件。

UX 文件中可以存在以下根节点：

- **`<import>`** 标签：用于引入其他组件，可以重复定义此标签；
- **`<template>`** 标签：定义组件界面的内容和结构，此节点有且只有一个；
- **`<template>`** 宏标签：定义可以重复使用的模板结构，此节点可以有多个，相见[模板宏](./template-macro.md)；
- **`<style>`** 标签：定义 CSS 样式表，此节点有且只有一个；
- **`<script>`** 标签：实现组件逻辑功能的 JavaScript 脚本，此节点有且只有一个。

以上节点的排列顺序是任意的。其中，`<import>` 节点总是不包含子节点。注意，`<style>` 节点和 `<script>` 节点内部不遵循 XML 语法，`>` `&` 等所有符号不需要使用 XML 转义规则，而是遵循 CSS 和 JavaScript 的语法（类似于 HTML）。

UX 文件要求所有标签必须闭合，例如 `<div>...</div>` 或者 `<div/>` 都是合法的，但是单独的 `<div>` 或者 `</div>` 将会报错。

## 页面组件

在 `manifest.json` 的 `router.pages` 字段中声明的组件可以直接作为页面使用。

相比于一般的组件，页面组件有更多的[生命周期函数](life-cycle#组件和页面的生命周期)，其他功能基本相同。已经用于页面组件的组件代码也可以直接作为普通组件使用。

## 引入组件

### 自定义组件

定义好的组件可以在别的组件中引用。在 UX 文件中填写 `<import>` 标签即可引用指定组件：
``` xml
<import name="Panel" src="path/to/Panel">
```

`src` 属性是组件的路径 URL，其中 `Panel` 是组件的文件名（不包含 `.ux` 后缀）；`name` 属性是可选的组件名，如果不定义此属性将使用组件的文件名作为组件名。

`src` 支持相对路径、绝对路径、以及外部路径

- 相对路径为相对于本 UX 文件的路径
- 绝对路径为相对于 APP 的 src 路径
- 外部路径可以导入 APP 之外的资源组件，具体路径为资源组件 APP 的 appdb.json 中 package 值加上绝对路径

### 全局组件

全局组件是在框架中定义的非原生组件，在应用中可以使用 `<import>` 标签并只指定 `name` 属性且省略 `src` 属性来引入全局组件：
``` html
<import name="TopBar" />
```

在应用只能引入全局组件而不能注册新的全局组件，系统开发者可以使用 [`globalComponent()`](/api/system-internal.md#globalcomponent) API 来注册全局组件。

## 属性文档规范

组件属性文档标题形式如下：

<div class="example-block">
  <h3 style="margin-bottom: 0.5rem">
    <span>
      <code>value</code>
      <decl type="number" get set listen />
    </span>
  </h3>
</div>

其中
- `value` 为属性的名字；
- `number` 为属性值类型；
- 右侧的 <span style="color:#666">读取 • 设置 • 监听</span> 表示该属性支持的访问模式。

### 访问模式

一个属性可以支持以下访问模式：
- **读取**：属性的值是可读的；
- **设置**：属性的值是可写的；
- **监听**：属性是可[监听](../commands/on.md)的，可监听属性通常在值变化时触发监听事件。

以 [scroll](/components/scroll.md) 组件的 [`index`](/components/scroll.md#index) 属性为例，该属性同时支持读取、设置和监听。可以在模板语法中操作 `index` 属性：
``` html
<scroll id="scroll1" :index="5" on:index="console.log($event)">
  ...
</scroll>
```
其中 `:index="5"` 将 `5` 赋值给 `index` 属性，而 `on:index="console.log($event)"` 则监听 `index` 属性的变化。更多描述请参考[组件间通信](/framework/component/communicate.md)和 [`on` 指令](../commands/on.md)。

### 组件对象和方法

还可以通过 [`$element()`](component-apis.md#element) 方法获取组件对象来访问属性：
``` js
const el = this.$element('scroll1') // 获取组件对象
console.log(el.index) // 读取 scroll 组件的 index 属性
el.index = 4 // 设置 scroll 组件的 index 属性
```
如果支持的话，可以**读取**或者**设置** `$element()` 方法返回的对象。`$element()` 方法不支持为属性绑定事件监听函数。

组件的属性还可以是一个**函数**或者**方法**，这种情况下文档标题形式如下：

<div class="example-block">
  <h3 style="margin-bottom: 0.5rem">
    <span>
      <code>method</code>
      <decl type="(x: number, y: number): void" method />
    </span>
  </h3>
</div>

其中
- `(x: number, y: number): void` 是函数或方法的签名
- 右侧的 <span style="color:#666">方法</span> 表示该属性是一个方法。

组件的方法只能通过组件对象访问。例如 scroll 组件的 [`setIndex`](/components/scroll.md#setindex) 属性为例：
``` js
const el = this.$element('scroll1') // 获取组件对象
el.setIndex(4) // 调用 setIndex() 方法
```
方法不支持读取、设置和监听访问模式，因此此类属性只有 <span style="color:#666">方法</span> 标记。

### 双向绑定

当属性同时支持了 <span style="color:#666">设置 • 监听</span> 访问模式时，它就是可以进行[双向绑定](../commands/model.md)的。
