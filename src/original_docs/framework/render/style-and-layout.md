# 样式和布局

Glyphix 的样式系统和 Web 技术中的 CSS 相似。通常直接在 UX 文件的 `<style>` 标签内定义 CSS。

## 编写 CSS

你可以在 `<style>` 标签内编写 CSS：

``` html
<style>
  div { display: flex; }
</style>
```

可以使用 `@import` 命令来导入 CSS 文件：

``` html
<style>
  @import 'style.css';
  div { display: flex; }
</style>
```

Glyphix 还提供有限的内联样式支持，内联样式直接写在组件的 style 属性中：
``` html
<div style="background: #f00; color: #fff"> ... </div>
```
内联样式的值是一个字符串，你可以通过更改这个字符串来更新样式。支持在内联样式中使用的 [CSS 属性](/framework/generic/styles.md)会添加 <badge type="info" text="内联" /> 标签。

::: warning
当前版本的内联样式效率较低，只应将其作为 js 逻辑更新组件样式的解决方案，大量使用可能引起性能问题。一般情况下应该使用在 `<style>` 标签中定义 CSS 规则的方案。
:::

## 样式选择器

目前，样式框架支持以下选择器：

- class 选择器
- type 选择器
- id 选择器
- 伪类（较少用到）
- 伪元素（较少用到）
- 后代选择器和直接后代选择器，例如 `div > .title` 或者 `div .title`
- 复合选择器，如 `#id.class` 或者 `div.class`

### class 选择器

class 选择器会选中具有对应 class 属性的组件，组件可以具有多个 class 值，例如
``` html
<p class="ceil content">...</p>
```
会匹配以下两个样式定义：
``` css
.ceil {
  background-color: #222;
  border-radius: 12px;
}

.content {
  font-size: 24px;
  padding: 12px;
}
```

### 组合选择器

支持用 `,` 为 rule-set 指定多个选择器：
``` css
#id, .class, div {
  display: flex;
  flex-direction: column;
  color: red;
}
```

### 继承属性

某些 CSS 属性可以从父级元素继承到子元素，以 `font-size` 为例：
``` html
<div>
  <p>Text</p>
</div>
```

``` css
div {
  font-size: 1.25rem;
}
```
尽管没有对 `<p>` 元素设置 `font-size` 属性，它还是会显示 `1.25rem` 的字号，这是由于 `<p>` 元素从父级 `<div>` 处继承了字号设置。换言之，在一个容器中设置了可以继承的样式属性之后，所有的子元素也会获得该属性设置。但要注意 CSS 属性继承机制的优先级很低，只有在元素没有指定被继承的样式属性时才会采用继承的值。假设对上面的例子使用以下 CSS：
``` css
* {
  font-size: 1rem;
}
div {
  font-size: 1.25rem;
}
```
由于 `*` 规则样式块的存在，现在 `<p>` 元素的字号会是 `1rem`，而不是采用继承值。

在 [CSS 属性](/framework/generic/styles.md)文档中，支持继承的属性会添加 <badge type="info" text="继承" /> 标签。

### 响应式支持

目前 `class` 属性和 `id` 属性都不支持响应式，因此
``` html
<div class="{{expr}}" id="{{expr}}"> ... </div>
```
都不支持，只能直接写静态的 `class` 和 `id` 属性值。

::: warning
开发者要留意 `class` 和 `id` 不支持响应式属性的限制！
:::

## 颜色值

### 颜色代码

颜色值支持 `#` 字符开头的 RGB 或 RGBA 颜色代码，合法的颜色代码有：

- `#RRGGBB[AA]`，例如 `#102000`，`#00ff0080`
- `#RGB[A]`，例如 `#0f0`，`#ff08`

如果颜色代码不包含 alpha 通道，那么该通道的值就是 `ff`（`#RRGGBB` 格式）或 `f`（`#RGB` 格式）。颜色代码中的每一位都是一个十六进制数，可用的字符为 `0-9`、`A-F` 和 `a-f`。`#RGB[A]` 是一种针对 `#RRGGBB[AA]` 代码的简写方法，例如 `#0f38` 的颜色和 `#00ff3388` 相同。

### 颜色函数

目前，CSS 块中支持用 `rgb()` 和 `rgba()` 函数定义颜色值。不支持 HSL 颜色格式。

### 标准颜色名

可以在 CSS 块中使用 Web 标准的颜色名，例如：
``` css
color: brown;
color: lightgray;
```

### 内联样式中的颜色

内联样式中只支持 `#` 开头的颜色代码，例如：
``` html
<p style="color: #ff00ff">...</p> <!-- 支持 -->
<p style="color: gray">...</p> <!-- 不支持，无法解析 -->
```

## 长度

长度值的通用格式为 `<value><unit>`，`value` 是长度的数值，`unit` 为长度单位，例如 `15px`。`value` 和 `unit` 之间不应添加空格。

还支持一种特殊的长度值 `auto`。这个长度值没有具体的数值和单位，实际渲染中的长度由具体的场景和规则来确定。

以下是可用的长度单位：

- `px`：以像素作为长度单位
- `pt`：将磅作为长度单位，一磅是 $1/72$ 英寸
- `%`：百分比长度单位，具体的值依属性和布局不同会有不同的换算关系
- [`rem`](/framework/application/font-config.md#rem-字号单位)：相对于系统默认字号的长度单位，例如 `1rem` 等于系统默认字号的尺寸，$1.5\rm rem$ 是前者的 $1.5$ 倍

其中 `pt` 是一种绝对长度单位，例如 `72pt` 对应 $1''$ （英寸）或者 $25.4\rm mm$，这与设备无关。而 `px` 是与设备有关的，但并不直接对应物理像素，其换算关系请参考 [`manifest.config.designWidth`](/framework/application/manifest.md#designwidth) 字段说明。百分比长度单位通常相对于父元素和元素本身的尺寸来计算，例如 `width`、`margin` 等 CSS 属性的百分比值是按父元素的尺寸来计算的，而 `border-radius` 则是按照元素自身的尺寸来计算的。

`rem` 单位专门用于字号（即 `font-size` 属性），这是一种简单的跨设备字体一致性方案。更多说明请参考 [`rem` 字号单位](/framework/application/font-config.md#rem-字号单位)。

## 布局

布局框架可以根据界面内容和屏幕的几何信息自动排列元素，开发者无需手动指定元素的位置和尺寸。布局框架是一种强大的机制，它可以让界面适用于不同分辨率或尺寸的设备，还可以处理变化的内容。Glyphix 的大部分原生组件支持两种自动布局模式：流式布局（flow layout）和弹性盒子布局（flexbox layout），同时也支持手动布局。某些原生组件具有强制的特殊布局，例如 [`swiper`](/components/swiper.md) 组件的子元素总是和视口一样大，而 [`stack`](/components/stack.md) 组件完全是用来提供堆叠布局的。

流式布局和弹性盒子布局的概念来自于 Web 标准，但针对低性能设备做了调整。

## 媒体查询

在 CSS 中，[媒体查询](media-query.md)主要是通过 [`@media` 规则](media-query.md#css-media-规则)根据特定的设备或媒体类型控制 CSS 样式。关于媒体查询的具体细节请参考相关[文档](media-query.md)。

## Less 扩展

如果要使用 [less](https://lesscss.org/) 作为 CSS 预处理器，首先要通过一种[包管理器](/tutorials/nodejs.md)安装 `less` 包：

::: code-tabs
@tab npm
```bash
npm install -D less
```

@tab pnpm
```bash
pnpm i -D less

@tab yarn
```bash
yarn add -D less
```
:::

::: tip
全局安装的 `less`（如 `npm install -g less`）不会被 Glyphix 打包工具识别，因此必须使用上面的方法在项目中安装 `less` 包。
:::

然后，你将可以在 UX 文件的 `<style>` 标签中使用 `lang="less"` 属性来指定样式类型：

``` html
<style lang="less">
@color: #4D926F;

.header {
  color: @color;
  .nested {
    font-size: 0.75rem;
  }
}
</style>
```
