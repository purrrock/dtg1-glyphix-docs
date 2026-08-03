# Font Specifications

The Glyphix framework comes with built-in system fonts, and applications can also define their own custom fonts.

## System-Level Fonts

These system fonts are guaranteed to be provided in all environments where Glyphix runs:
- `sans-serif`: The default sans-serif font.

Different devices may provide different actual font files, but these font names are always available.

### Default Font

If a UI element does not specify all font properties (font family, font size, etc.), the remaining properties will use system defaults. Therefore, when a UI element has no font properties specified, the default system font is used. The default font properties are specified by the device and have the following values:
- [`font-family`](/framework/generic/styles.md#font-family) is `sans-serif`;
- [`font-size`](/framework/generic/styles.md#font-size) is `1rem`.

### Glyph Fallback Issue

Due to device performance limitations, it is not possible to pre-install complete fonts for all languages and character sets. We only provide "primary fonts" for specific languages, which typically include common letters, numbers, and symbols. However, if you attempt to use uncommon characters, special symbols, or characters not included in these primary fonts, a "glyph fallback" phenomenon will occur.

When a character cannot be rendered by the currently supported font, it falls back to display as a "box". For example, here is the effect of displaying the text "Hello, 世界。" using the Roboto font, which does not support Chinese:

<glyphix id="font-config-fallback" height="30" width="300" inline>

```html
<p>Hello, 世界。</p>
```

</glyphix>

Here, the three characters "世界。" are not supported and are therefore rendered as three boxes.

## Application-Level Fonts

### Font Mapping File

The [`manifest.config.fontFaces`](manifest.md#fontfaces) field can be used to configure application-level font mapping files. This is a CSS file containing only [`@font-face` rules](/framework/generic/styles.md#font-face-rules). Fonts defined in this file can be used directly within the application without needing to reference the CSS file.

Assuming the font mapping file is located at `src/assets/font-faces.css` in the project, the `manifest.config.fontFaces` field should be configured as follows:
``` json
{
  "config": {
    "fontFaces": "assets/font-faces.css"
  }
}
```
Below is an example of the contents of the `src/assets/font-faces.css` file:
``` css
@font-face {
  font-family: Montserrat;
  src: url("fonts/Montserrat-Regular.ttf");
  font-weight: 400;
  font-style: normal;
}
```
Other CSS files can also be imported via `@import` rules, but only `@font-face` rule information will be retained in the font mapping file.

### `@font-face` Rules

You can also define and use fonts directly in CSS using [`@font-face` rules](/framework/generic/styles.md#font-face-rules). This approach is similar to standard web development workflows.

::: tip
Compared to defining fonts in individual CSS files, application-level fonts defined in the font mapping file run more efficiently and should be preferred.
:::

### When to Use Application-Level Fonts

For performance- and resource-constrained devices, the default fonts provided by the system have a lower resource footprint and better performance, and developers should prioritize using them. Application-level fonts are recommended only for specific requirements. Here are the specific guidelines:
- **Prioritize system-level fonts**: System-level fonts are optimized to reduce storage footprint and processing overhead. They can meet the needs of ordinary text display in most cases, such as menus, main pages, and descriptive text.
- **Use custom fonts for specific design requirements**: If an application needs to comply with a specific visual design style or brand requirement, custom fonts can be used. For example, an application may need to display a digital clock with a unique style, or emphasize text in certain titles and buttons; using custom fonts can achieve results that better match the design language.
- **Custom fonts should have a streamlined character set**: To avoid unnecessary storage and processing overhead, the character set of a custom font should be kept as lean as possible. Generally, it only needs to include Latin letters, numbers, and necessary punctuation marks. For example, when designing a digital clock, the custom font should only contain the numeric characters $0 \sim 9$.

::: warning
Do not use large font files (such as Chinese fonts) in your application. Large font files can introduce severe performance and resource risks. Typically, system-level fonts already include the character support required for the current language, eliminating the need to supplement the character set with custom fonts.
:::

## `rem` Font Size Unit

To achieve a font style consistent with the system across different devices, we introduce the `rem` unit, which is slightly different from web development. `1rem` is the system body font size defined by the device vendor. When the [`font-size`](/framework/generic/styles.md#font-size) property is not defined in CSS, the default font size of an element is `1rem`. There is no fixed conversion relationship between `rem` and [length](/framework/render/style-and-layout.md#长度) units such as `px` or `pt`. A font size of `1rem` typically corresponds to around `24px` to `32px`.

Using `rem` as the font size unit ensures consistent rendering of all applications in the system. **Do not** use units like `px` to set font sizes, otherwise, they may fail to work properly across devices. Specifically, the following configurations are recommended:
- **Headings** should use a `1.25rem` font size, and multi-level headings can choose other appropriate font sizes;
- **Body text** should use the default font size, which is `1rem`, and generally should not have this font size explicitly specified;
- **Footnotes** should use a `0.85rem` font size.

Developers are advised to choose a small, fixed set of font size tiers and use our recommended font sizes in the $3$ scenarios mentioned above.