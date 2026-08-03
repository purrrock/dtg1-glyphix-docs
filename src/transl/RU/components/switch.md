# switch

Компонент переключателя, по умолчанию является строчным элементом (inline). Используется для отображения двух состояний — включено/выключено, и позволяет пользователю переключаться между ними. Функционал `switch` аналогичен `checkbox`, но имеет другие принципы взаимодействия и назначение, выражая соответственно переключение и выбор нескольких опций.

<glyphix id="components-switch" height="30">

``` html
<div>
  <switch ::value="enabled" />
  <span>switch state: {{ enabled ? 'on' : 'off' }}</span>
</div>
```

``` js
export default {
  data: {
    enabled: false
  }
}
```
</glyphix>

::: note
Стили компонента `switch` обычно выглядят так, как показано в примере, но могут отличаться в зависимости от устройства. Стоит особенно отметить, что ширина `switch` на разных устройствах может варьироваться, поэтому разработчикам следует закладывать подходящие отступы в макете.
:::

## Свойства (Attributes)

### `value` <decl type="boolean" set get listen/>

Определяет состояние `switch`. Когда значение равно `true`, `switch` находится во включенном состоянии, в противном случае — в выключенном. Если свойство `value` не задано, компонент `switch` по умолчанию выключен.

### `checked` <decl type="boolean" set get/>

Это совместимое свойство платформы Quick App, рекомендуется использовать [`value`](#value).

### `change` <decl type="{ checked: boolean }" get listen/>

Это совместимое свойство платформы Quick App, рекомендуется использовать [`value`](#value).

## CSS-поведение

Общий стиль компонента `switch` определяется системой и не контролируется разработчиком, подобно различиям в стилях между [Fluent 2](https://fluent2.microsoftdesign/components/web/react/switch/usage) и [Material 3](https://m3.material.io/components/switch/overview). Glyphix позволяет настраивать цвет `switch` с помощью CSS, а также изменять его размер.

### CSS-свойства

#### `color`

Устанавливает цвет ползунка компонента `switch`. В отличие от обычного CSS-свойства [`color`](/framework/generic/styles.md#color), свойство `color` для `switch` не наследуется, поэтому вы должны определять его непосредственно для текущего компонента `switch`.

<glyphix id="components-switch-color" height="36" title="siwtch 滑块颜色">

``` html
<div>
  red color: <switch class="red"/>,
  not inherited: <switch/>
</div>
```

``` css
div {
  color: red; /* Обратите внимание: switch не наследует свойство color */
}

.red {
  color: red; /* color должен быть определен в стилях компонента switch */
}
```
</glyphix>

#### `background-color`

Управляет фоновым цветом компонента `switch`. Подробнее см. в документации по псевдоклассу [`active`](#active). 

#### `font-size`

Вы можете использовать CSS-свойство [`font-size`](/framework/generic/styles.md#font-size) для настройки размера `switch`, чтобы согласовать его с размером окружающего строчного (inline) текста. В следующем примере показана зависимость между `font-size` и размером `switch`:

<glyphix id="components-switch-size" height="100" title="font-size 与 siwtch 大小">

``` html
<div>
  <p class="title">
    title text: <switch/> (1.25rem)
  </p>
  <p>
    content text: <switch/> (1rem)
  </p>
</div>
```

``` css
div {
  line-height: 1.8rem;
}

.title {
  color: #415a77; /* Обратите внимание: switch не наследует свойство color */
  font-size: 1.25rem;
}
```
</glyphix>

::: warning
Отображаемый размер `switch` не контролируется такими свойствами, как `width` и `height`, а всегда определяется через `font-size`. Поэтому не задавайте размеры вроде `width` вручную во избежание некорректного отображения.
:::

### CSS-псевдоклассы

#### `active`

Псевдокласс `active` используется для определения стиля `switch` в активном (включенном) состоянии. Как показано в примере ниже, он обычно настраивается вместе с правилами обычного стиля:

<glyphix id="components-switch-colors" height="36" title="siwtch 滑块颜色设置">

``` html
<div>
  color switch: <switch/>
</div>
```

``` css
/* Стиль switch в выключенном состоянии */
switch {
  color: #415a77;
  background-color: #bde0fe;
}

/* Стиль switch в включенном состоянии */
switch:active {
  color: #fefae0;
  background-color: #ffafcc;
}
```
</glyphix>

В этом примере цвета при переключении `switch` управляются с помощью CSS-свойств `color` и `background-color`. Компонент `switch` реагирует только на настройку этих двух CSS-свойств даже в состоянии, активированном псевдоклассом `active`.

::: tip
Пожалуйста, определяйте свойства `color` и `background-color` как для обычного состояния, так и для состояния `active`, иначе при переключении `switch` не будет соответствующего изменения цвета.
:::