# text-field

Компонент для ввода однострочного текста, по умолчанию является строчным элементом (inline). В отличие от аналогичных GUI-элементов на телефонах или ПК, `text-field` в настоящее время не реагирует на устройства ввода, такие как клавиатура, и не вызывает интерфейс метода ввода (клавиатуру), поэтому вы должны редактировать его содержимое вручную. `text-field` поддерживает управление курсором с помощью сенсорных жестов (например, нажатие и прокрутка).

`text-field` подходит в качестве базового компонента для ввода однострочного текста, позволяя реализовать собственную программную клавиатуру в соответствии с вашими требованиями (например, цифровую клавиатуру для ввода пароля или даже голосовой ввод). Подробности см. в [примере](#基本示例).

## Свойства (Attributes)

### `value` <decl type="string" set get listen />

Свойство `value` представляет собой строку, которая является текущим редактируемым содержимым `text-field`. Чтение или прослушивание этого значения позволяет получить введенный текст, а также установить это свойство.

Обычно `value` двунаправленно связывается с определенным реактивным свойством, например:

```html
<text-field ::value="inputText" />
```

### `placeholder` <decl type="string" set get />

Когда содержимое `text-field` пусто, с помощью `placeholder` можно предоставить пользователю краткую подсказку, например «Введите текст» и т. д.

`placeholder` отображается автоматически, когда вводимый текст пуст, поэтому обычно требуется лишь фиксированное содержимое, например:

```html
<text-field ::value="inputText" placeholder="type here" />
```

### `password` <decl type="boolean" set get />

Когда это свойство установлено, `text-area` переходит в «режим пароля», то есть каждый символ заменяется на «•» ([Bullet, U+2022](http://www.fileformat.info/info/unicode/char/2022/index.htm)). Вы можете в любой момент включить или выключить свойство `password`, чтобы переключать состояние отображения/скрытия пароля.

В новых версиях <version-badge since="0.9" /> в режиме пароля вводится задержка перед скрытием символов: пользователь может увидеть только что введенный символ в течение короткого времени, после чего он заменяется на «•». В старых версиях введенные символы скрывались немедленно.

### `insert` <decl type="(text: string): void" method />

Вставляет текст с содержимым `text` в позицию курсора, при этом курсор автоматически перемещается после вставленного текста. Вызов этой функции инициирует событие прослушивания `value`.

### `backspace` <decl type="(): void" method />

Удаляет символ в позиции курсора, при этом курсор автоматически смещается вперед. Вызов этой функции инициирует событие прослушивания `value`.

## Инструкция по использованию

### Базовый пример

В следующем примере показано базовое использование `text-field`. Вы можете нажимать кнопки клавиатуры для ввода цифр. Нажмите кнопку «×» для удаления содержимого в позиции курсора, а нажатие «A/*» переключает между режимом пароля и обычным режимом ввода текста. В режиме пароля введенное содержимое скрывается с помощью `•`.

<glyphix id="components-text-field-1" width="410" height="160">

```html
<div class="flex-column">
  <div class="flex-row align-baseline">
    <text-field id="text-field"
                ::value="inputText"
                :password="password"
                placeholder="type here" />
    <button checkable ::press="password">A/*</button>
    <button on:click="textField.backspace()">×</button>
  </div>
  <!-- Простая цифровая матричная клавиатура -->
  <div class="flex-row" for="rows in keyboard">
    <button class="flex-1" for="key in rows"
            on:click="textField.insert(key)">
      {{key}}
    </button>
  </div>
</div>
```

```js
export default {
  data: {
    inputText: "",
    password: false,
  },
  keyboard: [
    ['1', '2', '3', '4', '5'],
    ['6', '7', '8', '9', '0'],
  ],
  textField: null,
  onReady() {
    // Получаем объект компонента TextField для удобного вызова методов insert() и backspace().
    this.textField = this.$element("text-field")
  },
}
```

```css
.flex-column {
  display: flex;
  flex-direction: column;
}

.flex-row {
  display: flex;
}

.align-baseline {
  align-items: baseline;
}

text-field {
  flex: 1;
  text-align: center;
  border-bottom: 2px solid #666;
}

button {
  border-radius: 8px;
  background-color: #dee2e6;
  margin: 8px;
  padding: auto 12px;
}

button:active {
  opacity: 0.5;
}

.flex-1 {
  flex: 1;
}
```
</glyphix>

В этом примере текст в `text-field` выравнивается по центру, что достигается с помощью свойства `text-align`:
```css
text-field {
  text-align: center;
}
```

Сначала мы получаем объект компонента `text-field` с помощью метода `$element` в функции жизненного цикла `onReady()`, так как в дальнейшем нам потребуется использовать методы [`insert()`](#insert) и [`backspace`](#backspace) для редактирования содержимого.

На этой основе мы можем напрямую вызывать методы `text-field` в прослушивателе событий `click` компонента `button`, например:
```html
<button on:click="textField.backspace()">×</button>
```

Поскольку аппаратной клавиатуры нет, разработчикам обычно требуется предоставлять собственную реализацию клавиатуры. В учебных целях в этом примере реализована только цифровая клавиатура из 2 строк и 5 столбцов. Значение каждой клавиши вставляется в `text-field` внутри функции прослушивания события `click` каждой клавиши:
```html
<div class="flex-row" for="rows in keyboard">
  <button class="flex-1" for="key in rows"
          on:click="textField.insert(key)">
    {{key}}
  </button>
</div>
```

В этом примере также продемонстрирован стандартный способ переключения режима пароля.

### Валидация и форматирование содержимого

Вы можете реализовать валидацию и форматирование вводимого содержимого, связав свойство [`value`](#value) компонента `text-field` двунаправленной связью с вычисляемым свойством (computed property). В следующем примере показан этот подход: он позволяет вводить не более 9 цифр (ввод букв и т. д. запрещен) и добавляет разделитель «`,`» каждые три цифры.

<glyphix id="components-text-field-validator" title="Валидатор содержимого" width="410" height="200">

```html
<div class="flex-column">
  <div class="flex-row align-baseline">
    <text-field id="text-field"
                ::value="inputText"
                :password="password"
                placeholder="type here" />
    <button checkable ::press="password">A/*</button>
    <button on:click="textField.backspace()">×</button>
  </div>
  <div class="flex-row" for="rows in keyboard">
    <button class="flex-1" for="key in rows"
            on:click="textField.insert(key)">
      {{key}}
    </button>
  </div>
</div>
```

```js
export default {
  data: {
    password: false,
    rawText: "",
  },
  computed: {
    inputText: {
      get() { return this.rawText },
      set(text) {
        if (text.length < 12 && /^[\d,]*$/.test(text)) {
          this.rawText = text.replace(/[^\d]/g, '')
                             .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
        }
      },
    },
  },
  keyboard: [
    ["1", "2", "3", "4", "5"],
    ["6", "7", "8", "9", "0"],
    ["A", "B", "C", "D", "E"],
  ],
  textField: null,
  onReady() {
    this.textField = this.$element("text-field")
  },
}
```

```css
.flex-column {
  display: flex;
  flex-direction: column;
}

.flex-row {
  display: flex;
}

.align-baseline {
  align-items: baseline;
}

text-field {
  flex: 1;
  border-bottom: 2px solid #666;
}

button {
  border-radius: 8px;
  background-color: #dee2e6;
  margin: 8px;
  padding: auto 12px;
}

button:active {
  opacity: 0.5;
}

.flex-1 {
  flex: 1;
}
```
</glyphix>

Валидация и форматирование содержимого реализуются с помощью двунаправленного связывания и вычисляемых свойств. Для узла компонента `text-field`:
```html
<text-field id="text-field"
            ::value="inputText"
            :password="password"
            placeholder="type here" />
```
свойство `value` двунаправленно связано с `inputText`, который на самом деле является вычисляемым свойством. Его метод `set()` проверяет, соответствует ли вводимое содержимое стандарту (не более 11 символов, разрешены только цифры и запятые), затем с помощью регулярного выражения фильтрует цифры и форматирует их, добавляя запятую каждые три цифры:
```js
function set(text) {
  if (text.length < 12 && /^[\d,]*$/.test(text)) {
    this.rawText = text.replace(/[^\d]/g, '')
                       .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }
}
```
Если вводимое содержимое не соответствует требованиям, метод `set()` игнорирует введенное значение, а механизм двунаправленного связывания гарантирует, что содержимое `text-field` останется согласованным со значением свойства `inputText` (получаемым через метод `get()`). Поэтому вы заметите, что ввод буквенных клавиш невозможен.