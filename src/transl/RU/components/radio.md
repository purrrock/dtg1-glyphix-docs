# radio

Радиокнопка (модификатор `radio`), по умолчанию является строчным элементом и часто используется в **группе радиокнопок**, которая содержит набор элементов для выбора одного варианта из серии связанных опций. Одновременно в группе может быть выбрана только одна радиокнопка. Обычно радиокнопки отображаются в виде небольших кружков, которые заполняются при выборе.

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
Радиокнопки похожи на [`checkbox`](checkbox.md), но элемент `radio` позволяет выбрать только одно значение из группы, в то время как `checkbox` позволяет выбирать несколько значений.
:::

## Свойства

### `checked` <decl type="boolean" get set listen />

Это свойство указывает, выбрана ли данная радиокнопка. Установка свойства `checked` позволяет переключать состояние выбора радиокнопки: если значение равно `true`, она отображается как выбранная.

Когда пользователь нажимает на радиокнопку, и ее состояние выбора изменяется, генерируется событие `checked`.

::: tip
Управление свойством `checked` не является рекомендуемым способом использования `radio`. Пожалуйста, используйте подход с [группой радиокнопок](#group).
:::

### `value` <decl type="any" get set />

Значение JavaScript, идентифицирующее радиокнопку, обычно это строка или число. Это значение не отображается визуально, но оно используется в [группе радиокнопок](#group).

### `group` <decl type="any" get set listen />

Если у вас есть несколько связанных компонентов `radio`, вы можете использовать комбинацию свойств `group` и `value`. Радиокнопки в одной группе взаимоисключающие: значение реактивного свойства, привязанного к `group`, равно свойству `value` выбранной радиокнопки. Например:
``` html
<radio value="red" model:group="color" />
<radio value="blue" model:group="color" />
<radio value="yellow" model:group="color" />
```
Здесь `color` — это реактивное свойство. Когда выбрана вторая радиокнопка, значение `color` становится равным `"blue"`. Если значение `color` не совпадает ни с одним `value` радиокнопок, ни одна из них не будет выбрана. Например:
``` html
<p on:click="color = null">reset select</p>
```
сбросит выбранное состояние:

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

По умолчанию радиокнопки являются строчными элементами. Их размер определяется CSS-свойством `font-size`, и они выравниваются по базовой линии текста. Пожалуйста, не задавайте вручную такие свойства, как `width` и `height`, так как это может привести к нарушению отображения.