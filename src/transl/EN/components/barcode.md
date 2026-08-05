# barcode

The `barcode` component is used to display [Code 128](https://en.wikipedia.org/wiki/Code_128) barcodes. The `barcode` component can display any ASCII string, making it suitable for showing product barcodes, payment codes, and other information.

In flow layouts, the `barcode` component defaults to a block-level element (`block`) and will occupy a single line by itself.

## Attributes

### `value` <decl type="string" get set />

Sets the content to be displayed by the barcode. Supports any ASCII string.

## CSS Notes

To make the barcode easily scannable, the CSS properties of the `barcode` component should be set correctly. These include:
- `color`: The color of the barcode bars, generally set to black (`black` or `#000`);
- `background-color`: The background color of the barcode should typically be white (`white` or `#fff`);
- `padding` / `margin`: Sufficient inner and outer margins help prevent the barcode from blending with other elements, increasing the scanning recognition rate;
- `width` / `height`: The dimensions of the barcode must be large enough to be easily captured by a camera.

By default, each bar of the barcode component occupies a width of $2\rm px$ and a height of $32\rm px$. This may be too small on small-screen devices such as smartwatches. Developers are advised to manually set the `width` / `height` properties of the barcode component as needed and test them on actual devices.

The following example demonstrates how to use the barcode component. Note that various margins are set for the `barcode` component in the CSS to ensure there is enough spacing between the barcode and other UI elements to avoid scanning interference.

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
  color: black; /* Set the barcode foreground color to black */
  background-color: white; /* Set the barcode background color to white */
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
You should always explicitly set **high-contrast** colors for the barcode component's bar color (`color`) and background (`background-color`) styles to prevent reduced scannability caused by deviations in the device's default style themes or inherited style properties.

At the same time, please set a sufficiently large padding (`padding`) to ensure easy scanning and recognition.
:::