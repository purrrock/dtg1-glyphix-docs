# Lifecycle

Components, pages, and applications all have lifecycles. You can invoke specific features during particular lifecycle stages using **lifecycle functions**.

## Component and Page Lifecycles

Lifecycle functions can be triggered by defining them within component and page objects. For example:
``` html
<script>
export default {
  onInit() {
    console.log("onInit() called!")
  }
}
</script>
```
The `onInit()` lifecycle function is called after the component is instantiated. Lifecycle functions do not take any parameters and do not use return values.

### Component Lifecycle Functions

These lifecycle functions are shared between components and pages.

#### `onInit` <decl type="(): Promise<any> | void" method />

At this point, the component has been instantiated, and the data in the view-model is ready. You can access this data using the `this` keyword. Developer-defined initialization logic is typically executed within this lifecycle function.

#### `onReady` <decl type="(): Promise<any> | void" method />

At this point, the component has been rendered. The component tree now has a corresponding control tree (similar to a DOM tree).

#### `onDestroy` <decl type="(): Promise<any> | void" method />

The component is about to be destroyed. Data in the view-model can still be accessed at this point. Custom resource release operations are typically executed in `onDestroy()`.

### Page Lifecycle Functions

These lifecycle functions only exist in pages.

#### `onShow` <decl type="(): Promise<any> | void" method />

Called when the page is about to be displayed. When returning using `router.back()`, `onShow()` is called when the underlying page is about to be displayed; it is also called before a newly created page is displayed for the first time.

#### `onHide` <decl type="(): Promise<any> | void" method />

Called when the page is about to be hidden. `onHide()` is called when the underlying page is hidden due to a call to `router.push()`. However, the page is not hidden before it is destroyed, so `onHide()` will not be called in that case.

When the device screen is turned off, `onHide()` of the foreground page is also called. For details, see [Screen State Changes](#screen-state-changes).

#### `onBackPress` <decl type="(): boolean" method />

Called when the user swipes back from the edge. Developers can handle the return logic in this function. Returning `true` indicates that the developer has handled the back operation, and the system will not execute the default back behavior; returning `false` indicates that the developer has not handled the back operation, and the system will execute the default back behavior (i.e., close the current page and return to the previous page).

::: warning
This lifecycle function disables interactive edge-swipe navigation (i.e., following the gesture). It is generally **not recommended** to use this lifecycle function, nor should you define a regular method named `onBackPress`. If you want to prevent the default back interaction, please refer to [Default Event Handling for Pages](/framework/generic/properties.md#default-event-handling-for-pages), which preserves interaction animations.
:::

#### `onRefresh` <decl type="(): Promise<any> | void" version="0.8" method />

Called when a page is opened in `singleTask` mode and returns to an existing page. For details, see [`launchMode`](../application/manifest.md#launchmode). Page data can be refreshed in this function.

## Application Lifecycle

### Application Lifecycle Functions

#### `onCreate` <decl type="(): Promise<any> | void" method />

Called when the application is loaded.

#### `onDestroy` <decl type="(): Promise<any> | void" method />

Called when the application is about to be destroyed.

#### `onShow` <decl type="(): Promise<any> | void" method />

Called when the application switches from the background to the foreground. The application's `onShow()` lifecycle function is always called after the page's `onShow()`. When the device screen is turned back on, the foreground application's `onShow()` is also called. For details, see [Screen State Changes](#screen-state-changes).

#### `onHide` <decl type="(): Promise<any> | void" method />

Called before the application is hidden from the foreground to the background.

If you do not want the application to remain active in the background, you can call [`launch.exit()`](/api/system-launch.md#exit) in `onHide()` to exit the application itself. For example:
```js
// in src/app.js
import launch from '@system.launch'

export default {
  onHide() {
    launch.exit()
  },
}
```

The application's `onHide()` lifecycle function is always called after the page's `onHide()`. When the device screen is turned off, the foreground application's `onHide()` is also called. For details, see [Screen State Changes](#screen-state-changes).

#### `onRoute` <decl type="(page: string, query: {[key: string]: string}): Promise<any> | void" method />

Called when the application is launched via a deeplink URI. The parameters `page` and `query` are the decoded URI fields. For example:
``` js
// file: app.ux
export default {
  // Assuming launched via app://example.app/page/to/deeplink?key=value&query=result
  onRoute(page, query) {
    console.log(page)  // Prints string '/page/to/deeplink'
    console.log(query) // Prints object {deeplink: 'key', query: 'result'}
  }
}
```

`onRoute()` is called after `onCreate()` and before `onShow()`. Developers can perform initialization in `onRoute()` based on the parameters specified by the deeplink (such as navigating to a specific page).

#### `onLocaleChanged` <decl type="(locale: {language: string}): void" method />

Called when the application's locale changes. The `locale` parameter is an object containing a `language` field representing the current locale (Language Tag), such as `'en-US'`, `zh-CN`, etc.

## Asynchronous Lifecycle Functions <experimental/>

Lifecycle functions for components, pages, or applications can be asynchronous (i.e., `async` functions or returning a `Promise` object). For example:
``` js
import fs from "@system.file"

export default {
  async onInit() {
    // Wait for asynchronous file reading to complete before proceeding.
    let text = await fs.readText({ uri: "internal://files/test.txt" })
    console.log(text)
  }
}
```
Assuming this is the `onInit()` lifecycle function of a component, component rendering will only proceed after the asynchronous file reading is complete. The following restrictions apply during the execution of asynchronous lifecycle functions:
- Component rendering will not be executed repeatedly, and any operations on reactive properties during this period will not cause UI updates;
- User input is temporarily blocked, and touches and key presses will not be responded to (otherwise, repeated user taps would lead to repeated responses).

The main purpose of asynchronous lifecycle functions is to wait for asynchronous I/O and resource operations, avoiding the premature display of unloads interfaces. In particular, when opening a new page, the system will wait for all of the page's `onInit()`, `onReady()`, and `onShow()` lifecycle functions to complete before displaying the page or playing transition animations.

::: warning
Asynchronous lifecycle functions are currently experimental and may cause various issues, including crashes. Closing a page while it is rendering during the execution of an asynchronous lifecycle function will cause a crash.

Firmware on most devices does not enable support for asynchronous lifecycle functions, and their behavior may not meet expectations. Please use asynchronous lifecycle functions with caution.
:::

## Screen State Changes

Changes in the device's screen state affect the lifecycle function calls of applications and pages. When the device screen is turned off, the `onHide()` lifecycle functions of the foreground application and page are called; when the screen is turned back on, the `onShow()` lifecycle functions of the foreground application and page are called. Developers can use these lifecycle functions to pause or resume network requests to reduce power consumption.

::: tip
Some devices switch applications to the background after the screen is turned off and kill them after a period of time. For applications that need to run continuously in the background, please pay attention to the [Background Management](../application/README.md#background-management) methods for keeping them alive.
:::