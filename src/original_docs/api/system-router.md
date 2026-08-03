# 页面路由

## 导入模块

``` js
import router from '@system.router'
```

## 接口定义

### `push` <decl type="(options: {uri: string, params?: Object}): Promise<any>" method />

跳转到应用内的指定页面。`options` 参数属性说明：
- `uri`：目标页面的名字，必须在 `mainfest.json` 中配置；
- `params`：跳转时需要传递的数据，`params` 参数的属性会替换目标页面的 `data` 属性值。

`push()` 返回一个 Promise 对象，它会在目标页面退出之后兑现并返回自定义的结果。例如：
```js
const result = await router.push({ uri: 'PageName' })
console.log("the page 'PageName' was closed with the result:", result)
```
其中 `result` 是由 [`close()`](#close) 方法指定的页面返回值，你可以通过上面的方法来获取。

::: warning
页面的返回时间通常取决于用户操作，所以 `await router.push()` 可能会等待很长时间。如果不需要获取页面的返回值则不建议通过 `await` 等待页面返回。
:::

当页面为 `singleTask` 启动模式时，跳转到一个已经打开的页面类似于 [`back('<page-name>')`](#back)，见 [`launchMode`](/framework/application/manifest.md#launchmode) <version-badge since="0.8" />。

### `replace` <decl type="(options: {uri: string, params?: Object}): Promise<boolean>" method />

跳转到应用内的指定页面并关闭当前页面。`options` 参数属性说明：
- `uri`：目标页面的名字，必须在 `mainfest.json` 中配置；
- `params`：跳转时需要传递的数据，`params` 参数的属性会替换目标页面的 `data` 属性值。

与 [`push()`](#push) 和 [`back()`](#back) 一样，调用 `replace()` 总是会播放标准的页面转场动画。即使在代码中**立即**调用 `replace()`，只要当前页面已经进入渲染阶段，用户仍然有可能短暂地看到当前页面的一帧画面，然后再进入目标页面。因此，`replace()` 更适合用于“当前页面本身就是用户流程的一部分”的场景，而不适合作为“静默重定向”、“完全隐藏入口页”的手段。

如果当前页面是通过 [`push()`](#push) 方法弹出的，由于 `replace()` 方法会替换当前页面，这会导致 [`push()`](#push) 返回的 Promise 对象兑现。

::: tip
不要使用 [`push()`](#push) 方法跳转到新页面并立即 [`close()`](#close) 当前页面来实现页面替换，这样会打断交互动效，甚至出现画面闪烁。请始终用 `replace()` 方法来替换页面，以保证平滑的页面转场体验。

此外，如果希望某个入口页（例如 `manifest.json` 中配置的 `router.entry` 页面、仅用于分发的隐私检查页等）在部分场景下**完全不展示**，不要在该页面内部调用 `replace()` 试图“立刻跳走”。这类需求应当通过[替换默认页面](#替换默认页面)的方式，在应用启动早期（如 `onCreate()` / `onRoute()`）直接 `push()` 出真正的首屏页面。
:::

`replace()` 常用于[开屏界面跳转](#开屏界面跳转)等场景。

当页面为 `singleTask` 启动模式时，跳转到一个已经打开的页面类似于 [`back('<page-name>')`](#back)，见 [`launchMode`](/framework/application/manifest.md#launchmode) <version-badge since="0.8" />。

### `back` <decl type="(name?: string): Promise<boolean>" method />

返回到名为 `name` 的页面，如果 `name` 为空或者不传递这个参数，`router.back()` 就返回到上一级页面。

调用 `back()` 方法会导致弹出相关页面的 [`push()`](#push) 方法所返回的 Promise 兑现。

### `close` <decl type="(page: Component, result?: any): Promise<void>" method />

关闭指定页面。`page` 是一个页面的 view-model 对象。例如：
``` js
router.close(this.$page)
```

`router.close()` 方法可以关闭应用内的任意页面。如果目标页面位于页面栈顶端，那么 `router.close()` 和 `router.back()` 等效。`router.close()` 还可以正确关闭悬浮页面。

可选参数 `result` 用于指定页面的返回值，即弹出该页面的 [`router.push()`](#push) 或 [`prompt.showPopup()`](system-prompt.md#showpopup) 返回的 Promise 兑现时的结果。考虑到有很多种方法退出页面（如用户侧滑、`router.back()` 方法等），你可以在页面组件的 [`onDestroy()`](/framework/component/life-cycle.md#ondestroy) 生命周期函数中显式调用 `close()` 方法以确保传递页面返回值：
```js
import router from '@system.router'

export default {
  // 这是一个组件对象 ...
  onDestroy() {
    router.close(this.$page, this.pageResult)
  },
  // 假设某个方法会设置页面返回值
  someMethod() {
    this.pageResult = { message: 'some page result' }
  },
}
```

::: tip
在页面 `onDestroy()` 返回前多次对页面调用 `router.close()` 方法**并传递了 `result` 参数**时，仅最后一次调用会生效为页面的返回值。这也是建议在 `onDestroy()` 生命周期函数中通过 `close()` 方法来返回值的原因。
:::

### `clear` <decl type="(): Promise<void>" method />

清空所有底层页面，仅保留顶层页面。调用 `clear()` 方法不会播放页面转场动画。在退出所有底层页面之后兑现本方法返回的 Promise 对象。

### `getPages` <decl type="(): Component[]" method />

获取当前应用页面栈中所有页面的页面组件。

### `getLength` <decl type="(): number" method />

获取当前应用页面栈中页面数量。

### `getPagesName` <decl type="(): String[]" method />

获取当前应用页面栈中所有页面的名称。

### `getPage` <decl type="(index: number): Component | undefined" method />

获取当前应用中由 `index` 指定的页面组件。`index` 是页面的索引（即在页面栈中的位置）。如果查找的页面不存在则返回 `undefined`。

### `getIndex` <decl type="(component: Component): number | undefined" />

获取当前应用中由页面组件 `component` 指定的页面索引。如果查找的页面不存在则返回 `undefined`。

### `queryPage` <decl type="(name: string): Component[]" />

获取页面栈中名为 `name` 的所有页面列表，页面列表和页面栈的顺序相同。

### `queryIndex` <decl type="(name: string): number[]" />

获取页面栈中名为 `name` 的所有页面索引，页面索引值的顺序和页面栈的顺序相同。

## 开发笔记

### 重复弹出页面

错误地使用 `router.push()` 方法可能导致重复弹出同一个页面。考虑这样一个元素：
``` html
<p on:click="onClick">Click Me!</p>
```
当组件的 `onClick()` 事件回调方法只是简单地弹出新页面时不会有任何问题：
``` js
export default{
  onClick() {
    router.push({ uri: 'CoverPage' })
  }
}
```
因为页面在播放转场动画（如果有的话）时不会响应手势，因此不会重复调用 `router.push()`。但是，如果 `onClick()` 在异步操作之后再调用 `router.push()` 就可能出问题，例如：
``` js
export default{
  async onClick() {
    // 这里使用一秒钟的定时器模拟异步操作。真实的异步操作，
    // 如文件读写、网络状态查询也会出现相同的问题
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    // 在异步操作之后再调用 router.push()
    router.push({ uri: 'CoverPage' })
  }
}
```
如果用户在异步操作（示例中为定时器）期间多次点击 “Click Me!” 按钮就会重复弹出页面。你可以尝试下面的 demo 来验证它：

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

首先，请在一秒钟内迅速多次点击 “Click Me!” 按钮，这会导致重复弹出 Cover Page，你可以通过该页面显示的计数来观察重复弹出的次数。

接下来，点击 Cover Page 或者右滑即可返回到上一级页面。此时你会发现：无论怎样快速、连续地点击，页面总是逐个返回，而不会重复操作，因为转场动画期间不会响应手势。

#### 避免异步操作

如果要在手势操作（如 click 手势）的回调函数中跳转页面，应当避免异步操作，因为这不仅容易导致重复弹出页面，还会增加手势响应的延迟。尤其是要注意某些异步操作的延迟是不可控的，例如弱网环境下检查在线状态可能要很长时间。

因此，在需要通过点击触发页面跳转的场景中，最好将可能的网络访问转移到新页面中，并通过加载动画来呈现忙状态。

#### 规避方法

如果必须在手势触发的页面跳转之前进行异步操作，请务必通过特定的标志位来避免重复跳转页面。以前面的 `onClick()` 回调为例：
``` js
export default {
  async onClick() {
    // 添加 isClicked 标志来跳过重复操作，不需要是响应式属性
    if (this.isClicked)
      return
    // 开始执行手势响应逻辑之前标记 isClicked
    this.isClicked = true
    await new Promise((resolve, reject) => {
      setTimeout(resolve, 1000)
    })
    router.push({ uri: 'CoverPage' })
    // 结束执行手势响应逻辑之后清除 isClicked
    this.isClicked = false
  }
}
```
使用相同的方式连续点击 “Click Me!” 按钮将不会重复弹出 Cover Page：

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

这个示例也证实了异步操作确实会增加页面跳转的延迟，在等待定时器超时的一秒钟内用户看不到任何返回！

### 替换默认页面

开发者可能不希望应用在启动时进入 `manifest.json` 的 [`router.entry`](/framework/application/manifest.md#entry) 页面。典型的场景是在通过 deeplink 启动应用时，根据具体的请求参数跳转到特定页面，而不是进入 entry 页面。

除了 deeplink 以外，应用在冷启动时还经常需要根据本地状态选择不同的首屏，例如根据登录态决定进入登录页或首页，或者根据本地存储的隐私协议同意标记决定进入隐私页或功能首页。如果直接把这些页面之一配置为 `router.entry`，再在该页面内部通过 [`router.replace()`](#replace) 跳转，就会在某些情况下短暂显示出不需要的页面，看起来像是页面“闪了一下”。

为此，你只需要在应用启动阶段的 [`onShow()`](/framework/component/life-cycle.md#onshow-1) 生命周期函数调用之前，通过 [`router.push()`](#push) 弹出你真正想要展示的页面即可。通常可以在应用的 [`onCreate()`](/framework/component/life-cycle.md#oncreate) 或 [`onRoute()`](/framework/component/life-cycle.md#onroute) 生命周期函数中完成本地状态检查并跳转首页。例如，`app.ux`/`app.js` 的 `onCreate()` 中同步读取存储的隐私协议状态，然后直接跳转到隐私页或首页：
```js
// app.js
import router from '@system.router'
import storage from '@system.storage'

export default {
  onCreate() {
    const agreed = storage.get('privacyAgreed')
    if (agreed) // 用户已同意隐私协议，直接进入功能首页
      router.push({ uri: 'MainPage' })
    else // 用户尚未同意隐私协议，首屏展示隐私页面
      router.push({ uri: 'PrivacyPage' })
  }
}
```
一旦开发者在应用启动早期手动跳转了页面，本次启动实际显示给用户的**首屏页面**就是通过 `router.push()` 弹出的目标页面，`manifest.json` 中的 `router.entry` 仅作为内部入口使用，不会在界面上短暂闪现。

### 开屏界面跳转

许多应用在首次进入时会显示一个开屏 logo 页面，然后再跳转到实际的功能首页。典型的路由结构是：`router.entry` 指向 logo 页面，logo 页面在初始化时通过 [`router.replace()`](#replace) 跳转到首页。这样，应用启动后用户首先看到短暂的开屏画面，随后看到从开屏页过渡到首页的动画，开屏页在跳转后会从页面栈中移除。
``` js
// 假设这是 logo 页面的 index.ux 脚本
export default {
  onInit() {
    // 在开屏 logo 页面延时一段时间之后跳转
    setTimeout(() => {
      router.replace({ uri: 'MainPage' })
    }, 1000)
  },
}
```
在这种结构下，logo 页面本身就是产品设计的一部分，因此用户短暂看到 logo 再过渡到首页是预期行为。需要注意的是，`replace()` 只能保证从 logo 页面到首页的过渡动画平滑，logo 页面的首帧仍然会出现在屏幕上，无法被“静默”跳过。

如果应用没有设计单独的 logo 或开屏页面，却仍然采用“入口页面 + `replace()` 跳转”的方式，例如将隐私协议页配置为 `router.entry` 并在其中通过 `replace()` 切换到首页，用户就会在冷启动应用时看到该入口页面“闪一下”，然后通过过渡动画切换到 `MainPage`。

::: tip
这种现象是由于路由机制本身决定的，如果你不希望用户观察到“页面切换”。应优先结合[替换默认页面](#替换默认页面)一节中的做法，在应用启动阶段通过 `router.push()` 直接选择最终首屏，而不是在入口页面内部用 `replace()` 把自己替换掉。
:::
