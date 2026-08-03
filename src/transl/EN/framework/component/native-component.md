# Native components


Native components are components implemented in C++. The main design goal of these components is to implement certain interface elements, such as buttons or list effects, but do not carry business logic. Different from web technology, native components themselves do not provide DOM interfaces, only responsive component interfaces.


The native components in Glyphix provide a large number of configuration interfaces to achieve rich display effects. In addition, the built-in components are optimized for embedded platform designs.


In this document, **native components** are used to refer to components implemented in C++; the term **built-in components** refers to the component packages provided by WearOS, but these components are not necessarily implemented in C++.


::: tip

This document will distinguish between native components and built-in components in the description, but readers generally do not need to ignore the difference between the two.
:::



## Interface function mechanism


Most of the interface-related mechanisms are only available in native components. These mechanisms include:
- CSS style sheets, layout and other mechanisms
- Gestures and touch events
- Rendering and drawing mechanisms


The interfaces of some native component mechanisms can be simulated in custom components through parameter/event passing between components, but these capabilities are essentially implemented by native components.


## Interface rendering


## Component Snapshot


Snapshot is a frame rate optimization technology. Turning on snapshots for complex components can speed up drawing and thus increase frame rate. Snapshots essentially take "screenshots" of components and speed things up by drawing those screenshots directly. Therefore, snapshots are an effective technique for components that are complex in content but updated infrequently. For other scenarios where updates are frequent but can tolerate no refresh, there are corresponding APIs to disable snapshot updates.


## native component object


The native component object can be obtained through the component's [`$element()`](component-apis#element) method, which can access the properties of the native component or call its methods, for example:


``` js
let el = this.$element('scroll-id')
console.log(`width: ${el.width}`) // Get the width of the component through the native component object
el.scrollTo({ top: 100 }) // Scroll list via API
```