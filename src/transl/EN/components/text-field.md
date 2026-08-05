# text-field

A component used for entering single-line text content, which is an inline element by default. Unlike GUI elements on mobile phones or PCs, `text-field` currently does not respond to input devices such as keyboards, nor does it pop up an IME (Input Method Editor) interface, so you must manually edit its content. `text-field` supports operating the cursor through touch gestures (such as tapping and scrolling).

`text-field` is suitable as the underlying component for single-line text input, allowing you to implement a soft keyboard according to your needs (such as a password keypad or even voice input). For details, please refer to the [Example](#basic-example).

## Attributes

### `value` <decl type="string" set get listen />

The `value` property is a string, which is the currently edited content of the `text-field`. Reading or listening to this value can retrieve the entered text, and this property can also be set.

Typically, `value` is two-way bound to a specific reactive property, such as:

```html
<text-field ::value="inputText" />
```

### `placeholder` <decl type="string" set get />

When the content of the `text-field` is empty, `placeholder` can be used to provide the user with a short prompt, such as phrases like "Please enter text".

`placeholder` is automatically displayed when the input text is empty, so it usually only requires a fixed content, such as:

```html
<text-field ::value="inputText" placeholder="type here" />
```

### `password` <decl type="boolean" set get />

When this property is set, `text-field` will use "password mode", meaning each character is replaced with a "•" ([Bullet, U+2022](http://www.fileformat.info/info/unicode/char/2022/index.htm)). You can turn the `password` property off or on at any time to switch between showing and hiding the password status.

In newer versions <version-badge since="0.9" />, password mode delays the masking of entered characters. Users can see the newly entered characters for a short time before they are replaced with "•". Older versions mask input characters immediately.

### `insert` <decl type="(text: string): void" method />

Inserts a piece of text with the content `text` at the cursor position, and the cursor will automatically move after the inserted text. Calling this function will trigger the `value` listening event.

### `backspace` <decl type="(): void" method />

Deletes the character at the cursor position, and the cursor will automatically move forward. Calling this function will trigger the `value` listening event.

## Usage Instructions

### Basic Example

The following example demonstrates the basic usage of `text-field`. You can click the keyboard buttons to enter numbers. Click the "×" button to delete the content at the cursor position, and click "A/*" to toggle between password mode and regular text input mode. In password mode, the entered content is hidden with `•`.

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
  <!-- A simple matrix numeric keyboard -->
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
    // Get the TextField component object to easily call the insert() and backspace() methods.
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

In this example, the text of the `text-field` is centered, which is achieved through `text-align`:
```css
text-field {
  text-align: center;
}
```

We first obtain the `text-field` component object using the `$element` method within the component's `onReady()` lifecycle function, because we will need to use the [`insert()`](#insert) and [`backspace`](#backspace) methods to edit the content.

Building on this, we can directly call the methods of `text-field` within the `click` event listener of the `button` component, for example:
```html
<button on:click="textField.backspace()">×</button>
```

Since there is no physical keyboard, developers usually need to provide a custom keyboard implementation. For educational purposes, this example only implements a 2-row by 5-column numeric keyboard. You need to insert the key value into the `text-field` in the `click` event listener function of each key:
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

You can achieve content validation and formatting by two-way binding the [`value`](#value) property of the `text-field` to a computed property. The following example demonstrates this approach, which allows you to enter a maximum of 9 digits (letters and other characters are not allowed) and adds a "," separator every three digits.

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

Content validation and formatting are implemented through two-way binding and computed properties. For the `text-field` component node:
```html
<text-field id="text-field"
            ::value="inputText"
            :password="password"
            placeholder="type here" />
```
The `value` property is two-way bound to `inputText`, which is actually a computed property. Its `set()` method checks whether the input content complies with the rules (at most 11 characters, allowing only digits and commas), then filters the digits using regular expressions and formats them by adding commas every three digits:
```js
function set(text) {
  if (text.length < 12 && /^[\d,]*$/.test(text)) {
    this.rawText = text.replace(/[^\d]/g, '')
                       .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }
}
```
If the entered content does not meet the requirements, the `set()` method will ignore the input value, and the two-way binding mechanism will keep the content of the `text-field` consistent with the property value of `inputText` (obtained via the `get()` method). Therefore, you will find that letter keys cannot be entered.