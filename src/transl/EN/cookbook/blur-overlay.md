# blur overlay menu


## Effect display


This tutorial demonstrates the development techniques for displaying the overlay menu after blurring the background. The following example demonstrates this interaction effect (clicking the "..." button in the lower right corner will display the occlusion interface).


<glyphix id="cookbook-blur-overlay" width="410" height="502" title="模糊覆盖层" inline>


</glyphix>



The main purpose of this tutorial is to show how to implement an interface with blur using Glyphix.


## Implementation method


### text shadow


The text "Hokkaido sika deer" in the example can be shadowed by overlaying a layer of blurred text:
``` html
<stack class="wallpaper-title">
  <p class="shadow">Hokkaido sika deer</p>
  <p>Hokkaido sika deer</p>
</stack>
```
Place two identical pieces of text inside a [`stack`](/components/stack.md) component, with the underlying text as a shadow. This is achieved via the `shadow` CSS class of the underlying text:
``` css
.shadow {
  color: #0008;
  /* 为背景文本添加模糊，以呈现阴影效果 */
  filter: blur(8px);
  /* 必须使用 transparent 标记元素是透明的 */
  transparent: true;
}
```
Set the color of the background text to a semi-transparent gray and the `<p>` text component as a shadow via the blur filter ( [`filter: blur(8px)`](/framework/generic/styles.md#filter) ) attribute. Please note that the foreground text color should not be transparent, otherwise it may overlap with the `.shadow` layer.


### Custom font


The text "Hokkaido sika deer" is rendered through a custom font. Custom fonts can be introduced in Glyphix in the same way as on the Web:
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
As you can see, a font can be declared in CSS via the [`@font-face`](/framework/generic/styles.md#font-face-规则) block and referenced in the element's [`font-family`](/framework/generic/styles.md#font-family) attribute.


### background layer blur


Since pages currently popped up through [`router` API](/api/system-router.md) do not support translucent backgrounds, pages cannot be used to implement popup menus. But you can use this trick to simulate a popup "page":
``` html
<stack class="window" :disabled="popups">
  <image class="wallpaper" src="/assets/images/sika-deer.jpg" />
  ...
</stack>
<div class="overlay" if="popups">
  ...
</div>
```
You need to add two levels of elements to the page (`stack.window` and `div.overlay` in this case) and control them through a condition (such as `popups`). Specifically:
- `popups` controls the `disabled` attribute of the underlying element, so when `popups` is true, the underlying element does not respond to input such as gestures;
- `popups` also controls the rendering of top-level elements. When it is true, the top-level elements will be displayed.


The [`disabled`](/framework/generic/properties.md#disabled) attribute also provides the opportunity to blur underlying elements when the occlusion layer pops up:
``` css
.window:disabled {
  filter: blur(40px);
}
```
When the `disabled` attribute is set on an element, the `:disabled` pseudo-element of the underlying element will also be activated, so the blur effect of the above CSS will work.


::: tip

Since Glyphix does not support the browser's [`backrop-filter`](https://developer.mozilla.org/docs/Web/CSS/backdrop-filter) attribute, background blur cannot be achieved directly through the `div.overlay` CSS rule. Instead, the technique in this example must be used.
:::



## performance risk


Because the blur effect is computationally intensive, developers need to pay special attention to its performance burden. We recommend using blur effects only in static interfaces, and preferably also adding the [`quiescent`](/framework/generic/properties.md#quiescent) attribute to the elements that need to be blurred.


If possible, the interface with obfuscation should be tested on a physical device to see if it meets performance expectations.