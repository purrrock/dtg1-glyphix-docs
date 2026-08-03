# Font specifications


There are some system fonts built into the Glyphix framework, and applications can also define their own fonts.


## System level fonts


These system fonts are guaranteed to be available in all environments running Glyphix:
- `sans-serif`: Default sans serif font.


The actual font files provided by different devices may differ, but these font names are always available.


### Default font


If an interface element does not specify all font properties (font family, font size, etc.), the remaining properties will use system default values. Therefore, when an interface element does not have any font attribute, the system default font will be used. Default font properties are device-specified and have the following properties:
- [`font-family`](/framework/generic/styles.md#font-family) is `sans-serif`;
- [`font-size`](/framework/generic/styles.md#font-size) is `1rem`.


### Glyph fallback issue


Due to device performance limitations, complete fonts for all languages ​​and character sets cannot be preinstalled. We will only provide "primary fonts" for a specific language, which typically include common letters, numbers, and symbols. However, if you try to use uncommon characters, special symbols, or characters that are not included in these major fonts, a "glyph fallback" phenomenon will occur.


When a character cannot be rendered by a currently supported font, it will fall back to being displayed as a "box". For example, this is the effect of displaying the text "Hello, World." in the Roboto font that does not support Chinese:


<glyphix id="font-config-fallback" height="30" width="300" inline>



```html
<p>Hello, 世界。</p>
```


</glyphix>



The three characters "world." are not supported, so they are rendered as three boxes.


## application-grade fonts


### font mapping file


The [`manifest.config.fontFaces`](manifest.md#fontfaces) field configures the application-level font mapping file. This is a CSS file containing only [`@font-face` rules](/framework/generic/styles.md#font-face-规则), and the fonts defined in it can be used directly in this application without referencing the CSS file.


Assume that the path of the font mapping file in the project is `src/assets/font-faces.css`, then the `manifest.config.fontFaces` field needs to be filled in as
``` json
{
  "config": {
    "fontFaces": "assets/font-faces.css"
  }
}
```
The following is an example of the contents of a `src/assets/font-faces.css` file
``` css
@font-face {
  font-family: Montserrat;
  src: url("fonts/Montserrat-Regular.ttf");
  font-weight: 400;
  font-style: normal;
}
```
Other CSS files can also be imported through the `@import` rule, but only the `@font-face` rule information will be retained in the font mapping file.


### `@font-face` Rules


You can also use [`@font-face` rules](/framework/generic/styles.md#font-face-规则) directly in CSS to define and use fonts. This approach is similar to the general web development process.


::: tip

Compared to defining fonts in individual CSS, application-level fonts defined in font mapping files run more efficiently and should be used in preference.
:::



### When to use application-level fonts


For devices with limited performance and resources, the default font provided by the system has lower resource usage and better performance, and developers should give priority to using it. Application-level fonts are only recommended for specific needs. Here are the specific guidelines:
- **Prefer system-level fonts**: System-level fonts are optimized to reduce storage usage and processing overhead. In most cases, they can meet the needs of ordinary text display, such as menus, home pages, descriptive text, etc.
- **Use custom fonts for specific design needs**: If the application needs to meet specific visual design style or brand requirements, you can use custom fonts. For example, the application may want to display a digital clock with a unique style, or emphasize text in certain titles and buttons. Using custom fonts can achieve an effect that is more in line with the design language.
- **Custom fonts should have a compact character set**: To avoid unnecessary storage and processing overhead, custom fonts should have a compact character set as much as possible. Typically, only Latin letters, numbers, and necessary punctuation are required. For example, when designing a digital clock, the custom font should contain only the numeric characters $0 \sim 9$.


::: warning

Do not use large font files (such as Chinese fonts) in your application. Large font file sizes can pose serious performance and resource risks. Typically, system-level fonts already include the character support required for the current language, and there is no need to supplement the character set with custom fonts.
:::



## `rem` font size unit


In order to achieve a consistent font style with the system on different devices, we introduced the `rem` unit, which is slightly different from web development. `1rem` is the system text size defined by the device manufacturer. When the [`font-size`](/framework/generic/styles.md#font-size) attribute is not defined in CSS, the default font size of the element is `1rem`. There is no fixed conversion relationship between `rem` and `px` or `pt` and other [length](/framework/render/style-and-layout.md#长度) units. Font sizes of `1rem` usually correspond to around `24px` to `32px`.


Using `rem` as the font size unit ensures consistent display across all applications in the system. **Don't** use units such as `px` to set the font size, otherwise it may not work across devices. Specifically, the following configuration is recommended:
- **Title** uses `1.25rem` font size. For multi-level titles, you can choose other font sizes appropriately;
- **Text** uses the default font size, which is `1rem`, and generally do not specify this font size explicitly;
- **Footnotes** use `0.85rem` font size.


It is recommended that developers select a small and fixed font size range and use our recommended font sizes in the above $3$ scenarios.