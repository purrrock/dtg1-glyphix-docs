# Template Syntax

Templates are the contents inside the `<template>` tag of a UX file. Overall, templates use standard HTML syntax; however, the template syntax also introduces syntax limitations and new syntax that differ from HTML, which will be introduced in this document.

## Tags

Tag nesting is supported in templates, but all tags must be closed. Therefore, the following writing is valid:
``` html
<div> <p>message</p> </div>
```
However, the following is invalid:
``` html
<div> <p>message</p> <!-- <div> tag is not closed -->
```

## Text Values

Text elements and attribute values in templates are text values. For example, in:
``` html
<com name="value">A message</com>
```
both `A message` and `value` are text. The `A message` text value will be passed to the `text` attribute of the `com` component, so the text node (the `A message` part) is actually syntactic sugar for the `text` attribute:
``` html
<p>text</p>
```
is equivalent to
``` html
<p text="text"></p>
```
Text values are represented internally as JavaScript strings.

### Text Child Nodes

Text child nodes can be used not only for native components, but also for custom components with a `text` attribute, such as:
```html
<p>The text element of P.</p>
<MyCom>The text element of MyCom.</MyCom>
```
You only need to provide a `text` [reactive property](component-object.md#reactive-properties) for the `MyCom` component to receive the content of the text node, without going through `<slot>` slots or other mechanisms.

::: warning
Some components do not have a `text` attribute (such as `div`), and placing text nodes as their children will not display anything! Make sure to place text nodes as children of native components such as `p`, `text`, or `span`.
:::

You can also use multiple text child nodes in a component, such as:
```html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```
which will mixed-display text and the [`switch`](/components/switch.md) component inside the `div`:

<glyphix id="component-template-text-1" height="32" inline>

``` html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```

</glyphix>

When a text node is mixed with other nodes, the text node will be translated into a [`span`](/components/span.md) node rather than being passed to a component's `text` attribute. Therefore, the above example is equivalent to this code:
```html
<div>
  <span>The switch&nbsp;</span>
  <switch />
  <span>&nbsp;and&nbsp;</span>
  <checkbox />
  <span>&nbsp;checkbox.</span>
</div>
```
Such implicit `span` elements can also have CSS styles assigned, but class selectors cannot be used (because there is no `class` attribute).

### Whitespace

All whitespace characters, such as line breaks and tabs, in the source code of text child nodes are treated as spaces. The rules for processing spaces are as follows:
- Leading spaces at the beginning of the first text child node are removed.
- Trailing spaces at the end of the last text child node are removed.
- Multiple consecutive spaces at other positions are treated as a single space.

::: tip
When there is only a single text node, it is both the first and the last text child node, so spaces before and after it are removed. If a text node has no content (including when there is no content left after removing spaces), it will be deleted.
:::

Therefore, writing like `<p>  spances </p>` will not display any spaces, while
```html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```
will remove the spaces (and line breaks) between `<div>` and `The switch`, as well as between `checkbox.` and `</div>`. However, a single space between `The switch` and `<switch />`, etc., will be preserved.

When you find that you cannot control whitespace using the above rules, you should consider using [HTML character references](https://developer.mozilla.org/en-US/docs/Glossary/Character_reference) to represent them.

::: tip
When mixing [interpolation expressions](#interpolation-expressions) within text nodes, keep in mind that the latter are JavaScript expressions, and strings within them must follow JavaScript [escape character](https://developer.mozilla.org/en-US/docs/Glossary/Escape_character) rules.
:::

## Attributes and Interpolation

### Interpolation Expressions

You can enclose an expression in double braces within text, which is an **interpolation** expression:
``` html
<p>Message: {{ msg }}!</p>
```
During rendering, the expression inside the double braces is evaluated and concatenated with the text before and after it. If there is no text before and after the expression, it forms an **unconcatenated** interpolation expression; in this case, the value of the expression is used directly without being converted to text.

Interpolation expressions can also be used in attribute values, for example:
``` html
<div visible="{{true}}"></div>
```
Here, `{{true}}` evaluates directly to the boolean value `true`, rather than a string.

::: tip
Attributes like `visible` require a boolean value type, so you need to use unconcatenated syntax like `visible="{{ expr }}"` to prevent text around the curly braces from causing the interpolation expression to turn into text. Due to JavaScript's value conversion rules, `visible="false"` would cause the attribute to evaluate to `true` (non-empty strings convert to boolean `true`). Of course, [implicit attribute values](#implicit-attribute-values) can also be used for this scenario.
:::

If you need to pass a numeric constant, either of the following two writings will work:
``` html
<scroll damping="{{1.5}}"></scroll>
<scroll damping="1.5"></scroll>
```
Because the string `"1.5"` can be automatically converted to the number `1.5`. We recommend the first approach because it requires no extra type conversion and is more semantically explicit.

The type of an unconcatenated interpolation expression attribute value is the type of the interpolation expression itself, such as the type of `{{1 + 2}}`, which is a number. Other interpolation expressions are text values.

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

If an element's attribute is specified with only its name and no value, it is equivalent to the boolean `true`:
``` html
<com focus></com>
```
is equivalent to
``` html
<com :focus="true"></com>
```
Implicit attribute values are suitable for various option attributes: specifying the attribute name means enabling the option, while omitting it means disabling the option. If you need to pass an empty string via an attribute, you should explicitly write an empty attribute value:
``` html
<com empty-property=""></com>
```
The rule for implicit attribute values applies to ordinary attributes and does not apply to [directive attributes](#directive-attribute-values), which should always have their attribute values written out.

### Directive Attribute Values

For [directives](/framework/commands/README.md) such as `if`, `for`, and `on`, the attribute value is not a text string, so interpolation expressions concatenated with text cannot be used. For example,
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
Note, however, that regular attributes must pass non-text type values via unconcatenated interpolation expressions or attribute binding expressions.

### `this` Binding

In interpolation expressions (including attribute binding expressions), identifiers generally automatically bind to the properties of the component object. That is, the expression `callback` in
``` html
<div on:visible="callback"></div>
```
is equivalent to the JavaScript code `this.callback`.

Identifiers appearing within the template syntax scope will not bind `this`, which is primarily reflected in the `for` directive. For example,
``` html
<p for="v in ['one', 'two']">{{ v }}</p>
```
The identifier `v` in the interpolation expression `{{ v }}` binds to the iteration variable `v` defined in the `for` directive, rather than binding to the `this` property of the component object.

Identifiers used by certain global objects and reserved names will also not bind to the `this` property of the component object. These names include:

- `this`, `true`, `false`, `undefined`, `null`
- `console`
- `Math`, `Date`, `Number`, `Array`, `Object`, `Boolean`, `String`, `RegExp`, `JSON`
- `NaN`, `Infinity`
- `isNaN`, `isFinite`
- `parseFloat`, `parseInt`

## Interpolation Expression Syntax

Interpolation expressions support most JavaScript expression syntax, but do not support statements or other syntaxes. This section lists all supported expressions.

`}}` cannot appear inside interpolation expressions, so writings like `{key: {a: 1.0}}` cannot be compiled. This can be resolved by adding spaces: `{ key: { a: 1.0 } }`.

### Basic Expressions

- Numbers: Numeric literals such as `1`, `1.0`, `1e10`, etc.
- Identifiers: Variable names, as well as primitive enum values like `true`, `null`, etc.
- Strings: String literals enclosed in single or double quotes (double quotes are not very convenient in XML/HTML environments)
- Parentheses: `( expr )`, using parentheses to raise the evaluation priority of internal expressions

### Unary Expressions

- Negative numbers: `- expr`
- Positive numbers: `+ expr`
- Logical NOT: `! expr`

### Binary Expressions

Binary expressions formed by operators and operands: `+`, `-`, `*`, `/`, `%`, `==`, `!=`, `>`, `>=`, `<`, `<=`, `&&`, `||`. The precedence and associativity of these operators are the same as in JavaScript.

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
The `}` character cannot appear within the expression `expr`, which means you cannot use JavaScript object literals and template literals containing expressions within it. Other expressions mentioned in this section can all be used inside template literals.

Template literals in interpolation expressions do not support line breaks.

::: tip
Syntax errors in expressions can be viewed and located using the glyphix.js tool.
:::

## Other Tips