---
icon: alternate-email
---
# on 指令

`on` 指令用于监听支持监听的属性值变化。

## 语法

``` html
<div on:attribute="expr"></div>
<div onattribute="expr"></div> <!-- 兼容快应用的语法 -->
<div @attribute="expr"></div>  <!-- Vue 风格语法 -->
```

`attribute` 是需要监听变化的属性名字，`expr` 是属性变化时需要执行的表达式。标准的 `on` 指令使用 `on:` 前缀，也支持 `on` 和 `@` 字符前缀。

`on` 指令的属性值支持[指令属性值](/framework/component/template.md#指令属性值)语法。

::: tip
建议使用 `on:attribute` 格式，`onattribute` 容易导致开发者在不知情的情况下混淆 `on` 指令和普通属性。此外，属性名如 `oneself` 会解析为 `on:eself` 的指令，应特别注意。
:::

## 监听表达式

### 基本用法

下面的代码监听一个 `div` 组件的触摸事件：
``` html
<div on:touchmove="console.log($event)"></div>
```
示例中监听 [`touchmove`](../generic/properties.md#touchmove) 事件此处直接打印了[触摸事件对象](../generic/properties.md#touchevent)。`$event` 变量用于获取事件值，它是由 `on` 指令定义的变量（作用域仅在 `on` 指令表达式内）。

还可以调用在组件对象中定义的方法：
``` html
<div on:touchmove="onTouch('move', $event)"></div>
```

``` js
export default {
  onTouch(type, event) {
    console(`touch ${type}:`, event)
  }
}
```

自定义事件的方法请参考[组件间通信](../component/communicate.md)。

### 函数表达式

如果监听表达式的值是一个函数，那么会自动调用该函数：
``` html
<div on:click="onClick" />
```

``` js
export default {
  onClick(event) {
    console.log(event)
  }
}
```
如示例所示，事件值会作为唯一的参数传递给函数。

::: tip
监听表达式不一定是一个函数变量，也可以是复杂表达式（例如包含函数调用的表达式）。只要该表达式的值是一个函数那么就会由 `on` 指令调用。
:::

## 监听组件属性值的变化

有些组件的属性值在变化时会产生事件，可以通过 `on` 指令来监听：

``` html
<list on:index="indexChanged($event)">
  <content/>
</list>
```

如[属性文档规范](../component/README.md#属性文档规范)中的描述，支持**监听**的属性可以使用 `on` 指令来监听值变化。
