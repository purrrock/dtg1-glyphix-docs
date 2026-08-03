# qrcode

`qrcode` 组件用于显示 [QR Code](https://en.wikipedia.org/wiki/QR_code) 二维码。该组件可以显示任意文本数据，适合用于显示网址、支付码、登陆扫码链接等信息。

在流式布局中，`qrcode` 组件默认为块级元素（`block`），会单独占据一行显示。

## 属性

### `value` <decl type="string" get set />

设置要显示为二维码的文本数据。`qrcode` 组件会自动根据数据的长度和长度选择合适的版本，目前最高支持版本 $12$。

## CSS 说明

要想让二维码容易被扫描，应正确设置 `qrcode` 组件的 CSS 属性，这包括：
- `color`：二维码的码点颜色，一般设置为黑色（`black` 或者 `#000`）；
- `background-color`：二维码的背景色通常要是白色（`white` 或者 `#fff`）；
- `padding` / `margin`：足够的内外边距可以避免二维码和其他元素混淆，增加扫描识别率；
- `width` / `height`：二维码的尺寸必须足够大以方便拍摄。

默认情况下二维码组件的每个码点（module）会占据 $4\rm{px}\times 4\rm{px}$ 范围，这在手表上可能只是一个勉强能被识别的尺寸。但是 flex 等布局策略可能缩小二维码的尺寸，因此建议开发者根据需要手动设置二维码组件的 `width` / `height` 属性并在设备上进行测试。

下面的例子展示了二维码组件的使用方法，请注意 CSS 中为 `qrcode` 组件设置了各种边距，这都是为了保证二维码和其他界面元素有足够的间隔以免干扰扫描。

<glyphix id="qrcode-1" :height="450" :width="350">

``` html
<div>
  <qrcode :value="text"/>
  <p>{{ text }}</p>
</div>
```

``` js
export default {
  data: {
    text: 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array'
  }
}
```

``` css
div {
  background-color: black;
  padding: 8px;
}

qrcode {
  margin: 16px;
  padding: 16px;
  color: black; /* 将二维码前景色设置为黑色 */
  background-color: white; /* 将二维码背景色设置为白色 */
  border-radius: 16px;
}

p {
  color: white;
  font-size: 0.75rem;
}
```

</glyphix>

::: tip
应总是显式设置**高对比度**的二维码组件的码点颜色（`color`）和背景（`background-color`）样式。以免设备的默认样式主题和继承的样式属性偏差导致识别性下降。

同时，请设置足够大的内边距（`padding`），确保容易扫描识别。
:::

