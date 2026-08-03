---
icon: rocket
---
# Quick start

In this chapter, we'll show you how to use Glyphix.js to create a simple application. We will start by installing the packaging tools, then create a project and run the simulator to see the effect. Finally, we briefly introduce the structure and main documents of the project. This tutorial does not cover how to run your app on a real device or how to publish it.

## Preparation

Before starting, please refer to [this document](/doc_en/glyphix.js/README.md#npm-installation) to install the Glyphix packaging tool. Simply put, you can use [npm](https://nodejs.org) to install the `glyphix-cli` package:
```bash
npm install -g glyphix-cli
```

Since the development tools of Glyphix are mainly command line, it is recommended to install modern shells such as Zsh and PowerShell 7+, and install some practical plug-ins to improve operational efficiency.

### Terminal tools

For Linux or macOS users, it is recommended to install [Oh My Zsh](https://ohmyz.sh/). Windows users are recommended to install [Windows Terminal](https://aka.ms/terminal) and use [Oh My Posh](https://ohmyposh.dev/). Please also refer to the [`gx completion`](/doc_en/glyphix.js/README.md#gx-completion) document to install the auto-completion script for the `gx` command.

You can use any editor to develop Glyphix applications, such as [VS Code](https://code.visualstudio.com/) or [Quick App IDE](https://www.quickapp.cn/devtool).

::: tip
There is no built-in glyphix.js packaging tool in the Quick App IDE. You still need to install `glyphix-cli` and use the `gx` command in the terminal to build and run the project. When using editors such as VS Code, it is recommended to bind `*.ux` files to `html` format to obtain basic syntax highlighting.
:::

### Using Node.js

If you decide to use npm packages in your project, or any resources from the web development ecosystem, please refer to the [Node.js](/doc_en/nodejs.md) configuration document. Using Node.js is not required, but it can support modern development tools like TypeScript.

### Use packaging tools

After everything is ready, enter the `gx list device` command in the terminal. If you get output similar to the following, the installation is successful:
```bash
$ gx list device
  default
  ...
```

Next create an application project and simulate running it! Just use the following command:
```bash
gx new myapp # Create a project named myapp, which will create a directory named myapp
cd myapp # Switch to the myapp directory
gx emu # Run emulator
```
As expected, you will see a window that says "Hello World!" The following tutorials will further explain how to use the commands of the glyphix.js tool.

::: tip
See the [`gx build`](/doc_en/glyphix.js/README.md#gx-build) and [`gx emu`](glyphix.js/emulator.html) documentation for more information on building and running the emulator.
:::

## Project structure

You can use a file browser to view the structure of the `myapp` directory. In the current version its structure is as follows:
```bash
<app-name>
├─ README.md # Project readme file
└─ src # The source code directory of the project
    ├─ app.js # app entry script file
    ├─ manifest.json # Configure basic application information
    ├─ assets # Store public resources (fonts, pictures, etc.)
    │ ├─ fonts # Store font resources
    │ └─ images # Store image resources
    └─ main # Directory to store the main page
        └─ index.ux #Interface description file of the main page
```

In the default project template, the source code is located in the `<app-name>/src` directory, and resources in the project that do not need to be packaged and released can be placed in other directories.

We recommend preparing a directory for each page (and using the name of the page as the directory name) and placing this directory in the root directory of the source code. Component source files (`*.ux` files) used only in the page should be placed in the directory of the page, while public files can be stored according to the following rules:
- Public UX files and scripts can be placed in the `common` directory
- Only script files referenced in the page are stored directly in the page directory
- Font files are stored in the `assets/fonts` directory
- Image files are stored in the `assets/images` directory
- Other assets can be stored in the appropriate location under the `assets` directory

### Project files

Now, you have seen that `myapp` has some files inside it. Please pay attention to the files with the suffix `*.ux` and the `manifest.json` file. These are the files that are most commonly encountered during development. The following tutorial will briefly introduce them.

## `manifest.json` file

The `manifest.json` file is the application configuration file, and this file will be used for application packaging. This file contains basic information about the application, including application name, version information, etc. It also contains descriptions and routing information for all pages within the application. In other words, you need to add the page description to `manifest.json` before you can jump to this page in code.

This is the content of the `manifest.json` file for the template application generated by the `gx` command:
``` json
{
  "package": "com.example.app",
  "name": "Example App",
  "versionName": "1.0.0",
  "versionCode": 1,
  "features": [],
  "router": { // Page routing information
    "entry": "main", // The initial page of the application
    "pages": { // Page description information
      "main": {
        "component": "index"
      }
    }
  }
}
```

::: warning
For educational purposes, there are some comments in this `manifest.json` code snippet, but JSON does not support comments, please do not add any comments in the project's `manifest.json` file.
:::

### Fill in application information

You can fill in your application information in `manifest.json`.

### Add page description information

In the root fields of the `manifest.json` file, the `router` and `pages` fields are related to page descriptions. The `router` field is the page routing table of the application. It must have at least an `entry` field to specify the entry page of the application. The `main` page is usually used as the entry page.

If you want to add a new page, you need to add content to the `pages` field. For example, if we want to create a new page named `NewPage`, the entry component of this page is `NewPage/index.ux`, then the content of the `pages` field is as follows:
``` json
"pages": {
  "main": {
    "component": "index"
  },
  "NewPage": { // This is a newly added page
    "component": "index"
  }
}
```
The `pages` field is a JSON object, each key of which is the name of the page, and by default the path to the page directory. The value corresponding to the page name is also an object, and its `component` is the name of the entry component of the page. This component must be stored in the page directory. The `component` field is the file name of the page entry component (excluding the suffix). All names are case-sensitive.

When you add or delete pages, remember to update the relevant fields in `manifest.json`.

For details on the structure of the `manifest.json` file, please refer to the relevant documentation.

## UX file introduction

UX (UI XML) is the interface description file of Glyphix. Taking the original template project as an example, the contents of the `main/index.ux` file are as follows:
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

A UX file is actually an XML file. This UX file has two root nodes: `<template>`, `<style>` and `<script>`. The content in the `<template>` node is the structural description of the interface, the `<style>` node defines the style sheet, and the content in the `<script>` node is a JavaScript script, which implements the interactive logic of this component.

::: tip
VS Code does not perform syntax coloring on UX files. You can switch the language to "HTML" in the lower right corner, which will have better highlighting effects.
:::

### Introduction to components

The object that the UX file corresponds to at runtime is called a component. Components are an important concept in the Glyphix JavaScript application framework. Each component is an interface element and has the following characteristics:
- Components have their own display effects
- Some components can respond to user input
- Some components can display corresponding effects based on data and status
- Components can be embedded into other components for use

Commonly used interface elements are components in the Glyphix JavaScript application framework, such as:
- Text: used to display text information
- Button: The button can also display text information. The most important thing is that it can respond to click events (of course it will also display the effect when clicked)
- List: The list accommodates other components and arranges them vertically. In addition, element components in the list can be moved through sliding gestures.

Components like lists that can hold other components are also called container components.

As you can imagine, a component has two elements: display appearance and behavioral logic. The `<template>` tag in the UX file declares the appearance of the component, taking `main/index.ux` as an example:
``` html
<template>
  <p>{{text}}</p>
</template>
```
The `main/index.ux` component implements content display by a `<p>` component, which is used to display text. The value of the `{{text}}` expression is the text to be displayed.

The JavaScript script in the `<script>` tag implements the behavioral logic of the component. In this tag, `export default` is always used to export a **component object**. The first thing to focus on is the `data` property of the component object, which is usually an object:
``` js
export default {
  data: {
    text: 'Hello, World!'
  }
}
```
Here, the `data` object has a `text` attribute, and the value of this attribute will be used as the display content of the previous `<text>` component.

### Component model and state update

If we need to design a component that displays different text when the component is clicked, then we need to listen to the input events on the component and update the display content. The following code will listen for click events on the `<p>` component:
``` html
<template>
  <p on:click="text += '!'">{{text}}</p>
</template>
```
The expression in the `on:click` attribute will be executed when the text is clicked. Therefore, when clicked, a `'!'` character will be added to the end of the `text` text displayed in the `<p>` component:

<glyphix id="getting-started-click-p" height="120" width="360" title="Click event">

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

In the following tutorials we will introduce the component update mechanism in detail.

## Start developing applications

Now you can start developing your own Glyphix applications! Start writing code from the default project template and run the emulator using the `gx emu` command. Other chapters in this document will introduce how to use Glyphix's built-in mechanisms, APIs, and components to build interfaces, and how to implement application interaction logic.