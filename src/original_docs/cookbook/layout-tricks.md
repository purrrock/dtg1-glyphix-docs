# 布局技巧

## 限制元素宽度

你可以使用 `margin` 属性来限制元素的宽度。

<glyphix id="cookbook-margin-layout-1" width="360" height="100">

```html
<div>
  <div class="limit">
    <p>{{text}}</p>
  </div>
</div>
```

```css
div {
  background-color: lightgreen;
}

.limit {
  border: 1px solid red;
  margin: 0 150px;
  display: flex;
  justify-content: flex-start;
}

p {
  border: 1px solid gray;
  margin: 2px;
}
```

```js
export default {
  data: { text: 'A' },
  onInit() {
    let index = 1
    setInterval(() => {
      this.text += String.fromCharCode(index++ + 0x41)
      if (index > 26) {
        this.text = 'A'
        index = 1
      }
    }, 200)
  }
}
```

</glyphix>
