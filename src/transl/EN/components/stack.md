# stack

`stack` is a stacked layout component. In a stacked layout, each child component has the same size and position as the `stack` component, and they are stacked and displayed sequentially in the order they are added. The following example shows two text elements overlapping inside a `stack` component.

<glyphix id="components-stack-layout" height="100" width="200" title="Stacked Layout">

``` html
<stack>
  <p class="text1">Text 1</p>
  <p class="text2">Text 2</p>
</stack>
```

``` css
* {
  text-align: center;
}

.text1 {
  font-size: 64px;
  color: #fff;
}

.text2 {
  font-size: 48px;
  color: #f008;
}

stack {
  background-color: gray;
}
```

</glyphix>

::: tip
The `stack` component always uses the stacked layout strategy and cannot be changed to other layouts (such as flex layout or flow layout) via CSS properties like `display`.
:::

## Layout Behavior

The `stack` component has a fixed stacked layout strategy. Its size is determined by two types of constraints:
1. The size of the `stack` is first specified by size-related CSS properties such as [`width`](../framework/generic/styles.md#width) or [`height`](../framework/generic/styles.md#width);
2. The layout of the parent element may directly determine the layout of the `stack`, such as properties like `align-items: stretch` or `flex: 1` in a flex layout;
3. Otherwise, the size of the `stack` component is determined by the maximum width and maximum height of its child elements.

Once the size of the `stack` is determined, all of its child elements will have the same outer frame size (i.e., the size of the child element plus `border` and `margin`). This can sometimes cause confusion; for example, using a `stack` to set an image as a background might result in the image failing to fill the area if the upper-layer element is too large.