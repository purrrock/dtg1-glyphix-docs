# Internal interface

The `system.internal` module provides some internal interfaces for use by the system. This module can only be used in launcher applications.

## Import module

``` js
import internal from '@system.internal'
```

## API

### `globalComponent` <decl type="(name: string, uri: string): void" method />

Register a [global component](/framework/component/README.md#global component). Global components can be introduced in all applications. The parameter `name` is the name of the global component, and `uri` is the path or URI of the global component UX file relative to the current source file. For example
``` js
internal.globalComponent('TopBar', '/global/TopBar.ux')
```
You can then use `<import name="TopBar" />` to reference the global component `TopBar` in all applications.

The `globalComponent()` method is best executed in the `app.js` execution phase of the launcher application, so that global component information can be registered before any interface is loaded.

### `setDefaultKeyHandler` <decl type="(handler: (event: KeyEvent) => void): void" method />

Register the system's default key handler. The parameter `handler` is a callback function. The `KeyEvent` type prototype is:
``` ts
interface KeyEvent {
  type: 'keydown' | 'keyup', // Type of key event
  key: string, // key name
  timestamp: number, // timestamp of key event reporting, unit is milliseconds
}
```
The default key handler can only be registered once, because multiple registrations will overwrite previous operations.
