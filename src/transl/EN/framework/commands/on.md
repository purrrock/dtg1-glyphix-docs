---

icon: alternate-email

---

# on command


The `on` directive is used to monitor changes in attribute values ​​that support monitoring.


## grammar


``` html
<div on:attribute="expr"></div>
<div onattribute="expr"></div> <!-- Syntax compatible with quick apps -->
<div @attribute="expr"></div>  <!-- Vue style syntax -->
```


`attribute` is the name of the attribute that needs to be monitored for changes, and `expr` is the expression that needs to be executed when the attribute changes. The standard `on` directive uses the `on:` prefix, and the `on` and `@` character prefixes are also supported.


The attribute value of the `on` directive supports the [directive attribute value](/framework/component/template.md#指令属性值) syntax.


::: tip

It is recommended to use the `on:attribute` format, as `onattribute` can easily cause developers to unknowingly confuse `on` directives with ordinary attributes. In addition, attribute names such as `oneself` will be parsed into instructions of `on:eself`, so special attention should be paid.
:::



## Listen expression


### Basic usage


The following code listens for touch events on a `div` component:
``` html
<div on:touchmove="console.log($event)"></div>
```
In the example, the [`touchmove`](../generic/properties.md#touchmove) event is listened to and [touch event object](../generic/properties.md#touchevent) is printed directly here. The `$event` variable is used to obtain the event value, which is a variable defined by the `on` directive (scoped only within the `on` directive expression).


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


For methods of customizing events, please refer to [Communication between components](../component/communicate.md).


### function expression


If the value of the listener expression is a function, the function will be called automatically:
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
As shown in the example, the event value is passed to the function as the only parameter.


::: tip

The listener expression does not have to be a function variable, but can also be a complex expression (such as an expression containing a function call). As long as the value of the expression is a function then it will be called by the `on` directive.
:::



## Monitor changes in component property values


Some components will generate events when their attribute values ​​change, which can be monitored through the `on` directive:


``` html
<list on:index="indexChanged($event)">
  <content/>
</list>
```


As described in [Property document specification](../component/README.md#属性文档规范), properties that support **listening** can use the `on` directive to listen for value changes.