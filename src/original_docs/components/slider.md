# slider

滑动选择器，默认为块级元素。

## 属性

### `value` <decl type="number" get set listen />

当前值，默认值：$10$。

设置 `value` 属性时，将会改变组件的当前值。可以通过 `on` 指令监听当前值的改变，每次当前值改变都会被触发。

### `min` <decl type="number" set />

最小值，默认值：$0$。

### `max` <decl type="number" set />

最大值，默认值：$100$。

### `vertical` <decl type="boolean" set />

如果 `vertical` 属性的值为 `true`，`slider` 组件将会垂直显示，否则水平显示。默认值为 `false`。 

## CSS 规范

开发者可以通过 CSS 来调整 `slider` 组件的外观。

### 尺寸计算

`slider` 默认宽高和元素的字体尺寸一样，字体尺寸由 [`font-size`](/framework/generic/styles.md#font-size) 属性设置（也可以继承而来）。通过 [`width`](/framework/generic/styles.md#width) 和 [`height`](/framework/generic/styles.md#height) 属性可以自定义 `progress` 的尺寸。

### CSS 属性

以下 CSS 属性可能会非常有用：
- [`background-color`](/framework/generic/styles.md#background-color) 可以控制 `slider` 的背景颜色；
- [`color`](/framework/generic/styles.md#color) 可以控制 `slider` 的进度条颜色；
- [`border-radius`](/framework/generic/styles.md#border-radius) 可以将 `slider` 设置为圆角边框，例如 `50%` 会产生半圆边框；

其他的 CSS 属性可能也有用，例如可以使用 [`border`](/framework/generic/styles.md#border) 属性设置边框样式。

### CSS 伪元素

#### `value`

该伪元素可以单独定义 `slider` 进度条而不包含背景部分的样式。例如可以分别设置滚动条背景和进度条部分的圆角半径，以实现外边框具有圆形线冒而进度条则是直线帽的效果。

``` css
slider {
  border-radius: 50%; /* 滚动条背景圆角 */
}

slider::value {
  border-radius: 0; /* 滚动条的进度条没有圆角 */
}
```

#### `thumb` <experimental/>

`thumb` 伪元素用于定义 `slider` 滑块的样式。默认情况下 `slider` 不包含手柄，要想显示手柄必须指定 `thumb` 元素的宽度和高度：
``` css
slider::thumb {
  width: 150%;
  height: 150%;
  border-radius: 50%;
}
```
百分比单位的 `width` 和 `height` 是相对于元素本身的尺寸计算的，水平 `slider` 的滑块宽高根据元素 CSS 的 `height` 计算百分比，而垂直 `slider` 的手柄宽高根据元素 CSS 的 `width` 属性计算百分比。例如元素 CSS 为
``` css
slider {
  width: 200px;
  height: 24px;
}
```
此时上面的 `slider::thumb` 对应的滑块宽度和高度都是 $24\rm{px} \times 150\% = 36\rm{px}$。而手柄的圆角半径百分比尺寸则是根据手柄自己的尺寸来计算的，本例子中 `50%` 的 `thumb` 伪元素圆角半径计算值为 $36\rm{px} \times 50\%=18\rm{px}$。

`thumb` 伪元素支持 `border` CSS 属性，不过边框不会超出 `thumb` 伪元素的尺寸。

### CSS 示例

下面的例子演示了一些通过 CSS 来自定义进度条外观的方法。
<glyphix id="components-slider-styles" height="180" width="480" title="Slider 样式">

``` html
<div>
  <!-- 默认样式 -->
  <slider ::value="value" />
  <!-- 直头进度条样式 -->
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
  /* value 伪元素的圆角半径设置为 0 即可实现进度条直头效果 */
  border-radius: 0;
}

.more-style {
  /* 自定义圆角半径 */
  border-radius: 30%;
  /* slider 背景色 */
  background-color: #b3c5d7;
  /* slider 前景颜色 */
  color: #b5179e;
  /* padding 可以调整 slider 前景的边距 */
  padding: 6px;
  height: 1rem;
}

/* 定义滚动条滑块样式 */
.more-style::thumb {
  width: 300%; /* 宽高比 2:1 的胶囊形滑块 */
  height: 150%;
  background-color: white;
  border: 4px solid #f3722c; /* 滑块边框 */
  border-radius: 50%;
}
```

``` js
export default {
  data: { value: 50 }
}
```

</glyphix>
