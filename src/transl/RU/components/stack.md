# stack

`stack` 是堆叠布局组件。在堆叠布局中，每个子组件的尺寸和位置与 `stack` 组件相同，并且按照先后顺序依次堆叠显示。下面的例子展示了两个在 `stack` 组件内重叠显示的文本元素。

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
`stack` 组件总是使用堆叠显示的布局策略，无法通过 `display` 等 CSS 属性将其更改为其他布局（如 flex 布局或流式布局）。
:::

## 布局行为

`stack` 组件具有固定的堆叠布局策略。其尺寸由以下规则决定：
1. `stack` 的尺寸首先由 [`width`](../framework/generic/styles.md#width) 或 [`height`](../framework/generic/styles.md#width) 等尺寸 CSS 属性指定；
2. 父级元素的布局可能会直接决定 `stack` 的布局，例如 flex 布局中的 `align-items: stretch`、`flex: 1` 等属性；
3. 否则，`stack` 组件的尺寸由子元素的最大宽度和最大高度决定。

一旦确定了 `stack` 的尺寸，其所有子元素都将具有相同的边框盒尺寸（即子元素加上 `border` 和 `margin` 后的尺寸）。这有时会带来困扰，例如通过 `stack` 将一张图片作为背景时，如果上层元素的尺寸过大，可能会导致这张图片无法铺满。