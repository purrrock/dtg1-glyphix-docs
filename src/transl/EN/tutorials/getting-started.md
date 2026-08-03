---
icon: rocket
---
# Quick Start

In this chapter, we will introduce how to use Glyphix.js to create a simple application. We will start by installing the packaging tool, then create a project, and run the simulator to see the results. Finally, we will briefly introduce the project structure and main files. This tutorial does not cover how to run applications on real devices or how to publish them.

## Preparation

Before getting started, please refer to [this document](/tutorials/glyphix.js/README.md#npm-installation) to install the Glyphix packaging tool. Simply put, you can use [npm](https://nodejs.org) to install the `glyphix-cli` package:
```bash
npm install -g glyphix-cli
```

Since Glyphix development tools are primarily command-line based, it is recommended to install a modern shell such as Zsh or PowerShell 7+, along with some practical plugins to improve operational efficiency.

### Terminal Tools

For Linux or macOS users, it is recommended to install [Oh My Zsh](https://ohmyz.sh/). Windows users are recommended to install [Windows Terminal](https://aka.ms/terminal) and use [Oh My Posh](https://ohmyposh.dev/). Please also refer to the [`gx completion`](/tutorials/glyphix.js/README.md#gx-completion) documentation to install the auto-completion script for the `gx` command.

You can use any editor to develop Glyphix applications, such as [VS Code](https://code.visualstudio.com/) or the [Quick App IDE](https://www.quickapp.cn/devtool).

::: tip
The Quick App IDE does not have the glyphix.js packaging tool built-in. You still need to install `glyphix-cli` and use the `gx` command in the terminal to build and run your project. When using editors like VS Code, it is recommended to associate `*.ux` files with the `html` format to get basic syntax highlighting.
:::

### Using Node.js

If you decide to use npm packages or any resources from the web development ecosystem in your project, please refer to the [Node.js](/tutorials/nodejs.md) configuration guide. Using Node.js is not mandatory, but it enables modern development tools such as TypeScript.

### Using the Packaging Tool

Once everything is ready, type the `gx list device` command in your terminal. If you see an output similar to the following, it means the installation was successful:
``` bash
$ gx list device
  default
  ...
```

Next, let's create an application project and run it in the simulator! Just use the following commands:
``` bash
gx new myapp # Create a project named myapp, which will create a directory named myapp
cd myapp     # Switch to the myapp directory
gx emu       # Run the simulator
```
Without any issues, you should see a window displaying "Hello World!". Subsequent tutorials will further explain how to use the commands of the glyphix.js tool.

::: tip
Refer to the [`gx build`](/tutorials/glyphix.js/README.md#gx-build) and [`gx emu`](glyphix.js/emulator.html) documentation for more information about building and running the simulator.
:::

## Project Structure

You can use a file explorer to view the structure of the `myapp` directory. In the current version, its structure is as follows:
``` bash
<app-name>
├─ README.md         # Project README file
└─ src               # Project source code directory
    ├─ app.js        # App entry script file
    ├─ manifest.json # Configures basic application information
    ├─ assets        # Stores public resources (fonts, images, etc.)
    │  ├─ fonts      # Stores font resources
    │  └─ images     # Stores image resources
    └─ main          # Directory storing the home page
        └─ index.ux  # Interface description file for the home page
```

In the default project template, the source code is located in the `<app-name>/src` directory, while project documents and other resources that do not need to be packaged and released can be placed in other directories.

We recommend preparing a directory for each page (using the page name as the directory name) and placing this directory under the root of the source code. Component source files (`*.ux` files) used exclusively within a page should be placed in that page's directory, while common files can be stored according to the following rules:
- Common UX files and scripts can be placed in the `common` directory
- Script files referenced exclusively by a specific page are placed directly in that page's directory
- Font files are stored in the `assets/fonts` directory
- Image files are stored in the `assets/images` directory
- Other resources can be placed in appropriate locations within the `assets` directory

### Project Files

By now, you have seen some files inside `myapp`. Please pay attention to files with the `*.ux` extension and the `manifest.json` file, as these are the files you will interact with most frequently during development. The following tutorial will briefly introduce them.

## The `manifest.json` File

The `manifest.json` file is the configuration file for the application and is used during app packaging. This file contains basic application information, such as the app name and version information, as well as descriptions and routing information for all pages within the app. In other words, page descriptions must be added to `manifest.json` before you can navigate to those pages in your code.

Here is the content of the `manifest.json` file generated by the `gx` template application:
``` json
{
  "package": "com.example.app",
  "name": "Example App",
  "versionName": "1.0.0",
  "versionCode": 1,
  "features": [],
  "router": { // Page routing information
    "entry": "main", // Initial page of the application
    "pages": { // Page description information
      "main": {
        "component": "index"
      }
    }
  }
}
```

::: warning
For educational purposes, there are some comments in this `manifest.json` code snippet, but JSON does not support comments. Please do not add any comments to the `manifest.json` file in your project.
:::

### Filling in Application Information

You can fill in your application information in `manifest.json`.

### Adding Page Description Information

In the root fields of the `manifest.json` file, the `router` and `pages` fields are related to page descriptions. The `router` field is the application's page routing table and must have at least an `entry` field to specify the entry page of the application, usually using the `main` page.

If you want to add a new page, you need to add content to the `pages` field. For example, if we want to create a new page named `NewPage`, with its entry component being `NewPage/index.ux`, the `pages` field will now look like this:
``` json
"pages": {
  "main": {
    "component": "index"
  },
  "NewPage": { // This is the newly added page
    "component": "index"
  }
}
```
The `pages` field is a JSON object where each key is the name of a page, which by default is also the path of the page directory. The value corresponding to the page name is also an object, and its `component` is the name of the page's entry component, which must be stored in the page directory. The `component` field is the file name of the page entry component (without the extension). All names are case-sensitive.

Remember to update the relevant fields in `manifest.json` whenever you add or remove pages.

For detailed descriptions of the `manifest.json` file structure, please refer to the related documentation.

## Introduction to UX Files

UX (UI XML) is Glyphix's interface description file. Taking the initial template project as an example, the content of the `main/index.ux` file is as follows:
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

A UX file is essentially an XML file with three root nodes: `<template>`, `<style>`, and `<script>`. The content within the `<template>` node describes the structure of the interface, the `<style>` node defines the style sheets, and the content within the `<script>` node consists of JavaScript scripts that implement the component's interaction logic.

::: tip
VS Code does not provide syntax coloring for UX files by default. You can switch the language to "HTML" in the bottom-right corner to get better highlighting effects.
:::

### Introduction to Components

The runtime object corresponding to a UX file is called a **component**. Components are an important concept in the Glyphix JavaScript application framework. Each component is an interface element with the following characteristics:
- Components have their own visual presentation
- Some components can respond to user input
- Some components can display corresponding effects based on data and state
- Components can be embedded and used within other components

Common interface elements in the Glyphix JavaScript application framework are all components, for example:
- Text: Used to display textual information
- Button: Buttons can display text, and most importantly, they can respond to click events (while also showing visual feedback upon clicking)
- List: Lists contain other components and arrange them vertically; elements within a list can also be moved via swipe gestures

Components that can contain other components, like lists, are also called **container components**.

As you can imagine, a component has two main elements: visual appearance and behavioral logic. The `<template>` tag in a UX file declares the component's appearance. Taking `main/index.ux` as an example:
``` html
<template>
  <p>{{text}}</p>
</template>
```
The `main/index.ux` component uses a `<p>` component to display content. This type of component is used to display text, and the value of the `{{text}}` expression is the text to be displayed.

The JavaScript script inside the `<script>` tag implements the component's behavioral logic, always exporting a **component object** using `export default`. The first thing to focus on is the `data` property of the component object, which is typically an object:
``` js
export default {
  data: {
    text: 'Hello, World!'
  }
}
```
Here, the `data` object has a `text` property, and the value of this property will be used as the display content of the aforementioned `<text>` (or `<p>`) component.

### Component Model and State Updates

Suppose we need to design a component that displays different text when clicked. In this case, we need to listen for input events on the component and update the display content. The following code listens for click events on the `<p>` component:
``` html
<template>
  <p on:click="text += '!'">{{text}}</p>
</template>
```
The expression in the `on:click` attribute is executed when the text is clicked. Therefore, upon clicking, an `'!'` character is appended to the `text` displayed in the `<p>` component:

<glyphix id="getting-started-click-p" height="120" width="360" title="Click Event">

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

In subsequent tutorials, we will cover the component update mechanism in detail.

## Start Developing Your App

Now, you can start developing your own Glyphix application! Begin writing code from the default project template and run the simulator using the `gx emu` command. Other sections of this document will explain how to use Glyphix's built-in mechanisms, APIs, and components to build interfaces, as well as how to implement application interaction logic.