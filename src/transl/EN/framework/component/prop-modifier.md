# attribute modifier


Ordinary attribute operations can realize attribute setting and monitoring functions. However, in some situations, there are some common requirements for attribute operations. For example, it is required that a certain attribute value setting operation of a component is not changed to a new value immediately, but uses animation to transition. The immediate solution is to code logic to implement the transition effect, but in reality this logic is universal for any property.


In order to simplify or reuse the code of some common attribute operations, Glyphix has several built-in attribute modifiers. Modifiers are attribute suffixes represented using `.`, e.g.


``` html
<progress :value="progress" value.transition="{curve: 'ease'}"/>
```


The attribute modifier key-value pair `value.transition="{curve: 'ease'}"` and the attribute key-value pair `value="{{progress}}"` filled in the component's XML attributes are independent of each other, and they may require completely different parameters.


This document will introduce the functions of each attribute modifier.


## `transition` modifier


This modifier will proxy the assignment operation of the attribute, transforming the process of assigning the attribute directly into a gradual assignment according to the animation transition method specified by the `transition` modifier. For example


``` html
<!-- The transition modifier defines the transition effect of the value attribute -->
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



Since the `value.transition` modifier of the [`progress`](/components/progress.md) component is defined, each time `this.progress` is modified, the displayed value of the `progress` component will not directly jump to the new value, but will gradually change through an animation. This effect can be achieved without writing any animation logic.


::: tip

The `value` attribute of the `progress` component in the example is an integer. Since the default $[0, 100]$ range tends to create a sense of segmentation in transition animations, the example uses `:max="1000"` to increase the value range of `value` to make the animation smoother.
:::



### Interpolation calculation


Currently, only some properties of native components support the `transition` modifier. Supported properties must have "interpolable" value types, specifically: for all property value types $a$ and $b$ and progress $p \in [0,1]$, the operation $(1-p)*a+p*b$ is valid.


JavaScript's `number` type is interpolable, in addition to transform and color values.


#### transform


Transformations are usually defined using strings, such as `scale(2) rotate(30deg)`. Strings themselves are not interpolable, but they are when used with transform properties (because these strings are parsed as sequences of transform operations, which are interpolable). Normally interpolation is done one transform at a time. For example, the transformation of each frame of `scale(2) rotate(30deg)` and `scale(1) rotate(90deg)` during the interpolation process includes two steps of scaling and rotation, where the scaling factor transitions from $2$ to $1$, and the rotation angle transitions from $30\deg$ to $90\deg$.


#### color


Colors are usually represented using string codes, such as `#ff0000`. Color interpolation is calculated individually for the red, green, blue, and transparency channels.


### `Transition` object


The value type of the `transition` modifier is a `Transition` object:
``` ts
interface Transition {
  curve?: string,
  duration?: number
}
```


#### `curve` <decl type="?: string"/>


Specify the [Easing function](../render/animation.md#缓动曲线) of the transition animation, the default is `'ease'`.


#### `duration` <decl type="?: number"/>


The duration of the animation, in seconds, defaults to `1`.