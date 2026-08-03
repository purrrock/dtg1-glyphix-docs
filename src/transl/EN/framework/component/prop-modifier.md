# Property Modifiers

Standard property operations allow for setting and observing properties. However, certain scenarios have common requirements for property operations—for example, requiring that setting a component's property value does not immediately change to the new value, but instead transitions using an animation. The direct solution is to write logic code to implement the transition effect, but in reality, such logic is common to any property.

To simplify or reuse code for certain common property operations, Glyphix includes several built-in property modifiers. Modifiers are property suffixes denoted by `.`, for example:

``` html
<progress :value="progress" value.transition="{curve: 'ease'}"/>
```

The property modifier key-value pair `value.transition="{curve: 'ease'}"` and the property key-value pair `value="{{progress}}"` filled in the component's XML attributes are independent of each other, and they may require completely different parameters.

This document will introduce the functions of each property modifier.

## The `transition` Modifier

This modifier proxies the property assignment operation, transforming the process of directly assigning a value to the property into a gradient assignment according to the animation transition method specified by the `transition` modifier. For example:

``` html
<!-- The transition modifier defines the transition effect for the value property -->
<progress :max="1000" :value="progress" value.transition="{curve: 'ease'}"/>
<!-- No transition effect -->
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

Because the `value.transition` modifier of the [`progress`](/components/progress.md) component is defined, every time `this.progress` is modified, the displayed value of the `progress` component does not jump directly to the new value, but instead transitions smoothly via an animation. This effect can be achieved without writing any animation logic.

::: tip
The `value` property of the `progress` component in the example is an integer. Since the default range of $[0, 100]$ is prone to segmentation artifacts during transition animations, the example uses `:max="1000"` to increase the value range of `value`, thereby making the animation smoother.
:::

### Interpolation Calculation

Currently, only some properties of native components support the `transition` modifier. Supported properties must have an "interpolatable" value type. Specifically: for all property value types $a$ and $b$ and progress $p \in [0,1]$, the operation $(1-p)*a+p*b$ must be valid.

The JavaScript `number` type is interpolatable. In addition, transformations and color values can also be interpolated.

#### Transformations

Transformations are usually defined using strings, such as `scale(2) rotate(30deg)`. The string itself is not interpolatable, but when used for transformation properties, it is interpolatable (because these strings are parsed into sequences of transformation operations, which are interpolatable). Generally speaking, interpolation is performed step by step for each transformation operation. For example, in the interpolation between `scale(2) rotate(30deg)` and `scale(1) rotate(90deg)`, the transformation in each frame includes two steps: scaling and rotation. The scale factor transitions from $2$ to $1$, while the rotation angle transitions from $30\deg$ to $90\deg$.

#### Colors

Colors are usually represented using string codes, such as `#ff0000`. Color interpolation is calculated individually for the red, green, blue, and alpha channels.

### The `Transition` Object

The value type of the `transition` modifier is the `Transition` object:
``` ts
interface Transition {
  curve?: string,
  duration?: number
}
```

#### `curve` <decl type="?: string"/>

Specifies the [easing function](../render/animation.md#easing-curves) for the transition animation. The default is `'ease'`.

#### `duration` <decl type="?: number"/>

The duration of the animation in seconds. The default is `1`.