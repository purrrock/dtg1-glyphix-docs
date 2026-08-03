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
