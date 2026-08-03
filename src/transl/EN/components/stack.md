# stack


`stack` stacked layout components. In the stacked layout, the size and position of each subcomponent are the same as the `stack` component, and they are stacked and displayed in order. The following example shows two overlapping text elements within a `stack` component.


<glyphix id="components-stack-layout" height="100" width="200" title="堆叠布局">


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

The `stack` component always uses the stacked display layout strategy and cannot be changed to other layouts (such as flex layout or fluid layout) through CSS properties such as `display`.
:::



## layout behavior


`stack` components have a fixed stacking layout strategy. Its size is determined by two constraints:
1. The dimensions of `stack` are first specified by size CSS properties such as [`width`](../framework/generic/styles.md#width) or [`height`](../framework/generic/styles.md#width);
2. The layout of the parent element may directly determine the layout of `stack`, such as `align-items: stretch`, `flex: 1` and other attributes in flex layout;
3. Otherwise the size of the `stack` component is determined by the maximum width and maximum height of the child elements.


Once the size of `stack` is determined, all its child elements will have the same outer box size (that is, the size of the child element plus `border` and `margin`). This sometimes causes trouble, for example, if an image is used as the background through `stack`, and the size of the upper element is too large, the image may not fit.