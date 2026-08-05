# input

By default, it is an inline element that provides an interactive interface to receive user input.

## Attributes

### `type` <decl type="'checkbox' | 'radio'" set />

Can be set to the above value types. The actual form of the `input` component is determined based on the set type.

### `name` <decl type="string" set />

Sets the name of the `input` component.

### `checked` <decl type="boolean" set />

The current checked state of the component, which can trigger the checked pseudo-class. This is effective when the type is checkbox. Setting it to `on` checks the checkbox by default.

### `value` <decl type="string" set />

Sets the value of the `input` component.