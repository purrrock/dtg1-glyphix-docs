# The manifest File

The `manifest.json` file contains information such as application descriptions, interface declarations, and page routing.

`manifest.json` is a JSON file, and its content must be a JSON Object. This document introduces the functions of each field in `manifest.json`.

## Field Descriptions

### Root Properties

These fields are properties of the root JSON object in the `manifest.json` file.

::: details Type Signature
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

The `package` field is the application's package name and is a mandatory field. It is recommended to use the format `com.company.module`, such as `com.example.demo`. Application package names must be unique within the system.

::: important
App stores of many device manufacturers do not support hyphens `-` as part of the package name, so please avoid them. We also do not recommend using underscores `_` or `.` as substitutes; in such cases, simply connect the words directly, e.g., `com.wateralert.demo`.
:::

#### `name` <decl type="string" />

The display name of the application, a mandatory field. It should be within 6 Chinese characters and match the name saved in the app store. It is used to display the app name on desktop icons, pop-up windows, etc. This field can use `${}` expressions to reference [internationalized strings](i18n.md), for example:
``` json
{
  "name": "${appName}"
}
```
Here, `appName` is a key for an internationalized string. Internationalized application names allow the device's application list to display the application name in the current language rather than a fixed language.

#### `icon` <decl type="string" />

The path to the application icon, for example, `/assets/icon.png`.

#### `versionName` <decl type="string" />

The application version string.

#### `versionCode` <decl type="number" />

The application version code, which is an integer. It is recommended to increment the version code by one every time an application is released.

#### `config` <decl type="?: Config" />

An optional field describing system configuration information, see [`Config` Object](#config-object).

#### `permissions` <decl type="?: PermissionInfo[]" />

An array consisting of `PermissionInfo` objects, representing the list of permissions used by the application. When the application needs to access location information, sensors, device information, audio recording, Bluetooth, health data, and other capabilities, the corresponding permissions must be declared in this field, for example:

``` json
{
  "permissions": [
    { "name": "watch.permission.LOCATION" },
    { "name": "watch.permission.RECORD" }
  ]
}
```
The `PermissionInfo` object describes the permission information required by the application. It currently only has a `name` field. Its signature is as follows:
``` ts
type PermissionInfo = {
  name: string; // Permission name, uniquely identifies a permission item
}
```
The `name` field identifies the specific permission name. The permission names correspond to the system module interface list as follows:

| Permission Name                       | Corresponding System Module                         | Permission Description                           |
| ------------------------------------- | --------------------------------------------------- | ------------------------------------------------ |
| `watch.permission.FOREGROUND_SERVICE` | [`@system.app`](/api/system-app.md)                 | Keep the application running in the foreground   |
| `watch.permission.LOCATION`           | [`@system.geolocation`](/api/system-geolocation.md) | Location information                             |
| `watch.permission.ACCESS_SENSORS`     | [`@system.compass`](/api/system-sensor.md)         | Built-in sensors (e.g., compass, accelerometer)  |
| `watch.permission.DEVICE_INFO`        | [`@system.device`](/api/system-device.md)           | Device information                               |
| `watch.permission.RECORD`             | [`@system.media`](/api/system-media.md)             | Audio recording related APIs only require permissions |
| `watch.permission.BLUETOOTH`          | [`@system.bluetooth.ble`](/api/system-ble.md)       | Allow using device Bluetooth                     |
| `watch.permission.READ_HEALTH_DATA`   | Not supported yet                                   | Read health data (e.g., step count, heart rate)  |
| `watch.permission.SCHEDULE`           | [`@system.schedule`](/api/system-schedule.md)       | Set scheduled tasks                              |
| `watch.permission.NOTIFICATION`       | [`@system.notification`](/api/system-notified.md)   | Allow application notification reminders         |

#### `router` <decl type="Router" />

A mandatory field describing page routing information within the application, see [`Router` Object](#router-object) for details.

#### `display` <decl type="?: Display" />

Configuration for display effects within the application, see [`Display` Object](#display-object) for details.

#### `dial` <decl type="?: Dial" />

If the `dial` field is present, it indicates that this project is a watch face package rather than an application. Exclusive watch face metadata is described by the [`Dial` Object](#dial-object). Watch face packages do not use the [`icon`](#icon) field.

#### `widgets` <decl type="?: Widget[]" />

Represents the configuration information for the list of widgets and small components. For configuration fields, see [`Widget` Object](#widget-object).

### `Config` Object

::: details Type Signature
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

The baseline width for page design (in pixels), with a default value of `750`. The `px` length unit in CSS will be scaled based on the ratio of the actual device width to `designWidth`. For example, when `designWidth` is `466`, pixel lengths on a device with an actual width of `410` pixels will be scaled by a factor of $410/466$.

It is recommended to use the screen size of the device currently being designed for, rather than the default `750`, to avoid a large amount of conversion during development.

#### `designImageScale` <decl type="?: number" />

The scaling factor for sliced image resources, with a default value of $1.0$. To meet multi-device resolution adaptation, designers need to scale images up according to the design draft before slicing to ensure quality after packaging.

`designImageScale` is the ratio between the size of the original resource image in the project and the logical resolution of the scaled image. Specifically, the scaling factor $\it{scale}$ of the resource image on the actual device is:
$$
\it{scale} = \tt{designImageScale}\frac{\tt{deviceWidth}}{\tt{designWidth}}
$$
Where $\tt{deviceWidth}$ is the actual width of the device screen. Therefore, the actual display size $(w', h')$ of the image is:
$$
(w', h') = \it{scale} \cdot (w, h)
$$
Where $(w, h)$ is the size of the original resource image.

::: tip
Do not use a `designImageScale` configuration smaller than $1$, as this means resource images will be enlarged during packaging, resulting in noticeable blurring and distortion. If you want your application to display images exquisitely across multiple devices, you should prepare resource images at a larger size than actually required and set the correct `designImageScale` parameter.

For example, if the image size displayed on the actual device (assuming $\tt{designWidth} == \tt{deviceWidth}$) is $96\rm px \times 96\rm px$, you can prepare $192\rm px \times 192\rm px$ assets with twice the resolution and set `designImageScale` to $2$.
:::

#### `fontFaces` <decl type="?: string" />

Specifies the file path of the application-level font mapping table, where fonts defined within it can be used directly in the application. This path can be a relative path to `manifest.json` or an absolute path relative to the root directory of the application resource package.

Refer to [Font Configuration](font-config.md).

#### `assets` <decl type="?: string | string[]" />

Specifies the path glob patterns (file wildcards) for custom resources. For example:
``` json
{
  "config": {
    "assets": [ "assets/**", "**/data.bin" ]
  }
}
```
This will package all files under the `assets` directory in the project and all `data.bin` files in the project. These files will only be packaged in the form of static resource files (i.e., copied directly).

File wildcards can be the same as paths, but have the following special forms:
- `*` matches a single path component, excluding path separators (`/`).
- `**` matches any number of path components and can include path separators.

For example:
- `test.js` can match the `test.js` file in the root directory of the project.
- `**/*-data.bin` can match files with the `-data.bin` suffix under any path.
- `*/*.bin` matches files with the `.bin` suffix under any level of directory in the project root.

### `Router` Object

Defines the composition of pages and related configuration information.

::: details Type Signature
``` ts
interface Router {
  entry?: string,
  pages: { [name: string]: PageInfo }
}
```
:::

#### `entry` <decl type="?: string" />

The name of the application home page. When the application starts, it will first navigate to this page. Defaults to `"main"`.

#### `pages` <decl type="{ [name: string]: PageInfo }" />

Declares the information for each page. The key `name` of the `pages` property is the page name, and the property value, the [`PageInfo` Object](#pageinfo-object), is the detailed configuration information of the page. For example:
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

All pages in the application must be entered into the routing table before they can be used, and each page must also have a unique name.

### `Display` Object

#### `pageAnimation` <decl type="?: PageAnimation" />

The default transition animation configuration for pages within the application. The value is a [`PageAnimation` Object](#pageanimation-object).

## `PageInfo` Object

The page configuration object is the property value of the `router.pages` object. The type of the page configuration object is Object. This section introduces the property field definitions of the page configuration object.

::: details Type Signature
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

The path of the page directory (the path of the folder storing page components). Defaults to the same as the page name, which is the key of the `Router` object.

#### `component` <decl type="?: string" />

The name of the page component, which matches the UX file name without the *.ux* extension. For example, the component name `"index"` corresponds to the `index.ux` file.

#### `pageAnimation` <decl type="?: PageAnimation" />

The transition animation configuration of the page, whose value is a [`PageAnimation` Object](#pageanimation-object). This configuration has a higher priority than the `display.pageAnimation` configuration in `manifest.json`.

#### `launchMode` <decl type="?: 'standard' | 'singleTask'" version="0.8" />

The launch mode of the page, defaulting to `standard`. When a page's `launchMode` is configured as `singleTask`, if you attempt to open a page instance that is already in the back stack, all page instances above that instance will be popped out of the stack, returning to the page where that instance resides (similar to [`router.back('<page-name>')`](/api/system-router.md#back)), rather than creating a new page instance.

When "opening" and returning to an existing page in `singleTask` mode, the [`onRefresh`](../component/life-cycle.md#onrefresh) lifecycle function is triggered.

### `PageAnimation` Object

The properties of this object configure the behavior of page transition animations. Transition animations are only valid for the top-most page; non-top pages will not play transition animations.

::: details Type Signature
``` ts
interface PageAnimation {
  openEnter?: string,
  closeEnter?: string,
  openExit?: string,
  closeExit?: string
}
```
:::

Each property can take the following values:
- `"none"`: No transition animation, which is the default value for all properties.
- `"slide"`: The page transitions with a sliding animation. This transition effect varies under different transition configuration properties:
  - For `openEnter` transitions, the slide effect is that the page enters from the left side of the screen towards the right until it completely covers the screen.
  - For `closeExit` transitions, the slide effect is that the page starts sliding to the right from a position completely covering the screen until it completely leaves the screen.
  - For `closeEnter` and `openExit` transitions, the slide effect has no animation.

Default transition animations for pages and applications are defined by the device. If `manifest.json` does not specify fields related to `pageAnimation`, some devices may not play transition animations, while other devices may use manufacturer-customized animation effects.

::: warning
The simulator always plays slide page transition animations, regardless of which device it is simulating. If you want to ensure that page transition animations are disabled, use syntax like:
``` json
{
  "pageAnimation": { "openEnter": "none" }
}
```
Rather than `"pageAnimation": {}`, as the latter does not take effect for unknown reasons.
:::

#### `openEnter` <decl type="?: string" />

This property configures the transition animation of the new page when opening a new page.

#### `closeEnter` <decl type="?: string" />

This property configures the transition animation of the old page underneath that will be covered when opening a new page.

#### `openExit` <decl type="?: string" />

This property configures the exit transition animation of the closed page when closing a page.

#### `closeExit` <decl type="?: string" />

This property configures the transition animation of the page that is about to be re-displayed underneath the closed page when closing a page.

### `Dial` Object

The `Dial` object describes configuration information related to watch faces.

::: details Type Signature
``` ts
interface Dial {
  component: string,
  preview: string
}
```
:::

#### `component` <decl type="string" />

The path of the watch face entry component. It can be an absolute path within the package or a relative path to the `manifest.json` file.

#### `preview` <decl type="string" />

The path of the watch face preview image. It can be an absolute path within the package or a relative path to the `manifest.json` file.

### `Widget` Object

The `Widget` object describes configuration information for widgets or small components.

::: details Type Signature
``` ts
interface Widget {
  name: string,
  component: string,
  preview: string
}
```
:::

#### `name` <decl type="string" />

The name of the widget/small component. Widgets within the same application package cannot have duplicate names.

#### `component` <decl type="string" />

The path of the widget/small component entry component. It can be an absolute path within the package or a relative path to the `manifest.json` file.

#### `preview` <decl type="string" />

The path of the widget/small component preview image. It can be an absolute path within the package or a relative path to the `manifest.json` file.