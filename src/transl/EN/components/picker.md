# picker

A text picker component. This component displays a set of texts. Clicking the middle text item triggers a selection event, while swiping allows all text items to be scrolled.

::: warning
The functionality of the `picker` component is unverified and unmaintained.
:::

## Properties

### `range` <decl type="string[]" set />

All strings in the `range` property value will be displayed in the `picker` component. Users can scroll or select these strings within the `picker` component.

For the indexing method of the strings in the `range` property value, refer to the [`index` property](#index).

### `loop` <decl type="boolean" set />

Configures whether the `picker` component displays in a looping (i.e., infinite) manner. When this property is set to `true`, looping is enabled. The default value is `false`.

### `value` <decl type="string" listen />

Listens to the text of the currently selected item. This listener is triggered when the selected item changes during scrolling. The functionality of this property can also be achieved using `on:index="handle(rangeData[$event])"`.

### `index` <decl type="Integer" get set listen />

The selected item index of the `picker` component. The indexing rule is: the index of the first string item in the [`range` property](#range) value array is $0$, and the indices of subsequent strings increment by one. Setting the `index` property specifies the selected item of the `picker` component, and you can also listen to changes in this property to detect selected item changes caused by scrolling operations.

### `scroll` <decl type="{ x: number y: number }" get set listen />

The `scroll` property can be used to listen to scrolling operations, as well as to programmatically control scrolling effects in the `picker` component. Similar to aligned list components, the `scroll` operation of the `picker` will snap to the nearest item.

Since the `picker` component only supports vertical mode, the `x` field of the `scroll` property value is always `0`.

### `scrolled` <decl type="boolean" read listen />

Listens to whether the `picker` is in a scrolling state via the `scrolled` property. A property value of `true` triggered by the event indicates that the `picker` is scrolling, otherwise it means the `picker` has stopped scrolling.

Both user touch-induced scrolling and programmatic scrolling via the `scroll` property will trigger the `scrolled` event. When the `picker` stops from a scrolling state, the parameter value of the `scrolled` event is `false`.

### `damping` <decl type="number" set />

Sets the damping coefficient for the `picker` scrolling animation. The valid value range is $[0.1, 50]$ (unsupported values will be automatically clamped to the upper or lower limits), with a default value of $1.5$. A larger damping coefficient causes the animation to stop faster; the default damping coefficient produces a relatively long-distance and long-duration inertial effect.

The damping coefficient should be set as a constant rather than modified; modifying the damping coefficient will not affect the bounce-back animation.