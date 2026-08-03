# 属性修饰符

普通的属性操作可以实现属性的设置、监听功能。但是某些场合会对属性操作有一些共性需求，例如：要求组件的某个属性值设置操作不是立即变更到新的值，而是使用动画来过渡。直接的解决方法是编写逻辑代码来实现过渡效果，但实际上这种逻辑对任何属性而言都是通用的。

为了简化或复用某些通用属性操作的代码，Glyphix 内置了若干属性修饰符。修饰符是使用 `.` 表示的属性后缀，例如

``` html
<progress :value="progress" value.transition="{curve: 'ease'}"/>
```

组件的 XML 属性中填写的属性修饰符键值对 `value.transition="{curve: 'ease'}"` 和属性键值对 `value="{{progress}}"` 是相互独立的，它们可能要求完全不同的参数。

本文档将介绍各属性修饰符的功能。

## `transition` 修饰符

此修饰符会代理属性的赋值操作，将原本直接对属性进行赋值的过程转变成按照 `transition` 修饰符指定的动画过渡方式渐变赋值。例如

``` html
<!-- transition 修饰符定义 value 属性的过渡效果 -->
<progress :max="1000" :value="progress" value.transition="{curve: 'ease'}"/>
<!-- 无过渡效果 -->
<progress :max="1000" :value="progress" />
```


<glyphix id="prop-modifier-transition" height="68" width="480" inline>

``` html
<div>
  <progress :max="1000" :value="progress" value.transition="{curve: 'ease'}"/>
  <progress :max="1000" :value="progress" />
</div>
```

``` css
div > * {
  margin: 8px;
  height: 0.75rem;
}
```

``` js
export default {
  data: {
    progress: 500
  },
  onInit() {
    setInterval(() => this.progress = parseInt(Math.random() * 1000), 3000)
  }
}
```

</glyphix>

由于定义了 [`progress`](/components/progress.md) 组件的 `value.transition` 修饰符，因此每次修改 `this.progress` 时，`progress` 组件的显示值不会直接跳变到新值，而是通过一个动画进行渐变。这个效果不需要编写任何动画逻辑就可以实现。

::: tip
例子中的 `progress` 组件的 `value` 属性是整数，由于默认的 $[0, 100]$ 范围在过渡动画中容易产生分段感，所以例子中通过 `:max="1000"` 来增加 `value` 的取值范围从而使动画更平滑。
:::

### 插值计算

目前只有原生组件的部分属性支持 `transition` 修饰符。支持的属性必须具有“可插值”的值类型，具体来说：对所有的属性值类型的值 $a$ 和 $b$ 和进度 $p \in [0,1]$，运算 $(1-p)*a+p*b$ 有效。

JavaScript 的 `number` 类型是可插值的，除此之外变换和颜色值也可以插值。

#### 变换

变换通常使用字符串来定义，例如 `scale(2) rotate(30deg)`。字符串本身不可插值，但是当它用于变换属性时则是可以插值的（因为这些字符串会被解析为变换操作序列，而它们是可插值的）。通常而言会逐个按变换操作进行插值。例如 `scale(2) rotate(30deg)` 和 `scale(1) rotate(90deg)` 在插值过程中每一帧的变换都包含缩放和旋转两个步骤，其中缩放倍数从 $2$ 过渡到 $1$，而旋转角度从 $30\deg$ 过渡到 $90\deg$。

#### 颜色

颜色通常使用字符串代码来表示，例如 `#ff0000`。颜色的插值按红、绿、蓝和透明通道逐一计算。

### `Transition` 对象

`transition` 修饰符的值类型是 `Transition` 对象：
``` ts
interface Transition {
  curve?: string,
  duration?: number
}
```

#### `curve` <decl type="?: string"/>

指定过渡动画的[缓动函数](../render/animation.md#缓动曲线)，默认为 `'ease'`。

#### `duration` <decl type="?: number"/>

动画的持续时间，单位为秒，默认为 `1`。
