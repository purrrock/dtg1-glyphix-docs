# Animation

## Basics

"Animation" creates transition effects for an interface over a period of time by playing a sequence of frames continuously and rapidly. There are two ways to implement animations in Glyphix:
- **Slideshow animation**, which rapidly plays a set of images;
- **Keyframe animation**, where intermediate frames are automatically calculated by the program.

### Keyframe Animation

Slideshow animations are implemented using dedicated components, and their principle is similar to that of videos. This section focuses primarily on keyframe animation. The following example demonstrates a keyframe animation:

<div class="animation-example-box">
  <div style="visibility: hidden">Hello World!</div>
  <div class="animation-span">Hello World!</div>
  <div class="keyframes-from">Hello World</div>
  <div class="keyframes-to">Hello World</div>
</div>

To achieve this animation, developers need to define the starting frame (red text) and ending frame (green text) of the animation, while the program automatically calculates each frame in between. The start and end frames specified by the developer are called **keyframes**. Keyframe animations also allow defining intermediate keyframes. The frames calculated by the program are called **interpolation frames** (or tweened frames). In this example, the initial keyframe is the original text component, the ending keyframe is the text translated by $200\rm px$ and scaled by a factor of $0.75$, and the interpolation frames are the intermediate transformation values calculated based on the animation progress. For instance, the interpolation frame at $50\%$ animation progress translates the original text by $100\rm px$ and scales it by $0.875$.

Compared to slideshows, keyframe animations are easier to create and are well-suited for interface element transition effects (such as button press visual effects).

Keyframe animations are mainly defined by several elements:
- Keyframes: Manually specified frames; typically, keyframes are used at $0\%$ and $100\%$ progress.
- Animation duration: The time required for the animation progress to go from $0\%$ to $100\%$.
- Easing function: Defines the progress adjustment curve for interpolation frames; linear animation effects tend to look less natural.
- Repeat count, delay, playback direction (forward, reverse, alternate), etc.

### Property Animation

Keyframe animations used in Glyphix are primarily **property animations**. This means that keyframes are defined by the properties of elements, and interpolation frames calculate the intermediate property values. For example, as implemented by the [`transition` property modifier](../component/prop-modifier.md#transition-modifier): the animation system automatically handles transition effects for property changes.

Property animations are mainly divided into two categories:
- Component property animations: Add animation transitions to component properties, implemented via the `transition` property modifier.
- CSS animations: Add animations to style properties.

## Easing Functions

Easing functions define the adjustment curve for animation progress, avoiding monotonous linear interpolation effects. Readers can experience the effects of easing functions at https://cubic-bezier.com/.

In the [`transition` property modifier](../component/prop-modifier.md#transition-modifier) and CSS [`animation` property](../generic/styles.md#animation), the easing function is a string, as shown in the table below.

|              Value              | Description                                                                                                                                    |
| :-----------------------------: | ---------------------------------------------------------------------------------------------------------------------------------------------- |
|             `ease`              | Default value. The animation starts slowly, then accelerates, and slows down before ending.                                                    |
|            `ease-in`            | The animation starts at a slow speed.                                                                                                          |
|           `ease-out`            | The animation ends at a slow speed.                                                                                                            |
|          `ease-in-out`          | The animation starts and ends at a slow speed.                                                                                                 |
|            `linear`             | The animation has the same speed from start to finish.                                                                                         |
|            `spring`             | Simulates a spring rebound animation effect, equivalent to `spring(1,1,1)`.                                                                    |
| `cubic-bezier(x1, y1, x2, y2)`  | Defines the easing function using a [cubic Bézier curve](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function#cubic_b%C3%A9zier_easing_function). |
| `spring(spring, damping, mass)` | Simulates a spring rebound animation effect, allowing you to specify elasticity coefficients, damping, and mass parameters (documentation needed). |

For most animations, the `ease` easing function yields good results, while complex requirements can be handled using the `cubic-bezier()` function. The `spring()` function is suitable for scenarios requiring physical rebound effects, such as rotating pointers.

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

You can add interactive animations to this button using the CSS [`animation`](../generic/styles.md#animation) property:

<Glyphix id="render-animation-button2" width="200" height="80">

``` html
<div>
  <button>Button</button>
</div>
```

``` css
/* Define keyframes for the active pseudo-class. Omitting the from / 0% keyframe
   causes the animation to start playing from the component's current state. */
@keyframes button-active {
  to {
    transform: scale(1.1, 1.1);
  }
}

/* Define keyframes for the non-pseudo-class state. Omitting the from / 0% keyframe
   causes the animation to start playing from the component's current state. */
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
  /* Animate the button to scale to 100% in the normal style */
  animation: 0.2s ease button-normal;
}

button:active {
  /* Animate the button to scale to 120% in the active pseudo-class style */
  animation: 0.2s ease button-active;
}
```
</Glyphix>

Currently, the CSS `transition` property is not supported, so animations must be defined separately for the button's normal and `active` pseudo-class styles.


### `spring` Animation Effect

The `spring` easing function provides an interpolation effect similar to spring-damped oscillation, which can be used for moving pointers. The following example demonstrates two ways to implement pointer animation: the left side uses uniform pointer rotation, while the right side uses the `spring` easing function.

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
