# Page routing

## Import module

``` js
import router from '@system.router'
```

## Interface definition

### `push` <decl type="(options: {uri: string, params?: Object}): Promise<any>" method />

Jump to the specified page within the application. `options` parameter attribute description:
- `uri`: the name of the target page, which must be configured in `mainfest.json`;
- `params`: The data that needs to be passed when jumping. The attribute of the `params` parameter will replace the `data` attribute value of the target page.

`push()` returns a Promise object that will be honored and return a custom result after the target page exits. For example:
```js
const result = await router.push({ uri: 'PageName' })
console.log("the page 'PageName' was closed with the result:", result)
```
Where `result` is the page return value specified by the [`close()`](#close) method, which you can obtain through the above method.

::: warning
The return time of the page usually depends on user actions, so `await router.push()` may wait for a long time. If you do not need to obtain the return value of the page, it is not recommended to wait for the page to return through `await`.
:::

When the page is in `singleTask` launch mode, jumping to an already opened page is similar to [`back('<page-name>')`](#back), see [`launchMode`](/framework/application/manifest.md#launchmode) <version-badge since="0.8" />.

### `replace` <decl type="(options: {uri: string, params?: Object}): Promise<boolean>" method />

Jump to the specified page in the application and close the current page. `options` parameter attribute description:
- `uri`: the name of the target page, which must be configured in `mainfest.json`;
- `params`: The data that needs to be passed when jumping. The attribute of the `params` parameter will replace the `data` attribute value of the target page.

Like [`push()`](#push) and [`back()`](#back) , calling `replace()` always plays the standard page transition animation. Even if `replace()` is called **immediately** in the code, as long as the current page has entered the rendering stage, the user may still briefly see a frame of the current page before entering the target page. Therefore, `replace()` is more suitable for use in scenarios where "the current page itself is part of the user flow", rather than as a means of "silent redirection" or "complete hiding of the entry page".

If the current page is popped up through the [`push()`](#push) method, since the `replace()` method will replace the current page, this will cause the Promise object returned by [`push()`](#push) to be fulfilled.

::: tip
Do not use the [`push()`](#push) method to jump to a new page and immediately [`close()`](#close) the current page to replace the page. This will interrupt the interactive effect and even cause the screen to flicker. Please always use the `replace()` method to replace pages to ensure a smooth page transition experience.

In addition, if you want an entry page (such as the `router.entry` page configured in `manifest.json`, the privacy check page only for distribution, etc.) to be **not displayed at all** in some scenarios, do not call `replace()` inside the page in an attempt to "jump away immediately". For such requirements, you should use [Replace Default Page](#Replace Default Page) to directly `push()` the real first-screen page early in the application startup (such as `onCreate()` / `onRoute()`).
:::

`replace()` is often used in scenarios such as [Jump to the screen-opening interface](#Jump to the screen-opening interface).

When the page is in `singleTask` launch mode, jumping to an already opened page is similar to [`back('<page-name>')`](#back), see [`launchMode`](/framework/application/manifest.md#launchmode) <version-badge since="0.8" />.

### `back` <decl type="(name?: string): Promise<boolean>" method />

Return to the page named `name`. If `name` is empty or this parameter is not passed, `router.back()` will return to the previous page.

Calling the `back()` method will cause the Promise returned by the [`push()`](#push) method to pop up the relevant page to be fulfilled.

### `close` <decl type="(page: Component, result?: any): Promise<void>" method />

Close the specified page. `page` is the view-model object of a page. For example:
``` js
router.close(this.$page)
```

The `router.close()` method can close any page within the application. If the target page is at the top of the page stack, then `router.close()` and `router.back()` are equivalent. `router.close()` can also correctly close floating pages.

The optional parameter `result` is used to specify the return value of the page, that is, the result of the Promise returned by [`router.push()`](#push) or [`prompt.showPopup()`](system-prompt.md#showpopup) that pops up the page. Considering that there are many ways to exit the page (such as user sliding, `router.back()` method, etc.), you can explicitly call the `close()` method in the [`onDestroy()`](/framework/component/life-cycle.md#ondestroy) life cycle function of the page component to ensure that the page return value is passed:
```js
import router from '@system.router'

export default {
  // This is a component object...
  onDestroy() {
    router.close(this.$page, this.pageResult)
  },
  // Assume that a method will set the page return value
  someMethod() {
    this.pageResult = { message: 'some page result' }
  },
}
```

::: tip
When the `router.close()` method** is called multiple times on the page before the page `onDestroy()` returns and the `result` parameter** is passed, only the last call will take effect as the return value of the page. This is why it is recommended to return values ​​through the `close()` method in the `onDestroy()` life cycle function.
:::

### `clear` <decl type="(): Promise<void>" method />

Clear all bottom-level pages, leaving only the top-level pages. Calling the `clear()` method will not play the page transition animation. The Promise object returned by this method is honored after exiting all underlying pages.

### `getPages` <decl type="(): Component[]" method />

Get the page components of all pages in the current application page stack.

### `getLength` <decl type="(): number" method />

Get the number of pages in the current application page stack.

### `getPagesName` <decl type="(): String[]" method />

Get the names of all pages in the current application page stack.

### `getPage` <decl type="(index: number): Component | undefined" method />

Get the page component specified by `index` in the current application. `index` is the index of the page (i.e. the position in the page stack). If the page being searched does not exist, `undefined` is returned.

### `getIndex` <decl type="(component: Component): number | undefined" />

Get the page index specified by the page component `component` in the current application. If the page being searched does not exist, `undefined` is returned.

### `queryPage` <decl type="(name: string): Component[]" />

Get a list of all pages named `name` in the page stack. The order of the page list and the page stack is the same.

### `queryIndex` <decl type="(name: string): number[]" />

Get all page indexes named `name` in the page stack. The order of page index values ​​​​is the same as the order of the page stack.

## Development Notes

### Repeat pop-up page

Improper use of the `router.push()` method may cause the same page to pop up repeatedly. Consider an element like this:
``` html
<p on:click="onClick">Click Me!</p>
```
There is no problem when the component's `onClick()` event callback method simply pops up the new page:
``` js
export default{
  onClick() {
    router.push({ uri: 'CoverPage' })
  }
}
```
Because the page does not respond to gestures while the transition animation (if any) is playing, `router.push()` is not called repeatedly. However, problems may occur if `onClick()` is called after an asynchronous operation and then called `router.push()`, for example:
``` js
export default{
  async onClick() {
    //A one-second timer is used here to simulate asynchronous operations. True asynchronous operation,
    // The same problem will also occur when reading and writing files and querying network status.
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    // Call router.push() after the asynchronous operation
    router.push({ uri: 'CoverPage' })
  }
}
```
If the user clicks the "Click Me!" button multiple times during an asynchronous operation (a timer in the example), the page will pop up repeatedly. You can try the following demo to verify it:

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

First, please click the "Click Me!" button quickly and multiple times within one second, which will cause the Cover Page to pop up repeatedly. You can observe the number of repeated popups through the count displayed on the page.

Next, click Cover Page or swipe right to return to the previous page. At this point you will find that no matter how quickly and continuously you click, the pages will always return one by one without repeating the operation, because the gesture will not respond during the transition animation.

#### Avoid asynchronous operations

If you want to jump to a page in the callback function of a gesture operation (such as a click gesture), you should avoid asynchronous operations, because this will not only easily cause the page to pop up repeatedly, but also increase the delay of gesture response. In particular, please note that the delay of some asynchronous operations is uncontrollable. For example, checking the online status may take a long time in a weak network environment.

Therefore, in scenarios where page jumps need to be triggered by clicks, it is best to transfer possible network access to the new page and present the busy status through loading animation.

#### Avoidance methods

If an asynchronous operation must be performed before a gesture-triggered page jump, be sure to use a specific flag to avoid repeated page jumps. Take the previous `onClick()` callback as an example:
``` js
export default {
  async onClick() {
    // Add isClicked flag to skip repeated operations, does not need to be a reactive attribute
    if (this.isClicked)
      return
    // Mark isClicked before starting to execute gesture response logic
    this.isClicked = true
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    router.push({ uri: 'CoverPage' })
    // Clear isClicked after finishing executing gesture response logic
    this.isClicked = false
  }
}
```
Using the same method to continuously click the "Click Me!" button will not pop up the Cover Page repeatedly:

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

This example also confirms that asynchronous operations will indeed increase the delay of page jumps. The user will not see any return within one second of waiting for the timer to expire!

### Replace default page

Developers may not want the application to enter the [`router.entry`](/framework/application/manifest.md#entry) page of `manifest.json` when it starts. A typical scenario is when starting an application through deeplink, jumping to a specific page based on specific request parameters instead of entering the entry page.

In addition to deeplink, applications often need to select different home screens based on local status during cold start, such as deciding to enter the login page or home page based on the login status, or deciding to enter the privacy page or functional home page based on the locally stored privacy agreement consent mark. If you directly configure one of these pages as `router.entry`, and then jump within the page through [`router.replace()`](#replace), the unnecessary page will be displayed briefly in some cases, and it will look like the page "flashes".

To do this, you only need to pop up the page you really want to display through [`router.push()`](#push) before calling the [`onShow()`](/framework/component/life-cycle.md#onshow-1) life cycle function in the application startup phase. You can usually complete the local status check and jump to the homepage in the application's [`onCreate()`](/framework/component/life-cycle.md#oncreate) or [`onRoute()`](/framework/component/life-cycle.md#onroute) life cycle function. For example, in `onCreate()` of `app.ux`/`app.js`, the stored privacy agreement status is synchronously read, and then jumps directly to the privacy page or home page:
```js
// app.js
import router from '@system.router'
import storage from '@system.storage'

export default {
  onCreate() {
    const agreed = storage.get('privacyAgreed')
    if (agreed) // The user has agreed to the privacy agreement and goes directly to the function homepage
      router.push({ uri: 'MainPage' })
    else // The user has not agreed to the privacy agreement, and the privacy page is displayed on the first screen
      router.push({ uri: 'PrivacyPage' })
  }
}
```
Once the developer manually jumps to the page in the early stage of application startup, the **first screen page** actually displayed to the user during this startup is the target page popped up through `router.push()`. `router.entry` in `manifest.json` is only used as an internal entry and will not flash briefly on the interface.

### Jump to the opening screen interface

Many apps will display an opening logo page when first entering, and then jump to the actual functional homepage. The typical routing structure is: `router.entry` points to the logo page, and the logo page jumps to the homepage through [`router.replace()`](#replace) during initialization. In this way, after the application is launched, the user first sees a brief opening screen, and then sees an animation transitioning from the opening page to the homepage. The opening page will be removed from the page stack after the jump.
``` js
// Assume this is the index.ux script of the logo page
export default {
  onInit() {
    // Jump to the opening logo page after a period of delay
    setTimeout(() => {
      router.replace({ uri: 'MainPage' })
    }, 1000)
  },
}
```
Under this structure, the logo page itself is part of the product design, so it is expected behavior for users to briefly see the logo and then transition to the homepage. It should be noted that `replace()` can only ensure a smooth transition animation from the logo page to the homepage. The first frame of the logo page will still appear on the screen and cannot be "silently" skipped.

If the application does not design a separate logo or opening page, but still uses the "entry page + `replace()` jump" method, for example, configure the privacy agreement page as `router.entry` and switch to the homepage through `replace()`, the user will see the entry page "flash" when cold starting the application, and then switch to `MainPage` through a transition animation.

::: tip
This phenomenon is due to the routing mechanism itself. If you don't want users to observe "page switching". Priority should be given to combining the practices in the [Replace Default Page](#Replace Default Page) section to directly select the final first screen through `router.push()` during the application startup phase, instead of using `replace()` to replace yourself inside the entry page.
:::
