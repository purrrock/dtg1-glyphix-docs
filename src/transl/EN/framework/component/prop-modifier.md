# Property Modifiers

Standard property operations allow you to set and observe properties. However, certain scenarios have common requirements for property operations. For example, you might want a component's property value not to change immediately when set, but rather transition smoothly using an animation. A direct solution is to write custom logic to achieve the transition effect, but in reality, such logic is common to any property.

To simplify or reuse code for certain common property operations, Glyphix includes several built-in property modifiers. Modifiers are property suffixes denoted by `.`, for example:

``` html
<progress :value="progress" value.transition="{curve: 'ease'}"/>
```

The property modifier key-value pair `value.transition="{curve: 'ease'}"` and the property key-value pair `value="{{progress}}"` written in the component's XML attributes are independent of each other, and they may require completely different parameters.

This document will introduce the functions of each property modifier.

## `transition` Modifier

This modifier proxies property assignment operations, transforming the direct property assignment process into a gradient assignment following the animation transition method specified by the `transition` modifier. For example:

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

Because the `value.transition` modifier is defined for the [`progress`](/components/progress.md) component, every time `this.progress` is modified, the displayed value of the `progress` component does not jump directly to the new value, but rather transitions smoothly via an animation. This effect can be achieved without writing any animation logic.

::: tip
The `value` property of the `progress` component in the example is an integer. Since the default $[0, 100]$ range is prone to stuttering during transition animations, the example uses `:max="1000"` to increase the value range of `value`, thereby making the animation smoother.
:::

### Interpolation Calculation

Currently, only some properties of native components support the `transition` modifier. Supported properties must have "interpolatable" value types. Specifically: for all property value types $a$ and $b$ and progress $p \in [0,1]$, the operation $(1-p)*a+p*b$ must be valid.

The JavaScript `number` type is interpolatable. In addition, transforms and color values can also be interpolated.

#### Transforms

Transforms are usually defined using strings, such as `scale(2) rotate(30deg)`. The string itself is not interpolatable, but when used as a transform property, it is interpolatable (because these strings are parsed into a sequence of transform operations, which are interpolatable). Generally speaking, interpolation is performed step-by-step for each transform operation. For example, during the interpolation of `scale(2) rotate(30deg)` and `scale(1) rotate(90deg)`, the transform in each frame contains two steps: scaling and rotation. The scale factor transitions from $2$ to $1$, while the rotation angle transitions from $30\deg$ to $90\deg$.

#### Colors

Colors are usually represented using string codes, such as `#ff0000`. Color interpolation is calculated channel by channel for red, green, blue, and alpha (transparency).

### `Transition` Object

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