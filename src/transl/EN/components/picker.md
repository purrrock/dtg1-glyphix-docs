# picker


Text selector component. This component displays a group of text. Clicking on the middle text item will trigger the selection event, and the sliding operation can make all text items scroll and display.


::: warning

`picker` The functionality of the component has not been verified and it is not maintained.
:::



## property


### `range` <decl type="string[]" set />


All strings in the `range` attribute value will be displayed in the `picker` component. The user can manipulate the `picker` component to scroll or select these strings.


`range` refers to [`index` 属性](#index) for the indexing method of strings in attribute values.


### `loop` <decl type="boolean" set />


Configure whether the `picker` component is displayed in a loop (i.e. infinitely long). When the value of this attribute is `true`, the loop display is enabled, and the default is `false`.


### `value` <decl type="string" listen />


Monitor the text of the current selected item. This monitoring will be triggered when the selected item changes during scrolling operation. The function of this attribute can also be implemented through the `on:index="handle(rangeData[$event])"` method.


### `index` <decl type="Integer" get set listen />


`picker` The selected item index value of the component. The indexing rules are: [`range` 属性](#range) The index value of the first string item in the attribute value array is $0$, and the indexes of other strings are increased by one in sequence. Setting the `index` attribute can specify the selected item of the `picker` component, and you can also listen to changes in this attribute to detect changes in the selected item caused by scrolling operations.


### `scroll` <decl type="{ x: number y: number }" get set listen />


The scrolling operation can be monitored through the `scroll` attribute, and the `picker` component can also be manipulated in code to display the scrolling effect. Similar to aligned list components, the `picker` operation of `scroll` also aligns to the nearest item.


Since the `picker` component only supports vertical mode, the `x` field of the `scroll` attribute value is always `0`.


### `scrolled` <decl type="boolean" read listen />


Monitor whether `picker` is in the scrolling state through the `scrolled` attribute. The attribute value triggered by the event is `true` which means that `picker` is scrolling, otherwise it means that `picker` has stopped scrolling.


The scrolling operation caused by user touch and scrolling through the `scroll` attribute will trigger the `scrolled` event. When `picker` stops from the scrolling state, the parameter value of the `scrolled` event is `false`.


### `damping` <decl type="number" set />


Set the damping coefficient of `picker` scroll animation. The valid value range is $[ 0.1, 50]$ (unsupported values ​​will be automatically modified to the upper and lower limits). The default value is $ 1.5 $. A larger damping coefficient will cause the animation to stop faster, and the default damping coefficient value can produce an inertial effect with a longer distance and longer duration.


The damping coefficient should be set to a constant and not modified. Modifying the damping coefficient will not affect the rebound animation.