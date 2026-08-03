# 跨设备适配

当你的应用需要在多种设备商运行时，可能会遇到多种交互兼容性问题，例如：
- 不同设备的屏幕分辨率和尺寸都不相同，应用在不同设备中应该进行适当的布局和缩放；
- 不同设备的系统字体、字号不尽相同，应用程序应遵循系统风格；
- 界面布局要考虑不同的屏幕形状，如圆形屏幕常使用鱼眼变形的列表；
- 不同的屏幕形状和屏幕分辨率下，页面的安全边距可能不同。

本文档介绍怎样在编写较少的适配代码的情况下，通过 Glyphix 应用框架来开发兼容广泛设备的手表应用。

## 模拟器参数

在使用 `gx emu` 命令启动模拟器时，`-d` 或 `--device` 参数可以指定被模拟的设备，例如 `gx emu -d default-watch-466x466` 将会模拟器分辨率为 $466\times 466$ 像素的圆屏设备。`gx emu` 会记住上次 `-d` 指定的设备，而不是自动回退到默认设备。

::: tip
如果你安装了 gx 命令的 PowerShell 或者 Zsh 补全脚本，那么输入 `gx emu -d` 之后就可以通过 `Tab` 键补全可用的设备名称。否则请先使用 `gx list device` 查看设备列表，例如：
``` bash
$ gx list device
default-watch-466x466
default
```
:::

默认情况下，模拟器的屏幕分辨率和实际设备一样，可以通过 `-r` 或 `--real-scale` 参数（`gx emu -r`）来模拟设备的实际屏幕尺寸而不是分辨率。不建议在非高分辨率显示器中使用 `-r` 参数，否则会导致显示过于模糊。

通过 `-d` 和 `-r` 参数就可以通过模拟器来测试多种设备的显示效果，而不必准备物理设备。

## 多分辨率适配

在 Web 开发中，开发者通常依赖媒体查询和 `px` 等单位进行精细的布局和样式调整。然而，在穿戴设备上，不同设备的最佳字号差异过大，难以在开发时精确规划。更重要的是，如何通过统一的视觉规范，确保一款设备中的所有应用具备一致的可读性和操作体验，是穿戴设备 UI 设计的核心问题之一。

以智能手表为例，不同设备的屏幕宽度可能分布在 $360\rm px$ 到 $466\rm px$ 之间，而高度则介于 $450\rm px$ 到 $500\rm px$ 左右。因此尽管存在 [`designWidth`](manifest.md#designwidth) 配置，通常也不能通过 `px` 单位来指定大多数界面元素的尺寸。无论怎样缩放，`px` 单位总会存在这些问题：
- 设备的 DPI 或者尺寸不同，无法通过固定的像素尺寸得到理想的字号；
- 圆形屏幕和矩形屏幕的宽高比差异大，难以通过像素值指定大的填充空隙。

本节将介绍针对这些问题的布局技巧。

### 字号规范

请参考字体规范的 [`rem` 字号单位](font-config.md#rem-字号单位)指南来规范应用中的字号，**不要**使用 `px` 作为字号单位。

### 边距配置

可以使用 `px` 等任何[长度](/framework/render/style-and-layout.md#长度)单位来指定较小的边距值，例如：

``` css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  padding: 8px; /* 使用 px 作为边距单位 */
  margin: 8px;
}
```

<glyphix id="font-config-margins-pixel" height="80" width="300" inline>

```html
<p>The message text.</p>
```

```css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  padding: 8px;
  margin: 8px;
}
```

</glyphix>

其中除了 `font-size` 使用了 `rem` 以外，其他几处属性均使用 `px` 单位。这是因为 Glyphix 会为目标设备自动缩放 `px` 单位的比例，且较小的 `px` 值通常没有溢出或者裁剪风险。

但是当尺寸值很大时，更建议建议使用百分比值，例如：

``` css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  /* 左内边距使用百分比单位，请注意示例文本左侧的边距 */
  padding: 8px 8px 8px 40%;
}
```

<glyphix id="font-config-margins-percent" height="80" width="300" inline>

```html
<p>Message</p>
```

```css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  padding: 8px 8px 8px 40%;
}
```

</glyphix>

这样可以更好地适配分辨率差异很大的设备。

::: warning
手表设备的屏幕高度差异较大，垂直方向上的大边距需要更加注意兼容性问题。
:::

### flex 布局

除了百分比长度单位以外，flex 布局可以提供更灵活的界面适应能力。应当优先使用 flex 布局，然后才是百分比长度单位。并应该避免手动布局，即直接指定元素的 `width` 和 `height` CSS 属性。

应该进行手动布局的一种例外情况是显示网络图标的界面，例如：
``` html
<scroll>
  <div class="item" for="item in items">
    <image :src="item.icon" />
    <p>{{ item.title }}</p>
  </div>
</scroll>
```
如果说 `item.icon` 指向的图片尺寸并不固定，那么为 `image` 元素指定合适的宽高会更美观，例如：
``` css
scroll {
  display: flex;
  flex-direction: column;
}

.item {
  display: flex;
}

/* 为网络图标指定固定的宽高 */
.item > image {
  width: 92px;
  height: 92px;
  border-radius: 10px;
  object-fit: fill; /* 必要时拉伸或缩放图片 */
}

/* item 中的文本占据行上的剩余空间 */
.item > p {
  flex: 1;
}
```

由于 [`image`](/components/image.md) 组件会自动居中显示图片，因此不必关心图片长宽比的差异。

### 媒体查询

当任何布局策略都无法适应分辨率的差异时，还可以使用[媒体查询](/framework/render/media-query.md)针对性地进行调整。

## 屏幕形状适配

智能手表通常有圆形和矩形两种屏幕形状。其中圆形屏幕的四角需要留出较大的安全边距，并且可能会使用鱼眼效果的列表。

### 媒体查询

以顶栏为例，圆形屏幕可能需要顶栏文本居中对齐，而矩形屏幕的顶栏文本是左对齐的。以下示例展示了两种屏幕形状对应的布局差异。

<glyphix id="circle-square-screens" height="400" width="800" title="异形屏幕布局">

```html
<div class="screens">
  <div class="square-screen">
    <p>TITLE BAR</p>
  </div>
  <div class="circle-screen">
    <p>TITLE BAR</p>
  </div>
</div>
```

```css
p {
  font-size: 1.25rem;
  color: #353535;
  margin: 32px;
}

.screens {
  display: flex;
}

.screens > div {
  display: flex;
  flex-direction: column;
  background-color: #adb5bd;
  flex: 1;
  margin: 10px;
}

.square-screen {
  border-radius: 10%;
}

.circle-screen {
  border-radius: 50%;
  /* 圆形屏幕的左右侧通常会留空，以改善显示效果 */
  padding: 0 48px;
}

.square-screen > p {
}

.circle-screen > p {
  text-align: center;
}
```

</glyphix>

可以通过媒体查询的 [`shape`](/framework/render/media-query.md#shape) 特性来分别处理两种屏幕形状，例如：
``` css
.title {
  font-size: 1.25rem;
  color: #353535;
  /* 默认情况下，标题仅仅是在四周留出 32px 的安全间距。 */
  margin: 32px;
}

/* 这些样式规则仅对圆形屏幕生效。 */
@media (shape: circle) {
  .title {
    /* 圆形屏幕时，标题文本应该居中。其他属性继承自上面的 .title 规则。 */
    text-align: center;
  }
}
```
这段 CSS 代码首先定义方形屏幕的样式规则，然后在一个媒体查询块中覆盖为适用于圆形屏幕的规则。

### 模板宏

使用媒体查询可以针对不同类型的设备来定义 CSS 规则，而结合[模板宏](/framework/component/template-macro.md)和 [`media-query` 属性](/framework/render/media-query.md#组件的-media-query-属性)可以为不同的设备应用不同的 UX 模板结构。这种技术可以自动为圆形设备上的列表界面添加鱼眼变形效果。

具体的使用方法请参考[模板宏](/framework/component/template-macro.md)章节。

## JavaScript 适配

如果需要为不同的设备编写不同的逻辑，那么还可以获取[设备信息](/api/system-device.md)。例如可以通过 [`device.screenShape`](/api/system-device.md#screenshape) 在运行时获取设备的屏幕形状枚举值。
