# p

文本组件。`p` 默认是块级元素，和 [`span`](span) 不同，`p` 组件在设置为行内元素时也不支持文本跨行，如果需要实现富文本排版应考虑使用 `span` 等组件。

## 属性

### `text` <decl type="string" get set/>

设置文本内容，支持如下两种写法。

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

设置文本颜色，只支持十六进制的颜色代码，如 `#f00`，`#e8bb80ff` 等。该属性是修改 CSS 内联属性 [`color`](/framework/generic/styles.md#color) 的一个快捷方式。

### `lines` <decl type="number" get set/>

设置文本的最大行数，超过该行数的文本会被截断或者省略。该属性是修改 CSS 内联属性 [`max-lines`](/framework/generic/styles.md#max-lines) 的一个快捷方式。

### `text-align` <decl type="string" set/>

设置文本对齐方式，支持 `left`、`center`、`right` 等值。该属性是修改 CSS 内联属性 [`text-align`](/framework/generic/styles.md#text-align) 的一个快捷方式。

### `font-size` <decl type="string" set/>

设置文本字体大小，支持 `12px`、`1.5em` 等 CSS 字体大小值。该属性是修改 CSS 内联属性 [`font-size`](/framework/generic/styles.md#font-size) 的一个快捷方式。

### `font-weight` <decl type="number" set/>

设置文本字体字重，目前只支持整数值，如 `400`，`600` 等。该属性是修改 CSS 内联属性 [`font-weight`](/framework/generic/styles.md#font-weight) 的一个快捷方式。

## 使用技巧

### 尺寸控制

一般情况下，不要手动设置 `p` 组件的高度，例如
``` css
p.my-paragraph {
  height: 48px;
  font-size: 32px;
}
```
表面上看，这为 `p` 组件设置了一个大于字体大小的高度，但实际情况是：
- 对于单行文本，某些字体的实际高度可能超过字体大小，即便 `48px` 的高度也可能出现垂直的裁剪。
- 对于多行文本，设置固定高度会导致多行文本被裁剪，无法完整显示。

如果你希望控制文本的显示行数，应使用 [`max-lines`](/framework/generic/styles.md#max-lines) 和 [`text-overflow`](/framework/generic/styles.md#text-overflow) 来实现文本的截断和省略，而不是设置固定高度。

### 文字裁剪动画 <version-badge since="0.9"/>

可以使用 [`width`](/framework/generic/styles.md#width) 属性配合 [`transition`](/framework/component/prop-modifier.md#transition-修饰符) 修饰来实现文字裁剪动画。例如：

``` html
<p :width="state ? 240 : 0"
   width.transition="{duration: 2.0}">
  Hello Glyphix!
</p>
```

配合 `max-lines: 1` 样式可以实现文字从左到右的裁剪动画。但是这个动画存在一个问题：当宽度不足时，最后一个字符会被直接丢弃而不是被裁剪。目前的绕过方法是将文本内容放在一个子组件中，并对父组件设置宽度动画：

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

但是，当使用 `div` 元素作为父组件时，动画会有一个问题：当宽度为 `0` 时，布局尺寸会计算为 `(width: 0, height: 0)`，这会导致该元素无法占据垂直空间，并在动画开始时出现垂直跳动。解决方法是将宽度设置为一个非常小的值（例如 `1px`）而不是 `0`，这样元素就可以占据垂直空间，从而避免跳动问题。
