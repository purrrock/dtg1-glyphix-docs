---
icon: layers-outline
---
# CSS Properties

This section introduces all CSS properties supported by the Glyphix framework. For an introduction to the styling and layout mechanism, please refer to [this document](/framework/render/style-and-layout.md).

## Layout Control

### Basic Properties

#### `display`

The `display` property sets an element's layout scheme. Currently, it can be set to the following values:

- `inline`: Default value. The element generates one or more inline element boxes that do not generate line breaks before or after them. In normal flow, if there is space, the next element will be on the same line.
- `block`: The element generates a block-level element box, generating line breaks before and after the element in normal flow.
- `flex`: The element behaves like a block-level element and lays out its contents according to `Flex` layout.
- `inline-flex` and `inline flex`: The element behaves like an inline element and its contents are laid out according to `Flex` layout.
- `none`: In this mode, the element is not displayed (not recommended).

#### `width`

The `width` property specifies the width of an element, including `padding` and `border` (border-box). If the element is located within a layout container or other constraints exist, the final element dimensions may differ from the value of the `width` property.

::: tip
Glyphix currently only supports the [border-box](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-sizing) mode, and the value of `width` always includes `padding` and `border`.
:::

The value of the `width` property is a CSS [length](/framework/render/style-and-layout.md#长度). The specific values are as follows:

- `auto`: Default value. This mode automatically calculates the element's width based on content dimensions and layout constraints. For example, a text element determines its width based on the size of the text content, while a container element determines its width based on the layout dimensions of its internal elements.
- `value [unit]`: Specifies the element width using a length unit. Layout or other constraints may adjust the actual dimensions of the element.

The `width` property of an element in a flex layout serves as its initial width, which will be further adjusted to the optimal actual width during the layout process.

#### `height`

The `height` property specifies the height of an element, including `padding` and `border` (border-box). The behavior of this property is similar to [`width`](#width).

### Flex Layout

#### `flex-direction`

Sets the main axis direction (horizontal or vertical) when using a flex layout container. Values are as follows:

- `row`: Default value, the main axis runs horizontally.
- `column`: The main axis runs vertically.

The `flex-direction` property is only valid when the element uses a flex layout, for example:

```css
display: flex;
flex-direction: column;
```

#### `flex-flow`

`flex-flow` is a shorthand property for `flex-direction` and `flex-wrap`. The syntax is:

```css
flex-flow: <flex-direcion> <flex-wrap>;
```

Currently, the `flex-wrap` property is not yet implemented, so this part will not have any effect.

#### `justify-content`

Specifies the alignment of child elements along the container's main axis when using flex layout.

Property values:

- `flex-start`: Default value. The first element is flush against the start of the container's main axis, and subsequent elements are arranged sequentially. No extra space is filled between elements.
- `flex-end`: The last element is flush against the end of the container's main axis, and preceding elements are arranged sequentially. No extra space is filled between elements.
- `center`: All elements are arranged sequentially in the middle of the container's main axis, with remaining space left at both ends of the main axis. No extra space is filled between elements.
- `space-between`: Elements are evenly distributed; the first element is placed at the start, the last element is placed at the end, and the remaining space is evenly distributed between the elements.
- `space-around`: Elements are evenly distributed, with equal space allocated around each element. Remaining space is also left before the first element and after the last element.

#### `align-items` <badge type="info" text="Inline" />

Specifies the alignment of child elements along the container's cross axis when using flex layout. Supports the following values:

- `stretch`: Default value. Elements stretch to fill all space in the container's cross axis.
- `flex-start`: Elements are flush against the start of the container's cross axis and do not stretch.
- `flex-end`: Elements are flush against the end of the container's cross axis and do not stretch.
- `center`: Elements are centered along the container's cross axis and do not stretch.
- `baseline`: Elements' cross axes are aligned according to their font baselines.


**Baseline alignment** allows text, images, or elements such as [`switch`](/components/switch.md) and [`checkbox`](/components/checkbox.md) to align according to the text baseline position, thereby ensuring a neat visual effect. Note that `align-items: baseline` is only valid when the main axis direction is [`row`](#flex-direction).

#### `align-self` <badge type="info" text="Inline" />

Specifies the alignment of a flex item itself along the cross axis. This property has a higher priority than `align-items`. Supports the following values:

- `auto`: Default value. Uses the flex container's cross-axis alignment.
- `stretch`: The element stretches to fill all space in the container's cross axis.
- `flex-start`: The element is flush against the start of the container's cross axis and does not stretch.
- `flex-end`: The element is flush against the end of the container's cross axis and does not stretch.
- `center`: The element is centered along the container's cross axis and does not stretch.
- `baseline`: `align-self` does not support the `baseline` value and has the same effect as `flex-start`.

::: tip
Unlike `align-items`, you cannot use the `baseline` value in `align-self`. Therefore, cross-axis baseline alignment can currently only be set via the flex container's `align-items` property.
:::

#### `flex-grow`

Specifies the flex growth factor of a flex item along the main axis. It is an integer between $[0, 100]$, with a default value of $0$. If there is remaining space along the main axis, each element will grow in proportion to its growth factor. Therefore, if all elements have a `flex-grow` of $1$, they will evenly divide the remaining space on the main axis, whereas elements with a growth factor of $0$ will not grow.

#### `flex-shrink`

Specifies the flex shrink factor of a flex item along the main axis. It is an integer between $[0, 100]$, with a default value of $1$. If the remaining space on the main axis is insufficient, the elements will shrink. The actual reduced size is jointly determined by the initial size of the element, the ratio of its shrink factor to the sum of all elements' shrink factors, and the remaining space. The larger an element's shrink factor or initial size, the more its size will be reduced. Elements with a `flex-shrink` of $0$ will not shrink.

#### `flex`

`flex` is a shorthand property for `flex-grow` and `flex-shrink`. The syntax is:

```css
flex: <flex-grow> <flex-shrink>;
```

Currently, Glyphix does not introduce the `flex-basis` property, so no extra value needs to be filled.

#### `max-height` (Not yet supported)

Sets the maximum height of an element (the max-height property does not include padding, borders, or margins). The `max-height` property is specified as a single [length](/framework/render/style-and-layout.md#长度) value.

**Default value**: Maximum height of the parent widget

#### `max-width` (Not yet supported)

Sets the maximum width of an element (the max-width property does not include padding, borders, or margins). The `max-width` property is specified as a single [length](/framework/render/style-and-layout.md#长度) value.

**Default value**: Maximum width of the parent widget

#### `min-height` (Not yet supported)

Sets the minimum height of an element (the min-height property does not include padding, borders, or margins). The `min-height` property is specified as a single [length](/framework/render/style-and-layout.md#长度) value.

**Default value**: `0`

#### `min-width` (Not yet supported)

Sets the minimum width of an element (the min-width property does not include padding, borders, or margins). The `min-width` property is specified as a single [length](/framework/render/style-and-layout.md#长度) value.

**Default value**: `0`

### Positioning

#### `position`

Specifies the positioning method of an element in the document. Can be set to the following values:

- `static`: Default value. Specifies that the element uses normal layout behavior, meaning the element is in its current layout position in the document's normal flow. In this state, the `top`, `right`, `bottom`, and `left` properties have no effect.
- `absolute`: The element is removed from the normal document flow and no space is reserved for it. The element's position is determined by specifying offsets relative to its containing element. Absolutely positioned elements can have margins.

#### `left`

Specifies the offset of an element from the left edge of its containing element.

The value of the `left` property is a CSS [length](/framework/render/style-and-layout.md#长度), and the default value is `auto`.

#### `right`

Specifies the offset of an element from the right edge of its containing element.

The value of the `right` property is a CSS [length](/framework/render/style-and-layout.md#长度), and the default value is `auto`.

#### `top`

Specifies the offset of an element from the top edge of its containing element.

The value of the `top` property is a CSS [length](/framework/render/style-and-layout.md#长度), and the default value is `auto`.

#### `bottom`

Specifies the offset of an element from the bottom edge of its containing element.

The value of the `bottom` property is a CSS [length](/framework/render/style-and-layout.md#长度), and the default value is `auto`.

## Text and Fonts

### Basic Properties

#### `font-family` <badge type="info" text="Inherited" />

Specifies a prioritized list of font family names for an element. Multiple fonts are separated by commas. If a font name contains spaces, it must be enclosed in quotes:

```css
font-family: serif;
font-family: "Times New Roman", serif;
```

Font names are defined by the [`@font-face`](#font-face-rule) rule. If `font-family` is not defined, the element will inherit the font family of its parent element. If none of the parent elements define a font family, the [system default font](/framework/application/font-config.md#默认字体) will be used.

#### `font-size` <badge type="info" text="Inherited" />

Specifies the font size of an element, which is a [length](/framework/render/style-and-layout.md#长度) value. Similar to `font-family`, `font-size` is also inherited from parent elements. If no parent element defines a font size, the font size of the [system default font](/framework/application/font-config.md#默认字体) will be used.

#### `font-weight` <badge type="info" text="Inherited" />

Specifies the font weight, i.e., the boldness of the font. The value is an integer in the range $[100, 900]$, with a default value of `400`. If the parent element does not define a font weight, the default weight `400` is used. If the specified weight is not found, the system will use the closest available weight.

::: tip
The `font-weight` property only supports values that are integer multiples of `100`, such as `100`, `200`, `300`, etc. Values with remainders (like `450`) are rounded to the nearest multiple. Devices currently on the market only support the `400` weight.
:::

#### `line-height` <badge type="info" text="Inherited" />

This property is used to set the amount of space used for lines, such as the spacing between lines of multi-line text. The `line-height` property is specified as a single [length](/framework/render/style-and-layout.md#长度) value or a **number** value. The **default** is `auto`.

In addition to length values, `line-height` can also use number values, representing a multiple of the font size. For example, `line-height: 1.5` means the line height is 1.5 times the font size. Older versions used `line-height: 150%` to achieve the same effect. <version-badge since="0.9" />

::: important Value Range
The valid range for calculated `line-height` is $[0, 1000\rm px]$. A line height of $0$ will fall back to the default line height (rather than having no line height at all). Regardless of whether a length or a number (ratio) is used, the calculated line height cannot exceed $1000\rm px$. For example, `line-height: 2.0; font-size: 32px` calculates to $64\rm px$, which is a valid line height value.
:::

##### Automatic Line Height <experimental /> <version-badge since="0.9" />

The `auto` value for `line-height` indicates that the line height will be automatically calculated based on the font size, with the following behavior:
- Normally, the default line height is close to 1.2 times the font size.
- For special fonts such as Arabic and Tibetan, the default line height is automatically increased to prevent overlapping between lines; this means different lines within a piece of text may have different line heights.
- Using any non-`auto` `line-height` value overrides the default line height behavior, causing all lines to have the same line height.
- `auto` is semantically similar to CSS's `normal` line height; direct use of the `normal` keyword is not currently supported.

For line height behavior in internationalization scenarios, please refer to the [i18n documentation](/framework/application/i18n.md#自动行高).

::: note Rendering Consistency <version-badge since="0.9" />
Text rendering behavior varies across devices, and the default line height value for `line-height: auto` may differ. Some devices do not automatically adjust line heights for special fonts, instead simply using a fixed line height, which may result in line overlapping when using automatic line height.
:::

##### Line Height Inheritance

When an element does not set `line-height`, it inherits the line height value of its parent element. The inherited line height is the raw value, not the calculated line height value. For example, if the parent element's `line-height` is `1.5`, the child element inherits `1.5` as well, rather than the parent's calculated line height (i.e., $1.5$ times the parent font size). If the parent element's `line-height` is `auto`, the child element also inherits `auto`, rather than the parent's calculated default line height value.

::: tip `auto` Line Height and Inheritance
`line-height: auto` does not inherit the parent element's line height; it defaults to the automatic line height. To use inherited line height, you must omit the `line-height` property. The `inherit` keyword for explicit inheritance is currently not supported.
:::

#### `text-align` <badge type="info" text="Inherited" />

Defines how text is aligned relative to its block parent element. `text-align` does not control the alignment of the block element itself, but only the alignment of its inline text.

Supports the following values:

- `left`: Left-aligned
- `right`: Right-aligned
- `hcenter`: Horizontally centered
- `justify`: Justified
- `top`: Top-aligned
- `bottom`: Bottom-aligned
- `vcenter`: Vertically centered
- `baseline`: Baseline-aligned
- `center`: Centered horizontally and vertically

::: tip
`text-align: center` centers alignment in both horizontal and vertical directions simultaneously, which is different from CSS `text-align: center` where it only centers horizontally. Please note this distinction. If you only need horizontal centering, please use `text-align: hcenter`.
:::

**Default value**: `left`

#### `max-lines`

Specifies the maximum number of lines text can display, with overflowing content handled as specified by [`text-overflow`](#text-overflow). The value type is number, with a default value of `0`, which means no limit on the maximum number of lines.

Syntax and examples:

```css
max-lines: 0; /* No limit on maximum lines */
max-lines: 1; /* Fixed to single-line display */
max-lines: 2; /* Display up to 2 lines of text */
max-lines: <number>; /* Specify the maximum number of text lines that can be displayed */
```

This property is compatible with the Quick App standard `lines` property.

#### `text-overflow`

Specifies how to signal to users that hidden overflow text content exists. It can be directly clipped or display an ellipsis (`...`). This property is used in conjunction with [`max-lines`](#max-lines)—meaning the overflow behavior is only triggered when the text reaches the `max-lines` limit; other clipping caused by layout height constraints is not considered.

Property values:

- `clip`: Overflowing text is simply hidden;
- `ellipsis`: When text overflows, an ellipsis is appended to the displayed text.

**Default value**: `clip`

<glyphix id="css-prop-text-overflow" height="100" width="600" title="Comparison of clip and ellipsis">

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

### `@font-face` Rule

The `@font-face` CSS at-rule specifies a custom font for displaying text. This font can be used as a font name in the [`font-family`](#font-family) property.

```css
@font-face {
  font-family: sans-serif;
  src: url("fonts/Roboto-Regular.ttf");
  font-weight: 400;
  font-style: normal;
}
```

It is recommended to define `@font-face` rules in the [app-level font mapping file](/framework/application/font-config.md#应用级字体). This section introduces the property definitions within the `@font-face` rule block.

#### `font-family`

The specified font name will be used for the [`font-family`](#基本属性-1) property. Note that this can only be a single font name, not a list of font names. For example: `font-family: <family-name>`.

#### `src`

Specifies the URI of the font file. The value of this property is a list, allowing developers to specify multiple font files for a font. For example:

```css
src: url("fonts/Roboto-Regular.ttf"), url("font/Other-Font.ttf");
```

Currently, the `src` property only supports the `url()` function or a list of strings; functions like `local()` and `format()` available in Web are not supported.

## Animation

For more knowledge about animations, please refer to the [Animation](../render/animation.md) chapter.

### Basic Properties

#### `animation`

Defines the animation effect to be executed by the element. Currently supported formats are:

```css
animation: <name>;
animation: <duration> <timing> <name>;
```

Descriptions of placeholders are as follows:

- `<name>`: A sequence name of keyframes defined by the [`@keyframes` rule](#keyframes-规则);
- `<duration>`: Animation duration in seconds or milliseconds, e.g., `1000ms`, `0.2s`, defaults to `1s`;
- `<timing>`: [Easing function](../render/animation.md#缓动函数), defaults to `ease`.

### `@keyframes` Rule

Please refer to MDN's [`@keyframes`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@keyframes) documentation.

## Transform and Display Effects

#### `transform`

The `transform` property allows developers to rotate, scale, skew, or translate elements. This property applies a visual transformation effect to the element without altering its layout properties. The value of the `transform` property can be a cascade of various transformation functions from the table below:

|          Value         | Description                                                                 |
| :--------------------: | --------------------------------------------------------------------------- |
|     `scale(x, y)`      | Scaling transform, where $x$ and $y$ specify the horizontal and vertical scaling ratios of the element respectively. |
|    `rotate(angle)`     | Rotation transform, where $\it angle$ specifies the angle of rotation, in units of `deg` or `rad`. |
|     `shear(h, v)`      | Shearing transform, where $h$ is the horizontal shear distance and $v$ is the vertical shear distance. |
| `skew(angleX, angleY)` | Skews the element along the $x$ and $y$ axes.                               |
|   `translate(x, y)`    | Translation transform, moving the element along the $x$ and $y$ axes.       |

For example, the following code first scales the element by $(2, 0.5)$ and then rotates it by $100^{\circ}$:

```css
transform: scale(2, 0.5) rotate(100deg);
```

**Default value**: `none`

Transformed elements may be clipped by parent elements or obscured by elements behind them. You can use the [`z-index`](#z-index) property to elevate the element's Z-axis order to prevent it from being obscured by sibling elements. Currently, the `transform` property may need to be used in conjunction with the [`transparent`](#transparent) property to work properly; otherwise, an incorrect black background may be generated.

#### `z-index`

The `z-index` property sets the Z-axis order of an element. Overlapping elements with a larger `z-index` will cover those with a smaller one.

#### `opacity`

This property specifies the opacity of an element. It is a numeric value in the range $[0, 1.0]$.

**Default value**: $1.0$ (completely opaque)

::: warning
`opacity` values other than `0` or `1` affect the rendering performance of elements. It is recommended to use this property only when necessary. If you only need to make text or background semi-transparent, you should use the RGBA format of color values, such as `rgba(255, 0, 0, 0.5)` or `#ff000080` for semi-transparent red.
:::

#### `object-fit`

Used to specify the strategy for how an image should be resized to fit its box determined by its height and width.

Property values:

- `none`: Default value. The image retains its original size.
- `contain`: The image is scaled to maintain its aspect ratio while filling the element's content box. The entire object retains its aspect ratio while filling the box.
- `cover`: The image fills the element's entire content box while maintaining its aspect ratio. If the aspect ratio of the object does not match the content box, the object will be clipped to fit.
- `fill`: The image exactly fills the element's content box. The entire object will completely fill this box. If the aspect ratio of the object does not match the content box, the object will be stretched to fit.
- `scale-down`: The image is scaled down to fit the content box while maintaining its aspect ratio, but is not scaled up when smaller than the content box. The actual scale factor for `scale-down` is equivalent to the smaller of `none` and `contain`.

::: note
Unlike the [Web standard](https://developer.mozilla.org/docs/Web/CSS/Reference/Properties/object-fit), the default value of the `object-fit` property is `none` rather than `fill`. For details, please refer to the description of the [`image`](/components/image.md#object-fit) component.
:::

#### `transparent`

Sets whether an element is transparent. This property usually does not affect the display effect of an element, but elements with snapshots may need to configure this property according to their actual transparency situation.

Property values:

- `false`: Marks this element as opaque;
- `true`: Marks this element as transparent.

**Default value**: `false`

#### `stroke-width`

Specifies the brush width when certain components are rendered, such as [`progress-arc`](/components/progress-arc.md). The value type is a [length](/framework/render/style-and-layout.md#长度).

#### `visibility` <badge type="info" text="Inherited" />

Sets whether an element is displayed. This property does not affect layout.

Property values:

- `hidden`: Hides the element;
- `visible`: Displays the element.

**Default value**: `visible`

#### `filter` <experimental />

Applies effects like blur to an element. Currently supported values are:

- `blur(<length>)`: Applies a blur effect to the element, e.g., `blur(5px)`.

::: warning Experimental Feature
On existing devices, using filter effects like `blur()` may cause severe performance issues. Note that the `blur()` function is not strictly a Gaussian blur, and its supported blur radius range is $r \in [8, 300]\,\rm px$. Specifically:
- When $r \lt 8\rm px$, no blur effect is produced;
- The degree of blur does not vary continuously with changes in $r$.

To improve performance, choose a larger blur radius whenever visual effects permit (recommended $r \ge 50\rm px$), because Glyphix optimizes for this scenario.
:::

Due to the high cost of blur effects, it is recommended to use them in conjunction with the [`quiescent`](/framework/generic/properties.md#quiescent) property of native components to avoid frequent rendering updates.

#### `overflow` <experimental /> <version-badge since="0.9" />

The `overflow` property is used to specify how to handle content that exceeds an element's dimensions. The value of this property can be one of the following:
```css
overflow: auto | clip | visible;
```
- `auto`: Default value. Overflowing content will be clipped, equivalent to `clip`.
- `clip`: Overflowing content will be clipped, and portions exceeding the element's content-box dimensions will not be visible.
- `visible`: Overflowing content will not be clipped by the element's own content-box, but will continue to be displayed.

When `overflow` is set to `visible`, content can be rendered within the content-box range of the nearest `clip` ancestor, unaffected by clipping from itself or intermediate visible containers.

::: tip Differences from Web CSS Standard
The default value of the `overflow` property is not `visible`, but clipping by default. Furthermore, Glyphix does not support values such as `scroll` and `hidden`, nor does it support sub-properties like `overflow-x` and `overflow-y`.
:::

##### `overflow` Behavior in Multi-Level Containers

`overflow: visible` is not an inherited property. If you want the overflowing content of the innermost element not to be clipped, you must set `overflow: visible` on every level of container along the path from the root to the target element. For example:
```html
<!-- The overflowing content of the inner item can be fully displayed -->
<div style="width:100px; height:100px; overflow:visible">     <!-- Intermediate container -->
  <p style="width:200px; line-height:100%; overflow:visible"> <!-- Overflowing element itself -->
    Long text in Tibetan, Thai, etc. will not go out of bounds
  </p>
</div>
```

##### Overflow Issues with i18n Text

In internationalization scenarios, text in many languages has a large height and tends to exceed the reserved line-height range, resulting in vertical clipping. For such cases, it is recommended to set the text element's `overflow` to `visible` and pair it with an appropriate `line-height` to ensure that the text content can be displayed in full.

The following example shows the effect when line height is too small under both `overflow: visible` and `overflow: clip`:

<glyphix id="css-overflow-visible" height="80" width="640" title="Text overflow">

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

The text above is clipped at `line-height: 22px` (e.g., the lower half of the letter 'g' is cut off), whereas setting `overflow: visible` allows the text to be displayed completely.

For more details, please refer to the [i18n documentation](/framework/application/i18n.md#文本溢出).

##### Component-Specific Behavior

Details of how various components handle `overflow` may vary. Please refer to component documentation such as [`scroll`](/components/scroll.md#padding-和-overflow), [`p`](/components/p.md), and [`marquee`](/components/marquee.md).

## Color and Background

#### `color` <badge type="info" text="Inherited" /> <badge type="info" text="Inline" />

Sets the text color (foreground color) of an element. For the syntax of color values, please refer to [Color Values](/framework/render/style-and-layout.md#颜色值).

**Default value**: `#ff0000`

#### `background-color` <badge type="info" text="Inline" />

Specifies the background color, which is mutually exclusive with the [`background-image`](#background-image) property. For the syntax of color values, please refer to [Color Values](/framework/render/style-and-layout.md#颜色值).

**Default value**: `#ff0000` (black background)

#### `background-image`

Sets the background image, which is mutually exclusive with [`background-color`](#background-color). Supports the following writing style:

- `background-image: url("path/to/image")`: The `url()` function provides the [URI](../application/resource.md#uri-和路径) of the background image.

Background images are fixed and aligned to the upper-right corner of the element for display, and stretching or scaling background images using properties similar to [`object-fit`](#object-fit) is not supported. For such complex scenarios, it is recommended to use a combination of [`stack`](/components/stack.md) and [`image`](/components/image.md) elements.

## Margins and Borders

#### `margin`

Sets the outer margins of an element in all four directions. The `margin` property accepts $1\sim4$ values, following this syntax:

- `margin: x`: Sets top, bottom, left, and right margins all to `x`
- `margin: v h`: Sets top and bottom margins to `v`, and left and right margins to `h`
- `margin: t h b`: Sets top margin to `t`, bottom margin to `b`, and left and right margins to `h`
- `margin: t r b l`: Sets top, right, bottom, and left margin widths to `t`, `r`, `b`, and `l` respectively.

Each value type is a [length](/framework/render/style-and-layout.md#长度).

**Default value**: `0`. In fluid layout, setting the left and right margins of a block-level element to `auto` can make the margins fill the width of the container, for example:

```css
.center-box {
  margin: 0 auto;
}
```

This centers the block-level element with the class `center-box` in the container. Similarly, if only the left or right margin is set to `auto`, that margin of the element will expand to fill the space, resulting in a right-aligned or left-aligned effect.

<glyphix id="css-margin-auto" height="120" width="360" title="auto margins">

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

Sets the left outer margin of an element.

#### `margin-top`

Sets the top outer margin of an element.

#### `margin-right`

Sets the right outer margin of an element.

#### `margin-bottom`

Sets the bottom outer margin of an element.

#### `padding`

Sets the inner padding of an element in all four directions. The `padding` property accepts $1\sim4$ values, following this syntax:

- `padding: x`: Sets top, bottom, left, and right padding all to `x`
- `padding: v h`: Sets top and bottom padding to `v`, and left and right padding to `h`
- `padding: t h b`: Sets top padding to `t`, bottom padding to `b`, and left and right padding to `h`
- `padding: t r b l`: Sets top, right, bottom, and left padding widths to `t`, `r`, `b`, and `l` respectively.

Each value type is a [length](/framework/render/style-and-layout.md#长度).

**Default value**: `auto`. Under the default value, the element's `padding` is $0$.

#### `padding-left`

Sets the left inner padding of an element.

#### `padding-top`

Sets the top inner padding of an element.

#### `padding-right`

Sets the right inner padding of an element.

#### `padding-bottom`

Sets the bottom inner padding of an element.

#### `border`

Sets the border style of an element. Supports the following writing styles:

- `border: <length>`: Represents a border with an outline width of `<length>` and a black color;
- `border: solid`: Represents a border with an outline width of `1 px` and a black color;
- `border: <length> solid <color>`: Represents a border with an outline width of `<length>` and a color of `<color>`.

Where `<length>` is a [length](/framework/render/style-and-layout.md#长度), and `<color>` is a [color value](/framework/render/style-and-layout.md#颜色值).

Glyphix only supports elements having all borders or one of the top, bottom, left, or right borders. For example, `border: solid` gives the element all borders, while `border-top: solid` gives the element only a top border. When multiple conflicting border properties coexist in CSS, only the last one will take effect.

#### `border-top`

Specifies the top border style of an element. The value format is consistent with the [`border`](#border) property.

#### `border-right`

Specifies the right border style of an element. The value format is consistent with the [`border`](#border) property.

#### `border-bottom`

Specifies the bottom border style of an element. The value format is consistent with the [`border`](#border) property.

#### `border-left`

Specifies the left border style of an element. The value format is consistent with the [`border`](#border) property.

#### `border-radius`

**Default value**: `0 px`

Sets the corner radius of the border. Currently supports a single [length](/framework/render/style-and-layout.md#长度) value. The `border-radius` property only takes effect when the element has all borders (see the [`border`](#border) property).

## Pseudo-classes

### `active`

Elements such as buttons will have this pseudo-class when in the pressed state.

### `disabled`

An element has this pseudo-class when it is in the [`disabled`](properties.md#disabled) state, during which the element does not respond to gesture events. You can typically lower the element's opacity to communicate this state to the user, for example:

```css
<some-selector>:disabled {
  opacity: 0.5;
}
```

For a more complete example, please refer to the [`disabled`](properties.md#disabled) property.