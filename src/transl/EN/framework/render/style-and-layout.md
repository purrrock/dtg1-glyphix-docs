# Styles and Layout

The styling system in Glyphix is similar to CSS in web technologies. Typically, CSS is defined directly inside the `<style>` tag of a UX file.

## Writing CSS

You can write CSS inside the `<style>` tag:

``` html
<style>
  div { display: flex; }
</style>
```

You can use the `@import` command to import CSS files:

``` html
<style>
  @import 'style.css';
  div { display: flex; }
</style>
```

Glyphix also provides limited support for inline styles, which are written directly in the `style` attribute of a component:
``` html
<div style="background: #f00; color: #fff"> ... </div>
```
The value of an inline style is a string, and you can update the styles by changing this string. [CSS properties](/framework/generic/styles.md) that support being used in inline styles are tagged with <badge type="info" text="Inline" />.

::: warning
Inline styles in the current version are relatively inefficient and should only be used as a solution for updating component styles via JS logic. Heavy usage may cause performance issues. In general, you should use CSS rules defined within the `<style>` tag.
:::

## Style Selectors

Currently, the styling framework supports the following selectors:

- Class selector
- Type selector
- ID selector
- Pseudo-class (rarely used)
- Pseudo-element (rarely used)
- Descendant selector and direct descendant selector, such as `div > .title` or `div .title`
- Compound selector, such as `#id.class` or `div.class`

### Class Selector

A class selector selects components with the corresponding `class` attribute. A component can have multiple class values, for example:
``` html
<p class="ceil content">...</p>
```
This will match the following two style definitions:
``` css
.ceil {
  background-color: #222;
  border-radius: 12px;
}

.content {
  font-size: 24px;
  padding: 12px;
}
```

### Grouping Selectors

You can use `,` to specify multiple selectors for a rule-set:
``` css
#id, .class, div {
  display: flex;
  flex-direction: column;
  color: red;
}
```

### Inherited Properties

Certain CSS properties can be inherited from parent elements down to child elements. Taking `font-size` as an example:
``` html
<div>
  <p>Text</p>
</div>
```

``` css
div {
  font-size: 1.25rem;
}
```
Even though the `font-size` property is not explicitly set on the `<p>` element, it will still display with a font size of `1.25rem`. This is because the `<p>` element inherits the font size setting from its parent `<div>`. In other words, once an inheritable style property is set on a container, all child elements will also inherit that property setting. However, note that the priority of the CSS property inheritance mechanism is very low, and inherited values are only used when the element has no specified style property of its own. Suppose the following CSS is applied to the example above:
``` css
* {
  font-size: 1rem;
}
div {
  font-size: 1.25rem;
}
```
Due to the presence of the `*` rule style block, the `<p>` element's font size will now be `1rem` instead of using the inherited value.

In the [CSS Properties](/framework/generic/styles.md) documentation, properties that support inheritance are tagged with <badge type="info" text="Inherited" />.

### Reactive Support

Currently, neither the `class` attribute nor the `id` attribute supports reactivity. Therefore:
``` html
<div class="{{expr}}" id="{{expr}}"> ... </div>
```
Neither of these is supported; you can only write static `class` and `id` attribute values directly.

::: warning
Developers must be aware of the limitation that `class` and `id` do not support reactive properties!
:::

## Color Values

### Color Codes

Color values support RGB or RGBA color codes starting with the `#` character. Valid color codes include:

- `#RRGGBB[AA]`, for example, `#102000`, `#00ff0080`
- `#RGB[A]`, for example, `#0f0`, `#ff08`

If a color code does not contain an alpha channel, its value defaults to `ff` (for `#RRGGBB` format) or `f` (for `#RGB` format). Each digit in a color code is a hexadecimal number, with available characters being `0-9`, `A-F`, and `a-f`. `#RGB[A]` is a shorthand method for `#RRGGBB[AA]` codes; for example, the color `#0f38` is identical to `#00ff3388`.

### Color Functions

Currently, CSS blocks support defining color values using the `rgb()` and `rgba()` functions. HSL color formats are not supported.

### Standard Color Names

You can use standard web color names within CSS blocks, for example:
``` css
color: brown;
color: lightgray;
```

### Colors in Inline Styles

Inline styles only support color codes starting with `#`, for example:
``` html
<p style="color: #ff00ff">...</p> <!-- Supported -->
<p style="color: gray">...</p> <!-- Not supported, cannot be parsed -->
```

## Lengths

The general format for length values is `<value><unit>`, where `value` is the numeric value of the length, and `unit` is the length unit, such as `15px`. There should be no space between `value` and `unit`.

A special length value `auto` is also supported. This length value has no specific numerical value or unit, and its actual rendered length is determined by the specific scenario and rules.

The following length units are available:

- `px`: Pixels as the length unit
- `pt`: Points as the length unit, where one point is $1/72$ of an inch
- `%`: Percentage length unit; the specific value varies in conversion relation depending on the property and layout
- [`rem`](/framework/application/font-config.md#rem-字号单位): Length unit relative to the system default font size, for example, `1rem` equals the size of the system default font, and $1.5\rm rem$ is $1.5$ times the former.

Among them, `pt` is an absolute length unit—for example, `72pt` corresponds to $1''$ (inch) or $25.4\rm mm$—which is device-independent. On the other hand, `px` is device-dependent, though it does not directly correspond to physical pixels; please refer to the [`manifest.config.designWidth`](/framework/application/manifest.md#designwidth) field description for conversion relations. Percentage length units are usually calculated relative to the dimensions of the parent element or the element itself; for example, percentage values for CSS properties like `width` and `margin` are calculated based on the parent element's dimensions, while `border-radius` is calculated based on the element's own dimensions.

The `rem` unit is specifically used for font sizes (i.e., the `font-size` property), serving as a simple cross-device font consistency solution. For more details, please refer to the [`rem` Font Size Unit](/framework/application/font-config.md#rem-字号单位).

## Layout

The layout framework can automatically arrange elements based on interface content and screen geometry information, eliminating the need for developers to manually specify element positions and sizes. The layout framework is a powerful mechanism that allows interfaces to adapt to devices of varying resolutions or sizes, while also handling dynamic content. Most native Glyphix components support two automatic layout modes: flow layout and flexbox layout, while also supporting manual layout. Certain native components have enforced special layouts; for example, the children of the [`swiper`](/components/swiper.md) component are always as large as the viewport, whereas the [`stack`](/components/stack.md) component is designed entirely to provide a stacking layout.

The concepts of flow layout and flexbox layout originate from web standards, but have been adjusted for low-performance devices.

## Media Queries

In CSS, [media queries](media-query.md) are primarily used via [`@media` rules](media-query.md#css-media-规则) to control CSS styles based on specific device or media types. For specific details regarding media queries, please refer to the relevant [documentation](media-query.md).

## Less Extensions

If you want to use [less](https://lesscss.org/) as your CSS preprocessor, you must first install the `less` package via a [package manager](/tutorials/nodejs.md):

::: code-tabs
@tab npm
```bash
npm install -D less
```

@tab pnpm
```bash
pnpm i -D less
```

@tab yarn
```bash
yarn add -D less
```
:::

::: tip
Globally installed `less` (such as `npm install -g less`) will not be recognized by the Glyphix bundling tool, so you must install the `less` package within your project using the method above.
:::

You can then use the `lang="less"` attribute in the `<style>` tag of your UX file to specify the style type:

``` html
<style lang="less">
@color: #4D926F;

.header {
  color: @color;
  .nested {
    font-size: 0.75rem;
  }
}
</style>
```