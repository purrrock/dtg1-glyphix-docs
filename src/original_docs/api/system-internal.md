# 内部接口

`system.internal` 模块提供一些供系统使用的内部接口，该模块只能在 launcher 应用中使用。

## 导入模块

``` js
import internal from '@system.internal'
```

## API

### `globalComponent` <decl type="(name: string, uri: string): void" method />

注册一个[全局组件](/framework/component/README.md#全局组件)，全局组件可以在所有应用中引入。参数 `name` 是全局组件的名字，`uri` 是全局组件 UX 文件相对于当前源文件的路径或 URI。例如
``` js
internal.globalComponent('TopBar', '/global/TopBar.ux')
```
之后在所有应用中都可以用 `<import name="TopBar" />` 来引用全局组件 `TopBar`。

`globalComponent()` 方法最好在 launcher 应用的 `app.js` 执行阶段执行，这样可以在任何界面加载之前就注册全局组件信息。

### `setDefaultKeyHandler` <decl type="(handler: (event: KeyEvent) => void): void" method />

注册系统的默认按键处理程序，参数 `handler` 是一个回调函数。`KeyEvent` 类型原型为：
``` ts
interface KeyEvent  {
  type: 'keydown' | 'keyup', // 按键事件的类型
  key: string, // 按键名称
  timestamp: number, // 按键事件上报的时间戳，单位是毫秒
}
```
默认按键处理程序只能注册一次，因为多次注册会覆盖前面的操作。
