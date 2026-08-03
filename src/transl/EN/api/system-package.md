# Package management

This module provides the installation and uninstallation functions of resource packages.

## Import module

``` js
import pkg from '@system.package'
```

Since `package` is a JavaScript keyword and cannot be used as a variable name, we can export the `"@system.package"` module to the `pkg` variable.

## Interface definition

### `install` <decl function type="(options: { src: string }): Promise<void>" />

Install an app or watch face package from the file system. The `src` attribute of the `options` parameter is the URI of the resource package file to be installed.

If the resource package is an application resource package, then after installing the resource package using `pkg.install({ src: 'package-uri' })` it can be launched by [`launch()`](system-launch.md#launch-launch-app) and the contents of the package can be accessed using the [`app`](/framework/application/resource.md#app) URI protocol.

`src` is the URI of the resource package file to be installed. The installed package must be a valid application or watch face package, that is, it must have a [`manifest.json`](/framework/application/manifest.md) file. The package name after installation is determined by [`manifest.package`](/framework/application/manifest.md#package).

After installation, you can use the [`prc`](/framework/application/resource.md#prc) protocol to access the resources in the resource package. For application resource packages, you can also use the `app` protocol.

If the package to be installed already exists, the upgrade operation will be performed. If the upgraded application is running, it will be exited first, and then you can call [`launch()`](system-launch.md#launch-launch-app) to start it again.

Installed packages can be removed by the [`remove()`](#remove) API.

### `remove`<decl type="(options: { package: string }): Promise<void>" function />

Remove resource packages installed by [`install()`](#install). The `package` attribute of the parameter `options` is the name of the resource package to be deleted, that is, the [`manifest.package`](/framework/application/manifest.md#package) field.

Before deleting the resource package, you should close related resources first, such as destroying related components and closing related pages. The `remove()` function will automatically close the application corresponding to the resource package (if it is an application resource package).

::: warning
Resource bundles must be removed using `remove()` rather than directly using the file system API, as the latter does not clear the resource cache and does not properly remove installation information.
:::

### `getInfo` <decl type="(query?: string | Query): Manifest | undefined" method/>

Get the manifest information of the application package. The optional parameter `query` can be a package name string or a more complex `Query` object:
``` ts
type Query = {
  package: string, // package name to be queried
  options?: ('dial' | 'widgets')[] // Optional query fields
}
```
If the package specified by the `package` field exists, `getInfo()` will return the `Manifest` information of the package, otherwise it will return `undefined`. When the `query` parameter is not specified, `getInfo()` will return the manifest information of the current application.

#### `Manifest` object

The returned `Manifest` object is basically a subset of [`manifest.json`](/framework/application/manifest.md):
``` ts
type Query = {
  type: 'app' | 'dial', // Package type, may be application or dial package
  name: string, // package name
  versionName: string, // version name
  versionCode: number, // version number
  icon?: string, // Application image path, this field only exists in application packages
  dial?: { // Optional field: dial information, only the dial package has this information
    component: string, //The path to the watch face component
    preview: string // Path to the watch face preview image
  },
  widgets?: { // Optional fields: widget and widget information
    name: string, //Pendant/widget name
    component: string, // widget/widget path
    preview: string // Preview image of widget/widget
  }[]
}
```
The `dial` and `widgets` of the `Manifest` object are optional fields, and their presence or absence is determined by the contents of `Query.options`. For example
``` js
pkg.getInfo({
  package: 'com.example.app',
  options: ['dial', 'widgets']
})
```
Will cause the resulting `Manifest` to contain the `dial` and `widgets` fields (however, application packages always do not contain the `dial` field).

When the `query` parameter is a string, it is equivalent to the `options` option being empty, that is
``` ts
pkg.getInfo('com.example.app')
pkg.getInfo({ package: 'com.example.app' })
```
The result is the same, in which case the returned `Manifest` object does not contain optional fields.

When the `query` parameter is not specified, the application information can be returned through `getInfo()`:
``` js
let manifest = pkg.getInfo()
console.log(manifest)
```

### `list` <decl function type="(type?: 'app' | 'dial'): string[]" />

Get a list of all installed apps or watch face package names.

### `countOf` <decl function type="(type?: 'app' | 'dial'): string[]" />

Get the number of installed apps or watch faces.
