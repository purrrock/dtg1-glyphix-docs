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

