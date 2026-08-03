# media inquiries


Media queries allow developers to use different styles based on different device types. Currently, media queries support the `@media` rule of CSS, but the `media` attribute of components is not yet supported.


## CSS `@media` rules


The grammatical form of the `@media` rule is
``` css
@media <查询条件> {
  <css-rules>
}
```
[`<query condition>`](#查询条件) is used to query media types and media characteristics, and can be combined using a variety of logical operators. The CSS rules in `<css-rules>` will take effect when the media query conditions are met. For example
``` css
@media screen and (shape: circle) {
  @import "circle.css";
}
```
Use the `@import "circle.css"` rule only on devices with round screens. `<css-rules>` can be any CSS rule, including any number of `@import`, `@font-face`, selectors, `@media` rules, etc.


## Component's `media-query` attribute


You can use the `media-query` attribute on any component to use media [Query conditions](#查询条件) to determine whether the component is rendered. For example
``` html
<div media-query="(shape: circle)">
  ...
</div>
```
The `<div>` in is a component that will only be rendered on devices with round screens.


The `media-query` attribute will only be processed during the packaging phase, and components that do not meet the media query conditions will be deleted directly. When the elements that need to be selected using the `media-query` attribute are more complex, you can consider using [template macro](../component/template-macro.md)


## Query conditions


The query condition is an expression with the following structure:
``` ebnf
(* 媒体查询表达式 *)
<query> := <query> and | or | , <query>  (* 可以使用 and or , 来组合逻辑 *)
         | (not <query>) (* not 表达式 *)
         | <media-type>  (* 媒体类型 *)
         | (<feature>: <value>)
         | (<feature> <relop> <value>)
         | (<value> <relop> <feature> <relop> <value>)
(* 关系运算符 *)
<relop> := < | <= | > | >=
```
Among them, `<media-type>` is a kind of [media type](#媒体类型), `<feature>` is any kind of [media properties](#媒体特性), and `<value>` is a value supported by this media feature. The following are legal query condition expressions:
``` css
@media screen { ... }
@media screen and (shape: rect) and (width < 500px) { ... }
@media not (shape: rect) { ... } /* This is equivalent to selecting a circular screen */
```


### Logical operators


Use `and`, `or` and `,` to combine multiple query condition expressions, and use the `not` operator to negate the query condition. You can also use parentheses to increase operator precedence:
``` css
@media (not (width < 500px)) or (orientation: portrait) { ... }
```
The meanings of the various operators are as follows:
- `A and B` is satisfied when `A` and `B` are satisfied at the same time;
- Satisfies `A and B` and `A, B` when one of `A` or `B` is satisfied;
- `not A` is not satisfied when `A` is satisfied, and vice versa.


### Relational operators


Some media properties support relational operators, such as `width`:
``` css
@media (width > 500px) { ... } /* Select devices wider than 500px */
@media (400px < width <= 600px) { ... } /* Support range comparison */
```
There are 4 types of relational operators: `<`, `<=`, `>`, `>=`.


## Query properties


### media type


The media type is a name. Currently, only the `screen` media type is supported. `screen` is also the default media type, so it does not need to be written.


### media properties


#### `width`


Query the width of the device screen, supporting relational operators. Values ​​must be in units of `px`, for example `500px`.


#### `max-width`


Specifies the maximum width of the screen. The value must be in `px` units. `(max-width: 500px)` is equivalent to `(width <= 500px)`.


#### `min-width`


Specifies the minimum width of the screen. The value must be in `px` units. `(min-width: 500px)` is equivalent to `(width >= 500px)`.


#### `height`


Query the height of the device screen, supporting relational operators. Values ​​must be in units of `px`, for example `500px`.


#### `max-height`


Specifies the maximum height of the screen. The unit of the value must be `px`. `(max-height: 500px)` is equivalent to `(height <= 500px)`.


#### `min-height`


Specifies the minimum height of the screen. The value must be in `px` units. `(min-height: 500px)` is equivalent to `(height >= 500px)`.


#### `shape`


Specifies the shape of the screen. Supported values ​​are:
- `rect`: represents a rectangular screen;
- `circle`: indicates a circular screen;


#### `aspect-ratio`


Query the aspect ratio of the screen, supporting relational operators. The value can be a number or a fraction, for example `1.5` and `3/2` both represent an aspect ratio of $3 / 2$.


#### `max-aspect-ratio`


Specifies the device's maximum screen aspect ratio.


#### `min-aspect-ratio`


Specifies the device's minimum screen aspect ratio.


#### `orientation`


Specifies the shape of the screen. Supported values ​​are:
- `portrait`: indicates a vertical screen device;
- `landscape`: Indicates horizontal screen device.


#### `memory-profile`


The Memory profile attribute is a reference value used to guide developers in reducing functionality under different memory budgets. It is set based on parameters such as the device's actual memory capacity and screen resolution. Memory profiles can help developers optimize and adjust functions according to the set memory budget to ensure that applications can run smoothly on low-end devices.


The `memory-profile` attribute supports the following syntax:
``` ebnf
 memory-profile := <number>   (* 内存配置大小，默认单位为 KiB *)
                 | <number> K (* 内存配置大小，单位为 KiB *)
                 | <number> M (* 内存配置大小，单位为 MiB，可以带有小数 *)
```


Note that `memory-profile` is not the actual memory capacity of the device. Generally speaking, the values ​​of this attribute are broken down as follows:
- $2048$ ($2\rm M$): Devices less than $2\rm MiB$ are low-end devices. Applications should cut off fisheye lists, long lists with a large number of pictures, etc. Some complex pages may also need to be simplified or eliminated.
- $4096$ ($4\rm M$): Devices less than $4\rm MiB$ are mid- to low-end devices. A small number of fisheye lists can be used in applications, but it is not recommended to use too long lists with pictures.
- $8192$ ($8\rm M$): Less than $8\rm MiB$ is a mid-to-high-end device that can basically use all functions, but performance can be improved with larger capacity.


For example, the following ligand query matches devices with memory profiles between $2{\rm MiB}\sim 4{\rm MiB}$:


``` css
@media (2M < memory-profile <= 4M) {
  /* Specific CSS rule-set */
}
```


If you need to get a device's memory profile in JavaScript, use the `@system.device` module's [`memoryProfile`](/api/system-device.md#memoryprofile) attribute.