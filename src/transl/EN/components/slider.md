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