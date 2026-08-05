# Application Context

## Import Module

```js
import app from '@system.app'
```

## Interface Definition

### `getInfo` <decl type="(): Manifest" method/>

Gets the context information of the current application and returns a [`Manifest` object](./system-package.md#manifest-object), which contains basic application information such as the package name and version number.

### `terminate` <decl type="(): void" method version="0.8"/>

Terminates the running of the current application. After calling this method, the application will be closed, and the user needs to restart the application to continue using it.

::: note Compatibility Risk
This API is not supported on all platforms. You can temporarily use the [`launch.exit()`](./system-launch.md#exit) method as an alternative.
:::

### `loadLibrary` <decl type="(name: string): object | undefined" method/>

Loads a Library Loader registered by a native implementation by name and returns the corresponding library object. If the library with the specified name is not registered, `undefined` is returned.

Typically, it is recommended to mount the library object onto the APP object:
```js
// app.js
import app from '@system.app'

export default {
  customLib: app.loadLibrary('custom-library'),
  onCreate() {
    if (!this.customLib) {
      // Handle the case where library loading fails, e.g., fall back to a script implementation
      this.customLib = someStubImplementation();
    } else {
      // Use the library object normally
      this.customLib.someFunction()
    }
  }
}
```
In this way, components can directly use `this.$app.customLib` to access the library object.

`loadLibrary()` is suitable for accessing non-standard system features. Applications can check whether the return value is `undefined` to determine whether the current platform supports the library, thereby downgrading to a script stub implementation in a general simulator environment without relying on the simulator's special handling of specific module paths.

If the application needs to support both standard Quick App APIs and system-customized features simultaneously, it can decide whether to fall back based on the return result of `loadLibrary()`.

### `keepForeground` <decl type="(options: { enable: boolean }): void" method/>

Sets whether the application should stay in the foreground. If the `enable` property in the `options` parameter is `true`, the application will attempt to remain in the foreground.

Using this method requires declaring the application's permission for `watch.permission.FOREGROUND_SERVICE` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

This method is merely a hint for system behavior and is not mandatory. The application may still be switched to the background due to user operations or other high-priority policies. When using this method to keep the application in the foreground, the device can still enter low-power mode:

- If AOD (Always on Display) mode is enabled, the UI refresh rate will be reduced.
- Otherwise, the screen will turn off after a period of time, but the application will still run in the foreground.

After the device enters low-power mode (including turning off the screen), the foreground application will still be scheduled and executed at a lower frequency rather than completely sleeping. Therefore, it can be used for navigation or fitness applications.