# Exchanging Data

The data exchange module `system.exchange` is used to store shared data across applications. This data is not persistently stored and will be lost once the device is powered off. Data stored in `system.exchange` can be accessed across all applications, making this module suitable for storing application configuration information, but not for sensitive data.

`system.exchange` stores data in the form of key-value pairs, where the key must be a string and the value is a JSON value (or a JavaScript value that can be serialized to JSON).

## Import Module

``` js
import exchange from '@system.exchange'
```

## API

### `get` <decl type="(key: string): any" method />

Gets the value corresponding to the key `key` in the storage. Returns `undefined` if the key-value pair does not exist.

### `set` <decl type="(key: string, value: any): void" method />

This method accepts a key `key` and a value `value` as parameters and adds this key-value pair to the storage. If the key already exists, its corresponding value is updated.

### `delete` <decl type="(key: string): boolean" method />

Deletes the key-value pair corresponding to the key `key` in the storage. Returns `true` if the key-value pair exists and is successfully deleted.

### `watch` <decl type="(key: string, callback: (value: any) => void): number" method />

Listens for changes to the data value of the key `key` in the storage, and invokes the `callback` function when the value changes. The parameter `value` of the callback function is the new data value. The `watch()` method returns a `watcher ID`, which can be used with the [`unwatch()`](#unwatch) method to remove the listener.

::: tip
When listening is no longer needed, the [`unwatch()`](#unwatch) method should be used to remove the listener, otherwise, a memory leak may occur.
:::

### `unwatch` <decl type="(watcherID: number): void" method />

Cancels a listener for a key in the storage. The parameter `watcherID` is the `watcher ID` returned when the listener was created by the [`watch()`](#watch) method.