# Cross-Device Adaptation

When your application needs to run on multiple types of devices, you may encounter various interaction compatibility issues. For example:
- Different devices have different screen resolutions and sizes, so applications should layout and scale appropriately across them;
- System fonts and font sizes vary across devices, and applications should adhere to the system style;
- Interface layouts must account for different screen shapes, such as circular screens often using fisheye-warped lists;
- Safe margins of pages may differ under different screen shapes and resolutions.

This document introduces how to develop watch applications compatible with a wide range of devices using the Glyphix application framework with minimal adaptation code.

## Simulator Parameters

When starting the simulator using the `gx emu` command, the `-d` or `--device` parameter can specify the simulated device. For example, `gx emu -d default-watch-466x466` will simulate a circular screen device with a resolution of $466\times 466$ pixels. `gx emu` will remember the device specified by the last `-d` instead of automatically falling back to the default device.

::: tip
If you have installed the PowerShell or Zsh completion script for the `gx` command, typing `gx emu -d` allows you to tab-complete available device names using the `Tab` key. Otherwise, please use `gx list device` first to view the device list, for example:
``` bash
$ gx list device
default-watch-466x466
default
```
:::

By default, the simulator's screen resolution is the same as the actual device. You can use the `-r` or `--real-scale` parameter (`gx emu -r`) to simulate the device's actual physical screen size rather than its resolution. It is not recommended to use the `-r` parameter on non-high-resolution displays, as it will cause the display to appear overly blurry.

Using the `-d` and `-r` parameters allows you to test the display effects of multiple devices through the simulator without needing physical devices.

## Multi-Resolution Adaptation

In Web development, developers usually rely on media queries and units like `px` for fine-grained layout and style adjustments. However, on wearable devices, the optimal font sizes vary too greatly between devices to be precisely planned during development. More importantly, ensuring consistent readability and operational experience for all applications on a device through a unified visual specification is one of the core issues in wearable UI design.

Taking smartwatches as an example, the screen width of different devices may range between $360\rm px$ and $466\rm px$, while the height ranges between $450\rm px$ and $500\rm px$ or so. Therefore, despite the existence of the [`designWidth`](manifest.md#designwidth) configuration, you generally cannot specify the sizes of most interface elements using `px` units. No matter how it is scaled, the `px` unit always presents these problems:
- Different device DPIs or sizes make it impossible to achieve ideal font sizes through fixed pixel dimensions;
- The large aspect ratio differences between circular and rectangular screens make it difficult to specify large padding gaps using pixel values.

This section will introduce layout techniques for addressing these issues.

### Font Size Specification

Please refer to the [`rem` Font Size Units](font-config.md#rem-字号单位) guide in the font specifications to standardize font sizes in your application. **Do not** use `px` as a font size unit.

### Margin Configuration

You can use `px` or any other [length](/framework/render/style-and-layout.md#长度) units to specify smaller margin values, for example:

``` css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  padding: 8px; /* Use px as margin unit */
  margin: 8px;
}
```

<glyphix id="font-config-margins-pixel" height="80" width="300" inline>

```html
<p>The message text.</p>
```

```css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  padding: 8px;
  margin: 8px;
}
```

</glyphix>

Except for `font-size` which uses `rem`, the other properties use `px` units. This is because Glyphix automatically scales the proportion of `px` units for the target device, and smaller `px` values typically carry no risk of overflow or clipping.

However, when size values are large, it is recommended to use percentage values instead, for example:

``` css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  /* Use percentage unit for left padding, please note the margin on the left side of the sample text */
  padding: 8px 8px 8px 40%;
}
```

<glyphix id="font-config-margins-percent" height="80" width="300" inline>

```html
<p>Message</p>
```

```css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  padding: 8px 8px 8px 40%;
}
```

</glyphix>

This allows better adaptation to devices with vastly different resolutions.

::: warning
Watch device screen heights vary significantly, and large vertical margins require greater attention to compatibility issues.
:::

### Flex Layout

In addition to percentage length units, flex layout provides more flexible interface adaptability. Flex layout should be prioritized over percentage length units. Manual layout—directly specifying the `width` and `height` CSS properties of elements—should be avoided.

An exception where manual layout should be used is an interface displaying network icons, for example:
``` html
<scroll>
  <div class="item" for="item in items">
    <image :src="item.icon" />
    <p>{{ item.title }}</p>
  </div>
</scroll>
```
If the image size pointed to by `item.icon` is not fixed, specifying appropriate width and height for the `image` element will look better, for example:
``` css
scroll {
  display: flex;
  flex-direction: column;
}

.item {
  display: flex;
}

/* Specify fixed width and height for network icons */
.item > image {
  width: 92px;
  height: 92px;
  border-radius: 10px;
  object-fit: fill; /* Stretch or scale image when necessary */
}

/* Text in item takes up remaining space in the row */
.item > p {
  flex: 1;
}
```

Since the [`image`](/components/image.md) component automatically centers images, you don't need to worry about differences in image aspect ratios.

### Media Queries

When no layout strategy can accommodate resolution differences, [media queries](/framework/render/media-query.md) can also be used for targeted adjustments.

## Screen Shape Adaptation

Smartwatches typically come in two screen shapes: circular and rectangular. Circular screens require larger safe margins in the four corners and may use fisheye-effect lists.

### Media Queries

Taking the top bar as an example, circular screens may require the top bar text to be center-aligned, whereas rectangular screen top bar text is left-aligned. The following example demonstrates the layout differences corresponding to the two screen shapes.

<glyphix id="circle-square-screens" height="400" width="800" title="Non-Standard Screen Layout">

```html
<div class="screens">
  <div class="square-screen">
    <p>TITLE BAR</p>
  </div>
  <div class="circle-screen">
    <p>TITLE BAR</p>
  </div>
</div>
```

```css
p {
  font-size: 1.25rem;
  color: #353535;
  margin: 32px;
}

.screens {
  display: flex;
}

.screens > div {
  display: flex;
  flex-direction: column;
  background-color: #adb5bd;
  flex: 1;
  margin: 10px;
}

.square-screen {
  border-radius: 10%;
}

.circle-screen {
  border-radius: 50%;
  /* Left and right sides of circular screens are usually left blank to improve display effects */
  padding: 0 48px;
}

.square-screen > p {
}

.circle-screen > p {
  text-align: center;
}
```

</glyphix>

You can use the [`shape`](/framework/render/media-query.md#shape) feature of media queries to handle the two screen shapes respectively, for example:
``` css
.title {
  font-size: 1.25rem;
  color: #353535;
  /* By default, the title simply leaves a 32px safe margin around it. */
  margin: 32px;
}

/* These style rules only apply to circular screens. */
@media (shape: circle) {
  .title {
    /* On circular screens, the title text should be centered. Other properties are inherited from the .title rule above. */
    text-align: center;
  }
}
```
This CSS code first defines the style rules for square screens and then overrides them for circular screens within a media query block.

### Template Macros

While media queries can be used to define CSS rules for different types of devices, combining [template macros](/framework/component/template-macro.md) with the [`media-query` attribute](/framework/render/media-query.md#组件的-media-query-属性) allows applying different UX template structures to different devices. This technique can automatically add fisheye warping effects to list interfaces on circular devices.

For specific usage methods, please refer to the [Template Macros](/framework/component/template-macro.md) section.

## JavaScript Adaptation

If you need to write different logic for different devices, you can also retrieve [device information](/api/system-device.md). For example, you can get the screen shape enumeration value of the device at runtime via [`device.screenShape`](/api/system-device.md#screenshape).