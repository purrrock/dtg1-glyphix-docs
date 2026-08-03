# 网络状态

## 导入模块

```js
import network from '@system.network';
```

## 接口定义

### `subscribe` <decl type="(callback: (status: NetworkState) => void): number" method/>

监听网络状态的变化。`callback` 的参数 `status` 为新的[网络状态](#networkstate)，此方法返回的 ID 可使用 [`unsubscribe()`](#unsubscribe) 方法来解除监听。

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

取消网络状态监听，`subscribeID` 是 [`subscribe()`](#subscribe) 方法返回的 ID 值。

### `getType` <decl type="(): Promise<NetworkState>" method/>

获取当前的网络状态，返回一个 [`NetworkState`](#networkstate) 值。

## 类型定义

### `NetworkState`

此对象用于表示当前的网络状态，类型签名如下：

```ts
type NetworkState = {
  device: string; // 网络设备的名字
  type: string; // 网络设备的类型
  linkUp: boolean; // 网络设备是否已经打开
  online: boolean; // 设备是否在线（是否可以访问互联网）
};
```

通常可以使用 `NetworkState` 的 `online` 属性来检查设备是否可以上网。
