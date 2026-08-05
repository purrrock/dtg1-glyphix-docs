# span

`span` is also a text component. Unlike the [`p` component](p), the `span` component is an inline element by default and can span across multiple lines, similar to the [`label`](label) and [`a`](a) components. Text spanning across lines means the element can be laid out across multiple lines instead of occupying an entire "box".

The `span` component can be used to implement [rich text typography](/framework/render/rich-text.md#富文本显示).

<glyphix id="span" :height="36">

``` html
<div>
  Hello Glyphix, this is <span style="color: #f0f">span</span> label!
</div>
```

</glyphix>