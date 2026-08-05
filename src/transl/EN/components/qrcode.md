# qrcode

The `qrcode` component is used to display a [QR Code](https://en.wikipedia.org/wiki/QR_code). This component can display arbitrary text data, making it suitable for displaying URLs, payment codes, login QR code links, and other information.

In a fluid layout, the `qrcode` component defaults to a block-level element (`block`) and takes up a single line by itself.

## Attributes

### `value` <decl type="string" get set />

Sets the text data to be displayed as a QR code. The `qrcode` component will automatically select the appropriate version based on the length of the data, currently supporting up to version $12$.

## CSS Notes

To ensure the QR code is easily scannable, you should correctly set the CSS properties of the `qrcode` component, including:
- `color`: The dot (module) color of the QR code, typically set to black (`black` or `#000`);
- `background-color`: The background color of the QR code, which should usually be white (`white` or `#fff`);
- `padding` / `margin`: Sufficient padding and margins prevent the QR code from blending with other elements and increase the scanning recognition rate;
- `width` / `height`: The dimensions of the QR code must be large enough for easy capturing.

By default, each module of the QR code component occupies a $4\rm{px}\times 4\rm{px}$ area, which might be barely scannable on a watch. However, layout strategies such as flex may reduce the size of the QR code. Therefore, developers are advised to manually set the `width` and `height` properties of the QR code component as needed and test them on the device.

The example below demonstrates how to use the QR code component. Please note that various margins and paddings are set for the `qrcode` component in the CSS to ensure there is enough space between the QR code and other UI elements to avoid interfering with scanning.

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
  color: black; /* Set the QR code foreground color to black */
  background-color: white; /* Set the QR code background color to white */
  border-radius: 16px;
}

p {
  color: white;
  font-size: 0.75rem;
}
```

</glyphix>

::: tip
You should always explicitly set **high-contrast** dot color (`color`) and background (`background-color`) styles for the QR code component to prevent a decrease in recognizability caused by deviations in the device's default style themes and inherited style properties.

At the same time, please set a sufficiently large padding (`padding`) to ensure easy scanning and recognition.
:::