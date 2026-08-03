# scroll

支持任意子组件的滚动列表容器。列表的滚动方向由具体的布局方式来指定：使用流式布局或者 `column` 方向的 flex 布局时元素沿垂直方向布局，列表可以垂直滚动；而使用 `row` 方向的 flex 布局时元素沿水平方向布局，列表可以水平滚动。`scroll` 组件不支持双向滚动（即水平和垂直方向同时可滚动）。

`scroll` 组件默认是使用流式布局的块级元素。

`scroll` 组件可以使用手势交互来滚动，垂直的 `scroll` 组件还支持编码器（手表的旋转表冠，模拟器上使用鼠标滚轮）滚动。

::: tip
本文档中部分可交互示例支持鼠标滚轮交互（标题右侧有鼠标图标图标）：你可以将指针悬停在示例内，然后使用鼠标滚轮来滚动列表。
:::

## 属性

### `scroll` <decl type="{ scrollX: number, scrollY: number, scrollState: number }" get listen />

`scroll` 属性值是一个对象，包含以下字段：`scrollX`、`scrollY` 和 `scrollState`。`scrollX` 和 `scrollY` 属性分别表示水平和垂直方向的滚动位置，单位为像素；`scrollState` 属性表示滚动状态，其值为 $0$、$1$ 或 $2$，具体含义如下表所示。通过 `on` 指令可以监听 `scroll` 属性的变化，任何由用户操作和 API 操作引起的内容位置变化都是触发监听。

| `scrollState` 值 | 效果说明                                                            |
| :--------------: | ------------------------------------------------------------------- |
|       $0$        | 已经停止滑动                                                        |
|       $1$        | 正在通过用户的手势滑动                                              |
|       $2$        | 用户已松手，由 [`scrollTo`](#scrollto) 等方法调用或惯性等导致的滑动 |

::: info
`scroll` 子元素所在的区域称作“内容”（content）区域，而列表组件实际显示出来的部分成为“视图”（view）区域。元素在内容区域布局，其尺寸可能超出视图区域，通过滚动可以改变内容的显示位置。
:::

滚动位置的范围通常在内容区域内，即水平列表的 `scrollX` 在 $[0, \texttt{contentWidth}]$ 范围内，而垂直列表的 `scrollY` 在 $[0, \texttt{contentHeight}]$ 范围内。但当列表滚动到内容的头部之前时，`scrollX` 或 `scrollY` 会小于 $0$；同样，当滚动到内容尾部之后，`scrollX` 或 `scrollY` 的值则会大于 `contentWidth` 或 `contentHeight`。

::: warning
`scroll` 事件在滚动过程中的每一帧都会触发，在 JavaScript 代码中监听此事件可能产生明显的掉帧，因此要尽量避免使用。
:::

### `scrollTop` <decl type="number" set get listen />

垂直方向的滚动位置，即 `scroll` 组件的内容顶部到视口顶部的距离，单位为像素。可通过此属性设置滚动位置，也可以通过此属性监听滚动位置的变化。

与 [`scroll`](#scroll) 属性不同，监听 `scrollTop` 属性本身无法区分是用户的手势滚动还是 API 调用或惯性产生的滚动。

### `scrollLeft` <decl type="number" set get listen />

垂直方向的滚动位置，即 `scroll` 组件的内容左边到视口左边的距离，单位为像素。可通过此属性设置滚动位置，也可以通过此属性监听滚动位置的变化。

与 [`scroll`](#scroll) 属性不同，监听 `scrollLeft` 属性本身无法区分是用户的手势滚动还是 API 调用或惯性产生的滚动。

### `scrollWidth` <decl type="number" get listen />

`scroll` 组件内容区域的宽度。垂直布局下的 `scroll` 宽度等于视图宽度，而水平布局的 `scroll` 宽度为所有元素宽度之和。可通过此监听内容宽度的变化。

### `scrollHeight` <decl type="number" get listen />

`scroll` 组件内容区域的高度。垂直布局下的 `scroll` 高度等于视图高度，而水平布局的 `scroll` 高度为所有元素高度之和。可通过此监听内容高度的变化。

### `damping` <decl type="number" set />

设置列表滚动动画的阻尼系数，有效取值范围为 $[0.1, 50]$（不支持的值会自动修改为上下限），默认值为 $1.5$。更大的阻尼系数会使动画停顿得更快，默认的阻尼系数值可以产生距离比较长、持续时间也比较久的惯性效果。

<glyphix id="components-scroll-damping" height="360" width="360" title="阻尼效果" wheel>

``` html
<div>
  <span>damping: {{damping}}</span>
  <button on:click="increase">+</button>
  <button on:click="decrease">-</button>
  <scroll :damping="damping">
    <p for="x in 50" class="item">
      Item {{ x + 1 }}
    </p>
  </scroll>
</div>
```

``` js
export default {
  data: {
    damping: 1
  },
  increase() {
    this.damping += 1
    if (this.damping > 20)
      this.damping = 1
  },
  decrease() {
    this.damping -= 1
    if (this.damping < 1)
      this.damping = 19.5
  }
}
```

``` css
span {
  color: #404040;
}

scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  height: 300px;
  width: 360px;
}

.item {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px 5px;
  margin: 10px;
  border-radius: 16px;
}

button {
  color: #fafafa;
  background-color: #adadad;
  border-radius: 12px;
  margin-left: 16px;
  margin-bottom: 16px;
  width: 1.2rem;
}
```

</glyphix>

::: tip
阻尼系数应当设置成常量而不要修改，修改阻尼系数不会影响回弹时的动画。
:::

### `snapshot` <decl type="boolean" get set />

开启 `snapshot` 属性时，列表中的子组件会开启快照模式。相关演示可参考原生组件的 [`quiescent`](/framework/generic/properties.md#quiescent) 属性。

开启快照可能提升复杂界面的帧率。例如列表项目中存在大量的文本且包含非透明的背景时，快照模式可以将大量的绘制操作缓存并合并成少量的快照。Glyphix 框架会在重复的绘制中缓存这些快照，以进一步提升性能。

但 `snapshot` 属性不提供对子组件使用快照的保证，当系统的内存不足，或者没有必要使用快照时可能忽略此属性。

### `deformation` <decl type="string | function" set />

设置列表的形变效果，通过形变效果可以实现鱼眼等外观。可以通过名称（字符串）指定一种内置的形变效果，也可以通过 JavaScript 函数来定义形变效果。

|     值      |             效果说明             |
| :---------: | :------------------------------: |
|  `'none'`   |       无形变效果（默认值）       |
| `'fisheye'` |          内置的鱼眼效果          |
|  function   | 通过 JavaScript 函数指定形变效果 |

形变效果应该是常量而不要修改。

当列表设置为鱼眼形变效果时建议将 [`scrollSnap`](#scrollsnap) 属性设置为 `'center'`，以得到最合理的效果。

下图演示了鱼眼形变效果，通过“center”开关可以调节是否居中对齐。

<glyphix id="components-scroll-deformation" height="360" width="360" title="鱼眼效果" wheel>

``` html
<div>
  <p>center <switch ::value="center" /></p>
  <scroll deformation="fisheye" :scroll-snap="center ? 'center' : null">
    <p for="x in 15">
      Item {{ x + 1 }}
    </p>
  </scroll>
</div>
```

``` css
div {
  color: #404040;
  display: flex;
  flex-direction: column;
}

scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  flex: 1;
}

scroll > p {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 40px 10px;
  margin: 5px;
  border-radius: 50%;
}
```

``` js
export default {
  data: {
    center: true
  }
}
```

</glyphix>

::: tip
形变效果一般会用到快照，所以在设置有 `deformation` 属性时无需重复设置 `snapshot`。
:::

### `scrollSnap` <decl type="'none' | 'start' | 'center' | 'edge'" get set />

设置列表项目的对齐和吸附方式。例如可以让元素居中对齐，或者在元素边界上吸附。

|     值     | 描述                                                                                                           |
| :--------: | -------------------------------------------------------------------------------------------------------------- |
|  `'none'`  | 元素无吸对齐和附效果，即子元素可按照滚动惯性停止在任何位置。                                                   |
| `'start'`  | 滚动停止时元素起始位置对齐到视口起始位置。此模式目前不支持。                                                   |
| `'center'` | 滚动停止是元素的中心位置会对齐到视口中心。                                                                     |
|  `'edge'`  | 滚动停止时，元素的起始或结束位置就近对齐到视口起始或结束位置。但是如果滚动不会跨越元素边界，那么不会引起吸附。 |

`scrollSnap` 属性不会调整元素尺寸，但是可以利用布局等机制来实现等尺寸项目的列表。

::: warning
该属性应该在组件初始化时设置并且不能改变，否则可能出现交互错误。
:::

### `index` <decl type="number" get set listen />

当前显示的子组件索引，设置 `index` 属性时，组件将通过动画滚动到指定的子组件。可以通过 `on` 指令监听位置变化，子组件索引变化时可以通过 `index` 属性监听到。

`index` 的值会自动进行限制以保证指向有效的元素。使用 `index` 时必须保证 `scroll` 组件的所有元素都是静态的（即 CSS 的 [`position`](/framework/generic/styles.md#position) 属性为默认的 `static`），否则会出现错误。

### `finalChanged` <decl type="bool" get set />

设置是否只在滚动停止时触发 [`index`](#index) 变化的事件。默认情况下（即 `finalChanged` 为 `false`），只要滚动手势或其他原因导致 `scroll` 组件的 `index` 属性变化时，都会触发其监听事件。但是这样做容易导致动画掉帧，或是过于频繁、不必要的事件触发。当设置 `finalChanged` 时，只有当滚动停止时才会触发 `index` 变化的事件。

::: tip
在通过监听 `index` 属性实现点指示器等效果时，建议将 `finalChanged` 设置为 `true`，这可以避免滑动过程因事件触发渲染更新导致的掉帧。
:::

以下示例展示了 `finalChanged` 的效果。你可以尝试切换 "final-changed" 复选框，然后滑动列表，观察 `index` 的变化频率和时机。

<glyphix id="components-scroll-final-changed" height="360" width="360" title="延迟 index 事件" wheel>

``` html
<div>
  <p>
    <checkbox id="checkbox" ::checked="finalChanged" />
    <label target="checkbox">final-changed</label>
    index: {{index}}
  </p>
  <scroll :final-changed="finalChanged" ::index="index">
    <p for="x in 50">
      Item {{ x + 1 }}
    </p>
  </scroll>
</div>
```

``` css
div {
  color: #404040;
  display: flex;
  flex-direction: column;
}

scroll {
  display: flex;
  flex-direction: column;
  flex: 1;
}

scroll > p {
  background-color: #f0f0f0;
  border-radius: 12px;
  text-align: center;
  margin: 8px;
  padding: 20px;
}
```

``` js
export default {
  data: {
    index: 0,
    finalChanged: true
  }
}
```

</glyphix>

### `bounces` <decl type="'none' | 'start' | 'end' | 'edge'" get set />

设置通过手势将 `scroll` 滚动到边界之后是否触发回弹。该属性的初始值为 `edge`，即允许起始位置和结束位置的回弹。

|    值     | 描述                                   |
| :-------: | -------------------------------------- |
| `'none'`  | 禁用所有边界回弹。                     |
| `'start'` | 只允许拖拽到内容起始位置后的回弹。     |
|  `'end'`  | 只允许拖拽到内容结束位置后的回弹。     |
| `'edge'`  | 允许拖拽到内容起始或结束位置后的回弹。 |

下面的示例展示了各个 `bounces` 值的作用，你可以尝试将每一个项目左右滑动超过边界，并观察对应的交互行为。

<glyphix id="components-scroll-bounces" height="360" width="400" title="拖拽回弹动画">

``` html
<scroll class="column-box">
  <scroll for="item in items" class="row-box"
          :bounces="item" scroll-snap="edge">
    <p class="item-body">bounces: {{item}}</p>
    <p class="slide-button">×</p>
  </scroll>
</scroll>
```

```js
export default {
  data: {
    items: ['none', 'start', 'end', 'edge']
  }
}
```

```css
.column-box {
  display: flex;
  flex-direction: column;
}

.row-box {
  display: flex;
  flex-direction: row;
}

.row-box > p {
  border-radius: 12px;
  text-align: center;
  margin: 8px;
  padding: 16px;
}

.item-body {
  background-color: #f0f0f0;
  width: 100%;
}

.slide-button {
  width: 30%;
  color: #ffffff;
  background-color: #f04040;
}
```

</glyphix>


::: note
目前 `bounces` 属性仅影响手势操作的回弹，但忽略了快速的惯性动画回弹。上面的示例使用了一种技巧来避免非预期行为：
- `.row-box` 使用边沿吸附策略（`snap-type="edge"`），以避免带回弹的手势动画。
- `.row-box` 的每个元素都不超过 `100%` 宽度，确保边沿吸附策略不会发生内部边界回弹。

这种技巧可以用于侧滑删除菜单等界面。
:::

`bounces` 属性也会起到和 [`weakGesture`](#weakgesture) 类似的作用。具体来说，当越过禁止回弹的边沿后会自动允许滚动手势事件冒泡传递。因此，无需同时设置 `bounces` 和 `weakGesture` 属性。

::: tip
`bounces` 和 `weakGesture` 的滚动手势冒泡行为是“相反”的，例如 `end` 模式回弹策略允许用户滚动过列表结束位置后的回弹，而这种策略会允许起始位置的滚动手势冒泡。这对应值为 `'start'` 的 `weakGesture`  属性效果。
:::

### `weakGesture` <decl type="'none' | 'start' | 'end' | 'edge'" get set />

设置 `scroll` 组件在哪些情况下会对滚动手势进行冒泡。默认情况下 `scroll` 对它响应的手势阻止冒泡，因此它的父级元素无法接收到使 `scroll` 滚动的手势。`weakGesture` 允许在拖拽到内容边界位置时对手势事件启用冒泡，从而使父级元素能够接收这些手势。

|    值     | 描述                                             |
| :-------: | ------------------------------------------------ |
| `'none'`  | 不对响应的手势事件进行冒泡。                     |
| `'start'` | 拖拽到内容起始位置后对响应的手势事件冒泡。       |
|  `'end'`  | 拖拽到内容结束位置后对响应的手势事件冒泡。       |
| `'edge'`  | 拖拽到内容起始或结束位置后对响应的手势事件冒泡。 |

如果页面的底层元素是一个水平的 `scroll` 组件，但是希望右滑手势能让页面返回，那么可以这样配置：
``` html
<scroll weak-gesture="start"> ... </scroll>
```
当用户滑动到 `scroll` 组件的头部之后继续右滑即可退出页面。

::: warning
该属性应该在组件初始化时设置并且不能改变，否则可能出现交互错误。
:::

### `scrollbar` <decl type="boolean" get set />

标记 `scroll` 组件是否要显示滚动条（默认不显示），仅支持垂直布局的 `scroll` 组件。`scrollbar` 属性必须是一个常量，不能用响应式属性修改，例如：
``` html
<scroll scrollbar>
  ...
</scroll>
```
将会创建一个带有滚动条的 `scroll` 组件。滚动条的效果请参考 [`setIndex`](#setindex) 方法的示例。

滚动条的样式由系统决定，例如在圆形屏幕上可能显示为弧形，而矩形屏幕上显示为直条状。

### `scrolled` <decl type="boolean" listen />

通过 `scrolled` 属性监听列表是否处于滚动状态。事件触发的属性值为 `true` 表示列表正在滚动，否则意味着列表已经停止滚动。

用户触摸产生的滚动操作和通过 `scroll` 属性来滚动都会触发 `scrolled` 事件。当列表从滚动状态停止时，`scrolled` 事件的参数值为 `false`。

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

调用 `setIndex()` 时必须保证 `scroll` 组件的所有元素都是静态的，否则会出现错误。

<glyphix id="components-scroll-setindex" height="360" width="400" title="setIndex 方法">

``` html
<div class="window">
  <scroll id="scroll"
          :scroll-snap="center ? 'center' : null"
          scrollbar>
    <p for="x in 50" class="item">Item {{ x }}</p>
  </scroll>
  <div class="controls">
    <button on:click="setIndex('smooth')">smooth</button>
    <button on:click="setIndex('instant')">instant</button>
    center <switch ::value="center" />
  </div>
</div>
```

``` js
import prompt from '@system.prompt'

export default {
  data: { center: false },
  setIndex(behavior) {
    let el = this.$element('scroll')
    let index = parseInt(Math.random() * 50)
    prompt.showToast({message: `${behavior}ly set index to ${index}`})
    el.setIndex({ index: index, behavior: behavior })
  }
}
```

``` css
.window {
  display: flex;
  flex-direction: column;
}

scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  flex: 1;
}

.item {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px 5px;
  border-radius: 16px;
  margin: 8px;
}

.controls {
  display: flex;
  align-items: center;
  color: #404040;
}

button {
  color: #fafafa;
  background-color: #adadad;
  border-radius: 12px;
  padding: 4px 10px;
  margin-left: 16px;
  margin-bottom: 16px;
  flex: 1;
  margin: 8px;
  padding: 8px;
  text-align: center;
}
```

</glyphix>

### `scrollTo`
<decl method><pre>
(options: {
  left?: number,
  top?: number,
  behavior?: 'instant' | 'smooth'
}): void
</pre></decl>

将内容滚动到指定的位置。`options` 参数属性的作用为：
- `left`：指定内容沿 y 轴滚动的位置，忽略 `left` 或者 scroll 组件具有垂直布局时不会进行 y 轴上的滚动。
- `top`：指定内容沿 x 轴滚动的位置，忽略 `top` 或者 scroll 组件具有水平布局时不会进行 x 轴上的滚动。
- `behavior`：指定滚动的过渡效果，`'instant'`（默认值）表示直接跳转到目标位置并没有过渡效果，而 `'smooth'` 会平滑滚动并产生过渡效果。

`scrollTo` 方法会忽略元素的吸附效果。

### `scrollBy`
<decl method><pre>
(options: {
  left?: number,
  top?: number,
  behavior?: 'instant' | 'smooth'
}): void
</pre></decl>

将内容滚动一段距离。与 [`scrollTo()`](#scrollTo) 不同，`scrollBy()` 是相对于当前的内容位置进行滚动。`options` 参数属性的作用为：
- `left`：指定内容沿 y 轴滚动的距离，忽略 `left` 或者 scroll 组件具有垂直布局时不会进行 y 轴上的滚动。
- `top`：指定内容沿 x 轴滚动的距离，忽略 `top` 或者 scroll 组件具有水平布局时不会进行 x 轴上的滚动。
- `behavior`：指定滚动的过渡效果，`'instant'`（默认值）表示直接跳转到目标位置并没有过渡效果，而 `'smooth'` 会平滑滚动并产生过渡效果。

`scrollBy` 方法会忽略元素的吸附效果。

## CSS 规范

### 布局方向控制

`scroll` 组件的滚动方向由其布局方式来决定，使用流式布局（默认布局）或者 `column` 方向的 flex 布局时元素沿垂直方向布局，列表可以垂直滚动；而使用 `row` 方向的 flex 布局时元素沿水平方向布局，列表可以水平滚动。

<glyphix id="components-scroll-layout" height="360" width="740" title="布局方式控制滚动方向">

``` html
<div>
  <scroll>
    <p for="20">vertical scroll</p>
  </scroll>
  <!-- 用于占位元素，因为 flex 布局现在还不支持 gap -->
  <div style="width: 20px"></div>
  <scroll style="display: flex; flex-direction: row;">
    <p for="20">horizontal<br>scroll</p>
  </scroll>
</div>
```

``` css
div {
  display: flex;
}

scroll {
  background-color: #f0f0f0;
  flex: 1;
}

p {
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px;
  margin: 4px;
  border-radius: 16px;
}
```

</glyphix>

### `padding` 和 `overflow` <version-badge since="0.9" />

默认情况下（`overflow: clip`），`scroll` 组件的内边距会直接裁剪可视区域。当内容发生滚动后，内边距区域也总是不可见的。设置 `overflow: visible` 可以让内边距区域在内容滚动时也保持可见。

<glyphix id="components-scroll-padding-overflow-visible" height="360" width="740" title="overflow: visible 的内边距">

``` html
<div>
  <scroll :index="2">
    <p for="20">overflow: clip</p>
  </scroll>
  <!-- 用于占位元素，因为 flex 布局现在还不支持 gap -->
  <div style="width: 20px"></div>
  <scroll style="overflow: visible;" :index="2">
    <p for="20">overflow: visible</p>
  </scroll>
</div>
```

``` css
div {
  display: flex;
}

scroll {
  padding: 20px;
  background-color: #f0f0f0;
  flex: 1;
}

p {
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px;
  margin: 4px;
  border-radius: 16px;
}
```

</glyphix>

即便设置 `overflow: visible`，`scroll` 也会将内容裁剪到 padding-box，而不是允许其超出该范围，这和 `div` 之类的常规元素不同。这是因为 `scroll` 的滚动行为和布局机制需要保证内容在一个确定的区域内进行滚动，而不是允许内容无限制地扩展到外部区域。

`div` 等普通容器在类似的 `overflow: visible` 的情况下，内容可以超出整个 `div` 的范围（如红色的 `border` 之外）：

<glyphix id="components-scroll-overflow-div" height="360" width="360" title="div 的 overflow: visible">

``` html
<div style="overflow: visible;">
  <p for="20">div {overflow: visible}</p>
</div>
```

``` css
div {
  display: flex;
  flex-direction: column;
  padding: 20px;
  margin-bottom: 100px;
  border: 2px solid red;
  background-color: #f0f0f0;
}

p {
  background-color: #bdbdbd;
  text-align: center;
  padding: 8px;
  margin: 4px;
  border-radius: 16px;
  flex-shrink: 0;
}
```

</glyphix>

#### i18n 场景的推荐设置

在 i18n（国际化）场景中，`scroll` 内的文本可能需要溢出以避免可能的截断。对于这种情况，推荐的设置是 `overflow: visible`，以允许[文本溢出](/framework/application/i18n.md#文本溢出)内容在滚动时超出 `scroll` 的内容边界，以尽可能利用空间来显示文本。

#### 和 HTML/CSS 规范的关系

`scroll` 在设置 `overflow: visible` 时的行为与 HTML/CSS 规范中的 `div { overflow-y: scroll; }` 类似，此时的 padding 可以在滚动中保持内容可见，例如这样的 CSS：

```css
div {
  padding: 20px;
  overflow-y: scroll;
}
```

会得到如下效果，即滚动时 padding 区域不会裁剪内容：

<div style="padding: 20px; background-color: var(--vp-c-grey-bg); overflow-y: scroll; height: 100px; width: 200px; border: 2px dotted red; font-family: sans-serif;">
  Michaelmas term lately over, and the Lord Chancellor sitting in Lincoln's Inn Hall.
  Implacable November weather. As much mud in the streets as if the waters had but
  newly retired from the face of the earth.
</div>

HTML 的 `div` 没有直接对应于 `scroll` 在 `overflow: clip` 时的行为。
