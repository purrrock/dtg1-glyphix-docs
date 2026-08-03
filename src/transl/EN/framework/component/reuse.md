# Component Reuse

Application-level component reuse is primarily achieved through custom components.

## Child Components

Suppose the structure inside the `<template>` tag of a [UX file](/framework/component/README.md#ux-file) describes the organization of the user interface, for example:
``` html
<template>
  <div>
    <p>text</p>
    <image src="path/to/image.png" />
    <qrcode value="hello world!" />
  </div>
</template>
```
At runtime, this corresponds to the following component tree structure:
``` mermaid
flowchart TB
  div --- p
  div --- image
  div --- qrcode
```
This component tree has a parent node `div` and $3$ child nodes: `p`, `image`, and `qrcode`. The `div` component is the outermost component within the `<template>` tag. We refer to this type of component as the **root component**. Root components are sometimes not unique; for example:
``` html
<template>
  <p>text</p>
  <image src="path/to/image.png" />
  <qrcode value="hello world!" />
</template>
```
contains $3$ root components. Additionally, using the [`for` directive](/framework/commands/for.md) may also result in multiple root component instances, for example:
``` html
<template>
  <p for="x in ['one', 'two', 'three']">
    label: {{x}}
  </p>
</template>
```
will be rendered as $3$ `p` component instances.