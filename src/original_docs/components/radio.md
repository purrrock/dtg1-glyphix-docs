# radio

单选按钮，默认为行内元素，常用于一个**单选组**中，其中包含一组描述一系列相关选项的单选按钮。同一时间只能选定组中的一个单选按钮。单选按钮通常呈现为小圆圈，在选择时被填充突出显示。

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
单选按钮和 [`checkbox`](checkbox.md) 有些类似，但是 `radio` 仅能够从组中选择一个值，`checkbox` 则允许选择多个值。
:::

## 属性

### `checked` <decl type="boolean" get set listen />

该属性指示是否选中此单选按钮。设置 `checked` 属性可以让单选按钮的选中状态切换：值为 `true` 时即显示为选中状态。

当用户点击单选按钮并导致其选中状态改变时，会触发 `checked` 事件。

::: tip
操作 `checked` 属性并不是使用 `radio` 的推荐用法，请使用[单选组](#group)方法。
:::

### `value` <decl type="any" get set />

标识单选按钮值的一个 JavaScript 值，通常是字符串或者数字。这个值并不会显示，但是它可以在[单选组](#group)中使用。

### `group` <decl type="any" get set listen />

如果有多个关联的 `radio` 组件，便可以将 `group` 和 `value` 属性组合起来。同一组内的单选按钮是互斥的：`group` 绑定的响应式属性值等于选中的单选框的 `value` 属性。例如：
``` html
<radio value="red" model:group="color" />
<radio value="blue" model:group="color" />
<radio value="yellow" model:group="color" />
```
其中 `color` 是一个响应式属性，当第二个单选按钮被选中时，`color` 的值为 `"blue"`。如果所有 单选按钮的 `value` 和 `color` 都不匹配，那么将不会选中单选按钮。例如：
``` html
<p on:click="color = null">reset select</p>
```
会清除选中状态：

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

### CSS 行为

单选按钮默认是行内元素，它的显示尺寸由 `font-size` CSS 属性决定，并且会和文本的显示基线对齐。请不要手动指定 `width` 和 `height` 等属性，否则可能导致显示错乱。
