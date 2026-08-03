# 富文本

在使用流式布局时，[`a`](/components/a.md)、[`span`](/components/span.md) 以及 [`checkbox`](/components/checkbox.md) 等行内元素可以沿着行进行布局并且可以断行，其中 `span` 等组件的文本还能跨越多行进行布局，利用这一点可以实现富文本显示。

## 纯文本显示

我们先看一下 Glyphix 是怎样显示纯文本的。[`p`](/components/a.md) 和 [`text`](/components/text.md) 组件可以用于纯文本显示。只需要将文本字符串指定为这些组件的 `text` 属性即可：
``` html
<p text="plain text string." />
<text text="plain text string." />
```
也支持 Web 的文本节点（即文本是元素的子节点）：
``` html
<p>plain text string."</p>
<text>plain text string."</text>
```
Glyphix 会把组件的唯一文本子节点转换成 `text` 属性，因此这两种写法本质上是一致的。换言之只要自定义组件支持 `text` 属性，就可以像 `p` 组件那样使用文本子节点。

## 富文本显示

`p` 和 `text` 组件无法用于富文本，因为它们总是一个完整的盒子而不能跨越多行布局。要实现富文本，首先需要有一个流式布局的容器，然后应使用 `span` 等组件来显示文本。例如：
``` html
<div>
  <span>rich&nbsp;</span>
  <span style="color: red">text&nbsp;</span>
  <span>string.</span>
</div>
```
很多组件默认都使用流式布局，例如 `div`、`p` 等。简单起见，也可以省略 `<span>` 标签：
``` html
<div>
  rich <span style="color: red">text</span> string.
</div>
```
组件有多个子元素时，其中的文本子元素会自动转换成 `span` 组件。
