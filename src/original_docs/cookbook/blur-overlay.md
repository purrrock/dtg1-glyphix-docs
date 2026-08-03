# 模糊覆盖菜单

## 效果展示

本教程展示将背景模糊之后展示遮盖层菜单的开发技巧。下面的示例展示了这种交互效果（点击右下角的 “...” 按钮会显示遮挡界面）。

<glyphix id="cookbook-blur-overlay" width="410" height="502" title="模糊覆盖层" inline>

</glyphix>

本教程的主要目的是展示如何用 Glyphix 实现带有模糊的界面。

## 实现方法

### 文字阴影

示例中的文字 “Hokkaido sika deer” 阴影可以通过叠加一层模糊文本来实现：
``` html
<stack class="wallpaper-title">
  <p class="shadow">Hokkaido sika deer</p>
  <p>Hokkaido sika deer</p>
</stack>
```
将两段相同的文本放置在一个 [`stack`](/components/stack.md) 组件内，并将底层文本作为阴影。这是通过底层文本的 `shadow` CSS 类实现的：
``` css
.shadow {
  color: #0008;
  /* 为背景文本添加模糊，以呈现阴影效果 */
  filter: blur(8px);
  /* 必须使用 transparent 标记元素是透明的 */
  transparent: true;
}
```
将背景文本的颜色设置为半透明的灰色，并通过模糊过滤器（[`filter: blur(8px)`](/framework/generic/styles.md#filter)）属性将 `<p>` 文本组件作为阴影。请注意前景的文字颜色不应该透明，否则可能和 `.shadow` 层叠加。

### 自定义字体

文本 “Hokkaido sika deer” 通过自定义字体来呈现，在 Glyphix 中可以使用和 Web 一样的方法来引入自定义字体：
``` css
@font-face {
  font-family: 'Playwrite Australia SA';
  src: url('/assets/PlaywriteAUSA-Regular.ttf');
}

.wallpaper-title {
  font-family: 'Playwrite Australia SA', 'sans-serif';
  color: #ffffff;
  margin-top: 25%;
}
```
如你所见，可以在 CSS 通过 [`@font-face`](/framework/generic/styles.md#font-face-规则) 块来声明一个字体，并在元素的 [`font-family`](/framework/generic/styles.md#font-family) 属性中引用。

### 背景层模糊

由于目前通过 [`router` API](/api/system-router.md) 弹出的页面不支持半透明背景，因此不能使用页面来实现弹出菜单。但可以使用这种技巧来模拟弹出的“页面”：
``` html
<stack class="window" :disabled="popups">
  <image class="wallpaper" src="/assets/images/sika-deer.jpg" />
  ...
</stack>
<div class="overlay" if="popups">
  ...
</div>
```
你需要在页面中添加两层元素（本例中是 `stack.window` 和 `div.overlay`）,并通过一个条件（如 `popups`）来控制。具体来说：
- `popups` 控制底层元素的 `disabled` 属性，因此当 `popups` 为真时，底层元素不会响应手势等输入；
- `popups` 同时还控制顶层元素的渲染，当它为真时顶层元素会显示出来。

在遮挡层弹出时，[`disabled`](/framework/generic/properties.md#disabled) 属性还提供了模糊底层元素的机会：
``` css
.window:disabled {
  filter: blur(40px);
}
```
当元素被设置了 `disabled` 属时，底层元素的 `:disabled` 伪元素也会激活，因此上面 CSS 的模糊效果会起作用。

::: tip
由于 Glyphix 不支持浏览器的 [`backrop-filter`](https://developer.mozilla.org/docs/Web/CSS/backdrop-filter) 属性，所以不能直接通过 `div.overlay` 的 CSS 规则来实现背景模糊，而是要用本示例的技巧。
:::

## 性能风险

由于模糊效果是计算密集的，开发者需要特别注意它的性能负担。我们建议仅在静态界面中使用模糊效果，最好还要为需要模糊的元素添加 [`quiescent`](/framework/generic/properties.md#quiescent) 属性。

如果可能的话，应该在物理设备上测试带有模糊的界面是否满足性能预期。
