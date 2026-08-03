# image

The image component is used to display image elements and is centered by default. The `image` component is an inline element by default.

## Attributes

### `src` <decl type="string" get set />

Sets the [URI](/framework/application/resource.md) of the image. For asset images within the application package, both relative and absolute paths are supported. The `image` component supports common PNG and JPEG image formats.

::: tip
The `image` component only supports local image resources, unlike the web `img` element which can directly display network image resources. For details, please refer to how to [display network images](#displaying-network-images) in Glyphix.
:::

### `noCache` <decl type="boolean" get set />

Sets whether the image should be cached. By default, caching is used to optimize image loading speed. When the `noCache` property is enabled, the `image` component will not use the cache, and changing the [`src`](#src) property will always reload the image from the file.

Image caching is a technique to optimize loading speed and reduce memory usage. When an image with the same URI is already loaded in the system, an `image` component with caching enabled will use that resource directly. However, image files downloaded from the network with a fixed name and potentially changing content (such as user avatars like `internal://cache/avatar.png`) usually need the `noCache` property enabled to ensure correct behavior. 

Even with the `noCache` property enabled, the `image` component still does not detect updates to the image file content, and the [`src`](#src) property must be manually changed at this point. Considering that the reactive framework filters out identical assignment operations, you must use a trick like this:
``` html
<!-- Assuming this is the image that needs to be updated, the no-cache property is required. -->
<image :src="avatarImage" no-cache />
```

``` js
const avatarImage = 'internal://cache/avatar.png' // Assuming this is an image downloaded from the web

export default {
  data: {
    avatarImage: avatarImage
  },
  // Call this method after the avatar download completes to update the UI
  onAvatarDownloaded() {
    this.avatarImage = null // Must assign a new value first
    this.avatarImage = avatarImage // Reassign to the correct URI
  }
}
```
In the example above, the reactive property `this.avatarImage` is first changed to `null` and then reassigned. This causes the value to change, thereby bypassing the optimization mechanism of the reactive framework and achieving the image update.


::: warning
You must use this trick to update resources with a fixed URI, otherwise the displayed content may not change. To be safe, if the resource path obtained from the network may be repeated, you also need to use this trick to ensure the UI updates.

In addition, you must wait for the image download or file writing to complete before updating the `src` property of the `image` component, otherwise the UI cannot be updated properly.
:::

### `async` <decl type="boolean" get set />

Loads image resources asynchronously. This mode ensures that image loading does not block the UI thread, improving interface fluency. However, compared to the default synchronous loading mode, images loaded asynchronously will not display actual content immediately, making them unsuitable for all interfaces.

The asynchronous loading mode is suitable for images downloaded from the network. Unlike image assets that are automatically optimized when the application is packaged, network images are usually slow-to-decode generic formats like PNG or JPEG. Synchronously decoding network images can be very stuttery, and such scenarios usually do not require the image to be displayed immediately.

`async` can be used together with the [`noCache`](#nocache) property, as the latter is also mainly used for network images:
``` html
<image :src="avatarImage" no-cache async />
```

## Inherited Attributes

These attributes are inherited from the [generic attributes](/framework/generic/properties.md) of native components, but the `image` component treats them specially.

### `opacity` <decl type="number" set />

Sets the opacity of the image. The value range is $[0, 1]$, where $0$ means completely transparent, $1$ means completely opaque, and the default value is $1$.

### `transform` <decl type="string" set />

Sets the transformation effect of the image, equivalent to the CSS [`transform`](/framework/generic/styles.md#transform) property.

## CSS Notes

### Unsupported Generic Attributes

Compared to other native components, `image` is special in that it does not support generic attributes such as `background-color` and `border`. This is also very different from web standards. Specifically, the following CSS properties are not supported:

- [`background-color`](/framework/generic/styles.md#background-color), [`background-image`](/framework/generic/styles.md#background-image)
- [`border`](/framework/generic/styles.md#border), [`border-top`](/framework/generic/styles.md#border-top), [`border-right`](/framework/generic/styles.md#border-right), [`border-bottom`](/framework/generic/styles.md#border-bottom), [`border-left`](/framework/generic/styles.md#border-left)

This means you cannot add background colors or images to the `image` component by setting CSS properties, nor can you set border styles for it. However, the `image` component does support the [`border-radius`](/framework/generic/styles.md#border-radius) property.

### Special Attributes

The `image` component supports other CSS properties applicable to non-container components, but a few properties can be used to achieve special effects.

#### `transform`

Sets the transformation of the image. When this CSS property is used on `image`, its effect is similar to the [`transform`](/framework/generic/styles.md#transform) of other elements, but it can be displayed normally without setting the [`transparent`](/framework/generic/styles.md#transparent) property.

#### `opacity`

Sets the opacity of the image, which has the same effect as the [`opacity`](#opacity) property.

#### `border-radius`

Sets the corner radius of the image. You can use this property to add rounded corners to the image, and the usage is the same as the generic [`border-radius`](/framework/generic/styles.md#border-radius). The `image` component always applies rounded corners to all four corners of the image, regardless of whether the aspect ratio of the image matches that of the `image` component itself.

#### `object-fit`

The default value of the `object-fit` property for the `image` component is `none`, which differs from the web standard (where it defaults to `fill`). By default, images are not automatically scaled, but are centered and displayed at their original size. If the size exceeds the container, they are cropped. This design takes into account the characteristics of MCU devices:
- **Performance First**: Image scaling usually requires additional calculations, and some devices even implement interpolated scaling via software, which significantly reduces frame rates.
- **Image Quality Consistency**: On certain devices, even proportional shrinking may cause noticeable blurring or aliasing. Defaulting to no scaling ensures that pixel-level rendering effects are undistorted.
- **Memory Constrained**: Default scaling might mask resource usage issues, leading to the unintentional loading of overly large images, thereby wasting precious storage and memory space.

It is recommended to provide image resources that match the display area during the design stage, allowing images to display correctly in their default state as much as possible. Only when truly necessary should you adjust the display effect by explicitly setting `object-fit` (such as `contain`).

## Tips and Tricks

### Displaying Network Images

#### Avatar Scenarios

This section demonstrates a method for loading images from the network, which is mainly used in scenarios such as user avatars—where the image has a fixed storage location locally, but the content may change. Due to the caching strategy of the Glyphix runtime, you need to use the trick in this example to ensure the displayed content is updated.

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
    // For details on the trick here, refer to the description of the noCache property
    this.avatar = null
    this.avatar = saveFile
  }
}
```