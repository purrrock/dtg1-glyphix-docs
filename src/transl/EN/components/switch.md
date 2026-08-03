# switch


Switch selects components, defaulting to inline elements. Used to represent on/off status and allow the user to switch between the two statuses. The function of `switch` is similar to that of `checkbox`, but the interaction effects and intentions are different, that is, they express switches and checks respectively.


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

The `switch` component is typically styled as shown in the example, but may vary depending on the device. In particular, it should be noted that the width of `switch` may be different on different devices, and developers should reserve appropriate layout margin.
:::



## property


### `value` <decl type="boolean" set get listen/>


Indicates the status of `switch`. When the value is `true`, `switch` is in the on state, otherwise it is in the off state. When the `value` attribute is not specified, the `switch` component is turned off by default.


### `checked` <decl type="boolean" set get/>


This is a Quick App compatibility attribute, and it is usually more recommended to use [`value`](#value)


### `change` <decl type="{ checked: boolean }" get listen/>


This is a Quick App compatibility attribute, and it is usually more recommended to use [`value`](#value)


## CSS behavior


The overall style of the `switch` component is determined by the system and is not controlled by the developer, just like the style differences between [Fluent 2](https://fluent2.microsoft.design/components/web/react/switch/usage) and [Material 3](https://m3.material.io/components/switch/overview). Glyphix allows the color of `switch` to be customized in CSS, and the size of `switch` to be resizable.


### CSS properties


#### `color`


Set the slider color of the `switch` component. Unlike the general CSS [`color`](/framework/generic/styles.md#color), the `color` attribute of `switch` does not support inheritance, so you must define it on the current `switch` component.


<glyphix id="components-switch-color" height="36" title="siwtch 滑块颜色">


``` html
<div>
  red color: <switch class="red"/>,
  not inherited: <switch/>
</div>
```


``` css
div {
  color: red; /* 注意 switch 不会继承 color 属性 */
}

.red {
  color: red; /* 必须在 switch 组件的样式上定义 color */
}
```
</glyphix>



#### `background-color`


Controls the background color of the `switch` component, see the documentation of the [`active`](#active) pseudo-class for details.


#### `font-size`


You can adjust the size of `switch` through the [`font-size`](/framework/generic/styles.md#font-size) CSS property to match the inline text size. The following example demonstrates the relationship between `font-size` and `switch` sizes:


<glyphix id="components-switch-size" height="100" title="font-size 与 siwtch 大小">


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
  color: #415a77; /* 注意 switch 不会继承 color 属性 */
  font-size: 1.25rem;
}
```
</glyphix>



::: warning

The display size of `switch` is not controlled by attributes such as `width` and `height`, but is always determined by `font-size`. Therefore, please do not manually specify size attributes such as `width` to avoid abnormal display.
:::



### CSS pseudo-class


#### `active`


The `active` pseudo-class is used to define the style in which `switch` is turned on. As shown in the following example, it is usually configured along with regular style rules:


<glyphix id="components-switch-colors" height="36" title="siwtch 滑块颜色设置">


``` html
<div>
  color switch: <switch/>
</div>
```


``` css
/* switch 关闭状态下的样式 */
switch {
  color: #415a77;
  background-color: #bde0fe;
}

/* switch 打开状态下的样式 */
switch:active {
  color: #fefae0;
  background-color: #ffafcc;
}
```
</glyphix>



This example uses the `color` and `background-color` CSS properties to control the color style when switching `switch`. The `switch` component will only respond to the configuration of these two CSS properties when the `active` pseudo-class is activated.


::: tip

Please define the `color` and `background-color` attributes in the normal state and `active` state at the same time, otherwise there will be no corresponding color change when `switch` is switched.
:::
