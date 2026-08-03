# component framework


Components are a technology in Glyphix that enables reuse of App interface development functions. Multiple components can be combined and form the overall appearance and functionality of the interface in a manner similar to nested HTML elements. On the other hand, each component encapsulates certain content and logic, which can reduce code complexity and maintenance costs through reasonable use.


Components are divided into built-in [**Native components**](../render/native-component.md) and **custom components** implemented by developers. Native components are generally encapsulations of UI elements and can be used to display specific UI content or for layout and interaction, such as text, image, div, list, etc. Custom components focus on logic implementation and functional encapsulation, because the interface implemented in custom components is actually hosted by native components.


## Define components


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


It can be seen that a component consists of styles, JavaScript scripts and "templates" that describe the interface.


## UX files


A UX (UI XML) file is a component description using XML format. Each UX file defines a component, and pages are also a component.


The following root nodes can exist in the UX file:


- ** `<import>` ** Label: used to introduce other components, this label can be defined repeatedly;
- ** `<template>` ** Label: Defines the content and structure of the component interface. There is only one node for this node;
- ** `<template>` ** Macro tag: defines a template structure that can be reused. There can be multiple nodes, see [template macro](./template-macro.md);
- ** `<style>` ** Tag: Define CSS style sheet, this node has only one;
- ** `<script>` ** Tag: JavaScript script that implements the component's logical function. There is only one node for this node.


The order of the above nodes is arbitrary. Among them, the `<import>` node always does not contain child nodes. Note that the `<style>` node and `<script>` node do not follow XML syntax internally. All symbols such as `>` and `&` do not need to use XML escaping rules, but follow the syntax of CSS and JavaScript (similar to HTML).


The UX file requires that all tags must be closed. For example, `<div>...</div>` or `<div/>` are legal, but a separate `<div>` or `</div>` will cause an error.


## Page components


Components declared in the `router.pages` field of `manifest.json` can be used directly as pages.


Compared with general components, page components have more [life cycle function](life-cycle#组件和页面的生命周期) and other functions are basically the same. Component code that has been used for page components can also be used directly as ordinary components.


## Introduce components


### Custom component


Defined components can be referenced in other components. Fill in the `<import>` tag in the UX file to reference the specified component:
``` xml
<import name="Panel" src="path/to/Panel">
```


The `src` attribute is the path URL of the component, where `Panel` is the file name of the component (excluding the `.ux` suffix); the `name` attribute is an optional component name. If this attribute is not defined, the file name of the component will be used as the component name.


`src` supports relative paths, absolute paths, and external paths


- The relative path is relative to the path of this UX file
- The absolute path is relative to the src path of the APP
- The external path can import resource components outside the APP. The specific path is the package value in appdb.json of the resource component APP plus the absolute path.


### global components


Global components are non-native components defined in the framework. You can use the `<import>` tag and specify only the `name` attribute and omit the `src` attribute to introduce global components in the application:
``` html
<import name="TopBar" />
```


In applications that can only introduce global components but cannot register new global components, system developers can use the [`globalComponent()`](/api/system-internal.md#globalcomponent) API to register global components.


## Property document specification


The component property document title format is as follows:


<div class="example-block">

  <h3 style="margin-bottom: 0.5rem">

    <span>

      <code>value</code>

      <decl type="number" get set listen />

    </span>

  </h3>

</div>



in
- `value` is the name of the attribute;
- `number` is the attribute value type;
- The <span style="color:#666"> on the right reads • sets • listens </span> indicates the access modes supported by the property.


### access mode


A property can support the following access modes:
- **Read**: The value of the attribute is readable;
- **Settings**: The value of the attribute is writable;
- **Listening**: Attributes are [monitor](../commands/on.md) able. Listenable attributes usually trigger listening events when their values ​​change.


Take the [`index`](/components/scroll.md#index) attribute of the [scroll](/components/scroll.md) component as an example. This attribute supports reading, setting, and monitoring at the same time. The `index` attribute can be manipulated in template syntax:
``` html
<scroll id="scroll1" :index="5" on:index="console.log($event)">
  ...
</scroll>
```
Among them, `:index="5"` assigns `5` to the `index` attribute, and `on:index="console.log($event)"` listens for changes in the `index` attribute. Please refer to [Communication between components](/framework/component/communicate.md) and [`on` directive](../commands/on.md) for more descriptions.


### Component objects and methods


Properties can also be accessed by getting the component object through the [`$element()`](component-apis.md#element) method:
``` js
const el = this.$element('scroll1') // Get component object
console.log(el.index) // Read the index property of the scroll component
el.index = 4 // Set the index property of the scroll component
```
If supported, the object returned by the `$element()` method can be read or set. The `$element()` method does not support binding event listeners to properties.


The attribute of the component can also be a **function** or **method**. In this case, the document title is in the following format:


<div class="example-block">

  <h3 style="margin-bottom: 0.5rem">

    <span>

      <code>method</code>

      <decl type="(x: number, y: number): void" method />

    </span>

  </h3>

</div>



in
- `(x: number, y: number): void` is the signature of the function or method
- The <span style="color:#666"> method </span> on the right side indicates that the attribute is a method.


Component methods can only be accessed through the component object. For example, the [`setIndex`](/components/scroll.md#setindex) attribute of the scroll component is as follows:
``` js
const el = this.$element('scroll1') // Get component object
el.setIndex(4) // Call the setIndex() method
```
Methods do not support read, set, and listen access modes, so such properties only have the <span style="color:#666"> method </span> tag.


### Two-way binding


A property is [Two-way binding](../commands/model.md) enabled when it also supports the <span style="color:#666"> setting • Listening for the </span> access mode.