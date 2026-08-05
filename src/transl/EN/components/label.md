# label

The `label` component is used to display text or tag information, and is an inline element by default. `label` can be used in conjunction with the following form components to display tag information:
- [input](input)
- [radio](radio)
- [switch](switch)
- [checkbox](checkbox)

When a `label` is associated with a supported form component, clicking the `label` component will also trigger a value update for the form component.

## Properties

### `text` <decl type="string" set get />

The text content of the label, supporting either attribute syntax or text child element syntax:
``` html
<label text="label text"></label>
<label>label text</label>
```

### `target` <decl type="string" set get />

The ID of the target component. For example:
```html
<radio id="red" /><label target="red">red</label>
```
Clicking the `label` component in the example will also trigger an update for the `radio` component with the ID `red`, but clicking the `label` component will not trigger touch events such as `click` on the target component.

Due to performance considerations, only target components that are siblings of the `label` component (i.e., sharing the same parent component) are supported.

::: warning
Changing the target component dynamically is currently not supported.
:::