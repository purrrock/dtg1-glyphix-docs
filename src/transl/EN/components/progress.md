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