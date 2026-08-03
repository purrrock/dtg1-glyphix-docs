# div

`div` is the most basic container component. `div` supports child components and layout, but does not support scrolling (content exceeding the boundaries will be clipped directly). If you want content to scroll, please use the [scroll](scroll) component.

## Notes

### Text Display

The `div` component cannot be used to display text directly; instead, text components such as `p` must be used. For example:

```html
<!-- Incorrect usage, text will not be displayed -->
<div>text content.</div>
<!-- Correct usage -->
<p>text content.</p>
```

However, if there are multiple child elements inside the `div`, text can be included as its child element:

```html
<div>
  first element,
  <span style="color: #f0f">second element.</span>
</div>
```

<Glyphix id="components-div-text-element" height="48" width="360" inline >

```html
<div>
  first element,
  <span style="color: #f0f">second element.</span>
</div>
```

</Glyphix>