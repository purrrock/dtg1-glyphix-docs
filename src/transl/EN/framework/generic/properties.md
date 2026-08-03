---

icon: xml

---

# Properties and events


This section introduces the common property interfaces and events provided by all native components.


## Property list


### Common properties


#### `top` <decl type="number" get set listen />


The position of the top of the component relative to the parent native component, in pixels. This attribute is actually the abbreviation of the `top` attribute in inline styles. For more details on how to use it, see [Component location operations](#组件位置操作).


When reading or listening to the `top` attribute, the calculated position of the component will be obtained, as well as the actual measured value after layout.


#### `left` <decl type="number" get set listen />


The position of the left side of the component relative to the parent native component, in pixels. This attribute is actually the abbreviation of the `left` attribute in inline styles. For more details on how to use it, see [Component location operations](#组件位置操作).


When reading or listening to the `left` attribute, the calculated position of the component will be obtained, as well as the actual measured value after layout.


#### `width` <decl type="number" get set listen />


The width of the component. When the `width` attribute is set, the [`width`](styles.md#width) attribute in the inline style is updated. Since the width of CSS adopts border-box mode, the actual stored style value will be automatically appended to the current `padding` and `border` dimensions of the element, thereby ensuring that the content width after layout is consistent with the set value.


When reading or listening to the `width` attribute, you will get the content width after layout calculation, excluding `padding` and `border`.


#### `height` <decl type="number" get set listen />


The height of the component. When the `height` attribute is set, the [`height`](styles.md#height) attribute in the inline style is updated. Since the height of CSS adopts the border-box mode, the actual stored style value will be automatically appended to the current `padding` and `border` dimensions of the element, thereby ensuring that the content height after layout is consistent with the set value.


When reading or listening to the `height` attribute, you will get the content height after layout calculation, excluding `padding` and `border`.


#### `show` <decl type="boolean" get set/>


Set whether the component is visible. Hidden components are not displayed and do not occupy layout space.


#### `quiescent` <decl type="boolean" get set/>


Set whether component snapshots are automatically updated (quiescent snapshots). If the component is displayed through a snapshot, when the value of this property is `false` (the default value) the snapshot is refreshed immediately to update the view when the component content is updated, otherwise the snapshot is not updated immediately. Setting this property to `true` can improve UI performance, but will cause display content to lag.


The following example shows the role of the `quiescent` attribute. There are two `p` elements in the interface that are placed in the `scroll` container, and the `scroll` container has [snapshot mode](../../components/scroll.md#snapshot) turned on. When the user scrolls the `scroll` component, a snapshot of the elements in it will be taken. Since the first `p` element is in normal snapshot mode and the second `p` element is in static snapshot mode, only the contents of the first `p` element are updated when scrolling.


<glyphix id="generic-properties-quiescent" height="200" title="懒快照">


``` html
<scroll snapshot scroll-snap="center">
  <p>normal snapshot {{ count }}</p>
  <p quiescent>quiescent snapshot {{ count }}</p>
</scroll>
```


``` css
scroll {
  display: flex;
  flex-direction: column;
  background-color: lightgray;
}

p {
  background-color: lightgreen;
  text-align: center;
  padding: 10px;
  margin: 10px;
}
```


``` js
export default {
  data: {
    count: 0
  },
  onReady(event) {
    setInterval(() => this.count++, 500)
  }
}
```


</glyphix>



#### `style` <decl type="string" set />


Set the component's inline style. Currently only [CSS properties](./styles.md) with the <badge type="info" text="内联" /> tag is supported.


#### `z-index` <decl type="number" get set />


The `z-index` attribute sets the Z-order of the elements, `z-index` larger overlapping elements overwrite smaller elements. This attribute value will be overridden by the [`z-index`](styles.md/#z-index) attribute in CSS.




#### `opacity` <decl type="number" get set />


Specifies the transparency of the component. The value range is $[0, 1]$, where $0$ means complete transparency. and the CSS property [`opacity`](styles.md#opacity). The effect is the same.


::: warning

The `opacity` value will affect the drawing performance of the element. For details, please refer to the description of the [`opacity`](styles.md#opacity) CSS attribute.
:::



#### `transform` <decl type="string" set />


Set the component's transformation, equivalent to the CSS [`transform`](styles.md#transform) property.


#### `disabled` <decl type="boolean" get set />


Used to set or get the disabled state of a component. When the attribute value is `true`, the element is disabled, the user cannot interact with it, and the element will not respond to any gestures (such as clicks, drags, etc.). When the attribute value is the **default** `false`, the component is available and users can interact with it normally.


The following example demonstrates the use of the `disabled` attribute while also controlling styling with the [`:disabled`](styles.md#disabled) CSS pseudo-class. This example shows that the `div` element can respond to click gestures in the normal state, but does not respond to any gestures in the `disabled` state.


<glyphix id="generic-properties-disabled" height="200" title="disabled 属性">


``` html
<div :disabled="disabled" on:click="onClick">
  {{disabled ? 'disabled' : 'normal'}} <switch />
</div>
```


``` css
div {
  background-color: lightgray;
  text-align: center;
  display: flex;
  justify-content: center;
}

/* :disabled pseudo-class can control the style of elements in disabled state */
div:disabled {
  opacity: 0.5;
}
```


``` js
import prompt from '@system.prompt'

export default {
  data: {
    disabled: false
  },
  onInit() {
    setInterval(() => {
      this.disabled = !this.disabled
    }, 2000)
  },
  onClick() {
    prompt.showToast({ message: 'clicked!', duration: 250 })
  }
}
```


</glyphix>



### Generic events


Most native components support common events, which can be listened to using [`on` directive](../commands/on.md). The value types for these events are described in Section [event type](#事件类型).


#### `touchstart` <decl type="TouchEvent" listen />


The `touchstart` event is fired when the user starts touching the component. Event values ​​are of type [`TouchEvent`](#touchevent).


#### `touchmove` <decl type="TouchEvent" listen />


The `touchmove` event is triggered when the user touch point moves on the component. During the movement, this event will always be triggered even if the touch point leaves the scope of the current native component. Event values ​​are of type [`TouchEvent`](#touchevent).


There is a certain "moving dead zone" when the touch state transitions from `touchstart` to `touchmove`. If the sliding distance of the user's touch is less than the dead zone range, `touchmove` will not be triggered. The range of the motion dead zone varies from device to device, the following example shows the motion dead zone.


<glyphix id="generic-properties-touchmove" height="200" title="移动死区">


``` html
<p on:touchstart="state = 'start'"
   on:touchmove="onTouchMove($event)"
   on:touchend="onTouchEnd">
  {{ `state: ${state} \ndead area: (${dx}, ${dy})` }}
</p>
```


``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```


``` js
export default {
  data: {
    state: null,
    dx: null,
    dy: null
  },
  onTouchMove(event) {
    if (!this.dx && !this.dy) {
      this.state = 'move'
      this.dx = event.touches[0].offsetX
      this.dy = event.touches[0].offsetY
    }
  },
  onTouchEnd() {
    this.state = 'end'
    this.dx = this.dy = null
  }
}
```


</glyphix>



#### `touchend` <decl type="TouchEvent" listen />


When the user leaves the screen, the `touchend` event will be sent to the previously touched native component. Event values ​​are of type [`TouchEvent`](#touchevent).


#### `touchcancel` <decl type="TouchEvent" listen />


`touchcancel` is fired when a native component's touch is interrupted. Event values ​​are of type [`TouchEvent`](#touchevent). There are many reasons why a touch may be interrupted, such as the component being hidden or the touch event being forced to respond by other elements.


#### `click` <decl type="ClickEvent" listen />


The `click` event is triggered when the native component is clicked and released. Event values ​​are of type [`ClickEvent`](#clickevent).


<glyphix id="generic-properties-click" height="100">



``` html
<p on:click="click = JSON.stringify($event)">
  {{ click }}
</p>
```


``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```


``` js
export default {
  data: {
    click: null
  }
}
```


</glyphix>



#### `longpress` <decl type="LongPressEvent" listen />


The `longpress` event is triggered when the native component is pressed for a long time. Event values ​​are of type [`LongPressEvent`](#longpressevent). The following interactive example shows when `longpress` and other events are triggered:


<glyphix id="generic-properties-longpress" height="100">



``` html
<p on:touchstart="state = 'touching...'"
   on:longpress="state = `longpress: ${JSON.stringify($event)}`"
   on:click="state = 'clicked.'">
  {{ state }}
</p>
```


``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```


``` js
export default {
  data: {
    state: null
  }
}
```


</glyphix>



The triggering timing and duration of the `longpress` event varies by device, but is typically triggered after pressing $500 \rm ms$. Unlike the [`click`](#click) event, `longpress` fires during the press, not when the hand is released. For the example above, you'll find:
- When the pressing time is less than the long pressing trigger time, the `click` event will be triggered after letting go;
- When pressed long enough, the `longpress` event will be triggered, and when released, the `click` event will be triggered (displayed as "clicked." state);
- Movement during pressing will not trigger the `longpress` or `click` events.


#### `swipe` <decl type="SwipeEvent" listen />


The `swipe` event is triggered when the component is swiped quickly. Event values ​​are of type [`SwipeEvent`](#swipeevent).


<glyphix id="generic-properties-swipe" height="250" >



``` html
<p on:swipe="onSwipe($event)">
  {{ swipe }}
</p>
```


``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```


``` js
export default {
  data: {
    swipe: null
  },
  onSwipe(event) {
    this.swipe = event.direction
    event.strongResponse()
  }
}
```


</glyphix>



#### `keydown` <decl type="KeyEvent" listen />


This event is fired when a key is pressed. The `keydown` and `keyup` events are used to capture entity key press operations. To capture events, the native component must be in focus. The root element of the page always gets focus automatically, so the following code can capture `keydown` and `keyup` events:
``` html
<!-- Assuming this is the root element of the page -->
<div on:keydown="console.log($event)" on:keyup="console.log($event)">
  ...
</div>
```
Please refer to [`KeyEvent`](#keyevent) for the event value type.


Watch devices typically register [Default key handler](/api/system-internal.md#setdefaultkeyhandler) so that application code can interact without responding to such events (for example, some watches return to the previous page when the Power key is pressed). To prevent the default key response, use the `stopPropagation()` method of the `KeyEvent` object to prevent bubbling.


#### `keyup` <decl type="KeyEvent" listen />


This event is fired when the button is lifted. Please refer to the [`keydown`](#keydown) event for more information.


#### `wheel` <decl type="WheelEvent" listen />


The `wheel` event is triggered when the user rotates the wheel. Scroll wheel devices include the rotating crown of a watch or the mouse wheel. To capture this time, the native component must be in focus. The root element of the page always gets focus automatically, so the following code can capture the `wheel` event:
``` html
<!-- Assuming this is the root element of the page -->
<div on:wheel="console.log($event)">
  ...
</div>
```
Please refer to [`WheelEvent`](#wheelevent) for the event value type.


## event type


### `BaseEvent`


The `BaseEvent` event object provides some methods to control event delivery, and its prototype is:
``` ts
interface BaseEvent {
  strongResponse(): void, // Force response to events
  stopPropagation(): void // Stop event bubbling
}
```


### `TouchEvent`


The prototype of `TouchEvent` event object is:
``` ts
interface TouchEvent extends BaseEvent {
  isTarget: boolean, // Whether the event target is the current component
  touches: { // All touch point data of this event
    clientX: number, // The x-coordinate of the touch point relative to the target component's content area
    clientY: number, // The y-coordinate of the touch point relative to the target component's content area
    offsetX: number, // The displacement of the touch point in the x direction during the touch process
    offsetY: number  // The displacement of the touch point in the y direction during the touch process
  }[];
}
```


### `ClickEvent`


The prototype of the `SwipeEvent` event object is:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Whether the event target is the current component
  clientX: number, // The x-coordinate of the click touch point relative to the content area of ​​the target component
  clientY: number // The y-coordinate of the click touch point relative to the content area of ​​the target component
}
```


### `LongPressEvent`


The prototype of the `LongPressEvent` event object is:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Whether the event target is the current component
  clientX: number, // The x-coordinate of the long-press touch point relative to the content area of ​​the target component
  clientY: number // The y-coordinate of the long-press touch point relative to the content area of ​​the target component
}
```


### `SwipeEvent`


The prototype of the `SwipeEvent` event object is:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Whether the event target is the current component
  direction: 'left' | 'right' | 'up' | 'down' // Sweep direction
}
```


### `KeyEvent`


The `KeyEvent` object describes the user's interaction event with the entity key. This type is used for the event attributes of elements [`keydown`](#keydown) and [`keyup`](#keyup). The prototype of the `KeyEvent` event object is:
``` ts
interface KeyEvent  {
  type: 'keydown' | 'keyup', // Type of key event
  key: string, // Button name
  timestamp: number, // Timestamp of key event reporting, unit is milliseconds
  stopPropagation(): void // Call this method to prevent the event from bubbling
}
```


Currently the following key names are supported:
- `'Power'`: The power button of the watch;
- `'Fn'`: function keys of the watch;
- Other printable character keys use a single character to form the key name, such as the letter `'A'`, the minus sign `'-'`, etc.


### `WheelEvent`


The `WheelEvent` object describes the user interaction event for rotating the scroll wheel. This type is used for the event attribute of the element [`wheel`](#wheel). The signature of the `WheelEvent` event object is:
``` ts
interface WheelEvent {
  deltaY: number, // The scroll increment of the wheel in the y direction
  stopPropagation(): void // Call this method to prevent the event from bubbling
}
```


Unlike the Web's [wheel event](https://developer.mozilla.org/en-US/docs/Web/API/Element/wheel_event), `WheelEvent` in Glyphix currently only contains the `deltaY` attribute.


## incident response mechanism


### Event bubbling


Touch and gesture events support bubbling. Bubbling means that when an event occurs on an element, it first executes the handler on that element, then the handler on its parent element, and then all the way up to the handlers on other ancestors. In the example below, the green `p` component and the gray `div` component both listen to touch events. When the `p` component is clicked, it will be observed that both the `p` component and the `div` component can receive the event.


<glyphix id="generic-event-bubbling" height="250" title="触摸事件冒泡">


``` html
<div on:touchstart="onTouch('div', $event)"
     on:touchmove="onTouch('div', $event)"
     on:touchend="onRelease('div', $event)">
  <p on:touchstart="onTouch('p', $event)"
     on:touchmove="onTouch('p', $event)"
     on:touchend="onRelease('p', $event)">
    {{ `touchs: ${touchs.div ? 'div' : '-'} ${touchs.p ? 'p' : '-'}, target: ${target}` }}
  </p>
</div>
```


``` css
div {
  display: flex;
  flex-direction: column;
  background-color: lightgray;
  justify-content: space-around;
}

p {
  background-color: lightgreen;
  text-align: center;
  height: 150px;
}
```


``` js
export default {
  data: {
    touchs: { div: false, p: false },
    target: null
  },
  onTouch(name, event) {
    this.touchs[name] = true
    // The isTarget attribute can distinguish whether the target of the event is the component currently listening to the event.
    if (event.isTarget)
      this.target = name
  },
  onRelease(name, event) {
    this.touchs[name] = false
    if (event.isTarget)
      this.target = null
  }
}
```


</glyphix>



In Glyphix, only touch and gesture events in this document bubble up. Event capturing is currently not possible in JavaScript code.


### Prevent events from bubbling up


Use the `BaseEvent` method of `stopPropagation()` to prevent events from bubbling up to the parent.


### strong response event


There are two response priorities for touch or gesture events in Glyphix: strong response and weak response. When an event has multiple targets to respond to at the same time, strong responses have higher priority than weak responses. Assume that there are 3 levels of parent-child elements on the interface: `A -> B -> C`, where `C` is weakly responsive to events, and `B` is strongly responsive, then the event will be dispatched to `B` and will not be dispatched to `C` again. An element that originally responded strongly to an event will re-dispatch the event after changing to a weak response.


Touch and gesture events in [Generic events](#通用事件) are weakly responsive by default. In the example below, a green `p` component is placed inside a gray `scroll` and listens for all touch events from the `p` component. Since `scroll` by default responds strongly to up and down sliding gestures, weakly responds to left and right sliding gestures, and does not respond to other gestures, you can observe during operation:
- When you click on the `p` component, the `touchstart` event will be triggered, and when you let go, the `touchend` event will be triggered;
- When dragging the `p` component horizontally, the `touchmove` event will be triggered;
- When dragging the `p` component up and down, since the parent `scroll` component has a strong response to up and down sliding, while the `p` component in the template code only responds weakly to `touchmove`, the up and down sliding will be responded to by the `scroll` component, and the `p` component will receive the `touchcancel` event.


<glyphix id="generic-event-strong-response-1" height="250" title="强响应事件">


``` html
<scroll>
  <p on:touchstart="state = 'touchstart'"
     on:touchmove="state = 'touchmove'"
     on:touchend="state = 'touchend'"
     on:touchcancel="state = 'touchcancel'">
    {{ `p.state: ${state}` }}
  </p>
</scroll>
```


``` css
scroll {
  background-color: lightgray;
}

p {
  background-color: lightgreen;
  text-align: center;
  height: 150px;
  margin: 50px;
}
```


``` js
export default {
  data: {
    state: null
  }
}
```


</glyphix>



The default gesture event handling mechanism of many native components is highly responsive. Use the `BaseEvent` object's `strongResponse()` method to specify that an event is in strong response mode in JavaScript code. In the example below, the outer gray `div` component will strongly respond to gestures, so even if the inner `p` element is touched, the event will only be dispatched to the `div` element after the gesture starts.


<glyphix id="generic-event-strong-response-2" height="250" title="强响应事件">


``` html
<div on:touchstart="onTouch('div', 'start', $event)"
     on:touchmove="onTouch('div', 'move', $event)"
     on:touchend="onTouch('div', 'end', $event)"
     on:touchcancel="onTouch('div', 'cancel', $event)">
  <p on:touchstart="onTouch('p', 'start', $event)"
     on:touchmove="onTouch('p', 'move', $event)"
     on:touchend="onTouch('p', 'end', $event)"
     on:touchcancel="onTouch('p', 'cancel', $event)">
    {{ `div state: ${touchs.div}, p state: ${touchs.p}, target: ${target}` }}
  </p>
</div>
```


``` css
div {
  display: flex;
  flex-direction: column;
  background-color: lightgray;
  justify-content: space-around;
}

p {
  background-color: lightgreen;
  text-align: center;
  height: 150px;
}
```


``` js
export default {
  data: {
    touchs: { div: null, p: null },
    target: null
  },
  onTouch(name, state, event) {
    console.log(name, state, event.isTarget)
    this.touchs[name] = state
    // The isTarget attribute can distinguish whether the target of the event is the component currently listening to the event.
    // If it is a cancel event, the target will not be recorded.
    if (event.isTarget && state != 'cancel')
      this.target = name
    if (name == 'div')
      event.strongResponse()
  }
}
```


</glyphix>



### The default event handling of the page


By default, the page will respond weakly to gesture events and prevent events from bubbling up, so gesture events cannot be dispatched and delivered through the page. In addition, the page will exit when receiving a right touchmove gesture. Developers can also intercept the gesture to disable this feature.


The specific method is to listen to the `touchmove` gesture of the page component and prevent bubbling:
``` html
<!-- This div is the root component of the page -->
<div on:touchmove="$event.stopPropagation()">
  ...
</div>
```
In this way, this page cannot be returned by swiping right, but can be returned by pressing the physical Power key. To prevent the user from keying back first, you can use the following:
``` html
<!-- This div is the root component of the page -->
<div on:keydown="onKeyup">
  ...
</div>
```


``` js
export default {
  onKeyup(event) {
    // Disable event bubbling when the key value is 'Power' to prevent the page from exiting
    if (event.key == 'Power')
      event.stopPropagation()
  }
}
```


::: warning

Carefully replace the default event handling mechanism of the page to avoid the situation where the user cannot return to the page.
:::



::: tip

In previous versions, the `swipe` gesture event was used to prevent the default return behavior of the page, but this method has been abandoned in the 0.6.4 version. Please use the `touchmove` event handler above instead. This adjustment is caused by the fact that the interactive return animation of the page (ie, follow-up exit) is completely incompatible with the semantics of `swipe` that prevents the page from returning.
:::



## Tips


### Component location operations


Component position can be easily modified using the native component's `top` and `left` properties:
``` html
<div :top="40" :left="20"> ... </div>
```
`top` and `left` are actually shorthand for CSS properties of the same name, so they will only take effect in absolute layouts, which can be achieved with the following CSS:
``` css
div {
  position: absolute;
}
```


You can then use responsive properties to modify the component's position. The following example shows an animated random component position movement implemented in combination with [`transition` modifier](/framework/component/prop-modifier.md#transition-修饰符).


<glyphix id="generic-widget-position" height="250" title="随机组件位置">


``` html
<div id="pane">
  <p id="tile" :top="top" :left="left"
     top.transition left.transition>
    Tile
  </p>
</div>
```


``` css
div {
  background-color: lightgray;
}

p {
  /* To use the top / left properties of a component, it must be absolutely positioned */
  position: absolute;
  background-color: lightgreen;
  text-align: center;
  width: 3rem;
  height: 3rem;
  border: 4px solid red;
  border-radius: 10%;
}
```


``` js
export default {
  data: {
    top: 0,
    left: 0
  },
  timer: null,
  onReady() {
    // Get the component object, the position range should not exceed the #pane container
    const pane = this.$element("pane")
    const tile = this.$element("tile")
    const width = pane.width - tile.width
    const height = pane.height - tile.height
    this.timer = setInterval(() => {
      this.top = Math.random() * height
      this.left = Math.random() * width
    }, 2000)
  },
  onDestroy() {
    clearInterval(this.timer)
  }
}
```


</glyphix>



This example randomly sets the position of the `#tile` component every two seconds, within the bounds of the container `#pane`. The default `transition` modifier plays the transition animation for $1$ seconds.