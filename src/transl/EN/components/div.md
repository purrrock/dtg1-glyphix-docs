# div


`div` is the most basic container component. `div` supports subcomponents and layout, but does not support scrolling (content will be cropped directly if it exceeds the boundary). If you want content to scroll, use the [scroll](scroll) component.


## Things to note


### text display


The `div` component cannot be used directly to display text. Instead, text components such as `p` must be used to display text, for example:


```html
<!-- 错误的写法，不会显示文本 -->
<div>text content.</div>
<!-- 正确的写法 -->
<p>text content.</p>
```


However, if `div` has multiple child elements, you can use text as its child element:


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
