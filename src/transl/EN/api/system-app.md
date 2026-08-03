# Application context

## Import module

```js
import app from '@system.app'
```

## Interface definition

### `getInfo` <decl type="(): Manifest" method/>

Get the context information of the current application and return a [`Manifest` object](./system-package.md#manifest-object), which contains the basic information of the application, such as package name, version number, etc.

### `terminate` <decl type="(): void" method version="0.8"/>

Terminate the current application. After calling this method, the app will be closed and the user will need to restart the app to continue using it.

::: note Compatibility Risk
This API is not supported on all platforms, the [`launch.exit()`](./system-launch.md#exit) method may be used as an alternative.
:::

### `loadLibrary` <decl type="(name: string): object | undefined" method/>

Loads a Library Loader registered by the native implementation by name and returns the corresponding library object. If the library with the specified name is not registered, `undefined` is returned.

Typically, it is recommended to mount the library object to the APP object:
```js
// app.js
import app from '@system.app'

export default {
  customLib: app.loadLibrary('custom-library'),
  onCreate() {
    if (!this.customLib) {
      // Handle library loading failure, such as falling back to script implementation
      this.customLib = someStubImplementation();
    } else {
      //Use library objects normally
      this.customLib.someFunction()
    }
  }
}
```
In this way, the component can directly use `this.$app.customLib` to access the library object.

`loadLibrary()` is suitable for accessing non-standard system functions. The application can detect whether the return value is `undefined` to determine whether the current platform supports the library, thereby downgrading to the piling implementation of the script in a general simulator environment without relying on the simulator's special processing of specific module paths.

If your application needs to support both standard quick app APIs and system customization functions, you can decide whether to roll back based on the return result of `loadLibrary()`.

### `keepForeground` <decl type="(options: { enable: boolean }): void" method/>

Sets whether the application remains in the foreground. If the `enable` attribute in the `options` parameter is `true`, the application will try to remain in the foreground.

Using this method requires declaring the application's permissions for `watch.permission.FOREGROUND_SERVICE` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

This method is just a reminder for system behavior and is not mandatory. The application may be switched to the background due to user operations or other high-priority policies. While using this method to keep the app in the foreground, the device can still enter low-power mode:

- If AOD (Always on Display) mode is turned on, the UI refresh rate will be reduced.
- Otherwise, the screen turns off after a while but the app remains running in the foreground.

When the device enters low-power mode (including turning off the screen), the foreground application will still be scheduled and executed at a lower frequency instead of completely sleeping. Therefore it can be used for navigation or fitness applications.
