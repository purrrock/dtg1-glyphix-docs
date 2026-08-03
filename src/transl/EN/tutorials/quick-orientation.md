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