---

icon: swap-horizontal

---

# model directive


Two-way binding of component properties can be achieved using the `model` directive.


## grammar


``` html
<com model:prop="value"></com>
<com ::prop="value"></com>
```
Use the `model:` prefix or the abbreviated `::` in the attribute to modify the attribute, and you can use the `model` directive for two-way binding. Among them, `prop` is the attribute name of the target component, and `value` is the view-model attribute name in the current component that requires two-way binding.


## Two-way binding


Two-way binding between component properties and view model properties can be achieved using [`on` directive](on.md) and [property binding expression](/framework/component/template.md#属性绑定表达式):
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



When the value of `this.state` is modified in JavaScript code, the `:value="state"` expression in the `switch` tag will cause the display state of the `switch` element to be updated, and the `on` directive expression will cause the value of `state` to be updated after the user clicks on the `switch` element.


During this process, the display state of the interface (`switch` component and text `value: {{state}}`) is consistent with the `state` attribute in the view-model. We call this mechanism **two-way binding**.


The `model` directive is essentially syntactic sugar for the above approach, which can easily implement two-way binding:
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



## Two-way binding of custom components


Two-way binding is often used for form components, but the `model` directive also supports custom components. Just provide an event with the same name for the property of the custom component and trigger it when the property changes. For example:


``` js
// file: com.ux
export default {
  data: {
    prop: 0 // Suppose you want to perform two-way binding on the prop attribute
  },
  watch: {
    prop(x) { // Trigger an event with the same name when the prop attribute value changes
      this.$emit('prop', x)
    }
  }
}
```
Assume this is a partial component object of a custom component, where the `prop` attribute is used for two-way binding. In this example, the `watch` object is used to listen for changes in the `prop` attribute and trigger an event named `'prop'` when it changes. Just do two-way binding like this in the caller component:
``` html
<com ::prop="valueName"></com>
```