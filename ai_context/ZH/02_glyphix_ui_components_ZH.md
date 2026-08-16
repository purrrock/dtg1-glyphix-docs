# Context File: 02_glyphix_ui_components_ZH.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/original_docs/components/list-item.md

# list-item

`list` 的子组件，用来展示列表具体 item，支持子组件及布局，但是不支持滚动。

::: tip
Glyphix 并不提供和快应用一样的 list 容器组件，而是用 [`scroll`](scroll.md) 实现滚动容器。同样的，也不需要使用 `list-item` 组件，请直接使用 [`div`](div.md) 或者其他任何组件作为列表项元素。
:::


============================================================
FILE_PATH: src/original_docs/components/collapsible-header.md

# collapsible-header

`collapsible-header` 组件用于为滚动列表添加一个可以折叠的标题栏。这种效果用于为手表类设备提供一种节约视图区域的交互效果，提升用户体验。

::: warning
<experimental /> 这是一个实验性组件，不要用本文档中没有示范的方法来使用它。
:::

## 属性

本组件支持[通用属性](/framework/generic/properties.md)，没有专用属性。

## 使用方法

`collapsible-header` 组件中必须要有两个子组件，否则可能产生非预期的效果。具体示例如下：

```html
<collapsible-header>
  <p>这是可折叠的标题</p>
  <scroll> ... </scroll>
</collapsible-header>
```

其中第一个子元素是一个可折叠的标题，而第二个元素必须是 [`scroll`](/components/scroll.md) 等可滚动的容器。下面是一个具体的例子：

<glyphix id="components-collapsible-header-1" height="360" width="360" title="可折叠标题栏">

```html
<collapsible-header>
  <p class="title-bar" on:click="clickTitle">TITLE BAR</p>
  <scroll scroll-snap="center" deformation="fisheye">
    <p for="x in 20" class="item">item {{ x + 1 }}</p>
  </scroll>
</collapsible-header>
```

```js
import prompt from "@system.prompt";

export default {
  clickTitle() {
    prompt.showToast({ message: "title clicked" });
  }
}
```

```css
.title-bar {
  margin: 56px auto auto;
  transparent: true;
  font-size: 1.5rem;
}

.item {
  height: 33.3%;
  background-color: #ddd;
  border-radius: 20%;
  margin: 8px;
  transparent: true;
  padding: 12px;
  text-align: center;
}
```

</glyphix>

### 原理说明

`collapsible-header` 接受两个子组件，其中第一个是可折叠的标题栏，第二个必须要是类似 `scroll` 的可滚动组件。`collapsible-header` 会组合这两个组件，并在列表滚动时操纵可折叠的标题栏的显示效果。

可以使用类似流式布局的方法来控制标题栏的位置，例如：

```css
/* 元素的顶部间距为 48px，左右居中，适用于圆形屏幕。 */
margin: 48px auto auto;
/* 元素左侧和顶部间距为 12px，适用于方型屏幕。 */
margin: 12px auto auto 12px;
```

根据实际需求将上述样式设置给标题栏元素即可实现特定的对齐效果。还可以使用包含子元素的复杂组件作为标题栏，例如使用一个包含返回按钮和页面标题文本的组件。但要注意，在点击标题栏时，点击事件可以同时发送到滚动列表和标题栏，如果存在冲突，可以通过阻止事件冒泡来解决。

### 注意事项

必须为 `collapsible-header` 按照上述要求提供两个子组件，且不要搞错顺序。另外，由于可折叠的标题栏和底层的滚动列表是堆叠显示的，这可能让列表的第一个元素和标题栏重叠显示。必要时，开发者应考虑某种占位方式来避免重叠，且 `scroll` 的居中[吸附模式](/components/scroll.md#scrollsnap)（`scroll-snap="center"`）也可以避免重叠。


============================================================
FILE_PATH: src/original_docs/components/image-animator.md

# image-animator

`image-animator` 组件用于播放一组图片序列帧动画，组件默认是行内元素。

<glyphix id="image-animator-1" height="190" width="360" >

```html
<div class="flex-column">
  <div class="frame-box">
    <image-animator :images="frames" :play="play" :duration="100" />
  </div>
  <div>
    <button on:click="play = 'start'">start</button>
    <button on:click="play = 'pause'">pause</button>
    <button on:click="play = 'stop'">stop</button>
  </div>
</div>
```

```js
export default {
  data: {
    play: "stop",
  },
  frames: Array.from({ length: 60 }, (_, i) => `/assets/planet-${i}.png`),
};
```

```css
.flex-column {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.frame-box {
  border: 2px solid lightgray;
  border-radius: 8px;
  padding: 8px;
}

button {
  border-radius: 8px;
  background-color: #dee2e6;
  margin: 8px;
  padding: auto 12px;
}

button:active {
  opacity: 0.5;
}
```

</glyphix>

## 属性

### `images` <decl type="string[]" set />

设置序列帧图片集合。`images` 的每个元素都是该帧图片的路径或者 URI。通常，每帧图片的尺寸是一致的。

支持 PNG 或者 JPEG 格式的图片。

如果序列帧不会变化，那么建议将其作为非响应式属性以节省内存：

```js
export default {
  // frames 是组件的非响应式属性
  frames: [
    "/assets/sprite-1.png",
    "/assets/sprite-2.png",
    "/assets/sprite-3.png",
  ],
};
```

这样做的好处是多个组件对象会公用同一个 `frames` 数组对象（响应式属性会拷贝到每一个组件实例）。仅当序列帧确实需要响应式特性时，才应该将其写在 `data` 对象中。

如果序列帧是按顺序编码的，那么可以使用这种技巧来简化序列帧数组的创建：

```js
export default {
  // 从 0 开始编号的 4 帧序列帧
  frames: Array.from({ length: 4 }, (_, i) => `/assets/sprite-${i}.png`),
  // 或者，从 1 开始编号的 4 帧序列帧
  frames: Array.from({ length: 4 }, (_, i) => `/assets/sprite-${i + 1}.png`),
};
```

在组件模板中将 `frames` 数组传递给 `images` 属性以指定序列帧，从而播放动画：

```html
<image-animator :images="frames" play :duration="100" />
```

::: note
`images` 属性现在还不支持快应用的 `ImageFrame` 结构，因此你不能使用 `[{ src: '...' }, ...]` 这样的帧集合定义。
:::

### `duration` <decl type="number" get set />

指定每一帧的播放时长，单位为毫秒。

### `play` <decl type="'start' | 'pause' | 'stop'" get set listen />

设置播放状状态，支持开始、暂停、结束状态。`image-animator` 在初始时处于 `stop` 状态，因此会自动停在 [`images`](#images) 的第一帧位置。

|    值     | 描述                   |
| :-------: | ---------------------- |
| `'start'` | 从当前帧开始播放。     |
| `'pause'` | 暂停播放并显示当前帧。 |
| `'stop'`  | 停止播放并显示第一帧。 |

如上所示，`play` 只支持 `'start`、`'pause'` 或者 `'stop'` 三种枚举值。但是下面的技巧可以用来自动播放动画：

```html
<image-animator :images="frames" play :duration="100" />
```

即直接写一个没有值的 `play` 属性，它是等效于 `:play="true"` 的[隐式属性](/framework/component/template.md#隐式属性值)写法。`true` 这种布尔类型总是会转换为默认的 `'start'` 枚举值。这种写法非常适用于需要自动播放序列帧动画的场景。

### `iteration` <decl type="number" set />

设置设置 `images` 中所有序列帧的重复播放次数，当达到次数上限时将自动切换到 `'pause'` 模式。`0` 表示无限次数播放。

## 继承的属性

`image-animator` 具有和 `image` 相同的[继承属性](/components/image.md#继承的属性)行为。

## CSS 说明

`image-animator` 具有和 `image` 相同的 [CSS 行为](/components/image.md#css-说明)。


============================================================
FILE_PATH: src/original_docs/components/div.md

# div

`div` 是最基本的容器组件。`div` 支持子组件及布局，但是不支持滚动（内容超出边界会直接裁剪）。如果想要内容滚动，请使用 [scroll](scroll) 组件。

## 注意事项

### 文本显示

`div` 组件不能直接用于显示文本，而是要使用 `p` 等文本组件来显示文本，例如：

```html
<!-- 错误的写法，不会显示文本 -->
<div>text content.</div>
<!-- 正确的写法 -->
<p>text content.</p>
```

不过如果 `div` 内有多个子元素，那么可以将文本作为它的子元素：

```html
<div>
  first element,
  <span style="color: #f0f">second element.</span>
</div>
```

<Glyphix id="components-div-text-element" height="48" width="360" inline >

```html
<div>
  first element,
  <span style="color: #f0f">second element.</span>
</div>
```

</Glyphix>


============================================================
FILE_PATH: src/original_docs/components/slider-arc.md

# slider-arc

弧形滑动选择器，默认是块级元素，暂不支持样式修改。

## 属性

继承 [slider](slider) 组件的属性

### `arc-center` <decl type="{ x: number, y: number }" set />

设置圆弧圆心的位置。

### `start-angle` <decl type="number" set />

设置圆弧开始角度，默认值：$-90$。

### `progress-angle` <decl type="number" set />

设置圆弧最大转动角度，默认值：$360$，一周圆弧。

### `arc-width` <decl type="number" set />

设置圆弧宽度。

### `arc-radius` <decl type="number" set />

设置圆弧半径。


============================================================
FILE_PATH: src/original_docs/components/progress-arc.md

# progress-arc

`progress-arc` 组件用于显示环形进度条，默认为块级元素。

## 属性

### `max` <decl type="number" set />

最大进度值，[`value`](#value) 属性不会大于它。

### `min` <decl type="number" get setet />

最小进度值，[`value`](#value) 属性不会小于它。

### `value` <decl type="number" get set listen />

设置进度值。进度的显示比例取决于 `value` 属性在 `min` 到 `max` 区间中的比例，同时显示比例会限制在$0\% \sim 100\%$ 之间。`value` 值是一个整数，如果设置浮点值则只会截取整数部分。

### `busy` <decl type="boolean" get set />

设置 `progress-arc` 组件是否处于忙状态，在忙状态下会显示一个加载动画，而不是显示 `value` 属性的值。下面的示例演示了如何用一个圆形进度条来模拟加载动画：

<glyphix id="components-progress-arc-busy" height="100" width="300" title="模拟加载动画">

``` html
<progress-arc busy :startAngle="0" :stopAngle="360" />
```

</glyphix>

在这个例子中，进度条的开始角度和结束角度相差 $360^\circ$，此时通过 `busy` 属性可以显示典型的加载动画效果。

::: tip
只要进度条为环形就会显示固定的忙动画效果，起始和结束角度并没有影响。
:::

### `startAngle` <decl type="number" get set />

弧形进度条的起始角度，默认值为 $135$，更多的信息请参考[角度配置](#角度配置)章节。

### `stopAngle` <decl type="number" get set />

弧形进度条的结束角度，默认值为 $405$，更多的信息请参考[角度配置](#角度配置)章节。

## 使用说明

### 角度配置

与线性的 [`progress`](progress.md) 不同，弧形或者环形的进度条需要合理配置 `startAngle` 属性和 `stopAngle` 属性才能正常显示。这两个属性均使用角度制单位，在屏幕坐标系中，$0^\circ$ 指向水平向右的方向，即时钟 $3$ 点钟方向，并沿着顺时针方向增加，反之减小。

`progress-arc` 的显示是根据 `value` 在 $[\texttt{min}, \texttt{max}]$ 中的比例对角度范围进行线性插值。具体而言，用户会看到进度的高亮角度从 `startAngle` 开始，并到 `valueAngle` 结束：

$$
\begin{aligned}
  k &= \frac{\texttt{value} - \texttt{min}}{\texttt{max}-\texttt{min}}\\
  \texttt{valueAngle} &= (1-k)\texttt{startAngle} + k\cdot\texttt{stopAngle}
\end{aligned}
$$

因此，如果要显示一整圈的环形进度条，需要让起始和结束角度相差 $360^\circ$，即使这两个角度从视觉上来看是相同的。另外，起始角度也可以大于结束角度，这将反转进度的方向。

下面的示例展示了多种角度配置的实际效果，请注意第二个示例展示了反向的进度显示技巧。

<glyphix id="components-progress-arc-angles" height="120" width="720" title="角度配置示例">

``` html
<div>
  <p class="progress-label">{{value}}%</p>
  <stack>
    <p>default</p>
    <progress-arc :value="value" />
  </stack>
  <stack>
    <p>405~135</p>
    <progress-arc :startAngle="405" :stopAngle="135" :value="value" />
  </stack>
  <stack>
    <p>-45~225</p>
    <progress-arc :startAngle="-45" :stopAngle="225" :value="value" />
  </stack>
  <stack>
    <p>0~360</p>
    <progress-arc :startAngle="0" :stopAngle="360" :value="value" />
  </stack>
  <stack>
    <p>-90~270</p>
    <progress-arc :startAngle="-90" :stopAngle="270" :value="value" />
  </stack>
</div>
```

``` js
export default {
  data: { value: 0 },
  onInit() {
    setInterval(() => {
      this.value = this.value + 5
      if (this.value > 100)
        this.value = 0
    }, 500)
  }
}
```

``` css
div {
  display: flex;
}

progress-arc {
  width: 200px;
  padding: 0 8px 0 8px;
  stroke-width: 0.5rem;
}

p {
  text-align: center;
  font-size: 0.7rem;
}

.progress-label {
  width: 3.5rem;
}
```

</glyphix>

## CSS 规范

### 尺寸计算

`progress-arc` 的显示尺寸由它的 `width` 和 `height` 属性决定。`progress-arc` 会占满较短的轴线，且弧形进度条的圆心为元素的中心。默认情况下，`progress-arc` 的尺寸可能和一个字符接近，这会导致非常怪异的显示效果，因此通常要在 CSS 中显式指定宽高，或使用其他合理的布局策略。

::: tip
最好为 `progress-arc` 组件指定一个合理的宽度和高度，否则它可能无法辨认。至少也应该设置 `width` CSS 属性，该组件的布局策略会自动使用 $1:1$ 宽高比。
:::

### CSS 属性

可以通过 CSS 来调整 `progress-arc` 组件的外观。

#### `stroke-width`

该属性指定 `progress-arc` 组件的弧形轮廓宽度。值类型为[长度](/framework/render/style-and-layout.md#长度)，不支持百分比单位。

::: tip
如果你希望 `progress-arc` 组件的绘制宽度和字体尺寸成一定的比例，建议使用 [`rem`](/framework/application/font-config.md#rem-字号单位) 长度单位，如 `0.15rem`。
:::

#### `color`

设置 `progress-arc` 高亮进度条的颜色，默认情况下会使用系统主题色。

#### `background-color`

设置 `progress-arc` 背景进度条的颜色，默认情况下会根据系统主题配置。

### CSS 伪元素

#### `value`



============================================================
FILE_PATH: src/original_docs/components/button.md

# button

按钮组件，默认为行内元素，当该组件被触碰到时，能够触发相应的事件。

## 属性

### `checkable`  <decl type="boolean" set />

设置为 `true` 时，表示一次触摸只响应一次状态改变，即：由按下转为抬起状态或由抬起转换为按下状态。并且按下状态 `press` 的监听值为 `true`、抬起为 `false`。

### `toggleable` <decl type="boolean" set />

设置为 `true` 时，表示 `press` 监听值是可以改变的，按下为 `true`，抬起为 `false`。

### `press` <decl type="boolean" get set listen />

设置 `press` 属性时，可改变组件的状态。也可以通过 `on` 指令监听组件的状态，默认情况下一次触摸完成，回调参数为 `ture`，可以配合 `checkable` `toggleable` 属性获取不同的监听值和状态。

## 功能限制

### `click` 事件失效

在不使用 `button` 组件时，通常通过 [`click`](/framework/generic/properties.md#click) 属性来监听任意原生组件的点击事件。但是这种方法通常不适用于 `button`。例如这样的代码：
```html
<button on:click="onOuterClick">
  <p on:click="onInnerClick">inner</p>
  outer button
</button>
```

```js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    // 阻止事件冒泡，以免外层按钮响应点击事件
    event.stopPropagation();
    console.log('inner click');
  }
}
```

<glyphix id="components-button-click-1" height="48" width="360" inline>

``` html
<button on:click="onOuterClick">
  <p on:click="onInnerClick">inner</p>
  outer button
</button>
```

``` css
button {
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}

button:active {
  opacity: 0.5;
}

p {
  border: 2px solid #444;
  padding: 0 10px;
}
```

``` js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    event.stopPropagation();
    console.log('inner click');
  }
}
```

</glyphix>

你可能期望点击 `"inner"` 文本时，能够触发 `onInnerClick` 方法，并阻止 `onOuterClick`。但你会发现并不是这样（最好打开浏览器的控制台查看日志）：`onInnerClick` 方法根本不会触发，只有外层 `button` 组件会响应点击，即：
- 点击`inner` 文本时，`inner click` 日志不会出现，只有 `outer click` 日志；
- `button` 按下时的交互被触发了（透明度降低）。

这就像点击外面的 `outer text` 一样。出现这种情况的原因是 `button` 组件会优先响应按下手势的整个生命周期（从按下到松手），而 `click` 事件在松手时触发。这意味着无论内层元素的 `click` 事件处理函数是否阻止冒泡都不能改变这种行为。

#### 解决方法

要解决这一问题，应该监听外层 `button` 的 `press` 事件，并监听内层元素的 `touchstart` 事件：

```html
<button on:press="onOuterClick">
  <p on:touchstart="onInnerClick">inner</p>
  outer button
</button>
```

```js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    // 阻止事件冒泡，以免外层按钮响应点击事件
    event.stopPropagation();
    console.log('inner click');
  }
}
```

<glyphix id="components-button-click-2" height="48" width="360" inline>

``` html
<button on:press="onOuterClick">
  <p on:touchstart="onInnerClick">inner</p>
  outer button
</button>
```

``` css
button {
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}

button:active {
  opacity: 0.5;
}

p {
  border: 2px solid #444;
  padding: 0 10px;
}
```

``` js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    event.stopPropagation();
    console.log('inner click');
  }
}
```

</glyphix>

尝试上面的示例，就会发现点击 `inner` 文本时只有 `onInnerClick` 方法被触发，`onOuterClick` 不会被触发，而 `button` 也不会呈现按下时的效果。

::: tip
`press` 事件通常也是在松手时触发的，但是它要求按钮的按下事件从未被阻止过。因此阻止冒泡的内层元素 `touchstart` 事件可以阻止外层按钮的 `press` 事件触发。
:::

#### 其他触发时机

这种方法的限制在于内层元素的 `touchstart` 事件在按下时触发，也可以改用 `touchend` 事件来来触发，但是要保留 `touchstart` 事件的阻止冒泡功能。这样可以确保在按下时不会触发外层按钮的 `press` 事件。

```html
<button on:press="onOuterClick">
  <p on:touchstart="$event.stopPropagation()" on:touchend="onInnerClick">inner</p>
  outer button
</button>
```

```js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    // 这里不需要阻止冒泡，因为已经在 touchstart 阻止了
    console.log('inner click');
  }
}
```

<glyphix id="components-button-click-3" height="48" width="360" inline>

``` html
<button on:press="onOuterClick">
  <p on:touchstart="$event.stopPropagation()" on:touchend="onInnerClick">inner</p>
  outer button
</button>
```

``` css
button {
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}

button:active {
  opacity: 0.5;
}

p {
  border: 2px solid #444;
  padding: 0 10px;
}
```

``` js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    console.log('inner click');
  }
}
```

</glyphix>

打开浏览器控制台，再次点击 `inner` 文本，你会发现 `onInnerClick` 的日志会在松手时才打印，并且一样可以阻止外层 `button` 响应手势。


============================================================
FILE_PATH: src/original_docs/components/textarea.md

# textarea

`textarea` <experimental/><version-badge since="0.9" /> 是一个多行文本输入组件，默认显示为块级元素。和手机或 PC 上的类似 GUI 元素不同，`textarea` 目前不响应键盘等输入设备，也不会弹出输入法界面，因此你必须手动编辑其内容。`textarea` 支持通过触摸手势操作光标（如点击和滚动），并提供了上下左右移动光标的方法。

`textarea` 适合作为多行文本输入的底层组件，并根据你的需求自己实现软键盘和光标控制，详情请参考[示例](#基本示例)。

::: important 兼容性
`textarea` 是一个实验性的扩展组件，目前仅在 Glyphix 0.9 及以上版本可用，并且仅部分设备支持该组件。
:::

## 属性

### `text` <decl type="string" get set listen />

`text` 属性是一个字符串，它是 `textarea` 当前编辑的文本内容。读取或者监听这个值可以获取输入的文本，也可以设置该属性。

通常会将 `text` 双向绑定到特定的响应式属性，也可以通过元素内部的内容来设置文本，如：

```html
<textarea ::text="inputText" />
```

或者

```html
<textarea @text="onTextChanged">{{ inputText }}</textarea>
```

:::tip
`textarea` 的 `text` 属性与 [`text-field`](text-field.md) 的 [`value`](text-field.md#value) 属性功能类似。
:::

### `placeholder` <decl type="string" set get />

当 `textarea` 的内容为空时，可以通过 `placeholder` 向用户提供一个简短的提示，如“请输入文本”等短语。

`placeholder` 在输入文本为空时自动显示，因此通常只需一个固定的内容，如：

```html
<textarea ::text="inputText" placeholder="type here" />
```

### `insert` <decl type="(text: string): void" method />

在光标处插入一段内容为 `text` 的文本，光标会自动移动到插入的文本之后。调用该函数会触发 `text` 监听事件。

### `backspace` <decl type="(): void" method />

删除光标处的字符，光标会自动向前移动。调用该函数会触发 `text` 监听事件。

### `moveCaret` <decl type="(direction: 'up' | 'down' | 'left' | 'right'): void" method />

将光标向指定方向移动一个位置。`direction` 参数可选值为 `'up'`、`'down'`、`'left'`、`'right'`，分别对应上下左右四个方向。

## 使用说明

### 基本示例

以下示例展示了 `textarea` 的基本用法。用户可以直接在文本框中输入多行文本，也可以使用下方的虚拟键盘来编辑内容：点击字母/符号键插入字符；"`×`" 键删除光标处的内容；"`Aa`" 键切换大小写；"`1#`" 键切换至符号键盘；"`Enter`" 键插入换行符；箭头键移动光标。

<glyphix id="components-textarea-basic" width="560" height="360" title="Textarea 基本示例">

```html
  <div class="window">
    <textarea
      id="textarea"
      :placeholder="placeholder"
      @text="onTextChanged"
    >
      {{ text }}
    </textarea>
    <div class="keyboard">
      <div class="kb-row" for="row in keyboard" :style="keyboardRowStyle(row)">
        <button
          class="kb-key"
          for="key in row.keys"
          :width="key.width ? key.width : null"
          on:touchstart="onKeyEvent(key, 'down')"
          on:touchend="onKeyEvent(key, 'up')"
          on:touchcancel="onKeyEvent(key, 'up')"
        >
          {{ key.code ? key.code : key }}
        </button>
      </div>
    </div>
  </div>
```

```js
const keyboardQwert = [
  { keys: ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", {code: "×", width: "13%"}] },
  { keys: ["Aa", "a", "s", "d", "f", "g", "h", "j", "k", "l", "Enter"] },
  {
    keys: ["z", "x", "c", "v", "b", "n", "m", ".", "↑"],
    margin: ["14%", "52px"],
  },
  { keys: [{code: "1#", width: "14%"}, {code: "Space", width: "55%"}, "←", "↓", "→"] },
];

const keyboardQwertUpper = [
  { keys: ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", {code: "×", width: "13%"}] },
  { keys: ["Aa", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"] },
  {
    keys: ["Z", "X", "C", "V", "B", "N", "M", ".", "↑"],
    margin: ["14%", "52px"],
  },
  { keys: [{code: "1#", width: "14%"}, {code: "Space", width: "55%"}, "←", "↓", "→"] },
];

const keyboard123 = [
  { keys: ["~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", {code: "×", width: "13%"}] },
  { keys: ["Aa", "@", "#", "$", "%", "&", "*", "-", "+", "=", "Enter"] },
  {
    keys: ["!", '"', "'", ";", ":", ",", ".", "/", "↑"],
    margin: ["14%", "52px"],
  },
  { keys: [{code: "abc", width: "14%"}, {code: "Space", width: "55%"}, "←", "↓", "→"] },
];

export default {
  data: {
    placeholder: "Enter your text here...",
    text: "Glyphix is a declarative GUI framework built for MCU devices.\n\nIt is lightweight, fast, and easy to use, offering rich UI components and development tools that help teams create modern, responsive graphical interfaces for embedded applications.",
    keyboard: keyboardQwert,
  },
  keyboardType: "qwerty",

  ta: null,
  onReady() {
    this.ta = this.$element("textarea");
  },

  onTextChanged() {
    console.log("You have edited the text");
  },
  toggleCase() {
    if (this.keyboardType == "qwerty") {
      this.keyboard = keyboardQwertUpper;
      this.keyboardType = "qwertyUpper";
    } else if (this.keyboardType == "qwertyUpper") {
      this.keyboard = keyboardQwert;
      this.keyboardType = "qwerty";
    }
  },
  keyboardRowStyle(row) {
    if (row.margin)
      return `margin-left: ${row.margin[0]}; margin-right: ${row.margin[1]};`;
    return "";
  },
  backspaceTimer: null,
  onKeyEvent(key, event) {
    if (event !== "down") {
      clearInterval(this.backspaceTimer);
      this.backspaceTimer = null;
      return; // skip if the key is released
    }

    if (key.code) key = key.code;
    switch (key) {
      case "Aa": this.toggleCase(); break;
      case "1#":
        this.keyboard = keyboard123;
        this.keyboardType = "123";
        break;
      case "abc":
        this.keyboard = keyboardQwert;
        this.keyboardType = "qwerty";
        break;
      case "×":
        this.ta.backspace();
        if (event == "down") {
          this.backspaceTimer = setTimeout(() => {
            this.backspaceTimer = setInterval(() => this.ta.backspace(), 50);
            this.ta.backspace();
          }, 500);
        }
        break;
      case "Enter": this.ta.insert("\n"); break;
      case "Space": this.ta.insert(" "); break;
      case "↑": this.ta.moveCaret("up"); break;
      case "↓": this.ta.moveCaret("down"); break;
      case "←": this.ta.moveCaret("left"); break; 
      case "→": this.ta.moveCaret("right"); break;
      default: this.ta.insert(key); break;
    }
  },
};
```

```css
.window {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 8px;
}

textarea {
  flex-grow: 1;
  padding: 6px;
  border: 2px solid #aaa6;
  border-radius: 12px;
  max-height: 160px;
}

.keyboard {
  display: flex;
  flex-direction: column;
}

.kb-row {
  display: flex;
  flex-direction: row;
}

.kb-key {
  flex-grow: 1;
  background-color: #f0f0f080;
  border: 2px solid #999;
  border-radius: 16px;
  text-align: center;
  padding: 6px auto;
  margin: 2px;
  font-size: 0.85rem;
  min-width: 40px;
}

.kb-key:active {
  background-color: #0003;
  border-color: #6663;
}
```

</glyphix>

我们首先在组件的 `onReady()` 生命周期函数中通过 `$element` 方法来获取 `textarea` 组件对象，因为接下来需要通过 [`insert()`](#insert)、[`backspace`](#backspace) 和 [`moveCaret`](#movecaret) 方法来编辑内容和移动光标。

在此基础上，我们就可以在 `button` 组件的触摸事件监听中调用 `textarea` 的方法，例如：

```html
<button on:touchstart="ta.insert('A')">A</button>
```

由于没有实体键盘，开发者通常需要提供自定义的键盘实现。本示例实现了完整的 QWERTY 键盘布局，支持大小写切换和符号键盘。在每一个键的触摸事件监听函数中调用相应的方法来编辑文本。箭头键通过 [`moveCaret()`](#movecaret) 方法移动光标（上下左右四个方向），换行键通过 [`insert()`](#insert) 插入换行符 `\n`。

### 和 text-field 的区别

`textarea` 和 `text-field` 都是文本输入组件，主要区别如下：

| 特性 | `textarea` | `text-field` |
|------|-----------|-------------|
| 文本行数 | 单行或多行 | 单行 |
| 换行支持 | 支持 `\n` 换行 | 不支持换行 |
| 光标移动 | 上下移动 | 左右移动 |
| 内容属性 | `text` | `value` |
| 密码模式 | 不支持 | 支持 `password` 属性 |
| 默认 display | 块级元素 | 行内元素 |


============================================================
FILE_PATH: src/original_docs/components/scroll.md

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


============================================================
FILE_PATH: src/original_docs/components/picker.md

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


============================================================
FILE_PATH: src/original_docs/components/label.md

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


============================================================
FILE_PATH: src/original_docs/components/a.md

# a

锚点组件，默认为行内元素，用于跳转到指定的页面。

## 属性

### `href` <decl type="string" get set />

指定需要跳转的[页面名称](/framework/application/manifest.md#pages)或者 URI 字符串。

``` html
<a href="page1">跳转到 page1 页面</a>
``` 

与 Web 中的 `<a>` 标签不同，`a` 组件只支持页面跳转而不支持超链接跳转。

`href` 属性还支持形如 `PageName?key=value` 的 [URI](/framework/application/resource.md#uri) 字符串，即由页面名称（作为 path 字段）和 query 字段构成的 URI。该 URI 的 query 字段会被解析为页面的跳转参数。如点击这个 `<a>` 元素时：

``` html
<a href="page1?text=test-text&message=hello">跳转到 page1 页面</a>
```

等效于调用以下 [`router.push()`](/api/system-router.md#push) 方法：

``` js
router.push({
  uri: 'page1',
  params: {text: 'test-text', message: 'hello'}
})
```

::: tip
请注意，URI 中 query 字段的值只会被解析为字符串类型，因此 `page1?size=100` 中的 `100` 会被解析为字符串 `'100'`，而不是数字 `100`。如果需要传递特定类型的参数，请使用 [`router`](/api/system-router.md) API。
:::


============================================================
FILE_PATH: src/original_docs/components/image.md

# image

图片组件用于显示图片元素，默认居中对齐。 `image` 组件默认是行内元素。

## 属性

### `src` <decl type="string" get set />

设置图片的 [URI](/framework/application/resource.md)，对于应用包内的资产图片，支持相对路径和绝对路径。`image` 组件支持 PNG 和 JPEG 通用图片格式。

::: tip
`image` 组件只支持本地的图片资源，而不像 Web 的 `img` 元素可以直接显示网络图片资源。详情请参考如何在 Glyphix 中[显示网络图片](#显示网络图片)。
:::

### `noCache` <decl type="boolean" get set />

设置图片是否要进行缓存，默认情况下会使用缓存以优化图片加载速度。在开启 `noCache` 属性时 `image` 组件不会使用缓存，此时更改 [`src`](#src) 属性后总是会从文件中重新加载图片。

图片缓存是一种优化加载速度并减少内存占用的技术，当系统中已经加载了相同 URI 的图片时，开启缓存的 `image` 组件会直接使用该资源。但是从网络中下载的名称固定、内容可能变动的图片文件（如用户头像的 `internal://cache/avatar.png`）通常需要开启 `noCache` 属性才能保证行为正确。 

即便开启了 `noCache` 属性，`image` 组件依然不会检测图片文件内容的更新，此时需要手动更改 [`src`](#src) 属性。考虑到响应式框架会过滤相同的赋值操作，你必须使用这样的技巧：
``` html
<!-- 假设这是需要更新显示的图片，no-cache 属性是必须的。 -->
<image :src="avatarImage" no-cache />
```

``` js
const avatarImage = 'internal://cache/avatar.png' // 假设这是从网上下载的图片

export default {
  data: {
    avatarImage: avatarImage
  },
  // 在头像下载完成后调用这个方法以更新界面
  onAvatarDownloaded() {
    this.avatarImage = null // 必须先赋一个新的值
    this.avatarImage = avatarImage // 重新赋值为正确的 URI
  }
}
```
在上面的示例中，响应式属性 `this.avatarImage` 首先被更改为 `null`，然后再重新赋值，这样值会发生变化，从而绕过响应式框架的优化机制，并实现图片更新。


::: warning
必须使用此技巧更新固定 URI 的资源，否则显示内容可能不会变化。保险起见，如果从网络中获取的资源路径可能重复，那么也需要使用此技巧确保界面更新。

此外，必须等待图片下载或者文件写入完成后才能更新 `image` 组件的 `src` 属性，否则也无法正常更新界面。
:::

### `async` <decl type="boolean" get set />

使用异步的方式加载图片资源。这种模式可以保证图片加载不会阻塞 UI 线程，提升界面的流畅性。但是相比于默认的同步加载模式，异步加载中的图片不会显示实际内容，因此不适用于所有界面。

异步加载模式适用于从网络中下载的图片。与应用打包时会自动优化的图片资产不同，网络图片通常是 PNG 或者 JPEG 这类解码缓慢的通用格式。同步解码网络图片会非常卡顿，而且这类场景中通常不需要立即显示图片。

`async` 可以和 [`noCache`](#nocache) 属性一起使用，因为后者也主要用于网络图片：
``` html
<image :src="avatarImage" no-cache async />
```

## 继承的属性

这些属性继承自原生组件的[通用属性](/framework/generic/properties.md)，但是 `image` 组件对这些属性做了特殊处理。

### `opacity` <decl type="number" set />

设置图片的透明度，取值范围为 $[0, 1]$，其中 $0$ 表示完全透明，$1$ 表示完全不透明，默认值为 $1$。

### `transform` <decl type="string" set />

设置图片的变换效果，等效于 CSS 的 [`transform`](/framework/generic/styles.md#transform) 属性。

## CSS 说明

### 不支持的通用属性

相比于其他原生组件，`image` 比较特殊，它不支持 `background-color`、`border` 等通用属性。这一点和 Web 标准也是非常不同的。具体而言，以下 CSS 属性不受支持：

- [`background-color`](/framework/generic/styles.md#background-color), [`background-image`](/framework/generic/styles.md#background-image)
- [`border`](/framework/generic/styles.md#border), [`border-top`](/framework/generic/styles.md#border-top), [`border-right`](/framework/generic/styles.md#border-right), [`border-bottom`](/framework/generic/styles.md#border-bottom), [`border-left`](/framework/generic/styles.md#border-left)

这意味着不能通过设置 CSS 属性为 `image` 组件添加背景颜色或图片，也不能为其设置边框样式。不过 `image` 组件是支持 [`border-radius`](/framework/generic/styles.md#border-radius) 属性的。

### 特殊属性

`image` 组件支持其他可用于非容器组件的 CSS 属性，但是有几个属性可用于实现特殊的效果。

#### `transform`

设置图片的变换，该 CSS 属性用于 `image` 时和其他元素的 [`transform`](/framework/generic/styles.md#transform) 效果类似，但是不需要设置 [`transparent`](/framework/generic/styles.md#transparent) 属性也可以正常显示。

#### `opacity`

设置图片的透明度，和 [`opacity`](#opacity) 属性效果一样。

#### `border-radius`

设置图片的圆角半径，可以使用此属性为图片添加圆角，使用方法和通用的 [`border-radius`](/framework/generic/styles.md#border-radius) 相同。`image` 组件总是会将圆角应用到图片的四个角上，无论图片的长宽比和 `image` 组件本身的长宽比是否一致。

#### `object-fit`

`image` 组件的 `object-fit` 属性默认值为 `none`，这与 Web 标准（默认为 `fill`）不同。默认情况下，图片不会自动缩放，而是按原始尺寸居中显示，若尺寸超出容器则会被裁剪。这种设计是出于对 MCU 设备特性的考虑：
- **性能优先**：图片缩放通常需要额外的计算，部分设备甚至通过软件方式实现插值缩放，这会显著降低帧率。
- **画质一致性**：某些设备上，即使是等比缩小也可能导致明显的模糊或锯齿。默认不缩放可确保像素级渲染效果不失真。
- **内存受限**：默认缩放可能掩盖资源使用问题，导致无意中加载过大的图像，从而浪费宝贵的存储与内存空间。

建议在设计阶段就提供与显示区域匹配的图片资源，尽量让图像在默认状态下即可正确显示；只有在确有需要时，才应通过显式设置 `object-fit`（如 `contain`）来调整显示效果。

## 使用技巧

### 显示网络图片

#### 头像类场景

本节演示一种需要从网络上加载图片的方法，该方法主要用于用户头像等场合，即图片在本地有固定的存储位置，但是内容可能会变化。由于 Glyphix 运行时的缓存策略，你需要使用本示例中的技巧来确保显示内容更新。

``` html
<template>
  <image :src="avatar" no-cache />
</template>
```

``` js
import request from '@system.request'

export default {
  data: {
    avatar: null
  },
  onInit() {
    this.downloadAvatar()
  },
  async downloadAvatar() {
    const saveFile = 'internal://files/avatar.png'
    await request.download({
      url: 'https://example.com/url/to/avatar.png',
      filename: saveFile,
    }).complete
    // 此处技巧详见 noCache 属性的说明
    this.avatar = null
    this.avatar = saveFile
  }
}
```



============================================================
FILE_PATH: src/original_docs/components/span.md

# span

`span` 也是一种文本组件。和 [`p` 组件](p)不同，`span` 组件默认是行内元素并且可以跨行，[`label` ](label) 组件和 [`a`](a) 组件也有类似的效果。文本跨行是指元素可以跨越多行进行布局，而不是占据一整个“盒子”。

`span` 组件可以用于实现[富文本排版](/framework/render/rich-text.md#富文本显示)。

<glyphix id="span" :height="36">

``` html
<div>
  Hello Glyphix, this is <span style="color: #f0f">span</span> label!
</div>
```

</glyphix>


============================================================
FILE_PATH: src/original_docs/components/scroll-bar.md

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


============================================================
FILE_PATH: src/original_docs/components/barcode.md

# barcode

`barcode` 组件用于显示 [Code 128](https://en.wikipedia.org/wiki/Code_128) 条形码。`barcode` 组件可以显示任意 ASCII 字符串，适合用于显示商品条码、支付码等信息。

在流式布局中，`barcode` 组件默认为块级元素（`block`），会单独占据一行显示。

## 属性

### `value` <decl type="string" get set />

设置条形码要显示的内容。支持任意 ASCII 字符串。

## CSS 说明

要想让条形码容易被扫描，应正确设置 `barcode` 组件的 CSS 属性，这包括：
- `color`：条形码的条颜色，一般设置为黑色（`black` 或者 `#000`）；
- `background-color`：条形码的背景色通常要是白色（`white` 或者 `#fff`）；
- `padding` / `margin`：足够的内外边距可以避免条形码和其他元素混淆，增加扫描识别率；
- `width` / `height`：条形码的尺寸必须足够大以方便拍摄。

默认情况下条形码组件的每一条码会占据 $2\rm px$ 宽度和 $32\rm px$ 高度，这在手表等小屏幕设备上可能过小，建议开发者根据需要手动设置条形码组件的 `width` / `height` 属性并在设备上进行测试。

下面的例子展示了条形码组件的使用方法，请注意 CSS 中为 `barcode` 组件设置了各种边距，这都是为了保证条形码和其他界面元素有足够的间隔以免干扰扫描。

<glyphix id="barcode-1" :height="150" :width="350">

``` html
<div>
  <barcode :value="text"/>
  <p>{{ text }}</p>
</div>
```

``` js
export default {
  data: {
    text: '9787111407010'
  }
}
```

``` css
div {
  background-color: black;
  padding: 8px;
}

barcode {
  margin: 8px;
  padding: 8px;
  color: black; /* 将条形码前景色设置为黑色 */
  background-color: white; /* 将条形码背景色设置为白色 */
  border-radius: 16px;
  height: 80px;
}

p {
  color: white;
  font-size: 0.75rem;
  text-align: center;
}
```

</glyphix>

::: tip
应总是显式设置**高对比度**的条形码组件的码点颜色（`color`）和背景（`background-color`）样式。以免设备的默认样式主题和继承的样式属性偏差导致识别性下降。

同时，请设置足够大的内边距（`padding`），确保容易扫描识别。
:::



============================================================
FILE_PATH: src/original_docs/components/drawer-navigation.md

# drawer-navigation

[`drawer`](drawer) 的子组件，用来展示具体的抽屉内容。

## 属性

### `direction` <decl type=" 'left' | 'right' | 'up' | 'down' " set />

`direction` 属性用于设置 `drawer-navigation` 的方向，可选值为 `'left'`、`'right'`、`'up'`、`'down'`。

|    值     | 描述                                              |
| :-------: | ------------------------------------------------ |
| `'left'`  | 屏幕左边的drawer-navigation，用于响应从左往右滑动的手势。       |
| `'right'` | 屏幕右边的drawer-navigation，用于相应从右往左滑动的手势。       |
|  `'up'`   | 屏幕下边的drawer-navigation，用于相应从从下往上滑动的手势。     |
| `'down'`  | 屏幕上边的drawer-navigation，用于相应从上往下滑动的手势。       |






============================================================
FILE_PATH: src/original_docs/components/p.md

# p

文本组件。`p` 默认是块级元素，和 [`span`](span) 不同，`p` 组件在设置为行内元素时也不支持文本跨行，如果需要实现富文本排版应考虑使用 `span` 等组件。

## 属性

### `text` <decl type="string" get set/>

设置文本内容，支持如下两种写法。

``` html
<p text="Hello Glyphix"></p>
<p>Hello Glyphix</p>
```

<glyphix id="p" :height="70" inline>

``` html
<div>
  <p text="Hello Glyphix"></p>
  <p>Hello Glyphix</p>
</div>
```

</glyphix>

### `color` <decl type="string" get set/>

设置文本颜色，只支持十六进制的颜色代码，如 `#f00`，`#e8bb80ff` 等。该属性是修改 CSS 内联属性 [`color`](/framework/generic/styles.md#color) 的一个快捷方式。

### `lines` <decl type="number" get set/>

设置文本的最大行数，超过该行数的文本会被截断或者省略。该属性是修改 CSS 内联属性 [`max-lines`](/framework/generic/styles.md#max-lines) 的一个快捷方式。

### `text-align` <decl type="string" set/>

设置文本对齐方式，支持 `left`、`center`、`right` 等值。该属性是修改 CSS 内联属性 [`text-align`](/framework/generic/styles.md#text-align) 的一个快捷方式。

### `font-size` <decl type="string" set/>

设置文本字体大小，支持 `12px`、`1.5em` 等 CSS 字体大小值。该属性是修改 CSS 内联属性 [`font-size`](/framework/generic/styles.md#font-size) 的一个快捷方式。

### `font-weight` <decl type="number" set/>

设置文本字体字重，目前只支持整数值，如 `400`，`600` 等。该属性是修改 CSS 内联属性 [`font-weight`](/framework/generic/styles.md#font-weight) 的一个快捷方式。

## 使用技巧

### 尺寸控制

一般情况下，不要手动设置 `p` 组件的高度，例如
``` css
p.my-paragraph {
  height: 48px;
  font-size: 32px;
}
```
表面上看，这为 `p` 组件设置了一个大于字体大小的高度，但实际情况是：
- 对于单行文本，某些字体的实际高度可能超过字体大小，即便 `48px` 的高度也可能出现垂直的裁剪。
- 对于多行文本，设置固定高度会导致多行文本被裁剪，无法完整显示。

如果你希望控制文本的显示行数，应使用 [`max-lines`](/framework/generic/styles.md#max-lines) 和 [`text-overflow`](/framework/generic/styles.md#text-overflow) 来实现文本的截断和省略，而不是设置固定高度。

### 文字裁剪动画 <version-badge since="0.9"/>

可以使用 [`width`](/framework/generic/styles.md#width) 属性配合 [`transition`](/framework/component/prop-modifier.md#transition-修饰符) 修饰来实现文字裁剪动画。例如：

``` html
<p :width="state ? 240 : 0"
   width.transition="{duration: 2.0}">
  Hello Glyphix!
</p>
```

配合 `max-lines: 1` 样式可以实现文字从左到右的裁剪动画。但是这个动画存在一个问题：当宽度不足时，最后一个字符会被直接丢弃而不是被裁剪。目前的绕过方法是将文本内容放在一个子组件中，并对父组件设置宽度动画：

``` html
<div :width="state ? 240 : 1"
     width.transition="{duration: 2.0}">
  <p style="max-lines: 1">Hello Glyphix!</p>
</div>
```

<glyphix id="p-width-transition" title="文字裁剪动画" height="120">

``` html
<div class="container">
  <p class="animated-text"
     :width="state ? 240 : 0"
     width.transition="{duration: 2.0}">
    Hello Glyphix!
  </p>
  <div class="animated-text"
       :width="state ? 240 : 1"
       width.transition="{duration: 2.0}">
    <p>Hello Glyphix!</p>
  </div>
</div>
```

``` js
export default {
  data: {
    state: false
  },
  onReady() {
    setInterval(() => this.state = !this.state, 2500)
  }
}
```

```css
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.animated-text {
  margin: 4px;
  border: 1px solid #f00;
}

p {
  max-lines: 1;
  text-overflow: clip;
}
````

</glyphix>

但是，当使用 `div` 元素作为父组件时，动画会有一个问题：当宽度为 `0` 时，布局尺寸会计算为 `(width: 0, height: 0)`，这会导致该元素无法占据垂直空间，并在动画开始时出现垂直跳动。解决方法是将宽度设置为一个非常小的值（例如 `1px`）而不是 `0`，这样元素就可以占据垂直空间，从而避免跳动问题。


============================================================
FILE_PATH: src/original_docs/components/marquee.md

# marquee

`marquee` 组件用于显示滚动的文本内容，只支持单行显示。`marquee` 组件不支持包括 `span` 在内的任何子组件。

`marquee` 支持通用的 CSS 属性，但是由于实现的原因，现在可能不支持 `text-align` 属性。由于 `marquee` 只显示单行文本，并会在文本内容超长时滚动显示，`max-lines` 等属性也均不起作用。

## 属性

### `text` <decl type="string" get set/>

设置文本内容，和 `p` 组件的 [`text`](p.md#text) 属性用法相同。当文本内容的长度超过 `marquee` 的宽度时，文本会自动滚动显示。


============================================================
FILE_PATH: src/original_docs/components/text-field.md

# text-field

用于输入单行文本内容的组件，默认为行内元素。和手机或 PC 上的类似 GUI 元素不同，`text-field` 目前不响应键盘等输入设备，也不会弹出输入法界面，因此你必须手动编辑其内容。`text-field` 支持通过触摸手势操作光标（如点击和滚动）。

`text-field` 适合作为单行文本输入的底层组件，并根据你的需求自己实现软键盘（如密码九宫格，甚至是语音输入），详情请参考[示例](#基本示例)。

## 属性

### `value` <decl type="string" set get listen />

`value` 属性是一个字符串，它是 `text-field` 当前编辑的内容。读取或者监听这个值可以获取输入的文本，也可以设置该属性。

通常会将 `value` 双向绑定到特定的响应式属性，如：

```html
<text-field ::value="inputText" />
```

### `placeholder` <decl type="string" set get />

当 `text-field` 的内容为空时，可以通过 `placeholder` 向用户提供一个简短的提示，如“请输入文本”等短语。

`placeholder` 在输入文本为空时自动显示，因此通常只需一个固定的内容，如：

```html
<text-field ::value="inputText" placeholder="type here" />
```

### `password` <decl type="boolean" set get />

当该属性被设置时，`text-area` 将使用“密码模式”，即每个字符会被替换为“•”（[Bullet, U+2022](http://www.fileformat.info/info/unicode/char/2022/index.htm)）。你可以随时关闭或者打开 `password` 属性，以实现显示、隐藏密码状态的切换。

在新版本中 <version-badge since="0.9" />，密码模式会延时遮盖输入的字符，用户可以在短时间内看到刚输入的字符，之后才会被替换为“•”。旧版本则会立即遮盖输入字符。

### `insert` <decl type="(text: string): void" method />

在光标处插入一段内容为 `text` 的文本，光标会自动移动到插入的文本之后。调用该函数会触发 `value` 监听事件。

### `backspace` <decl type="(): void" method />

删除光标处的字符，光标会自动向前移动。调用该函数会触发 `value` 监听事件。

## 使用说明

### 基本示例

以下示例展示了 `text-field` 的基本用法。你可以点击键盘按钮来输入数字。点击“×”按钮来删除光标处的内容，点击“A/*”则会在密码模式和普通文本输入模式之间切换。密码模式下，输入的内容会以 `•` 隐藏。

<glyphix id="components-text-field-1" width="410" height="160">

```html
<div class="flex-column">
  <div class="flex-row align-baseline">
    <text-field id="text-field"
                ::value="inputText"
                :password="password"
                placeholder="type here" />
    <button checkable ::press="password">A/*</button>
    <button on:click="textField.backspace()">×</button>
  </div>
  <!-- 一个简单的矩阵数字键盘 -->
  <div class="flex-row" for="rows in keyboard">
    <button class="flex-1" for="key in rows"
            on:click="textField.insert(key)">
      {{key}}
    </button>
  </div>
</div>
```

```js
export default {
  data: {
    inputText: "",
    password: false,
  },
  keyboard: [
    ['1', '2', '3', '4', '5'],
    ['6', '7', '8', '9', '0'],
  ],
  textField: null,
  onReady() {
    // 获取 TextField 组件对象，方便调用 insert() 和 backspace() 方法。
    this.textField = this.$element("text-field")
  },
}
```

```css
.flex-column {
  display: flex;
  flex-direction: column;
}

.flex-row {
  display: flex;
}

.align-baseline {
  align-items: baseline;
}

text-field {
  flex: 1;
  text-align: center;
  border-bottom: 2px solid #666;
}

button {
  border-radius: 8px;
  background-color: #dee2e6;
  margin: 8px;
  padding: auto 12px;
}

button:active {
  opacity: 0.5;
}

.flex-1 {
  flex: 1;
}
```
</glyphix>

本示例中 `text-field` 的文本是居中显示的，这是通过 `text-align` 实现的：
```css
text-field {
  text-align: center;
}
```

我们首先在组件的 `onReady()` 生命周期函数中通过 `$element` 方法来获取 `text-field` 组件对象，因为接下来需要通过 [`insert()`](#insert) 和 [`backspace`](#backspace) 方法来编辑内容。

在此基础上，我们就可以直接在 `button` 组件的 `click` 事件监听中调用 `text-field` 的方法，例如：
```html
<button on:click="textField.backspace()">×</button>
```

由于没有实体键盘，开发者通常需要提供自定义的键盘实现。处于教学的目的，本示例仅实现了 2 行 5 列的数字键盘。并要在每一个键的 `click` 事件监听函数中将键值插入到 `text-field` 中：
```html
<div class="flex-row" for="rows in keyboard">
  <button class="flex-1" for="key in rows"
          on:click="textField.insert(key)">
    {{key}}
  </button>
</div>
```

本示例还演示了切换密码模式的标准方法。

### 内容验证和格式化

你可以通过将 `text-field` 的 [`value`](#value) 属性双向绑定到一个计算属性上来实现对输入内容的验证和格式化。下面的示例展示了这种方法，该示例最多只允许你输入 9 位数字（不能输入字母等），并会在每三位数之间添加“`,`” 分隔。

<glyphix id="components-text-field-validator" title="内容验证器" width="410" height="200">

```html
<div class="flex-column">
  <div class="flex-row align-baseline">
    <text-field id="text-field"
                ::value="inputText"
                :password="password"
                placeholder="type here" />
    <button checkable ::press="password">A/*</button>
    <button on:click="textField.backspace()">×</button>
  </div>
  <div class="flex-row" for="rows in keyboard">
    <button class="flex-1" for="key in rows"
            on:click="textField.insert(key)">
      {{key}}
    </button>
  </div>
</div>
```

```js
export default {
  data: {
    password: false,
    rawText: "",
  },
  computed: {
    inputText: {
      get() { return this.rawText },
      set(text) {
        if (text.length < 12 && /^[\d,]*$/.test(text)) {
          this.rawText = text.replace(/[^\d]/g, '')
                             .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
        }
      },
    },
  },
  keyboard: [
    ["1", "2", "3", "4", "5"],
    ["6", "7", "8", "9", "0"],
    ["A", "B", "C", "D", "E"],
  ],
  textField: null,
  onReady() {
    this.textField = this.$element("text-field")
  },
}
```

```css
.flex-column {
  display: flex;
  flex-direction: column;
}

.flex-row {
  display: flex;
}

.align-baseline {
  align-items: baseline;
}

text-field {
  flex: 1;
  border-bottom: 2px solid #666;
}

button {
  border-radius: 8px;
  background-color: #dee2e6;
  margin: 8px;
  padding: auto 12px;
}

button:active {
  opacity: 0.5;
}

.flex-1 {
  flex: 1;
}
```
</glyphix>

内容验证和格式化是通过双向绑定和计算属性来实现的。对于 `text-field` 组件节点
```html
<text-field id="text-field"
            ::value="inputText"
            :password="password"
            placeholder="type here" />
```
来说，`value` 属性被双向绑定到了 `inputText`，后者其实是一个计算属性。它的 `set()` 方法会检查输入内容是否符合规范（最多 11 个字符，且只允许数字和逗号），然后通过正则表达式来过滤数字，并按照每三位数字之间加逗号进行格式化：
```js
function set(text) {
  if (text.length < 12 && /^[\d,]*$/.test(text)) {
    this.rawText = text.replace(/[^\d]/g, '')
                       .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }
}
```
如果输入的内容不符合要求，那么 `set()` 方法会忽略输入值，双向绑定机制会使得 `text-field` 的内容和 `inputText` 的属性值（通过 `get()` 方法获取）保持一致。因此你会发现无法输入字母按键。


============================================================
FILE_PATH: src/original_docs/components/canvas.md

# canvas

画布组件，通过使用 JavaScript 中的脚本，可以在 `canvas` 上绘制图形等。

### `context`

**值类型**：画布 API 获取的上下文内容

**操作**：设置

设置画布要绘制图形的上下文。


============================================================
FILE_PATH: src/original_docs/components/checkbox.md

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


============================================================
FILE_PATH: src/original_docs/components/README.md

# 原生组件


============================================================
FILE_PATH: src/original_docs/components/radio.md

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


============================================================
FILE_PATH: src/original_docs/components/stack.md

# stack

`stack` 堆叠布局组件。在堆叠布局中，每个子组件的尺寸和位置和 `stack` 组件相同，并且按照先后顺序依次堆叠显示。下面的例子展示了两个在 `stack` 组件内重叠显示的文本元素。

<glyphix id="components-stack-layout" height="100" width="200" title="堆叠布局">

``` html
<stack>
  <p class="text1">Text 1</p>
  <p class="text2">Text 2</p>
</stack>
```

``` css
* {
  text-align: center;
}

.text1 {
  font-size: 64px;
  color: #fff;
}

.text2 {
  font-size: 48px;
  color: #f008;
}

stack {
  background-color: gray;
}
```

</glyphix>

::: tip
`stack` 组件总是使用堆叠显示的布局策略，无法通过 `display` 等 CSS 属性更改为其他布局（如 flex 布局或流式布局）。
:::

## 布局行为

`stack` 组件具有固定的堆叠布局策略。其尺寸由两种约束决定：
1. `stack` 的尺寸首先由 [`width`](../framework/generic/styles.md#width) 或 [`height`](../framework/generic/styles.md#width) 等尺寸 CSS 属性指定；
2. 父级元素的布局可能会直接决定 `stack` 的布局，如 flex 布局中的 `align-items: stretch`、`flex: 1` 等属性；
3. 否则 `stack` 组件的尺寸由子元素的最大宽度和最大高度决定。

一旦确定了 `stack` 的尺寸，那么它的所有子元素都会具有相同的外框尺寸（即子元素加上 `border` 和 `margin` 后的尺寸）。这有时会导致困扰，例如通过 `stack` 将一张图片做为背景，而上层的元素尺寸过大会导致这张图片可能铺不满。


============================================================
FILE_PATH: src/original_docs/components/input.md

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


============================================================
FILE_PATH: src/original_docs/components/switch.md

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


============================================================
FILE_PATH: src/original_docs/components/progress.md

# progress

`progress` 组件用于显示进度条，默认为块级元素。

## 属性

### `max` <decl type="number" set />

最大进度值，[`value`](#value) 属性不会大于它。

### `min` <decl type="number" set />

最小进度值，[`value`](#value) 属性不会小于它。

### `value` <decl type="number" set get listen />

设置进度值。进度的显示比例取决于 `value` 属性在 `min` 到 `max` 区间中的比例，同时显示比例会限制在$0\% \sim 100\%$ 之间。`value` 值是一个整数，如果设置浮点值则只会截取整数部分。

### `vertical` <decl type="boolean" set />

如果 `vertical` 属性的值为 `true`，`progress` 组件将会垂直显示，否则水平显示。默认值为 `false`。 

## CSS 规范

开发者可以通过 CSS 来调整 `progress` 组件的外观。

### 尺寸计算

`progress` 默认宽高和元素的字体尺寸一样，字体尺寸由 [`font-size`](/framework/generic/styles.md#font-size) 属性设置（也可以继承而来）。通过 [`width`](/framework/generic/styles.md#width) 和 [`height`](/framework/generic/styles.md#height) 属性可以自定义 `progress` 的尺寸。

### CSS 属性

以下 CSS 属性可能会非常有用：
- [`background-color`](/framework/generic/styles.md#background-color) 可以控制 `progress` 的背景颜色；
- [`color`](/framework/generic/styles.md#color) 可以控制 `progress` 的进度条颜色；
- [`border-radius`](/framework/generic/styles.md#border-radius) 可以将 `progress` 设置为圆角边框，例如 `50%` 会产生半圆边框；

其他的 CSS 属性可能也有用，例如可以使用 [`border`](/framework/generic/styles.md#border) 属性设置边框样式。

### CSS 伪元素

#### `value`

该伪元素可以单独定义 `progress` 进度条而不包含背景部分的样式。例如可以分别设置滚动条背景和进度条部分的圆角半径，以实现外边框具有圆形线冒而进度条则是直线帽的效果。

``` css
progress {
  border-radius: 50%; /* 滚动条背景圆角 */
}

progress::value {
  border-radius: 0; /* 滚动条的进度条没有圆角 */
}
```

### CSS 示例

下面的例子演示了一些通过 CSS 来自定义进度条外观的方法。

<glyphix id="components-progress-styles" height="140" width="480" title="进度条样式">

``` html
<div>
  <!-- 默认样式 -->
  <progress :value="40" />
  <!-- 直头进度条样式 -->
  <progress class="flat" :value="50" />
  <progress class="more-style" :value="60" />
</div>
```

``` css
div > * {
  margin: 8px;
}

.flat::value {
  /* value 伪元素的圆角半径设置为 0 即可实现进度条直头效果 */
  border-radius: 0;
}

.more-style {
  /* 自定义圆角半径 */
  border-radius: 30%;
  /* 进度条背景色 */
  background-color: #b3c5d7;
  /* 进度条前景颜色 */
  color: #b5179e;
  /* padding 可以调整进度条前景的边距 */
  padding: 6px;
  height: 1.25rem;
}
```

</glyphix>


============================================================
FILE_PATH: src/original_docs/components/slider.md

# slider

滑动选择器，默认为块级元素。

## 属性

### `value` <decl type="number" get set listen />

当前值，默认值：$10$。

设置 `value` 属性时，将会改变组件的当前值。可以通过 `on` 指令监听当前值的改变，每次当前值改变都会被触发。

### `min` <decl type="number" set />

最小值，默认值：$0$。

### `max` <decl type="number" set />

最大值，默认值：$100$。

### `vertical` <decl type="boolean" set />

如果 `vertical` 属性的值为 `true`，`slider` 组件将会垂直显示，否则水平显示。默认值为 `false`。 

## CSS 规范

开发者可以通过 CSS 来调整 `slider` 组件的外观。

### 尺寸计算

`slider` 默认宽高和元素的字体尺寸一样，字体尺寸由 [`font-size`](/framework/generic/styles.md#font-size) 属性设置（也可以继承而来）。通过 [`width`](/framework/generic/styles.md#width) 和 [`height`](/framework/generic/styles.md#height) 属性可以自定义 `progress` 的尺寸。

### CSS 属性

以下 CSS 属性可能会非常有用：
- [`background-color`](/framework/generic/styles.md#background-color) 可以控制 `slider` 的背景颜色；
- [`color`](/framework/generic/styles.md#color) 可以控制 `slider` 的进度条颜色；
- [`border-radius`](/framework/generic/styles.md#border-radius) 可以将 `slider` 设置为圆角边框，例如 `50%` 会产生半圆边框；

其他的 CSS 属性可能也有用，例如可以使用 [`border`](/framework/generic/styles.md#border) 属性设置边框样式。

### CSS 伪元素

#### `value`

该伪元素可以单独定义 `slider` 进度条而不包含背景部分的样式。例如可以分别设置滚动条背景和进度条部分的圆角半径，以实现外边框具有圆形线冒而进度条则是直线帽的效果。

``` css
slider {
  border-radius: 50%; /* 滚动条背景圆角 */
}

slider::value {
  border-radius: 0; /* 滚动条的进度条没有圆角 */
}
```

#### `thumb` <experimental/>

`thumb` 伪元素用于定义 `slider` 滑块的样式。默认情况下 `slider` 不包含手柄，要想显示手柄必须指定 `thumb` 元素的宽度和高度：
``` css
slider::thumb {
  width: 150%;
  height: 150%;
  border-radius: 50%;
}
```
百分比单位的 `width` 和 `height` 是相对于元素本身的尺寸计算的，水平 `slider` 的滑块宽高根据元素 CSS 的 `height` 计算百分比，而垂直 `slider` 的手柄宽高根据元素 CSS 的 `width` 属性计算百分比。例如元素 CSS 为
``` css
slider {
  width: 200px;
  height: 24px;
}
```
此时上面的 `slider::thumb` 对应的滑块宽度和高度都是 $24\rm{px} \times 150\% = 36\rm{px}$。而手柄的圆角半径百分比尺寸则是根据手柄自己的尺寸来计算的，本例子中 `50%` 的 `thumb` 伪元素圆角半径计算值为 $36\rm{px} \times 50\%=18\rm{px}$。

`thumb` 伪元素支持 `border` CSS 属性，不过边框不会超出 `thumb` 伪元素的尺寸。

### CSS 示例

下面的例子演示了一些通过 CSS 来自定义进度条外观的方法。
<glyphix id="components-slider-styles" height="180" width="480" title="Slider 样式">

``` html
<div>
  <!-- 默认样式 -->
  <slider ::value="value" />
  <!-- 直头进度条样式 -->
  <slider class="flat" ::value="value" />
  <slider class="more-style" ::value="value" />
  <p>value: {{value}}</p>
</div>
```

``` css
div > * {
  margin: 8px;
  padding: 6px;
}

.flat::value {
  /* value 伪元素的圆角半径设置为 0 即可实现进度条直头效果 */
  border-radius: 0;
}

.more-style {
  /* 自定义圆角半径 */
  border-radius: 30%;
  /* slider 背景色 */
  background-color: #b3c5d7;
  /* slider 前景颜色 */
  color: #b5179e;
  /* padding 可以调整 slider 前景的边距 */
  padding: 6px;
  height: 1rem;
}

/* 定义滚动条滑块样式 */
.more-style::thumb {
  width: 300%; /* 宽高比 2:1 的胶囊形滑块 */
  height: 150%;
  background-color: white;
  border: 4px solid #f3722c; /* 滑块边框 */
  border-radius: 50%;
}
```

``` js
export default {
  data: { value: 50 }
}
```

</glyphix>


============================================================
FILE_PATH: src/original_docs/components/mapview.md

# mapview

地图组件，用于加载和显示基于瓦片（Tile）的地图。`mapview` 支持手势平移、缩放层级切换、当前位置显示以及路线导航绘制，是构建地图类应用的核心组件。

`mapview` 默认是块级元素。

::: tip
`mapview` 是运行时扩展组件，使用前需要确认目标平台已集成 `mapview` 模块。
:::

## 属性

### `baseUri` <decl type="string" get set />

瓦片图资源的**基础路径** URI，瓦片文件将在此目录下按固定层级结构存放。`mapview` 会根据当前缩放层级和坐标自动计算所需的瓦片文件路径，格式为：

```
{baseUri}/{zoomLevel}/{tileX}/{tileY}/normal.png     (标准地图)
{baseUri}/{zoomLevel}/{tileX}/{tileY}/satellite.png  (卫星地图)
```

典型用法是将地图瓦片缓存到设备本地存储，然后将 `baseUri` 指向对应目录：

```html
<mapview baseUri="internal://files/tiles/map_provider" />
```

### `tileType` <decl type="number" get set />

瓦片地图的图层类型，取值如下：

| 值 | 说明 |
| :-: | :-- |
| `0` | 标准地图（默认值），加载 `normal.png` 瓦片文件 |
| `1` | 卫星地图，加载 `satellite.png` 瓦片文件 |

### `loadPlace` <decl type="string" get set />

瓦片图加载中时显示的**占位图** URI。当对应的瓦片文件尚未缓存到本地时，`mapview` 会在该瓦片位置显示此图片，直到瓦片下载完成后触发 [`reload()`](#reload) 刷新。

```html
<mapview loadPlace="/assets/imgs/loading.png" />
```

### `zoomLevel` <decl type="number" get set />

地图缩放层级，取值范围为 $[3, 23]$，默认值为 $17$。层级越高，地图越详细；层级越低，可见范围越大。

::: info
该属性对应地图瓦片标准中的 Zoom Level（缩放级别），与 Bing Maps、Google Maps 等主流瓦片服务的层级定义一致。
:::

### `arrowIcon` <decl type="string" get set />

当前位置图标的图片 URI。该图标会绘制在 [`navCoordinate`](#navcoordinate) 或 [`setLocation()`](#setlocation) 所指定的经纬度对应的屏幕位置上，图标以中心点对齐坐标点。

```html
<mapview arrowIcon="/assets/imgs/location.png" />
```

### `navCoordinate` <decl type="{ x: number, y: number }" get set />

当前位置的经纬度坐标，格式为 `{ x: latitude, y: longitude }`，其中 `x` 为纬度，`y` 为经度。设置该属性仅更新图标位置，不会自动将地图中心移动到该坐标。若需要同时将地图中心定位到当前位置，请使用 [`setLocation()`](#setlocation) 方法并传入 `force: true`。

::: tip
对于需要跟踪实时位置的场景，推荐使用 [`setLocation()`](#setlocation) 方法替代直接赋值此属性，以便通过 `force` 参数控制是否自动回中。
:::

### `arrowLineWidth` <decl type="number" get set />

导航路线的线条宽度，单位为像素，默认值为 `12`。

### `arrowLineBackgroundColor` <decl type="color" get set />

导航路线的**背景色**（已走过部分的颜色），接受 CSS 颜色值，默认值为 `#898b90`。

### `arrowLineForgeColor` <decl type="color" get set />

导航路线的**前景色**（剩余路线部分的颜色），接受 CSS 颜色值，默认值为 `#4b73ec`。

### `smallMem` <decl type="boolean" get set />

是否开启低内存设备模式，默认值为 `false`。

开启后，`mapview` 会将四张 256×256 的瓦片合并缩放为一张 512×512 的图片进行绘制，减少内存中同时缓存的瓦片数量，以适配内存有限的设备。

::: warning
低内存模式会牺牲部分地图清晰度，仅在设备内存明显不足时开启此选项。
:::

### `missTiles` <decl type="Array<{ z: number, x: number, y: number }>" get listen />

只读属性，当地图发现本地缺失瓦片文件时触发监听。回调参数为一个数组，每个元素描述一张缺失的瓦片：

| 字段 | 类型 | 说明 |
| :-- | :-- | :-- |
| `z` | `number` | 缩放层级（Zoom Level） |
| `x` | `number` | 瓦片 X 坐标（列编号） |
| `y` | `number` | 瓦片 Y 坐标（行编号） |

收到该事件后，应用通常需要从服务器下载对应的瓦片文件，并在下载完成后调用 [`reload()`](#reload) 刷新地图：

```js
export default {
  missTileHandler(tiles) {
    // tiles: [{ z: 17, x: 105234, y: 49832 }, ...]
    downloadTiles(tiles).then(() => {
      this.$element('mapview').reload()
    })
  }
}
```

```html
<mapview id="mapview" on:missTiles="missTileHandler" />
```

### `directionInfo` <decl type="{ event: string, stepIndex?: number, distance?: number }" get listen />

地图事件的只读属性，当地图发生以下操作时触发监听：

| `event` 值 | 触发时机 | 附加字段 |
| :-- | :-- | :-- |
| `"move"` | 用户手势平移地图时触发 | 无 |
| `"calc"` | 导航中重新计算位置和偏航距离时触发 | `stepIndex`（当前路线段索引）、`distance`（当前位置到路线的偏离距离，单位米） |

```js
export default {
  onDirectionInfo(info) {
    if (info.event === 'move') {
      // 用户手动拖动了地图，可暂停自动回中
    } else if (info.event === 'calc') {
      console.log(`当前步骤：${info.stepIndex}，偏航距离：${info.distance} 米`)
    }
  }
}
```

## 方法

### `reload()`

重新加载所有瓦片。当新的瓦片文件写入本地存储后，需要调用此方法刷新地图显示。

```js
this.$element('mapview').reload()
```

### `locate()`

将地图中心移动到当前位置（[`navCoordinate`](#navcoordinate) 指定的坐标），用于"回到当前位置"功能。

```js
this.$element('mapview').locate()
```

### `setLocation(location)`

设置当前位置坐标，并可选择性地将地图中心移动到该位置。

| 参数字段 | 类型 | 说明 |
| :-- | :-- | :-- |
| `latitude` | `number` | 纬度 |
| `longitude` | `number` | 经度 |
| `force` | `boolean` | 为 `true` 时立即将地图中心定位到该坐标（等效于调用 [`locate()`](#locate)），为 `false` 时仅更新图标位置 |

```js
// 仅更新图标位置，不移动地图
this.$element('mapview').setLocation({
  latitude: 39.9042,
  longitude: 116.4074,
  force: false,
})

// 更新图标位置并将地图中心移动到该坐标
this.$element('mapview').setLocation({
  latitude: 39.9042,
  longitude: 116.4074,
  force: true,
})
```

### `startNav(linePoints)`

设置导航路线并开始导航。调用后地图会自动定位到路线起点，并绘制完整路线。

`linePoints` 为路线点数组，每个元素为 `[经度, 纬度]` 格式的二元数组：

```js
const route = [
  [116.397428, 39.909736],  // [经度, 纬度]
  [116.404730, 39.913370],
  [116.410072, 39.918933],
]
this.$element('mapview').startNav(route)
```

::: warning
注意参数顺序：每个坐标点的第一个值为**经度**（longitude），第二个值为**纬度**（latitude），与常见的"纬度在前"约定相反。
:::

### `insetNavPoint(linePoints)`

在现有导航路线中追加路线点，格式与 [`startNav()`](#startnav) 相同。适用于分段接收路线数据的场景。追加后需调用 [`reload()`](#reload) 刷新显示。

```js
this.$element('mapview').insetNavPoint(newPoints)
this.$element('mapview').reload()
```

## 使用示例

### 基础地图显示

以下示例展示了如何配置一个基础的地图组件，监听缺失瓦片事件并触发下载。

```html
<template>
  <mapview
    id="map"
    :zoomLevel="zoom"
    :baseUri="tileBaseUri"
    :tileType="tileType"
    loadPlace="/assets/imgs/tile-loading.png"
    arrowIcon="/assets/imgs/location.png"
    on:missTiles="onMissTiles"
    on:directionInfo="onDirectionInfo"
  />
</template>
```

```js
export default {
  data: {
    zoom: 17,
    tileType: 0,
    tileBaseUri: 'internal://files/tiles/my_provider',
  },

  onReady() {
    // 初始化当前位置
    this.$element('map').setLocation({
      latitude: 39.9042,
      longitude: 116.4074,
      force: true,
    })
  },

  onMissTiles(tiles) {
    // tiles: 缺失瓦片列表，向服务器发起下载请求
    fetchTilesFromServer(tiles).then(() => {
      this.$element('map').reload()
    })
  },

  onDirectionInfo(info) {
    if (info.event === 'move') {
      // 用户平移了地图
    }
  },
}
```

```css
mapview {
  width: 100%;
  height: 100%;
}
```

### 导航路线绘制

```html
<template>
  <stack>
    <mapview
      id="map"
      :baseUri="tileBaseUri"
      :zoomLevel="zoom"
      arrowIcon="/assets/imgs/location.png"
      arrowLineWidth="10"
      arrowLineBackgroundColor="#888888"
      arrowLineForgeColor="#1a73e8"
      on:missTiles="onMissTiles"
    />
    <button @click="startNavigation">开始导航</button>
  </stack>
</template>
```

```js
export default {
  data: {
    zoom: 16,
    tileBaseUri: 'internal://files/tiles/my_provider',
  },

  startNavigation() {
    const route = [
      [116.397428, 39.909736],
      [116.404730, 39.913370],
      [116.410072, 39.918933],
    ]
    this.$element('map').startNav(route)
  },

  onMissTiles(tiles) {
    fetchTilesFromServer(tiles).then(() => {
      this.$element('map').reload()
    })
  },
}
```

### 低内存设备适配

```html
<mapview
  id="map"
  :baseUri="tileBaseUri"
  :zoomLevel="zoom"
  :smallMem="isLowEndDevice"
/>
```

```js
import SysDevice from '@system.device'

export default {
  data: {
    zoom: 17,
    tileBaseUri: 'internal://files/tiles/my_provider',
    isLowEndDevice: false,
  },
  onInit() {
    // 根据设备内存档位判断是否启用低内存模式
    this.isLowEndDevice = SysDevice.memoryProfile <= 4096
  },
}
```


============================================================
FILE_PATH: src/original_docs/components/drawer.md

# drawer

抽屉组件，默认隐藏，可以通过滑动的方式展示内容。
drawer 是基本的抽屉组件。drawer 支持子组件及布局，可以在drawer内设置4个drawer-navigation组件用于显示上下左右四个位置的抽屉。

[`drawer`](drawer)组件滑动速度跟随手势滑动速度，手势滑动速度越快，组件滑动速度越快。

### 示例

下面的例子演示了drawer的功能

<glyphix id="components-drawer" height="360" width="360" >

``` html
 <drawer class="drop-down">
      <drawer-navigation direction="down" class="drop-down1">
        <p>dawn panel</p>
      </drawer-navigation>
      <drawer-navigation direction="up" class="drop-down1">
        <p>up panel</p>
      </drawer-navigation>
       <drawer-navigation direction="left" class="drop-down1">
        <p>left panel</p>
      </drawer-navigation>
       <drawer-navigation direction="right" class="drop-down1">
        <p>right panel</p>
      </drawer-navigation>
</drawer>
```
``` css
.drop-down {
    background-color: pink;
  }
.drop-down1 {
    background-color: blue;
  }
p {
  background-color: lightgreen;
  text-align: center;
  margin: 10px;
}
```
</glyphix>


============================================================
FILE_PATH: src/original_docs/components/text.md

# text

文本组件，`text` 组件和 [`p` 组件](p)除了组件名称之外完全相同。


============================================================
FILE_PATH: src/original_docs/components/pullable.md

# pullable

`pullable` 组件用于在滚动列表内添加在顶部下拉和底部上拉时触发增量加载或者刷新交互的功能。`pullable` 组件默认是块级元素。

::: warning
<experimental /> 这是一个实验性组件，`pullable` 的功能并不稳定，并且动效可能不够自然。
:::

`pullable` 应该是 [`scroll`](scroll.md) 的第一个或者最后一个子组件。当它是第一个子组件时，在 `scroll` 内容的头部继续下拉将会触发 `pulling` 事件；相反，当 `pullable` 是 `scroll` 的最后一个子组件时，在底部上拉会触发 `pulling` 事件。

`pullable` 组件默认处于隐藏状态，只在被上/下拉的时候才会显示。下面的例子演示了 `pullable` 组件的使用方法。

<glyphix id="components-pullable-1" height="360" width="360" title="上/下拉加载更多">

```html
<scroll scrollbar>
  <pullable :hold="pulldown" on:pulling="onPulldown">
    <progress-arc busy start-angle="0" stop-angle="360" />
    <p>{{pulldown || 'keep pull down...'}}</p>
  </pullable>
  <p for="item in items">item ({{item}})</p>
  <pullable :hold="pullup" on:pulling="onPullup">
    <progress-arc busy start-angle="0" stop-angle="360" />
    <p>{{pullup || 'keep pull up...'}}</p>
  </pullable>
</scroll>
```

```js
export default {
  data: {
    pulldown: null,
    pullup: null,
    items: []
  },
  first: 0,
  last: 0,
  onInit() {
    this.update(0, 10)
  },
  update(first, last) {
    for (let i = this.first; i > first; --i)
      this.items.unshift(i)
    for (let i = this.last; i < last; ++i)
      this.items.push(i)
    this.first = first
    this.last = last
  },
  onPulldown(event) {
    this.pulldown = event ? 'please release' : 'updating...'
    if (!event) {
      setTimeout(() => {
        this.update(this.first - 5, this.last)
        this.pulldown = null
      }, 1000)
    }
  },
  onPullup(event) {
    this.pullup = event ? 'please release' : 'updating...'
    if (!event) {
      setTimeout(() => {
        this.update(this.first, this.last + 5)
        this.pullup = null
      }, 1000)
    }
  }
}
```

```css
scroll {
  display: flex;
  flex-direction: column;
}

scroll > p {
  background-color: #ddd;
  border-radius: 32px;
  margin: 12px;
  padding: 32px;
  text-align: center;
}

pullable {
  display: flex;
  justify-content: center;
  margin: 32px;
}

pullable > progress-arc {
  stroke-width: 0.25rem;
  margin-right: 16px;
}
```

</glyphix>

详细的用法请参考[使用说明](#使用说明)。

## 属性

### `hold` <decl type="bool" get set />

默认情况下，`pullable` 仅仅在顶部下拉或底部上拉时可见，但是当 `hold` 属性为 `true` 时，`pullable` 组件将保持显示状态。该属性通常在 [`pulling`](#pulling) 事件导致了内容更新时设置，并在内容更新完成后取消。

### `pulling` <decl type="bool" get listen />

当 `pullable` 在完全被拉出时会触发 `pulling` 事件，其事件值的含义为：
- `true`：在下拉/上拉达到 `pullable` 的完全拉出触发距离时触发此事件；
- `false`：在达到上述完全拉出条件后，用户松手时触发此事件。

下面的示例展示了 `pulling` 事件值的触发时机。你可以尝试缓慢地从列表顶部下拉，并注意触发 `pulling` 事件时的 toast 弹窗信息。

<glyphix id="components-pullable-pulling" height="360" width="360" title="pulling 事件">

```html
<scroll scrollbar>
  <pullable :hold="refresh" on:pulling="onPulling">
    <p>pulling...</p>
  </pullable>
  <p for="item in 10">item {{item}}</p>
</scroll>
```

```js
import prompt from '@system.prompt'

export default {
  data: {
    refresh: false
  },
  onPulling(event) {
    prompt.showToast({
      message: `pulling: ${event ? 'trigged' : 'release'}`
    })
    if (!event) {
      this.refresh = true
      setTimeout(() => this.refresh = false, 1000)
    }
  }
}
```

```css
scroll {
  display: flex;
  flex-direction: column;
}

scroll > p {
  background-color: #ddd;
  border-radius: 32px;
  margin: 12px;
  padding: 32px;
  text-align: center;
}

pullable {
  text-align: center;
  margin: 32px;
}
```

</glyphix>

## 使用说明

### 组件位置

`pullable` 组件必须是垂直 `scroll` 的第一个或者最后一个子元素。它会根据位置自动决定操作模式：当是第一个子元素是检测用户从列表顶部下拉的操作，反之亦然。

对于只需要下拉刷新的列表来说，以下用法就可以了：
```html
<scroll>
  <pullable :hold="refresh" on:pulling="onPulling">
    <p>pulling...</p>
  </pullable>
  <div for="item in items">
    ...
  </div>
</scroll>
```

JavaScript 代码中可以监听 `pulling` 事件，并控制 `refresh` 属性：
``` js
export default {
  data: {
    refresh: false
  },
  onPulling(hold) {
    if (!hold) { // 用户松手时 hold 为 false
      this.refresh = true // 表示正在刷新
      // 本示例中用一个定时器模拟加载操作，并在 1s 后停止加载
      setTimeout(() => this.refresh = false, 1000)
    }
  }
}
```

具体的效果请参考 [`pulling`](#pulling) 事件文档的示例。

### 提示内容控制

`pullable` 组件内部可以容纳各种组件来显示提示内容。如本文当前面的示例那样，你可以将加载动画和提示文本结合起来。此外，`pulling` 事件的值可以用于控制提示内容，通常建议使用这样的状态处理方式：
1. 为每个 `pullable` 组件设置一个响应式属性（例如 `refresh`），默认值为 `null`，`refresh` 属性还用于控制 `pullable` 的 [`hold`](#hold) 属性。
2. 处于初始状态时（即 `refresh` 为假），`pullable` 的提示内容应该提醒用户“继续拉拽以进行更新”。
3. 当用户下拉时，会触发 `pulling` 事件，根据其事件值采取 4 或 5 步骤。
4. `pulling` 为 `true` 时，应该提示用户“松手以开始刷新”。
5. `pulling` 为 `false` 时表示用户已经松手，此时应该将 `refresh` 置为 `true` 并开始刷新内容。并应该提醒用户“正在刷新中”。
6. 内容刷新完成后，重新将 `refresh` 置为 `false`，回到初始状态。

你也可以参考本文档的第一个示例，它同时实现了在列表头部下拉和尾部上拉的继续加载功能。该示例使用了一个技巧，仅使用一个响应式属性来控制 `pullable` 的所有状态。

该技巧将 `refresh` 响应式属性的初始值设置为 `null`（类似于 `false`），并使用这样的模板代码：
``` html
<pullable :hold="refresh" on:pulling="onPulling">
  <p>{{refresh || '继续下拉'}}</p>
</pullable>
```
当 `refresh` 没有设置时，一旦 `pullable` 被拉出来就会显示默认的“继续下拉”提示内容。然后，`onPulling` 事件回调函数应该这样编写：
``` js
export default {
  async onPulling(event) {
    this.refresh = event ? '请松手' : '更新中'
    if (!event) { // 松手时触发刷新操作
        await runRefreshJobs()
        this.refresh = null // 刷新完成后重置状态
    }
  }
}
```

### 限制

目前 `pullable` 组件存在一些限制。除了必须在垂直的 `scroll` 组件中使用外，你还需要保证列表元素的数量超出 `scroll` 可视区域的尺寸，否则可能会出现问题。此外，`pullable` 的交互效果可能也比较生硬。


============================================================
FILE_PATH: src/original_docs/components/qrcode.md

# qrcode

`qrcode` 组件用于显示 [QR Code](https://en.wikipedia.org/wiki/QR_code) 二维码。该组件可以显示任意文本数据，适合用于显示网址、支付码、登陆扫码链接等信息。

在流式布局中，`qrcode` 组件默认为块级元素（`block`），会单独占据一行显示。

## 属性

### `value` <decl type="string" get set />

设置要显示为二维码的文本数据。`qrcode` 组件会自动根据数据的长度和长度选择合适的版本，目前最高支持版本 $12$。

## CSS 说明

要想让二维码容易被扫描，应正确设置 `qrcode` 组件的 CSS 属性，这包括：
- `color`：二维码的码点颜色，一般设置为黑色（`black` 或者 `#000`）；
- `background-color`：二维码的背景色通常要是白色（`white` 或者 `#fff`）；
- `padding` / `margin`：足够的内外边距可以避免二维码和其他元素混淆，增加扫描识别率；
- `width` / `height`：二维码的尺寸必须足够大以方便拍摄。

默认情况下二维码组件的每个码点（module）会占据 $4\rm{px}\times 4\rm{px}$ 范围，这在手表上可能只是一个勉强能被识别的尺寸。但是 flex 等布局策略可能缩小二维码的尺寸，因此建议开发者根据需要手动设置二维码组件的 `width` / `height` 属性并在设备上进行测试。

下面的例子展示了二维码组件的使用方法，请注意 CSS 中为 `qrcode` 组件设置了各种边距，这都是为了保证二维码和其他界面元素有足够的间隔以免干扰扫描。

<glyphix id="qrcode-1" :height="450" :width="350">

``` html
<div>
  <qrcode :value="text"/>
  <p>{{ text }}</p>
</div>
```

``` js
export default {
  data: {
    text: 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array'
  }
}
```

``` css
div {
  background-color: black;
  padding: 8px;
}

qrcode {
  margin: 16px;
  padding: 16px;
  color: black; /* 将二维码前景色设置为黑色 */
  background-color: white; /* 将二维码背景色设置为白色 */
  border-radius: 16px;
}

p {
  color: white;
  font-size: 0.75rem;
}
```

</glyphix>

::: tip
应总是显式设置**高对比度**的二维码组件的码点颜色（`color`）和背景（`background-color`）样式。以免设备的默认样式主题和继承的样式属性偏差导致识别性下降。

同时，请设置足够大的内边距（`padding`），确保容易扫描识别。
:::



============================================================
FILE_PATH: src/original_docs/components/swiper.md

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


