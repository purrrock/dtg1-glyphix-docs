# swiper

卡片视图容器，支持任意子组件。卡片视图的滚动方向由具体的布局方式来指定：使用 `flex-column` 布局的列表为垂直方向，而 `flex-row` 布局的列表为水平方向。

## 属性

### `scroll` <decl type="{ scrollX: number, scrollY: number, scrollState: number }" get listen />

`scroll` 属性值是一个对象，包含以下字段：`scrollX`、`scrollY` 和 `scrollState`。`scrollX` 和 `scrollY` 属性分别表示水平和垂直方向的滚动位置，单位为像素；`scrollState` 属性表示滚动状态，其值为 $0$、$1$ 或 $2$，具体含义如下表所示。通过 `on` 指令可以监听 `scroll` 属性的变化，任何由用户操作和 API 操作引起的内容位置变化都是触发监听。

| `scrollState` 值 | 效果说明                                                            |
| :--------------: | ------------------------------------------------------------------- |
|       $0$        | 已经停止滑动                                                        |
|       $1$        | 正在通过用户的手势滑动                                              |
|       $2$        | 用户已松手，由 [`scrollTo`](#scrollto) 等方法调用或惯性等导致的滑动 |

### `scrollTop` <decl type="number" get listen />

垂直方向的滚动位置，即 `swiper` 组件的内容顶部到视口顶部的距离，单位为像素。可以通过此属性监听滚动位置的变化。与 [`scroll`](#scroll) 属性不同，监听 `scrollTop` 属性本身无法区分是用户的手势滚动还是 API 调用或惯性产生的滚动。

### `scrollLeft` <decl type="number" get listen />

水平方向的滚动位置，即 `swiper` 组件的内容左边到视口左边的距离，单位为像素，可以通过此属性监听滚动位置的变化。与 [`scroll`](#scroll) 属性不同，监听 `scrollLeft` 属性本身无法区分是用户的手势滚动还是 API 调用或惯性产生的滚动。

### `scrollWidth` <decl type="number" get listen />

`swiper` 组件内容区域的宽度。垂直布局下的 `swiper` 宽度等于视图宽度，而水平布局的 `swiper` 宽度为所有元素宽度之和。可通过此监听内容宽度的变化。

### `scrollHeight` <decl type="number" get listen />

`swiper` 组件内容区域的高度。垂直布局下的 `swiper` 高度等于视图高度，而水平布局的 `swiper` 高度为所有元素高度之和。可通过此监听内容高度的变化。

### `snapshot` <decl type="boolean" get set />

开启 `snapshot` 属性时，`swiper` 的子组件会开启快照模式。请参考 `scroll` 组件的 [`snapshot`](scroll.md#snapshot) 属性。

### `deformation` <decl type="string" set />

设置子元素的形变效果，通过形变效果可以实现鱼眼等外观。可以通过名称（字符串）指定一种内置的形变效果，也可以通过 JavaScript 函数来定义形变效果。

| 值 | 效果说明 |
| :-: | :- |
| `'none'` | 无形变效果（默认值）。 |
| `'fade'` | 渐隐缩放切换效果，这种效果突出了当前视口内元素的“聚焦”，并使视口外的元素显得退居次位。详情请参考本节中示例的效果。 |
| `'fisheye'` | 内置的鱼眼效果，该属性组件用于 [`scroll`](scroll.md) 组件，而不是 `swiper`。 |
| function | 通过 JavaScript 函数指定形变效果。 |

形变效果应该是常量而不要修改。

如果 `swiper` 的子元素内容经常变化，在使用变形效果时建议为元素添加 [`quiescent`](/framework/generic/properties.md#quiescent) 属性以避免在切换时更新并提升性能。可以参考下面的示例：

<glyphix id="components-swiper-deformation" height="360" width="360" title="元素形变效果">

```html
<swiper deformation="fade" indicator>
  <div for="x in 5" :quiescent="x != 0">
    <progress-arc busy :start-angle="0" :stop-angle="360" />
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

progress-arc {
  width: 30%;
  height: 30%;
  margin-bottom: 5%;
}
```

</glyphix>

示例中的第一个子元素没有开启 `quiescent` 属性，因此在切换过程中会持续更新，而其他元素则会停止更新。

### `vertical` <decl type="boolean" set />

设置 `swiper` 组件是否垂直布局，默认为 `false` 时会使用水平布局。以下示例演示了垂直布局下的 `swiper` 交互效果（注意要垂直滚动，水平滑动是没有响应的）。

<glyphix id="components-swiper-vertical" height="360" width="360" title="垂直布局">

``` html
<swiper vertical deformation="fade" indicator>
  <p for="x in 5">
    pane {{ x + 1 }}
    {{ x == 0 ? '(swipe up)' : x == 4 ? '(swipe down)' : '' }}
  </p>
</swiper>
```

``` css
p {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
}
```

</glyphix>

### `indicator` <decl type="boolean" get set />

设置 `swiper` 组件是否显示点指示器，点指示器的显示位置由 `vertical` 属性决定：垂直布局时点指示器显示右侧中间，水平布局时点指示器显示在底部中间。具体效果请参考 [`deformation`](#deformation) 和 [`vertical`](#vertical) 属性的示例。

参考[点指示器 CSS 属性](#点指示器-css-属性)了解如何自定义点指示器的显示样式。

### `pageLength`  <decl type="number" set />

设置子页面的大小或占比，为百分比时，设置在滑动方向上的子组件大小（相对于组件本身）；为其他数字时，设置在滑动方向上的子组件大小。

### `index`  <decl type="number" get set listen />

当前显示的子组件索引，设置 `index` 属性时，组件将通过动画滚动到指定的子组件。可以通过 `on` 指令监听位置变化，子组件索引变化时可以通过 `index` 属性监听到。

### `finalChanged` <decl type="bool" get set />

设置是否只在滚动停止时触发 [`index`](#index) 变化的事件。默认情况下（即 `finalChanged` 为 `false`），只要滚动手势或其他原因导致 `swiper` 组件的 `index` 属性变化时，都会触发其监听事件。但是这样做容易导致动画掉帧，或是过于频繁、不必要的事件触发。当设置 `finalChanged` 时，只有当滚动停止时才会触发 `index` 变化的事件。

::: tip
在通过监听 `index` 属性实现点指示器等效果时，建议将 `finalChanged` 设置为 `true`，这可以避免滑动过程因事件触发渲染更新导致的掉帧。
:::

### `weakGesture` <decl type="'none' | 'start' | 'end' | 'edge'" get set />

设置 `swiper` 组件在哪些情况下会对滚动手势进行冒泡。默认情况下 `swiper` 对它响应的手势阻止冒泡，因此它的父级元素无法接收到使 `swiper` 滚动的手势。`weakGesture` 允许在拖拽到内容边界位置时对手势事件启用冒泡，从而使父级元素能够接收这些手势。

|    值     | 描述                                             |
| :-------: | ------------------------------------------------ |
| `'none'`  | 不对响应的手势事件进行冒泡。                     |
| `'start'` | 拖拽到内容起始位置后对响应的手势事件冒泡。       |
|  `'end'`  | 拖拽到内容结束位置后对响应的手势事件冒泡。       |
| `'edge'`  | 拖拽到内容起始或结束位置后对响应的手势事件冒泡。 |

如果页面的底层元素是一个水平的 `swiper` 组件，但是希望右滑手势能让页面返回，那么可以这样配置：
``` html
<swiper weak-gesture="start"> ... </swiper>
```
当用户滑动到 `swiper` 组件的头部之后继续右滑即可退出页面。

### `bounces` <decl type="'none' | 'start' | 'end' | 'edge'" get set />

设置通过手势将 `swiper` 滚动到边界之后是否触发回弹。该属性的初始值为 `edge`，即允许起始位置和结束位置的回弹。`swiper` 的 `bounces` 属性与 [`scroll`](scroll.md) 组件的 [`bounces`](scroll.md#bounces) 属性类似，更多说明请参考相关文档。

### `scrolled` <decl type="boolean" listen />

通过 `scrolled` 属性监听 `swiper` 组件是否处于滚动状态。事件触发的属性值为 `true` 表示正在滚动，否则意味着已经停止滚动。

用户触摸产生的滚动操作和通过 `scroll` 属性来滚动都会触发 `scrolled` 事件。从滚动状态停止时，`scrolled` 事件的参数值为 `false`。

### `setIndex`
<decl method><pre>
(options: {
  index: number,
  behavior?: 'instant' | 'smooth'
}): void
</pre></decl>

将视口移动到由索引所指定的子组件。如果本次移动会越过视口边界，视口位置将停留在第一个或最后一个组件处。`options` 参数属性的作用为：
- `index`：待移动的目标子组件的索引，$0$ 表示第一个子组件。
- `behavior`：为 `'smooth'` 时使用动画过渡，为 `'instant'`（默认值）时立即移动到指定的子组件位置。

### `scrollTo` <decl type="(position: number): void" method />

将内容滚动到指定的位置，滚动方向和 scroll 组件的布局方向一致。

`scrollTo` 方法会忽略元素的吸附效果。

## CSS 规范

### 点指示器 CSS 属性

本节介绍 `swiper` 组件开启 [`indicator`](#indicator) 属性后可用的 CSS 属性，它们用于控制点指示器的部分显示样式。`swiper` 的点指示器总是显示为一组水平或垂直排列的圆点，开发者只能在此基础上进行自定义。

#### `indicator-color`

定义未选中点指示器的颜色。效果如下所示：

<glyphix id="components-swiper-indicator-color" height="360" width="360" title="点指示器颜色">

```html
<swiper indicator>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-color: #333;
  indicator-selected-color: #ff60ff;
  indicator-bottom: 16px;
}
```

</glyphix>

#### `indicator-selected-color`

定义选中点指示器的颜色。效果可参考 [`indicator-color`](#indicator-color) 属性的示例，您可以观察到选中页面所对应的点指示器显示为该 CSS 属性所定义的颜色。

#### `indicator-size`

定义点指示器中每一个指示点的大小，单位为像素。默认值为 `10px`。以下示例演示了将点指示器大小设置为 `16px` 的效果：

<glyphix id="components-swiper-indicator-size" height="360" width="360" title="点指示器大小">

```html
<swiper indicator>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-color: #333;
  indicator-selected-color: #ff60ff;
  indicator-bottom: 24px;
  indicator-size: 16px;
}
```

</glyphix>

#### `indicator-top`

当 `swiper` 具有[水平布局](#vertical)时，使用 `indicator-top` 属性可以指定点指示器距离顶部的距离。默认情况下，点指示器将显示在底部中间位置，该属性可以将其显示在顶部：

<glyphix id="components-swiper-indicator-top" height="360" width="360" title="顶部点指示器">

```html
<swiper indicator>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-top: 16px;
}
```

</glyphix>

::: warning
不要同时设置 `indicator-left`、`indicator-top`、`indicator-right` 和 `indicator-bottom`，否则会导致点指示器位置不可预期。
:::

#### `indicator-left`

当 `swiper` 具有[垂直布局](#vertical)时，使用 `indicator-left` 属性可以指定点指示器距离左侧的距离。默认情况下，点指示器将显示在右侧中间位置，该属性可以将其显示在左侧：

<glyphix id="components-swiper-indicator-left" height="360" width="360" title="左侧点指示器">

```html
<swiper indicator vertical>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-left: 16px;
}
```

</glyphix>

#### `indicator-right`

当 `swiper` 具有[垂直布局](#vertical)时，使用 `indicator-right` 属性可以指定点指示器距离右侧的距离。效果如下所示：

<glyphix id="components-swiper-indicator-right" height="360" width="360" title="右侧点指示器">

```html
<swiper indicator vertical>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-right: 32px;
}
```

</glyphix>

#### `indicator-bottom`

当 `swiper` 具有[水平布局](#vertical)时，使用 `indicator-bottom` 属性可以指定点指示器距离底部的距离。效果可参考 [`indicator-color`](#indicator-color) 和 [`indicator-size`](#indicator-size) 属性的示例。

### `padding` 和 `overflow` <version-badge since="0.9" />

参见 [scroll 组件](scroll.md#padding-和-overflow)的相关说明。`swiper` 组件的 `padding` 和 `overflow` 属性与 `scroll` 组件的同名属性具有相同的行为规范，更多说明请参考相关文档。
