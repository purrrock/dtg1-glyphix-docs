---
icon: layers-outline
---
# CSS 属性

本节介绍 Glyphix 框架支持的所有 CSS 属性，关于样式和布局机制的介绍请参考[这篇文档](/framework/render/style-and-layout.md)。

## 布局控制

### 基本属性

#### `display`

`display` 属性设置元素的布局方案。目前可以设置为以下值：

- `inline`：默认值，该元素生成一个或多个内联元素盒，它们之前或者之后并不会产生换行。在正常的流中，如果有空间，下一个元素将会在同一行上。
- `block`：该元素生成一个块级元素盒，在正常的流中，该元素之前和之后产生换行。
- `flex`：该元素的行为类似块级元素并且根据 `Flex` 布局它的内容。
- `inline-flex` 和 `inline flex`：元素的行为类似于内联元素并且它的内容根据 `Flex` 布局。
- `none`：这种模式下元素不会显示（不建议使用）。

#### `width`

`width` 属性指定元素的宽度，包含 `padding` 和 `border`（border-box）。如果元素位于布局容器中或者存在其他限制，最终的元素尺寸可能和 `width` 属性的值不一致。

::: tip
Glyphix 现在只支持 [border-box](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-sizing) 模式，`width` 的值始终包含 `padding` 和 `border`。
:::

`width` 属性的值是一个 CSS [长度](/framework/render/style-and-layout.md#长度)，具体的取值如下：

- `auto`：默认值，此模式会依据内容尺寸和布局约束自动计算元素的宽度。例如一个文本元素会根据文本内容的尺寸来确定宽度，而容器元素会根据内部元素的布局尺寸来确定宽度。
- `value [unit]`：使用某种长度单位来指定元素宽度，布局或其他约束可能会调整元素实际的尺寸。

使用 flex 布局中元素的 `width` 属性会作为元素的初始宽度，布局过程中会进一步调整为最佳的实际宽度。

#### `height`

`height` 属性指定元素的高度，包含 `padding` 和 `border`（border-box）。该属性的行为与 [`width`](#width) 类似。

### Flex 布局

#### `flex-direction`

设置 flex 布局容器时的主轴方向（水平或垂直），取值如下：

- `row`：默认值，主轴沿水平方向。
- `column`：主轴沿垂直方向。

`flex-direcion` 属性仅在元素使用 flex 布局时有效，例如：

```css
display: flex;
flex-direction: column;
```

#### `flex-flow`

`flex-flow` 是 `flex-direction` 和 `flex-wrap` 的简写。语法为

```css
flex-flow: <flex-direcion> <flex-wrap>;
```

目前 `flex-wrap` 属性还没有实装，因此这部分不会起作用。

#### `justify-content`

指定在使用 flex 布局时子元素在容器的主轴方向上的对齐方式。

属性值：

- `flex-start`：默认值，首个元素紧靠容器主轴的起始位置，后续元素依次排列。元素之间不额外填充空隙。
- `flex-end`：最后一个元素紧靠容器主轴的尾部位置，前面的元素依次排列。元素之间不额外填充空隙。
- `center`：所有元素依次排列在容器主轴的中间，主轴两端的剩余空间将会空出。元素之间不额外填充空隙。
- `space-between`：均匀排列每个元素，首个元素放置于起点，末尾元素放置于终点，剩余空间均匀填充在元素之间。
- `space-around`：均匀排列每个元素，每个元素周围分配相同的空间，首尾元素前后也会空出剩余空间。

#### `align-items` <badge type="info" text="内联" />

指定在使用 flex 布局时子元素在容器的交叉轴方向上的对齐方式。支持以下值：

- `stretch`：默认值，元素拉伸填充容器交叉轴的所有空间。
- `flex-start`：元素紧靠在容器交叉轴起点位置，不拉伸。
- `flex-end`：元素紧靠在容器交叉轴终点位置，不拉伸。
- `center`：元素在容器交叉轴上居中对齐，不拉伸。
- `baseline`：元素的交叉轴按照字体基线对齐。


**基线对齐**可以让文本、图片或者 [`switch`](/components/switch.md)、[`checkbox`](/components/checkbox.md) 等元素按照文本的基线位置对齐，从而保证比较整齐的视觉效果。注意，`align-items: baseline` 只在主轴方向为 [`row`](#flex-direction) 时有效。

#### `align-self` <badge type="info" text="内联" />

指定 flex 元素自身在交叉轴上的对齐方式，该属性的优先级比 `align-items` 更高。支持以下值：

- `auto`：默认值，使用 flex 容器的交叉轴对齐方式。
- `stretch`：元素拉伸填充容器交叉轴的所有空间。
- `flex-start`：元素紧靠在容器交叉轴起点位置，不拉伸。
- `flex-end`：元素紧靠在容器交叉轴终点位置，不拉伸。
- `center`：元素在容器交叉轴上居中对齐，不拉伸。
- `baseline`：`align-self` 不支持 `baseline` 值，和 `flex-start` 的效果相同。

::: tip
和 `align-items` 不同，你不能在 `align-self` 中使用 `baseline` 值。因此目前只能通过 flex 容器的 `align-items` 属性来设置交叉轴的基线对齐。
:::

#### `flex-grow`

指定 flex 元素在主轴方向上的 flex 增长系数。是 $[0, 100]$ 间的整数，默认值为 $0$。如果主轴方向上有剩余空间，各元素将增长按照增长系数比例所分配的剩余空间。因此，如果元素的 `flex-grow` 都为 $1$ 那么它们将平分主轴的剩余空间，而增长系数为 $0$ 的元素不会增长。

#### `flex-shrink`

指定 flex 元素在主轴方向的收缩率。是 $[0, 100]$ 间的整数，默认值为 $1$。如果主轴的剩余空间不足将对元素进行收缩。实际缩小的尺寸由元素初始尺寸、元素自己的收缩率占所有元素搜索率之和的比例，以及剩余空间共同决定。元素的收缩率越大或初始尺寸越大，那么该元素将产生更多的收缩尺寸。`flex-shrink` 为 $0$ 的元素不会收缩。

#### `flex`

`flex` 是 `flex-grow` 和 `flex-shrink` 的简写。语法为

```css
flex: <flex-grow> <flex-shrink>;
```

目前 Glyphix 没有引入 `flex-basis` 属性，因此不需要填写额外的值。

#### `max-height`(暂未支持)

设置元素的最大高度（max-height 属性不包括填充，边框，或页边距）。`max-height` 属性被指定为一个单一的[长度](/framework/render/style-and-layout.md#长度)值。

**默认值**：父控件的最大高度

#### `max-width`(暂未支持)

设置元素的最大宽度（max-width属性不包括填充，边框，或页边距）。`max-width` 属性被指定为一个单一的[长度](/framework/render/style-and-layout.md#长度)值。

**默认值**：父控件的最大宽度

#### `min-height`(暂未支持)

设置元素的最低高度（min-height属性不包括填充，边框，或页边距）。`min-height` 属性被指定为一个单一的[长度](/framework/render/style-and-layout.md#长度)值。

**默认值**：`0`

#### `min-width`(暂未支持)

设置元素的最小宽度（min-width 属性不包括填充，边框，或页边距）。`min-width` 属性被指定为一个单一的[长度](/framework/render/style-and-layout.md#长度)值。

**默认值**：`0`

### 定位方式

#### `position`

指定一个元素在文档中的定位方式。可以设置为以下值：

- `static`：默认值，指定元素使用正常的布局行为，即元素在文档常规流中当前的布局位置。此时 `top`, `right`, `bottom`, `left` 属性无效。
- `absolute`：元素会被移出正常文档流，并不为元素预留空间。通过指定元素相对于父元素的偏移，来确定元素位置。绝对定位的元素可以设置外边距（margins）。

#### `left`

指定元素相对于其包含元素左边缘的偏移量。

`left` 属性的值是一个 CSS [长度](/framework/render/style-and-layout.md#长度)，默认值是 `auto`。

#### `right`

指定元素相对于其包含元素右边缘的偏移量。

`right` 属性的值是一个 CSS [长度](/framework/render/style-and-layout.md#长度)，默认值是 `auto`。

#### `top`

指定元素相对于其包含元素顶部边缘的偏移量。

`top` 属性的值是一个 CSS [长度](/framework/render/style-and-layout.md#长度)，默认值是 `auto`。

#### `bottom`

指定元素相对于其包含元素底部边缘的偏移量。

`bottom` 属性的值是一个 CSS [长度](/framework/render/style-and-layout.md#长度)，默认值是 `auto`。

## 文本和字体

### 基本属性

#### `font-family` <badge type="info" text="继承" />

为元素指定一个有先后顺序的，有名字组成的字体族列表。多个字体之间使用逗号分隔，如果字体名字中存在空格还需要用引号包含字体名：

```css
font-family: serif;
font-family: "Times New Roma", serif;
```

字体名由 [`@font-face`](#font-face-规则) 规则定义。如果不定义 `font-family`，元素将继承父级元素的字体族，如果父级都没有定义字体族将使用[系统默认字体](/framework/application/font-config.md#默认字体)。

#### `font-size` <badge type="info" text="继承" />

指定元素的字体大小，是一个[长度](/framework/render/style-and-layout.md#长度)值。和 `font-family` 类似，`font-size` 也会从父级元素继承，在所有父级元素都没有定义字体大小的时候将使用[系统默认字体](/framework/application/font-config.md#默认字体)的字号。

#### `font-weight` <badge type="info" text="继承" />

指定元素的字重，即字体的粗细。值的范围是 $[100, 900]$ 的整数，默认值是 `400`。如果父级元素没有定义字重，则使用默认的 `400` 字重。如果找不到指定的字重，系统会使用最接近的可用字重。

::: tip
`font-weight` 属性只支持 `100` 的整数倍数值，例如 `100`、`200`、`300` 等。带有余数的值（如 `450`）会被四舍五入到最接近的整倍数。目前发售的设备仅支持 `400` 字重。
:::

#### `line-height` <badge type="info" text="继承" />

该属性用于设置多行元素的空间量，如多行文本的间距。`line-height` 属性被指定为一个单一的[长度](/framework/render/style-and-layout.md#长度)值或**数字**值。**默认** 为 `auto`。

除了长度值，`line-height` 还可以使用数字值，表示相对于字体大小的倍数。例如，`line-height: 1.5` 表示行高为字体大小的 1.5 倍。旧版本中使用 `line-height: 150%` 来表示相同的效果。<version-badge since="0.9" />

::: important 取值范围
计算后的 `line-height` 有效值范围为 $[0, 1000\rm px]$。其中 $0$ 行高会回退到默认行高（而不是完全没有行高）。无论使用长度还是数值（比例），计算后的行高都不能超过 $1000\rm px$，例如 `line-height: 2.0; font-size: 32px` 的计算结果为 $64\rm px$，因此是有效的行高值。
:::

##### 自动行高 <experimental /> <version-badge since="0.9" />

`line-height` 的 `auto` 值表示行高将根据字体大小自动计算，行为如下：
- 通常情况下，默认行高接近字体大小的 1.2 倍。
- 对于阿拉伯文、藏文等特殊字体，默认行高会自动加大以免行间重叠；这使得一段文本中的不同行可能具有不同的行高。
- 使用任何非 `auto` 的 `line-height` 值都会覆盖默认行高的行为，导致所有行具有相同的行高。
- `auto` 与 CSS 的 `normal` 行高语义相似，暂不支持直接使用 `normal` 关键字。

关于国际化场景中的行高行为请参考[ i18n 文档](/framework/application/i18n.md#自动行高)。

::: note 渲染一致性 <version-badge since="0.9" />
不同设备所使用的文本渲染行为不完全一致，`line-height: auto` 的默认行高值可能会有差异。一些设备不会自动调整特殊字体的行高，而是简单地使用固定行高，因此在使用自动行高时可能会出现行间重叠的情况。
:::

##### 行高继承

元素没有设置 `line-height` 时会继承父级元素的行高值。继承的行高是原始值，而不是计算后的行高值。例如，如果父级元素的 `line-height` 是 `1.5`，子级元素继承的也是 `1.5`，而不是父级元素计算后的行高值（即父元素字体大小的 $1.5$ 倍）。如果父级元素的 `line-height` 是 `auto`，子级元素继承的也是 `auto`，而不是父级元素计算后的默认行高值。

::: tip `auto` 行高与继承
`line-height: auto` 并不继承父级元素的行高，而是默认行高。要使用继承行高，必须不设置 `line-height` 属性。当前不支持 `inherit` 关键字来显式继承。
:::

#### `text-align` <badge type="info" text="继承" />

定义文字如何相对它的块父元素对齐，`text-align` 并不控制块元素自己的对齐，只控制它行内文本的对齐。

支持以下值：

- `left`: 左对齐
- `right`: 右对齐
- `hcenter`: 水平居中对齐
- `justify`: 自定调整
- `top`: 顶对齐
- `bottom`: 底对齐
- `vcenter`: 垂直居中对齐
- `baseline`: 基线对齐
- `center`: 水平垂直对齐

::: tip
`text-align: center` 是同时在水平和垂直方向上居中对齐，这和 CSS 中的 `text-align: center` 只在水平方向上居中对齐不同，应注意区分。如果只需要水平居中对齐，请使用 `text-align: hcenter`。
:::

**默认值**：`left`

#### `max-lines`

指定文本最多显示多少行，溢出的内容按照 [`text-overflow`](#text-overflow) 指定的方式处理。值类型为 number，默认值是 `0`，表示不限制最大行数。

语法和示例：

```css
max-lines: 0; /* 不限制最大行数 */
max-lines: 1; /* 固定为单行显示 */
max-lines: 2; /* 最多显示 2 行文本 */
max-lines: <number>; /* 指定最多可显示的文本行数 */
```

该属性兼容快应用标准的 `lines` 属性。

#### `text-overflow`

指定如何提示用户存在隐藏的溢出文本内容。可以直接裁剪或是显示一个省略号（`...`）。该属性配合 [`max-lines`](#max-lines) 使用，即只在文本行数达到 `max-lines` 限制时触发溢出行为，其他因为布局高度限制导致的裁剪则不会被考虑。

属性值：

- `clip`：溢出的文本直接被隐藏；
- `ellipsis`：当文本溢出时会在显示的文本后面添加省略号。

**默认值**：`clip`

<glyphix id="css-prop-text-overflow" height="100" width="600" title="clip 和 ellipses 对比">

```html
<div>
  <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>
  <p class="ellipsis">
    Lorem ipsum dolor sit amet, consectetur adipisicing elit.
  </p>
</div>
```

```css
div {
  display: flex;
}

p {
  background-color: #ddd;
  margin: 8px;
  padding: 8px;
  max-lines: 2;
}

.ellipsis {
  text-overflow: ellipsis;
}
```

</glyphix>

### `@font-face` 规则

`@font-face` CSS at-rule 指定一个用于显示文本的自定义字体。该字体可以在 [`font-family`](#font-family) 属性中作为字体名使用。

```css
@font-face {
  font-family: sans-serif;
  src: url("fonts/Roboto-Regular.ttf");
  font-weight: 400;
  font-style: normal;
}
```

建议在[应用级字体映射文件](/framework/application/font-config.md#应用级字体)中定义 `@font-face` 规则。本节介绍 `@font-face` 规则块中的属性定义。

#### `font-family`

所指定的字体名字将会被用于 [`font-family`](#基本属性-1) 属性。注意这里只能是一个字体名，而不是字体名的列表。例如：`font-family: <family-name>`。

#### `src`

指定字体文件的 URI，该属性的值是一个列表，允许开发者为字体指定多个字体文件。例如

```css
src: url("fonts/Roboto-Regular.ttf"), url("font/Other-Font.ttf");
```

目前 `src` 属性只支持 `url()` 函数或者字符串列表，Web 中可用的 `local()`、`format()` 等函数不受支持。

## 动画

有关动画的更多知识请参考[动画](../render/animation.md)章节。

### 基础属性

#### `animation`

定义元素要执行动画效果。目前支持的格式如下：

```css
animation: <name>;
animation: <duration> <timing> <name>;
```

各占位符描述如下：

- `<name>`：一个由 [`@keyframes` 规则](#keyframes-规则)定义的关键帧序列名；
- `<duration>`：动画持续时间，单位为秒或者毫秒，例如 `1000ms`，`0.2s`，默认为 `1s`；
- `<timing>`：[缓动函数](../render/animation.md#缓动函数)，默认为 `ease`。

### `@keyframes` 规则

请参考 MDN 的 [`@keyframes`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@keyframes) 文档。

## 变换和显示效果

#### `transform`

`transform` 属性允许开发者旋转、缩放倾斜或者平移元素。该属性对元素施加视觉上的变换效果，并不会改变元素的布局属性。`transform` 属性的值可以是下表中各种变换函数的级联：

|           值           | 描述                                                                |
| :--------------------: | ------------------------------------------------------------------- |
|     `scale(x, y)`      | 缩放转换，$x$ 和 $y$ 分别指定元素水平和垂直方向的缩放比例。         |
|    `rotate(angle)`     | 旋转变换，$\it angle$ 指定旋转的角度，单位可以是 `deg` 或者 `rad`。 |
|     `shear(h, v)`      | 错切变换，$h$ 为水平方向的错切距离，$v$ 为垂直方向的错切距离。      |
| `skew(angleX, angleY)` | 沿着 $x$ 和 $y$ 轴的倾斜元素。                                      |
|   `translate(x, y)`    | 平变换移，沿着 $x$ 和 $y$ 轴移动元素。                              |

例如下面的代码会将元素先缩放 $(2, 0.5)$ 倍，然后旋转 $100^{\circ}$：

```css
transform: scale(2, 0.5) rotate(100deg);
```

**默认值**：`none`

变换后的元素可能会被父级元素裁剪，也可以被位于后面的元素遮挡。可以使用 [`z-index`](#z-index) 属性提升元素的 Z 轴顺序，避免被同级别的元素遮挡。目前 `transform` 属性可能要配合 [`transparent`](#transparent) 属性才能正常工作，否则可能会产生错误的黑色背景。

#### `z-index`

`z-index` 属性设置元素的 Z 轴顺序，`z-index` 较大的重叠元素会覆盖较小的元素。

#### `opacity`

该属性指定了一个元素的不透明度。是一个取值范围为 $[0, 1.0]$ 的数值。

**默认值**：$1.0$（完全不透明）

::: warning
`0` 或 `1` 以外的 `opacity` 值会影响元素的绘制性能，建议仅在必要时使用该属性。如果只是需要使文本或背景呈现半透明，应该使用颜色值的 RGBA 格式来实现，例如 `rgba(255, 0, 0, 0.5)` 或 `#ff000080` 表示半透明的红色。
:::

#### `object-fit`

用来指定图像应该如何适应到其使用高度和宽度确定的框的策略。

属性值：

- `none`：默认值，图像将保持其原有的尺寸。
- `contain`：图像将被缩放，以在填充元素的内容框时保持其宽高比。整个对象在填充盒子的同时保留其长宽比。
- `cover`：图像在保持其宽高比的同时填充元素的整个内容框。如果对象的宽高比与内容框不相匹配，该对象将被剪裁以适应内容框。
- `fill`：图像正好填充元素的内容框。整个对象将完全填充此框。如果对象的宽高比与内容框不相匹配，那么该对象将被拉伸以适应内容框。
- `scale-down`：图像可以被保持长宽比地缩小以适应内容框的尺寸，但是当图像小于内容框的尺寸时不会进行缩放。`scale-down` 实际的缩放系数等效于 `none` 和 `contain` 中较小的那一个。

::: note
与 [Web 标准](https://developer.mozilla.org/docs/Web/CSS/Reference/Properties/object-fit)不同，`object-fit` 属性的默认值是 `none` 而不是 `fill`。详情请参考 [`image`](/components/image.md#object-fit) 组件的说明。
:::

#### `transparent`

设置元素是否透明。该属性通常不会影响元素的显示效果，但对存在快照的元素可能需要按照实际的透明情况配置此属性。

属性值：

- `false`：标记此元素不透明；
- `true`：标记元素是透明的。

**默认值**：`false`

#### `stroke-width`

指定某些组件绘制时的画笔宽度，例如 [`progress-arc`](/components/progress-arc.md)。值的类型是一个[长度](/framework/render/style-and-layout.md#长度)。

#### `visibility` <badge type="info" text="继承" />

设置元素是否显示，该属性不会影响布局。

属性值：

- `hidden`：隐藏元素；
- `visible`：显示元素。

**默认值**：`visible`

#### `filter` <experimental />

将模糊等效果应用于元素。目前支持这些值：

- `blur(<length>)`：将模糊效果应用于元素，例如 `blur(5px)`。

::: warning 实验性功能
在现有的设备上，使用 `blur()` 等过滤器效果可能会导致较严重的性能问题。需要注意的是，`blur()` 函数并非严格的高斯模糊，其模糊半径 $r$ 的支持范围为 $r \in [8, 300]\,\rm px$。具体来说：
- 当 $r \lt 8\rm px$ 时，不会产生模糊效果；
- 模糊程度随着 $r$ 的变化并不连续。

为了提升性能，在视觉效果允许的情况下，应尽量选择较大的模糊半径（建议 $r \ge 50\rm px$），这是因为 Glyphix 优化了这种情况。
:::

由于模糊效果的开销较大，建议配合原生组件的 [`quiescent`](/framework/generic/properties.md#quiescent) 属性来避免频繁的绘制更新。

#### `overflow` <experimental /> <version-badge since="0.9" />

`overflow` 属性用于指定当元素内容超过元素尺寸时的处理方式。该属性的值可以是以下之一：
```css
overflow: auto | clip | visible;
```
- `auto`：默认值，内容溢出时会被裁剪，等同于 `clip`。
- `clip`：内容溢出时会被裁剪，超出元素 content-box 尺寸的部分将不可见。
- `visible`：内容溢出时不会被元素自身的 content-box 裁剪，而是继续显示。

当 `overflow` 设置为 `visible` 时，内容可在最近 `clip` 祖先的 content-box 范围内绘制，不被自身及中间 visible 容器的裁剪影响。

::: tip 与 Web CSS 标准差异
`overflow` 属性的默认值不是 `visible`，而是默认裁剪。且 Glyphix 不支持 `scroll` 和 `hidden` 等值；也不支持 `overflow-x` 和 `overflow-y` 等子属性。
:::

##### 多级容器的 `overflow` 行为

`overflow: visible` 不是继承属性。如果希望最内层元素的溢出内容不被裁剪，需要从根到目标元素路径上的每一级容器都设置 `overflow: visible`。例如：
```html
<!-- 内层 item 的溢出内容可完整显示 -->
<div style="width:100px; height:100px; overflow:visible">     <!-- 中间容器 -->
  <p style="width:200px; line-height:100%; overflow:visible"> <!-- 溢出元素自身 -->
    藏文、泰文等长文本不出界
  </p>
</div>
```

##### i18n 文本的溢出问题

在国际化场景中，许多语言的文本高度较大，容易超出预留的行高范围，导致垂直被裁剪。对于这种情况，建议将文本元素的 `overflow` 设置为 `visible`，并且配合适当的 `line-height` 来确保文本内容能够完整显示。

下面的示例展示了在 `overflow: visible` 和 `overflow: clip` 两种情况下，行高过小时的效果：

<glyphix id="css-overflow-visible" height="80" width="640" title="文本 overflow">

```html
<div>
  <p>Some i18n text with large line height.</p>
  <p style="overflow: visible">Some i18n text with large line height.</p>
</div>
```

```css
div {
  font-size: 1.2rem;
  display: flex;
  flex-direction: column;
}

p {
  line-height: 22px;
  margin: 6px;
  border: 1px solid gray;
}
```

</glyphix>

上面的文本在 `line-height: 22px` 的情况下被裁剪了（如字母 'g' 的下半部分被切掉了），而设置 `overflow: visible` 后文本就能完整显示了。

更多说明请参考 [i18n 文档](/framework/application/i18n.md#文本溢出)。

##### 组件特定行为

各组件对于 `overflow` 的处理细节也有所不同，请参考 [`scroll`](/components/scroll.md#padding-和-overflow)、[`p`](/components/p.md)、[`marquee`](/components/marquee.md) 等组件的文档说明。

## 颜色和背景

#### `color` <badge type="info" text="继承" /> <badge type="info" text="内联" />

设置元素的文本颜色（前景色），颜色值的语法请参考[颜色值](/framework/render/style-and-layout.md#颜色值)。

**默认值**： `#ff0000`

#### `background-color` <badge type="info" text="内联" />

指定背景颜色，和 [`background-image`](#background-image) 属性互斥。颜色值的语法请参考[颜色值](/framework/render/style-and-layout.md#颜色值)。

**默认值**： `#ff0000` (黑色背景)

#### `background-image`

设置背景图片，和 [`background-color`](#background-color) 互斥。支持如下写法：

- `background-image: url("path/to/image")`：`url()` 函数给出背景图片的 [URI](../application/resource.md#uri-和路径)。

背景图片固定对齐到元素的右上角显示，并且不支持用类似 [`object-fit`](#object-fit) 类似的属性来拉伸或者缩放背景图片。对于此类复杂场景，建议使用 [`stack`](/components/stack.md) 和 [`image`](/components/image.md) 元素的组合来实现。

## 边距和边框

#### `margin`

设置元素的在四个方向上的外边距。`margin` 属性接受 $1\sim4$ 个值，即如下写法

- `margin: x`：将上、下、左、右边距的都设置为 `x`
- `margin: v h`：将上、下边距设置为 `v`，左、右边距设置为 `h`
- `margin: t h b`：将上边距设置为 `t`，下边距设置为 `b`，左、右边距设置为 `h`
- `margin: t r b l`：将上、右、下、左边距宽度设置为 `t`、`r`、`b`、`l`

每个值的类型为[长度](/framework/render/style-and-layout.md#长度)。

**默认值**：`0`。在流式布局中，将块级元素的左、右边距设置为 `auto` 可以使边距占满容器的宽度，例如：

```css
.center-box {
  margin: 0 auto;
}
```

会让类为 `center-box` 的块级元素在容器中居中。类似的，如果仅设置了左或者右边距为 `auto`，那么元素的该边距将会占满，产生居右或者居左的效果。

<glyphix id="css-margin-auto" height="120" width="360" title="auto 边距">

```html
<div>
  <p class="auto">margin: 0 auto</p>
  <p class="left-auto">margin: 0 0 0 auto</p>
  <p class="right-auto">margin: 0 auto 0 0</p>
</div>
```

```css
div {
  background-color: lightgreen;
}

.auto {
  margin: 0 auto;
}

.left-auto {
  margin: 0 0 0 auto;
}

.right-auto {
  margin: 0 auto 0 0;
}

div > p {
  border: 1px solid gray;
  margin-top: 4px;
  margin-bottom: 4px;
}
```

</glyphix>

#### `margin-left`

设置元素的左外边距。

#### `margin-top`

设置元素的上外边距。

#### `margin-right`

设置元素的右外边距。

#### `margin-bottom`

设置元素的下外边距。

#### `padding`

设置元素的在四个方向上的内边距。`padding` 属性接受 $1\sim4$ 个值，即如下写法

- `padding: x`：将上、下、左、右边距的都设置为 `x`
- `padding: v h`：将上、下边距设置为 `v`，左、右边距设置为 `h`
- `padding: t h b`：将上边距设置为 `t`，下边距设置为 `b`，左、右边距设置为 `h`
- `padding: t r b l`：将上、右、下、左边距宽度设置为 `t`、`r`、`b`、`l`

每个值的类型为[长度](/framework/render/style-and-layout.md#长度)。

**默认值**：`auto`。在默认值下，元素的 `padding` 为 $0$。

#### `padding-left`

设置元素的左内边距。

#### `padding-top`

设置元素的上内边距。

#### `padding-right`

设置元素的右内边距。

#### `padding-bottom`

设置元素的下内边距。

#### `border`

设置元素的边框样式。支持如下写法：

- `border: <length>`：表示轮廓宽度为 `<length>` ，颜色为黑色的边框；
- `border: solid`：表示轮廓宽度为 `1 px` ，颜色为黑色的边框；
- `border: <length> solid <color>`：表示轮廓宽度为 `<length>` ，颜色为 `<color>` 的边框。

其中 `<length>` 是一个[长度](/framework/render/style-and-layout.md#长度)，而 `<color>` 是一个[颜色值](/framework/render/style-and-layout.md#颜色值)。

Glyphix 只支持元素具有所有边框或者上、下、左、右边框之一。例如 `border: solid` 会让元素具有所有边框，而 `border-top: solid` 则让元素具有上边框。当 CSS 中同时存在这些边框属性时只有最后一个属性会生效。

#### `border-top`

指定元素的上边框样式。值的格式和 [`border`](#border) 属性一致。

#### `border-right`

指定元素的右边框样式。值的格式和 [`border`](#border) 属性一致。

#### `border-bottom`

指定元素的下边框样式。值的格式和 [`border`](#border) 属性一致。

#### `border-left`

指定元素的左边框样式。值的格式和 [`border`](#border) 属性一致。

#### `border-radius`

**默认值**：`0 px`

设置边框的圆角半径。目前支持一个[长度](/framework/render/style-and-layout.md#长度)值。`border-radius` 属性只在元素具有所有边框时生效（参见 [`border`](#border) 属性）。

## 伪类

### `active`

按钮等元素在按下状态时会会具有此伪类。

### `disabled`

元素处于 [`disabled`](properties.md#disabled) 状态下时具有此伪类，此时元素不响应手势事件。通常可以将元素的透明度降低来向用户传达此状态，例如：

```css
<some-selector>:disabled {
  opacity: 0.5;
}
```

更完整的示例请参考 [`disabled`](properties.md#disabled) 属性。
