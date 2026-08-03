# Template syntax


The template is the content within the `<template>` tag of the UX file. Generally speaking, templates are standard HTML syntax, but template syntax also introduces syntax restrictions and new syntax that are different from HTML. This document will introduce these contents.


## Label


Templates support tag nesting, but all tags must be closed. Therefore the following writing is legal:
``` html
<div> <p>message</p> </div>
```
But the following way of writing is illegal:
``` html
<div> <p>message</p> <!-- <div> tag is not closed -->
```


## text value


Text elements and attribute values ​​in templates are text values, for example
``` html
<com name="value">A message</com>
```
`A message` and `value` in are both text. The `A message` text value is passed to the `text` attribute of the `com` component, so the text node (the `A message` part) is actually syntactic sugar for the `text` attribute:
``` html
<p>text</p>
```
Equivalent to
``` html
<p text="text"></p>
```
Text values ​​are represented internally using JavaScript strings.


### text child node


Text subnodes can be used not only for native components, but also for custom components with `text` attributes, such as:
```html
<p>The text element of P.</p>
<MyCom>The text element of MyCom.</MyCom>
```
Simply provide the `MyCom` component with a `text` [Responsive properties](component-object.md#响应式属性) to receive the contents of the text node without going through a `<slot>` slot or other mechanism.


::: warning

Some components don't have a `text` attribute (like `div` ), and having text nodes as their children won't show anything! Make sure to make the text node a child of a native component such as `p`, `text`, or `span`.
:::



You can also use multiple text child nodes in the component, such as:
```html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```
A mix of text and [`switch`](/components/switch.md) components will be displayed in `div`:


<glyphix id="component-template-text-1" height="32" inline>



``` html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```


</glyphix>



When text nodes are mixed with other nodes, the text node is translated into a [`span`](/components/span.md) node instead of being passed to a component's `text` attribute. So the above example is equivalent to this code:
```html
<div>
  <span>The switch&nbsp;</span>
  <switch />
  <span>&nbsp;and&nbsp;</span>
  <checkbox />
  <span>&nbsp;checkbox.</span>
</div>
```
Such implicit `span` elements can also specify CSS styles, but cannot use class selectors (because there is no `class` attribute).


### White space characters


All whitespace characters such as newlines and tabs in the source code of text subnodes are treated as spaces, and the processing rules for spaces are:
- The leading spaces of the first text child node will be removed.
- Trailing spaces in the last text child node will be removed.
- Multiple consecutive spaces in other positions are treated as one space.


::: tip

When there is only one text node, it is both the first text child node and the last child node, so the spaces before and after it will be deleted. If the text node has no content (including the case where there is no content after removing the spaces), it will be deleted.
:::



Therefore, writing `<p> spances </p>` will not display any spaces, but
```html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```
Spaces (and newlines) between `<div>` and `The siwtch`, and between `checkbox.` and `</div>` are removed. But a space between `The switch` and `<switch />` etc. will be retained.


When you find that you cannot use the above rules to control whitespace characters, you need to consider using [HTML character reference](https://developer.mozilla.org/en-US/docs/Glossary/Character_reference).


::: tip

When mixing [interpolation expression](#插值表达式) in text nodes, be aware that the latter is a JavaScript expression, and the strings within it use JavaScript [escape character](https://developer.mozilla.org/en-US/docs/Glossary/Escape_character) rules.
:::



## Properties and interpolation


### interpolation expression


You can enclose an expression, an **interpolation** expression, in text using double brackets:
``` html
<p>Message: {{ msg }}!</p>
```
When rendering, the expression within the double curly braces will be evaluated and spliced ​​with the preceding and following text. If there is no text before and after the expression, it constitutes an **unspliced** interpolation expression, and the value of the expression is used directly without converting it to text.


Interpolation expressions can also be used in attribute values, for example:
``` html
<div visible="{{true}}"></div>
```
Among them, `{{true}}` will be directly calculated as a boolean value of `true` instead of a string.


::: tip

Attributes like `visible` require the incoming value type to be boolean, so you need to use unspliced ​​writing like `visibe="{{ expr }}"` to avoid the text before and after the curly braces causing the interpolation expression to become text. Due to JavaScript's value conversion rules, `visible="false"` causes the property to evaluate to `true` (non-empty strings are converted to boolean `true`). Of course, [implicit attribute value](#隐式属性值) can also be used in this scenario.
:::



If you need to pass a numeric constant, the following two writing methods will take effect:
``` html
<scroll damping="{{1.5}}"></scroll>
<scroll damping="1.5"></scroll>
```
Because the string `"1.5"` can be automatically converted to the numeric value `1.5`. We recommend using the first way of writing, because it does not require redundant type conversion and has clearer semantics.


The type of the unspliced ​​interpolation expression attribute value is the value of the interpolation expression. For example, the type of `{{1 + 2}}` is number. While other interpolation expressions are text values.


### property binding expression


If the component's properties are not of text type, you can use unspliced ​​interpolation expressions:
``` html
<com items="{{ [1, 2, 3] }}" />
```
You can also use property binding expression syntax:
``` html
<com :items="[1, 2, 3]" />
```
Compared with ordinary attributes, attribute binding expressions need to add a `:` character in front of the attribute. At this time, the attribute value will be compiled as an expression instead of a string. This method eliminates the need to write `{{ }}` and is more readable.


### implicit attribute value


If the element's attribute only writes the attribute name, but not the attribute value, then it is equivalent to boolean's `true`:
``` html
<com focus></com>
```
Equivalent to
``` html
<com :focus="true"></com>
```
Implicit attribute values ​​are applicable to various option attributes: filling in the attribute name means turning on the option, and not filling in the attribute name means turning off the option. If you need to pass an empty string through an attribute, you should write out the empty attribute value explicitly:
``` html
<com empty-property=""></com>
```
The rules for implicit attribute values ​​apply to ordinary attributes, not to [Command attributes](#指令属性值), directive attributes should always write out the attribute value.


### directive attribute value


For `if`, `for` and `on` like [instruction](/framework/commands/README.md), the value of the attribute will not be a text, so interpolation expressions concatenated with text cannot be used, e.g.
``` html
<div on:click="console.dir({{$event}})"></div>
```
is illegal. In this case, unspliced ​​interpolation expressions can be used:
``` html
<div on:click="{{console.dir($event)}}"></div>
```
All directive attributes support omitting double curly braces, so the above code can be shortened to:
``` html
<div on:click="console.dir($event)"></div>
```
But be aware that ordinary properties must pass non-text values ​​through unspliced ​​interpolation expressions or property binding expressions.


### `this` binding


In interpolation expressions (including property binding expressions), the name (identifier) ​​is generally automatically bound to the property of the component object, that is
``` html
<div on:visible="callback"></div>
```
The equivalent JavaScript code for the expression in `callback` is `this.callback`.


Names appearing in template syntax scope are not bound to `this`, which is mainly reflected in the `for` directive. For example
``` html
<p for="v in ['one', 'two']">{{ v }}</p>
```
The name `v` in the interpolation expression `{{ v }}` is bound to the iteration variable `v` defined in the `for` directive, rather than to the `this` property of the component object.


Some names used by global objects and reserved names are also not bound to the `this` attribute of the component object. These names are:


- `this`、`true`、`false`、`undefined`、`null`
- `console`
- `Math`、`Date`、`Number`、`Array`、`Object`、`Boolean`、`String`、`RegExp`、`JSON`
- `NaN`、`Infinity`
- `isNaN`、`isFinite`
- `parseFloat`、`parseInt`


## Interpolation expression syntax


Interpolation expressions support most JavaScript expression syntax, but do not support syntax such as statements. This section lists all supported expressions.


`}}` cannot appear inside the interpolation expression, so writing like `{key: {a: 1.0}}` cannot be compiled. In this case, it can be solved by adding spaces: `{ key: { a: 1.0 } }`.


### basic expression


- Numerical values: `1`, `1.0`, `1e10` and other numerical literals
- Identifier: variable name, and enumeration values ​​of basic types such as `true` and `null`
- String: Use a string literal enclosed in single or double quotes (double quotes are not easy to use in an XML/HTML environment)
- Parentheses: `( expr )`, use parentheses to increase the evaluation priority of inner expressions


### unary expression


- Negative number: `- expr`
- Positive number: `+ expr`
- Logical negation: `! expr`


### binary expression


A binary expression composed of `+`, `-`, `*`, `/`, `%`, `==`, `!=`, `>`, `>=`, `<`, `<=`, `&&`, `||` operators and operands. The precedence and associativity of these operators are the same as in JavaScript/


Supports `=`, `+=`, `-=`, `*=`, `/=`, `%=` assignment operators.


### ternary expression


Trinocular selection expression: `cond ? expr : expr`.


### Other expressions


- Function call: same syntax as JavaScript
- Member expression: `objct.prop`
- Subscript expression: `array[index]`
- Array literal: `[1, expr,...]`, the same syntax as JavaScript
- Object literal: `{ a: 1, b: expr }`, the same syntax as JavaScript


### template string


Interpolation expressions partially support the [template string](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Template_literals) syntax. For example in the following template string
``` js
`head ${ expr } tail`
```
The `}` character cannot appear in the expression `expr`, which means you cannot use JavaScript object literals and template strings containing expressions. The other expressions mentioned in this section can be used in template strings.


Template strings in interpolation expressions do not support newlines.


::: tip

Syntax errors in expressions can be viewed and located using the glyphix.js tool.
:::



## Other tips