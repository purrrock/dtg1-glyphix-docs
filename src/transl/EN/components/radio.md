# radio

Radio buttons are inline elements by default, commonly used in a **radio group**, which contains a set of radio buttons describing a series of related options. Only one radio button in the group can be selected at a time. Radio buttons are usually presented as small circles that are filled and highlighted when selected.

<glyphix id="radio-1" :height="65" title="Radio Button">

``` html
<div>
  <p>picked color: {{color}}</p>
  <div>
    <radio id="red" value="red" model:group="color" />
    <label target="red">red</label>
    <radio id="blue" value="blue" model:group="color" />
    <label target="blue">blue</label>
    <radio id="yellow" value="yellow" model:group="color" />
    <label target="yellow">yellow</label>
  </div>
</div>
```

``` js
export default {
  data: {
    color: 'blue'
  }
}
```

``` css
label {
  margin-right: 0.5rem;
}
```

</glyphix>

::: tip
Radio buttons are somewhat similar to [`checkbox`](checkbox.md), but a `radio` only allows selecting a single value from a group, whereas a `checkbox` allows selecting multiple values.
:::

## Attributes

### `checked` <decl type="boolean" get set listen />

This attribute indicates whether the radio button is checked. Setting the `checked` attribute toggles the selection state of the radio button: when the value is `true`, it is displayed as checked.

When the user clicks the radio button and causes its selection state to change, the `checked` event is triggered.

::: tip
Manipulating the `checked` attribute is not the recommended way to use `radio`; please use the [radio group](#group) method instead.
:::

### `value` <decl type="any" get set />

A JavaScript value that identifies the value of the radio button, typically a string or a number. This value is not displayed, but it can be used within a [radio group](#group).

### `group` <decl type="any" get set listen />

If there are multiple related `radio` components, you can combine the `group` and `value` attributes. Radio buttons in the same group are mutually exclusive: the value of the reactive property bound to `group` equals the `value` attribute of the currently selected radio button. For example:
``` html
<radio value="red" model:group="color" />
<radio value="blue" model:group="color" />
<radio value="yellow" model:group="color" />
```
Here, `color` is a reactive property. When the second radio button is selected, the value of `color` is `"blue"`. If the `value` of all radio buttons does not match `color`, no radio button will be selected. For example:
``` html
<p on:click="color = null">reset select</p>
```
This will clear the selection state:

<glyphix id="radio-reset" :height="65" title="Clear Selection State">

``` html
<div>
  <p on:click="color = null">picked color: {{color}} (click to reset)</p>
  <div>
    <radio id="red" value="red" model:group="color" />
    <label target="red">red</label>
    <radio id="blue" value="blue" model:group="color" />
    <label target="blue">blue</label>
    <radio id="yellow" value="yellow" model:group="color" />
    <label target="yellow">yellow</label>
  </div>
</div>
```

``` js
export default {
  data: {
    color: 'blue'
  }
}
```

``` css
label {
  margin-right: 0.5rem;
}
```

</glyphix>

### CSS Behavior

Radio buttons are inline elements by default. Their display size is determined by the `font-size` CSS property, and they align with the text baseline. Please do not manually specify properties like `width` and `height`, as this may cause layout distortion.