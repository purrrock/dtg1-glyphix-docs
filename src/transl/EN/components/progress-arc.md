# progress-arc


The `progress-arc` component is used to display a circular progress bar and defaults to a block-level element.


## property


### `max` <decl type="number" set />


The maximum progress value that the [`value`](#value) attribute will not be greater than.


### `min` <decl type="number" get setet />


The minimum progress value that the [`value`](#value) attribute will not be less than.


### `value` <decl type="number" get set listen />


Set the progress value. The display ratio of the progress depends on the ratio of the `value` attribute in the interval from `min` to `max`, and the display ratio will be limited to $0\% \sim 100\%$. The `value` value is an integer. If a floating point value is set, only the integer part will be truncated.


### `busy` <decl type="boolean" get set />


Set whether the `progress-arc` component is in a busy state. In the busy state, a loading animation will be displayed instead of displaying the value of the `value` attribute. The following example demonstrates how to use a circular progress bar to simulate a loading animation:


<glyphix id="components-progress-arc-busy" height="100" width="300" title="模拟加载动画">


``` html
<progress-arc busy :startAngle="0" :stopAngle="360" />
```


</glyphix>



In this example, the difference between the start angle and the end angle of the progress bar is $360^\circ$. At this time, the typical loading animation effect can be displayed through the `busy` attribute.


::: tip

As long as the progress bar is circular, it will display a fixed busy animation effect, and the starting and ending angles have no effect.
:::



### `startAngle` <decl type="number" get set />


The starting angle of the arc-shaped progress bar. The default value is $135$. For more information, please refer to the [角度配置](#角度配置) chapter.


### `stopAngle` <decl type="number" get set />


The end angle of the arc-shaped progress bar. The default value is $405$. For more information, please refer to the [角度配置](#角度配置) chapter.


## Instructions for use


### angle configuration


Unlike linear [`progress`](progress.md), arc-shaped or circular progress bars need to be properly configured with `startAngle` attributes and `stopAngle` attributes to display properly. Both properties use angle units. In the screen coordinate system, $0^\circ$ points to the horizontal right direction, that is, the $3$ o'clock direction of the clock, and increases in the clockwise direction, and vice versa decreases.


The display of `progress-arc` is a linear interpolation of the angular range based on the scale of `value` in $[\texttt{min}, \texttt{max}]$. Specifically, the user will see the highlighted angle of progress starting at `startAngle` and ending at `valueAngle`:


$$

\begin{aligned}

  k &= \frac{\texttt{value} - \texttt{min}}{\texttt{max}-\texttt{min}}\\

  \texttt{valueAngle} &= (1-k)\texttt{startAngle} + k\cdot\texttt{stopAngle}

\end{aligned}

$$



Therefore, if you want to display a full circle of circular progress bar, you need to make the starting and ending angles differ by $360^\circ$, even though the two angles are visually the same. Alternatively, the starting angle can be larger than the ending angle, which will reverse the direction of the progress.


The examples below show various angle configurations in action, please note that the second example shows the reverse progress display technique.


<glyphix id="components-progress-arc-angles" height="120" width="720" title="角度配置示例">


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



## CSS specifications


### Size calculation


The display size of `progress-arc` is determined by its `width` and `height` attributes. `progress-arc` will occupy the shorter axis, and the center of the arc-shaped progress bar will be the center of the element. By default, the size of `progress-arc` may be close to one character, which will lead to very weird display effects, so it is usually necessary to explicitly specify the width and height in CSS, or use other reasonable layout strategies.


::: tip

It's best to specify a reasonable width and height for the `progress-arc` component, otherwise it may not be recognized. At a minimum, the `width` CSS property should also be set, and the component's layout strategy will automatically use the $1:1$ aspect ratio.
:::



### CSS properties


The appearance of the `progress-arc` component can be adjusted via CSS.


#### `stroke-width`


This property specifies the arc outline width of the `progress-arc` component. The value type is [长度](/framework/render/style-and-layout.md#长度) and does not support percentage units.


::: tip

If you want the drawing width of the `progress-arc` component to be proportional to the font size, it is recommended to use the [`rem`](/framework/application/font-config.md#rem-字号单位) length unit, such as `0.15rem`.
:::



#### `color`


Set `progress-arc` to highlight the color of the progress bar. By default, the system theme color will be used.


#### `background-color`


Set the color of the `progress-arc` background progress bar, which will be configured according to the system theme by default.


### CSS pseudo-elements


#### `value`
