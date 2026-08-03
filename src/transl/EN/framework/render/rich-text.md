# rich text


When using fluid layout, inline elements such as [`a`](/components/a.md), [`span`](/components/span.md) and [`checkbox`](/components/checkbox.md) can be laid out along the lines and can be broken. The text of components such as `span` can also be laid out across multiple lines. This can be used to achieve rich text display.


## Plain text display


Let's first take a look at how Glyphix displays plain text. The [`p`](/components/a.md) and [`text`](/components/text.md) components can be used for plain text display. Just specify a text string as the `text` attribute of these components:
``` html
<p text="plain text string." />
<text text="plain text string." />
```
Web text nodes are also supported (i.e. the text is a child node of the element):
``` html
<p>plain text string."</p>
<text>plain text string."</text>
```
Glyphix will convert the component's only text child node into a `text` attribute, so the two ways of writing are essentially the same. In other words, as long as the custom component supports the `text` attribute, it can use text subnodes just like the `p` component.


## Rich text display


The `p` and `text` components cannot be used with rich text because they are always a complete box and cannot be laid out across multiple lines. To implement rich text, you first need to have a container with a fluid layout, and then you should use components such as `span` to display the text. For example:
``` html
<div>
  <span>rich&nbsp;</span>
  <span style="color: red">text&nbsp;</span>
  <span>string.</span>
</div>
```
Many components use fluid layout by default, such as `div`, `p`, etc. For simplicity, you can also omit the `<span>` tag:
``` html
<div>
  rich <span style="color: red">text</span> string.
</div>
```
When a component has multiple sub-elements, the text sub-elements will be automatically converted into `span` components.