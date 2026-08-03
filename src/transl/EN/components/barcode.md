# barcode


The `barcode` component is used to display the [Code 128](https://en.wikipedia.org/wiki/Code_128) barcode. The `barcode` component can display any ASCII string and is suitable for displaying product barcodes, payment codes and other information.


In a fluid layout, the `barcode` component defaults to a block-level element (`block`) and will be displayed on a separate line.


## property


### `value` <decl type="string" get set />


Set the content to be displayed in the barcode. Arbitrary ASCII strings are supported.


## CSS description


To make barcodes easily scannable, the CSS properties of the `barcode` component should be set correctly, including:
- `color`: Bar code bar color, generally set to black (`black` or `#000`);
- `background-color`: The background color of the barcode is usually white (`white` or `#fff`);
- `padding` / `margin`: Sufficient inner and outer margins can avoid confusion between barcodes and other elements and increase the scanning recognition rate;
- `width` / `height` : The size of the barcode must be large enough to be easily photographed.


By default, each barcode of the barcode component will occupy $2\rm px$ width and $32\rm px$ height, which may be too small on small screen devices such as watches. It is recommended that developers manually set the `width` / `height` attributes of the barcode component as needed and test on the device.


The following example shows how to use the barcode component. Please note that various margins are set for the `barcode` component in CSS. This is to ensure that there is enough space between the barcode and other interface elements to avoid interfering with scanning.


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

The codepoint color ( `color` ) and background ( `background-color` ) styles of high-contrast barcode components should always be set explicitly. To avoid deviations between the device's default style theme and inherited style attributes, resulting in reduced recognition.


At the same time, please set a large enough padding (`padding`) to ensure easy scanning and recognition.
:::
