# image-animator

`image-animator` 组件用于播放一组图片序列帧动画，组件默认是行内元素。

<glyphix id="image-animator-1" height="190" width="360" >

```html
<div class="flex-column">
  <div class="frame-box">
    <image-animator :images="frames" :play="play" :duration="100" />
  </div>
  <div>
    <button on:click="play = 'start'">start</button>
    <button on:click="play = 'pause'">pause</button>
    <button on:click="play = 'stop'">stop</button>
  </div>
</div>
```

```js
export default {
  data: {
    play: "stop",
  },
  frames: Array.from({ length: 60 }, (_, i) => `/assets/planet-${i}.png`),
};
```

```css
.flex-column {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.frame-box {
  border: 2px solid lightgray;
  border-radius: 8px;
  padding: 8px;
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
```

</glyphix>

## 属性

### `images` <decl type="string[]" set />

设置序列帧图片集合。`images` 的每个元素都是该帧图片的路径或者 URI。通常，每帧图片的尺寸是一致的。

支持 PNG 或者 JPEG 格式的图片。

如果序列帧不会变化，那么建议将其作为非响应式属性以节省内存：

```js
export default {
  // frames 是组件的非响应式属性
  frames: [
    "/assets/sprite-1.png",
    "/assets/sprite-2.png",
    "/assets/sprite-3.png",
  ],
};
```

这样做的好处是多个组件对象会公用同一个 `frames` 数组对象（响应式属性会拷贝到每一个组件实例）。仅当序列帧确实需要响应式特性时，才应该将其写在 `data` 对象中。

如果序列帧是按顺序编码的，那么可以使用这种技巧来简化序列帧数组的创建：

```js
export default {
  // 从 0 开始编号的 4 帧序列帧
  frames: Array.from({ length: 4 }, (_, i) => `/assets/sprite-${i}.png`),
  // 或者，从 1 开始编号的 4 帧序列帧
  frames: Array.from({ length: 4 }, (_, i) => `/assets/sprite-${i + 1}.png`),
};
```

在组件模板中将 `frames` 数组传递给 `images` 属性以指定序列帧，从而播放动画：

```html
<image-animator :images="frames" play :duration="100" />
```

::: note
`images` 属性现在还不支持快应用的 `ImageFrame` 结构，因此你不能使用 `[{ src: '...' }, ...]` 这样的帧集合定义。
:::

### `duration` <decl type="number" get set />

指定每一帧的播放时长，单位为毫秒。

### `play` <decl type="'start' | 'pause' | 'stop'" get set listen />

设置播放状状态，支持开始、暂停、结束状态。`image-animator` 在初始时处于 `stop` 状态，因此会自动停在 [`images`](#images) 的第一帧位置。

|    值     | 描述                   |
| :-------: | ---------------------- |
| `'start'` | 从当前帧开始播放。     |
| `'pause'` | 暂停播放并显示当前帧。 |
| `'stop'`  | 停止播放并显示第一帧。 |

如上所示，`play` 只支持 `'start`、`'pause'` 或者 `'stop'` 三种枚举值。但是下面的技巧可以用来自动播放动画：

```html
<image-animator :images="frames" play :duration="100" />
```

即直接写一个没有值的 `play` 属性，它是等效于 `:play="true"` 的[隐式属性](/framework/component/template.md#隐式属性值)写法。`true` 这种布尔类型总是会转换为默认的 `'start'` 枚举值。这种写法非常适用于需要自动播放序列帧动画的场景。

### `iteration` <decl type="number" set />

设置设置 `images` 中所有序列帧的重复播放次数，当达到次数上限时将自动切换到 `'pause'` 模式。`0` 表示无限次数播放。

## 继承的属性

`image-animator` 具有和 `image` 相同的[继承属性](/components/image.md#继承的属性)行为。

## CSS 说明

`image-animator` 具有和 `image` 相同的 [CSS 行为](/components/image.md#css-说明)。
