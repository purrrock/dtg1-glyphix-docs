# 媒体查询

媒体查询允许开发者根据不同的设备类型使用不同的样式。目前媒体查询支持 CSS 的 `@media` 规则，尚不支持组件的 `media` 属性。

## CSS `@media` 规则

`@media` 规则的语法形式为
``` css
@media <查询条件> {
  <css-rules>
}
```
[`<查询条件>`](#查询条件)用于查询媒体类型和媒体特性，并且可以使用多种逻辑操作符进行组合。当媒体查询条件满足时 `<css-rules>` 中的 CSS 规则就会生效。例如
``` css
@media screen and (shape: circle) {
  @import "circle.css";
}
```
仅在圆形屏幕的设备上使用 `@import "circle.css"` 规则。`<css-rules>` 可以是任意的 CSS 规则，这包含任意数量的 `@import`、`@font-face`、选择器以及 `@media` 规则等。

## 组件的 `media-query` 属性

可以在任意组件上使用 `media-query` 属性来利用媒体[查询条件](#查询条件)决定组件是否被渲染。例如
``` html
<div media-query="(shape: circle)">
  ...
</div>
```
中的 `<div>` 是一个只会在圆形屏幕的设备上才会渲染的组件。

`media-query` 属性只会在打包阶段进行处理，不符合媒体查询条件的组件会被直接删除掉。当需要用 `media-query` 属性选择的元素较为复杂时，可以考虑使用[模板宏](../component/template-macro.md)

## 查询条件

查询条件是一种表达式，它的结构如下：
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
其中，`<media-type>` 是一种[媒体类型](#媒体类型)，`<feature>` 是任意一种[媒体特性](#媒体特性)，`<value>` 是该媒体特性支持的值。以下都是合法的查询条件表达式：
``` css
@media screen { ... }
@media screen and (shape: rect) and (width < 500px) { ... }
@media not (shape: rect) { ... } /* 这个等效于选择圆形屏 */
```

### 逻辑运算符

使用 `and`、`or` 以及 `,` 可以组合多个查询条件表达式，使用 `not` 运算符可以对查询条件取反。还可以使用括号来提高运算符的优先级：
``` css
@media (not (width < 500px)) or (orientation: portrait) { ... }
```
各种运算符的含义如下：
- 同时满足 `A` 和 `B` 时满足 `A and B`；
- 满足 `A` 或 `B` 之一时满足 `A and B` 以及 `A, B`；
- 满足 `A` 时不满足 `not A`，反之亦然。

### 关系运算符

某些媒体特性支持关系运算符，例如 `width`：
``` css
@media (width > 500px) { ... } /* 选择宽度大于 500px 的设备 */
@media (400px < width <= 600px) { ... } /* 支持范围比较 */
```
关系运算符有 4 种：`<`、`<=`、`>`、`>=`。

## 查询属性

### 媒体类型

媒体类型是一个名字，目前只支持 `screen` 媒体类型，`screen` 也是默认的媒体类型，因此可以不写。

### 媒体特性

#### `width`

查询设备屏幕的宽度，支持关系运算符。值的单位必须为 `px`，例如 `500px`。

#### `max-width`

指定屏幕的最大宽度，值的单位必须是 `px`。`(max-width: 500px)` 等价于 `(width <= 500px)`。

#### `min-width`

指定屏幕的最小宽度，值的单位必须是 `px`。`(min-width: 500px)` 等价于 `(width >= 500px)`。

#### `height`

查询设备屏幕的高度，支持关系运算符。值的单位必须为 `px`，例如 `500px`。

#### `max-height`

指定屏幕的最大高度，值的单位必须是 `px`。`(max-height: 500px)` 等价于 `(height <= 500px)`。

#### `min-height`

指定屏幕的最小高度，值的单位必须是 `px`。`(min-height: 500px)` 等价于 `(height >= 500px)`。

#### `shape`

指定屏幕的形状，支持的值有：
- `rect`：表示矩形屏幕；
- `circle`：表示圆形屏幕；

#### `aspect-ratio`

查询屏幕的宽高比，支持关系运算符。值可以是一个数或者分数，例如 `1.5` 和 `3/2` 都表示宽高比为 $3 / 2$。

#### `max-aspect-ratio`

指定设备最大的屏幕宽高比。

#### `min-aspect-ratio`

指定设备最小的屏幕宽高比。

#### `orientation`

指定屏幕的形状，支持的值有：
- `portrait`：表示竖屏设备；
- `landscape`：表示横屏设备。

#### `memory-profile`

Memory profile（内存配置文件）属性是一个用于指导开发者在不同内存预算下裁减功能的参考值。它是根据设备的实际内存容量和屏幕分辨率等参数设置的。内存配置文件可以帮助开发者根据设定的内存预算进行功能优化和调整，以确保应用在低端设备上也能流畅运行。

`memory-profile` 属性支持以下语法：
``` ebnf
 memory-profile := <number>   (* 内存配置大小，默认单位为 KiB *)
                 | <number> K (* 内存配置大小，单位为 KiB *)
                 | <number> M (* 内存配置大小，单位为 MiB，可以带有小数 *)
```

注意，`memory-profile` 并不是设备的真实内存容量。一般来说，该属性的值分档如下：
- $2048$ ($2\rm M$)：小于 $2\rm MiB$ 的属于低端设备，应用应该砍掉鱼眼列表、有大量图片的长列表等。某些复杂的页面可能也需要简化或者砍掉。
- $4096$ ($4\rm M$)：小于 $4\rm MiB$ 的属于中低端设备，应用中可以使用少量的鱼眼列表，但是不建议使用太长的带图片的列表。
- $8192$ ($8\rm M$)：小于 $8\rm MiB$ 的属于中高端设备，基本可以使用所有的功能，但是容量更大时还可有性能提升。

例如以下配体查询语句匹配内存配置文件在 $2{\rm MiB}\sim 4{\rm MiB}$ 之间的设备：

``` css
@media (2M < memory-profile <= 4M) {
  /* 具体的 CSS rule-set */
}
```

如果需要在 JavaScript 中获取设备的内存配置文件，请使用 `@system.device` 模块的 [`memoryProfile`](/api/system-device.md#memoryprofile) 属性。
