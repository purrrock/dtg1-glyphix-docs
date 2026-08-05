# Application Framework

A Glyphix application is an interactive program that can run independently, designed specifically for MCU (Microcontroller Unit) devices. It consists of a series of pages, components, and related logic, and is supported and managed by a runtime environment. Through the Glyphix application framework, developers can build and organize applications using HTML templates, CSS, and JavaScript in a way that is close to Web development.

You can think of an application as a standalone program like a mobile app: they can be installed, launched, switched, and uninstalled. Each application has its own resources and data storage space, and runs in a controlled environment.

## Runtime

The runtime is a native system integrated into the device firmware. It provides a standard application runtime environment and manages all system resources required by the application. This section introduces the various responsibilities of the runtime and its behavioral standards.

### Launching Applications

The runtime can launch an application via native or JavaScript APIs. Each application has an independent runtime environment, which means:
- Applications run in independent JavaScript execution environments without interfering with each other.
- Each application has independent resource access, including page structures, file resources, data storage, and various other resources.
- No low-level privileges: The application's runtime environment is unrelated to the underlying system and therefore cannot bypass the runtime to access low-level resources.

However, certain resources are globally unique, such as the visible area of the screen and public file directories. As user operations occur, some applications will enter the **foreground** interactive state, while others will switch to the background.

### Page Management

The interface of a Glyphix application is primarily provided by **pages**. Therefore, the runtime maintains the page objects for each application and manages global popup pages. These management mechanisms include page switching, rendering, and lifecycle control.

### Memory Resource Management

The runtime system uniformly manages memory and various system resources for individual applications and across multiple applications, thereby optimizing overhead and avoiding leaks:
- Postponing loading operations for resources such as images and text to reduce interface loading latency.
- Caching and optimizing page and component files to accelerate hot-loading performance.
- Maintaining resource and low-level file mappings to achieve device-agnostic I/O and resource access.
- Optimizing memory footprint to avoid exhausting MCU memory.

### Resource Reclamation

When an application exits, the runtime reclaims all resources, releasing system consumption back to the level before the application was launched. This is a system-level mechanism that cannot be controlled at the application level, which also means:
- Applications will not fulfill pending Promise objects upon exit, so asynchronous operations may never yield a result. Please note that necessary handling should be done in the application's [`onDestroy`](/framework/component/life-cycle.md#ondestroy-1) lifecycle function.
- The underlying system may kill the application at any time and has complete operational permissions. Absolute persistence cannot be guaranteed at the application level, nor can you assume the device's application scheduling policy.

### Standard APIs

The runtime provides a set of standard [APIs](/api/README.md) that abstract differences in Bluetooth, networking, sensors, and system functions across specific devices. Most APIs are supported by all devices, but some are only supported on specific devices.

### Background Management

The application framework supports running applications in the background, which allows users to return to interfaces like the app list and then return to the current application without restarting it. Background-running applications are subject to certain limitations, such as:
- Background applications cannot navigate pages; APIs such as [`router.push()`](/api/system-router.md#push) will be directly suspended.
- Background applications may automatically return to the main page (i.e., the bottommost page), just like a user returning manually.
- Most applications can only remain in the background briefly and will be killed by the system in about half a minute to release resources.
- Applications performing specific tasks such as audio playback can continue running in the background.

::: tip
If your application needs to play audio in the background (such as a podcast app), please ensure that you start the audio playback task on the main page or in an interface-agnostic script, rather than playing it on deep pages. Otherwise, when the background application returns to the main page, audio playback may be interrupted and lose background residency.
:::

The application background mechanism involves a series of lifecycle management; for details, see [Application Lifecycle](../component/life-cycle.md).

## Pages

Applications are divided into multiple pages, similar to HTML pages: each page implements a category of interaction logic, and users can navigate between multiple pages.

A page is an interface element that fills the entire screen, so only one page can be displayed on the device at a time. To support this, the application framework provides a page stack mechanism: each application can open several pages at runtime, which are maintained in a stack manner, displaying only the top-most page at any given time. Because the page stack is a stack, it supports `push` and `pop` operations, through which new pages can be pushed into the application's page stack or the top page can be closed. In addition, the application framework extends several practical page operations.

Most pages reside in the application's page stack. When the application is in the foreground (i.e., it is the currently displayed application), the page at the top of the page stack is displayed, while all pages of background applications are hidden. The page stacks of different applications are completely independent.

A page consists of a **page component** and several sub-components. All pages must be declared in [`manifest.json`](manifest.md#router) before they can be used. Pages within the application navigate and switch via the [`system.router`](/api/system-router.md) API, which includes a routing mechanism and a data transfer method between pages.

Pages use a stack layout by default, just like the [`stack`](/components/stack.md) component. Therefore, using a template like this within a page component:
``` html
<scroll>
  <p>background</p>
</scroll>
<p>overlay</p>
```

has the same effect as placing it inside a `stack` component:
``` html
<stack>
  <scroll>
    <p>Background</p>
  </scroll>
  <p>Overlay</p>
</stack>
```

You can observe this stacking effect using the interactive demo below. You can use your mouse or touchpad to scroll the "Background" text and observe the stacking layer effect.

<glyphix id="application-page-component" height="200" width="300" title="Page Component Stacking Effect">

``` html
<scroll>
  <p>Background</p>
</scroll>
<p>Overlay</p>
```

``` css
p {
  text-align: center;
  color: #f088;
  font-size: 1.5rem;
}

scroll>p {
  height: 100%;
  color: black;
  font-size: 1.25rem;
}
```

</glyphix>

## Components

For details, see [Component Framework](/framework/component/README.md).