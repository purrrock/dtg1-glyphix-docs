# label

`label` 组件用于展示文本或者标记信息，默认为行内元素。`label` 可以配合以下表单组件显示标记信息：
- [input](input)
- [radio](radio)
- [switch](switch)
- [checkbox](checkbox)

当 `label` 与支持的表单组件关联后，点击 `label` 组件也会触发表单组件的值更新。

## 属性

### `text` <decl type="string" set get />

标签的文本内容，支持属性语法或者文本子元素语法：
``` html
<label text="label text"></label>
<label>label text</label>
```

### `target` <decl type="string" set get />

目标组件的 ID。例如：
```html
<radio id="red" /><label target="red">red</label>
```
点击例子中的 `label` 组件之后也会触发 ID 为 `red` 的 `radio` 组件更新，但是点击 `label` 组件并不会触发目标组件的 `click` 等触摸事件。

考虑到性能问题，只支持和 `label` 组件同级的目标组件（即具有相同的父组件）。

::: warning
目前不支持更改目标组件。
:::
