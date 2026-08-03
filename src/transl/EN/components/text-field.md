# text-field

A component used for entering single-line text content, which defaults to an inline element. Unlike GUI elements on mobile phones or PCs, `text-field` currently does not respond to input devices such as keyboards, nor does it pop up an input method interface, so you must edit its content manually. `text-field` supports operating the cursor via touch gestures (such as tapping and scrolling).

`text-field` is suitable as a low-level component for single-line text input, allowing you to implement a soft keyboard according to your needs (such as a password numeric keypad or even voice input). For details, please refer to the [Example](#基本示例).

## Attributes

### `value` <decl type="string" set get listen />

The `value` property is a string representing the content currently being edited in `text-field`. Reading or listening to this value allows you to retrieve the input text, and this property can also be set.

Typically, `value` is two-way bound to a specific reactive property, such as:

```html
<text-field ::value="inputText" />
```

### `placeholder` <decl type="string" set get />

When the content of `text-field` is empty, `placeholder` can be used to provide a brief prompt to the user, such as phrases like "Please enter text".

`placeholder` automatically displays when the input text is empty, so it usually only requires a fixed content, such as:

```html
<text-field ::value="inputText" placeholder="type here" />
```

### `password` <decl type="boolean" set get />

When this property is set, `text-area` will use "password mode", meaning each character is replaced with "•" ([Bullet, U+2022](http://www.fileformat.info/info/unicode/char/2022/index.htm)). You can turn the `password` property off or on at any time to switch between showing and hiding the password status.

In newer versions <version-badge since="0.9" />, password mode delays masking the input characters, allowing users to see the just-entered characters for a short time before they are replaced with "•". Older versions mask input characters immediately.

### `insert` <decl type="(text: string): void" method />

Inserts a piece of text with the content `text` at the cursor position, and the cursor automatically moves past the inserted text. Calling this function triggers a `value` listening event.

### `backspace` <decl type="(): void" method />

Deletes the character at the cursor position, and the cursor automatically moves forward. Calling this function triggers a `value` listening event.

## Usage Instructions

### Basic Example

The following example demonstrates the basic usage of `text-field`. You can click the keyboard buttons to input numbers. Click the "×" button to delete the content at the cursor position, and click "A/*" to toggle between password mode and regular text input mode. In password mode, the input content is hidden with `•`.

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
  <!-- A simple matrix numeric keypad -->
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
    // Get the TextField component object for easy invocation of insert() and backspace() methods.
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

In this example, the text in `text-field` is centered, which is achieved via `text-align`:
```css
text-field {
  text-align: center;
}
```

We first obtain the `text-field` component object using the `$element` method within the component's `onReady()` lifecycle function, because we need to use the [`insert()`](#insert) and [`backspace`](#backspace) methods to edit the content subsequently.

With this in place, we can directly call the methods of `text-field` within the `click` event listener of the `button` component, for example:
```html
<button on:click="textField.backspace()">×</button>
```

Since there is no physical keyboard, developers usually need to provide a custom keyboard implementation. For educational purposes, this example only implements a 2-row by 5-column numeric keypad, and inserts the key value into `text-field` within the `click` event listener function of each key:
```html
<div class="flex-row" for="rows in keyboard">
  <button class="flex-1" for="key in rows"
          on:click="textField.insert(key)">
    {{key}}
  </button>
</div>
```

This example also demonstrates the standard method for toggling password mode.

### Content Validation and Formatting

You can achieve validation and formatting of input content by two-way binding the [`value`](#value) property of `text-field` to a computed property. The following example demonstrates this approach, which allows you to input a maximum of 9 digits (no letters, etc.) and adds a "," separator every three digits.

<glyphix id="components-text-field-validator" title="Content Validator" width="410" height="200">

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

Content validation and formatting are implemented via two-way binding and computed properties. For the `text-field` component node:
```html
<text-field id="text-field"
            ::value="inputText"
            :password="password"
            placeholder="type here" />
```
The `value` property is two-way bound to `inputText`, which is actually a computed property. Its `set()` method checks whether the input content complies with the rules (maximum 11 characters, allowing only numbers and commas), then filters the numbers using regular expressions and formats them by adding commas every three digits:
```js
function set(text) {
  if (text.length < 12 && /^[\d,]*$/.test(text)) {
    this.rawText = text.replace(/[^\d]/g, '')
                       .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }
}
```
If the input content does not meet the requirements, the `set()` method ignores the input value, and the two-way binding mechanism keeps the content of `text-field` consistent with the property value of `inputText` (obtained via the `get()` method). Therefore, you will find that letter keys cannot be entered.