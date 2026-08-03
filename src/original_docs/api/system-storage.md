# 数据存储

数据存储模块 `system.storage` 允许应用存储自己的数据，这些数据会持久化地保存在应用的存储对象中，当应用卸载后存储在 `system.storage` 中的数据会被清除。

`system.storage` 以键值对的形式存储数据，其中键必须是字符串，而值是一个 JSON 值（也可以是可以序列化为 JSON 的 JavaScript 值）。

## 导入模块

``` js
import storage from '@system.storage'
```

## API

### `get` <decl type="(key: string): any" method />

获取存储中键名 `key` 所对应的值。如果键值对不存在则返回 `undefined`。

### `set` <decl type="(key: string, value: any): void" method />

该方法接受一个键名 `key` 和值 `value` 作为参数并将此键值对添加到存储中。如果键名已经存在则更新其对应的值。

### `delete` <decl type="(key: string): boolean" method />

删除存储中键名 `key` 对应的键值对。键值对存在且删除成功后返回 `true`。

### `clear` <decl type="(): void" method />

清空应用中的所有存储数据。
