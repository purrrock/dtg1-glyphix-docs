# checkbox


The `checkbox` (checkbox) element displays a checked (tickled) box when activated, indicating that an item is selected.


<glyphix id="checkbox-1" :height="65" title="单个复选框">


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

`checkbox` is usually a square that can be ticked, but the exact effect depends on the device. Developers currently cannot modify the color and other styles of `checkbox` through CSS.
:::



## property


### `checked` <decl type="boolean" get set listen />


This property indicates whether this check box is selected. Setting the `checked` attribute can switch the selected state of the check box: when the value is `true`, it is displayed in the selected state. You can also operate on individual checkboxes via two-way binding:
``` html
<checkbox model:checked="yes" />
```


The example earlier in this article demonstrates the use of this binding, please note that you do not bind to the [`value`](#value) attribute, but to `checked`.


The event is only fired when the user clicks on the checkbox, causing the `checked` attribute to change.


::: warning

Do not set the `checked` attribute in [复选框组](#group) to avoid confusion.
:::



### `value` <decl type="any" get set />


A JavaScript value that identifies the checkbox value, usually a string or number. This value is not displayed, but it can be used in [分组操作](#group).


### `group` <decl type="any[]" get set listen />


If you have multiple associated `checkbox` components, you can combine the `group` and `value` attributes; checkboxes within the same group form an array of selected values. Please refer to the following example:


<glyphix id="checkbox-group" :height="65" title="复选框组" >


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



This can be achieved by bidirectionally binding the `group` attribute to a reactive array (`selected` in the example) using `model:group` or `::group`:
- When the user operates a checkbox in the group, the value of the responsive array will be updated;
- When the elements of the reactive array change, it will be reflected in the performance of `checkbox`.


As shown in the example above: In the initial state, the grouping checkbox is selected based on the value of the `group` attribute. Specifically, for a checkbox like:
``` html
<checkbox value="red" model:group="selected" />
```
Since the `value` attribute specifies the `"red"` value, the checkbox will be checked when the value of the reactive attribute `selected` contains `"red"` (such as `["red"]` ). Clicking the checkbox again causes it to become unchecked and the `"red"` element is removed from the `selected` array.


::: tip

If you don't want to group checkboxes, you can also use the [`checked`](#checked) attribute to operate individually. But don't use `checked` and `group` at the same time, Glyphix doesn't take this case into account.
:::



### `indeterminate` <decl type="boolean" get set />


The `indeterminate` attribute indicates that the checkbox is in an undefined state. When this property is `true`, the checkbox has a horizontal line like a minus sign in the middle to indicate uncertainty about its status.


The indeterminate state can be used when an item has multiple options: if all children are selected, the parent will also be selected; if all are unselected, the parent will not be selected either. If some of the children are selected, the parent will be in an indeterminate state.


The following example demonstrates this usage. This example demonstrates crafting a list of enchantment tables so that when you select a partial recipe, the "Enchantment table" checkbox will be partially selected. As you can see, this example allows you to use the parent checkbox to check or uncheck all of its children.


<glyphix id="checkbox-indeterminate" :height="140" title="三态复选框" >


``` html
<div>
  <div>
    <!--
      当 selected.length == 3 时，entirety 就会选中，否则：
      - 如果 selected.length == 0，那么未选中；
      - 其他情况意味着选择了部分配方，因此处于 indeterminate 状态。
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
  // This function is called when the entirety checkbox is clicked to set the selected state of all recipes
  selectEntirety(status) {
    // Use [... this.parts ] to copy the list to avoid modifying it in place
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

When the `checked` attribute is set (note that it is not cleared), the `indeterminate` attribute is automatically cleared. Even if a checkbox has both properties, it will appear selected rather than in an indeterminate state.
:::



### CSS behavior


The checkbox is an inline element by default, its display size is determined by the `font-size` CSS property, and it will be aligned with the display baseline of the text. Please do not manually specify attributes such as `width` and `height`, otherwise the display may be confused.