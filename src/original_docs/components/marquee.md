# marquee

`marquee` 组件用于显示滚动的文本内容，只支持单行显示。`marquee` 组件不支持包括 `span` 在内的任何子组件。

`marquee` 支持通用的 CSS 属性，但是由于实现的原因，现在可能不支持 `text-align` 属性。由于 `marquee` 只显示单行文本，并会在文本内容超长时滚动显示，`max-lines` 等属性也均不起作用。

## 属性

### `text` <decl type="string" get set/>

设置文本内容，和 `p` 组件的 [`text`](p.md#text) 属性用法相同。当文本内容的长度超过 `marquee` 的宽度时，文本会自动滚动显示。
