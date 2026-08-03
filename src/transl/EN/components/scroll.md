# scroll


A scrolling list container that supports any subcomponent. The scrolling direction of the list is specified by the specific layout method: when using fluid layout or `column` direction flex layout, the elements are laid out in the vertical direction, and the list can be scrolled vertically; when using `row` direction flex layout, the elements are laid out in the horizontal direction, and the list can be scrolled horizontally. The `scroll` component does not support bidirectional scrolling (that is, horizontal and vertical scrolling at the same time).


`scroll` components are block-level elements using fluid layout by default.


The `scroll` component can be scrolled using gesture interaction, and the vertical `scroll` component also supports encoder (rotating crown on the watch, mouse wheel on the simulator) scrolling.


::: tip

Some of the interactive examples in this document support mouse wheel interaction (mouse icon icon to the right of the title): you can hover the pointer inside the example and use the mouse wheel to scroll the list.
:::



## property


### `scroll` <decl type="{ scrollX: number, scrollY: number, scrollState: number }" get listen />


The `scroll` attribute value is an object containing the following fields: `scrollX`, `scrollY`, and `scrollState`. The `scrollX` and `scrollY` attributes represent the horizontal and vertical scrolling positions respectively, in pixels; the `scrollState` attribute represents the scrolling state, and its value is $0$, $1$ or $2$. The specific meaning is as shown in the following table. Changes to the `scroll` attribute can be monitored through the `on` directive. Any change in content location caused by user operations and API operations will trigger monitoring.


| `scrollState` value | Effect description |
| :--------------: | ------------------------------------------------------------------- |

| $0$ | Stopped sliding |
| $1$ | Swiping via user's gesture |
| $2$ | The user has let go, sliding caused by method calls such as [`scrollTo`](#scrollto) or inertia |


::: info

`scroll` The area where the child elements are located is called the "content" area, and the part actually displayed by the list component is called the "view" area. Elements are laid out in the content area, and their size may exceed the view area, and the display position of the content can be changed by scrolling.
:::



The range of the scroll position is usually within the content area, that is, `scrollX` for horizontal lists is within the range of $[0, \texttt{contentWidth}]$, and `scrollY` for vertical lists is within the range of $[0, \texttt{contentHeight}]$. But when the list is scrolled before the head of the content, `scrollX` or `scrollY` will be less than $0$; similarly, when the list is scrolled to the end of the content, the value of `scrollX` or `scrollY` will be greater than `contentWidth` or `contentHeight`.


::: warning

The `scroll` event will be triggered every frame during the scrolling process. Listening to this event in JavaScript code may cause obvious frame drops, so try to avoid using it.
:::



### `scrollTop` <decl type="number" set get listen />


The vertical scroll position, that is, the distance from the top of the content of the `scroll` component to the top of the viewport, in pixels. You can set the scroll position through this property, and you can also listen for changes in the scroll position through this property.


Unlike the [`scroll`](#scroll) attribute, the listener `scrollTop` attribute itself cannot distinguish between scrolling by the user's gestures and scrolling caused by API calls or inertia.


### `scrollLeft` <decl type="number" set get listen />


The vertical scroll position, that is, the distance from the left side of the content of the `scroll` component to the left side of the viewport, in pixels. You can set the scroll position through this property, and you can also listen for changes in the scroll position through this property.


Unlike the [`scroll`](#scroll) attribute, the listener `scrollLeft` attribute itself cannot distinguish between scrolling by the user's gestures and scrolling caused by API calls or inertia.


### `scrollWidth` <decl type="number" get listen />


`scroll` The width of the component's content area. The width of `scroll` in vertical layout is equal to the view width, while the width of `scroll` in horizontal layout is the sum of the widths of all elements. You can use this to monitor content width changes.


### `scrollHeight` <decl type="number" get listen />


`scroll` The height of the component's content area. The height of `scroll` in vertical layout is equal to the view height, while the height of `scroll` in horizontal layout is the sum of the heights of all elements. You can use this to monitor content height changes.


### `damping` <decl type="number" set />


Set the damping coefficient of the list scroll animation. The valid value range is $[0.1, 50]$ (unsupported values ​​will be automatically modified to the upper and lower limits). The default value is $1.5$. A larger damping coefficient will cause the animation to stop faster, and the default damping coefficient value can produce an inertial effect with a longer distance and longer duration.


<glyphix id="components-scroll-damping" height="360" width="360" title="阻尼效果" wheel>


``` html
<div>
  <span>damping: {{damping}}</span>
  <button on:click="increase">+</button>
  <button on:click="decrease">-</button>
  <scroll :damping="damping">
    <p for="x in 50" class="item">
      Item {{ x + 1 }}
    </p>
  </scroll>
</div>
```


``` js
export default {
  data: {
    damping: 1
  },
  increase() {
    this.damping += 1
    if (this.damping > 20)
      this.damping = 1
  },
  decrease() {
    this.damping -= 1
    if (this.damping < 1)
      this.damping = 19.5
  }
}
```


``` css
span {
  color: #404040;
}

scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  height: 300px;
  width: 360px;
}

.item {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px 5px;
  margin: 10px;
  border-radius: 16px;
}

button {
  color: #fafafa;
  background-color: #adadad;
  border-radius: 12px;
  margin-left: 16px;
  margin-bottom: 16px;
  width: 1.2rem;
}
```


</glyphix>



::: tip

The damping coefficient should be set to a constant and not modified. Modifying the damping coefficient will not affect the rebound animation.
:::



### `snapshot` <decl type="boolean" get set />


When the `snapshot` attribute is turned on, the subcomponents in the list will turn on snapshot mode. For related demonstrations, please refer to the [`quiescent`](/framework/generic/properties.md#quiescent) attribute of native components.


Enabling snapshots may increase the frame rate of complex interfaces. For example, when a list item contains a large amount of text and contains a non-transparent background, snapshot mode can cache and merge a large number of drawing operations into a small number of snapshots. The Glyphix framework caches these snapshots across repeated draws to further improve performance.


However, the `snapshot` attribute does not provide a guarantee that snapshots will be used for subcomponents. This attribute may be ignored when the system has insufficient memory or when there is no need to use snapshots.


### `deformation` <decl type="string | function" set />


Set the deformation effect of the list. Through the deformation effect, you can achieve fish-eye and other appearances. A built-in morph effect can be specified by name (a string), or a morph effect can be defined through a JavaScript function.


| Value | Effect Description |
| :---------: | :------------------------------: |

| `'none'` | No deformation effect (default value) |
| `'fisheye'` | Built-in fisheye effect |
| function | Specify deformation effects through JavaScript functions |


The deformation effect should be constant and not modified.


When the list is set to fisheye deformation effect, it is recommended to set the [`scrollSnap`](#scrollsnap) attribute to `'center'` to get the most reasonable effect.


The picture below demonstrates the fisheye deformation effect. You can adjust whether to center the image through the "center" switch.


<glyphix id="components-scroll-deformation" height="360" width="360" title="鱼眼效果" wheel>


``` html
<div>
  <p>center <switch ::value="center" /></p>
  <scroll deformation="fisheye" :scroll-snap="center ? 'center' : null">
    <p for="x in 15">
      Item {{ x + 1 }}
    </p>
  </scroll>
</div>
```


``` css
div {
  color: #404040;
  display: flex;
  flex-direction: column;
}

scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  flex: 1;
}

scroll > p {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 40px 10px;
  margin: 5px;
  border-radius: 50%;
}
```


``` js
export default {
  data: {
    center: true
  }
}
```


</glyphix>



::: tip

Deformation effects generally use snapshots, so there is no need to repeatedly set `snapshot` when setting the `deformation` attribute.
:::



### `scrollSnap` <decl type="'none' | 'start' | 'center' | 'edge'" get set />


Set the alignment and snapping mode of list items. For example, you can center-align the element or snap it to the edge of the element.


| value | description |
| :--------: | -------------------------------------------------------------------------------------------------------------- |

| `'none'` | The element has no suction alignment and attachment effects, that is, the child elements can stop at any position according to scroll inertia. |
| `'start'` | The starting position of the element is aligned to the starting position of the viewport when scrolling stops. This mode is currently not supported. |
| `'center'` | The scroll stop is when the center of the element is aligned to the center of the viewport. |
| `'edge'` | When scrolling stops, the start or end position of the element is aligned to the start or end position of the viewport. But if the scroll does not cross the element boundary, it will not cause adsorption. |


The `scrollSnap` attribute does not adjust the element size, but can use mechanisms such as layout to implement a list of equal-sized items.


::: warning

This property should be set when the component is initialized and cannot be changed, otherwise interaction errors may occur.
:::



### `index` <decl type="number" get set listen />


The index of the currently displayed subcomponent. When the `index` attribute is set, the component will scroll to the specified subcomponent through animation. Position changes can be monitored through the `on` directive, and changes in subcomponent index can be monitored through the `index` attribute.


The value of `index` is automatically restricted to ensure that it points to a valid element. When using `index`, you must ensure that all elements of the `scroll` component are static (that is, the [`position`](/framework/generic/styles.md#position) attribute of CSS is the default `static`), otherwise an error will occur.


### `finalChanged` <decl type="bool" get set />


Set whether the [`index`](#index) change event is only triggered when scrolling stops. By default (that is, `finalChanged` is `false`), whenever the scroll gesture or other reasons cause the `index` attribute of the `scroll` component to change, its listening event will be triggered. However, doing so can easily cause animation frames to drop, or trigger too frequent and unnecessary events. When `finalChanged` is set, the `index` changed event will only be triggered when scrolling stops.


::: tip

When implementing effects such as point indicators by monitoring the `index` attribute, it is recommended to set `finalChanged` to `true`. This can avoid frame drops caused by event-triggered rendering updates during the sliding process.
:::



The following example demonstrates the effect of `finalChanged`. You can try switching the "final-changed" checkbox, then slide the list and observe the frequency and timing of changes to `index`.


<glyphix id="components-scroll-final-changed" height="360" width="360" title="延迟 index 事件" wheel>


``` html
<div>
  <p>
    <checkbox id="checkbox" ::checked="finalChanged" />
    <label target="checkbox">final-changed</label>
    index: {{index}}
  </p>
  <scroll :final-changed="finalChanged" ::index="index">
    <p for="x in 50">
      Item {{ x + 1 }}
    </p>
  </scroll>
</div>
```


``` css
div {
  color: #404040;
  display: flex;
  flex-direction: column;
}

scroll {
  display: flex;
  flex-direction: column;
  flex: 1;
}

scroll > p {
  background-color: #f0f0f0;
  border-radius: 12px;
  text-align: center;
  margin: 8px;
  padding: 20px;
}
```


``` js
export default {
  data: {
    index: 0,
    finalChanged: true
  }
}
```


</glyphix>



### `bounces` <decl type="'none' | 'start' | 'end' | 'edge'" get set />


Set whether to trigger rebound after scrolling `scroll` to the boundary through gestures. The initial value of this property is `edge`, which allows rebounding of the start and end positions.


| value | description |
| :-------: | -------------------------------------- |

| `'none'` | Disables all boundary bounce. |
| `'start'` | Only allows rebound after dragging to the starting position of the content. |
| `'end'` | Only allows rebound after dragging to the end of the content. |
| `'edge'` | Allows rebound after dragging to the start or end of the content. |


The following example shows the role of each `bounces` value. You can try sliding each item left or right beyond the boundary and observe the corresponding interaction behavior.


<glyphix id="components-scroll-bounces" height="360" width="400" title="拖拽回弹动画">


``` html
<scroll class="column-box">
  <scroll for="item in items" class="row-box"
          :bounces="item" scroll-snap="edge">
    <p class="item-body">bounces: {{item}}</p>
    <p class="slide-button">×</p>
  </scroll>
</scroll>
```


```js
export default {
  data: {
    items: ['none', 'start', 'end', 'edge']
  }
}
```


```css
.column-box {
  display: flex;
  flex-direction: column;
}

.row-box {
  display: flex;
  flex-direction: row;
}

.row-box > p {
  border-radius: 12px;
  text-align: center;
  margin: 8px;
  padding: 16px;
}

.item-body {
  background-color: #f0f0f0;
  width: 100%;
}

.slide-button {
  width: 30%;
  color: #ffffff;
  background-color: #f04040;
}
```


</glyphix>





::: note

Currently the `bounces` attribute only affects the rebound of gesture operations, but ignores the rebound of fast inertial animations. The example above uses a trick to avoid unexpected behavior:
- `.row-box` Use edge snapping strategy ( `snap-type="edge"` ) to avoid gesture animations with bounce.
- Each element of `.row-box` does not exceed the width of `100%`, ensuring that the edge snapping strategy does not cause internal boundary rebound.


This technique can be used for interfaces such as sliding delete menus.
:::



The `bounces` attribute will also play a similar role to [`weakGesture`](#weakgesture). Specifically, when the edge that prohibits rebounding is crossed, scroll gesture events are automatically allowed to bubble up and be delivered. Therefore, there is no need to set both the `bounces` and `weakGesture` attributes.


::: tip

The scroll gesture bubbling behavior of `bounces` and `weakGesture` is "opposite". For example, the `end` mode bounce policy allows the user to bounce back after scrolling past the end position of the list, and this policy allows the scroll gesture to bubble at the starting position. This corresponds to the effect of the `weakGesture` attribute with value `'start'`.
:::



### `weakGesture` <decl type="'none' | 'start' | 'end' | 'edge'" get set />


Set the circumstances under which the `scroll` component will bubble scroll gestures. By default `scroll` blocks bubbling of gestures it responds to, so its parent element cannot receive gestures that cause `scroll` to scroll. `weakGesture` allows bubbling of gesture events when dragging into content boundaries, allowing the parent element to receive these gestures.


| value | description |
| :-------: | ------------------------------------------------ |

| `'none'` | Do not bubble the corresponding gesture event. |
| `'start'` | Bubbles the corresponding gesture event after dragging to the starting position of the content. |
| `'end'` | Bubbles the corresponding gesture event after dragging to the end of the content. |
| `'edge'` | Bubbles the corresponding gesture event after dragging to the beginning or end of the content. |


If the underlying element of the page is a horizontal `scroll` component, but you want the right swipe gesture to return the page, you can configure it like this:
``` html
<scroll weak-gesture="start"> ... </scroll>
```
When the user slides to the head of the `scroll` component and continues to slide right to exit the page.


::: warning

This property should be set when the component is initialized and cannot be changed, otherwise interaction errors may occur.
:::



### `scrollbar` <decl type="boolean" get set />


Mark whether the `scroll` component should display scroll bars (not displayed by default). Only the `scroll` component with vertical layout is supported. The `scrollbar` attribute must be a constant and cannot be modified with reactive attributes, for example:
``` html
<scroll scrollbar>
  ...
</scroll>
```
A `scroll` component with a scrollbar will be created. For the effect of the scroll bar, please refer to the example of the [`setIndex`](#setindex) method.


The style of the scroll bar is determined by the system. For example, it may appear as an arc on a circular screen, or as a straight bar on a rectangular screen.


### `scrolled` <decl type="boolean" listen />


Monitor whether the list is in scrolling state through the `scrolled` attribute. An event-triggered attribute with a value of `true` means that the list is scrolling, otherwise it means that the list has stopped scrolling.


The scrolling operation caused by user touch and scrolling through the `scroll` attribute will trigger the `scrolled` event. When the list stops scrolling, the parameter value of the `scrolled` event is `false`.


### `setIndex`
<decl method><pre>

(options: {

  index: number,

  behavior?: 'instant' | 'smooth'

}): void

</pre></decl>



Moves the viewport to the child component specified by index. If this movement crosses the viewport boundary, the viewport position will stay at the first or last component. The function of `options` parameter attribute is:
- `index`: The index of the target subcomponent to be moved, $0$ represents the first subcomponent.
- `behavior`: Use animation transition when `'smooth'`, move to the specified sub-component position immediately when `'instant'` (default value).


When calling `setIndex()`, you must ensure that all elements of the `scroll` component are static, otherwise an error will occur.


<glyphix id="components-scroll-setindex" height="360" width="400" title="setIndex 方法">


``` html
<div class="window">
  <scroll id="scroll"
          :scroll-snap="center ? 'center' : null"
          scrollbar>
    <p for="x in 50" class="item">Item {{ x }}</p>
  </scroll>
  <div class="controls">
    <button on:click="setIndex('smooth')">smooth</button>
    <button on:click="setIndex('instant')">instant</button>
    center <switch ::value="center" />
  </div>
</div>
```


``` js
import prompt from '@system.prompt'

export default {
  data: { center: false },
  setIndex(behavior) {
    let el = this.$element('scroll')
    let index = parseInt(Math.random() * 50)
    prompt.showToast({message: `${behavior}ly set index to ${index}`})
    el.setIndex({ index: index, behavior: behavior })
  }
}
```


``` css
.window {
  display: flex;
  flex-direction: column;
}

scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  flex: 1;
}

.item {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px 5px;
  border-radius: 16px;
  margin: 8px;
}

.controls {
  display: flex;
  align-items: center;
  color: #404040;
}

button {
  color: #fafafa;
  background-color: #adadad;
  border-radius: 12px;
  padding: 4px 10px;
  margin-left: 16px;
  margin-bottom: 16px;
  flex: 1;
  margin: 8px;
  padding: 8px;
  text-align: center;
}
```


</glyphix>



### `scrollTo`
<decl method><pre>

(options: {

  left?: number,

  top?: number,

  behavior?: 'instant' | 'smooth'

}): void

</pre></decl>



Scrolls the content to the specified position. The function of `options` parameter attribute is:
- `left`: Specifies the position where the content scrolls along the y-axis. If `left` is ignored or the scroll component has a vertical layout, scrolling on the y-axis will not occur.
- `top`: Specifies the position where the content scrolls along the x-axis. If `top` is ignored or the scroll component has a horizontal layout, scrolling on the x-axis will not occur.
- `behavior`: Specifies the transition effect of scrolling. `'instant'` (default value) means jumping directly to the target position without a transition effect, while `'smooth'` will scroll smoothly and produce a transition effect.


The `scrollTo` method ignores the adsorption effect of elements.


### `scrollBy`
<decl method><pre>

(options: {

  left?: number,

  top?: number,

  behavior?: 'instant' | 'smooth'

}): void

</pre></decl>



Scroll content a certain distance. Unlike [`scrollTo()`](#scrollTo), `scrollBy()` scrolls relative to the current content position. The function of `options` parameter attribute is:
- `left`: Specifies the distance for scrolling the content along the y-axis. If `left` is ignored or the scroll component has a vertical layout, scrolling on the y-axis will not occur.
- `top`: Specifies the distance for scrolling the content along the x-axis. If `top` is ignored or the scroll component has a horizontal layout, scrolling on the x-axis will not occur.
- `behavior`: Specifies the transition effect of scrolling. `'instant'` (default value) means jumping directly to the target position without a transition effect, while `'smooth'` will scroll smoothly and produce a transition effect.


The `scrollBy` method ignores the adsorption effect of elements.


## CSS specifications


### Layout direction control


The scrolling direction of the `scroll` component is determined by its layout method. When using fluid layout (default layout) or `column` direction flex layout, the elements are laid out in the vertical direction, and the list can be scrolled vertically; when using the `row` direction flex layout, the elements are laid out in the horizontal direction, and the list can be scrolled horizontally.


<glyphix id="components-scroll-layout" height="360" width="740" title="布局方式控制滚动方向">


``` html
<div>
  <scroll>
    <p for="20">vertical scroll</p>
  </scroll>
  <!-- 用于占位元素，因为 flex 布局现在还不支持 gap -->
  <div style="width: 20px"></div>
  <scroll style="display: flex; flex-direction: row;">
    <p for="20">horizontal<br>scroll</p>
  </scroll>
</div>
```


``` css
div {
  display: flex;
}

scroll {
  background-color: #f0f0f0;
  flex: 1;
}

p {
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px;
  margin: 4px;
  border-radius: 16px;
}
```


</glyphix>



### `padding` and `overflow` <version-badge since="0.9" />


By default ( `overflow: clip` ), the `scroll` component's padding directly clips the visible area. When content is scrolled, the padding area is always invisible. Setting `overflow: visible` allows the padding area to remain visible as the content scrolls.


<glyphix id="components-scroll-padding-overflow-visible" height="360" width="740" title="overflow: visible 的内边距">


``` html
<div>
  <scroll :index="2">
    <p for="20">overflow: clip</p>
  </scroll>
  <!-- 用于占位元素，因为 flex 布局现在还不支持 gap -->
  <div style="width: 20px"></div>
  <scroll style="overflow: visible;" :index="2">
    <p for="20">overflow: visible</p>
  </scroll>
</div>
```


``` css
div {
  display: flex;
}

scroll {
  padding: 20px;
  background-color: #f0f0f0;
  flex: 1;
}

p {
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px;
  margin: 4px;
  border-radius: 16px;
}
```


</glyphix>



Even if `overflow: visible` is set, `scroll` will clip the content to the padding-box instead of allowing it to exceed that range, unlike regular elements like `div`. This is because the scrolling behavior and layout mechanism of `scroll` need to ensure that the content scrolls within a certain area, rather than allowing the content to expand unlimitedly to the outside area.


In a similar situation to `overflow: visible`, the content of ordinary containers such as `div` can exceed the scope of the entire `div` (such as outside the red `border`):


<glyphix id="components-scroll-overflow-div" height="360" width="360" title="div 的 overflow: visible">


``` html
<div style="overflow: visible;">
  <p for="20">div {overflow: visible}</p>
</div>
```


``` css
div {
  display: flex;
  flex-direction: column;
  padding: 20px;
  margin-bottom: 100px;
  border: 2px solid red;
  background-color: #f0f0f0;
}

p {
  background-color: #bdbdbd;
  text-align: center;
  padding: 8px;
  margin: 4px;
  border-radius: 16px;
  flex-shrink: 0;
}
```


</glyphix>



#### Recommended settings for i18n scenarios


In i18n (internationalization) scenarios, the text within `scroll` may need to be overflowed to avoid possible truncation. For this case, the recommended setting is `overflow: visible`, to allow the [文本溢出](/framework/application/i18n.md#文本溢出) content to exceed the content boundaries of `scroll` when scrolled, to maximize the use of space for text display.


#### Relationship to HTML/CSS specifications


The behavior of `scroll` when setting `overflow: visible` is similar to `div { overflow-y: scroll; }` in the HTML/CSS specification. The padding at this time can keep the content visible during scrolling, such as this CSS:


```css
div {
  padding: 20px;
  overflow-y: scroll;
}
```


The following effect will be obtained, that is, the padding area will not crop the content when scrolling:


<div style="padding: 20px; background-color: var(--vp-c-grey-bg); overflow-y: scroll; height: 100px; width: 200px; border: 2px dotted red; font-family: sans-serif;">

  Michaelmas term lately over, and the Lord Chancellor sitting in Lincoln's Inn Hall.

  Implacable November weather. As much mud in the streets as if the waters had but

  newly retired from the face of the earth.

</div>



HTML's `div` does not directly correspond to the behavior of `scroll` in `overflow: clip`.