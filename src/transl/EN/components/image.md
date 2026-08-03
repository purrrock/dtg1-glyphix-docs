# image


The picture component is used to display picture elements and is centered by default. `image` components are inline elements by default.


## property


### `src` <decl type="string" get set />


Set the [URI](/framework/application/resource.md) of the image. For asset images in the application package, relative paths and absolute paths are supported. The `image` component supports the common image formats PNG and JPEG.


::: tip

The `image` component only supports local image resources, unlike the Web's `img` element which can directly display network image resources. See How to [显示网络图片](#显示网络图片) in Glyphix for details.
:::



### `noCache` <decl type="boolean" get set />


Set whether the image should be cached. By default, caching will be used to optimize image loading speed. The `image` component will not use the cache when the `noCache` attribute is turned on, and the image will always be reloaded from the file after changing the [`src`](#src) attribute.


Image caching is a technology that optimizes loading speed and reduces memory usage. When an image with the same URI is already loaded in the system, the `image` component with caching enabled will directly use the resource. However, image files downloaded from the Internet with fixed names and possibly changing contents (such as `internal://cache/avatar.png` for user avatars) usually need to enable the `noCache` attribute to ensure correct behavior.


Even if the `noCache` attribute is turned on, the `image` component still will not detect updates to the image file content. In this case, you need to manually change the [`src`](#src) attribute. Considering that reactive frameworks filter identical assignments, you have to use a trick like this:
``` html
<!-- 假设这是需要更新显示的图片，no-cache 属性是必须的。 -->
<image :src="avatarImage" no-cache />
```


``` js
const avatarImage = 'internal:// cache/ avatar.png ' // Assume this is a picture downloaded from the Internet

export default {
  data: {
    avatarImage: avatarImage
  },
  // Call this method after the avatar download is completed to update the interface
  onAvatarDownloaded() {
    this.avatarImage = null // A new value must be assigned first
    this.avatarImage = avatarImage // Reassign to the correct URI
  }
}
```
In the above example, the responsive attribute `this.avatarImage` is first changed to `null` and then reassigned, so that the value changes, thereby bypassing the optimization mechanism of the responsive framework and enabling image updates.




::: warning

Resources with fixed URIs must be updated using this technique, otherwise the displayed content may not change. To be on the safe side, if the resource paths obtained from the network may be duplicated, you also need to use this technique to ensure that the interface is updated.


In addition, you must wait for the image download or file writing to be completed before updating the `src` attribute of the `image` component, otherwise the interface cannot be updated normally.
:::



### `async` <decl type="boolean" get set />


Load image resources asynchronously. This mode can ensure that image loading will not block the UI thread and improve the smoothness of the interface. However, compared to the default synchronous loading mode, images loaded asynchronously do not display the actual content, so they are not suitable for all interfaces.


Asynchronous loading mode is suitable for images downloaded from the network. Unlike image assets that are automatically optimized when the application is packaged, web images are usually common formats such as PNG or JPEG that are slow to decode. Synchronously decoding network images will be very laggy, and in such scenarios there is usually no need to display images immediately.


`async` can be used together with the [`noCache`](#nocache) attribute, since the latter is also mainly used for web images:
``` html
<image :src="avatarImage" no-cache async />
```


## Inherited properties


These properties are inherited from the native component's [generic properties](/framework/generic/properties.md), but the`image` component handles these properties specially.


### `opacity` <decl type="number" set />


Set the transparency of the image, the value range is $[0, 1]$, where $0$ means completely transparent, $1$ means completely opaque, and the default value is $1$.


### `transform` <decl type="string" set />


Set the transformation effect of the image, which is equivalent to the [`transform`](/framework/generic/styles.md#transform) attribute of CSS.


## CSS description


### Unsupported common properties


Compared with other native components, `image` is special. It does not support common attributes such as `background-color` and `border`. This is also very different from web standards. Specifically, the following CSS properties are not supported:


- [`background-color`](/framework/generic/styles.md#background-color), [`background-image`](/framework/generic/styles.md#background-image)
- [`border`](/framework/generic/styles.md#border), [`border-top`](/framework/generic/styles.md#border-top), [`border-right`](/framework/generic/styles.md#border-right), [`border-bottom`](/framework/generic/styles.md#border-bottom), [`border-left`](/framework/generic/styles.md#border-left)


This means that you cannot add a background color or image to the `image` component by setting CSS properties, nor can you set a border style for it. However, the `image` component supports the [`border-radius`](/framework/generic/styles.md#border-radius) attribute.


### Special properties


The `image` component supports other CSS properties that can be used with non-container components, but several properties can be used to achieve special effects.


#### `transform`


Set the transformation of the image. When this CSS attribute is used for `image`, it has a similar effect to [`transform`](/framework/generic/styles.md#transform) for other elements, but it can be displayed normally without setting the [`transparent`](/framework/generic/styles.md#transparent) attribute.


#### `opacity`


Set the transparency of the image, which has the same effect as the [`opacity`](#opacity) attribute.


#### `border-radius`


Set the corner radius of the picture. You can use this property to add rounded corners to the picture. The usage method is the same as the general [`border-radius`](/framework/generic/styles.md#border-radius). The `image` component will always apply rounded corners to the four corners of the image, regardless of whether the aspect ratio of the image is consistent with the aspect ratio of the `image` component itself.


#### `object-fit`


The `image` component's `object-fit` attribute defaults to `none`, which differs from the web standard (which defaults to `fill` ). By default, the image will not be automatically scaled, but will be displayed centered at the original size. If the size exceeds the container, it will be cropped. This design is based on the consideration of MCU device characteristics:
- **Performance first**: Image scaling usually requires additional calculations, and some devices even implement interpolation scaling through software, which will significantly reduce the frame rate.
- **Image quality consistency**: On some devices, even scaling down can cause noticeable blurring or aliasing. The default of no scaling ensures pixel-level rendering without distortion.
- **Memory Restricted**: Default scaling can mask resource usage issues, resulting in inadvertently loading images that are too large, wasting valuable storage and memory space.


It is recommended to provide image resources that match the display area during the design stage, so that the image can be displayed correctly in the default state; only when necessary, the display effect should be adjusted by explicitly setting `object-fit` (such as `contain`).


## Tips


### Show network pictures


#### Avatar scenes


This section demonstrates a method that requires loading images from the network. This method is mainly used in situations such as user avatars. That is, the images have a fixed storage location locally, but the content may change. Due to the caching policy of the Glyphix runtime, you need to use the techniques in this example to ensure that the display content is updated.


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
    // For details on the techniques here, see the description of the noCache attribute.
    this.avatar = null
    this.avatar = saveFile
  }
}
```
