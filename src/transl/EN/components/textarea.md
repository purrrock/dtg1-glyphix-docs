# textarea

`textarea` <experimental/><version-badge since="0.9" /> is a multi-line text input component, which defaults to displaying as a block-level element. Unlike similar GUI elements on mobile phones or PCs, `textarea` currently does not respond to input devices such as keyboards, nor does it pop up an input method editor (IME) interface; therefore, you must manually edit its content. `textarea` supports operating the cursor via touch gestures (such as tapping and scrolling) and provides methods to move the cursor up, down, left, and right.

`textarea` is suitable as a low-level component for multi-line text input, allowing you to implement your own soft keyboard and cursor control according to your needs. For details, please refer to the [Example](#basic-example).

::: important Compatibility
`textarea` is an experimental extended component currently available only in Glyphix version 0.9 and above, and is supported on only some devices.
:::

## Attributes

### `text` <decl type="string" get set listen />

The `text` attribute is a string representing the currently edited text content of the `textarea`. Reading or listening to this value retrieves the input text, and this attribute can also be set.

Typically, `text` is two-way bound to a specific reactive property, or text can be set using the content inside the element, such as:

```html
<textarea ::text="inputText" />
```

Or

```html
<textarea @text="onTextChanged">{{ inputText }}</textarea>
```

:::tip
The `text` attribute of `textarea` functions similarly to the [`value`](text-field.md#value) attribute of [`text-field`](text-field.md).
:::

### `placeholder` <decl type="string" set get />

When the content of the `textarea` is empty, `placeholder` can be used to provide a brief prompt to the user, such as phrases like "Please enter text".

`placeholder` automatically appears when the input text is empty, so it usually only requires fixed content, such as:

```html
<textarea ::text="inputText" placeholder="type here" />
```

### `insert` <decl type="(text: string): void" method />

Inserts a piece of text with the content `text` at the cursor position, and the cursor automatically moves after the inserted text. Calling this function triggers a `text` listening event.

### `backspace` <decl type="(): void" method />

Deletes the character at the cursor position, and the cursor automatically moves forward. Calling this function triggers a `text` listening event.

### `moveCaret` <decl type="(direction: 'up' | 'down' | 'left' | 'right'): void" method />

Moves the cursor one position in the specified direction. Valid values for the `direction` parameter are `'up'`, `'down'`, `'left'`, and `'right'`, corresponding to the four directions: up, down, left, and right.

## Usage Instructions

### Basic Example

The following example demonstrates the basic usage of `textarea`. Users can input multi-line text directly in the text box, or use the virtual keyboard below to edit the content: tap letter/symbol keys to insert characters; the "`×`" key deletes content at the cursor position; the "`Aa`" key toggles letter case; the "`1#`" key switches to the symbol keyboard; the "`Enter`" key inserts a newline character; and arrow keys move the cursor.

<glyphix id="components-textarea-basic" width="560" height="360" title="Textarea Basic Example">

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

We first obtain the `textarea` component object via the `$element` method in the component's `onReady()` lifecycle function, because we subsequently need to edit content and move the cursor using the [`insert()`](#insert), [`backspace`](#backspace), and [`moveCaret`](#movecaret) methods.

Building on this, we can call the methods of `textarea` within the touch event listeners of the `button` component, for example:

```html
<button on:touchstart="ta.insert('A')">A</button>
```

Since there is no physical keyboard, developers typically need to provide a custom keyboard implementation. This example implements a complete QWERTY keyboard layout supporting case switching and a symbol keyboard. The corresponding methods are called in the touch event listener function of each key to edit the text. The arrow keys move the cursor using the [`moveCaret()`](#movecaret) method (in the four directions: up, down, left, and right), and the newline key inserts a newline character `\n` via [`insert()`](#insert).

### Differences from text-field

Both `textarea` and `text-field` are text input components. The main differences are as follows:

| Feature | `textarea` | `text-field` |
|------|-----------|-------------|
| Text lines | Single or multi-line | Single line |
| Newline support | Supports `\n` newlines | Does not support newlines |
| Cursor movement | Up and down | Left and right |
| Content property | `text` | `value` |
| Password mode | Not supported | Supports `password` attribute |
| Default display | Block-level element | Inline element |