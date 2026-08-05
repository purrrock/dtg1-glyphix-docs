# Animation

## Basics

"Animation" creates transition effects for the interface over a period of time by playing a sequence of frames continuously and rapidly. There are two ways to implement animations in Glyphix:
- **Slideshow animation**, which rapidly plays a set of images;
- **Keyframe animation**, where the program automatically calculates the intermediate frames.

### Keyframe Animation

Slideshow animations are implemented using dedicated components, and their principle is similar to videos. This section primarily introduces keyframe animations. The following example demonstrates a keyframe animation:

<div class="animation-example-box">
  <div style="visibility: hidden">Hello World!</div>
  <div class="animation-span">Hello World!</div>
  <div class="keyframes-from">Hello World</div>
  <div class="keyframes-to">Hello World</div>
</div>

To implement this animation, developers need to define the starting frame (red text) and ending frame (green text) of the animation. The program then automatically calculates each frame in between. The start and end frames specified by the developer are called **keyframes**, and keyframe animations also allow defining intermediate keyframes. The frames calculated by the program are called **interpolated frames**. In this example, the initial keyframe is the original text component, while the final keyframe translates the text by $200\rm px$ and scales it by $0.75$. The interpolated frame is the intermediate transformation value calculated based on the animation progress. For example, the interpolated frame at $50\%$ animation progress translates the original text by $100\rm px$ and scales it by $0.875$.

Compared to slideshows, keyframe animations are easier to create and are suitable for interface element transitions (such as button press effects).

Keyframe animations are mainly defined by several elements:
- Keyframes: Manually specified frames, typically used at $0\%$ and $100\%$ progress;
- Duration: The time required for the animation progress to go from $0\%$ to $100\%$;
- Easing function: Defines the progress adjustment curve of the interpolated frames; linear animation effects tend to look poor visually;
- Repeat count, delay, playback direction (forward, reverse, alternate), etc.

### Property Animation

The keyframe animations used in Glyphix are primarily **property animations**. That is, keyframes are defined by the element's properties, and interpolated frames calculate the intermediate property values. For example, as achieved by the [`transition` property modifier](../component/prop-modifier.md#transition-modifier): the animation system automatically handles transition effects for property changes.

Property animations are mainly divided into two categories:
- Component property animations: Add animation transitions to component properties, implemented via the `transition` property modifier;
- CSS animations: Add animations to style properties.

## Easing Functions

Easing functions define the adjustment curve of the animation progress, avoiding monotonous linear interpolation effects. Readers can experience the effects of easing functions at https://cubic-bezier.com/.

In the [`transition` property modifier](../component/prop-modifier.md#transition-modifier) and CSS [`animation` property](../generic/styles.md#animation), the easing function is a string, the contents of which are shown in the table below.

|              Value              | Description                                                                                                                                              |
| :-----------------------------: | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
|             `ease`              | Default value. The animation starts slowly, then accelerates, and slows down before ending.                                                              |
|            `ease-in`            | The animation starts slowly.                                                                                                                           |
|           `ease-out`            | The animation ends slowly.                                                                                                                               |
|          `ease-in-out`          | The animation starts and ends slowly.                                                                                                                  |
|            `linear`             | The animation has the same speed from start to finish.                                                                                                   |
|            `spring`             | Simulates a spring rebound animation effect, equivalent to `spring(1,1,1)`.                                                                             |
| `cubic-bezier(x1, y1, x2, y2)`  | Defines the easing function using a [cubic Bézier curve](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function#cubic_b%C3%A9zier_easing_function). |
| `spring(spring, damping, mass)` | Simulates a spring rebound animation effect, allowing you to specify elasticity, damping, and mass parameters (documentation needed).                   |

For most animations, the `ease` easing function yields good results, while complex requirements can use the `cubic-bezier()` function. The `spring()` function is suitable for scenarios requiring physical rebound effects, such as rotating pointers.

## Examples

### Button Animation

As shown below, the default button effect has no press animation:

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

You can use the CSS [`animation`](../generic/styles.md#animation) property to add interactive animations to this button:

<Glyphix id="render-animation-button2" width="200" height="80">

``` html
<div>
  <button>Button</button>
</div>
```

``` css
/* Define active pseudo-class keyframes. If from / 0% keyframe is omitted,
   the animation will start playing from the component's current state */
@keyframes button-active {
  to {
    transform: scale(1.1, 1.1);
  }
}

/* Define non-pseudo-class keyframes. If from / 0% keyframe is omitted,
   the animation will start playing from the component's current state */
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
  /* Animate the button to scale to 100% in the non-pseudo-class style */
  animation: 0.2s ease button-normal;
}

button:active {
  /* Animate the button to scale to 120% in the active pseudo-class style */
  animation: 0.2s ease button-active;
}
```
</Glyphix>

Currently, the CSS `transition` property is not supported, so animations must be defined separately in the button's non-pseudo-class style and `active` pseudo-class style.


### `spring` Animation Effect

The `spring` easing function provides an interpolation effect similar to spring-damped vibration, which can be used for moving pointers. The following example demonstrates two ways to implement pointer animations: the left side uses uniform pointer rotation, while the right side uses the `spring` easing function.

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

Both animations update the pointer angle at $1$-second intervals, but the component property's `transition` modifier automatically adds the rotation animation.

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
