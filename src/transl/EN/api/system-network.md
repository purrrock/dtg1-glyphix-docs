# Network status

## Import module

```js
import network from '@system.network';
```

## Interface definition

### `subscribe` <decl type="(callback: (status: NetworkState) => void): number" method/>

Monitor changes in network status. The parameter `status` of `callback` is the new [network state](#networkstate). The ID returned by this method can be used to unsubscribe using the [`unsubscribe()`](#unsubscribe) method.

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancel network status monitoring. `subscribeID` is the ID value returned by the [`subscribe()`](#subscribe) method.

### `getType` <decl type="(): Promise<NetworkState>" method/>

Get the current network status and return a [`NetworkState`](#networkstate) value.

## Type definition

### `NetworkState`

This object is used to represent the current network status. The type signature is as follows:

```ts
type NetworkState = {
  device: string; //The name of the network device
  type: string; // Type of network device
  linkUp: boolean; // Whether the network device has been opened
  online: boolean; // Whether the device is online (whether it can access the Internet)
};
```

You can usually use the `online` property of `NetworkState` to check whether the device can access the Internet.
