# swiper

Card view container, supporting arbitrary sub-components. The scrolling direction of the card view is specified by the specific layout mode: lists using the `flex-column` layout are vertical, while lists using the `flex-row` layout are horizontal.

## Properties

### `scroll` <decl type="{ scrollX: number, scrollY: number, scrollState: number }" get listen />

The `scroll` property value is an object containing the following fields: `scrollX`, `scrollY`, and `scrollState`. The `scrollX` and `scrollY` properties represent the horizontal and vertical scrolling positions in pixels, respectively. The `scrollState` property represents the scrolling state, with a value of $0$, $1$, or $2$, as detailed in the table below. Changes to the `scroll` property can be listened to using the `on` directive. Any content position changes caused by user operations and API operations will trigger the listener.

| `scrollState` Value | Description |
| :--------------: | ------------------------------------------------------------------- |
|       $0$        | Stopped scrolling |
|       $1$        | Scrolling via user gestures |
|       $2$        | The user has released their hand; scrolling is caused by method calls such as [`scrollTo`](#scrollto) or inertia |

### `scrollTop` <decl type="number" get listen />

The vertical scrolling position, which is the distance from the top of the `swiper` component's content to the top of the viewport, in pixels. This property can be used to listen to changes in the scroll position. Unlike the [`scroll`](#scroll) property, listening to the `scrollTop` property itself cannot distinguish whether it is a user gesture scroll, an API call, or an inertia-generated scroll.

### `scrollLeft` <decl type="number" get listen />

The horizontal scrolling position, which is the distance from the left of the `swiper` component's content to the left of the viewport, in pixels. This property can be used to listen to changes in the scroll position. Unlike the [`scroll`](#scroll) property, listening to the `scrollLeft` property itself cannot distinguish whether it is a user gesture scroll, an API call, or an inertia-generated scroll.

### `scrollWidth` <decl type="number" get listen />

The width of the `swiper` component's content area. The width of a vertically laid out `swiper` equals the viewport width, while the width of a horizontally laid out `swiper` is the sum of the widths of all elements. Changes to the content width can be listened to via this.

### `scrollHeight` <decl type="number" get listen />

The height of the `swiper` component's content area. The height of a vertically laid out `swiper` equals the viewport height, while the height of a horizontally laid out `swiper` is the sum of the heights of all elements. Changes to the content height can be listened to via this.

### `snapshot` <decl type="boolean" get set />

When the `snapshot` property is enabled, the sub-components of `swiper` will enter snapshot mode. Please refer to the [`snapshot`](scroll.md#snapshot) property of the `scroll` component.

### `deformation` <decl type="string" set />

Sets the deformation effect of child elements. Through deformation effects, appearances like fisheye can be achieved. A built-in deformation effect can be specified by name (string), or defined via a JavaScript function.

| Value | Description |
| :-: | :- |
| `'none'` | No deformation effect (default). |
| `'fade'` | Fade and scale transition effect. This effect highlights the "focus" of elements within the current viewport while making elements outside the viewport recede into the background. For details, please refer to the effect in the example in this section. |
| `'fisheye'` | Built-in fisheye effect. This property component is used for the [`scroll`](scroll.md) component rather than `swiper`. |
| function | Specifies the deformation effect via a JavaScript function. |

Deformation effects should be constants and should not be modified.

If the content of `swiper`'s child elements changes frequently, it is recommended to add the [`quiescent`](/framework/generic/properties.md#quiescent) property to the elements when using deformation effects to avoid updating during transitions and to improve performance. You can refer to the example below:

<glyphix id="components-swiper-deformation" height="360" width="360" title="Element Deformation Effect">

```html
<swiper deformation="fade" indicator>
  <div for="x in 5" :quiescent="x != 0">
    <progress-arc busy :start-angle="0" :stop-angle="360" />
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

progress-arc {
  width: 30%;
  height: 30%;
  margin-bottom: 5%;
}
```

</glyphix>

The first child element in the example does not have the `quiescent` property enabled, so it will continue to update during the transition process, while other elements will stop updating.

### `vertical` <decl type="boolean" set />

Sets whether the `swiper` component uses a vertical layout. When set to the default `false`, a horizontal layout is used. The following example demonstrates the interaction effect of a `swiper` under a vertical layout (note that it must be scrolled vertically; horizontal sliding will not respond).

<glyphix id="components-swiper-vertical" height="360" width="360" title="Vertical Layout">

``` html
<swiper vertical deformation="fade" indicator>
  <p for="x in 5">
    pane {{ x + 1 }}
    {{ x == 0 ? '(swipe up)' : x == 4 ? '(swipe down)' : '' }}
  </p>
</swiper>
```

``` css
p {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
}
```

</glyphix>

### `indicator` <decl type="boolean" get set />

Sets whether the `swiper` component displays dot indicators. The display position of the dot indicators is determined by the `vertical` property: for a vertical layout, the dot indicators are displayed in the middle of the right side; for a horizontal layout, they are displayed in the middle of the bottom. For specific effects, please refer to the examples of the [`deformation`](#deformation) and [`vertical`](#vertical) properties.

Refer to [Dot Indicator CSS Properties](#dot-indicator-css-properties) to learn how to customize the display style of dot indicators.

### `pageLength`  <decl type="number" set />

Sets the size or proportion of child pages. When expressed as a percentage, it sets the size of the sub-components along the sliding direction (relative to the component itself); when expressed as other numbers, it sets the size of the sub-components along the sliding direction.

### `index`  <decl type="number" get set listen />

The index of the currently displayed sub-component. When the `index` property is set, the component will scroll to the specified sub-component via animation. Position changes can be listened to using the `on` directive, and sub-component index changes can be listened to via the `index` property.

### `finalChanged` <decl type="bool" get set />

Sets whether to trigger the [`index`](#index) change event only when scrolling stops. By default (i.e., when `finalChanged` is `false`), listening events are triggered whenever scrolling gestures or other reasons cause the `index` property of the `swiper` component to change. However, doing so can easily lead to dropped animation frames, or overly frequent and unnecessary event triggering. When `finalChanged` is set, the `index` change event is triggered only when scrolling stops.

::: tip
When implementing dot indicators and other effects by listening to the `index` property, it is recommended to set `finalChanged` to `true`, which can prevent dropped frames caused by rendering updates triggered by events during the sliding process.
:::

### `weakGesture` <decl type="'none' | 'start' | 'end' | 'edge'" get set />

Sets under which circumstances the `swiper` component will bubble up scrolling gestures. By default, `swiper` prevents bubbling for the gestures it responds to, so its parent elements cannot receive gestures that cause `swiper` to scroll. `weakGesture` allows enabling gesture event bubbling when dragged to the content boundary positions, enabling parent elements to receive these gestures.

|    Value    | Description                                             |
| :-------: | ------------------------------------------------ |
| `'none'`  | Do not bubble responded gesture events.                     |
| `'start'` | Bubble responded gesture events after dragging to the start position of the content.       |
|  `'end'`  | Bubble responded gesture events after dragging to the end position of the content.       |
| `'edge'`  | Bubble responded gesture events after dragging to the start or end position of the content. |

If the underlying element of the page is a horizontal `swiper` component, but you want right-swipe gestures to return to the previous page, you can configure it like this:
``` html
<swiper weak-gesture="start"> ... </swiper>
```
When the user swipes to the beginning of the `swiper` component and continues to swipe right, they can exit the page.

### `bounces` <decl type="'none' | 'start' | 'end' | 'edge'" get set />

Sets whether to trigger a bounce effect after scrolling `swiper` to the boundaries via gestures. The initial value of this property is `edge`, which allows bouncing at the start and end positions. The `bounces` property of `swiper` is similar to the [`bounces`](scroll.md#bounces) property of the [`scroll`](scroll.md) component; please refer to the related documentation for more details.

### `scrolled` <decl type="boolean" listen />

Listens to whether the `swiper` component is in a scrolling state via the `scrolled` property. A property value of `true` triggered by the event indicates that it is currently scrolling, otherwise it means it has stopped scrolling.

Both scrolling operations generated by user touches and scrolling via the `scroll` property will trigger the `scrolled` event. When stopping from the scrolling state, the parameter value of the `scrolled` event is `false`.

### `setIndex`
<decl method><pre>
(options: {
  index: number,
  behavior?: 'instant' | 'smooth'
}): void
</pre></decl>

Moves the viewport to the sub-component specified by the index. If this move crosses the viewport boundary, the viewport position will stay at the first or last component. The roles of the `options` parameter properties are:
- `index`: The index of the target sub-component to move to, where $0$ represents the first sub-component.
- `behavior`: Uses an animation transition when set to `'smooth'`, or moves immediately to the specified sub-component position when set to `'instant'` (default).

### `scrollTo` <decl type="(position: number): void" method />

Scrolls the content to the specified position. The scrolling direction is consistent with the layout direction of the scroll component.

The `scrollTo` method ignores the snap effect of elements.

## CSS Specifications

### Dot Indicator CSS Properties

This section introduces the CSS properties available when the `swiper` component has the [`indicator`](#indicator) property enabled, which are used to control some display styles of the dot indicators. The dot indicators of `swiper` are always displayed as a group of horizontally or vertically aligned dots, and developers can only customize based on this foundation.

#### `indicator-color`

Defines the color of unselected dot indicators. The effect is shown below:

<glyphix id="components-swiper-indicator-color" height="360" width="360" title="Dot Indicator Color">

```html
<swiper indicator>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-color: #333;
  indicator-selected-color: #ff60ff;
  indicator-bottom: 16px;
}
```

</glyphix>

#### `indicator-selected-color`

Defines the color of selected dot indicators. For the effect, refer to the example of the [`indicator-color`](#indicator-color) property, where you can observe that the dot indicator corresponding to the selected page is displayed in the color defined by this CSS property.

#### `indicator-size`

Defines the size of each indicator dot in the dot indicators, in pixels. The default value is `10px`. The following example demonstrates the effect of setting the dot indicator size to `16px`:

<glyphix id="components-swiper-indicator-size" height="360" width="360" title="Dot Indicator Size">

```html
<swiper indicator>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-color: #333;
  indicator-selected-color: #ff60ff;
  indicator-bottom: 24px;
  indicator-size: 16px;
}
```

</glyphix>

#### `indicator-top`

When `swiper` has a [horizontal layout](#vertical), the `indicator-top` property can be used to specify the distance of the dot indicators from the top. By default, the dot indicators are displayed at the bottom middle position; this property can display them at the top:

<glyphix id="components-swiper-indicator-top" height="360" width="360" title="Top Dot Indicator">

```html
<swiper indicator>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-top: 16px;
}
```

</glyphix>

::: warning
Do not set `indicator-left`, `indicator-top`, `indicator-right`, and `indicator-bottom` at the same time, otherwise it will lead to unexpected dot indicator positions.
:::

#### `indicator-left`

When `swiper` has a [vertical layout](#vertical), the `indicator-left` property can be used to specify the distance of the dot indicators from the left. By default, the dot indicators are displayed in the middle of the right side; this property can display them on the left:

<glyphix id="components-swiper-indicator-left" height="360" width="360" title="Left Dot Indicator">

```html
<swiper indicator vertical>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-left: 16px;
}
```

</glyphix>

#### `indicator-right`

When `swiper` has a [vertical layout](#vertical), the `indicator-right` property can be used to specify the distance of the dot indicators from the right. The effect is shown below:

<glyphix id="components-swiper-indicator-right" height="360" width="360" title="Right Dot Indicator">

```html
<swiper indicator vertical>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```

``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-right: 32px;
}
```

</glyphix>

#### `indicator-bottom`

When `swiper` has a [horizontal layout](#vertical), the `indicator-bottom` property can be used to specify the distance of the dot indicators from the bottom. For the effect, refer to the examples of the [`indicator-color`](#indicator-color) and [`indicator-size`](#indicator-size) properties.

### `padding` and `overflow` <version-badge since="0.9" />

See the relevant instructions in the [scroll component](scroll.md#padding-and-overflow). The `padding` and `overflow` properties of the `swiper` component share the same behavioral specifications as properties of the same name in the `scroll` component. Please refer to the related documentation for more details.