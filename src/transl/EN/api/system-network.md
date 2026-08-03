# Network Status

## Import Module

```js
import network from '@system.network';
```

## Interface Definition

### `subscribe` <decl type="(callback: (status: NetworkState) => void): number" method/>

Listens for changes in network status. The `status` parameter of the `callback` is the new [Network State](#networkstate). The ID returned by this method can be used with the [`unsubscribe()`](#unsubscribe) method to stop listening.

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancels network status listening. `subscribeID` is the ID value returned by the [`subscribe()`](#subscribe) method.

### `getType` <decl type="(): Promise<NetworkState>" method/>

Gets the current network status and returns a [`NetworkState`](#networkstate) value.

## Type Definitions

### `NetworkState`

This object is used to represent the current network status, with the following type signature:

```ts
type NetworkState = {
  device: string; // The name of the network device
  type: string; // The type of the network device
  linkUp: boolean; // Whether the network device is turned on
  online: boolean; // Whether the device is online (whether the internet can be accessed)
};
```

Typically, the `online` property of `NetworkState` can be used to check whether the device has internet access.