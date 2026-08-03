# button

按钮组件，默认为行内元素，当该组件被触碰到时，能够触发相应的事件。

## 属性

### `checkable`  <decl type="boolean" set />

设置为 `true` 时，表示一次触摸只响应一次状态改变，即：由按下转为抬起状态或由抬起转换为按下状态。并且按下状态 `press` 的监听值为 `true`、抬起为 `false`。

### `toggleable` <decl type="boolean" set />

设置为 `true` 时，表示 `press` 监听值是可以改变的，按下为 `true`，抬起为 `false`。

### `press` <decl type="boolean" get set listen />

设置 `press` 属性时，可改变组件的状态。也可以通过 `on` 指令监听组件的状态，默认情况下一次触摸完成，回调参数为 `ture`，可以配合 `checkable` `toggleable` 属性获取不同的监听值和状态。

## 功能限制

### `click` 事件失效

在不使用 `button` 组件时，通常通过 [`click`](/framework/generic/properties.md#click) 属性来监听任意原生组件的点击事件。但是这种方法通常不适用于 `button`。例如这样的代码：
```html
<button on:click="onOuterClick">
  <p on:click="onInnerClick">inner</p>
  outer button
</button>
```

```js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    // 阻止事件冒泡，以免外层按钮响应点击事件
    event.stopPropagation();
    console.log('inner click');
  }
}
```

<glyphix id="components-button-click-1" height="48" width="360" inline>

``` html
<button on:click="onOuterClick">
  <p on:click="onInnerClick">inner</p>
  outer button
</button>
```

``` css
button {
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}

button:active {
  opacity: 0.5;
}

p {
  border: 2px solid #444;
  padding: 0 10px;
}
```

``` js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    event.stopPropagation();
    console.log('inner click');
  }
}
```

</glyphix>

你可能期望点击 `"inner"` 文本时，能够触发 `onInnerClick` 方法，并阻止 `onOuterClick`。但你会发现并不是这样（最好打开浏览器的控制台查看日志）：`onInnerClick` 方法根本不会触发，只有外层 `button` 组件会响应点击，即：
- 点击`inner` 文本时，`inner click` 日志不会出现，只有 `outer click` 日志；
- `button` 按下时的交互被触发了（透明度降低）。

这就像点击外面的 `outer text` 一样。出现这种情况的原因是 `button` 组件会优先响应按下手势的整个生命周期（从按下到松手），而 `click` 事件在松手时触发。这意味着无论内层元素的 `click` 事件处理函数是否阻止冒泡都不能改变这种行为。

#### 解决方法

要解决这一问题，应该监听外层 `button` 的 `press` 事件，并监听内层元素的 `touchstart` 事件：

```html
<button on:press="onOuterClick">
  <p on:touchstart="onInnerClick">inner</p>
  outer button
</button>
```

```js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    // 阻止事件冒泡，以免外层按钮响应点击事件
    event.stopPropagation();
    console.log('inner click');
  }
}
```

<glyphix id="components-button-click-2" height="48" width="360" inline>

``` html
<button on:press="onOuterClick">
  <p on:touchstart="onInnerClick">inner</p>
  outer button
</button>
```

``` css
button {
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}

button:active {
  opacity: 0.5;
}

p {
  border: 2px solid #444;
  padding: 0 10px;
}
```

``` js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    event.stopPropagation();
    console.log('inner click');
  }
}
```

</glyphix>

尝试上面的示例，就会发现点击 `inner` 文本时只有 `onInnerClick` 方法被触发，`onOuterClick` 不会被触发，而 `button` 也不会呈现按下时的效果。

::: tip
`press` 事件通常也是在松手时触发的，但是它要求按钮的按下事件从未被阻止过。因此阻止冒泡的内层元素 `touchstart` 事件可以阻止外层按钮的 `press` 事件触发。
:::

#### 其他触发时机

这种方法的限制在于内层元素的 `touchstart` 事件在按下时触发，也可以改用 `touchend` 事件来来触发，但是要保留 `touchstart` 事件的阻止冒泡功能。这样可以确保在按下时不会触发外层按钮的 `press` 事件。

```html
<button on:press="onOuterClick">
  <p on:touchstart="$event.stopPropagation()" on:touchend="onInnerClick">inner</p>
  outer button
</button>
```

```js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    // 这里不需要阻止冒泡，因为已经在 touchstart 阻止了
    console.log('inner click');
  }
}
```

<glyphix id="components-button-click-3" height="48" width="360" inline>

``` html
<button on:press="onOuterClick">
  <p on:touchstart="$event.stopPropagation()" on:touchend="onInnerClick">inner</p>
  outer button
</button>
```

``` css
button {
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}

button:active {
  opacity: 0.5;
}

p {
  border: 2px solid #444;
  padding: 0 10px;
}
```

``` js
export default {
  onOuterClick() {
    console.log('outer click');
  },
  onInnerClick(event) {
    console.log('inner click');
  }
}
```

</glyphix>

打开浏览器控制台，再次点击 `inner` 文本，你会发现 `onInnerClick` 的日志会在松手时才打印，并且一样可以阻止外层 `button` 响应手势。
