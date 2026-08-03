# Rich Text

When using a flow layout, inline elements such as [`a`](/components/a.md), [`span`](/components/span.md), and [`checkbox`](/components/checkbox.md) can be laid out along lines and can wrap. The text of components like `span` can even span multiple lines, which can be used to implement rich text display.

## Plain Text Display

Let's first look at how Glyphix displays plain text. The [`p`](/components/a.md) and [`text`](/components/text.md) components can be used for plain text display. You simply need to specify the text string as the `text` property of these components:
``` html
<p text="plain text string." />
<text text="plain text string." />
```
Web-style text nodes (where the text is a child node of the element) are also supported:
``` html
<p>plain text string."</p>
<text>plain text string."</text>
```
Glyphix converts the single text child node of a component into the `text` property, so these two syntaxes are essentially identical. In other words, as long as a custom component supports the `text` property, it can use text child nodes just like the `p` component.

## Rich Text Display

The `p` and `text` components cannot be used for rich text because they always form a complete box and cannot wrap across multiple lines. To implement rich text, you first need a container with a flow layout, and then use components such as `span` to display the text. For example:
``` html
<div>
  <span>rich&nbsp;</span>
  <span style="color: red">text&nbsp;</span>
  <span>string.</span>
</div>
```
Many components use a flow layout by default, such as `div`, `p`, etc. For simplicity, the `<span>` tags can also be omitted:
``` html
<div>
  rich <span style="color: red">text</span> string.
</div>
```
When a component has multiple child elements, any text child elements among them will be automatically converted into `span` components.