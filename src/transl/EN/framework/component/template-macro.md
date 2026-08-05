# Template Macros

Template macros are a way to simplify repetitive code. They are top-level `<template>` elements in UX files with a `macro:` attribute:
``` html
<template macro:scroll>
  <scroll #props media-query="(shape: rect)">
    <slot />
  </scroll>
  <scroll #props deformation="fisheye"
          scroll-snap="center" media-query="(shape: circle)">
    <slot />
  </scroll>
</template>
```
For example, a macro named `scroll` is defined here. The macro replaces components with the same name inside the `<template>` template of the current UX file, and:
- All attributes of the component with the same name replace the `#props` placeholder in the template macro;
- The child elements of the component with the same name replace the `<slot />` node in the template macro.

For example:
``` html
<template>
  <scroll :index="3" on:index="onIndexChange">
    <p for="i in 10">item {{i + 1}}</p>
  </scroll>
</template>
```
will be replaced by the `scroll` template macro with:
``` html
<template>
  <scroll :index="3" on:index="onIndexChange" media-query="(shape: rect)">
    <p for="i in 10">item {{i + 1}}</p>
  </scroll>
  <scroll :index="3" on:index="onIndexChange" deformation="fisheye"
          scroll-snap="center" media-query="(shape: circle)">
    <p for="i in 10">item {{i + 1}}</p>
  </scroll>
</template>
```

::: tip
In this example, the macro name is `scroll`, and the macro content also contains the `scroll` tag, but the macro replacement is only performed once and will not be recursively replaced.
:::

## Purpose

As can be seen from the above example, template macros can statically replace ordinary components into another form. The replaced code is usually inconvenient to write by hand and understand. For instance:
``` html
<scroll :index="3" on:index="onIndexChange">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
```
is replaced by:
``` html
<scroll :index="3" on:index="onIndexChange" media-query="(shape: rect)">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
<scroll :index="3" on:index="onIndexChange" deformation="fisheye"
        scroll-snap="center" media-query="(shape: circle)">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
```
The replaced code actually statically selects different `scroll` component attributes based on [media queries](/framework/render/media-query.md) for screen shapes. Specifically, it adds two attributes to the [`scroll`](/components/scroll.md) component on circular screens:
- [`deformation="fisheye"`](/components/scroll.md#deformation): Enables the fisheye effect for circular screens;
- [`scroll-snap="center"`](/components/scroll.md#scrollsnap): Centers the `scroll` child elements on circular screens.

This template macro adds adaptation for non-standard screen shapes to the original hand-written code. This modification does not require changing the template source code, making it non-intrusive.

## Usage

Currently, there is no way to export template macros for use in other UX files. Therefore, you need to repeatedly write template macros in every UX file that requires them, i.e., top-level elements like:
``` html
<template macro:scroll>
  ...
</template>
```
Template macro nodes and `<template>` nodes can be in any order, but do not define template macros with the same name within a single UX file.