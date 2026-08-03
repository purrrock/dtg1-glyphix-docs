# image

图片组件用于显示图片元素，默认居中对齐。 `image` 组件默认是行内元素。

## 属性

### `src` <decl type="string" get set />

设置图片的 [URI](/framework/application/resource.md)，对于应用包内的资产图片，支持相对路径和绝对路径。`image` 组件支持 PNG 和 JPEG 通用图片格式。

::: tip
`image` 组件只支持本地的图片资源，而不像 Web 的 `img` 元素可以直接显示网络图片资源。详情请参考如何在 Glyphix 中[显示网络图片](#显示网络图片)。
:::

### `noCache` <decl type="boolean" get set />

设置图片是否要进行缓存，默认情况下会使用缓存以优化图片加载速度。在开启 `noCache` 属性时 `image` 组件不会使用缓存，此时更改 [`src`](#src) 属性后总是会从文件中重新加载图片。

图片缓存是一种优化加载速度并减少内存占用的技术，当系统中已经加载了相同 URI 的图片时，开启缓存的 `image` 组件会直接使用该资源。但是从网络中下载的名称固定、内容可能变动的图片文件（如用户头像的 `internal://cache/avatar.png`）通常需要开启 `noCache` 属性才能保证行为正确。 

即便开启了 `noCache` 属性，`image` 组件依然不会检测图片文件内容的更新，此时需要手动更改 [`src`](#src) 属性。考虑到响应式框架会过滤相同的赋值操作，你必须使用这样的技巧：
``` html
<!-- 假设这是需要更新显示的图片，no-cache 属性是必须的。 -->
<image :src="avatarImage" no-cache />
```

``` js
const avatarImage = 'internal://cache/avatar.png' // 假设这是从网上下载的图片

export default {
  data: {
    avatarImage: avatarImage
  },
  // 在头像下载完成后调用这个方法以更新界面
  onAvatarDownloaded() {
    this.avatarImage = null // 必须先赋一个新的值
    this.avatarImage = avatarImage // 重新赋值为正确的 URI
  }
}
```
在上面的示例中，响应式属性 `this.avatarImage` 首先被更改为 `null`，然后再重新赋值，这样值会发生变化，从而绕过响应式框架的优化机制，并实现图片更新。


::: warning
必须使用此技巧更新固定 URI 的资源，否则显示内容可能不会变化。保险起见，如果从网络中获取的资源路径可能重复，那么也需要使用此技巧确保界面更新。

此外，必须等待图片下载或者文件写入完成后才能更新 `image` 组件的 `src` 属性，否则也无法正常更新界面。
:::

### `async` <decl type="boolean" get set />

使用异步的方式加载图片资源。这种模式可以保证图片加载不会阻塞 UI 线程，提升界面的流畅性。但是相比于默认的同步加载模式，异步加载中的图片不会显示实际内容，因此不适用于所有界面。

异步加载模式适用于从网络中下载的图片。与应用打包时会自动优化的图片资产不同，网络图片通常是 PNG 或者 JPEG 这类解码缓慢的通用格式。同步解码网络图片会非常卡顿，而且这类场景中通常不需要立即显示图片。

`async` 可以和 [`noCache`](#nocache) 属性一起使用，因为后者也主要用于网络图片：
``` html
<image :src="avatarImage" no-cache async />
```

## 继承的属性

这些属性继承自原生组件的[通用属性](/framework/generic/properties.md)，但是 `image` 组件对这些属性做了特殊处理。

### `opacity` <decl type="number" set />

设置图片的透明度，取值范围为 $[0, 1]$，其中 $0$ 表示完全透明，$1$ 表示完全不透明，默认值为 $1$。

### `transform` <decl type="string" set />

设置图片的变换效果，等效于 CSS 的 [`transform`](/framework/generic/styles.md#transform) 属性。

## CSS 说明

### 不支持的通用属性

相比于其他原生组件，`image` 比较特殊，它不支持 `background-color`、`border` 等通用属性。这一点和 Web 标准也是非常不同的。具体而言，以下 CSS 属性不受支持：

- [`background-color`](/framework/generic/styles.md#background-color), [`background-image`](/framework/generic/styles.md#background-image)
- [`border`](/framework/generic/styles.md#border), [`border-top`](/framework/generic/styles.md#border-top), [`border-right`](/framework/generic/styles.md#border-right), [`border-bottom`](/framework/generic/styles.md#border-bottom), [`border-left`](/framework/generic/styles.md#border-left)

这意味着不能通过设置 CSS 属性为 `image` 组件添加背景颜色或图片，也不能为其设置边框样式。不过 `image` 组件是支持 [`border-radius`](/framework/generic/styles.md#border-radius) 属性的。

### 特殊属性

`image` 组件支持其他可用于非容器组件的 CSS 属性，但是有几个属性可用于实现特殊的效果。

#### `transform`

设置图片的变换，该 CSS 属性用于 `image` 时和其他元素的 [`transform`](/framework/generic/styles.md#transform) 效果类似，但是不需要设置 [`transparent`](/framework/generic/styles.md#transparent) 属性也可以正常显示。

#### `opacity`

设置图片的透明度，和 [`opacity`](#opacity) 属性效果一样。

#### `border-radius`

设置图片的圆角半径，可以使用此属性为图片添加圆角，使用方法和通用的 [`border-radius`](/framework/generic/styles.md#border-radius) 相同。`image` 组件总是会将圆角应用到图片的四个角上，无论图片的长宽比和 `image` 组件本身的长宽比是否一致。

#### `object-fit`

`image` 组件的 `object-fit` 属性默认值为 `none`，这与 Web 标准（默认为 `fill`）不同。默认情况下，图片不会自动缩放，而是按原始尺寸居中显示，若尺寸超出容器则会被裁剪。这种设计是出于对 MCU 设备特性的考虑：
- **性能优先**：图片缩放通常需要额外的计算，部分设备甚至通过软件方式实现插值缩放，这会显著降低帧率。
- **画质一致性**：某些设备上，即使是等比缩小也可能导致明显的模糊或锯齿。默认不缩放可确保像素级渲染效果不失真。
- **内存受限**：默认缩放可能掩盖资源使用问题，导致无意中加载过大的图像，从而浪费宝贵的存储与内存空间。

建议在设计阶段就提供与显示区域匹配的图片资源，尽量让图像在默认状态下即可正确显示；只有在确有需要时，才应通过显式设置 `object-fit`（如 `contain`）来调整显示效果。

## 使用技巧

### 显示网络图片

#### 头像类场景

本节演示一种需要从网络上加载图片的方法，该方法主要用于用户头像等场合，即图片在本地有固定的存储位置，但是内容可能会变化。由于 Glyphix 运行时的缓存策略，你需要使用本示例中的技巧来确保显示内容更新。

``` html
<template>
  <image :src="avatar" no-cache />
</template>
```

``` js
import request from '@system.request'

export default {
  data: {
    avatar: null
  },
  onInit() {
    this.downloadAvatar()
  },
  async downloadAvatar() {
    const saveFile = 'internal://files/avatar.png'
    await request.download({
      url: 'https://example.com/url/to/avatar.png',
      filename: saveFile,
    }).complete
    // 此处技巧详见 noCache 属性的说明
    this.avatar = null
    this.avatar = saveFile
  }
}
```

