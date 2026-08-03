# 模板宏

模板宏是一种简化重复代码的方法，它是 UX 文件中带有 `macro:` 属性的 `<template>` 顶级元素：
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
例如这里定义了一个名为 `scroll` 的宏，宏会替换当前 UX 文件的 `<template>` 模板内的同名组件，并且
- 同名组件的所有属性会替换模板宏中的 `#props` 占位符；
- 同名组件的子元素会替换模板宏中的 `<slot />` 节点。

例如
``` html
<template>
  <scroll :index="3" on:index="onIndexChange">
    <p for="i in 10">item {{i + 1}}</p>
  </scroll>
</template>
```
会被 `scroll` 模板宏替换为
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
这个例子中的宏名字为 `scroll`，而宏的内容也含有 `scroll` 标签，但是宏替换只会进行一次，不会重复进行替换。
:::

## 用途

从上面的示例可以看出，模板宏可以将普通的组件静态地替换为另一种形式，替换后的代码通常不便于手写和理解。如：
``` html
<scroll :index="3" on:index="onIndexChange">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
```
被替换为：
``` html
<scroll :index="3" on:index="onIndexChange" media-query="(shape: rect)">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
<scroll :index="3" on:index="onIndexChange" deformation="fisheye"
        scroll-snap="center" media-query="(shape: circle)">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
```
替换后的代码实际上是根据屏幕形状的[媒体查询](/framework/render/media-query.md)来静态地选择不同的 `scroll` 组件属性。具体来说，它在圆形屏幕上为 [`scroll`](/components/scroll.md) 组件添加了两个属性：
- [`deformation="fisheye"`](/components/scroll.md#deformation)：为圆形屏幕启用鱼眼效果；
- [`scroll-snap="center"`](/components/scroll.md#scrollsnap)：圆形屏幕下 `scroll` 子元素居中对齐。

这个模板宏为原先的手写代码添加了异形屏幕形状的适配。这种修改不需要修改模板源代码，因此是非侵入的。

## 使用方法

目前没有办法将模板宏导出到其他 UX 文件中使用。因此要在每个需要的 UX 文件重复编写模板宏，即类似
``` html
<template macro:scroll>
  ...
</template>
```
的顶级元素。模板宏节点和 `<template>` 节点可以具有任意的顺序，但不要在一个 UX 文件中定义同名的模板宏。
