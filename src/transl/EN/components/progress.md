# progress


The `progress` component is used to display the progress bar and defaults to a block-level element.


## property


### `max` <decl type="number" set />


The maximum progress value that the [`value`](#value) attribute will not be greater than.


### `min` <decl type="number" set />


The minimum progress value that the [`value`](#value) attribute will not be less than.


### `value` <decl type="number" set get listen />


Set the progress value. The display ratio of the progress depends on the ratio of the `value` attribute in the interval from `min` to `max`, and the display ratio will be limited to $0\% \sim 100\%$. The `value` value is an integer. If a floating point value is set, only the integer part will be truncated.


### `vertical` <decl type="boolean" set />


If the value of the `vertical` attribute is `true`, the `progress` component will be displayed vertically, otherwise it will be displayed horizontally. The default value is `false`.


## CSS specifications


Developers can adjust the appearance of the `progress` component through CSS.


### Size calculation


The default width and height of `progress` are the same as the element's font size, which is set by the [`font-size`](/framework/generic/styles.md#font-size) attribute (can also be inherited). The size of `progress` can be customized through the [`width`](/framework/generic/styles.md#width) and [`height`](/framework/generic/styles.md#height) attributes.


### CSS properties


The following CSS properties may be useful:
- [`background-color`](/framework/generic/styles.md#background-color) can control the background color of `progress`;
- [`color`](/framework/generic/styles.md#color) can control the color of the progress bar of `progress`;
- [`border-radius`](/framework/generic/styles.md#border-radius) can set `progress` to a rounded border, for example `50%` will produce a semicircular border;


Other CSS properties may be useful, such as the [`border`](/framework/generic/styles.md#border) property to style the border.


### CSS pseudo-elements


#### `value`


This pseudo-element can define the `progress` progress bar alone without containing the style of the background part. For example, you can set the corner radius of the scroll bar background and the progress bar part separately to achieve the effect that the outer border has a circular line cap and the progress bar has a straight cap.


``` css
progress {
  border-radius: 50%; /* 滚动条背景圆角 */
}

progress::value {
  border-radius: 0; /* 滚动条的进度条没有圆角 */
}
```


### CSS example


The following example demonstrates some ways to customize the appearance of the progress bar through CSS.


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
