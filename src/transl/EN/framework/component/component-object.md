# component object


The `<script>` tag located within the UX file defines and exports a component object. A typical component object is defined as follows:
``` js
export default {
  data: {
    text: "Hello world"
  },
  onInit() {
    console.log("component onInit()")
  },
  clicked(event) {
    console.log(`clicked: ${event}`)
  }
}
```
The component framework allows developers to fill in some properties for component objects to implement functions. This document will introduce these properties.


## Reactive programming


**Reactive Programming** is a programming paradigm for dynamically updating interface and data state. Through **responsive properties**, developers can automatically track data changes and update the interface without having to manually trigger and manage these updates. This keeps the data and interface always synchronized, enabling a simple and efficient UI programming experience.


### Responsive properties


The properties defined in the [`data` attribute](#data-属性) and [`computed` attribute](#computed-属性) objects of the component object are all **responsive properties** of the component, also called view-model properties:
- ** `data` attribute**: directly reflects the status of the component. For example, temperature value, display text or button status can be defined in `data`. When the values ​​of these properties change, the frame automatically synchronizes them to the view.
- ** `computed` attribute **: used to define derived attributes calculated based on `data` or other `computed` attributes. Computed properties are automatically updated as dependent data changes, making complex logical expressions more intuitive and concise.


All in all, when the responsive property values ​​of a component change, the content that relies on these properties will be automatically updated and rendered, ensuring that the displayed content is consistent with the data.


### Automatic data binding


**Automatic data binding** is the core concept of reactive programming, which allows data changes to be directly reflected on the interface without the need for developers to manually handle it.


Because each responsive attribute is automatically bound to the relevant part of the interface, when the attribute value changes, the interface is automatically updated without the need to call the attribute update function of a specific element.


For example, define a reactive attribute named `counter`:
``` js
export default {
  data: { // Define the counter reactive property in the data object
    counter: 0 // Initial value is 0
  }
}
```


Whenever the value of `counter` changes, the interface that references this attribute will be automatically updated. The following [template](template) code demonstrates this mechanism:
``` html
<p on:click="counter += 1">
  counter: {{ counter }}
</p>
```
This example demonstrates a counter that increases the value displayed by `counter` by one when clicking the `<p>` label. You can click on the online demo below to test it:


<glyphix id="component-object-reactive" height="50" width="200" inline>



``` html
<p on:click="counter += 1">
  counter: {{ counter }}
</p>
```


``` js
export default {
  data: {
    counter: 0
  }
}
```


``` css
p {
  border: 2px solid gray;
  border-radius: 16px;
  padding: 2px 8px;
  text-align: center;
  height: 100%;
}
```


</glyphix>



`{{ counter }}` in the `<p>` tag is a template [interpolation expression](template.md#插值表达式), and its dependency on `counter` is automatically bound. And [`on:click` listening](/framework/commands/on.md) in the `<p>` tag modifies the `counter` attribute value when clicked. It can be seen that through automatic data binding, the manual **data**-**interface** update operation in traditional GUI development is eliminated, making the interface logic more concise and clear.


## `data` attribute


The `data` attribute is used to declare the reactive data attributes of the component. The property is an object, for example:
``` js
export default {
  data: {
    text: "Hello world"
  }
}
```
The value of the `data` attribute must be serializable through `JSON.stringify()`. To be precise, the following conditions must be met:
- Simple type values: `number`, `string`, `boolean`, `null` or `undefined`
- In `Object` and `Array` with recursive structures, the value of the deepest element must be one of the above


This means that attributes of `data` objects in source code cannot have functions or other special types of values, and this also includes objects like `Date`.


::: note

It is a known limitation that `data` objects do not support non-JSON compatible data types, such as `Date`, `Proxy` objects, and so on. If you need to use these types of data, you can define them as [Custom properties](#自定义属性), otherwise unpredictable behavior will result.
:::



The `data` attributes are all view-model attributes of the component, so the data therein can be used for reactive programming. Using `this.prop` in the component object can directly access the properties in the `data` object. So, in the following component object
``` js
export default {
  data: {
    onInit: true
  },
  onInit() {}
}
```
Code `this.onInit` will access the `onInit` attribute in the `data` object, not the lifecycle function `onInit`.


::: tip

To optimize performance, only data used for UI rendering and state management is defined in the `data` object. For data that does not require reactivity, they can be defined as [Custom properties](#自定义属性). For example: timer ID (return value of `setTimeout()`), [audio player](/api/system-media.md#createaudioplayer) handle, WebSocket connection object, etc. Such objects are generally unnecessary as reactive properties and will not work properly.
:::



## `computed` attribute


The `computed` property of the component object declares the computed properties in the component. Compared to the reactive properties in `data`, computed properties can implement properties that require some calculations to get the result. For example
``` html
<text> reversed message: {{ reversedMessage }}
```


``` js
export default {
  data: {
    message: "hello"
  },
  computed: {
    reversedMessage() { // This is the getter method of the reversedMessage computed property
      return this.message.split('').reverse().join('')
    }
  }
}
```
A `reversedMessage` computed attribute is declared here, which implements a getter function to obtain the attribute value. Use `this.reversedMessage` directly (`this.` can be omitted in the template) to get the value of the calculated attribute.


Computed properties are also view-model properties of components. The value of the calculated property is cached, so the value of the calculated property is not recalculated multiple times. Computed properties, on the other hand, are automatically updated when the view-model properties they depend on change. In this example, the value of the computed attribute is calculated from the `message` attribute, so when the `message` attribute changes, the value of the `reversedMessage` attribute is automatically updated.


### Setter methods for computed properties


The default computed properties only have getter methods, but you can also provide setter methods for computed properties:
``` js
export default {
  data: {
    message: "hello"
  },
  computed: {
    reversedMessage: {
      get() { // This is the getter method of the reversedMessage computed property
        return this.message.split('').reverse().join('')
      },
      set(value) {
        this.message = value.split('').reverse().join('')
      }
    }
  }
}
```
At this time, the value of the calculated attribute `reversedMessage` is no longer a function, but an object, which has two methods: getter method `get` and setter method `set`. The parameter of the `set` method is the new value that the calculated property needs to be set to.


## `watch` attribute


The `watch` object method is used to monitor changes in view-model properties, for example:
``` js
export default {
  data: {
    value: 0
  },
  watch: {
    value(newValue, oldValue) {
      console.log(`value change: ${oldValue} -> ${newValue}`)
    }
  }
}
```
The method of the `watch` object will listen for changes in the view-model attribute with the same name, so `watch.value()` listens for changes in the `value` attribute. Changes to computed properties can also be monitored by `watch`.


## life cycle function


See the [life cycle](life-cycle.md) documentation for details.


## Custom properties


Users can also define custom properties in component objects that are not in the view-model (i.e. not in the `data` or `computed` objects) and therefore are not reactive. Developers can define methods as custom attributes, and can also use custom attributes to store some data that does not require responsiveness. For example:
``` html
<p on:click="onClick()">{{ text }}</p>
```


``` js
export default {
  data: {
    text: "some text"
  },
  // Custom properties are not in the data or computed objects, but are defined directly in the component object.
  timer: null, // Stores the timer handle and does not need to be defined in advance. This attribute will be automatically created when this.timer is assigned a value.
  onInit() {
    // The new property assigned to this is a custom property
    this.timer = setInterval(() => this.text += "?", 1000)
  },
  onDestroy() {
    clearInterval(this.timer)
  },
  onClick() {
    this.text += "." // Manipulate view-model properties in custom methods
  }
}
```


The `text` attribute in the example is reactive, while `timer` is a non-responsive custom attribute. The `timer` attribute is used to store the timer handle. This value has nothing to do with the interface view, so it does not need to be used as a view-model attribute. Considering the standardization of the code, custom properties can also be defined in advance in the component object:
``` js
export default {
  data: {
    text: "some text"
  },
  timer: null, // Custom properties are direct properties of the component object
  // ...
}
```
As shown in the example, custom properties can be defined directly in the component object. Custom properties for each component are distinct instances and are not shared.


::: warning

Custom attributes, `data` objects, `computed` objects, life cycle functions and other attributes cannot have duplicate names, otherwise some attributes will be overwritten and become inaccessible.
:::



### method


Custom properties and methods are both direct properties of the component object, and they are essentially equivalent. When you assign a function to a property of a component object, the property becomes a method. This section demonstrates this equivalence through two examples.


Method 1: Directly define the method. This is the most common and recommended way of writing.
``` js
export default {
  data: {
    count: 0
  },
  increment() {
    this.count++
  }
}
```


Method 2: Define attributes and assign values ​​to functions.
``` js
export default {
  data: {
    count: 0
  },
  increment: function() {
    this.count++
  }
}
```
The two writing methods are completely identical in function and can be called through `this.increment()`. It's the same when used in a template:
``` html
<button on:click="increment()">Count: {{ count }}</button>
```


::: tip

It is recommended to use method 1, which is the object method syntax supported by the ES6+ standard and is more concise and clear.
:::



### Dynamic assignment method


In addition to defining methods directly in the component object, you can also dynamically assign methods after the component is instantiated (such as in the `onInit` life cycle). The key feature of this approach is that the dynamic methods of each component instance are independent and can capture and maintain different states through closures.


Consider a timer component where each instance has its own counter and can be stopped independently. This is a typical application scenario of the dynamic assignment method:
``` html
<div>
  <text>timeout: {{ counter }}</text>
  <button on:click="stopTimer">Stop</button>
</div>
```


``` js
export default {
  data: {
    counter: 0,
  },
  stopTimer: null, // Optional: Predefined stopTimer method
  onInit() {
    const timer = setInterval(() => {
      this.counter++
    }, 1000)
    // Dynamically create a stopTimer method and capture the timer variable through a closure
    this.stopTimer = () => {
      clearInterval(timer)
      this.stopTimer = null // Leave the method empty after stopping
    }
  },
}
```


The following example instantiates 4 timer components at the same time. You can try to stop any of them independently:


<glyphix id="component-object-dynamic-method" height="200" width="300" inline>

</glyphix>



The implementation of this dynamic assignment method relies on the following key points:
- **Closure Capture**: The `timer` constant created in `onInit` is a local variable, and the `stopTimer` method captures this variable through closure
- **Instance Independence**: Each component instance creates its own `timer` and `stopTimer` when calling `onInit`, and they do not interfere with each other.
- **State Isolation**: Clicking the "Stop" button of an instance will only stop the timer of that instance and will not affect other instances.


Of course, for this example, it is more common to define the `stopTimer` method directly in the component object:
``` js
export default {
  data: {
    counter: 0,
  },
  timer: null,
  onInit() {
    // In this case, timer needs to be stored as a custom attribute
    this.timer = setInterval(() => {
      this.counter++
    }, 1000)
  },
  stopTimer() {
    // The stopTimer method accesses this.timer to stop the timer
    clearInterval(this.timer)
    this.timer = null // Clear timer reference
  }
}
```
This is usually more intuitive for timers, but when some have complex contexts and require dynamic distribution strategies, dynamic assignment methods can be used to implement more flexible logic. The following table shows the difference between dynamic methods vs directly defined methods:


| Features | Direct definition method | Dynamic assignment method |
|------|------------|------------|

| Sharability | All instances share the same function object | Each instance has an independent copy of the function |
| Closure capture | Does not capture local variables in the scope | Can capture local variables in the scope |
| Memory usage | Less (shared) | Slightly more (one copy per instance) |
| Applicable scenarios | General, stateless operations | Operations that need to capture local states |
