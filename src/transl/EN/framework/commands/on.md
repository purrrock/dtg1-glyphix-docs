---
icon: alternate-email
---
# on Directive

The `on` directive is used to listen for changes in property values that support listening.

## Syntax

``` html
<div on:attribute="expr"></div>
<div onattribute="expr"></div> <!-- Syntax compatible with Quick App -->
<div @attribute="expr"></div>  <!-- Vue-style syntax -->
```

`attribute` is the name of the property to listen for changes on, and `expr` is the expression to execute when the property changes. The standard `on` directive uses the `on:` prefix, and `on` and `@` character prefixes are also supported.

The property value of the `on` directive supports the [directive property value](/framework/component/template.md#指令属性值) syntax.

::: tip
It is recommended to use the `on:attribute` format. `onattribute` can easily lead developers to unconsciously confuse the `on` directive with regular properties. In addition, property names like `oneself` will be parsed as the `on:eself` directive, which requires special attention.
:::

## Listening Expressions

### Basic Usage

The following code listens to a touch event on a `div` component:
``` html
<div on:touchmove="console.log($event)"></div>
```
In this example, the [`touchmove`](../generic/properties.md#touchmove) event is listened to, and the [touch event object](../generic/properties.md#touchevent) is printed directly. The `$event` variable is used to get the event value, which is defined by the `on` directive (its scope is limited to the `on` directive expression).

You can also call methods defined in the component object:
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

For methods on custom events, please refer to [Inter-component Communication](../component/communicate.md).

### Function Expressions

If the value of the listening expression is a function, that function will be called automatically:
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
As shown in the example, the event value will be passed as the sole argument to the function.

::: tip
The listening expression does not necessarily have to be a function variable; it can also be a complex expression (such as an expression containing a function call). As long as the value of the expression is a function, it will be invoked by the `on` directive.
:::

## Listening to Component Property Value Changes

Some component property values generate events when they change, which can be listened to using the `on` directive:

``` html
<list on:index="indexChanged($event)">
  <content/>
</list>
```

As described in the [Property Documentation Specification](../component/README.md#属性文档规范), properties that support **listening** can have their value changes listened to using the `on` directive.