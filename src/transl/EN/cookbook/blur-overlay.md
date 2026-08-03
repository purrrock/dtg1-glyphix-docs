# Blur Overlay Menu

## Demo

This tutorial demonstrates the development technique of displaying an overlay menu after blurring the background. The following example shows this interactive effect (click the "..." button in the bottom right corner to show the overlay interface).

<glyphix id="cookbook-blur-overlay" width="410" height="502" title="Blur Overlay" inline>

</glyphix>

The main purpose of this tutorial is to show how to implement a blurred interface using Glyphix.

## Implementation

### Text Shadow

The shadow of the text "Hokkaido sika deer" in the example can be achieved by overlaying a layer of blurred text:
``` html
<stack class="wallpaper-title">
  <p class="shadow">Hokkaido sika deer</p>
  <p>Hokkaido sika deer</p>
</stack>
```
Place two identical texts inside a [`stack`](/components/stack.md) component, and use the bottom text as the shadow. This is achieved through the `shadow` CSS class on the bottom text:
``` css
.shadow {
  color: #0008;
  /* Add blur to the background text to create a shadow effect */
  filter: blur(8px);
  /* transparent is required to mark the element as transparent */
  transparent: true;
}
```
Set the color of the background text to translucent gray, and use the blur filter ([`filter: blur(8px)`](/framework/generic/styles.md#filter)) property to turn the `<p>` text component into a shadow. Note that the foreground text color should not be transparent, otherwise it may overlap with the `.shadow` layer.

### Custom Fonts

The text "Hokkaido sika deer" is rendered using a custom font. In Glyphix, custom fonts can be introduced using the same method as on the Web:
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
As you can see, a font can be declared in CSS via the [`@font-face`](/framework/generic/styles.md#font-face-规则) block and referenced in the element's [`font-family`](/framework/generic/styles.md#font-family) property.

### Background Blur

Since pages popped up via the [`router` API](/api/system-router.md) do not currently support translucent backgrounds, pages cannot be used to implement popup menus. However, this technique can be used to simulate a popped-up "page":
``` html
<stack class="window" :disabled="popups">
  <image class="wallpaper" src="/assets/images/sika-deer.jpg" />
  ...
</stack>
<div class="overlay" if="popups">
  ...
</div>
```
You need to add two layers of elements to the page (`stack.window` and `div.overlay` in this example), and control them through a condition (such as `popups`). Specifically:
- `popups` controls the `disabled` property of the underlying element, so when `popups` is true, the underlying element will not respond to inputs such as gestures;
- `popups` also controls the rendering of the top-level element, which is displayed when it is true.

When the overlay pops up, the [`disabled`](/framework/generic/properties.md#disabled) property also provides an opportunity to blur the underlying element:
``` css
.window:disabled {
  filter: blur(40px);
}
```
When the element is set with the `disabled` property, the `:disabled` pseudo-class of the underlying element is also activated, so the blur effect in the CSS above will take effect.

::: tip
Since Glyphix does not support the browser's [`backdrop-filter`](https://developer.mozilla.org/docs/Web/CSS/backdrop-filter) property, you cannot achieve background blur directly through CSS rules on `div.overlay`, but instead must use the technique in this example.
:::

## Performance Risks

Since blur effects are computationally intensive, developers need to pay special attention to their performance burden. We recommend using blur effects only in static interfaces, and preferably adding the [`quiescent`](/framework/generic/properties.md#quiescent) property to elements that need to be blurred.

If possible, you should test whether the blurred interface meets performance expectations on physical devices.