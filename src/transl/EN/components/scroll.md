# scroll

A scrollable list container that supports arbitrary child components. The scrolling direction of the list is determined by the specific layout method: when using a flow layout or a flex layout in the `column` direction, elements are laid out vertically and the list can scroll vertically; when using a flex layout in the `row` direction, elements are laid out horizontally and the list can scroll horizontally. The `scroll` component does not support bidirectional scrolling (i.e., being scrollable in both horizontal and vertical directions simultaneously).

By default, the `scroll` component is a block-level element that uses a flow layout.

The `scroll` component can be scrolled using touch gestures. Vertical `scroll` components also support encoder scrolling (the rotating crown of a smartwatch, simulated using the mouse wheel on the simulator).

::: tip
Some interactive examples in this document support mouse wheel interaction (indicated by a mouse icon on the right side of the title): you can hover your pointer over the example and use the mouse wheel to scroll the list.
:::

## Properties

### `scroll` <decl type="{ scrollX: number, scrollY: number, scrollState: number }" get listen />

The value of the `scroll` property is an object containing the following fields: `scrollX`, `scrollY`, and `scrollState`. The `scrollX` and `scrollY` properties represent the horizontal and vertical scroll positions in pixels, respectively. The `scrollState` property represents the scroll state, with a value of $0$, $1$, or $2$, as detailed in the table below. Changes to the `scroll` property can be listened to via the `on` directive. Any change to the content position caused by user actions or API operations will trigger the listener.

| `scrollState` Value | Description |
| :--------------: | ------------------------------------------------------------------- |
|       $0$        | Sliding has stopped |
|       $1$        | Sliding via user gestures |
|       $2$        | The user has released their hand; sliding caused by methods like [`scrollTo`](#scrollto) or inertia |

::: info
The area where the children of `scroll` are located is called the "content" area, while the portion of the list component actually displayed is called the "view" area. Elements are laid out in the content area, and their dimensions may exceed the view area. Scrolling changes the display position of the content.
:::

The range of the scroll position is typically within the content area—that is, `scrollX` for a horizontal list is within the range $[0, \texttt{contentWidth}]$, and `scrollY` for a vertical list is within the range $[0, \texttt{contentHeight}]$. However, when the list is scrolled past the beginning of the content, `scrollX` or `scrollY` will be less than $0$; similarly, when scrolled past the end of the content, the value of `scrollX` or `scrollY` will be greater than `contentWidth` or `contentHeight`.

::: warning
The `scroll` event is triggered on every frame during the scrolling process. Listening to this event in JavaScript code may cause noticeable frame drops, so it should be avoided as much as possible.
:::

### `scrollTop` <decl type="number" set get listen />

The vertical scroll position, which is the distance from the top of the content of the `scroll` component to the top of the viewport, in pixels. You can set the scroll position or listen to changes in the scroll position using this property.

Unlike the [`scroll`](#scroll) property, listening to the `scrollTop` property itself cannot distinguish whether the scroll was caused by a user gesture, an API call, or inertia.

### `scrollLeft` <decl type="number" set get listen />

The vertical scroll position, which is the distance from the left of the content of the `scroll` component to the left of the viewport, in pixels. You can set the scroll position or listen to changes in the scroll position using this property.

Unlike the [`scroll`](#scroll) property, listening to the `scrollLeft` property itself cannot distinguish whether the scroll was caused by a user gesture, an API call, or inertia.

### `scrollWidth` <decl type="number" get listen />

The width of the content area of the `scroll` component. The width of a `scroll` in a vertical layout equals the viewport width, while the width of a `scroll` in a horizontal layout is the sum of the widths of all elements. You can listen to changes in the content width using this.

### `scrollHeight` <decl type="number" get listen />

The height of the content area of the `scroll` component. The height of a `scroll` in a vertical layout equals the viewport height, while the height of a `scroll` in a horizontal layout is the sum of the heights of all elements. You can listen to changes in the content height using this.

### `damping` <decl type="number" set />

Sets the damping coefficient for the list scrolling animation. The valid value range is $[0.1, 50]$ (unsupported values are automatically adjusted to the upper or lower limits), with a default value of $1.5$. A larger damping coefficient causes the animation to stop faster, while the default damping coefficient produces a longer-distance and longer-lasting inertial effect.

<glyphix id="components-scroll-damping" height="360" width="360" title="Damping Effect" wheel>

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
The damping coefficient should be set as a constant rather than modified dynamically; changing the damping coefficient will not affect the animation during rebounding.
:::

### `snapshot` <decl type="boolean" get set />

When the `snapshot` property is enabled, child components in the list will enter snapshot mode. For a related demonstration, refer to the [`quiescent`](/framework/generic/properties.md#quiescent) property of native components.

Enabling snapshots may improve the frame rate of complex interfaces. For example, when list items contain a large amount of text and a non-transparent background, snapshot mode can cache and combine numerous drawing operations into a small number of snapshots. The Glyphix framework will cache these snapshots across repeated drawings to further boost performance.

However, the `snapshot` property does not guarantee that child components will use snapshots; this property may be ignored when system memory is low or when using snapshots is unnecessary.

### `deformation` <decl type="string | function" set />

Sets the deformation effect of the list, which can be used to achieve appearances such as a fisheye effect. You can specify a built-in deformation effect by its name (string), or define a custom deformation effect using a JavaScript function.

|     Value      |             Description             |
| :---------: | :------------------------------: |
|  `'none'`   |       No deformation effect (default)       |
| `'fisheye'` |          Built-in fisheye effect          |
|  function   | Define a deformation effect via a JavaScript function |

Deformation effects should be constants and should not be modified.

When the list is set to the fisheye deformation effect, it is recommended to set the [`scrollSnap`](#scrollsnap) property to `'center'` for the most reasonable appearance.

The figure below demonstrates the fisheye deformation effect. You can use the "center" switch to adjust whether center alignment is enabled.

<glyphix id="components-scroll-deformation" height="360" width="360" title="Fisheye Effect" wheel>

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
Deformation effects generally utilize snapshots, so there is no need to separately configure the `snapshot` property when `deformation` is set.
:::

### `scrollSnap` <decl type="'none' | 'start' | 'center' | 'edge'" get set />

Sets the alignment and snapping behavior of list items. For example, you can center-align elements or snap them to their boundaries.

|     Value     | Description                                                                                                           |
| :--------: | -------------------------------------------------------------------------------------------------------------- |
|  `'none'`  | Elements have no alignment or snapping effects; child components can stop at any position according to scroll inertia. |
| `'start'`  | When scrolling stops, the start position of the element aligns with the start position of the viewport. This mode is currently not supported. |
| `'center'` | When scrolling stops, the center position of the element aligns with the center of the viewport. |
|  `'edge'`  | When scrolling stops, the start or end position of the element aligns to the nearest start or end position of the viewport. However, if scrolling does not cross an element boundary, no snapping will be triggered. |

The `scrollSnap` property does not adjust element dimensions, but you can utilize layout mechanisms to create lists of uniformly sized items.

::: warning
This property should be set during component initialization and must not be changed afterwards; otherwise, interaction errors may occur.
:::

### `index` <decl type="number" get set listen />

The index of the currently displayed child component. When the `index` property is set, the component will animate and scroll to the specified child component. You can listen to position changes using the `on` directive, and changes to the child component index can be detected via the `index` property.

The value of `index` is automatically clamped to ensure it points to a valid element. When using `index`, you must ensure that all elements of the `scroll` component are static (i.e., the CSS [`position`](/framework/generic/styles.md#position) property is the default `static`), otherwise errors will occur.

### `finalChanged` <decl type="bool" get set />

Sets whether to trigger [`index`](#index) change events only when scrolling stops. By default (i.e., when `finalChanged` is `false`), the listener event is triggered whenever scrolling gestures or other reasons cause the `index` property of the `scroll` component to change. However, this can easily lead to animation frame drops or overly frequent, unnecessary event triggers. When `finalChanged` is set, the `index` change event is triggered only when scrolling completely stops.

::: tip
When implementing point indicators or similar features by listening to the `index` property, it is recommended to set `finalChanged` to `true`. This prevents frame drops during the sliding process caused by event-triggered render updates.
:::

The following example demonstrates the effect of `finalChanged`. You can try toggling the "final-changed" checkbox, then swipe the list to observe the frequency and timing of `index` changes.

<glyphix id="components-scroll-final-changed" height="360" width="360" title="Delayed index Events" wheel>

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

Sets whether rebounding is triggered after scrolling the `scroll` to an edge via gestures. The initial value of this property is `edge`, meaning rebounding at both the start and end positions is allowed.

|    Value     | Description                                   |
| :-------: | -------------------------------------- |
| `'none'`  | Disables all edge rebounds.                     |
| `'start'` | Allows rebounding only when dragged past the start position of the content.     |
|  `'end'`  | Allows rebounding only when dragged past the end position of the content.     |
| `'edge'`  | Allows rebounding when dragged past either the start or end position of the content. |

The example below demonstrates the effects of various `bounces` values. You can try dragging each item left or right beyond the boundaries and observe the corresponding interaction behavior.

<glyphix id="components-scroll-bounces" height="360" width="400" title="Drag Rebound Animation">

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
Currently, the `bounces` property only affects rebounding caused by gesture operations, ignoring rapid inertial animation rebounds. The example above uses a technique to avoid unintended behavior:
- `.row-box` uses an edge-snapping strategy (`snap-type="edge"`) to prevent gesture animations with rebounds.
- Each element in `.row-box` does not exceed `100%` width, ensuring that the edge-snapping strategy does not trigger internal boundary rebounds.

This technique can be used for interfaces such as swipe-to-delete menus.
:::

The `bounces` property also plays a role similar to [`weakGesture`](#weakgesture). Specifically, once you cross a boundary where rebounding is disabled, scroll gesture events are automatically allowed to bubble up. Therefore, there is no need to set both `bounces` and `weakGesture` properties simultaneously.

::: tip
The scroll gesture bubbling behavior of `bounces` and `weakGesture` is "opposite". For example, the `end` mode rebound policy allows users to rebound after scrolling past the end of the list, whereas this policy allows scroll gestures at the start position to bubble. This corresponds to the effect of the `weakGesture` property with a value of `'start'`.
:::

### `weakGesture` <decl type="'none' | 'start' | 'end' | 'edge'" get set />

Sets under which circumstances the `scroll` component should bubble up scroll gestures. By default, `scroll` prevents gestures it responds to from bubbling, so its parent elements cannot receive gestures that cause `scroll` to scroll. `weakGesture` allows enabling gesture event bubbling when dragged to the content boundary positions, thereby allowing parent elements to receive these gestures.

|    Value     | Description                                             |
| :-------: | ------------------------------------------------ |
| `'none'`  | Does not bubble the gesture events it responds to.                     |
| `'start'` | Bubbles gesture events after being dragged to the start position of the content.       |
|  `'end'`  | Bubbles gesture events after being dragged to the end position of the content.       |
| `'edge'`  | Bubbles gesture events after being dragged to either the start or end position of the content. |

If the underlying element of a page is a horizontal `scroll` component, but you want a right-swipe gesture to exit the page, you can configure it like this:
``` html
<scroll weak-gesture="start"> ... </scroll>
```
When the user swipes to the beginning of the `scroll` component and continues to swipe right, they can exit the page.

::: warning
This property should be set during component initialization and must not be changed afterwards; otherwise, interaction errors may occur.
:::

### `scrollbar` <decl type="boolean" get set />

Indicates whether the `scroll` component should display a scrollbar (hidden by default). This is only supported for vertical layout `scroll` components. The `scrollbar` property must be a constant and cannot be modified using reactive properties. For example:
``` html
<scroll scrollbar>
  ...
</scroll>
```
This will create a `scroll` component with a scrollbar. For the appearance of the scrollbar, please refer to the example of the [`setIndex`](#setindex) method.

The style of the scrollbar is determined by the system—for example, it may appear as an arc on circular screens and as a straight bar on rectangular screens.

### `scrolled` <decl type="boolean" listen />

Use the `scrolled` property to listen to whether the list is in a scrolling state. An event property value of `true` indicates that the list is currently scrolling, while `false` means the list has stopped scrolling.

Both scrolling operations generated by user touch and programmatic scrolling via the `scroll` property will trigger the `scrolled` event. When the list transitions from scrolling to stopped, the parameter value of the `scrolled` event is `false`.

### `setIndex`
<decl method><pre>
(options: {
  index: number,
  behavior?: 'instant' | 'smooth'
}): void
</pre></decl>

Moves the viewport to the child component specified by the index. If this movement would cross the viewport boundary, the viewport position will stop at the first or last component. The properties of the `options` parameter are:
- `index`: The index of the target child component to move to, where $0$ represents the first child component.
- `behavior`: When set to `'smooth'`, an animated transition is used; when set to `'instant'` (default), it moves immediately to the specified child component position.

When calling `setIndex()`, you must ensure that all elements of the `scroll` component are static, otherwise errors will occur.

<glyphix id="components-scroll-setindex" height="360" width="400" title="setIndex Method">

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

Scrolls the content to a specified position. The properties of the `options` parameter are:
- `left`: Specifies the scroll position of the content along the y-axis. Omitting `left` or having a vertical layout on the scroll component will result in no y-axis scrolling.
- `top`: Specifies the scroll position of the content along the x-axis. Omitting `top` or having a horizontal layout on the scroll component will result in no x-axis scrolling.
- `behavior`: Specifies the transition effect for scrolling. `'instant'` (default) jumps directly to the target position without transition effects, while `'smooth'` scrolls smoothly with a transition effect.

The `scrollTo` method ignores element snapping effects.

### `scrollBy`
<decl method><pre>
(options: {
  left?: number,
  top?: number,
  behavior?: 'instant' | 'smooth'
}): void
</pre></decl>

Scrolls the content by a specified distance. Unlike [`scrollTo()`](#scrollTo), `scrollBy()` scrolls relative to the current content position. The properties of the `options` parameter are:
- `left`: Specifies the distance for the content to scroll along the y-axis. Omitting `left` or having a vertical layout on the scroll component will result in no y-axis scrolling.
- `top`: Specifies the distance for the content to scroll along the x-axis. Omitting `top` or having a horizontal layout on the scroll component will result in no x-axis scrolling.
- `behavior`: Specifies the transition effect for scrolling. `'instant'` (default) jumps directly to the target position without transition effects, while `'smooth'` scrolls smoothly with a transition effect.

The `scrollBy` method ignores element snapping effects.

## CSS Specifications

### Layout Direction Control

The scrolling direction of the `scroll` component is determined by its layout method. When using flow layout (default layout) or a flex layout in the `column` direction, elements are laid out vertically and the list can scroll vertically. When using a flex layout in the `row` direction, elements are laid out horizontally and the list can scroll horizontally.

<glyphix id="components-scroll-layout" height="360" width="740" title="Controlling Scroll Direction via Layout Method">

``` html
<div>
  <scroll>
    <p for="20">vertical scroll</p>
  </scroll>
  <!-- Used as a placeholder element since flex layout does not yet support gap -->
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

By default (`overflow: clip`), the padding of the `scroll` component directly clips the visible area. Once the content is scrolled, the padding area is always invisible. Setting `overflow: visible` allows the padding area to remain visible even when the content is scrolled.

<glyphix id="components-scroll-padding-overflow-visible" height="360" width="740" title="Padding with overflow: visible">

``` html
<div>
  <scroll :index="2">
    <p for="20">overflow: clip</p>
  </scroll>
  <!-- Used as a placeholder element since flex layout does not yet support gap -->
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

Even when `overflow: visible` is set, `scroll` clips its content to the padding-box rather than allowing it to overflow beyond that range, unlike regular elements such as `div`. This is because the scrolling behavior and layout mechanism of `scroll` require content to scroll within a defined area, rather than allowing it to expand indefinitely into external areas.

For ordinary containers like `div` with similar `overflow: visible` settings, content can extend beyond the entire `div` range (such as outside the red `border`):

<glyphix id="components-scroll-overflow-div" height="360" width="360" title="overflow: visible in div">

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

#### Recommended Settings for i18n Scenarios

In i18n (internationalization) scenarios, text inside `scroll` may need to overflow to avoid potential truncation. For such cases, the recommended setting is `overflow: visible`, which allows [text overflow](/framework/application/i18n.md#文本溢出) content to extend beyond the content boundaries of `scroll` during scrolling, maximizing available space for text display.

#### Relationship with HTML/CSS Specifications

The behavior of `scroll` when `overflow: visible` is set is similar to `div { overflow-y: scroll; }` in the HTML/CSS specification, where the padding keeps content visible during scrolling. For example, CSS like this:

```css
div {
  padding: 20px;
  overflow-y: scroll;
}
```

Produces the following effect, where the padding area does not clip the content during scrolling:

<div style="padding: 20px; background-color: var(--vp-c-grey-bg); overflow-y: scroll; height: 100px; width: 200px; border: 2px dotted red; font-family: sans-serif;">
  Michaelmas term lately over, and the Lord Chancellor sitting in Lincoln's Inn Hall.
  Implacable November weather. As much mud in the streets as if the waters had but
  newly retired from the face of the earth.
</div>

HTML `div` does not have a behavior that directly corresponds to `scroll` when `overflow: clip` is set.