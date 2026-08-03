---

icon: layers-outline

---

# CSS properties


This section introduces all CSS properties supported by the Glyphix framework. For an introduction to the style and layout mechanism, please refer to [This document](/framework/render/style-and-layout.md).


## layout control


### Basic properties


#### `display`


The `display` attribute sets the layout scheme of the element. Currently can be set to the following values:


- `inline`: Default value. This element generates one or more inline element boxes without newlines before or after them. In a normal flow, if there is space, the next element will be on the same line.
- `block`: This element generates a block-level element box. In normal flow, line breaks are generated before and after this element.
- `flex`: This element behaves like a block-level element and lays out its content according to `Flex`.
- `inline-flex` and `inline flex`: The element behaves like an inline element and its content is laid out according to `Flex`.
- `none`: Elements will not be displayed in this mode (not recommended).


#### `width`


The `width` attribute specifies the width of the element, including `padding` and `border` (border-box). If the element is in a layout container or otherwise restricted, the final element size may not be consistent with the value of the `width` attribute.


::: tip

Glyphix now only supports [border-box](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-sizing) mode, the value of `width` always contains `padding` and `border`.
:::



The value of the `width` attribute is a CSS [length](/framework/render/style-and-layout.md#长度). The specific values ​​are as follows:


- `auto`: Default value, this mode automatically calculates the width of the element based on content size and layout constraints. For example, a text element will determine its width based on the size of the text content, while a container element will determine its width based on the layout size of the inner element.
- `value [unit]`: Use some length unit to specify the element width. Layout or other constraints may adjust the actual size of the element.


Using the `width` attribute of an element in flex layout will be used as the initial width of the element, which will be further adjusted to the best actual width during the layout process.


#### `height`


The `height` attribute specifies the height of the element, including `padding` and `border` (border-box). This attribute behaves like [`width`](#width).


### Flex layout


#### `flex-direction`


Set the main axis direction (horizontal or vertical) of the flex layout container. The values ​​are as follows:


- `row`: Default value, the main axis is in the horizontal direction.
- `column`: The main axis is in the vertical direction.


The `flex-direcion` attribute is only valid when the element is laid out using flex, for example:


```css
display: flex;
flex-direction: column;
```


#### `flex-flow`


`flex-flow` is short for `flex-direction` and `flex-wrap`. The syntax is


```css
flex-flow: <flex-direcion> <flex-wrap>;
```


Currently the `flex-wrap` attribute is not implemented yet, so this part will not work.


#### `justify-content`


Specifies the alignment of child elements along the main axis of the container when using flex layout.


Property value:


- `flex-start`: Default value, the first element is close to the starting position of the main axis of the container, and subsequent elements are arranged in order. There is no additional padding between elements.
- `flex-end`: The last element is located close to the tail of the main axis of the container, and the previous elements are arranged in order. There is no additional padding between elements.
- `center`: All elements are arranged in the middle of the main axis of the container, and the remaining space at both ends of the main axis will be vacated. There is no additional padding between elements.
- `space-between`: Arrange each element evenly, with the first element placed at the starting point, the last element placed at the end point, and the remaining space is evenly filled between elements.
- `space-around`: Arrange each element evenly, allocate the same space around each element, and leave remaining space before and after the first and last elements.


#### `align-items` <badge type="info" text="内联" />


Specifies the alignment of child elements along the cross axis of the container when using flex layout. The following values ​​are supported:


- `stretch`: Default value, the element stretches to fill all the space of the cross axis of the container.
- `flex-start`: The element is close to the starting point of the cross axis of the container and does not stretch.
- `flex-end`: The element is close to the end position of the cross axis of the container and does not stretch.
- `center`: The element is centered on the cross axis of the container and does not stretch.
- `baseline` : The cross axis of the element is aligned to the font baseline.




**Baseline Alignment** allows text, pictures, or elements such as [`switch`](/components/switch.md) and [`checkbox`](/components/checkbox.md) to be aligned according to the baseline position of the text, thereby ensuring a neater visual effect. Note that `align-items: baseline` is only valid when the spindle direction is [`row`](#flex-direction).


#### `align-self` <badge type="info" text="内联" />


Specifies the alignment of the flex element itself on the cross axis. This attribute has a higher priority than `align-items`. The following values ​​are supported:


- `auto`: Default value, uses the cross-axis alignment of the flex container.
- `stretch`: The element stretches to fill all the space across the container's cross axis.
- `flex-start`: The element is close to the starting point of the cross axis of the container and does not stretch.
- `flex-end`: The element is close to the end position of the cross axis of the container and does not stretch.
- `center`: The element is centered on the cross axis of the container and does not stretch.
- `baseline`: `align-self` does not support the `baseline` value and has the same effect as `flex-start`.


::: tip

Unlike `align-items`, you cannot use `baseline` values ​​in `align-self`. Therefore, currently the baseline alignment of the cross axis can only be set through the `align-items` attribute of the flex container.
:::



#### `flex-grow`


Specifies the flex growth factor of the flex element in the main axis direction. Is an integer between $[0, 100]$, the default value is $0$. If there is remaining space in the main axis direction, each element will grow by the remaining space allocated in proportion to the growth coefficient. Therefore, if the elements' `flex-grow` are both $1$ then they will equally divide the remaining space of the main axis, and the element with a growth factor of $0$ will not grow.


#### `flex-shrink`


Specifies the shrinkage rate of the flex element in the main axis direction. Is an integer between $[0, 100]$, the default value is $1$. If there is insufficient remaining space on the main axis, the element will be shrunk. The actual reduced size is determined by the initial size of the element, the ratio of the element's own shrinkage to the sum of the search rates of all elements, and the remaining space. The greater the element's shrinkage or initial size, the more shrinkage the element will produce. Elements with `flex-shrink` of $0$ will not shrink.


#### `flex`


`flex` is short for `flex-grow` and `flex-shrink`. The syntax is


```css
flex: <flex-grow> <flex-shrink>;
```


Currently Glyphix does not introduce the `flex-basis` attribute, so there is no need to fill in additional values.


#### `max-height` (not supported yet)


Sets the maximum height of the element (the max-height property does not include padding, borders, or margins). The `max-height` attribute is specified as a single [length](/framework/render/style-and-layout.md#长度) value.


**Default**: The maximum height of the parent control


#### `max-width` (not supported yet)


Sets the maximum width of the element (the max-width attribute does not include padding, borders, or margins). The `max-width` attribute is specified as a single [length](/framework/render/style-and-layout.md#长度) value.


**Default**: The maximum width of the parent control


#### `min-height` (not supported yet)


Sets the minimum height of the element (the min-height property does not include padding, borders, or margins). The `min-height` attribute is specified as a single [length](/framework/render/style-and-layout.md#长度) value.


**Default**: `0`


#### `min-width` (not supported yet)


Sets the minimum width of an element (the min-width property does not include padding, borders, or margins). The `min-width` attribute is specified as a single [length](/framework/render/style-and-layout.md#长度) value.


**Default**: `0`


### Positioning method


#### `position`


Specifies how an element is positioned in the document. Can be set to the following values:


- `static`: Default value, specifies that the element uses normal layout behavior, that is, the element's current layout position in the general flow of the document. At this time, the `top`, `right`, `bottom`, `left` attributes are invalid.
- `absolute`: The element will be moved out of the normal document flow and no space will be reserved for the element. Determine the position of an element by specifying its offset relative to its parent element. Absolutely positioned elements can have margins set.


#### `left`


Specifies the offset of the element relative to the left edge of its containing element.


The value of the `left` attribute is a CSS [length](/framework/render/style-and-layout.md#长度), and the default value is `auto`.


#### `right`


Specifies the offset of the element relative to the right edge of its containing element.


The value of the `right` attribute is a CSS [length](/framework/render/style-and-layout.md#长度), and the default value is `auto`.


#### `top`


Specifies the offset of the element relative to the top edge of its containing element.


The value of the `top` attribute is a CSS [length](/framework/render/style-and-layout.md#长度), and the default value is `auto`.


#### `bottom`


Specifies the offset of the element relative to the bottom edge of its containing element.


The value of the `bottom` attribute is a CSS [length](/framework/render/style-and-layout.md#长度), and the default value is `auto`.


## Text and fonts


### Basic properties


#### `font-family` <badge type="info" text="继承" />


Specify an ordered, named font family list for the element. Use commas to separate multiple fonts. If there are spaces in the font name, you need to include the font name in quotes:


```css
font-family: serif;
font-family: "Times New Roma", serif;
```


Font names are defined by the [`@font-face`](#font-face-规则) rule. If `font-family` is not defined, the element will inherit the font family of the parent element. If neither parent defines a font family, [System default font](/framework/application/font-config.md#默认字体) will be used.


#### `font-size` <badge type="info" text="继承" />


Specifies the font size of the element, which is a [length](/framework/render/style-and-layout.md#长度) value. Similar to `font-family`, `font-size` will also inherit from parent elements, and will use the font size of [System default font](/framework/application/font-config.md#默认字体) when no font size is defined in any parent element.


#### `font-weight` <badge type="info" text="继承" />


Specifies the font weight of the element, that is, the thickness of the font. The value range is an integer in the range $[100, 900]$ and the default value is `400`. If the parent element does not define a weight, the default `400` weight is used. If the specified weight is not found, the closest available weight is used.


::: tip

The `font-weight` attribute only supports integer multiples of `100`, such as `100`, `200`, `300`, etc. Values ​​with remainders (such as `450` ) are rounded to the nearest integral multiple. Currently shipping devices only support `400` font weight.
:::



#### `line-height` <badge type="info" text="继承" />


This property is used to set the amount of space for multiline elements, such as the spacing between multiple lines of text. The `line-height` attribute is specified as a single [length](/framework/render/style-and-layout.md#长度) value or as a **numeric** value. **Default** is `auto`.


In addition to length values, `line-height` can also use numeric values, representing multiples relative to the font size. For example, `line-height: 1.5` means that the line height is 1.5 times the font size. Older versions used `line-height: 150%` for the same effect. <version-badge since="0.9" />


::: important value range
The calculated valid value range of `line-height` is $[0, 1000\rm px]$. Where $0$ row height falls back to the default row height (rather than no row height at all). Regardless of whether length or numeric value (scale) is used, the calculated row height cannot exceed $1000\rm px$. For example, `line-height: 2.0; font-size: 32px` evaluates to $64\rm px$ and is therefore a valid row height value.
:::



##### Automatic row height <experimental /> <version-badge since="0.9" />


The `line-height` value of `auto` means that the line height will be automatically calculated based on the font size, and the behavior is as follows:
- Typically, the default line height is approximately 1.2 times the font size.
- For special fonts such as Arabic and Tibetan, the default line height will be automatically increased to avoid overlap between lines; this makes different lines in a text may have different line heights.
- Using any `line-height` value other than `auto` overrides the behavior of the default row height, causing all rows to have the same row height.
- `auto` has similar semantics to CSS's `normal` line height. Direct use of the `normal` keyword is not supported yet.


Please refer to [i18n documentation](/framework/application/i18n.md#自动行高) for row height behavior in international scenarios.


::: note Rendering Consistency <version-badge since="0.9" />
The text rendering behavior used by different devices is not completely consistent, and the default line height value of `line-height: auto` may be different. Some devices do not automatically adjust the line height for special fonts, but simply use a fixed line height, so there may be overlap between lines when using automatic line height.
:::



##### row height inheritance


When the element is not set to `line-height`, it will inherit the row height value of the parent element. The inherited row height is the original value, not the calculated row height value. For example, if the parent element's `line-height` is `1.5`, the child element inherits `1.5` instead of the calculated line height value of the parent element (i.e. $ 1.5 $ times the parent element's font size). If the `line-height` of the parent element is `auto`, the child element inherits `auto` instead of the calculated default row height value of the parent element.


::: tip `auto` Row height and inheritance
`line-height: auto` does not inherit the row height of the parent element, but the default row height. To use inherited row height, the `line-height` attribute must not be set. The `inherit` keyword is not currently supported for explicit inheritance.
:::



#### `text-align` <badge type="info" text="继承" />


Defines how text is aligned relative to its block parent element. `text-align` does not control the alignment of the block element itself, only the alignment of its inline text.


The following values ​​are supported:


- `left` : left aligned
- `right` : right aligned
- `hcenter` : Horizontally centered alignment
- `justify` : Custom adjustment
- `top` : top aligned
- `bottom` : Bottom aligned
- `vcenter` : vertical center alignment
- `baseline` : baseline alignment
- `center` : horizontal and vertical alignment


::: tip

`text-align: center` is centered in the horizontal and vertical directions at the same time, which is different from `text-align: center` in CSS, which is only centered in the horizontal direction. You should pay attention to the distinction. If you only need horizontal center alignment, use `text-align: hcenter`.
:::



**Default**: `left`


#### `max-lines`


Specify the maximum number of lines of text to be displayed, and overflow content will be handled in the manner specified by [`text-overflow`](#text-overflow). The value type is number, and the default value is `0`, which means there is no limit to the maximum number of rows.


Syntax and examples:


```css
max-lines: 0; /* No limit on the maximum number of rows */
max-lines: 1; /* Fixed to single line display */
max-lines: 2; /* Display up to 2 lines of text */
max-lines: <number>; /* Specifies the maximum number of lines of text that can be displayed */
```


This attribute is compatible with the standard `lines` attribute of Quick Apps.


#### `text-overflow`


Specifies how to prompt the user for hidden overflow text content. You can crop directly or display an ellipsis (`...`). This attribute is used in conjunction with [`max-lines`](#max-lines), that is, the overflow behavior is only triggered when the number of text lines reaches the `max-lines` limit, and other clipping caused by layout height restrictions will not be considered.


Property value:


- `clip`: Overflowed text is directly hidden;
- `ellipsis`: An ellipsis will be added after the displayed text when the text overflows.


**Default**: `clip`


<glyphix id="css-prop-text-overflow" height="100" width="600" title="clip 和 ellipses 对比">


```html
<div>
  <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>
  <p class="ellipsis">
    Lorem ipsum dolor sit amet, consectetur adipisicing elit.
  </p>
</div>
```


```css
div {
  display: flex;
}

p {
  background-color: #ddd;
  margin: 8px;
  padding: 8px;
  max-lines: 2;
}

.ellipsis {
  text-overflow: ellipsis;
}
```


</glyphix>



### `@font-face` Rules


`@font-face` CSS at-rule specifies a custom font for displaying text. The font is available as the font name in the [`font-family`](#font-family) attribute.


```css
@font-face {
  font-family: sans-serif;
  src: url("fonts/Roboto-Regular.ttf");
  font-weight: 400;
  font-style: normal;
}
```


It is recommended to define `@font-face` rules in [Application level font mapping file](/framework/application/font-config.md#应用级字体). This section describes the attribute definitions in the `@font-face` rule block.


#### `font-family`


The specified font name will be used in the [`font-family`](#基本属性-1) attribute. Note that there can only be one font name here, not a list of font names. For example: `font-family: <family-name>`.


#### `src`


Specifies the URI of the font file. The value of this attribute is a list, allowing developers to specify multiple font files for the font. For example


```css
src: url("fonts/Roboto-Regular.ttf"), url("font/Other-Font.ttf");
```


Currently, the `src` attribute only supports the `url()` function or string list, and the `local()`, `format()` and other functions available in the Web are not supported.


## animation


For more information about animation, please refer to chapter [animation](../render/animation.md).


### Basic attributes


#### `animation`


Define elements to perform animation effects. Currently supported formats are as follows:


```css
animation: <name>;
animation: <duration> <timing> <name>;
```


Each placeholder is described as follows:


- `<name>`: a keyframe sequence name defined by [`@keyframes` rules](#keyframes-规则);
- `<duration>`: animation duration, unit is seconds or milliseconds, such as `1000ms`, `0.2s`, default is `1s`;
- `<timing>` : [Easing function](../render/animation.md#缓动函数), default is `ease`.


### `@keyframes` Rules


Please refer to MDN's [`@keyframes`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@keyframes) documentation.


## Transform and display effects


#### `transform`


The `transform` attribute allows developers to rotate, scale, tilt, or translate the element. This attribute applies a visual transformation effect to the element and does not change the layout properties of the element. The value of the `transform` attribute can be a concatenation of the various transformation functions in the following table:


| value | description |
| :--------------------: | ------------------------------------------------------------------- |

| `scale(x, y)` | Scaling transformation, $x$ and $y$ specify the horizontal and vertical scaling ratio of the element respectively. |
| `rotate(angle)` | Rotation transformation, $\it angle$ specifies the angle of rotation, the unit can be `deg` or `rad`. |
| `shear(h, v)` | Miscut transformation, $h$ is the miscut distance in the horizontal direction, $v$ is the miscut distance in the vertical direction. |
| `skew(angleX, angleY)` | Inclined elements along the $x$ and $y$ axes. |
| `translate(x, y)` | Translation shift, moves elements along the $x$ and $y$ axes. |


For example, the following code will first scale the element $(2, 0.5 )$ times, and then rotate $100^{\circ}$:


```css
transform: scale(2, 0.5) rotate(100deg);
```


**Default**: `none`


The transformed element may be clipped by the parent element or obscured by elements behind it. You can use the [`z-index`](#z-index) attribute to promote the Z-axis order of elements to avoid being obscured by elements of the same level. Currently, the `transform` attribute may need to be combined with the [`transparent`](#transparent) attribute to work properly, otherwise an incorrect black background may be produced.


#### `z-index`


The `z-index` attribute sets the Z-order of the elements, `z-index` larger overlapping elements overwrite smaller elements.


#### `opacity`


This property specifies the opacity of an element. is a numerical value in the range $[0, 1.0 ]$.


**Default**: $1.0$ (fully opaque)


::: warning

`opacity` values ​​other than `0` or `1` can affect the drawing performance of the element, and it is recommended to use this attribute only when necessary. If you just need to make the text or background translucent, you should do so using the RGBA format of color values, such as `rgba(255, 0, 0, 0.5)` or `#ff000080` for translucent red.
:::



#### `object-fit`


A strategy used to specify how an image should fit into its box determined using height and width.


Property value:


- `none`: Default value, the image will maintain its original dimensions.
- `contain` : The image will be scaled to maintain its aspect ratio when filling the element's content box. The entire object fills the box while retaining its aspect ratio.
- `cover` : The image fills the element's entire content box while maintaining its aspect ratio. If the object's aspect ratio does not match the content box, the object will be clipped to fit the content box.
- `fill` : The image exactly fills the element's content box. The entire object will completely fill this box. If the object's aspect ratio does not match the content box, the object will be stretched to fit the content box.
- `scale-down`: The image can be scaled down to fit the size of the content box while maintaining aspect ratio, but will not scale when the image is smaller than the size of the content box. The actual scaling factor of `scale-down` is equivalent to the smaller of `none` and `contain`.


::: note

Unlike [web standards](https://developer.mozilla.org/docs/Web/CSS/Reference/Properties/object-fit), the default value of the `object-fit` attribute is `none` instead of `fill`. Please refer to the description of the [`image`](/components/image.md#object-fit) component for details.
:::



#### `transparent`


Sets whether the element is transparent. This property usually does not affect the display effect of the element, but for elements with snapshots, this property may need to be configured according to the actual transparency situation.


Property value:


- `false`: Mark this element as opaque;
- `true`: The marked element is transparent.


**Default**: `false`


#### `stroke-width`


Specify the brush width when drawing certain components, such as [`progress-arc`](/components/progress-arc.md). The type of the value is a [length](/framework/render/style-and-layout.md#长度).


#### `visibility` <badge type="info" text="继承" />


Sets whether the element is displayed. This property does not affect layout.


Property value:


- `hidden`: hidden element;
- `visible`: Display element.


**Default**: `visible`


#### `filter` <experimental />


Apply effects like blur to elements. Currently these values ​​are supported:


- `blur(<length>)` : Applies a blur effect to an element, such as `blur(5px)`.


::: warning experimental feature
On existing devices, using filter effects such as `blur()` may cause serious performance issues. It should be noted that the `blur()` function is not a strict Gaussian blur, and its blur radius $r$ supports a range of $r \in [8, 300]\,\rm px$. Specifically:
- When $r \lt 8\rm px$, there will be no blurring effect;
- The degree of blurriness does not vary continuously with $r$.


In order to improve performance, if the visual effect allows, you should try to choose a larger blur radius ($r \ge 50\rm px$ is recommended), because Glyphix optimizes this situation.
:::



Since the blur effect is expensive, it is recommended to use the [`quiescent`](/framework/generic/properties.md#quiescent) attribute of the native component to avoid frequent drawing updates.


#### `overflow` <experimental /> <version-badge since="0.9" />


The `overflow` attribute is used to specify what to do when the content of an element exceeds the size of the element. The value of this attribute can be one of the following:
```css
overflow: auto | clip | visible;
```
- `auto`: Default value, the content will be cropped when it overflows, equivalent to `clip`.
- `clip`: The content will be cropped when it overflows, and the part beyond the element's content-box size will not be visible.
- `visible`: When the content overflows, it will not be clipped by the element's own content-box, but will continue to be displayed.


When `overflow` is set to `visible`, content can be drawn within the content-box range of the nearest `clip` ancestor, and will not be affected by clipping of itself and the intermediate visible container.


:::tip Differences from Web CSS standards
The default value of the `overflow` attribute is not `visible` but default clipping. And Glyphix does not support values ​​such as `scroll` and `hidden`; nor does it support sub-attributes such as `overflow-x` and `overflow-y`.
:::



##### `overflow` behavior for multi-level containers


`overflow: visible` is not an inherited property. If you want the overflow content of the innermost element not to be clipped, you need to set `overflow: visible` for each level of container on the path from the root to the target element. For example:
```html
<!-- The overflow content of the inner item can be fully displayed -->
<div style="width:100px; height:100px; overflow:visible">     <!-- intermediate container -->
  <p style="width:200px; line-height:100%; overflow:visible"> <!-- overflow element itself -->
    藏文、泰文等长文本不出界
  </p>
</div>
```


##### i18n text overflow problem


In international scenarios, the text height in many languages ​​is large and easily exceeds the reserved line height range, resulting in vertical cropping. In this case, it is recommended to set the `overflow` of the text element to `visible` and use appropriate `line-height` to ensure that the text content can be displayed completely.


The following example shows the effect of a row height that is too small in both cases `overflow: visible` and `overflow: clip`:


<glyphix id="css-overflow-visible" height="80" width="640" title="文本 overflow">


```html
<div>
  <p>Some i18n text with large line height.</p>
  <p style="overflow: visible">Some i18n text with large line height.</p>
</div>
```


```css
div {
  font-size: 1.2rem;
  display: flex;
  flex-direction: column;
}

p {
  line-height: 22px;
  margin: 6px;
  border: 1px solid gray;
}
```


</glyphix>



The above text is cropped in the case of `line-height: 22px` (for example, the lower part of the letter 'g' is cut off), but the text can be displayed completely after setting `overflow: visible`.


Please refer to [i18n documentation](/framework/application/i18n.md#文本溢出) for more instructions.


##### Component specific behavior


Each component also has different processing details for `overflow`. Please refer to the documentation of [`scroll`](/components/scroll.md#padding-和-overflow), [`p`](/components/p.md), [`marquee`](/components/marquee.md) and other components.


## color and background


#### `color` <badge type="info" text="继承" /> <badge type="info" text="内联" />


Set the text color (foreground color) of the element. Please refer to [color value](/framework/render/style-and-layout.md#颜色值) for the syntax of color values.


**Default**: `#ff0000`


#### `background-color` <badge type="info" text="内联" />


Specifies the background color, and is mutually exclusive with the [`background-image`](#background-image) attribute. Please refer to [color value](/framework/render/style-and-layout.md#颜色值) for the syntax of color values.


**Default**: `#ff0000` (black background)


#### `background-image`


Set the background image, mutually exclusive with [`background-color`](#background-color). The following writing methods are supported:


- `background-image: url("path/to/image")` : `url()` function gives [URI](../application/resource.md#uri-和路径) of the background image.


The background image is fixedly aligned to the upper right corner of the element and does not support using attributes like [`object-fit`](#object-fit) to stretch or scale the background image. For such complex scenarios, it is recommended to use a combination of [`stack`](/components/stack.md) and [`image`](/components/image.md) elements.


## Margins and borders


#### `margin`


Sets the element's margins in four directions. The `margin` attribute accepts $1\sim4$ values, which is written as follows


- `margin: x`: Set the top, bottom, left and right margins to `x`
- `margin: v h`: Set the top and bottom margins to `v`, and set the left and right margins to `h`
- `margin: t h b`: Set the top margin to `t`, the bottom margin to `b`, and the left and right margins to `h`
- `margin: t r b l`: Set the top, right, bottom, and left margin widths to `t`, `r`, `b`, `l`


Each value is of type [length](/framework/render/style-and-layout.md#长度).


**Default**: `0`. In a fluid layout, setting the left and right margins of block-level elements to `auto` can make the margins fill the width of the container, for example:


```css
.center-box {
  margin: 0 auto;
}
```


Will center block-level elements of class `center-box` in the container. Similarly, if only the left or right margin is set to `auto`, then the margin of the element will be filled, resulting in a right or left-centered effect.


<glyphix id="css-margin-auto" height="120" width="360" title="auto 边距">


```html
<div>
  <p class="auto">margin: 0 auto</p>
  <p class="left-auto">margin: 0 0 0 auto</p>
  <p class="right-auto">margin: 0 auto 0 0</p>
</div>
```


```css
div {
  background-color: lightgreen;
}

.auto {
  margin: 0 auto;
}

.left-auto {
  margin: 0 0 0 auto;
}

.right-auto {
  margin: 0 auto 0 0;
}

div > p {
  border: 1px solid gray;
  margin-top: 4px;
  margin-bottom: 4px;
}
```


</glyphix>



#### `margin-left`


Sets the left margin of the element.


#### `margin-top`


Sets the top margin of the element.


#### `margin-right`


Sets the right margin of the element.


#### `margin-bottom`


Sets the bottom margin of the element.


#### `padding`


Sets the element's padding in all four directions. The `padding` attribute accepts $1\sim4$ values, which is written as follows


- `padding: x`: Set the top, bottom, left and right margins to `x`
- `padding: v h`: Set the top and bottom margins to `v`, and set the left and right margins to `h`
- `padding: t h b`: Set the top margin to `t`, the bottom margin to `b`, and the left and right margins to `h`
- `padding: t r b l`: Set the top, right, bottom, and left margin widths to `t`, `r`, `b`, `l`


Each value is of type [length](/framework/render/style-and-layout.md#长度).


**Default**: `auto`. By default, the element's `padding` is $0$.


#### `padding-left`


Sets the left padding of the element.


#### `padding-top`


Sets the top padding of an element.


#### `padding-right`


Sets the right padding of the element.


#### `padding-bottom`


Sets the bottom padding of the element.


#### `border`


Sets the element's border style. The following writing methods are supported:


- `border: <length>`: Indicates a border with an outline width of `<length>` and a black color;
- `border: solid`: Indicates a border with an outline width of `1 px` and a black color;
- `border: <length> solid <color>`: Indicates a border with an outline width of `<length>` and a color of `<color>`.


where `<length>` is a [length](/framework/render/style-and-layout.md#长度) and `<color>` is a [color value](/framework/render/style-and-layout.md#颜色值).


Glyphix only supports elements with all borders or one of top, bottom, left or right borders. For example, `border: solid` will give the element a full border, while `border-top: solid` will give the element a top border. When both of these border properties exist in CSS, only the last property will take effect.


#### `border-top`


Specifies the top border style of the element. The format of the value is consistent with the [`border`](#border) attribute.


#### `border-right`


Specifies the right border style of the element. The format of the value is consistent with the [`border`](#border) attribute.


#### `border-bottom`


Specifies the bottom border style of the element. The format of the value is consistent with the [`border`](#border) attribute.


#### `border-left`


Specifies the left border style of the element. The format of the value is consistent with the [`border`](#border) attribute.


#### `border-radius`


**Default**: `0 px`


Sets the border's corner radius. Currently a [length](/framework/render/style-and-layout.md#长度) value is supported. The `border-radius` attribute only takes effect if the element has all borders (see the [`border`](#border) attribute).


## Pseudo class


### `active`


Elements such as buttons will have this pseudo-class when pressed.


### `disabled`


The element has this pseudo-class when it is in the [`disabled`](properties.md#disabled) state, where it does not respond to gesture events. This state can often be communicated to the user by making the element less transparent, for example:


```css
<some-selector>:disabled {
  opacity: 0.5;
}
```


For a more complete example, see the [`disabled`](properties.md#disabled) attribute.