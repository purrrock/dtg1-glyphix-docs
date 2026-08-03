# scroll-bar

滚动条组件。该组件可以在滚动内容较多时显示滚动条，用户可以通过滚动条来控制内容的滚动。

## 属性

### `value` <decl type="number" set get listen />

滚动条的当前值，该值是 `min` 和 `max` 之间的一个值，默认值为 $0$。

### `min` <decl type="number" set />

滚动条的最小值，该值应该不大于 `max`。默认值为 $0$。

### `max` <decl type="number" set />

滚动条的最大值，该值应该不小于 `min`。默认值为 $100$。

### `pagestep` <decl type="number" set />

滚动条的滚动步长，即每次滚动的距离。默认值为 $10$。
