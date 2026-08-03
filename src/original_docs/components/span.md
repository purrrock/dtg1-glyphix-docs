# span

`span` 也是一种文本组件。和 [`p` 组件](p)不同，`span` 组件默认是行内元素并且可以跨行，[`label` ](label) 组件和 [`a`](a) 组件也有类似的效果。文本跨行是指元素可以跨越多行进行布局，而不是占据一整个“盒子”。

`span` 组件可以用于实现[富文本排版](/framework/render/rich-text.md#富文本显示)。

<glyphix id="span" :height="36">

``` html
<div>
  Hello Glyphix, this is <span style="color: #f0f">span</span> label!
</div>
```

</glyphix>
