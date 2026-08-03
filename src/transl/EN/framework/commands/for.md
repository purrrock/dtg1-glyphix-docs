---

icon: format-list-bulleted

---

# for directive


The `for` directive is used for list rendering.


## grammar


``` html
<div for="expr"></div> <!-- Subscript and iteration variables are not defined -->
<div for="value in expr"></div> <!-- Do not define subscript variables -->
<div for="index, value in expr"></div>
<div for="(index, value) in expr"></div>
```
The value expressed by `expr` is a [`Array` object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array) or numerical value. The `for` instruction will traverse the entire list and pass the subscript value and the value of the iterated item during the iteration process. If you do not define a subscript variable or an iteration variable, the default name is `$idx` for the subscript variable and `$item` for the iteration variable.


When the `for` instruction and the `if` instruction exist at the same time, the `if` instruction has a higher priority. This means that if the `if` directive evaluates to false, the entire list will not be rendered.


Attribute values ​​of the `for` directive support the [directive attribute value](/framework/component/template.md#指令属性值) syntax, so double curly braces can also be used to surround expressions.


::: warning

It is not recommended to use the `if` and `for` instructions together to improve code readability.
:::



## List rendering


Render a [JavaScript array](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/First_steps/Arrays) as a list via the `for` directive. It is usually used on subcomponents of [`scroll`](/components/scroll.md), for example:
``` html
<scroll :damping="damping">
  <p for="item in items" class="item">
    {{ item.message }}
  </p>
</scroll>
```
The `for` directive on the `p` component iterates through the `items` array and generates a `p` component node for each iterated item. `item` is the variable name of the iteration item, and its `message` attribute is accessed in `{{ item.message }}` [interpolation expression](/framework/component/template.md#插值表达式).


`items` is an array of type [Component object properties](/framework/component/component-object.md), for example:
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



The rendered result is a scrollable list containing three entries, the contents of which are "Foo", "Bar" and "Baz". You can use the `for` directive on native [components](/framework/component/README.md) or custom components to implement list rendering.


You can also use the default `$item` iteration variable name:
``` html
<scroll :damping="damping">
  <p for="items" class="item">
    {{ $item.message }}
  </p>
</scroll>
```
The rendering result is the same as above.


## Nesting and scoping


In the same label, subscripts and iteration variables must be accessed after the `for` directive, so you need to pay attention to the order of related attributes:
``` html
<panel for="value in expr" title="value.title"></panel> <!-- correct -->
<panel title="value.title" for="value in expr"></panel> <!-- mistake -->
```
The wrong order will not cause a compile error, but instead try to find the `value` attribute in the `this` scope. In other words, variables defined in the `for` directive will hide the names of the outer scope, including:
- The component’s view-model (i.e. accessed via the `this` attribute)
- global object


Taking into account issues with variable scope and directive precedence, the `if` directive should precede the `for` directive, otherwise confusing behavior may occur.


For the current component node, variables defined in the `for` directive are only visible in the attributes after it. Also visible in static subcomponents, e.g.
``` html
<panel for="value in expr" title="value.title">
  <p>message: {{value.message}}</p>
</panel>
<p>{{value.message}}</p> <!-- At this time access this.value.message -->
```
Except for the last `{{value.message}}` expression, several other `value` are within the scope of the `for` directive.


The `for` directive can be nested and the scope rules are the same as above. Note that the scope of subscripts and iteration variables with the same name will be hidden by the inner `for` directive, so these variables need to be defined explicitly.


## Array change detection


The `for` instruction can detect changes in the [Responsive](/framework/component/component-object.md#响应式编程) array and update the interface. The following operations will trigger `for` rendering updates:
- Replace with a new array;
- Call array update methods such as [`push()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/push), [`pop()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/pop), [`shift()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/shift), [`unshift()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/unshift), [`splice()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/splice), [`sort()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/sort) and [`reverse()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/reverse).


### replace an array


The reactive property used for list rendering can be replaced with a new array to trigger UI updates. For example:
``` js
this.items = this.items.filter((item) => item.message.match(/Foo/))
```
In this way, `this.items` is assigned a new array, and the `for` directive will re-render the new list after this operation.


::: tip

Arrays have some immutable methods, such as `filter()`, `concat()` and `slice()`, which do not change the original array but always return a new array. When encountering immutable methods, you need to use the above method to replace the old array with the new one.
:::



### Array update method


View updates can also be triggered using the update method of an array, for example:
``` js
// Insert a new element with the content Grault at the bottom of the original list
this.items.push({ message: 'Grault' })
```


You can also directly modify the array length to truncate the array, such as:
``` js
// Remove elements after the third item in the list
this.items.length = 2
```


You can also change elements of the list:
``` js
// Change the second element content to Gault
this.items[1] = { message: 'Grault' }
```


::: warning

The `for` directive currently cannot track attribute changes of list elements, see [List element update](#列表元素更新) for details.
:::



## Defects and Limitations


### List element update


The `for` directive cannot listen for deep property updates of array items, which means
``` js
this.items[1].message = 'Grault'
```
Interface updates will not be triggered correctly. To solve this problem, the array item must be replaced with a new object:
``` js
this.items[1] = { message: 'Grault' }
```


When the project object has many attributes, but only wants to update a few of them, it is recommended to use [Expand syntax (`...`)](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to copy the object first, and then update the attributes:
``` js
this.items[1] = {
  ...this.items[1], // Copy all attributes of the second element
  message: 'Grault' // Update message attribute
}
```


::: warning

The number of attributes of the array item object will have an impact on performance. When you find that the list update is stuck, please see [unnecessary updates](#不必要的更新).


Due to reasons such as other elements in the interface being updated together, the interface may be updated after directly changing the deep properties of the project, but this is not stable, please do not use it like this.
:::



### List subscript problem


Although the `for` instruction supports obtaining the project subscript during rendering, such as:
``` html
<p for="index, value in items">
  {{ index }} - {{ value }}
</p>
```
However, responsive updating of subscripts is currently not supported, and modifications to the `items` array may cause display confusion. Updating the entire array avoids this problem.


However, due to some optimization mechanisms, it is difficult for developers to ensure that the entire `items` array is actually updated, which can lead to strange unexpected subscript confusion problems.


### unnecessary updates


List rendering can be one of the bottlenecks for fluency and performance, especially long lists that can be slower to render. Reducing unnecessary list updates may be an effective optimization method.


#### Update list directly


Consider a list like this:
``` html
<div for="(idx, task) in tasks" on:click="process(idx)">
  <p>{{ task.name }}</p>
  <p>{{ task.progress }}%</p>
</div>
```
This is a task processing interface that displays a list of tasks and processes a task when the user clicks on it. For simplicity, we initialize the task list like this:
``` js
this.tasks = Array.from({ length: 10 },
  (_, i) => ({ name: `Task #${i + 1}`, progress: 0 }))
```
At this point you will see a to-do list with 10 items. The following `process()` method simply updates the task progress:
``` js
process(idx) { // idx is the index of the clicked task item
  this.tasks[idx].progress = 0
  // Create a timer to simulate processing progress
  let timer = setInterval(() => {
    // Since the for instruction does not support deep attribute updates, copy an object first
    let task = {...this.tasks[idx]}
    task.progress += 10
    this.tasks[idx] = task
    if (task.progress >= 100)
      clearInterval(timer) // Delete timer when processing is complete
  }, 100)
}
```
As shown below, this implementation can interact normally.


<glyphix id="commands-for-tasklist-1" height="360" width="360" title="任务清单列表">


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



This simple method may become laggy in complex and long list interfaces. At this time, you may observe:
- Frames dropped in animations such as progress in the interface;
- Scrolling up and down the list becomes noticeably laggy.


#### Optimize through subcomponents


One optimization method is to split the project into an independent component, in this example you can add a `Task` component:
``` html
<div on:click="process">
  <p>{{ name }}</p>
  <p>{{ progress }}%</p>
</div>
```
The `Task` component's JavaScript script can handle its own `process()` operations:
``` js
export default {
  data: {
    name: null, // The task name must be passed in from the outer layer
    progress: 0
  },
  // Each Task component object will handle its own process operation,
  // And access your own reactive properties through this.
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


Compared with the previous method, the new scheme can be used directly after [Introduce `Task` component](/framework/component/README.md#引入组件):
``` html
<task for="task in tasks" :name="task.name" />
```
The JavaScript code of the parent component can also be simpler:
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
This has the following changes compared to updating the list directly:
- The inserted array item does not have a `progress` attribute because it only needs to be processed in the `Task` subcomponent;
- The `process()` method was removed and moved to the `Task` component;
- There is no need to use the `idx` subscript variable to distinguish different items.


This method can implement the same task list interface, except that the processing of `progress` is moved to the `Task` subcomponent, thereby avoiding updating the task array when the progress is modified. Using this method can optimize the internal interface update problem of list elements and reduce code complexity.