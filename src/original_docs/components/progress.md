# progress

`progress` 组件用于显示进度条，默认为块级元素。

## 属性

### `max` <decl type="number" set />

最大进度值，[`value`](#value) 属性不会大于它。

### `min` <decl type="number" set />

最小进度值，[`value`](#value) 属性不会小于它。

### `value` <decl type="number" set get listen />

设置进度值。进度的显示比例取决于 `value` 属性在 `min` 到 `max` 区间中的比例，同时显示比例会限制在$0\% \sim 100\%$ 之间。`value` 值是一个整数，如果设置浮点值则只会截取整数部分。

### `vertical` <decl type="boolean" set />

如果 `vertical` 属性的值为 `true`，`progress` 组件将会垂直显示，否则水平显示。默认值为 `false`。 

## CSS 规范

开发者可以通过 CSS 来调整 `progress` 组件的外观。

### 尺寸计算

`progress` 默认宽高和元素的字体尺寸一样，字体尺寸由 [`font-size`](/framework/generic/styles.md#font-size) 属性设置（也可以继承而来）。通过 [`width`](/framework/generic/styles.md#width) 和 [`height`](/framework/generic/styles.md#height) 属性可以自定义 `progress` 的尺寸。

### CSS 属性

以下 CSS 属性可能会非常有用：
- [`background-color`](/framework/generic/styles.md#background-color) 可以控制 `progress` 的背景颜色；
- [`color`](/framework/generic/styles.md#color) 可以控制 `progress` 的进度条颜色；
- [`border-radius`](/framework/generic/styles.md#border-radius) 可以将 `progress` 设置为圆角边框，例如 `50%` 会产生半圆边框；

其他的 CSS 属性可能也有用，例如可以使用 [`border`](/framework/generic/styles.md#border) 属性设置边框样式。

### CSS 伪元素

#### `value`

该伪元素可以单独定义 `progress` 进度条而不包含背景部分的样式。例如可以分别设置滚动条背景和进度条部分的圆角半径，以实现外边框具有圆形线冒而进度条则是直线帽的效果。

``` css
progress {
  border-radius: 50%; /* 滚动条背景圆角 */
}

progress::value {
  border-radius: 0; /* 滚动条的进度条没有圆角 */
}
```

### CSS 示例

下面的例子演示了一些通过 CSS 来自定义进度条外观的方法。

<glyphix id="components-progress-styles" height="140" width="480" title="进度条样式">

``` html
<div>
  <!-- 默认样式 -->
  <progress :value="40" />
  <!-- 直头进度条样式 -->
  <progress class="flat" :value="50" />
  <progress class="more-style" :value="60" />
</div>
```

``` css
div > * {
  margin: 8px;
}

.flat::value {
  /* value 伪元素的圆角半径设置为 0 即可实现进度条直头效果 */
  border-radius: 0;
}

.more-style {
  /* 自定义圆角半径 */
  border-radius: 30%;
  /* 进度条背景色 */
  background-color: #b3c5d7;
  /* 进度条前景颜色 */
  color: #b5179e;
  /* padding 可以调整进度条前景的边距 */
  padding: 6px;
  height: 1.25rem;
}
```

</glyphix>
