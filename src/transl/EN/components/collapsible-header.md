# collapsible-header


The `collapsible-header` component is used to add a collapsible title bar to the scrolling list. This effect is used to provide an interactive effect that saves the view area for watch-type devices and improves the user experience.


::: warning

<experimental /> This is an experimental component, do not use it in ways not demonstrated in this document.
:::



## property


This component supports [通用属性](/framework/generic/properties.md) and has no dedicated attributes.


## How to use


There must be two subcomponents in the `collapsible-header` component, otherwise unexpected effects may occur. Specific examples are as follows:


```html
<collapsible-header>
  <p>这是可折叠的标题</p>
  <scroll> ... </scroll>
</collapsible-header>
```


The first child element is a collapsible title, and the second element must be a scrollable container such as [`scroll`](/components/scroll.md). Here is a specific example:


<glyphix id="components-collapsible-header-1" height="360" width="360" title="可折叠标题栏">


```html
<collapsible-header>
  <p class="title-bar" on:click="clickTitle">TITLE BAR</p>
  <scroll scroll-snap="center" deformation="fisheye">
    <p for="x in 20" class="item">item {{ x + 1 }}</p>
  </scroll>
</collapsible-header>
```


```js
import prompt from "@system.prompt";

export default {
  clickTitle() {
    prompt.showToast({ message: "title clicked" });
  }
}
```


```css
.title-bar {
  margin: 56px auto auto;
  transparent: true;
  font-size: 1.5rem;
}

.item {
  height: 33.3%;
  background-color: #ddd;
  border-radius: 20%;
  margin: 8px;
  transparent: true;
  padding: 12px;
  text-align: center;
}
```


</glyphix>



### Principle description


`collapsible-header` accepts two child components, the first of which is a collapsible title bar, and the second must be a scrollable component similar to `scroll`. `collapsible-header` combines these two components and manipulates the display of the collapsible title bar as the list scrolls.


You can use something like Fluid Layout to control the position of the title bar, for example:


```css
/* 元素的顶部间距为 48px，左右居中，适用于圆形屏幕。 */
margin: 48px auto auto;
/* 元素左侧和顶部间距为 12px，适用于方型屏幕。 */
margin: 12px auto auto 12px;
```


Set the above style to the title bar element according to actual needs to achieve a specific alignment effect. You can also use a complex component containing child elements as a title bar, for example using a component containing a back button and page title text. But be aware that when the title bar is clicked, the click event can be sent to both the scroll list and the title bar. If there is a conflict, it can be resolved by preventing the event from bubbling.


### Things to note


You must provide both subcomponents for `collapsible-header` as specified above, and in the correct order. In addition, since the collapsible title bar and the underlying scrolling list are displayed stacked, this may cause the first element of the list to overlap with the title bar. When necessary, developers should consider some kind of placeholder method to avoid overlap, and centered `scroll` [吸附模式](/components/scroll.md#scrollsnap) ( `scroll-snap="center"` ) can also avoid overlap.