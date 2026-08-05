# switch

The switch selection component, which is an inline element by default. It is used to represent two states (on/off) and allows the user to toggle between them. The function of `switch` is similar to `checkbox`, but their interaction effects and intents are different, representing switches and checkboxes respectively.

<glyphix id="components-switch" height="30">

``` html
<div>
  <switch ::value="enabled" />
  <span>switch state: {{ enabled ? 'on' : 'off' }}</span>
</div>
```

``` js
export default {
  data: {
    enabled: false
  }
}
```
</glyphix>

::: note
The style of the `switch` component is usually as shown in the example, but it may vary depending on the device. In particular, the width of the `switch` may differ across devices, and developers should reserve appropriate layout margins.
:::

## Attributes

### `value` <decl type="boolean" set get listen/>

Represents the state of the `switch`. When the value is `true`, the `switch` is in the on state; otherwise, it is in the off state. When the `value` attribute is not specified, the `switch` component is off by default.

### `checked` <decl type="boolean" set get/>

This is a Quick App compatibility attribute. Using [`value`](#value) is generally recommended instead.

### `change` <decl type="{ checked: boolean }" get listen/>

This is a Quick App compatibility attribute. Using [`value`](#value) is generally recommended instead.

## CSS Behavior

The overall style of the `switch` component is determined by the system and is not controlled by the developer, much like the style differences between [Fluent 2](https://fluent2.microsoft.design/components/web/react/switch/usage) and [Material 3](https://m3.material.io/components/switch/overview). Glyphix allows customizing the color of the `switch` in CSS and adjusting its size.

### CSS Properties

#### `color`

Sets the thumb color of the `switch` component. Unlike general CSS [`color`](/framework/generic/styles.md#color), the `color` property of the `switch` does not support inheritance, so you must define it directly on the current `switch` component.

<glyphix id="components-switch-color" height="36" title="switch thumb color">

``` html
<div>
  red color: <switch class="red"/>,
  not inherited: <switch/>
</div>
```

``` css
div {
  color: red; /* Note that switch does not inherit the color property */
}

.red {
  color: red; /* color must be defined on the switch component's style */
}
```
</glyphix>

#### `background-color`

Controls the background color of the `switch` component. For details, refer to the documentation for the [`active`](#active) pseudo-class. 

#### `font-size`

You can adjust the size of the `switch` using the [`font-size`](/framework/generic/styles.md#font-size) CSS property so that it harmonizes with inline text sizes. The following example demonstrates the relationship between `font-size` and the `switch` size:

<glyphix id="components-switch-size" height="100" title="font-size and switch size">

``` html
<div>
  <p class="title">
    title text: <switch/> (1.25rem)
  </p>
  <p>
    content text: <switch/> (1rem)
  </p>
</div>
```

``` css
div {
  line-height: 1.8rem;
}

.title {
  color: #415a77; /* Note that switch does not inherit the color property */
  font-size: 1.25rem;
}
```
</glyphix>

::: warning
The display size of the `switch` is not controlled by properties such as `width` and `height`, but is always determined by `font-size`. Therefore, please do not manually specify dimension properties like `width` to avoid abnormal rendering.
:::

### CSS Pseudo-classes

#### `active`

The `active` pseudo-class is used to define the style of the `switch` when it is in the on state. As shown in the example below, it is usually configured alongside regular style rules:

<glyphix id="components-switch-colors" height="36" title="switch thumb color settings">

``` html
<div>
  color switch: <switch/>
</div>
```

``` css
/* Style when the switch is off */
switch {
  color: #415a77;
  background-color: #bde0fe;
}

/* Style when the switch is on */
switch:active {
  color: #fefae0;
  background-color: #ffafcc;
}
```
</glyphix>

This example controls the color style of the `switch` during toggling via the `color` and `background-color` CSS properties. The `switch` component will only respond to the configuration of these two CSS properties when the `active` pseudo-class is activated.

::: tip
Please define the `color` and `background-color` properties for both the normal and `active` states; otherwise, the `switch` will not transition colors accordingly when toggled.
:::