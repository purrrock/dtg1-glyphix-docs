# 包管理

本模块提供资源包的安装和卸载功能。

## 导入模块

``` js
import pkg from '@system.package'
```

由于 `package` 是 JavaScript 的关键字且不能作为作为变量名，我们可以将 `"@system.package"` 模块导出到 `pkg` 变量。

## 接口定义

### `install` <decl function type="(options: { src: string }): Promise<void>" />

从文件系统中安装一个应用或者表盘包。参数 `options` 的 `src` 属性是即将安装的资源包文件 URI。

如果资源包是一个应用资源包，那么在使用 `pkg.install({ src: 'package-uri' })` 安装该资源包之后可以由 [`launch()`](system-launch.md#launch-launch-app) 启动，并可以使用 [`app`](/framework/application/resource.md#app) URI 协议来访问包中的内容。

`src` 是即将安装的资源包文件的 URI。安装的包必须是有效的应用或者表盘包，也就是要有 [`manifest.json`](/framework/application/manifest.md) 文件。安装之后的包名由 [`manifest.package`](/framework/application/manifest.md#package) 决定。

安装后可以使用 [`prc`](/framework/application/resource.md#prc) 协议访问来访问资源包中的资源，对于应用资源包还可以用 `app` 协议来访问。

如果待安装的包已经存在，那么会进行升级操作。如果升级的应用正在运行，那么会先退出该应用，此后也可以调用 [`launch()`](system-launch.md#launch-launch-app) 再次启动。

安装的包可以由 [`remove()`](#remove) API 删除。

### `remove`<decl type="(options: { package: string }): Promise<void>" function />

删除由 [`install()`](#install) 安装的资源包。参数 `options` 的 `package` 属性为待删除的资源包名，即 [`manifest.package`](/framework/application/manifest.md#package) 字段。

在删除资源包之前应先关闭相关的资源，例如销毁相关组件并关闭相关页面等。`remove()` 函数会自动关闭资源包对应的应用（如果是应用资源包）。

::: warning
必须用 `remove()` 而不要直接使用文件系统 API 删除资源包，因为后者不会清理资源缓存并且无法正确删除安装信息。
:::

### `getInfo` <decl type="(query?: string | Query): Manifest | undefined" method/>

获取应用包的 manifest 信息。可选参数 `query` 可以是一个包名字符串，也可以是更复杂的 `Query` 对象：
``` ts
type Query = {
  package: string,                 // 待查询的包名
  options?: ('dial' | 'widgets')[] // 可选查询字段
}
```
如果 `package` 字段所指定的包存在 `getInfo()` 将返回包的 `Manifest` 信息，否则返回 `undefined`。当不指定 `query` 参数时，`getInfo()` 将返回当前应用的 manifest 信息。

#### `Manifest` 对象

返回的 `Manifest` 对象基本上是 [`manifest.json`](/framework/application/manifest.md) 的子集：
``` ts
type Query = {
  type: 'app' | 'dial', // 包类型，可能是应用或者表盘包
  name: string,         // 包名
  versionName: string,  // 版本名
  versionCode: number,  // 版本编号
  icon?: string,        // 应用图片路径，只有应用包才存在此字段
  dial?: {              // 可选字段：表盘信息，只有表盘包才有此信息
    component: string,  // 表盘组件的路径
    preview: string     // 表盘预览图的路径
  },
  widgets?: {           // 可选字段：挂件和小组件信息
    name: string,       // 挂件/小组件名字
    component: string,  // 挂件/小组件路径
    preview: string     // 挂件/小组件预览图
  }[]
}
```
`Manifest` 对象的 `dial` 和 `widgets` 是可选字段，他们是否存在由 `Query.options` 的内容决定。例如
``` js
pkg.getInfo({
  package: 'com.example.app',
  options: ['dial', 'widgets']
})
```
将会使结果的 `Manifest` 包含 `dial` 和 `widgets` 字段（不过应用包总是不包含 `dial` 字段）。

当 `query` 参数是一个字符串时等效于 `options` 选项为空，即
``` ts
pkg.getInfo('com.example.app')
pkg.getInfo({ package: 'com.example.app' })
```
的结果都一样，这种情况下返回的 `Manifest` 对象不包含可选字段。

当不指定 `query` 参数时，可以通过 `getInfo()` 返回本应用的信息：
``` js
let manifest = pkg.getInfo()
console.log(manifest)
```

### `list` <decl function type="(type?: 'app' | 'dial'): string[]" />

获取所有已安装的应用或表盘包名列表。

### `countOf` <decl function type="(type?: 'app' | 'dial'): string[]" />

获取已经安装的应用或者表盘数量。
