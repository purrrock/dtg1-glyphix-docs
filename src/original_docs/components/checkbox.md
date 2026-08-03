# checkbox

`checkbox`（复选框）元素会在被激活的情况下显示被选中（打勾）的方框，表示一个项目被选中。

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
`checkbox` 通常是一个可以打勾的正方形，但具体的效果由设备决定。开发者目前无法通过 CSS 修改 `checkbox` 的颜色等样式。
:::

## 属性

### `checked` <decl type="boolean" get set listen />

该属性指示是否选中此复选框。设置 `checked` 属性可以让复选框的选中状态切换：值为 `true` 时即显示为选中状态。还可以通过双向绑定对单个复选框进行操作：
``` html
<checkbox model:checked="yes" />
```

本文当前面的实例展示了这种绑定的用法，请注意不要绑定到 [`value`](#value) 属性，而是绑定到 `checked`。

仅当用户点击复选框导致 `checked` 属性变化时才会触发事件。

::: warning
不要在[复选框组](#group)中设置 `checked` 属性，以免发生混乱。
:::

### `value` <decl type="any" get set />

标识复选框值的一个 JavaScript 值，通常是字符串或者数字。这个值并不会显示，但是它可以在[分组操作](#group)中使用。

### `group` <decl type="any[]" get set listen />

如果有多个关联的 `checkbox` 组件，便可以将 `group` 和 `value` 属性组合起来；同一组内的复选框会形成一个选定值的数组。请参考下面的示例：

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

使用 `model:group` 或者 `::group` 将 `group` 属性双向绑定到一个响应式的数组（例子中的 `selected`）就可以实现：
- 当用户操作了组内的某个复选框之后，响应式数组的值会发生更新；
- 响应式数组的元素改变时会反映到 `checkbox` 的表现上。

如上面的示例所示：在初始状态下，分组复选框的选中情况由 `group` 属性的值决定。具体来说，对于一个复选框，如：
``` html
<checkbox value="red" model:group="selected" />
```
由于 `value` 属性指定了 `"red"` 值，当响应式属性 `selected` 的值包含 `"red"` 时（如 `["red"]`），该复选框就会被选中。用户再次点击这个复选框会导致它变为未选中状态，而 `selected` 数组也会删除 `"red"` 元素。

::: tip
如果不想对复选框分组，还可以使用 [`checked`](#checked) 属性来单独操作。但不要同时使用 `checked` 和 `group`，Glyphix 没有考虑这种情形。
:::

### `indeterminate` <decl type="boolean" get set />

`indeterminate` 属性表示复选框处于**不确定**的状态。当该属性为 `true` 时，复选框在中间有一条像减号一样的水平线，以表示不确定其状态。

不确定状态可以在一个项目有多个自选项时使用：如果所有的子项被选中，则父级也会被选中；如果全部未选中，则父级也不会选中。如果有部分子项被选中，父级将会处于不确定状态。

下面的示例演示了这种用法。此示例演示了合成附魔台的清单，当你选中了部分配方时，“Enchantment table” 复选框就会处于部分选中状态。如你所见，这个示例允许你使用父级复选框来选中或取消选中所有的子项。

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
  // 点击 entirety 复选框时调用此函数设置所有配方的选中状态
  selectEntirety(status) {
    // 要使用 [...this.parts] 拷贝列表，以免原地修改
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
当 `checked` 属性被设置时（注意并不是清除）会自动清除 `indeterminate` 属性。即使复选框同时具有这两个属性，也会显示为选中状态，而不是不确定状态。
:::

### CSS 行为

复选框默认是行内元素，它的显示尺寸由 `font-size` CSS 属性决定，并且会和文本的显示基线对齐。请不要手动指定 `width` 和 `height` 等属性，否则可能导致显示错乱。
