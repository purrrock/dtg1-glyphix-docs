# 交换数据

交换数据模块 `system.exchange` 用于存储跨应用的共享数据，这些数据不会持久化存储，一旦设备断电即会丢失。。`system.exchange` 中存储的数据可以在所有应用中访问，因此该模块可用于存储应用的一些配置信息，但不适合存储敏感数据。

`system.exchange` 以键值对的形式存储数据，其中键必须是字符串，而值是一个 JSON 值（也可以是可以序列化为 JSON 的 JavaScript 值）。

## 导入模块

``` js
import exchange from '@system.exchange'
```

## API

### `get` <decl type="(key: string): any" method />

获取存储中键名 `key` 所对应的值。如果键值对不存在则返回 `undefined`。

### `set` <decl type="(key: string, value: any): void" method />

该方法接受一个键名 `key` 和值 `value` 作为参数并将此键值对添加到存储中。如果键名已经存在则更新其对应的值。

### `delete` <decl type="(key: string): boolean" method />

删除存储中键名 `key` 对应的键值对。键值对存在且删除成功后返回 `true`。

### `watch` <decl type="(key: string, callback: (value: any) => void): number" method />

监听存储中键名为 `key` 的数据值变化，并在值变化时调用 `callback` 回调函数。回调函数的参数 `value` 为新的数据值。`watch()` 方法返回一个 `wtacher ID`，该 ID 可用于 [`unwatch()`](#unwatch) 方法来解除监听。

::: tip
不再需要监听时应使用 [`unwatch()`](#unwatch) 方法解除监听，否则可能造成内存泄漏。
:::

### `unwatch` <decl type="(watcherID: number): void" method />

取消存储中对键名为 `key` 的一个监听。参数 `watcherID` 是 [`watch()`](#watch) 方法创建监听时返回的 `wtacher ID`。
