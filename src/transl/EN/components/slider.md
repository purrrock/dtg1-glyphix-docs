# slider

Slider component, which defaults to a block-level element.

## Attributes

### `value` <decl type="number" get set listen />

The current value, with a default of $10$.

Setting the `value` attribute will change the current value of the component. You can listen for changes to the current value using the `on` directive, which is triggered every time the current value changes.

### `min` <decl type="number" set />

The minimum value, with a default of $0$.

### `max` <decl type="number" set />

The maximum value, with a default of $100$.

### `vertical` <decl type="boolean" set />

If the value of the `vertical` attribute is `true`, the `slider` component will be displayed vertically; otherwise, it will be displayed horizontally. The default value is `false`. 

## CSS Specifications

Developers can customize the appearance of the `slider` component using CSS.

### Dimension Calculation

The default width and height of a `slider` are the same as the element's font size, which is set by the [`font-size`](/framework/generic/styles.md#font-size) property (or inherited). You can customize the dimensions of the `progress` using the [`width`](/framework/generic/styles.md#width) and [`height`](/framework/generic/styles.md#height) properties.

### CSS Properties

The following CSS properties may be very useful:
- [`background-color`](/framework/generic/styles.md#background-color) controls the background color of the `slider`;
- [`color`](/framework/generic/styles.md#color) controls the progress bar color of the `slider`;
- [`border-radius`](/framework/generic/styles.md#border-radius) can set the `slider` to have rounded borders, for example, `50%` produces a semi-circular border;

Other CSS properties may also be useful, such as setting border styles using the [`border`](/framework/generic/styles.md#border) property.

### CSS Pseudo-elements

#### `value`

This pseudo-element can be used to style the `slider` progress bar independently of the background portion. For example, you can set the border-radius for the track background and the progress bar portion separately to achieve an effect where the outer border has rounded line caps while the progress bar has straight caps.

``` css
slider {
  border-radius: 50%; /* Track background border-radius */
}

slider::value {
  border-radius: 0; /* Progress bar of the track has no border-radius */
}
```

#### `thumb` <experimental/>

The `thumb` pseudo-element is used to define the style of the `slider` thumb. By default, the `slider` does not include a thumb; to display a thumb, you must specify the width and height of the `thumb` element:
``` css
slider::thumb {
  width: 150%;
  height: 150%;
  border-radius: 50%;
}
```
Percentage units for `width` and `height` are calculated relative to the element's own dimensions. For a horizontal `slider`, the thumb's width and height are calculated as a percentage based on the element's CSS `height`, while for a vertical `slider`, the thumb's width and height are calculated based on the element's CSS `width` property. For example, if the element's CSS is:
``` css
slider {
  width: 200px;
  height: 24px;
}
```
Then the width and height of the thumb corresponding to `slider::thumb` above are both $24\rm{px} \times 150\% = 36\rm{px}$. The percentage-based border-radius of the thumb is calculated based on the thumb's own dimensions. In this example, the calculated border-radius for the `thumb` pseudo-element with `50%` is $36\rm{px} \times 50\%=18\rm{px}$.

The `thumb` pseudo-element supports the `border` CSS property, but the border will not exceed the dimensions of the `thumb` pseudo-element.

### CSS Example

The following example demonstrates some ways to customize the appearance of the progress bar using CSS.
<glyphix id="components-slider-styles" height="180" width="480" title="Slider Styles">

``` html
<div>
  <!-- Default style -->
  <slider ::value="value" />
  <!-- Flat-ended progress bar style -->
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
  /* Setting the border-radius of the value pseudo-element to 0 achieves a flat-ended progress bar effect */
  border-radius: 0;
}

.more-style {
  /* Custom border-radius */
  border-radius: 30%;
  /* slider background color */
  background-color: #b3c5d7;
  /* slider foreground color */
  color: #b5179e;
  /* padding can adjust the margin of the slider foreground */
  padding: 6px;
  height: 1rem;
}

/* Define track thumb style */
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