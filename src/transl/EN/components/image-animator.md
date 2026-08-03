# image-animator


The `image-animator` component is used to play a set of picture sequence frame animations. The component is an inline element by default.


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



## property


### `images` <decl type="string[]" set />


Set the sequence frame picture collection. Each element of `images` is the path or URI of the frame image. Usually, the size of each frame is the same.


Supports images in PNG or JPEG format.


If the sequence frame does not change, it is recommended to make it a non-reactive property to save memory:


```js
export default {
  // frames is a non-responsive property of the component
  frames: [
    "/assets/sprite-1.png",
    "/assets/sprite-2.png",
    "/assets/sprite-3.png",
  ],
};
```


The advantage of this is that multiple component objects will share the same `frames` array object (responsive properties will be copied to each component instance). Sequence frames should be written in a `data` object only if they really require responsiveness.


If the sequence frames are encoded sequentially, you can use this trick to simplify the creation of the sequence frame array:


```js
export default {
  // 4-frame sequence numbered starting from 0
  frames: Array.from({ length: 4 }, (_, i) => `/assets/sprite-${i}.png`),
  // Alternatively, a sequence of 4 frames numbered starting from 1
  frames: Array.from({ length: 4 }, (_, i) => `/assets/sprite-${i + 1}.png`),
};
```


Play the animation by passing the `frames` array to the `images` attribute in the component template to specify the sequence frames:


```html
<image-animator :images="frames" play :duration="100" />
```


::: note

The `images` attribute currently does not support the `ImageFrame` structure of Quick Apps, so you cannot use frame collection definitions such as `[{ src: '...' },...]`.
:::



### `duration` <decl type="number" get set />


Specify the playback duration of each frame in milliseconds.


### `play` <decl type="'start' | 'pause' | 'stop'" get set listen />


Set the playback status, supporting start, pause, and end status. `image-animator` is in the `stop` state initially, so it will automatically stop at the first frame position of [`images`](#images).


| value | description |
| :-------: | ---------------------- |

| `'start'` | Start playing from the current frame. |
| `'pause'` | Pause playback and display the current frame. |
| `'stop'` | Stop playback and display the first frame. |


As shown above, `play` only supports three enumeration values: `'start`, `'pause'` or `'stop'`. But the following trick can be used to automatically play animations:


```html
<image-animator :images="frames" play :duration="100" />
```


That is, directly write a `play` attribute with no value, which is equivalent to the [隐式属性](/framework/component/template.md#隐式属性值) writing method of `:play="true"`. `true` This boolean type is always converted to the default `'start'` enumeration value. This writing method is very suitable for scenes that require automatic playback of sequence frame animation.


### `iteration` <decl type="number" set />


Set the number of repeat playback times for all sequence frames in `images`. When the upper limit is reached, it will automatically switch to `'pause'` mode. `0` means unlimited play times.


## Inherited properties


`image-animator` has the same [继承属性](/components/image.md#继承的属性) behavior as `image`.


## CSS description


`image-animator` has the same [CSS 行为](/components/image.md#css-说明) as `image`.