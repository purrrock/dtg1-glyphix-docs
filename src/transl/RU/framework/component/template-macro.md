# Шаблонные макросы

Шаблонный макрос — это способ упрощения повторяющегося кода. Он представляет собой корневой элемент `<template>` с атрибутом `macro:` в UX-файле:
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
- Все атрибуты одноименного компонента заменяют заполнитель `#props` в шаблонном макросе;
- Дочерние элементы одноименного компонента заменяют узел `<slot />` в шаблонном макросе.

Например:
``` html
<template>
  <scroll :index="3" on:index="onIndexChange">
    <p for="i in 10">item {{i + 1}}</p>
  </scroll>
</template>
```
Будет заменено шаблонным макросом `scroll` на:
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
В этом примере макрос называется `scroll`, и его содержимое также содержит тег `scroll`, однако замена макроса происходит только один раз и не запускает рекурсивную подстановку.
:::

## Назначение

Как видно из примера выше, шаблонные макросы могут статический заменять обычные компоненты на другую структуру, причем полученный код обычно неудобен для ручного написания и восприятия. Например:
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
Полученный код фактически статически выбирает различные свойства компонента `scroll` на основе [медиазапросов](/framework/render/media-query.md) для формы экрана. В частности, он добавляет два свойства для компонента [`scroll`](/components/scroll.md) на экранах круглой формы:
- [`deformation="fisheye"`](/components/scroll.md#deformation): включает эффект «рыбьего глаза» для круглых экранов;
- [`scroll-snap="center"`](/components/scroll.md#scrollsnap): выравнивание дочерних элементов `scroll` по центру на круглом экране.

Этот шаблонный макрос добавляет адаптацию под экраны нестандартной формы для исходного кода, написанного вручную. Такая модификация не требует изменения исходного кода шаблона, поэтому является неинвазивной.

## Использование

В настоящее время нет способа экспортировать шаблонные макросы для использования в других UX-файлах. Поэтому шаблонные макросы необходимо дублировать в каждом нуждающемся в них UX-файле, определяя корневой элемент вроде:
``` html
<template macro:scroll>
  ...
</template>
```
Узел шаблонного макроса и узел `<template>` могут идти в любом порядке, однако не следует определять шаблонные макросы с одинаковыми именами в рамках одного UX-файла.