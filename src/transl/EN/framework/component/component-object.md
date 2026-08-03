# Component Object

The `<script>` tag inside a UX file defines and exports a component object. A typical component object is defined as follows:
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
The component framework allows developers to populate component objects with certain properties to implement functionality. This document will introduce these properties.

## Reactive Programming

**Reactive programming** is a programming paradigm used to dynamically update the UI and data states. Through **reactive properties**, developers can automatically track data changes and update the UI without manual triggering and management. This keeps data and the UI synchronized at all times, delivering a concise and efficient UI programming experience.

### Reactive Properties

Properties defined within the [`data` property](#data-property) and [`computed` property](#computed-property) objects of a component are **reactive properties** of the component, also known as view-model properties:
- **`data` property**: Directly reflects the state of the component. For example, temperature values, display text, or button states can be defined in `data`. When these property values change, the framework automatically synchronizes them to the view.
- **`computed` property**: Used to define derived properties calculated based on `data` or other `computed` properties. Computed properties are automatically updated when their dependent data changes, making complex logical expressions more intuitive and concise.

In summary, when a component's reactive property value changes, content depending on these properties will automatically update and re-render, thereby ensuring that the displayed content remains consistent with the data.

### Automatic Data Binding

**Automatic data binding** is a core concept of reactive programming, enabling data changes to be directly reflected on the UI without requiring manual handling by the developer.

Since each reactive property is automatically bound to the relevant parts of the UI, the UI updates automatically when the property value changes, eliminating the need to call property update functions on specific elements.

For example, defining a reactive property named `counter`:
``` js
export default {
  data: { // Define the counter reactive property in the data object
    counter: 0 // Initial value is 0
  }
}
```

Whenever the value of `counter` changes, the UI referencing this property will also update automatically. The following [template](template) code demonstrates this mechanism:
``` html
<p on:click="counter += 1">
  counter: {{ counter }}
</p>
```
This example demonstrates a counter where clicking the `<p>` tag increments the displayed value of `counter` by 1. You can click the online demo below to test it:

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

`{{ counter }}` inside the `<p>` tag is a template [interpolation expression](template.md#interpolation-expression), and its dependency on `counter` is automatically bound. Meanwhile, the [`on:click` listener](/framework/commands/on.md) on the `<p>` tag modifies the `counter` property value upon clicking. As you can see, automatic data binding eliminates the manual **data**-to-**UI** update operations typical of traditional GUI development, making UI logic cleaner and more straightforward.

## `data` Property

The `data` property is used to declare reactive data properties of a component. This property is an object, for example:
``` js
export default {
  data: {
    text: "Hello world"
  }
}
```
The value of the `data` property must be serializable via `JSON.stringify()`. Specifically, it must meet the following conditions:
- Primitive types: `number`, `string`, `boolean`, `null`, or `undefined`
- For recursively structured `Object`s and `Array`s, the values of the deepest elements must belong to one of the types above.

This means that the properties of the `data` object in the source code cannot contain functions or other special types of values, which also includes objects like `Date`.

::: note
The `data` object does not support non-JSON-compatible data types, such as `Date`, `Proxy` objects, etc.; this is a known limitation. If you need to use these types of data, you can define them as [custom properties](#custom-properties); otherwise, it will lead to unexpected behavior.
:::

All properties in the `data` property are view-model properties of the component, so the data within can be used for reactive programming. You can directly access properties in the `data` object inside the component object using `this.prop`. Therefore, in the following component object:
``` js
export default {
  data: {
    onInit: true
  },
  onInit() {}
}
```
The code `this.onInit` will access the `onInit` property inside the `data` object, rather than the `onInit` lifecycle function.

::: tip
To optimize performance, only define data used for UI rendering and state management in the `data` object. For non-reactive data, you can define them as [custom properties](#custom-properties). For example: timer IDs (return value of `setTimeout()`), [audio player](/api/system-media.md#createaudioplayer) handles, WebSocket connection objects, etc. Such objects generally do not need to be reactive properties and will not function correctly if they are.
:::

## `computed` Property

The `computed` property object of a component object declares computed properties within the component. Compared to reactive properties in `data`, computed properties can implement properties that require some calculation to obtain their results. For example:
``` html
<text> reversed message: {{ reversedMessage }}
```

``` js
export default {
  data: {
    message: "hello"
  },
  computed: {
    reversedMessage() { // This is the getter method for the reversedMessage computed property
      return this.message.split('').reverse().join('')
    }
  }
}
```
Here, a `reversedMessage` computed property is declared, implementing a getter function to retrieve the property value. You can directly use `this.reversedMessage` (the `this.` can be omitted in templates) to get the value of this computed property.

Computed properties are also view-model properties of the component. The values of computed properties are cached, so retrieving a computed property's value multiple times will not trigger recalculations. On the other hand, computed properties are automatically updated when their dependent view-model properties change. In this example, the value of the computed property is calculated from the `message` property, so when the `message` property changes, the value of `reversedMessage` will automatically update.

### Computed Property Setter Method

By default, computed properties only have a getter method, but you can also provide a setter method for a computed property:
``` js
export default {
  data: {
    message: "hello"
  },
  computed: {
    reversedMessage: {
      get() { // This is the getter method for the reversedMessage computed property
        return this.message.split('').reverse().join('')
      },
      set(value) {
        this.message = value.split('').reverse().join('')
      }
    }
  }
}
```
In this case, the value of the `reversedMessage` computed property is no longer a function, but an object containing two methods: a getter method `get` and a setter method `set`. The parameter of the `set` method is the new value to be set for the computed property.

## `watch` Property

The `watch` object method is used to watch for changes in view-model properties, for example:
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
Methods in the `watch` object monitor changes to view-model properties with the same name, so `watch.value()` watches for changes to the `value` property. Changes to computed properties can also be watched by `watch`.

## Lifecycle Functions

See the [Lifecycle](life-cycle.md) documentation for details.

## Custom Properties

Users can also define custom properties in the component object. These properties are not in the view-model (i.e., not in the `data` or `computed` objects) and are therefore not reactive. Developers can define methods as custom properties and use custom properties to store data that does not require reactivity. For example:
``` html
<p on:click="onClick()">{{ text }}</p>
```

``` js
export default {
  data: {
    text: "some text"
  },
  // Custom properties are not in data or computed objects, defined directly within the component object
  timer: null, // Stores the timer handle; does not need to be predefined, assigning to this.timer creates this property automatically
  onInit() {
    // New properties assigned to this are custom properties
    this.timer = setInterval(() => this.text += "?", 1000)
  },
  onDestroy() {
    clearInterval(this.timer)
  },
  onClick() {
    this.text += "." // Operate on view-model properties within custom methods
  }
}
```

In the example, the `text` property is reactive, while `timer` is a non-reactive custom property. The `timer` property is used to store the timer handle. This value has nothing to do with the UI view, so it does not need to be a view-model property. For code standardization, custom properties can also be predefined in the component object:
``` js
export default {
  data: {
    text: "some text"
  },
  timer: null, // Custom properties are direct properties of the component object
  // ...
}
```
As shown in the example, custom properties can be defined directly inside the component object. The custom properties of each component are separate instances and are not shared.

::: warning
Custom properties, the `data` object, the `computed` object, lifecycle functions, and other properties must not share duplicate names; otherwise, some properties will be overwritten and become inaccessible.
:::

### Methods

Custom properties and methods are both direct properties of the component object, and the two are essentially equivalent. When you assign a function to a property of a component object, that property becomes a method. This section demonstrates this equivalence through two examples.

Approach 1: Define methods directly, which is the most common and recommended writing style.
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

Approach 2: Define a property and assign a function to it.
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
Both writing styles are functionally identical and can be called via `this.increment()`. They are also used identically within templates:
``` html
<button on:click="increment()">Count: {{ count }}</button>
```

::: tip
It is recommended to use Approach 1. This is the object method syntax supported by the ES6+ standard, making it more concise and straightforward.
:::

### Dynamically Assigning Methods

In addition to directly defining methods in the component object, you can also dynamically assign methods after the component is instantiated (e.g., in the `onInit` lifecycle). The key feature of this approach is that the dynamic methods of each component instance are independent and can capture and maintain different states via closures.

Consider a timer component where each instance has its own counter and can be stopped independently. This is a typical use case for dynamically assigned methods:
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
  stopTimer: null, // Optional: Predefine the stopTimer method
  onInit() {
    const timer = setInterval(() => {
      this.counter++
    }, 1000)
    // Dynamically create the stopTimer method, capturing the timer variable through a closure
    this.stopTimer = () => {
      clearInterval(timer)
      this.stopTimer = null // Set the method to null after stopping
    }
  },
}
```

The following example instantiates 4 timer components simultaneously, and you can try stopping any of them independently:

<glyphix id="component-object-dynamic-method" height="200" width="300" inline>
</glyphix>

The implementation of this dynamic assignment method relies on the following key points:
- **Closure capture**: The `timer` constant created in `onInit` is a local variable, and the `stopTimer` method captures this variable via a closure.
- **Instance independence**: Each component instance creates its own `timer` and `stopTimer` when `onInit` is called, and they do not interfere with each other.
- **State isolation**: Clicking the "Stop" button of a specific instance only stops that instance's timer without affecting other instances.

Of course, for this example, a more common approach is to define the `stopTimer` method directly in the component object:
``` js
export default {
  data: {
    counter: 0,
  },
  timer: null,
  onInit() {
    // In this case, timer needs to be stored as a custom property
    this.timer = setInterval(() => {
      this.counter++
    }, 1000)
  },
  stopTimer() {
    // The stopTimer method accesses this.timer to stop the timer
    clearInterval(this.timer)
    this.timer = null // Clear the timer reference
  }
}
```
This is generally more intuitive for timers, but in some scenarios with complex contexts that require dynamic dispatch strategies, dynamic method assignment can be used to implement more flexible logic. The table below shows the differences between dynamic methods vs. directly defined methods:

| Feature | Directly Defined Methods | Dynamically Assigned Methods |
|---------|-------------------------|-----------------------------|
| Shareability | All instances share the same function object | Each instance has an independent function copy |
| Closure Capture | Does not capture local variables in the scope | Can capture local variables in the scope |
| Memory Footprint | Less (shared) | Slightly more (one per instance) |
| Applicable Scenarios | General, stateless operations | Operations requiring local state capture |