---

icon: file-tree

---

# if / elif / else instructions


`if` / `elif` / `else` directives are used for conditional rendering. These directives control whether the component will be rendered. For example, the `if` directive will only render the component if the condition is true, otherwise it will remove the component. This is different from the component's `show` attribute, which controls whether the component is displayed but does not remove the component.


## grammar


### if directive


``` html
<p if="cond">if: true</p>
```
If the `cond` expression is true, the component will be rendered, otherwise it will not be rendered.


## elif and else directives


Components containing `elif` and `else` directives must follow components containing `if` or `elif` directives, and use the negation of the previous condition to control whether the component is rendered:
``` html
<p if="cond1">if cond1: true</p>
<p elif="cond2">elif cond2: true</p>
<p elif="cond3">elif cond3: true</p>
<p else>else</p> <!-- else directive does not support attribute values -->
```
The code behaves as follows:
- If the `cond1` condition is true, then only the `if cond1: true` text will be rendered;
- Otherwise, if `cond2` is true, only `elif cond2: true` will be rendered;
- Otherwise, if `cond3` is true, only `elif cond3: true` will be rendered;
- All conditions are false, rendering the `else` text.


The attribute values ​​of the `if` / `elif` / `else` directives support the [directive attribute value](/framework/component/template.md#指令属性值) syntax.