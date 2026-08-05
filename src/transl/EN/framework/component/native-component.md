# Native Components

Native components refer to components implemented in C++. The main design goal of these components is to implement specific UI elements, such as buttons or list effects, without carrying business logic. Unlike Web technologies, native components themselves do not provide DOM interfaces, but only reactive component interfaces.

Native components in Glyphix provide a large number of configuration interfaces to achieve rich visual effects. In addition, built-in components feature optimizations designed specifically for embedded platforms.

In this documentation, **native components** refer to components implemented in C++; the term **built-in components** refers to component packages provided by WearOS, though these components are not necessarily implemented in C++.

::: tip
While this documentation distinguishes between native components and built-in components in its descriptions, readers generally do not need to worry about the difference between the two.
:::

## UI Functional Mechanisms

Most UI-related mechanisms are only available in native components. These mechanisms include:
- CSS style sheets, layout, and other mechanisms
- Gestures and touch events
- Rendering and drawing mechanisms

While certain native component mechanism interfaces can be simulated in custom components through parameter/event passing between components, these capabilities are fundamentally implemented by native components.

## UI Rendering

## Component Snapshots

Snapshots are a frame rate optimization technique. Enabling snapshots for complex components can speed up drawing and thus improve frame rate. Essentially, a snapshot is a "screenshot" of a component, and rendering is accelerated by directly drawing these screenshots. Therefore, snapshots are an effective technique for components with complex content that update infrequently. For other scenarios where updates are frequent but lagging or skipped frames can be tolerated, there are corresponding APIs to disable snapshot updates.

## Native Component Objects

You can obtain the native component object using the component's [`$element()`](component-apis#element) method, which allows you to access native component properties or call its methods, for example:

``` js
let el = this.$element('scroll-id')
console.log(`width: ${el.width}`) // Get the component's width via the native component object
el.scrollTo({ top: 100 }) // Scroll the list via API
```