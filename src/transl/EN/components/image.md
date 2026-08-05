# image

The image component is used to display image elements and is centered by default. The `image` component is an inline element by default.

## Attributes

### `src` <decl type="string" get set />

Sets the [URI](/framework/application/resource.md) of the image. For asset images within the application package, both relative and absolute paths are supported. The `image` component supports common PNG and JPEG image formats.

::: tip
The `image` component only supports local image resources, unlike the Web `img` element which can directly display network image resources. For details, please refer to how to [display network images](#display-network-images) in Glyphix.
:::

### `noCache` <decl type="boolean" get set />

Sets whether the image should be cached. By default, caching is used to optimize image loading speed. When the `noCache` attribute is enabled, the `image` component will not use the cache, and changing the [`src`](#src) attribute will always reload the image from the file.

Image caching is a technique to optimize loading speed and reduce memory usage. When an image with the same URI is already loaded in the system, an `image` component with caching enabled will directly use that resource. However, image files downloaded from the network with fixed names but potentially changing contents (such as user avatars like `internal://cache/avatar.png`) usually require the `noCache` attribute to be enabled to ensure correct behavior.

Even if the `noCache` attribute is enabled, the `image` component still does not detect updates to the image file content. In this case, you need to manually change the [`src`](#src) attribute. Considering that the reactive framework filters out identical assignment operations, you must use a trick like this:
``` html
<!-- Assuming this is the image that needs to be updated and displayed, the no-cache attribute is mandatory. -->
<image :src="avatarImage" no-cache />
```

``` js
const avatarImage = 'internal://cache/avatar.png' // Assuming this is an image downloaded from the web

export default {
  data: {
    avatarImage: avatarImage
  },
  // Call this method after the avatar download is complete to update the interface
  onAvatarDownloaded() {
    this.avatarImage = null // Must assign a new value first
    this.avatarImage = avatarImage // Reassign to the correct URI
  }
}
```
In the example above, the reactive property `this.avatarImage` is first changed to `null` and then reassigned. This causes the value to change, thereby bypassing the reactive framework's optimization mechanism and achieving image updates.


::: warning
You must use this trick to update resources with a fixed URI, otherwise the displayed content may not change. To be safe, if the path of a resource obtained from the network may be duplicated, you also need to use this trick to ensure the interface updates.

In addition, you must wait for the image download or file write to complete before updating the `src` attribute of the `image` component, otherwise the interface cannot be updated properly.
:::

### `async` <decl type="boolean" get set />

Loads image resources asynchronously. This mode ensures that image loading does not block the UI thread, improving interface fluency. However, compared to the default synchronous loading mode, images in asynchronous loading will not display actual content immediately, so it is not suitable for all interfaces.

Asynchronous loading mode is suitable for images downloaded from the network. Unlike image assets that are automatically optimized when the application is packaged, network images are usually slow-to-decode common formats such as PNG or JPEG. Synchronously decoding network images can be very stuttery, and such scenarios usually do not require the image to be displayed immediately.

`async` can be used together with the [`noCache`](#nocache) attribute, as the latter is also mainly used for network images:
``` html
<image :src="avatarImage" no-cache async />
```

## Inherited Attributes

These attributes are inherited from the [generic attributes](/framework/generic/properties.md) of native components, but the `image` component handles them specially.

### `opacity` <decl type="number" set />

Sets the opacity of the image, with a value range of $[0, 1]$, where $0$ means completely transparent and $1$ means completely opaque. The default value is $1$.

### `transform` <decl type="string" set />

Sets the transformation effect of the image, equivalent to the CSS [`transform`](/framework/generic/styles.md#transform) property.

## CSS Notes

### Unsupported Generic Attributes

Compared to other native components, `image` is quite special as it does not support generic attributes such as `background-color` and `border`. This is also very different from web standards. Specifically, the following CSS properties are not supported:

- [`background-color`](/framework/generic/styles.md#background-color), [`background-image`](/framework/generic/styles.md#background-image)
- [`border`](/framework/generic/styles.md#border), [`border-top`](/framework/generic/styles.md#border-top), [`border-right`](/framework/generic/styles.md#border-right), [`border-bottom`](/framework/generic/styles.md#border-bottom), [`border-left`](/framework/generic/styles.md#border-left)

This means you cannot add a background color or image to the `image` component by setting CSS properties, nor can you set border styles for it. However, the `image` component does support the [`border-radius`](/framework/generic/styles.md#border-radius) property.

### Special Attributes

The `image` component supports other CSS properties available for non-container components, but a few properties can be used to achieve special effects.

#### `transform`

Sets the image transformation. When this CSS property is used on an `image`, its effect is similar to the [`transform`](/framework/generic/styles.md#transform) of other elements, but it can be displayed normally without setting the [`transparent`](/framework/generic/styles.md#transparent) property.

#### `opacity`

Sets the image opacity, which has the same effect as the [`opacity`](#opacity) attribute.

#### `border-radius`

Sets the corner radius of the image. You can use this property to add rounded corners to the image. The usage is the same as the generic [`border-radius`](/framework/generic/styles.md#border-radius). The `image` component always applies rounded corners to all four corners of the image, regardless of whether the aspect ratio of the image matches that of the `image` component itself.

#### `object-fit`

The default value of the `object-fit` property for the `image` component is `none`, which differs from the web standard (where it defaults to `fill`). By default, images are not automatically scaled, but are centered and displayed at their original size. If the size exceeds the container, it will be cropped. This design is based on the characteristics of MCU devices:
- **Performance First**: Image scaling usually requires extra computation, and some devices even implement interpolated scaling via software, which significantly reduces the frame rate.
- **Image Quality Consistency**: On certain devices, even proportional scaling can cause noticeable blurring or aliasing. Not scaling by default ensures that pixel-level rendering remains undistorted.
- **Memory Constrained**: Default scaling may mask resource usage issues, leading to the accidental loading of oversized images, thereby wasting precious storage and memory space.

It is recommended to provide image resources that match the display area during the design stage, allowing images to be displayed correctly in their default state as much as possible; only when truly necessary should the display effect be adjusted by explicitly setting `object-fit` (such as `contain`).

## Usage Tips

### Displaying Network Images

#### Avatar Scenarios

This section demonstrates a method for loading images from the network. This method is mainly used for occasions such as user avatars, where the image has a fixed storage location locally, but the content may change. Due to the caching strategy of the Glyphix runtime, you need to use the trick in this example to ensure that the displayed content is updated.

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
    // For details on the trick here, refer to the description of the noCache attribute
    this.avatar = null
    this.avatar = saveFile
  }
}
```