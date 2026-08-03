# text-field

用于输入单行文本内容的组件，默认为行内元素。和手机或 PC 上的类似 GUI 元素不同，`text-field` 目前不响应键盘等输入设备，也不会弹出输入法界面，因此你必须手动编辑其内容。`text-field` 支持通过触摸手势操作光标（如点击和滚动）。

`text-field` 适合作为单行文本输入的底层组件，并根据你的需求自己实现软键盘（如密码九宫格，甚至是语音输入），详情请参考[示例](#基本示例)。

## 属性

### `value` <decl type="string" set get listen />

`value` 属性是一个字符串，它是 `text-field` 当前编辑的内容。读取或者监听这个值可以获取输入的文本，也可以设置该属性。

通常会将 `value` 双向绑定到特定的响应式属性，如：

```html
<text-field ::value="inputText" />
```

### `placeholder` <decl type="string" set get />

当 `text-field` 的内容为空时，可以通过 `placeholder` 向用户提供一个简短的提示，如“请输入文本”等短语。

`placeholder` 在输入文本为空时自动显示，因此通常只需一个固定的内容，如：

```html
<text-field ::value="inputText" placeholder="type here" />
```

### `password` <decl type="boolean" set get />

当该属性被设置时，`text-area` 将使用“密码模式”，即每个字符会被替换为“•”（[Bullet, U+2022](http://www.fileformat.info/info/unicode/char/2022/index.htm)）。你可以随时关闭或者打开 `password` 属性，以实现显示、隐藏密码状态的切换。

在新版本中 <version-badge since="0.9" />，密码模式会延时遮盖输入的字符，用户可以在短时间内看到刚输入的字符，之后才会被替换为“•”。旧版本则会立即遮盖输入字符。

### `insert` <decl type="(text: string): void" method />

在光标处插入一段内容为 `text` 的文本，光标会自动移动到插入的文本之后。调用该函数会触发 `value` 监听事件。

### `backspace` <decl type="(): void" method />

删除光标处的字符，光标会自动向前移动。调用该函数会触发 `value` 监听事件。

## 使用说明

### 基本示例

以下示例展示了 `text-field` 的基本用法。你可以点击键盘按钮来输入数字。点击“×”按钮来删除光标处的内容，点击“A/*”则会在密码模式和普通文本输入模式之间切换。密码模式下，输入的内容会以 `•` 隐藏。

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
    // 获取 TextField 组件对象，方便调用 insert() 和 backspace() 方法。
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

本示例中 `text-field` 的文本是居中显示的，这是通过 `text-align` 实现的：
```css
text-field {
  text-align: center;
}
```

我们首先在组件的 `onReady()` 生命周期函数中通过 `$element` 方法来获取 `text-field` 组件对象，因为接下来需要通过 [`insert()`](#insert) 和 [`backspace`](#backspace) 方法来编辑内容。

在此基础上，我们就可以直接在 `button` 组件的 `click` 事件监听中调用 `text-field` 的方法，例如：
```html
<button on:click="textField.backspace()">×</button>
```

由于没有实体键盘，开发者通常需要提供自定义的键盘实现。处于教学的目的，本示例仅实现了 2 行 5 列的数字键盘。并要在每一个键的 `click` 事件监听函数中将键值插入到 `text-field` 中：
```html
<div class="flex-row" for="rows in keyboard">
  <button class="flex-1" for="key in rows"
          on:click="textField.insert(key)">
    {{key}}
  </button>
</div>
```

本示例还演示了切换密码模式的标准方法。

### 内容验证和格式化

你可以通过将 `text-field` 的 [`value`](#value) 属性双向绑定到一个计算属性上来实现对输入内容的验证和格式化。下面的示例展示了这种方法，该示例最多只允许你输入 9 位数字（不能输入字母等），并会在每三位数之间添加“`,`” 分隔。

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

内容验证和格式化是通过双向绑定和计算属性来实现的。对于 `text-field` 组件节点
```html
<text-field id="text-field"
            ::value="inputText"
            :password="password"
            placeholder="type here" />
```
来说，`value` 属性被双向绑定到了 `inputText`，后者其实是一个计算属性。它的 `set()` 方法会检查输入内容是否符合规范（最多 11 个字符，且只允许数字和逗号），然后通过正则表达式来过滤数字，并按照每三位数字之间加逗号进行格式化：
```js
function set(text) {
  if (text.length < 12 && /^[\d,]*$/.test(text)) {
    this.rawText = text.replace(/[^\d]/g, '')
                       .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }
}
```
如果输入的内容不符合要求，那么 `set()` 方法会忽略输入值，双向绑定机制会使得 `text-field` 的内容和 `inputText` 的属性值（通过 `get()` 方法获取）保持一致。因此你会发现无法输入字母按键。
