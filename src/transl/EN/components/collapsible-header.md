# collapsible-header

The `collapsible-header` component is used to add a collapsible header bar to a scrolling list. This effect provides an interactive way to save view area for watch-type devices and improves the user experience.

::: warning
<experimental /> This is an experimental component. Do not use methods other than those demonstrated in this documentation.
:::

## Attributes

This component supports [Generic Attributes](/framework/generic/properties.md) and has no dedicated attributes.

## Usage

The `collapsible-header` component must contain two child components, otherwise unexpected behavior may occur. A specific example is shown below:

```html
<collapsible-header>
  <p>This is a collapsible header</p>
  <scroll> ... </scroll>
</collapsible-header>
```

The first child element is a collapsible header, and the second element must be a scrollable container such as [`scroll`](/components/scroll.md). Below is a concrete example:

<glyphix id="components-collapsible-header-1" height="360" width="360" title="Collapsible Header Bar">

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

`collapsible-header` accepts two child components: the first one is the collapsible header bar, and the second one must be a scrollable component similar to `scroll`. `collapsible-header` combines these two components and manipulates the display effect of the collapsible header bar when the list scrolls.

You can use a flow-layout-like approach to control the position of the header bar, for example:

```css
/* The element has a top margin of 48px and is horizontally centered, suitable for circular screens. */
margin: 48px auto auto;
/* The element has a left and top margin of 12px, suitable for square screens. */
margin: 12px auto auto 12px;
```

By applying the above styles to the header bar element according to actual requirements, specific alignment effects can be achieved. You can also use complex components containing child elements as the header bar, such as using a component that includes a back button and page title text. However, note that when clicking the header bar, the click event can be sent to both the scrolling list and the header bar simultaneously. If there is a conflict, it can be resolved by stopping event propagation.

### Precautions

You must provide two child components for `collapsible-header` according to the above requirements, and do not mix up their order. In addition, since the collapsible header bar and the underlying scrolling list are displayed stacked, this may cause the first element of the list to overlap with the header bar. When necessary, developers should consider some placeholder method to avoid overlapping, and the centering [snap mode](/components/scroll.md#scrollsnap) (`scroll-snap="center"`) of `scroll` can also prevent overlapping.