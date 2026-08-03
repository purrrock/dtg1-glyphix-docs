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