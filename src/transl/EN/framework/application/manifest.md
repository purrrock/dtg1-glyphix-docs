# manifest file


The `manifest.json` file contains application description, interface declaration, page routing and other information.


`manifest.json` is a JSON file, and the file content must be a JSON Object. This document will introduce the functions of each field of `manifest.json`.


## Field description


### root attribute


These fields are properties of the `manifest.json` file root JSON object.


::: details type signature
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


The `package` field is the application package name and is a required field. It is recommended to use the `com.company.module` format, such as: `com.example.demo`. Application package names in the system must be unique.


::: important

Many device manufacturers' app stores do not support the dash `-` as part of the package name, so please avoid this. We also do not recommend using underscores `_` or `.` instead, in which case please connect the words directly, such as `com.wateralert.demo`.
:::



#### `name` <decl type="string" />


Display name of the application, required field. Within 6 Chinese characters, consistent with the name saved in the app store, used to display the app name on desktop icons, pop-up windows, etc. The field can be referenced using the `${}` expression [Internationalized string](i18n.md), for example:
``` json
{
  "name": "${appName}"
}
```
where `appName` is the key of an internationalized string. Internationalized application names allow the device's application list to display application names in the current language instead of a fixed language.


#### `icon` <decl type="string" />


The path to the application icon, such as `/assets/icon.png`.


#### `versionName` <decl type="string" />


Application version string.


#### `versionCode` <decl type="number" />


The application version code is an integer. It is recommended to increase the version code by one every time you publish your app.


#### `config` <decl type="?: Config" />


Optional field describing system configuration information, see [`Config` object](#config-对象).


#### `permissions` <decl type="?: PermissionInfo[]" />


An array of `PermissionInfo` objects representing the list of permissions used by the application. When an application needs to access location information, sensors, device information, recording, Bluetooth, health data, etc., it needs to declare the corresponding permissions in this field, for example:


``` json
{
  "permissions": [
    { "name": "watch.permission.LOCATION" },
    { "name": "watch.permission.RECORD" }
  ]
}
```
The `PermissionInfo` object describes the permission information required by the application. It currently has only one `name` field. Its signature is as follows:
``` ts
type PermissionInfo = {
  name: string; // Permission name, uniquely identifies a permission item
}
```
The `name` field identifies the specific permission name. The system module interface list corresponding to the permission name is as follows:


| Permission name | Corresponding system module | Permission description |
| ------------------------------------- | --------------------------------------------------- | -------------------------------- |

| `watch.permission.FOREGROUND_SERVICE` | [`@system.app`](/api/system-app.md) | Keep the application running in the foreground |
| `watch.permission.LOCATION` | [`@system.geolocation`](/api/system-geolocation.md) | Location information |
| `watch.permission.ACCESS_SENSORS` | [`@system.compass`](/api/system-sensor.md) | Built-in sensors (such as compass, accelerometer, etc.) |
| `watch.permission.DEVICE_INFO` | [`@system.device`](/api/system-device.md) | Device information |
| `watch.permission.RECORD` | [`@system.media`](/api/system-media.md) | Only recording related APIs require permissions |
| `watch.permission.BLUETOOTH` | [`@system.bluetooth.ble`](/api/system-ble.md) | Allow device Bluetooth |
| `watch.permission.READ_HEALTH_DATA` | Not supported yet | Read health data (such as steps, heart rate, etc.) |
| `watch.permission.SCHEDULE` | [`@system.schedule`](/api/system-schedule.md) | Set up scheduled tasks |
| `watch.permission.NOTIFICATION` | [`@system.notification`](/api/system-notified.md) | Allow app notification reminders |


#### `router` <decl type="Router" />


A required field describing page routing information within the application. See [`Router` object](#router-对象) for details.


#### `display` <decl type="?: Display" />


For display effect configuration within the application, see [`Display` object](#display-对象) for details.


#### `dial` <decl type="?: Dial" />


If the `dial` field is present, it indicates that this project is a watch face package rather than an application. The watch face's unique metadata is described by [`Dial` object](#dial-对象). The dial package [`icon`](#icon) does not use fields.


#### `widgets` <decl type="?: Widget[]" />


Represents the configuration information of the widget and widget list. For details on the configuration fields, see [`Widget` object](#widget-对象).


### `Config` object


::: details type signature
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


The base width of the page design (unit is pixels), the default value is `750`. The `px` length unit in CSS scales based on the ratio of the actual device width to `designWidth`. For example, when the value of `designWidth` is `466`, the pixel length will be scaled $410/466$ times on a device with an actual width of `410` pixels.


It is recommended to use the currently designed device size instead of the default `750` to avoid doing a lot of conversions during development.


#### `designImageScale` <decl type="?: number" />


The image scaling factor of image resources. The default value is $1.0$. In order to meet the resolution adaptation of multiple devices, the designer needs to enlarge the picture according to the design draft and then cut the picture to ensure the quality after packaging.


`designImageScale` is the ratio of the size of the original resource image in the project to the logical resolution of the scaled image. Specifically, the scaling factor $\it{scale}$ of the resource image on the actual device is:
$$

\it{scale} = \tt{designImageScale}\frac{\tt{deviceWidth}}{\tt{designWidth}}

$$

Where $\tt{deviceWidth}$ is the actual width of the device screen. Therefore, the actual display size $(w', h')$ of the image is:
$$

(w', h') = \it{scale} \cdot (w, h)

$$

Where $(w, h)$ is the size of the original resource image.


::: tip

Do not use a `designImageScale` configuration smaller than $1$, which means that the resource image will be enlarged during packaging, resulting in obvious blurring and distortion. If you want your application to display images elegantly across multiple devices, you should prepare resource images at a larger size than required and set the correct `designImageScale` parameter.


For example, if the image size displayed on the actual device (assuming $\tt{designWidth} == \tt{deviceWidth}$) is $96\rm px \times 96\rm px$, then you can prepare a $192\rm px \times 192\rm px$ material with twice the resolution and set `designImageScale` to $2$.
:::



#### `fontFaces` <decl type="?: string" />


Specify the application-level font mapping table file path, and the fonts defined in it can be used directly in the application. This path can be relative to `manifest.json` or absolute relative to the root directory of the app's resource bundle.


Reference [Font configuration](font-config.md).


#### `assets` <decl type="?: string | string[]" />


Specifies the path to a custom resource using glob patterns (file wildcards). For example:
``` json
{
  "config": {
    "assets": [ "assets/**", "**/data.bin" ]
  }
}
```
All files in the `assets` directory of the project and all `data.bin` files in the project will be packaged. These files will only be packaged in the form of static resource files (that is, the files will be copied directly).


File wildcards can be the same as paths, but have the following special forms:
- `*` matches a path component without a path separator ( `/` ).
- `**` matches any number of path components and may include path separators.


For example:
- `test.js` can match `test.js` files in projects and directories.
- `**/*-data.bin` can match files with the `-data.bin` suffix in any path.
- `*/*.bin` matches files with the `.bin` suffix in any one-level directory in the project root.


### `Router` object


Define the composition of the page and related configuration information.


::: details type signature
``` ts
interface Router {
  entry?: string,
  pages: { [name: string]: PageInfo }
}
```
:::



#### `entry` <decl type="?: string" />


The name of the application homepage. This page will be jumped to after starting the application. Default is `"main"`.


#### `pages` <decl type="{ [name: string]: PageInfo }" />


Declare information for each page. The key of the `pages` attribute `name` is the page name, and the attribute value [`PageInfo` object](#pageinfo-对象) is the detailed configuration information of the page. For example:
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


All pages in the application must be filled in the routing table before they can be used, and each page must also have a unique name.


### `Display` object


#### `pageAnimation` <decl type="?: PageAnimation" />


The default transition animation configuration of the in-app page, the value is [`PageAnimation` object](#pageanimation-对象).


## `PageInfo` object


The page configuration object is the attribute value of the `router.pages` object. The type of page configuration object is Object. This section introduces the attribute field definitions of the page configuration object.


::: details type signature
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


The path to the page directory (the path to the folder where the page components are stored). Defaults to the same as the page name, which is the key of the `Router` object.


#### `component` <decl type="?: string" />


The name of the page component is consistent with the UX file name and does not require a *.ux* suffix. For example, the component name `"index"` corresponds to the `index.ux` file.


#### `pageAnimation` <decl type="?: PageAnimation" />


The transition animation configuration of the page, the value is [`PageAnimation` object](#pageanimation-对象). This configuration takes precedence over the `display.pageAnimation` configuration in `mainfest.json`.


#### `launchMode` <decl type="?: 'standard' | 'singleTask'" version="0.8" />


The startup mode of the page, the default is `standard`. When the page's `launchMode` is configured as `singleTask`, if you want to open a page instance that is already on the return stack, all the pages above the instance will be popped from the stack and returned to the page where the instance is located (similar to [`router.back('<page-name>')`](/api/system-router.md#back)), instead of creating a new page instance.


The [`onRefresh`](../component/life-cycle.md#onrefresh) lifecycle function is triggered when "opening" in `singleTask` mode and returning to an already existing page.


### `PageAnimation` object


The properties of this object configure the behavior of page transition animations. The transition animation is only effective for the top page, and the transition animation will not be played on non-top pages.


::: details type signature
``` ts
interface PageAnimation {
  openEnter?: string,
  closeEnter?: string,
  openExit?: string,
  closeExit?: string
}
```
:::



Each attribute can take on the following values:
- `"none"`: No transition animation, this is the default value for all properties
- `"slide"`: The page transitions with a sliding animation. This transition effect varies under different transition configuration properties, including:
  - For `openEnter` transition, the slide effect is that the page starts from the left to the right of the screen until it completely covers the screen.
  - For `closeExit` transition, the slide effect is that the page slides to the right starting from a position that completely covers the screen until it completely leaves the screen.
  - For `closeEnter` and `openExit` transitions, the slide effect is not animated.


Default transition animations for pages and apps are defined by the device. If no `pageAnimation` related fields are specified in `manifest.json`, some devices may not play transition animations, while other devices may use manufacturer-customized animation effects.


::: warning

The emulator will always play the slide page transition animation, regardless of which device it is emulating. If you want to ensure that page transition animations are turned off, use
``` json
{
  "pageAnimation": { "openEnter": "none" }
}
```
This way of writing is not `"pageAnimation": {}`, which does not take effect for unknown reasons.
:::



#### `openEnter` <decl type="?: string" />


This property configures the transition animation of the new page when opening a new page.


#### `closeEnter` <decl type="?: string" />


This property configures the transition animation of the old page that will be overwritten when a new page is opened.


#### `openExit` <decl type="?: string" />


This property configures the exit transition animation of the closed page when the page is closed.


#### `closeExit` <decl type="?: string" />


This property configures the transition animation of the page to be re-displayed under the closed page when the page is closed.


### `Dial` object


The `Dial` object describes configuration information related to the dial.


::: details type signature
``` ts
interface Dial {
  component: string,
  preview: string
}
```
:::





#### `component` <decl type="string" />


Path to the watch face entry component. Can be an absolute path within the package or relative to the `manifest.json` file.


#### `preview` <decl type="string" />


The path to the watch face preview image. Can be an absolute path within the package or relative to the `manifest.json` file.


### `Widget` object


The `Widget` object describes the configuration information of the widget or widget.


::: details type signature
``` ts
interface Widget {
  name: string,
  component: string,
  preview: string
}
```
:::



#### `name` <decl type="string" />


The name of the widget/widget. Widgets in the same application package cannot have the same name.


#### `component` <decl type="string" />


The path to the widget/widget entry component. Can be an absolute path within the package or relative to the `manifest.json` file.


#### `preview` <decl type="string" />


The path of the widget/widget preview image. Can be an absolute path within the package or relative to the `manifest.json` file.