# textarea

`textarea` <experimental/><version-badge since="0.9" /> — это компонент многострочного текстового ввода, который по умолчанию отображается как блочный элемент. В отличие от аналогичных GUI-элементов на мобильных устройствах или ПК, `textarea` в настоящее время не реагирует на устройства ввода, такие как клавиатура, и не вызывает интерфейс метода ввода (клавиатуру), поэтому редактировать его содержимое необходимо вручную. `textarea` поддерживает управление курсором с помощью сенсорных жестов (например, нажатие и прокрутка) и предоставляет методы для перемещения курсора вверх, вниз, влево и вправо.

`textarea` подходит в качестве базового компонента для ввода многострочного текста, позволяя самостоятельно реализовать программную клавиатуру и управление курсором в соответствии с вашими требованиями. Подробности см. в [примере](#基本示例).

::: important Совместимость
`textarea` — это экспериментальный расширенный компонент, который в настоящее время доступен только в Glyphix версии 0.9 и выше, причем поддерживается только на некоторых устройствах.
:::

## Свойства

### `text` <decl type="string" get set listen />

Свойство `text` представляет собой строку, содержащую текущий редактируемый текст в `textarea`. Чтение или прослушивание этого значения позволяет получить введенный текст, также это свойство можно устанавливать.

Обычно `text` двунаправленно связывается с определенным реактивным свойством, но текст также можно задать через внутреннее содержимое элемента, например:

```html
<textarea ::text="inputText" />
```

или

```html
<textarea @text="onTextChanged">{{ inputText }}</textarea>
```

:::tip
Свойство `text` компонента `textarea` аналогично по функционалу свойству [`value`](text-field.md#value) компонента [`text-field`](text-field.md).
:::

### `placeholder` <decl type="string" set get />

Когда содержимое `textarea` пусто, с помощью свойства `placeholder` можно показать пользователю короткую подсказку, например «Введите текст» и т. п.

`placeholder` отображается автоматически, когда вводимый текст пуст, поэтому обычно требуется лишь фиксированное содержимое, например:

```html
<textarea ::text="inputText" placeholder="type here" />
```

### `insert` <decl type="(text: string): void" method />

Вставляет текст с содержимым `text` в позицию курсора, при этом курсор автоматически перемещается сразу за вставленным текстом. Вызов этой функции вызывает событие прослушивания `text`.

### `backspace` <decl type="(): void" method />

Удаляет символ в позиции курсора, при этом курсор автоматически смещается назад. Вызов этой функции вызывает событие прослушивания `text`.

### `moveCaret` <decl type="(direction: 'up' | 'down' | 'left' | 'right'): void" method />

Перемещает курсор на одну позицию в указанном направлении. Параметр `direction` может принимать значения `'up'`, `'down'`, `'left'`, `'right'`, которые соответствуют направлениям вверх, вниз, влево и вправо.

## Инструкции по использованию

### Базовый пример

В следующем примере продемонстрировано базовое использование `textarea`. Пользователь может вводить многострочный текст непосредственно в текстовое поле или использовать виртуальную клавиатуру ниже для редактирования содержимого: нажатие клавиш с буквами/символами вставляет символы; клавиша «`×`» удаляет содержимое в позиции курсора; клавиша «`Aa`» переключает регистр; клавиша «`1#`» переключает на клавиатуру символов; клавиша «`Enter`» вставляет символ перевода строки; клавиши со стрелками перемещают курсор.

<glyphix id="components-textarea-basic" width="560" height="360" title="Базовый пример Textarea">

```html
  <div class="window">
    <textarea
      id="textarea"
      :placeholder="placeholder"
      @text="onTextChanged"
    >
      {{ text }}
    </textarea>
    <div class="keyboard">
      <div class="kb-row" for="row in keyboard" :style="keyboardRowStyle(row)">
        <button
          class="kb-key"
          for="key in row.keys"
          :width="key.width ? key.width : null"
          on:touchstart="onKeyEvent(key, 'down')"
          on:touchend="onKeyEvent(key, 'up')"
          on:touchcancel="onKeyEvent(key, 'up')"
        >
          {{ key.code ? key.code : key }}
        </button>
      </div>
    </div>
  </div>
```

```js
const keyboardQwert = [
  { keys: ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", {code: "×", width: "13%"}] },
  { keys: ["Aa", "a", "s", "d", "f", "g", "h", "j", "k", "l", "Enter"] },
  {
    keys: ["z", "x", "c", "v", "b", "n", "m", ".", "↑"],
    margin: ["14%", "52px"],
  },
  { keys: [{code: "1#", width: "14%"}, {code: "Space", width: "55%"}, "←", "↓", "→"] },
];

const keyboardQwertUpper = [
  { keys: ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", {code: "×", width: "13%"}] },
  { keys: ["Aa", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"] },
  {
    keys: ["Z", "X", "C", "V", "B", "N", "M", ".", "↑"],
    margin: ["14%", "52px"],
  },
  { keys: [{code: "1#", width: "14%"}, {code: "Space", width: "55%"}, "←", "↓", "→"] },
];

const keyboard123 = [
  { keys: ["~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", {code: "×", width: "13%"}] },
  { keys: ["Aa", "@", "#", "$", "%", "&", "*", "-", "+", "=", "Enter"] },
  {
    keys: ["!", '"', "'", ";", ":", ",", ".", "/", "↑"],
    margin: ["14%", "52px"],
  },
  { keys: [{code: "abc", width: "14%"}, {code: "Space", width: "55%"}, "←", "↓", "→"] },
];

export default {
  data: {
    placeholder: "Enter your text here...",
    text: "Glyphix is a declarative GUI framework built for MCU devices.\n\nIt is lightweight, fast, and easy to use, offering rich UI components and development tools that help teams create modern, responsive graphical interfaces for embedded applications.",
    keyboard: keyboardQwert,
  },
  keyboardType: "qwerty",

  ta: null,
  onReady() {
    this.ta = this.$element("textarea");
  },

  onTextChanged() {
    console.log("You have edited the text");
  },
  toggleCase() {
    if (this.keyboardType == "qwerty") {
      this.keyboard = keyboardQwertUpper;
      this.keyboardType = "qwertyUpper";
    } else if (this.keyboardType == "qwertyUpper") {
      this.keyboard = keyboardQwert;
      this.keyboardType = "qwerty";
    }
  },
  keyboardRowStyle(row) {
    if (row.margin)
      return `margin-left: ${row.margin[0]}; margin-right: ${row.margin[1]};`;
    return "";
  },
  backspaceTimer: null,
  onKeyEvent(key, event) {
    if (event !== "down") {
      clearInterval(this.backspaceTimer);
      this.backspaceTimer = null;
      return; // skip if the key is released
    }

    if (key.code) key = key.code;
    switch (key) {
      case "Aa": this.toggleCase(); break;
      case "1#":
        this.keyboard = keyboard123;
        this.keyboardType = "123";
        break;
      case "abc":
        this.keyboard = keyboardQwert;
        this.keyboardType = "qwerty";
        break;
      case "×":
        this.ta.backspace();
        if (event == "down") {
          this.backspaceTimer = setTimeout(() => {
            this.backspaceTimer = setInterval(() => this.ta.backspace(), 50);
            this.ta.backspace();
          }, 500);
        }
        break;
      case "Enter": this.ta.insert("\n"); break;
      case "Space": this.ta.insert(" "); break;
      case "↑": this.ta.moveCaret("up"); break;
      case "↓": this.ta.moveCaret("down"); break;
      case "←": this.ta.moveCaret("left"); break; 
      case "→": this.ta.moveCaret("right"); break;
      default: this.ta.insert(key); break;
    }
  },
};
```

```css
.window {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 8px;
}

textarea {
  flex-grow: 1;
  padding: 6px;
  border: 2px solid #aaa6;
  border-radius: 12px;
  max-height: 160px;
}

.keyboard {
  display: flex;
  flex-direction: column;
}

.kb-row {
  display: flex;
  flex-direction: row;
}

.kb-key {
  flex-grow: 1;
  background-color: #f0f0f080;
  border: 2px solid #999;
  border-radius: 16px;
  text-align: center;
  padding: 6px auto;
  margin: 2px;
  font-size: 0.85rem;
  min-width: 40px;
}

.kb-key:active {
  background-color: #0003;
  border-color: #6663;
}
```

</glyphix>

Сначала мы получаем объект компонента `textarea` с помощью метода `$element` в функции жизненного цикла `onReady()`, так как в дальнейшем потребуется редактировать содержимое и перемещать курсор с помощью методов [`insert()`](#insert), [`backspace`](#backspace) и [`moveCaret`](#movecaret).

Основываясь на этом, мы можем вызывать методы `textarea` в прослушивателях событий касания компонента `button`, например:

```html
<button on:touchstart="ta.insert('A')">A</button>
```

В связи с отсутствием физической клавиатуры разработчикам обычно требуется предоставлять собственную реализацию клавиатуры. В данном примере реализована полноценная раскладка QWERTY-клавиатуры с поддержкой переключения регистра и символьной клавиатуры. В функции-прослушивателе событий касания для каждой клавиши вызывается соответствующий метод для редактирования текста. Клавиши со стрелками перемещают курсор с помощью метода [`moveCaret()`](#movecaret) (в четырех направлениях: вверх, вниз, влево и вправо), а клавиша ввода новой строки вставляет символ перевода строки `\n` с помощью [`insert()`](#insert).

### Отличия от text-field

`textarea` и `text-field` являются компонентами текстового ввода, основные различия между ними приведены ниже:

| Характеристика | `textarea` | `text-field` |
|----------------|------------|--------------|
| Количество строк текста | Однострочный или многострочный | Однострочный |
| Поддержка переноса строк | Поддерживает перенос `\n` | Не поддерживает перенос |
| Перемещение курсора | Вверх и вниз | Влево и вправо |
| Свойство содержимого | `text` | `value` |
| Режим пароля | Не поддерживается | Поддерживает свойство `password` |
| Отображение по умолчанию (`display`) | Блочный элемент | Строчный элемент |