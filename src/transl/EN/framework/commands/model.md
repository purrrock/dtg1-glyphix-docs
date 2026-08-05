---
icon: swap-horizontal
---
# model Directive

The `model` directive is used to implement two-way binding for component properties.

## Syntax

``` html
<com model:prop="value"></com>
<com ::prop="value"></com>
```
You can use the `model:` prefix or the shorthand `::` to decorate a property, enabling two-way binding with the `model` directive. Here, `prop` is the name of the target component's property, and `value` is the name of the view-model property in the current component to be bound.

## Two-Way Binding

Using the [`on` directive](on.md) and [property binding expressions](/framework/component/template.md#属性绑定表达式), you can achieve two-way binding between component properties and view-model properties:
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

When the value of `this.state` is modified in the JavaScript code, the `:value="state"` expression inside the `switch` tag updates the display state of the `switch` element, while the `on` directive expression updates the value of `state` after the user clicks the `switch` element.

Throughout this process, the UI display state (the `switch` component and the text `value: {{state}}`) remains consistent with the `state` property in the view-model. We call this mechanism **two-way binding**.

Essentially, the `model` directive is syntactic sugar for the syntax shown above, simplifying two-way binding:
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

## Two-Way Binding for Custom Components

Two-way binding is commonly used for form components, but the `model` directive also supports custom components. To use it, simply provide an event with the same name as the custom component's property and trigger it when the property changes. For example:

``` js
// file: com.ux
export default {
  data: {
    prop: 0 // Assuming we want two-way binding for the prop property
  },
  watch: {
    prop(x) { // Trigger an event with the same name when the prop property value changes
      this.$emit('prop', x)
    }
  }
}
```
Assume this is part of the component object for a custom component, where the `prop` property is used for two-way binding. In this example, the `watch` object is used to monitor changes to the `prop` property and trigger an event named `'prop'` when it changes. In the parent component, you can simply perform two-way binding like this:
``` html
<com ::prop="valueName"></com>
```