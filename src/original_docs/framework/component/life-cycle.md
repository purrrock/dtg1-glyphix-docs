# 生命周期

组件、页面和应用都有生命周期。可以通过**生命周期函数**在对象的特定生命周期阶段调用指定的功能。

## 组件和页面的生命周期

在组件和页面对象中定义生命周期函数即可触发调用。例如：
``` html
<script>
export default {
  onInit() {
    console.log("onInit() called!")
  }
}
</script>
```
`onInit()` 生命周期函数会在组件实例化之后调用。生命周期函数都没有参数，也不使用返回值。

### 组件生命周期函数

这些生命周期函数是组件和页面共有的。

#### `onInit` <decl type="(): Promise<any> | void" method />

此时组件已经实例化，且 view-model 中的数据已经准备好，可以通过 `this` 关键字访问其中的数据。通常在此生命周期函数中执行开发者自定义的初始化逻辑。

#### `onReady` <decl type="(): Promise<any> | void" method />

此时组件已经渲染完成。此时的组件树具有对应的控件树（类似于 DOM 树）。

#### `onDestroy` <decl type="(): Promise<any> | void" method />

组件准备销毁。此时仍可以访问 view-model 中的数据。通常在在 `onDestroy()` 中执行自定义的资源释放操作。

### 页面生命周期函数

这些生命周期函数只存在于页面中。

#### `onShow` <decl type="(): Promise<any> | void" method />

页面即将显示时调用。使用 `router.back()` 返回时，底层的页面即将显示时会调用 `onShow()`；刚创建的新页面在第一次显示之前也会调用 `onShow()`。

#### `onHide` <decl type="(): Promise<any> | void" method />

页面即将隐藏时调用。使用 `router.push()` 时导致底层页面隐藏时会调用 `onHide()`。但是页面销毁之前并不会隐藏页面，因此不会调用 `onHide()`。

设备屏幕关闭时，前台页面的 `onHide()` 也会被调用，详见[屏幕状态变化](#屏幕状态变化)。

#### `onBackPress` <decl type="(): boolean" method />

当用户侧滑返回时调用此生命周期函数。开发者可以在此函数中处理返回逻辑。如果返回 `true`，表示开发者已经处理了返回操作，系统不会执行默认的返回行为；如果返回 `false`，表示开发者没有处理返回操作，系统会执行默认的返回行为（即关闭当前页面并返回到上一个页面）。

::: warning
此生命周期函数会导致交互式侧滑返回（即跟手侧滑）被禁用。通常**不建议**使用此生命周期函数，也不要定义名为 `onBackPress` 的普通方法。如果希望阻止默认的返回交互，请参考[页面的默认事件处理](/framework/generic/properties.md#页面的默认事件处理)，这样可以保留交互动效。
:::

#### `onRefresh` <decl type="(): Promise<any> | void" version="0.8" method />

当页面以 `singleTask` 模式打开并回到已经存在的页面时会调用此生命周期函数，详见 [`launchMode`](../application/manifest.md#launchmode)。可以在此函数中刷新页面数据。

## 应用生命周期

### 应用生命周期函数

#### `onCreate` <decl type="(): Promise<any> | void" method />

应用加载时调用此生命周期函数。

#### `onDestroy` <decl type="(): Promise<any> | void" method />

应用将要销毁时调用此生命周期函数。

#### `onShow` <decl type="(): Promise<any> | void" method />

应用从后台切换到前台显示时调用此生命周期函数。应用的 `onShow()` 生命周期函数总是在页面的 `onShow()` 之后调用。设备屏幕重新打开时，前台应用的 `onShow()` 也会被调用，详见[屏幕状态变化](#屏幕状态变化)。

#### `onHide` <decl type="(): Promise<any> | void" method />

应用从前台隐藏到后台前调用此生命周期函数。

如果你不希望应用在后台保持活动，可以在 `onHide()` 中调用 [`launch.exit()`](/api/system-launch.md#exit) 来退出应用自身。例如：
```js
// in src/app.js
import launch from '@system.launch'

export default {
  onHide() {
    launch.exit()
  },
}
```

应用的 `onHide()` 生命周期函数总是在页面的 `onHide()` 之后调用。设备屏幕关闭时，前台应用的 `onHide()` 也会被调用，详见[屏幕状态变化](#屏幕状态变化)。

#### `onRoute` <decl type="(page: string, query: {[key: string]: string}): Promise<any> | void" method />

通过 deeplink URI 启动应用时会调用 `onRoute` 生命周期函数。参数 `page` 和 `query` 是解码后的 URI 字段。例如：
``` js
// file: app.ux
export default {
  // 假设通过 app://example.app/page/to/deeplink?key=value&query=result
  onRoute(page, query) {
    console.log(page)  // 打印字符串 '/page/to/deeplink'
    console.log(query) // 打印对象 {deeplink: 'key', query: 'result'}
  }
}
```

`onRoute()` 会在 `onCreate()` 之后，`onShow()` 之前调用。开发者可以在 `onRoute()` 中根据 deeplink 指定的参数进行初始化（例如跳转到特定的页面）。

#### `onLocaleChanged` <decl type="(locale: {language: string}): void" method />

当应用的语言环境发生变化时调用此生命周期函数。参数 `locale` 是一个对象，包含 `language` 字段，表示当前的语言环境（Language Tag），如 `'en-US'`、`zh-CN` 等。

## 异步生命周期函数 <experimental/>

组件、页面或者应用的生命周期函数可以是异步的，即 `async` 函数或者返回 `Promise` 对象。例如
``` js
import fs from "@system.file"

export default {
  async onInit() {
    // 等待异步的文件读取完成再继续执行。
    let text = await fs.readText({ uri: "internal://files/test.txt" })
    console.log(text)
  }
}
```
假设这是某个组件的 `onInit()` 生命周期函数，那么它会在异步的文件读取完成后才会继续执行组件渲染。在异步生命周期函数执行期间存在以下限制：
- 不会重复执行组件渲染，在此期间任何对响应式属性的操作不会导致界面更新；
- 暂时屏蔽用户输入，触摸和按键都不会响应（否则用户如果反复点击会导致重复响应）。

异步生命周期函数的主要作用是等待异步的 IO 和资源操作，避免过早地显示未加载好的界面。特别是打开新页面时会等待页面的 `onInit()`、`onReady()` 和 `onShow()` 生命周期函数全部执行完才会开始显示页面或播放转场动画。

::: warning
目前异步生命周期函数是实验性的，它们可能引起包括崩溃在内的各种问题。在异步生命周期函数调用过程中关闭正在渲染的页面会导致崩溃。

大部分设备的固件没有启用异步生命周期函数的支持，它们的行为可能不符合预期。请谨慎使用异步生命周期函数。
:::

## 屏幕状态变化

设备的屏幕状态变化会影响应用和页面的生命周期函数调用。当设备屏幕关闭时，前台应用和页面的 `onHide()` 生命周期函数会被调用；当屏幕重新打开时，前台应用和页面的 `onShow()` 生命周期函数会被调用。开发者可以利用这些生命周期函数来暂停或恢复网络请求，以降低功耗。

::: tip
部分设备在关闭屏幕后会将应用切换到后台，并在一段时间后杀死应用。对于需要持续后台运行的应用，需要注意[后台](../application/README.md#后台管理)保活的方法。
:::
