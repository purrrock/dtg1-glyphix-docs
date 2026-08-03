---
icon: swap-horizontal
---
# model 指令

使用 `model` 指令可以实现组件属性的双向绑定。

## 语法

``` html
<com model:prop="value"></com>
<com ::prop="value"></com>
```
在属性中使用 `model:` 前缀或者简写的 `::` 来修饰属性即可使用 `model` 指令进行双向绑定。其中 `prop` 为目标组件的属性名字，而 `value` 为当前组件中需要双向绑定的 view-model 属性名。

## 双向绑定

使用 [`on` 指令](on.md)和[属性绑定表达式](/framework/component/template.md#属性绑定表达式)可以实现组件属性和 view model 属性之间的双向绑定：
``` html
<div>
  <switch :value="state" on:value="state = $event"/> value: {{state}}
</div>
```

``` js
export default {
  data: {
    state: false
  },
  onReady() {
    setInterval(() => this.state = !this.state, 2000)
  }
}
```

<Glyphix id="commands-model-1" height="32" inline>

``` html
<div>
  <switch :value="state" on:value="state = $event"/> value: {{state}}
</div>
```

``` js
export default {
  data: {
    state: false
  },
  onReady() {
    setInterval(() => this.state = !this.state, 2000)
  }
}
```

</Glyphix>

当 JavaScript 代码中修改了 `this.state` 的值时，`switch` 标签中的 `:value="state"` 表达式会使 `switch` 元素的显示状态被更新，而 `on` 指令表达式会在用户点击 `switch` 元素后使 `state` 的值得到更新。

这个过程中界面的显示状态（`switch` 组件和文本 `value: {{state}}`）和 view-model 中的 `state` 属性都是一致的，我们称这种机制为**双向绑定**。

`model` 指令本质上是上面写法的语法糖，它可以简单地实现双向绑定：
``` html
<div>
  <switch ::value="state"/> value: {{state}}
</div>
```

<Glyphix id="commands-model-2" height="32" inline>

``` html
<div>
  <switch ::value="state"/> value: {{state}}
</div>
```

``` js
export default {
  data: {
    state: false
  },
  onReady() {
    setInterval(() => this.state = !this.state, 2000)
  }
}
```

</Glyphix>

## 自定义组件的双向绑定

双向绑定常用于表单组件，但是 `model` 指令也支持自定义组件，只要为自定义组件的属性提供一个同名的事件并在属性变化时触发即可。例如：

``` js
// file: com.ux
export default {
  data: {
    prop: 0 // 假设要对 prop 属性进行双向绑定
  },
  watch: {
    prop(x) { // 在 prop 属性值变化时触发同名事件
      this.$emit('prop', x)
    }
  }
}
```
假设这是某个自定义组件的部分组件对象，其中 `prop` 属性用于双向绑定。这个例子中使用了 `watch` 对象来监听 `prop` 属性的变化，并在其变化时触发名为 `'prop'` 的事件。在调用方组件中只需这样进行双向绑定：
``` html
<com ::prop="valueName"></com>
```