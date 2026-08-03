# Template Macros

Template macros are a way to simplify repetitive code. They are top-level `<template>` elements in UX files with the `macro:` attribute:
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
For example, a macro named `scroll` is defined here. The macro will replace components with the same name inside the `<template>` of the current UX file, and:
- All attributes of the component with the same name will replace the `#props` placeholder in the template macro;
- The child elements of the component with the same name will replace the `<slot />` node in the template macro.

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
In this example, the macro name is `scroll`, and the macro content also contains the `scroll` tag, but macro replacement is only performed once and will not be repeated recursively.
:::

## Purpose

As can be seen from the above example, template macros can statically replace ordinary components into another form. The replaced code is usually inconvenient to write and understand manually. For example:
``` html
<scroll :index="3" on:index="onIndexChange">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
```
is replaced with:
``` html
<scroll :index="3" on:index="onIndexChange" media-query="(shape: rect)">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
<scroll :index="3" on:index="onIndexChange" deformation="fisheye"
        scroll-snap="center" media-query="(shape: circle)">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
```
The replaced code actually statically selects different `scroll` component attributes based on screen shape [media queries](/framework/render/media-query.md). Specifically, it adds two attributes to the [`scroll`](/components/scroll.md) component on circular screens:
- [`deformation="fisheye"`](/components/scroll.md#deformation): Enables the fisheye effect for circular screens;
- [`scroll-snap="center"`](/components/scroll.md#scrollsnap): Aligns `scroll` child elements to the center on circular screens.

This template macro adds adaptation for non-standard screen shapes to the original hand-written code. This modification does not require changing the template source code, making it non-intrusive.

## Usage

Currently, there is no way to export template macros for use in other UX files. Therefore, template macros must be repeatedly written in each UX file where they are needed, meaning top-level elements like:
``` html
<template macro:scroll>
  ...
</template>
```
can be used. Template macro nodes and `<template>` nodes can appear in any order, but do not define template macros with the same name within a single UX file.