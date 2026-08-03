# marquee


The `marquee` component is used to display scrolling text content and only supports single-line display. The `marquee` component does not support any subcomponents including `span`.


`marquee` supports common CSS properties, but due to implementation reasons, the `text-align` property may not be supported at this time. Since `marquee` only displays a single line of text and will scroll when the text content is too long, attributes such as `max-lines` also have no effect.


## property


### `text` <decl type="string" get set/>


Set the text content in the same way as the [`text`](p.md#text) attribute of the `p` component. When the length of the text content exceeds the width of `marquee`, the text will automatically scroll.