# input

Defaults to an inline element, providing an interactive interface to receive user input.

## Attributes

### `type` <decl type="'checkbox' | 'radio'" set />

Can be set to the above value types. The final actual form of the `input` component is determined by the configured type.

### `name` <decl type="string" set />

Sets the name of the `input` component.

### `checked` <decl type="boolean" set />

The current checked state of the component, which can trigger the checked pseudo-class. This takes effect when the type is checkbox. Setting it to `on` makes the checkbox checked by default.

### `value` <decl type="string" set />

Sets the value of the `input` component.