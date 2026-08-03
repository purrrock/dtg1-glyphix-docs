# progress-arc

`progress-arc` 组件用于显示环形进度条，默认为块级元素。

## 属性

### `max` <decl type="number" set />

最大进度值，[`value`](#value) 属性不会大于它。

### `min` <decl type="number" get setet />

最小进度值，[`value`](#value) 属性不会小于它。

### `value` <decl type="number" get set listen />

设置进度值。进度的显示比例取决于 `value` 属性在 `min` 到 `max` 区间中的比例，同时显示比例会限制在$0\% \sim 100\%$ 之间。`value` 值是一个整数，如果设置浮点值则只会截取整数部分。

### `busy` <decl type="boolean" get set />

设置 `progress-arc` 组件是否处于忙状态，在忙状态下会显示一个加载动画，而不是显示 `value` 属性的值。下面的示例演示了如何用一个圆形进度条来模拟加载动画：

<glyphix id="components-progress-arc-busy" height="100" width="300" title="模拟加载动画">

``` html
<progress-arc busy :startAngle="0" :stopAngle="360" />
```

</glyphix>

在这个例子中，进度条的开始角度和结束角度相差 $360^\circ$，此时通过 `busy` 属性可以显示典型的加载动画效果。

::: tip
只要进度条为环形就会显示固定的忙动画效果，起始和结束角度并没有影响。
:::

### `startAngle` <decl type="number" get set />

弧形进度条的起始角度，默认值为 $135$，更多的信息请参考[角度配置](#角度配置)章节。

### `stopAngle` <decl type="number" get set />

弧形进度条的结束角度，默认值为 $405$，更多的信息请参考[角度配置](#角度配置)章节。

## 使用说明

### 角度配置

与线性的 [`progress`](progress.md) 不同，弧形或者环形的进度条需要合理配置 `startAngle` 属性和 `stopAngle` 属性才能正常显示。这两个属性均使用角度制单位，在屏幕坐标系中，$0^\circ$ 指向水平向右的方向，即时钟 $3$ 点钟方向，并沿着顺时针方向增加，反之减小。

`progress-arc` 的显示是根据 `value` 在 $[\texttt{min}, \texttt{max}]$ 中的比例对角度范围进行线性插值。具体而言，用户会看到进度的高亮角度从 `startAngle` 开始，并到 `valueAngle` 结束：

$$
\begin{aligned}
  k &= \frac{\texttt{value} - \texttt{min}}{\texttt{max}-\texttt{min}}\\
  \texttt{valueAngle} &= (1-k)\texttt{startAngle} + k\cdot\texttt{stopAngle}
\end{aligned}
$$

因此，如果要显示一整圈的环形进度条，需要让起始和结束角度相差 $360^\circ$，即使这两个角度从视觉上来看是相同的。另外，起始角度也可以大于结束角度，这将反转进度的方向。

下面的示例展示了多种角度配置的实际效果，请注意第二个示例展示了反向的进度显示技巧。

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

## CSS 规范

### 尺寸计算

`progress-arc` 的显示尺寸由它的 `width` 和 `height` 属性决定。`progress-arc` 会占满较短的轴线，且弧形进度条的圆心为元素的中心。默认情况下，`progress-arc` 的尺寸可能和一个字符接近，这会导致非常怪异的显示效果，因此通常要在 CSS 中显式指定宽高，或使用其他合理的布局策略。

::: tip
最好为 `progress-arc` 组件指定一个合理的宽度和高度，否则它可能无法辨认。至少也应该设置 `width` CSS 属性，该组件的布局策略会自动使用 $1:1$ 宽高比。
:::

### CSS 属性

可以通过 CSS 来调整 `progress-arc` 组件的外观。

#### `stroke-width`

该属性指定 `progress-arc` 组件的弧形轮廓宽度。值类型为[长度](/framework/render/style-and-layout.md#长度)，不支持百分比单位。

::: tip
如果你希望 `progress-arc` 组件的绘制宽度和字体尺寸成一定的比例，建议使用 [`rem`](/framework/application/font-config.md#rem-字号单位) 长度单位，如 `0.15rem`。
:::

#### `color`

设置 `progress-arc` 高亮进度条的颜色，默认情况下会使用系统主题色。

#### `background-color`

设置 `progress-arc` 背景进度条的颜色，默认情况下会根据系统主题配置。

### CSS 伪元素

#### `value`

