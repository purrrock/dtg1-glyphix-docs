# life cycle


Components, pages, and applications all have life cycles. Specified functions can be called at specific life cycle stages of the object through **lifecycle functions**.


## Component and page lifecycle


Defining lifecycle functions in component and page objects can trigger calls. For example:
``` html
<script>
export default {
  onInit() {
    console.log("onInit() called!")
  }
}
</script>
```
The `onInit()` lifecycle function will be called after the component is instantiated. Lifecycle functions have no parameters and do not use return values.


### Component life cycle functions


These lifecycle functions are common to components and pages.


#### `onInit` <decl type="(): Promise<any> | void" method />


At this point, the component has been instantiated and the data in the view-model is ready. The data can be accessed through the `this` keyword. Developer-defined initialization logic is usually executed in this life cycle function.


#### `onReady` <decl type="(): Promise<any> | void" method />


At this point the component has been rendered. The component tree at this time has a corresponding control tree (similar to the DOM tree).


#### `onDestroy` <decl type="(): Promise<any> | void" method />


The component is ready for destruction. The data in the view-model can still be accessed at this point. Custom resource release operations are usually performed in `onDestroy()`.


### Page life cycle functions


These lifecycle functions only exist within the page.


#### `onShow` <decl type="(): Promise<any> | void" method />


Called when the page is about to be displayed. When returning using `router.back()`, `onShow()` will be called when the underlying page is about to be displayed; `onShow()` will also be called before the new page just created is displayed for the first time.


#### `onHide` <decl type="(): Promise<any> | void" method />


Called when the page is about to be hidden. `onHide()` is called when using `router.push()` causes the underlying page to be hidden. However, the page will not be hidden until it is destroyed, so `onHide()` will not be called.


When the device screen is closed, `onHide()` of the foreground page will also be called, see [Screen status changes](#屏幕状态变化) for details.


#### `onBackPress` <decl type="(): boolean" method />


This lifecycle function is called when the user swipes back. Developers can handle return logic in this function. If `true` is returned, it means that the developer has processed the return operation, and the system will not perform the default return behavior; if `false` is returned, it means that the developer has not processed the return operation, and the system will perform the default return behavior (that is, close the current page and return to the previous page).


::: warning

This lifecycle function causes interactive slide returns (i.e. follow-up slides) to be disabled. It is generally not recommended to use this lifecycle function, nor to define a normal method named `onBackPress`. If you want to prevent the default return interaction, please refer to [The default event handling of the page](/framework/generic/properties.md#页面的默认事件处理), so that the interaction effect can be preserved.
:::



#### `onRefresh` <decl type="(): Promise<any> | void" version="0.8" method />


This life cycle function is called when the page is opened in `singleTask` mode and returned to an existing page. See [`launchMode`](../application/manifest.md#launchmode) for details. Page data can be refreshed in this function.


## Application life cycle


### Application life cycle functions


#### `onCreate` <decl type="(): Promise<any> | void" method />


This lifecycle function is called when the app loads.


#### `onDestroy` <decl type="(): Promise<any> | void" method />


This lifecycle function is called when the app is about to be destroyed.


#### `onShow` <decl type="(): Promise<any> | void" method />


This lifecycle function is called when the app switches from the background to the foreground. The application's `onShow()` lifecycle function is always called after the page's `onShow()`. When the device screen is reopened, the `onShow()` of the foreground application will also be called, see [Screen status changes](#屏幕状态变化) for details.


#### `onHide` <decl type="(): Promise<any> | void" method />


This lifecycle function is called before the app is hidden from the foreground to the background.


If you don't want your app to remain active in the background, you can call [`launch.exit()`](/api/system-launch.md#exit) in `onHide()` to exit the app itself. For example:
```js
// in src/app.js
import launch from '@system.launch'

export default {
  onHide() {
    launch.exit()
  },
}
```


The application's `onHide()` lifecycle function is always called after the page's `onHide()`. When the device screen is turned off, `onHide()` of the foreground application will also be called, see [Screen status changes](#屏幕状态变化) for details.


#### `onRoute` <decl type="(page: string, query: {[key: string]: string}): Promise<any> | void" method />


The `onRoute` lifecycle function is called when the application is launched via a deeplink URI. Parameters `page` and `query` are decoded URI fields. For example:
``` js
// file: app.ux
export default {
  // Assume that through app:// example.app /page/to/deeplink?key=value&query=result
  onRoute(page, query) {
    console.log(page)  // Print the string '/page/to/deeplink'
    console.log(query) // Print object {deeplink: 'key', query: 'result'}
  }
}
```


`onRoute()` will be called after `onCreate()` and before `onShow()`. Developers can initialize in `onRoute()` based on the parameters specified by deeplink (such as jumping to a specific page).


#### `onLocaleChanged` <decl type="(locale: {language: string}): void" method />


This lifecycle function is called when the app's locale changes. Parameter `locale` is an object containing the `language` field, which represents the current language environment (Language Tag), such as `'en-US'`, `zh-CN`, etc.


## Asynchronous life cycle function <experimental/>


Component, page or application lifecycle functions can be asynchronous, i.e. `async` functions or return `Promise` objects. For example
``` js
import fs from "@system.file"

export default {
  async onInit() {
    // Wait for the asynchronous file reading to complete before continuing execution.
    let text = await fs.readText({ uri: "internal://files/test.txt" })
    console.log(text)
  }
}
```
Assuming this is the `onInit()` life cycle function of a component, it will continue to perform component rendering only after the asynchronous file reading is completed. The following limitations exist during asynchronous lifecycle function execution:
- Component rendering will not be performed repeatedly, and any operation on responsive properties during this period will not cause the interface to be updated;
- Temporarily blocking user input, touch and key presses will not respond (otherwise if the user clicks repeatedly, it will cause repeated responses).


The main function of the asynchronous life cycle function is to wait for asynchronous IO and resource operations to avoid prematurely displaying an unloaded interface. Especially when opening a new page, it will wait until the page's `onInit()`, `onReady()` and `onShow()` life cycle functions are all executed before starting to display the page or play the transition animation.


::: warning

Asynchronous lifecycle functions are currently experimental and they can cause various issues including crashes. Closing the rendering page during an asynchronous lifecycle function call will cause a crash.


The firmware of most devices does not enable support for asynchronous lifecycle functions, and their behavior may not be as expected. Use asynchronous lifecycle functions with caution.
:::



## Screen status changes


Changes in the device's screen status will affect the life cycle function calls of applications and pages. When the device screen is turned off, the `onHide()` life cycle function of the foreground application and page will be called; when the screen is reopened, the `onShow()` life cycle function of the foreground application and page will be called. Developers can use these lifecycle functions to pause or resume network requests to reduce power consumption.


::: tip

Some devices will switch apps to the background after turning off the screen and kill the app after a while. For applications that need to continue running in the background, you need to pay attention to the [Backstage](../application/README.md#后台管理) method of keeping alive.
:::
