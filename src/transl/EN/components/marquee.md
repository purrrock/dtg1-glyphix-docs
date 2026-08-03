# marquee

The `marquee` component is used to display scrolling text content and only supports single-line display. The `marquee` component does not support any child components, including `span`.

`marquee` supports general CSS properties, but due to implementation reasons, the `text-align` property may not be supported at the moment. Since `marquee` only displays a single line of text and scrolls it when the content is too long, properties like `max-lines` have no effect.

## Attributes

### `text` <decl type="string" get set/>

Sets the text content, which is used in the same way as the [`text`](p.md#text) attribute of the `p` component. When the length of the text content exceeds the width of the `marquee`, the text will automatically scroll.