# label


The `label` component is used to display text or markup information, and is an inline element by default. `label` can display mark information with the following form components:
- [input](input)
- [radio](radio)
- [switch](switch)
- [checkbox](checkbox)


When `label` is associated with a supported form component, clicking the `label` component will also trigger the value update of the form component.


## property


### `text` <decl type="string" set get />


The text content of the label supports attribute syntax or text subelement syntax:
``` html
<label text="label text"></label>
<label>label text</label>
```


### `target` <decl type="string" set get />


The ID of the target component. For example:
```html
<radio id="red" /><label target="red">red</label>
```
Clicking on the `label` component in the example will also trigger the update of the `radio` component with ID `red`, but clicking on the `label` component will not trigger touch events such as `click` on the target component.


Considering performance issues, only target components that are at the same level as the `label` component (i.e. have the same parent component) are supported.


::: warning

Changing the target component is not currently supported.
:::
