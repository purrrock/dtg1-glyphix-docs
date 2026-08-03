# Template Syntax

Templates are the contents inside the `<template>` tag of a UX file. Overall, templates use standard HTML syntax, but the template syntax also introduces syntax limitations and new features that differ from HTML. This document will cover these topics.

## Tags

Tag nesting is supported in templates, but all tags must be closed. Therefore, the following code is valid:
``` html
<div> <p>message</p> </div>
```
However, the following code is invalid:
``` html
<div> <p>message</p> <!-- <div> tag is not closed -->
```

## Text Values

Text elements and attribute values in templates are text values. For example, in:
``` html
<com name="value">A message</com>
```
both `A message` and `value` are text. The `A message` text value is passed to the `text` attribute of the `com` component, so the text node (the `A message` part) is actually syntactic sugar for the `text` attribute:
``` html
<p>text</p>
```
is equivalent to:
``` html
<p text="text"></p>
```
Text values are represented internally as JavaScript strings.

### Text Child Nodes

Text child nodes can be used not only in native components but also in custom components with a `text` attribute, such as:
```html
<p>The text element of P.</p>
<MyCom>The text element of MyCom.</MyCom>
```
You only need to provide a `text` [reactive property](component-object.md#reactive-properties) for the `MyCom` component to receive the content of the text node, without needing to use `<slot>` or other mechanisms.

::: warning
Some components do not have a `text` attribute (such as `div`), and placing text nodes as their child nodes will not display any content! Please make sure to place text nodes as child nodes of native components like `p`, `text`, or `span`.
:::

You can also use multiple text child nodes in a component, such as:
```html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```
This will mix text and the [`switch`](/components/switch.md) component within the `div`:

<glyphix id="component-template-text-1" height="32" inline>

``` html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```

</glyphix>

When text nodes are mixed with other nodes, the text nodes are translated into [`span`](/components/span.md) nodes rather than being passed to a component's `text` attribute. Therefore, the above example is equivalent to this code:
```html
<div>
  <span>The switch&nbsp;</span>
  <switch />
  <span>&nbsp;and&nbsp;</span>
  <checkbox />
  <span>&nbsp;checkbox.</span>
</div>
```
Such implicit `span` elements can also be assigned CSS styles, but class selectors cannot be used (because there is no `class` attribute).

### Whitespace

All whitespace characters, such as line breaks and tabs in the source code of text child nodes, are treated as spaces. The rules for processing spaces are as follows:
- Spaces at the beginning of the first text child node are removed.
- Spaces at the end of the last text child node are removed.
- Multiple consecutive spaces in other positions are treated as a single space.

::: tip
When there is only a single text node, it is both the first and the last text child node, so spaces at both its beginning and end will be removed. If a text node has no content (including when it has no content after removing spaces), it will be deleted.
:::

Therefore, writing `<p>  spances </p>` will not display any spaces, while:
```html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```
will remove the spaces (and line breaks) between `<div>` and `The switch`, as well as between `checkbox.` and `</div>`. However, a single space between `The switch` and `<switch />`, etc., will be preserved.

When you find that you cannot control whitespace using the above rules, you should consider using [HTML character references](https://developer.mozilla.org/en-US/docs/Glossary/Character_reference).

::: tip
When mixing [interpolation expressions](#interpolation-expressions) within text nodes, keep in mind that the latter are JavaScript expressions, and strings within them must follow JavaScript [escape character](https://developer.mozilla.org/en-US/docs/Glossary/Escape_character) rules.
:::

## Attributes and Interpolation

### Interpolation Expressions

You can enclose an expression in double curly braces within text, which is an **interpolation** expression:
``` html
<p>Message: {{ msg }}!</p>
```
During rendering, the expression inside the double curly braces is evaluated and concatenated with the text before and after it. If there is no text before or after the expression, it forms an **unconcatenated** interpolation expression. In this case, the value of the expression is used directly without being converted to text.

Interpolation expressions can also be used in attribute values, for example:
``` html
<div visible="{{true}}"></div>
```
Here, `{{true}}` evaluates directly to a boolean `true` value rather than a string.

::: tip
Attributes like `visible` require a boolean value type, so you need to use unconcatenated syntax like `visible="{{ expr }}"` to prevent text around the curly braces from turning the interpolation expression into text. Due to JavaScript's value conversion rules, `visible="false"` would cause the attribute to evaluate to `true` (non-empty strings convert to boolean `true`). Of course, [implicit attribute values](#implicit-attribute-values) can also be used for this scenario.
:::

If you need to pass a numeric constant, both of the following approaches will work:
``` html
<scroll damping="{{1.5}}"></scroll>
<scroll damping="1.5"></scroll>
```
Because the string `"1.5"` can be automatically converted to the number `1.5`. We recommend using the first approach because it avoids unnecessary type conversion and is more semantically explicit.

The type of an unconcatenated interpolation expression attribute value is simply the type of the expression's value, for example, `{{1 + 2}}` has the type `number`. Other interpolation expressions result in text values.

### Attribute Binding Expressions

If a component's attribute is not of a text type, you can use an unconcatenated interpolation expression:
``` html
<com items="{{ [1, 2, 3] }}" />
```
You can also use the attribute binding expression syntax:
``` html
<com :items="[1, 2, 3]" />
```
Compared to regular attributes, attribute binding expressions require adding a `:` character before the attribute name. In this case, the attribute value is compiled as an expression rather than a string. This method avoids writing `{{ }}` and offers better readability.

### Implicit Attribute Values

If an element's attribute is written with only its name and no value, it is equivalent to a boolean `true`:
``` html
<com focus></com>
```
is equivalent to:
``` html
<com :focus="true"></com>
```
Implicit attribute values are suitable for various option attributes: providing the attribute name means enabling the option, while omitting it means disabling the option. If you need to pass an empty string via an attribute, you should explicitly write out an empty attribute value:
``` html
<com empty-property=""></com>
```
The rule for implicit attribute values applies to ordinary attributes and does not apply to [directive attributes](#directive-attribute-values). Directive attributes should always have their values written out.

### Directive Attribute Values

For [directives](/framework/commands/README.md) like `if`, `for`, and `on`, the attribute value is not text, so you cannot use interpolation expressions with concatenated text. For example:
``` html
<div on:click="console.dir({{$event}})"></div>
```
is invalid. Instead, you can use an unconcatenated interpolation expression:
``` html
<div on:click="{{console.dir($event)}}"></div>
```
All directive attributes support omitting the double curly braces, so the code above can be shortened to:
``` html
<div on:click="console.dir($event)"></div>
```
However, note that ordinary attributes must pass non-text values via unconcatenated interpolation expressions or attribute binding expressions.

### `this` Binding

In interpolation expressions (including attribute binding expressions), identifiers generally bind automatically to the component object's properties. That is, in:
``` html
<div on:visible="callback"></div>
```
the expression `callback` is equivalent to the JavaScript code `this.callback`.

Identifiers appearing within the scope of the template syntax do not bind to `this`. This is mainly reflected in `for` directives. For example:
``` html
<p for="v in ['one', 'two']">{{ v }}</p>
```
The identifier `v` in the interpolation expression `{{ v }}` binds to the iteration variable `v` defined in the `for` directive, rather than to the component object's `this` property.

Certain names used by global objects and reserved names also do not bind to the component object's `this` property. These names are:

- `this`, `true`, `false`, `undefined`, `null`
- `console`
- `Math`, `Date`, `Number`, `Array`, `Object`, `Boolean`, `String`, `RegExp`, `JSON`
- `NaN`, `Infinity`
- `isNaN`, `isFinite`
- `parseFloat`, `parseInt`

## Interpolation Expression Syntax

Interpolation expressions support most JavaScript expression syntax, but do not support statements or other syntaxes. This section lists all supported expressions.

Interpolation expressions cannot contain `}}` inside them, so constructs like `{key: {a: 1.0}}` cannot be compiled. This can be resolved by adding spaces: `{ key: { a: 1.0 } }`.

### Basic Expressions

- Numbers: Numeric literals such as `1`, `1.0`, `1e10`
- Identifiers: Variable names, as well as primitive enum values like `true`, `null`
- Strings: String literals enclosed in single or double quotes (double quotes are less convenient in XML/HTML environments)
- Parentheses: `( expr )`, using parentheses to elevate the evaluation priority of inner expressions

### Unary Expressions

- Negative: `- expr`
- Positive: `+ expr`
- Logical NOT: `! expr`

### Binary Expressions

Binary expressions formed by operands and operators `+`, `-`, `*`, `/`, `%`, `==`, `!=`, `>`, `>=`, `<`, `<=`, `&&`, `||`. The precedence and associativity of these operators are the same as in JavaScript.

Assignment operators `=`, `+=`, `-=`, `*=`, `/=`, `%=` are supported.

### Ternary Expressions

Ternary conditional expressions: `cond ? expr : expr`.

### Other Expressions

- Function calls: Same as JavaScript syntax
- Member expressions: `object.prop`
- Subscript expressions: `array[index]`
- Array literals: `[1, expr, ...]`, same as JavaScript syntax
- Object literals: `{ a: 1, b: expr }`, same as JavaScript syntax

### Template Literals

Interpolation expressions partially support [template literal](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Template_literals) syntax. For example, in the following template literal:
``` js
`head ${ expr } tail`
```
The expression `expr` cannot contain the `}` character, which means you cannot use JavaScript object literals or nested template literals containing expressions. Other expressions mentioned in this section can be used within template literals.

Template literals in interpolation expressions do not support line breaks.

::: tip
Syntax errors in expressions can be inspected and located using the glyphix.js tool.
:::

## Other Tips