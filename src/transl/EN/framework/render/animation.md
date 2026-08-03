# animation


## basic knowledge


"Animation" plays several frames continuously and quickly to make the interface present a transition effect over a period of time. There are two ways to implement animation in Glyphix:
- By quickly playing a **carousel animation** of a group of pictures;
- **Keyframe animation** for intermediate frames is automatically calculated through the program.


### Keyframe animation


Carousel animation is implemented through specialized components, and its principle is similar to that of video. This section mainly introduces keyframe animation. The following example demonstrates a keyframe animation:


<div class="animation-example-box">

  <div style="visibility: hidden">Hello World!</div>

  <div class="animation-span">Hello World!</div>

  <div class="keyframes-from">Hello World</div>

  <div class="keyframes-to">Hello World</div>

</div>



To implement this animation, developers need to define the start frame (red text) and end frame (green text) of the animation. The program will automatically calculate each frame in the animation. The start and end frames specified by the developer are called keyframes. Keyframe animation also allows the definition of intermediate keyframes. The frames calculated by the program are called **interpolated frames**. In this example, the starting keyframe is the original text component, while the ending keyframe translates the text $200\rm px$ and scales it $ 0.75 $ times, and the interpolated frame is the intermediate transformation value calculated based on the animation progress. For example, the interpolation frame when the animation plays to $50\%$ is to translate the original text $100\rm px$ and scale it $ 0.875 $ times.


Compared with carousels, keyframe animations are easier to create and are suitable for transition effects of interface elements (such as button press animations).


Keyframe animation is mainly defined by several elements:
- Keyframe: Manually specified frame, usually keyframes are used at $0\%$ and $100\%$ progress;
- Animation duration: that is, the time required for the animation progress from $0\%$ to $100\%$;
- Easing function: defines the progress adjustment curve of the interpolation frame. The linear animation effect has a poor look and feel;
- Number of repetitions, delay, playback direction (forward, reverse, reciprocating), etc.


### Property animation


The keyframe animation used in Glyphix is ​​mainly **attribute animation**. That is, keyframes are defined by the element's attributes, while interpolated frames calculate intermediate attribute values. For example, the animation implemented by [`transition` attribute modifier](../component/prop-modifier.md#transition-修饰符) is like this: the animation system will automatically handle the transition effect of attribute changes.


Property animations are mainly divided into two categories:
- Component property animation: Add animated transitions to component properties, implemented by the `transition` property modifier;
- CSS Animation: Add animation to style properties.


## Easing function


The easing function defines the adjustment curve of the animation progress, thus avoiding the monotonous linear interpolation effect. Readers can go to https://cubic-bezier.com/ to experience the effect of the easing function.


In [`transition` attribute modifier](../component/prop-modifier.md#transition-修饰符) and CSS's [`animation` property](../generic/styles.md#animation). The easing function is a string whose contents are shown in the following table.


| value | description |
| :-----------------------------: | -------------------------------------------------------------------------------------------------------------------------------------- |

| `ease` | Default value. The animation starts at a slow speed, then speeds up, and slows down before ending. |
| `ease-in` | The animation starts at a slow speed. |
| `ease-out` | The animation ends at low speed. |
| `ease-in-out` | The animation starts and ends at a slow speed. |
| `linear` | The speed of the animation is the same from beginning to end. |
| `spring` | Simulates the animation effect of spring rebound, equivalent to `spring(1,1,1)`. |
| `cubic-bezier(x1, y1, x2, y2)` | Use [cubic bezier curve](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function#cubic_b%C3%A9zier_easing_function) to define the easing function. |
| `spring(spring, damping, mass)` | Simulates the animation effect of spring rebound, and can specify elastic coefficient, damping and mass parameters (document required). |


For most animations, the `ease` easing function can get good results, and for complex requirements, the `cubic-bezier()` function can be used. The `spring()` function is suitable for scenarios such as pointer rotation that require rebound physical effects.


## Example


### Button animation


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
/* Define active pseudo-class keyframe, do not write from / 0% keyframe
   The animation will start playing from the current state of the component */
@keyframes button-active {
  to {
    transform: scale(1.1, 1.1);
  }
}

/* Define no pseudo-class keyframes, do not write from / 0% keyframes
   The animation will start playing from the current state of the component */
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
  /* Animate scaling of button to 100% in pseudo-class style */
  animation: 0.2s ease button-normal;
}

button:active {
  /* Animate scaling button to 120% in active pseudo-class style */
  animation: 0.2s ease button-active;
}
```
</Glyphix>



The CSS `transition` attribute is not currently supported, so animations must be defined separately in the button's unpseudo-classed style and in the `active` pseudo-classed style.




### `spring` animation effect


The `spring` easing function provides an interpolation effect similar to spring-damped vibration, which can be used for moving pointers. The following example demonstrates two methods of implementing pointer animation: uniform pointer rotation on the left, and using the `spring` easing function on the right.


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



Both animations update the pointer angle at $1$ second intervals, but the `transition` modifier of the component property automatically adds a rotation animation.


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
