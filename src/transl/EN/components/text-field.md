# text-field


A component used to enter a single line of text content, which defaults to an inline element. Unlike similar GUI elements on mobile phones or PCs, `text-field` currently does not respond to input devices such as keyboards, nor does it pop up the input method interface, so you must manually edit its content. `text-field` supports cursor manipulation via touch gestures (such as clicking and scrolling).


`text-field` is suitable as a low-level component for single-line text input, and you can implement your own soft keyboard (such as password grid, or even voice input) according to your needs. For details, please refer to [示例](#基本示例).


## property


### `value` <decl type="string" set get listen />


The `value` attribute is a string that is the currently edited content of `text-field`. Reading or listening to this value can obtain the input text, and you can also set this property.


It is common to bind `value` bidirectionally to a specific reactive property, such as:


```html
<text-field ::value="inputText" />
```


### `placeholder` <decl type="string" set get />


When the content of `text-field` is empty, `placeholder` can be used to provide a brief prompt to the user, such as a phrase such as "Please enter text."


`placeholder` is automatically displayed when the input text is empty, so usually only a fixed content is needed, such as:


```html
<text-field ::value="inputText" placeholder="type here" />
```


### `password` <decl type="boolean" set get />


When this attribute is set, `text-area` will use "cipher mode", that is, each character will be replaced with a "•" ( [Bullet, U+2022](http://www.fileformat.info/info/unicode/char/2022/index.htm) ). You can turn off or turn on the `password` attribute at any time to switch between showing and hiding the password state.


In the new version <version-badge since="0.9" />, the password mode will delay masking the entered characters, and the user can see the characters just entered for a short time before being replaced with "•". Older versions will immediately mask the entered characters.


### `insert` <decl type="(text: string): void" method />


Insert a piece of text with the content `text` at the cursor, and the cursor will automatically move after the inserted text. Calling this function will trigger the `value` listening event.


### `backspace` <decl type="(): void" method />


Delete the character at the cursor and the cursor will automatically move forward. Calling this function will trigger the `value` listening event.


## Instructions for use


### basic example


The following example shows basic usage of `text-field`. You can click on the keyboard buttons to enter numbers. Click the "×" button to delete the content at the cursor, and click "A/*" to switch between password mode and normal text input mode. In password mode, the entered content will be hidden with `•`.


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
  <!-- 一个简单的矩阵数字键盘 -->
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
    // Get the TextField component object to facilitate calling insert() and backspace() methods.
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



In this example, the text of `text-field` is centered, which is achieved through `text-align`:
```css
text-field {
  text-align: center;
}
```


We first obtain the `text-field` component object through the `$element` method in the component's `onReady()` life cycle function, because then we need to edit the content through the [`insert()`](#insert) and [`backspace`](#backspace) methods.


On this basis, we can directly call the `text-field` method in the `click` event listener of the `button` component, for example:
```html
<button on:click="textField.backspace()">×</button>
```


Since there is no physical keyboard, developers usually need to provide a custom keyboard implementation. For teaching purposes, this example only implements a numeric keyboard with 2 rows and 5 columns. And insert the key value into `text-field` in the `click` event listening function of each key:
```html
<div class="flex-row" for="rows in keyboard">
  <button class="flex-1" for="key in rows"
          on:click="textField.insert(key)">
    {{key}}
  </button>
</div>
```


This example also demonstrates the standard method of switching password modes.


### Content validation and formatting


You can validate and format input by bidirectionally binding the [`value`](#value) property of `text-field` to a computed property. The following example demonstrates this approach, which only allows you to enter up to 9 digits (no letters, etc.) and adds a " `,` " separator between each three digits.


<glyphix id="components-text-field-validator" title="内容验证器" width="410" height="200">


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



Content validation and formatting are implemented through two-way binding and computed properties. For the `text-field` component node
```html
<text-field id="text-field"
            ::value="inputText"
            :password="password"
            placeholder="type here" />
```
For example, the `value` property is bidirectionally bound to `inputText`, which is actually a computed property. Its `set()` method checks that the input conforms to the specification (up to 11 characters, and only numbers and commas are allowed), then filters the numbers through a regular expression and formats them with commas between every three digits:
```js
function set(text) {
  if (text.length < 12 && /^[\d,]*$/.test(text)) {
    this.rawText = text.replace(/[^\d]/g, '')
                       .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }
}
```
If the input content does not meet the requirements, the `set()` method will ignore the input value, and the two-way binding mechanism will make the content of `text-field` and the attribute value of `inputText` (obtained through the `get()` method) consistent. Therefore you will find that you cannot enter alphabetic keys.