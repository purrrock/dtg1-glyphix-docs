# barcode

`barcode` 组件用于显示 [Code 128](https://en.wikipedia.org/wiki/Code_128) 条形码。`barcode` 组件可以显示任意 ASCII 字符串，适合用于显示商品条码、支付码等信息。

在流式布局中，`barcode` 组件默认为块级元素（`block`），会单独占据一行显示。

## 属性

### `value` <decl type="string" get set />

设置条形码要显示的内容。支持任意 ASCII 字符串。

## CSS 说明

要想让条形码容易被扫描，应正确设置 `barcode` 组件的 CSS 属性，这包括：
- `color`：条形码的条颜色，一般设置为黑色（`black` 或者 `#000`）；
- `background-color`：条形码的背景色通常要是白色（`white` 或者 `#fff`）；
- `padding` / `margin`：足够的内外边距可以避免条形码和其他元素混淆，增加扫描识别率；
- `width` / `height`：条形码的尺寸必须足够大以方便拍摄。

默认情况下条形码组件的每一条码会占据 $2\rm px$ 宽度和 $32\rm px$ 高度，这在手表等小屏幕设备上可能过小，建议开发者根据需要手动设置条形码组件的 `width` / `height` 属性并在设备上进行测试。

下面的例子展示了条形码组件的使用方法，请注意 CSS 中为 `barcode` 组件设置了各种边距，这都是为了保证条形码和其他界面元素有足够的间隔以免干扰扫描。

<glyphix id="barcode-1" :height="150" :width="350">

``` html
<div>
  <barcode :value="text"/>
  <p>{{ text }}</p>
</div>
```

``` js
export default {
  data: {
    text: '9787111407010'
  }
}
```

``` css
div {
  background-color: black;
  padding: 8px;
}

barcode {
  margin: 8px;
  padding: 8px;
  color: black; /* 将条形码前景色设置为黑色 */
  background-color: white; /* 将条形码背景色设置为白色 */
  border-radius: 16px;
  height: 80px;
}

p {
  color: white;
  font-size: 0.75rem;
  text-align: center;
}
```

</glyphix>

::: tip
应总是显式设置**高对比度**的条形码组件的码点颜色（`color`）和背景（`background-color`）样式。以免设备的默认样式主题和继承的样式属性偏差导致识别性下降。

同时，请设置足够大的内边距（`padding`），确保容易扫描识别。
:::

