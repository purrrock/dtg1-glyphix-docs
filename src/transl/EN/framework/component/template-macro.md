# template macro


Template macros are a way to simplify repetitive code and are top-level elements in UX files with a `macro:` attribute:
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
For example, a macro named `scroll` is defined here. The macro will replace the component of the same name in the `<template>` template of the current UX file, and
- All attributes of components with the same name will replace the `#props` placeholder in the template macro;
- Child elements of components with the same name replace the `<slot />` node in the template macro.


For example
``` html
<template>
  <scroll :index="3" on:index="onIndexChange">
    <p for="i in 10">item {{i + 1}}</p>
  </scroll>
</template>
```
will be replaced by the `scroll` template macro
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

The macro name in this example is `scroll`, and the content of the macro also contains the `scroll` tag, but the macro replacement will only be performed once and will not be repeated.
:::



## use


As can be seen from the above example, template macros can statically replace ordinary components into another form. The replaced code is usually inconvenient to handwrite and understand. like:
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
The replaced code actually statically selects different `scroll` component properties based on the [media inquiries](/framework/render/media-query.md) of the screen shape. Specifically, it adds two properties to the [`scroll`](/components/scroll.md) component on circular screens:
- [`deformation="fisheye"`](/components/scroll.md#deformation): Enable fisheye effect for circular screens;
- [`scroll-snap="center"`](/components/scroll.md#scrollsnap): Center-align the `scroll` child elements on a circular screen.


This template macro adds special-shaped screen shape adaptation to the original handwritten code. This modification does not require modification of the template source code and is therefore non-intrusive.


## How to use


There is currently no way to export template macros for use in other UX files. Therefore, the template macro needs to be written repeatedly in each required UX file, that is, something like
``` html
<template macro:scroll>
  ...
</template>
```
top level element. Template macro nodes and `<template>` nodes can be in any order, but do not define template macros with the same name in a UX file.