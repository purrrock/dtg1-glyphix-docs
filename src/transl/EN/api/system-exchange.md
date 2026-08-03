# Exchange data

The exchange data module `system.exchange` is used to store shared data across applications. This data is not stored persistently and will be lost once the device is powered off. . The data stored in `system.exchange` can be accessed in all applications, so this module can be used to store some configuration information of the application, but it is not suitable for storing sensitive data.

`system.exchange` stores data as key-value pairs, where the key must be a string and the value is a JSON value (or a JavaScript value that can be serialized to JSON).

## Import module

``` js
import exchange from '@system.exchange'
```

## API

### `get` <decl type="(key: string): any" method />

Get the value corresponding to the key name `key` in the storage. Returns `undefined` if the key-value pair does not exist.

### `set` <decl type="(key: string, value: any): void" method />

This method accepts a key name `key` and a value `value` as parameters and adds this key-value pair to the storage. If the key name already exists, update its corresponding value.

### `delete` <decl type="(key: string): boolean" method />

Delete the key-value pair corresponding to the key name `key` in the storage. Returns `true` if the key-value pair exists and is successfully deleted.

### `watch` <decl type="(key: string, callback: (value: any) => void): number" method />

Monitor changes in the data value of the key named `key` in the storage, and call the `callback` callback function when the value changes. The parameter `value` of the callback function is the new data value. The `watch()` method returns a `wtacher ID`, which can be used with the [`unwatch()`](#unwatch) method to unwatch.

::: tip
When monitoring is no longer needed, the [`unwatch()`](#unwatch) method should be used to unblock monitoring, otherwise memory leaks may occur.
:::

### `unwatch` <decl type="(watcherID: number): void" method />

Cancel a listener on the key named `key` in the storage. The parameter `watcherID` is the `wtacher ID` returned when the [`watch()`](#watch) method creates a watcher.
