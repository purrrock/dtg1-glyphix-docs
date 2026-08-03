# mapview


Map component, used to load and display tile-based maps. `mapview` supports gesture panning, zoom level switching, current location display and route navigation drawing, and is a core component for building map applications.


`mapview` defaults to block-level elements.


::: tip

`mapview` is a runtime extension component. Before using it, you need to confirm that the target platform has integrated the `mapview` module.
:::



## property


### `baseUri` <decl type="string" get set />


The **base path** URI of the tile image resource. The tile files will be stored in a fixed hierarchical structure in this directory. `mapview` will automatically calculate the required tile file path based on the current zoom level and coordinates. The format is:


```
{baseUri}/{zoomLevel}/{tileX}/{tileY}/normal.png     (标准地图)
{baseUri}/{zoomLevel}/{tileX}/{tileY}/satellite.png  (卫星地图)
```


Typical usage is to cache map tiles to the local storage of the device, and then point `baseUri` to the corresponding directory:


```html
<mapview baseUri="internal://files/tiles/map_provider" />
```


### `tileType` <decl type="number" get set />


The layer type of the tile map, the values ​​are as follows:


| value | description |
| :-: | :-- |

| `0` | Standard map (default), load `normal.png` tile file |
| `1` | Satellite map, load `satellite.png` tile file |


### `loadPlace` <decl type="string" get set />


The **placeholder** URI displayed when the tile image is loading. When the corresponding tile file has not been cached locally, `mapview` will display the image at the tile location until the [`reload()`](#reload) refresh is triggered after the tile is downloaded.


```html
<mapview loadPlace="/assets/imgs/loading.png" />
```


### `zoomLevel` <decl type="number" get set />


Map zoom level, the value range is $[3, 23]$, the default value is $17$. The higher the level, the more detailed the map; the lower the level, the wider the visible range.


::: info

This attribute corresponds to the Zoom Level in the map tile standard, which is consistent with the level definition of mainstream tile services such as Bing Maps and Google Maps.
:::



### `arrowIcon` <decl type="string" get set />


Image URI for the current location icon. The icon will be drawn at the screen position corresponding to the longitude and latitude specified by [`navCoordinate`](#navcoordinate) or [`setLocation()`](#setlocation), and the icon will be aligned with the coordinate point with the center point.


```html
<mapview arrowIcon="/assets/imgs/location.png" />
```


### `navCoordinate` <decl type="{ x: number, y: number }" get set />


The latitude and longitude coordinates of the current location, in the format `{ x: latitude, y: longitude }`, where `x` is the latitude and `y` is the longitude. Setting this property only updates the icon position and does not automatically move the map center to these coordinates. If you need to position the map center to the current location at the same time, please use the [`setLocation()`](#setlocation) method and pass in `force: true`.


::: tip

For scenarios where real-time position tracking is required, it is recommended to use the [`setLocation()`](#setlocation) method instead of directly assigning this attribute to control whether to automatically return to center through the `force` parameter.
:::



### `arrowLineWidth` <decl type="number" get set />


The line width of the navigation route, in pixels. The default value is `12`.


### `arrowLineBackgroundColor` <decl type="color" get set />


The **background color** of the navigation route (the color of the traveled part), accepts CSS color values, and the default value is `#898b90`.


### `arrowLineForgeColor` <decl type="color" get set />


The foreground color of the navigation route (the color of the remaining route portion), accepts CSS color values, and defaults to `#4b73ec`.


### `smallMem` <decl type="boolean" get set />


Whether to enable low memory device mode, the default value is `false`.


When enabled, `mapview` will merge and scale four 256×256 tiles into a 512×512 picture for drawing, reducing the number of tiles cached in memory at the same time to adapt to devices with limited memory.


::: warning

Low memory mode will sacrifice some map clarity and should only be turned on when the device is obviously low on memory.
:::



### `missTiles` <decl type="Array<{ z: number, x: number, y: number }>" get listen />


Read-only attribute, triggers monitoring when the map finds a local missing tile file. The callback parameter is an array, each element describes a missing tile:


| Field | Type | Description |
| :-- | :-- | :-- |

| `z` | `number` | Zoom Level |
| `x` | `number` | Tile X coordinate (column number) |
| `y` | `number` | Tile Y coordinate (row number) |


After receiving this event, the application usually needs to download the corresponding tile file from the server and call [`reload()`](#reload) to refresh the map after the download is completed:


```js
export default {
  missTileHandler(tiles) {
    // tiles: [{ z: 17, x: 105234, y: 49832 }, ...]
    downloadTiles(tiles).then(() => {
      this.$element('mapview').reload()
    })
  }
}
```


```html
<mapview id="mapview" on:missTiles="missTileHandler" />
```


### `directionInfo` <decl type="{ event: string, stepIndex?: number, distance?: number }" get listen />


Read-only property of the map event, the listener is triggered when the following operations occur on the map:


| `event` value | Trigger timing | Additional fields |
| :-- | :-- | :-- |

| `"move"` | Triggered when the user gestures to pan the map | None |
| `"calc"` | Triggered when the position and yaw distance are recalculated in navigation | `stepIndex` (current route segment index), `distance` (deviation distance from the current position to the route, in meters) |


```js
export default {
  onDirectionInfo(info) {
    if (info.event === 'move') {
      // If the user manually drags the map, the automatic return to center can be paused.
    } else if (info.event === 'calc') {
      console.log(`Current step: ${info.stepIndex}, yaw distance: ${info.distance} meters`)
    }
  }
}
```


## method


### `reload()`


Reload all tiles. After the new tile file is written to the local storage, this method needs to be called to refresh the map display.


```js
this.$element('mapview').reload()
```


### `locate()`


Moves the center of the map to the current location (the coordinates specified by [`navCoordinate`](#navcoordinate)) for the "return to current location" function.


```js
this.$element('mapview').locate()
```


### `setLocation(location)`


Sets the current location coordinates and optionally moves the map center to that location.


| Parameter fields | Type | Description |
| :-- | :-- | :-- |

| `latitude` | `number` | Latitude |
| `longitude` | `number` | Longitude |
| `force` | `boolean` | If it is `true`, the map center will be positioned to this coordinate immediately (equivalent to calling [`locate()`](#locate)), if it is `false`, only the icon position will be updated |


```js
// Only updates the icon position, does not move the map
this.$element('mapview').setLocation({
  latitude: 39.9042,
  longitude: 116.4074,
  force: false,
})

// Update the icon position and move the map center to that coordinate
this.$element('mapview').setLocation({
  latitude: 39.9042,
  longitude: 116.4074,
  force: true,
})
```


### `startNav(linePoints)`


Set navigation route and start navigation. After calling, the map will automatically locate the starting point of the route and draw the complete route.


`linePoints` is an array of route points, and each element is a binary array in the format of `[经度, 纬度]`:


```js
const route = [
  [116.397428, 39.909736],  // [longitude, latitude]
  [116.404730, 39.913370],
  [116.410072, 39.918933],
]
this.$element('mapview').startNav(route)
```


::: warning

Note the order of parameters: the first value of each coordinate point is longitude, and the second value is latitude, contrary to the common "latitude first" convention.
:::



### `insetNavPoint(linePoints)`


Appends a route point to an existing navigation route, in the same format as [`startNav()`](#startnav). Suitable for scenarios where route data is received in segments. After appending, you need to call [`reload()`](#reload) to refresh the display.


```js
this.$element('mapview').insetNavPoint(newPoints)
this.$element('mapview').reload()
```


## Usage example


### Basic map display


The following example shows how to configure a basic map component to listen for missing tile events and trigger downloads.


```html
<template>
  <mapview
    id="map"
    :zoomLevel="zoom"
    :baseUri="tileBaseUri"
    :tileType="tileType"
    loadPlace="/assets/imgs/tile-loading.png"
    arrowIcon="/assets/imgs/location.png"
    on:missTiles="onMissTiles"
    on:directionInfo="onDirectionInfo"
  />
</template>
```


```js
export default {
  data: {
    zoom: 17,
    tileType: 0,
    tileBaseUri: 'internal://files/tiles/my_provider',
  },

  onReady() {
    // Initialize current location
    this.$element('map').setLocation({
      latitude: 39.9042,
      longitude: 116.4074,
      force: true,
    })
  },

  onMissTiles(tiles) {
    // tiles: Missing tile list, initiate a download request to the server
    fetchTilesFromServer(tiles).then(() => {
      this.$element('map').reload()
    })
  },

  onDirectionInfo(info) {
    if (info.event === 'move') {
      // User panned the map
    }
  },
}
```


```css
mapview {
  width: 100%;
  height: 100%;
}
```


### Navigation route drawing


```html
<template>
  <stack>
    <mapview
      id="map"
      :baseUri="tileBaseUri"
      :zoomLevel="zoom"
      arrowIcon="/assets/imgs/location.png"
      arrowLineWidth="10"
      arrowLineBackgroundColor="#888888"
      arrowLineForgeColor="#1a73e8"
      on:missTiles="onMissTiles"
    />
    <button @click="startNavigation">开始导航</button>
  </stack>
</template>
```


```js
export default {
  data: {
    zoom: 16,
    tileBaseUri: 'internal://files/tiles/my_provider',
  },

  startNavigation() {
    const route = [
      [116.397428, 39.909736],
      [116.404730, 39.913370],
      [116.410072, 39.918933],
    ]
    this.$element('map').startNav(route)
  },

  onMissTiles(tiles) {
    fetchTilesFromServer(tiles).then(() => {
      this.$element('map').reload()
    })
  },
}
```


### Low memory device adaptation


```html
<mapview
  id="map"
  :baseUri="tileBaseUri"
  :zoomLevel="zoom"
  :smallMem="isLowEndDevice"
/>
```


```js
import SysDevice from '@system.device'

export default {
  data: {
    zoom: 17,
    tileBaseUri: 'internal://files/tiles/my_provider',
    isLowEndDevice: false,
  },
  onInit() {
    // Determine whether to enable low memory mode based on the archive bit in the device
    this.isLowEndDevice = SysDevice.memoryProfile <= 4096
  },
}
```