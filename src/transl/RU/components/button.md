# button

Компонент кнопки, по умолчанию является строчным элементом. При касании компонента генерируются соответствующие события.

## Свойства

### `checkable`  <decl type="boolean" set />

Если установлено значение `true`, это означает, что одно касание вызывает изменение состояния только один раз, а именно: переход из состояния нажатия в отпущенное состояние или из отпущенного в нажатое. При этом значение прослушивателя состояния `press` равно `true` для нажатия и `false` для отпускания.

### `toggleable` <decl type="boolean" set />

Если установлено значение `true`, это означает, что значение прослушивателя `press` может изменяться: при нажатии оно равно `true`, а при отпускании — `false`.

### `press` <decl type="boolean" get set listen />

Установка свойства `press` позволяет изменять состояние компонента. Также можно прослушивать состояние компонента с помощью директивы `on`. По умолчанию после завершения одного касания параметр обратного вызова равен `true`. Вы можете использовать свойства `checkable` и `toggleable` для получения различных значений и состояний прослушивания.

## Ограничения функциональности

### Сбой события `click`

Когда компонент `button` не используется, для прослушивания событий нажатия любых нативных компонентов обычно применяется свойство [`click`](/framework/generic/properties.md#click). Однако этот подход обычно не применим к `button`. Например, следующий код:
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
    // Останавливаем всплытие события, чтобы внешняя кнопка не реагировала на клик
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

Вы можете ожидать, что при нажатии на текст `"inner"` сработает метод `onInnerClick` и предотвратится вызов `onOuterClick`. Но вы обнаружите, что это не так (лучше открыть консоль браузера для просмотра логов): метод `onInnerClick` не сработает вообще, и на клик отреагирует только внешний компонент `button`, а именно:
- При клике на текст `inner` лог `inner click` не появится, будет только лог `outer click`;
- Сработает интерактив нажатия `button` (уменьшится прозрачность).

Это работает так же, как клик по внешнему тексту `outer text`. Причина этого заключается в том, что компонент `button` имеет приоритет при обработке всего жизненного цикла жеста нажатия (от нажатия до отпускания), в то время как событие `click` срабатывает в момент отпускания. Это означает, что независимо от того, останавливает ли обработчик события `click` внутреннего элемента всплытие, такое поведение изменить нельзя.

#### Решение

Чтобы решить эту проблему, следует прослушивать событие `press` внешней кнопки `button` и событие `touchstart` внутреннего элемента:

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
    // Останавливаем всплытие события, чтобы внешняя кнопка не реагировала на клик
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

Попробуйте пример выше, и вы увидите, что при нажатии на текст `inner` срабатывает только метод `onInnerClick`, `onOuterClick` не вызывается, а кнопка `button` не отображает визуальный эффект нажатия.

::: tip
Событие `press` обычно также срабатывает при отпускании, но оно требует, чтобы событие нажатия на кнопку никогда не было заблокировано. Следовательно, остановка всплытия в событии `touchstart` внутреннего элемента может предотвратить срабатывание события `press` внешней кнопки.
:::

#### Другие моменты срабатывания

Ограничение этого метода заключается в том, что событие `touchstart` внутреннего элемента срабатывает в момент нажатия. Вместо него вы также можете использовать событие `touchend` для срабатывания, но при этом необходимо сохранить функцию остановки всплытия в событии `touchstart`. Это гарантирует, что событие `press` внешней кнопки не сработает в момент нажатия.

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
    // Здесь не нужно останавливать всплытие, так как оно уже остановлено в touchstart
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

Откройте консоль браузера и снова нажмите на текст `inner` — вы увидите, что лог `onInnerClick` выведется только после отпускания кнопки, и это по-прежнему предотвратит реакцию внешней кнопки `button` на жест.