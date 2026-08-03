# slider


Sliding selector, defaults to block-level elements.


## property


### `value` <decl type="number" get set listen />


Current value, default: $10$.


When setting the `value` attribute, the current value of the component will be changed. You can monitor changes in the current value through the `on` instruction, which will be triggered every time the current value changes.


### `min` <decl type="number" set />


Minimum value, default value: $0$.


### `max` <decl type="number" set />


Maximum value, default value: $100$.


### `vertical` <decl type="boolean" set />


If the value of the `vertical` attribute is `true`, the `slider` component will be displayed vertically, otherwise it will be displayed horizontally. The default value is `false`.


## CSS specifications


Developers can adjust the appearance of the `slider` component through CSS.


### Size calculation


The default width and height of `slider` are the same as the element's font size, which is set by the [`font-size`](/framework/generic/styles.md#font-size) attribute (can also be inherited). The size of `progress` can be customized through the [`width`](/framework/generic/styles.md#width) and [`height`](/framework/generic/styles.md#height) attributes.


### CSS properties


The following CSS properties may be useful:
- [`background-color`](/framework/generic/styles.md#background-color) can control the background color of `slider`;
- [`color`](/framework/generic/styles.md#color) can control the color of the progress bar of `slider`;
- [`border-radius`](/framework/generic/styles.md#border-radius) can set `slider` to a rounded border, for example `50%` will produce a semicircular border;


Other CSS properties may be useful, such as the [`border`](/framework/generic/styles.md#border) property to style the border.


### CSS pseudo-elements


#### `value`


This pseudo-element can define the `slider` progress bar alone without containing the style of the background part. For example, you can set the corner radius of the scroll bar background and the progress bar part separately to achieve the effect that the outer border has a circular line cap and the progress bar has a straight cap.


``` css
slider {
  border-radius: 50%; /* 滚动条背景圆角 */
}

slider::value {
  border-radius: 0; /* 滚动条的进度条没有圆角 */
}
```


#### `thumb` <experimental/>


The `thumb` pseudo-element is used to define the style of the `slider` slider. By default `slider` does not contain handles. To display handles you must specify the width and height of the `thumb` element:
``` css
slider::thumb {
  width: 150%;
  height: 150%;
  border-radius: 50%;
}
```
The percentage units of `width` and `height` are calculated relative to the size of the element itself. The horizontal `slider` slider width and height are calculated as a percentage based on the `height` of the element's CSS, while the vertical `slider` handle width and height are calculated as a percentage based on the `width` attribute of the element's CSS. For example, the element CSS is
``` css
slider {
  width: 200px;
  height: 24px;
}
```
At this time, the width and height of the slider corresponding to `slider::thumb` above are both $24\rm{px} \times 150\% = 36\rm{px}$. The handle's fillet radius percentage size is calculated based on the handle's own size. In this example, the calculated value of the `50%` pseudo-element fillet radius of `thumb` is $36\rm{px} \times 50\%=18\rm{px}$.


The `thumb` pseudo-element supports the `border` CSS property, but the border will not exceed the dimensions of the `thumb` pseudo-element.


### CSS example


The following example demonstrates some ways to customize the appearance of the progress bar through CSS.
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
