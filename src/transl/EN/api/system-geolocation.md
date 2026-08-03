# Geolocation

## Import Module

```js
import geolocation from '@system.geolocation';
```

Developers need to declare the application's access permission to `watch.permission.LOCATION` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

## Interface Definitions

### `getLocation` 
<decl method><pre>
(options: {
  mode?: string
  timeout?: number
}): Promise&lt;Location>
</pre></decl>

Obtain the latitude and longitude of the current location once, returning an asynchronous [Location](#location) object.

`options` Parameter Description
- `mode`: Declares the positioning accuracy. `fine` represents precise positioning, and `coarse` represents rough positioning. The default value is `coarse`.
- `timeout`: Positioning timeout in `ms`, with a default value of 30000.

### `subscribe` <decl type="(callback: (location: Location) => void): number" method/>

Listen for location changes. The `location` parameter of the `callback` is the current [Location](#location) information. The ID returned by this method can be used with the [`unsubscribe()`](#unsubscribe) method to stop listening.

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancel listening for location changes.

## Type Definitions

### `Location`

Used to represent the location information data obtained from positioning.

```ts
ts
type Location = {
  code: number; // Positioning status code, indicating whether the current location information is valid
  msg: string; // Positioning error message
  data: {
    // Location information data
    longitude: number; // Latitude value
    latitude: number; // Longitude value
    coordType: string; // Coordinate system type, such as 'WGS84', 'GCJ02', etc.
  };
};
```

The positioning status codes for the `code` field are as follows:

- `200`: Current location information is valid;
- `1002`: Currently not connected to the mobile phone's Bluetooth network;
- `1300`: The mobile phone cannot obtain positioning services;
- `1301`: Positioning services are not enabled on the mobile phone;
- `1302`: Location permission is not granted to the mobile application;
- `1399`: Unknown error.