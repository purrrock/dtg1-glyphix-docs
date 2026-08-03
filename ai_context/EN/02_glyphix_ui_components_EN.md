# Context File: 02_glyphix_ui_components_EN.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/transl/EN/components/span.md

# span

`span` is also a text component. Unlike the [`p` component](p), the `span` component is an inline element by default and can span across multiple lines, similar to the [`label`](label) and [`a`](a) components. Text spanning across lines means the element can lay out across multiple lines instead of occupying an entire "box".

The `span` component can be used to implement [rich text layout](/framework/render/rich-text.md#富文本显示).

<glyphix id="span" :height="36">

``` html
<div>
  Hello Glyphix, this is <span style="color: #f0f">span</span> label!
</div>
```

</glyphix>

============================================================
FILE_PATH: src/transl/EN/components/canvas.md

# canvas

Canvas component. Using scripts in JavaScript, you can draw graphics and more on the `canvas`.

### `context`

**Value Type**: The context content obtained from the canvas API

**Operation**: Set

Sets the context for drawing graphics on the canvas.

============================================================
FILE_PATH: src/transl/EN/components/marquee.md

# marquee

The `marquee` component is used to display scrolling text content and only supports single-line display. The `marquee` component does not support any child components, including `span`.

`marquee` supports general CSS properties, but due to implementation reasons, the `text-align` property may not be supported at the moment. Since `marquee` only displays a single line of text and scrolls it when the content is too long, properties like `max-lines` have no effect.

## Attributes

### `text` <decl type="string" get set/>

Sets the text content, which is used in the same way as the [`text`](p.md#text) attribute of the `p` component. When the length of the text content exceeds the width of the `marquee`, the text will automatically scroll.

============================================================
FILE_PATH: src/transl/EN/components/scroll-bar.md

# scroll-bar

Scroll bar component. This component displays a scroll bar when there is a large amount of scrollable content, allowing users to control content scrolling via the scroll bar.

## Attributes

### `value` <decl type="number" set get listen />

The current value of the scroll bar. This value is between `min` and `max`, with a default value of $0$.

### `min` <decl type="number" set />

The minimum value of the scroll bar. This value should not be greater than `max`. The default value is $0$.

### `max` <decl type="number" set />

The maximum value of the scroll bar. This value should not be less than `min`. The default value is $100$.

### `pagestep` <decl type="number" set />

The scroll step size of the scroll bar, which is the distance scrolled per step. The default value is $10$.

============================================================
FILE_PATH: src/transl/EN/components/p.md

# p

Text component. `p` is a block-level element by default. Unlike [`span`](span), the `p` component does not support text wrapping across lines even when set as an inline element. If rich text layout is required, you should consider using components like `span`.

## Properties

### `text` <decl type="string" get set/>

Sets the text content. Supports the following two writing formats:

``` html
<p text="Hello Glyphix"></p>
<p>Hello Glyphix</p>
```

<glyphix id="p" :height="70" inline>

``` html
<div>
  <p text="Hello Glyphix"></p>
  <p>Hello Glyphix</p>
</div>
```

</glyphix>

### `color` <decl type="string" get set/>

Sets the text color. Only hexadecimal color codes are supported, such as `#f00`, `#e8bb80ff`, etc. This property is a shorthand for modifying the CSS inline property [`color`](/framework/generic/styles.md#color).

### `lines` <decl type="number" get set/>

Sets the maximum number of lines for the text. Text exceeding this number of lines will be truncated or omitted. This property is a shorthand for modifying the CSS inline property [`max-lines`](/framework/generic/styles.md#max-lines).

### `text-align` <decl type="string" set/>

Sets the text alignment. Supports values such as `left`, `center`, `right`, etc. This property is a shorthand for modifying the CSS inline property [`text-align`](/framework/generic/styles.md#text-align).

### `font-size` <decl type="string" set/>

Sets the font size of the text. Supports CSS font size values like `12px`, `1.5em`, etc. This property is a shorthand for modifying the CSS inline property [`font-size`](/framework/generic/styles.md#font-size).

### `font-weight` <decl type="number" set/>

Sets the font weight of the text. Currently, only integer values are supported, such as `400`, `600`, etc. This property is a shorthand for modifying the CSS inline property [`font-weight`](/framework/generic/styles.md#font-weight).

## Tips & Tricks

### Size Control

In general, you should avoid manually setting the height of the `p` component. For example:
``` css
p.my-paragraph {
  height: 48px;
  font-size: 32px;
}
```
On the surface, this sets a height greater than the font size for the `p` component, but in reality:
- For single-line text, the actual height of certain fonts may exceed the font size, and vertical clipping may occur even with a height of `48px`.
- For multi-line text, setting a fixed height will cause the multi-line text to be clipped, preventing it from displaying completely.

If you want to control the number of displayed lines of text, you should use [`max-lines`](/framework/generic/styles.md#max-lines) and [`text-overflow`](/framework/generic/styles.md#text-overflow) to achieve text truncation and omission, rather than setting a fixed height.

### Text Clipping Animation <version-badge since="0.9"/>

You can use the [`width`](/framework/generic/styles.md#width) property combined with the [`transition`](/framework/component/prop-modifier.md#transition-modifier) modifier to achieve a text clipping animation. For example:

``` html
<p :width="state ? 240 : 0"
   width.transition="{duration: 2.0}">
  Hello Glyphix!
</p>
```

Combined with the `max-lines: 1` style, this can achieve a left-to-right text clipping animation. However, there is a problem with this animation: when the width is insufficient, the last character is dropped directly instead of being clipped. The current workaround is to place the text content inside a child component and apply the width animation to the parent component:

``` html
<div :width="state ? 240 : 1"
     width.transition="{duration: 2.0}">
  <p style="max-lines: 1">Hello Glyphix!</p>
</div>
```

<glyphix id="p-width-transition" title="Text Clipping Animation" height="120">

``` html
<div class="container">
  <p class="animated-text"
     :width="state ? 240 : 0"
     width.transition="{duration: 2.0}">
    Hello Glyphix!
  </p>
  <div class="animated-text"
       :width="state ? 240 : 1"
       width.transition="{duration: 2.0}">
    <p>Hello Glyphix!</p>
  </div>
</div>
```

``` js
export default {
  data: {
    state: false
  },
  onReady() {
    setInterval(() => this.state = !this.state, 2500)
  }
}
```

```css
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.animated-text {
  margin: 4px;
  border: 1px solid #f00;
}

p {
  max-lines: 1;
  text-overflow: clip;
}
````

</glyphix>

However, when using a `div` element as the parent component, the animation has an issue: when the width is `0`, the layout dimensions calculate to `(width: 0, height: 0)`, which causes the element to fail to occupy vertical space, resulting in a vertical jump at the start of the animation. The solution is to set the width to a very small value (e.g., `1px`) instead of `0` so that the element can still occupy vertical space, thereby avoiding the jumping issue.

============================================================
FILE_PATH: src/transl/EN/components/div.md

# div

`div` is the most basic container component. `div` supports child components and layout, but does not support scrolling (content exceeding the boundaries will be clipped directly). If you want content to scroll, please use the [scroll](scroll) component.

## Notes

### Text Display

The `div` component cannot be used to display text directly; instead, text components such as `p` must be used. For example:

```html
<!-- Incorrect usage, text will not be displayed -->
<div>text content.</div>
<!-- Correct usage -->
<p>text content.</p>
```

However, if there are multiple child elements inside the `div`, text can be included as its child element:

```html
<div>
  first element,
  <span style="color: #f0f">second element.</span>
</div>
```

<Glyphix id="components-div-text-element" height="48" width="360" inline >

```html
<div>
  first element,
  <span style="color: #f0f">second element.</span>
</div>
```

</Glyphix>

============================================================
FILE_PATH: src/transl/EN/components/image-animator.md

# image-animator

The `image-animator` component is used to play a sequence of image frames as an animation. By default, it is an inline element.

<glyphix id="image-animator-1" height="190" width="360" >

```html
<div class="flex-column">
  <div class="frame-box">
    <image-animator :images="frames" :play="play" :duration="100" />
  </div>
  <div>
    <button on:click="play = 'start'">start</button>
    <button on:click="play = 'pause'">pause</button>
    <button on:click="play = 'stop'">stop</button>
  </div>
</div>
```

```js
export default {
  data: {
    play: "stop",
  },
  frames: Array.from({ length: 60 }, (_, i) => `/assets/planet-${i}.png`),
};
```

```css
.flex-column {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.frame-box {
  border: 2px solid lightgray;
  border-radius: 8px;
  padding: 8px;
}

button {
  border-radius: 8px;
  background-color: #dee2e6;
  margin: 8px;
  padding: auto 12px;
}

button:active {
  opacity: 0.5;
}
```

</glyphix>

## Properties

### `images` <decl type="string[]" set />

Sets the collection of sequence frame images. Each element in `images` is the path or URI of that frame's image. Typically, the dimensions of each frame are consistent.

Supports PNG or JPEG format images.

If the frame sequence does not change, it is recommended to define it as a non-reactive property to save memory:

```js
export default {
  // frames is a non-reactive property of the component
  frames: [
    "/assets/sprite-1.png",
    "/assets/sprite-2.png",
    "/assets/sprite-3.png",
  ],
};
```

The benefit of this is that multiple component instances will share the same `frames` array object (reactive properties are copied to each component instance). You should only place it in the `data` object if the frame sequence truly needs reactivity.

If the frame sequence is sequentially encoded, you can use this trick to simplify the creation of the frames array:

```js
export default {
  // 4 frames numbered starting from 0
  frames: Array.from({ length: 4 }, (_, i) => `/assets/sprite-${i}.png`),
  // Or, 4 frames numbered starting from 1
  frames: Array.from({ length: 4 }, (_, i) => `/assets/sprite-${i + 1}.png`),
};
```

Pass the `frames` array to the `images` property in the component template to specify the frame sequence and play the animation:

```html
<image-animator :images="frames" play :duration="100" />
```

::: note
The `images` property does not yet support Quick App's `ImageFrame` structure, so you cannot use frame collection definitions like `[{ src: '...' }, ...]`.
:::

### `duration` <decl type="number" get set />

Specifies the playback duration of each frame, in milliseconds.

### `play` <decl type="'start' | 'pause' | 'stop'" get set listen />

Sets the playback state, supporting start, pause, and stop states. `image-animator` is initially in the `stop` state and will therefore automatically stay at the first frame of [`images`](#images).

|   Value   | Description                         |
| :-------: | ----------------------------------- |
| `'start'` | Starts playing from the current frame. |
| `'pause'` | Pauses playback and displays the current frame. |
| `'stop'`  | Stops playback and displays the first frame. |

As shown above, `play` only supports the three enumerated values `'start'`, `'pause'`, or `'stop'`. However, the following trick can be used to automatically play the animation:

```html
<image-animator :images="frames" play :duration="100" />
```

Writing the `play` property without a value is equivalent to the [implicit property value](/framework/component/template.md#隐式属性值) syntax of `:play="true"`. Boolean types like `true` are always converted to the default `'start'` enumerated value. This syntax is very useful for scenarios where you need to automatically play a frame sequence animation.

### `iteration` <decl type="number" set />

Sets the number of repetitions for all frames in `images`. When the limit is reached, it will automatically switch to `'pause'` mode. `0` indicates infinite playback.

## Inherited Properties

`image-animator` shares the same [inherited property](/components/image.md#继承的属性) behavior as `image`.

## CSS Notes

`image-animator` shares the same [CSS behavior](/components/image.md#css-说明) as `image`.

============================================================
FILE_PATH: src/transl/EN/components/drawer-navigation.md

# drawer-navigation

A sub-component of [`drawer`](drawer) used to display the specific drawer content.

## Properties

### `direction` <decl type=" 'left' | 'right' | 'up' | 'down' " set />

The `direction` property is used to set the direction of `drawer-navigation`. Available values are `'left'`, `'right'`, `'up'`, and `'down'`.

|   Value   | Description                                              |
| :-------: | -------------------------------------------------------- |
| `'left'`  | A drawer-navigation on the left side of the screen, used to respond to gestures swiping from left to right. |
| `'right'` | A drawer-navigation on the right side of the screen, used to respond to gestures swiping from right to left. |
|  `'up'`   | A drawer-navigation at the bottom of the screen, used to respond to gestures swiping from bottom to top. |
| `'down'`  | A drawer-navigation at the top of the screen, used to respond to gestures swiping from top to bottom. |

============================================================
FILE_PATH: src/transl/EN/components/text.md

# text

The text component, the `text` component and the [`p` component](p) are identical except for their component names.

============================================================
FILE_PATH: src/transl/EN/components/picker.md

# picker

A text picker component. This component displays a set of texts. Clicking the middle text item triggers a selection event, while swiping allows all text items to be scrolled.

::: warning
The functionality of the `picker` component is unverified and unmaintained.
:::

## Properties

### `range` <decl type="string[]" set />

All strings in the `range` property value will be displayed in the `picker` component. Users can scroll or select these strings within the `picker` component.

For the indexing method of the strings in the `range` property value, refer to the [`index` property](#index).

### `loop` <decl type="boolean" set />

Configures whether the `picker` component displays in a looping (i.e., infinite) manner. When this property is set to `true`, looping is enabled. The default value is `false`.

### `value` <decl type="string" listen />

Listens to the text of the currently selected item. This listener is triggered when the selected item changes during scrolling. The functionality of this property can also be achieved using `on:index="handle(rangeData[$event])"`.

### `index` <decl type="Integer" get set listen />

The selected item index of the `picker` component. The indexing rule is: the index of the first string item in the [`range` property](#range) value array is $0$, and the indices of subsequent strings increment by one. Setting the `index` property specifies the selected item of the `picker` component, and you can also listen to changes in this property to detect selected item changes caused by scrolling operations.

### `scroll` <decl type="{ x: number y: number }" get set listen />

The `scroll` property can be used to listen to scrolling operations, as well as to programmatically control scrolling effects in the `picker` component. Similar to aligned list components, the `scroll` operation of the `picker` will snap to the nearest item.

Since the `picker` component only supports vertical mode, the `x` field of the `scroll` property value is always `0`.

### `scrolled` <decl type="boolean" read listen />

Listens to whether the `picker` is in a scrolling state via the `scrolled` property. A property value of `true` triggered by the event indicates that the `picker` is scrolling, otherwise it means the `picker` has stopped scrolling.

Both user touch-induced scrolling and programmatic scrolling via the `scroll` property will trigger the `scrolled` event. When the `picker` stops from a scrolling state, the parameter value of the `scrolled` event is `false`.

### `damping` <decl type="number" set />

Sets the damping coefficient for the `picker` scrolling animation. The valid value range is $[0.1, 50]$ (unsupported values will be automatically clamped to the upper or lower limits), with a default value of $1.5$. A larger damping coefficient causes the animation to stop faster; the default damping coefficient produces a relatively long-distance and long-duration inertial effect.

The damping coefficient should be set as a constant rather than modified; modifying the damping coefficient will not affect the bounce-back animation.

============================================================
FILE_PATH: src/transl/EN/components/drawer.md

# drawer

The drawer component is hidden by default and can display content through sliding gestures.
The drawer is a basic drawer component. It supports sub-components and layouts, and you can place up to four `drawer-navigation` components inside a drawer to display drawers from the top, bottom, left, and right positions.

The sliding speed of the [`drawer`](drawer) component follows the gesture sliding speed: the faster the gesture, the faster the component slides.

### Example

The following example demonstrates the functionality of the drawer.

<glyphix id="components-drawer" height="360" width="360" >

``` html
 <drawer class="drop-down">
      <drawer-navigation direction="down" class="drop-down1">
        <p>dawn panel</p>
      </drawer-navigation>
      <drawer-navigation direction="up" class="drop-down1">
        <p>up panel</p>
      </drawer-navigation>
       <drawer-navigation direction="left" class="drop-down1">
        <p>left panel</p>
      </drawer-navigation>
       <drawer-navigation direction="right" class="drop-down1">
        <p>right panel</p>
      </drawer-navigation>
</drawer>
```
``` css
.drop-down {
    background-color: pink;
  }
.drop-down1 {
    background-color: blue;
  }
p {
  background-color: lightgreen;
  text-align: center;
  margin: 10px;
}
```
</glyphix>

============================================================
FILE_PATH: src/transl/EN/components/switch.md

# switch

The switch selection component, which is an inline element by default. It is used to represent two states (on/off) and allows the user to toggle between them. The function of `switch` is similar to `checkbox`, but their interaction effects and intents are different, representing switches and checkboxes respectively.

<glyphix id="components-switch" height="30">

``` html
<div>
  <switch ::value="enabled" />
  <span>switch state: {{ enabled ? 'on' : 'off' }}</span>
</div>
```

``` js
export default {
  data: {
    enabled: false
  }
}
```
</glyphix>

::: note
The style of the `switch` component is typically as shown in the example, but it may vary depending on the device. In particular, the width of the `switch` may differ across devices, and developers should reserve appropriate layout margins.
:::

## Attributes

### `value` <decl type="boolean" set get listen/>

Represents the state of the `switch`. When the value is `true`, the `switch` is in the on state; otherwise, it is in the off state. When the `value` attribute is not specified, the `switch` component is off by default.

### `checked` <decl type="boolean" set get/>

This is a Quick App compatibility attribute. Using [`value`](#value) is generally recommended instead.

### `change` <decl type="{ checked: boolean }" get listen/>

This is a Quick App compatibility attribute. Using [`value`](#value) is generally recommended instead.

## CSS Behavior

The overall style of the `switch` component is determined by the system and is not controlled by the developer, much like the style differences between [Fluent 2](https://fluent2.microsoft.design/components/web/react/switch/usage) and [Material 3](https://m3.material.io/components/switch/overview). Glyphix allows customizing the color of the `switch` in CSS and adjusting its size.

### CSS Properties

#### `color`

Sets the color of the `switch` component's thumb. Unlike general CSS [`color`](/framework/generic/styles.md#color), the `color` property of the `switch` does not support inheritance, so you must define it directly on the current `switch` component.

<glyphix id="components-switch-color" height="36" title="siwtch thumb color">

``` html
<div>
  red color: <switch class="red"/>,
  not inherited: <switch/>
</div>
```

``` css
div {
  color: red; /* Note: switch does not inherit the color property */
}

.red {
  color: red; /* color must be defined on the switch component's style */
}
```
</glyphix>

#### `background-color`

Controls the background color of the `switch` component. See the documentation for the [`active`](#active) pseudo-class for details.

#### `font-size`

You can use the [`font-size`](/framework/generic/styles.md#font-size) CSS property to adjust the size of the `switch` so that its inline text size coordinates harmoniously. The following example demonstrates the relationship between `font-size` and the size of the `switch`:

<glyphix id="components-switch-size" height="100" title="font-size and switch size">

``` html
<div>
  <p class="title">
    title text: <switch/> (1.25rem)
  </p>
  <p>
    content text: <switch/> (1rem)
  </p>
</div>
```

``` css
div {
  line-height: 1.8rem;
}

.title {
  color: #415a77; /* Note: switch does not inherit the color property */
  font-size: 1.25rem;
}
```
</glyphix>

::: warning
The display size of the `switch` is not controlled by properties such as `width` and `height`, but is always determined by `font-size`. Therefore, please do not manually specify dimension properties like `width` to avoid abnormal rendering.
:::

### CSS Pseudo-classes

#### `active`

The `active` pseudo-class is used to define the style of the `switch` when it is in the on state. As shown in the example below, it is usually configured alongside regular style rules:

<glyphix id="components-switch-colors" height="36" title="siwtch thumb color settings">

``` html
<div>
  color switch: <switch/>
</div>
```

``` css
/* Style when the switch is off */
switch {
  color: #415a77;
  background-color: #bde0fe;
}

/* Style when the switch is on */
switch:active {
  color: #fefae0;
  background-color: #ffafcc;
}
```
</glyphix>

This example controls the color style of the `switch` when toggled using the `color` and `background-color` CSS properties. The `switch` component will only respond to the configuration of these two CSS properties even when the `active` pseudo-class is activated.

::: tip
Please define both the `color` and `background-color` properties for both the normal state and the `active` state; otherwise, the `switch` will not transition colors accordingly when toggled.
:::

============================================================
FILE_PATH: src/transl/EN/components/image.md

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

============================================================
FILE_PATH: src/transl/EN/components/barcode.md

# barcode

The `barcode` component is used to display [Code 128](https://en.wikipedia.org/wiki/Code_128) barcodes. The `barcode` component can display any ASCII string, making it suitable for showing product barcodes, payment codes, and other information.

In flow layout, the `barcode` component defaults to a block-level element (`block`) and occupies an entire row by itself.

## Attributes

### `value` <decl type="string" get set />

Sets the content to be displayed by the barcode. Supports any ASCII string.

## CSS Notes

To make the barcode easily scannable, you should correctly set the CSS properties of the `barcode` component, which include:
- `color`: The color of the barcode bars, usually set to black (`black` or `#000`);
- `background-color`: The background color of the barcode, which should typically be white (`white` or `#fff`);
- `padding` / `margin`: Sufficient inner and outer margins prevent the barcode from blending with other elements, increasing the scan recognition rate;
- `width` / `height`: The dimensions of the barcode must be large enough to be easily captured by a camera.

By default, each bar of the barcode component occupies $2\rm px$ in width and $32\rm px$ in height. This may be too small on small-screen devices such as smartwatches. Developers are advised to manually set the `width` and `height` properties of the barcode component as needed and test them on actual devices.

The example below demonstrates how to use the barcode component. Please note that various margins are set for the `barcode` component in the CSS to ensure there is enough space between the barcode and other UI elements to avoid interfering with scanning.

<glyphix id="barcode-1" :height="150" :width="350">

``` html
<div>
  <barcode :value="text"/>
  <p>{{ text }}</p>
</div>
```

``` js
export default {
  data: {
    text: '9787111407010'
  }
}
```

``` css
div {
  background-color: black;
  padding: 8px;
}

barcode {
  margin: 8px;
  padding: 8px;
  color: black; /* Set the barcode foreground color to black */
  background-color: white; /* Set the barcode background color to white */
  border-radius: 16px;
  height: 80px;
}

p {
  color: white;
  font-size: 0.75rem;
  text-align: center;
}
```

</glyphix>

::: tip
You should always explicitly set **high-contrast** styles for the barcode component's bar color (`color`) and background (`background-color`). This prevents reduced readability caused by discrepancies in the device's default style themes or inherited style properties.

Additionally, please set a sufficiently large padding (`padding`) to ensure easy scanning and recognition.
:::

============================================================
FILE_PATH: src/transl/EN/components/slider.md

# slider

Slider component, which defaults to a block-level element.

## Attributes

### `value` <decl type="number" get set listen />

Current value, default value: $10$.

Setting the `value` attribute will change the current value of the component. You can listen to changes in the current value using the `on` directive, which is triggered every time the current value changes.

### `min` <decl type="number" set />

Minimum value, default value: $0$.

### `max` <decl type="number" set />

Maximum value, default value: $100$.

### `vertical` <decl type="boolean" set />

If the value of the `vertical` attribute is `true`, the `slider` component will be displayed vertically; otherwise, it is displayed horizontally. The default value is `false`.

## CSS Specifications

Developers can customize the appearance of the `slider` component using CSS.

### Size Calculation

The default width and height of the `slider` are the same as the font size of the element, which is set by the [`font-size`](/framework/generic/styles.md#font-size) attribute (or inherited). The size of the `progress` can be customized using the [`width`](/framework/generic/styles.md#width) and [`height`](/framework/generic/styles.md#height) attributes.

### CSS Attributes

The following CSS attributes may be very useful:
- [`background-color`](/framework/generic/styles.md#background-color) can control the background color of the `slider`;
- [`color`](/framework/generic/styles.md#color) can control the progress bar color of the `slider`;
- [`border-radius`](/framework/generic/styles.md#border-radius) can set the `slider` to have rounded borders, for example, `50%` will produce semi-circular borders;

Other CSS attributes may also be useful, such as using the [`border`](/framework/generic/styles.md#border) attribute to set border styles.

### CSS Pseudo-elements

#### `value`

This pseudo-element can be used to separately define the style of the `slider` progress bar without including the background part. For example, you can set the border-radius of the track background and the progress bar part separately to achieve an effect where the outer border has rounded line caps while the progress bar has flat caps.

``` css
slider {
  border-radius: 50%; /* Track background border radius */
}

slider::value {
  border-radius: 0; /* Progress bar has no border radius */
}
```

#### `thumb` <experimental/>

The `thumb` pseudo-element is used to define the style of the `slider` thumb. By default, the `slider` does not include a thumb; to display a thumb, the width and height of the `thumb` element must be specified:
``` css
slider::thumb {
  width: 150%;
  height: 150%;
  border-radius: 50%;
}
```
Percentage-based `width` and `height` are calculated relative to the element's own dimensions. The width and height of the thumb for a horizontal `slider` are calculated based on the element's CSS `height`, while the thumb's width and height for a vertical `slider` are calculated based on the element's CSS `width` attribute. For example, if the element's CSS is:
``` css
slider {
  width: 200px;
  height: 24px;
}
```
Then the width and height of the thumb corresponding to the above `slider::thumb` are both $24\rm{px} \times 150\% = 36\rm{px}$. The percentage-based border-radius dimension of the thumb is calculated based on the thumb's own dimensions. In this example, the calculated border-radius value for a `50%` `thumb` pseudo-element is $36\rm{px} \times 50\%=18\rm{px}$.

The `thumb` pseudo-element supports the `border` CSS attribute, but the border will not exceed the dimensions of the `thumb` pseudo-element.

### CSS Examples

The following example demonstrates some ways to customize the appearance of the progress bar using CSS.
<glyphix id="components-slider-styles" height="180" width="480" title="Slider Style">

``` html
<div>
  <!-- Default style -->
  <slider ::value="value" />
  <!-- Flat-head progress bar style -->
  <slider class="flat" ::value="value" />
  <slider class="more-style" ::value="value" />
  <p>value: {{value}}</p>
</div>
```

``` css
div > * {
  margin: 8px;
  padding: 6px;
}

.flat::value {
  /* Set the border-radius of the value pseudo-element to 0 to achieve a flat-head progress bar effect */
  border-radius: 0;
}

.more-style {
  /* Custom border radius */
  border-radius: 30%;
  /* slider background color */
  background-color: #b3c5d7;
  /* slider foreground color */
  color: #b5179e;
  /* padding can adjust the margin of the slider foreground */
  padding: 6px;
  height: 1rem;
}

/* Define the slider thumb style */
.more-style::thumb {
  width: 300%; /* Capsule-shaped thumb with a 2:1 aspect ratio */
  height: 150%;
  background-color: white;
  border: 4px solid #f3722c; /* Thumb border */
  border-radius: 50%;
}
```

``` js
export default {
  data: { value: 50 }
}
```

</glyphix>

============================================================
FILE_PATH: src/transl/EN/components/textarea.md

# textarea

`textarea` <experimental/><version-badge since="0.9" /> is a multi-line text input component, which defaults to displaying as a block-level element. Unlike similar GUI elements on mobile phones or PCs, `textarea` currently does not respond to input devices such as keyboards, nor does it pop up an input method editor (IME) interface, so you must manually edit its content. `textarea` supports operating the caret via touch gestures (such as clicking and scrolling) and provides methods to move the caret up, down, left, and right.

`textarea` is suitable as the underlying component for multi-line text input, allowing you to implement your own soft keyboard and caret control according to your needs. For details, please refer to the [Example](#basic-example).

::: important Compatibility
`textarea` is an experimental extended component, currently available only in Glyphix version 0.9 and above, and is supported on only some devices.
:::

## Properties

### `text` <decl type="string" get set listen />

The `text` property is a string representing the currently edited text content of the `textarea`. Reading or listening to this value retrieves the input text, and this property can also be set.

Usually, `text` is two-way bound to a specific reactive property, or the text can be set via the content inside the element, such as:

```html
<textarea ::text="inputText" />
```

Or:

```html
<textarea @text="onTextChanged">{{ inputText }}</textarea>
```

:::tip
The `text` property of `textarea` is functionally similar to the [`value`](text-field.md#value) property of [`text-field`](text-field.md).
:::

### `placeholder` <decl type="string" set get />

When the content of `textarea` is empty, `placeholder` can be used to provide a short hint to the user, such as phrases like "Please enter text".

`placeholder` automatically displays when the input text is empty, so it usually only requires fixed content, such as:

```html
<textarea ::text="inputText" placeholder="type here" />
```

### `insert` <decl type="(text: string): void" method />

Inserts a piece of text with the content `text` at the current caret position, and the caret automatically moves after the inserted text. Calling this function triggers a `text` listening event.

### `backspace` <decl type="(): void" method />

Deletes the character at the current caret position, and the caret automatically moves forward. Calling this function triggers a `text` listening event.

### `moveCaret` <decl type="(direction: 'up' | 'down' | 'left' | 'right'): void" method />

Moves the caret one position in the specified direction. The optional values for the `direction` parameter are `'up'`, `'down'`, `'left'`, and `'right'`, corresponding to the four directions: up, down, left, and right.

## Usage Instructions

### Basic Example

The following example demonstrates the basic usage of `textarea`. Users can directly input multi-line text in the text box or use the virtual keyboard below to edit the content: tap letter/symbol keys to characters; the "`×`" key deletes content at the caret; the "`Aa`" key toggles case; the "`1#`" key switches to the symbol keyboard; the "`Enter`" key inserts a newline character; arrow keys move the caret.

<glyphix id="components-textarea-basic" width="560" height="360" title="Textarea Basic Example">

```html
  <div class="window">
    <textarea
      id="textarea"
      :placeholder="placeholder"
      @text="onTextChanged"
    >
      {{ text }}
    </textarea>
    <div class="keyboard">
      <div class="kb-row" for="row in keyboard" :style="keyboardRowStyle(row)">
        <button
          class="kb-key"
          for="key in row.keys"
          :width="key.width ? key.width : null"
          on:touchstart="onKeyEvent(key, 'down')"
          on:touchend="onKeyEvent(key, 'up')"
          on:touchcancel="onKeyEvent(key, 'up')"
        >
          {{ key.code ? key.code : key }}
        </button>
      </div>
    </div>
  </div>
```

```js
const keyboardQwert = [
  { keys: ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", {code: "×", width: "13%"}] },
  { keys: ["Aa", "a", "s", "d", "f", "g", "h", "j", "k", "l", "Enter"] },
  {
    keys: ["z", "x", "c", "v", "b", "n", "m", ".", "↑"],
    margin: ["14%", "52px"],
  },
  { keys: [{code: "1#", width: "14%"}, {code: "Space", width: "55%"}, "←", "↓", "→"] },
];

const keyboardQwertUpper = [
  { keys: ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", {code: "×", width: "13%"}] },
  { keys: ["Aa", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"] },
  {
    keys: ["Z", "X", "C", "V", "B", "N", "M", ".", "↑"],
    margin: ["14%", "52px"],
  },
  { keys: [{code: "1#", width: "14%"}, {code: "Space", width: "55%"}, "←", "↓", "→"] },
];

const keyboard123 = [
  { keys: ["~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", {code: "×", width: "13%"}] },
  { keys: ["Aa", "@", "#", "$", "%", "&", "*", "-", "+", "=", "Enter"] },
  {
    keys: ["!", '"', "'", ";", ":", ",", ".", "/", "↑"],
    margin: ["14%", "52px"],
  },
  { keys: [{code: "abc", width: "14%"}, {code: "Space", width: "55%"}, "←", "↓", "→"] },
];

export default {
  data: {
    placeholder: "Enter your text here...",
    text: "Glyphix is a declarative GUI framework built for MCU devices.\n\nIt is lightweight, fast, and easy to use, offering rich UI components and development tools that help teams create modern, responsive graphical interfaces for embedded applications.",
    keyboard: keyboardQwert,
  },
  keyboardType: "qwerty",

  ta: null,
  onReady() {
    this.ta = this.$element("textarea");
  },

  onTextChanged() {
    console.log("You have edited the text");
  },
  toggleCase() {
    if (this.keyboardType == "qwerty") {
      this.keyboard = keyboardQwertUpper;
      this.keyboardType = "qwertyUpper";
    } else if (this.keyboardType == "qwertyUpper") {
      this.keyboard = keyboardQwert;
      this.keyboardType = "qwerty";
    }
  },
  keyboardRowStyle(row) {
    if (row.margin)
      return `margin-left: ${row.margin[0]}; margin-right: ${row.margin[1]};`;
    return "";
  },
  backspaceTimer: null,
  onKeyEvent(key, event) {
    if (event !== "down") {
      clearInterval(this.backspaceTimer);
      this.backspaceTimer = null;
      return; // skip if the key is released
    }

    if (key.code) key = key.code;
    switch (key) {
      case "Aa": this.toggleCase(); break;
      case "1#":
        this.keyboard = keyboard123;
        this.keyboardType = "123";
        break;
      case "abc":
        this.keyboard = keyboardQwert;
        this.keyboardType = "qwerty";
        break;
      case "×":
        this.ta.backspace();
        if (event == "down") {
          this.backspaceTimer = setTimeout(() => {
            this.backspaceTimer = setInterval(() => this.ta.backspace(), 50);
            this.ta.backspace();
          }, 500);
        }
        break;
      case "Enter": this.ta.insert("\n"); break;
      case "Space": this.ta.insert(" "); break;
      case "↑": this.ta.moveCaret("up"); break;
      case "↓": this.ta.moveCaret("down"); break;
      case "←": this.ta.moveCaret("left"); break; 
      case "→": this.ta.moveCaret("right"); break;
      default: this.ta.insert(key); break;
    }
  },
};
```

```css
.window {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 8px;
}

textarea {
  flex-grow: 1;
  padding: 6px;
  border: 2px solid #aaa6;
  border-radius: 12px;
  max-height: 160px;
}

.keyboard {
  display: flex;
  flex-direction: column;
}

.kb-row {
  display: flex;
  flex-direction: row;
}

.kb-key {
  flex-grow: 1;
  background-color: #f0f0f080;
  border: 2px solid #999;
  border-radius: 16px;
  text-align: center;
  padding: 6px auto;
  margin: 2px;
  font-size: 0.85rem;
  min-width: 40px;
}

.kb-key:active {
  background-color: #0003;
  border-color: #6663;
}
```

</glyphix>

We first obtain the `textarea` component object via the `$element` method in the component's `onReady()` lifecycle function, because we subsequently need to edit content and move the caret using the [`insert()`](#insert), [`backspace`](#backspace), and [`moveCaret`](#movecaret) methods.

Based on this, we can call the methods of `textarea` within the touch event listener of the `button` component, for example:

```html
<button on:touchstart="ta.insert('A')">A</button>
```

Since there is no physical keyboard, developers typically need to provide a custom keyboard implementation. This example implements a complete QWERTY keyboard layout, supporting case toggling and a symbol keyboard. Call the corresponding methods in each key's touch event listener function to edit the text. The arrow keys move the caret via the [`moveCaret()`](#movecaret) method (in four directions: up, down, left, and right), and the newline key inserts a newline character `\n` via [`insert()`](#insert).

### Differences from text-field

Both `textarea` and `text-field` are text input components. The main differences are as follows:

| Feature | `textarea` | `text-field` |
|---------|-----------|-------------|
| Text lines | Single or multi-line | Single line |
| Newline support | Supports `\n` newlines | Does not support newlines |
| Caret movement | Up and down | Left and right |
| Content property | `text` | `value` |
| Password mode | Not supported | Supports `password` property |
| Default display | Block-level element | Inline element |

============================================================
FILE_PATH: src/transl/EN/components/button.md

# button

The button component is an inline element by default and can trigger corresponding events when touched.

## Properties

### `checkable`  <decl type="boolean" set />

When set to `true`, it means a single touch only responds to one state change, i.e., transitioning from the pressed state to the released state, or from the released state to the pressed state. Additionally, the listening value for the `press` state is `true` when pressed and `false` when released.

### `toggleable` <decl type="boolean" set />

When set to `true`, it indicates that the `press` listening value can be changed, with `true` for pressed and `false` for released.

### `press` <decl type="boolean" get set listen />

When setting the `press` property, the state of the component can be changed. You can also listen to the component's state using the `on` directive. By default, upon completing a touch, the callback parameter is `true`. You can use it with the `checkable` and `toggleable` properties to get different listening values and states.

## Limitations

### `click` Event Invalidation

When not using the `button` component, you typically listen for click events on any native component via the [`click`](/framework/generic/properties.md#click) property. However, this method generally does not work for `button`. For example, consider the following code:
```html
<button on:click="onOuterClick">
  <p on:click="onInnerClick">inner</p>
  outer button
</button>
```

```js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    // Prevent event bubbling to avoid the outer button responding to the click event
    event.stopPropagation();
    console.log('inner click');
  }
}
```

<glyphix id="components-button-click-1" height="48" width="360" inline>

``` html
<button on:click="onOuterClick">
  <p on:click="onInnerClick">inner</p>
  outer button
</button>
```

``` css
button {
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}

button:active {
  opacity: 0.5;
}

p {
  border: 2px solid #444;
  padding: 0 10px;
}
```

``` js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    event.stopPropagation();
    console.log('inner click');
  }
}
```

</glyphix>

You might expect that clicking the `"inner"` text would trigger the `onInnerClick` method and prevent `onOuterClick`. However, you will find that this is not the case (it is best to open the browser console to view the logs): the `onInnerClick` method is not triggered at all, and only the outer `button` component responds to the click, meaning:
- When clicking the `inner` text, the `inner click` log does not appear, only the `outer click` log;
- The interaction for when the `button` is pressed is triggered (opacity is reduced).

This is just like clicking the outer `outer text`. The reason for this behavior is that the `button` component takes priority in responding to the entire lifecycle of the press gesture (from pressing down to releasing), while the `click` event is triggered upon release. This means that regardless of whether the inner element's `click` event handler stops propagation or not, this behavior cannot be changed.

#### Solution

To resolve this issue, you should listen to the `press` event of the outer `button` and the `touchstart` event of the inner element:

```html
<button on:press="onOuterClick">
  <p on:touchstart="onInnerClick">inner</p>
  outer button
</button>
```

```js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    // Prevent event bubbling to avoid the outer button responding to the click event
    event.stopPropagation();
    console.log('inner click');
  }
}
```

<glyphix id="components-button-click-2" height="48" width="360" inline>

``` html
<button on:press="onOuterClick">
  <p on:touchstart="onInnerClick">inner</p>
  outer button
</button>
```

``` css
button {
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}

button:active {
  opacity: 0.5;
}

p {
  border: 2px solid #444;
  padding: 0 10px;
}
```

``` js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    event.stopPropagation();
    console.log('inner click');
  }
}
```

</glyphix>

Try the example above, and you will find that clicking the `inner` text only triggers the `onInnerClick` method, `onOuterClick` will not be triggered, and the `button` will not render the pressed state effect.

::: tip
The `press` event is also typically triggered upon release, but it requires that the button's press event has never been prevented. Therefore, stopping the propagation of the inner element's `touchstart` event can prevent the outer button's `press` event from being triggered.
:::

#### Alternative Trigger Timing

The limitation of this method is that the inner element's `touchstart` event is triggered upon pressing down. You can alternatively use the `touchend` event to trigger the action, but you must retain the propagation-stopping functionality of the `touchstart` event. This ensures that the outer button's `press` event is not triggered when pressing down.

```html
<button on:press="onOuterClick">
  <p on:touchstart="$event.stopPropagation()" on:touchend="onInnerClick">inner</p>
  outer button
</button>
```

```js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    // No need to stop propagation here, as it was already stopped in touchstart
    console.log('inner click');
  }
}
```

<glyphix id="components-button-click-3" height="48" width="360" inline>

``` html
<button on:press="onOuterClick">
  <p on:touchstart="$event.stopPropagation()" on:touchend="onInnerClick">inner</p>
  outer button
</button>
```

``` css
button {
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}

button:active {
  opacity: 0.5;
}

p {
  border: 2px solid #444;
  padding: 0 10px;
}
```

``` js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    console.log('inner click');
  }
}
```

</glyphix>

Open the browser console and click the `inner` text again. You will find that the `onInnerClick` log is only printed upon release, and it still successfully prevents the outer `button` from responding to the gesture.

============================================================
FILE_PATH: src/transl/EN/components/progress-arc.md

# progress-arc

The `progress-arc` component is used to display a circular progress bar and defaults to a block-level element.

## Attributes

### `max` <decl type="number" set />

The maximum progress value. The [`value`](#value) attribute will not exceed it.

### `min` <decl type="number" get setet />

The minimum progress value. The [`value`](#value) attribute will not be less than it.

### `value` <decl type="number" get set listen />

Sets the progress value. The display proportion of the progress depends on the ratio of the `value` attribute within the interval from `min` to `max`, and the display proportion is restricted between $0\% \sim 100\%$. The `value` is an integer; if a floating-point value is set, only the integer part will be truncated.

### `busy` <decl type="boolean" get set />

Sets whether the `progress-arc` component is in a busy state. In the busy state, a loading animation is displayed instead of the value of the `value` attribute. The following example demonstrates how to use a circular progress bar to simulate a loading animation:

<glyphix id="components-progress-arc-busy" height="100" width="300" title="Simulating a Loading Animation">

``` html
<progress-arc busy :startAngle="0" :stopAngle="360" />
```

</glyphix>

In this example, the difference between the start angle and the stop angle of the progress bar is $360^\circ$. At this point, a typical loading animation effect can be displayed using the `busy` attribute.

::: tip
As long as the progress bar is circular, a fixed busy animation effect will be displayed; the start and stop angles have no effect on this.
:::

### `startAngle` <decl type="number" get set />

The start angle of the arc progress bar, with a default value of $135$. For more information, please refer to the [Angle Configuration](#angle-configuration) section.

### `stopAngle` <decl type="number" get set />

The stop angle of the arc progress bar, with a default value of $405$. For more information, please refer to the [Angle Configuration](#angle-configuration) section.

## Instructions

### Angle Configuration

Unlike the linear [`progress`](progress.md), arc or circular progress bars require proper configuration of the `startAngle` and `stopAngle` attributes to display correctly. Both attributes use angular units. In the screen coordinate system, $0^\circ$ points horizontally to the right (the 3 o'clock position on a clock) and increases in the clockwise direction, decreasing otherwise.

The display of `progress-arc` linearly interpolates the angle range based on the proportion of `value` within $[\texttt{min}, \texttt{max}]$. Specifically, users will see the highlighted angle of the progress start at `startAngle` and end at `valueAngle`:

$$
\begin{aligned}
  k &= \frac{\texttt{value} - \texttt{min}}{\texttt{max}-\texttt{min}}\\
  \texttt{valueAngle} &= (1-k)\texttt{startAngle} + k\cdot\texttt{stopAngle}
\end{aligned}
$$

Therefore, to display a full-circle progress bar, the difference between the start and stop angles must be $360^\circ$, even if these two angles appear visually identical. Additionally, the start angle can be greater than the stop angle, which will reverse the direction of the progress.

The following example shows the practical effects of various angle configurations. Note that the second example demonstrates the reverse progress display technique.

<glyphix id="components-progress-arc-angles" height="120" width="720" title="Angle Configuration Example">

``` html
<div>
  <p class="progress-label">{{value}}%</p>
  <stack>
    <p>default</p>
    <progress-arc :value="value" />
  </stack>
  <stack>
    <p>405~135</p>
    <progress-arc :startAngle="405" :stopAngle="135" :value="value" />
  </stack>
  <stack>
    <p>-45~225</p>
    <progress-arc :startAngle="-45" :stopAngle="225" :value="value" />
  </stack>
  <stack>
    <p>0~360</p>
    <progress-arc :startAngle="0" :stopAngle="360" :value="value" />
  </stack>
  <stack>
    <p>-90~270</p>
    <progress-arc :startAngle="-90" :stopAngle="270" :value="value" />
  </stack>
</div>
```

``` js
export default {
  data: { value: 0 },
  onInit() {
    setInterval(() => {
      this.value = this.value + 5
      if (this.value > 100)
        this.value = 0
    }, 500)
  }
}
```

``` css
div {
  display: flex;
}

progress-arc {
  width: 200px;
  padding: 0 8px 0 8px;
  stroke-width: 0.5rem;
}

p {
  text-align: center;
  font-size: 0.7rem;
}

.progress-label {
  width: 3.5rem;
}
```

</glyphix>

## CSS Specifications

### Dimension Calculation

The display size of `progress-arc` is determined by its `width` and `height` attributes. `progress-arc` will fill the shorter axis, and the center of the arc progress bar will be the center of the element. By default, the size of `progress-arc` may be close to a single character, resulting in a very bizarre display effect. Therefore, it is usually necessary to explicitly specify the width and height in CSS, or use other reasonable layout strategies.

::: tip
It is best to specify a reasonable width and height for the `progress-arc` component; otherwise, it may become unrecognizable. At the very least, the `width` CSS property should be set, and the component's layout strategy will automatically use a $1:1$ aspect ratio.
:::

### CSS Properties

You can adjust the appearance of the `progress-arc` component using CSS.

#### `stroke-width`

This property specifies the width of the arc outline of the `progress-arc` component. The value type is [Length](/framework/render/style-and-layout.md#长度), and percentage units are not supported.

::: tip
If you want the rendering width of the `progress-arc` component to be proportional to the font size, it is recommended to use the [`rem`](/framework/application/font-config.md#rem-字号单位) length unit, such as `0.15rem`.
:::

#### `color`

Sets the color of the highlighted progress bar for `progress-arc`. By default, the system theme color is used.

#### `background-color`

Sets the color of the background progress bar for `progress-arc`. By default, it is configured according to the system theme.

### CSS Pseudo-Elements

#### `value`



============================================================
FILE_PATH: src/transl/EN/components/input.md

# input

Defaults to an inline element, providing an interactive interface to receive user input.

## Attributes

### `type` <decl type="'checkbox' | 'radio'" set />

Can be set to the above value types. The final actual form of the `input` component is determined by the configured type.

### `name` <decl type="string" set />

Sets the name of the `input` component.

### `checked` <decl type="boolean" set />

The current checked state of the component, which can trigger the checked pseudo-class. This takes effect when the type is checkbox. Setting it to `on` makes the checkbox checked by default.

### `value` <decl type="string" set />

Sets the value of the `input` component.

============================================================
FILE_PATH: src/transl/EN/components/checkbox.md

# checkbox

The `checkbox` element displays a checked box when activated, indicating that an item has been selected.

<glyphix id="checkbox-1" :height="65" title="Single Checkbox">

``` html
<div>
  <checkbox id="checkbox" ::checked="checked" />
  <label target="checkbox">Check me!</label>
  <p>checked: {{ checked }}</p>
</div>
```

``` js
export default {
  data: {
    checked: true
  }
}
```
</glyphix>

::: note
A `checkbox` is typically a square that can be checked, but the exact appearance depends on the device. Developers currently cannot modify the color and other styles of a `checkbox` via CSS.
:::

## Properties

### `checked` <decl type="boolean" get set listen />

This property indicates whether the checkbox is selected. Setting the `checked` property toggles the selection state of the checkbox: when the value is `true`, it appears in the checked state. Two-way binding can also be used to operate on a single checkbox:
``` html
<checkbox model:checked="yes" />
```

The earlier example in this article demonstrates the usage of this binding. Please note not to bind to the [`value`](#value) property, but to `checked`.

Events are triggered only when the user clicks the checkbox, causing the `checked` property to change.

::: warning
Do not set the `checked` property in a [checkbox group](#group) to avoid confusion.
:::

### `value` <decl type="any" get set />

A JavaScript value that identifies the checkbox value, typically a string or a number. This value is not displayed, but it can be used in [group operations](#group).

### `group` <decl type="any[]" get set listen />

If there are multiple associated `checkbox` components, you can combine the `group` and `value` properties; checkboxes within the same group will form an array of selected values. Please refer to the example below:

<glyphix id="checkbox-group" :height="65" title="Checkbox Group" >

``` html
<div>
  <p>selected colors: {{selected.join(', ')}}</p>
  <div>
    <checkbox id="red" value="red" model:group="selected" />
    <label target="red">red</label>
    <checkbox id="blue" value="blue" model:group="selected" />
    <label target="blue">blue</label>
    <checkbox id="yellow" value="yellow" model:group="selected" />
    <label target="yellow">yellow</label>
  </div>
</div>
```

``` js
export default {
  data: {
    selected: ['yellow']
  }
}
```

``` css
label {
  margin-right: 0.5rem;
}
```

</glyphix>

This can be achieved by using `model:group` or `::group` to two-way bind the `group` property to a reactive array (`selected` in the example):
- After the user interacts with a checkbox in the group, the value of the reactive array is updated;
- Changes to the elements of the reactive array are reflected in the appearance of the `checkbox`.

As shown in the example above: in the initial state, the selection status of grouped checkboxes is determined by the value of the `group` property. Specifically, for a checkbox such as:
``` html
<checkbox value="red" model:group="selected" />
```
Since the `value` property specifies `"red"`, when the value of the reactive property `selected` contains `"red"` (e.g., `["red"]`), the checkbox will be checked. Clicking the checkbox again causes it to become unchecked, and the `"red"` element is removed from the `selected` array.

::: tip
If you do not want to group checkboxes, you can use the [`checked`](#checked) property to operate them individually. However, do not use `checked` and `group` at the same time; Glyphix does not account for this scenario.
:::

### `indeterminate` <decl type="boolean" get set />

The `indeterminate` property indicates that the checkbox is in an **indeterminate** state. When this property is `true`, the checkbox displays a horizontal line resembling a minus sign in the middle, indicating that its state is uncertain.

The indeterminate state can be used when an item has multiple sub-items: if all sub-items are checked, the parent is also checked; if all are unchecked, the parent is also unchecked. If some sub-items are checked, the parent will be in an indeterminate state.

The example below demonstrates this usage. This example shows an inventory for crafting an enchanting table; when you select some of the recipes, the "Enchantment table" checkbox enters a partially checked state. As you can see, this example allows you to use the parent checkbox to select or deselect all sub-items.

<glyphix id="checkbox-indeterminate" :height="140" title="Tri-state Checkbox" >

``` html
<div>
  <div>
    <!--
      When selected.length == 3, entirety is checked; otherwise:
      - If selected.length == 0, it is unchecked;
      - Otherwise, it means some recipes are selected, so it is in the indeterminate state. 
      -->
    <checkbox id="entirety"
              :indeterminate="selected.length && selected.length < 3"
              :checked="selected.length == 3"
              on:checked="selectEntirety" />
    <label target="entirety">
      &nbsp;Enchantment table:
    </label>
  </div>
  <div class="group">
    <div for="x in parts">
      •
      <checkbox :id="x" :value="x" model:group="selected" />
      <label :target="x">&nbsp;{{x}}</label>
    </div>
  </div>
</div>
```

``` js
export default {
  data: {
    selected: ['Diamonds'],
  },
  parts: ['Book', 'Diamonds', 'Obsidian'],
  // Called when clicking the entirety checkbox to set the selection state of all recipes
  selectEntirety(status) {
    // Use [...this.parts] to copy the list to avoid mutating in place
    this.selected = status ? [...this.parts] : []
  },
}
```

``` css
.group {
  margin-left: 0.4rem;
}
```

</glyphix>

::: tip
When the `checked` property is set (note: not cleared), the `indeterminate` property is automatically cleared. Even if the checkbox has both properties, it will display as checked rather than indeterminate.
:::

### CSS Behavior

Checkboxes are inline elements by default. Their display size is determined by the `font-size` CSS property and they align with the text baseline. Please do not manually specify properties like `width` and `height`, as this may cause rendering issues.

============================================================
FILE_PATH: src/transl/EN/components/qrcode.md

# qrcode

The `qrcode` component is used to display a [QR Code](https://en.wikipedia.org/wiki/QR_code). This component can display arbitrary text data, making it suitable for displaying URLs, payment codes, login QR code links, and other information.

In a flow layout, the `qrcode` component defaults to a block-level element (`block`), taking up a full line by itself.

## Properties

### `value` <decl type="string" get set />

Sets the text data to be displayed as a QR code. The `qrcode` component automatically selects the appropriate version based on the data length. Currently, it supports up to version $12$.

## CSS Notes

To make the QR code easy to scan, the CSS properties of the `qrcode` component should be set correctly, which include:
- `color`: The dot (module) color of the QR code, generally set to black (`black` or `#000`);
- `background-color`: The background color of the QR code, which should usually be white (`white` or `#fff`);
- `padding` / `margin`: Sufficient inner and outer margins prevent the QR code from blending with other elements, increasing the scanning recognition rate;
- `width` / `height`: The dimensions of the QR code must be large enough for easy capture.

By default, each module of the QR code component occupies a $4\rm{px}\times 4\rm{px}$ area, which may be barely scannable on a watch. However, layout strategies such as flex may shrink the QR code size; therefore, developers are advised to manually set the `width` / `height` properties of the QR code component as needed and test it on the device.

The following example demonstrates how to use the QR code component. Please note that various margins are set for the `qrcode` component in the CSS to ensure sufficient spacing between the QR code and other interface elements to avoid interfering with scanning.

<glyphix id="qrcode-1" :height="450" :width="350">

``` html
<div>
  <qrcode :value="text"/>
  <p>{{ text }}</p>
</div>
```

``` js
export default {
  data: {
    text: 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array'
  }
}
```

``` css
div {
  background-color: black;
  padding: 8px;
}

qrcode {
  margin: 16px;
  padding: 16px;
  color: black; /* Set the QR code foreground color to black */
  background-color: white; /* Set the QR code background color to white */
  border-radius: 16px;
}

p {
  color: white;
  font-size: 0.75rem;
}
```

</glyphix>

::: tip
You should always explicitly set a **high-contrast** dot color (`color`) and background (`background-color`) style for the QR code component to prevent reduced recognizability caused by deviations in the device's default style themes and inherited style properties.

At the same time, please set a sufficiently large padding (`padding`) to ensure easy scanning and recognition.
:::

============================================================
FILE_PATH: src/transl/EN/components/mapview.md

# mapview

A map component used for loading and displaying tile-based maps. `mapview` supports gesture panning, zoom level switching, current location display, and route navigation drawing, making it a core component for building map-based applications.

`mapview` is a block-level element by default.

::: tip
`mapview` is a runtime-extended component. Before using it, ensure that the target platform has integrated the `mapview` module.
:::

## Attributes

### `baseUri` <decl type="string" get set />

The **base path** URI for tile map resources. Tile files will be stored in this directory according to a fixed hierarchical structure. `mapview` automatically calculates the required tile file path based on the current zoom level and coordinates, with the following format:

```
{baseUri}/{zoomLevel}/{tileX}/{tileY}/normal.png     (Standard map)
{baseUri}/{zoomLevel}/{tileX}/{tileY}/satellite.png  (Satellite map)
```

A typical usage is to cache map tiles to the device's local storage and then point `baseUri` to the corresponding directory:

```html
<mapview baseUri="internal://files/tiles/map_provider" />
```

### `tileType` <decl type="number" get set />

The layer type of the tile map. Possible values are:

| Value | Description |
| :-: | :-- |
| `0` | Standard map (default value), loads `normal.png` tile files |
| `1` | Satellite map, loads `satellite.png` tile files |

### `loadPlace` <decl type="string" get set />

The URI of the **placeholder image** displayed while tile maps are loading. When the corresponding tile file has not yet been cached locally, `mapview` will display this image at the tile's position until the tile download is complete and the [`reload()`](#reload) method is triggered to refresh.

```html
<mapview loadPlace="/assets/imgs/loading.png" />
```

### `zoomLevel` <decl type="number" get set />

The map zoom level, with a value range of $[3, 23]$ and a default value of $17$. The higher the level, the more detailed the map; the lower the level, the larger the visible area.

::: info
This property corresponds to the Zoom Level in map tile standards, consistent with the level definitions of mainstream tile services such as Bing Maps and Google Maps.
:::

### `arrowIcon` <decl type="string" get set />

The image URI for the current location icon. This icon is drawn at the screen position corresponding to the latitude and longitude specified by [`navCoordinate`](#navcoordinate) or [`setLocation()`](#setlocation), with the center point aligning with the coordinate point.

```html
<mapview arrowIcon="/assets/imgs/location.png" />
```

### `navCoordinate` <decl type="{ x: number, y: number }" get set />

The latitude and longitude coordinates of the current location in the format `{ x: latitude, y: longitude }`, where `x` is the latitude and `y` is the longitude. Setting this property only updates the icon position and does not automatically center the map on these coordinates. If you need to center the map on the current location at the same time, use the [`setLocation()`](#setlocation) method and pass `force: true`.

::: tip
For scenarios requiring real-time location tracking, it is recommended to use the [`setLocation()`](#setlocation) method instead of directly assigning a value to this property, so that the `force` parameter can control whether to automatically recenter.
:::

### `arrowLineWidth` <decl type="number" get set />

The line width of the navigation route, in pixels, with a default value of `12`.

### `arrowLineBackgroundColor` <decl type="color" get set />

The **background color** of the navigation route (the color of the traversed part). Accepts CSS color values, with a default value of `#898b90`.

### `arrowLineForgeColor` <decl type="color" get set />

The **foreground color** of the navigation route (the color of the remaining route part). Accepts CSS color values, with a default value of `#4b73ec`.

### `smallMem` <decl type="boolean" get set />

Whether to enable low-memory device mode. The default value is `false`.

When enabled, `mapview` combines and scales four 256×256 tiles into a single 512×512 image for rendering, reducing the number of tiles cached simultaneously in memory to suit devices with limited memory.

::: warning
Low-memory mode sacrifices some map clarity and should only be enabled when device memory is noticeably insufficient.
:::

### `missTiles` <decl type="Array<{ z: number, x: number, y: number }>" get listen />

A read-only property that triggers a listener when the map discovers locally missing tile files. The callback parameter is an array, where each element describes a missing tile:

| Field | Type | Description |
| :-- | :-- | :-- |
| `z` | `number` | Zoom Level |
| `x` | `number` | Tile X coordinate (column number) |
| `y` | `number` | Tile Y coordinate (row number) |

Upon receiving this event, the application typically needs to download the corresponding tile files from the server and call [`reload()`](#reload) to refresh the map once the download is complete:

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

A read-only property for map events that triggers a listener when the following operations occur on the map:

| `event` Value | Trigger Timing | Additional Fields |
| :-- | :-- | :-- |
| `"move"` | Triggered when the user pans the map via gestures | None |
| `"calc"` | Triggered during navigation when recalculating position and off-route distance | `stepIndex` (current route segment index), `distance` (deviation distance from the current position to the route, in meters) |

```js
export default {
  onDirectionInfo(info) {
    if (info.event === 'move') {
      // The user manually dragged the map, automatic recentering can be paused
    } else if (info.event === 'calc') {
      console.log(`Current step: ${info.stepIndex}, off-route distance: ${info.distance} meters`)
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

Moves the center of the map to the current location (the coordinates specified by [`navCoordinate`](#navcoordinate)), used for the "return to current location" feature.

```js
this.$element('mapview').locate()
```

### `setLocation(location)`

Sets the current location coordinates and optionally moves the map center to that location.

| Parameter Field | Type | Description |
| :-- | :-- | :-- |
| `latitude` | `number` | Latitude |
| `longitude` | `number` | Longitude |
| `force` | `boolean` | When `true`, immediately centers the map on these coordinates (equivalent to calling [`locate()`](#locate)); when `false`, only updates the icon position |

```js
// Update icon position only, do not move the map
this.$element('mapview').setLocation({
  latitude: 39.9042,
  longitude: 116.4074,
  force: false,
})

// Update icon position and move the map center to these coordinates
this.$element('mapview').setLocation({
  latitude: 39.9042,
  longitude: 116.4074,
  force: true,
})
```

### `startNav(linePoints)`

Sets the navigation route and starts navigation. After calling this, the map will automatically locate to the route starting point and draw the complete route.

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
Note the parameter order: the first value of each coordinate point is **longitude**, and the second value is **latitude**, which is opposite to the common convention of "latitude first".
:::

### `insetNavPoint(linePoints)`

Appends route points to the existing navigation route, in the same format as [`startNav()`](#startnav). Suitable for scenarios where route data is received in segments. After appending, you must call [`reload()`](#reload) to refresh the display.

```js
this.$element('mapview').insetNavPoint(newPoints)
this.$element('mapview').reload()
```

## Usage Examples

### Basic Map Display

The following example demonstrates how to configure a basic map component, listen for missing tile events, and trigger downloads.

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

### Drawing Navigation Routes

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
    // Determine whether to enable low-memory mode based on the device memory tier
    this.isLowEndDevice = SysDevice.memoryProfile <= 4096
  },
}
```

============================================================
FILE_PATH: src/transl/EN/components/collapsible-header.md

# collapsible-header

The `collapsible-header` component is used to add a collapsible header bar to a scrolling list. This effect provides an interactive way to save view area for watch-type devices and improves the user experience.

::: warning
<experimental /> This is an experimental component. Do not use methods other than those demonstrated in this documentation.
:::

## Attributes

This component supports [Generic Attributes](/framework/generic/properties.md) and has no dedicated attributes.

## Usage

The `collapsible-header` component must contain two child components, otherwise unexpected behavior may occur. A specific example is shown below:

```html
<collapsible-header>
  <p>This is a collapsible header</p>
  <scroll> ... </scroll>
</collapsible-header>
```

The first child element is a collapsible header, and the second element must be a scrollable container such as [`scroll`](/components/scroll.md). Below is a concrete example:

<glyphix id="components-collapsible-header-1" height="360" width="360" title="Collapsible Header Bar">

```html
<collapsible-header>
  <p class="title-bar" on:click="clickTitle">TITLE BAR</p>
  <scroll scroll-snap="center" deformation="fisheye">
    <p for="x in 20" class="item">item {{ x + 1 }}</p>
  </scroll>
</collapsible-header>
```

```js
import prompt from "@system.prompt";

export default {
  clickTitle() {
    prompt.showToast({ message: "title clicked" });
  }
}
```

```css
.title-bar {
  margin: 56px auto auto;
  transparent: true;
  font-size: 1.5rem;
}

.item {
  height: 33.3%;
  background-color: #ddd;
  border-radius: 20%;
  margin: 8px;
  transparent: true;
  padding: 12px;
  text-align: center;
}
```

</glyphix>

### Principle Explanation

`collapsible-header` accepts two child components: the first one is the collapsible header bar, and the second one must be a scrollable component similar to `scroll`. `collapsible-header` combines these two components and manipulates the display effect of the collapsible header bar when the list scrolls.

You can use a flow-layout-like approach to control the position of the header bar, for example:

```css
/* The element has a top margin of 48px and is horizontally centered, suitable for circular screens. */
margin: 48px auto auto;
/* The element has a left and top margin of 12px, suitable for square screens. */
margin: 12px auto auto 12px;
```

By applying the above styles to the header bar element according to actual requirements, specific alignment effects can be achieved. You can also use complex components containing child elements as the header bar, such as using a component that includes a back button and page title text. However, note that when clicking the header bar, the click event can be sent to both the scrolling list and the header bar simultaneously. If there is a conflict, it can be resolved by stopping event propagation.

### Precautions

You must provide two child components for `collapsible-header` according to the above requirements, and do not mix up their order. In addition, since the collapsible header bar and the underlying scrolling list are displayed stacked, this may cause the first element of the list to overlap with the header bar. When necessary, developers should consider some placeholder method to avoid overlapping, and the centering [snap mode](/components/scroll.md#scrollsnap) (`scroll-snap="center"`) of `scroll` can also prevent overlapping.

============================================================
FILE_PATH: src/transl/EN/components/label.md

# label

The `label` component is used to display text or tag information, and defaults to an inline element. `label` can be used in conjunction with the following form components to display tag information:
- [input](input)
- [radio](radio)
- [switch](switch)
- [checkbox](checkbox)

When a `label` is associated with a supported form component, clicking the `label` component will also trigger a value update for the form component.

## Properties

### `text` <decl type="string" set get />

The text content of the label, supporting either attribute syntax or text child element syntax:
``` html
<label text="label text"></label>
<label>label text</label>
```

### `target` <decl type="string" set get />

The ID of the target component. For example:
```html
<radio id="red" /><label target="red">red</label>
```
Clicking the `label` component in this example will also trigger an update of the `radio` component with the ID `red`, but clicking the `label` component will not trigger touch events such as `click` on the target component.

Due to performance considerations, only target components that are siblings to the `label` component (i.e., share the same parent component) are supported.

::: warning
Changing the target component is currently not supported.
:::

============================================================
FILE_PATH: src/transl/EN/components/radio.md

# radio

Radio buttons are inline elements by default and are commonly used in a **radio group**, which contains a set of radio buttons describing a series of related options. Only one radio button in the group can be selected at any given time. Radio buttons are usually rendered as small circles that are filled to highlight when selected.

<glyphix id="radio-1" :height="65" title="Radio Button">

``` html
<div>
  <p>picked color: {{color}}</p>
  <div>
    <radio id="red" value="red" model:group="color" />
    <label target="red">red</label>
    <radio id="blue" value="blue" model:group="color" />
    <label target="blue">blue</label>
    <radio id="yellow" value="yellow" model:group="color" />
    <label target="yellow">yellow</label>
  </div>
</div>
```

``` js
export default {
  data: {
    color: 'blue'
  }
}
```

``` css
label {
  margin-right: 0.5rem;
}
```

</glyphix>

::: tip
Radio buttons are somewhat similar to [`checkbox`](checkbox.md), but a `radio` only allows selecting a single value from a group, whereas a `checkbox` allows selecting multiple values.
:::

## Attributes

### `checked` <decl type="boolean" get set listen />

This attribute indicates whether the radio button is checked. Setting the `checked` attribute can toggle the checked state of the radio button: a value of `true` displays it as checked.

When the user clicks the radio button and causes its checked state to change, the `checked` event is triggered.

::: tip
Manipulating the `checked` attribute directly is not the recommended way to use `radio`. Please use the [radio group](#group) approach instead.
:::

### `value` <decl type="any" get set />

A JavaScript value that identifies the value of the radio button, typically a string or a number. This value is not displayed, but it can be used within a [radio group](#group).

### `group` <decl type="any" get set listen />

If there are multiple related `radio` components, you can combine the `group` and `value` attributes. Radio buttons within the same group are mutually exclusive: the reactive property value bound to `group` is equal to the `value` attribute of the selected radio button. For example:
``` html
<radio value="red" model:group="color" />
<radio value="blue" model:group="color" />
<radio value="yellow" model:group="color" />
```
Here, `color` is a reactive property. When the second radio button is selected, the value of `color` is `"blue"`. If none of the radio buttons' `value` matches `color`, then no radio button will be selected. For example:
``` html
<p on:click="color = null">reset select</p>
```
This will clear the selected state:

<glyphix id="radio-reset" :height="65" title="Clear Selection State">

``` html
<div>
  <p on:click="color = null">picked color: {{color}} (click to reset)</p>
  <div>
    <radio id="red" value="red" model:group="color" />
    <label target="red">red</label>
    <radio id="blue" value="blue" model:group="color" />
    <label target="blue">blue</label>
    <radio id="yellow" value="yellow" model:group="color" />
    <label target="yellow">yellow</label>
  </div>
</div>
```

``` js
export default {
  data: {
    color: 'blue'
  }
}
```

``` css
label {
  margin-right: 0.5rem;
}
```

</glyphix>

### CSS Behavior

Radio buttons are inline elements by default. Their display size is determined by the `font-size` CSS property, and they align with the text's baseline. Please do not manually specify properties such as `width` and `height`, as this may cause layout distortion.

============================================================
FILE_PATH: src/transl/EN/components/stack.md

# stack

`stack` is a stacked layout component. In a stacked layout, each child component has the same size and position as the `stack` component, and they are stacked and displayed sequentially in the order they are added. The following example shows two text elements overlapping inside a `stack` component.

<glyphix id="components-stack-layout" height="100" width="200" title="Stacked Layout">

``` html
<stack>
  <p class="text1">Text 1</p>
  <p class="text2">Text 2</p>
</stack>
```

``` css
* {
  text-align: center;
}

.text1 {
  font-size: 64px;
  color: #fff;
}

.text2 {
  font-size: 48px;
  color: #f008;
}

stack {
  background-color: gray;
}
```

</glyphix>

::: tip
The `stack` component always uses the stacked layout strategy and cannot be changed to other layouts (such as flex layout or flow layout) via CSS properties like `display`.
:::

## Layout Behavior

The `stack` component has a fixed stacked layout strategy. Its size is determined by two types of constraints:
1. The size of the `stack` is first specified by size-related CSS properties such as [`width`](../framework/generic/styles.md#width) or [`height`](../framework/generic/styles.md#width);
2. The layout of the parent element may directly determine the layout of the `stack`, such as properties like `align-items: stretch` or `flex: 1` in a flex layout;
3. Otherwise, the size of the `stack` component is determined by the maximum width and maximum height of its child elements.

Once the size of the `stack` is determined, all of its child elements will have the same outer frame size (i.e., the size of the child element plus `border` and `margin`). This can sometimes cause confusion; for example, using a `stack` to set an image as a background might result in the image failing to fill the area if the upper-layer element is too large.

============================================================
FILE_PATH: src/transl/EN/components/list-item.md

# list-item

A sub-component of `list`, used to display a specific list item. It supports sub-components and layouts, but does not support scrolling.

::: tip
Glyphix does not provide a `list` container component like QuickApp does; instead, it uses [`scroll`](scroll.md) to implement scrolling containers. Similarly, there is no need to use the `list-item` component—please directly use [`div`](div.md) or any other component as the list item element.
:::

============================================================
FILE_PATH: src/transl/EN/components/scroll.md

# scroll

A scrollable list container that supports arbitrary child components. The scrolling direction of the list is determined by the specific layout mode: when using flow layout or a flex layout with a `column` direction, elements are laid out vertically, allowing the list to scroll vertically; whereas when using a flex layout with a `row` direction, elements are laid out horizontally, allowing the list to scroll horizontally. The `scroll` component does not support bidirectional scrolling (i.e., scrolling both horizontally and vertically at the same time).

By default, the `scroll` component is a block-level element that uses flow layout.

The `scroll` component can be scrolled using touch gestures, and vertical `scroll` components also support encoder (watch rotating crown, or mouse wheel on the simulator) scrolling.

::: tip
Some interactive examples in this document support mouse wheel interaction (indicated by a mouse icon on the right side of the title): you can hover your pointer over the example and use your mouse wheel to scroll the list.
:::

## Properties

### `scroll` <decl type="{ scrollX: number, scrollY: number, scrollState: number }" get listen />

The value of the `scroll` property is an object containing the following fields: `scrollX`, `scrollY`, and `scrollState`. The `scrollX` and `scrollY` properties represent the horizontal and vertical scrolling positions in pixels, respectively; the `scrollState` property represents the scrolling state, with a value of $0$, $1$, or $2$, as detailed in the table below. You can listen to changes in the `scroll` property using the `on` directive. Any change in content position caused by user actions or API operations will trigger the listener.

| `scrollState` Value | Description of Effect |
| :--------------: | ------------------------------------------------------------------- |
|       $0$        | Scrolling has stopped.                                                        |
|       $1$        | Scrolling via user gestures.                                              |
|       $2$        | The user has released their hand; scrolling is caused by methods such as [`scrollTo`](#scrollto) or inertia. |

::: info
The area where the child elements of `scroll` are located is called the "content" area, while the portion of the list component actually displayed is called the "view" area. Elements are laid out within the content area, and their dimensions may exceed the view area. Scrolling changes the display position of the content.
:::

The range of the scrolling position is typically within the content area—that is, `scrollX` for a horizontal list is within the range $[0, \texttt{contentWidth}]$, and `scrollY` for a vertical list is within the range $[0, \texttt{contentHeight}]$. However, when the list is scrolled past the beginning of the content, `scrollX` or `scrollY` will be less than $0$; similarly, when scrolled past the end of the content, the value of `scrollX` or `scrollY` will be greater than `contentWidth` or `contentHeight`.

::: warning
The `scroll` event is triggered on every frame during scrolling. Listening to this event in JavaScript code may cause noticeable frame drops, so it should be avoided as much as possible.
:::

### `scrollTop` <decl type="number" set get listen />

The vertical scroll position, which is the distance from the top of the content of the `scroll` component to the top of the viewport, in pixels. You can set the scroll position or listen to changes in the scroll position through this property.

Unlike the [`scroll`](#scroll) property, listening to the `scrollTop` property itself cannot distinguish whether the scroll was caused by a user gesture, an API call, or inertia.

### `scrollLeft` <decl type="number" set get listen />

The horizontal scroll position, which is the distance from the left of the content of the `scroll` component to the left of the viewport, in pixels. You can set the scroll position or listen to changes in the scroll position through this property.

Unlike the [`scroll`](#scroll) property, listening to the `scrollLeft` property itself cannot distinguish whether the scroll was caused by a user gesture, an API call, or inertia.

### `scrollWidth` <decl type="number" get listen />

The width of the content area of the `scroll` component. The width of a vertically laid out `scroll` equals the viewport width, while the width of a horizontally laid out `scroll` is the sum of the widths of all elements. You can listen to changes in content width using this.

### `scrollHeight` <decl type="number" get listen />

The height of the content area of the `scroll` component. The height of a vertically laid out `scroll` equals the viewport height, while the height of a horizontally laid out `scroll` is the sum of the heights of all elements. You can listen to changes in content height using this.

### `damping` <decl type="number" set />

Sets the damping coefficient for the list scrolling animation. The valid value range is $[0.1, 50]$ (unsupported values are automatically clamped to the upper or lower limits), with a default value of $1.5$. A larger damping coefficient causes the animation to stop faster, while the default damping coefficient produces a longer-distance, longer-duration inertial effect.

<glyphix id="components-scroll-damping" height="360" width="360" title="Damping Effect" wheel>

``` html
<div>
  <span>damping: {{damping}}</span>
  <button on:click="increase">+</button>
  <button on:click="decrease">-</button>
  <scroll :damping="damping">
    <p for="x in 50" class="item">
      Item {{ x + 1 }}
    </p>
  </scroll>
</div>
```

``` js
export default {
  data: {
    damping: 1
  },
  increase() {
    this.damping += 1
    if (this.damping > 20)
      this.damping = 1
  },
  decrease() {
    this.damping -= 1
    if (this.damping < 1)
      this.damping = 19.5
  }
}
```

``` css
span {
  color: #404040;
}

scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  height: 300px;
  width: 360px;
}

.item {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px 5px;
  margin: 10px;
  border-radius: 16px;
}

button {
  color: #fafafa;
  background-color: #adadad;
  border-radius: 12px;
  margin-left: 16px;
  margin-bottom: 16px;
  width: 1.2rem;
}
```

</glyphix>

::: tip
The damping coefficient should be set as a constant rather than modified dynamically. Modifying the damping coefficient will not affect the bounce-back animation.
:::

### `snapshot` <decl type="boolean" get set />

When the `snapshot` property is enabled, child components in the list will enter snapshot mode. For a related demonstration, refer to the [`quiescent`](/framework/generic/properties.md#quiescent) property of native components.

Enabling snapshots may improve the frame rate of complex interfaces. For example, when list items contain a large amount of text and a non-transparent background, snapshot mode can cache and combine numerous drawing operations into a small number of snapshots. The Glyphix framework caches these snapshots across repeated draws to further enhance performance.

However, the `snapshot` property does not guarantee that child components will use snapshots; this property may be ignored when system memory is low or when using snapshots is unnecessary.

### `deformation` <decl type="string | function" set />

Sets the deformation effect of the list, which can be used to achieve appearances such as a fisheye lens. You can specify a built-in deformation effect by name (string) or define one using a JavaScript function.

|     Value     |             Description             |
| :---------: | :------------------------------: |
|  `'none'`   |       No deformation effect (default)       |
| `'fisheye'` |          Built-in fisheye effect          |
|  function   | Specifies a deformation effect via a JavaScript function |

Deformation effects should be constants and should not be modified.

When the list is set to the fisheye deformation effect, it is recommended to set the [`scrollSnap`](#scrollsnap) property to `'center'` to achieve the most reasonable effect.

The figure below demonstrates the fisheye deformation effect. You can use the "center" switch to adjust whether to center-align.

<glyphix id="components-scroll-deformation" height="360" width="360" title="Fisheye Effect" wheel>

``` html
<div>
  <p>center <switch ::value="center" /></p>
  <scroll deformation="fisheye" :scroll-snap="center ? 'center' : null">
    <p for="x in 15">
      Item {{ x + 1 }}
    </p>
  </scroll>
</div>
```

``` css
div {
  color: #404040;
  display: flex;
  flex-direction: column;
}

scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  flex: 1;
}

scroll > p {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 40px 10px;
  margin: 5px;
  border-radius: 50%;
}
```

``` js
export default {
  data: {
    center: true
  }
}
```

</glyphix>

::: tip
Deformation effects generally make use of snapshots, so there is no need to separately enable the `snapshot` property when `deformation` is set.
:::

### `scrollSnap` <decl type="'none' | 'start' | 'center' | 'edge'" get set />

Sets the alignment and snapping behavior of list items. For example, you can center-align elements or snap them to element boundaries.

|     Value     | Description                                                                                                           |
| :--------: | -------------------------------------------------------------------------------------------------------------- |
|  `'none'`  | Elements have no alignment or snapping effect; child elements can stop at any position according to scrolling inertia. |
| `'start'`  | When scrolling stops, the start position of the element aligns with the start position of the viewport. This mode is currently not supported. |
| `'center'` | When scrolling stops, the center position of the element aligns with the center of the viewport. |
|  `'edge'`  | When scrolling stops, the start or end position of the element snaps to the nearest start or end position of the viewport. However, if scrolling does not cross an element boundary, no snapping is triggered. |

The `scrollSnap` property does not adjust element dimensions, but you can use layout mechanisms and other methods to create lists of equal-sized items.

::: warning
This property should be set during component initialization and must not be changed afterwards; otherwise, interaction errors may occur.
:::

### `index` <decl type="number" get set listen />

The index of the currently displayed child component. When the `index` property is set, the component will animate and scroll to the specified child component. You can listen to position changes using the `on` directive, and changes to the child component index can be observed via the `index` property.

The value of `index` is automatically clamped to ensure it points to a valid element. When using `index`, you must ensure that all elements of the `scroll` component are static (i.e., the CSS [`position`](/framework/generic/styles.md#position) property is set to the default `static`), otherwise errors will occur.

### `finalChanged` <decl type="bool" get set />

Sets whether to trigger the [`index`](#index) change event only when scrolling stops. By default (i.e., when `finalChanged` is `false`), the listening event is triggered whenever scrolling gestures or other reasons cause the `index` property of the `scroll` component to change. However, doing so can easily lead to animation frame drops or overly frequent, unnecessary event triggers. When `finalChanged` is set, the `index` change event is triggered only when scrolling completely stops.

::: tip
When implementing dot indicators or similar effects by listening to the `index` property, it is recommended to set `finalChanged` to `true`. This avoids frame drops during the sliding process caused by event-triggered render updates.
:::

The following example demonstrates the effect of `finalChanged`. You can try toggling the "final-changed" checkbox, then swipe the list to observe the frequency and timing of `index` changes.

<glyphix id="components-scroll-final-changed" height="360" width="360" title="Delayed Index Event" wheel>

``` html
<div>
  <p>
    <checkbox id="checkbox" ::checked="finalChanged" />
    <label target="checkbox">final-changed</label>
    index: {{index}}
  </p>
  <scroll :final-changed="finalChanged" ::index="index">
    <p for="x in 50">
      Item {{ x + 1 }}
    </p>
  </scroll>
</div>
```

``` css
div {
  color: #404040;
  display: flex;
  flex-direction: column;
}

scroll {
  display: flex;
  flex-direction: column;
  flex: 1;
}

scroll > p {
  background-color: #f0f0f0;
  border-radius: 12px;
  text-align: center;
  margin: 8px;
  padding: 20px;
}
```

``` js
export default {
  data: {
    index: 0,
    finalChanged: true
  }
}
```

</glyphix>

### `bounces` <decl type="'none' | 'start' | 'end' | 'edge'" get set />

Sets whether a bounce-back effect is triggered when `scroll` is scrolled past its boundaries via gestures. The initial value of this property is `edge`, which allows bounce-back at both the start and end positions.

|    Value     | Description                                   |
| :-------: | -------------------------------------- |
| `'none'`  | Disables all boundary bounce-back effects.                     |
| `'start'` | Allows bounce-back only when dragged past the start position of the content.     |
|  `'end'`  | Allows bounce-back only when dragged past the end position of the content.     |
| `'edge'`  | Allows bounce-back when dragged past either the start or end position of the content. |

The example below demonstrates the effect of each `bounces` value. You can try dragging each item left and right beyond the boundaries and observe the corresponding interaction behavior.

<glyphix id="components-scroll-bounces" height="360" width="400" title="Drag Bounce Animation">

``` html
<scroll class="column-box">
  <scroll for="item in items" class="row-box"
          :bounces="item" scroll-snap="edge">
    <p class="item-body">bounces: {{item}}</p>
    <p class="slide-button">×</p>
  </scroll>
</scroll>
```

```js
export default {
  data: {
    items: ['none', 'start', 'end', 'edge']
  }
}
```

```css
.column-box {
  display: flex;
  flex-direction: column;
}

.row-box {
  display: flex;
  flex-direction: row;
}

.row-box > p {
  border-radius: 12px;
  text-align: center;
  margin: 8px;
  padding: 16px;
}

.item-body {
  background-color: #f0f0f0;
  width: 100%;
}

.slide-button {
  width: 30%;
  color: #ffffff;
  background-color: #f04040;
}
```

</glyphix>


::: note
Currently, the `bounces` property only affects the bounce behavior of gesture operations, while ignoring fast inertial animation bounces. The example above uses a technique to avoid unintended behavior:
- `.row-box` uses the edge snap strategy (`snap-type="edge"`) to avoid gesture animations with bouncing.
- Each element of `.row-box` does not exceed `100%` width, ensuring that the edge snap strategy does not trigger internal boundary bouncing.

This technique can be used for interfaces such as swipe-to-delete menus.
:::

The `bounces` property also plays a role similar to [`weakGesture`](#weakgesture). Specifically, once you scroll past a boundary where bouncing is disabled, rolling gesture events are automatically allowed to bubble up. Therefore, there is no need to set both the `bounces` and `weakGesture` properties simultaneously.

::: tip
The scrolling gesture bubbling behavior of `bounces` and `weakGesture` are "inverse". For example, the `end` mode bounce strategy allows the user to bounce back after scrolling past the end of the list, and this strategy permits scroll gestures to bubble up at the start position. This corresponds to the effect of the `weakGesture` property with a value of `'start'`.
:::

### `weakGesture` <decl type="'none' | 'start' | 'end' | 'edge'" get set />

Sets under which circumstances the `scroll` component should bubble up scrolling gestures. By default, `scroll` prevents the gestures it responds to from bubbling, so its parent elements cannot receive gestures that cause `scroll` to scroll. `weakGesture` allows bubbling of gesture events when dragged to the content boundary positions, enabling parent elements to receive those gestures.

|    Value     | Description                                             |
| :-------: | ------------------------------------------------ |
| `'none'`  | Does not bubble up responded gesture events.                     |
| `'start'` | Bubbles up responded gesture events after being dragged to the start position of the content.       |
|  `'end'`  | Bubbles up responded gesture events after being dragged to the end position of the content.       |
| `'edge'`  | Bubbles up responded gesture events after being dragged to either the start or end position of the content. |

If the underlying element of the page is a horizontal `scroll` component, but you want a right-swipe gesture to allow navigating back in the page, you can configure it like this:
``` html
<scroll weak-gesture="start"> ... </scroll>
```
When the user scrolls to the head of the `scroll` component and continues to swipe right, they can exit the page.

::: warning
This property should be set during component initialization and must not be changed afterwards; otherwise, interaction errors may occur.
:::

### `scrollbar` <decl type="boolean" get set />

Indicates whether the `scroll` component should display a scrollbar (hidden by default). This is only supported for vertically laid out `scroll` components. The `scrollbar` property must be a constant and cannot be modified using reactive properties. For example:
``` html
<scroll scrollbar>
  ...
</scroll>
```
This will create a `scroll` component with a scrollbar. For the appearance of the scrollbar, please refer to the example of the [`setIndex`](#setindex) method.

The style of the scrollbar is determined by the system—for example, it may appear as an arc on circular screens and as a straight bar on rectangular screens.

### `scrolled` <decl type="boolean" listen />

Use the `scrolled` property to listen to whether the list is in a scrolling state. An event-triggered property value of `true` indicates that the list is currently scrolling, while `false` means the list has stopped scrolling.

Both scrolling operations generated by user touch and programmatic scrolling via the `scroll` property will trigger the `scrolled` event. When the list stops moving from a scrolling state, the parameter value of the `scrolled` event is `false`.

### `setIndex`
<decl method><pre>
(options: {
  index: number,
  behavior?: 'instant' | 'smooth'
}): void
</pre></decl>

Moves the viewport to the child component specified by the index. If this movement would cross the viewport boundary, the viewport position will stay at the first or last component. The properties of the `options` parameter are:
- `index`: The index of the target child component to move to, where $0$ represents the first child component.
- `behavior`: When set to `'smooth'`, an animated transition is used; when set to `'instant'` (default), it moves immediately to the specified child component position.

When calling `setIndex()`, you must ensure that all elements of the `scroll` component are static, otherwise errors will occur.

<glyphix id="components-scroll-setindex" height="360" width="400" title="setIndex Method">

``` html
<div class="window">
  <scroll id="scroll"
          :scroll-snap="center ? 'center' : null"
          scrollbar>
    <p for="x in 50" class="item">Item {{ x }}</p>
  </scroll>
  <div class="controls">
    <button on:click="setIndex('smooth')">smooth</button>
    <button on:click="setIndex('instant')">instant</button>
    center <switch ::value="center" />
  </div>
</div>
```

``` js
import prompt from '@system.prompt'

export default {
  data: { center: false },
  setIndex(behavior) {
    let el = this.$element('scroll')
    let index = parseInt(Math.random() * 50)
    prompt.showToast({message: `${behavior}ly set index to ${index}`})
    el.setIndex({ index: index, behavior: behavior })
  }
}
```

``` css
.window {
  display: flex;
  flex-direction: column;
}

scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  flex: 1;
}

.item {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px 5px;
  border-radius: 16px;
  margin: 8px;
}

.controls {
  display: flex;
  align-items: center;
  color: #404040;
}

button {
  color: #fafafa;
  background-color: #adadad;
  border-radius: 12px;
  padding: 4px 10px;
  margin-left: 16px;
  margin-bottom: 16px;
  flex: 1;
  margin: 8px;
  padding: 8px;
  text-align: center;
}
```

</glyphix>

### `scrollTo`
<decl method><pre>
(options: {
  left?: number,
  top?: number,
  behavior?: 'instant' | 'smooth'
}): void
</pre></decl>

Scrolls the content to the specified position. The properties of the `options` parameter are:
- `left`: Specifies the scroll position of the content along the y-axis. Omitting `left` or having the scroll component use a vertical layout will result in no scrolling along the y-axis.
- `top`: Specifies the scroll position of the content along the x-axis. Omitting `top` or having the scroll component use a horizontal layout will result in no scrolling along the x-axis.
- `behavior`: Specifies the transition effect for scrolling. `'instant'` (default) means jumping directly to the target position without a transition effect, while `'smooth'` performs smooth scrolling with a transition effect.

The `scrollTo` method ignores element snapping effects.

### `scrollBy`
<decl method><pre>
(options: {
  left?: number,
  top?: number,
  behavior?: 'instant' | 'smooth'
}): void
</pre></decl>

Scrolls the content by a specified distance. Unlike [`scrollTo()`](#scrollTo), `scrollBy()` scrolls relative to the current content position. The properties of the `options` parameter are:
- `left`: Specifies the distance to scroll the content along the y-axis. Omitting `left` or having the scroll component use a vertical layout will result in no scrolling along the y-axis.
- `top`: Specifies the distance to scroll the content along the x-axis. Omitting `top` or having the scroll component use a horizontal layout will result in no scrolling along the x-axis.
- `behavior`: Specifies the transition effect for scrolling. `'instant'` (default) means jumping directly to the target position without a transition effect, while `'smooth'` performs smooth scrolling with a transition effect.

The `scrollBy` method ignores element snapping effects.

## CSS Specifications

### Layout Direction Control

The scrolling direction of the `scroll` component is determined by its layout mode. When using flow layout (default layout) or a flex layout with a `column` direction, elements are laid out vertically, allowing the list to scroll vertically; whereas when using a flex layout with a `row` direction, elements are laid out horizontally, allowing the list to scroll horizontally.

<glyphix id="components-scroll-layout" height="360" width="740" title="Layout Mode Controlling Scroll Direction">

``` html
<div>
  <scroll>
    <p for="20">vertical scroll</p>
  </scroll>
  <!-- Used as a spacer element because flex layout does not support gap yet -->
  <div style="width: 20px"></div>
  <scroll style="display: flex; flex-direction: row;">
    <p for="20">horizontal<br>scroll</p>
  </scroll>
</div>
```

``` css
div {
  display: flex;
}

scroll {
  background-color: #f0f0f0;
  flex: 1;
}

p {
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px;
  margin: 4px;
  border-radius: 16px;
}
```

</glyphix>

### `padding` and `overflow` <version-badge since="0.9" />

By default (`overflow: clip`), the padding of the `scroll` component directly clips the visible area. Once content is scrolled, the padding area is always invisible. Setting `overflow: visible` allows the padding area to remain visible even when the content is scrolled.

<glyphix id="components-scroll-padding-overflow-visible" height="360" width="740" title="Padding with overflow: visible">

``` html
<div>
  <scroll :index="2">
    <p for="20">overflow: clip</p>
  </scroll>
  <!-- Used as a spacer element because flex layout does not support gap yet -->
  <div style="width: 20px"></div>
  <scroll style="overflow: visible;" :index="2">
    <p for="20">overflow: visible</p>
  </scroll>
</div>
```

``` css
div {
  display: flex;
}

scroll {
  padding: 20px;
  background-color: #f0f0f0;
  flex: 1;
}

p {
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px;
  margin: 4px;
  border-radius: 16px;
}
```

</glyphix>

Even with `overflow: visible` set, `scroll` clips its content to the padding-box rather than allowing it to extend beyond that range, which differs from regular elements like `div`. This is because the scrolling behavior and layout mechanism of `scroll` require content to scroll within a defined region, rather than allowing content to expand indefinitely into external areas.

For ordinary containers like `div` under similar `overflow: visible` conditions, content can overflow the entire `div` range (such as outside the red `border`):

<glyphix id="components-scroll-overflow-div" height="360" width="360" title="div's overflow: visible">

``` html
<div style="overflow: visible;">
  <p for="20">div {overflow: visible}</p>
</div>
```

``` css
div {
  display: flex;
  flex-direction: column;
  padding: 20px;
  margin-bottom: 100px;
  border: 2px solid red;
  background-color: #f0f0f0;
}

p {
  background-color: #bdbdbd;
  text-align: center;
  padding: 8px;
  margin: 4px;
  border-radius: 16px;
  flex-shrink: 0;
}
```

</glyphix>

#### Recommended Settings for i18n Scenarios

In i18n (internationalization) scenarios, text inside `scroll` may need to overflow to avoid potential truncation. For such cases, the recommended setting is `overflow: visible`, which allows [text overflow](/framework/application/i18n.md#text-overflow) content to extend beyond the content boundaries of `scroll` during scrolling, making maximum use of space to display text.

#### Relationship with HTML/CSS Specifications

The behavior of `scroll` when `overflow: visible` is set is similar to `div { overflow-y: scroll; }` in the HTML/CSS specifications. In this case, padding keeps content visible during scrolling—for example, CSS like this:

```css
div {
  padding: 20px;
  overflow-y: scroll;
}
```

Will produce the following effect, where the padding area does not clip the content during scrolling:

<div style="padding: 20px; background-color: var(--vp-c-grey-bg); overflow-y: scroll; height: 100px; width: 200px; border: 2px dotted red; font-family: sans-serif;">
  Michaelmas term lately over, and the Lord Chancellor sitting in Lincoln's Inn Hall.
  Implacable November weather. As much mud in the streets as if the waters had but
  newly retired from the face of the earth.
</div>

HTML's `div` does not have a behavior that directly corresponds to `scroll` when `overflow: clip` is set.

============================================================
FILE_PATH: src/transl/EN/components/text-field.md

# text-field

A component used for entering single-line text content, which defaults to an inline element. Unlike GUI elements on mobile phones or PCs, `text-field` currently does not respond to input devices such as keyboards, nor does it pop up an input method interface, so you must edit its content manually. `text-field` supports operating the cursor via touch gestures (such as tapping and scrolling).

`text-field` is suitable as a low-level component for single-line text input, allowing you to implement a soft keyboard according to your needs (such as a password numeric keypad or even voice input). For details, please refer to the [Example](#基本示例).

## Attributes

### `value` <decl type="string" set get listen />

The `value` property is a string representing the content currently being edited in `text-field`. Reading or listening to this value allows you to retrieve the input text, and this property can also be set.

Typically, `value` is two-way bound to a specific reactive property, such as:

```html
<text-field ::value="inputText" />
```

### `placeholder` <decl type="string" set get />

When the content of `text-field` is empty, `placeholder` can be used to provide a brief prompt to the user, such as phrases like "Please enter text".

`placeholder` automatically displays when the input text is empty, so it usually only requires a fixed content, such as:

```html
<text-field ::value="inputText" placeholder="type here" />
```

### `password` <decl type="boolean" set get />

When this property is set, `text-area` will use "password mode", meaning each character is replaced with "•" ([Bullet, U+2022](http://www.fileformat.info/info/unicode/char/2022/index.htm)). You can turn the `password` property off or on at any time to switch between showing and hiding the password status.

In newer versions <version-badge since="0.9" />, password mode delays masking the input characters, allowing users to see the just-entered characters for a short time before they are replaced with "•". Older versions mask input characters immediately.

### `insert` <decl type="(text: string): void" method />

Inserts a piece of text with the content `text` at the cursor position, and the cursor automatically moves past the inserted text. Calling this function triggers a `value` listening event.

### `backspace` <decl type="(): void" method />

Deletes the character at the cursor position, and the cursor automatically moves forward. Calling this function triggers a `value` listening event.

## Usage Instructions

### Basic Example

The following example demonstrates the basic usage of `text-field`. You can click the keyboard buttons to input numbers. Click the "×" button to delete the content at the cursor position, and click "A/*" to toggle between password mode and regular text input mode. In password mode, the input content is hidden with `•`.

<glyphix id="components-text-field-1" width="410" height="160">

```html
<div class="flex-column">
  <div class="flex-row align-baseline">
    <text-field id="text-field"
                ::value="inputText"
                :password="password"
                placeholder="type here" />
    <button checkable ::press="password">A/*</button>
    <button on:click="textField.backspace()">×</button>
  </div>
  <!-- A simple matrix numeric keypad -->
  <div class="flex-row" for="rows in keyboard">
    <button class="flex-1" for="key in rows"
            on:click="textField.insert(key)">
      {{key}}
    </button>
  </div>
</div>
```

```js
export default {
  data: {
    inputText: "",
    password: false,
  },
  keyboard: [
    ['1', '2', '3', '4', '5'],
    ['6', '7', '8', '9', '0'],
  ],
  textField: null,
  onReady() {
    // Get the TextField component object for easy invocation of insert() and backspace() methods.
    this.textField = this.$element("text-field")
  },
}
```

```css
.flex-column {
  display: flex;
  flex-direction: column;
}

.flex-row {
  display: flex;
}

.align-baseline {
  align-items: baseline;
}

text-field {
  flex: 1;
  text-align: center;
  border-bottom: 2px solid #666;
}

button {
  border-radius: 8px;
  background-color: #dee2e6;
  margin: 8px;
  padding: auto 12px;
}

button:active {
  opacity: 0.5;
}

.flex-1 {
  flex: 1;
}
```
</glyphix>

In this example, the text in `text-field` is centered, which is achieved via `text-align`:
```css
text-field {
  text-align: center;
}
```

We first obtain the `text-field` component object using the `$element` method within the component's `onReady()` lifecycle function, because we need to use the [`insert()`](#insert) and [`backspace`](#backspace) methods to edit the content subsequently.

With this in place, we can directly call the methods of `text-field` within the `click` event listener of the `button` component, for example:
```html
<button on:click="textField.backspace()">×</button>
```

Since there is no physical keyboard, developers usually need to provide a custom keyboard implementation. For educational purposes, this example only implements a 2-row by 5-column numeric keypad, and inserts the key value into `text-field` within the `click` event listener function of each key:
```html
<div class="flex-row" for="rows in keyboard">
  <button class="flex-1" for="key in rows"
          on:click="textField.insert(key)">
    {{key}}
  </button>
</div>
```

This example also demonstrates the standard method for toggling password mode.

### Content Validation and Formatting

You can achieve validation and formatting of input content by two-way binding the [`value`](#value) property of `text-field` to a computed property. The following example demonstrates this approach, which allows you to input a maximum of 9 digits (no letters, etc.) and adds a "," separator every three digits.

<glyphix id="components-text-field-validator" title="Content Validator" width="410" height="200">

```html
<div class="flex-column">
  <div class="flex-row align-baseline">
    <text-field id="text-field"
                ::value="inputText"
                :password="password"
                placeholder="type here" />
    <button checkable ::press="password">A/*</button>
    <button on:click="textField.backspace()">×</button>
  </div>
  <div class="flex-row" for="rows in keyboard">
    <button class="flex-1" for="key in rows"
            on:click="textField.insert(key)">
      {{key}}
    </button>
  </div>
</div>
```

```js
export default {
  data: {
    password: false,
    rawText: "",
  },
  computed: {
    inputText: {
      get() { return this.rawText },
      set(text) {
        if (text.length < 12 && /^[\d,]*$/.test(text)) {
          this.rawText = text.replace(/[^\d]/g, '')
                             .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
        }
      },
    },
  },
  keyboard: [
    ["1", "2", "3", "4", "5"],
    ["6", "7", "8", "9", "0"],
    ["A", "B", "C", "D", "E"],
  ],
  textField: null,
  onReady() {
    this.textField = this.$element("text-field")
  },
}
```

```css
.flex-column {
  display: flex;
  flex-direction: column;
}

.flex-row {
  display: flex;
}

.align-baseline {
  align-items: baseline;
}

text-field {
  flex: 1;
  border-bottom: 2px solid #666;
}

button {
  border-radius: 8px;
  background-color: #dee2e6;
  margin: 8px;
  padding: auto 12px;
}

button:active {
  opacity: 0.5;
}

.flex-1 {
  flex: 1;
}
```
</glyphix>

Content validation and formatting are implemented via two-way binding and computed properties. For the `text-field` component node:
```html
<text-field id="text-field"
            ::value="inputText"
            :password="password"
            placeholder="type here" />
```
The `value` property is two-way bound to `inputText`, which is actually a computed property. Its `set()` method checks whether the input content complies with the rules (maximum 11 characters, allowing only numbers and commas), then filters the numbers using regular expressions and formats them by adding commas every three digits:
```js
function set(text) {
  if (text.length < 12 && /^[\d,]*$/.test(text)) {
    this.rawText = text.replace(/[^\d]/g, '')
                       .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }
}
```
If the input content does not meet the requirements, the `set()` method ignores the input value, and the two-way binding mechanism keeps the content of `text-field` consistent with the property value of `inputText` (obtained via the `get()` method). Therefore, you will find that letter keys cannot be entered.

============================================================
FILE_PATH: src/transl/EN/components/progress.md

# progress

The `progress` component is used to display a progress bar and is a block-level element by default.

## Attributes

### `max` <decl type="number" set />

The maximum progress value. The [`value`](#value) attribute will not exceed it.

### `min` <decl type="number" set />

The minimum progress value. The [`value`](#value) attribute will not be less than it.

### `value` <decl type="number" set get listen />

Sets the progress value. The display ratio of the progress depends on the proportion of the `value` attribute within the range from `min` to `max`, and the display ratio is restricted between $0\% \sim 100\%$. The `value` is an integer; if a floating-point value is set, only the integer part will be truncated.

### `vertical` <decl type="boolean" set />

If the value of the `vertical` attribute is `true`, the `progress` component will be displayed vertically, otherwise horizontally. The default value is `false`.

## CSS Specifications

Developers can customize the appearance of the `progress` component using CSS.

### Dimension Calculation

By default, the width and height of `progress` are the same as the font size of the element, which is set by the [`font-size`](/framework/generic/styles.md#font-size) property (or inherited). The dimensions of `progress` can be customized via the [`width`](/framework/generic/styles.md#width) and [`height`](/framework/generic/styles.md#height) properties.

### CSS Properties

The following CSS properties may be very useful:
- [`background-color`](/framework/generic/styles.md#background-color) can control the background color of `progress`;
- [`color`](/framework/generic/styles.md#color) can control the progress bar color of `progress`;
- [`border-radius`](/framework/generic/styles.md#border-radius) can set `progress` to have rounded borders, for example, `50%` will produce semi-circular borders;

Other CSS properties may also be useful, such as using the [`border`](/framework/generic/styles.md#border) property to set border styles.

### CSS Pseudo-elements

#### `value`

This pseudo-element can be used to style the `progress` bar independently of the background portion. For example, you can set the border radius of the scrollbar background and the progress bar portion separately to achieve an effect where the outer border has rounded line caps while the progress bar has straight line caps.

``` css
progress {
  border-radius: 50%; /* Scrollbar background border radius */
}

progress::value {
  border-radius: 0; /* Progress bar has no border radius */
}
```

### CSS Example

The following example demonstrates some ways to customize the appearance of the progress bar using CSS.

<glyphix id="components-progress-styles" height="140" width="480" title="Progress Bar Style">

``` html
<div>
  <!-- Default style -->
  <progress :value="40" />
  <!-- Flat-cap progress bar style -->
  <progress class="flat" :value="50" />
  <progress class="more-style" :value="60" />
</div>
```

``` css
div > * {
  margin: 8px;
}

.flat::value {
  /* Set the border-radius of the value pseudo-element to 0 for a flat-cap progress bar effect */
  border-radius: 0;
}

.more-style {
  /* Custom border radius */
  border-radius: 30%;
  /* Progress bar background color */
  background-color: #b3c5d7;
  /* Progress bar foreground color */
  color: #b5179e;
  /* padding can adjust the margin of the progress bar foreground */
  padding: 6px;
  height: 1.25rem;
}
```

</glyphix>

============================================================
FILE_PATH: src/transl/EN/components/a.md

# a

The anchor component, which is an inline element by default, used to jump to a specified page.

## Attributes

### `href` <decl type="string" get set />

Specifies the [page name](/framework/application/manifest.md#pages) or URI string to jump to.

``` html
<a href="page1">Jump to page1</a>
``` 

Unlike the `<a>` tag in Web, the `a` component only supports page navigation and does not support hyperlink navigation.

The `href` attribute also supports [URI](/framework/application/resource.md#uri) strings in the form of `PageName?key=value`, which consists of a page name (as the path field) and a query field. The query field of this URI will be parsed as navigation parameters for the page. For example, when clicking this `<a>` element:

``` html
<a href="page1?text=test-text&message=hello">Jump to page1</a>
```

It is equivalent to calling the following [`router.push()`](/api/system-router.md#push) method:

``` js
router.push({
  uri: 'page1',
  params: {text: 'test-text', message: 'hello'}
})
```

::: tip
Please note that the value of the query field in the URI will only be parsed as a string type. Therefore, `100` in `page1?size=100` will be parsed as the string `'100'` rather than the number `100`. If you need to pass parameters of a specific type, please use the [`router`](/api/system-router.md) API.
:::

============================================================
FILE_PATH: src/transl/EN/components/README.md

# Native Components

============================================================
FILE_PATH: src/transl/EN/components/swiper.md

# swiper

Card view container, supporting arbitrary sub-components. The scrolling direction of the card view is specified by the specific layout mode: lists using the `flex-column` layout are vertical, while lists using the `flex-row` layout are horizontal.

## Properties

### `scroll` <decl type="{ scrollX: number, scrollY: number, scrollState: number }" get listen />

The `scroll` property value is an object containing the following fields: `scrollX`, `scrollY`, and `scrollState`. The `scrollX` and `scrollY` properties represent the horizontal and vertical scrolling positions in pixels, respectively. The `scrollState` property represents the scrolling state, with a value of $0$, $1$, or $2$, as detailed in the table below. Changes to the `scroll` property can be listened to using the `on` directive. Any content position changes caused by user operations and API operations will trigger the listener.

| `scrollState` Value | Description |
| :--------------: | ------------------------------------------------------------------- |
|       $0$        | Stopped scrolling |
|       $1$        | Scrolling via user gestures |
|       $2$        | The user has released their hand; scrolling is caused by method calls such as [`scrollTo`](#scrollto) or inertia |

### `scrollTop` <decl type="number" get listen />

The vertical scrolling position, which is the distance from the top of the `swiper` component's content to the top of the viewport, in pixels. This property can be used to listen to changes in the scroll position. Unlike the [`scroll`](#scroll) property, listening to the `scrollTop` property itself cannot distinguish whether it is a user gesture scroll, an API call, or an inertia-generated scroll.

### `scrollLeft` <decl type="number" get listen />

The horizontal scrolling position, which is the distance from the left of the `swiper` component's content to the left of the viewport, in pixels. This property can be used to listen to changes in the scroll position. Unlike the [`scroll`](#scroll) property, listening to the `scrollLeft` property itself cannot distinguish whether it is a user gesture scroll, an API call, or an inertia-generated scroll.

### `scrollWidth` <decl type="number" get listen />

The width of the `swiper` component's content area. The width of a vertically laid out `swiper` equals the viewport width, while the width of a horizontally laid out `swiper` is the sum of the widths of all elements. Changes to the content width can be listened to via this.

### `scrollHeight` <decl type="number" get listen />

The height of the `swiper` component's content area. The height of a vertically laid out `swiper` equals the viewport height, while the height of a horizontally laid out `swiper` is the sum of the heights of all elements. Changes to the content height can be listened to via this.

### `snapshot` <decl type="boolean" get set />

When the `snapshot` property is enabled, the sub-components of `swiper` will enter snapshot mode. Please refer to the [`snapshot`](scroll.md#snapshot) property of the `scroll` component.

### `deformation` <decl type="string" set />

Sets the deformation effect of child elements. Through deformation effects, appearances like fisheye can be achieved. A built-in deformation effect can be specified by name (string), or defined via a JavaScript function.

| Value | Description |
| :-: | :- |
| `'none'` | No deformation effect (default). |
| `'fade'` | Fade and scale transition effect. This effect highlights the "focus" of elements within the current viewport while making elements outside the viewport recede into the background. For details, please refer to the effect in the example in this section. |
| `'fisheye'` | Built-in fisheye effect. This property component is used for the [`scroll`](scroll.md) component rather than `swiper`. |
| function | Specifies the deformation effect via a JavaScript function. |

Deformation effects should be constants and should not be modified.

If the content of `swiper`'s child elements changes frequently, it is recommended to add the [`quiescent`](/framework/generic/properties.md#quiescent) property to the elements when using deformation effects to avoid updating during transitions and to improve performance. You can refer to the example below:

<glyphix id="components-swiper-deformation" height="360" width="360" title="Element Deformation Effect">

```html
<swiper deformation="fade" indicator>
  <div for="x in 5" :quiescent="x != 0">
    <progress-arc busy :start-angle="0" :stop-angle="360" />
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

progress-arc {
  width: 30%;
  height: 30%;
  margin-bottom: 5%;
}
```

</glyphix>

The first child element in the example does not have the `quiescent` property enabled, so it will continue to update during the transition process, while other elements will stop updating.

### `vertical` <decl type="boolean" set />

Sets whether the `swiper` component uses a vertical layout. When set to the default `false`, a horizontal layout is used. The following example demonstrates the interaction effect of a `swiper` under a vertical layout (note that it must be scrolled vertically; horizontal sliding will not respond).

<glyphix id="components-swiper-vertical" height="360" width="360" title="Vertical Layout">

``` html
<swiper vertical deformation="fade" indicator>
  <p for="x in 5">
    pane {{ x + 1 }}
    {{ x == 0 ? '(swipe up)' : x == 4 ? '(swipe down)' : '' }}
  </p>
</swiper>
```

``` css
p {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
}
```

</glyphix>

### `indicator` <decl type="boolean" get set />

Sets whether the `swiper` component displays dot indicators. The display position of the dot indicators is determined by the `vertical` property: for a vertical layout, the dot indicators are displayed in the middle of the right side; for a horizontal layout, they are displayed in the middle of the bottom. For specific effects, please refer to the examples of the [`deformation`](#deformation) and [`vertical`](#vertical) properties.

Refer to [Dot Indicator CSS Properties](#dot-indicator-css-properties) to learn how to customize the display style of dot indicators.

### `pageLength`  <decl type="number" set />

Sets the size or proportion of child pages. When expressed as a percentage, it sets the size of the sub-components along the sliding direction (relative to the component itself); when expressed as other numbers, it sets the size of the sub-components along the sliding direction.

### `index`  <decl type="number" get set listen />

The index of the currently displayed sub-component. When the `index` property is set, the component will scroll to the specified sub-component via animation. Position changes can be listened to using the `on` directive, and sub-component index changes can be listened to via the `index` property.

### `finalChanged` <decl type="bool" get set />

Sets whether to trigger the [`index`](#index) change event only when scrolling stops. By default (i.e., when `finalChanged` is `false`), listening events are triggered whenever scrolling gestures or other reasons cause the `index` property of the `swiper` component to change. However, doing so can easily lead to dropped animation frames, or overly frequent and unnecessary event triggering. When `finalChanged` is set, the `index` change event is triggered only when scrolling stops.

::: tip
When implementing dot indicators and other effects by listening to the `index` property, it is recommended to set `finalChanged` to `true`, which can prevent dropped frames caused by rendering updates triggered by events during the sliding process.
:::

### `weakGesture` <decl type="'none' | 'start' | 'end' | 'edge'" get set />

Sets under which circumstances the `swiper` component will bubble up scrolling gestures. By default, `swiper` prevents bubbling for the gestures it responds to, so its parent elements cannot receive gestures that cause `swiper` to scroll. `weakGesture` allows enabling gesture event bubbling when dragged to the content boundary positions, enabling parent elements to receive these gestures.

|    Value    | Description                                             |
| :-------: | ------------------------------------------------ |
| `'none'`  | Do not bubble responded gesture events.                     |
| `'start'` | Bubble responded gesture events after dragging to the start position of the content.       |
|  `'end'`  | Bubble responded gesture events after dragging to the end position of the content.       |
| `'edge'`  | Bubble responded gesture events after dragging to the start or end position of the content. |

If the underlying element of the page is a horizontal `swiper` component, but you want right-swipe gestures to return to the previous page, you can configure it like this:
``` html
<swiper weak-gesture="start"> ... </swiper>
```
When the user swipes to the beginning of the `swiper` component and continues to swipe right, they can exit the page.

### `bounces` <decl type="'none' | 'start' | 'end' | 'edge'" get set />

Sets whether to trigger a bounce effect after scrolling `swiper` to the boundaries via gestures. The initial value of this property is `edge`, which allows bouncing at the start and end positions. The `bounces` property of `swiper` is similar to the [`bounces`](scroll.md#bounces) property of the [`scroll`](scroll.md) component; please refer to the related documentation for more details.

### `scrolled` <decl type="boolean" listen />

Listens to whether the `swiper` component is in a scrolling state via the `scrolled` property. A property value of `true` triggered by the event indicates that it is currently scrolling, otherwise it means it has stopped scrolling.

Both scrolling operations generated by user touches and scrolling via the `scroll` property will trigger the `scrolled` event. When stopping from the scrolling state, the parameter value of the `scrolled` event is `false`.

### `setIndex`
<decl method><pre>
(options: {
  index: number,
  behavior?: 'instant' | 'smooth'
}): void
</pre></decl>

Moves the viewport to the sub-component specified by the index. If this move crosses the viewport boundary, the viewport position will stay at the first or last component. The roles of the `options` parameter properties are:
- `index`: The index of the target sub-component to move to, where $0$ represents the first sub-component.
- `behavior`: Uses an animation transition when set to `'smooth'`, or moves immediately to the specified sub-component position when set to `'instant'` (default).

### `scrollTo` <decl type="(position: number): void" method />

Scrolls the content to the specified position. The scrolling direction is consistent with the layout direction of the scroll component.

The `scrollTo` method ignores the snap effect of elements.

## CSS Specifications

### Dot Indicator CSS Properties

This section introduces the CSS properties available when the `swiper` component has the [`indicator`](#indicator) property enabled, which are used to control some display styles of the dot indicators. The dot indicators of `swiper` are always displayed as a group of horizontally or vertically aligned dots, and developers can only customize based on this foundation.

#### `indicator-color`

Defines the color of unselected dot indicators. The effect is shown below:

<glyphix id="components-swiper-indicator-color" height="360" width="360" title="Dot Indicator Color">

```html
<swiper indicator>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-color: #333;
  indicator-selected-color: #ff60ff;
  indicator-bottom: 16px;
}
```

</glyphix>

#### `indicator-selected-color`

Defines the color of selected dot indicators. For the effect, refer to the example of the [`indicator-color`](#indicator-color) property, where you can observe that the dot indicator corresponding to the selected page is displayed in the color defined by this CSS property.

#### `indicator-size`

Defines the size of each indicator dot in the dot indicators, in pixels. The default value is `10px`. The following example demonstrates the effect of setting the dot indicator size to `16px`:

<glyphix id="components-swiper-indicator-size" height="360" width="360" title="Dot Indicator Size">

```html
<swiper indicator>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-color: #333;
  indicator-selected-color: #ff60ff;
  indicator-bottom: 24px;
  indicator-size: 16px;
}
```

</glyphix>

#### `indicator-top`

When `swiper` has a [horizontal layout](#vertical), the `indicator-top` property can be used to specify the distance of the dot indicators from the top. By default, the dot indicators are displayed at the bottom middle position; this property can display them at the top:

<glyphix id="components-swiper-indicator-top" height="360" width="360" title="Top Dot Indicator">

```html
<swiper indicator>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-top: 16px;
}
```

</glyphix>

::: warning
Do not set `indicator-left`, `indicator-top`, `indicator-right`, and `indicator-bottom` at the same time, otherwise it will lead to unexpected dot indicator positions.
:::

#### `indicator-left`

When `swiper` has a [vertical layout](#vertical), the `indicator-left` property can be used to specify the distance of the dot indicators from the left. By default, the dot indicators are displayed in the middle of the right side; this property can display them on the left:

<glyphix id="components-swiper-indicator-left" height="360" width="360" title="Left Dot Indicator">

```html
<swiper indicator vertical>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-left: 16px;
}
```

</glyphix>

#### `indicator-right`

When `swiper` has a [vertical layout](#vertical), the `indicator-right` property can be used to specify the distance of the dot indicators from the right. The effect is shown below:

<glyphix id="components-swiper-indicator-right" height="360" width="360" title="Right Dot Indicator">

```html
<swiper indicator vertical>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-right: 32px;
}
```

</glyphix>

#### `indicator-bottom`

When `swiper` has a [horizontal layout](#vertical), the `indicator-bottom` property can be used to specify the distance of the dot indicators from the bottom. For the effect, refer to the examples of the [`indicator-color`](#indicator-color) and [`indicator-size`](#indicator-size) properties.

### `padding` and `overflow` <version-badge since="0.9" />

See the relevant instructions in the [scroll component](scroll.md#padding-and-overflow). The `padding` and `overflow` properties of the `swiper` component share the same behavioral specifications as properties of the same name in the `scroll` component. Please refer to the related documentation for more details.

============================================================
FILE_PATH: src/transl/EN/components/pullable.md

# pullable

The `pullable` component is used within a scrolling list to add incremental loading or refresh interaction triggered by pulling down at the top or pulling up at the bottom. The `pullable` component is a block-level element by default.

::: warning
<experimental /> This is an experimental component. The functionality of `pullable` is not yet stable, and its animations may not feel entirely natural.
:::

`pullable` should be the first or last child component of [`scroll`](scroll.md). When it is the first child component, pulling down further at the top of the `scroll` content will trigger the `pulling` event; conversely, when `pullable` is the last child component of `scroll`, pulling up at the bottom will trigger the `pulling` event.

The `pullable` component is hidden by default and is only displayed when being pulled up or down. The example below demonstrates how to use the `pullable` component.

<glyphix id="components-pullable-1" height="360" width="360" title="Pull down/up to load more">

```html
<scroll scrollbar>
  <pullable :hold="pulldown" on:pulling="onPulldown">
    <progress-arc busy start-angle="0" stop-angle="360" />
    <p>{{pulldown || 'keep pull down...'}}</p>
  </pullable>
  <p for="item in items">item ({{item}})</p>
  <pullable :hold="pullup" on:pulling="onPullup">
    <progress-arc busy start-angle="0" stop-angle="360" />
    <p>{{pullup || 'keep pull up...'}}</p>
  </pullable>
</scroll>
```

```js
export default {
  data: {
    pulldown: null,
    pullup: null,
    items: []
  },
  first: 0,
  last: 0,
  onInit() {
    this.update(0, 10)
  },
  update(first, last) {
    for (let i = this.first; i > first; --i)
      this.items.unshift(i)
    for (let i = this.last; i < last; ++i)
      this.items.push(i)
    this.first = first
    this.last = last
  },
  onPulldown(event) {
    this.pulldown = event ? 'please release' : 'updating...'
    if (!event) {
      setTimeout(() => {
        this.update(this.first - 5, this.last)
        this.pulldown = null
      }, 1000)
    }
  },
  onPullup(event) {
    this.pullup = event ? 'please release' : 'updating...'
    if (!event) {
      setTimeout(() => {
        this.update(this.first, this.last + 5)
        this.pullup = null
      }, 1000)
    }
  }
}
```

```css
scroll {
  display: flex;
  flex-direction: column;
}

scroll > p {
  background-color: #ddd;
  border-radius: 32px;
  margin: 12px;
  padding: 32px;
  text-align: center;
}

pullable {
  display: flex;
  justify-content: center;
  margin: 32px;
}

pullable > progress-arc {
  stroke-width: 0.25rem;
  margin-right: 16px;
}
```

</glyphix>

For detailed usage, please refer to [Usage Instructions](#usage-instructions).

## Attributes

### `hold` <decl type="bool" get set />

By default, `pullable` is only visible when pulled down at the top or pulled up at the bottom. However, when the `hold` attribute is set to `true`, the `pullable` component will remain visible. This attribute is typically set when the [`pulling`](#pulling) event causes a content update, and cleared once the content update is complete.

### `pulling` <decl type="bool" get listen />

The `pulling` event is triggered when `pullable` is pulled out completely. The meanings of the event values are:
- `true`: Triggered when the pull-down/pull-up reaches the distance required to fully reveal the `pullable` component;
- `false`: Triggered when the user releases their hand after meeting the above pull-out condition.

The example below demonstrates the timing of when the `pulling` event values are triggered. You can try slowly pulling down from the top of the list and pay attention to the toast message when the `pulling` event is triggered.

<glyphix id="components-pullable-pulling" height="360" width="360" title="pulling event">

```html
<scroll scrollbar>
  <pullable :hold="refresh" on:pulling="onPulling">
    <p>pulling...</p>
  </pullable>
  <p for="item in 10">item {{item}}</p>
</scroll>
```

```js
import prompt from '@system.prompt'

export default {
  data: {
    refresh: false
  },
  onPulling(event) {
    prompt.showToast({
      message: `pulling: ${event ? 'trigged' : 'release'}`
    })
    if (!event) {
      this.refresh = true
      setTimeout(() => this.refresh = false, 1000)
    }
  }
}
```

```css
scroll {
  display: flex;
  flex-direction: column;
}

scroll > p {
  background-color: #ddd;
  border-radius: 32px;
  margin: 12px;
  padding: 32px;
  text-align: center;
}

pullable {
  text-align: center;
  margin: 32px;
}
```

</glyphix>

## Usage Instructions

### Component Position

The `pullable` component must be the first or last child element of a vertical `scroll` component. It automatically determines the operation mode based on its position: when it is the first child element, it detects the user pulling down from the top of the list, and vice versa.

For a list that only requires pull-down to refresh, the following usage is sufficient:
```html
<scroll>
  <pullable :hold="refresh" on:pulling="onPulling">
    <p>pulling...</p>
  </pullable>
  <div for="item in items">
    ...
  </div>
</scroll>
```

In the JavaScript code, you can listen to the `pulling` event and control the `refresh` attribute:
``` js
export default {
  data: {
    refresh: false
  },
  onPulling(hold) {
    if (!hold) { // hold is false when the user releases their hand
      this.refresh = true // Indicates that refreshing is in progress
      // This example uses a timer to simulate a loading operation and stops loading after 1s
      setTimeout(() => this.refresh = false, 1000)
    }
  }
}
```

For the specific effect, please refer to the example in the [`pulling`](#pulling) event documentation.

### Prompt Content Control

The `pullable` component can contain various components inside to display prompt contents. As shown in the earlier example in this document, you can combine a loading animation with prompt text. In addition, the value of the `pulling` event can be used to control the prompt content. The following state handling approach is generally recommended:
1. Set a reactive attribute (such as `refresh`) for each `pullable` component with a default value of `null`. The `refresh` attribute is also used to control the [`hold`](#hold) attribute of `pullable`.
2. When in the initial state (i.e., `refresh` is falsy), the prompt content of `pullable` should remind the user to "keep pulling down to update".
3. When the user pulls down, the `pulling` event is triggered. Proceed to step 4 or 5 based on its event value.
4. When `pulling` is `true`, it should prompt the user to "release to start refreshing".
5. When `pulling` is `false`, it indicates that the user has released their hand. At this point, `refresh` should be set to `true`, content refreshing should start, and the user should be prompted that "updating is in progress".
6. Once content refreshing is complete, reset `refresh` to `false` to return to the initial state.

You can also refer to the first example in this document, which implements continuous loading functionality by pulling down at the head and pulling up at the tail of the list. That example uses a trick to control all states of `pullable` using just a single reactive attribute.

This trick sets the initial value of the `refresh` reactive attribute to `null` (similar to `false`) and uses template code like this:
``` html
<pullable :hold="refresh" on:pulling="onPulling">
  <p>{{refresh || 'Keep pulling down'}}</p>
</pullable>
```
When `refresh` is not set, as soon as `pullable` is pulled out, the default "Keep pulling down" prompt content will be displayed. Then, the `onPulling` event callback function should be written as follows:
``` js
export default {
  async onPulling(event) {
    this.refresh = event ? 'Please release' : 'Updating'
    if (!event) { // Trigger refresh operation upon release
        await runRefreshJobs()
        this.refresh = null // Reset status after refresh completes
    }
  }
}
```

### Limitations

Currently, the `pullable` component has some limitations. In addition to having to be used within a vertical `scroll` component, you also need to ensure that the number of list elements exceeds the size of the `scroll` viewport, otherwise issues may occur. Furthermore, the interaction effects of `pullable` may feel somewhat rigid.

============================================================
FILE_PATH: src/transl/EN/components/slider-arc.md

# slider-arc

An arc slider selector. It is a block-level element by default, and style customization is currently not supported.

## Properties

Inherits properties from the [slider](slider) component.

### `arc-center` <decl type="{ x: number, y: number }" set />

Sets the position of the arc's center.

### `start-angle` <decl type="number" set />

Sets the starting angle of the arc. Default value: $-90$.

### `progress-angle` <decl type="number" set />

Sets the maximum rotation angle of the arc. Default value: $360$ (a full circle).

### `arc-width` <decl type="number" set />

Sets the width of the arc.

### `arc-radius` <decl type="number" set />

Sets the radius of the arc.

