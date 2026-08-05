# Network Status

## Import Module

```js
import network from '@system.network';
```

## Interface Definition

### `subscribe` <decl type="(callback: (status: NetworkState) => void): number" method/>

Listens for changes in network status. The `status` parameter of the `callback` is the new [Network State](#networkstate). The ID returned by this method can be used with the [`unsubscribe()`](#unsubscribe) method to stop listening.

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancels the network status listener. `subscribeID` is the ID value returned by the [`subscribe()`](#subscribe) method.

### `getType` <decl type="(): Promise<NetworkState>" method/>

Gets the current network status, returning a [`NetworkState`](#networkstate) value.

## Type Definitions

### `NetworkState`

This object represents the current network status. The type signature is as follows:

```ts
type NetworkState = {
  device: string; // The name of the network device
  type: string; // The type of the network device
  linkUp: boolean; // Whether the network device is turned on
  online: boolean; // Whether the device is online (whether the internet is accessible)
};
```

Typically, you can use the `online` property of `NetworkState` to check whether the device has internet access.