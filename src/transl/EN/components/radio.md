# radio


Radio buttons, which are inline elements by default, are often used in a **radio group**, which contains a set of radio buttons that describe a series of related options. Only one radio button in the group can be selected at a time. Radio buttons are typically rendered as small circles that are filled to highlight when selected.


<glyphix id="radio-1" :height="65" title="单选按钮">


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

Radio buttons are similar to [`checkbox`](checkbox.md), but `radio` can only select one value from the group, while `checkbox` allows multiple values ​​to be selected.
:::



## property


### `checked` <decl type="boolean" get set listen />


This property indicates whether this radio button is selected. Setting the `checked` attribute can toggle the selected state of the radio button: when the value is `true`, it is displayed in the selected state.


The `checked` event is triggered when the user clicks on a radio button and causes its selected state to change.


::: tip

Manipulating the `checked` attribute is not a recommended use of `radio`, please use the [单选组](#group) method.
:::



### `value` <decl type="any" get set />


A JavaScript value that identifies the radio button value, usually a string or number. This value is not displayed, but it can be used in [单选组](#group).


### `group` <decl type="any" get set listen />


If you have multiple associated `radio` components, you can combine the `group` and `value` attributes. Radio buttons within the same group are mutually exclusive: the value of the `group` bound responsive property is equal to the `value` property of the selected radio button. For example:
``` html
<radio value="red" model:group="color" />
<radio value="blue" model:group="color" />
<radio value="yellow" model:group="color" />
```
Where `color` is a responsive attribute, and when the second radio button is selected, the value of `color` is `"blue"`. If all radio buttons' `value` and `color` do not match, then the radio button will not be selected. For example:
``` html
<p on:click="color = null">reset select</p>
```
The selected state will be cleared:


<glyphix id="radio-reset" :height="65" title="清除选中状态">


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



### CSS behavior


The radio button is an inline element by default, its display size is determined by the `font-size` CSS property, and it will be aligned with the display baseline of the text. Please do not manually specify attributes such as `width` and `height`, otherwise the display may be confused.