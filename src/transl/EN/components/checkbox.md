# checkbox

The `checkbox` element displays a checked box when activated, indicating that an item has been selected.

<glyphix id="checkbox-1" :height="65" title="Single Checkbox">

``` html
<div>
  <checkbox id="checkbox" ::checked="checked" />
  <label target="checkbox">Check me!</label>
  <p>checked: {{ checked }}</p>
</div>
```

``` js
export default {
  data: {
    checked: true
  }
}
```
</glyphix>

::: note
A `checkbox` is typically a square that can be checked, but the exact appearance depends on the device. Developers currently cannot modify the color and other styles of a `checkbox` via CSS.
:::

## Properties

### `checked` <decl type="boolean" get set listen />

This property indicates whether the checkbox is selected. Setting the `checked` property toggles the selection state of the checkbox: when the value is `true`, it appears in the checked state. Two-way binding can also be used to operate on a single checkbox:
``` html
<checkbox model:checked="yes" />
```

The earlier example in this article demonstrates the usage of this binding. Please note not to bind to the [`value`](#value) property, but to `checked`.

Events are triggered only when the user clicks the checkbox, causing the `checked` property to change.

::: warning
Do not set the `checked` property in a [checkbox group](#group) to avoid confusion.
:::

### `value` <decl type="any" get set />

A JavaScript value that identifies the checkbox value, typically a string or a number. This value is not displayed, but it can be used in [group operations](#group).

### `group` <decl type="any[]" get set listen />

If there are multiple associated `checkbox` components, you can combine the `group` and `value` properties; checkboxes within the same group will form an array of selected values. Please refer to the example below:

<glyphix id="checkbox-group" :height="65" title="Checkbox Group" >

``` html
<div>
  <p>selected colors: {{selected.join(', ')}}</p>
  <div>
    <checkbox id="red" value="red" model:group="selected" />
    <label target="red">red</label>
    <checkbox id="blue" value="blue" model:group="selected" />
    <label target="blue">blue</label>
    <checkbox id="yellow" value="yellow" model:group="selected" />
    <label target="yellow">yellow</label>
  </div>
</div>
```

``` js
export default {
  data: {
    selected: ['yellow']
  }
}
```

``` css
label {
  margin-right: 0.5rem;
}
```

</glyphix>

This can be achieved by using `model:group` or `::group` to two-way bind the `group` property to a reactive array (`selected` in the example):
- After the user interacts with a checkbox in the group, the value of the reactive array is updated;
- Changes to the elements of the reactive array are reflected in the appearance of the `checkbox`.

As shown in the example above: in the initial state, the selection status of grouped checkboxes is determined by the value of the `group` property. Specifically, for a checkbox such as:
``` html
<checkbox value="red" model:group="selected" />
```
Since the `value` property specifies `"red"`, when the value of the reactive property `selected` contains `"red"` (e.g., `["red"]`), the checkbox will be checked. Clicking the checkbox again causes it to become unchecked, and the `"red"` element is removed from the `selected` array.

::: tip
If you do not want to group checkboxes, you can use the [`checked`](#checked) property to operate them individually. However, do not use `checked` and `group` at the same time; Glyphix does not account for this scenario.
:::

### `indeterminate` <decl type="boolean" get set />

The `indeterminate` property indicates that the checkbox is in an **indeterminate** state. When this property is `true`, the checkbox displays a horizontal line resembling a minus sign in the middle, indicating that its state is uncertain.

The indeterminate state can be used when an item has multiple sub-items: if all sub-items are checked, the parent is also checked; if all are unchecked, the parent is also unchecked. If some sub-items are checked, the parent will be in an indeterminate state.

The example below demonstrates this usage. This example shows an inventory for crafting an enchanting table; when you select some of the recipes, the "Enchantment table" checkbox enters a partially checked state. As you can see, this example allows you to use the parent checkbox to select or deselect all sub-items.

<glyphix id="checkbox-indeterminate" :height="140" title="Tri-state Checkbox" >

``` html
<div>
  <div>
    <!--
      When selected.length == 3, entirety is checked; otherwise:
      - If selected.length == 0, it is unchecked;
      - Otherwise, it means some recipes are selected, so it is in the indeterminate state. 
      -->
    <checkbox id="entirety"
              :indeterminate="selected.length && selected.length < 3"
              :checked="selected.length == 3"
              on:checked="selectEntirety" />
    <label target="entirety">
      &nbsp;Enchantment table:
    </label>
  </div>
  <div class="group">
    <div for="x in parts">
      •
      <checkbox :id="x" :value="x" model:group="selected" />
      <label :target="x">&nbsp;{{x}}</label>
    </div>
  </div>
</div>
```

``` js
export default {
  data: {
    selected: ['Diamonds'],
  },
  parts: ['Book', 'Diamonds', 'Obsidian'],
  // Called when clicking the entirety checkbox to set the selection state of all recipes
  selectEntirety(status) {
    // Use [...this.parts] to copy the list to avoid mutating in place
    this.selected = status ? [...this.parts] : []
  },
}
```

``` css
.group {
  margin-left: 0.4rem;
}
```

</glyphix>

::: tip
When the `checked` property is set (note: not cleared), the `indeterminate` property is automatically cleared. Even if the checkbox has both properties, it will display as checked rather than indeterminate.
:::

### CSS Behavior

Checkboxes are inline elements by default. Their display size is determined by the `font-size` CSS property and they align with the text baseline. Please do not manually specify properties like `width` and `height`, as this may cause rendering issues.