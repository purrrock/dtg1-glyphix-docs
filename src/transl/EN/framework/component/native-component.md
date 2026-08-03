# Native Components

Native components refer to components implemented in C++. The main design goal of these components is to implement specific UI elements, such as buttons or list effects, without carrying business logic. Unlike Web technologies, native components themselves do not provide DOM interfaces, but only reactive component interfaces.

Native components in Glyphix provide a large number of configuration interfaces to achieve rich display effects. In addition, built-in components feature optimizations designed for embedded platforms.

In this document, **native components** refers to components implemented in C++; the term **built-in components** refers to component packages provided by WearOS, though these components are not necessarily implemented in C++.

::: tip
This document distinguishes between native components and built-in components in its descriptions, but readers generally do not need to worry about the difference between the two.
:::

## UI Functional Mechanisms

Most UI-related mechanisms are only available in native components. These mechanisms include:
- CSS style sheets, layouts, and other mechanisms
- Gestures and touch events
- Rendering and drawing mechanisms

Interfaces for certain native component mechanisms can be simulated in custom components through parameter/event passing between components, but these capabilities are essentially implemented by native components.

## UI Rendering

## Component Snapshots

Snapshots are a frame rate optimization technique. Enabling snapshots for complex components can speed up drawing and thus improve the frame rate. Essentially, snapshots take a "screenshot" of the component and accelerate rendering by directly drawing these screenshots. Therefore, for components with complex content but infrequent updates, snapshots are an effective technique. For other scenarios where updates are frequent but the loss of refresh updates can be tolerated, there are corresponding APIs to disable snapshot updates.

## Native Component Objects

You can obtain the native component object through the component's [`$element()`](component-apis#element) method, which allows you to access the properties of the native component or call its methods, for example:

``` js
let el = this.$element('scroll-id')
console.log(`width: ${el.width}`) // Get the width of the component through the native component object
el.scrollTo({ top: 100 }) // Scroll the list through the API
```