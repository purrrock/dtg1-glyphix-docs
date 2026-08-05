# Шаблонные макросы

Шаблонные макросы — это способ упрощения повторяющегося кода. Они представляют собой корневой элемент `<template>` с атрибутом `macro:` в UX-файле:
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
Например, здесь определен макрос с именем `scroll`. Макрос заменяет компонент с тем же именем внутри шаблона `<template>` текущего UX-файла, при этом:
- Все атрибуты компонента с тем же именем заменяют заполнитель `#props` в макросе шаблона;
- Дочерние элементы компонента с тем же именем заменяют узел `<slot />` в макросе шаблона.

Например, следующий код:
``` html
<template>
  <scroll :index="3" on:index="onIndexChange">
    <p for="i in 10">item {{i + 1}}</p>
  </scroll>
</template>
```
будет заменен макросом шаблона `scroll` на следующий вариант:
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
В этом примере макрос называется `scroll`, и его содержимое также содержит тег `scroll`, однако замена макроса происходит только один раз и не повторяется рекурсивно.
:::

## Назначение

Как видно из примера выше, шаблонные макросы могут статический заменять обычные компоненты на другую форму, причем полученный код обычно неудобен для ручного написания и понимания. Например:
``` html
<scroll :index="3" on:index="onIndexChange">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
```
заменяется на:
``` html
<scroll :index="3" on:index="onIndexChange" media-query="(shape: rect)">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
<scroll :index="3" on:index="onIndexChange" deformation="fisheye"
        scroll-snap="center" media-query="(shape: circle)">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
```
Результирующий код фактически статический выбирает различные свойства компонента `scroll` на основе [медиазапросов](/framework/render/media-query.md) для формы экрана. В частности, он добавляет два свойства к компоненту [`scroll`](/components/scroll.md) для экранов круглой формы:
- [`deformation="fisheye"`](/components/scroll.md#deformation): включает эффект «рыбий глаз» для круглых экранов;
- [`scroll-snap="center"`](/components/scroll.md#scrollsnap): выравнивание дочерних элементов `scroll` по центру на круглом экране.

Этот шаблонный макрос добавляет адаптацию под нестандартную форму экрана в исходный код, написанный вручную. Такая модификация не требует изменения исходного кода шаблона, поэтому она является неинтрузивной.

## Использование

В настоящее время нет возможности экспортировать шаблонные макросы для использования в других UX-файлах. Поэтому шаблонные макросы необходимо дублировать в каждом UX-файле, где они требуются, определяя корневой элемент вида:
``` html
<template macro:scroll>
  ...
</template>
```
Узел шаблонного макроса и узел `<template>` могут располагаться в любом порядке, однако не следует определять шаблонные макросы с одинаковыми именами в рамках одного UX-файла.