# pullable

Компонент `pullable` используется для добавления функции инкрементальной загрузки или взаимодействия с обновлением, которые срабатывают при потягивании вниз в верхней части или потягивании вверх в нижней части прокручиваемого списка. По умолчанию компонент `pullable` является блочным элементом.

::: warning
<experimental /> Это экспериментальный компонент. Функциональность `pullable` нестабильна, а анимация может выглядеть недостаточно естественно.
:::

`pullable` должен быть первым или последним дочерним компонентом [`scroll`](scroll.md). Когда он является первым дочерним элементом, продолжение потягивания вниз в начале содержимого `scroll` вызывает событие `pulling`; наоборот, когда `pullable` является последним дочерним элементом `scroll`, потягивание вверх внизу вызывает событие `pulling`.

Компонент `pullable` по умолчанию находится в скрытом состоянии и отображается только при потягивании вверх/вниз. В следующем примере продемонстрировано использование компонента `pullable`.

<glyphix id="components-pullable-1" height="360" width="360" title="Загрузка дополнительных данных при потягивании вверх/вниз">

```html
<scroll scrollbar>
  <pullable :hold="pulldown" on:pulling="onPulldown">
    <progress-arc busy start-angle="0" stop-angle="360" />
    <p>{{pulldown || 'keep pull down...'}}</p>
  </pullable>
  <p for="item in items">item ({{item}})</p>
  <pullable :hold="pullup" on:pulling="onPullup">
    <progress-arc busy start-angle="0" stop-angle="360" />
    <p>{{pullup || 'keep pull up...'}}</p>
  </pullable>
</scroll>
```

```js
export default {
  data: {
    pulldown: null,
    pullup: null,
    items: []
  },
  first: 0,
  last: 0,
  onInit() {
    this.update(0, 10)
  },
  update(first, last) {
    for (let i = this.first; i > first; --i)
      this.items.unshift(i)
    for (let i = this.last; i < last; ++i)
      this.items.push(i)
    this.first = first
    this.last = last
  },
  onPulldown(event) {
    this.pulldown = event ? 'please release' : 'updating...'
    if (!event) {
      setTimeout(() => {
        this.update(this.first - 5, this.last)
        this.pulldown = null
      }, 1000)
    }
  },
  onPullup(event) {
    this.pullup = event ? 'please release' : 'updating...'
    if (!event) {
      setTimeout(() => {
        this.update(this.first, this.last + 5)
        this.pullup = null
      }, 1000)
    }
  }
}
```

```css
scroll {
  display: flex;
  flex-direction: column;
}

scroll > p {
  background-color: #ddd;
  border-radius: 32px;
  margin: 12px;
  padding: 32px;
  text-align: center;
}

pullable {
  display: flex;
  justify-content: center;
  margin: 32px;
}

pullable > progress-arc {
  stroke-width: 0.25rem;
  margin-right: 16px;
}
```

</glyphix>

Подробное описание использования см. в разделе [Инструкции по использованию](#使用说明).

## Свойства

### `hold` <decl type="bool" get set />

По умолчанию `pullable` виден только при потягивании вниз вверху или вверх внизу, но когда свойство `hold` имеет значение `true`, компонент `pullable` остается видимым. Это свойство обычно устанавливается, когда событие [`pulling`](#pulling) приводит к обновлению содержимого, и сбрасывается после завершения обновления содержимого.

### `pulling` <decl type="bool" get listen />

Событие `pulling` срабатывает, когда `pullable` вытягивается полностью. Значения события означают следующее:
- `true`: событие срабатывает при достижении порога полного вытягивания `pullable` при потягивании вниз/вверх;
- `false`: событие срабатывает, когда пользователь отпускает палец после достижения вышеуказанного условия полного вытягивания.

В следующем примере показан момент срабатывания значений события `pulling`. Вы можете попытаться плавно потянуть список вниз с самого верха и обратить внимание на всплывающее сообщение toast при срабатывании события `pulling`.

<glyphix id="components-pullable-pulling" height="360" width="360" title="Событие pulling">

```html
<scroll scrollbar>
  <pullable :hold="refresh" on:pulling="onPulling">
    <p>pulling...</p>
  </pullable>
  <p for="item in 10">item {{item}}</p>
</scroll>
```

```js
import prompt from '@system.prompt'

export default {
  data: {
    refresh: false
  },
  onPulling(event) {
    prompt.showToast({
      message: `pulling: ${event ? 'trigged' : 'release'}`
    })
    if (!event) {
      this.refresh = true
      setTimeout(() => this.refresh = false, 1000)
    }
  }
}
```

```css
scroll {
  display: flex;
  flex-direction: column;
}

scroll > p {
  background-color: #ddd;
  border-radius: 32px;
  margin: 12px;
  padding: 32px;
  text-align: center;
}

pullable {
  text-align: center;
  margin: 32px;
}
```

</glyphix>

## Инструкции по использованию

### Расположение компонента

Компонент `pullable` должен быть первым или последним дочерним элементом вертикального `scroll`. Он автоматически определяет режим работы в зависимости от своего расположения: если он является первым дочерним элементом, он определяет операцию потягивания пользователя вниз от верхней части списка, и наоборот.

Для списка, которому требуется только обновление при потягивании вниз, достаточно следующего использования:
```html
<scroll>
  <pullable :hold="refresh" on:pulling="onPulling">
    <p>pulling...</p>
  </pullable>
  <div for="item in items">
    ...
  </div>
</scroll>
```

В коде JavaScript вы можете прослушивать событие `pulling` и управлять свойством `refresh`:
``` js
export default {
  data: {
    refresh: false
  },
  onPulling(hold) {
    if (!hold) { // hold равен false, когда пользователь отпускает палец
      this.refresh = true // Означает, что идет обновление
      // В этом примере таймер используется для симуляции операции загрузки, а загрузка останавливается через 1 с
      setTimeout(() => this.refresh = false, 1000)
    }
  }
}
```

Конкретный эффект см. в примере в документации по событию [`pulling`](#pulling).

### Управление подсказками

Внутри компонента `pullable` можно размещать различные компоненты для отображения подсказок. Как показано в предыдущих примерах в этой статье, вы можете комбинировать анимацию загрузки и текст подсказки. Кроме того, значение события `pulling` можно использовать для управления содержимым подсказки. Обычно рекомендуется следующий подход к обработке состояния:
1. Установите реактивное свойство (например, `refresh`) для каждого компонента `pullable` со значением по умолчанию `null`. Свойство `refresh` также используется для управления свойством [`hold`](#hold) компонента `pullable`.
2. В начальном состоянии (то есть когда `refresh` имеет ложное значение) подсказка `pullable` должна призывать пользователя «продолжать тянуть для обновления».
3. Когда пользователь тянет вниз, срабатывает событие `pulling`. В зависимости от его значения выполните шаг 4 или 5.
4. Когда `pulling` равен `true`, пользователю следует подсказать: «Отпустите, чтобы начать обновление».
5. Когда `pulling` равен `false`, это означает, что пользователь отпустил палец. В это время вы должны установить `refresh` в значение `true` и начать обновление содержимого. Также следует сообщить пользователю: «Идет обновление».
6. После завершения обновления содержимого снова установите `refresh` в значение `false`, чтобы вернуться в исходное состояние.

Вы также можете обратиться к первому примеру в этом документе, который реализует функцию продолжения загрузки как при потягивании вниз вверху списка, так и при потягивании вверх внизу. В этом примере используется прием использования всего одного реактивного свойства для управления всеми состояниями `pullable`.

Этот прием устанавливает начальное значение реактивного свойства `refresh` равным `null` (что аналогично `false`) и использует следующий шаблон кода:
``` html
<pullable :hold="refresh" on:pulling="onPulling">
  <p>{{refresh || 'Продолжайте тянуть вниз'}}</p>
</pullable>
```
Когда свойство `refresh` не задано, подсказка по умолчанию «Продолжайте тянуть вниз» отображается сразу же после вытягивания `pullable`. Затем функцию обратного вызова события `onPulling` следует написать следующим образом:
``` js
export default {
  async onPulling(event) {
    this.refresh = event ? 'Пожалуйста, отпустите' : 'Обновление...'
    if (!event) { // Запуск операции обновления при отпускании
        await runRefreshJobs()
        this.refresh = null // Сброс состояния после завершения обновления
    }
  }
}
```

### Ограничения

В настоящее время компонент `pullable` имеет ряд ограничений. Помимо обязательного использования внутри вертикального компонента `scroll`, вам также необходимо убедиться, что количество элементов списка превышает размеры видимой области `scroll`, иначе могут возникнуть проблемы. Кроме того, интерактивный эффект `pullable` может оказаться несколько резким.