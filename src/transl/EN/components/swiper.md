# swiper


Card view container, supporting any sub-component. The scrolling direction of the card view is specified by the specific layout method: the list using `flex-column` layout is vertical, while the list using `flex-row` layout is horizontal.


## property


### `scroll` <decl type="{ scrollX: number, scrollY: number, scrollState: number }" get listen />


The `scroll` attribute value is an object containing the following fields: `scrollX`, `scrollY`, and `scrollState`. The `scrollX` and `scrollY` attributes represent the horizontal and vertical scrolling positions respectively, in pixels; the `scrollState` attribute represents the scrolling state, and its value is $0$, $1$ or $2$. The specific meaning is as shown in the following table. Changes to the `scroll` attribute can be monitored through the `on` directive. Any change in content location caused by user operations and API operations will trigger monitoring.


| `scrollState` value | Effect description |
| :--------------: | ------------------------------------------------------------------- |

| $0$ | Stopped sliding |
| $1$ | Swiping via user's gesture |
| $2$ | The user has let go, sliding caused by method calls such as [`scrollTo`](#scrollto) or inertia |


### `scrollTop` <decl type="number" get listen />


The vertical scroll position, that is, the distance from the top of the content of the `swiper` component to the top of the viewport, in pixels. Changes in the scroll position can be monitored through this property. Unlike the [`scroll`](#scroll) attribute, the listener `scrollTop` attribute itself cannot distinguish between scrolling by the user's gestures and scrolling caused by API calls or inertia.


### `scrollLeft` <decl type="number" get listen />


The scroll position in the horizontal direction, that is, the distance from the left side of the content of the `swiper` component to the left side of the viewport, in pixels. You can use this property to monitor changes in the scroll position. Unlike the [`scroll`](#scroll) attribute, the listener `scrollLeft` attribute itself cannot distinguish between scrolling by the user's gestures and scrolling caused by API calls or inertia.


### `scrollWidth` <decl type="number" get listen />


`swiper` The width of the component's content area. The width of `swiper` in vertical layout is equal to the view width, while the width of `swiper` in horizontal layout is the sum of the widths of all elements. You can use this to monitor content width changes.


### `scrollHeight` <decl type="number" get listen />


`swiper` The height of the component's content area. The height of `swiper` in vertical layout is equal to the view height, while the height of `swiper` in horizontal layout is the sum of the heights of all elements. You can use this to monitor content height changes.


### `snapshot` <decl type="boolean" get set />


When the `snapshot` attribute is enabled, the subcomponents of `swiper` will enable snapshot mode. Please refer to the [`snapshot`](scroll.md#snapshot) attribute of the `scroll` component.


### `deformation` <decl type="string" set />


Set the deformation effect of the sub-element, and use the deformation effect to achieve fish-eye and other appearances. A built-in morph effect can be specified by name (a string), or a morph effect can be defined through a JavaScript function.


| Value | Effect Description |
| :-: | :- |

| `'none'` | No deformation effect (default). |
| `'fade'` | Fade zoom switching effect, this effect highlights the "focus" of elements within the current viewport and makes elements outside the viewport appear to take a back seat. See the effects of the examples in this section for details. |
| `'fisheye'` | Built-in fisheye effect, this attribute component is used for [`scroll`](scroll.md) component instead of `swiper`. |
| function | Specify the deformation effect through JavaScript function. |


The deformation effect should be constant and not modified.


If the content of `swiper`'s child elements changes frequently, it is recommended to add the [`quiescent`](/framework/generic/properties.md#quiescent) attribute to the element when using the transformation effect to avoid updating when switching and improve performance. You can refer to the following examples:


<glyphix id="components-swiper-deformation" height="360" width="360" title="元素形变效果">


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



The first child element in the example does not have the `quiescent` attribute turned on, so it will continue to update during the switching process, while other elements will stop updating.


### `vertical` <decl type="boolean" set />


Set whether the `swiper` component is vertically laid out. When the default is `false`, horizontal layout will be used. The following example demonstrates the `swiper` interaction effect under vertical layout (note that vertical scrolling is required, horizontal sliding is unresponsive).


<glyphix id="components-swiper-vertical" height="360" width="360" title="垂直布局">


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


Set whether the `swiper` component displays the point indicator. The display position of the point indicator is determined by the `vertical` attribute: the point indicator displays in the middle of the right side when the layout is vertical, and the point indicator displays in the middle of the bottom when the layout is horizontal. Please refer to the examples of [`deformation`](#deformation) and [`vertical`](#vertical) attributes for specific effects.


See [点指示器 CSS 属性](#点指示器-css-属性) to learn how to customize the display style of point indicators.


### `pageLength`  <decl type="number" set />


Set the size or proportion of the subpage. When it is a percentage, set the size of the subcomponent in the sliding direction (relative to the component itself); when it is other numbers, set the size of the subcomponent in the sliding direction.


### `index`  <decl type="number" get set listen />


The index of the currently displayed subcomponent. When the `index` attribute is set, the component will scroll to the specified subcomponent through animation. Position changes can be monitored through the `on` directive, and changes in subcomponent index can be monitored through the `index` attribute.


### `finalChanged` <decl type="bool" get set />


Set whether the [`index`](#index) change event is only triggered when scrolling stops. By default (that is, `finalChanged` is `false`), whenever the scroll gesture or other reasons cause the `index` attribute of the `swiper` component to change, its listening event will be triggered. However, doing so can easily cause animation frames to drop, or trigger too frequent and unnecessary events. When `finalChanged` is set, the `index` changed event will only be triggered when scrolling stops.


::: tip

When implementing effects such as point indicators by monitoring the `index` attribute, it is recommended to set `finalChanged` to `true`. This can avoid frame drops caused by event-triggered rendering updates during the sliding process.
:::



### `weakGesture` <decl type="'none' | 'start' | 'end' | 'edge'" get set />


Set the circumstances under which the `swiper` component will bubble scroll gestures. By default `swiper` blocks bubbling of gestures it responds to, so its parent element cannot receive gestures that cause `swiper` to scroll. `weakGesture` allows bubbling of gesture events when dragging into content boundaries, allowing the parent element to receive these gestures.


| value | description |
| :-------: | ------------------------------------------------ |

| `'none'` | Do not bubble the corresponding gesture event. |
| `'start'` | Bubbles the corresponding gesture event after dragging to the starting position of the content. |
| `'end'` | Bubbles the corresponding gesture event after dragging to the end of the content. |
| `'edge'` | Bubbles the corresponding gesture event after dragging to the beginning or end of the content. |


If the underlying element of the page is a horizontal `swiper` component, but you want the right swipe gesture to return the page, you can configure it like this:
``` html
<swiper weak-gesture="start"> ... </swiper>
```
When the user slides to the head of the `swiper` component and continues to slide right to exit the page.


### `bounces` <decl type="'none' | 'start' | 'end' | 'edge'" get set />


Set whether to trigger rebound after scrolling `swiper` to the boundary through gestures. The initial value of this property is `edge`, which allows rebounding of the start and end positions. The `bounces` attribute of `swiper` is similar to the [`bounces`](scroll.md#bounces) attribute of the [`scroll`](scroll.md) component. Please refer to the relevant documentation for more instructions.


### `scrolled` <decl type="boolean" listen />


Monitor whether the `swiper` component is in a scrolling state through the `scrolled` attribute. The attribute value triggered by the event is `true`, which means scrolling, otherwise it means that scrolling has stopped.


The scrolling operation caused by user touch and scrolling through the `scroll` attribute will trigger the `scrolled` event. When stopping from a scrolling state, the parameter value of the `scrolled` event is `false`.


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


### `scrollTo` <decl type="(position: number): void" method />


Scroll the content to the specified position. The scrolling direction is consistent with the layout direction of the scroll component.


The `scrollTo` method ignores the adsorption effect of elements.


## CSS specifications


### Point indicator CSS property


This section introduces the CSS properties available after the `swiper` component turns on the [`indicator`](#indicator) attribute. They are used to control part of the display style of the point indicator. `swiper`'s point indicator always appears as a set of dots arranged horizontally or vertically, and can only be customized by the developer.


#### `indicator-color`


Defines the color of the unselected point indicator. The effect is as follows:


<glyphix id="components-swiper-indicator-color" height="360" width="360" title="点指示器颜色">


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


Defines the color of the selected point indicator. You can refer to the example of the [`indicator-color`](#indicator-color) attribute for the effect. You can observe that the point indicator corresponding to the selected page displays the color defined by the CSS attribute.


#### `indicator-size`


Defines the size of each indicator point in the point indicator, in pixels. The default value is `10px`. The following example demonstrates the effect of setting the point indicator size to `16px`:


<glyphix id="components-swiper-indicator-size" height="360" width="360" title="点指示器大小">


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


When `swiper` has [水平布局](#vertical), use the `indicator-top` attribute to specify the distance of the point indicator from the top. By default, the point indicator will be displayed at the bottom center, this property can be used to display it at the top:


<glyphix id="components-swiper-indicator-top" height="360" width="360" title="顶部点指示器">


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

Do not set `indicator-left`, `indicator-top`, `indicator-right` and `indicator-bottom` at the same time, otherwise the point indicator position will be unpredictable.
:::



#### `indicator-left`


When `swiper` has [垂直布局](#vertical), use the `indicator-left` attribute to specify the distance of the point indicator from the left. By default, the point indicator will be displayed in the middle position on the right, this property can display it on the left:


<glyphix id="components-swiper-indicator-left" height="360" width="360" title="左侧点指示器">


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


When `swiper` has [垂直布局](#vertical), use the `indicator-right` attribute to specify the distance of the point indicator from the right. The effect is as follows:


<glyphix id="components-swiper-indicator-right" height="360" width="360" title="右侧点指示器">


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


When `swiper` has [水平布局](#vertical), use the `indicator-bottom` attribute to specify the distance of the point indicator from the bottom. The effect can be seen in the examples of the [`indicator-color`](#indicator-color) and [`indicator-size`](#indicator-size) attributes.


### `padding` and `overflow` <version-badge since="0.9" />


See the description of [scroll 组件](scroll.md#padding-和-overflow). The `padding` and `overflow` attributes of the `swiper` component have the same behavior specifications as the attributes of the same name of the `scroll` component. For more instructions, please refer to the relevant documentation.