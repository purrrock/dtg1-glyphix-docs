# Component Framework

Components are a technology in Glyphix used to achieve code reuse in App interface development. By nesting HTML-like elements, multiple components can be combined to form the overall appearance and function of an interface. On the other hand, each component encapsulates specific content and logic, and their rational use can reduce code complexity and maintenance costs.

Components are divided into built-in [**native components**](../render/native-component.md) and **custom components** implemented by developers. Native components are generally encapsulations of UI elements, used to display specific UI content or for layout and interaction, such as `text`, `image`, `div`, `list`, etc. Custom components, however, focus on logic implementation and functional encapsulation, because the interfaces implemented within custom components are ultimately hosted by native components.

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

As can be seen, a component consists of styles, JavaScript scripts, and a "template" that describes the interface.

## UX Files

A UX (UI XML) file is a component description using XML format. Each UX file defines a component, and a page is also a type of component.

The following root nodes can exist in a UX file:

- **`<import>`** tag: Used to import other components. This tag can be defined multiple times;
- **`<template>`** tag: Defines the content and structure of the component interface. There is one and only one such node;
- **`<template>`** macro tag: Defines reusable template structures. There can be multiple such nodes; see [Template Macros](./template-macro.md);
- **`<style>`** tag: Defines the CSS stylesheet. There is one and only one such node;
- **`<script>`** tag: A JavaScript script that implements the logical functions of the component. There is one and only one such node.

The order of the above nodes is arbitrary. Among them, the `<import>` node never contains child nodes. Note that the contents of the `<style>` and `<script>` nodes do not follow XML syntax; symbols like `>` and `&` do not require XML escaping rules, but instead follow CSS and JavaScript syntax (similar to HTML).

UX files require all tags to be closed. For example, `<div>...</div>` or `<div/>` are both valid, but a standalone `<div>` or `</div>` will result in an error.

## Page Components

Components declared in the `router.pages` field of `manifest.json` can be used directly as pages.

Compared to regular components, page components have more [lifecycle functions](life-cycle#组件和页面的生命周期), while other functions are basically the same. Component code already used for page components can also be used directly as regular components.

## Importing Components

### Custom Components

Defined components can be referenced in other components. Fill in the `<import>` tag in the UX file to reference the specified component:
``` xml
<import name="Panel" src="path/to/Panel">
```

The `src` attribute is the path URL of the component, where `Panel` is the component's filename (excluding the `.ux` extension); the `name` attribute is an optional component name. If this attribute is not defined, the component's filename will be used as its name.

`src` supports relative paths, absolute paths, and external paths:

- Relative paths are relative to the current UX file.
- Absolute paths are relative to the app's `src` path.
- External paths can import resource components outside the app. The specific path is the `package` value in the `appdb.json` of the resource component's app plus the absolute path.

### Global Components

Global components are non-native components defined in the framework. In an application, you can import a global component by using the `<import>` tag, specifying only the `name` attribute and omitting the `src` attribute:
``` html
<import name="TopBar" />
```

Applications can only import global components and cannot register new ones. System developers can use the [`globalComponent()`](/api/system-internal.md#globalcomponent) API to register global components.

## Attribute Documentation Specification

Component attribute documentation titles take the following form:

<div class="example-block">
  <h3 style="margin-bottom: 0.5rem">
    <span>
      <code>value</code>
      <decl type="number" get set listen />
    </span>
  </h3>
</div>

Where:
- `value` is the name of the attribute;
- `number` is the attribute value type;
- On the right, <span style="color:#666">Get • Set • Listen</span> indicates the supported access modes for the attribute.

### Access Modes

An attribute can support the following access modes:
- **Get**: The value of the attribute is readable;
- **Set**: The value of the attribute is writable;
- **Listen**: The attribute is [listenable](../commands/on.md), and listenable attributes typically trigger listening events when their values change.

Taking the [`index`](/components/scroll.md#index) attribute of the [scroll](/components/scroll.md) component as an example, this attribute supports reading, setting, and listening simultaneously. You can manipulate the `index` attribute in template syntax:
``` html
<scroll id="scroll1" :index="5" on:index="console.log($event)">
  ...
</scroll>
```
Here, `:index="5"` assigns `5` to the `index` attribute, while `on:index="console.log($event)"` listens for changes to the `index` attribute. For more details, please refer to [Inter-component Communication](/framework/component/communicate.md) and the [`on` Directive](../commands/on.md).

### Component Objects and Methods

You can also obtain the component object via the [`$element()`](component-apis.md#element) method to access its attributes:
``` js
const el = this.$element('scroll1') // Get the component object
console.log(el.index) // Read the index attribute of the scroll component
el.index = 4 // Set the index attribute of the scroll component
```
If supported, you can **get** or **set** the object returned by the `$element()` method. The `$element()` method does not support binding event listener functions to attributes.

A component's attribute can also be a **function** or a **method**. In this case, the documentation title format is as follows:

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
- On the right, <span style="color:#666">Method</span> indicates that the attribute is a method.

Component methods can only be accessed through the component object. For example, taking the [`setIndex`](/components/scroll.md#setindex) attribute of the scroll component:
``` js
const el = this.$element('scroll1') // Get the component object
el.setIndex(4) // Call the setIndex() method
```
Methods do not support get, set, and listen access modes, so such attributes only have the <span style="color:#666">Method</span> tag.

### Two-Way Binding

When an attribute simultaneously supports the <span style="color:#666">Set • Listen</span> access modes, it supports [two-way binding](../commands/model.md).