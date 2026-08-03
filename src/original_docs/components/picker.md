# picker

文本选择器组件。该组件显示一组文本，点击中间的文本项会触发选中事件，而滑动操作可以使所有的文本项滚动显示。

::: warning
`picker` 组件的功能没有验证过，并且无人维护。
:::

## 属性

### `range` <decl type="string[]" set />

`range` 属性值中的所有字符串将显示在 `picker` 组件中。用户可以操作 `picker` 组件滚动或者选择这些字符串。

`range` 属性值中字符串的索引方式参考 [`index` 属性](#index)。

### `loop` <decl type="boolean" set />

配置 `picker` 组件是否循环（即无限长）显示。此属性值为 `true` 时开启循环显示，默认为 `false`。

### `value` <decl type="string" listen />

监听当前的选中项文本，滚动操作中选中项变化后会触发此监听。本属性的功能也可以通过 `on:index="handle(rangeData[$event])"` 的方法实现。

### `index` <decl type="Integer" get set listen />

`picker` 组件的选中项索引值。索引的规则是：[`range` 属性](#range) 属性值数组的第一个字符串项目的索引值为 $0$，其他字符串的索引依次加一。设置 `index` 属性可以指定 `picker` 组件的选中项，同时也可以监听该属性的变化来检测滚动操作导致的选中项变化。

### `scroll` <decl type="{ x: number y: number }" get set listen />

通过 `scroll` 属性可以监听滚动操作，同时也可以在代码中操纵 `picker` 组件显示滚动效果。类似于对齐的列表组件，`picker` 的 `scroll` 操作也会对齐到最近的项目。

由于 `picker` 组件只支持垂直模式，所以 `scroll` 属性值的 `x` 字段始终为 `0`。

### `scrolled` <decl type="boolean" read listen />

通过 `scrolled` 属性监听 `picker` 是否处于滚动状态。事件触发的属性值为 `true` 表示 `picker` 正在滚动，否则意味着 `picker` 已经停止滚动。

用户触摸产生的滚动操作和通过 `scroll` 属性来滚动都会触发 `scrolled` 事件。当 `picker` 从滚动状态停止时，`scrolled` 事件的参数值为 `false`。

### `damping` <decl type="number" set />

设置 `picker` 滚动动画的阻尼系数，有效取值范围为 $[0.1, 50]$（不支持的值会自动修改为上下限），默认值为 $1.5$。更大的阻尼系数会使动画停顿得更快，默认的阻尼系数值可以产生距离比较长、持续时间也比较久的惯性效果。

阻尼系数应当设置成常量而不要修改，修改阻尼系数不会影响回弹时的动画。
