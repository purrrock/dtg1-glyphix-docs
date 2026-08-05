---
icon: file-tree
---
# if / elif / else Directives

The `if` / `elif` / `else` directives are used for conditional rendering. These directives control whether a component is rendered. For example, the `if` directive renders the component only when the condition is true, otherwise it deletes the component. This is different from the component's `show` attribute, which controls whether the component is displayed but does not delete it.

## Syntax

### if Directive

``` html
<p if="cond">if: true</p>
```
If the `cond` expression is true, the component is rendered; otherwise, it is not rendered.

## elif and else Directives

Components with `elif` and `else` directives must follow a component with an `if` or `elif` directive, and use the negation of the previous condition to control whether the component is rendered:
``` html
<p if="cond1">if cond1: true</p> 
<p elif="cond2">elif cond2: true</p>
<p elif="cond3">elif cond3: true</p>
<p else>else</p> <!-- The else directive does not support attribute values -->
```
The behavior of this code is as follows:
- If the `cond1` condition is true, only the `if cond1: true` text is rendered;
- Otherwise, if `cond2` is true, only `elif cond2: true` is rendered;
- Otherwise, if `cond3` is true, only `elif cond3: true` is rendered;
- If all conditions are false, the `else` text is rendered.

The attribute values of the `if` / `elif` / `else` directives support the [Directive Attribute Values](/framework/component/template.md#指令属性值) syntax.