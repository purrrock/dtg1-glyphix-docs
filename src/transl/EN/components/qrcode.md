# qrcode


The `qrcode` component is used to display the [QR Code](https://en.wikipedia.org/wiki/QR_code) QR code. This component can display any text data and is suitable for displaying information such as website addresses, payment codes, login scan code links, etc.


In a fluid layout, the `qrcode` component defaults to a block-level element (`block`) and will be displayed on a separate line.


## property


### `value` <decl type="string" get set />


Set the text data to be displayed as a QR code. The `qrcode` component will automatically select the appropriate version based on the length and length of the data. Currently, the highest supported version is $12$.


## CSS description


To make the QR code easy to scan, the CSS properties of the `qrcode` component should be set correctly, including:
- `color`: The code point color of the QR code, generally set to black (`black` or `#000`);
- `background-color`: The background color of the QR code is usually white (`white` or `#fff`);
- `padding` / `margin`: Sufficient internal and external margins can avoid confusion between the QR code and other elements and increase the scanning recognition rate;
- `width` / `height`: The size of the QR code must be large enough to facilitate shooting.


By default, each code point (module) of the QR code component will occupy the range of $4\rm{px}\times 4\rm{px}$, which may only be a barely recognizable size on a watch. However, layout strategies such as flex may reduce the size of the QR code, so developers are recommended to manually set the `width` / `height` properties of the QR code component as needed and test on the device.


The following example shows how to use the QR code component. Please note that various margins are set for the `qrcode` component in CSS. This is to ensure that there is enough space between the QR code and other interface elements to avoid interfering with scanning.


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

The codepoint color ( `color` ) and background ( `background-color` ) styles of **high contrast** QR code components should always be set explicitly. To avoid deviations between the device's default style theme and inherited style attributes, resulting in reduced recognition.


At the same time, please set a large enough padding (`padding`) to ensure easy scanning and recognition.
:::
