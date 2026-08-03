# barcode

The `barcode` component is used to display [Code 128](https://en.wikipedia.org/wiki/Code_128) barcodes. The `barcode` component can display any ASCII string, making it suitable for showing product barcodes, payment codes, and other information.

In flow layout, the `barcode` component defaults to a block-level element (`block`) and occupies an entire row by itself.

## Attributes

### `value` <decl type="string" get set />

Sets the content to be displayed by the barcode. Supports any ASCII string.

## CSS Notes

To make the barcode easily scannable, you should correctly set the CSS properties of the `barcode` component, which include:
- `color`: The color of the barcode bars, usually set to black (`black` or `#000`);
- `background-color`: The background color of the barcode, which should typically be white (`white` or `#fff`);
- `padding` / `margin`: Sufficient inner and outer margins prevent the barcode from blending with other elements, increasing the scan recognition rate;
- `width` / `height`: The dimensions of the barcode must be large enough to be easily captured by a camera.

By default, each bar of the barcode component occupies $2\rm px$ in width and $32\rm px$ in height. This may be too small on small-screen devices such as smartwatches. Developers are advised to manually set the `width` and `height` properties of the barcode component as needed and test them on actual devices.

The example below demonstrates how to use the barcode component. Please note that various margins are set for the `barcode` component in the CSS to ensure there is enough space between the barcode and other UI elements to avoid interfering with scanning.

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
You should always explicitly set **high-contrast** styles for the barcode component's bar color (`color`) and background (`background-color`). This prevents reduced readability caused by discrepancies in the device's default style themes or inherited style properties.

Additionally, please set a sufficiently large padding (`padding`) to ensure easy scanning and recognition.
:::