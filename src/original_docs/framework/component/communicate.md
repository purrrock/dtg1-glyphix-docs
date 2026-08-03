# 组件间通信

组件之间的通信由组件参数和事件绑定实现。例如：
``` html
<scroll scroll-snap="center" on:scroll="scrolled($event)" />
```
就向 `scroll` 组件实例传递了 `scroll-snap` 属性参数使元素居中对齐，并且会监听 `scroll` 属性的变化。

## 属性参数

通过组件节点的**属性**（attribute）字段可以向子组件传递参数，例如：
``` html
<p text="A message"></p>
```
会向一个 `p` 组件实例传递一个名称为 `text`，值为 `"A message"` 的属性。可以按照 XML/HTML 的语法传递多个属性。通过[插值表达式](template#插值表达式)可以向组件的属性中传递一个被计算的值。

## 事件响应

[原生组件](native-component)封装了很多 UI 输入事件，比如触摸手势的响应以及 UI 变化的事件。这些事件都可以通过 [`on` 指令](../commands/on.md)进行监听。

## 触发事件

对于自定义组件，可以使用组件对象的 [`$emit(name, value)`](/framework/component/component-apis.md#emit) 方法来触发一个事件：
``` html
<panel on:some-event="console.log(`the event ${$event} was emited!`)">
```

``` js
// in panel.ux
export default {
  emitEvent() {
    this.$emit('someEvent', 'hello')
  }
}
```

`$emit` 方法有两个参数：
- `name`：需要发送事件的属性名称，必须使用小驼峰命名法（对应的模板属性为蛇形命名法或小驼峰命名法）
- `value`：可选参数，事件属性的值，将作为 `on` 指令的 `$event` 变量的值

如果组件对象的 view-model 中有名为 `name` 的属性，`$emit` 方法不会将属性值修改为 `value`。
