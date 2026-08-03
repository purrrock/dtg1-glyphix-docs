# input

默认为行内元素，提供可交互的界面，接收用户的输入。

## 属性

### `type` <decl type="'checkbox' | 'radio'" set />

可设置为以上值类型的控件，根据设置的类型决定最终 `input` 组件的实际形态。

### `name` <decl type="string" set />

设置 `input` 组件名称。

### `checked` <decl type="boolean" set />

当前组件的 checked 状态，可触发 checked 伪类，type 为 checkbox 时生效，设置为 `on` 时 checkbox 默认勾选。

### `value` <decl type="string" set />

设置 `input` 组件的值。
