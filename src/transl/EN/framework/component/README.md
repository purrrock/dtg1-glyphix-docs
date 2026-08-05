# Component Framework

Components are a technology in Glyphix used to achieve functional reuse in App UI development. By nesting HTML-like elements, multiple components can be combined to form the overall appearance and function of an interface. On the other hand, a certain amount of content and logic is encapsulated within each component, which, when used properly, can reduce code complexity and maintenance costs.

Components are divided into built-in [**native components**](../render/native-component.md) and **custom components** implemented by developers. Native components are generally encapsulations of UI elements, which can be used to display specific UI content or for layout and interaction, such as `text`, `image`, `div`, `list`, etc. Custom components, however, focus on logic implementation and functional encapsulation, because the interfaces implemented within custom components are ultimately hosted by native components.

## Defining Components

Each custom component is defined in a separate `.ux` file:

``` html
<template>
  <p>{{text}}</p>
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
      text: "Hello, World!"
    }
  }
</script>
```

As can be seen, a component consists of styles, a JavaScript script, and a "template" that describes the interface.

## UX Files

A UX (UI XML) file is a component description using the XML format. Each UX file defines a component, and pages are also a type of component.

The following root nodes can exist in a UX file:

- **`<import>`** tag: Used to introduce other components. This tag can be defined multiple times;
- **`<template>`** tag: Defines the content and structure of the component interface. There is one and only one such node;
- **`<template>`** macro tag: Defines repeatedly usable template structures. There can be multiple such nodes, see [Template Macros](./template-macro.md);
- **`<style>`** tag: Defines CSS style sheets. There is one and only one such node;
- **`<script>`** tag: A JavaScript script that implements the logical functions of the component. There is one and only one such node.

The arrangement order of the above nodes is arbitrary. Among them, the `<import>` node never contains child nodes. Note that the insides of the `<style>` node and `<script>` node do not follow XML syntax; symbols such as `>` and `&` do not need to use XML escape rules, but instead follow CSS and JavaScript syntax (similar to HTML).

UX files require all tags to be closed; for example, `<div>...</div>` or `<div/>` are both valid, but a standalone `<div>` or `</div>` will result in an error.

## Page Components

Components declared in the `router.pages` field of `manifest.json` can be used directly as pages.

Compared to general components, page components have more [lifecycle functions](life-cycle#组件和页面的生命周期), while other functions are basically the same. Component code that has already been used for page components can also be used directly as ordinary components.

## Importing Components

### Custom Components

Defined components can be referenced in other components. Fill in the `<import>` tag in the UX file to reference the specified component:
``` xml
<import name="Panel" src="path/to/Panel">
```

The `src` attribute is the path URL of the component, where `Panel` is the file name of the component (excluding the `.ux` suffix); the `name` attribute is an optional component name. If this attribute is not defined, the component's file name will be used as the component name.

`src` supports relative paths, absolute paths, and external paths:

- Relative paths are paths relative to the current UX file.
- Absolute paths are paths relative to the app's `src` path.
- External paths can import resource components outside the app. The specific path is the `package` value in the `appdb.json` of the resource component's app plus the absolute path.

### Global Components

Global components are non-native components defined in the framework. In an application, you can use the `<import>` tag, specify only the `name` attribute, and omit the `src` attribute to import a global component:
``` html
<import name="TopBar" />
```

Applications can only import global components and cannot register new global components. System developers can use the [`globalComponent()`](/api/system-internal.md#globalcomponent) API to register global components.

## Property Documentation Specification

Component property documentation titles take the following form:

<div class="example-block">
  <h3 style="margin-bottom: 0.5rem">
    <span>
      <code>value</code>
      <decl type="number" get set listen />
    </span>
  </h3>
</div>

Where:
- `value` is the name of the property;
- `number` is the property value type;
- <span style="color:#666">Read • Set • Listen</span> on the right indicates the access modes supported by this property.

### Access Modes

A property can support the following access modes:
- **Read**: The value of the property is readable;
- **Set**: The value of the property is writable;
- **Listen**: The property is [listenable](../commands/on.md). Listenable properties typically trigger a listening event when their value changes.

Taking the [`index`](/components/scroll.md#index) property of the [scroll](/components/scroll.md) component as an example, this property supports reading, setting, and listening simultaneously. You can manipulate the `index` property in template syntax:
``` html
<scroll id="scroll1" :index="5" on:index="console.log($event)">
  ...
</scroll>
```
Here, `:index="5"` assigns `5` to the `index` property, while `on:index="console.log($event)"` listens for changes to the `index` property. For more descriptions, please refer to [Inter-component Communication](/framework/component/communicate.md) and the [`on` Directive](../commands/on.md).

### Component Objects and Methods

You can also obtain the component object via the [`$element()`](component-apis.md#element) method to access properties:
``` js
const el = this.$element('scroll1') // Get the component object
console.log(el.index) // Read the index property of the scroll component
el.index = 4 // Set the index property of the scroll component
```
If supported, you can **read** or **set** the object returned by the `$element()` method. The `$element()` method does not support binding event listener functions to properties.

A component's property can also be a **function** or **method**. In this case, the documentation title takes the following form:

<div class="example-block">
  <h3 style="margin-bottom: 0.5rem">
    <span>
      <code>method</code>
      <decl type="(x: number, y: number): void" method />
    </span>
  </h3>
</div>

Where:
- `(x: number, y: number): void` is the signature of the function or method.
- <span style="color:#666">Method</span> on the right indicates that this property is a method.

Component methods can only be accessed through the component object. For example, taking the [`setIndex`](/components/scroll.md#setindex) property of the scroll component:
``` js
const el = this.$element('scroll1') // Get the component object
el.setIndex(4) // Call the setIndex() method
```
Methods do not support read, set, and listen access modes, so such properties only have the <span style="color:#666">Method</span> tag.

### Two-way Binding

When a property simultaneously supports the <span style="color:#666">Set • Listen</span> access modes, it is capable of [two-way binding](../commands/model.md).