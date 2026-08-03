# Cross-device adaptation


When your application needs to run on multiple device vendors, you may encounter a variety of cross-compatibility issues, such as:
- Different devices have different screen resolutions and sizes, and applications should be appropriately laid out and scaled on different devices;
- The system fonts and font sizes of different devices are different, and the application should follow the system style;
- Interface layout should consider different screen shapes. For example, circular screens often use a list of fisheye deformations;
- The safe margins of the page may be different under different screen shapes and screen resolutions.


This document describes how to use the Glyphix application framework to develop watch applications compatible with a wide range of devices while writing less adaptation code.


## Simulator parameters


When using the `gx emu` command to start the emulator, the `-d` or `--device` parameter can specify the device to be simulated. For example, `gx emu -d default-watch-466x466` will emulate a round screen device with a resolution of $466\times 466$ pixels. `gx emu` will remember the last device specified by `-d` instead of automatically falling back to the default device.


::: tip

If you have installed the PowerShell or Zsh completion script for the gx command, you can complete available device names through the `Tab` key after typing `gx emu -d`. Otherwise please use `gx list device` to view the device list first, for example:
``` bash
$ gx list device
default-watch-466x466
default
```
:::



By default, the emulator's screen resolution is the same as the actual device's, you can pass the `-r` or `--real-scale` parameter ( `gx emu -r` ) to simulate the device's actual screen size instead of the resolution. It is not recommended to use the `-r` parameter on non-high-resolution displays, as it will cause the display to be too blurry.


Through the `-d` and `-r` parameters, you can use the simulator to test the display effects of multiple devices without having to prepare physical devices.


## Multi-resolution adaptation


In web development, developers often rely on media queries and units like `px` for fine-grained layout and style adjustments. However, on wearable devices, the optimal font sizes for different devices vary greatly, making it difficult to plan accurately during development. More importantly, how to ensure consistent readability and operating experience for all applications on a device through unified visual specifications is one of the core issues in wearable device UI design.


Taking a smart watch as an example, the screen width of different devices may range from $360\rm px$ to $466\rm px$, while the height ranges from about $450\rm px$ to $500\rm px$. Therefore, despite the existence of [`designWidth`](manifest.md#designwidth) configuration, the dimensions of most interface elements cannot generally be specified in `px` units. No matter how you scale, `px` units always have these problems:
- The DPI or size of the device is different, and the ideal font size cannot be obtained through a fixed pixel size;
- The large difference in aspect ratio between circular and rectangular screens makes it difficult to specify large filling gaps through pixel values.


This section introduces layout techniques to address these issues.


### Font size specifications


Please refer to the [`rem` font size unit](font-config.md#rem-字号单位) guidelines of the font specification to standardize font sizes in your application, **Do not** use `px` as the font size unit.


### Margin configuration


You can use any [length](/framework/render/style-and-layout.md#长度) unit such as `px` to specify smaller margin values, for example:


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



Except for `font-size` which uses `rem`, several other attributes use `px` units. This is because Glyphix automatically scales `px` units for the target device, and smaller `px` values ​​usually have no risk of overflow or clipping.


But when the size value is large, it is more recommended to use a percentage value, for example:


``` css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  /* Use percentage units for left padding, please note the margin to the left of the example text */
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



This allows for better adaptation to devices with widely different resolutions.


::: warning

The screen heights of watch devices vary greatly, and large margins in the vertical direction require more attention to compatibility issues.
:::



### flex layout


In addition to percentage length units, flex layout can provide more flexible interface adaptability. Flex layout should be used first, then percentage length units. And manual layout, i.e. directly specifying the `width` and `height` CSS properties of the element, should be avoided.


One exception where manual layout should be done is for interfaces that display network icons, for example:
``` html
<scroll>
  <div class="item" for="item in items">
    <image :src="item.icon" />
    <p>{{ item.title }}</p>
  </div>
</scroll>
```
If the size of the image pointed to by `item.icon` is not fixed, then it would be more beautiful to specify the appropriate width and height for the `image` element, for example:
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
  object-fit: fill; /* Stretch or scale the image if necessary */
}

/* The text in item occupies the remaining space on the line */
.item > p {
  flex: 1;
}
```


Since the [`image`](/components/image.md) component automatically displays the image in the center, you don't have to worry about the difference in aspect ratio of the image.


### media inquiries


When any layout strategy cannot adapt to the difference in resolution, you can also use [media inquiries](/framework/render/media-query.md) to make targeted adjustments.


## Screen shape adaptation


Smartwatches usually come in two screen shapes, round and rectangular. Among them, large safety margins need to be left at the four corners of the circular screen, and a fisheye effect may be used.


### media inquiries


Taking the top bar as an example, a circular screen may require the top bar text to be center-aligned, while a rectangular screen may require the top bar text to be left-aligned. The following example shows the layout differences for the two screen shapes.


<glyphix id="circle-square-screens" height="400" width="800" title="异形屏幕布局">


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
  /* The left and right sides of a circular screen are usually left blank to improve the display */
  padding: 0 48px;
}

.square-screen > p {
}

.circle-screen > p {
  text-align: center;
}
```


</glyphix>



The two screen shapes can be processed separately through the [`shape`](/framework/render/media-query.md#shape) attribute of media queries, for example:
``` css
.title {
  font-size: 1.25rem;
  color: #353535;
  /* By default, the title is simply surrounded by a safe margin of 32px. */
  margin: 32px;
}

/* These style rules only take effect for round screens. */
@media (shape: circle) {
  .title {
    /* On round screens, title text should be centered. Other properties are inherited from the .title rule above. */
    text-align: center;
  }
}
```
This CSS code first defines the style rules for square screens and then overrides them in a media query block to apply to round screens.


### template macro


Use media queries to define CSS rules for different types of devices, and combine [template macro](/framework/component/template-macro.md) and [`media-query` attribute](/framework/render/media-query.md#组件的-media-query-属性) to apply different UX template structures for different devices. This technology can automatically add a fisheye distortion effect to list interfaces on round devices.


Please refer to chapter [template macro](/framework/component/template-macro.md) for specific usage methods.


## JavaScript adaptation


If you need to write different logic for different devices, you can also get [Device information](/api/system-device.md). For example, you can get the device's screen shape enumeration value at runtime through [`device.screenShape`](/api/system-device.md#screenshape).