---
icon: xml
---
# Properties and Events

This section introduces the common property interfaces and events provided by all native components.

## Property List

### Common Properties

#### `top` <decl type="number" get set listen />

The position of the top of the component relative to the parent native component, in pixels. This property is actually a shorthand for the `top` property in inline styles. For more usage methods, see [Component Position Operation](#component-position-operation).

Reading or listening to the `top` property returns the calculated position of the component, which is the actual measured value after layout.

#### `left` <decl type="number" get set listen />

The position of the left side of the component relative to the parent native component, in pixels. This property is actually a shorthand for the `left` property in inline styles. For more usage methods, see [Component Position Operation](#component-position-operation).

Reading or listening to the `left` property returns the calculated position of the component, which is the actual measured value after layout.

#### `width` <decl type="number" get set listen />

The width of the component. When setting the `width` property, the [`width`](styles.md#width) property in the inline styles will be updated. Since CSS width uses the border-box model, the actually stored style value will automatically include the element's current `padding` and `border` sizes to ensure that the content width after layout matches the set value.

Reading or listening to the `width` property returns the layout-calculated content width, excluding `padding` and `border`.

#### `height` <decl type="number" get set listen />

The height of the component. When setting the `height` property, the [`height`](styles.md#height) property in the inline styles will be updated. Since CSS height uses the border-box model, the actually stored style value will automatically include the element's current `padding` and `border` sizes to ensure that the content height after layout matches the set value.

Reading or listening to the `height` property returns the layout-calculated content height, excluding `padding` and `border`.

#### `show` <decl type="boolean" get set/>

Sets whether the component is visible. Hidden components are neither displayed nor occupy layout space.

#### `quiescent` <decl type="boolean" get set/>

Sets whether the component snapshot updates automatically (quiescent snapshot). If a component is displayed via a snapshot, when this property value is `false` (default), the snapshot will be refreshed immediately to update the view when the component content updates; otherwise, the snapshot will not be updated immediately. Setting this property to `true` can improve UI performance, but will cause a lag in the displayed content.

The following example demonstrates the role of the `quiescent` property. Two `p` elements are placed inside a `scroll` container, and the `scroll` container has [snapshot mode](../../components/scroll.md#snapshot) enabled. When the user scrolls the `scroll` component, snapshots of the elements within it are taken. Since the first `p` element uses the normal snapshot mode while the second `p` element uses the quiescent snapshot mode, only the content update of the first `p` element can be observed during scrolling.

<glyphix id="generic-properties-quiescent" height="200" title="Lazy Snapshot">

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

Sets the inline style of the component. Currently, only [CSS properties](./styles.md) with the <badge type="info" text="inline" /> tag are supported.

#### `z-index` <decl type="number" get set />

The `z-index` property sets the Z-axis order of elements. Overlapping elements with a larger `z-index` will cover elements with a smaller one. This property value will be overridden by the [`z-index`](styles.md/#z-index) property in CSS.


#### `opacity` <decl type="number" get set />

Specifies the opacity of the component. The value range is $[0, 1]$, where $0$ represents completely transparent. It has the same effect as the CSS property [`opacity`](styles.md#opacity).

::: warning
The `opacity` value will affect the rendering performance of the element. For details, please refer to the description of the [`opacity`](styles.md#opacity) CSS property.
:::

#### `transform` <decl type="string" set />

Sets the transformation of the component, equivalent to the CSS [`transform`](styles.md#transform) property.

#### `disabled` <decl type="boolean" get set />

Used to set or get the disabled state of the component. When the property value is `true`, the element is in a disabled state, the user cannot interact with it, and the element will not respond to any gestures (such as clicks, drags, etc.). When the property value is the **default** `false`, the component is in an available state, and the user can interact with it normally.

The following example demonstrates the usage of the `disabled` property, while also using the [`:disabled`](styles.md#disabled) CSS pseudo-class to control styles. This example shows that a `div` element can respond to click gestures in the normal state, but does not respond to any gestures in the `disabled` state.

<glyphix id="generic-properties-disabled" height="200" title="disabled Property">

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

/* :disabled pseudo-class can control the style of elements in the disabled state */
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

### Common Events

Most native components support common events, which can be listened to using the [`on` directive](../commands/on.md). The value types of these events are introduced in the [Event Types](#event-types) section.

#### `touchstart` <decl type="TouchEvent" listen />

Triggered when the user starts touching the component. The event value is of type [`TouchEvent`](#touchevent).

#### `touchmove` <decl type="TouchEvent" listen />

Triggered when the user's touch point moves on the component. During the movement, this event will continue to trigger even if the touch point leaves the range of the current native component. The event value is of type [`TouchEvent`](#touchevent).

There is a certain "dead zone for movement" when transitioning the touch state from `touchstart` to `touchmove`. If the user's touch sliding distance is less than the dead zone range, `touchmove` will not be triggered. The movement dead zone range varies by device. The following example illustrates the movement dead zone.

<glyphix id="generic-properties-touchmove" height="200" title="Movement Dead Zone">

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

When the user's touch point leaves the screen, a `touchend` event is sent to the previously touched native component. The event value is of type [`TouchEvent`](#touchevent).

#### `touchcancel` <decl type="TouchEvent" listen />

Triggered when the touch on the native component is interrupted. The event value is of type [`TouchEvent`](#touchevent). There are multiple reasons that can cause a touch interruption, such as the component being hidden or the touch event being forcibly responded to by other elements.

#### `click` <decl type="ClickEvent" listen />

Triggered when the native component is clicked and released. The event value is of type [`ClickEvent`](#clickevent).

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

Triggered when the native component is pressed for a long time. The event value is of type [`LongPressEvent`](#longpressevent). The interactive example below shows the triggering timing of `longpress` and other events:

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

The triggering timing and duration of the `longpress` event vary by device, usually triggered after pressing for $500 \rm ms$. Unlike the [`click`](#click) event, `longpress` is triggered during the press, rather than upon release. For the above example, you will find that:
- When the press time is less than the long-press trigger time, releasing the touch triggers the `click` event;
- When pressed long enough, the `longpress` event is triggered, and releasing the touch triggers the `click` event (displayed as the "clicked." state);
- Moving during the press will not trigger the `longpress` or `click` events.

#### `swipe` <decl type="SwipeEvent" listen />

Triggered when the component is swiped quickly. The event value is of type [`SwipeEvent`](#swipeevent).

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

Triggered when a key is pressed down. The `keydown` and `keyup` events are used to capture physical key operations. To capture events, the native component must be in focus. The root element of the page always automatically gets focus, so the following code can capture `keydown` and `keyup` events:
``` html
<!-- Assuming this is the root element of the page -->
<div on:keydown="console.log($event)" on:keyup="console.log($event)">
  ...
</div>
```
Please refer to [`KeyEvent`](#keyevent) for the event value type.

Watch devices usually register [default key handlers](/api/system-internal.md#setdefaultkeyhandler), so application code can interact even if it does not respond to these types of events (for example, some watches return to the previous page when the Power button is pressed). To prevent default key responses, you can use the `stopPropagation()` method of the `KeyEvent` object to stop bubbling.

#### `keyup` <decl type="KeyEvent" listen />

Triggered when a key is released. For more details, please refer to the [`keydown`](#keydown) event.

#### `wheel` <decl type="WheelEvent" listen />

Triggered when the user operates a rotating wheel. Wheel devices include the rotating bezel of a watch or a mouse wheel. To capture this event, the native component must be in focus. The root element of the page always automatically gets focus, so the following code can capture the `wheel` event:
``` html
<!-- Assuming this is the root element of the page -->
<div on:wheel="console.log($event)">
  ...
</div>
```
Please refer to [`WheelEvent`](#wheelevent) for the event value type.

## Event Types

### `BaseEvent`

The `BaseEvent` event object provides methods to control event propagation. Its prototype is:
``` ts
interface BaseEvent {
  strongResponse(): void, // Force response to the event
  stopPropagation(): void // Stop event bubbling
}
```

### `TouchEvent`

The prototype of the `TouchEvent` event object is:
``` ts
interface TouchEvent extends BaseEvent {
  isTarget: boolean, // Whether the event target is the current component
  touches: { // All touch point data for this event
    clientX: number, // X coordinate of the touch point relative to the target component's content area
    clientY: number, // Y coordinate of the touch point relative to the target component's content area
    offsetX: number, // Displacement of the touch point in the X direction during the touch process
    offsetY: number  // Displacement of the touch point in the Y direction during the touch process
  }[];
}
```

### `ClickEvent`

The prototype of the `SwipeEvent` event object is:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Whether the event target is the current component
  clientX: number, // X coordinate of the click touch point relative to the target component's content area
  clientY: number // Y coordinate of the click touch point relative to the target component's content area
}
```

### `LongPressEvent`

The prototype of the `LongPressEvent` event object is:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Whether the event target is the current component
  clientX: number, // X coordinate of the long-press touch point relative to the target component's content area
  clientY: number // Y coordinate of the long-press touch point relative to the target component's content area
}
```

### `SwipeEvent`

The prototype of the `SwipeEvent` event object is:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Whether the event target is the current component
  direction: 'left' | 'right' | 'up' | 'down' // Swipe direction
}
```

### `KeyEvent`

The `KeyEvent` object describes the user's interaction events with physical keys. This type is used for the event properties of elements [`keydown`](#keydown) and [`keyup`](#keyup). The prototype of the `KeyEvent` event object is:
``` ts
interface KeyEvent  {
  type: 'keydown' | 'keyup', // Type of key event
  key: string, // Name of the key
  timestamp: number, // Timestamp when the key event was reported, in milliseconds
  stopPropagation(): void // Call this method to prevent event bubbling
}
```

The following key names are currently supported:
- `'Power'`: The power button of the watch;
- `'Fn'`: The function button of the watch;
- Keys for other printable characters consist of a single character as the key name, such as the letter `'A'`, hyphen `'-'`, etc.

### `WheelEvent`

The `WheelEvent` object describes the user's interaction events with a rotating wheel. This type is used for the event properties of elements [`wheel`](#wheel). The signature of the `WheelEvent` event object is:
``` ts
interface WheelEvent {
  deltaY: number, // Scrolling increment of the wheel in the Y direction
  stopPropagation(): void // Call this method to prevent event bubbling
}
```

Unlike the Web's [wheel event](https://developer.mozilla.org/en-US/docs/Web/API/Element/wheel_event), the `WheelEvent` in Glyphix currently only contains the `deltaY` property.

## Event Response Mechanism

### Event Bubbling

Touch and gesture events support bubbling. Bubbling means that when an event occurs on an element, it first executes the handler on that element, then executes the handler on its parent element, and so on up to handlers on other ancestors. In the example below, both the green `p` component and the gray `div` component listen for touch events. When clicking the `p` component, you can observe that both the `p` component and the `div` component receive the event.

<glyphix id="generic-event-bubbling" height="250" title="Touch Event Bubbling">

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
    // isTarget property can distinguish whether the target of the event is the current component listening to the event
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

In Glyphix, only the touch and gesture events in this document will bubble. Event capture cannot be performed in JavaScript code at present.

### Stopping Event Bubbling

Use the `stopPropagation()` method of `BaseEvent` to prevent the event from bubbling up to the parent.

### Strong Response Events

In Glyphix, touch or gesture events have two response priorities: strong response and weak response. When an event has multiple targets waiting to respond at the same time, the strong response has a higher priority than the weak response. Suppose there are 3 levels of parent-child elements on the interface: `A -> B -> C`, where `C` has a weak response to the event and `B` has a strong response. Then the event will be dispatched to `B` and will no longer be dispatched to `C`. An element that originally had a strong response event will re-dispatch events after being changed to a weak response.

The touch and gesture events in [Common Events](#common-events) are weakly responsive by default. In the example below, a green `p` component is placed inside a gray `scroll`, and all touch events of the `p` component are listened to. Since `scroll` strongly responds to up and down sliding gestures by default, weakly responds to left and right sliding gestures, and does not respond to other gestures, you can observe during operation that:
- Clicking the `p` component triggers the `touchstart` event, and releasing it triggers the `touchend` event;
- Dragging the `p` component horizontally triggers the `touchmove` event;
- Dragging the `p` component vertically—since the parent `scroll` component has a strong response to vertical sliding, while the `p` component in the template code only has a weak response to `touchmove`—results in the vertical sliding being responded to by the `scroll` component, and the `p` component receives a `touchcancel` event.

<glyphix id="generic-event-strong-response-1" height="250" title="Strong Response Events">

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

The default gesture event handling mechanism of many native components is strongly responsive. Using the `strongResponse()` method of the `BaseEvent` object can specify the event as strong response mode in JavaScript code. In the example below, the outer gray `div` component will strongly respond to gestures, so even if the inner `p` element is touched, the event will only be dispatched to the `div` component after the gesture starts.

<glyphix id="generic-event-strong-response-2" height="250" title="Strong Response Events">

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
    // isTarget property can distinguish whether the target of the event is the current component listening to the event.
    // Do not record the target if it is a cancel event.
    if (event.isTarget && state != 'cancel')
      this.target = name
    if (name == 'div')
      event.strongResponse()
  }
}
```

</glyphix>

### Default Event Handling of Pages

Pages weakly respond to gesture events by default and prevent event bubbling, so gesture events cannot be dispatched and transmitted through the page. In addition, pages will exit when receiving a rightward `touchmove` gesture. Developers can also intercept gestures to disable this feature.

The specific approach is to listen to the `touchmove` gesture of the page component and prevent bubbling:
``` html
<!-- This div is the root component of the page -->
<div on:touchmove="$event.stopPropagation()">
  ...
</div>
```
In this way, the page cannot be returned from via a right-swipe operation, but can be returned from by pressing the physical Power button. To also prevent users from returning via keypress, you can use the following method:
``` html
<!-- This div is the root component of the page -->
<div on:keydown="onKeyup">
  ...
</div>
```

``` js
export default {
  onKeyup(event) {
    // Prevent event bubbling to block page exit when key value is 'Power'
    if (event.key == 'Power')
      event.stopPropagation()
  }
}
```

::: warning
Exercise caution when overriding the default event handling mechanism of pages to avoid situations where users cannot return from the page.
:::

::: tip
In previous versions, the `swipe` gesture event was used to prevent the page's default return behavior, but this approach was deprecated in version 0.6.4. Please use the aforementioned `touchmove` event handling instead. This adjustment was made because the page's interactive return animation (i.e., follow-finger exit) is completely incompatible with the semantics of `swipe` preventing page returns.
:::

## Tips and Tricks

### Component Position Operation

You can easily modify the component position by utilizing the `top` and `left` properties of native components:
``` html
<div :top="40" :left="20"> ... </div>
```
`top` and `left` are actually shorthands for CSS properties of the same name, so they only take effect in absolute layouts, which can be achieved via the following CSS:
``` css
div {
  position: absolute;
}
```

You can then use reactive properties to modify the component's position. The example below shows animated random component position movement implemented in combination with the [`transition` modifier](/framework/component/prop-modifier.md#transition-modifier).

<glyphix id="generic-widget-position" height="250" title="Random Component Position">

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
  /* Absolute positioning is required to use the component's top / left properties */
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
    // Get component object, position range should not exceed the #pane container
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

This example randomly sets the position of the `#tile` component every two seconds, ensuring it stays within the boundaries of the container `#pane`. The default `transition` modifier plays a $1$-second transition animation.