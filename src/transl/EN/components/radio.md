# radio

Radio buttons are inline elements by default and are commonly used in a **radio group**, which contains a set of radio buttons describing a series of related options. Only one radio button in the group can be selected at any given time. Radio buttons are usually rendered as small circles that are filled to highlight when selected.

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

This attribute indicates whether the radio button is checked. Setting the `checked` attribute can toggle the checked state of the radio button: a value of `true` displays it as checked.

When the user clicks the radio button and causes its checked state to change, the `checked` event is triggered.

::: tip
Manipulating the `checked` attribute directly is not the recommended way to use `radio`. Please use the [radio group](#group) approach instead.
:::

### `value` <decl type="any" get set />

A JavaScript value that identifies the value of the radio button, typically a string or a number. This value is not displayed, but it can be used within a [radio group](#group).

### `group` <decl type="any" get set listen />

If there are multiple related `radio` components, you can combine the `group` and `value` attributes. Radio buttons within the same group are mutually exclusive: the reactive property value bound to `group` is equal to the `value` attribute of the selected radio button. For example:
``` html
<radio value="red" model:group="color" />
<radio value="blue" model:group="color" />
<radio value="yellow" model:group="color" />
```
Here, `color` is a reactive property. When the second radio button is selected, the value of `color` is `"blue"`. If none of the radio buttons' `value` matches `color`, then no radio button will be selected. For example:
``` html
<p on:click="color = null">reset select</p>
```
This will clear the selected state:

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

Radio buttons are inline elements by default. Their display size is determined by the `font-size` CSS property, and they align with the text's baseline. Please do not manually specify properties such as `width` and `height`, as this may cause layout distortion.