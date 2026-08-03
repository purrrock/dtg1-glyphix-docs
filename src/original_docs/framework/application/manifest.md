# manifest 文件

`manifest.json` 文件中包含了应用描述、接口声明、页面路由等信息。

`manifest.json` 是一个 JSON 文件，且文件内容必须是一个 JSON Object，本文档会介绍 `manifest.json` 各个字段的功能。

## 字段说明

### 根属性

这些字段是 `manifest.json` 文件根 JSON 对象的属性。

::: details 类型签名
``` ts
interface Manifest {
  package: string,
  name: string,
  icon: string,
  versionName: string,
  versionCode: number,
  config?: Config,
  permissions?: PermissionInfo[],
  router: Router,
  display?: Display,
  dial?: Dial,
  widgets?: Widget[]
}
```
:::

#### `package` <decl type="string" />

`package` 字段是应用的包名，必填字段。推荐采用 `com.company.module` 的格式，如：`com.example.demo`。系统中的应用包名必须唯一。

::: important
许多设备厂商的应用商店不支持短横线 `-` 作为包名的一部分，请注意避免。我们也不推荐使用下划线 `_` 或 `.` 来替代，这种情况请直接连接单词，例如 `com.wateralert.demo`。
:::

#### `name` <decl type="string" />

应用的显示名称，必填字段。6 个汉字以内，与应用商店保存的名称一致，用于在桌面图标、弹窗等处显示应用名称。该字段可以用 `${}` 表达式来引用[国际化字符串](i18n.md)，例如：
``` json
{
  "name": "${appName}"
}
```
中 `appName` 就是一个国际化字符串的键。国际化的应用名可以让设备的应用列表以当前语言显示应用名称，而不是固定的语言。

#### `icon` <decl type="string" />

应用图标的路径，例如 `/assets/icon.png`。

#### `versionName` <decl type="string" />

应用版本字符串。

#### `versionCode` <decl type="number" />

应用版本代码，是一个整数。建议在每次发布应用时将版本代码加一。

#### `config` <decl type="?: Config" />

描述系统配置信息的可选字段，见 [`Config` 对象](#config-对象)。

#### `permissions` <decl type="?: PermissionInfo[]" />

由 `PermissionInfo` 对象组成的数组，表示应用使用的权限列表。当应用需要访问位置信息、传感器、设备信息、录音、蓝牙、健康数据等能力时，需要在此字段中声明对应的权限，例如：

``` json
{
  "permissions": [
    { "name": "watch.permission.LOCATION" },
    { "name": "watch.permission.RECORD" }
  ]
}
```
`PermissionInfo` 对象描述应用所需权限信息，它目前只有一个 `name` 字段。其签名如下：
``` ts
type PermissionInfo = {
  name: string; // 权限名称，唯一标识一个权限项
}
```
`name` 字段标识具体的权限名称。权限名对应系统模块接口清单如下:

| 权限名称                              | 对应系统模块                                        | 权限描述                         |
| ------------------------------------- | --------------------------------------------------- | -------------------------------- |
| `watch.permission.FOREGROUND_SERVICE` | [`@system.app`](/api/system-app.md)                 | 保持应用在前台运行               |
| `watch.permission.LOCATION`           | [`@system.geolocation`](/api/system-geolocation.md) | 位置信息                         |
| `watch.permission.ACCESS_SENSORS`     | [`@system.compass`](/api/system-sensor.md)         | 内置传感器(如指南针、加速度计等) |
| `watch.permission.DEVICE_INFO`        | [`@system.device`](/api/system-device.md)           | 设备信息                        |
| `watch.permission.RECORD`             | [`@system.media`](/api/system-media.md)             | 仅录音相关 API 需要权限          |
| `watch.permission.BLUETOOTH`          | [`@system.bluetooth.ble`](/api/system-ble.md)       | 允许使用设备蓝牙                |
| `watch.permission.READ_HEALTH_DATA`   | 暂不支持                                            | 读取健康数据(如步数、心率等)     |
| `watch.permission.SCHEDULE`           | [`@system.schedule`](/api/system-schedule.md)       | 设置定时任务                   |
| `watch.permission.NOTIFICATION`       | [`@system.notification`](/api/system-notified.md)   | 允许应用通知提醒                |

#### `router` <decl type="Router" />

描述应用内页面路由信息的必填字段，详见 [`Router` 对象](#router-对象)。

#### `display` <decl type="?: Display" />

应用内的显示效果配置，详见 [`Display` 对象](#display-对象)。

#### `dial` <decl type="?: Dial" />

如果存在 `dial` 字段则表示此项目是一个表盘包而不是应用。表盘的专属元数据由 [`Dial` 对象](#dial-对象)描述。表盘包 [`icon`](#icon) 不使用字段。

#### `widgets` <decl type="?: Widget[]" />

表示挂件和小组件列表的配置信息，配置字段详见 [`Widget` 对象](#widget-对象)。

### `Config` 对象

::: details 类型签名
``` ts
interface Config {
  designWidth?: number,
  designImageScale?: number,
  fontFaces?: string,
  assets?: string | string[]
}
```
:::

#### `designWidth` <decl type="?: number" />

页面设计的基准宽度（单位是像素），默认值为 `750`。CSS 中的 `px` 长度单位会根据实际的设备宽度和 `designWidth` 的比值来缩放。例如当 `designWidth` 的值为 `466` 时，在实际宽度为 `410` 像素的设备上像素长度会被缩放 $410/466$ 倍。

建议使用当前设计的设备尺寸，而不是默认的 `750`，以避免在开发中做大量的换算。

#### `designImageScale` <decl type="?: number" />

图片资源的切图缩放系数，默认值为 $1.0$。为了满足多设备分辨率适配，需要设计师将图片按照设计稿放大后切图来保证打包后的质量。

`designImageScale` 是项目中资源原图的尺寸和缩放后图片逻辑分辨率的比值。具体来说，资源图片在实际设备上的缩放系数 $\it{scale}$ 为：
$$
\it{scale} = \tt{designImageScale}\frac{\tt{deviceWidth}}{\tt{designWidth}}
$$
其中 $\tt{deviceWidth}$ 为设备屏幕的实际宽度。因此，图片的实际显示尺寸 $(w', h')$ 为：
$$
(w', h') = \it{scale} \cdot (w, h)
$$
其中 $(w, h)$ 是资源原图的尺寸。

::: tip
不要使用小于 $1$ 的 `designImageScale` 配置，这意味着打包时会对资源图片进行放大，并因此产生明显的模糊和失真。如果你希望应用可以在多种设备中精致地显示图片，应该按照比实际需求更大的尺寸来准备资源图片，并设置正确的 `designImageScale` 参数。

例如，如果实际设备（假设 $\tt{designWidth} == \tt{deviceWidth}$）上显示的图片尺寸为 $96\rm px \times 96\rm px$，那么可以准备两倍分辨率的 $192\rm px \times 192\rm px$ 素材，并将 `designImageScale` 设置为 $2$。
:::

#### `fontFaces` <decl type="?: string" />

指定应用级的字体映射表文件路径，其中定义的字体可在应用中直接使用。此路径可以是相对于 `manifest.json` 的相对路径，也可以是相对于应用资源包根目录的绝对路径。

参考[字体配置](font-config.md)。

#### `assets` <decl type="?: string | string[]" />

指定自定义资源的路径 glob 模式（文件通配符）。例如：
``` json
{
  "config": {
    "assets": [ "assets/**", "**/data.bin" ]
  }
}
```
会将项目中 `assets` 目录下的所有文件和项目中所有的 `data.bin` 文件进行打包。这些文件只会按照静态资源文件的形式打包（即直接拷贝文件）。

文件通配符可以和路径相同，但是有以下特殊形式：
- `*` 匹配一个路径组件，但不包含路径分隔符（`/`）。
- `**` 匹配任意数量的路径组建，并可以包含路径分隔符。

例如：
- `test.js` 可以匹配项目跟目录下的 `test.js` 文件。
- `**/*-data.bin` 可以匹配任意路径下具有 `-data.bin` 后缀的文件。
- `*/*.bin` 匹配项目根中任意一级目录下具有 `.bin` 后缀的文件。

### `Router` 对象

定义页面的组成和相关配置信息。

::: details 类型签名
``` ts
interface Router {
  entry?: string,
  pages: { [name: string]: PageInfo }
}
```
:::

#### `entry` <decl type="?: string" />

应用首页的名称，启动应用后会先跳转到此页面。默认为 `"main"`。

#### `pages` <decl type="{ [name: string]: PageInfo }" />

声明各个页面的信息。 `pages` 属性的键 `name` 是页面名称，属性值 [`PageInfo` 对象](#pageinfo-对象)是页面的详细配置信息。例如：
``` json
{
  "router": {
    "entry": "Main",
    "pages": {
      "Main": {
        "path": "/Path/To/Main",
        "component": "index",
        "launchMode": "singleTask"
      }
    }
  }
}
```

应用中所有的页面都必须填写到路由表中才可以使用，每个页面也必须具有唯一的名字。

### `Display` 对象

#### `pageAnimation` <decl type="?: PageAnimation" />

应用内页面的默认转场动画配置，值是 [`PageAnimation` 对象](#pageanimation-对象)。

## `PageInfo` 对象

页面配置对象是 `router.pages` 对象的属性值。页面配置对象的类型是 Object。本节介绍页面配置对象的属性字段定义。

::: details 类型签名
``` ts
interface PageInfo {
  path?: string,
  component?: string,
  pageAnimation?: PageAnimation,
  launchMode?: 'standard' | 'singleTask'
}
```
:::

#### `path` <decl type="?: string" />

页面目录的路径（存放页面组件的文件夹的路径）。默认和页面名称相同，即 `Router` 对象的键。

#### `component` <decl type="?: string" />

页面组件的名称，和 UX 文件名一致并且不需要 *.ux* 后缀名，例如组件名 `"index"` 对应 `index.ux` 文件。

#### `pageAnimation` <decl type="?: PageAnimation" />

页面的转场动画配置，值是 [`PageAnimation` 对象](#pageanimation-对象)。此配置的优先级高于 `mainfest.json` 中的 `display.pageAnimation` 配置。

#### `launchMode` <decl type="?: 'standard' | 'singleTask'" version="0.8" />

页面的启动模式，默认为 `standard`。当页面的 `launchMode` 配置为 `singleTask` 时，如果要打开一个已经在返回栈中的页面实例，则会将该实例上方的页面全部出栈，并回到该实例所在的页面（类似于 [`router.back('<page-name>')`](/api/system-router.md#back)），而不是创建一个新的页面实例。

在以 `singleTask` 模式“打开”并回到已经存在的页面时，会触发 [`onRefresh`](../component/life-cycle.md#onrefresh) 生命周期函数。

### `PageAnimation` 对象

此对象的属性配置页面转场动画的行为。转场动画只对顶部的页面有效，非顶部的页面是不会播放转场动画的。

::: details 类型签名
``` ts
interface PageAnimation {
  openEnter?: string,
  closeEnter?: string,
  openExit?: string,
  closeExit?: string
}
```
:::

每个属性都可以取以下值：
- `"none"`：无转场动画，这是所有属性的默认值
- `"slide"`：页面以滑动动画进行转场，此转场效果在不同的转场配置属性下有所不同，其中：
  - 对于 `openEnter` 转场，slide 效果是页面从屏幕左边向右开始进入，直到完全覆盖屏幕
  - 对于 `closeExit` 转场，slide 效果是页面从完全覆盖屏幕的位置开始向右滑动，直到完全离开屏幕
  - 对于 `closeEnter` 和 `openExit` 转场，slide 效果是没有动画的

页面和应用的默认转场动画是由设备定义的。如果 `manifest.json` 中没有指定 `pageAnimation` 相关的字段，某些设备可能不播放转场动画，而另一些设备则可能使用厂商定制的动画效果。

::: warning
模拟器总会播放 slide 页面转场动画，而无论它在模拟哪一款设备。如果想确保关闭页面的转场动画，请使用
``` json
{
  "pageAnimation": { "openEnter": "none" }
}
```
这样的写法，而不是 `"pageAnimation": {}`，后者由于未知原因不生效。
:::

#### `openEnter` <decl type="?: string" />

这个属性配置打开新页面时，新页面的转场动画。

#### `closeEnter` <decl type="?: string" />

这个属性配置打开新页面时，底下将被覆盖的旧页面的转场动画。

#### `openExit` <decl type="?: string" />

这个属性配置关闭页面时，被关闭页面的退出转场动画。

#### `closeExit` <decl type="?: string" />

这个属性配置关闭页面时，被关闭页面底下将要重新显示页面的转场动画。

### `Dial` 对象

`Dial` 对象描述表盘相关的配置信息。

::: details 类型签名
``` ts
interface Dial {
  component: string,
  preview: string
}
```
:::


#### `component` <decl type="string" />

表盘入口组件的路径。可以是包中的绝对路径或相对于 `manifest.json` 文件的相对路径。

#### `preview` <decl type="string" />

表盘预览图片的路径。可以是包中的绝对路径或相对于 `manifest.json` 文件的相对路径。

### `Widget` 对象

`Widget` 对象描述挂件或小组件的配置信息。

::: details 类型签名
``` ts
interface Widget {
  name: string,
  component: string,
  preview: string
}
```
:::

#### `name` <decl type="string" />

挂件/小部件的名字，同一个应用包内的小部件不能重名。

#### `component` <decl type="string" />

挂件/小部件入口组件的路径。可以是包中的绝对路径或相对于 `manifest.json` 文件的相对路径。

#### `preview` <decl type="string" />

挂件/小部件预览图片的路径。可以是包中的绝对路径或相对于 `manifest.json` 文件的相对路径。
