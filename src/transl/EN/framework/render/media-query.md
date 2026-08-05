# Media Queries

Media queries allow developers to use different styles for different device types. Currently, media queries support CSS `@media` rules, while the component `media` property is not yet supported.

## CSS `@media` Rules

The syntax of the `@media` rule is:
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
The `@import "circle.css"` rule is only applied on devices with circular screens. `<css-rules>` can be any CSS rules, which include any number of `@import`, `@font-face`, selectors, and `@media` rules, etc.

## Component `media-query` Property

The `media-query` property can be used on any component to determine whether the component should be rendered based on media [query conditions](#query-conditions). For example:
``` html
<div media-query="(shape: circle)">
  ...
</div>
```
The `<div>` here is a component that will only be rendered on devices with circular screens.

The `media-query` property is only processed during the packaging stage, and components that do not meet the media query conditions will be directly removed. When the elements selected using the `media-query` property are relatively complex, consider using [Template Macros](../component/template-macro.md).

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
Where `<media-type>` is a [media type](#media-types), `<feature>` is any [media feature](#media-features), and `<value>` is the value supported by that media feature. The following are all valid query condition expressions:
``` css
@media screen { ... }
@media screen and (shape: rect) and (width < 500px) { ... }
@media not (shape: rect) { ... } /* This is equivalent to selecting a circular screen */
```

### Logical Operators

Multiple query condition expressions can be combined using `and`, `or`, and `,`, and the `not` operator can be used to negate a query condition. Parentheses can also be used to increase operator precedence:
``` css
@media (not (width < 500px)) or (orientation: portrait) { ... }
```
The meanings of various operators are as follows:
- `A and B` is met when both `A` and `B` are met;
- `A and B` (note: typically referring to `or` logic) and `A, B` are met when either `A` or `B` is met;
- `not A` is met when `A` is not met, and vice versa.

### Relational Operators

Some media features support relational operators, such as `width`:
``` css
@media (width > 500px) { ... } /* Select devices with a width greater than 500px */
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

Specifies the maximum width of the screen; the unit of the value must be `px`. `(max-width: 500px)` is equivalent to `(width <= 500px)`.

#### `min-width`

Specifies the minimum width of the screen; the unit of the value must be `px`. `(min-width: 500px)` is equivalent to `(width >= 500px)`.

#### `height`

Queries the height of the device screen, supporting relational operators. The unit of the value must be `px`, for example, `500px`.

#### `max-height`

Specifies the maximum height of the screen; the unit of the value must be `px`. `(max-height: 500px)` is equivalent to `(height <= 500px)`.

#### `min-height`

Specifies the minimum height of the screen; the unit of the value must be `px`. `(min-height: 500px)` is equivalent to `(height >= 500px)`.

#### `shape`

Specifies the shape of the screen. Supported values are:
- `rect`: Represents a rectangular screen;
- `circle`: Represents a circular screen;

#### `aspect-ratio`

Queries the aspect ratio of the screen, supporting relational operators. The value can be a number or a fraction, for example, `1.5` and `3/2` both represent an aspect ratio of $3 / 2$.

#### `max-aspect-ratio`

Specifies the maximum screen aspect ratio of the device.

#### `min-aspect-ratio`

Specifies the minimum screen aspect ratio of the device.

#### `orientation`

Specifies the orientation of the screen. Supported values are:
- `portrait`: Represents a portrait device;
- `landscape`: Represents a landscape device.

#### `memory-profile`

The memory-profile property is a reference value used to guide developers in trimming features under different memory budgets. It is set based on parameters such as the device's actual memory capacity and screen resolution. The memory profile helps developers optimize and adjust features based on a set memory budget to ensure that the application runs smoothly even on low-end devices.

The `memory-profile` property supports the following syntax:
``` ebnf
 memory-profile := <number>   (* Memory configuration size, default unit is KiB *)
                 | <number> K (* Memory configuration size, unit is KiB *)
                 | <number> M (* Memory configuration size, unit is MiB, decimals allowed *)
```

Note that `memory-profile` is not the true physical memory capacity of the device. Generally, the values of this property are tiered as follows:
- $2048$ ($2\rm M$): Less than $2\rm MiB$ belongs to low-end devices, where applications should drop fish-eye lists, long lists with a large number of images, etc. Some complex pages may also need to be simplified or removed.
- $4096$ ($4\rm M$): Less than $4\rm MiB$ belongs to mid-to-low-end devices, where a small number of fish-eye lists can be used in the application, but excessively long lists with images are not recommended.
- $8192$ ($8\rm M$): Less than $8\rm MiB$ belongs to mid-to-high-end devices, where basically all features can be used, though performance may still improve with larger capacities.

For example, the following media query statement matches devices with a memory profile between $2{\rm MiB}\sim 4{\rm MiB}$:

``` css
@media (2M < memory-profile <= 4M) {
  /* Specific CSS rule-set */
}
```

If you need to get the device's memory profile in JavaScript, please use the [`memoryProfile`](/api/system-device.md#memoryprofile) property of the `@system.device` module.