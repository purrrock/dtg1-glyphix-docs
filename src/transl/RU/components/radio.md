# radio

Радиокнопка (single choice button), по умолчанию является строчным элементом, часто используется в **группе радиокнопок**, которая содержит набор элементов, описывающих ряд связанных опций. Одновременно в группе может быть выбрана только одна радиокнопка. Радиокнопки обычно отображаются в виде небольших кружков, которые заполняются и подсвечиваются при выборе.

<glyphix id="radio-1" :height="65" title="单选按钮">

``` html
<div>
  <p>picked color: {{color}}</p>
  <div>
    <radio id="red" value="red" model:group="color" />
    <label target="red">red</label>
    <radio id="blue" value="blue" model:group="color" />
    <label target="blue">blue</label>
    <radio id="yellow" value="yellow" model:group="color" />
    <label target="yellow">yellow</label>
  </div>
</div>
```

``` js
export default {
  data: {
    color: 'blue'
  }
}
```

``` css
label {
  margin-right: 0.5rem;
}
```

</glyphix>

::: tip
Радиокнопки в чем-то похожи на [`checkbox`](checkbox.md), но `radio` позволяет выбрать только одно значение из группы, в то время как `checkbox` разрешает выбор нескольких значений.
:::

## Свойства

### `checked` <decl type="boolean" get set listen />

Это свойство указывает, выбрана ли данная радиокнопка. Установка свойства `checked` позволяет переключать состояние выбора радиокнопки: при значении `true` она отображается как выбранная.

Когда пользователь нажимает на радиокнопку, что приводит к изменению ее состояния выбора, генерируется событие `checked`.

::: tip
Манипуляции со свойством `checked` не являются рекомендуемым способом использования `radio`, пожалуйста, используйте метод [группы радиокнопок](#group).
:::

### `value` <decl type="any" get set />

Значение JavaScript, идентифицирующее радиокнопку, обычно представляет собой строку или число. Это значение не отображается визуально, но может использоваться в [группе радиокнопок](#group).

### `group` <decl type="any" get set listen />

Если у вас есть несколько связанных компонентов `radio`, вы можете объединить свойства `group` и `value`. Радиокнопки в одной группе взаимоисключающие: значение реактивного свойства, привязанного к `group`, равно свойству `value` выбранной радиокнопки. Например:
``` html
<radio value="red" model:group="color" />
<radio value="blue" model:group="color" />
<radio value="yellow" model:group="color" />
```
Здесь `color` — это реактивное свойство. Когда выбрана вторая радиокнопка, значение `color` становится равным `"blue"`. Если `value` ни одной из радиокнопок не совпадает со значением `color`, то ни одна радиокнопка не будет выбрана. Например:
``` html
<p on:click="color = null">reset select</p>
```
сбросит состояние выбора:

<glyphix id="radio-reset" :height="65" title="清除选中状态">

``` html
<div>
  <p on:click="color = null">picked color: {{color}} (click to reset)</p>
  <div>
    <radio id="red" value="red" model:group="color" />
    <label target="red">red</label>
    <radio id="blue" value="blue" model:group="color" />
    <label target="blue">blue</label>
    <radio id="yellow" value="yellow" model:group="color" />
    <label target="yellow">yellow</label>
  </div>
</div>
```

``` js
export default {
  data: {
    color: 'blue'
  }
}
```

``` css
label {
  margin-right: 0.5rem;
}
```

</glyphix>

### Поведение CSS

По умолчанию радиокнопки являются строчными элементами, их размеры определяются CSS-свойством `font-size`, и они выравниваются по базовой линии текста. Пожалуйста, не задавайте вручную такие свойства, как `width` и `height`, так как это может привести к нарушению отображения.