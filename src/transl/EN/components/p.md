# p


Text component. `p` is a block-level element by default. Unlike [`span`](span), the `p` component does not support text crossing lines when set as an inline element. If you need to implement rich text typesetting, you should consider using components such as `span`.


## property


### `text` <decl type="string" get set/>


Set text content and support the following two writing methods.


``` html
<p text="Hello Glyphix"></p>
<p>Hello Glyphix</p>
```


<glyphix id="p" :height="70" inline>



``` html
<div>
  <p text="Hello Glyphix"></p>
  <p>Hello Glyphix</p>
</div>
```


</glyphix>



### `color` <decl type="string" get set/>


Set text color. Only hexadecimal color codes are supported, such as `#f00`, `#e8bb80ff`, etc. This property is a shortcut for modifying the CSS inline property [`color`](/framework/generic/styles.md#color).


### `lines` <decl type="number" get set/>


Set the maximum number of lines of text. Text exceeding this number will be truncated or omitted. This property is a shortcut for modifying the CSS inline property [`max-lines`](/framework/generic/styles.md#max-lines).


### `text-align` <decl type="string" set/>


Set the text alignment, supporting `left`, `center`, `right` and other values. This property is a shortcut for modifying the CSS inline property [`text-align`](/framework/generic/styles.md#text-align).


### `font-size` <decl type="string" set/>


Set the text font size, supporting `12px`, `1.5em` and other CSS font size values. This property is a shortcut for modifying the CSS inline property [`font-size`](/framework/generic/styles.md#font-size).


### `font-weight` <decl type="number" set/>


Set the text font weight. Currently, only integer values ​​are supported, such as `400`, `600`, etc. This property is a shortcut for modifying the CSS inline property [`font-weight`](/framework/generic/styles.md#font-weight).


## Tips


### size control


In general, do not manually set the height of the `p` component, e.g.
``` css
p.my-paragraph {
  height: 48px;
  font-size: 32px;
}
```
On the face of it, this sets a height for the `p` component that is larger than the font size, but what happens is:
- For single-line text, the actual height of some fonts may exceed the font size, and even heights of `48px` may appear vertically clipped.
- For multi-line text, setting a fixed height will cause the multi-line text to be cropped and cannot be displayed completely.


If you wish to control the number of lines of text displayed, you should use [`max-lines`](/framework/generic/styles.md#max-lines) and [`text-overflow`](/framework/generic/styles.md#text-overflow) to implement text truncation and omission instead of setting a fixed height.


### Text clipping animation <version-badge since="0.9"/>


You can use the [`width`](/framework/generic/styles.md#width) attribute with the [`transition`](/framework/component/prop-modifier.md#transition-修饰符) modification to implement text clipping animation. For example:


``` html
<p :width="state ? 240 : 0"
   width.transition="{duration: 2.0}">
  Hello Glyphix!
</p>
```


With the `max-lines: 1` style, you can achieve text cropping animation from left to right. But there is a problem with this animation: when the width is insufficient, the last character will be discarded instead of being cropped. The current workaround is to put the text content in a child component and animate the width of the parent component:


``` html
<div :width="state ? 240 : 1"
     width.transition="{duration: 2.0}">
  <p style="max-lines: 1">Hello Glyphix!</p>
</div>
```


<glyphix id="p-width-transition" title="文字裁剪动画" height="120">


``` html
<div class="container">
  <p class="animated-text"
     :width="state ? 240 : 0"
     width.transition="{duration: 2.0}">
    Hello Glyphix!
  </p>
  <div class="animated-text"
       :width="state ? 240 : 1"
       width.transition="{duration: 2.0}">
    <p>Hello Glyphix!</p>
  </div>
</div>
```


``` js
export default {
  data: {
    state: false
  },
  onReady() {
    setInterval(() => this.state = !this.state, 2500)
  }
}
```


```css
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.animated-text {
  margin: 4px;
  border: 1px solid #f00;
}

p {
  max-lines: 1;
  text-overflow: clip;
}
````


</glyphix>



However, when using a `div` element as a parent component, there is a problem with the animation: when the width is `0`, the layout size is calculated as `(width: 0, height: 0)`, which causes the element to be unable to occupy the vertical space and vertical jumps at the beginning of the animation. The solution is to set the width to a very small value (e.g. `1px` ) instead of `0` so that the element can occupy the vertical space and thus avoid the bounce problem.