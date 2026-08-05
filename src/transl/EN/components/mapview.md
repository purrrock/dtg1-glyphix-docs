# mapview

A map component used to load and display tile-based maps. `mapview` supports gesture panning, zoom level switching, current location display, and route navigation drawing. It is the core component for building map-based applications.

`mapview` is a block-level element by default.

::: tip
`mapview` is a runtime extension component. Before using it, make sure that the target platform has integrated the `mapview` module.
:::

## Attributes

### `baseUri` <decl type="string" get set />

The **base path** URI of the tile map resources. Tile files will be stored in this directory according to a fixed hierarchical structure. `mapview` will automatically calculate the required tile file path based on the current zoom level and coordinates. The format is:

```
{baseUri}/{zoomLevel}/{tileX}/{tileY}/normal.png     (Standard map)
{baseUri}/{zoomLevel}/{tileX}/{tileY}/satellite.png  (Satellite map)
```

A typical usage is to cache map tiles to the device's local storage and then point `baseUri` to the corresponding directory:

```html
<mapview baseUri="internal://files/tiles/map_provider" />
```

### `tileType` <decl type="number" get set />

The layer type of the tile map. Available values:

| Value | Description |
| :-: | :-- |
| `0` | Standard map (default), loads `normal.png` tile files |
| `1` | Satellite map, loads `satellite.png` tile files |

### `loadPlace` <decl type="string" get set />

The URI of the **placeholder image** displayed while tile maps are loading. When the corresponding tile file has not yet been cached locally, `mapview` will display this image at the tile position until the tile download is complete, which then triggers [`reload()`](#reload) to refresh.

```html
<mapview loadPlace="/assets/imgs/loading.png" />
```

### `zoomLevel` <decl type="number" get set />

The map zoom level, with a value range of $[3, 23]$ and a default value of $17$. The higher the level, the more detailed the map; the lower the level, the larger the visible area.

::: info
This property corresponds to the Zoom Level in map tile standards, which is consistent with the level definitions of mainstream tile services such as Bing Maps and Google Maps.
:::

### `arrowIcon` <decl type="string" get set />

The image URI of the current location icon. This icon will be drawn at the screen position corresponding to the latitude and longitude specified by [`navCoordinate`](#navcoordinate) or [`setLocation()`](#setlocation), with the icon aligned to the coordinate point at its center.

```html
<mapview arrowIcon="/assets/imgs/location.png" />
```

### `navCoordinate` <decl type="{ x: number, y: number }" get set />

The latitude and longitude coordinates of the current location, formatted as `{ x: latitude, y: longitude }`, where `x` is the latitude and `y` is the longitude. Setting this property only updates the icon position and will not automatically move the map center to this coordinate. If you need to center the map on the current location at the same time, please use the [`setLocation()`](#setlocation) method and pass `force: true`.

::: tip
For scenarios that require tracking real-time locations, it is recommended to use the [`setLocation()`](#setlocation) method instead of directly assigning a value to this property, so that you can control whether to automatically recenter via the `force` parameter.
:::

### `arrowLineWidth` <decl type="number" get set />

The line width of the navigation route in pixels, with a default value of `12`.

### `arrowLineBackgroundColor` <decl type="color" get set />

The **background color** of the navigation route (the color of the traversed part). Accepts CSS color values, with a default value of `#898b90`.

### `arrowLineForgeColor` <decl type="color" get set />

The **foreground color** of the navigation route (the color of the remaining route part). Accepts CSS color values, with a default value of `#4b73ec`.

### `smallMem` <decl type="boolean" get set />

Whether to enable low-memory device mode. The default value is `false`.

When enabled, `mapview` will combine and scale four 256×256 tiles into a single 512×512 image for rendering, reducing the number of tiles cached in memory simultaneously to adapt to devices with limited memory.

::: warning
Low-memory mode sacrifices some map clarity. Enable this option only when device memory is significantly insufficient.
:::

### `missTiles` <decl type="Array<{ z: number, x: number, y: number }>" get listen />

A read-only property that triggers a listener when the map detects missing local tile files. The callback parameter is an array, where each element describes a missing tile:

| Field | Type | Description |
| :-- | :-- | :-- |
| `z` | `number` | Zoom Level |
| `x` | `number` | Tile X coordinate (column number) |
| `y` | `number` | Tile Y coordinate (row number) |

After receiving this event, the application typically needs to download the corresponding tile files from the server and call [`reload()`](#reload) to refresh the map once the download is complete:

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

A read-only property for map events, which triggers a listener when the following operations occur on the map:

| `event` Value | Trigger Timing | Additional Fields |
| :-- | :-- | :-- |
| `"move"` | Triggered when the user pans the map via gestures | None |
| `"calc"` | Triggered when recalculating position and off-route distance during navigation | `stepIndex` (current route segment index), `distance` (deviation distance from the current position to the route, in meters) |

```js
export default {
  onDirectionInfo(info) {
    if (info.event === 'move') {
      // The user manually dragged the map, auto-recentering can be paused
    } else if (info.event === 'calc') {
      console.log(`Current step: ${info.stepIndex}, Deviation distance: ${info.distance} meters`)
    }
  }
}
```

## Methods

### `reload()`

Reloads all tiles. When new tile files are written to local storage, this method needs to be called to refresh the map display.

```js
this.$element('mapview').reload()
```

### `locate()`

Moves the map center to the current location (the coordinates specified by [`navCoordinate`](#navcoordinate)). Used for the "back to current location" feature.

```js
this.$element('mapview').locate()
```

### `setLocation(location)`

Sets the current location coordinates and optionally moves the map center to that location.

| Parameter Field | Type | Description |
| :-- | :-- | :-- |
| `latitude` | `number` | Latitude |
| `longitude` | `number` | Longitude |
| `force` | `boolean` | When `true`, immediately centers the map on this coordinate (equivalent to calling [`locate()`](#locate)); when `false`, only updates the icon position |

```js
// Only updates the icon position without moving the map
this.$element('mapview').setLocation({
  latitude: 39.9042,
  longitude: 116.4074,
  force: false,
})

// Updates the icon position and centers the map on the coordinates
this.$element('mapview').setLocation({
  latitude: 39.9042,
  longitude: 116.4074,
  force: true,
})
```

### `startNav(linePoints)`

Sets the navigation route and starts navigation. Once called, the map will automatically locate the route starting point and draw the complete route.

`linePoints` is an array of route points, where each element is a two-element array in the format `[longitude, latitude]`:

```js
const route = [
  [116.397428, 39.909736],  // [longitude, latitude]
  [116.404730, 39.913370],
  [116.410072, 39.918933],
]
this.$element('mapview').startNav(route)
```

::: warning
Pay attention to the parameter order: the first value of each coordinate point is **longitude**, and the second value is **latitude**, which is the reverse of the common "latitude first" convention.
:::

### `insetNavPoint(linePoints)`

Appends route points to the existing navigation route, using the same format as [`startNav()`](#startnav). Suitable for scenarios where route data is received in chunks. After appending, you need to call [`reload()`](#reload) to refresh the display.

```js
this.$element('mapview').insetNavPoint(newPoints)
this.$element('mapview').reload()
```

## Usage Examples

### Basic Map Display

The following example shows how to configure a basic map component, listen for missing tile events, and trigger downloads.

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
    // tiles: List of missing tiles, initiate download request to the server
    fetchTilesFromServer(tiles).then(() => {
      this.$element('map').reload()
    })
  },

  onDirectionInfo(info) {
    if (info.event === 'move') {
      // The user panned the map
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

### Navigation Route Drawing

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
    <button @click="startNavigation">Start Navigation</button>
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

### Low-Memory Device Adaptation

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
    // Determine whether to enable low-memory mode based on device memory tier
    this.isLowEndDevice = SysDevice.memoryProfile <= 4096
  },
}
```