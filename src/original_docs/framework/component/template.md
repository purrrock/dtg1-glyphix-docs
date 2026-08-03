# 模板语法

模板是 UX 文件的 `<template>` 标签内的内容。整体上来说模板是标准的 HTML 语法，但是模板语法也引入了不同于 HTML 的语法限制以及新语法，本文档将介绍这些内容。

## 标签

模板中支持标签嵌套，但是所有的标签都必须闭合。因此以下写法是合法的：
``` html
<div> <p>message</p> </div>
```
但是下面的写法不合法：
``` html
<div> <p>message</p> <!-- <div> 标签没有闭合 -->
```

## 文本值

模板中的文本元素和属性值都是文本值，例如
``` html
<com name="value">A message</com>
```
中的 `A message` 和 `value` 都是文本。`A message` 文本值会传递给 `com` 组件的 `text` 属性，因此文本节点（`A message` 部分）实际上是 `text` 属性的语法糖：
``` html
<p>text</p>
```
等效于
``` html
<p text="text"></p>
```
文本值在内部使用 JavaScript 字符串表示。

### 文本子节点

文本子节点不仅可以用于原生组件，也可以用于带有 `text` 属性的自定义组件，如：
```html
<p>The text element of P.</p>
<MyCom>The text element of MyCom.</MyCom>
```
只需为 `MyCom` 组件提供一个 `text` [响应式属性](component-object.md#响应式属性)即可接收文本节点的内容，而不需要通过 `<slot>` 插槽或其他机制。

::: warning
某些组件没有 `text` 属性（如 `div`），将文本节点作为它们的子节点将不会显示任何内容！请确保将文本节点作为 `p`、`text` 或 `span` 等原生组件的子节点。
:::

还可以在组件中使用多个文本子节点，如：
```html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```
会在 `div` 中混合显示文本和 [`switch`](/components/switch.md) 组件：

<glyphix id="component-template-text-1" height="32" inline>

``` html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```

</glyphix>

当文本节点和其他节点混合时，文本节点会被翻译为 [`span`](/components/span.md) 节点，而不是将其传递给某个组件的 `text` 属性。因此上面的示例等效于这段代码：
```html
<div>
  <span>The switch&nbsp;</span>
  <switch />
  <span>&nbsp;and&nbsp;</span>
  <checkbox />
  <span>&nbsp;checkbox.</span>
</div>
```
这样的隐式 `span` 元素也可以指定 CSS 样式，但无法使用类选择器（因为没有 `class` 属性）。

### 空白字符

文本子节点源码中的换行、制表符等所有空白字符都被当作空格，而空格的处理规则为：
- 第一个文本子节点头部的空格会被删除。
- 最后一个文本子节点尾部的空格会被删除。
- 其他位置连续的多个空格视为一个空格。

::: tip
只有一个文本节点时，它既是第一个文本子节点，也是最后一个子节点，所以其前后的空格都会删除。如果文本节点没有任何内容（包括删除空格之后没有内容的情况），它就会被删除。
:::

因此，`<p>  spances </p>` 这样的写法不会显示任何空格，而
```html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```
会删除 `<div>` 和 `The siwtch` 之间，以及 `checkbox.` 和 `</div>` 之间的空格（和换行）。但是会保留 `The switch` 和 `<switch />` 等之间的一个空格。

当你发现无法利用上述规则控制空白字符时，就需要考虑用 [HTML 字符参考](https://developer.mozilla.org/en-US/docs/Glossary/Character_reference)来表示。

::: tip
在文本节点中混合[插值表达式](#插值表达式)时，需要注意后者是 JavaSscript 表达式，其中的字符串要使用 JavaScript [转义字符](https://developer.mozilla.org/en-US/docs/Glossary/Escape_character)规则。
:::

## 属性和插值

### 插值表达式

可以在文本中使用双括号包含一个表达式，即**插值**表达式：
``` html
<p>Message: {{ msg }}!</p>
```
渲染时会将双花括号内的表达式进行求值并和前后的文本拼接。如果表达式前后没有文本，就构成了**未拼接**的插值表达式，此时直接使用表达式的值而不会将其转换为文本。

在属性值中也可以使用插值表达式，例如：
``` html
<div visible="{{true}}"></div>
```
其中 `{{true}}` 会直接计算为 boolean 型的 `true` 值，而不是字符串。

::: tip
像 `visible` 之类的属性要求传入的值类型为 boolean 型，因此需要使用 `visibe="{{ expr }}"` 这样的未拼接写法，从而避免大括号前后的文本导致插值表达式变成文本。由于 JavaScript 的值转换规则，`visible="false"` 会使属性求值为 `true`（非空字符串转换为 boolean 型的 `true`）。当然，这种场景也可以使用[隐式属性值](#隐式属性值)。
:::

如果需要传递一个数值常量，以下两种写法都会生效：
``` html
<scroll damping="{{1.5}}"></scroll>
<scroll damping="1.5"></scroll>
```
因为字符串 `"1.5"` 可以被自动转换为数值 `1.5`。我们推荐用第一种写法，因为它不需要做多余的类型转换并且语义更明确。

未拼接的插值表达式属性值的类型就是插值表达式的值，例如 `{{1 + 2}}` 的类型是 number。而其他插值表达式是文本值。

### 属性绑定表达式

如果组件的属性不是文本类型，就可以用未拼接的插值表达式：
``` html
<com items="{{ [1, 2, 3] }}" />
```
也可以使用属性绑定表达式语法：
``` html
<com :items="[1, 2, 3]" />
```
相比于一般的属性，属性绑定表达式需要在属性前面添加一个 `:` 字符，此时属性值会作为表达式来编译而不是字符串。用这种方法不用写 `{{ }}` 并且可读性更好。

### 隐式属性值

如果元素的属性只写属性名，但是不写属性值，那么它等效于 boolean 的 `true`：
``` html
<com focus></com>
```
等效于
``` html
<com :focus="true"></com>
```
隐式属性值适用于各种选项属性：填写属性名表示开启选项，而不填属性名表示关闭选项。如果需要通过属性传递空字符串，应当显式地写出空的属性值：
``` html
<com empty-property=""></com>
```
隐式属性值的规则适用于普通的属性，不适用于[指令属性](#指令属性值)，指令属性应总是写出属性值。

### 指令属性值

对于 `if`、`for` 和 `on` 之类的[指令](/framework/commands/README.md)来说，属性的值不会是一个文本，因此不可以使用拼接了文本的插值表达式，例如
``` html
<div on:click="console.dir({{$event}})"></div>
```
是不合法的。此时可以使用未拼接的插值表达式：
``` html
<div on:click="{{console.dir($event)}}"></div>
```
所有的指令属性都支持省略双花括号，因此上面的代码可以简写成：
``` html
<div on:click="console.dir($event)"></div>
```
但要注意，普通的属性必须通过未拼接的插值表达式，或者属性绑定表达式来传递非文本类型的值。

### `this` 绑定

在插值表达式（包括属性绑定表达式）中，名称（identifier）一般会自动绑定到组件对象的属性，即
``` html
<div on:visible="callback"></div>
```
中的表达式 `callback` 等效的 JavaScript 代码是 `this.callback`。

出现在模板语法作用域中的名称不会绑定 `this`，这主要体现在 `for` 指令中。例如
``` html
<p for="v in ['one', 'two']">{{ v }}</p>
```
插值表达式 `{{ v }}` 中的名称 `v` 会绑定到 `for` 指令中所定义的迭代变量 `v`，而不是绑定到组件对象的 `this` 属性。

某些全局对象所使用的名称和保留名称也不会绑定到组件对象的 `this` 属性，这些名称有：

- `this`、`true`、`false`、`undefined`、`null`
- `console`
- `Math`、`Date`、`Number`、`Array`、`Object`、`Boolean`、`String`、`RegExp`、`JSON`
- `NaN`、`Infinity`
- `isNaN`、`isFinite`
- `parseFloat`、`parseInt`

## 插值表达式语法

插值表达式支持大部分的 JavaScript 表达式语法，但不支持语句等语法。本节列出所有受支持的表达式。

插值表达式内部不能出现 `}}`，因此类似 `{key: {a: 1.0}}` 的写法是无法编译的，此时可以通过添加空格解决：`{ key: { a: 1.0 } }`。

### 基础表达式

- 数值：`1`、`1.0`、`1e10` 等数值字面量
- 标识符：变量名称，以及 `true`、`null` 等基础类型的枚举值
- 字符串：使用单引号或双引号包含的字符串字面量（在 XML/HTML 环境中双引号并不好用）
- 括号：`( expr )`，使用圆括号来提升内部表达式的求值优先级

### 一元表达式

- 负数：`- expr`
- 正数：`+ expr`
- 逻辑取反：`! expr`

### 二元表达式

由 `+`、`-`、`*`、`/`、`%`、`==`、`!=`、`>`、`>=`、`<`、`<=`、`&&`、`||` 运算符和操作数构成的二元表达式。这些运算符的优先级和结合性与 JavaScript 相同/

支持 `=`、`+=`、`-=`、`*=`、`/=`、`%=` 赋值运算符。

### 三元表达式

三目选择表达式：`cond ? expr : expr`。

### 其他表达式

- 函数调用：和 JavaScript 语法相同
- 成员表达式：`objct.prop`
- 下标表达式：`array[index]`
- Array 字面量：`[1, expr, ...]`，和 JavaScript 语法相同
- Object 字面量：`{ a: 1, b: expr }`，和 JavaScript 语法相同

### 模板字符串

插值表达式部分支持[模板字符串](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Template_literals)语法。例如在以下模板字符串中
``` js
`head ${ expr } tail`
```
表达式 `expr` 中不能出现 `}` 字符，这意味着你不能使用 JavaScript 对象字面量以及包含表达式的模板字符串。本节提到的其他表达式则都可以在模板字符串中使用。

插值表达式中的模板字符串不支持换行。

::: tip
表达式中的语法错误可以通过 glyphix.js 工具来查看并定位。
:::

## 其他提示
