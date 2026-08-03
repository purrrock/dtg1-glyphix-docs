# div

`div` 是最基本的容器组件。`div` 支持子组件及布局，但是不支持滚动（内容超出边界会直接裁剪）。如果想要内容滚动，请使用 [scroll](scroll) 组件。

## 注意事项

### 文本显示

`div` 组件不能直接用于显示文本，而是要使用 `p` 等文本组件来显示文本，例如：

```html
<!-- 错误的写法，不会显示文本 -->
<div>text content.</div>
<!-- 正确的写法 -->
<p>text content.</p>
```

不过如果 `div` 内有多个子元素，那么可以将文本作为它的子元素：

```html
<div>
  first element,
  <span style="color: #f0f">second element.</span>
</div>
```

<Glyphix id="components-div-text-element" height="48" width="360" inline >

```html
<div>
  first element,
  <span style="color: #f0f">second element.</span>
</div>
```

</Glyphix>
