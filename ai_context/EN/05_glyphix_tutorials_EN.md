# Context File: 05_glyphix_tutorials_EN.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/transl/EN/tutorials/nodejs.md

---
icon: nodejs
---
# Node.js Package Managers

In addition to standalone usage, the `gx` build tool can be used in conjunction with JavaScript package managers such as npm, pnpm, or yarn. The prerequisite is installing the `glyphix` package:

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

Otherwise, you may encounter an error like this when running `gx build`:
```bash
$ gx build
fatal: glyphix not found, please install it by `npm install -D glyphix' or other package manager.
```

Using a JavaScript package manager in Glyphix application development mainly offers the following benefits:
- Use TypeScript instead of JavaScript as the development language, providing type safety and a better development experience
- Use JavaScript libraries from the Node.js ecosystem suitable for embedded development (such as algorithm libraries, data processing tools, etc.)
- Use tools like ESLint and Prettier to improve code quality and development efficiency
- Facilitate team collaboration and project maintenance

::: warning
Currently, only standard JavaScript or TypeScript dependencies can be managed via package managers; Glyphix components cannot be reused. When choosing third-party libraries, please ensure they are suitable for embedded environments and avoid using libraries that depend on the DOM, Node.js-specific APIs, or are excessively large.
:::

::: tip
If [Glyphix.js](glyphix.js/README.md) devtools is installed globally, you can directly run commands like `gx build` to bundle the app; otherwise, you need to add `scripts` configuration in `package.json`.
:::

## Project Configuration

### `package.json` Configuration

When using a Node.js package manager, it is recommended to add the necessary scripts and configurations to `package.json`:

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

### `tsconfig.json` Configuration

If using TypeScript, you need to create a `tsconfig.json` file in the project root directory:

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
The Glyphix build tool automatically handles the compilation of TypeScript files. The above configuration is mainly used for IDE type checking and code completion.
:::

## `glyphix.config.js` Configuration

It is recommended to create a `glyphix.config.js` file in the project root directory (the directory containing `src/` or `package.json`) to customize build options:
```js
module.exports = {
  minify: false, // Disable code minification for easier debugging with source line numbers
};
```
If you use TypeScript, you can create a `glyphix.config.ts` file instead.

::: tip
Be sure to create this file and configure `minify: false`; otherwise, the bundled code will be minified and obfuscated, making it impossible to map back to source line numbers during debugging.
:::

## Using TypeScript

The Glyphix framework provides experimental TypeScript support, allowing you to enjoy the benefits of type safety and modern JavaScript syntax in application development.

### Basic Component Example

Below is an example of a component written in TypeScript:

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

Compared to default JavaScript component scripts, using TypeScript requires the following adjustments:
1. Use `lang="ts"` in the `<script>` tag to specify the language type as TypeScript.
2. Import the `defineComponent` function from the `glyphix` module.
3. Pass the component object to be exported as an argument to `defineComponent`, and export the return value of this function.

After using TypeScript, the `defineComponent` function will make code completion and type checking in the IDE more accurate.

### `app.ts`

Simply rename `app.js` to `app.ts` to switch to a TypeScript application entry file, and the build tool will handle it automatically.

============================================================
FILE_PATH: src/transl/EN/tutorials/name-spec.md

---
icon: code-tags-check
---
# Component Naming Conventions

This document describes the mandatory naming conventions and recommended naming styles for the component framework. Mandatory naming conventions are strict requirements, and non-compliance may lead to unexpected behavior. Using the recommended naming conventions ensures maximum compatibility.

## Template Naming Conventions

Tag names in templates must be named in kebab-case or PascalCase:
``` html
<Button></Button>
<button></button>
<scroll-area></scroll-area>
<ScrollArea></ScrollArea>
```

Attribute names must be in kebab-case or camelCase:
``` html
<component prop-name="expr"></component>
<component propName="expr"></component>
```

It is recommended to consistently use kebab-case, which aligns with Web standards.

## JavaScript Code Naming Conventions

Component names in JavaScript code must use PascalCase, while the corresponding kebab-case names are used in templates.

Component property names in JavaScript code must use camelCase:
``` js
export default {
  data: {
    propName: 0 // The attribute name in the template is prop-name
  }
}
```
These property names will automatically be converted to the corresponding kebab-case names in template code.

## File Naming Conventions

UX files must use the same name as the component, which means PascalCase. In the `<import>` tag, the `src` attribute must be a case-sensitive file URL, while the `name` attribute uses PascalCase or kebab-case:
``` html
<import src="path/to/UxFile" name="UxFile"/>
<import src="path/to/UxFile" name="ux-file"/>
```
In fact, the naming requirements for the `name` attribute are consistent with the tag names in templates.

============================================================
FILE_PATH: src/transl/EN/tutorials/qa.md

---
icon: help-circle-outline
---
# Frequently Asked Questions

## Bundling Tools

### Project Build Issues

#### `Lisp Error: thread killed` Error

Specifically, an error message similar to the following appears:

``` log
[ 47%] Process image src/assets/images/frame1.png
error: Lisp Error: thread killed
```

This issue is caused by an error in a preceding build task, which causes the ongoing image conversion build task to be canceled. Simply fix the build task that threw the `fatal` error to resolve it; no special handling is required for this error itself.

### Emulator

#### Default Emulator Language

The default language for the emulator is `zh-CN`. Therefore, if you have added [i18n](/framework/component/i18n.md) configurations, the `zh-CN.json` translation file will be used by default. When running the emulator with the `gx` command, you can use the `-l` or `--language` option to specify the language:
``` shell
gx emu -l en-US # Use American English
```
You can also dynamically change the language using the inspector debugging tool while the emulator is running.

============================================================
FILE_PATH: src/transl/EN/tutorials/quick-orientation.md

---
title: Quick Start: From Web to Glyphix
icon: compass
---

# Quick Start: From Web to Glyphix

This document is designed for developers familiar with Web front-end development (especially Vue.js). We will skip basic syntax tutorials and jump directly into the core mechanisms of the Glyphix framework to help you quickly build the correct mental model.

## Core Concepts and Runtime Environment

Glyphix is an application framework running on MCU (Microcontroller Unit) devices. Although it uses HTML/CSS/JS for development, it is **not** a browser. This framework is used to build complete applications rather than refreshable web pages, and each application runs in an independent sandbox container.

You need to understand the following core differences:
- **No DOM**: The underlying layer is rendered directly by a native C++ engine; there is no DOM tree.
- **No Web APIs**: Browser APIs such as `window`, `document`, and `localStorage` are not supported. System capabilities (network, storage, sensors) are provided via `@system.*` modules.
- **JS Engine**: It uses a lightweight JS engine (supporting ES6 standards), but memory is extremely limited.

### Resource Constraints

Resource constraints are the biggest difference compared to Web development. The RAM of MCU devices is typically only a few megabytes. This means you should not use network requests to load massive JSON data or directly [`fetch`](../api/system-fetch.md) an image. Keep the following points in mind:
- You can use the [`@system.request`](../api/system-request.md) module to download resources as files; `fetch` loads the response directly into memory.
- Image resources are usually stored inside the application package, and their dimensions should match the screen resolution as closely as possible.
- **Background Freezing**: After an application enters the background (`onHide`), it will typically be suspended or destroyed by the system within a few tens of seconds. Please make sure to save the application state.

### Device Form Factors

Glyphix applications typically run on small-screen devices such as smartwatches. Watch screens are usually around 1.5 to 2 inches, with a typical resolution of 466×466 pixels, though both circular and rectangular screens exist. Lower-end devices may have lower pixel density, but their dimensions are generally similar. These devices commonly interact via touchscreens and may support physical buttons or rotating crowns; the system transparently handles most interaction details.

Emulators are typically used for development and debugging, as physical device deployment and debugging workflows are still relatively fragmented and time-consuming.

### Typical Project Structure

This is our recommended project file structure, which is also the standard structure for Quick Apps:
```bash
src/
├─ manifest.json  # Application manifest: configure permissions and register page routes
├─ app.js         # Application entry point: global lifecycles (onCreate, onDestroy)
├─ pages/         # Pages directory
│  └─ Main/
│     └─ index.ux # Page component
└─ assets/        # Common assets
  └─ icon.png
```
You can introduce the [Node.js](nodejs.md) toolchain to manage dependencies as needed. You can also adjust the directory structure as required, but [`src/manifest.json`](/framework/application/manifest.md) and `src/app.js` must remain in these fixed locations.

## UI Development

Glyphix adopts [`.ux`](../framework/component/README.md) single-file components (similar to Vue SFC), with a style close to the Vue Options API, but with significant differences.

### Flexbox Layout First

Web defaults to Flow Layout, whereas Glyphix pages default to a stacked layout: if you place two `div` elements on a page, they will **overlap** rather than be arranged vertically. This is because the framework supports multiple root nodes in `<template>`, for example:
```html
<template>
  <image class="background" src="/assets/bg.png" />
  <div class="content"> ... </div>
</template>
```
The default stacked layout is usually very suitable for this kind of scenario.

Although containers like `div` default to flow layout, Flexbox is recommended for layout control. Most containers should explicitly declare `display: flex`, combined with `flex-direction` to control child element layout.

Given the significant variations in device screen sizes, pay special attention to the use of length units:
- Use `px` units for small dimensions; it represents logical pixels and scales automatically based on screen density.
- Fonts should always use `rem` units, whose baseline is defined by device manufacturers to better align with system UX consistency standards.
- Percentage (`%`) units can be used to achieve responsive layouts, but there are currently many limitations and flaws, so please be careful when debugging.

Because screens are very small, you may particularly need the [`scroll`](../components/scroll.md) component to create scrollable areas. Unlike the Web, `div` containers themselves do not support scrolling, nor can they be controlled using the `overflow` property.

### Template Syntax Differences

Although it looks like Vue templates, note the following differences:
- Directives do not have the `v-` prefix: e.g., `<div if="show">` or `<div for="item in items">`.
- Event binding can use `on` or `@`: e.g., `<p on:click="handler">`.
- Text components like `<p>` must be used: `<text>Hello</text>` renders correctly, but `<div>Hello</div>` will not render any content.
- Supports [two-way binding](../framework/commands/model.md) on any component property using `model:prop="state"` or `::prop="state"`, as long as an event with the same name as the property is triggered.

### Style Limitations

CSS support is a subset:
- Supports class (`.class`), ID (`#id`), tag (`div`), and descendant (`.a .b`). Complex combinators such as `~`, `+`, and `>` are **not supported**.
- **Visual effect limitations**: Gradients, shadows, etc., are not supported. `transition` animations are currently not supported.
- **Performance limitations**: Avoid using `transform` to move or align elements. `object-fit` defaults to `none`, and keeping the default is recommended.
- Dynamic `class` binding and CSS variables are currently not supported.

## Components and Logic

### Script Model

Component scripts are very close to the Vue Options API; the following example highlights the main differences:
```js
export default {
  // Data model (Data): no need to declare props, data properties are automatically exported as props
  data: {
    count: 0, // Mutating this.count automatically triggers view updates
  },
  timer: null, // Non-reactive fields defined directly on the component instance (or left undeclared)
  // Lifecycle hooks
  onInit() {}, // Data initialized; network requests can be initiated
  onReady() {}, // UI rendering completed
  onDestroy() {}, // Be sure to clear timers and event subscriptions here

  // Methods, defined directly in the component object
  handleTap() {
    this.count++
    // Emit custom event to parent component
    this.$emit('change', { value: this.count })
  }
}
```
Fields in the `data` object are reactive properties, which currently only support JSON-compatible types (no `Date`, `Map`, `Set`, etc.). If reactive updates are not required, it is recommended to define fields on the component instance (`this`).

::: tip
Do not wrap methods inside a `methods` object; define them directly in the component object. You also do not need to use `props` to define properties—fields in the `data` object are automatically exported as props.

DOM APIs like `document.getElementById` cannot be used to find elements. You can use the [`this.$element()`](../framework/component/component-apis.md#element) method to get an element instance with a specified ID.
:::

### Pages and Routing

Glyphix applications consist of multiple pages, navigated via routing. All pages must be statically registered in the [`router.pages`](../framework/application/manifest.md#pages) field in `manifest.json`. Page components are similar to regular components, but they support `onShow` and `onHide` lifecycle hooks.

Use the `system.router` system module for navigation:
```js
import router from '@system.router'

// Navigate and pass parameters
router.push({ uri: 'pages/Detail', params: { id: 123 } })
```
::: tip
Do not use other routing libraries, and do not pretend to build a single-page application (SPA). Otherwise, you won't be able to utilize existing features such as transition animations and page stack management.
:::

### TypeScript Support

If you create a project using the Node.js scaffolding tool and install dependencies such as `glyphix` and `typescript` via npm, pnpm, etc., you can use TypeScript for development.

For `.ux` single-file components, you can add the `lang="ts"` attribute to the `<script>` tag to enable TypeScript support. For example:
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

## System Capabilities Integration

Do not attempt to use browser APIs; please use the Glyphix [standard library](../api/README.md).

### Common Modules Quick Reference

| Feature | Glyphix Module | Description |
| :--- | :--- | :--- |
| **Network** | [`@system.fetch`](../api/system-fetch.md) | Must handle async callbacks or Promises |
| **Prompt** | [`@system.prompt`](../api/system-prompt.md) | Provides Toast and Dialog |
| **Storage** | [`@system.storage`](../api/system-storage.md) | Synchronous local storage, reading/writing objects directly instead of strings |
| **Router** | [`@system.router`](../api/system-router.md) | Manages page stack |
| **Logging** | `console.log` | Outputs to debug terminal, same as browsers |

### Asynchronous Programming Patterns

System APIs usually support both asynchronous callback and Promise styles. Using `async/await` is recommended to keep code clean.

```js
import fetch from '@system.fetch'
import prompt from '@system.prompt'

export default {
  onReady() { this.loadData() },
  async loadData() {
    try {
      const response = await fetch.fetch({
        url: 'https://api.example.com/data',
        method: 'GET', // Defaults to GET
        responseType: 'json', // Avoids manual parsing with JSON.parse
      })

      if (response.data.code === 200)
        this.data = response.data.data
    } catch (err) {
      prompt.showToast({ message: 'Network Error' })
    }
  }
}
```

## Build and Run

Use the [`gx emu`](../tutorials/glyphix.js/README.md) command to launch the emulator, or `gx build` to build the application package. If you are using the Node.js CLI scaffolding, you can also run `gx` commands directly.

Please refer to the [Quick Start](getting-started.md) tutorial for detailed steps.

## Comprehensive Example

The following is a complete component example demonstrating the combined usage of layout, data binding, event handling, and system APIs. You can preview this example directly in the browser and click the `>` button to view the full code.

<glyphix id="quick-orientation-example" title="Counter Component Example" height="240">

```html
<!-- Flex layout recommended for root container; disabled during loading -->
<div class="container" :disabled="loading">
  <text class="title">Hello, {{ name }}</text>

  <div class="card">
    <text class="count">{{ count }}</text>
    <text class="btn" value="+1" on:click="increment">Add</text>
  </div>
</div>

<!-- Overlay loading prompt using page's stacked layout -->
<text if="loading" class="loading">Loading...</text>
```

```css
.container {
  /* Page components do not need width/height set; they always fill the screen */
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  /* Note: Page background is rarely set; this is for demonstration only */
  background-color: #f5f5f5;
  border-radius: 16px;
  padding: 10%; /* Percentage padding */
}

.title {
  font-size: 1.25rem; /* Use rem units for fonts */
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
  border-radius: 50%; /* Circular button */
  text-align: center;
}

.loading {
  color: #3d3d3d;
  font-size: 0.8rem;
  text-align: center;
}

/* Dimmed style for disabled state */
*:disabled {
  opacity: 0.5;
}
```

```js
import prompt from '@system.prompt'

export default {
  // Component data
  data: {
    name: 'Glyphix',
    count: 0,
    loading: false
  },
  // Lifecycle: component initialized
  onInit() {
    console.log('Component initialized')
    this.simulateFetch()
  },
  // Method definitions
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
    // Simulate async operation, creating a loading state
    setTimeout(() => {
      this.loading = false
      this.name = 'Developer'
    }, 1000)
  }
}
```

</glyphix>

============================================================
FILE_PATH: src/transl/EN/tutorials/README.md

---
title: Glyphix 应用开发教程
index: false
icon: routes
category:
  - Guide
---

## What is Glyphix

Glyphix is ​​an efficient, lightweight application development framework for MCU (microcontroller) devices. It provides developers with a declarative UI development paradigm similar to the Web ecosystem: through HTML templates, CSS, and JavaScript, developers can easily build pages and components and publish applications to various smart devices (such as smart watches).

For more information, please refer to the [Framework](/framework/README.md) chapter.

### Web-like framework

Unlike traditional MCU firmware development, Glyphix is ​​closer to a framework based on a web technology stack. App developers need to be familiar with JavaScript, CSS, and basic HTML knowledge. You don’t need to master the complete web development technology stack, such as browser DOM, standard HTML tags, and complex build tool chains. But if you are familiar with Web UI frameworks such as [Vue.js](https://vuejs.org/) ([Options API](https://vuejs.org/guide/introduction#options-api)), it will be easy to get started with Glyphix.

::: tip
To be clear, Glyphix is not a “low-code” platform. During the development process, you will still encounter challenges such as logic abstraction, interface organization, user experience, and performance trade-offs. Therefore, mastering a solid JavaScript foundation and a good front-end way of thinking will help you fully realize the potential of Glyphix.
:::

### Declarative UI framework

Traditional interface development is usually imperative: functions need to be called step by step to create controls, update state, and refresh the interface. This method is very flexible, but the business and interface logic are highly coupled. As the application scale expands, the code will quickly become complex and difficult to maintain. Patterns such as MVC and MVVM were proposed precisely to solve this complexity.

Glyphix adopts the declarative UI paradigm. Developers only need to describe "what the interface should look like", and the framework will automatically complete rendering and updates based on changes in data and state. This approach greatly reduces the complexity of interface logic and state management, and allows developers to focus on function and interaction design instead of maintaining the UI hierarchy and refresh process.

### Application container

Glyphix is ​​not just a UI framework, it also provides functions such as application life cycle management, permission isolation and system API. Applications run in an independent container and are isolated from each other to ensure system stability and security.

Please read the [Quick Start](getting-started.md) tutorial to get started with Glyphix application development immediately.

## Other questions

### Need to be familiar with MCU and embedded development?

Application developers generally do not need specific knowledge of MCUs and embedded development. But you should have some understanding of the device's resource limitations. For example, the memory capacity of MCUs is usually only a few MB, and there are also limits on the memory for running JavaScript code. This means that there may be an inability to request very large JSON data from the network, or to encode the entire image as Base64 and obtain it through a GET request.

These limitations, which are completely different from web development, are indeed caused by the limited resources of the MCU device, but this is not included in the typical MCU body of knowledge.

Intuitively, it's best to confirm that the app experience is good enough by running the app on the device. You can run it multiple times on a real device at different stages of development to ensure the best experience.

### Should C/C++ be used for application development?

Glyphix application development is done entirely using HTML, CSS, and JavaScript, so there is no need to use C/C++ languages.

### How can embedded developers get started with Glyphix application development?

Embedded developers can use this tutorial [Quick Start](getting-started.md) to gradually understand the core concepts of Glyphix. The framework uses a componentization and data binding mechanism similar to the Vue Options API, which will be a little different for readers who are used to imperative GUIs such as [LVGL](https://lvgl.io/) and Qt widgets. However, Glyphix's declarative design can also bring a more intuitive interface control experience.

Developers do not need to fully master HTML, CSS and JavaScript, but familiarity with the basic syntax of JavaScript (such as variables, conditional judgments, function calls, etc.) will help understand Glyphix's rendering logic and event processing. You can familiarize yourself with these contents through sample code and practical operations in tutorials and documents to speed up the development process.

### Do you want to pay attention to application performance optimization?

Our framework has been deeply optimized for the resource constraints of embedded systems and can adapt well to a variety of hardware environments. Most applications can run smoothly and stably enough under default settings, so there is usually no need to spend extra time on performance optimization.

If there is a need for in-depth understanding of specific optimization solutions in the future, we will provide special performance optimization documents to help developers further improve the operating efficiency of applications.

### Is there a difference between the Glyphix environment and the browser?

Yes, there are significant differences between the Glyphix environment and the browser. Glyphix does not have the DOM structure in the browser, nor does it provide objects such as `window` and `document`. Instead, it directly and uniquely provides a set of declarative interfaces through which developers can develop components and interact with interfaces. This design simplifies the development process and is more suitable for embedded environments.

============================================================
FILE_PATH: src/transl/EN/tutorials/component-basic.md

---
icon: information-outline
---
# Component basics

The previous document "[Quick Start](getting-started)" briefly introduced the concept of components. This tutorial will further explain the knowledge about components. Before reading this document, you need to know how to create and build a project, and how to edit source files. If you don't know, please read the "[Quick Start](getting-started)" tutorial.

## Introduction

In Glyphix application development, all interfaces are components - from buttons to pages. Component technology allows the development of interfaces using simple template languages:
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
This is basically the `main/index.ux` file of the default project template. Use the `gx emu` command to observe the display effect. The content in the `<template>` tag is the component's template, which describes the appearance of the component. Here, the `<p>` node will display the `text` property from the component model object. Please note that the component framework internally associates the content of the `<p>` node with the `text` attribute of the component model. As long as the value of the `text` attribute is modified, the interface will be updated synchronously.

We can test this with a timer:
``` js
export default {
  data: { text: "begin!" },
  onInit() {
    let count = 0
    setInterval(() => this.text = "timeout: " + count++, 1000)
  }
}
```
You will now see that the displayed count increases by 1 every second.

## Programming model of components

An important function of GUI programs is to change their appearance based on data and input to achieve interaction. In traditional GUI programming and native HTML, developers need to find the target element node in the interface tree and then call the API to update it. It turns out that developing interfaces in this way will be very complicated. Therefore, there are design patterns suitable for GUIs such as MVC, MVP, and MVVM, and some new frameworks have emerged in the field of Web development. These technologies have greatly reduced the difficulty of interface development.

The programming model of Glyphix components is very similar to front-end frameworks like Vue. The basic idea of ​​these frameworks is to calculate a new interface based on the state of the interface model, rather than requiring interface elements to be updated when the state changes. Compared with traditional technology, the interface view part in this solution is stateless and therefore simpler. Let's continue using the previous example:
``` html
<template>
  <p>{{ text }}</p>
</template>
```
We already know that the interface will automatically update when the `text` property of the component model is updated. However, in traditional GUI frameworks, it is often necessary to manually update the `<p>` node after the `text` of the model is updated (which usually comes from changes in input or internal data). Frameworks such as MVC can simplify these operations, but they are not very concise.

Now consider a very simple approach: we write a `render()` function that generates an interface tree based on the current state of the model. If we replace the original interface tree with the value of the `render()` function every frame, then any changes to the model will be reflected in the interface. This solution is very simple, but you will deny it because of the efficiency. In fact, it was to solve the efficiency problem of this solution that the traditional GUI programming model was born: only modified elements in the interface are modified, but it introduces state in the view layer and also brings a lot of complexity.

The Glyphix component framework is based on this simple concept: the content in the `<template>` tag implements the function of the `render()` function, while the js code focuses on maintaining the model, and data changes in the model will automatically be reflected in the relevant interfaces. You can think of the Glyphix component framework as always calculating a new interface based on the state of the model, so we don't have to manually update interface elements.

::: tip
The bottom layer of Glyphix is not a DOM tree, and naturally there is no API for operating DOM elements. In fact, the component framework is the native Glyphix JavaScript API.
:::

## Respond to input

There are some components that can respond to user input events. In this case, you can use the `on` directive to specify an event listener. For example, listen for click events on the text component:
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
Clicking on the text will automatically update the display. The value of the `on:click` attribute `text += ' click'` is a JavaScript expression, and Glyphix will automatically bind the `this` of the variable in the expression to the component object.

## Conditional rendering

The `if` directive is used to render component content conditionally. The content area controlled by this directive will be rendered only when the value of the expression in the `if` directive is true.
``` html
<p if="display">Hello World</p>
```

The following example will implement a mutually exclusive switch effect. When clicked continuously, the interface will alternately display the text "Component A" or "Component B".
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

## List rendering

Use the `for` directive to repeatedly render a component to generate a list. The basic usage of the `for` directive is:
``` html
<p for="(index, value) in list">{{index}}: {{value}}</p>
```
Among them, `list` is a list attribute in the component model (must be of type `Array`), `index` and `value` are two iteration variables, the value of `index` is the index of the current item, and the value of `value` is the value of the current item.

The `for` directive can be abbreviated to the following forms:
``` html
<p for="list">{{$idx}}: {{$item}}</p>
<p for="value in list">{{$idx}}: {{value}}</p>
<p for="index, value in list">{{$idx}}: {{value}}</p>
```
The first abbreviation is to only write the expression that needs to be iterated, in which case `$idx` and `$item` will be used as the default iteration variable names; the second way of writing explicitly defines the iteration variable of the current value, and the current index variable name uses the default `$idx`; the third way of writing is the abbreviation of the standard way of omitting parentheses.

::: tip
Due to the scope relationship, the variables used iteratively when writing the `for` directive will only take effect when used after the `for` directive.
:::

``` html
<!-- correct -->
<button for="list" text="{{$item}}"/>
<!-- error -->
<button text="{{$item}}" for="list"/>
```

### Use both `if` and `for` directives

You can use both the `if` and `for` directives on an element, in which case the `if` directive has higher priority. In this example, when the `display` property is false, the entire `button` component list will not render:
```html
<button for="value in items" if="display">Hello {{value}}</button>
<p if="!display">Paragraph 1</p>
```

And if your purpose is to conditionally render some nodes in the list generated by the `for` directive, you need to place the `if` directive on the inner element of the `for` directive.
```html
<button for="value in items">
  <p if="display">item: {{value}}</p>
</button>
```

::: tip
Using the `if` and `for` directives on the same element is not recommended as it reduces code readability.
:::

## slot

Similar to the content distribution of other frameworks, Glyphix also implements a set of content distribution APIs. We can use the `slot` component as an outlet to carry distributed content.

In the child component, use the `slot` component to host the content defined in the parent component. The `slot` component will become the element passed in by the parent component when rendering.

```html
<div>
  <slot/>
</div>
```

## Use components in combination

Combining multiple components into a larger interface is the Glyphix component framework's approach to interface building. If there is a component named `Menu`, you can import it by using the `<import>` tag under the root node of the UX file that needs to be referenced:
``` html
<import src="path/to/Menu" name="Menu"/>
```
The `src` attribute is the path of the component, do not add the `.ux` suffix. The `name` attribute is an optional component name. If this attribute is not filled in, the component's file name will be used as the component name.

Use the `<import>` tag multiple times to import all dependent components:
``` html
<import src="path/to/ComA"/>
<import src="path/to/ComB"/>
<import src="path/to/ComC"/>
```

Custom components can be used just like native components:
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

This is a menu interface. We hope that when the user clicks on the menu, the information of the current menu item will be printed through the `clickMenu` method. Therefore, the `Menu` component needs to be able to display menu content and be able to monitor its own click event through `on:click`.

This is the content of the `Menu.ux` file:
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
We simply use a native component `div` to respond to user clicks and report them. The `div` component will also display the subcomponent passed in last time, finally allowing the menu list to be displayed.

============================================================
FILE_PATH: src/transl/EN/tutorials/getting-started.md

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

============================================================
FILE_PATH: src/transl/EN/tutorials/glyphix.js/image-forge.md

---
icon: image-filter
---
# Image management

The glyphix.js packaging tool will manage all PNG image resources in the project (`src` directory). Related modules mainly provide the following functions:
- Supports configuration files for image resources and provides related configuration interfaces
- Convert images to device-optimized sizes and formats when packaging

Application developers only need to configure the packaging parameters of image resources according to their own needs, while device vendors need to define specific image conversion strategies for devices.

## Application development configuration

In application development, you need to configure image packaging parameters to correctly generate resource packages.
Configuring `config/image-rules.json` and `config.designWidth` of `src/menifest.json` during application development will affect the packaging behavior of image resources. `config/image-rules.json` is generally used to configure quality and performance parameters, while the fields in `menifest.json` affect the global scaling of the image (used to adapt to devices with different resolutions).

::: tip
`config/image-rules.json` can be configured using the `gx config` command or other methods, but it is not recommended to edit it directly with a text editor.
:::

If using the `gx config` command, developers will mainly focus on two parameters: transparent and quality.

### Transparent parameter

Transparent indicates whether the image contains transparent pixels. If it is configured as no (`false`) and the resource image contains transparent pixels, these pixels will be converted to opaque when generated (usually superimposed on a black background). Therefore, necessary images need to be marked as preserving transparent pixels, otherwise incorrect overlay effects will be displayed. Since opaque images perform better on some platforms and require less data, the transparent option is turned off by default.

### Quality parameters

The Quality parameter represents the quality of the packaged image and is an integer in the range of $[0, 100]$. However, generally only 3 rough quality levels are used:
- High: 100, indicating the highest quality
- Middle: 50, medium quality, default value
- Low: 0, low quality

When converting image resources, they will be optimized according to quality parameters. Generally speaking, medium quality is a conversion strategy that balances factors such as display effect, drawing/loading performance, and memory resource usage on the target platform, so it is recommended. Using high quality may have better quality, but may incur performance degradation. Low quality can be used for images where quality can be lost to improve performance (such as photos). Specific target platforms may also ignore the quality parameter and use a unified strategy.

## Device and platform adaptation

Assuming that device and platform developers have implemented optimized image resource formats for specific target platforms and support multiple qualities and pixel formats, the following work needs to be done in order to generate these image formats in glyphix.js:
- Command line tools required to achieve **single image** conversion
  - Must provide a command line interface for converting PNG images to custom formats, supporting output to a specified path (including overwriting the original file)
  - It is best to provide a command line interface for converting from a custom format to a PNG image, and support output to a specified path (including overwriting the original file). Without this function, PC break preview will not be possible.
- Write device description files and image conversion scripts

### Image conversion script

The image conversion script is a scheme file. When an image needs to be converted, glyphix.js will call this script. The latter can determine how to convert the image based on these variables:
- `env.image-path`: The absolute path of the image to be converted, the converted image is overwritten and written to this path
- `env.transparent`: the transparency parameter of this image
- `env.quailty`: the quality parameters of this image
- `env.target`: Convert target mode, see description below
- `env.verbose`: Whether to enable verbose mode, if so, detailed logs can be output, otherwise logs should not be output
- `env.script-dir`: The absolute path where the current script file is located. If the command required for conversion is relative to this script file and not in the `PATH` environment variable, you can use this parameter for splicing

`env.target` represents the **target mode** of image conversion, and its value determines which conversion method is applied:
- `"device"`: performs a complete conversion process for the target device, such as removing the transparent channel of the opaque image, and then converting it to PGF format (Glyphix picture format) according to the quality parameters
- `"emulator"`: Execute the conversion process for the simulator. Since the simulator does not support the texture format of specific hardware (such as ETC2, etc.), in order to ensure that the image is displayed normally in the simulator, you can only remove the transparent channel of the opaque image without further conversion to the target device format (or convert to the PGF format supported by the software)
- `"preprocess"`: Only perform the preprocessing step, that is, remove the transparent channel of the opaque image, and output the result in PNG format
- `"preview"`: To generate a PNG image for preview, you must first convert the image into a custom target format according to the conversion process of the `"device"` target, and then convert the output image back to PNG for preview use

::: tip
If the command line tool for image conversion does not support converting a custom format to PNG, then do not implement the `"preprocess"` and `"preview"` target modes.
:::

### image-forge command line tool

image-forge is a PGF image format command line tool provided by Glyphix and has the following functions:
- Supports converting PNG images to PGF format, and converting PGF to PNG images
- Supports common ARGB and PAL pixel formats, and distinguishes premultiplied alpha modes
- Supports blending transparent ARGB images onto a specified solid color background to convert them into opaque images (instead of directly discarding the alpha channel)
- Supports line alignment by pixels or bytes
- Supports LZ4 compression and can set the minimum compression threshold (image data below the threshold will not be compressed)

For platforms using other custom image formats, image-forge can also be used to remove the transparency channel.

## Image conversion script example

The following example demonstrates how to use commands such as image-forge to convert PNG to PGF images, using the color lookup table (PAL) format first.

First define the target format in the opaque and transparent cases:
``` scheme
; Define pixel format rules for opaque colors
(define (opaque-formats q)
  (cond ((<= q 50) "pal-rgb")
        (else "rgb24")))

; Define pixel format rules for transparent colors
(define (transparent-formats q)
  (cond ((<= q 50) "pal-argb-premul")
        (else "argb32-premul")))

; Calculate target pixel format under transparency and quality parameters
(define pixel-format
  ((if env.transparent
      transparent-formats opaque-formats)
    env.quailty))

; Whether the image is converted to color lookup table format
(define palette (<= env.quailty 50))
```

The above code will use the color lookup table format when the quality is 50 or less, and will use `pal-rgb` or `pal-argb` depending on whether it is transparent or not. Quality above 50 uses RGB or ARGB 8bit sampled pixel format. Finally, the `pixel-format` variable is the name of the actual pixel format used, and `palette` indicates whether to use the color lookup table format.

Next define the commands that need to be used in various situations:

``` scheme
; Whether to add the --verbose command line parameter
(define if-verbose (if env.verbose "--verbose " ""))

; Call the pngquant command to reduce the image color to less than 256 colors. pngquant needs to be installed in the system.
(define color-reduction
  (string-append "pngquant --ext=.png --force " if-verbose env.image-path))

; Convert image to PGF format
(define convert (string-append "image-forge "
  "--format=" pixel-format " " ; Specify the output pixel format
  "--compress --min-compress-ratio=5 " ; Compress image data to reduce file size, the minimum compression ratio is 5
  "--align=16 --pixel-align " ; Align the image to 16 pixels
  if-verbose
  env.image-path))

; Remove image alpha channel and add background
(define remove-alpha (string-append "image-forge --bypass "
  ; On bes2500ibp watches, non-transparent images can have their alpha channel removed and blended with a black background, which improves image quality after PAL color reduction
  (if env.transparent "" "--background black ")
  if-verbose
  env.image-path))

; Command to convert PGF image back to PNG
(define decode
  (string-append "image-forge --decode " if-verbose env.image-path))
```

In the following code, `execute-try` calls the specified `f` function after the command exits with a non-zero value. The `execute` function prints an error log and exits the script abnormally after the command exits with a non-zero value. The `run-convert` function performs the complete target device image conversion process (calling the `remove-alpha` and `convert` commands).

``` scheme
; Execute a command and print the command content in verbose mode, calling function f if the command exits with a non-zero exception
(define (execute-try cmd f)
  (begin
    (if env.verbose; If it is verbose mode, print the command content
      (display (string-append "Run command: " cmd "\n")))
    (let ((r (system (string-append env.script-dir "/bin/" cmd))))
      (if (= r 0) 0 (f r)))
  ))

; Execute a command and print the command content in verbose mode. If the command exits abnormally, the program will exit.
(define (execute cmd)
  (execute-try cmd (lambda (x)
    (begin; print error code and exit abnormally when failure occurs
      (display (string-append "subprocess failed (" (number->string x) "): " cmd "\n"))
      (exit-fail)
  ))))

;Convert image
(define (run-convert)
  (begin
    (execute remove-alpha) ; Remove the transparent channel first
    (if palette (execute color-reduction)) ; If it is a color lookup table format, reduce the number of pixels in the image
    (execute convert) ; Execute image conversion command
  ))
```

The `targets` macro defines the processing methods for all target modes. For example, the `"device"` mode will call the `run-convert` function, etc.

``` scheme
; Define the conversion strategy corresponding to the target
(targets env.target
  ; Device mode: the final image conversion process for the target device
  ("device" (run-convert))
  ; Simulator mode: only remove the alpha channel of non-transparent images, without converting the format
  ("emulator" (execute remove-alpha))
  ; Preprocessing mode: remove the alpha channel of non-transparent images and add a background
  ("preprocess" (execute remove-alpha))
  ; Preview mode: generate a PNG preview image that is consistent with the display effect of the actual device
  ("preview" (begin
    (run-convert) ; First convert the image to PGF format
    (execute decode))) ; Convert the image back to PNG
  )
```

### Use image conversion script

To use the image conversion script, you need to add a field to the device model description file:

```yaml
description: default watch

screen:
  width: 454 # pixels
  height: 454 #pixels
  dpi: 326 # pixels per inch

# ...
image-build: image-convert-pal.scm # The path of the image conversion script relative to this Yaml file
```

### More complex strategies

Since the image conversion script is a complete programming language rather than configuration languages ​​such as Yaml and JSON, we can implement more complex custom conversion strategies without being limited by the functions provided by the framework. Take the above color lookup table format conversion as an example: PAL format does not work well on pictures with rich colors. At this time, the picture can be converted to a format that performs better in such scenes. The specific ideas are:
1. The `pngquant` command supports exiting abnormally if the quality after conversion to PAL format is lower than the specified value, so configure the command parameters according to this purpose
2. In the `run-convert` function, the `color-reduction` operation performed by `execute` is changed to be performed by `execute-try`, and the alternative format conversion operation is used in the latter's exception handling function.
3. Targets such as `preview` are processed in a similar manner, but please note that when converting the output format to PNG, you also need to recognize that the command exits abnormally and continue trying with subsequent commands.

All in all, it is similar to the idea of ​​​​a shell script, using the abnormal exit code of the command to control the process.

============================================================
FILE_PATH: src/transl/EN/tutorials/glyphix.js/cli.md

---
icon: console-line
---
# Command line options

To be migrated.

============================================================
FILE_PATH: src/transl/EN/tutorials/glyphix.js/emulator.md

---
icon: watch-import-variant
---
# Simulator and debugging

To run the emulator, you need to switch to the root directory of your project on the command line and run the `gx emu` subcommand to start the emulator. The Glyphix simulator has a highly consistent environment with the real device runtime, so you can use the simulator to develop and debug most interfaces and functions without the need to frequently install applications on the real device.

::: tip
Due to the limitations of the current [`glyphix`](https://www.npmjs.com/package/glyphix) npm package, please be sure to configure [`glyphix.config.js`](/doc_en/nodejs.md#glyphix-config-js-configuration), otherwise the source code line number of the error message cannot be seen when executing `gx emu`.
:::

## `gx emu` subcommand

Run the emulator using the last build target device configuration. This command needs to be executed in the root directory of the Glyphix project. It automatically builds the project and creates the resource files required by the emulator, so there is no need to perform `gx build` first.

#### Command options

- `-d --device=NAME`: Specify the simulated device name, the default is `default` (resolution is $410 \times 502\rm px$).
- `-e --emulator-exe=CMD`: Specify the executable file of the emulator, the default is `glyphix-emu`. Usually no modification is required.
- `-l --language=NAME`: Specify the language environment of the simulator, the default is `zh-CN` (Simplified Chinese). The list of supported languages ​​can be viewed through the `gx list language` command.
- `--target=URI`: Set the package name or deeplink when the emulator is started, such as `app://com.example.app/SomePage?query=value` or `com.example.app`.
- `-i --inspector`: Enables the inspector when running the simulator. The inspector is a web page that can debug interface elements in the simulator in the browser.
- `-m --mobile-network`: (not yet implemented) Enable the mobile SDK's network proxy only in the emulator, without direct access to the network.
- `-w --watch`: Monitor the project directory when running the simulator, and automatically rebuild and refresh the simulator interface when the source files change.
- `-r --real-scale`: Display the emulator window using real size instead of scaling the display to the device resolution. This option is recommended for HiDPI screens.
- `-t --top`: Keep the emulator window on top.
- `-p --profiling`: Enable profiling mode. Due to the large differences in emulator and device performance, this option is generally not very useful.

## Startup mode

By default, `gx emu` will start the emulator with the device configuration it was last built with. You can also adjust the emulator's startup behavior through command options.

### Specify device model

Use the `-d` or `--device` option to specify the device model you wish to emulate, for example:
```bash
gx emu -d generic-watch-466x466
```
Will start the emulator for the device `generic-watch-466x466`. You can view the list of installed devices using the `gx list device` command.

If this option is not specified, the last device specified will be used. The `default` device will be used when starting the emulator for the first time or after `gx clean`.

### Deeplink startup

By default, the simulator will launch the application of the current project, or launch an application menu interface. But when debugging the [`onRoute()`](/framework/component/life-cycle.md#onroute) lifecycle function, you may want to launch the application through a deeplink to ensure that `onRoute()` receives specific parameters. Deeplinks can be specified using the `--target` option, for example:
```bash
gx emu --target app://com.example.app/SomePage?query=value
```
This will start the application with the package name `com.example.app`, and the path and query fields of the Deeplink URI will be passed to the `onRoute()` function of the application.

### Analog device size

By default, the simulator uses the actual pixel resolution of the device, which causes the display size on the computer to be larger than the actual screen size of the device and makes it difficult for developers to confirm that UI elements (including design drafts) are sized optimally on the device. The `-r` or `--real-scale` option can simulate real device dimensions:
```bash
gx emu -r
```
When using this option, you don't need to install the app on the device to confirm the actual size of the UI. However, considering that the DPI of most watches exceeds 300, a 1080p display will cause the interface to be too blurry when using real-scale mode. It is recommended to use this option on HiDPI displays (such as 4K displays, or Retina screens on macOS).

::: tip
When using real-scale mode, you should specify the target device you wish to emulate via the `--device` option. It is worth noting that due to different DPI, two devices with the same resolution may have different screen sizes, so the display sizes in real-scale mode will also be different.
:::

### Automatic refresh

The `-w` or `--watch` option can monitor the project directory when running the simulator and automatically rebuild and restart the application when the source files change. It is usually recommended to use it with the `--top` option, for example:
```bash
gx emu -wt
```
This keeps the simulator window on top and automatically restarts the application after modifying the source file. This is very useful for development and debugging: switch directly from the code editor to the simulator, no need to manually restart the simulator, and no need to switch windows frequently.

::: tip
Currently, hot update pages are not supported. Instead, the entire application is restarted after modifying the source file. If you want faster debugging, you can adjust [`manifest.router.entry`](/framework/application/manifest.md#entry) to the page under development, so that you will go directly to the page every time you restart the application.
:::

## Connect to mobile phone

You can connect to the emulator through the [Glyphix Debug](https://www.pgyer.com/KLeBQFv6) Android mobile application to facilitate debugging functions related to the real device and mobile phone interconnection.

### Preparation

You need to install the Glyphix Debug app on your phone and make sure your phone and computer are on the same LAN, such as connected to the same Wi-Fi. After starting the simulator and opening the Glyphix Debug application, click the "Socket Connection" button. The application will display a connection interface. You can select the searched simulator IP address, or manually enter the computer IP and simulator port to connect.

The emulator listens to network port 7768 by default. If the port is occupied (usually multiple emulators are started), the next available port is automatically selected and the actual port number used is printed when starting. For example:
```bash
$ gx emu
[simulator.socket] MAS TCP server bind port 7768 successful
```

::: tip
Once the emulator port is occupied and a non-7768 port number is selected, the Glyphix Debug application will not be able to automatically search for the emulator and must manually enter the correct IP address and port number to connect.
:::

It is strongly recommended that the simulator turns on the mobile network proxy mode in the next section to avoid using the computer network and mobile network at the same time. Otherwise, it may interfere with the normal work of [`@system.interconnect`](/api/system-interconnect.md) and other dependent mobile phone interconnection APIs.

### Mobile network proxy

Use the `-m` or `--mobile-network` option to enable only the network proxy function of the mobile SDK, which is similar to the network environment of a real device. When using this option, the emulator does not automatically launch the target application, but displays an application list interface.

Before manually launching the app, you should connect to the emulator via "Socket Network" via the Glyphix Debug mobile app and then click on the target app. Otherwise the application will not be able to access the network.

::: tip
When using `-m` mobile network proxy, you can simulate network interruption by killing the mobile debugging application and reconnecting the emulator. Otherwise the simulator will automatically switch to the computer network.
:::

### Common connection issues

If you cannot connect to the emulator through the Glyphix Debug app, please check whether the computer and mobile phone are connected to the same LAN, and the emulator program and port are not blocked by firewall rules. If you are connected to a public network, you may not be able to connect due to a firewall or network isolation.

If you use VPN or proxy software, please ensure that the traffic within the LAN is not proxied, otherwise you will not be able to connect.

## Other operations

### Clear application data

You can use [`gx clean`](README.md#gx-clean) to clear the application data when the emulator is running. Then when you start the emulator, it will start from the state of first installation.

### Combine command options

You can combine multiple options together, for example:
```bash
gx emu -rwt -d default-watch-466x466
```
Equivalent to using separately
```bash
gx emu -r -w -t -d devault-watch-466x466
gx emu --real-scale --watch --top --device default-watch-466x466
```
It is recommended to install an auto-completion script as described in [`gx completion`](#gx-completion) to select device names and command options in the terminal.

============================================================
FILE_PATH: src/transl/EN/tutorials/glyphix.js/README.md

---
icon: package-variant-closed
---
# Glyphix.js packaging tool

glyphix.js is a packaging tool for Glyphix applications. It contains a command line tool called `gx` that can be used to create, build and run Glyphix applications. The tool also includes a graphical simulator that can simulate running Glyphix applications on your computer.

This document provides installation and usage instructions for glyphix.js, and the [Quick Start](/doc_en/getting-started.md) tutorial is a simpler getting started guide. Also read [Build and Run](#buildandrun) to learn how to develop, build, and publish a Glyphix application.

## Install

This section introduces how to install the glyphix.js packaging tool. For general use, just know the [npm install](#npm-install) method. [Manual installation](#manual-installation) method is suitable for special scenarios, such as network-limited environments, CI builds, etc.

### npm installation

You can use the [npm](https://nodejs.org) package manager to install the glyphix.js packaging tool. It is recommended to use the `-g` option for global installation:
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
Before using pnpm to install globally, you may need to execute `pnpm setup` to configure environment variables. The `pnpm install -g` command will prompt how to configure environment variables.
:::

After the installation is complete, you can execute `gx --version` in the terminal to check whether the installation is successful. For example:
```bash
$ npm install -g glyphix-cli
$ gx --version
gx v0.10.1 - The Glyphix applet development toolchain
commit a9337cf1 - Tue Sep 23 10:03:48 2025 +0800
```

Additionally, [pngquant](#pngquant) must be installed to package app resources for some devices.

### Manual installation

You can also install it manually from the compressed package of the glyphix.js packaging tool: add the `bin` directory in the unzipped directory to the `PATH` environment variable. The following will introduce the installation methods on mainstream operating systems.

::: tip
The glyphix.js tool is not just an executable file, do not leave out other resource files (including all files in the `bin` and `share` directories).
:::

#### macOS/Linux

For macOS or Linux, you can use the `tar` command to install the glyphix.js packaging tool. Before that, you also need to install tools such as `xz`:

::: code-tabs
@tab macOS
```bash
brew install xz
```

@tab Ubuntu/Debian
```bash
sudo apt update
sudo apt install xz-utils
```

@tab Arch Linux
```bash
sudo pacman -S xz
```
:::

After downloading the compressed package of glyphix.js, use the following commands to decompress and install:
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
Please be careful to replace the `.tar.xz` file name with the actual downloaded file name that corresponds to your operating system and CPU architecture. After decompression, commands such as `gx` will be located in the `~/.local/bin` directory. Please add this directory to the `PATH` environment variable, for example, update `.bashrc` like this:
```bash
# If ~/.local/bin is not in PATH, add
echo "$PATH" | grep -q "$HOME/.local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc # Reload bash configuration
```

::: tip
When using `Zsh`, the `.zshrc` configuration file may import `.bashrc`, so only `.bashrc` needs to be updated. Otherwise, please update `.zshrc` as above.

It is recommended to install the glyphix.js packaging tool in the user's `~/.local` directory to avoid using root privileges for installation.
:::

#### Windows

To install glyphix.js on Windows, please download the corresponding Windows version compressed package, and then use an decompression tool that supports `7z` format (such as [7-Zip](https://www.7-zip.org/)) to extract it to a directory, such as `C:\glyphix`. Then add `C:\glyphix\bin` to the system's [`PATH` environment variable](https://learn.microsoft.com/zh-cn/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)).

You can also use the `7z` command line tool to decompress, for example:
```shell
7z x -y glyphix-v0.7.2-windows-x64.7z -oC:/glyphix
```
This is similar to the installation method for systems such as macOS.

### Install system dependencies

#### pngquant

Linux and macOS users need to install `pngquant` additionally, you can use `npm` to install it:
```bash
npm install -g pngquant-bin # pngquant-bin only supports installation with npm
```
The Windows `glyphi-cli` includes `pngquant.exe`, so no additional installation is required.

::: tip
You can also download precompiled binaries from [pngquant.org](https://pngquant.org/) or install from your system's package manager.
:::

#### Linux system dependencies

The Linux installation package of glyphix.js does not distinguish between specific distribution versions. Currently, there are only build packages for the linux-x86_64 architecture. We tested it running on Ubuntu 20.04 (or newer) and Arch Linux.

If you just use the `gx` command for packaging (which is commonly used for CI packaging), Linux distributions without a desktop environment should work out of the box. Running the graphical simulator relies on the X Window System, so you may need to install xorg-related software packages, especially for Wayland environments. You also need to install the `xwayland` software package (the simulator does not yet support native Wayland).

### uninstall

For glyphix.js installed globally through a package manager such as npm, you can use the corresponding package manager to uninstall, for example:
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
For non-global installation using a package manager such as npm, just remove the `glyphix-cli` dependency in `package.json` and execute `npm install` (or `pnpm install`, `yarn install`) to update the `node_modules` directory.
:::

For manual installation, just delete the files in the installation compressed package, such as the `tar.xz` installation file for macOS and Linux:
```bash
tar -tf glyphix-v0.7.2-darwin-arm64.tar.xz > filelist.txt
cat filelist.txt # Check the file list to be deleted
xargs -I {} rm -f "~/.local/{}" < filelist.txt # Execute deletion after confirmation
```
The `tar -tf` command will list the files in the compressed package, and `glyphix-xxx.tar.xz` should be replaced with the actual installation file. Manual uninstallation on Windows is similar.

## Build and run

After installing glyphix.js, use the [`gx build`](#gx-build) command in the root directory of the app source code to build the app package, or use the [`gx emu`](#gx-emu) command to run the emulator.

After building the application, please refer to the [Submit Application Package](#submit-application-package) chapter to learn how to install the application on the device or submit it to the application publishing platform.

## Command line parameters

### General options

#### `gx --help`

View help information. Help information can also be used in specific subcommands. For example, use `gx build --help` to view the help information of the `build` subcommand separately.

#### `gx --version`

The `-V --version` option is used to view the version number of the `gx` command.

#### `gx --verbose`

`-v --verbose` enables verbose logging output, which application developers generally do not need to use.

#### `gx --numeric-version`

Output the purely numeric version number of the `gx` command, for example `0.10.1`.

#### `gx --quiet`

`-q --quiet` enables quiet mode and suppresses most non-warning and error log output. This includes build progress logs when using `gx build`, a mode commonly used in CI environments where a large number of application packages need to be built.

View the version number.

### `gx new`

Creating a new project, for example `gx new myapp` will create a new project named `myapp`.

### `gx build`

Build the project (default action), use the `--device` or `-d` option to specify the target device, e.g.
```bash
gx build -d default # Specify the default device build
```
Use the `--dump` option to print compilation details of the UX file.

Glyphix.js supports incremental builds. When the source code changes, only the changed parts will be rebuilt.

The `-r --image-rules` parameter can specify the image packaging rule file, the default is `config/image-rules.json`. The value of this parameter will be cached, and subsequent executions of `gx build` or `gx emu` will be executed according to the previous configuration.

#### Command options

- `-d --device=NAME`: Specify the target device name, which must be the installed device configuration name. You can view the list of installed devices using the `gx list device` command. If this option is not specified, the `default` device is used by default.
- `-f --full`: Force a complete rebuild of the project instead of an incremental build.
- `-e --emulator`: Build the project for the emulator instead of the actual device. This option is automatically used when executing the `gx emu` command.
- `-r --image-rules=PATH`: Specify the image packaging rule file, the default is `config/image-rules.json`.

#### Submit application package

After building with `gx build`, the `.glyphix-work/dist/<device-name>/<package-name>` directory will be generated in the project directory, which contains the built application package file (`.pkg` file). This file can be installed and run on the device through the mobile phone debugging application, or it can be submitted to the application publishing platform.

Application packages should be built separately for all devices that need support using the `-d` option. Here is an example directory structure:
```bash
.glyphix-work/dist
├─ generic-watch-368x448
│ └─ com.example.app
│ ├─ bundle.pkg
│ ├─ icon.png
│ └─ manifest.json
└─ generic-watch-466x466
   └─ com.example.app
      ├─ bundle.pkg
      ├─ icon.png
      └─ manifest.json
```
When submitting an application package, please package and upload the entire `.glyphix-work/dist` directory instead of just uploading the `.pkg` file or any subdirectory. The platform identifies the app based on information in the `manifest.json` file and may require `icon.png` as a preview icon.

::: tip
For Linux or macOS users, you can use this command to package applications for certain types of devices:
```bash
gx list device | grep "^generic-" | xargs -n 1 gx build -d
```
This will build app packages for all devices whose names start with `generic-`.

You can also use similar PoweShell commands to build in batches under Windows:
```shell
gx list device | ? { $_ -match "^generic-" } | % { gx build -d $_ }
```
:::

### `gx emu`

Meet the [Emulator and Debugging](/doc_en/glyphix.js/emulator.md) documentation.

### `gx clean`

Clean the build product. This command will delete the `.glyphix-work` directory under the project folder.

### `gx config`

This command starts a web interface for editing image packaging rule files. Follow the command prompts to open the page in the browser for operation. This command has two uses:
```bash
gx config # When in a Glyphix project, there is no need to specify the source directory (currently it can only be used in the project root directory)
gx config path/to/dir # Configure the specified directory, which can be used to configure non-project image resources
```

The `-r --image-rules` parameter can specify the image packaging rule file, the default is `config/image-rules.json`.

### `gx image-forge`

Convert free image files. This command can specify any source path and output path, and does not need to be executed in the Glyphix project:
```bash
gx image-forge src -o dist
```

Option description:
- `src` is the source path to be converted. The `image-forge` command recursively converts all images and generates them according to the relative directory structure to the target path specified by `-o, --output` (default is `dist`).
- The `-r --image-rules` parameter can specify the image packaging rule file, the default is `config/image-rules.json`.
- `-d --device` specifies the target device for image conversion.

### `gx list`

List some information. Currently three operations are supported:
```bash
gx list device # List all installed device configurations
gx list template # List all installed project templates
gx list image # List the relative paths of all image resources in the current directory (similar to the find command)
```

Some information can use `-d, --detailed` to list detailed description text, for example:
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

This command is used to generate a shell auto-completion script for the `gx` command. It currently supports [Zsh](https://www.zsh.org/) and [PowerShell 7+](https://github.com/PowerShell/PowerShell). Using `gx completion [SHELL]` will output the auto-completion script for the specified shell (when the `SHELL` parameter is not specified, the current shell will be detected). If you want to install a completion script, use:
```bash
gx completion --install
```
After the installation is successful, you will be prompted for the installation path of the command completion script. You can use automatic completion by restarting the shell session, or you can use these commands to take effect immediately:
::: code-tabs
@tab Oh My Zsh
```bash
omz reload
```

@tab PowerShell
```shell
Import-Module glyphix-Force
```
:::

When using the auto-completion script, you can select the device, command line options, etc. of `gx emu` in the terminal without manual input.

PowerShell uses loop completion by default. It is recommended to change to the completion menu:
```shell
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
```
Add this command to the [`$PROFILE`](https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/creating-profiles#adding-customizations-to-your-profile) profile to make it permanent.

::: note
If the `--install` option cannot be installed automatically, you can also use the `gx completion` command to manually install the completion script, for example:
```shell
gx completion zsh > ~/.zsh/completion/_gx.zsh
```
:::

## Default configuration path

Configuration, project templates, device information and other information in the glyphix.js tool can be stored in the following path:
- System-level configuration: `share/glyphix` directory relative to the directory above the `gx`/`gx.exe` executable file. Suppose, for example, that the path of the `gx` executable file is in `/usr/local/glyphix`, then the resource path of the system-level configuration configuration is `/usr/local/share/glyphix`
- User-level configuration: `~/.local/share/glyphix` on Unix-like systems, `%APPDATA%\AppData\Roaming\glyphix` on Windows

The configuration file can be stored in one of the above paths, where user-level configuration has higher priority. `gx.js` will come with a default configuration file when installed.

## Project template

Project templates are stored in the `templates` directory of the configuration path. Currently, only the `simple` template is supported and customization is not supported.

## Device configuration file

Device configuration files are stored in the `devices` directory of the configuration path. Each device has a YAML configuration file, and the name of the configuration file is `<device-name>.yml`. The format of the configuration file is described as follows:

```yaml
# file: default.yml
description:
  Device description information for developers to view.

screen: # Fields describing the device screen configuration, these fields are required (will affect UI layout and resource scaling)
  width: 454 # Number of horizontal pixels on the screen
  height: 454 # Number of vertical pixels on the screen
  dpi: 326 # The pixel density of the screen, in pixels/inch

ui: # Global interface configuration, all optional fields
  font-family: sans-serif # System default font family name (default is serif)
  font-size: 3.5 # The system default font size, the unit is points (pt, points), note not pixels! !
  font-map: true # Whether to use the global font configuration mapping file, if so, it must exist in the system resources
                 # font-faces.css file

# Optional system global resource package path, the following configuration means that the global resource package is stored at the same level as default.yml
# Under the default-global folder. The global resource package contains preset fonts and font configuration mapping files in the system.
global-assets: default-global

# Optional image conversion script, the script file path is stored relative to the current device description file. If you do not specify image conversion
# When the script is packaged, it will output the original PNG material, but resolution scaling will be applied.
image-build: image-convert.scm

# The command to run the emulator will execute glyphix-emu by default. The executable file for the emulator command must be in PATH
# The path of the environment variable, otherwise it will not be executed.
emulator: glyphix-emu
```

============================================================
FILE_PATH: src/transl/EN/cookbook/layout-tricks.md

# Layout tips


## Limit element width


You can use the `margin` attribute to limit the width of an element.


<glyphix id="cookbook-margin-layout-1" width="360" height="100">



```html
<div>
  <div class="limit">
    <p>{{text}}</p>
  </div>
</div>
```


```css
div {
  background-color: lightgreen;
}

.limit {
  border: 1px solid red;
  margin: 0 150px;
  display: flex;
  justify-content: flex-start;
}

p {
  border: 1px solid gray;
  margin: 2px;
}
```


```js
export default {
  data: { text: 'A' },
  onInit() {
    let index = 1
    setInterval(() => {
      this.text += String.fromCharCode(index++ + 0x41)
      if (index > 26) {
        this.text = 'A'
        index = 1
      }
    }, 200)
  }
}
```


</glyphix>


============================================================
FILE_PATH: src/transl/EN/cookbook/swiper-indicator.md

# Swiper page indicator


<Glyphix id="cookbook-swiper-indicator" height="466" width="466" designWidth="466" title="Swiper 指示器">


``` html
<stack>
  <swiper ::index="index">
    <p for="i in panels">Panel {{i + 1}}</p>
  </swiper>
  <div class="indicator">
    <image for="x in indicator" :src="x" />
  </div>
</stack>
```


``` js
export default {
  data: {
    panels: 5,
    index: 2
  },
  computed: {
    indicator() {
      let result = []
      for (let i = 0; i < this.panels; i++) {
        let suffix = i == this.index ? '1' : '0'
        result.push(`/assets/images/ind-${suffix}.png`)
      }
      return result
    }
  }
}
```


``` css
swiper > p {
  background-color: #888;
  margin: 32px;
  border-radius: 32px;
  text-align: center;
}

.indicator {
  display: flex;
  justify-content: center;
  align-items: flex-end;
}

.indicator > * {
  margin: 0 4px 56px 4px;
}
```


</Glyphix>


============================================================
FILE_PATH: src/transl/EN/cookbook/game-2048.md

# 2048 game


## Effect display


Tip: Use the mouse to quickly slide up, down, left, and right to operate in "2048 Game".


<glyphix id="cookbook-game-2048" height="466" width="466" title="2048 游戏" inline>


</glyphix>


============================================================
FILE_PATH: src/transl/EN/cookbook/async.md

# Asynchronous operations


The main purpose of introducing asynchronous operations in JavaScript scripts is to execute time-consuming work in the background to avoid JavaScript thread blocking. The work placed in the background for processing is mainly IO-intensive operations. Glyphix provides a basic JavaScript asynchronous framework for developers to use, which only makes necessary abstractions for asynchronous workflows, so it does not introduce additional overhead.


## Applicable scenarios


Applicable scenarios for asynchronous workflow models


- The request is initiated by JavaScript code, and the result is returned after processing by the native asynchronous processing thread;
- The request is initiated by JavaScript code, and the native asynchronous processing thread reports the message regularly after processing;
  - JavaScript code can proactively ask for revocation/cancellation requests.


## Data request pattern


In the data request pattern, JavaScript code calls a C++ API to create a request and returns the result to the JavaScript code after performing the operation in an asynchronous thread. In this process, data will be transmitted through an asynchronous queue. The `async::ResultSession` template class provides a general operation framework for this mode.


### Scene description


The following scenarios are typical data request patterns:


- **File reading and writing**: When JavaScript initiates a call, you need to specify the path of the file, the offset position of the file to be read and written, the data length, or the data to be written; when the request is sent to the asynchronous thread for execution, the actual file read and write operation will be performed, and after the operation is completed, the result will be notified or returned to the JavaScript code.
- **Network Request**: Similar to file reading and writing, request parameters must be specified when JavaScript initiates a call, and then the background thread processes and returns the result.


The scenario of data request mode has the following characteristics:
- The result returned by the request is a single time, so sensors or timer monitoring that may be triggered multiple times are not suitable for this mode;
- The request always has a result: if the request is successful, the result is returned, otherwise an error message is returned, and the result is returned asynchronously;
- Once a request is made it cannot be revoked.


### Example: Obtaining power value


#### JavaScript API


Suppose you want to implement an asynchronous JavaScript function to get the battery level:
``` ts
getLevel(): Promise<number> // Promise style API
getLevel(options: { // Callback style API
    success: (level: number) => void,
    fail: (code: number, msg: string) => void // Battery level reading does not actually fail
}): void
```
Use the `getLevel()` function to obtain the battery level asynchronously, which provides two API styles: `Promise` style and callback style. The code for these two styles is as follows:
``` js
async function printBatteryLevel() {
    const level = await getLevel() // Get battery value asynchronously
    console.log(`battery level: ${level}%`)
}
printBatteryLevel() // Print the power value, console output example:
// battery level: 59%

// The following is callback style code, which is not recommended:
getLevel({
    success(level) { console.log(`battery level: ${level}%`) }
})
```


#### C++ native interface export


The `getLevel()` function in JavaScript is actually implemented in C++. When the JavaScript code calls this function, it will initiate an asynchronous request to obtain the battery power, and after getting the result, the result value will be returned to the JavaScript code through the callback function or `Promise`. The C++ function that implements `getLevel()` is as follows:
``` cpp
static JsValue getLevel(const JsCallContext &ctx) {
    typedef async::ResultSession<BatteryGetLevel> Session;
    Session *session = new Session; // Create Session object
    session->request(ctx.argc() ? ctx.arg(0) : JsValue());
    return session->promise();
}
```


The template class `async::ResultSession` (the `async` namespace is omitted below) implements the framework required for asynchronous data requests. Each asynchronous data request includes the following steps:
1. Create a `ResultSession` object
2. Call the `ResultSession::request()` method to initiate a request
3. Use `ResultSession::promise()` to return the `Promise` object to JavaScript.


this line of code
``` cpp
session->request(ctx.argc() ? ctx.arg(0) : JsValue());
```
In addition to initiating the request, we also pass the $0$th parameter passed in by the JavaScript caller to the `ResultSession::request()` method. `ResultSession` will automatically select the callback and `Promise` style based on whether the parameter exists `success` / `fail` and other callback functions. If it is `Promise` style, then
``` cpp
return session->promise();
```
A `Promise` object will be returned to obtain the result of the asynchronous request, otherwise `undefined` will be returned and the callback function will handle the result.


#### `ResultSession` template class


The declaration of `ResultSession` template class is as follows:
``` cpp
template<class T, class H = ResultHandler> class ResultSession;
```
The template parameter `T` is a class that implements specific asynchronous operations. This example will implement a `BatteryGetLevel` class to achieve asynchronous acquisition of battery power. The template parameter `H` determines how to handle the results of asynchronous requests. The default `ResultHandler` will automatically select the callback or `Promise` style, and developers generally do not need to modify it.


#### `BatteryGetLevel` class


The `BatteryGetLevel` class is defined as follows:
``` cpp
struct BatteryGetLevel {
    async::Result<int> resolve() const {
        return battery_read_level(); // Get battery level
    }
    // errorMessage() is used to translate error codes into text. However, the power reading will not go wrong and can be implemented at will.
    static const char *errorMessage(Status) {
        return "get battery level failed";
    }
};
```
As you can see, `BatteryGetLevel` has two member functions. The `resolve()` function is used to perform specific operations in an asynchronous thread. The return value of a `resolve()` function must be of type `async::Result<T>`, in this case `async::Result<int>`.


The `resolve()` function's return value `async::Result<T>`'s template parameter `T` type is consistent with the JavaScript API's callback function parameter or `Promise` data type. For example, in this example, `int` corresponds to the JavaScript API's
``` ts
// C++ BatteryGetLevel::resolve() function return value type
// async::Result <int> corresponds to JavaScript's Promise <number>
getLevel(): Promise<number>
```


In other words, if `resolve()` returns the `async::Result<String>` value, then it will return `Promise<string>` in JavaScript, which is `{ success(value: string): void }` for the callback function. Please refer to [数据类型转换](#数据类型转换) for details on conversion between C++ and JavaScript data types.


### Example: file reading


#### JavaScript API


Suppose you want to implement an asynchronous JavaScript function for file reading:
``` ts
readfile(url:string): Promise<string> // Promise style API
readFile(option: {   // Callback style API
  uri: string,
  success?: (data: string) => void,
  fail?: (code: number, msg: string) => void,
}): void
```
This function will read the content of the file asynchronously and return it through the `Promise` object. The return value is the file content. The actual JavaScript code looks like this;
``` js
async function printReadFile() {
    const data = await readFile("file.txt") // Get battery value asynchronously
    console.log('File read successfully:', data)
}

printReadFile() // Print the file contents as a string, console output example:
// File read successfully: hello

// Below is the callback style code
readFile({
    url: "file.txt",
    success: (data: string) => {
        console.log('File read successfully:', data);
    }
})
```


#### C++ native interface export


The `readFile()` function in JavaScript is actually implemented in C++. When the JavaScript code calls this function, it will initiate an asynchronous request to read the file, and after getting the result, the result value will be returned to the JavaScript code through the callback function or `Promise`. The C++ function that implements `readFile()` is as follows:
``` cpp
JsValue readFile(const JsCallContext &ctx) {
    typedef async::ResultSession<ReadFileRequest> Session;
    if (ctx.argc() > 0 && ctx.arg(0).isObject()) {
        Session *session = new Session;
        // Convert JavaScript function parameter url field to C++ String
        session->client().url = ctx.arg(0)["url"].toString();
        session->request(ctx.argc() ? ctx.arg(0) : JsValue());
        return JsValue();
    }
}
```
For explanation of the template class used, refer to [resultsession-模板类](#resultsession-模板类) and for code explanation, refer to [c-原生接口导出](#c-原生接口导出) for obtaining the electric power value.


#### readFile class


The `ReadFileRequest` class is defined as follows:
``` cpp
struct ReadFileRequest {
    String url; // The url of the file to be read.
    Result<String> resolve() {
        ByteArray array = File::read(url); // Read file content via url
        return String(array.charData(), array.size());
    }
    // errorMessage() is used to translate error codes into text
    const char *errorMessage(Status) { return "read file error"; }
};
```
As you can see, `ReadFileRequest` has two member functions. The `resolve()` function is used to perform specific operations in an asynchronous thread. The return value of a `resolve()` function must be of type `async::Result<T>`, in this case `async::Result<String>`. It should be noted that the `resolve()` function cannot process data types in JavaScript. The url is an asynchronous request that is converted to the C++ String type in the `readFile()` function. Similar data conversion cannot be processed in the `resolve()` function.


## Listen mode


In the listening mode, the JavaScript code calls the C++ API to create a request. For multiple asynchronous requests such as monitoring of sensor data, an asynchronous event will be executed when the data changes and the results will be returned to JavaScript. The `async::ListenSession` and `async::Signal` template classes provide a common operation framework for this mode.


### Scene description


The following scenarios are typical monitoring modes:


- **Monitoring of various sensors**: Initiated by JavaScript, calling the C++ API for monitoring the corresponding sensor requires specifying a callback function. When the sensor reads data and sends changes, the new data will be returned to the JavaScript code through the asynchronous thread as a formal parameter of the callback function.
- **Periodic scheduled tasks**: When JavaScript initiates a call, you need to set the time of the scheduled task, the callback function after the task times out, and whether it is periodic; when each timed task times out after sending a request, the asynchronous thread will return the result to JavaScript, triggering the callback function set by JavaScript.


The monitoring mode scenario has the following characteristics:
- After the monitoring is started, multiple asynchronous requests are supported, so asynchronous events for a single file read and write and network status request may not be applicable;
- After starting the monitoring, you must cancel the monitoring when not in use, otherwise it will cause a memory leak.


### Example: Monitor battery power value


#### JavaScript API


If you want to implement an asynchronous JavaScript function that monitors battery power:
``` ts
subscribe(callback: (Level: number) => void): number // Monitor battery power level
unsubscribe(subscribeID: number): void // Cancel monitoring
```


Use the `subscribe()` function to asynchronously monitor the battery power value and the `unsubscribe()` function to cancel monitoring. The usage examples are as follows:
``` js
// Start monitoring and return an id to cancel monitoring.
let id = subscribe(level => {
  // If the battery power value changes, the listening callback function will be triggered. Example of console printing:
  // now battery level: 59
  console.log(`now battery level: ${level}%`)
})

unsubscribe(id); // Cancel monitoring
```


#### C++ listening interface export


The `subscribe()` function in JavaScript is actually implemented in C++. When the JavaScript code calls this function, it will monitor the battery power value. Whenever the power value changes, an asynchronous request will be initiated and the result value will be returned to the JavaScript code through the callback function. The C++ function that implements `subscribe()` is as follows:
``` cpp
async::Signal<int> Level; // Create a global object Level

level(45); // The Level value changes and an asynchronous request is sent.

static JsValue subscribe(const JsCallContext &ctx) {
    Applet *applet = Applet::current(&ctx.vm());
    if (applet && ctx.argc())  // Check whether the parameters passed in
        return applet->bindObject(Level.connect(ctx.arg(0)));
    return JsValue();
}
```
A global object `Level` must be created. The template class `sync::Signal` used (the `async` namespace is omitted below) implements the framework for monitoring requests. Monitoring requests includes the following steps:
1. Before listening, an object of the global `Siganal` class must be created;
2. Use the `Signal::connect()` method to associate the first parameter passed in by JavaScript with `Level`;
3. Call `Applet::bindObject` to bind the `Level` object; when the state of `Level` changes, call the callback function and return the result to JavaScript code.


this line of code
```cpp
level(45);
```
The value of `Level` changes to $45$, triggering the listening mechanism and will initiate an asynchronous request. The changed value is used as the formal parameter of the callback function, and finally the result is returned to the JavaScript code.


#### C++ Cancel export of listening interface


The `unsubscribe()` function in JavaScript is also implemented in C++. When the JavaScript code calls this function, the listening function is cancelled. Avoid memory leaks caused when not using listeners. The C++ function that implements `unsubscribe()` is as follows:
``` cpp
static JsValue unsubscribe(const JsCallContext &ctx) {
    Applet *applet = Applet::current(&ctx.vm());
    if (applet && ctx.argc() >= 1 && ctx.arg(0).isNumber()) // Check whether the passed parameters are correct
        delete applet->unbindObject<async::Slot>(ctx.arg(0).toInt());
    return JsValue();
}
```
To cancel the listening request, you need to call `Applet::unbindObject` to unbind, and you need to pass in the return ID of the `subscribe()` function to determine the unbound object.


#### `Signal` template class


``` cpp
template<class T, class H = ListenHandler> class Signal;
```
Template parameter T is a class that implements specific asynchronous operations. This example shows a `int` type to monitor battery power. Template parameter H determines how to handle the results of asynchronous requests. The default ResultHandler will automatically choose callback or Promise style, and developers generally do not need to modify it.


## Data type conversion


In `ResultSession` or `ListenSession`, the data of asynchronous operations must be converted into `JsValue` objects before they can be used in JavaScript code. For example, [BatteryGetLevel](#batterygetlevel-类) defines
``` cpp
async::Result<int> BatteryGetLevel::resolve() const;
```
Function, this function declaration means that the return data type of the battery power request is `int`, which can be converted to `JsValue`. In fact, the following types can be converted to `JsValue`:
- `bool`: converted to `boolean` type;
- `int`: converted to `number` type;
- `float`, `double`: converted to `number` type;
- `String`: converted to `string` type.


::: warning

C-style strings are not supported. It will be converted to type `boolean`.
:::



The timing of the conversion is automatic and does not require developer intervention.

============================================================
FILE_PATH: src/transl/EN/cookbook/clangd-lsp.md

# Clangd configuration


When developing firmware with a cross-compilation tool chain, if you use the arm-none-eabi-gcc tool chain, and when using a build system such as CMake, you can configure the Clangd language server to improve the development experience. Specifically you will get these benefits:
- Accurately jump to declaration or definition based on actual project structure;
- View the API documentation (documentation comments written using `/**`, `//!` and other Doxygen format comments);
- Support code formatting rules defined by `.clange-format`;
- No compilation required, real-time static checking or error checking;
- Code prompts and completion during input;
- Find usage, code refactoring, and more.


## Preparation


Start by using an editor that supports LSP (Language Server Protocol), such as Visual Studio Code, and then install clangd and related plugins. If you need to install clangd manually, you can download the appropriate version of [LLVM](https://github.com/llvm/llvm-project/releases) or install it using your operating system's package manager.


After installing the necessary plugins, clangd may be able to be used in simple host projects without any configuration, but further configuration will be required in complex cross-compilation environments.


## Cross-compilation environment configuration


### CMake options


If using CMake as your build system, then to turn on the `CMAKE_EXPORT_COMPILE_COMMANDS` option you can do this via the command line argument:
``` bash
cmake .. -DCMAKE_EXPORT_COMPILE_COMMANDS=ON # CMake 配置阶段的命令行参数
```
If it is not convenient to use command line parameters, you can also define this variable in any `CMakeLists.txt` file:
``` cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```
Then when using CMake to configure or build the project, a `compile_commands.json` file will be generated in the output directory, which will be used by clangd.


### Clangd configuration


After configuring CMake and generating `compile_commands.json`, clangd may work partially, but you may encounter the following problems:
- `compile_commands.json` is located very deep in the directory hierarchy and clangd cannot find it;
- clangd cannot find standard header files suitable for cross-compilation environments, such as `stdint.h` etc.


To solve these problems, first create a `.clangd` file in the root directory of the project (that is, the directory opened by the editor, usually the directory where the `.git` folder is located). It is a YAML file and fill in the following content:
``` yaml
CompileFlags:
  CompilationDatabase: "Relative path to the directory containing compile_commands.json"
  Add:
    - -resource-dir=C:/gcc-arm-none-eabi-9-2020-q2/arm-none-eabi/include
    - -IC:/gcc-arm-none-eabi-9-2020-q2/arm-none-eabi/include
    - -IC:/gcc-arm-none-eabi-9-2020-q2/arm-none-eabi/include/c++/9.3.1
    - -IC:/gcc-arm-none-eabi-9-2020-q2/arm-none-eabi/include/c++/9.3.1/arm-none-eabi
    - -IC:/gcc-arm-none-eabi-9-2020-q2/lib/gcc/arm-none-eabi/9.3.1/include
  Remove:
    - -fno-reorder-functions
```
Please modify the file path according to the actual situation. Then add the following command line options to clangd's startup arguments:
``` bash
--query-driver=C:/gcc-arm-none-eabi-9-2020-q2/bin/arm-none-eabi-g++.exe # 路径根据实际情况填写
```
Then restart the language clangd and it should work normally.


vscode can add parameters through `clangd.arguments` in `.vscode/settings.json` of the project:
``` json
{
  "clangd.arguments": [
    "--query-driver=C:/gcc-arm-none-eabi-9-2020-q2/bin/arm-none-eabi-g++.exe"
  ]
}
```

============================================================
FILE_PATH: src/transl/EN/cookbook/blur-overlay.md

# blur overlay menu


## Effect display


This tutorial demonstrates the development techniques for displaying the overlay menu after blurring the background. The following example demonstrates this interaction effect (clicking the "..." button in the lower right corner will display the occlusion interface).


<glyphix id="cookbook-blur-overlay" width="410" height="502" title="模糊覆盖层" inline>


</glyphix>



The main purpose of this tutorial is to show how to implement an interface with blur using Glyphix.


## Implementation method


### text shadow


The text "Hokkaido sika deer" in the example can be shadowed by overlaying a layer of blurred text:
``` html
<stack class="wallpaper-title">
  <p class="shadow">Hokkaido sika deer</p>
  <p>Hokkaido sika deer</p>
</stack>
```
Place two identical pieces of text inside a [`stack`](/components/stack.md) component, with the underlying text as a shadow. This is achieved via the `shadow` CSS class of the underlying text:
``` css
.shadow {
  color: #0008;
  /* 为背景文本添加模糊，以呈现阴影效果 */
  filter: blur(8px);
  /* 必须使用 transparent 标记元素是透明的 */
  transparent: true;
}
```
Set the color of the background text to a semi-transparent gray and the `<p>` text component as a shadow via the blur filter ( [`filter: blur(8px)`](/framework/generic/styles.md#filter) ) attribute. Please note that the foreground text color should not be transparent, otherwise it may overlap with the `.shadow` layer.


### Custom font


The text "Hokkaido sika deer" is rendered through a custom font. Custom fonts can be introduced in Glyphix in the same way as on the Web:
``` css
@font-face {
  font-family: 'Playwrite Australia SA';
  src: url('/assets/PlaywriteAUSA-Regular.ttf');
}

.wallpaper-title {
  font-family: 'Playwrite Australia SA', 'sans-serif';
  color: #ffffff;
  margin-top: 25%;
}
```
As you can see, a font can be declared in CSS via the [`@font-face`](/framework/generic/styles.md#font-face-规则) block and referenced in the element's [`font-family`](/framework/generic/styles.md#font-family) attribute.


### background layer blur


Since pages currently popped up through [`router` API](/api/system-router.md) do not support translucent backgrounds, pages cannot be used to implement popup menus. But you can use this trick to simulate a popup "page":
``` html
<stack class="window" :disabled="popups">
  <image class="wallpaper" src="/assets/images/sika-deer.jpg" />
  ...
</stack>
<div class="overlay" if="popups">
  ...
</div>
```
You need to add two levels of elements to the page (`stack.window` and `div.overlay` in this case) and control them through a condition (such as `popups`). Specifically:
- `popups` controls the `disabled` attribute of the underlying element, so when `popups` is true, the underlying element does not respond to input such as gestures;
- `popups` also controls the rendering of top-level elements. When it is true, the top-level elements will be displayed.


The [`disabled`](/framework/generic/properties.md#disabled) attribute also provides the opportunity to blur underlying elements when the occlusion layer pops up:
``` css
.window:disabled {
  filter: blur(40px);
}
```
When the `disabled` attribute is set on an element, the `:disabled` pseudo-element of the underlying element will also be activated, so the blur effect of the above CSS will work.


::: tip

Since Glyphix does not support the browser's [`backrop-filter`](https://developer.mozilla.org/docs/Web/CSS/backdrop-filter) attribute, background blur cannot be achieved directly through the `div.overlay` CSS rule. Instead, the technique in this example must be used.
:::



## performance risk


Because the blur effect is computationally intensive, developers need to pay special attention to its performance burden. We recommend using blur effects only in static interfaces, and preferably also adding the [`quiescent`](/framework/generic/properties.md#quiescent) attribute to the elements that need to be blurred.


If possible, the interface with obfuscation should be tested on a physical device to see if it meets performance expectations.

============================================================
FILE_PATH: src/transl/EN/cookbook/README.md

# Practical guide


