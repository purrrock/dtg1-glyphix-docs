# Context File: 05_glyphix_tutorials_ZH.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/original_docs/src/tutorials/component-basic.md

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


============================================================
FILE_PATH: src/original_docs/src/tutorials/getting-started.md

---
icon: rocket
---
# 快速开始

在本章节中，我们将介绍如何使用 Glyphix.js 来创建一个简单的应用程序。我们会从安装打包工具开始，接着创建一个项目，并运行模拟器来查看效果。最后，我们会简要介绍项目的结构和主要文件。本教程不涉及怎样在真实设备上运行应用，以及如何发布应用。

## 准备工作

在开始之前，请先参照[此文档](/tutorials/glyphix.js/README.md#npm-安装)来安装 Glyphix 打包工具。简单来说，你可以用 [npm](https://nodejs.org) 来安装 `glyphix-cli` 包：
```bash
npm install -g glyphix-cli
```

由于 Glyphix 的开发工具以命令行为主，建议安装 Zsh、PowerShell 7+ 等现代 shell，并安装一些实用插件以提高操作效率。

### 终端工具

对于 Linux 或者 macOS 用户，建议安装 [Oh My Zsh](https://ohmyz.sh/)。而 Windows 用户建议安装 [Windows Terminal](https://aka.ms/terminal) 并使用 [Oh My Posh](https://ohmyposh.dev/)。另请参照 [`gx completion`](/tutorials/glyphix.js/README.md#gx-completion) 文档来安装 `gx` 命令的自动补全脚本。

您可以使用任何编辑器来开发 Glyphix 应用，如 [VS Code](https://code.visualstudio.com/) 或者[快应用 IDE](https://www.quickapp.cn/devtool)。

::: tip
快应用 IDE 中没有内置 glyphix.js 打包工具，你仍需安装 `glyphix-cli` 并终端中使用 `gx` 命令来构建和运行项目。在使用 VS Code 等编辑器时，建议将 `*.ux` 文件绑定为 `html` 格式，以获得基本的语法高亮。
:::

### 使用 Node.js

如果您决定在项目中使用 npm 包，或者任何 Web 开发生态的资源，请参考 [Node.js](/tutorials/nodejs.md) 配置文档。使用 Node.js 并非必须，但它可以支持 TypeScript 等现代开发工具。

### 使用打包工具

一切妥当之后，在终端中输入 `gx list device` 命令，若得到类似以下输出就表示安装成功：
``` bash
$ gx list device
  default
  ...
```

接下来创建一个应用项目并模拟运行！只需使用以下命令：
``` bash
gx new myapp # 创建名为 myapp 的项目，这将创建一个名为 myapp 的目录
cd myapp     # 切换到 myapp 目录
gx emu       # 运行模拟器
```
不出意外，你会看到一个显示 “Hello World!” 的窗口。后面的教程中会进一步讲解 glyphix.js 工具的命令使用方法。

::: tip
参考 [`gx build`](/tutorials/glyphix.js/README.md#gx-build) 和 [`gx emu`](glyphix.js/emulator.html) 文档了解更多关于构建和运行模拟器的信息。
:::

## 项目结构

你可以使用文件浏览器查看 `myapp` 目录的结构。在现在的版本中它的结构如下：
``` bash
<app-name>
├─ README.md         # 项目自述文件
└─ src               # 项目的源代码目录
    ├─ app.js        # app 入口脚本文件
    ├─ manifest.json # 配置应用基本信息
    ├─ assets        # 存放公共资源（字体、图片等）
    │  ├─ fonts      # 存放字体资源
    │  └─ images     # 存放图片资源
    └─ main          # 存放主页面的目录
        └─ index.ux  # 主页面的界面描述文件
```

在默认的项目模板中，源代码位于 `<app-name>/src` 目录中，项目中的文档等不需要打包释放的资源可以放在其他目录。

我们推荐为每个页面准备一个目录（并使用页面的名字作为目录的名字），并将这个目录放在源码的根目录下。仅在页面中使用的组件源文件（`*.ux` 文件）应当放在页面的目录下，而公共文件可以按以下规则存放：
- 公共的 UX 文件和脚本可以放在 `common` 目录下
- 仅在页面中引用的脚本文件直接存放在页面目录下
- 字体文件存放在 `assets/fonts` 目录下
- 图片文件存放在 `assets/images` 目录下
- 其他资源可以存放在 `assets` 目录下的合适位置

### 项目文件

现在，你已经看到了 `myapp` 里面有一些文件。请注意后缀为 `*.ux` 的文件和 `manifest.json` 文件，这些是开发时最常接触的文件。下面的教程将简单地介绍它们。

## `manifest.json` 文件

`manifest.json` 文件是应用的配置文件，此文件会用于应用打包。这个文件中包含了应用的基本信息，包括应用名称、版本信息等，它还包含应用内所有页面的描述和路由信息。换言之，要把页面描述添加到 `manifest.json` 之后才能在代码中跳转到此页面。

这是 `gx` 命令所生成的模板应用的 `manifest.json` 文件内容：
``` json
{
  "package": "com.example.app",
  "name": "Example App",
  "versionName": "1.0.0",
  "versionCode": 1,
  "features": [],
  "router": { // 页面路由信息
    "entry": "main", // 应用的初始页面
    "pages": { // 页面描述信息
      "main": {
        "component": "index"
      }
    }
  }
}
```

::: warning
出于教学目的，此 `manifest.json` 代码片段中有一些注释，但是 JSON 是不支持注释的，请勿在项目的 `manifest.json` 文件中添加任何注释。
:::

### 填写应用信息

你可以在 `manifest.json` 中填写你的应用信息。

### 添加页面描述信息

在  `manifest.json` 文件的根字段中，`router` 和 `pages` 字段和页面描述有关。`router` 字段是应用的页面路由表，它至少要有 `entry` 字段来指定应用的入口页面，通常使用 `main` 页面作为入口页面。

如果你要增加新的页面，就需要在 `pages` 字段中增加内容。例如，我们要新建一个名为 `NewPage` 的页面，此页面的入口组件为 `NewPage/index.ux`，那么现在 `pages` 字段的内容如下：
``` json
"pages": {
  "main": {
    "component": "index"
  },
  "NewPage": { // 这是新添加的页面
    "component": "index"
  }
}
```
`pages` 字段是一个 JSON 对象，它的每一个键都是页面的名称，默认情况下也是页面目录的路径。页面名对应的值也是一个对象，它的 `component` 是页面的入口组件名，这个组件必须存放在页面目录下。`component` 字段就是页面入口组件的文件名（不包含后缀）。所有的名字都区分大小写。

当你新增或者删除了页面，记得更新 `manifest.json` 的有关字段。

`manifest.json` 文件的结构说明详见相关文档。

## UX 文件介绍

UX（UI XML）是 Glyphix 的界面描述文件。以最初的模板工程为例，`main/index.ux` 文件的内容如下：
``` html
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

UX 文件实际上是一种 XML 文件，这个 UX 文件有两个根节点：`<template>`、`<style>` 和 `<script>`。其中 `<template>` 节点中的内容是界面的结构描述，`<style>` 节点中定义了样式表，而 `<script>` 节点中的内容是 JavaScript 脚本，它实现这个组件的交互逻辑。

::: tip
VS Code 不会对 UX 文件进行语法着色，你可以在右下角将语言切换到“HTML”，这样就会有较好的高亮效果。
:::

### 组件简介

UX 文件在运行时所对应的对象称为**组件**。组件是 Glyphix JavaScript 应用框架中的重要概念，每一个组件都是一个界面元素，它具有这些特征：
- 组件有自己的显示效果
- 有些组件可以响应用户的输入
- 有些组件可以根据数据和状态显示对应的效果
- 组件可以嵌入到其他组件中使用

常用的界面元素在 Glyphix JavaScript 应用框架中都是组件，例如：
- 文本：用于显示文字信息
- 按钮：按钮也可以显示文字信息，最重要的是它可以响应点击事件（当然也会显示点击时的效果）
- 列表：列表容纳其他组件并将它们垂直排列，另外可以通过滑动手势使列表中的元素组件移动

像列表这样能够容纳其他组件的组件也被称为**容器组件**。

可以想象，组件有两个要素：显示外观和行为逻辑。UX 文件中的 `<template>` 标签便声明了组件的外观，以 `main/index.ux` 为例：
``` html
<template>
  <p>{{text}}</p>
</template>
```
`main/index.ux` 组件由一个 `<p>` 组件实现内容的显示，这种组件用于显示文本，`{{text}}` 表达式的值就是要显示的文本。

`<script>` 标签中的 JavaScript 脚本实现了组件的行为逻辑，该标签内总是使用 `export default` 导出一个**组件对象**。首先要关注的是组件对象的 `data` 属性，它通常是一个对象：
``` js
export default {
  data: {
    text: 'Hello, World!'
  }
}
```
这里，`data` 对象有一个 `text` 属性，这个属性的值将作为前面 `<text>` 组件的显示内容。

### 组件模型和状态更新

假如我们需要设计这样一个组件：当组件被点击之后显示不同的文字，这时候就要监听组件上的输入事件并更新显示内容。下面的代码将监听 `<p>` 组件上的点击事件：
``` html
<template>
  <p on:click="text += '!'">{{text}}</p>
</template>
```
`on:click` 属性中的表达式会在文本被点击的时候执行。因此在点击时，`<p>` 组件中显示的 `text` 文本尾部会增加一个 `'!'` 字符：

<glyphix id="getting-started-click-p" height="120" width="360" title="点击事件">

``` html
<p on:click="text += '!'">{{text}}</p>
```

``` js
export default {
  data: {
    text: "Hello, World!"
  }
}
```

``` css
p {
  font-size: 32px;
  text-align: center;
}
```

</glyphix>

在后面的教程中我们将详细介绍组件的更新机制。

## 开始开发应用

现在，你可以开始开发自己的 Glyphix 应用程序了！从默认的项目模板开始编写代码，并使用 `gx emu` 命令运行模拟器。本文档的其他章节将介绍如何用 Glyphix 内置的机制、API 和组件来构建界面，以及怎样实现应用的交互逻辑。


============================================================
FILE_PATH: src/original_docs/src/tutorials/name-spec.md

---
icon: code-tags-check
---
# 组件命名规范

本文档介绍组件框架的强制命名规范以及建议的命名风格。其中强制命名规范强制性的要求，如果不遵守可能导致效果不符合预期。而使用推荐的命名规范则可以保证最大的兼容性。

## 模板命名规范

模板中的标签名称必须是短横线式（kebab-case）或者帕斯卡式（PascalCase）命名：
``` html
<Button></Button>
<button></button>
<scroll-area></scroll-area>
<ScrollArea></ScrollArea>
```

属性名称必须是短横线式或者驼峰式（camelCase）命名法：
``` html
<component prop-name="expr"></component>
<component propName="expr"></component>
```

推荐统一使用符合 Web 规范的短横线命名法。

## JavaScript 代码命名规范


JavaScript 代码中的组件名必须是帕斯卡命名，而模板中则使用对应的短横线命名。

JavaScript 代码中的组件属性名称必须是驼峰式命名：
``` js
export default {
  data: {
    propName: 0 // 在模板中的属性名是 prop-name
  }
}
```
这些属性名在模板代码中会自动转换成成对应的短横线命名。

## 文件名命名规范

UX 文件必须使用和组件相同的名字，也就是帕斯卡命名。在 `<import>` 标签中，`src` 属性（attribute）必须是区分大小写的文件 URL，而 `name` 属性则使用帕斯卡命名或者短横线命名：
``` html
<import src="path/to/UxFile" name="UxFile"/>
<import src="path/to/UxFile" name="ux-file"/>
```
实际上 `name` 属性的命名要求和模板中的标签名称是一致的。


============================================================
FILE_PATH: src/original_docs/src/tutorials/nodejs.md

---
icon: nodejs
---
# Node.js 包管理器

除了独立使用，`gx` 打包工具可以配合 npm、pnpm 或者 yarn 等 JavaScript 包管理器使用。前提是安装 `glyphix` 包：

::: code-tabs
@tab npm
```bash
npm install -D glyphix
```

@tab pnpm
```bash
pnpm i -D glyphix

@tab yarn
```bash
yarn add -D glyphix
```
:::

否则在执行 `gx build` 时可能会遇到这样的报错：
```bash
$ gx build
fatal: glyphix not found, please install it by `npm install -D glyphix' or other package manager.
```

在 Glyphix 应用的开发中使用 JavaScript 包管理器主要有以下好处：
- 用 TypeScript，而不是 JavaScript 作为开发语言，提供类型安全和更好的开发体验
- 使用 Node.js 生态中适用于嵌入式开发的 JavaScript 库（如算法库、数据处理工具等）
- 使用 ESLint、Prettier 等工具来提升代码质量和开发效率
- 便于团队协作和项目维护

::: warning
目前仅支持通过包管理器来管理普通的 JavaScript 或 TypeScript 依赖，无法复用 Glyphix 组件。在选择第三方库时，请确保它们适用于嵌入式环境，避免使用依赖 DOM、Node.js 特定 API 或过于庞大的库。
:::

::: tip
如果 [Glyphix.js](glyphix.js/README.md) devtools 是全局安装的，那么可以直接用 `gx build` 这样的命令来打包，否则要在 `package.json` 中添加 `scripts` 配置。
:::

## 项目配置

### `package.json` 配置

当使用 Node.js 包管理器时，建议在 `package.json` 中添加必要的脚本和配置：

```json
{
  "name": "my-glyphix-app",
  "version": "1.0.0",
  "scripts": {
    "build": "gx build",
    "emu": "gx emu",
    "clean": "gx clean"
  },
  "devDependencies": {
    "glyphix": "^1.0.41",
    "typescript": "^5.8.3"
  }
}
```

### `tsconfig.json` 配置

如果使用 TypeScript，需要在项目根目录创建 `tsconfig.json` 文件：

```json
{
  "compilerOptions": {
    "target": "ES2021",
    "module": "commonjs",
    "baseUrl": "./",
    "paths": {
      "/*": ["src/*"],
      "/assets": ["src/assets/*"]
    },
    "types": ["glyphix", "node"],
    "allowImportingTsExtensions": true,
    "checkJs": true,
    "declaration": true,
    "declarationMap": true,
    "emitDeclarationOnly": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "noImplicitAny": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "skipLibCheck": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*.ts", "src/**/*.ux"]
}
```

::: info
Glyphix 打包工具自动处理 TypeScript 文件的编译，上述配置主要用于 IDE 的类型检查和代码提示。
:::

## `glyphix.config.js` 配置

建议在项目根目录（`src/` 或 `package.json` 所在的目录）创建 `glyphix.config.js` 文件，以便自定义打包选项：
```js
module.exports = {
  minify: false, // 关闭代码压缩，便于调试获取源代码行号
};
```
如果你使用 TypeScript，可以改为创建 `glyphix.config.ts` 文件。

::: tip
一定要创建该文件并配置 `minify: false`，否则打包后的代码会被压缩混淆，导致调试时无法对应到源代码行号。
:::

## 使用 TypeScript

Glyphix 框架提供实验性的 TypeScript 支持，让您能够在应用开发中享受类型安全和现代 JavaScript 语法的优势。

### 基本组件示例

下面是一个使用 TypeScript 编写的组件示例：

```html
<template>
  <p on:click="onClick">{{count}}</p>
</template>

<script lang="ts">
import { defineComponent } from "glyphix"

export default defineComponent({
  data: {
    count: 0
  },
  onClick() {
    this.count++
  }
})
</script>
```

相比于默认的 JavaScript 组件脚本，使用 TypeScript 需要做以下调整：
1. `<script>` 标签中使用 `lang="ts"` 标注语言类型为 TypeScript。
2. 从 `glyphix` 模块导入 `defineComponent` 函数。
3. 待导出的组件对象要作为 `defineComponent` 的参数，并导出该函数的返回值。

使用 TypeScript 之后，`defineComponent` 函数会让 IDE 中的代码提示和类型检查更加准确。

### `app.ts`

将 `app.js` 重命名 `app.ts` 即可改用 TypeScript 应用入口文件，打包工具会自动处理。


============================================================
FILE_PATH: src/original_docs/src/tutorials/qa.md

---
icon: help-circle-outline
---
# 常见问题解答

## 打包工具

### 项目构建问题

#### `Lisp Error: thread killed` 报错

具体的现象是出现类似以下的报错信息：

``` log
[ 47%] Process image src/assets/images/frame1.png
error: Lisp Error: thread killed
```

这个问题是由于前面某一项构建出错，导致正在执行的图片转换构建操作被取消。只需要修复 `fatal` 报错的构建操作即可恢复，无需专门处理。

### 模拟器

#### 模拟器默认语言

模拟器默认语言为 `zh-CN`。因此，如果你添加了[国际化](/framework/component/i18n.md)配置将默认使用 `zh-CN.json` 翻译文件。用 `gx` 命令运行模拟器可以使用 `-l` 或 `--language` 选项来指定语言：
``` shell
gx emu -l en-US # 使用美式英语
```
你也可以在模拟器运行时用 inspector 调试工具动态更改语言。


============================================================
FILE_PATH: src/original_docs/src/tutorials/quick-orientation.md

---
title: 开发速览：从 Web 到 Glyphix
icon: compass
---

# 开发速览：从 Web 到 Glyphix

本文档专为熟悉 Web 前端（特别是 Vue.js）的开发者设计。我们将跳过基础语法教学，直接切入 Glyphix 框架的核心机制，帮助你快速建立正确的心智模型。

## 核心概念与运行环境

Glyphix 是一个运行在 MCU（微控制器）设备上的应用框架。虽然它使用 HTML/CSS/JS 进行开发，但它**不是**一个浏览器。本框架用于开发完整应用，而不是可刷新的页面，每个应用运行在独立的沙箱容器中。

你需要理解以下几个核心差异：
- **无 DOM**：底层由 C++ 原生引擎直接渲染，不存在 DOM 树。
- **无 Web API**：不支持 `window`、`document`、`localStorage` 等浏览器 API。系统能力（网络、存储、传感器）通过 `@system.*` 模块提供。
- **JS 引擎**：使用轻量级 JS 引擎（支持 ES6 标准），但内存极其受限。

### 资源限制

资源限制是与 Web 开发最大的不同点。MCU 设备的 RAM 通常仅有几 MB。这意味着不要使用网络请求加载超大 JSON 数据，或者直接 [`fetch`](../api/system-fetch.md) 一张图片。请牢记以下几点：
- 可以使用 [`@system.request`](../api/system-request.md) 模块将资源下载为文件，`fetch` 则会将响应加载到内存中。
- 图片资源通常存放在应用包内，尺寸尽可能与屏幕分辨率匹配。
- **后台冻结**：应用进入后台（`onHide`）后，通常会在几十秒内被系统挂起或销毁。请注意保存状态。

### 设备形态

Glyphix 应用通常运行在智能手表等小屏设备上。手表的屏幕尺寸通常为 1.5 到 2 英寸左右，典型分辨率为 466×466 像素，但存在圆形、矩形屏幕。低端设备的像素密度可能更低，但尺寸基本相似。这类设备常用触摸屏进行交互，可能支持物理按键或者旋钮，系统透明地处理了大部分交互细节。

通常使用模拟器进行开发和调试，因为真机部署和调试流程还比较碎片化，耗时较长。

### 典型项目结构

这是我们推荐的项目文件结构，这也是快应用标准的结构：
```bash
src/
├─ manifest.json  # 应用清单：配置权限、注册页面路由
├─ app.js         # 应用入口：全局生命周期 (onCreate, onDestroy)
├─ pages/         # 页面目录
│  └─ Main/
│     └─ index.ux # 页面组件
└─ assets/        # 公共资源
  └─ icon.png
```
你可以根据需要引入 [Node.js](nodejs.md) 工具链来管理依赖。也可以按照需要调整目录结构，但 [`src/manifest.json`](/framework/application/manifest.md) 和 `src/app.js` 必须固定在此位置。

## UI 开发

Glyphix 采用 [`.ux`](../framework/component/README.md) 单文件组件（类似 Vue SFC），风格接近 Vue Options API，但也有显著差异。

### Flexbox 布局优先

Web 默认是流式布局（Flow Layout），而 Glyphix 的页面默认为堆叠布局：如果你在页面中放两个 `div`，它们会**重叠**在一起，而不是上下排列。这是因为本框架支持在 `<template>` 中使用多个根节点，例如：
```html
<template>
  <image class="background" src="/assets/bg.png" />
  <div class="content"> ... </div>
</template>
```
默认的堆叠布局对于这种场景通常非常合适。

尽管 `div` 等容器默认使用流式布局，但推荐使用 Flexbox 来进行布局控制。绝大多数容器都应该显式声明 `display: flex`，再结合 `flex-direction` 控制子元素排列方式。

考虑到设备屏幕尺寸差异较大，请特别注意长度单位的使用：
- 在较小的尺寸中使用 `px` 单位，它是逻辑像素，会根据屏幕密度自动缩放。
- 字体应总是使用 `rem` 单位，它由设备厂商定义基准，更符合系统 UX 规范的一致性要求。
- 可以使用百分比（`%`）单位来实现响应式布局，但是目前限制和缺陷较多，请注意调试。

由于屏幕太小，你可能特别需要 [`scroll`](../components/scroll.md) 组件来实现滚动区域。和 Web 不同，`div` 容器本身不支持滚动，也无法使用 `overflow` 属性来控制。

### 模板语法差异

虽然长得像 Vue 模板，但请注意以下区别：
- 指令无 `v-` 前缀：如 `<div if="show">` 或 `<div for="item in items">`
- 事件绑定用 `on`、`@` 均可，如：`<p on:click="handler">`
- 必须使用 `<p>` 等文本组件：`<text>Hello</text>` 可以正常显示，但是 `<div>Hello</div>` 不会渲染任何内容。
- 支持用 `model:prop="state"` 或 `::prop="state"` [双向绑定](../framework/commands/model.md)任意组件属性，只要有和属性同名的事件触发即可。

### 样式限制

CSS 支持是子集：
- 支持类 (`.class`)、ID (`#id`)、标签 (`div`) 和后代 (`.a .b`)。**不支持** `~`、`+`、`>` 等复杂关系选择器。
- **效果限制**：不支持渐变、阴影等效果。暂不支持 `transition` 动画。
- **性能限制**：避免使用 `transform` 来移动或对齐元素。`object-fit` 默认为 `none` 并推荐保持默认。
- 目前不支持动态 `class` 绑定，也不支持 CSS 变量。

## 组件与逻辑

### 脚本模型

组件脚本非常接近 Vue Options API，以下示范指出了主要差异：
```js
export default {
  // 数据模型 (Data)，不需要声明属性，data 属性自动导出为属性
  data: {
    count: 0, // 修改 this.count 会自动触发视图更新
  },
  timer: null, // 非响应式字段直接定义在组件实例上，也可以不声明
  // 生命周期
  onInit() {}, // 数据已初始化，可发起网络请求
  onReady() {}, // 界面已渲染完成
  onDestroy() {}, // 务必在此清理定时器、订阅事件

  // 方法 (Methods)，直接定义在组件对象中
  handleTap() {
    this.count++
    // 触发自定义事件给父组件
    this.$emit('change', { value: this.count })
  }
}
```
其中 `data` 对象中的字段为响应式属性，它目前只支持 JSON 兼容的类型（不支持 `Date`、`Map`、`Set` 等）。如果不需要响应式更新，推荐将字段定义在组件实例（`this`）上。

::: tip
不要使用 `methods` 对象包裹方法，直接定义在组件对象中即可。也不需要使用 `props` 定义属性，`data` 对象中的字段会自动导出为属性。

也不能用 `document.getElementById` 等 DOM API 查找元素。可以使用 [`this.$element()`](../framework/component/component-apis.md#element) 方法获取指定 ID 的元素实例。
:::

### 页面与路由

Glyphix 应用由多个页面组成，页面间通过路由导航。所有页面均需在 `manifest.json` 中的 [`router.pages`](../framework/application/manifest.md#pages) 字段中静态注册。页面组件与普通组件类似，但支持 `onShow` 和 `onHide` 生命周期钩子。

使用 `system.router` 系统模块进行跳转：
```js
import router from '@system.router'

// 跳转并传递参数
router.push({ uri: 'pages/Detail', params: { id: 123 } })
```
::: tip
不要使用其他的路由库，也不要假装在开发单页面应用（SPA）。否则将无法利用转场动效、页面栈管理等现有功能。
:::

### TypeScript 支持

如果使用 Node.js 脚手架创建项目，使用 npm、pnpm 等安装 `glyphix` 和 `typescript` 等依赖后，可以在项目中使用 TypeScript 进行开发。

对于 `.ux` 单文件组件，可以在 `<script>` 标签上添加 `lang="ts"` 属性启用 TypeScript 支持。例如：
```html
<script lang="ts">
import { defineComponent } from 'glyphix'

export default defineComponent({
  data() {
    count: 0: number
  },
  increment() { this.count++ },
})
</script>
```

## 系统能力集成

不要尝试使用浏览器 API，请使用 Glyphix [标准库](../api/README.md)。

### 常用模块速查

| 功能 | Glyphix 模块 | 说明 |
| :--- | :--- | :--- |
| **网络** | [`@system.fetch`](../api/system-fetch.md) | 必须处理异步回调或 Promise |
| **弹窗** | [`@system.prompt`](../api/system-prompt.md) | 提供 Toast 和 Dialog |
| **存储** | [`@system.storage`](../api/system-storage.md) | 同步本地存储，直接读写对象而非字符串 |
| **路由** | [`@system.router`](../api/system-router.md) | 管理页面栈 |
| **日志** | `console.log` | 输出到调试终端，和浏览器一样 |

### 异步编程模式

系统 API 通常支持异步回调和 Promise 两种风格。推荐使用 `async/await` 以保持代码整洁。

```js
import fetch from '@system.fetch'
import prompt from '@system.prompt'

export default {
  onReady() { this.loadData() },
  async loadData() {
    try {
      const response = await fetch.fetch({
        url: 'https://api.example.com/data',
        method: 'GET', // 默认为 GET
        responseType: 'json', // 这样不需要 JSON.parse 手动解析
      })

      if (response.data.code === 200)
        this.data = response.data.data
    } catch (err) {
      prompt.showToast({ message: 'Network Error' })
    }
  }
}
```

## 构建和运行

使用 [`gx emu`](../tutorials/glyphix.js/README.md) 命令启动模拟器，或使用 `gx build` 构建应用包。如果使用了 Node.js 脚手架，也可以直接使用 `gx` 命令。

请参考[快速开始](getting-started.md)教程了解详细步骤。 

## 综合示例

以下是一个完整的组件示例，展示了布局、数据绑定、事件处理和系统 API 的综合使用。你可以直接在浏览器中查看此示例，点击 `>` 按钮来查看完整代码。

<glyphix id="quick-orientation-example" title="计数器组件示例" height="240">

```html
<!-- 根容器推荐使用 Flex 布局，加载中不允许操作 -->
<div class="container" :disabled="loading">
  <text class="title">Hello, {{ name }}</text>

  <div class="card">
    <text class="count">{{ count }}</text>
    <text class="btn" value="+1" on:click="increment">Add</text>
  </div>
</div>

<!-- 利用页面的堆叠布局来叠加加载状态提示 -->
<text if="loading" class="loading">Loading...</text>
```

```css
.container {
  /* 页面组件不需要设置宽高，它们总是铺满 */
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  /* 注意一般不设置页面背景，这只是演示 */
  background-color: #f5f5f5;
  border-radius: 16px;
  padding: 10%; /* 百分比边距 */
}

.title {
  font-size: 1.25rem; /* 字体使用 rem 单位 */
  color: #333333;
  align-self: center;
}

.card {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 16px;
}

.count {
  font-size: 1.5rem;
  color: #007aff;
  min-width: 80px;
}

.btn {
  width: 120px;
  background-color: #007aff;
  color: #ffffff;
  border-radius: 50%; /* 圆形按钮 */
  text-align: center;
}

.loading {
  color: #3d3d3d;
  font-size: 0.8rem;
  text-align: center;
}

/* disabled 状态的淡化样式 */
*:disabled {
  opacity: 0.5;
}
```

```js
import prompt from '@system.prompt'

export default {
  // 组件数据
  data: {
    name: 'Glyphix',
    count: 0,
    loading: false
  },
  // 生命周期：组件初始化完成
  onInit() {
    console.log('Component initialized')
    this.simulateFetch()
  },
  // 方法定义
  increment() {
    this.count++
    if (this.count % 5 === 0) {
      prompt.showToast({
        message: `Count reached ${this.count}!`
      })
    }
  },
  async simulateFetch() {
    this.loading = true
    // 模拟异步操作，这会产生加载状态
    setTimeout(() => {
      this.loading = false
      this.name = 'Developer'
    }, 1000)
  }
}
```

</glyphix>


============================================================
FILE_PATH: src/original_docs/src/tutorials/README.md

---
title: Glyphix 应用开发教程
index: false
icon: routes
category:
  - Guide
---

## 什么是 Glyphix

Glyphix 是一种面向 MCU（微控制器）设备的高效、轻量级应用开发框架。它为开发者提供类似于 Web 生态的声明式 UI 开发范式：通过 HTML 模板、CSS 和 JavaScript 的方式，开发者可以轻松构建页面和组件，并将应用发布到各种智能设备（如智能手表）上。  

更多的信息请参考[框架](/framework/README.md)章节。

### 类 Web 框架

与传统的 MCU 固件开发不同，Glyphix 更接近于基于 Web 技术栈的框架。应用开发者需要熟悉 JavaScript、CSS 和基本的 HTML 知识。你无需掌握完整的 Web 开发技术栈，如浏览器 DOM、标准 HTML 标签，以及复杂的构建工具链等。但若熟悉 [Vue.js](https://vuejs.org/) ([Options API](https://vuejs.org/guide/introduction#options-api)) 等 Web UI 框架，将会很容易上手 Glyphix。

::: tip
需要的说明是，Glyphix 并非“低代码”平台。在开发过程中，依然会遇到逻辑抽象、界面组织、用户体验和性能权衡等挑战。因此，掌握扎实的 JavaScript 基础与良好的前端思维方式，将有助于你充分发挥 Glyphix 的潜力。
:::

### 声明式 UI 框架

传统的界面开发通常是命令式的：需要逐步调用函数来创建控件、更新状态、刷新界面。这种方式很灵活，但业务和界面逻辑高度耦合，随着应用规模扩大，代码会迅速变得复杂而难以维护。MVC、MVVM 等模式的提出，正是为了解决这种复杂性。  

Glyphix 则采用声明式 UI 的范式。开发者只需描述“界面应该是什么样子”，框架会根据数据和状态的变化自动完成渲染和更新。这种方式大幅降低了界面逻辑与状态管理的复杂度，也让开发者可以将主要精力放在功能与交互设计，而非维护 UI 的层次结构和刷新流程。

### 应用容器

Glyphix 不只是一个 UI 框架，它还提供了应用的生命周期管理、权限隔离和系统 API 等功能。应用运行在一个独立的容器中，彼此隔离，确保系统的稳定性和安全性。

请阅读[快速开始](getting-started.md)教程，即刻上手 Glyphix 应用开发。

## 其他问题

### 需要熟悉 MCU 和嵌入式开发吗？

应用开发者通常不需要理解 MCU 和嵌入式开发的具体知识。但应当对设备的资源限制有一些了解。例如 MCU 的内存容量通常只有几 MB，而且运行 JavaScript 代码的内存也有限制。这意味着可能会出现无法从网络上请求非常大的 JSON 数据，或者无法将整张图片编码为 Base64 并通过 GET 请求获取。

这些与 Web 开发完全不同的限制确实是因为 MCU 设备的资源有限导致的，但这也不是典型的 MCU 知识体系所包含的。

直观来说，最好通过在设备上运行应用来确认应用的体验是否足够好。你可以在开发的不同阶段多次使用真机运行以确保体验。

### 应用开发要使用 C/C++ 吗？

Glyphix 应用开发完全使用 HTML、CSS 和 JavaScript，因此不需要使用 C/C++ 语言。

### 嵌入式开发者要怎样上手 Glyphix 应用开发？

嵌入式开发者可以本教程[快速开始](getting-started.md)，逐步理解 Glyphix 的核心概念。该框架采用类似 Vue Options API 的组件化和数据绑定机制，这对于习惯 [LVGL](https://lvgl.io/) 、Qt widgets 等命令式 GUI 的读者来说会有些不同，但 Glyphix 的声明式设计也能带来更直观的界面控制体验。

开发者并不需要完全掌握 HTML、CSS 和 JavaScript，不过熟悉 JavaScript 的基本语法（如变量、条件判断、函数调用等）会有助于理解 Glyphix 的渲染逻辑和事件处理。您可以通过教程和文档中的示例代码和实际操作来熟悉这些内容，加速上手开发流程。

### 要关注应用的性能优化吗？

我们的框架已经针对嵌入式系统的资源限制进行了深入优化，能够很好地适应多种硬件环境。多数应用能在默认设置下获得足够流畅、稳定的运行表现，因此通常不需要花费额外时间在性能优化上。

如果将来有需要深入了解特定优化方案，我们会提供专门的性能优化文档，帮助开发者进一步提升应用的运行效率。

### Glyphix 环境和浏览器有区别吗？

是的，Glyphix 环境与浏览器有明显区别。Glyphix 并没有浏览器中的 DOM 结构，也不提供 `window`、`document` 等对象。相反，它直接且唯一地提供了一套声明式的接口，开发者可以通过这些接口进行组件开发和界面交互。这种设计简化了开发流程，更适合嵌入式环境。


============================================================
FILE_PATH: src/original_docs/src/tutorials/glyphix.js/cli.md

---
icon: console-line
---
# 命令行选项

待迁移。


============================================================
FILE_PATH: src/original_docs/src/tutorials/glyphix.js/emulator.md

---
icon: watch-import-variant
---
# 模拟器和调试

要运行模拟器，你需要在命令行中切换到项目的根目录，然后运行 `gx emu` 子命令来启动模拟器。Glyphix 模拟器拥有和真实设备运行时高度一致的环境，因此可以利用模拟器开发和调试大部分界面和功能，而不需要频繁地将应用安装到真实设备上。

::: tip
由于当前 [`glyphix`](https://www.npmjs.com/package/glyphix) npm 包的限制，请务必配置 [`glyphix.config.js`](/tutorials/nodejs.md#glyphix-config-js-配置)，否则在执行 `gx emu` 时无法看到错误信息的源代码行号。
:::


## `gx emu` 子命令

使用上次的构建目标设备配置来运行模拟器。该命令需要在 Glyphix 项目的根目录中执行。它会自动构建项目并创建模拟器所需的资源文件，因此无需先执行 `gx build`。

#### 命令选项

- `-d --device=NAME`：指定模拟的设备名称，默认为 `default`（分辨率为 $410 \times 502\rm px$）。
- `-e --emulator-exe=CMD`：指定模拟器的可执行文件，默认为 `glyphix-emu`。通常不需要修改。
- `-l --language=NAME`：指定模拟器的语言环境，默认为 `zh-CN`（简体中文）。通过 `gx list language` 命令可以查看支持的语言列表。
- `--target=URI`：设置模拟器启动时的包名或者 deeplink，例如 `app://com.example.app/SomePage?query=value` 或者 `com.example.app`。
- `-i --inspector`：在运行模拟器时启用检查器，检查器是一个 Web 页面，可以在浏览器中调试模拟器中的界面元素。
- `-m --mobile-network`：（尚未实现）仅在模拟器中启用手机 SDK 的网络代理，而不直接访问网络。
- `-w --watch`：运行模拟器时监听项目目录，当源文件发生变动时自动重新构建并刷新模拟器界面。
- `-r --real-scale`：使用真实尺寸显示模拟器窗口，而不是按设备分辨率缩放显示。此选项建议在 HiDPI 屏幕上使用。
- `-t --top`：保持模拟器窗口置顶。
- `-p --profiling`：启用性能分析模式。由于模拟器和设备性能差异较大，该选项通常不是很有用。

## 启动模式

默认情况下，`gx emu` 会按照上次构建时使用的设备配置来启动模拟器。还可以通过命令选项来调整模拟器的启动行为。

### 指定设备型号

使用 `-d` 或 `--device` 选项可以指定希望模拟的设备型号，例如：
```bash
gx emu -d generic-watch-466x466
```
将会为 `generic-watch-466x466` 这款设备启动模拟器。可以使用 `gx list device` 命令查看已安装的设备列表。

如果不指定该选项，则会使用上次指定过的设备。第一次或 `gx clean` 之后启动模拟器时会使用 `default` 设备。

### Deeplink 启动

默认情况下，模拟器会启动当前项目的应用，或是启动一个应用菜单界面。但在调试 [`onRoute()`](/framework/component/life-cycle.md#onroute) 生命周期函数时，可能希望通过 deeplink 启动应用，以确保 `onRoute()` 接收到特定参数。可以使用 `--target` 选项来指定 deeplink，例如：
```bash
gx emu --target app://com.example.app/SomePage?query=value
```
这会启动包名为 `com.example.app` 的应用，而 Deeplink URI 的 path（含根目录 `/`，即 `/SomePage`）和 query 字段会被传递给该应用的 `onRoute()` 函数。

### 模拟设备尺寸

默认情况下，模拟器会使用设备的实际像素分辨率，这会导致电脑上的显示尺寸大于设备的实际屏幕尺寸，并使开发者难以确认 UI 元素（包括设计稿）在设备上的具有较佳尺寸。`-r` 或 `--real-scale` 选项可以按真实设备尺寸来模拟：
```bash
gx emu -r
```
使用此选项时，您不需要将应用安装到设备上即可确认 UI 的实际尺寸。但考虑到大部分手表的 DPI 超过 300，1080p 显示器在使用 real-scale 模式时会导致界面过于模糊，建议在 HiDPI 显示器（如 4K 显示器，或者 macOS 上的 Retina 屏幕）上使用此选项。

::: tip
使用 real-scale 模式时，您应该通过 `--device` 选项来指定希望模拟的目标设备。值得注意的是：由于 DPI 不同，两款相同的分辨率设备可能有不同的屏幕尺寸，因此 real-scale 模式的显示尺寸也会不同。
:::

### 自动刷新

`-w` 或 `--watch` 选项可以在运行模拟器时监听项目目录，当源文件发生变动时自动重新构建并重启应用。通常建议配合 `--top` 选项使用，例如：
```bash
gx emu -wt
```
这样可以保持模拟器窗口置顶，并且在修改源文件后自动重启应用。这对于开发调试非常有用：直接从代码编辑器切换到模拟器，不需要手动重启模拟器，也不需要频繁切换窗口。

::: tip
目前不支持热更新页面，而是在修改源文件后重启整个应用。如果想要更快的调试速度，可以将 [`manifest.router.entry`](/framework/application/manifest.md#entry) 调整为正在开发的页面，这样每次重启应用时都会直接进入该页面。
:::

## 连接手机

可以通过 [Glyphix Debug](https://www.pgyer.com/KLeBQFv6) Android 手机应用连接模拟器，以便于调试真实设备和手机互联相关的功能。

### 准备工作

你需要在手机上安装 Glyphix Debug 应用，并确保手机和电脑处于同一局域网内，例如连接到同一个 Wi-Fi。启动模拟器并打开打开 Glyphix Debug 应用后，点击“Socket 连接”按钮，应用会显示一个连接界面，你可以选择搜索到的模拟器 IP 地址，或手动输入电脑 IP 和模拟器端口进行连接。

模拟器默认监听 7768 网络端口，如果该端口被占用（通常是启动了多个模拟器），则自动选择下一个可用端口，并在启动时打印实际使用的端口号。例如：
```bash
$ gx emu
[simulator.socket] MAS TCP server bind port 7768 successful 
```

::: tip
一旦模拟器端口被占用并选择了非 7768 端口号，Glyphix Debug 应用将无法自动搜索到该模拟器，必须手动输入正确的 IP 地址和端口号进行连接。
:::

强烈建议模拟器开启下一节的手机网络代理模式，以免同时使用电脑网络和手机网络。否则可能会干扰 [`@system.interconnect`](/api/system-interconnect.md) 之类依赖手机互联 API 的正常工作。

### 手机网络代理

使用 `-m` 或者 `--mobile-network` 选项可以只启用手机 SDK 的网络代理功能，这类似于真实设备的网络环境。使用此选项时，模拟器不会自动启动目标应用，而是显示一个应用列表界面。

在手动启动应用之前，应通过 Glyphix Debug 手机应用通过“Socket 网络”连接模拟器，然后再点击目标应用。否则应用将无法访问网络。

::: tip
在使用 `-m` 手机网络代理时，可以通过杀死手机调试应用、重新连接模拟器等方式来模拟网络中断的情况。否则模拟器会自动切换到电脑网络。
:::

### 常见连接问题

如果无法通过 Glyphix Debug 应用连接模拟器，请检查电脑和手机是否连接到同一个局域网，且模拟器程序和端口未被防火墙规则屏蔽。如果你连接到了公共网络，那么和可能因为防火墙或者网络隔离而无法连接。

如果你使用了 VPN 或者代理软件，请确保局域网内的流量不被代理，否则也会无法连接。

## 其他操作

### 清除应用数据

你可以使用 [`gx clean`](README.md#gx-clean) 清除模拟器运行时的应用数据，之后再启动模拟器时将从首次安装的状态开始运行。

### 组合命令选项

你可以将多个选项组合在一起使用，例如：
```bash
gx emu -rwt -d default-watch-466x466
```
等效于分开使用
```bash
gx emu -r -w -t -d devault-watch-466x466
gx emu --real-scale --watch --top --device default-watch-466x466
```
建议按 [`gx completion`](#gx-completion) 中介绍的方法安装自动补全脚本，以便在终端中选择设备名称和命令选项。


============================================================
FILE_PATH: src/original_docs/src/tutorials/glyphix.js/image-forge.md

---
icon: image-filter
---
# 图片管理

glyphix.js 打包工具会管理项目中所有的 PNG 图片资源（ `src` 目录）。相关模块主要提供以下功能：
- 支持图片资源的配置文件，并提供相关配置界面
- 打包时将图片转换为为设备优化的尺寸和格式

应用开发者只需要按自己的需要配置图片资源的打包参数，而设备供应商需要为设备定义具体的图片转换策略。

## 应用开发配置

在应用开发中需要配置图片打包参数才可以正确生成资源包
在应用开发中配置 `config/image-rules.json` 以及 `src/menifest.json` 的 `config.designWidth` 等属性均会影响图片资源的打包行为。`config/image-rules.json` 一般用来配置质量和性能参数，而 `menifest.json` 中的字段影响图片的全局缩放比例（用于适配不同分辨率的设备）。

::: tip
`config/image-rules.json` 可以使用 `gx config` 命令或其他方式配置，但不建议直接用文本编辑器编辑。
:::

如果使用 `gx config` 命令，开发者将主要会关注两个参数：transparent 和 quality。

### Transparent 参数

Transparent 表示图片是否包含透明像素，如果为配置为否（`false`）并且资源图片是包含透明像素的，那么生成时会将这些像素转换为不透明（通常是叠加到一个黑色背景上）。因此需要将必要的图片标记为保留透明像素，否则会显示不正确的覆盖效果。由于某些平台上不透明图片的性能更好，且不透明图片的数据量更少，transparent 选项默认关闭。

### Quality 参数

Quality 参数代表打包后图片的品质，是一个 $[0, 100]$ 范围的整数。不过通常只使用 3 个大致的品质级别：
- High：100，表示最高品质
- Middle：50，中等品质，默认值
- Low：0，低品质

转换图片资源时会根据品质参数进行优化。通常而言，中等品质是在目标平台上平衡了显示效果、绘制/加载性能以及内存资源占用等因素后的转换策略，因此推荐使用。使用高品质可能有更好的质量，但可能产生性能下降。低品质可用于可以损失质量以提升性能的图片（例如如照片）。具体的目标平台也可能忽略 quality 参数而使用统一策略。

## 设备和平台适配

假设设备和平台开发商已经针对具体目标平台实现了优化的图片资源格式并支持多种品质和像素格式，为了在 glyphix.js 中可以生成这些图片格式需要做以下工作：
- 实现**单张图片**转换所需的命令行工具
  - 必须提供从 PNG 图片转换为自定义格式的命令行接口，支持输出到指定路径（包括覆盖原文件）
  - 最好提供从自定义格式转换为 PNG 图片的的命令行接口，支持输出到指定路径（包括覆盖原文件），缺失此功能将无法实现 PC 断预览
- 编写设备描述文件和图片转换脚本

### 图片转换脚本

图片转换脚本是一个 scheme 文件，需要转换图片时 glyphix.js 会调用此脚本，后者可以根据这些变量确定如何转换图片：
- `env.image-path`：待转换图片的绝对路径，转换后的图片覆盖写入到此路径
- `env.transparent`：此图片的透明参数
- `env.quailty`：此图片的品质参数
- `env.target`：转换目标模式，见后文描述
- `env.verbose`：是否开启 verbose 模式，如果是则可以输出详细的日志，否则不应输出日志
- `env.script-dir`：当前脚本文件所在的绝对路径，如果转换所需的命令是相对于此脚本文件而不在 `PATH` 环境变量中，可以利用此参数进行拼接

`env.target` 表示图片转换的**目标模式**，它的值决定具体应用何种转换方式：
- `"device"`：执行针对目标设备的完整转换流程，例如将不透明图片的透明通道移除，然后将其按照品质参数转换为 PGF 格式（Glyphix 图片格式）
- `"emulator"`：执行针对模拟器的转换流程，由于模拟器并不支持特定硬件的纹理格式（例如 ETC2 等），为了保证图片在模拟器中正常显示，可以只移除不透明图片的透明通道而不进一步转换为目标设备格式（或者转换为软件支持的 PGF 格式）
- `"preprocess"`：只执行预处理步骤，也就是移除不透明图片的透明通道，并且要将结果输出为 PNG 格式
- `"preview"`：生成预览的 PNG 图片，首先要按照 `"device"` 目标的转换流程将图片转换为自定义目标格式，然后将输出图片转回 PNG 供预览使用

::: tip
如果图片转换的命令行工具不支持将自定义格式转换为 PNG，那么不要实现 `"preprocess"` 和 `"preview"` 目标模式。
:::

### image-forge 命令行工具

image-forge 是 Glyphix 提供的 PGF 图片格式命令行工具，具有以下功能：
- 支持 PNG 图片转换为 PGF 格式，以及将 PGF 转换为 PNG 图片
- 支持常见的 ARGB 和 PAL 像素格式，且区分 premultiplied alpha 模式
- 支持将透明的 ARGB 图片混合到指定的纯色背景上使之转换为不透明图片（不是直接丢弃 alpha 通道）
- 支持行按像素或字节对齐
- 支持 LZ4 压缩，并可以设置最小压缩阈值（低于阈值的图片数据不会压缩）

对于使用其他自定义图片格式的平台，也可以利用 image-forge 来移除透明通道。

## 图片转换脚本示例

以下示例演示如何利用 image-forge 等命令将 PNG 转换为 PGF 图片，并且优先使用查色表（PAL）格式。

首先定义不透明和透明情况下的目标格式：
``` scheme
; 定义不透明颜色的像素格式规则
(define (opaque-formats q)
  (cond ((<= q 50) "pal-rgb")
        (else "rgb24")))

; 定义透明颜色的像素格式规则
(define (transparent-formats q)
  (cond ((<= q 50) "pal-argb-premul")
        (else "argb32-premul")))

; 计算透明和品质参数作用下的目标像素格式
(define pixel-format
  ((if env.transparent
      transparent-formats opaque-formats)
    env.quailty))

; 图片是否转换为查色表格式
(define palette (<= env.quailty 50))
```

以上代码会在品质小于等于 50 时使用查色表格式，并且会根据是否透明使用 `pal-rgb` 或 `pal-argb`。质量高于 50 时使用 RGB 或 ARGB 8bit 位采样的像素格式。最终，`pixel-format` 变量即实际使用的像素格式名称，`palette` 表示是否使用查色表格式。

接下来定义各种情况下需要使用的命令：

``` scheme
; 是否添加 --verbose 命令行参数
(define if-verbose (if env.verbose "--verbose " ""))

; 调用 pngquant 命令将图片颜色缩减至 256 色以内，系统中需要安装 pngquant
(define color-reduction
  (string-append "pngquant --ext=.png --force " if-verbose env.image-path))

; 转换图片为 PGF 格式
(define convert (string-append "image-forge "
  "--format=" pixel-format " " ; 指定输出像素格式
  "--compress --min-compress-ratio=5 " ; 压缩图像数据减小文件尺寸，最小压缩比为 5
  "--align=16 --pixel-align " ; 图片按 16 像素对齐
  if-verbose
  env.image-path))

; 移除图片 Alpha 通道并添加背景
(define remove-alpha (string-append "image-forge --bypass "
  ; 在 bes2500ibp 手表上，非透明图片可以移除 alpha 通道并用黑色背景混合，这种操作可以提高 PAL 颜色缩减后的图像质量
  (if env.transparent "" "--background black ")
  if-verbose
  env.image-path))

; 将 PGF 图像转回 PNG 的命令
(define decode
  (string-append "image-forge --decode " if-verbose env.image-path))
```

以下代码中，`execute-try` 在命令非 0 退出后调用指定的 `f` 函数，`execute` 函数在命令非 0 退出后打印错误日志并异常退出脚本。`run-convert` 函数执行完整的目标设备图像转换流程（调用 `remove-alpha` 和 `convert` 的命令）。

``` scheme
; 执行一个命令并在 verbose 模式中打印命令内容，如果命令以非 0 异常退出则调用函数 f
(define (execute-try cmd f)
  (begin
    (if env.verbose ; 如果为 verbose 模式则打印命令内容
      (display (string-append "Run command: " cmd "\n")))
    (let ((r (system (string-append env.script-dir "/bin/" cmd))))
      (if (= r 0) 0 (f r)))
  ))

; 执行一个命令，并会在 verbose 模式打印命令内容，如果命令异常退出则退出程序
(define (execute cmd)
  (execute-try cmd (lambda (x)
    (begin ; 失败时打印错误码并异常退出
      (display (string-append "subprocess failed (" (number->string x) "): " cmd "\n"))
      (exit-fail)
  ))))

; 转换图像
(define (run-convert)
  (begin
    (execute remove-alpha) ; 先移除透明通道
    (if palette (execute color-reduction)) ; 如果是查色表格式则缩减图片的像素数量
    (execute convert) ; 执行图片转换命令
  ))
```

`targets` 宏定义所有目标模式的处理方法，例如 `"device"` 模式将调用 `run-convert` 函数等。

``` scheme
; 定义目标对应的转换策略
(targets env.target
  ; 设备模式：最终用于目标设备的图片转换流程
  ("device" (run-convert))
  ; 模拟器模式：仅移除非透明图片的 alpha 通道，不转换格式
  ("emulator" (execute remove-alpha))
  ; 预处理模式：移除非透明图片的 alpha通道并添加背景
  ("preprocess" (execute remove-alpha))
  ; 预览模式：生成和实际设备显示效果一致的 PNG 预览图片
  ("preview" (begin
    (run-convert) ; 先把图片转换为 PGF 格式
    (execute decode))) ; 再把图片转回 PNG
  )
```

### 使用图片转换脚本

要使用图片转换脚本，需要在设备型号描述文件中增加一个字段：

``` yaml
description: default watch

screen:
  width: 454 # pixels
  height: 454 # pixels
  dpi: 326 # pixels per inch

#...
image-build: image-convert-pal.scm # 图片转换脚本相对于本 Yaml 文件的路径
```

### 更复杂的策略

由于图片转换脚本是完整的编程语言而不是 Yaml、JSON 等配置语言，我们可以实现更复杂的自定义转换策略而不会受限于框架提供的功能。以上面的查色表格式转换为例：PAL 格式在颜色丰富的图片上效果不好，此时可以将图片转换为在这类场景中表现更好的格式。具体的思路为：
1. `pngquant` 命令支持在转换 PAL 格式后质量低于指定值的情况下异常退出，因此按照此目的配置命令参数
2. 在 `run-convert` 函数由 `execute` 执行的 `color-reduction` 的操作改为由 `execute-try` 执行，并在后者的异常处理函数中使用替代格式的转换操作
3. `preview` 等目标的处理方式类似，但要注意，在将输出格式转换为 PNG 的时候，也需要识别命令异常退出并改由后续的命令继续尝试

总而言之类似于 shell 脚本的思路，利用命令的异常退出码来控制流程。


============================================================
FILE_PATH: src/original_docs/src/tutorials/glyphix.js/README.md

---
icon: package-variant-closed
---
# Glyphix.js 打包工具

glyphix.js 是 Glyphix 应用的打包工具，它包含一个名为 `gx` 的命令行工具，可以用来创建、构建和运行 Glyphix 应用。该工具还包含一个图形化的模拟器，可以在电脑上模拟运行 Glyphix 应用。

本文档提供 glyphix.js 的安装和使用说明，[快速开始](/tutorials/getting-started.md)教程则是一份更简单的入门指南。另请阅读[构建和运行](#构建和运行)来了解如何开发、构建和发布一个 Glyphix 应用。

## 安装

本节介绍 glyphix.js 打包工具的安装方法。对于一般用途，只需要了解 [npm 安装](#npm-安装)方法。[手动安装](#手动安装)方法适用于特殊场景，例如网络受限的环境、CI 构建等。

### npm 安装

可以使用 [npm](https://nodejs.org) 包管理器来安装 glyphix.js 打包工具，建议使用 `-g` 选项来进行全局安装：
::: code-tabs
@tab npm
```bash
npm install -g glyphix-cli
```

@tab pnpm
```bash
pnpm install -g glyphix-cli
```

@tab yarn
```bash
yarn global add glyphix-cli
```
:::

::: tip
使用 pnpm 全局安装前，可能要执行 `pnpm setup` 来配置环境变量，`pnpm install -g` 命令会提示如何配置环境变量。
:::

安装完成后，可以在终端中执行 `gx --version` 来查看安装是否成功。例如：
```bash
$ npm install -g glyphix-cli
$ gx --version
gx v0.10.1 - The Glyphix applet development toolchain
commit a9337cf1 - Tue Sep 23 10:03:48 2025 +0800
```

此外，还必须安装 [pngquant](#pngquant) 才能为某些设备打包应用资源。

### 手动安装

还可以从 glyphix.js 打包工具的压缩包手动安装：将解压后目录中的 `bin` 目录添加到 `PATH` 环境变量中。下面将介绍主流操作系统上的安装方法。

::: tip
glyphix.js 工具并不只是一个可执行文件，请勿遗漏其他资源文件（包括 `bin` 和 `share` 目录中的所有文件）。
:::

#### macOS / Linux

对于 macOS 或 Linux，可以使用 `tar` 命令来安装 glyphix.js 打包工具。在此之前，还需要安装 `xz` 等工具：

::: code-tabs
@tab macOS
```bash
brew install xz
```

@tab Ubuntu / Debian
```bash
sudo apt update
sudo apt install xz-utils
```

@tab Arch Linux
```bash
sudo pacman -S xz
```
:::

下载好 glyphix.js 的压缩包后，使用以下命令解压并安装：
::: code-tabs
@tab macOS
```bash
tar -xvJf glyphix-v0.7.2-darwin-arm64.tar.xz -C ~/.local
```

@tab Linux
```bash
tar -xvJf glyphix-v0.7.2-linux-x86_64.tar.xz -C ~/.local
```
:::
请注意将 `.tar.xz` 文件名替换为实际下载的、对应于操作系统和 CPU 架构的文件名。解压后，`gx` 等命令会位于 `~/.local/bin` 目录下，请将该目录添加到 `PATH` 环境变量中，例如这样更新 `.bashrc`：
```bash
# 如果 ~/.local/bin 不在 PATH 中，则添加
echo "$PATH" | grep -q "$HOME/.local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc # 重新加载 bash 配置
```

::: tip
在使用 `Zsh` 时，`.zshrc` 配置文件可能导入了 `.bashrc`，因此只需要更新 `.bashrc` 即可。否则请按上述方法更新 `.zshrc`。

建议将 glyphix.js 打包工具安装在用户的 `~/.local` 目录中，这样可以避免使用 root 权限安装。
:::

#### Windows

要在 Windows 上安装 glyphix.js，请下载对应的 Windows 版本压缩包，然后使用支持 `7z` 格式的解压工具（例如 [7-Zip](https://www.7-zip.org/)）将其解压到某个目录下，例如 `C:\glyphix`。然后将 `C:\glyphix\bin` 添加到系统的 [`PATH` 环境变量](https://learn.microsoft.com/zh-cn/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14))中。

也可以使用 `7z` 命令行工具来解压，例如：
```shell
7z x -y glyphix-v0.7.2-windows-x64.7z -oC:/glyphix
```
这和 macOS 等系统的安装方法类似。

### 安装系统依赖

#### pngquant

Linux 和 macOS 用户需要额外安装 `pngquant`，你可以使用 `npm` 来安装它：
```bash
npm install -g pngquant-bin # pngquant-bin 只支持用 npm 安装
```
Windows 的 `glyphi-cli` 包含了 `pngquant.exe`，因此不需要额外安装。

::: tip
还可以从 [pngquant.org](https://pngquant.org/) 下载预编译的二进制文件，或者从系统的包管理器安装。
:::

#### Linux 系统依赖

glyphix.js 的 Linux 安装包不区分具体发行版，目前仅有 linux-x86_64 架构的构建包。我们测试其可以在 Ubuntu 20.04（或更新）和 Arch Linux 上运行。

如果你仅使用 `gx` 命令进行打包（这常用于 CI 打包），那么无桌面环境的 Linux 发行版应该可以直接使用。运行图形化的模拟器则依赖 X 窗口系统，因此您可能要安装 xorg 相关的软件包，尤其是 Wayland 环境下，您还需要安装 `xwayland` 软件包（模拟器尚不支持原生 Wayland）。

### 卸载

对于通过 npm 等包管理器全局安装的 glyphix.js，可以使用相应的包管理器来卸载，例如：
::: code-tabs
@tab npm
```bash
npm uninstall -g glyphix-cli
```

@tab pnpm
```bash
pnpm uninstall -g glyphix-cli
```

@tab yarn
```bash
yarn global remove glyphix-cli
```
:::

::: tip
对于使用 npm 等包管理器的非全局安装，只需要删除 `package.json` 中的 `glyphix-cli` 依赖，并执行 `npm install`（或 `pnpm install`、`yarn install`）来更新 `node_modules` 目录。
:::

对于手动安装，删除安装压缩包中的文件即可，例如对于 macOS 和 Linux 的 `tar.xz` 安装文件：
```bash
tar -tf glyphix-v0.7.2-darwin-arm64.tar.xz > filelist.txt
cat filelist.txt # 检查要删除的文件列表
xargs -I {} rm -f "~/.local/{}" < filelist.txt # 确认无误后执行删除
```
`tar -tf` 命令会列出压缩包中的文件列表，应该将 `glyphix-xxx.tar.xz` 替换为实际的安装文件。Windows 上的手动卸载操作也类似。

## 构建和运行

安装后 glyphix.js 后，在应用源代码的根目录中使用 [`gx build`](#gx-build) 命令来构建应用包，或使用 [`gx emu`](#gx-emu) 命令运行模拟器。

构建应用以后，请参考[提交应用包](#提交应用包)章节来了解如何将应用安装到设备上，或是提交到应用发布平台。

## 命令行参数

### 通用选项

#### `gx --help`

查看帮助信息。在具体的子命令中也可以使用帮助信息，例如使用 `gx build --help` 可以单独查看 `build` 子命令的帮助信息。

#### `gx --version`

`-V --version` 选项用于查看 `gx` 命令的版本号。

#### `gx --verbose`

`-v --verbose` 启用详细日志输出，应用开发者通常无需使用。

#### `gx --numeric-version`

输出 `gx` 命令的纯数字版本号，例如 `0.10.1`。

#### `gx --quiet`

`-q --quiet` 启用安静模式，抑制大部分非警告、错误的日志输出。这包括使用 `gx build` 时的构建进度日志，这种模式通常在需要构建大量应用包的 CI 环境中使用。

查看版本号。

### `gx new`

创建一个新项目，例如 `gx new myapp` 会创建一个名为 `myapp` 的新项目。

### `gx build`

构建项目（默认操作），使用 `--device` 或 `-d` 选项可以指定目标设备，例如
``` bash
gx build -d default # 指定为 default 设备构建
```
使用 `--dump` 选项可以打印 UX 文件的编译细节信息。

glyphix.js 支持增量构建，当源代码发生变动时，只有变化的部分会重新构建。

`-r --image-rules` 参数可以指定图片打包规则文件，默认为 `config/image-rules.json`。此参数的值会被缓存，后续执行 `gx build` 或 `gx emu` 将会按照先前的配置执行。

#### 命令选项

- `-d --device=NAME`：指定目标设备名称，必须是已安装的设备配置名称。可以使用 `gx list device` 命令查看已安装的设备列表。如果不指定该选项，则默认使用 `default` 设备。
- `-f --full`：强制完全重新构建项目，而不是增量构建。
- `-e --emulator`：为模拟器构建项目，而不是为实际设备构建。执行 `gx emu` 命令时会自动使用该选项。
- `-r --image-rules=PATH`：指定图片打包规则文件，默认为 `config/image-rules.json`。

#### 提交应用包

使用 `gx build` 构建后，将会在项目目录下生成 `.glyphix-work/dist/<device-name>/<package-name>` 目录，里面包含了构建好的应用包文件（`.pkg` 文件）。可以将该文件通过手机调试应用安装到设备上运行，也可以提交到应用发布平台。

应使用 `-d` 选项为所有需要支持的设备分别构建应用包。这是一个示例目录结构：
```bash
.glyphix-work/dist
├─ generic-watch-368x448
│  └─ com.example.app
│     ├─ bundle.pkg
│     ├─ icon.png
│     └─ manifest.json
└─ generic-watch-466x466
   └─ com.example.app
      ├─ bundle.pkg
      ├─ icon.png
      └─ manifest.json
```
在提交应用包时，请将**整个** `.glyphix-work/dist` 目录打包上传，而不是仅上传 `.pkg` 文件，或是任一子目录。平台会根据 `manifest.json` 文件中的信息来识别应用，并可能需要 `icon.png` 作为预览图标。

::: tip
对于 Linux 或 macOS 用户，可以使用这样的命令来打包某类设备的应用：
```bash
gx list device | grep "^generic-" | xargs -n 1 gx build -d
```
这会为所有名称以 `generic-` 开头的设备构建应用包。

Windows 下也可以使用类似的 PoweShell 命令批量构建：
```shell
gx list device | ? { $_ -match "^generic-" } | % { gx build -d $_ }
```
:::

### `gx emu`

相见[模拟器和调试](/tutorials/glyphix.js/emulator.md)文档。

### `gx clean`

清理构建产物，此命令会将项目文件夹下的 `.glyphix-work` 目录删除。

### `gx config`

此命令启动一个编辑图片打包规则文件的 Web 界面，按照命令提示可在浏览器中打开页面进行操作。该命令有两种用法：
``` bash
gx config # 在 Glyphix 项目中时，不用指定源目录（目前只能在项目根目录下使用）
gx config path/to/dir # 对指定的目录进行配置，可用于非项目图片资源的配置
```

`-r --image-rules` 参数可以指定图片打包规则文件，默认为 `config/image-rules.json`。

### `gx image-forge`

对游离的图片文件进行转换。该命令可以指定任意的源路径和输出路径，不需要在 Glyphix 项目中执行：
``` bash
gx image-forge src -o dist
```

选项说明：
- `src` 是要转换的源路径，`image-forge` 命令递归地转换所有的图片并按照相对目录结构生成到 `-o, --output` 指定的目标路径中（默认为 `dist`）。
- `-r --image-rules` 参数可以指定图片打包规则文件，默认为 `config/image-rules.json`。
- `-d --device` 指定图片转换的目标设备。

### `gx list`

列出某些信息。目前支持三种操作：
``` bash
gx list device # 列出所有已安装的设备配置
gx list template # 列出所有已安装的项目模板
gx list image # 列出当前目录下所有图片资源的相对路径（类似于 find 命令）
```

某些信息可以使用 `-d, --detailed` 来列出详细的说明文本，例如：
```
$ gx list device -d
The following devices have been found:
  default
    Default virtual device, for debugging purposes only.

  rtt-watch
    A smartwatch from RT-Thread. With a 1.43 inch screen
    and 4 GB of storage.
```

### `gx completion`

此命令用于生成 `gx` 命令的 shell 的自动补全脚本，目前支持 [Zsh](https://www.zsh.org/) 和 [PowerShell 7+](https://github.com/PowerShell/PowerShell)。使用 `gx completion [SHELL]` 会输出指定 shell 的自动补全脚本（不指定 `SHELL` 参数时会检测当前 Shell）。如果要安装补全脚本，请使用：
```bash
gx completion --install
```
安装成功后会提示命令补全脚本的安装路径，重启 Shell 会话即可使用自动补全，也可以使用这些命令立即生效：
::: code-tabs
@tab Oh My Zsh
```bash
omz reload
```

@tab PowerShell
```shell
Import-Module glyphix -Force
```
:::

使用自动补全脚本时可以在终端中选择 `gx emu` 的设备、命令行选项等，而不需要手动输入。

PowerShell 默认使用循环补全，建议更改为补全菜单：
```shell
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
```
将该命令添加到 [`$PROFILE`](https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/creating-profiles#adding-customizations-to-your-profile) 配置文件即可永久生效。

::: note
如果 `--install` 选项无法自动安装，还可以用 `gx completion` 命令手动安装补全脚本，例如：
```shell
gx completion zsh > ~/.zsh/completion/_gx.zsh
```
:::

## 默认配置路径

glyphix.js 工具中的配置、项目模板、设备信息等信息可以存储在以下路径中：
- 系统级配置：相对于 `gx`/`gx.exe` 可执行文件上级目录的 `share/glyphix` 目录。假设例如 `gx` 可执行文件的路径在 `/usr/local/glyphix`，那么系统级配置配置的资源路径是 `/usr/local/share/glyphix`
- 用户级配置：在类 Unix 系统中为 `~/.local/share/glyphix`，在 Windows 中为 `%APPDATA%\AppData\Roaming\glyphix`

可以将配置文件存放在以上路径之一，其中用户级配置的优先级更高。`gx.js` 安装时会自带默认配置文件。

## 工程模板

项目模板存储在配置路径的 `templates` 目录下，目前只支持 `simple` 模板，并且不支持自定义。

## 设备配置文件

设备配置文件存储在配置路径的 `devices` 目录下。每个设备都一个 YAML 配置文件，配置文件的名称为 `<device-name>.yml`。配置文件的格式说明如下：

``` yaml
# file: default.yml
description:
  供开发者查看的设备描述信息。

screen: # 描述设备屏幕配置的字段，这些字段都是必填的（会影响 UI 布局和资源缩放）
  width: 454 # 屏幕水平像素数
  height: 454 # 屏幕垂直像素数
  dpi: 326 # 屏幕的像素密度，单位是像素/英寸

ui: # 全局界面配置，都是可选字段
  font-family: sans-serif # 系统默认的字体族名称（默认为 serif）
  font-size: 3.5 # 系统默认的字号，单位是磅（pt、点），注意不是像素！！
  font-map: true # 是否使用全局字体配置映射文件，如果是，则系统资源中必须存在
                 # font-faces.css 文件

# 可选的系统的全局资源包路径，以下配置意味着全局资源包存储在 default.yml 同级的
# default-global 文件夹下。全局资源包包含系统中预置的字体和字体配置映射文件等。
global-assets: default-global

# 可选的图片转换脚本，脚本文件路径相对于当前设备描述文件存放。如果不指定图片转换
# 脚本打包时会输出原始 PNG 素材，但是会应用分辨率缩放。
image-build: image-convert.scm

# 运行模拟器的命令，默认会执行 glyphix-emu。模拟器命令的可执行文件必须位于 PATH
# 环境变量的路径下，否则会无法执行。
emulator: glyphix-emu
```


