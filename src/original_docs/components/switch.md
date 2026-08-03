# switch

开关选择组件，默认为行内元素。用于表示开/关两种状态，并允许用户在两种状态之间切换。`switch` 的功能和 `checkbox` 类似，但是交互效果和意图不同，即分别表达开关和复选。

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
`switch` 组件的样式通常如示例中所示，但也可能因设备而异。尤其需要注意的是，不同设备上的 `switch` 宽度可能是有差异的，开发者应该预留合适的布局余量。
:::

## 属性

### `value` <decl type="boolean" set get listen/>

表示 `switch` 的状态，值为 `true` 时，`switch` 处于开启状态，否则处于关闭状态。当不指定 `value` 属性时，`switch` 组件默认是关闭的。

### `checked` <decl type="boolean" set get/>

这是快应用兼容属性，通常更推荐使用 [`value`](#value)

### `change` <decl type="{ checked: boolean }" get listen/>

这是快应用兼容属性，通常更推荐使用 [`value`](#value)

## CSS 行为

`switch` 组件的整体风格由系统决定，不受开发者控制，正如 [Fluent 2](https://fluent2.microsoft.design/components/web/react/switch/usage) 和 [Material 3](https://m3.material.io/components/switch/overview) 的风格差异那样。Glyphix 允许在 CSS 中定制 `switch` 的颜色，并且可以调整 `switch` 的大小。

### CSS 属性

#### `color`

设置 `switch` 组件的滑块颜色，与一般的 CSS [`color`](/framework/generic/styles.md#color) 不同，`switch` 的 `color` 属性不支持继承，因此你必须将它定义在当前 `switch` 组件上。

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

控制 `switch` 组件的背景颜色，详见 [`active`](#active) 伪类的文档。 

#### `font-size`

可以通过 [`font-size`](/framework/generic/styles.md#font-size) CSS 属性来调整 `switch` 的大小，使其行内（inline）的文字尺寸配合协调。下面的示例演示了 `font-size` 与 `switch` 大小的关系：

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
`switch` 的显示大小并不受 `width` 和 `height` 等属性的控制，而是总是由 `font-size` 决定。因此请不要手动指定 `width` 等尺寸属性，以免显示异常。
:::

### CSS 伪类

#### `active`

`active` 伪类用于定义 `switch` 处于打开状态的样式。如下面的示例所示，它通常和常规样式规则一起配置：

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

本示例通过 `color` 和 `background-color` CSS 属性来控制 `switch` 切换时的颜色样式。`switch` 组件在 `active` 伪类激活的状态下也只会响应这两个 CSS 属性的配置。

::: tip
请同时定义普通状态和 `active` 状态下的 `color` 和 `background-color` 属性，否则 `switch` 切换时不会有相应的颜色转变。
:::
