# Internal Interfaces

The `system.internal` module provides internal interfaces for system use. This module can only be used in the launcher application.

## Import Module

``` js
import internal from '@system.internal'
```

## API

### `globalComponent` <decl type="(name: string, uri: string): void" method />

Registers a [global component](/framework/component/README.md#全局组件), which can be imported in all applications. The `name` parameter is the name of the global component, and the `uri` parameter is the relative path or URI of the global component UX file to the current source file. For example:
``` js
internal.globalComponent('TopBar', '/global/TopBar.ux')
```
Afterwards, the global component `TopBar` can be referenced in all applications using `<import name="TopBar" />`.

It is best to execute the `globalComponent()` method during the execution phase of the launcher application's `app.js`, so that global component information can be registered before any interface is loaded.

### `setDefaultKeyHandler` <decl type="(handler: (event: KeyEvent) => void): void" method />

Registers the system's default key handler. The `handler` parameter is a callback function. The prototype of the `KeyEvent` type is:
``` ts
interface KeyEvent  {
  type: 'keydown' | 'keyup', // Type of the key event
  key: string, // Name of the key
  timestamp: number, // Timestamp when the key event was reported, in milliseconds
}
```
The default key handler can only be registered once, as multiple registrations will overwrite previous operations.