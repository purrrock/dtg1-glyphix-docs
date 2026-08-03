---
icon: information-outline
---
# 组件基础

上一篇文档“[快速开始](getting-started)”中简单介绍了组件的概念。而本教程会进一步讲解关于组件的知识。在阅读本文档之前，您需要知道如何新建并构建项目，以及如何编辑源文件，如果您不了解，请阅读“[快速开始](getting-started)”教程。

## 简介

在 Glyphix 的应用开发中，所有的界面都是组件——小到按钮，大到页面。组件技术允许使用简单的模板语言开发界面：
``` html
<!-- main/index.ux -->
<template>
  <p>{{text}}</p>
</template>

<style>
  * {
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
这基本上就是默认项目模板的 `main/index.ux` 文件，使用 `gx emu` 命令即可观察显示效果。`<template>` 标签中的内容是组件的模板，它描述组件的外观。这里，`<p>` 节点将显示组件模型对象中的 `text` 属性。请注意，组件框架内部会将 `<p>` 节点的内容和组件模型的 `text` 属性关联，只要修改 `text` 属性的值，界面就会同步更新。

我们可以用一个定时器进行测试：
``` js
export default {
  data: { text: "begin!" },
  onInit() {
    let count = 0
    setInterval(() => this.text = "timeout: " + count++, 1000)
  }
}
```
现在，你将看到显示的计数值每秒都会加 1。

## 组件的编程模型

GUI 程序的的一个重要功能是根据数据和输入改变自己的外观，从而实现交互。 在传统的 GUI 编程和原生的 HTML 中，开发者需要找到界面树中的目标元素节点，然后调用 API 更新它。事实证明这样开发界面会非常的复杂，因此有了诸如 MVC、MVP、MVVM 等适用于 GUI 的设计模式，Web 开发领域也出现了一些新框架，这些技术都大大降低了界面开发的难度。

Glyphix 组件的编程模型和 Vue 之类的前端框架很相似。这些框架的基本思路是根据界面模型的状态去计算新的界面，而不是要求状态改变时更新界面元素。相比于传统技术，这种方案中的界面视图部分是无状态的，因此更加简单。让我们继续使用前面的例子来介绍：
``` html
<template>
  <p>{{ text }}</p>
</template>
```
我们已经知道，组件模型的 `text` 属性更新时界面将会自动更新。但是在传统的 GUI 框架中，往往需要在模型的 `text` 更新之后（这一般来自于输入或者内部数据的改变）手动更新 `<p>` 节点。MVC 等框架可以简化这些操作，但是并不非常简洁。

现在考虑一个非常简单的方法：我们编写了一个 `render()` 函数，它根据模型当前的状态生成一颗界面树。如果我们在每一帧都用 `render()` 函数的值取代原来的界面树，那么模型的任何变化都会体现到界面中。这个方案非常简单，但是你会因为效率而否定它。实际上正是为了解决这个方案的效率问题才诞生了传统的 GUI 编程模型：只修改界面中变动的元素，但它在视图层引入了状态，也带来了不少复杂度。

Glyphix 组件框架就基于这个简单的理念：`<template>` 标签内的内容便实现了 `render()` 函数的功能，而 js 代码则专注于维护模型，而模型的数据变更会自动体现到相关的界面。你可以认为 Glyphix 组件框架总是根据模型的状态计算新的界面，所以我们不用手动更新界面元素。

::: tip
Glyphix 底层的并不是 DOM 树，自然也没有操作 DOM 元素的 API。实际上组件框架才是原生的 Glyphix JavaScript API。
:::

## 响应输入

有一些组件可以响应用户的输入事件，此时可以使用 `on` 指令指定事件的监听器。例如监听对文本组件的点击事件：
``` html
<template>
  <p on:click="text += ' click'">{{text}}</p>
</template>

<style>
  * {
    text-align: center;
  }
</style>

<script>
  export default {
    data: {
      text: "Text "
    }
  }
</script>
```
点击文本将自动更新的显示内容。`on:click` 属性的值 `text += ' click'` 是一个 JavaScript 表达式，Glyphix 会自动将表达式中变量的 `this` 绑定到组件对象。

## 条件渲染

`if` 指令用于条件性地渲染组件内容，受到该指令控制的内容区域只有在 `if` 指令中的表达式的值为真时会被渲染。
``` html
<p if="display">Hello World</p>
```

下面的例子会实现一个互斥的开关效果，连续点击时界面将交替显示 "Component A" 或 "Component B" 文本。
``` html
<template>
  <p if="display" on:click="display = false">Component A</p>
  <p if="!display" on:click="display = true">Component B</p>
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
      display: true
    }
  }
</script>
```

## 列表渲染

使用 `for` 指令重复渲染一个组件以生成列表。`for` 指令的基本用法为：
``` html
<p for="(index, value) in list">{{index}}: {{value}}</p>
```
其中 `list` 是组件模型中的一个列表属性（必须是 `Array` 类型），`index` 和 `value` 是两个迭代变量，`index` 的值是当前项的索引，`value` 的值是当前项的值。

`for` 指令可以简写为以下几种形式
``` html
<p for="list">{{$idx}}: {{$item}}</p>
<p for="value in list">{{$idx}}: {{value}}</p>
<p for="index, value in list">{{$idx}}: {{value}}</p>
```
第一种简写是只写需要迭代的表达式，此时将使用 `$idx` 和 `$item` 作为默认的迭代变量名称；第二种写法显式定义了当前值的迭代变量，而当前索引变量名则使用默认的 `$idx`；第三种写法是标准写法省略括号的简写。

::: tip
由于作用域的关系，书写 `for` 指令时迭代使用的变量只有在 `for` 指令之后使用才能生效。
:::

``` html
<!-- correct -->
<button for="list" text="{{$item}}"/>
<!-- error -->
<button text="{{$item}}" for="list"/>
```

### 同时使用 `if` 和 `for` 指令

可以在一个元素上同时使用 `if` 和 `for` 指令，此时 `if` 指令具有更高的优先级。在这个例子中，当 `display` 属性为假时，整个 `button` 组件列表将不会渲染：
```html
<button for="value in items" if="display">Hello {{value}}</button>
<p if="!display">Paragraph 1</p>
```

而如果你的目的是想要按照条件渲染 `for` 指令所生成列表中的部分节点时，就需要将 `if` 指令置于 `for` 指令的内层元素上。
```html
<button for="value in items">
  <p if="display">item: {{value}}</p>
</button>
```

::: tip
不推荐在同一元素上使用 `if` 和 `for` 指令，因为这会降低代码的可读性。
:::

## 插槽

类似于其他框架的内容分发，在 Glyphix 也实现了一套内容分发的 API，我们可以使用 `slot` 组件作为承载分发内容的出口。

在子组件中，使用 `slot` 组件来承载父组件中定义的内容。`slot` 组件在渲染时会变成由父组件传入的元素。

```html
<div>
  <slot/>
</div>
```

## 组合使用组件

将多个组件组合成更大的界面是 Glyphix 组件框架的界面构建方式。假如有一个名为 `Menu` 的组件，在需要引用它的 UX 文件根节点下使用 `<import>` 标签即可导入它：
``` html
<import src="path/to/Menu" name="Menu"/>
```
`src` 属性是组件的路径，请勿加上 `.ux` 后缀。`name` 属性是可选的组件名，如果不填写此属性，将使用组件的文件名作为组件名。

多次使用 `<import>` 标签来导入所有依赖的组件：
``` html
<import src="path/to/ComA"/>
<import src="path/to/ComB"/>
<import src="path/to/ComC"/>
```

可以像使用原生组件那样使用自定义的组件：
``` html
<div>
  <menu for="menus" on:click="clickMenu($idx, $item)">
    <p>Menu {{$item}}</p>
  </menu>
</div>
```

``` css
div {
  display: flex;
  flex-direction: column;
}

text {
  text-align: center;
}
```

``` js
export default {
  data: {
    menus: ["Dog", "Cat", "Pig", "Fish"],
  },
  clickMenu(id, name) {
    console.log(`clicked id: ${id}, name: ${name}.`)
  }
}
```

这是一个菜单界面，我们希望用户点击菜单的时候通过 `clickMenu` 方法打印当前菜单项的信息。因此 `Menu` 组件需要能够显示菜单内容，并且能够将自己的点击事件通过 `on:click` 监听到。

这是 `Menu.ux` 文件的内容：
``` html
<template>
  <div on:click="$emit('click')"> <slot /> </div>
</template>

<style>
  div { display: flex; }
</style>

<script>
  export default {}
</script>
```
我们只是简单地使用一个原生组件 `div` 响应用户的点击并上报。`div` 组件内部还会显示上次传递进来的子组件，最终使菜单列表得以显示。
