---
icon: information-outline
---
# Component Basics

The previous document, "[Getting Started](getting-started)", briefly introduced the concept of components. This tutorial will further explain components in detail. Before reading this document, you need to know how to create and build a project, as well as how to edit source files. If you are not familiar with these, please read the "[Getting Started](getting-started)" tutorial.

## Introduction

In Glyphix application development, all user interfaces are components—ranging from a button to an entire page. Component technology allows you to develop interfaces using a simple template language:
``` html
<!-- main/index.ux -->
<template>
  <p>{{text}}</p>
</template>

<style>
  * {
    text-align: center;
  }
</style>

<script>
  export default {
    data: {
      text: "Hello, World!"
    }
  }
</script>
```
This is basically the `main/index.ux` file of the default project template. You can use the `gx emu` command to observe the display effect. The content inside the `<template>` tag is the component's template, which describes its appearance. Here, the `<p>` node will display the `text` property from the component's model object. Please note that the component framework internally associates the content of the `<p>` node with the `text` property of the component model. Whenever the value of the `text` property is modified, the interface will be updated synchronously.

We can test this using a timer:
``` js
export default {
  data: { text: "begin!" },
  onInit() {
    let count = 0
    setInterval(() => this.text = "timeout: " + count++, 1000)
  }
}
```
Now, you will see the displayed counter value increment by 1 every second.

## Programming Model of Components

An important function of GUI programs is to change their appearance based on data and input to achieve interaction. In traditional GUI programming and native HTML, developers need to find the target element node in the interface tree and then call APIs to update it. Experience has shown that developing interfaces this way can be very complex. As a result, design patterns suitable for GUIs—such as MVC, MVP, and MVVM—have emerged, and new frameworks have appeared in the web development field. All these technologies have greatly reduced the difficulty of interface development.

The programming model of Glyphix components is very similar to frontend frameworks like Vue. The basic idea of these frameworks is to compute the new interface based on the state of the interface model, rather than requiring you to update interface elements when the state changes. Compared to traditional technology, the view part of the interface in this approach is stateless and therefore much simpler. Let's continue using the previous example to explain:
``` html
<template>
  <p>{{ text }}</p>
</template>
```
As we already know, when the `text` property of the component model updates, the interface will automatically update. However, in traditional GUI frameworks, it is often necessary to manually update the `<p>` node after the model's `text` updates (which generally comes from user input or internal data changes). Frameworks like MVC can simplify these operations, but they are not very concise.

Now consider a very simple method: we write a `render()` function that generates an interface tree based on the current state of the model. If we replace the original interface tree with the value of the `render()` function on every frame, any changes to the model will be reflected in the interface. This approach is very simple, but you might reject it due to efficiency concerns. In fact, traditional GUI programming models were born precisely to solve the efficiency problem of this approach: modifying only the elements in the interface that have changed, but this introduces state into the view layer and brings a lot of complexity.

The Glyphix component framework is based on this simple concept: the content inside the `<template>` tag implements the functionality of the `render()` function, while the JS code focuses on maintaining the model, and data changes in the model are automatically reflected in the relevant interface. You can think of the Glyphix component framework as always calculating the new interface based on the model's state, so we do not need to manually update interface elements.

::: tip
Underneath, Glyphix does not use a DOM tree, and naturally, there are no APIs for manipulating DOM elements. In fact, the component framework itself is the native Glyphix JavaScript API.
:::

## Responding to Input

Some components can respond to user input events. In this case, you can use the `on` directive to specify event listeners. For example, listening to a click event on a text component:
``` html
<template>
  <p on:click="text += ' click'">{{text}}</p>
</template>

<style>
  * {
    text-align: center;
  }
</style>

<script>
  export default {
    data: {
      text: "Text "
    }
  }
</script>
```
Clicking the text will automatically update the displayed content. The value of the `on:click` attribute, `text += ' click'`, is a JavaScript expression, and Glyphix automatically binds `this` for the variables in the expression to the component object.

## Conditional Rendering

The `if` directive is used to conditionally render component content. The content area controlled by this directive will only be rendered when the value of the expression in the `if` directive is true.
``` html
<p if="display">Hello World</p>
```

The following example implements a mutually exclusive toggle effect. Clicking continuously will cause the interface to alternately display "Component A" or "Component B".
``` html
<template>
  <p if="display" on:click="display = false">Component A</p>
  <p if="!display" on:click="display = true">Component B</p>
</template>

<style>
  * {
    font-size: 48;
    text-align: center;
  }
</style>

<script>
  export default {
    data: {
      display: true
    }
  }
</script>
```

## List Rendering

Use the `for` directive to repeatedly render a component to generate a list. The basic usage of the `for` directive is:
``` html
<p for="(index, value) in list">{{index}}: {{value}}</p>
```
Where `list` is a list property in the component model (must be of type `Array`), and `index` and `value` are two iteration variables. The value of `index` is the index of the current item, and the value of `value` is the value of the current item.

The `for` directive can be abbreviated into the following forms:
``` html
<p for="list">{{$idx}}: {{$item}}</p>
<p for="value in list">{{$idx}}: {{value}}</p>
<p for="index, value in list">{{$idx}}: {{value}}</p>
```
The first abbreviation only writes the expression to be iterated; in this case, `$idx` and `$item` are used as the default iteration variable names. The second form explicitly defines the iteration variable for the current value, while using the default `$idx` for the current index variable name. The third form is the standard syntax with parentheses omitted.

::: tip
Due to scoping rules, the iteration variables used when writing a `for` directive will only take effect if used *after* the `for` directive.
:::

``` html
<!-- correct -->
<button for="list" text="{{$item}}"/>
<!-- error -->
<button text="{{$item}}" for="list"/>
```

### Using `if` and `for` Directives Simultaneously

You can use both `if` and `for` directives on the same element, in which case the `if` directive has higher priority. In this example, when the `display` property is false, the entire list of `button` components will not be rendered:
```html
<button for="value in items" if="display">Hello {{value}}</button>
<p if="!display">Paragraph 1</p>
```

If your intention is to conditionally render specific nodes within the list generated by the `for` directive, you need to place the `if` directive on an inner element of the `for` directive.
```html
<button for="value in items">
  <p if="display">item: {{value}}</p>
</button>
```

::: tip
It is not recommended to use the `if` and `for` directives on the same element because this reduces code readability.
:::

## Slots

Similar to content distribution in other frameworks, Glyphix also implements a content distribution API. We can use the `slot` component as an outlet for distributed content.

In a child component, use the `slot` component to host the content defined in the parent component. The `slot` component will render as the element passed in by the parent component.

```html
<div>
  <slot/>
</div>
```

## Combining Components

Combining multiple components into a larger interface is the way user interfaces are built in the Glyphix component framework. Suppose there is a component named `Menu`; you can import it by using the `<import>` tag under the root node of the UX file that needs to reference it:
``` html
<import src="path/to/Menu" name="Menu"/>
```
The `src` attribute is the path of the component, please do not include the `.ux` suffix. The `name` attribute is an optional component name; if this attribute is omitted, the component's filename will be used as its name.

Use the `<import>` tag multiple times to import all dependent components:
``` html
<import src="path/to/ComA"/>
<import src="path/to/ComB"/>
<import src="path/to/ComC"/>
```

You can use custom components just like native components:
``` html
<div>
  <menu for="menus" on:click="clickMenu($idx, $item)">
    <p>Menu {{$item}}</p>
  </menu>
</div>
```

``` css
div {
  display: flex;
  flex-direction: column;
}

text {
  text-align: center;
}
```

``` js
export default {
  data: {
    menus: ["Dog", "Cat", "Pig", "Fish"],
  },
  clickMenu(id, name) {
    console.log(`clicked id: ${id}, name: ${name}.`)
  }
}
```

This is a menu interface. We want to print the information of the current menu item via the `clickMenu` method when the user clicks the menu. Therefore, the `Menu` component needs to be able to display the menu content and listen to its own click event via `on:click`.

Here is the content of the `Menu.ux` file:
``` html
<template>
  <div on:click="$emit('click')"> <slot /> </div>
</template>

<style>
  div { display: flex; }
</style>

<script>
  export default {}
</script>
```
We simply use a native `div` component to respond to the user's click and report it upward. Inside the `div` component, the child components passed from the parent will also be displayed, ultimately making the menu list visible.