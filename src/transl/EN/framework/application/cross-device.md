# Cross-Device Adaptation

When your application needs to run on multiple types of devices, you may encounter various interaction compatibility issues. For example:
- Different devices have different screen resolutions and sizes, so applications should layout and scale appropriately across different devices;
- Different devices have different system fonts and font sizes, so applications should adhere to the system style;
- Interface layouts must account for different screen shapes, such as circular screens which often use fisheye-distorted lists;
- Safe margins of pages may vary under different screen shapes and resolutions.

This document describes how to use the Glyphix application framework to develop watch applications compatible with a wide range of devices while writing minimal adaptation code.

## Simulator Parameters

When starting the simulator using the `gx emu` command, the `-d` or `--device` parameter can specify the target simulated device. For example, `gx emu -d default-watch-466x466` will simulate a circular screen device with a resolution of $466\times 466$ pixels. `gx emu` will remember the device specified by the last `-d` instead of automatically falling back to the default device.

::: tip
If you have installed the PowerShell or Zsh completion script for the `gx` command, you can press the `Tab` key to autocomplete available device names after typing `gx emu -d`. Otherwise, please use `gx list device` first to view the device list, for example:
``` bash
$ gx list device
default-watch-466x466
default
```
:::

By default, the simulator's screen resolution matches that of the actual device. You can use the `-r` or `--real-scale` parameter (`gx emu -r`) to simulate the actual physical screen size of the device rather than its resolution. It is not recommended to use the `-r` parameter on non-high-resolution displays, as it may cause the display to appear overly blurry.

Using the `-d` and `-r` parameters allows you to test the display effects of various devices through the simulator without needing physical hardware.

## Multi-Resolution Adaptation

In Web development, developers typically rely on media queries and units like `px` for precise layout and style adjustments. However, on wearable devices, the optimal font sizes vary too greatly between different devices, making precise planning during development difficult. More importantly, ensuring consistent readability and operational experience for all applications on a given device through a unified visual specification is one of the core issues in wearable UI design.

Taking smartwatches as an example, the screen width of different devices may range between $360\rm px$ and $466\rm px$, while the height ranges from around $450\rm px$ to $500\rm px$. Therefore, despite the [`designWidth`](manifest.md#designwidth) configuration, it is usually impossible to specify the sizes of most interface elements using `px` units. No matter how it is scaled, the `px` unit always presents these issues:
- Devices have different DPIs or sizes, making it impossible to achieve ideal font sizes through fixed pixel dimensions;
- Circular and rectangular screens have large aspect ratio differences, making it difficult to specify large padding gaps using pixel values.

This section will introduce layout techniques to address these issues.

### Font Size Specifications

Please refer to the [`rem` font size units](font-config.md#rem-字号单位) guide in the font specifications to standardize font sizes in your application. **Do not** use `px` as a font size unit.

### Margin Configuration

You can use `px` or any other [length](/framework/render/style-and-layout.md#长度) unit to specify smaller margin values, for example:

``` css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  padding: 8px; /* Use px as the margin unit */
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

Except for `font-size` which uses `rem`, the other properties use `px` units. This is because Glyphix automatically scales the proportion of `px` units for the target device, and smaller `px` values usually carry no risk of overflow or clipping.

However, when size values are large, it is recommended to use percentage values instead, for example:

``` css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  /* Left padding uses percentage unit, please note the margin on the left side of the sample text */
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
Watch device screen heights vary significantly, and large vertical margins require extra attention regarding compatibility issues.
:::

### Flex Layout

In addition to percentage length units, flex layout provides more flexible interface adaptability. Flex layout should be prioritized over percentage length units. Manual layouts—i.e., directly specifying the `width` and `height` CSS properties of elements—should be avoided.

An exception where manual layout should be used is an interface displaying network icons, for example:
``` html
<scroll>
  <div class="item" for="item in items">
    <image :src="item.icon" />
    <p>{{ item.title }}</p>
  </div>
</scroll>
```
If the image size pointed to by `item.icon` is not fixed, specifying appropriate width and height for the `image` element makes it more aesthetically pleasing, for example:
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
  object-fit: fill; /* Stretch or scale the image when necessary */
}

/* The text in the item occupies the remaining space on the line */
.item > p {
  flex: 1;
}
```

Since the [`image`](/components/image.md) component automatically centers images, you do not need to worry about differences in image aspect ratios.

### Media Queries

When no layout strategy can accommodate resolution differences, you can also use [media queries](/framework/render/media-query.md) to make targeted adjustments.

## Screen Shape Adaptation

Smartwatches typically come in two screen shapes: circular and rectangular. Circular screens require larger safe margins in the four corners and may use fisheye-effect lists.

### Media Queries

Taking the top bar as an example, circular screens may require top bar text to be center-aligned, while rectangular screens have left-aligned top bar text. The following example demonstrates the layout differences corresponding to the two screen shapes.

<glyphix id="circle-square-screens" height="400" width="800" title="Irregular Screen Layout">

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
  /* The left and right sides of circular screens are usually left blank to improve display effects */
  padding: 0 48px;
}

.square-screen > p {
}

.circle-screen > p {
  text-align: center;
}
```

</glyphix>

You can use the [`shape`](/framework/render/media-query.md#shape) feature of media queries to handle the two screen shapes separately, for example:
``` css
.title {
  font-size: 1.25rem;
  color: #353535;
  /* By default, the title simply leaves a 32px safe margin around all sides. */
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
This CSS code first defines style rules for square screens, and then overrides them in a media query block for rules applicable to circular screens.

### Template Macros

While media queries can define CSS rules for different types of devices, combining [template macros](/framework/component/template-macro.md) with the [`media-query` attribute](/framework/render/media-query.md#组件的-media-query-属性) allows applying different UX template structures for different devices. This technique can automatically add fisheye distortion effects to list interfaces on circular devices.

For specific usage methods, please refer to the [Template Macros](/framework/component/template-macro.md) section.

## JavaScript Adaptation

If you need to write different logic for different devices, you can also retrieve [device information](/api/system-device.md). For example, you can obtain the screen shape enum value of the device at runtime via [`device.screenShape`](/api/system-device.md#screenshape).