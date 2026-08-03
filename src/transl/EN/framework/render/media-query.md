# Media Queries

Media queries allow developers to use different styles for different device types. Currently, media queries support CSS `@media` rules, but do not yet support the `media` attribute of components.

## CSS `@media` Rules

The syntax for the `@media` rule is:
``` css
@media <query> {
  <css-rules>
}
```
[`<query>`](#query-conditions) is used to query media types and media features, and can be combined using various logical operators. When the media query condition is met, the CSS rules within `<css-rules>` will take effect. For example:
``` css
@media screen and (shape: circle) {
  @import "circle.css";
}
```
The `@import "circle.css"` rule is only used on devices with circular screens. `<css-rules>` can be any CSS rules, including any number of `@import`, `@font-face`, selectors, and `@media` rules.

## The `media-query` Attribute of Components

The `media-query` attribute can be used on any component to determine whether the component should be rendered using media [query conditions](#query-conditions). For example:
``` html
<div media-query="(shape: circle)">
  ...
</div>
```
The `<div>` in the example above is a component that is only rendered on devices with circular screens.

The `media-query` attribute is processed only during the build stage, and components that do not meet the media query conditions are directly removed. When elements selected by the `media-query` attribute are relatively complex, consider using [Template Macros](../component/template-macro.md).

## Query Conditions

A query condition is an expression with the following structure:
``` ebnf
(* Media query expression *)
<query> := <query> and | or | , <query>  (* Logical combination using and, or, , *)
         | (not <query>) (* not expression *)
         | <media-type>  (* Media type *)
         | (<feature>: <value>)
         | (<feature> <relop> <value>)
         | (<value> <relop> <feature> <relop> <value>)
(* Relational operators *)
<relop> := < | <= | > | >=
```
Where `<media-type>` is a [media type](#media-types), `<feature>` is any [media feature](#media-features), and `<value>` is the value supported by that media feature. All of the following are valid query condition expressions:
``` css
@media screen { ... }
@media screen and (shape: rect) and (width < 500px) { ... }
@media not (shape: rect) { ... } /* This is equivalent to selecting circular screens */
```

### Logical Operators

Multiple query condition expressions can be combined using `and`, `or`, and `,`. The `not` operator can be used to negate a query condition. Parentheses can also be used to increase operator precedence:
``` css
@media (not (width < 500px)) or (orientation: portrait) { ... }
```
The meanings of the various operators are as follows:
- `A and B` is satisfied when both `A` and `B` are met;
- `A and B` (referring to `or` logic context) and `A, B` are satisfied when either `A` or `B` is met;
- `not A` is not satisfied when `A` is met, and vice versa.

### Relational Operators

Certain media features support relational operators, such as `width`:
``` css
@media (width > 500px) { ... } /* Selects devices with a width greater than 500px */
@media (400px < width <= 600px) { ... } /* Range comparison is supported */
```
There are 4 relational operators: `<`, `<=`, `>`, `>=`.

## Query Properties

### Media Types

A media type is a name. Currently, only the `screen` media type is supported. `screen` is also the default media type, so it can be omitted.

### Media Features

#### `width`

Queries the width of the device screen, supporting relational operators. The unit of the value must be `px`, for example, `500px`.

#### `max-width`

Specifies the maximum width of the screen. The unit of the value must be `px`. `(max-width: 500px)` is equivalent to `(width <= 500px)`.

#### `min-width`

Specifies the minimum width of the screen. The unit of the value must be `px`. `(min-width: 500px)` is equivalent to `(width >= 500px)`.

#### `height`

Queries the height of the device screen, supporting relational operators. The unit of the value must be `px`, for example, `500px`.

#### `max-height`

Specifies the maximum height of the screen. The unit of the value must be `px`. `(max-height: 500px)` is equivalent to `(height <= 500px)`.

#### `min-height`

Specifies the minimum height of the screen. The unit of the value must be `px`. `(min-height: 500px)` is equivalent to `(height >= 500px)`.

#### `shape`

Specifies the shape of the screen. Supported values are:
- `rect`: Represents a rectangular screen;
- `circle`: Represents a circular screen;

#### `aspect-ratio`

Queries the aspect ratio of the screen, supporting relational operators. The value can be a number or a fraction, for example, both `1.5` and `3/2` represent an aspect ratio of $3 / 2$.

#### `max-aspect-ratio`

Specifies the maximum screen aspect ratio of the device.

#### `min-aspect-ratio`

Specifies the minimum screen aspect ratio of the device.

#### `orientation`

Specifies the screen orientation. Supported values are:
- `portrait`: Represents a portrait screen device;
- `landscape`: Represents a landscape screen device.

#### `memory-profile`

The memory profile attribute is a reference value used to guide developers in trimming features under different memory budgets. It is set based on parameters such as the device's actual memory capacity and screen resolution. The memory profile helps developers optimize and adjust features according to a set memory budget, ensuring that applications run smoothly even on low-end devices.

The `memory-profile` attribute supports the following syntax:
``` ebnf
 memory-profile := <number>   (* Memory profile size, default unit is KiB *)
                 | <number> K (* Memory profile size, unit is KiB *)
                 | <number> M (* Memory profile size, unit is MiB, can include decimals *)
```

Note that `memory-profile` is not the device's actual memory capacity. Generally, the values of this attribute are categorized as follows:
- $2048$ ($2\rm M$): Less than $2\rm MiB$ belongs to low-end devices. Applications should cut features like fish-eye lists, long lists with a large number of images, etc. Some complex pages may also need to be simplified or removed.
- $4096$ ($4\rm M$): Less than $4\rm MiB$ belongs to mid-to-low-end devices. Applications can use a small number of fish-eye lists, but overly long lists with images are not recommended.
- $8192$ ($8\rm M$): Less than $8\rm MiB$ belongs to mid-to-high-end devices. Basically, all features can be used, but performance improvements can still be achieved with larger capacity.

For example, the following media query statement matches devices with a memory profile between $2{\rm MiB}$ and $4{\rm MiB}$:

``` css
@media (2M < memory-profile <= 4M) {
  /* Specific CSS rule-set */
}
```

If you need to get the device's memory profile in JavaScript, please use the [`memoryProfile`](/api/system-device.md#memoryprofile) property of the `@system.device` module.