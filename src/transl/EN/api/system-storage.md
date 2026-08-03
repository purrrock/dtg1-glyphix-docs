# Data storage

The data storage module `system.storage` allows an application to store its own data. This data will be persisted in the application's storage object. When the application is uninstalled, the data stored in `system.storage` will be cleared.

`system.storage` stores data as key-value pairs, where the key must be a string and the value is a JSON value (or a JavaScript value that can be serialized to JSON).

## Import module

``` js
import storage from '@system.storage'
```

## API

### `get` <decl type="(key: string): any" method />

Get the value corresponding to the key name `key` in the storage. Returns `undefined` if the key-value pair does not exist.

### `set` <decl type="(key: string, value: any): void" method />

This method accepts a key name `key` and a value `value` as parameters and adds this key-value pair to the storage. If the key name already exists, update its corresponding value.

### `delete` <decl type="(key: string): boolean" method />

Delete the key-value pair corresponding to the key name `key` in the storage. Returns `true` if the key-value pair exists and is successfully deleted.

### `clear` <decl type="(): void" method />

Clear all stored data in the app.
