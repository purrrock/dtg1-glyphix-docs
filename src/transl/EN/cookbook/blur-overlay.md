# Blur Overlay Menu

## Demo

This tutorial demonstrates the development technique of displaying an overlay menu after blurring the background. The following example shows this interactive effect (clicking the "..." button in the bottom right corner will display the blocking interface).

<glyphix id="cookbook-blur-overlay" width="410" height="502" title="Blur Overlay" inline>

</glyphix>

The main purpose of this tutorial is to show how to implement a blurred interface using Glyphix.

## Implementation

### Text Shadow

The shadow for the text "Hokkaido sika deer" in the example can be achieved by overlaying a layer of blurred text:
``` html
<stack class="wallpaper-title">
  <p class="shadow">Hokkaido sika deer</p>
  <p>Hokkaido sika deer</p>
</stack>
```
Place two identical texts inside a [`stack`](/components/stack.md) component, and use the bottom text as a shadow. This is achieved through the `shadow` CSS class on the bottom text:
``` css
.shadow {
  color: #0008;
  /* Add blur to the background text to render a shadow effect */
  filter: blur(8px);
  /* transparent must be used to indicate the element is transparent */
  transparent: true;
}
```
Set the color of the background text to translucent gray, and use the blur filter ([`filter: blur(8px)`](/framework/generic/styles.md#filter)) property to treat the `<p>` text component as a shadow. Note that the foreground text color should not be transparent, otherwise it might blend with the `.shadow` layer.

### Custom Fonts

The text "Hokkaido sika deer" is rendered using a custom font. In Glyphix, you can import custom fonts using the same method as on the Web:
``` css
@font-face {
  font-family: 'Playwrite Australia SA';
  src: url('/assets/PlaywriteAUSA-Regular.ttf');
}

.wallpaper-title {
  font-family: 'Playwrite Australia SA', 'sans-serif';
  color: #ffffff;
  margin-top: 25%;
}
```
As you can see, you can declare a font via the [`@font-face`](/framework/generic/styles.md#font-face-规则) block in CSS and reference it in the element's [`font-family`](/framework/generic/styles.md#font-family) property.

### Background Layer Blur

Since pages popped up via the [`router` API](/api/system-router.md) do not currently support translucent backgrounds, pages cannot be used to implement pop-up menus. However, you can use this technique to simulate a popped-up "page":
``` html
<stack class="window" :disabled="popups">
  <image class="wallpaper" src="/assets/images/sika-deer.jpg" />
  ...
</stack>
<div class="overlay" if="popups">
  ...
</div>
```
You need to add two layers of elements to the page (`stack.window` and `div.overlay` in this example) and control them via a condition (such as `popups`). Specifically:
- `popups` controls the `disabled` property of the underlying element, so when `popups` is true, the underlying element will not respond to inputs such as gestures;
- `popups` also controls the rendering of the top-level element, which is displayed when true.

When the overlay pops up, the [`disabled`](/framework/generic/properties.md#disabled) property also provides the opportunity to blur the underlying element:
``` css
.window:disabled {
  filter: blur(40px);
}
```
When the element has the `disabled` property set, the `:disabled` pseudo-element of the underlying element is also activated, so the blur effect in the CSS above will take effect.

::: tip
Since Glyphix does not support the browser's [`backdrop-filter`](https://developer.mozilla.org/docs/Web/CSS/backdrop-filter) property, background blur cannot be achieved directly through CSS rules on `div.overlay`. Instead, the technique demonstrated in this example must be used.
:::

## Performance Risks

Since blur effects are computationally intensive, developers need to pay special attention to their performance overhead. We recommend using blur effects only in static interfaces, and ideally adding the [`quiescent`](/framework/generic/properties.md#quiescent) property to elements that need to be blurred.

If possible, you should test whether the blurred interface meets performance expectations on physical devices.