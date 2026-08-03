# 应用上下文

## 导入模块

```js
import app from '@system.app'
```

## 接口定义

### `getInfo` <decl type="(): Manifest" method/>

获取当前应用的上下文信息，返回一个 [`Manifest` 对象](./system-package.md#manifest-对象)，包含应用的基本信息，例如包名、版本号等。

### `terminate` <decl type="(): void" method version="0.8"/>

终止当前应用的运行。调用此方法后，应用将被关闭，用户需要重新启动应用才能继续使用。

::: note 兼容性风险
该 API 未在所有平台上支持，可暂时使用 [`launch.exit()`](./system-launch.md#exit) 方法作为替代。
:::

### `loadLibrary` <decl type="(name: string): object | undefined" method/>

按名称加载一个由原生实现注册的 Library Loader，返回对应的库对象。若指定名称的库未注册，则返回 `undefined`。

典型情况下，建议将库对象挂载到 APP 对象上：
```js
// app.js
import app from '@system.app'

export default {
  customLib: app.loadLibrary('custom-library'),
  onCreate() {
    if (!this.customLib) {
      // 处理库加载失败的情况，例如回退到脚本实现
      this.customLib = someStubImplementation();
    } else {
      // 正常使用库对象
      this.customLib.someFunction()
    }
  }
}
```
这样，组件中可以直接使用 `this.$app.customLib` 来访问库对象。

`loadLibrary()` 适用于非标准系统功能的接入，应用可以检测返回值是否为 `undefined` 来判断当前平台是否支持该库，从而在通用模拟器环境中降级到脚本的打桩实现，而不依赖模拟器对特定模块路径的特殊处理。

如果应用需要同时支持标准快应用 API 和系统定制功能，可以根据 `loadLibrary()` 的返回结果决定是否回退。

### `keepForeground` <decl type="(options: { enable: boolean }): void" method/>

设置应用是否保持在前台显示，如果 `options` 参数中的 `enable` 属性为 `true`，则应用会试图保持在前台。

使用该方法需要在 [`manifest.json`](/framework/application/manifest.md#permissions) 文件中声明应用对 `watch.permission.FOREGROUND_SERVICE` 的权限。

该方法只是一个针对系统行为的提示，并不是强制性的，可能因用户操作或其他高优先级策略将应用切换到后台。使用该方法将应用保持在前台时，设备依然可以进入低功耗模式：

- 如果开启 AOD（Always on Display）模式，那么会降低 UI 刷新率。
- 否则，屏幕会在一段时间后关闭，但应用仍然保持在前台运行。

当设备进入低功耗模式后（包括关闭屏幕），前台应用依然会以较低的频率调度并执行，而不是完全休眠。因此可以用于导航或者健身类的应用。
