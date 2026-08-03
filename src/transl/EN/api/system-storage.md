# Data Storage

The data storage module `system.storage` allows applications to store their own data, which is persistently saved in the application's storage object. Data stored in `system.storage` will be cleared when the application is uninstalled.

`system.storage` stores data in the form of key-value pairs, where the key must be a string, and the value is a JSON value (or a JavaScript value that can be serialized to JSON).

## Import Module

``` js
import storage from '@system.storage'
```

## API

### `get` <decl type="(key: string): any" method />

Gets the value corresponding to the key `key` in the storage. Returns `undefined` if the key-value pair does not exist.

### `set` <decl type="(key: string, value: any): void" method />

This method accepts a key `key` and a value `value` as parameters and adds this key-value pair to the storage. If the key already exists, its corresponding value is updated.

### `delete` <decl type="(key: string): boolean" method />

Deletes the key-value pair corresponding to the key `key` from the storage. Returns `true` if the key-value pair exists and is successfully deleted.

### `clear` <decl type="(): void" method />

Clears all stored data in the application.