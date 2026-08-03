---
icon: xml
---
# Свойства и события

В этом разделе описываются общие интерфейсы свойств и событий, предоставляемые всеми нативными компонентами.

## Список свойств

### Общие свойства

#### `top` <decl type="number" get set listen />

Положение верхней границы компонента относительно родительского нативного компонента в пикселях. Это свойство фактически является сокращением для свойства `top` в инлайн-стилях. Подробнее об использовании см. в разделе [Операции с позиционированием компонентов](#组件位置操作).

При чтении или прослушивании (listen) свойства `top` возвращается вычисленное положение компонента, то есть его фактическое измеренное значение после компоновки (layout).

#### `left` <decl type="number" get set listen />

Положение левой границы компонента относительно родительского нативного компонента в пикселях. Это свойство фактически является сокращением для свойства `left` в инлайн-стилях. Подробнее об использовании см. в разделе [Операции с позиционированием компонентов](#组件位置操作).

При чтении или прослушивании свойства `left` возвращается вычисленное положение компонента, то есть его фактическое измеренное значение после компоновки.

#### `width` <decl type="number" get set listen />

Ширина компонента. При установке свойства `width` обновляется свойство [`width`](styles.md#width) в инлайн-стилях. Поскольку ширина в CSS использует модель `border-box`, к фактически сохраняемому значению стиля автоматически добавляются текущие размеры `padding` и `border` элемента, что гарантирует соответствие ширины содержимого после компоновки заданному значению.

При чтении или прослушивании свойства `width` возвращается ширина содержимого, вычисленная после компоновки, без учета `padding` и `border`.

#### `height` <decl type="number" get set listen />

Высота компонента. При установке свойства `height` обновляется свойство [`height`](styles.md#height) в инлайн-стилях. Поскольку высота в CSS использует модель `border-box`, к фактически сохраняемому значению стиля автоматически добавляются текущие размеры `padding` и `border` элемента, что гарантирует соответствие высоты содержимого после компоновки заданному значению.

При чтении или прослушивании свойства `height` возвращается высота содержимого, вычисленная после компоновки, без учета `padding` и `border`.

#### `show` <decl type="boolean" get set/>

Определяет, видим ли компонент. Скрытые компоненты не отображаются и не занимают пространство в макете.

#### `quiescent` <decl type="boolean" get set/>

Управляет тем, обновляется ли снимок (snapshot) компонента автоматически (статичный снимок). Если компонент отображается с помощью снимка, то при значении `quiescent` равном `false` (значение по умолчанию) снимок будет немедленно перерисовываться при обновлении содержимого компонента для актуализации вида, в противном случае — нет. Установка этого свойства в значение `true` может повысить производительность интерфейса, но приведет к задержке отображения контента.

В следующем примере демонстрируется работа свойства `quiescent`. Внутри контейнера `scroll` размещены два элемента `p`, причем для контейнера `scroll` включен [режим снимков](../../components/scroll.md#snapshot). Когда пользователь прокручивает компонент `scroll`, для находящихся в нем элементов создаются снимки. Поскольку первый элемент `p` использует обычный режим снимков, а второй — режим статичного снимка, при прокрутке можно заметить обновление содержимого только у первого элемента `p`.

<glyphix id="generic-properties-quiescent" height="200" title="Ленивый снимок">

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

Установка инлайн-стилей компонента. В настоящее время поддерживаются только [CSS-свойства](./styles.md) с меткой <badge type="info" text="Инлайн" />.

#### `z-index` <decl type="number" get set />

Свойство `z-index` задает порядок наложения элементов по оси Z. Перекрывающиеся элементы с большим значением `z-index` будут отображаться поверх элементов с меньшим значением. Это значение свойства будет перезаписано CSS-свойством [`z-index`](styles.md/#z-index).

#### `opacity` <decl type="number" get set />

Задает прозрачность компонента, значение лежит в диапазоне $[0, 1]$, где $0$ означает полную прозрачность. Эффект аналогичен CSS-свойству [`opacity`](styles.md#opacity).

::: warning
Значение `opacity` влияет на производительность отрисовки элементов. Подробности см. в описании CSS-свойства [`opacity`](styles.md#opacity).
:::

#### `transform` <decl type="string" set />

Задает трансформацию компонента, эквивалентно CSS-свойству [`transform`](styles.md#transform).

#### `disabled` <decl type="boolean" get set />

Используется для установки или получения состояния блокировки компонента. Когда значение свойства равно `true`, элемент находится в заблокированном состоянии, пользователь не может с ним взаимодействовать, и элемент не реагирует ни на какие жесты (такие как клики, перетаскивания и т.д.). Когда значение свойства **по умолчанию** равно `false`, компонент доступен, и пользователь может нормально с ним взаимодействовать.

В следующем примере продемонстрировано использование свойства `disabled`, а также управление стилями с помощью псевдокласса [`:disabled`](styles.md#disabled). Пример показывает, что элемент `div` реагирует на клики в обычном состоянии, но не реагирует ни на какие жесты в состоянии `disabled`.

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

/* Псевдокласс :disabled позволяет управлять стилями элемента в заблокированном состоянии */
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

Большинство нативных компонентов поддерживают общие события, для их прослушивания можно использовать [директиву `on`](../commands/on.md). Типы значений этих событий описаны в разделе [Типы событий](#事件类型).

#### `touchstart` <decl type="TouchEvent" listen />

Событие `touchstart` срабатывает, когда пользователь начинает касание компонента. Значение события имеет тип [`TouchEvent`](#touchevent).

#### `touchmove` <decl type="TouchEvent" listen />

Событие `touchmove` срабатывает при перемещении точки касания по компоненту. Оно продолжает генерироваться во время движения, даже если точка касания вышла за пределы текущего нативного компонента. Значение события имеет тип [`TouchEvent`](#touchevent).

При переходе состояния касания от `touchstart` к `touchmove` существует определенная «мертвая зона перемещения» (dead zone): если расстояние скольжения пальца пользователя меньше размера мертвой зоны, событие `touchmove` не сработает. Размер мертвой зоны зависит от устройства. В следующем примере продемонстрирована мертвая зона перемещения.

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

Когда точка касания пользователя покидает экран, ранее затронутому нативному компоненту отправляется событие `touchend`. Значение события имеет тип [`TouchEvent`](#touchevent).

#### `touchcancel` <decl type="TouchEvent" listen />

Событие `touchcancel` срабатывает при прерывании касания нативного компонента. Значение события имеет тип [`TouchEvent`](#touchevent). Касание может быть прервано по разным причинам, например, если компонент был скрыт или событие касания было принудительно перехвачено другим элементом.

#### `click` <decl type="ClickEvent" listen />

Событие `click` срабатывает, когда нативный компонент нажимают и отпускают. Значение события имеет тип [`ClickEvent`](#clickevent).

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

Событие `longpress` срабатывает при длительном нажатии на нативный компонент. Значение события имеет тип [`LongPressEvent`](#longpressevent). Следующий интерактивный пример демонстрирует моменты срабатывания `longpress` и других событий:

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

Момент срабатывания и длительность события `longpress` зависят от устройства, обычно оно срабатывает через $500 \rm ms$ после начала нажатия. В отличие от события [`click`](#click), `longpress` срабатывает *во время* удержания, а не в момент отпускания пальца. Из примера выше вы можете заметить, что:
- Если время нажатия меньше порога срабатывания длинного нажатия, при отпускании пальца сработает событие `click`;
- Если удерживать палец достаточно долго, сработает событие `longpress`, а при отпускании — событие `click` (отобразится состояние «clicked.»);
- Перемещение пальца во время нажатия отменяет срабатывание событий `longpress` или `click`.

#### `swipe` <decl type="SwipeEvent" listen />

Событие `swipe` срабатывает при быстром свайпе (смахивании) компонента. Значение события имеет тип [`SwipeEvent`](#swipeevent).

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

Событие срабатывает при нажатии аппаратной клавиши. События `keydown` и `keyup` используются для перехвата действий с физическими кнопками. Чтобы событие могло быть перехвачено, нативный компонент должен находиться в фокусе. Корневой элемент страницы всегда автоматически получает фокус, поэтому следующий код позволит перехватить события `keydown` и `keyup`:
``` html
<!-- Предполагается, что это корневой элемент страницы -->
<div on:keydown="console.log($event)" on:keyup="console.log($event)">
  ...
</div>
```
Описание типа значения события см. в [`KeyEvent`](#keyevent).

Устройства-часы обычно регистрируют [обработчик клавиш по умолчанию](/api/system-internal.md#setdefaultkeyhandler), поэтому код приложения может взаимодействовать с ними, даже если явно не обрабатывает такие события (например, при нажатии кнопки Power некоторые часы возвращаются на предыдущую страницу). Чтобы предотвратить реакцию на кнопку по умолчанию, вы можете использовать метод `stopPropagation()` объекта `KeyEvent` для остановки всплытия.

#### `keyup` <decl type="KeyEvent" listen />

Событие срабатывает при отпускании клавиши. Подробнее см. в описании события [`keydown`](#keydown).

#### `wheel` <decl type="WheelEvent" listen />

Событие `wheel` срабатывает при вращении колесика прокрутки. К устройствам с колесиком относятся вращающийся безель (корона) часов или колесико мыши. Чтобы перехватить это событие, нативный компонент должен находиться в фокусе. Корневой элемент страницы всегда автоматически получает фокус, поэтому следующий код перехватит событие `wheel`:
``` html
<!-- Предполагается, что это корневой элемент страницы -->
<div on:wheel="console.log($event)">
  ...
</div>
```
Описание типа значения события см. в [`WheelEvent`](#wheelevent).

## Типы событий

### `BaseEvent`

Объект события `BaseEvent` предоставляет методы для управления распространением событий, его прототип выглядит так:
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
  isTarget: boolean, // Является ли целью события текущий компонент
  touches: { // Данные обо всех точках касания в текущем событии
    clientX: number, // X-координата точки касания относительно области содержимого целевого компонента
    clientY: number, // Y-координата точки касания относительно области содержимого целевого компонента
    offsetX: number, // Смещение точки касания по оси X в процессе движения
    offsetY: number  // Смещение точки касания по оси Y в процессе движения
  }[];
}
```

### `ClickEvent`

Прототип объекта события `SwipeEvent` (прим. переводчика: в документации оригинала опечатка в имени интерфейса, относится к ClickEvent):
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Является ли целью события текущий компонент
  clientX: number, // X-координата точки клика относительно области содержимого целевого компонента
  clientY: number // Y-координата точки клика относительно области содержимого целевого компонента
}
```

### `LongPressEvent`

Прототип объекта события `LongPressEvent`:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Является ли целью события текущий компонент
  clientX: number, // X-координата точки длинного нажатия относительно области содержимого целевого компонента
  clientY: number // Y-координата точки длинного нажатия относительно области содержимого целевого компонента
}
```

### `SwipeEvent`

Прототип объекта события `SwipeEvent`:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Является ли целью события текущий компонент
  direction: 'left' | 'right' | 'up' | 'down' // Направление свайпа
}
```

### `KeyEvent`

Объект `KeyEvent` описывает событие взаимодействия пользователя с физической кнопкой. Этот тип используется для свойств событий элементов [`keydown`](#keydown) и [`keyup`](#keyup). Прототип объекта события `KeyEvent`:
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
- Другие символьные клавиши имеют имя, состоящее из одного символа, например, буква `'A'`, дефис `'-'` и т.д.

### `WheelEvent`

Объект `WheelEvent` описывает событие взаимодействия пользователя с вращающимся колесиком. Этот тип используется для свойств событий элемента [`wheel`](#wheel). Сигнатура объекта события `WheelEvent`:
``` ts
interface WheelEvent {
  deltaY: number, // Приращение прокрутки колесика по оси Y
  stopPropagation(): void // Вызов этого метода предотвращает всплытие события
}
```

В отличие от [wheel event](https://developer.mozilla.org/en-US/docs/Web/API/Element/wheel_event) в веб-стандартах, `WheelEvent` в Glyphix в настоящее время содержит только свойство `deltaY`.

## Механизм реагирования на события

### Всплытие событий (Bubbling)

События касаний и жестов поддерживают всплытие (bubbling). Всплытие означает, что когда событие происходит на каком-либо элементе, оно сначала выполняет обработчик на этом элементе, затем на его родительском элементе и так далее поднимается вверх по цепочке предков. В следующем примере зеленый компонент `p` и серый компонент `div` оба прослушивают события касания. При клике на компонент `p` можно заметить, что событие получают и компонент `p`, и компонент `div`.

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
    // Свойство isTarget позволяет определить, является ли целью события компонент, прослушивающий это событие в данный момент
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

В Glyphix всплывают только события касаний и жестов, описанные в этом документе. В настоящее время перехват событий (capturing) в коде JavaScript недоступен.

### Предотвращение всплытия событий

Использование метода `stopPropagation()` объекта `BaseEvent` позволяет остановить всплытие события к родительским элементам.

### Принудительный ответ на событие (Strong Response)

В Glyphix события касаний и жестов имеют два приоритета реагирования: сильный (strong) и слабый (weak). Когда на одно событие претендует несколько целей, сильный ответ имеет приоритет над слабым. Предположим, в интерфейсе есть 3 уровня родительских и дочерних элементов: `A -> B -> C`, где `C` реагирует на событие слабо, а `B` — сильно. В этом случае событие будет передано в `B` и больше не дойдет до `C`. Элемент, изначально настроенный на сильный ответ, может перенаправить событие повторно, если его перевести в режим слабого ответа.

События касаний и жестов из раздела [Общие события](#通用事件) по умолчанию имеют слабый ответ. В следующем примере зеленый компонент `p` помещен внутрь серого контейнера `scroll` и прослушивает все события касания компонента `p`. Поскольку `scroll` по умолчанию имеет сильный ответ на жесты вертикальной прокрутки, слабый ответ на горизонтальную прокрутку и не реагирует на другие жесты, во время работы можно наблюдать следующее:
- При клике на компонент `p` срабатывает событие `touchstart`, а при отпускании — `touchend`;
- При перетаскивании компонента `p` по горизонтали срабатывает событие `touchmove`;
- При перетаскивании компонента `p` по вертикали, поскольку родительский компонент `scroll` имеет сильный ответ на вертикальную прокрутку, а в коде шаблона компонент `p` имеет лишь слабый ответ на `touchmove`, вертикальное перетаскивание будет перехвачено компонентом `scroll`, а компонент `p` получит событие `touchcancel`.

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

Механизм обработки жестов по умолчанию у многих нативных компонентов настроен на сильный ответ. Метод `strongResponse()` объекта `BaseEvent` позволяет указать в JavaScript-коде, что событие должно обрабатываться в режиме сильного ответа. В следующем примере внешний серый компонент `div` дает сильный ответ на жест, поэтому даже при касании внутреннего элемента `p`, после начала жеста событие будет отправляться только компоненту `div`.

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
    // Свойство isTarget позволяет отличить, является ли целью события текущий прослушивающий его компонент.
    // Для события cancel цель не записывается.
    if (event.isTarget && state != 'cancel')
      this.target = name
    if (name == 'div')
      event.strongResponse()
  }
}
```

</glyphix>

### Обработка событий страницы по умолчанию

Страница по умолчанию имеет слабый ответ на события жестов и блокирует их всплытие, поэтому события жестов не могут распределяться и передаваться сквозь страницу. Кроме того, страница закрывается при получении жеста `touchmove` вправо. Разработчики также могут перехватывать жесты, чтобы отключить эту особенность.

Для этого нужно прослушивать жест `touchmove` компонента страницы и остановить всплытие:
``` html
<!-- Этот div является корневым компонентом страницы -->
<div on:touchmove="$event.stopPropagation()">
  ...
</div>
```
Таким образом, с этой страницы нельзя будет вернуться с помощью свайпа вправо, но можно будет вернуться нажатием физической кнопки Power. Чтобы заблокировать возврат по кнопке, можно использовать следующий подход:
``` html
<!-- Этот div является корневым компонентом страницы -->
<div on:keydown="onKeyup">
  ...
</div>
```

``` js
export default {
  onKeyup(event) {
    // Если код клавиши равен 'Power', запрещаем всплытие, чтобы предотвратить выход со страницы
    if (event.key == 'Power')
      event.stopPropagation()
  }
}
```

::: warning
Действуйте осторожно, заменяя стандартную обработку событий страницы, чтобы избежать ситуаций, когда пользователь не сможет покинуть страницу.
:::

::: tip
В предыдущих версиях для предотвращения стандартного поведения возврата со страницы использовалось событие жеста `swipe`, но начиная с версии 0.6.4 этот способ устарел. Пожалуйста, используйте для этого описанную выше обработку события `touchmove`. Данное изменение связано с тем, что интерактивный анимационный возврат со страницы (выход вслед за пальцем) полностью несовместим со смыслом блокировки возврата через `swipe`.
:::

## Советы по использованию

### Операции с позиционированием компонентов

Использование свойств `top` и `left` нативных компонентов позволяет легко изменять положение компонента:
``` html
<div :top="40" :left="20"> ... </div>
```
`top` и `left` фактически являются сокращениями для одноименных CSS-свойств, поэтому они работают только в абсолютном позиционировании (absolute layout), которое можно задать с помощью следующего CSS:
``` css
div {
  position: absolute;
}
```

Затем вы можете использовать реактивные свойства для изменения положения компонента. В следующем примере показано случайное перемещение компонента с анимацией в сочетании с [модификатором `transition`](/framework/component/prop-modifier.md#transition-修饰符).

<glyphix id="generic-widget-position" height="250" title="Случайное положение компонента">

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
    // Получаем объекты компонентов, диапазон позиций не должен превышать контейнер #pane
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

В этом примере каждые две секунды случайным образом устанавливается положение компонента `#tile`, причем диапазон не выходит за границы контейнера `#pane`. Модификатор `transition` по умолчанию воспроизводит переходную анимацию длительностью в $1$ секунду.