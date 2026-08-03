# Context File: 05_glyphix_tutorials_EN.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/transl/EN/tutorials/nodejs.md

---
icon: nodejs
---
# Node.js Package Manager

In addition to using it independently, the `gx` packaging tool can be used with JavaScript package managers such as npm, pnpm, or yarn. This requires the `glyphix` package to be installed:

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

The main benefits of using a JavaScript package manager in Glyphix app development include:
- Using TypeScript instead of JavaScript as the development language, providing type safety and a better developer experience
- Using JavaScript libraries from the Node.js ecosystem suitable for embedded development (such as algorithm libraries, data processing tools, etc.)
- Using tools like ESLint and Prettier to improve code quality and development efficiency
- Facilitating team collaboration and project maintenance

::: warning
Currently, package managers are only supported for managing standard JavaScript or TypeScript dependencies; Glyphix components cannot be reused in this way. When choosing third-party libraries, make sure they are suitable for embedded environments and avoid libraries that depend on the DOM, Node.js-specific APIs, or are overly bloated.
:::

::: tip
If the [Glyphix.js](glyphix.js/README.md) devtools are installed globally, you can directly run commands like `gx build` to package your project. Otherwise, you need to add `scripts` configuration in `package.json`.
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
The Glyphix packaging tool automatically handles the compilation of TypeScript files. The configuration above is primarily used for IDE type checking and code hints.
:::

## `glyphix.config.js` Configuration

It is recommended to create a `glyphix.config.js` file in the project root directory (the directory where `src/` or `package.json` is located) to customize packaging options:
```js
module.exports = {
  minify: false, // Disable code minification to facilitate debugging and mapping to source code line numbers
};
```
If you are using TypeScript, you can create a `glyphix.config.ts` file instead.

::: tip
Be sure to create this file and configure `minify: false`. Otherwise, the packaged code will be minified and obfuscated, making it impossible to map to source code line numbers during debugging.
:::

## Using TypeScript

The Glyphix framework provides experimental TypeScript support, allowing you to enjoy the benefits of type safety and modern JavaScript syntax in your app development.

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

Compared to the default JavaScript component script, using TypeScript requires the following adjustments:
1. Use `lang="ts"` in the `<script>` tag to specify TypeScript as the language type.
2. Import the `defineComponent` function from the `glyphix` module.
3. Pass the component object to be exported as an argument to `defineComponent` and export the return value of this function.

When using TypeScript, the `defineComponent` function makes code hints and type checking in your IDE much more accurate.

### `app.ts`

Rename `app.js` to `app.ts` to switch to the TypeScript app entry file, and the packaging tool will handle it automatically.

============================================================
FILE_PATH: src/transl/EN/tutorials/name-spec.md

---
icon: code-tags-check
---
# Component Naming Conventions

This document introduces the mandatory naming conventions and recommended naming styles for the component framework. Mandatory naming conventions must be followed; otherwise, unexpected results may occur. Adhering to the recommended naming conventions ensures maximum compatibility.

## Template Naming Conventions

Tag names in templates must be in kebab-case or PascalCase:
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

It is recommended to uniformly use the Web-compliant kebab-case naming convention.

## JavaScript Code Naming Conventions


Component names in JavaScript code must be in PascalCase, while the corresponding kebab-case should be used in templates.

Component property names in JavaScript code must be in camelCase:
``` js
export default {
  data: {
    propName: 0 // The property name in the template is prop-name
  }
}
```
These property names are automatically converted to their corresponding kebab-case equivalents in template code.

## File Naming Conventions

UX files must use the same name as the component, which is PascalCase. In the `<import>` tag, the `src` attribute must be a case-sensitive file URL, and the `name` attribute must use either PascalCase or kebab-case:
``` html
<import src="path/to/UxFile" name="UxFile"/>
<import src="path/to/UxFile" name="ux-file"/>
```
In fact, the naming requirements for the `name` attribute are consistent with those for tag names in templates.

============================================================
FILE_PATH: src/transl/EN/tutorials/qa.md

---
icon: help-circle-outline
---
# Frequently Asked Questions

## Bundler

### Project Build Issues

#### `Lisp Error: thread killed` Error

The specific symptom is an error message similar to the following:

``` log
[ 47%] Process image src/assets/images/frame1.png
error: Lisp Error: thread killed
```

This issue occurs because a previous build step failed, causing the ongoing image conversion build operation to be cancelled. You only need to fix the build operation with the `fatal` error to recover; no special handling is required.

### Simulator

#### Simulator Default Language

The default language of the simulator is `zh-CN`. Therefore, if you have added [internationalization](/framework/component/i18n.md) configuration, it will use the `zh-CN.json` translation file by default. When running the simulator using the `gx` command, you can use the `-l` or `--language` option to specify the language:
``` shell
gx emu -l en-US # Use American English
```
You can also dynamically change the language while the simulator is running using the inspector debugging tool.

============================================================
FILE_PATH: src/transl/EN/tutorials/quick-orientation.md

---
title: Quick Overview: From Web to Glyphix
icon: compass
---

# Quick Overview: From Web to Glyphix

This document is designed for developers familiar with Web front-end development (especially Vue.js). We will skip basic syntax tutorials and dive straight into the core mechanisms of the Glyphix framework to help you quickly build the correct mental model.

## Core Concepts & Runtime Environment

Glyphix is an application framework running on MCU (Microcontroller Unit) devices. Although it uses HTML/CSS/JS for development, it is **not** a browser. This framework is used to develop complete applications rather than refreshable pages, with each app running in an independent sandbox container.

You need to understand the following core differences:
- **No DOM**: The underlying layer is directly rendered by a native C++ engine; there is no DOM tree.
- **No Web APIs**: Browser APIs such as `window`, `document`, and `localStorage` are not supported. System capabilities (network, storage, sensors) are provided via `@system.*` modules.
- **JS Engine**: A lightweight JS engine (supporting the ES6 standard) is used, but memory is extremely limited.

### Resource Constraints

Resource limitation is the biggest difference compared to Web development. MCU devices typically have only a few megabytes of RAM. This means you should not use network requests to load oversized JSON data, or directly [`fetch`](../api/system-fetch.md) an image. Keep the following in mind:
- You can use the [`@system.request`](../api/system-request.md) module to download resources as files, whereas `fetch` loads responses into memory.
- Image resources are typically stored within the application package, and their dimensions should match the screen resolution as closely as possible.
- **Background Freezing**: When an application enters the background (`onHide`), it is usually suspended or destroyed by the system within tens of seconds. Please make sure to save your state.

### Device Form Factors

Glyphix applications typically run on small-screen devices such as smartwatches. Watch screens are usually around 1.5 to 2 inches, with a typical resolution of 466x466 pixels, and come in both circular and rectangular shapes. Lower-end devices may have lower pixel densities, but dimensions are largely similar. These devices typically use touchscreens for interaction and may support physical buttons or rotating bezels; the system handles most interaction details transparently.

Simulators are generally used for development and debugging, as the deployment and debugging process for physical devices is still somewhat fragmented and time-consuming.

### Typical Project Structure

This is the recommended project file structure, which also follows the QuickApp standard structure:
```bash
src/
├─ manifest.json  # Application manifest: configure permissions, register page routes
├─ app.js         # Application entry point: global lifecycle (onCreate, onDestroy)
├─ pages/         # Page directory
│  └─ Main/
│     └─ index.ux # Page component
└─ assets/        # Public resources
  └─ icon.png
```
You can optionally introduce the [Node.js](nodejs.md) toolchain to manage dependencies. You may also adjust the directory structure as needed, but [`src/manifest.json`](/framework/application/manifest.md) and `src/app.js` must remain in their fixed locations.

## UI Development

Glyphix adopts [`.ux`](../framework/component/README.md) Single File Components (similar to Vue SFC), featuring a style close to the Vue Options API, but with notable differences.

### Flexbox Layout First

The Web defaults to Flow Layout, whereas Glyphix pages default to a stacking layout: if you place two `div` elements on a page, they will **overlap** instead of stacking vertically. This is because the framework supports multiple root nodes inside `<template>`, for example:
```html
<template>
  <image class="background" src="/assets/bg.png" />
  <div class="content"> ... </div>
</template>
```
The default stacking layout is usually ideal for this kind of scenario.

Although containers like `div` use flow layout by default, it is recommended to use Flexbox for layout control. The vast majority of containers should explicitly declare `display: flex`, combined with `flex-direction` to control the arrangement of child elements.

Given the significant variations in device screen sizes, pay special attention to the use of length units:
- Use the `px` unit for smaller sizes; it represents logical pixels and scales automatically according to screen density.
- Fonts should always use the `rem` unit, whose baseline is defined by the device manufacturer, better aligning with system UX consistency guidelines.
- Percentage (`%`) units can be used for responsive layouts, but currently have several limitations and flaws, so please test carefully.

Due to small screen sizes, you may have a particular need for the [`scroll`](../components/scroll.md) component to implement scrollable areas. Unlike the Web, `div` containers do not support scrolling natively, nor can the `overflow` property be used to control it.

### Template Syntax Differences

Although it looks like a Vue template, note the following differences:
- Directives have no `v-` prefix: e.g., `<div if="show">` or `<div for="item in items">`
- Event binding can use either `on:` or `@`, e.g., `<p on:click="handler">`
- You must use text components like `<p>`: `<text>Hello</text>` renders correctly, but `<div>Hello</div>` renders nothing.
- Supports [two-way binding](../framework/commands/model.md) of arbitrary component properties using `model:prop="state"` or `::prop="state"`, as long as an event with the same name as the property is emitted.

### Style Limitations

CSS support is a subset:
- Supports classes (`.class`), IDs (`#id`), tags (`div`), and descendants (`.a .b`). Complex relational selectors like `~`, `+`, and `>` are **not supported**.
- **Visual Effects Limitations**: Gradients, shadows, and other effects are not supported. `transition` animations are not yet supported.
- **Performance Limitations**: Avoid using `transform` to move or align elements. `object-fit` defaults to `none` and keeping it as default is recommended.
- Dynamic `class` binding and CSS variables are currently not supported.

## Components & Logic

### Script Model

Component scripts are very close to the Vue Options API. The following example highlights the primary differences:
```js
export default {
  // Data model: properties do not need to be declared, data properties are automatically exported as instance properties
  data: {
    count: 0, // Modifying this.count automatically triggers view updates
  },
  timer: null, // Non-reactive fields can be defined directly on the component instance without declaration
  // Lifecycle
  onInit() {}, // Data initialized, network requests can be initiated
  onReady() {}, // UI rendering completed
  onDestroy() {}, // Be sure to clear timers and unsubscribe from events here

  // Methods: defined directly in the component object
  handleTap() {
    this.count++
    // Emit a custom event to the parent component
    this.$emit('change', { value: this.count })
  }
}
```
Fields within the `data` object are reactive properties, which currently only support JSON-compatible types (`Date`, `Map`, `Set`, etc., are not supported). If reactive updates are not needed, it is recommended to define fields directly on the component instance (`this`).

::: tip
Do not use a `methods` object to wrap methods; define them directly in the component object. You also do not need to use `props` to define properties; fields in the `data` object are automatically exported as properties.

Nor can you use DOM APIs such as `document.getElementById` to find elements. You can use the [`this.$element()`](../framework/component/component-apis.md#element) method to get an instance of the element with a specified ID.
:::

### Pages & Routing

Glyphix applications consist of multiple pages, and navigation between pages is handled via routing. All pages must be statically registered in the [`router.pages`](../framework/application/manifest.md#pages) field within `manifest.json`. Page components are similar to regular components, but they support the `onShow` and `onHide` lifecycle hooks.

Use the `system.router` system module for navigation:
```js
import router from '@system.router'

// Navigate and pass parameters
router.push({ uri: 'pages/Detail', params: { id: 123 } })
```
::: tip
Do not use other routing libraries, and do not pretend to develop a Single Page Application (SPA). Doing so will prevent you from utilizing existing features such as transition animations and page stack management.
:::

### TypeScript Support

If you create a project using the Node.js CLI scaffolding and install dependencies such as `glyphix` and `typescript` via npm or pnpm, you can develop using TypeScript in your project.

For `.ux` Single File Components, you can add the `lang="ts"` attribute to the `<script>` tag to enable TypeScript support. For example:
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

## System Capability Integration

Do not attempt to use browser APIs; use the Glyphix [standard library](../api/README.md).

### Common Modules Quick Reference

| Feature | Glyphix Module | Description |
| :--- | :--- | :--- |
| **Network** | [`@system.fetch`](../api/system-fetch.md) | Must handle asynchronous callbacks or Promises |
| **Dialogs** | [`@system.prompt`](../api/system-prompt.md) | Provides Toast and Dialogs |
| **Storage** | [`@system.storage`](../api/system-storage.md) | Synchronous local storage, reads/writes objects directly instead of strings |
| **Routing** | [`@system.router`](../api/system-router.md) | Manages the page stack |
| **Logging** | `console.log` | Outputs to the debug terminal, just like a browser |

### Asynchronous Programming Model

System APIs typically support both asynchronous callback and Promise styles. Using `async/await` is recommended to keep code clean.

```js
import fetch from '@system.fetch'
import prompt from '@system.prompt'

export default {
  onReady() { this.loadData() },
  async loadData() {
    try {
      const response = await fetch.fetch({
        url: 'https://api.example.com/data',
        method: 'GET', // GET by default
        responseType: 'json', // Avoids the need for manual JSON.parse
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

Use the [`gx emu`](../tutorials/glyphix.js/README.md) command to launch the simulator, or use `gx build` to build the application package. If you used the Node.js scaffolding, you can also use the `gx` command directly.

Please refer to the [Getting Started](getting-started.md) tutorial for detailed steps.

## Comprehensive Example

Below is a complete component example demonstrating the combined use of layout, data binding, event handling, and system APIs. You can view this example directly in the browser by clicking the `>` button to see the full code.

<glyphix id="quick-orientation-example" title="Counter Component Example" height="240">

```html
<!-- Flex layout is recommended for root containers; operations are disabled while loading -->
<div class="container" :disabled="loading">
  <text class="title">Hello, {{ name }}</text>

  <div class="card">
    <text class="count">{{ count }}</text>
    <text class="btn" value="+1" on:click="increment">Add</text>
  </div>
</div>

<!-- Use the page's stacking layout to overlay a loading status indicator -->
<text if="loading" class="loading">Loading...</text>
```

```css
.container {
  /* Page components do not need width and height set; they always fill the screen */
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  /* Note: page backgrounds are generally not set; this is for demonstration only */
  background-color: #f5f5f5;
  border-radius: 16px;
  padding: 10%; /* Percentage padding */
}

.title {
  font-size: 1.25rem; /* Fonts use the rem unit */
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

/* Faded styling for the disabled state */
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
  // Lifecycle: Component initialization completed
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
    // Simulate an async operation, which generates a loading state
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
title: Glyphix Application Development Tutorial
index: false
icon: routes
category:
  - Guide
---

## What is Glyphix

Glyphix is an efficient and lightweight application development framework designed for MCU (Microcontroller Unit) devices. It provides developers with a declarative UI development paradigm similar to the Web ecosystem: through HTML templates, CSS, and JavaScript, developers can easily build pages and components, and deploy applications to various smart devices (such as smartwatches).  

For more information, please refer to the [Framework](/framework/README.md) section.

### Web-like Framework

Unlike traditional MCU firmware development, Glyphix is closer to frameworks based on Web technology stacks. Application developers need to be familiar with JavaScript, CSS, and basic HTML knowledge. You do not need to master the complete Web development technology stack, such as the browser DOM, standard HTML tags, and complex build toolchains. However, if you are familiar with Web UI frameworks such as [Vue.js](https://vuejs.org/) ([Options API](https://vuejs.org/guide/introduction#options-api)), you will find it very easy to get started with Glyphix.

::: tip
It should be noted that Glyphix is not a "low-code" platform. During the development process, you will still encounter challenges such as logic abstraction, interface organization, user experience, and performance trade-offs. Therefore, mastering a solid foundation in JavaScript and a good frontend mindset will help you fully unleash the potential of Glyphix.
:::

### Declarative UI Framework

Traditional interface development is usually imperative: it requires step-by-step function calls to create controls, update states, and refresh interfaces. While flexible, this approach leads to tight coupling between business and interface logic. As the application scale grows, the code quickly becomes complex and difficult to maintain. Patterns such as MVC and MVVM were proposed precisely to solve this complexity.  

Glyphix adopts a declarative UI paradigm. Developers only need to describe "what the interface should look like," and the framework automatically completes rendering and updates based on data and state changes. This approach significantly reduces the complexity of interface logic and state management, allowing developers to focus primarily on functionality and interaction design rather than maintaining the UI hierarchy and refresh pipeline.

### Application Container

Glyphix is not just a UI framework; it also provides features such as application lifecycle management, permission isolation, and system APIs. Applications run within independent containers and are isolated from one another, ensuring system stability and security.

Please read the [Getting Started](getting-started.md) tutorial to start developing Glyphix applications right away.

## Other Questions

### Do I need to be familiar with MCU and embedded development?

Application developers generally do not need to understand the specific details of MCU and embedded development. However, they should have some awareness of device resource constraints. For example, MCU memory capacity is usually only a few megabytes, and there are also limits on the memory available for running JavaScript code. This means you might encounter situations where you cannot request very large JSON data from the network, or you cannot encode an entire image into Base64 and fetch it via a GET request.

These limitations, which are completely different from Web development, are indeed caused by the limited resources of MCU devices, but they are not part of typical MCU knowledge systems.

Intuitively, the best way to confirm whether your application's experience is good enough is to run it on the actual device. You can run it on real hardware multiple times at different stages of development to ensure the experience.

### Do I need to use C/C++ for application development?

Glyphix application development uses HTML, CSS, and JavaScript exclusively, so there is no need to use C/C++.

### How can embedded developers get started with Glyphix application development?

Embedded developers can follow the [Getting Started](getting-started.md) tutorial to gradually understand the core concepts of Glyphix. The framework adopts componentization and data-binding mechanisms similar to the Vue Options API. This may feel a bit different for readers accustomed to imperative GUIs like [LVGL](https://lvgl.io/) or Qt widgets, but Glyphix's declarative design also brings a more intuitive interface control experience.

Developers do not need to completely master HTML, CSS, and JavaScript, though familiarity with basic JavaScript syntax (such as variables, conditional statements, and function calls) will help in understanding Glyphix's rendering logic and event handling. You can familiarize yourself with these aspects through sample code and practical operations in tutorials and documentation to accelerate your development workflow.

### Do I need to focus on application performance optimization?

Our framework has been deeply optimized for the resource constraints of embedded systems, making it well-suited for a variety of hardware environments. Most applications can achieve sufficiently smooth and stable running performance under default settings, so there is usually no need to spend extra time on performance optimization.

If there is a need in the future to dive deeper into specific optimization solutions, we will provide dedicated performance optimization documentation to help developers further improve application runtime efficiency.

### Is the Glyphix environment different from a browser?

Yes, the Glyphix environment is significantly different from a browser. Glyphix does not have the DOM structure found in browsers, nor does it provide objects like `window` or `document`. Instead, it directly and exclusively provides a set of declarative interfaces through which developers can perform component development and interface interaction. This design simplifies the development process and is more suitable for embedded environments.

============================================================
FILE_PATH: src/transl/EN/tutorials/component-basic.md

---
icon: information-outline
---
# Component Basics

The previous document, "[Getting Started](getting-started)", briefly introduced the concept of components. This tutorial will explain components in further detail. Before reading this document, you need to know how to create and build a project, as well as how to edit source files. If you are not familiar with these topics, please read the "[Getting Started](getting-started)" tutorial.

## Introduction

In Glyphix application development, all user interfaces are components—ranging from a button as small as anything to an entire page. Component technology allows you to develop interfaces using a simple template language:
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
This is basically the `main/index.ux` file of the default project template. You can use the `gx emu` command to observe the display effect. The content inside the `<template>` tag is the component's template, which describes the component's appearance. Here, the `<p>` node will display the `text` property from the component's model object. Note that the component framework internally associates the content of the `<p>` node with the `text` property of the component model; whenever the value of the `text` property is modified, the interface will be updated synchronously.

We can use a timer to test this:
``` js
export default {
  data: { text: "begin!" },
  onInit() {
    let count = 0
    setInterval(() => this.text = "timeout: " + count++, 1000)
  }
}
```
Now, you will see that the displayed count value increases by 1 every second.

## Programming Model of Components

An important function of a GUI program is to change its appearance based on data and input, thereby achieving interactivity. In traditional GUI programming and native HTML, developers need to find the target element node in the interface tree and then call APIs to update it. Experience has proven that developing interfaces this way can be very complex. Therefore, GUI-applicable design patterns such as MVC, MVP, and MVVM have emerged, and new frameworks have also appeared in the web development field. These technologies have significantly reduced the difficulty of interface development.

The programming model of Glyphix components is very similar to front-end frameworks like Vue. The basic idea of these frameworks is to calculate the new interface based on the state of the interface model, rather than requiring you to update interface elements when the state changes. Compared to traditional technology, the interface view part in this approach is stateless and therefore simpler. Let's continue using the previous example to illustrate:
``` html
<template>
  <p>{{ text }}</p>
</template>
```
We already know that the interface will automatically update when the `text` property of the component model is updated. However, in traditional GUI frameworks, it is often necessary to manually update the `<p>` node after the model's `text` updates (which generally comes from user input or internal data changes). Frameworks like MVC can simplify these operations, but they are not extremely concise.

Now consider a very simple method: we write a `render()` function that generates an interface tree based on the current state of the model. If we replace the original interface tree with the value of the `render()` function on every frame, any changes to the model will be reflected in the interface. This approach is very simple, but you might reject it due to efficiency concerns. In fact, traditional GUI programming models were born precisely to solve the efficiency problem of this approach: only modify the elements in the interface that change, but doing so introduces state into the view layer, which also brings a lot of complexity.

The Glyphix component framework is based on this simple concept: the content inside the `<template>` tag implements the functionality of the `render()` function, while the JS code focuses on maintaining the model, and data changes in the model are automatically reflected in the relevant interface. You can think of the Glyphix component framework as always calculating a new interface based on the model's state, so we don't need to manually update interface elements.

::: tip
The underlying layer of Glyphix is not a DOM tree, and naturally there are no APIs for operating DOM elements. In fact, the component framework itself is the native Glyphix JavaScript API.
:::

## Responding to Input

Some components can respond to user input events. In this case, you can use the `on` directive to specify an event listener. For example, listening to the click event on a text component:
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
Clicking the text will automatically update the displayed content. The value of the `on:click` attribute, `text += ' click'`, is a JavaScript expression. Glyphix automatically binds `this` for the variables in the expression to the component object.

## Conditional Rendering

The `if` directive is used to conditionally render component content. The content area controlled by this directive will only be rendered when the value of the expression in the `if` directive is true.
``` html
<p if="display">Hello World</p>
```

The following example implements a mutually exclusive toggle effect. Clicking consecutively will cause the interface to alternately display "Component A" or "Component B".
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

## List Rendering

Use the `for` directive to repeatedly render a component to generate a list. The basic usage of the `for` directive is:
``` html
<p for="(index, value) in list">{{index}}: {{value}}</p>
```
Where `list` is a list property in the component model (must be of type `Array`), and `index` and `value` are two iteration variables. The value of `index` is the index of the current item, and the value of `value` is the value of the current item.

The `for` directive can be abbreviated in several forms:
``` html
<p for="list">{{$idx}}: {{$item}}</p>
<p for="value in list">{{$idx}}: {{value}}</p>
<p for="index, value in list">{{$idx}}: {{value}}</p>
```
The first shorthand only writes the expression to be iterated; in this case, `$idx` and `$item` will be used as the default iteration variable names. The second syntax explicitly defines the iteration variable for the current value, while the current index variable name defaults to `$idx`. The third syntax is the standard syntax with parentheses omitted.

::: tip
Due to scoping rules, the variables used for iteration when writing a `for` directive will only be active if used after the `for` directive.
:::

``` html
<!-- correct -->
<button for="list" text="{{$item}}"/>
<!-- error -->
<button text="{{$item}}" for="list"/>
```

### Using `if` and `for` Directives Simultaneously

You can use both `if` and `for` directives on the same element, in which case the `if` directive has a higher priority. In this example, when the `display` property is false, the entire list of `button` components will not be rendered:
```html
<button for="value in items" if="display">Hello {{value}}</button>
<p if="!display">Paragraph 1</p>
```

If your purpose is to conditionally render some nodes within the list generated by the `for` directive, you need to place the `if` directive on an inner element of the `for` directive.
```html
<button for="value in items">
  <p if="display">item: {{value}}</p>
</button>
```

::: tip
It is not recommended to use `if` and `for` directives on the same element, as this reduces code readability.
```

## Slots

Similar to content distribution in other frameworks, Glyphix also implements a content distribution API. We can use the `slot` component as an outlet for carrying distributed content.

In a child component, use the `slot` component to host the content defined in the parent component. During rendering, the `slot` component is replaced by the elements passed in from the parent component.

```html
<div>
  <slot/>
</div>
```

## Combining Components

Combining multiple components into a larger interface is the way user interfaces are built in the Glyphix component framework. Suppose there is a component named `Menu`; you can import it by using the `<import>` tag under the root node of the UX file that needs to reference it:
``` html
<import src="path/to/Menu" name="Menu"/>
```
The `src` attribute is the path of the component; please do not append the `.ux` suffix. The `name` attribute is an optional component name. If this attribute is omitted, the component's file name will be used as its name.

Use the `<import>` tag multiple times to import all dependent components:
``` html
<import src="path/to/ComA"/>
<import src="path/to/ComB"/>
<import src="path/to/ComC"/>
```

You can use custom components just like native components:
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

This is a menu interface. We want to print the information of the current menu item via the `clickMenu` method when the user clicks the menu. Therefore, the `Menu` component needs to be able to display the menu content and listen to its own click event via `on:click`.

Here is the content of the `Menu.ux` file:
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
We simply use a native `div` component to respond to the user's click and report it upward. The inner part of the `div` component will also display the child components passed in from above, ultimately making the menu list visible.

============================================================
FILE_PATH: src/transl/EN/tutorials/getting-started.md

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

============================================================
FILE_PATH: src/transl/EN/tutorials/glyphix.js/image-forge.md

---
icon: image-filter
---
# Image Management

The glyphix.js packaging tool manages all PNG image resources (`src` directory) in the project. The related modules mainly provide the following features:
- Support for image resource configuration files and provision of related configuration interfaces
- Conversion of images into device-optimized sizes and formats during packaging

Application developers only need to configure the packaging parameters for image resources according to their needs, while device vendors need to define specific image conversion strategies for their devices.

## Application Development Configuration

In application development, image packaging parameters must be configured to correctly generate resource packages.
Configuring `config/image-rules.json` and properties such as `config.designWidth` in `src/manifest.json` during application development will affect the packaging behavior of image resources. `config/image-rules.json` is generally used to configure quality and performance parameters, while fields in `manifest.json` affect the global scaling ratio of images (used for adapting to devices with different resolutions).

::: tip
`config/image-rules.json` can be configured using the `gx config` command or other methods, but direct editing with a text editor is not recommended.
:::

If using the `gx config` command, developers will primarily focus on two parameters: `transparent` and `quality`.

### Transparent Parameter

The `transparent` parameter indicates whether an image contains transparent pixels. If configured to `false` and the source image does contain transparent pixels, these pixels will be converted to opaque during generation (usually by blending onto a black background). Therefore, necessary images must be marked to retain transparent pixels; otherwise, incorrect overlay effects will be displayed. Because opaque images generally offer better performance on certain platforms and consume less data, the `transparent` option is disabled by default.

### Quality Parameter

The `quality` parameter represents the quality of the packed image and is an integer in the range $[0, 100]$. However, typically only 3 rough quality levels are used:
- High: 100, representing the highest quality
- Middle: 50, medium quality, the default value
- Low: 0, low quality

Image resources are optimized based on the quality parameter during conversion. Generally speaking, medium quality is a conversion strategy that balances display effects, rendering/loading performance, and memory resource consumption on the target platform, so it is recommended. Using high quality may yield better fidelity, but could result in performance degradation. Low quality can be used for images where quality can be sacrificed to improve performance (such as photographs). Specific target platforms may also ignore the `quality` parameter and use a unified strategy.

## Device and Platform Adaptation

Assuming that device and platform developers have implemented optimized image resource formats for specific target platforms and support multiple quality and pixel formats, the following work is required to generate these image formats in glyphix.js:
- Implement a command-line tool required for converting **a single image**
  - Must provide a command-line interface to convert from PNG images to a custom format, supporting output to a specified path (including overwriting the original file)
  - It is recommended to provide a command-line interface to convert from the custom format back to PNG images, supporting output to a specified path (including overwriting the original file). Missing this feature will prevent PC-side previews.
- Write device description files and image conversion scripts

### Image Conversion Scripts

The image conversion script is a scheme file. When an image needs to be converted, glyphix.js will call this script, which can determine how to convert the image based on the following variables:
- `env.image-path`: The absolute path of the image to be converted; the converted image is written over this path.
- `env.transparent`: The transparency parameter of this image.
- `env.quailty`: The quality parameter of this image.
- `env.target`: The conversion target mode, described later in this document.
- `env.verbose`: Whether to enable verbose mode. If true, detailed logs can be output; otherwise, logs should not be output.
- `env.script-dir`: The absolute path of the current script file. If the command required for conversion is relative to this script file rather than in the `PATH` environment variable, this parameter can be used for path concatenation.

`env.target` represents the **target mode** of image conversion, and its value determines the specific conversion method applied:
- `"device"`: Executes the complete conversion process targeted at the target device, such as removing the transparent channel of opaque images and then converting them to the PGF format (Glyphix Image Format) according to the quality parameter.
- `"emulator"`: Executes the conversion process targeted at the emulator. Since the emulator does not support specific hardware texture formats (such as ETC2, etc.), to ensure images are displayed properly in the emulator, only the transparent channel of opaque images may be removed without further conversion to the target device format (or converting to a software-supported PGF format).
- `"preprocess"`: Executes only the preprocessing step, which is removing the transparent channel of opaque images and outputting the result in PNG format.
- `"preview"`: Generates a preview PNG image. First, the image is converted to the custom target format following the `"device"` target conversion process, and then the output image is converted back to PNG for preview purposes.

::: tip
If the command-line tool for image conversion does not support converting custom formats to PNG, do not implement the `"preprocess"` and `"preview"` target modes.
:::

### The image-forge Command-Line Tool

`image-forge` is a command-line tool for the PGF image format provided by Glyphix, featuring the following capabilities:
- Supports converting PNG images to PGF format and PGF images to PNG.
- Supports common ARGB and PAL pixel formats, distinguishing between premultiplied alpha modes.
- Supports blending transparent ARGB images onto a specified solid background to convert them into opaque images (rather than directly discarding the alpha channel).
- Supports row alignment by pixels or bytes.
- Supports LZ4 compression with configurable minimum compression thresholds (image data below the threshold will not be compressed).

Platforms using other custom image formats can also utilize `image-forge` to remove transparency channels.

## Image Conversion Script Example

The following example demonstrates how to use commands like `image-forge` to convert PNGs to PGF images, prioritizing the palette (PAL) format.

First, define the pixel format rules for opaque and transparent conditions:
``` scheme
; Define pixel format rules for opaque colors
(define (opaque-formats q)
  (cond ((<= q 50) "pal-rgb")
        (else "rgb24")))

; Define pixel format rules for transparent colors
(define (transparent-formats q)
  (cond ((<= q 50) "pal-argb-premul")
        (else "argb32-premul")))

; Calculate the target pixel format under the influence of transparency and quality parameters
(define pixel-format
  ((if env.transparent
      transparent-formats opaque-formats)
    env.quailty))

; Whether the image is converted to a palette format
(define palette (<= env.quailty 50))
```

The code above will use the palette format when the quality is less than or equal to 50, using `pal-rgb` or `pal-argb` depending on whether it is transparent. When the quality is higher than 50, it uses RGB or ARGB 8-bit sampled pixel formats. Ultimately, the `pixel-format` variable represents the actual pixel format name used, and `palette` indicates whether the palette format is used.

Next, define the commands needed for various situations:

``` scheme
; Whether to append the --verbose command-line argument
(define if-verbose (if env.verbose "--verbose " ""))

; Call the pngquant command to reduce image colors to 256 colors or fewer; pngquant must be installed in the system
(define color-reduction
  (string-append "pngquant --ext=.png --force " if-verbose env.image-path))

; Convert image to PGF format
(define convert (string-append "image-forge "
  "--format=" pixel-format " " ; Specify output pixel format
  "--compress --min-compress-ratio=5 " ; Compress image data to reduce file size, with a minimum compression ratio of 5
  "--align=16 --pixel-align " ; Align images to 16 pixels
  if-verbose
  env.image-path))

; Remove image Alpha channel and add background
(define remove-alpha (string-append "image-forge --bypass "
  ; On the bes2500ibp watch, non-transparent images can have their alpha channel removed and blended with a black background; this operation can improve image quality after PAL color reduction
  (if env.transparent "" "--background black ")
  if-verbose
  env.image-path))

; Command to decode PGF images back to PNG
(define decode
  (string-append "image-forge --decode " if-verbose env.image-path))
```

In the code below, `execute-try` calls the specified `f` function when a command exits with a non-zero status, while the `execute` function prints an error log and abnormally exits the script when a command exits with a non-zero status. The `run-convert` function executes the complete target device image conversion process (calling `remove-alpha` and `convert` commands).

``` scheme
; Execute a command and print its content in verbose mode; if the command exits abnormally with a non-zero status, call function f
(define (execute-try cmd f)
  (begin
    (if env.verbose ; Print command content if in verbose mode
      (display (string-append "Run command: " cmd "\n")))
    (let ((r (system (string-append env.script-dir "/bin/" cmd))))
      (if (= r 0) 0 (f r)))
  ))

; Execute a command, print its content in verbose mode, and exit the program if the command exits abnormally
(define (execute cmd)
  (execute-try cmd (lambda (x)
    (begin ; Print error code on failure and exit abnormally
      (display (string-append "subprocess failed (" (number->string x) "): " cmd "\n"))
      (exit-fail)
  ))))

; Convert image
(define (run-convert)
  (begin
    (execute remove-alpha) ; Remove transparency channel first
    (if palette (execute color-reduction)) ; Reduce pixel count if palette format is used
    (execute convert) ; Execute image conversion command
  ))
```

The `targets` macro defines the processing methods for all target modes, such as the `"device"` mode calling the `run-convert` function, etc.

``` scheme
; Define conversion strategies corresponding to targets
(targets env.target
  ; Device mode: Final image conversion process used for target devices
  ("device" (run-convert))
  ; Emulator mode: Only remove the alpha channel of non-transparent images, without format conversion
  ("emulator" (execute remove-alpha))
  ; Preprocess mode: Remove the alpha channel of non-transparent images and add a background
  ("preprocess" (execute remove-alpha))
  ; Preview mode: Generate PNG preview images consistent with the actual device display effect
  ("preview" (begin
    (run-convert) ; Convert image to PGF format first
    (execute decode))) ; Then convert image back to PNG
  )
```

### Using Image Conversion Scripts

To use an image conversion script, a field needs to be added to the device model description file:

``` yaml
description: default watch

screen:
  width: 454 # pixels
  height: 454 # pixels
  dpi: 326 # pixels per inch

#...
image-build: image-convert-pal.scm # Path of the image conversion script relative to this Yaml file
```

### More Complex Strategies

Since the image conversion script is a fully-featured programming language rather than a configuration language like Yaml or JSON, we can implement more complex custom conversion strategies without being limited by the features provided by the framework. Taking the aforementioned palette format conversion as an example: the PAL format does not perform well on color-rich images. In such cases, images can be converted to formats that perform better in these scenarios. The specific approach is as follows:
1. The `pngquant` command supports exiting abnormally when the quality falls below a specified value after converting to PAL format; configure the command arguments for this purpose.
2. Change the `color-reduction` operation executed by `execute` in the `run-convert` function to be executed by `execute-try`, and use alternative format conversion operations in the latter's error handling function.
3. Handling methods for targets like `preview` are similar, but note that when converting the output format to PNG, command exit anomalies must also be recognized so subsequent commands can continue trying.

In short, it follows the philosophy of shell scripting—using command exit codes to control the flow.

============================================================
FILE_PATH: src/transl/EN/tutorials/glyphix.js/cli.md

---
icon: console-line
---
# Command-Line Options

To be migrated.

============================================================
FILE_PATH: src/transl/EN/tutorials/glyphix.js/emulator.md

---
icon: watch-import-variant
---
# Simulator and Debugging

To run the simulator, you need to switch to the root directory of your project in the command line and run the `gx emu` subcommand. The Glyphix simulator provides an environment that is highly consistent with the runtime on a real device, allowing you to develop and debug most interfaces and features using the simulator without frequently installing the application onto a physical device.

::: tip
Due to limitations of the current [`glyphix`](https://www.npmjs.com/package/glyphix) npm package, please make sure to configure [`glyphix.config.js`](/tutorials/nodejs.md#glyphix-config-js-配置), otherwise source code line numbers for error messages will not be available when running `gx emu`.
:::


## The `gx emu` Subcommand

Runs the simulator using the device configuration from the last build. This command must be executed in the root directory of the Glyphix project. It automatically builds the project and creates the resource files required by the simulator, so there is no need to run `gx build` beforehand.

#### Command Options

- `-d --device=NAME`: Specifies the name of the simulated device. Defaults to `default` (with a resolution of $410 \times 502\rm px$).
- `-e --emulator-exe=CMD`: Specifies the emulator executable file. Defaults to `glyphix-emu`. Usually, this does not need to be modified.
- `-l --language=NAME`: Specifies the emulator's locale, defaulting to `zh-CN` (Simplified Chinese). You can view the list of supported languages using the `gx list language` command.
- `--target=URI`: Sets the package name or deeplink when the simulator starts, for example, `app://com.example.app/SomePage?query=value` or `com.example.app`.
- `-i --inspector`: Enables the inspector when running the simulator. The inspector is a web page that allows you to debug UI elements in the simulator via a browser.
- `-m --mobile-network`: (Not implemented yet) Enables only the mobile SDK's network proxy in the simulator rather than accessing the network directly.
- `-w --watch`: Watches the project directory while running the simulator, automatically rebuilding and refreshing the simulator interface when source files change.
- `-r --real-scale`: Displays the simulator window at real scale rather than scaling it according to the device resolution. This option is recommended for use on HiDPI screens.
- `-t --top`: Keeps the simulator window always on top.
- `-p --profiling`: Enables profiling mode. Due to significant performance differences between the simulator and the device, this option is usually not very useful.

## Startup Modes

By default, `gx emu` starts the simulator using the device configuration used in the last build. You can also adjust the startup behavior of the simulator using command options.

### Specifying the Device Model

You can use the `-d` or `--device` option to specify the device model you wish to simulate, for example:
```bash
gx emu -d generic-watch-466x466
```
This will start the simulator for the `generic-watch-466x466` device. You can use the `gx list device` command to view the list of installed devices.

If this option is not specified, the device specified last time will be used. When starting the simulator for the first time or after `gx clean`, the `default` device will be used.

### Deeplink Startup

By default, the simulator will start the application of the current project or an application menu interface. However, when debugging the [`onRoute()`](/framework/component/life-cycle.md#onroute) lifecycle function, you might want to start the application via a deeplink to ensure `onRoute()` receives specific parameters. You can use the `--target` option to specify a deeplink, for example:
```bash
gx emu --target app://com.example.app/SomePage?query=value
```
This will start the application with the package name `com.example.app`, and the path (including the root directory `/`, i.e., `/SomePage`) and query fields of the Deeplink URI will be passed to the application's `onRoute()` function.

### Simulating Device Dimensions

By default, the simulator uses the actual pixel resolution of the device, which may make the display size on your computer larger than the actual screen size of the device, making it difficult for developers to confirm whether UI elements (including design drafts) have optimal sizes on the device. The `-r` or `--real-scale` option allows you to simulate based on the real device dimensions:
```bash
gx emu -r
```
When using this option, you do not need to install the application onto a device to confirm the actual size of the UI. However, considering that the DPI of most watches exceeds 300, a 1080p monitor will cause the interface to appear too blurry in real-scale mode. It is recommended to use this option on HiDPI displays (such as 4K monitors or Retina screens on macOS).

::: tip
When using real-scale mode, you should use the `--device` option to specify your desired target device. Note that due to differing DPIs, two devices with the same resolution may have different screen sizes, so the display size in real-scale mode will also vary.
:::

### Auto-Refresh

The `-w` or `--watch` option monitors the project directory while running the simulator, automatically rebuilding and restarting the application when source files change. It is usually recommended to use this in combination with the `--top` option, for example:
```bash
gx emu -wt
```
This keeps the simulator window on top and automatically restarts the application after modifying source files. This is very useful for development and debugging: you can switch directly from your code editor to the simulator without manually restarting the simulator or frequently switching windows.

::: tip
Hot reloading of pages is currently not supported; instead, the entire application is restarted when source files are modified. If you want faster debugging speeds, you can set [`manifest.router.entry`](/framework/application/manifest.md#entry) to the page currently under development, so that every time the application restarts, it will directly enter that page.
:::

## Connecting to a Phone

You can connect to the simulator using the [Glyphix Debug](https://www.pgyer.com/KLeBQFv6) Android mobile app to facilitate debugging real devices and features related to phone-watch interconnection.

### Preparation

You need to install the Glyphix Debug app on your phone and ensure that your phone and computer are on the same local area network (LAN), such as connected to the same Wi-Fi. After starting the simulator and opening the Glyphix Debug app, tap the "Socket Connection" button. The app will display a connection interface where you can select the discovered simulator IP address or manually enter the computer IP and simulator port to connect.

The simulator listens on network port 7768 by default. If this port is occupied (usually when multiple simulators are started), it will automatically select the next available port and print the actually used port number upon startup. For example:
```bash
$ gx emu
[simulator.socket] MAS TCP server bind port 7768 successful 
```

::: tip
Once the simulator port is occupied and a port other than 7768 is selected, the Glyphix Debug app will not be able to automatically discover the simulator. You must manually enter the correct IP address and port number to connect.
:::

It is strongly recommended to enable the mobile network proxy mode of the simulator (covered in the next section) to avoid using the computer network and mobile network simultaneously. Otherwise, it may interfere with the normal operation of APIs that rely on phone-watch interconnection, such as [`@system.interconnect`](/api/system-interconnect.md).

### Mobile Network Proxy

Using the `-m` or `--mobile-network` option enables only the mobile SDK's network proxy feature, simulating a network environment similar to a real device. When using this option, the simulator will not automatically start the target application, but instead display an application list interface.

Before manually starting the application, you should connect the simulator via the "Socket Network" in the Glyphix Debug mobile app, and then tap the target application. Otherwise, the application will not be able to access the network.

::: tip
When using the `-m` mobile network proxy, you can simulate network interruptions by killing the mobile debugging app and reconnecting to the simulator. Otherwise, the simulator will automatically switch to the computer network.
:::

### Common Connection Issues

If you cannot connect to the simulator via the Glyphix Debug app, please check whether your computer and phone are connected to the same LAN, and ensure that the simulator program and port are not blocked by firewall rules. If you are connected to a public network, connection failures may occur due to firewalls or network isolation.

If you are using a VPN or proxy software, please ensure that traffic within the LAN is not proxied, otherwise connection will also fail.

## Other Operations

### Clearing Application Data

You can use [`gx clean`](README.md#gx-clean) to clear the application data of the running simulator. The next time you start the simulator, it will run as if it were in its initial installation state.

### Combining Command Options

You can combine multiple options together, for example:
```bash
gx emu -rwt -d default-watch-466x466
```
This is equivalent to using them separately:
```bash
gx emu -r -w -t -d default-watch-466x466
gx emu --real-scale --watch --top --device default-watch-466x466
```
It is recommended to install the auto-completion script as described in [`gx completion`](#gx-completion) to easily select device names and command options in the terminal.


============================================================
FILE_PATH: src/transl/EN/tutorials/glyphix.js/README.md

---
icon: package-variant-closed
---
# Glyphix.js Packaging Tool

glyphix.js is the packaging tool for Glyphix applications. It includes a command-line tool named `gx`, which can be used to create, build, and run Glyphix applications. The tool also includes a graphical simulator for running Glyphix applications on a computer.

This document provides installation and usage instructions for glyphix.js. The [Getting Started](/tutorials/getting-started.md) tutorial serves as a simpler introductory guide. Please also read [Building and Running](#building-and-running) to learn how to develop, build, and publish a Glyphix application.

## Installation

This section covers how to install the glyphix.js packaging tool. For general purposes, only the [npm Installation](#npm-installation) method is needed. The [Manual Installation](#manual-installation) method is suitable for special scenarios, such as restricted network environments or CI builds.

### npm Installation

You can use the [npm](https://nodejs.org) package manager to install the glyphix.js packaging tool. It is recommended to use the `-g` option for a global installation:
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
Before performing a global installation with pnpm, you may need to run `pnpm setup` to configure environment variables. The `pnpm install -g` command will prompt you on how to configure them.
:::

Once installed, you can run `gx --version` in your terminal to verify the installation. For example:
```bash
$ npm install -g glyphix-cli
$ gx --version
gx v0.10.1 - The Glyphix applet development toolchain
commit a9337cf1 - Tue Sep 23 10:03:48 2025 +0800
```

Additionally, [pngquant](#pngquant) must be installed to package application assets for certain devices.

### Manual Installation

You can also install glyphix.js manually from its compressed archive: add the `bin` directory from the extracted folder to your `PATH` environment variable. The installation methods for mainstream operating systems are described below.

::: tip
The glyphix.js tool is not just a single executable file; please do not omit other resource files (including all files in the `bin` and `share` directories).
:::

#### macOS / Linux

For macOS or Linux, you can use the `tar` command to install the glyphix.js packaging tool. Before doing so, you also need to install tools like `xz`:

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

After downloading the glyphix.js compressed archive, use the following commands to extract and install it:
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
Please replace the `.tar.xz` filename with the actual downloaded filename corresponding to your operating system and CPU architecture. After extraction, commands like `gx` will be located in the `~/.local/bin` directory. Please add this directory to your `PATH` environment variable, for example, by updating `.bashrc` like this:
```bash
# If ~/.local/bin is not in PATH, add it
echo "$PATH" | grep -q "$HOME/.local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc # Reload bash configuration
```

::: tip
When using `Zsh`, your `.zshrc` configuration file may import `.bashrc`, so you only need to update `.bashrc`. Otherwise, update `.zshrc` using the method above.

It is recommended to install the glyphix.js packaging tool in the user's `~/.local` directory to avoid root permissions.
:::

#### Windows

To install glyphix.js on Windows, download the corresponding Windows version archive, and use an extraction tool that supports the `7z` format (such as [7-Zip](https://www.7-zip.org/)) to extract it to a directory, such as `C:\glyphix`. Then, add `C:\glyphix\bin` to your system's [`PATH` environment variable](https://learn.microsoft.com/zh-cn/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)).

You can also use the `7z` command-line tool to extract it, for example:
```shell
7z x -y glyphix-v0.7.2-windows-x64.7z -oC:/glyphix
```
This is similar to the installation method on macOS and other systems.

### Installing System Dependencies

#### pngquant

Linux and macOS users need to install `pngquant` additionally. You can use `npm` to install it:
```bash
npm install -g pngquant-bin # pngquant-bin only supports installation via npm
```
The Windows version of `glyphix-cli` includes `pngquant.exe`, so no additional installation is required.

::: tip
You can also download precompiled binaries from [pngquant.org](https://pngquant.org/) or install them via your system's package manager.
:::

#### Linux System Dependencies

The Linux installation package for glyphix.js is distro-agnostic, and currently only includes a build for the `linux-x86_64` architecture. We have tested it to run on Ubuntu 20.04 (or newer) and Arch Linux.

If you only use the `gx` command for packaging (commonly used in CI builds), headless Linux distributions should work out of the box. Running the graphical simulator relies on the X Window System, so you may need to install Xorg-related packages. Especially under a Wayland environment, you will also need to install the `xwayland` package (native Wayland is not yet supported by the simulator).

### Uninstallation

For glyphix.js installed globally via a package manager like npm, use the corresponding package manager to uninstall it, for example:
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
For non-global installations using package managers like npm, simply remove the `glyphix-cli` dependency from `package.json` and run `npm install` (or `pnpm install`, `yarn install`) to update the `node_modules` directory.
:::

For manual installations, simply delete the files from the installation archive. For example, for a `tar.xz` installation on macOS and Linux:
```bash
tar -tf glyphix-v0.7.2-darwin-arm64.tar.xz > filelist.txt
cat filelist.txt # Inspect the list of files to be deleted
xargs -I {} rm -f "~/.local/{}" < filelist.txt # Execute deletion after confirmation
```
The `tar -tf` command lists the files in the archive. Replace `glyphix-xxx.tar.xz` with your actual installation file. Manual uninstallation on Windows is similar.

## Building and Running

After installing glyphix.js, use the [`gx build`](#gx-build) command in the root directory of your app source code to build the app package, or use the [`gx emu`](#gx-emu) command to run the simulator.

After building the application, refer to the [Submitting Application Packages](#submitting-application-packages) section to learn how to install the app onto a device or submit it to an app publishing platform.

## Command-Line Arguments

### General Options

#### `gx --help`

View help information. Help information can also be used with specific subcommands, for example, `gx build --help` views the help information for the `build` subcommand exclusively.

#### `gx --version`

The `-V --version` option is used to view the version number of the `gx` command.

#### `gx --verbose`

`-v --verbose` enables verbose logging output, which is generally unnecessary for application developers.

#### `gx --numeric-version`

Outputs the pure numeric version number of the `gx` command, such as `0.10.1`.

#### `gx --quiet`

`-q --quiet` enables quiet mode, suppressing most non-warning and non-error log outputs. This includes build progress logs when using `gx build`, which is typically used in CI environments that need to build a large number of app packages.

View the version number.

### `gx new`

Creates a new project. For example, `gx new myapp` creates a new project named `myapp`.

### `gx build`

Builds the project (default action). You can use the `--device` or `-d` option to specify the target device, for example:
``` bash
gx build -d default # Specify building for the default device
```
Use the `--dump` option to print compilation details of UX files.

glyphix.js supports incremental builds; when source code changes, only the modified parts are rebuilt.

The `-r --image-rules` parameter can specify the image packaging rules file, which defaults to `config/image-rules.json`. The value of this parameter will be cached, and subsequent executions of `gx build` or `gx emu` will follow the previous configuration.

#### Command Options

- `-d --device=NAME`: Specifies the target device name, which must be an installed device configuration name. You can use the `gx list device` command to view the list of installed devices. If this option is not specified, the `default` device is used.
- `-f --full`: Forces a complete rebuild of the project instead of an incremental build.
- `-e --emulator`: Builds the project for the emulator rather than an actual device. This option is automatically used when running the `gx emu` command.
- `-r --image-rules=PATH`: Specifies the image packaging rules file, defaulting to `config/image-rules.json`.

#### Submitting Application Packages

After building with `gx build`, a `.glyphix-work/dist/<device-name>/<package-name>` directory will be generated in your project directory, containing the built app package file (`.pkg` file). You can install this file onto a device for debugging using the mobile debug app, or submit it to an app publishing platform.

You should use the `-d` option to build app packages separately for all supported devices. Here is an example directory structure:
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
When submitting the app package, please compress and upload the **entire** `.glyphix-work/dist` directory, rather than just uploading the `.pkg` file or any single subdirectory. The platform identifies the app based on the information in `manifest.json` and may require `icon.png` as a preview icon.

::: tip
For Linux or macOS users, you can use a command like this to package apps for a specific category of devices:
```bash
gx list device | grep "^generic-" | xargs -n 1 gx build -d
```
This builds app packages for all devices whose names start with `generic-`.

Under Windows, you can also use a similar PowerShell command for batch building:
```shell
gx list device | ? { $_ -match "^generic-" } | % { gx build -d $_ }
```
:::

### `gx emu`

See the [Simulator and Debugging](/tutorials/glyphix.js/emulator.md) documentation.

### `gx clean`

Cleans build artifacts. This command deletes the `.glyphix-work` directory under the project folder.

### `gx config`

This command launches a Web interface for editing image packaging rules files. Following the command prompts, you can open the page in a browser to operate. This command has two usages:
``` bash
gx config # When inside a Glyphix project, no source directory needs to be specified (currently can only be used in the project root directory)
gx config path/to/dir # Configures the specified directory, usable for non-project image resource configuration
```

The `-r --image-rules` parameter can specify the image packaging rules file, defaulting to `config/image-rules.json`.

### `gx image-forge`

Converts loose image files. This command can specify arbitrary source and output paths and does not need to be executed inside a Glyphix project:
``` bash
gx image-forge src -o dist
```

Option Descriptions:
- `src` is the source path to convert. The `image-forge` command recursively converts all images and generates them into the target path specified by `-o, --output` (defaulting to `dist`), preserving the relative directory structure.
- `-r --image-rules` parameter can specify the image packaging rules file, defaulting to `config/image-rules.json`.
- `-d --device` specifies the target device for image conversion.

### `gx list`

Lists certain information. Three operations are currently supported:
``` bash
gx list device # Lists all installed device configurations
gx list template # Lists all installed project templates
gx list image # Lists relative paths of all image resources in the current directory (similar to the find command)
```

Detailed description text for certain information can be listed using `-d, --detailed`, for example:
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

This command is used to generate shell auto-completion scripts for the `gx` command, currently supporting [Zsh](https://www.zsh.org/) and [PowerShell 7+](https://github.com/PowerShell/PowerShell). Using `gx completion [SHELL]` outputs the auto-completion script for the specified shell (detecting the current shell if the `SHELL` argument is omitted). To install the completion script, use:
```bash
gx completion --install
```
Upon successful installation, it will prompt the installation path of the command completion script. Restarting your shell session will enable auto-completion, or you can use these commands to take effect immediately:
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

When using the auto-completion script, you can select `gx emu` devices, command-line options, etc., directly in the terminal without manual typing.

PowerShell uses cyclic completion by default; it is recommended to change it to a completion menu:
```shell
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
```
Add this command to your [`$PROFILE`](https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/creating-profiles#adding-customizations-to-your-profile) configuration file to make it permanently effective.

::: note
If the `--install` option fails to install automatically, you can also manually install the completion script using the `gx completion` command, for example:
```shell
gx completion zsh > ~/.zsh/completion/_gx.zsh
```
:::

## Default Configuration Paths

Configurations, project templates, device information, and other data in the glyphix.js tool can be stored in the following paths:
- System-level configuration: The `share/glyphix` directory relative to the parent directory of the `gx`/`gx.exe` executable. For example, assuming the `gx` executable path is `/usr/local/glyphix`, the system-level configuration resource path is `/usr/local/share/glyphix`.
- User-level configuration: `~/.local/share/glyphix` on Unix-like systems, and `%APPDATA%\AppData\Roaming\glyphix` on Windows.

Configuration files can be placed in either of these paths, with user-level configuration taking higher priority. `gx.js` comes with default configuration files bundled upon installation.

## Project Templates

Project templates are stored in the `templates` directory under the configuration path. Currently, only the `simple` template is supported, and customization is not supported.

## Device Configuration Files

Device configuration files are stored in the `devices` directory under the configuration path. Each device has a YAML configuration file named `<device-name>.yml`. The format of the configuration file is explained below:

``` yaml
# file: default.yml
description:
  Device description information for developers to view.

screen: # Fields describing the device screen configuration; all these fields are mandatory (affects UI layout and resource scaling)
  width: 454 # Horizontal pixels of the screen
  height: 454 # Vertical pixels of the screen
  dpi: 326 # Pixel density of the screen, in pixels per inch

ui: # Global interface configuration, all optional fields
  font-family: sans-serif # System default font family name (defaults to serif)
  font-size: 3.5 # System default font size, in points (pt, point), note: not pixels!!
  font-map: true # Whether to use a global font configuration mapping file. If true, the system resources must contain
                 # a font-faces.css file

# Optional system global asset package path; the following configuration means the global asset package
# is stored in a folder named default-global at the same level as default.yml. The global asset package
# contains pre-installed fonts and font configuration mapping files, etc.
global-assets: default-global

# Optional image conversion script. The script file path is relative to where the current device description file is stored.
# If no image conversion script is specified, raw PNG assets will be output during packaging, but resolution scaling will be applied.
image-build: image-convert.scm

# Command to run the simulator, defaults to executing glyphix-emu. The simulator command's executable file
# must be located in a directory within the PATH environment variable, otherwise execution will fail.
emulator: glyphix-emu
```

============================================================
FILE_PATH: src/transl/EN/cookbook/layout-tricks.md

# Layout Tips

## Limit Element Width

You can use the `margin` property to limit the width of an element.

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

# Swiper Page Indicator

<Glyphix id="cookbook-swiper-indicator" height="466" width="466" designWidth="466" title="Swiper Indicator">

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

# 2048 Game

## Demo

Tip: Use the mouse to swipe quickly up, down, left, and right to play the "2048 Game".

<glyphix id="cookbook-game-2048" height="466" width="466" title="2048 游戏" inline>

</glyphix>

============================================================
FILE_PATH: src/transl/EN/cookbook/async.md

# Asynchronous Operations

The main purpose of introducing asynchronous operations in JavaScript scripts is to move time-consuming tasks to the background for execution, avoiding the blocking of the JavaScript thread. The tasks moved to the background for processing are primarily I/O-bound operations. Glyphix provides a basic JavaScript asynchronous framework for developers. This framework provides only the necessary abstractions for asynchronous workflows and therefore introduces no extra overhead.

## Applicable Scenarios

Applicable scenarios for the asynchronous workflow model:

- Requests initiated by JavaScript code, processed by a native asynchronous processing thread, and results returned;
- Requests initiated by JavaScript code, processed by a native asynchronous processing thread, and messages reported periodically;
  - JavaScript code can actively request to revoke/cancel the request.

## Data Request Pattern

In the data request pattern, JavaScript code calls C++ APIs to create requests, executes operations in an asynchronous thread, and returns the results to the JavaScript code. During this process, data is transmitted through an asynchronous queue. The `async::ResultSession` template class provides a general operation framework for this pattern.

### Scenario Description

The following scenarios are typical of the data request pattern:

- **File Read and Write**: When JavaScript initiates a call, it needs to specify the file path, the file offset position, data length, or the data to be written. When the request is sent to the asynchronous thread for execution, the actual file read/write operation is performed, and upon completion, it notifies or returns the result to the JavaScript code.
- **Network Requests**: Similar to file read and write, when JavaScript initiates a call, it specifies the request parameters, which are then processed in a background thread and the results are returned.

The scenarios of the data request pattern have the following characteristics:
- The result returned by a request is single-fired, so this pattern is not suitable for sensors or timer listeners that may be triggered multiple times;
- A request always yields a result: if the request succeeds, it returns the result; otherwise, it returns an error message. The return of the result is also asynchronous;
- Once a request is initiated, it cannot be revoked.

### Example: Getting Battery Level

#### JavaScript API

Suppose we want to implement an asynchronous JavaScript function to get the battery level:
``` ts
getLevel(): Promise<number> // Promise-style API
getLevel(options: { // Callback-style API
    success: (level: number) => void,
    fail: (code: number, msg: string) => void // Battery level reading actually does not fail
}): void
```
Use the `getLevel()` function to asynchronously get the battery level. This function provides two API styles: `Promise` style and callback style. The code for both styles is as follows:
``` js
async function printBatteryLevel() {
    const level = await getLevel() // Asynchronously get the battery level
    console.log(`battery level: ${level}%`)
}
printBatteryLevel() // Print the battery level, console output example:
// battery level: 59%

// Below is the callback-style code, which is not recommended:
getLevel({
    success(level) { console.log(`battery level: ${level}%`) }
})
```

#### C++ Native Interface Export

The `getLevel()` function in JavaScript is actually implemented by C++. When JavaScript code calls this function, it initiates an asynchronous request to get the battery level, and upon obtaining the result, returns the result value to the JavaScript code via a callback function or a `Promise`. The C++ function implementing `getLevel()` is as follows:
``` cpp
static JsValue getLevel(const JsCallContext &ctx) {
    typedef async::ResultSession<BatteryGetLevel> Session;
    Session *session = new Session; // Create a Session object
    session->request(ctx.argc() ? ctx.arg(0) : JsValue());
    return session->promise();
}
```

The template class `async::ResultSession` (the `async` namespace is omitted below) implements the framework required for asynchronous data requests. Each asynchronous data request includes the following steps:
1. Create a `ResultSession` object
2. Call the `ResultSession::request()` method to initiate the request
3. Use `ResultSession::promise()` to return the `Promise` object to JavaScript.

This line of code
``` cpp
session->request(ctx.argc() ? ctx.arg(0) : JsValue());
```
In addition to initiating the request, we also pass the 0-th parameter passed by the JavaScript caller to the `ResultSession::request()` method. `ResultSession` automatically selects between the callback and `Promise` styles based on whether `success` / `fail` and other callback functions exist in that parameter. If it is `Promise` style, then
``` cpp
return session->promise();
```
returns a `Promise` object used to obtain the result of the asynchronous request; otherwise, it returns `undefined` and the callback function handles the result.

#### `ResultSession` Template Class

The declaration of the `ResultSession` template class is as follows:
``` cpp
template<class T, class H = ResultHandler> class ResultSession;
```
The template parameter `T` is a class that implements the specific asynchronous operation. This example implements a `BatteryGetLevel` class to achieve asynchronous retrieval of the battery level. The template parameter `H` determines how to handle the result of the asynchronous request. The default `ResultHandler` automatically selects the callback or `Promise` style, and developers generally do not need to modify it.

#### `BatteryGetLevel` Class

The definition of the `BatteryGetLevel` class is as follows:
``` cpp
struct BatteryGetLevel {
    async::Result<int> resolve() const {
        return battery_read_level(); // Get battery level
    }
    // errorMessage() is used to translate error codes into text. However, reading the battery level does not fail, so it can be implemented arbitrarily.
    static const char *errorMessage(Status) {
        return "get battery level failed";
    }
};
```
As you can see, `BatteryGetLevel` has two member functions. The `resolve()` function is used to execute specific operations in the asynchronous thread. The return value of the `resolve()` function must be of type `async::Result<T>`, which in this example is `async::Result<int>`.

The template parameter `T` of the return value `async::Result<T>` of the `resolve()` function is consistent with the type of the callback function parameter of the JavaScript API or the `Promise` data type. For example, in this case, `int` corresponds to the JavaScript API as:
``` ts
// The return value type of C++'s BatteryGetLevel::resolve() function
// async::Result<int> corresponds to JavaScript's Promise<number>
getLevel(): Promise<number>
```

In other words, if `resolve()` returns an `async::Result<String>` value, it will return a `Promise<string>` in JavaScript, or `{ success(value: string): void }` for a callback function. For details on C++ and JavaScript data type conversion, please refer to [Data Type Conversion](#data-type-conversion).

### Example: File Reading

#### JavaScript API

Suppose we want to implement an asynchronous JavaScript function for file reading:
``` ts
readfile(url:string): Promise<string> // Promise-style API
readFile(option: {   // Callback-style API
  uri: string,
  success?: (data: string) => void,
  fail?: (code: number, msg: string) => void,
}): void
```
This function will asynchronously read the contents of the file and return them via a `Promise` object, with the return value being the file contents. The actual JavaScript code looks like this:
``` js
async function printReadFile() {
    const data = await readFile("file.txt") // Asynchronously get the file contents
    console.log('File read successfully:', data)
}

printReadFile() // Print the file contents as a string, console output example:
// File read successfully: hello

// Below is the callback-style code
readFile({
    url: "file.txt", 
    success: (data: string) => {  
        console.log('File read successfully:', data);  
    }
})
```

#### C++ Native Interface Export

The `readFile()` function in JavaScript is actually implemented by C++. When JavaScript code calls this function, it initiates an asynchronous request to read a file, and upon obtaining the result, returns the result value to the JavaScript code via a callback function or a `Promise`. The C++ function implementing `readFile()` is as follows:
``` cpp
JsValue readFile(const JsCallContext &ctx) {
    typedef async::ResultSession<ReadFileRequest> Session;
    if (ctx.argc() > 0 && ctx.arg(0).isObject()) { 
        Session *session = new Session;
        // Convert the url field of the JavaScript function parameter to a C++ String 
        session->client().url = ctx.arg(0)["url"].toString(); 
        session->request(ctx.argc() ? ctx.arg(0) : JsValue());
        return JsValue();
    }
}
```
For an explanation of the template class used, please refer to [ResultSession Template Class](#resultsession-template-class), and for code explanation, refer to [C++ Native Interface Export](#c-native-interface-export) under Getting Battery Level.

#### ReadFile Class

The definition of the `ReadFileRequest` class is as follows:
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
As you can see, `ReadFileRequest` has two member functions. The `resolve()` function is used to execute specific operations in the asynchronous thread. The return value of the `resolve()` function must be of type `async::Result<T>`, which in this example is `async::Result<String>`. Note that JavaScript data types cannot be processed inside the `resolve()` function; the `url` is converted to a C++ String type inside the `readFile()` function before initiating the asynchronous request, and such data conversions cannot be processed within the `resolve()` function.

## Listen Pattern

In the listen pattern, JavaScript code calls C++ APIs to create requests for multiple asynchronous events, such as listening to sensor data. When the data changes, an asynchronous event is executed to return the result to JavaScript. The `async::ListenSession` and `async::Signal` template classes provide a general operation framework for this pattern.

### Scenario Description

The following scenarios are typical of the listen pattern:

- **Listening to various sensors**: Initiated by JavaScript by calling the C++ API for listening to the corresponding sensor, which requires specifying a callback function. When the sensor reads data and it changes, an asynchronous thread returns the new data to the JavaScript code as a parameter of the callback function.
- **Periodic timer tasks**: When JavaScript initiates a call, it needs to set the time for the timer task, the callback function after the task times out, and whether it is periodic. After sending the request, every time the timer task times out, the asynchronous thread returns the result to JavaScript, triggering the callback function set by JavaScript.

The scenarios of the listen pattern have the following characteristics:
- Once listening is started, it supports multiple asynchronous requests, so it may not be suitable for single-shot asynchronous events like file reading/writing and network status requests;
- Once listening is started, it must be canceled when no longer needed, otherwise it will cause a memory leak.

### Example: Listening to Battery Level

#### JavaScript API

Suppose we want to implement an asynchronous JavaScript function to listen to the battery level:
``` ts
subscribe(callback: (level: number) => void): number // Listen to battery level
unsubscribe(subscribeID: number): void // Cancel listening
```

Use the `subscribe()` function to asynchronously listen to the battery level and the `unsubscribe()` function to cancel listening. An example of usage is as follows:
``` js
// Start listening and return an ID used to cancel listening
let id = subscribe(level => {
  // If the battery level changes, the listening callback function is triggered, console print example:
  // now battery level: 59
  console.log(`now battery level: ${level}%`)
})

unsubscribe(id); // Cancel listening
``` 

#### C++ Listen Interface Export

The `subscribe()` function in JavaScript is actually implemented by C++. When JavaScript code calls this function, it listens to the battery level. Whenever the battery level changes, it initiates an asynchronous request and returns the result value to the JavaScript code via a callback function. The C++ function implementing `subscribe()` is as follows:
``` cpp
async::Signal<int> Level; // Create a global object Level

level(45); // Level value changes, send an asynchronous request

static JsValue subscribe(const JsCallContext &ctx) {
    Applet *applet = Applet::current(&ctx.vm());
    if (applet && ctx.argc())  // Check if parameters are passed
        return applet->bindObject(Level.connect(ctx.arg(0)));
    return JsValue();
}
```
A global object `Level` must be created. The template class `async::Signal` (the `async` namespace is omitted below) used here implements the listening request framework. Listening requests include the following steps:
1. Before listening, a global `Signal` class object must be created;
2. Use the `Signal::connect()` method to associate the first parameter passed by JavaScript with `Level`;
3. Call `Applet::bindObject` to bind the `Level` object; when the state of `Level` changes, call the callback function to return the result to the JavaScript code.

This line of code
``` cpp
level(45);
```
changes the `Level` value to $45$, triggering the listening mechanism to initiate an asynchronous request, using the changed value as a parameter for the callback function, and finally returning the result to the JavaScript code.

#### C++ Cancel Listen Interface Export

The `unsubscribe()` function in JavaScript is also implemented by C++. When JavaScript code calls this function, it cancels the listening to avoid memory leaks caused by unused listeners. The C++ function implementing `unsubscribe()` is as follows:
``` cpp
static JsValue unsubscribe(const JsCallContext &ctx) {
    Applet *applet = Applet::current(&ctx.vm());
    if (applet && ctx.argc() >= 1 && ctx.arg(0).isNumber()) // Check if the passed parameters are correct
        delete applet->unbindObject<async::Slot>(ctx.arg(0).toInt());   
    return JsValue();
}
```
Canceling a listen request requires calling `Applet::unbindObject` to unbind, passing the ID returned by the `subscribe()` function to determine the object to be unbound.

#### `Signal` Template Class

``` cpp
template<class T, class H = ListenHandler> class Signal;
```
The template parameter `T` is a class that implements the specific asynchronous operation. This example demonstrates using an `int` type to implement battery level listening. The template parameter `H` determines how to handle the result of the asynchronous request. The default `ResultHandler` automatically selects the callback or Promise style, and developers generally do not need to modify it.

## Data Type Conversion

In `ResultSession` or `ListenSession`, data for asynchronous operations must be converted into `JsValue` objects to be used in JavaScript code. For example, [BatteryGetLevel](#batterygetlevel-class) defines:
``` cpp
async::Result<int> BatteryGetLevel::resolve() const;
```
This function declaration means that the return data type of the battery level request is `int`, which can be converted to `JsValue`. In fact, the following types can be converted to `JsValue`:
- `bool`: Converted to `boolean` type;
- `int`: Converted to `number` type;
- `float`, `double`: Converted to `number` type;
- `String`: Converted to `string` type.

::: warning
C-style strings are not supported. They will be converted to the `boolean` type.
:::

The conversion happens automatically without requiring developer intervention.

============================================================
FILE_PATH: src/transl/EN/cookbook/clangd-lsp.md

# Clangd Configuration

When developing firmware using a cross-compilation toolchain such as `arm-none-eabi-gcc` along with a build system like CMake, you can configure the Clangd language server to enhance your development experience. Specifically, you will gain the following benefits:
- Accurate jump-to-declaration or definition based on the actual project structure;
- View API documentation (documentation comments written in Doxygen formats such as `/**` or `//!`);
- Support for code formatting rules defined by `.clang-format`;
- Real-time static analysis or error checking without the need for compilation;
- Code hints and completion while typing;
- Find references, code refactoring, and more.

## Prerequisites

First, use an editor that supports LSP (Language Server Protocol), such as Visual Studio Code, and install clangd and its related extension. If you need to install clangd manually, you can download a suitable version from [LLVM Releases](https://github.com/llvm/llvm-project/releases) or use your operating system's package manager.

After installing the necessary extensions, clangd may work out-of-the-box in simple native projects, but further configuration is required in complex cross-compilation environments.

## Cross-Compilation Environment Configuration

### CMake Options

If you use CMake as your build system, you need to enable the `CMAKE_EXPORT_COMPILE_COMMANDS` option. You can do this via a command-line argument:
``` bash
cmake .. -DCMAKE_EXPORT_COMPILE_COMMANDS=ON # Command-line argument during the CMake configuration stage
```
If using command-line arguments is inconvenient, you can also define this variable in any `CMakeLists.txt` file:
``` cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```
Then, when you configure or build the project using CMake, a `compile_commands.json` file will be generated in the output directory, which will be used by clangd.

### Clangd Configuration

After configuring CMake and generating `compile_commands.json`, clangd may work partially, but you are likely to encounter the following issues:
- `compile_commands.json` is located deep in the directory hierarchy, and clangd cannot find it;
- clangd cannot find the standard header files suitable for the cross-compilation environment, such as `stdint.h`.

To solve these problems, you first need to create a `.clangd` file in the project's root directory (i.e., the directory opened by the editor, usually where the `.git` folder resides). This is a YAML file; populate it with the following content:
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
Please modify the file paths according to your actual situation. Next, add the following command-line option to clangd's startup arguments:
``` bash
--query-driver=C:/gcc-arm-none-eabi-9-2020-q2/bin/arm-none-eabi-g++.exe # Fill in the path based on your actual situation
```
Then restart the language server, and clangd should work properly.

In VS Code, you can add arguments via `clangd.arguments` in the project's `.vscode/settings.json`:
``` json
{
  "clangd.arguments": [
    "--query-driver=C:/gcc-arm-none-eabi-9-2020-q2/bin/arm-none-eabi-g++.exe"
  ]
}
```

============================================================
FILE_PATH: src/transl/EN/cookbook/blur-overlay.md

# Blur Overlay Menu

## Demo

This tutorial demonstrates the development technique of displaying an overlay menu after blurring the background. The following example shows this interactive effect (click the "..." button in the bottom right corner to show the overlay interface).

<glyphix id="cookbook-blur-overlay" width="410" height="502" title="Blur Overlay" inline>

</glyphix>

The main purpose of this tutorial is to show how to implement a blurred interface using Glyphix.

## Implementation

### Text Shadow

The shadow of the text "Hokkaido sika deer" in the example can be achieved by overlaying a layer of blurred text:
``` html
<stack class="wallpaper-title">
  <p class="shadow">Hokkaido sika deer</p>
  <p>Hokkaido sika deer</p>
</stack>
```
Place two identical texts inside a [`stack`](/components/stack.md) component, and use the bottom text as the shadow. This is achieved through the `shadow` CSS class on the bottom text:
``` css
.shadow {
  color: #0008;
  /* Add blur to the background text to create a shadow effect */
  filter: blur(8px);
  /* transparent is required to mark the element as transparent */
  transparent: true;
}
```
Set the color of the background text to translucent gray, and use the blur filter ([`filter: blur(8px)`](/framework/generic/styles.md#filter)) property to turn the `<p>` text component into a shadow. Note that the foreground text color should not be transparent, otherwise it may overlap with the `.shadow` layer.

### Custom Fonts

The text "Hokkaido sika deer" is rendered using a custom font. In Glyphix, custom fonts can be introduced using the same method as on the Web:
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
As you can see, a font can be declared in CSS via the [`@font-face`](/framework/generic/styles.md#font-face-规则) block and referenced in the element's [`font-family`](/framework/generic/styles.md#font-family) property.

### Background Blur

Since pages popped up via the [`router` API](/api/system-router.md) do not currently support translucent backgrounds, pages cannot be used to implement popup menus. However, this technique can be used to simulate a popped-up "page":
``` html
<stack class="window" :disabled="popups">
  <image class="wallpaper" src="/assets/images/sika-deer.jpg" />
  ...
</stack>
<div class="overlay" if="popups">
  ...
</div>
```
You need to add two layers of elements to the page (`stack.window` and `div.overlay` in this example), and control them through a condition (such as `popups`). Specifically:
- `popups` controls the `disabled` property of the underlying element, so when `popups` is true, the underlying element will not respond to inputs such as gestures;
- `popups` also controls the rendering of the top-level element, which is displayed when it is true.

When the overlay pops up, the [`disabled`](/framework/generic/properties.md#disabled) property also provides an opportunity to blur the underlying element:
``` css
.window:disabled {
  filter: blur(40px);
}
```
When the element is set with the `disabled` property, the `:disabled` pseudo-class of the underlying element is also activated, so the blur effect in the CSS above will take effect.

::: tip
Since Glyphix does not support the browser's [`backdrop-filter`](https://developer.mozilla.org/docs/Web/CSS/backdrop-filter) property, you cannot achieve background blur directly through CSS rules on `div.overlay`, but instead must use the technique in this example.
:::

## Performance Risks

Since blur effects are computationally intensive, developers need to pay special attention to their performance burden. We recommend using blur effects only in static interfaces, and preferably adding the [`quiescent`](/framework/generic/properties.md#quiescent) property to elements that need to be blurred.

If possible, you should test whether the blurred interface meets performance expectations on physical devices.

============================================================
FILE_PATH: src/transl/EN/cookbook/README.md

# Practical Guide

