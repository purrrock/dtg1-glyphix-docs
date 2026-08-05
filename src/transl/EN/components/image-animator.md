# image-animator

The `image-animator` component is used to play a sequence of image frames as an animation. It is an inline element by default.

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

## Properties

### `images` <decl type="string[]" set />

Sets the collection of sequence frame images. Each element in `images` is the path or URI of that frame's image. Typically, the dimensions of each frame image are consistent.

Supports PNG or JPEG format images.

If the frame sequence does not change, it is recommended to define it as a non-reactive property to save memory:

```js
export default {
  // frames is a non-reactive property of the component
  frames: [
    "/assets/sprite-1.png",
    "/assets/sprite-2.png",
    "/assets/sprite-3.png",
  ],
};
```

The advantage of doing this is that multiple component instances will share the same `frames` array object (reactive properties are copied to each component instance). You should only place it in the `data` object if the frame sequence truly requires reactivity.

If the frame sequence is sequentially numbered, you can use this trick to simplify the creation of the frames array:

```js
export default {
  // 4 frames numbered starting from 0
  frames: Array.from({ length: 4 }, (_, i) => `/assets/sprite-${i}.png`),
  // Or, 4 frames numbered starting from 1
  frames: Array.from({ length: 4 }, (_, i) => `/assets/sprite-${i + 1}.png`),
};
```

Pass the `frames` array to the `images` property in the component template to specify the frame sequence and play the animation:

```html
<image-animator :images="frames" play :duration="100" />
```

::: note
The `images` property does not yet support Quick App's `ImageFrame` structure, so you cannot use frame collection definitions like `[{ src: '...' }, ...]`.
:::

### `duration` <decl type="number" get set />

Specifies the playback duration of each frame in milliseconds.

### `play` <decl type="'start' | 'pause' | 'stop'" get set listen />

Sets the playback state, supporting start, pause, and stop states. `image-animator` is initially in the `stop` state, so it will automatically rest at the first frame position of [`images`](#images).

|   Value   | Description                          |
| :-------: | ------------------------------------ |
| `'start'` | Starts playing from the current frame. |
| `'pause'` | Pauses playback and displays the current frame. |
| `'stop'`  | Stops playback and displays the first frame. |

As shown above, `play` only supports three enumerated values: `'start'`, `'pause'`, or `'stop'`. However, the following trick can be used to automatically play the animation:

```html
<image-animator :images="frames" play :duration="100" />
```

Writing the `play` property without a value is equivalent to the [implicit property value](/framework/component/template.md#隐式属性值) syntax `:play="true"`. Boolean types like `true` are always converted to the default `'start'` enumerated value. This syntax is very useful for scenarios that require automatic playback of frame sequence animations.

### `iteration` <decl type="number" set />

Sets the number of repetitions for all frame sequences in `images`. When the maximum limit is reached, it will automatically switch to `'pause'` mode. `0` indicates infinite playback.

## Inherited Properties

`image-animator` shares the same [inherited property](/components/image.md#继承的属性) behavior as `image`.

## CSS Notes

`image-animator` shares the same [CSS behavior](/components/image.md#css-说明) as `image`.