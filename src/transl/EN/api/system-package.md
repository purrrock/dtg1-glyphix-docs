# Package Management

This module provides resource package installation and uninstallation functions.

## Import Module

``` js
import pkg from '@system.package'
```

Since `package` is a JavaScript keyword and cannot be used as a variable name, we can export the `"@system.package"` module to the `pkg` variable.

## Interface Definition

### `install` <decl function type="(options: { src: string }): Promise<void>" />

Installs an application or watch face package from the file system. The `src` property of the `options` parameter is the URI of the resource package file to be installed.

If the resource package is an application resource package, it can be launched via [`launch()`](system-launch.md#launch-launch-app) after being installed using `pkg.install({ src: 'package-uri' })`, and the contents within the package can be accessed using the [`app`](/framework/application/resource.md#app) URI scheme.

`src` is the URI of the resource package file to be installed. The installed package must be a valid application or watch face package, meaning it must contain a [`manifest.json`](/framework/application/manifest.md) file. The package name after installation is determined by [`manifest.package`](/framework/application/manifest.md#package).

After installation, resources within the resource package can be accessed using the [`prc`](/framework/application/resource.md#prc) scheme, and application resource packages can also be accessed using the `app` scheme.

If the package to be installed already exists, an upgrade operation will be performed. If the application being upgraded is currently running, it will be exited first, and can be launched again later by calling [`launch()`](system-launch.md#launch-launch-app).

The installed package can be deleted by the [`remove()`](#remove) API.

### `remove`<decl type="(options: { package: string }): Promise<void>" function />

Deletes the resource package installed by [`install()`](#install). The `package` property of the `options` parameter is the name of the resource package to be deleted, which is the [`manifest.package`](/framework/application/manifest.md#package) field.

Related resources should be closed before deleting the resource package, such as destroying related components and closing related pages. The `remove()` function will automatically close the application corresponding to the resource package (if it is an application resource package).

::: warning
You must use `remove()` instead of directly using the file system API to delete the resource package, because the latter will not clear the resource cache and cannot correctly delete the installation information.
:::

### `getInfo` <decl type="(query?: string | Query): Manifest | undefined" method/>

Gets the manifest information of the application package. The optional parameter `query` can be a package name string or a more complex `Query` object:
``` ts
type Query = {
  package: string,                 // Package name to query
  options?: ('dial' | 'widgets')[] // Optional query fields
}
```
If the package specified by the `package` field exists, `getInfo()` will return the `Manifest` information of the package, otherwise it returns `undefined`. When the `query` parameter is not specified, `getInfo()` will return the manifest information of the current application.

#### `Manifest` Object

The returned `Manifest` object is basically a subset of [`manifest.json`](/framework/application/manifest.md):
``` ts
type Query = {
  type: 'app' | 'dial', // Package type, can be an application or watch face package
  name: string,         // Package name
  versionName: string,  // Version name
  versionCode: number,  // Version code
  icon?: string,        // Application image path, this field only exists for application packages
  dial?: {              // Optional field: watch face information, only present in watch face packages
    component: string,  // Path of the watch face component
    preview: string     // Path of the watch face preview image
  },
  widgets?: {           // Optional field: widget and small widget information
    name: string,       // Widget/small widget name
    component: string,  // Widget/small widget path
    preview: string     // Widget/small widget preview image path
  }[]
}
```
The `dial` and `widgets` fields of the `Manifest` object are optional fields, and their existence is determined by the contents of `Query.options`. For example:
``` js
pkg.getInfo({
  package: 'com.example.app',
  options: ['dial', 'widgets']
})
```
will make the resulting `Manifest` contain the `dial` and `widgets` fields (however, application packages never contain the `dial` field).

When the `query` parameter is a string, it is equivalent to an empty `options` option, meaning:
``` ts
pkg.getInfo('com.example.app')
pkg.getInfo({ package: 'com.example.app' })
```
yield the same results. In this case, the returned `Manifest` object does not contain optional fields.

When the `query` parameter is not specified, the information of the current application can be returned via `getInfo()`:
``` js
let manifest = pkg.getInfo()
console.log(manifest)
```

### `list` <decl function type="(type?: 'app' | 'dial'): string[]" />

Gets a list of all installed application or watch face package names.

### `countOf` <decl function type="(type?: 'app' | 'dial'): string[]" />

Gets the number of installed applications or watch faces.