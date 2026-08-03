---
icon: information-outline
---
# Component basics

The previous document "[Quick Start](getting-started)" briefly introduced the concept of components. This tutorial will further explain the knowledge about components. Before reading this document, you need to know how to create and build a project, and how to edit source files. If you don't know, please read the "[Quick Start](getting-started)" tutorial.

## Introduction

In Glyphix application development, all interfaces are components - from buttons to pages. Component technology allows the development of interfaces using simple template languages:
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
This is basically the `main/index.ux` file of the default project template. Use the `gx emu` command to observe the display effect. The content in the `<template>` tag is the component's template, which describes the appearance of the component. Here, the `<p>` node will display the `text` property from the component model object. Please note that the component framework internally associates the content of the `<p>` node with the `text` attribute of the component model. As long as the value of the `text` attribute is modified, the interface will be updated synchronously.

We can test this with a timer:
``` js
export default {
  data: { text: "begin!" },
  onInit() {
    let count = 0
    setInterval(() => this.text = "timeout: " + count++, 1000)
  }
}
```
You will now see that the displayed count increases by 1 every second.

## Programming model of components

An important function of GUI programs is to change their appearance based on data and input to achieve interaction. In traditional GUI programming and native HTML, developers need to find the target element node in the interface tree and then call the API to update it. It turns out that developing interfaces in this way will be very complicated. Therefore, there are design patterns suitable for GUIs such as MVC, MVP, and MVVM, and some new frameworks have emerged in the field of Web development. These technologies have greatly reduced the difficulty of interface development.

The programming model of Glyphix components is very similar to front-end frameworks like Vue. The basic idea of ​​these frameworks is to calculate a new interface based on the state of the interface model, rather than requiring interface elements to be updated when the state changes. Compared with traditional technology, the interface view part in this solution is stateless and therefore simpler. Let's continue using the previous example:
``` html
<template>
  <p>{{ text }}</p>
</template>
```
We already know that the interface will automatically update when the `text` property of the component model is updated. However, in traditional GUI frameworks, it is often necessary to manually update the `<p>` node after the `text` of the model is updated (which usually comes from changes in input or internal data). Frameworks such as MVC can simplify these operations, but they are not very concise.

Now consider a very simple approach: we write a `render()` function that generates an interface tree based on the current state of the model. If we replace the original interface tree with the value of the `render()` function every frame, then any changes to the model will be reflected in the interface. This solution is very simple, but you will deny it because of the efficiency. In fact, it was to solve the efficiency problem of this solution that the traditional GUI programming model was born: only modified elements in the interface are modified, but it introduces state in the view layer and also brings a lot of complexity.

The Glyphix component framework is based on this simple concept: the content in the `<template>` tag implements the function of the `render()` function, while the js code focuses on maintaining the model, and data changes in the model will automatically be reflected in the relevant interfaces. You can think of the Glyphix component framework as always calculating a new interface based on the state of the model, so we don't have to manually update interface elements.

::: tip
The bottom layer of Glyphix is not a DOM tree, and naturally there is no API for operating DOM elements. In fact, the component framework is the native Glyphix JavaScript API.
:::

## Respond to input

There are some components that can respond to user input events. In this case, you can use the `on` directive to specify an event listener. For example, listen for click events on the text component:
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
Clicking on the text will automatically update the display. The value of the `on:click` attribute `text += ' click'` is a JavaScript expression, and Glyphix will automatically bind the `this` of the variable in the expression to the component object.

## Conditional rendering

The `if` directive is used to render component content conditionally. The content area controlled by this directive will be rendered only when the value of the expression in the `if` directive is true.
``` html
<p if="display">Hello World</p>
```

The following example will implement a mutually exclusive switch effect. When clicked continuously, the interface will alternately display the text "Component A" or "Component B".
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

## List rendering

Use the `for` directive to repeatedly render a component to generate a list. The basic usage of the `for` directive is:
``` html
<p for="(index, value) in list">{{index}}: {{value}}</p>
```
Among them, `list` is a list attribute in the component model (must be of type `Array`), `index` and `value` are two iteration variables, the value of `index` is the index of the current item, and the value of `value` is the value of the current item.

The `for` directive can be abbreviated to the following forms:
``` html
<p for="list">{{$idx}}: {{$item}}</p>
<p for="value in list">{{$idx}}: {{value}}</p>
<p for="index, value in list">{{$idx}}: {{value}}</p>
```
The first abbreviation is to only write the expression that needs to be iterated, in which case `$idx` and `$item` will be used as the default iteration variable names; the second way of writing explicitly defines the iteration variable of the current value, and the current index variable name uses the default `$idx`; the third way of writing is the abbreviation of the standard way of omitting parentheses.

::: tip
Due to the scope relationship, the variables used iteratively when writing the `for` directive will only take effect when used after the `for` directive.
:::

``` html
<!-- correct -->
<button for="list" text="{{$item}}"/>
<!-- error -->
<button text="{{$item}}" for="list"/>
```

### Use both `if` and `for` directives

You can use both the `if` and `for` directives on an element, in which case the `if` directive has higher priority. In this example, when the `display` property is false, the entire `button` component list will not render:
```html
<button for="value in items" if="display">Hello {{value}}</button>
<p if="!display">Paragraph 1</p>
```

And if your purpose is to conditionally render some nodes in the list generated by the `for` directive, you need to place the `if` directive on the inner element of the `for` directive.
```html
<button for="value in items">
  <p if="display">item: {{value}}</p>
</button>
```

::: tip
Using the `if` and `for` directives on the same element is not recommended as it reduces code readability.
:::

## slot

Similar to the content distribution of other frameworks, Glyphix also implements a set of content distribution APIs. We can use the `slot` component as an outlet to carry distributed content.

In the child component, use the `slot` component to host the content defined in the parent component. The `slot` component will become the element passed in by the parent component when rendering.

```html
<div>
  <slot/>
</div>
```

## Use components in combination

Combining multiple components into a larger interface is the Glyphix component framework's approach to interface building. If there is a component named `Menu`, you can import it by using the `<import>` tag under the root node of the UX file that needs to be referenced:
``` html
<import src="path/to/Menu" name="Menu"/>
```
The `src` attribute is the path of the component, do not add the `.ux` suffix. The `name` attribute is an optional component name. If this attribute is not filled in, the component's file name will be used as the component name.

Use the `<import>` tag multiple times to import all dependent components:
``` html
<import src="path/to/ComA"/>
<import src="path/to/ComB"/>
<import src="path/to/ComC"/>
```

Custom components can be used just like native components:
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

This is a menu interface. We hope that when the user clicks on the menu, the information of the current menu item will be printed through the `clickMenu` method. Therefore, the `Menu` component needs to be able to display menu content and be able to monitor its own click event through `on:click`.

This is the content of the `Menu.ux` file:
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
We simply use a native component `div` to respond to user clicks and report them. The `div` component will also display the subcomponent passed in last time, finally allowing the menu list to be displayed.