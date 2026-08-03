# Style and layout


Glyphix's style system is similar to CSS in web technology. CSS is usually defined directly within the `<style>` tag of the UX file.


## Writing CSS


You can write CSS inside the `<style>` tag:


``` html
<style>
  div { display: flex; }
</style>
```


CSS files can be imported using the `@import` command:


``` html
<style>
  @import 'style.css';
  div { display: flex; }
</style>
```


Glyphix also provides limited support for inline styles, which are written directly in the component's style attribute:
``` html
<div style="background: #f00; color: #fff"> ... </div>
```
The value of an inline style is a string, and you can update the style by changing this string. Support for [CSS properties](/framework/generic/styles.md) used in inline styles adds the <badge type="info" text="内联" /> tag.


::: warning

The current version of inline styles is inefficient and should only be used as a solution for js logic to update component styles. Extensive use may cause performance issues. Generally you should use the scheme of defining CSS rules in the `<style>` tag.
:::



## style selector


Currently, the styling framework supports the following selectors:


- class selector
- type selector
- id selector
- Pseudo class (rarely used)
- Pseudo elements (rarely used)
- Descendant selectors and direct descendant selectors, such as `div >.title` or `div.title`
- Compound selector, such as `#id.class` or `div.class`


### class selector


The class selector selects components with corresponding class attributes. Components can have multiple class values, such as
``` html
<p class="ceil content">...</p>
```
Will match the following two style definitions:
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


### Combination selector


Supports specifying multiple selectors for rule-set using `,`:
``` css
#id, .class, div {
  display: flex;
  flex-direction: column;
  color: red;
}
```


### Inherited properties


Some CSS properties can be inherited from parent elements to child elements, taking `font-size` as an example:
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
Even though the `font-size` attribute is not set on the `<p>` element, it still displays the font size of `1.25rem` because the `<p>` element inherits the font size setting from its parent `<div>`. In other words, after setting an inheritable style attribute in a container, all child elements will also get the attribute setting. But please note that the priority of the CSS property inheritance mechanism is very low. The inherited value will only be used when the element does not specify an inherited style attribute. Assume the following CSS is used for the example above:
``` css
* {
  font-size: 1rem;
}
div {
  font-size: 1.25rem;
}
```
Due to the `*` regular style block, the font size of the `<p>` element will now be `1rem` instead of taking the inherited value.


In [CSS properties](/framework/generic/styles.md) documents, properties that support inheritance have the <badge type="info" text="继承" /> tag added.


### Responsive support


Currently, neither the `class` attribute nor the `id` attribute supports reactivity, so
``` html
<div class="{{expr}}" id="{{expr}}"> ... </div>
```
Neither is supported, only static `class` and `id` attribute values ​​can be written directly.


::: warning

Developers should pay attention to the limitation that `class` and `id` do not support responsive attributes!
:::



## color value


### color code


Color values ​​support RGB or RGBA color codes starting with `#` characters. Legal color codes are:


- `#RRGGBB[AA]`, such as `#102000`, `#00ff0080`
- `#RGB[A]`, such as `#0f0`, `#ff08`


If the color code does not contain an alpha channel, the value of that channel is `ff` (`#RRGGBB` format) or `f` (`#RGB` format). Each bit in the color code is a hexadecimal number, and the available characters are `0-9`, `A-F`, and `a-f`. `#RGB[A]` is a shorthand method for `#RRGGBB[AA]` code, for example, `#0f38` has the same color as `#00ff3388`.


### color function


Currently, the `rgb()` and `rgba()` functions are supported for defining color values ​​in CSS blocks. HSL color format is not supported.


### Standard color name


You can use web-standard color names in CSS blocks, for example:
``` css
color: brown;
color: lightgray;
```


### Color in inline styles


Only color codes starting with `#` are supported in inline styles, for example:
``` html
<p style="color: #ff00ff">...</p> <!-- support -->
<p style="color: gray">...</p> <!-- Not supported, cannot be parsed -->
```


## length


The general format of the length value is `<value><unit>`, `value` is the numerical value of the length, and `unit` is the length unit, such as `15px`. No space should be added between `value` and `unit`.


A special length value `auto` is also supported. This length value has no specific value or unit. The length in actual rendering is determined by specific scenes and rules.


The following length units are available:


- `px`: Use pixels as the length unit
- `pt`: Use pounds as the unit of length, one pound is $1/72$ inch
- `%`: Percent length unit. The specific value will have different conversion relationships depending on the attributes and layout.
- [`rem`](/framework/application/font-config.md#rem-字号单位): The length unit relative to the system default font size, for example, `1rem` is equal to the size of the system default font size, $ 1.5 \rm rem$ is $ 1.5 $ times of the former


where `pt` is an absolute unit of length, for example `72pt` corresponds to $1''$ (inches) or $ 25.4 \rm mm$, regardless of the device. `px` is related to the device, but does not directly correspond to physical pixels. Please refer to the [`manifest.config.designWidth`](/framework/application/manifest.md#designwidth) field description for its conversion relationship. The percentage length unit is usually calculated relative to the size of the parent element and the element itself. For example, the percentage value of CSS attributes such as `width` and `margin` is calculated based on the size of the parent element, while `border-radius` is calculated based on the size of the element itself.


The `rem` unit is used exclusively for font sizes (that is, the `font-size` attribute), which is a simple scheme for cross-device font consistency. Please refer to [`rem` font size unit](/framework/application/font-config.md#rem-字号单位) for more instructions.


## layout


The layout framework can automatically arrange elements based on the interface content and the geometric information of the screen. Developers do not need to manually specify the position and size of elements. Layout frameworks are a powerful mechanism for adapting interfaces to devices of different resolutions or sizes, as well as handling changing content. Most of Glyphix's native components support two automatic layout modes: flow layout and flexbox layout, and also support manual layout. Some native components have special layouts that are enforced. For example, the [`swiper`](/components/swiper.md) component's child elements are always as large as the viewport, while the [`stack`](/components/stack.md) component is designed entirely to provide a stacked layout.


The concepts of fluid layout and flexbox layout come from web standards, but are adapted for low-performance devices.


## media inquiries


In CSS, [media inquiries](media-query.md) is mainly used to control CSS styles according to specific devices or media types through [`@media` rules](media-query.md#css-media-规则). Please refer to relevant [document](media-query.md) for specific details regarding media inquiries.


## Less extension


If you want to use [less](https://lesscss.org/) as a CSS preprocessor, first install the `less` package via a [Package manager](/tutorials/nodejs.md) one:


::: code-tabs

@tab npm

```bash
npm install -D less
```


@tab pnpm

```bash
pnpm i -D less

@tab yarn
```bash
yarn add -D less

```
:::

::: tip
全局安装的 `less`（如 `npm install -g less`）不会被 Glyphix 打包工具识别，因此必须使用上面的方法在项目中安装 `less` 包。
:::

然后，你将可以在 UX 文件的 `<style>` 标签中使用 `lang="less"` 属性来指定样式类型：

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