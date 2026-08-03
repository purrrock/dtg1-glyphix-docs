# textarea

`textarea` <experimental/><version-badge since="0.9" /> 是一个多行文本输入组件，默认显示为块级元素。和手机或 PC 上的类似 GUI 元素不同，`textarea` 目前不响应键盘等输入设备，也不会弹出输入法界面，因此你必须手动编辑其内容。`textarea` 支持通过触摸手势操作光标（如点击和滚动），并提供了上下左右移动光标的方法。

`textarea` 适合作为多行文本输入的底层组件，并根据你的需求自己实现软键盘和光标控制，详情请参考[示例](#基本示例)。

::: important 兼容性
`textarea` 是一个实验性的扩展组件，目前仅在 Glyphix 0.9 及以上版本可用，并且仅部分设备支持该组件。
:::

## 属性

### `text` <decl type="string" get set listen />

`text` 属性是一个字符串，它是 `textarea` 当前编辑的文本内容。读取或者监听这个值可以获取输入的文本，也可以设置该属性。

通常会将 `text` 双向绑定到特定的响应式属性，也可以通过元素内部的内容来设置文本，如：

```html
<textarea ::text="inputText" />
```

或者

```html
<textarea @text="onTextChanged">{{ inputText }}</textarea>
```

:::tip
`textarea` 的 `text` 属性与 [`text-field`](text-field.md) 的 [`value`](text-field.md#value) 属性功能类似。
:::

### `placeholder` <decl type="string" set get />

当 `textarea` 的内容为空时，可以通过 `placeholder` 向用户提供一个简短的提示，如“请输入文本”等短语。

`placeholder` 在输入文本为空时自动显示，因此通常只需一个固定的内容，如：

```html
<textarea ::text="inputText" placeholder="type here" />
```

### `insert` <decl type="(text: string): void" method />

在光标处插入一段内容为 `text` 的文本，光标会自动移动到插入的文本之后。调用该函数会触发 `text` 监听事件。

### `backspace` <decl type="(): void" method />

删除光标处的字符，光标会自动向前移动。调用该函数会触发 `text` 监听事件。

### `moveCaret` <decl type="(direction: 'up' | 'down' | 'left' | 'right'): void" method />

将光标向指定方向移动一个位置。`direction` 参数可选值为 `'up'`、`'down'`、`'left'`、`'right'`，分别对应上下左右四个方向。

## 使用说明

### 基本示例

以下示例展示了 `textarea` 的基本用法。用户可以直接在文本框中输入多行文本，也可以使用下方的虚拟键盘来编辑内容：点击字母/符号键插入字符；"`×`" 键删除光标处的内容；"`Aa`" 键切换大小写；"`1#`" 键切换至符号键盘；"`Enter`" 键插入换行符；箭头键移动光标。

<glyphix id="components-textarea-basic" width="560" height="360" title="Textarea 基本示例">

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

我们首先在组件的 `onReady()` 生命周期函数中通过 `$element` 方法来获取 `textarea` 组件对象，因为接下来需要通过 [`insert()`](#insert)、[`backspace`](#backspace) 和 [`moveCaret`](#movecaret) 方法来编辑内容和移动光标。

在此基础上，我们就可以在 `button` 组件的触摸事件监听中调用 `textarea` 的方法，例如：

```html
<button on:touchstart="ta.insert('A')">A</button>
```

由于没有实体键盘，开发者通常需要提供自定义的键盘实现。本示例实现了完整的 QWERTY 键盘布局，支持大小写切换和符号键盘。在每一个键的触摸事件监听函数中调用相应的方法来编辑文本。箭头键通过 [`moveCaret()`](#movecaret) 方法移动光标（上下左右四个方向），换行键通过 [`insert()`](#insert) 插入换行符 `\n`。

### 和 text-field 的区别

`textarea` 和 `text-field` 都是文本输入组件，主要区别如下：

| 特性 | `textarea` | `text-field` |
|------|-----------|-------------|
| 文本行数 | 单行或多行 | 单行 |
| 换行支持 | 支持 `\n` 换行 | 不支持换行 |
| 光标移动 | 上下移动 | 左右移动 |
| 内容属性 | `text` | `value` |
| 密码模式 | 不支持 | 支持 `password` 属性 |
| 默认 display | 块级元素 | 行内元素 |
