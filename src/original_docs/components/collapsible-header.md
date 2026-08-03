# collapsible-header

`collapsible-header` 组件用于为滚动列表添加一个可以折叠的标题栏。这种效果用于为手表类设备提供一种节约视图区域的交互效果，提升用户体验。

::: warning
<experimental /> 这是一个实验性组件，不要用本文档中没有示范的方法来使用它。
:::

## 属性

本组件支持[通用属性](/framework/generic/properties.md)，没有专用属性。

## 使用方法

`collapsible-header` 组件中必须要有两个子组件，否则可能产生非预期的效果。具体示例如下：

```html
<collapsible-header>
  <p>这是可折叠的标题</p>
  <scroll> ... </scroll>
</collapsible-header>
```

其中第一个子元素是一个可折叠的标题，而第二个元素必须是 [`scroll`](/components/scroll.md) 等可滚动的容器。下面是一个具体的例子：

<glyphix id="components-collapsible-header-1" height="360" width="360" title="可折叠标题栏">

```html
<collapsible-header>
  <p class="title-bar" on:click="clickTitle">TITLE BAR</p>
  <scroll scroll-snap="center" deformation="fisheye">
    <p for="x in 20" class="item">item {{ x + 1 }}</p>
  </scroll>
</collapsible-header>
```

```js
import prompt from "@system.prompt";

export default {
  clickTitle() {
    prompt.showToast({ message: "title clicked" });
  }
}
```

```css
.title-bar {
  margin: 56px auto auto;
  transparent: true;
  font-size: 1.5rem;
}

.item {
  height: 33.3%;
  background-color: #ddd;
  border-radius: 20%;
  margin: 8px;
  transparent: true;
  padding: 12px;
  text-align: center;
}
```

</glyphix>

### 原理说明

`collapsible-header` 接受两个子组件，其中第一个是可折叠的标题栏，第二个必须要是类似 `scroll` 的可滚动组件。`collapsible-header` 会组合这两个组件，并在列表滚动时操纵可折叠的标题栏的显示效果。

可以使用类似流式布局的方法来控制标题栏的位置，例如：

```css
/* 元素的顶部间距为 48px，左右居中，适用于圆形屏幕。 */
margin: 48px auto auto;
/* 元素左侧和顶部间距为 12px，适用于方型屏幕。 */
margin: 12px auto auto 12px;
```

根据实际需求将上述样式设置给标题栏元素即可实现特定的对齐效果。还可以使用包含子元素的复杂组件作为标题栏，例如使用一个包含返回按钮和页面标题文本的组件。但要注意，在点击标题栏时，点击事件可以同时发送到滚动列表和标题栏，如果存在冲突，可以通过阻止事件冒泡来解决。

### 注意事项

必须为 `collapsible-header` 按照上述要求提供两个子组件，且不要搞错顺序。另外，由于可折叠的标题栏和底层的滚动列表是堆叠显示的，这可能让列表的第一个元素和标题栏重叠显示。必要时，开发者应考虑某种占位方式来避免重叠，且 `scroll` 的居中[吸附模式](/components/scroll.md#scrollsnap)（`scroll-snap="center"`）也可以避免重叠。
