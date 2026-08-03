---
icon: format-list-bulleted
---
# for Directive

The `for` directive is used for list rendering.

## Syntax

``` html
<div for="expr"></div> <!-- Without index and iteration variables defined -->
<div for="value in expr"></div> <!-- Without index variable defined -->
<div for="index, value in expr"></div>
<div for="(index, value) in expr"></div>
```
The value expressed by `expr` is an [`Array` object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array) or a number. The `for` directive traverses the entire list and passes the index value and the iteration item value during the iteration process. If neither the index variable nor the iteration variable is defined, the default name for the index variable is `$idx`, and the default name for the iteration variable is `$item`.

When both the `for` directive and the `if` directive are present on the same element, the `if` directive has higher priority. This means that if the `if` directive evaluates to falsy, the entire list will not be rendered.

The attribute value of the `for` directive supports the [directive attribute value](/framework/component/template.md#directive-attribute-values) syntax, so expressions enclosed in double curly braces can also be used.

::: warning
It is not recommended to use the `if` and `for` directives simultaneously in order to improve code readability.
:::

## List Rendering

Render a [JavaScript array](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/First_steps/Arrays) into a list using the `for` directive. It is typically used on child components of [`scroll`](/components/scroll.md), for example:
``` html
<scroll :damping="damping">
  <p for="item in items" class="item">
    {{ item.message }}
  </p>
</scroll>
```
The `for` directive on the `p` component iterates over the `items` array and generates a `p` component node for each iteration item. `item` is the variable name for the iteration item, and its `message` property is accessed in the `{{ item.message }}` [interpolation expression](/framework/component/template.md#interpolation-expressions).

`items` is a [component object property](/framework/component/component-object.md) of array type, for example:
``` js
export default {
  data: {
    items: [
      { message: 'Foo' },
      { message: 'Bar' },
      { message: 'Baz' },
    ]
  }
}
```

This code will render the following interface:

<glyphix id="commands-for-1" height="200" width="360" inline>

``` html
<scroll :damping="damping">
  <p for="item in items" class="item">
    {{ item.message }}
  </p>
</scroll>
```

``` js
export default {
  data: {
    items: [
      { message: 'Foo' },
      { message: 'Bar' },
      { message: 'Baz' },
    ]
  }
}
```

``` css
scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
}

.item {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 40px 10px;
  margin: 10px;
  border-radius: 16px;
}
```

</glyphix>

The rendering result is a scrollable list containing three items with the contents "Foo", "Bar", and "Baz". You can use the `for` directive on native [components](/framework/component/README.md) or custom components to achieve list rendering.

You can also use the default `$item` iteration variable name:
``` html
<scroll :damping="damping">
  <p for="items" class="item">
    {{ $item.message }}
  </p>
</scroll>
```
The rendering result of this is the same as above.

## Nesting and Scoping

Within the same tag, the index and iteration variables can only be accessed after the `for` directive, so you need to pay attention to the order of related attributes:
``` html
<panel for="value in expr" title="value.title"></panel> <!-- Correct -->
<panel title="value.title" for="value in expr"></panel> <!-- Incorrect -->
```
The incorrect order will not cause a compilation error, but will instead attempt to look up the `value` property in the `this` scope. In other words, variables defined in the `for` directive will shadow names in the outer scope, which include:
- The component's view-model (i.e., accessed via properties of `this`)
- Global objects

Considering variable scoping and directive priority issues, the `if` directive should be placed before the `for` directive, otherwise it may lead to confusing behavior.

For the current component node, variables defined in the `for` directive are only visible in attributes that appear after it. They are also visible in static child components, for example:
``` html
<panel for="value in expr" title="value.title">
  <p>message: {{value.message}}</p>
</panel>
<p>{{value.message}}</p> <!-- Accessing this.value.message here -->
```
Except for the last `{{value.message}}` expression, the `value` in all other places is within the scope of the `for` directive.

The `for` directive can be nested, and the scoping rules in this case are the same as above. Note that index and iteration variables with the same name will be shadowed by the inner `for` directive, so these variables need to be explicitly defined.

## Array Change Detection

The `for` directive can detect changes in [reactive](/framework/component/component-object.md#reactive-programming) arrays and update the interface. The following operations will trigger `for` rendering updates:
- Replacing with a new array;
- Calling array mutation methods, such as [`push()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/push), [`pop()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/pop), [`shift()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/shift), [`unshift()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/unshift), [`splice()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/splice), [`sort()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/sort), and [`reverse()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/reverse).

### Replacing an Array

You can trigger an interface update by replacing the reactive property used for list rendering with a new array. For example:
``` js
this.items = this.items.filter((item) => item.message.match(/Foo/))
```
In this way, `this.items` is assigned a new array, and the `for` directive will re-render the new list after this operation.

::: tip
Arrays have some immutable methods, such as `filter()`, `concat()`, and `slice()`, which do not mutate the original array but always **return a new array**. When encountering immutable methods, you need to use the method above to replace the old array with the new one.
:::

### Array Mutation Methods

Using array mutation methods can also trigger view updates, for example:
``` js
// Insert a new element with content 'Grault' at the bottom of the original list
this.items.push({ message: 'Grault' })
```

You can also truncate the array by directly modifying its length, such as:
``` js
// Remove elements after the third item in the list
this.items.length = 2
```

You can also change elements of the list:
``` js
// Change the content of the second element to 'Grault'
this.items[1] = { message: 'Grault' }
```

::: warning
The `for` directive currently cannot track property mutations of list elements. See [List Element Updates](#list-element-updates) for details.
:::

## Caveats and Limitations

### List Element Updates

The `for` directive cannot listen for deep property updates of array items, meaning that
``` js
this.items[1].message = 'Grault'
```
will not correctly trigger an interface update. To solve this problem, you must replace the array item with a new object:
``` js
this.items[1] = { message: 'Grault' }
```

When an item object has many properties, but you only want to update a few of them, it is recommended to first copy the object using the [Spread syntax (`...`)](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Spread_syntax), and then update the properties:
``` js
this.items[1] = {
  ...this.items[1], // Copy all properties of the second element
  message: 'Grault' // Update the message property
}
```

::: warning
The number of properties on array item objects will impact performance. When you notice lag in list updates, please refer to [Unnecessary Updates](#unnecessary-updates).

Due to reasons such as other elements in the interface updating simultaneously, directly mutating deep properties of an item might sometimes update the interface, but this is unstable; please do not use it this way.
:::

### List Index Issues

Although the `for` directive supports getting the item index during rendering, such as:
``` html
<p for="index, value in items">
  {{ index }} - {{ value }}
</p>
```
It currently does not support reactive index updates. Modifications to the `items` array may lead to display disorders. Updating the entire array can avoid this problem.

However, due to certain optimization mechanisms, it is difficult for developers to guarantee that the entire `items` array is **truly** updated, which can lead to strange and unexpected index disorder issues.

### Unnecessary Updates

List rendering can be a bottleneck for fluency and performance, especially as rendering long lists can be slow. Reducing unnecessary list updates can be an effective optimization technique.

#### Direct List Updates

Consider a list like this:
``` html
<div for="(idx, task) in tasks" on:click="process(idx)">
  <p>{{ task.name }}</p>
  <p>{{ task.progress }}%</p>
</div>
```
This is a task processing interface that displays a task list and processes a specific task when the user clicks it. For simplicity, we initialize this task list like this:
``` js
this.tasks = Array.from({ length: 10 },
  (_, i) => ({ name: `Task #${i + 1}`, progress: 0 }))
```
At this point, you will see a task list containing 10 items. The following `process()` method simply implements task progress updating:
``` js
process(idx) { // idx is the index of the clicked task item
  this.tasks[idx].progress = 0
  // Create a timer to simulate processing progress
  let timer = setInterval(() => {
    // Since the for directive does not support deep property updates, copy an object first
    let task = {...this.tasks[idx]}
    task.progress += 10
    this.tasks[idx] = task
    if (task.progress >= 100)
      clearInterval(timer) // Delete the timer when processing is complete
  }, 100)
}
```
As shown below, this implementation can be interacted with normally.

<glyphix id="commands-for-tasklist-1" height="360" width="360" title="Task List">

``` html
<scroll>
  <div for="(idx, task) in tasks" on:click="process(idx)">
    <p>{{ task.name }}</p>
    <p>{{ task.progress }}%</p>
  </div>
</scroll>
```

``` js
export default {
  data: {
    tasks: []
  },
  onInit() {
    this.tasks = Array.from({ length: 10 },
      (_, i) => ({ name: `Task #${i + 1}`, progress: 0 }))
  },
  process(idx) {
    this.tasks[idx].progress = 0
    let timer = setInterval(() => {
      let task = {...this.tasks[idx]}
      task.progress += 10
      this.tasks[idx] = task
      if (task.progress >= 100)
        clearInterval(timer)
    }, 100)
  }
}
```

``` css
scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
}

div {
  color: #fafafa;
  background-color: #bdbdbd;
  display: flex;
  justify-content: space-between;
  padding: 40px 10px;
  margin: 10px;
  border-radius: 16px;
}
```

</glyphix>

This simple approach can become very laggy in complex and long list interfaces, at which point you might observe:
- Frame drops in animations such as progress bars in the interface;
- Noticeable stuttering when scrolling up and down the list.

#### Optimization via Child Components

An optimization method is to split the items into independent components. In this example, a `Task` component can be added:
``` html
<div on:click="process">
  <p>{{ name }}</p>
  <p>{{ progress }}%</p>
</div>
```
The JavaScript script of the `Task` component can handle its own `process()` operation:
``` js
export default {
  data: {
    name: null, // Task name needs to be passed in from the outside
    progress: 0
  },
  // Each Task component object will handle its own process operation,
  // and access its own reactive properties via this.
  process() {
    this.progress = 0
    let timer = setInterval(() => {
      this.progress += 10
      if (this.progress >= 100)
        clearInterval(timer)
    }, 100)
  }
}
```

Compared to the previous method, the new solution can be used directly after [importing the `Task` component](/framework/component/README.md#importing-components):
``` html
<task for="task in tasks" :name="task.name" />
```
And the parent component's JavaScript code can be simpler:
``` js
export default {
  data: {
    tasks: []
  },
  onInit() {
    for (let i = 0; i < 10; ++i)
      this.tasks.push({ name: `Task #${i + 1}` })
  }
}
```
Compared to updating the list directly, this brings the following changes:
- The inserted array items do not have a `progress` property, because it only needs to be handled within the `Task` subcomponent;
- The `process()` method has been removed and moved inside the `Task` component;
- There is no need to use the `idx` index variable to distinguish different items.

This approach achieves the same task list interface, but moves the handling of `progress` into the `Task` subcomponent, thereby avoiding updating the task array when modifying progress. Using this method can optimize the issue of internal interface updates for list elements while reducing code complexity.