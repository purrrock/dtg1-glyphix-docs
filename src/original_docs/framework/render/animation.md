# 动画

## 基础知识

“动画”通过连续、快速地播放若干帧，从而使界面呈现在一段时间的过渡效果。在 Glyphix 中有两种方法实现动画：
- 通过快速播放一组图片的**轮播图动画**；
- 通过程序自动计算中间帧的**关键帧动画**。

### 关键帧动画

轮播图动画是通过专门的组件来实现的，它的原理和视频类似。本节主要介绍关键帧动画。下面的例子演示了一个关键帧动画：

<div class="animation-example-box">
  <div style="visibility: hidden">Hello World!</div>
  <div class="animation-span">Hello World!</div>
  <div class="keyframes-from">Hello World</div>
  <div class="keyframes-to">Hello World</div>
</div>

要实现这个动画，开发者需要定义动画的的起始帧（红色文本）和结束帧（绿色文本）。而程序会自动计算动画中的每一帧。由开发者指定的开始帧和结束帧被成为**关键帧**，关键帧动画还允许定义中间关键帧。由程序计算的帧称为**插值帧**。在这个例子中，起始关键帧为原始的文本组件，而结束关键帧是对该文本平移 $200\rm px$ 并缩放 $0.75$ 倍，插值帧则是根据动画进度计算的中间变换值。例如动画播放到 $50\%$ 时的插值帧是将原文本平移 $100\rm px$ 并缩放 $0.875$ 倍。

在相比于轮播图，关键帧动画更容易制作，并且适用于界面元素的过渡效果（例如按钮的按下动效）。

关键帧动画主要由几个要素来定义：
- 关键帧：人工指定的帧，通常来说 $0\%$ 和 $100\%$ 进度时会使用关键帧；
- 动画时长：即动画进度从 $0\%$ 到 $100\%$ 所需要的时间；
- 缓动函数：定义插值帧的进度调整曲线，线性的动画效果观感比较差；
- 重复次数、延时、播放方向（正向、反向、往复）等。

### 属性动画

Glyphix 中使用的关键帧动画主要是**属性动画**。即关键帧是由元素的属性来定义，而插值帧计算中间属性值。例如 [`transition` 属性修饰符](../component/prop-modifier.md#transition-修饰符)所实现的动画那样：动画系统会自动处理属性变化的过渡效果。

属性动画主要分为两类：
- 组件属性动画：为组件的属性添加动画过渡，由 `transition` 属性修饰符实现；
- CSS 动画：为样式属性添加动画。

## 缓动函数

缓动函数定义动画进度的调整曲线，从而避免单调的线性插值效果。读者可以到 https://cubic-bezier.com/ 体验缓动函数的效果。

在 [`transition` 属性修饰符](../component/prop-modifier.md#transition-修饰符)和 CSS 的 [`animation` 属性](../generic/styles.md#animation)中。缓动函数是一个字符串，其内容如下表所示。

|               值                | 描述                                                                                                                                   |
| :-----------------------------: | -------------------------------------------------------------------------------------------------------------------------------------- |
|             `ease`              | 默认值。动画以低速开始，然后加快，并在结束前变慢。                                                                                      |
|            `ease-in`            | 动画以低速开始。                                                                                                                       |
|           `ease-out`            | 动画以低速结束。                                                                                                                       |
|          `ease-in-out`          | 动画以低速开始和结束。                                                                                                                 |
|            `linear`             | 动画从头到尾的速度是相同的。                                                                                                           |
|            `spring`             | 模拟弹簧回弹的动画效果，等效于 `spring(1,1,1)`。                                                                                       |
| `cubic-bezier(x1, y1, x2, y2)`  | 使用[三次贝赛尔曲线](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function#cubic_b%C3%A9zier_easing_function)定义缓动函数。 |
| `spring(spring, damping, mass)` | 模拟弹簧回弹的动画效果，可以指定弹性系数、阻尼和质量参数（需要文档）。                                                                 |

对于大多数动画来说，`ease` 缓动函数能得到不错的效果，复杂的需求则可以使用 `cubic-bezier()` 函数。`spring()` 函数则适用于指针旋转等需要回弹物理效果的场景。

## 示例

### 按钮动画

如下所示，默认的按钮效果是没有按下动画的：

<Glyphix id="render-animation-button1" width="200" height="80">

``` html
<div>
  <button>Button</button>
</div>
```

``` css
button {
  display: block;
  background-color: #8af;
  padding: 8px 16px;
  border-radius: 50%;
  margin: 16px;
}

button:active {
  transform: scale(1.1, 1.1);
}
```
</Glyphix>

使用 CSS 的 [`animation`](../generic/styles.md#animation) 属性可以为这个按钮添加交互动画：

<Glyphix id="render-animation-button2" width="200" height="80">

``` html
<div>
  <button>Button</button>
</div>
```

``` css
/* 定义 active 伪类关键帧，不写 from / 0% 关键帧
   时动画会从组件的当前状态开始播放 */
@keyframes button-active {
  to {
    transform: scale(1.1, 1.1);
  }
}

/* 定义无伪类关键帧，不写 from / 0% 关键帧
   时动画会从组件的当前状态开始播放 */
@keyframes button-normal {
  to {
    transform: scale(1, 1);
  }
}

button {
  display: block;
  background-color: #8af;
  padding: 8px 16px;
  border-radius: 50%;
  margin: 16px;
  /* 在无伪类样式中通过动画将按钮缩放到 100% */
  animation: 0.2s ease button-normal;
}

button:active {
  /* 在 active 伪类样式中通过动画将按钮缩放到 120% */
  animation: 0.2s ease button-active;
}
```
</Glyphix>

目前不支持 CSS `transition` 属性，所以必须在按钮的无伪类样式和 `active` 伪类样式中分别定义动画。


### `spring` 动画效果

`spring` 缓动函数提供类似弹簧阻尼振动的插值效果，这种效果可以用于运动的指针。下面的示例中演示了两种实现指针动画的方法：左边是均匀的指针旋转，而右边使用 `spring` 缓动函数。

<Glyphix id="render-animation-spring" width="400" height="200">

``` html
<div class="window">
  <div class="clock">
    <div class="pointer"
      transform="translate(0, -40%) rotate({{angle}}deg) translate(0, 50%)"
      transform.transition="{curve: 'linear', duration: 1}" />
    <div class="pointer invisible"></div>
  </div>
  <div class="clock">
    <div class="pointer"
      transform="translate(0, -40%) rotate({{angle}}deg) translate(0, 50%)"
      transform.transition="{curve: 'spring(1.2,1,1.2)', duration: 1}" />
    <div class="pointer invisible"></div>
  </div>
</div>
```

``` css
.window {
  display: flex;
}

.clock {
  background-color: gray;
  border-radius: 50%;
  flex: 1;
  margin: 4px;
}


.pointer {
  background-color: #0f0;
  width: 12px;
  height: 50%;
  margin: 4px auto;
  border-radius: 50%;
}

.invisible {
  visibility: hidden;
}
```

``` js
export default {
  data: {
    angle: 0
  },
  onInit() {
    setInterval(() => this.angle += 5, 1000)
  }
}
```

</Glyphix>

这两种动画都以 $1$ 秒钟的间隔更新指针角度，但是组件属性的 `transition` 修饰符会自动添加旋转动画。

<style scoped>
@keyframes animation-example {
  to {
    transform: translate(200px, 0) scale(0.75);
  }
}

.animation-example-box {
  position: relative;
  width: 320px;
  margin: 0 auto;
  font-family: sans-serif;
  font-size: 24px;
  user-select: none;
}

.animation-span {
  position: absolute;
  left: 0;
  top: 0;
  animation: 5s ease infinite animation-example;
}

.keyframes-from, .keyframes-to {
  color: red;
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0.5;
}

.keyframes-to {
  color: green;
  transform: translate(200px, 0) scale(0.75);
}
</style>
