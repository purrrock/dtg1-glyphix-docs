# mapview

地图组件，用于加载和显示基于瓦片（Tile）的地图。`mapview` 支持手势平移、缩放层级切换、当前位置显示以及路线导航绘制，是构建地图类应用的核心组件。

`mapview` 默认是块级元素。

::: tip
`mapview` 是运行时扩展组件，使用前需要确认目标平台已集成 `mapview` 模块。
:::

## 属性

### `baseUri` <decl type="string" get set />

瓦片图资源的**基础路径** URI，瓦片文件将在此目录下按固定层级结构存放。`mapview` 会根据当前缩放层级和坐标自动计算所需的瓦片文件路径，格式为：

```
{baseUri}/{zoomLevel}/{tileX}/{tileY}/normal.png     (标准地图)
{baseUri}/{zoomLevel}/{tileX}/{tileY}/satellite.png  (卫星地图)
```

典型用法是将地图瓦片缓存到设备本地存储，然后将 `baseUri` 指向对应目录：

```html
<mapview baseUri="internal://files/tiles/map_provider" />
```

### `tileType` <decl type="number" get set />

瓦片地图的图层类型，取值如下：

| 值 | 说明 |
| :-: | :-- |
| `0` | 标准地图（默认值），加载 `normal.png` 瓦片文件 |
| `1` | 卫星地图，加载 `satellite.png` 瓦片文件 |

### `loadPlace` <decl type="string" get set />

瓦片图加载中时显示的**占位图** URI。当对应的瓦片文件尚未缓存到本地时，`mapview` 会在该瓦片位置显示此图片，直到瓦片下载完成后触发 [`reload()`](#reload) 刷新。

```html
<mapview loadPlace="/assets/imgs/loading.png" />
```

### `zoomLevel` <decl type="number" get set />

地图缩放层级，取值范围为 $[3, 23]$，默认值为 $17$。层级越高，地图越详细；层级越低，可见范围越大。

::: info
该属性对应地图瓦片标准中的 Zoom Level（缩放级别），与 Bing Maps、Google Maps 等主流瓦片服务的层级定义一致。
:::

### `arrowIcon` <decl type="string" get set />

当前位置图标的图片 URI。该图标会绘制在 [`navCoordinate`](#navcoordinate) 或 [`setLocation()`](#setlocation) 所指定的经纬度对应的屏幕位置上，图标以中心点对齐坐标点。

```html
<mapview arrowIcon="/assets/imgs/location.png" />
```

### `navCoordinate` <decl type="{ x: number, y: number }" get set />

当前位置的经纬度坐标，格式为 `{ x: latitude, y: longitude }`，其中 `x` 为纬度，`y` 为经度。设置该属性仅更新图标位置，不会自动将地图中心移动到该坐标。若需要同时将地图中心定位到当前位置，请使用 [`setLocation()`](#setlocation) 方法并传入 `force: true`。

::: tip
对于需要跟踪实时位置的场景，推荐使用 [`setLocation()`](#setlocation) 方法替代直接赋值此属性，以便通过 `force` 参数控制是否自动回中。
:::

### `arrowLineWidth` <decl type="number" get set />

导航路线的线条宽度，单位为像素，默认值为 `12`。

### `arrowLineBackgroundColor` <decl type="color" get set />

导航路线的**背景色**（已走过部分的颜色），接受 CSS 颜色值，默认值为 `#898b90`。

### `arrowLineForgeColor` <decl type="color" get set />

导航路线的**前景色**（剩余路线部分的颜色），接受 CSS 颜色值，默认值为 `#4b73ec`。

### `smallMem` <decl type="boolean" get set />

是否开启低内存设备模式，默认值为 `false`。

开启后，`mapview` 会将四张 256×256 的瓦片合并缩放为一张 512×512 的图片进行绘制，减少内存中同时缓存的瓦片数量，以适配内存有限的设备。

::: warning
低内存模式会牺牲部分地图清晰度，仅在设备内存明显不足时开启此选项。
:::

### `missTiles` <decl type="Array<{ z: number, x: number, y: number }>" get listen />

只读属性，当地图发现本地缺失瓦片文件时触发监听。回调参数为一个数组，每个元素描述一张缺失的瓦片：

| 字段 | 类型 | 说明 |
| :-- | :-- | :-- |
| `z` | `number` | 缩放层级（Zoom Level） |
| `x` | `number` | 瓦片 X 坐标（列编号） |
| `y` | `number` | 瓦片 Y 坐标（行编号） |

收到该事件后，应用通常需要从服务器下载对应的瓦片文件，并在下载完成后调用 [`reload()`](#reload) 刷新地图：

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

地图事件的只读属性，当地图发生以下操作时触发监听：

| `event` 值 | 触发时机 | 附加字段 |
| :-- | :-- | :-- |
| `"move"` | 用户手势平移地图时触发 | 无 |
| `"calc"` | 导航中重新计算位置和偏航距离时触发 | `stepIndex`（当前路线段索引）、`distance`（当前位置到路线的偏离距离，单位米） |

```js
export default {
  onDirectionInfo(info) {
    if (info.event === 'move') {
      // 用户手动拖动了地图，可暂停自动回中
    } else if (info.event === 'calc') {
      console.log(`当前步骤：${info.stepIndex}，偏航距离：${info.distance} 米`)
    }
  }
}
```

## 方法

### `reload()`

重新加载所有瓦片。当新的瓦片文件写入本地存储后，需要调用此方法刷新地图显示。

```js
this.$element('mapview').reload()
```

### `locate()`

将地图中心移动到当前位置（[`navCoordinate`](#navcoordinate) 指定的坐标），用于"回到当前位置"功能。

```js
this.$element('mapview').locate()
```

### `setLocation(location)`

设置当前位置坐标，并可选择性地将地图中心移动到该位置。

| 参数字段 | 类型 | 说明 |
| :-- | :-- | :-- |
| `latitude` | `number` | 纬度 |
| `longitude` | `number` | 经度 |
| `force` | `boolean` | 为 `true` 时立即将地图中心定位到该坐标（等效于调用 [`locate()`](#locate)），为 `false` 时仅更新图标位置 |

```js
// 仅更新图标位置，不移动地图
this.$element('mapview').setLocation({
  latitude: 39.9042,
  longitude: 116.4074,
  force: false,
})

// 更新图标位置并将地图中心移动到该坐标
this.$element('mapview').setLocation({
  latitude: 39.9042,
  longitude: 116.4074,
  force: true,
})
```

### `startNav(linePoints)`

设置导航路线并开始导航。调用后地图会自动定位到路线起点，并绘制完整路线。

`linePoints` 为路线点数组，每个元素为 `[经度, 纬度]` 格式的二元数组：

```js
const route = [
  [116.397428, 39.909736],  // [经度, 纬度]
  [116.404730, 39.913370],
  [116.410072, 39.918933],
]
this.$element('mapview').startNav(route)
```

::: warning
注意参数顺序：每个坐标点的第一个值为**经度**（longitude），第二个值为**纬度**（latitude），与常见的"纬度在前"约定相反。
:::

### `insetNavPoint(linePoints)`

在现有导航路线中追加路线点，格式与 [`startNav()`](#startnav) 相同。适用于分段接收路线数据的场景。追加后需调用 [`reload()`](#reload) 刷新显示。

```js
this.$element('mapview').insetNavPoint(newPoints)
this.$element('mapview').reload()
```

## 使用示例

### 基础地图显示

以下示例展示了如何配置一个基础的地图组件，监听缺失瓦片事件并触发下载。

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
    // 初始化当前位置
    this.$element('map').setLocation({
      latitude: 39.9042,
      longitude: 116.4074,
      force: true,
    })
  },

  onMissTiles(tiles) {
    // tiles: 缺失瓦片列表，向服务器发起下载请求
    fetchTilesFromServer(tiles).then(() => {
      this.$element('map').reload()
    })
  },

  onDirectionInfo(info) {
    if (info.event === 'move') {
      // 用户平移了地图
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

### 导航路线绘制

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

### 低内存设备适配

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
    // 根据设备内存档位判断是否启用低内存模式
    this.isLowEndDevice = SysDevice.memoryProfile <= 4096
  },
}
```
