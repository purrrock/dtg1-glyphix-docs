# p

Text component. `p` is a block-level element by default. Unlike [`span`](span), the `p` component does not support text wrapping across lines even when set as an inline element. If rich text layout is required, you should consider using components like `span`.

## Properties

### `text` <decl type="string" get set/>

Sets the text content. Supports the following two writing formats:

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

Sets the text color. Only hexadecimal color codes are supported, such as `#f00`, `#e8bb80ff`, etc. This property is a shortcut for modifying the CSS inline property [`color`](/framework/generic/styles.md#color).

### `lines` <decl type="number" get set/>

Sets the maximum number of lines for the text. Text exceeding this number of lines will be truncated or elided. This property is a shortcut for modifying the CSS inline property [`max-lines`](/framework/generic/styles.md#max-lines).

### `text-align` <decl type="string" set/>

Sets the text alignment. Supports values such as `left`, `center`, `right`, etc. This property is a shortcut for modifying the CSS inline property [`text-align`](/framework/generic/styles.md#text-align).

### `font-size` <decl type="string" set/>

Sets the font size of the text. Supports CSS font size values like `12px`, `1.5em`, etc. This property is a shortcut for modifying the CSS inline property [`font-size`](/framework/generic/styles.md#font-size).

### `font-weight` <decl type="number" set/>

Sets the font weight of the text. Currently, only integer values are supported, such as `400`, `600`, etc. This property is a shortcut for modifying the CSS inline property [`font-weight`](/framework/generic/styles.md#font-weight).

## Tips & Tricks

### Size Control

In general, avoid manually setting the height of the `p` component. For example:
``` css
p.my-paragraph {
  height: 48px;
  font-size: 32px;
}
```
On the surface, this sets a height greater than the font size for the `p` component, but in reality:
- For single-line text, the actual height of certain fonts may exceed the font size, and even a height of `48px` may result in vertical clipping.
- For multi-line text, setting a fixed height will cause the multi-line text to be clipped, preventing it from displaying completely.

If you want to control the number of displayed lines of text, you should use [`max-lines`](/framework/generic/styles.md#max-lines) and [`text-overflow`](/framework/generic/styles.md#text-overflow) to achieve text truncation and ellipsis, rather than setting a fixed height.

### Text Clipping Animation <version-badge since="0.9"/>

You can use the [`width`](/framework/generic/styles.md#width) property in combination with the [`transition`](/framework/component/prop-modifier.md#transition-modifier) modifier to create a text clipping animation. For example:

``` html
<p :width="state ? 240 : 0"
   width.transition="{duration: 2.0}">
  Hello Glyphix!
</p>
```

Combined with the `max-lines: 1` style, this can achieve a left-to-right text clipping animation. However, there is an issue with this animation: when the width is insufficient, the last character is directly discarded rather than clipped. The current workaround is to place the text content inside a child component and apply the width animation to the parent component:

``` html
<div :width="state ? 240 : 1"
     width.transition="{duration: 2.0}">
  <p style="max-lines: 1">Hello Glyphix!</p>
</div>
```

<glyphix id="p-width-transition" title="Text Clipping Animation" height="120">

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

However, when using a `div` element as the parent component, the animation has a side effect: when the width is `0`, the layout size is computed as `(width: 0, height: 0)`, which causes the element to occupy no vertical space and results in a vertical jump at the start of the animation. The solution is to set the width to a very small value (such as `1px`) instead of `0`, allowing the element to occupy vertical space and thus avoiding the jumping issue.