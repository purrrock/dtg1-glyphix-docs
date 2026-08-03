---
title: Quick View: From Web to Glyphix
icon: compass
---

# Development Quick Tour: From Web to Glyphix

This document is designed for developers familiar with web front-ends (specifically Vue.js). We will skip the basic grammar teaching and go directly to the core mechanism of the Glyphix framework to help you quickly establish a correct mental model.

## Core concepts and operating environment

Glyphix is ​​an application framework that runs on MCU (microcontroller) devices. Although it is developed using HTML/CSS/JS, it is not a browser. This framework is used to develop complete applications instead of refreshable pages. Each application runs in an independent sandbox container.

There are several core differences you need to understand:
- **No DOM**: The bottom layer is directly rendered by the C++ native engine, and there is no DOM tree.
- **No Web API**: Browser APIs such as `window`, `document`, `localStorage`, etc. are not supported. System capabilities (network, storage, sensors) are provided through `@system.*` modules.
- **JS Engine**: Uses a lightweight JS engine (supports ES6 standard), but is extremely memory-constrained.

### Resource limits

Resource limitations are the biggest difference with web development. MCU devices typically have only a few MB of RAM. This means don't use network requests to load very large JSON data, or directly [`fetch`](../api/system-fetch.md) an image. Please keep the following points in mind:
- You can use the [`@system.request`](../api/system-request.md) module to download resources as files, and `fetch` will load the response into memory.
- Image resources are usually stored in the application package, and the size matches the screen resolution as much as possible.
- **Background Freeze**: After the application enters the background (`onHide`), it will usually be suspended or destroyed by the system within tens of seconds. Please note the save status.

### Equipment form

Glyphix apps typically run on small-screen devices such as smartwatches. Watch screen sizes are usually around 1.5 to 2 inches, with a typical resolution of 466×466 pixels, but round and rectangular screens exist. Lower-end devices may have lower pixel density, but the dimensions will be essentially similar. Such devices often use touch screens for interaction, which may support physical buttons or knobs, and the system handles most interaction details transparently.

Simulators are usually used for development and debugging, because the real machine deployment and debugging process is still fragmented and takes a long time.

### Typical project structure

This is our recommended project file structure, which is also the standard structure of quick applications:
```bash
src/
├─ manifest.json # Application manifest: configuration permissions, registration page routing
├─ app.js # Application entry: global life cycle (onCreate, onDestroy)
├─ pages/ # Page directory
│ └─ Main/
│ └─ index.ux # Page component
└─ assets/ # public resources
  └─ icon.png
```
You can introduce the [Node.js](nodejs.md) tool chain to manage dependencies as needed. The directory structure can also be adjusted as needed, but [`src/manifest.json`](/framework/application/manifest.md) and `src/app.js` must be fixed at this location.

## UI Development

Glyphix uses the [`.ux`](../framework/component/README.md) single-file component (similar to Vue SFC), which is similar in style to the Vue Options API, but there are significant differences.

### Flexbox layout first

The web defaults to a flow layout (Flow Layout), and the Glyphix page defaults to a stacked layout: if you put two divs on the page, they will overlap instead of being arranged one above the other. This is because this framework supports the use of multiple root nodes in `<template>`, for example:
```html
<template>
  <image class="background" src="/assets/bg.png" />
  <div class="content"> ... </div>
</template>
```
The default stacked layout is usually very suitable for this scenario.

Although containers such as `div` use fluid layout by default, it is recommended to use Flexbox for layout control. Most containers should explicitly declare `display: flex`, combined with `flex-direction` to control the arrangement of child elements.

Considering that device screen sizes vary greatly, please pay special attention to the use of length units:
- Use `px` units in smaller sizes, which are logical pixels and automatically scale based on screen density.
- Fonts should always use `rem` units, which are baselined by the device manufacturer and more consistent with system UX specifications.
- You can use percentage (`%`) units to implement responsive layout, but there are currently many limitations and defects, so please pay attention to debugging.

Since the screen is too small, you may specifically need the [`scroll`](../components/scroll.md) component to implement the scroll area. Unlike the web, the `div` container itself does not support scrolling and cannot be controlled using the `overflow` property.

### Template syntax differences

Although it looks like a Vue template, please note the following differences:
- Commands without `v-` prefix: such as `<div if="show">` or `<div for="item in items">`
- Event binding can be done with `on` or `@`, such as: `<p on:click="handler">`
- Text components such as `<p>` must be used: `<text>Hello</text>` can be displayed normally, but `<div>Hello</div>` will not render anything.
- Supports using `model:prop="state"` or `::prop="state"` [two-way binding](../framework/commands/model.md) for any component attribute, as long as an event with the same name as the attribute is triggered.

### Style restrictions

CSS support is a subset:
- Supports classes (`.class`), IDs (`#id`), tags (`div`) and descendants (`.a .b`). **Not supported** Complex relationship selectors such as `~`, `+`, `>`, etc.
- **Effect limitations**: Gradient, shadow and other effects are not supported. `transition` animation is not supported yet.
- **Performance Limitation**: Avoid using `transform` to move or align elements. `object-fit` defaults to `none` and is recommended to be left as default.
- Currently there is no support for dynamic `class` binding, nor for CSS variables.

## Components and Logic

### Script model

Component scripts are very close to the Vue Options API, and the following demonstration points out the main differences:
```js
export default {
  // Data model (Data), no need to declare attributes, data attributes are automatically exported as attributes
  data: {
    count: 0, // Modifying this.count will automatically trigger a view update
  },
  timer: null, // Non-responsive fields are defined directly on the component instance, or they do not need to be declared.
  // life cycle
  onInit() {}, // The data has been initialized and network requests can be initiated.
  onReady() {}, // The interface has been rendered
  onDestroy() {}, // Be sure to clean up the timer and subscribe to events here

//Methods, defined directly in the component object
  handleTap() {
    this.count++
    // Trigger custom events to the parent component
    this.$emit('change', { value: this.count })
  }
}
```
The fields in the `data` object are responsive properties, which currently only support JSON-compatible types (`Date`, `Map`, `Set`, etc. are not supported). If responsive updates are not required, it is recommended to define the field on the component instance (`this`).

::: tip
Do not use the `methods` object to wrap methods, just define them directly in the component object. There is no need to use `props` to define properties, fields in the `data` object are automatically exported as properties.

Nor can you use DOM APIs such as `document.getElementById` to find elements. You can use the [`this.$element()`](../framework/component/component-apis.md#element) method to get the element instance with the specified ID.
:::

### Pages and routing

A Glyphix application consists of multiple pages, which are navigated through routes. All pages need to be statically registered in the [`router.pages`](../framework/application/manifest.md#pages) field in `manifest.json`. Page components are similar to normal components, but support `onShow` and `onHide` lifecycle hooks.

Use the `system.router` system module to jump:
```js
import router from '@system.router'

// Jump and pass parameters
router.push({ uri: 'pages/Detail', params: { id: 123 } })
```
::: tip
Don't use other routing libraries, and don't pretend to be developing a single page application (SPA). Otherwise, existing functions such as transition effects and page stack management will not be available.
:::

### TypeScript support

If you use Node.js scaffolding to create a project, you can use TypeScript in the project for development after installing dependencies such as `glyphix` and `typescript` using npm, pnpm, etc.

For `.ux` single-file components, you can enable TypeScript support by adding the `lang="ts"` attribute on the `<script>` tag. For example:
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

## System capability integration

Don't try to use the browser API, use Glyphix [standard library](../api/README.md).

### Quick check of commonly used modules

| Function | Glyphix module | Description |
| :--- | :--- | :--- |
| **Network** | [`@system.fetch`](../api/system-fetch.md) | Must handle asynchronous callbacks or Promise |
| **Pop-up** | [`@system.prompt`](../api/system-prompt.md) | Provide Toast and Dialog |
| **Storage** | [`@system.storage`](../api/system-storage.md) | Synchronize local storage, directly read and write objects instead of strings |
| **Routing** | [`@system.router`](../api/system-router.md) | Management page stack |
| **Log** | `console.log` | Output to debugging terminal, same as browser |

### Asynchronous programming mode

System APIs usually support asynchronous callback and Promise styles. It is recommended to use `async/await` to keep the code clean.

```js
import fetch from '@system.fetch'
import prompt from '@system.prompt'

export default {
  onReady() { this.loadData() },
  async loadData() {
    try {
      const response = await fetch.fetch({
        url: 'https://api.example.com/data',
        method: 'GET', //default is GET
        responseType: 'json', // This does not require manual JSON.parse parsing
      })

if (response.data.code === 200)
        this.data = response.data.data
    } catch (err) {
      prompt.showToast({ message: 'Network Error' })
    }
  }
}
```

## Build and run

Use the [`gx emu`](../tutorials/glyphix.js/README.md) command to start the emulator, or use `gx build` to build the application package. If you use Node.js scaffolding, you can also use the `gx` command directly.

Please refer to the [Quick Start](getting-started.md) tutorial for detailed steps.

## Comprehensive example

The following is a complete component example that demonstrates the combined use of layout, data binding, event handling, and system APIs. You can view this example directly in your browser by clicking the `>` button to see the full code.

<glyphix id="quick-orientation-example" title="Counter component example" height="240">

```html
<!-- It is recommended to use Flex layout for the root container, operations are not allowed during loading -->
<div class="container" :disabled="loading">
  <text class="title">Hello, {{ name }}</text>

<div class="card">
    <text class="count">{{ count }}</text>
    <text class="btn" value="+1" on:click="increment">Add</text>
  </div>
</div>

<!-- Use the stacking layout of the page to overlay the loading status prompt -->
<text if="loading" class="loading">Loading...</text>
```

```css
.container {
  /* Page components do not need to set width and height, they are always full */
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  /* Note that the page background is generally not set, this is just a demonstration */
  background-color: #f5f5f5;
  border-radius: 16px;
  padding: 10%; /* percentage margin */
}

.title {
  font-size: 1.25rem; /* The font uses rem units */
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
  border-radius: 50%; /* round button */
  text-align: center;
}

.loading {
  color: #3d3d3d;
  font-size: 0.8rem;
  text-align: center;
}

/* Fade style for disabled state */
*:disabled {
  opacity: 0.5;
}
```

```js
import prompt from '@system.prompt'

export default {
  // component data
  data: {
    name: 'Glyphix',
    count: 0,
    loading: false
  },
  // Life cycle: component initialization completed
  onInit() {
    console.log('Component initialized')
    this.simulateFetch()
  },
  //method definition
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
    // Simulate an asynchronous operation, which produces a loading state
    setTimeout(() => {
      this.loading = false
      this.name = 'Developer'
    }, 1000)
  }
}
```

</glyphix>