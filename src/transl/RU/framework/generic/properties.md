---
icon: xml
---
# Свойства и события

В этом разделе описываются общие интерфейсы свойств и события, которые предоставляются всеми нативными компонентами.

## Список свойств

### Общие свойства

#### `top` <decl type="number" get set listen />

Положение верхней границы компонента относительно родительского нативного компонента в пикселях. Это свойство по сути является сокращением для свойства `top` в инлайн-стилях. Подробнее о вариантах использования см. в разделе [Операции с позицией компонента](#операции-с-позицией-компонента).

При чтении или прослушивании свойства `top` возвращается вычисленное положение компонента, то есть фактическое измеренное значение после компоновки (layout).

#### `left` <decl type="number" get set listen />

Положение левой границы компонента относительно родительского нативного компонента в пикселях. Это свойство по сути является сокращением для свойства `left` in инлайн-стилях. Подробнее о вариантах использования см. в разделе [Операции с позицией компонента](#операции-с-позицией-компонента).

При чтении или прослушивании свойства `left` возвращается вычисленное положение компонента, то есть фактическое измеренное значение после компоновки.

#### `width` <decl type="number" get set listen />

Ширина компонента. При установке свойства `width` обновляется свойство [`width`](styles.md#width) в инлайн-стилях. Поскольку ширина в CSS использует модель `border-box`, к фактически сохраняемому значению стиля автоматически добавляются текущие размеры `padding` и `border` элемента, что гарантирует соответствие ширины содержимого после компоновки установленному значению.

При чтении или прослушивании свойства `width` возвращается ширина содержимого, вычисленная после компоновки (без учета `padding` и `border`).

#### `height` <decl type="number" get set listen />

Высота компонента. При установке свойства `height` обновляется свойство [`height`](styles.md#height) в инлайн-стилях. Поскольку высота в CSS использует модель `border-box`, к фактически сохраняемому значению стиля автоматически добавляются текущие размеры `padding` и `border` элемента, что гарантирует соответствие высоты содержимого после компоновки установленному значению.

При чтении или прослушивании свойства `height` возвращается высота содержимого, вычисленная после компоновки (без учета `padding` и `border`).

#### `show` <decl type="boolean" get set/>

Определяет, виден ли компонент. Скрытый компонент не отображается и не занимает место в структуре макета.

#### `quiescent` <decl type="boolean" get set/>

Определяет, должен ли снимок компонента обновляться автоматически (статичный снимок). Если компонент отображается с помощью снимка, и значение этого свойства равно `false` (значение по умолчанию), то при обновлении содержимого компонента снимок будет немедленно перерисован для обновления представления; в противном случае снимок обновляться не будет. Установка этого свойства в значение `true` может повысить производительность пользовательского интерфейса, но приведет к задержке отображения контента.

В следующем примере демонстрируется работа свойства `quiescent`. На экране внутри контейнера `scroll` размещены два элемента `p`, причем для контейнера `scroll` включен [режим снимков](../../components/scroll.md#snapshot). Когда пользователь прокручивает компонент `scroll`, для находящихся в нем элементов создаются снимки. Поскольку первый элемент `p` использует обычный режим снимков, а второй — режим статичного снимка, при прокрутке можно наблюдать обновление содержимого только первого элемента `p`.

<glyphix id="generic-properties-quiescent" height="200" title="Ленивые снимки">

``` html
<scroll snapshot scroll-snap="center">
  <p>normal snapshot {{ count }}</p>
  <p quiescent>quiescent snapshot {{ count }}</p>
</scroll>
```

``` css
scroll {
  display: flex;
  flex-direction: column;
  background-color: lightgray;
}

p {
  background-color: lightgreen;
  text-align: center;
  padding: 10px;
  margin: 10px;
}
```

``` js
export default {
  data: {
    count: 0
  },
  onReady(event) {
    setInterval(() => this.count++, 500)
  }
}
```

</glyphix>

#### `style` <decl type="string" set />

Устанавливает инлайн-стили компонента. В настоящее время поддерживаются только [CSS-свойства](./styles.md) с меткой <badge type="info" text="Инлайн" />.

#### `z-index` <decl type="number" get set />

Свойство `z-index` устанавливает порядок элементов по оси Z. Перекрывающиеся элементы с большим значением `z-index` будут располагаться поверх элементов с меньшим значением. Это значение свойства будет переопределено свойством [`z-index`](styles.md/#z-index) из CSS.


#### `opacity` <decl type="number" get set />

Задает прозрачность компонента. Диапазон значений составляет $[0, 1]$, где $0$ означает полную прозрачность. Эффект аналогичен CSS-свойству [`opacity`](styles.md#opacity).

::: warning
Значение `opacity` влияет на производительность отрисовки элементов. Подробности см. в описании CSS-свойства [`opacity`](styles.md#opacity).
:::

#### `transform` <decl type="string" set />

Задает трансформацию компонента, что эквивалентно CSS-свойству [`transform`](styles.md#transform).

#### `disabled` <decl type="boolean" get set />

Используется для установки или получения состояния блокировки компонента. Когда значение свойства равно `true`, элемент находится в заблокированном состоянии: пользователь не может взаимодействовать с ним, и элемент не реагирует на какие-либо жесты (такие как нажатия, перетаскивания и т. д.). Когда значение свойства равно значению **по умолчанию** `false`, компонент доступен, и пользователь может нормально с ним взаимодействовать.

В следующем примере демонстрируется использование свойства `disabled`, а также управление стилями с помощью псевдокласса [`:disabled`](styles.md#disabled). Пример показывает, что элемент `div` в обычном состоянии реагирует на жесты нажатия, но в состоянии `disabled` не реагирует ни на какие жесты.

<glyphix id="generic-properties-disabled" height="200" title="Свойство disabled">

``` html
<div :disabled="disabled" on:click="onClick">
  {{disabled ? 'disabled' : 'normal'}} <switch />
</div>
```

``` css
div {
  background-color: lightgray;
  text-align: center;
  display: flex;
  justify-content: center;
}

/* Псевдокласс :disabled позволяет управлять стилем элемента в состоянии disabled */
div:disabled {
  opacity: 0.5;
}
```

``` js
import prompt from '@system.prompt'

export default {
  data: {
    disabled: false
  },
  onInit() {
    setInterval(() => {
      this.disabled = !this.disabled
    }, 2000)
  },
  onClick() {
    prompt.showToast({ message: 'clicked!', duration: 250 })
  }
}
```

</glyphix>

### Общие события

Большинство нативных компонентов поддерживают общие события, которые можно прослушивать с помощью [директивы `on`](../commands/on.md). Типы значений этих событий описаны в разделе [Типы событий](#типы-событий).

#### `touchstart` <decl type="TouchEvent" listen />

Событие `touchstart` срабатывает, когда пользователь начинает касаться компонента. Значением события является тип [`TouchEvent`](#touchevent).

#### `touchmove` <decl type="TouchEvent" listen />

Событие `touchmove` срабатывает при перемещении точки касания по компоненту. Оно продолжает срабатывать в процессе перемещения, даже если точка касания вышла за пределы текущего нативного компонента. Значением события является тип [`TouchEvent`](#touchevent).

Между состояниями `touchstart` и `touchmove` существует определенная «мертвая зона перемещения» (dead zone): если расстояние прокрутки при касании меньше этой зоны, событие `touchmove` не сработает. Размер мертвой зоны зависит от устройства. В следующем примере показана мертвая зона перемещения.

<glyphix id="generic-properties-touchmove" height="200" title="Мертвая зона перемещения">

``` html
<p on:touchstart="state = 'start'"
   on:touchmove="onTouchMove($event)"
   on:touchend="onTouchEnd">
  {{ `state: ${state} \ndead area: (${dx}, ${dy})` }}
</p>
```

``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```

``` js
export default {
  data: {
    state: null,
    dx: null,
    dy: null
  },
  onTouchMove(event) {
    if (!this.dx && !this.dy) {
      this.state = 'move'
      this.dx = event.touches[0].offsetX
      this.dy = event.touches[0].offsetY
    }
  },
  onTouchEnd() {
    this.state = 'end'
    this.dx = this.dy = null
  }
}
```

</glyphix>

#### `touchend` <decl type="TouchEvent" listen />

Когда точка касания пользователя покидает экран, нативному компоненту, к которому прикасались ранее, отправляется событие `touchend`. Значением события является тип [`TouchEvent`](#touchevent).

#### `touchcancel` <decl type="TouchEvent" listen />

Событие `touchcancel` срабатывает при прерывании касания нативного компонента. Значением события является тип [`TouchEvent`](#touchevent). Касание может прерываться по разным причинам, например, если компонент был скрыт или событие касания было принудительно перехвачено другим элементом.

#### `click` <decl type="ClickEvent" listen />

Событие `click` срабатывает при нажатии на нативный компонент и последующем отпускании палица/курсора. Значением события является тип [`ClickEvent`](#clickevent).

<glyphix id="generic-properties-click" height="100">

``` html
<p on:click="click = JSON.stringify($event)">
  {{ click }}
</p>
```

``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```

``` js
export default {
  data: {
    click: null
  }
}
```

</glyphix>

#### `longpress` <decl type="LongPressEvent" listen />

Событие `longpress` срабатывает при длительном нажатии на нативный компонент. Значением события является тип [`LongPressEvent`](#longpressevent). Следующий интерактивный пример демонстрирует моменты срабатывания `longpress` и других событий:

<glyphix id="generic-properties-longpress" height="100">

``` html
<p on:touchstart="state = 'touching...'"
   on:longpress="state = `longpress: ${JSON.stringify($event)}`"
   on:click="state = 'clicked.'">
  {{ state }}
</p>
```

``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```

``` js
export default {
  data: {
    state: null
  }
}
```

</glyphix>

Момент срабатывания и длительность события `longpress` зависят от устройства; обычно оно срабатывает после удержания в течение $500 \rm ms$. В отличие от события [`click`](#click), `longpress` срабатывает во время удержания, а не в момент отпускания. В приведенном выше примере вы заметите следующее:
- Если время удержания меньше времени срабатывания долгого нажатия, то при отпускании сработает событие `click`;
- Если удерживать палец достаточно долго, сработает событие `longpress`, а после отпускания сработает событие `click` (отобразится статус «clicked.»);
- Перемещение пальца во время удержания предотвратит срабатывание событий `longpress` и `click`.

#### `swipe` <decl type="SwipeEvent" listen />

Событие `swipe` срабатывает при быстром свайпе (смахивании) по компоненту. Значением события является тип [`SwipeEvent`](#swipeevent).

<glyphix id="generic-properties-swipe" height="250" >

``` html
<p on:swipe="onSwipe($event)">
  {{ swipe }}
</p>
```

``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```

``` js
export default {
  data: {
    swipe: null
  },
  onSwipe(event) {
    this.swipe = event.direction
    event.strongResponse()
  }
}
```

</glyphix>

#### `keydown` <decl type="KeyEvent" listen />

Событие срабатывает при нажатии аппаратной клавиши. События `keydown` и `keyup` используются для перехвата действий с физическими кнопками. Для перехвата событий нативный компонент должен находиться в фокусе. Корневой элемент страницы всегда получает фокус автоматически, поэтому следующий код позволяет перехватывать события `keydown` и `keyup`:
``` html
<!-- Предполагается, что это корневой элемент страницы -->
<div on:keydown="console.log($event)" on:keyup="console.log($event)">
  ...
</div>
```
Описание типа значения события см. в разделе [`KeyEvent`](#keyevent).

Устройства-часы обычно регистрируют [обработчик клавиш по умолчанию](/api/system-internal.md#setdefaultkeyhandler), поэтому код приложения может взаимодействовать с ними, даже не реагируя на такие события напрямую (например, при нажатии кнопки питания некоторые часы возвращаются на предыдущую страницу). Чтобы заблокировать реакцию на клавишу по умолчанию, используйте метод `stopPropagation()` объекта `KeyEvent` для предотвращения всплытия.

#### `keyup` <decl type="KeyEvent" listen />

Событие срабатывает при отпускании клавиши. Подробнее см. в описании события [`keydown`](#keydown).

#### `wheel` <decl type="WheelEvent" listen />

Событие `wheel` срабатывает при вращении колесика. К устройствам с колесиком относятся вращающаяся заводная головка (колесико) часов, колесико мыши и т. д. Для перехвата этого события нативный компонент должен находиться в фокусе. Корневой элемент страницы всегда получает фокус автоматически, поэтому следующий код позволяет перехватывать событие `wheel`:
``` html
<!-- Предполагается, что это корневой элемент страницы -->
<div on:wheel="console.log($event)">
  ...
</div>
```
Описание типа значения события см. в разделе [`WheelEvent`](#wheelevent).

## Типы событий

### `BaseEvent`

Объект события `BaseEvent` предоставляет методы для управления передачей событий. Его прототип выглядит следующим образом:
``` ts
interface BaseEvent {
  strongResponse(): void, // Принудительный ответ на событие (strong response)
  stopPropagation(): void // Остановить всплытие события
}
```

### `TouchEvent`

Прототип объекта события `TouchEvent`:
``` ts
interface TouchEvent extends BaseEvent {
  isTarget: boolean, // Является ли цель события текущим компонентом
  touches: { // Данные всех точек касания для данного события
    clientX: number, // Координата X точки касания относительно области содержимого целевого компонента
    clientY: number, // Координата Y точки касания относительно области содержимого целевого компонента
    offsetX: number, // Смещение точки касания по оси X в процессе движения
    offsetY: number  // Смещение точки касания по оси Y в процессе движения
  }[];
}
```

### `ClickEvent`

Прототип объекта события `ClickEvent`:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Является ли цель события текущим компонентом
  clientX: number, // Координата X точки нажатия относительно области содержимого целевого компонента
  clientY: number // Координата Y точки нажатия относительно области содержимого целевого компонента
}
```

### `LongPressEvent`

Прототип объекта события `LongPressEvent`:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Является ли цель события текущим компонентом
  clientX: number, // Координата X точки долгого нажатия относительно области содержимого целевого компонента
  clientY: number // Координата Y точки долгого нажатия относительно области содержимого целевого компонента
}
```

### `SwipeEvent`

Прототип объекта события `SwipeEvent`:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Является ли цель события текущим компонентом
  direction: 'left' | 'right' | 'up' | 'down' // Направление свайпа
}
```

### `KeyEvent`

Объект `KeyEvent` описывает взаимодействие пользователя с физическими кнопками. Этот тип используется для свойств событий [`keydown`](#keydown) и [`keyup`](#keyup) элементов. Прототип объекта события `KeyEvent`:
``` ts
interface KeyEvent  {
  type: 'keydown' | 'keyup', // Тип события клавиши
  key: string, // Имя клавиши
  timestamp: number, // Временная метка ( timestamp ) отправки события клавиши в миллисекундах
  stopPropagation(): void // Вызов этого метода предотвращает всплытие события
}
```

В настоящее время поддерживаются следующие имена клавиш:
- `'Power'` — кнопка питания часов;
- `'Fn'` — функциональная кнопка часов;
- Другие символьные клавиши обозначаются одним символом, например, буква `'A'`, дефис `'-'` и т. д.

### `WheelEvent`

Объект `WheelEvent` описывает взаимодействие пользователя с вращающимся колесиком. Этот тип используется для свойства события [`wheel`](#wheel) элементов. Сигнатура объекта `WheelEvent`:
``` ts
interface WheelEvent {
  deltaY: number, // Приращение прокрутки колесика по оси Y
  stopPropagation(): void // Вызов этого метода предотвращает всплытие события
}
```

В отличие от [wheel event](https://developer.mozilla.org/en-US/docs/Web/API/Element/wheel_event) в веб-стандартах, `WheelEvent` в Glyphix в настоящее время содержит только свойство `deltaY`.

## Механизм реагирования на события

### Всплытие событий (Bubbling)

События касаний и жестов поддерживают всплытие (bubbling). Всплытие означает, что когда событие происходит на каком-то элементе, оно сначала выполняет обработчик на этом элементе, затем на его родительском элементе и так далее вверх по цепочке предков. В следующем примере зеленый компонент `p` и серый компонент `div` оба прослушивают события касания. При нажатии на компонент `p` можно заметить, что событие получают как компонент `p`, так и компонент `div`.

<glyphix id="generic-event-bubbling" height="250" title="Всплытие событий касания">

``` html
<div on:touchstart="onTouch('div', $event)"
     on:touchmove="onTouch('div', $event)"
     on:touchend="onRelease('div', $event)">
  <p on:touchstart="onTouch('p', $event)"
     on:touchmove="onTouch('p', $event)"
     on:touchend="onRelease('p', $event)">
    {{ `touchs: ${touchs.div ? 'div' : '-'} ${touchs.p ? 'p' : '-'}, target: ${target}` }}
  </p>
</div>
```

``` css
div {
  display: flex;
  flex-direction: column;
  background-color: lightgray;
  justify-content: space-around;
}

p {
  background-color: lightgreen;
  text-align: center;
  height: 150px;
}
```

``` js
export default {
  data: {
    touchs: { div: false, p: false },
    target: null
  },
  onTouch(name, event) {
    this.touchs[name] = true
    // Свойство isTarget позволяет определить, является ли целью события компонент, который в данный момент прослушивает это событие
    if (event.isTarget)
      this.target = name
  },
  onRelease(name, event) {
    this.touchs[name] = false
    if (event.isTarget)
      this.target = null
  }
}
```

</glyphix>

В Glyphix всплывают только события касаний и жестов, описанные в этом документе. В настоящее время перехват событий (capturing) в коде JavaScript не поддерживается.

### Предотвращение всплытия событий

Используйте метод `stopPropagation()` объекта `BaseEvent`, чтобы предотвратить всплытие события к родительским элементам.

### Принудительный ответ на событие (Strong Response)

В Glyphix события касаний и жестов имеют два приоритета реагирования: сильный (strong response) и слабый (weak response). Если на одно событие претендуют несколько целей, приоритет сильного ответа выше приоритета слабого. Предположим, на странице есть 3 уровня родительских и дочерних элементов: `A -> B -> C`, где `C` имеет слабый ответ на событие, а `B` — сильный. В этом случае событие будет передано в `B`, а до `C` оно уже не дойдет. Элемент, имевший изначально сильный ответ на событие, может перенаправить событие повторно, если его перевести в режим слабого ответа.

События касаний и жестов из раздела [Общие события](#общие события) по умолчанию имеют слабый ответ. В следующем примере зеленый компонент `p` помещен внутрь серого контейнера `scroll` и прослушивает все события касания компонента `p`. Поскольку `scroll` по умолчанию имеет сильный ответ на вертикальные жесты свайпа, слабый ответ на горизонтальные жесты и не реагирует на остальные жесты, в процессе работы можно наблюдать следующее:
- При нажатии на компонент `p` срабатывает событие `touchstart`, а при отпускании — `touchend`;
- При горизонтальном перетаскивании компонента `p` срабатывает событие `touchmove`;
- При вертикальном перетаскивании компонента `p`, поскольку родительский компонент `scroll` имеет сильный ответ на вертикальную прокрутку, а компонент `p` в коде шаблона имеет слабый ответ только на `touchmove`, вертикальное перетаскивание будет перехвачено компонентом `scroll`, а компонент `p` получит событие `touchcancel`.

<glyphix id="generic-event-strong-response-1" height="250" title="Сильный ответ на событие">

``` html
<scroll>
  <p on:touchstart="state = 'touchstart'"
     on:touchmove="state = 'touchmove'"
     on:touchend="state = 'touchend'"
     on:touchcancel="state = 'touchcancel'">
    {{ `p.state: ${state}` }}
  </p>
</scroll>
```

``` css
scroll {
  background-color: lightgray;
}

p {
  background-color: lightgreen;
  text-align: center;
  height: 150px;
  margin: 50px;
}
```

``` js
export default {
  data: {
    state: null
  }
}
```

</glyphix>

Механизм обработки жестов по умолчанию у многих нативных компонентов настроен на сильный ответ. Метод `strongResponse()` объекта `BaseEvent` позволяет явно указать в коде JavaScript режим сильного ответа для события. В следующем примере внешний серый компонент `div` дает сильный ответ на жесты, поэтому даже при касании внутреннего элемента `p` после начала жеста событие будет отправляться исключительно компоненту `div`.

<glyphix id="generic-event-strong-response-2" height="250" title="Сильный ответ на событие">

``` html
<div on:touchstart="onTouch('div', 'start', $event)"
     on:touchmove="onTouch('div', 'move', $event)"
     on:touchend="onTouch('div', 'end', $event)"
     on:touchcancel="onTouch('div', 'cancel', $event)">
  <p on:touchstart="onTouch('p', 'start', $event)"
     on:touchmove="onTouch('p', 'move', $event)"
     on:touchend="onTouch('p', 'end', $event)"
     on:touchcancel="onTouch('p', 'cancel', $event)">
    {{ `div state: ${touchs.div}, p state: ${touchs.p}, target: ${target}` }}
  </p>
</div>
```

``` css
div {
  display: flex;
  flex-direction: column;
  background-color: lightgray;
  justify-content: space-around;
}

p {
  background-color: lightgreen;
  text-align: center;
  height: 150px;
}
```

``` js
export default {
  data: {
    touchs: { div: null, p: null },
    target: null
  },
  onTouch(name, state, event) {
    console.log(name, state, event.isTarget)
    this.touchs[name] = state
    // Свойство isTarget позволяет определить, является ли целью события компонент, который в данный момент прослушивает это событие.
    // Если это событие cancel, цель не записывается.
    if (event.isTarget && state != 'cancel')
      this.target = name
    if (name == 'div')
      event.strongResponse()
  }
}
```

</glyphix>

### Обработка событий по умолчанию на странице

Страница по умолчанию имеет слабый ответ на жесты и предотвращает всплытие событий, поэтому события жестов не могут передаваться и распространяться сквозь страницу. Кроме того, страница закрывается при получении жеста `touchmove` вправо. Разработчики также могут перехватывать жесты, чтобы отключить эту особенность.

Для этого нужно прослушивать жест `touchmove` компонента страницы и останавливать всплытие:
``` html
<!-- Этот div является корневым компонентом страницы -->
<div on:touchmove="$event.stopPropagation()">
  ...
</div>
```
После этого страница перестанет закрываться по свайпу вправо, но ее по-прежнему можно будет закрыть нажатием физической кнопки Power. Чтобы заблокировать возврат по нажатию кнопки, можно использовать следующий подход:
``` html
<!-- Этот div является корневым компонентом страницы -->
<div on:keydown="onKeyup">
  ...
</div>
```

``` js
export default {
  onKeyup(event) {
    // Если значение клавиши 'Power', останавливаем всплытие, чтобы предотвратить закрытие страницы
    if (event.key == 'Power')
      event.stopPropagation()
  }
}
```

::: warning
Относитесь с осторожностью к изменению стандартного механизма обработки событий страницы, чтобы избежать ситуаций, когда пользователь не сможет вернуться со страницы.
:::

::: tip
В предыдущих версиях для предотвращения стандартного поведения возврата на странице использовался жест `swipe`, однако начиная с версии 0.6.4 этот способ устарел. Используйте описанную выше обработку события `touchmove`. Это изменение связано с тем, что интерактивная анимация возврата страницы (т.е. закрытие вслед за пальцем) была полностью несовместима с семантикой блокировки возврата через `swipe`.
:::

## Советы по использованию

### Операции с позицией компонента

Используя свойства `top` и `left` нативного компонента, можно легко изменять его положение:
``` html
<div :top="40" :left="20"> ... </div>
```
Поскольку `top` и `left` на самом деле являются сокращениями для одноименных CSS-свойств, они работают только при абсолютном позиционировании (absolute layout), которое задается с помощью следующего CSS:
``` css
div {
  position: absolute;
}
```

Затем вы можете использовать реактивные свойства для изменения положения компонента. В следующем примере показано случайное перемещение компонента с анимацией в сочетании с [модификатором `transition`](/framework/component/prop-modifier.md#transition-модификатор).

<glyphix id="generic-widget-position" height="250" title="Случайная позиция компонента">

``` html
<div id="pane">
  <p id="tile" :top="top" :left="left"
     top.transition left.transition>
    Tile
  </p>
</div>
```

``` css
div {
  background-color: lightgray;
}

p {
  /* Чтобы использовать свойства top / left компонента, он должен иметь абсолютное позиционирование */
  position: absolute;
  background-color: lightgreen;
  text-align: center;
  width: 3rem;
  height: 3rem;
  border: 4px solid red;
  border-radius: 10%;
}
```

``` js
export default {
  data: {
    top: 0,
    left: 0
  },
  timer: null,
  onReady() {
    // Получаем объекты компонентов, диапазон позиций не должен выходить за пределы контейнера #pane
    const pane = this.$element("pane")
    const tile = this.$element("tile")
    const width = pane.width - tile.width
    const height = pane.height - tile.height
    this.timer = setInterval(() => {
      this.top = Math.random() * height
      this.left = Math.random() * width
    }, 2000)
  },
  onDestroy() {
    clearInterval(this.timer)
  }
}
```

</glyphix>

В этом примере положение компонента `#tile` случайным образом меняется каждые две секунды, не выходя за границы контейнера `#pane`. Модификатор `transition` по умолчанию воспроизводит анимацию перехода длительностью в $1$ секунду.