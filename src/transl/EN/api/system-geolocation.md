# location

## Import module

```js
import geolocation from '@system.geolocation';
```

Developers need to declare the application's access permissions to `watch.permission.LOCATION` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

## Interface definition

### `getLocation`
<decl method><pre>
(options: {
  mode?: string
  timeout?: number
}): Promise&lt;Location>
</pre></decl>

Get the longitude and latitude of the current location once and return an asynchronous [location information](#location).

`options` parameter description
- `mode`: declare the positioning accuracy, `fine` is precise positioning, `coarse` is fuzzy positioning, the default value is `coarse`
- `timeout`: positioning timeout, unit is `ms`, default is 30000

### `subscribe` <decl type="(callback: (location: Location) => void): number" method/>

Listen for location changes. The parameter `location` of `callback` is the current [location information](#location). The ID returned by this method can be used to unsubscribe using the [`unsubscribe()`](#unsubscribe) method.

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancel listening for location changes.

## Type definition

### `Location`

Location information data used to represent positioning.

```ts
type Location = {
  code: number; // Positioning status code, indicating whether the current location information is valid
  msg: string; // Positioning error message
  data: {
    //Data of location information
    longitude: number; // latitude value
    latitude: number; // longitude value
    coordType: string; //Coordinate system type, such as 'WGS84', 'GCJ02', etc.
  };
};
```

The positioning status code of the `code` field is as follows:

- `200`: The current positioning information is valid;
- `1002`: Currently not connected to the mobile phone Bluetooth network
- `1300`: The mobile phone cannot obtain location services
- `1301`: Location service is not enabled on the phone
- `1302`: The mobile application does not grant location permission
- `1399`: unknown error
