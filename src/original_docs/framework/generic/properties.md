---
icon: xml
---
# 属性和事件

本节介绍所有原生组件都提供的通用属性接口以及事件。

## 属性列表

### 通用属性

#### `top` <decl type="number" get set listen />

组件顶部相对于父级原生组件的位置，单位为像素。此属性实际上是内联样式中 `top` 属性的简写，更多的使用方法详见[组件位置操作](#组件位置操作)。

读取或监听 `top` 属性时会得到组件已计算的位置，也及时布局后的实际测量值。

#### `left` <decl type="number" get set listen />

组件左侧相对于父级原生组件的位置，单位为像素。此属性实际上是内联样式中 `left` 属性的简写，更多的使用方法详见[组件位置操作](#组件位置操作)。

读取或监听 `left` 属性时会得到组件已计算的位置，也及时布局后的实际测量值。

#### `width` <decl type="number" get set listen />

组件的宽度。设置 `width` 属性时，会更新内联样式中的 [`width`](styles.md#width) 属性。由于 CSS 的宽度采用 border-box 模式，实际存储的样式值会自动附加上元素当前的 `padding` 和 `border` 尺寸，从而保证布局后的内容宽度与设置值一致。

读取或监听 `width` 属性时会得到布局计算后的内容宽度，不包含 `padding` 和 `border`。

#### `height` <decl type="number" get set listen />

组件的高度。设置 `height` 属性时，会更新内联样式中的 [`height`](styles.md#height) 属性。由于 CSS 的高度采用 border-box 模式，实际存储的样式值会自动附加上元素当前的 `padding` 和 `border` 尺寸，从而保证布局后的内容高度与设置值一致。

读取或监听 `height` 属性时会得到布局计算后的内容高度，不包含 `padding` 和 `border`。

#### `show` <decl type="boolean" get set/>

设置组件是否可见。隐藏的组件不会显示，也不占据布局空间。

#### `quiescent` <decl type="boolean" get set/>

设置组件快照是否自动更新（静止快照）。如果组件通过快照显示，此属性的值为 `false` 时（默认值）组件内容更新时会立即刷新快照以更新视图，否则不会立即更新快照。将此属性设置为 `true` 可以提高 UI 性能，但会造成显示内容滞后。

下面的示例展示了 `quiescent` 属性的作用。界面中有两个 `p` 元素被放置在 `scroll` 容器内，且 `scroll` 容器开启了[快照模式](../../components/scroll.md#snapshot)，当用户滚动 `scroll` 组件时会对其中的元素截取快照。由于第一个 `p` 元素是普通快照模式而第二个 `p` 元素则为静止快照模式，因此滚动时只能观察到第一个 `p` 元素的内容更新。

<glyphix id="generic-properties-quiescent" height="200" title="懒快照">

``` html
<scroll snapshot scroll-snap="center">
  <p>normal snapshot {{ count }}</p>
  <p quiescent>quiescent snapshot {{ count }}</p>
</scroll>
```

``` css
scroll {
  display: flex;
  flex-direction: column;
  background-color: lightgray;
}

p {
  background-color: lightgreen;
  text-align: center;
  padding: 10px;
  margin: 10px;
}
```

``` js
export default {
  data: {
    count: 0
  },
  onReady(event) {
    setInterval(() => this.count++, 500)
  }
}
```

</glyphix>

#### `style` <decl type="string" set />

设置组件的内联样式。目前只支持带有 <badge type="info" text="内联" /> 标签的 [CSS 属性](./styles.md)。

#### `z-index` <decl type="number" get set />

`z-index` 属性设置元素的 Z 轴顺序，`z-index` 较大的重叠元素会覆盖较小的元素。该属性值会被 CSS 中的 [`z-index`](styles.md/#z-index) 属性覆盖。


#### `opacity` <decl type="number" get set />

指定组件的透明度，值范围是 $[0, 1]$，其中 $0$ 表示完全透明。和 CSS 属性 [`opacity`](styles.md#opacity) 效果相同。

::: warning
`opacity` 值会影响元素的绘制性能，详情请参考 [`opacity`](styles.md#opacity) CSS 属性的说明。
:::

#### `transform` <decl type="string" set />

设置组件的变换，等效于 CSS 的 [`transform`](styles.md#transform) 属性。

#### `disabled` <decl type="boolean" get set />

用于设置或获取组件的禁用状态。当属性值为 `true` 时，元素处于禁用状态，用户无法与其交互，元素将不响应任何手势（如点击、拖动等）。当属性值为**默认**的 `false` 时，组件处于可用状态，用户可以正常与其交互。

下面的示例演示了 `disabled` 属性的用法，同时还用 [`:disabled`](styles.md#disabled) CSS 伪类控制样式。该示例展示了 `div` 元素在普通状态下可以响应点击手势，但是在 `disabled` 状态下不响应任何手势。

<glyphix id="generic-properties-disabled" height="200" title="disabled 属性">

``` html
<div :disabled="disabled" on:click="onClick">
  {{disabled ? 'disabled' : 'normal'}} <switch />
</div>
```

``` css
div {
  background-color: lightgray;
  text-align: center;
  display: flex;
  justify-content: center;
}

/* :disabled 伪类可以控制元素在 disabled 状态下的样式 */
div:disabled {
  opacity: 0.5;
}
```

``` js
import prompt from '@system.prompt'

export default {
  data: {
    disabled: false
  },
  onInit() {
    setInterval(() => {
      this.disabled = !this.disabled
    }, 2000)
  },
  onClick() {
    prompt.showToast({ message: 'clicked!', duration: 250 })
  }
}
```

</glyphix>

### 通用事件

大部分原生组件都支持通用事件，它们可以用 [`on` 指令](../commands/on.md)进行监听。这些事件的值类型在[事件类型](#事件类型)节介绍。

#### `touchstart` <decl type="TouchEvent" listen />

用户开始触摸组件时触发 `touchstart` 事件。事件值是 [`TouchEvent`](#touchevent) 类型。

#### `touchmove` <decl type="TouchEvent" listen />

用户触点在组件上移动时触发 `touchmove` 事件，在移动过程中即使触点离开了当前原生组件的范围也会一直触发此事件。事件值是 [`TouchEvent`](#touchevent) 类型。

触摸状态从 `touchstart` 转换到 `touchmove` 存在一定的“移动死区”，如果用户触摸的滑动距离小于死区范围则不会触发 `touchmove`。移动死区范围因设备而异，下面的例子展示了移动死区。

<glyphix id="generic-properties-touchmove" height="200" title="移动死区">

``` html
<p on:touchstart="state = 'start'"
   on:touchmove="onTouchMove($event)"
   on:touchend="onTouchEnd">
  {{ `state: ${state} \ndead area: (${dx}, ${dy})` }}
</p>
```

``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```

``` js
export default {
  data: {
    state: null,
    dx: null,
    dy: null
  },
  onTouchMove(event) {
    if (!this.dx && !this.dy) {
      this.state = 'move'
      this.dx = event.touches[0].offsetX
      this.dy = event.touches[0].offsetY
    }
  },
  onTouchEnd() {
    this.state = 'end'
    this.dx = this.dy = null
  }
}
```

</glyphix>

#### `touchend` <decl type="TouchEvent" listen />

用户触点离开屏幕时会对之前触摸的原生组件发送 `touchend` 事件。事件值是 [`TouchEvent`](#touchevent) 类型。

#### `touchcancel` <decl type="TouchEvent" listen />

当原生组件的触摸被中断时触发 `touchcancel`。事件值是 [`TouchEvent`](#touchevent) 类型。有多种原因可能导致触摸中断，例如组件被隐藏或者触摸事件被其他元素强制响应等。

#### `click` <decl type="ClickEvent" listen />

当原生组件被点击并松手时触发 `click` 事件。事件值是 [`ClickEvent`](#clickevent) 类型。

<glyphix id="generic-properties-click" height="100">

``` html
<p on:click="click = JSON.stringify($event)">
  {{ click }}
</p>
```

``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```

``` js
export default {
  data: {
    click: null
  }
}
```

</glyphix>

#### `longpress` <decl type="LongPressEvent" listen />

当原生组件被长时间按压时触发 `longpress` 事件。事件值是 [`LongPressEvent`](#longpressevent) 类型。下面的可交互示例展示了 `longpress` 和其他事件的触发时机：

<glyphix id="generic-properties-longpress" height="100">

``` html
<p on:touchstart="state = 'touching...'"
   on:longpress="state = `longpress: ${JSON.stringify($event)}`"
   on:click="state = 'clicked.'">
  {{ state }}
</p>
```

``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```

``` js
export default {
  data: {
    state: null
  }
}
```

</glyphix>

`longpress` 事件的触发时机和持续时间因设备而异，通常在按压 $500 \rm ms$ 后触发。不同于 [`click`](#click) 事件，`longpress` 在按压期间触发，而不是松手时触发。对于上面的示例，你会发现：
- 当按压时间小于长按触发时间时，松手后会触发 `click` 事件；
- 按压的足够久时会触发 `longpress` 事件，松手后触发 `click` 事件（显示为“clicked.”状态）；
- 按压过程中发生移动将不会触发 `longpress` 或 `click` 事件。

#### `swipe` <decl type="SwipeEvent" listen />

当组件被快速扫动时触发 `swipe` 事件。事件值是 [`SwipeEvent`](#swipeevent) 类型。

<glyphix id="generic-properties-swipe" height="250" >

``` html
<p on:swipe="onSwipe($event)">
  {{ swipe }}
</p>
```

``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```

``` js
export default {
  data: {
    swipe: null
  },
  onSwipe(event) {
    this.swipe = event.direction
    event.strongResponse()
  }
}
```

</glyphix>

#### `keydown` <decl type="KeyEvent" listen />

当按键按下时触发此事件。`keydown` 和 `keyup` 事件用于捕获实体按键的操作。要想捕获事件，原生组件必须处于焦点状态，页面的根元素总是会自动获取焦点，因此下面的代码可以捕获到 `keydown` 和 `keyup` 事件：
``` html
<!-- 假设这是页面的根元素 -->
<div on:keydown="console.log($event)" on:keyup="console.log($event)">
  ...
</div>
```
事件值类型请参考 [`KeyEvent`](#keyevent)。

手表设备通常会注册[默认按键处理程序](/api/system-internal.md#setdefaultkeyhandler)，因此应用代码即使不响应这类事件也可以进行交互（例如按下 Power 键时一些手表会返回上一页）。要想阻止默认按键响应，可使用 `KeyEvent` 对象的 `stopPropagation()` 方法来阻止冒泡。

#### `keyup` <decl type="KeyEvent" listen />

当按键抬起时触发此事件。更多内容请参考 [`keydown`](#keydown) 事件。

#### `wheel` <decl type="WheelEvent" listen />

当用户操作旋转滚轮时触发 `wheel` 事件。滚轮设备包括手表的旋转表冠，或者鼠标滚轮等。想要捕获此时间，原生组件必须处于焦点状态，页面的根元素总是会自动获取焦点，因此下面的代码可以捕获到 `wheel` 事件：
``` html
<!-- 假设这是页面的根元素 -->
<div on:wheel="console.log($event)">
  ...
</div>
```
事件值类型请参考 [`WheelEvent`](#wheelevent)。

## 事件类型

### `BaseEvent`

`BaseEvent` 事件对象提供一些控制事件传递的方法，其原型是：
``` ts
interface BaseEvent {
  strongResponse(): void, // 强制响应事件
  stopPropagation(): void // 停止事件冒泡
}
```

### `TouchEvent`

`TouchEvent` 事件对象的原型为：
``` ts
interface TouchEvent extends BaseEvent {
  isTarget: boolean, // 事件目标是否为当前组件
  touches: { // 本事件所有的触摸点数据
    clientX: number, // 触摸点相对于目标组件内容区域的 x 坐标
    clientY: number, // 触摸点相对于目标组件内容区域的 y 坐标
    offsetX: number, // 触摸点在触摸过程中 x 方向的位移量
    offsetY: number  // 触摸点在触摸过程中 y 方向的位移量
  }[];
}
```

### `ClickEvent`

`SwipeEvent` 事件对象的原型是：
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // 事件目标是否为当前组件
  clientX: number, // 点击触摸点相对于目标组件内容区域的 x 坐标
  clientY: number // 点击触摸点相对于目标组件内容区域的 y 坐标
}
```

### `LongPressEvent`

`LongPressEvent` 事件对象的原型是：
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // 事件目标是否为当前组件
  clientX: number, // 长按触摸点相对于目标组件内容区域的 x 坐标
  clientY: number // 长按触摸点相对于目标组件内容区域的 y 坐标
}
```

### `SwipeEvent`

`SwipeEvent` 事件对象的原型是：
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // 事件目标是否为当前组件
  direction: 'left' | 'right' | 'up' | 'down' // 扫动方向
}
```

### `KeyEvent`

`KeyEvent` 对象描述了用户对实体按键的交互事件，该类型用于元素 [`keydown`](#keydown) 和 [`keyup`](#keyup) 的事件属性。`KeyEvent` 事件对象的原型是：
``` ts
interface KeyEvent  {
  type: 'keydown' | 'keyup', // 按键事件的类型
  key: string, // 按键名称
  timestamp: number, // 按键事件上报的时间戳，单位是毫秒
  stopPropagation(): void // 调用此方法可以阻止事件冒泡
}
```

目前支持以下按键名称：
- `'Power'`：手表的电源键；
- `'Fn'`：手表的功能键；
- 其他可打印字符的按键以单个字符构成键名，例如字母 `'A'`、减号 `'-'` 等。

### `WheelEvent`

`WheelEvent` 对象描述了用户对旋转滚轮的交互事件，该类型用于元素 [`wheel`](#wheel) 的事件属性。`WheelEvent` 事件对象的签名是：
``` ts
interface WheelEvent {
  deltaY: number, // 滚轮在 y 方向的滚动增量
  stopPropagation(): void // 调用此方法可以阻止事件冒泡
}
```

与 Web 的 [wheel event](https://developer.mozilla.org/en-US/docs/Web/API/Element/wheel_event) 不同，Glyphix 中的 `WheelEvent` 目前只包含 `deltaY` 属性。

## 事件响应机制

### 事件冒泡

触摸和手势事件支持冒泡（bubbling）。冒泡是指当事件发生在一个元素上，它会首先执行该元素上的处理程序，然后执行其父元素上的处理程序，然后一直向上到其他祖先上的处理程序。下面的例子中，绿色的 `p` 组件和灰色的 `div` 组件都监听了触摸事件，其中在点击 `p` 组件时会观察到 `p` 组件和 `div` 组件都能接收到事件。

<glyphix id="generic-event-bubbling" height="250" title="触摸事件冒泡">

``` html
<div on:touchstart="onTouch('div', $event)"
     on:touchmove="onTouch('div', $event)"
     on:touchend="onRelease('div', $event)">
  <p on:touchstart="onTouch('p', $event)"
     on:touchmove="onTouch('p', $event)"
     on:touchend="onRelease('p', $event)">
    {{ `touchs: ${touchs.div ? 'div' : '-'} ${touchs.p ? 'p' : '-'}, target: ${target}` }}
  </p>
</div>
```

``` css
div {
  display: flex;
  flex-direction: column;
  background-color: lightgray;
  justify-content: space-around;
}

p {
  background-color: lightgreen;
  text-align: center;
  height: 150px;
}
```

``` js
export default {
  data: {
    touchs: { div: false, p: false },
    target: null
  },
  onTouch(name, event) {
    this.touchs[name] = true
    // isTarget 属性可以区分事件的目标是否是当前监听该事件的组件
    if (event.isTarget)
      this.target = name
  },
  onRelease(name, event) {
    this.touchs[name] = false
    if (event.isTarget)
      this.target = null
  }
}
```

</glyphix>

在 Glyphix 中，只有本文档中的触摸和手势事件会冒泡。目前不能在 JavaScript 代码中进行事件捕获。

### 阻止事件冒泡

使用 `BaseEvent` 的 `stopPropagation()` 方法可以阻止事件向父级冒泡。

### 强响应事件

在 Glyphix 中触摸或手势事件有两种响应优先级：强响应和弱响应。当一个事件同时有多个待响应的目标时强响应的优先级高于弱响应。假设界面上存在 3 级父子元素：`A -> B -> C`，其中 `C` 对事件是弱响应的，而 `B` 是强响应，那么事件将派发给 `B` 之后就不会再派发到 `C` 了。一个原本强响应事件的元素在改为弱响应之后会重新派发事件。

[通用事件](#通用事件)中的触摸和手势事件默认是弱响应的。在下面的例子中，一个绿色的 `p` 组件被放置在灰色的 `scroll` 内，并且监听了 `p` 组件的所有触摸事件。由于 `scroll` 默认强响应上下滑动的手势，弱响应左右滑动手势，且不响应其他手势，所以在操作中可以观察到：
- 点击 `p` 组件时会触发 `touchstart` 事件，松手时触发 `touchend` 事件；
- 横向拖拽 `p` 组件时会触发 `touchmove` 事件；
- 上下拖拽 `p` 组件时，由于父级 `scroll` 组件对上下滑动有强响应，而模板代码中 `p` 组件对 `touchmove` 只有弱响应，所以上下滑动会被 `scroll` 组件响应，`p` 组件会收到 `touchcancel` 事件。

<glyphix id="generic-event-strong-response-1" height="250" title="强响应事件">

``` html
<scroll>
  <p on:touchstart="state = 'touchstart'"
     on:touchmove="state = 'touchmove'"
     on:touchend="state = 'touchend'"
     on:touchcancel="state = 'touchcancel'">
    {{ `p.state: ${state}` }}
  </p>
</scroll>
```

``` css
scroll {
  background-color: lightgray;
}

p {
  background-color: lightgreen;
  text-align: center;
  height: 150px;
  margin: 50px;
}
```

``` js
export default {
  data: {
    state: null
  }
}
```

</glyphix>

很多原生组件的默认手势事件处理机制是强响应的。使用 `BaseEvent` 对象的 `strongResponse()` 方法可以在 JavaScript 代码中指定事件为强响应模式。下面的例子中外层灰色的 `div` 组件会强响应手势，因此即使触摸内部的 `p` 元素，在手势开始之后事件会只派发给 `div` 元素。

<glyphix id="generic-event-strong-response-2" height="250" title="强响应事件">

``` html
<div on:touchstart="onTouch('div', 'start', $event)"
     on:touchmove="onTouch('div', 'move', $event)"
     on:touchend="onTouch('div', 'end', $event)"
     on:touchcancel="onTouch('div', 'cancel', $event)">
  <p on:touchstart="onTouch('p', 'start', $event)"
     on:touchmove="onTouch('p', 'move', $event)"
     on:touchend="onTouch('p', 'end', $event)"
     on:touchcancel="onTouch('p', 'cancel', $event)">
    {{ `div state: ${touchs.div}, p state: ${touchs.p}, target: ${target}` }}
  </p>
</div>
```

``` css
div {
  display: flex;
  flex-direction: column;
  background-color: lightgray;
  justify-content: space-around;
}

p {
  background-color: lightgreen;
  text-align: center;
  height: 150px;
}
```

``` js
export default {
  data: {
    touchs: { div: null, p: null },
    target: null
  },
  onTouch(name, state, event) {
    console.log(name, state, event.isTarget)
    this.touchs[name] = state
    // isTarget 属性可以区分事件的目标是否是当前监听该事件的组件，
    // 如果是 cancel 事件就不记录目标。
    if (event.isTarget && state != 'cancel')
      this.target = name
    if (name == 'div')
      event.strongResponse()
  }
}
```

</glyphix>

### 页面的默认事件处理

页面默认会弱响应手势事件并且阻止事件冒泡，因此手势事件无法透过页面进行派发和传递。另外页面会在收到向右的 touchmove 手势时退出，开发者也可以拦截手势以禁用此特性。

具体的做法是监听页面组件的 `touchmove` 手势并阻止冒泡：
``` html
<!-- 这个 div 是页面的根组件 -->
<div on:touchmove="$event.stopPropagation()">
  ...
</div>
```
这样，这个页面就无法通过右滑操作返回，但是可以通过按下实体 Power 键返回。要先阻止用户按键返回，可以使用以下方式：
``` html
<!-- 这个 div 是页面的根组件 -->
<div on:keydown="onKeyup">
  ...
</div>
```

``` js
export default {
  onKeyup(event) {
    // 判定键值为 'Power' 时禁止事件冒泡以阻止页面退出
    if (event.key == 'Power')
      event.stopPropagation()
  }
}
```

::: warning
谨慎替代页面的默认事件处理机制，避免出现用户无法返回页面的情况。
:::

::: tip
之前的版本中，通过 `swipe` 手势事件来阻止页面的默认返回行为，但是在 0.6.4 版本中已经废弃了这种方式。请使用上述的 `touchmove` 事件处理来替代。这一调整是由于页面的交互式返回动效（即跟手退出）完全无法兼容 `swipe` 阻止页面返回的语义导致的。
:::

## 使用技巧

### 组件位置操作

利用原生组件的 `top` 和 `left` 属性可以轻松地修改组件位置：
``` html
<div :top="40" :left="20"> ... </div>
```
`top` 和 `left` 实际上是同名 CSS 属性的简写，因此它们只会在绝对布局中生效，可以通过以下 CSS 来实现：
``` css
div {
  position: absolute;
}
```

然后你可以使用响应式的属性来修改组件的位置。下面的例子展示了结合 [`transition` 修饰符](/framework/component/prop-modifier.md#transition-修饰符)所实现的带动画的随机组件位置移动。

<glyphix id="generic-widget-position" height="250" title="随机组件位置">

``` html
<div id="pane">
  <p id="tile" :top="top" :left="left"
     top.transition left.transition>
    Tile
  </p>
</div>
```

``` css
div {
  background-color: lightgray;
}

p {
  /* 要使用组件的 top / left 属性就必须是绝对定位 */
  position: absolute;
  background-color: lightgreen;
  text-align: center;
  width: 3rem;
  height: 3rem;
  border: 4px solid red;
  border-radius: 10%;
}
```

``` js
export default {
  data: {
    top: 0,
    left: 0
  },
  timer: null,
  onReady() {
    // 获取组件对象，位置范围不应超出 #pane 容器
    const pane = this.$element("pane")
    const tile = this.$element("tile")
    const width = pane.width - tile.width
    const height = pane.height - tile.height
    this.timer = setInterval(() => {
      this.top = Math.random() * height
      this.left = Math.random() * width
    }, 2000)
  },
  onDestroy() {
    clearInterval(this.timer)
  }
}
```

</glyphix>

本示例每隔两秒钟随机设置一次 `#tile` 组件的位置，且范围不超出容器 `#pane` 的边界。默认的 `transition` 修饰符会播放 $1$ 秒钟的过渡动画。
