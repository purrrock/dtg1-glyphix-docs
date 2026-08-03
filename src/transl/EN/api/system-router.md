# Page Routing

## Importing Modules

``` js
import router from '@system.router'
```

## Interface Definitions

### `push` <decl type="(options: {uri: string, params?: Object}): Promise<any>" method />

Navigates to a specified page within the application. Description of `options` parameter properties:
- `uri`: The name of the target page, which must be configured in `manifest.json`;
- `params`: Data to be passed during navigation. The properties of the `params` parameter will replace the `data` property value of the target page.

`push()` returns a Promise object, which is fulfilled after the target page is closed and returns a custom result. For example:
```js
const result = await router.push({ uri: 'PageName' })
console.log("the page 'PageName' was closed with the result:", result)
```
Here, `result` is the page return value specified by the [`close()`](#close) method, which you can obtain using the method above.

::: warning
The return time of a page typically depends on user actions, so `await router.push()` may wait for a long time. If you do not need to get the return value of the page, it is not recommended to use `await` to wait for the page return.
:::

When the page is in the `singleTask` launch mode, navigating to an already opened page is similar to [`back('<page-name>')`](#back). See [`launchMode`](/framework/application/manifest.md#launchmode) <version-badge since="0.8" />.

### `replace` <decl type="(options: {uri: string, params?: Object}): Promise<boolean>" method />

Navigates to a specified page within the application and closes the current page. Description of `options` parameter properties:
- `uri`: The name of the target page, which must be configured in `manifest.json`;
- `params`: Data to be passed during navigation. The properties of the `params` parameter will replace the `data` property value of the target page.

Like [`push()`](#push) and [`back()`](#back), calling `replace()` always plays the standard page transition animation. Even if `replace()` is called **immediately** in the code, as long as the current page has entered the rendering stage, the user may still briefly see a single frame of the current page before entering the target page. Therefore, `replace()` is more suitable for scenarios where "the current page itself is part of the user flow," rather than as a means for "silent redirection" or "completely hiding the entry page."

If the current page was popped via the [`push()`](#push) method, calling `replace()` will replace the current page, which causes the Promise object returned by [`push()`](#push) to be fulfilled.

::: tip
Do not use the [`push()`](#push) method to navigate to a new page and immediately [`close()`](#close) the current page to achieve page replacement, as this will interrupt the interaction animation and may even cause screen flickering. Always use the `replace()` method to replace pages to ensure a smooth page transition experience.

In addition, if you want a certain entry page (such as the `router.entry` page configured in `manifest.json`, a privacy check page used only for dispatching, etc.) to **not be displayed at all** in certain scenarios, do not call `replace()` inside that page in an attempt to "jump away immediately." Such requirements should be handled by [replacing the default page](#replacing-the-default-page), directly pushing (`push()`) the actual first screen page early in the application startup phase (such as `onCreate()` / `onRoute()`).
:::

`replace()` is commonly used in scenarios such as [splash screen navigation](#splash-screen-navigation).

When the page is in the `singleTask` launch mode, navigating to an already opened page is similar to [`back('<page-name>')`](#back). See [`launchMode`](/framework/application/manifest.md#launchmode) <version-badge since="0.8" />.

### `back` <decl type="(name?: string): Promise<boolean>" method />

Returns to the page named `name`. If `name` is empty or omitted, `router.back()` returns to the previous page.

Calling the `back()` method causes the Promise returned by the [`push()`](#push) method of the relevant page to be fulfilled.

### `close` <decl type="(page: Component, result?: any): Promise<void>" method />

Closes the specified page. `page` is the view-model object of a page. For example:
``` js
router.close(this.$page)
```

The `router.close()` method can close any page within the application. If the target page is at the top of the page stack, `router.close()` is equivalent to `router.back()`. `router.close()` can also correctly close floating pages.

The optional parameter `result` is used to specify the return value of the page, which is the result when the Promise returned by [`router.push()`](#push) or [`prompt.showPopup()`](system-prompt.md#showpopup) that popped the page is fulfilled. Considering that there are many ways to exit a page (such as user swiping, the `router.back()` method, etc.), you can explicitly call the `close()` method in the [`onDestroy()`](/framework/component/life-cycle.md#ondestroy) lifecycle hook of the page component to ensure the page return value is passed:
```js
import router from '@system.router'

export default {
  // This is a component object ...
  onDestroy() {
    router.close(this.$page, this.pageResult)
  },
  // Assume a certain method sets the page return value
  someMethod() {
    this.pageResult = { message: 'some page result' }
  },
}
```

::: tip
If `router.close()` is called multiple times on a page before `onDestroy()` returns **with the `result` parameter passed**, only the last call will take effect as the return value of the page. This is why it is recommended to return values via the `close()` method in the `onDestroy()` lifecycle hook.
:::

### `clear` <decl type="(): Promise<void>" method />

Clears all underlying pages, leaving only the top-level page. Calling the `clear()` method does not play page transition animations. The Promise object returned by this method is fulfilled after all underlying pages are exited.

### `getPages` <decl type="(): Component[]" method />

Gets the page components of all pages in the current application page stack.

### `getLength` <decl type="(): number" method />

Gets the number of pages in the current application page stack.

### `getPagesName` <decl type="(): String[]" method />

Gets the names of all pages in the current application page stack.

### `getPage` <decl type="(index: number): Component | undefined" method />

Gets the page component specified by `index` in the current application. `index` is the index of the page (i.e., its position in the page stack). Returns `undefined` if the searched page does not exist.

### `getIndex` <decl type="(component: Component): number | undefined" />

Gets the page index specified by the page component `component` in the current application. Returns `undefined` if the searched page does not exist.

### `queryPage` <decl type="(name: string): Component[]" />

Gets a list of all pages named `name` in the page stack. The order of the page list is the same as that of the page stack.

### `queryIndex` <decl type="(name: string): number[]" />

Gets the indices of all pages named `name` in the page stack. The order of the page index values is the same as that of the page stack.

## Development Notes

### Repeated Page Pushing

Incorrect use of the `router.push()` method may lead to repeatedly pushing the same page. Consider such an element:
``` html
<p on:click="onClick">Click Me!</p>
```
There is no issue when the component's `onClick()` event callback method simply pushes a new page:
``` js
export default{
  onClick() {
    router.push({ uri: 'CoverPage' })
  }
}
```
Because the page does not respond to gestures while playing transition animations (if any), `router.push()` will not be called repeatedly. However, if `onClick()` calls `router.push()` after an asynchronous operation, issues may arise, for example:
``` js
export default{
  async onClick() {
    // A one-second timer is used here to simulate an asynchronous operation. Real asynchronous operations,
    // such as file read/write or network status queries, will encounter the same issue
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    // Call router.push() after the asynchronous operation
    router.push({ uri: 'CoverPage' })
  }
}
```
If the user clicks the "Click Me!" button multiple times during the asynchronous operation (the timer in the example), the page will be pushed repeatedly. You can try the following demo to verify it:

<glyphix id="api-router-push-repeat-1" height="100" inline>

``` html
<div class="window">
  <p class="button" on:click="onClick">Click Me!</p>
</div>
```

``` css
.window {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #e5e5e5;
  border-radius: 12px;
}

.button {
  border: 2px solid gray;
  border-radius: 20%;
  padding: 8px;
}
```

``` js
import router from '@system.router'

export default {
  async onClick() {
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    router.push({ uri: 'CoverPage' })
  }
}
```

</glyphix>

First, click the "Click Me!" button rapidly multiple times within one second. This will cause the Cover Page to be pushed repeatedly, and you can observe the number of repeated pushes through the counter displayed on that page.

Next, click the Cover Page or swipe right to return to the previous page. At this point, you will find that no matter how fast or continuously you click, the pages always return one by one without duplicate operations, because gestures are not responded to during transition animations.

#### Avoiding Asynchronous Operations

If you need to navigate pages within the callback function of a gesture operation (such as a click gesture), asynchronous operations should be avoided, as this not only easily leads to repeated page pushing, but also increases gesture response latency. In particular, note that the latency of certain asynchronous operations is uncontrollable, such as checking online status in a poor network environment, which may take a long time.

Therefore, in scenarios where page navigation needs to be triggered by a click, it is best to move potential network accesses to the new page and present a busy state via loading animations.

#### Workarounds

If asynchronous operations must be performed before a gesture-triggered page navigation, be sure to use a specific flag to prevent repeated page navigation. Taking the `onClick()` callback above as an example:
``` js
export default {
  async onClick() {
    // Add an isClicked flag to skip duplicate operations; does not need to be a reactive property
    if (this.isClicked)
      return
    // Mark isClicked before executing gesture response logic
    this.isClicked = true
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    router.push({ uri: 'CoverPage' })
    // Clear isClicked after executing gesture response logic
    this.isClicked = false
  }
}
```
Using the same method to continuously click the "Click Me!" button will no longer repeatedly push the Cover Page:

<glyphix id="api-router-push-repeat-2" height="100" inline>

``` html
<div class="window">
  <p class="button" on:click="onClick">Click Me!</p>
</div>
```

``` css
.window {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #e5e5e5;
  border-radius: 12px;
}

.button {
  border: 2px solid gray;
  border-radius: 20%;
  padding: 8px;
}
```

``` js
import router from '@system.router'

export default {
  async onClick() {
    if (this.isClicked)
      return
    this.isClicked = true
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    router.push({ uri: 'CoverPage' })
    this.isClicked = false
  }
}
```

</glyphix>

This example also confirms that asynchronous operations indeed increase page navigation latency—users cannot see any return during the one-second wait for the timer to time out!

### Replacing the Default Page

Developers may not want the application to enter the [`router.entry`](/framework/application/manifest.md#entry) page of `manifest.json` upon startup. A typical scenario is when starting the application via a deeplink, where it should navigate to a specific page based on specific request parameters instead of entering the entry page.

In addition to deeplinks, applications during cold startup often need to select different first screens based on local state, such as deciding whether to enter the login page or home page based on the login state, or entering the privacy page or functional home page based on the locally stored privacy agreement consent flag. If one of these pages is directly configured as `router.entry` and then [`router.replace()`](#replace) is used inside that page to navigate, unwanted pages will be briefly displayed in certain scenarios, looking like the page "flashed."

To solve this, you only need to push (`router.push()`) the page you actually want to display before the [`onShow()`](/framework/component/life-cycle.md#onshow-1) lifecycle hook is called during the application startup phase. Typically, local state checks and home page navigation can be completed in the [`onCreate()`](/framework/component/life-cycle.md#oncreate) or [`onRoute()`](/framework/component/life-cycle.md#onroute) lifecycle hooks of the application. For example, synchronously read the stored privacy agreement state in `onCreate()` of `app.ux`/`app.js`, and then directly navigate to the privacy page or home page:
```js
// app.js
import router from '@system.router'
import storage from '@system.storage'

export default {
  onCreate() {
    const agreed = storage.get('privacyAgreed')
    if (agreed) // User has agreed to the privacy policy, enter the functional home page directly
      router.push({ uri: 'MainPage' })
    else // User has not yet agreed to the privacy policy, display the privacy page on the first screen
      router.push({ uri: 'PrivacyPage' })
  }
}
```
Once the developer manually navigates pages early in the application startup, the actual **first screen page** displayed to the user for this startup is the target page pushed via `router.push()`. `router.entry` in `manifest.json` is used only as an internal entry and will not flash briefly on the interface.

### Splash Screen Navigation

Many applications display a splash logo page when first entered, and then navigate to the actual functional home page. A typical routing structure is: `router.entry` points to the logo page, and the logo page navigates to the home page via [`router.replace()`](#replace) upon initialization. Thus, after the application starts, the user first sees a brief splash screen, followed by the animation transitioning from the splash page to the home page, and the splash page is removed from the page stack after navigation.
``` js
// Assuming this is the index.ux script of the logo page
export default {
  onInit() {
    // Navigate after a delay on the splash logo page
    setTimeout(() => {
      router.replace({ uri: 'MainPage' })
    }, 1000)
  },
}
```
Under this structure, the logo page itself is part of the product design, so users briefly seeing the logo and then transitioning to the home page is expected behavior. Note that `replace()` can only ensure that the transition animation from the logo page to the home page is smooth; the first frame of the logo page will still appear on the screen and cannot be skipped "silently."

If the application is not designed with a separate logo or splash page, but still adopts the "entry page + `replace()` navigation" approach—such as configuring the privacy agreement page as `router.entry` and switching to the home page via `replace()` inside it—the user will see that entry page "flash" when cold-starting the application, and then switch to `MainPage` via a transition animation.

::: tip
This phenomenon is determined by the routing mechanism itself. If you do not want users to observe "page switching," you should prioritize incorporating the approach in the [Replacing the Default Page](#replacing-the-default-page) section, directly selecting the final first screen via `router.push()` during the application startup phase, rather than replacing itself inside the entry page using `replace()`.
:::