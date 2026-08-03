# button

Компонент кнопки, по умолчанию является строчным элементом. При касании компонента генерируются соответствующие события.

## Свойства

### `checkable`  <decl type="boolean" set />

Если установлено значение `true`, это означает, что одно касание вызывает изменение состояния только один раз, а именно: переход из состояния нажатия в отпущенное или из отпущенного в нажатое. При этом значение прослушивателя состояния нажатия `press` равно `true`, а для отпущенного состояния — `false`.

### `toggleable` <decl type="boolean" set />

Если установлено значение `true`, это означает, что значение прослушивателя `press` может изменяться: при нажатии оно равно `true`, а при отпускании — `false`.

### `press` <decl type="boolean" get set listen />

При установке свойства `press` можно изменить состояние компонента. Состояние компонента также можно отслеживать с помощью директивы `on`. По умолчанию после завершения одного касания параметр обратного вызова равен `ture`. Вы можете использовать свойства `checkable` и `toggleable` для получения различных значений прослушивателя и состояний.

## Ограничения функциональности

### Сбой события `click`

Когда компонент `button` не используется, для прослушивания событий клика любых нативных компонентов обычно применяется свойство [`click`](/framework/generic/properties.md#click). Однако этот подход обычно не применим к `button`. Например, следующий код:
```html
<button on:click="onOuterClick">
  <p on:click="onInnerClick">inner</p>
  outer button
</button>
```

```js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    // 阻止事件冒泡，以免外层按钮响应点击事件
    event.stopPropagation();
    console.log('inner click');
  }
}
```

<glyphix id="components-button-click-1" height="48" width="360" inline>

``` html
<button on:click="onOuterClick">
  <p on:click="onInnerClick">inner</p>
  outer button
</button>
```

``` css
button {
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}

button:active {
  opacity: 0.5;
}

p {
  border: 2px solid #444;
  padding: 0 10px;
}
```

``` js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    event.stopPropagation();
    console.log('inner click');
  }
}
```

</glyphix>

Вы можете ожидать, что при нажатии на текст `"inner"` сработает метод `onInnerClick` и предотвратит выполнение `onOuterClick`. Но вы обнаружите, что это не так (лучше открыть консоль браузера для просмотра логов): метод `onInnerClick` вообще не вызывается, а на клик реагирует только внешний компонент `button`, то есть:
- При нажатии на текст `inner` лог `inner click` не появляется, выводится только лог `outer click`;
- Срабатывает интерактивный эффект нажатия `button` (снижение прозрачности).

Это происходит так же, как при клике на внешний текст `outer text`. Причина такого поведения заключается в том, что компонент `button` имеет приоритет в обработке всего жизненного цикла жеста нажатия (от нажатия до отпускания пальца), в то время как событие `click` срабатывает в момент отпускания. Это означает, что независимо от того, предотвращает ли обработчик события `click` внутреннего элемента всплытие события, такое поведение не изменится.

#### Решение

Для решения этой проблемы следует прослушивать событие `press` внешнего элемента `button` и событие `touchstart` внутреннего элемента:

```html
<button on:press="onOuterClick">
  <p on:touchstart="onInnerClick">inner</p>
  outer button
</button>
```

```js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    // 阻止事件冒泡，以免外层按钮响应点击事件
    event.stopPropagation();
    console.log('inner click');
  }
}
```

<glyphix id="components-button-click-2" height="48" width="360" inline>

``` html
<button on:press="onOuterClick">
  <p on:touchstart="onInnerClick">inner</p>
  outer button
</button>
```

``` css
button {
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}

button:active {
  opacity: 0.5;
}

p {
  border: 2px solid #444;
  padding: 0 10px;
}
```

``` js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    event.stopPropagation();
    console.log('inner click');
  }
}
```

</glyphix>

Попробуйте пример выше, и вы заметите, что при нажатии на текст `inner` вызывается только метод `onInnerClick`, метод `onOuterClick` не вызывается, а кнопка `button` не отображает визуальный эффект нажатия.

::: tip
Событие `press` обычно также срабатывает при отпускании пальца, но оно требует, чтобы событие нажатия на кнопку никогда не было заблокировано. Следовательно, остановка всплытия в событии `touchstart` внутреннего элемента может предотвратить срабатывание события `press` внешней кнопки.
:::

#### Другие моменты срабатывания

Ограничение этого метода заключается в том, что событие `touchstart` внутреннего элемента срабатывает в момент нажатия. Вы также можете использовать событие `touchend` для срабатывания, но при этом необходимо сохранить функцию остановки всплытия (stopPropagation) для события `touchstart`. Это гарантирует, что событие `press` внешней кнопки не сработает в момент нажатия.

```html
<button on:press="onOuterClick">
  <p on:touchstart="$event.stopPropagation()" on:touchend="onInnerClick">inner</p>
  outer button
</button>
```

```js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    // 这里不需要阻止冒泡，因为已经在 touchstart 阻止了
    console.log('inner click');
  }
}
```

<glyphix id="components-button-click-3" height="48" width="360" inline>

``` html
<button on:press="onOuterClick">
  <p on:touchstart="$event.stopPropagation()" on:touchend="onInnerClick">inner</p>
  outer button
</button>
```

``` css
button {
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}

button:active {
  opacity: 0.5;
}

p {
  border: 2px solid #444;
  padding: 0 10px;
}
```

``` js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    console.log('inner click');
  }
}
```

</glyphix>

Откройте консоль браузера и снова нажмите на текст `inner` — вы увидите, что лог `onInnerClick` выведется только после отпускания пальца, и внешний `button` по-прежнему не отреагирует на жест.