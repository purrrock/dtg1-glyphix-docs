---
icon: file-tree
---
# if / elif / else 指令

`if` / `elif` / `else` 指令用于条件渲染。这些指令控制组件是否会被渲染，例如 `if` 指令仅会在条件为真时渲染组件，否则会删除组件。这和组件 `show` 属性不同，后者控制组件是否显示但不会删除组件。

## 语法

### if 指令

``` html
<p if="cond">if: true</p>
```
如果 `cond` 表达式为真，那么组件会被渲染，否则不被渲染。

## elif 和 else 指令

含有 `elif` 和 `else` 指令的组件必须跟随在含有 `if` 或 `elif` 指令的组件之后，并使用上一个条件的否定来控制组件是否被渲染：
``` html
<p if="cond1">if cond1: true</p> 
<p elif="cond2">elif cond2: true</p>
<p elif="cond3">elif cond3: true</p>
<p else>else</p> <!-- else 指令不支持属性值 -->
```
该代码的行为如下：
- 如果 `cond1` 条件为真，那么仅 `if cond1: true` 文本会被渲染；
- 否则如果 `cond2` 为真，会只渲染 `elif cond2: true`；
- 否则如果 `cond3` 为真，会只渲染 `elif cond3: true`；
- 所有条件都为假，渲染 `else` 文本。

`if` / `elif` / `else` 指令的属性值支持[指令属性值](/framework/component/template.md#指令属性值)语法。
