# collapsible-header

The `collapsible-header` component is used to add a collapsible title bar to a scrolling list. This effect provides a view-saving interaction for watch-like devices, enhancing the user experience.

::: warning
<experimental /> This is an experimental component. Do not use methods other than those demonstrated in this documentation.
:::

## Attributes

This component supports [Generic Attributes](/framework/generic/properties.md) and has no dedicated attributes.

## Usage

The `collapsible-header` component must contain two child components, otherwise unexpected behavior may occur. A specific example is as follows:

```html
<collapsible-header>
  <p>This is a collapsible title</p>
  <scroll> ... </scroll>
</collapsible-header>
```

The first child element is a collapsible title, while the second element must be a scrollable container such as [`scroll`](/components/scroll.md). Below is a concrete example:

<glyphix id="components-collapsible-header-1" height="360" width="360" title="Collapsible Title Bar">

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

### Principle Explanation

`collapsible-header` accepts two child components: the first one is the collapsible title bar, and the second one must be a scrollable component similar to `scroll`. `collapsible-header` combines these two components and manipulates the display effect of the collapsible title bar as the list scrolls.

You can use a flow-layout-like approach to control the position of the title bar, for example:

```css
/* The top margin of the element is 48px, centered horizontally, suitable for circular screens. */
margin: 48px auto auto;
/* The left and top margins of the element are 12px, suitable for square screens. */
margin: 12px auto auto 12px;
```

Applying the above styles to the title bar element according to actual needs can achieve specific alignment effects. You can also use complex components containing child elements as the title bar, such as using a component that includes a back button and page title text. However, note that when clicking the title bar, the click event can be sent to both the scrolling list and the title bar simultaneously. If conflicts occur, they can be resolved by stopping event propagation.

### Precautions

You must provide two child components for `collapsible-header` according to the above requirements, and make sure not to get the order wrong. In addition, since the collapsible title bar and the underlying scrolling list are displayed stacked on top of each other, this may cause the first element of the list to overlap with the title bar. When necessary, developers should consider some placeholder method to avoid overlapping, and the centering [snap mode](/components/scroll.md#scrollsnap) of `scroll` (`scroll-snap="center"`) can also help avoid overlapping.