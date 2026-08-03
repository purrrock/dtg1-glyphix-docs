# Context File: 02_glyphix_ui_components_EN.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/transl/EN/components/a.md

# a


Anchor component, which defaults to an inline element, is used to jump to the specified page.


## property


### `href` <decl type="string" get set />


Specify the [页面名称](/framework/application/manifest.md#pages) or URI string to be jumped.


``` html
<a href="page1">跳转到 page1 页面</a>
```


Unlike the `<a>` tag in the Web, the `a` component only supports page jumps but not hyperlink jumps.


The `href` attribute also supports [URI](/framework/application/resource.md#uri) strings of the form `PageName?key=value`, which are URIs consisting of the page name (as the path field) and the query field. The query field of the URI will be parsed as the page's jump parameter. For example, when clicking this `<a>` element:


``` html
<a href="page1?text=test-text&message=hello">跳转到 page1 页面</a>
```


Equivalent to calling the following [`router.push()`](/api/system-router.md#push) method:


``` js
router.push({
  uri: 'page1',
  params: {text: 'test-text', message: 'hello'}
})
```


::: tip

Please note that the value of the query field in the URI will only be parsed as a string type, so `100` in `page1?size=100` will be parsed as a string `'100'` instead of a number `100`. If you need to pass parameters of a specific type, use the [`router`](/api/system-router.md) API.
:::


============================================================
FILE_PATH: src/transl/EN/components/barcode.md

# barcode


The `barcode` component is used to display the [Code 128](https://en.wikipedia.org/wiki/Code_128) barcode. The `barcode` component can display any ASCII string and is suitable for displaying product barcodes, payment codes and other information.


In a fluid layout, the `barcode` component defaults to a block-level element (`block`) and will be displayed on a separate line.


## property


### `value` <decl type="string" get set />


Set the content to be displayed in the barcode. Arbitrary ASCII strings are supported.


## CSS description


To make barcodes easily scannable, the CSS properties of the `barcode` component should be set correctly, including:
- `color`: Bar code bar color, generally set to black (`black` or `#000`);
- `background-color`: The background color of the barcode is usually white (`white` or `#fff`);
- `padding` / `margin`: Sufficient inner and outer margins can avoid confusion between barcodes and other elements and increase the scanning recognition rate;
- `width` / `height` : The size of the barcode must be large enough to be easily photographed.


By default, each barcode of the barcode component will occupy $2\rm px$ width and $32\rm px$ height, which may be too small on small screen devices such as watches. It is recommended that developers manually set the `width` / `height` attributes of the barcode component as needed and test on the device.


The following example shows how to use the barcode component. Please note that various margins are set for the `barcode` component in CSS. This is to ensure that there is enough space between the barcode and other interface elements to avoid interfering with scanning.


<glyphix id="barcode-1" :height="150" :width="350">



``` html
<div>
  <barcode :value="text"/>
  <p>{{ text }}</p>
</div>
```


``` js
export default {
  data: {
    text: '9787111407010'
  }
}
```


``` css
div {
  background-color: black;
  padding: 8px;
}

barcode {
  margin: 8px;
  padding: 8px;
  color: black; /* 将条形码前景色设置为黑色 */
  background-color: white; /* 将条形码背景色设置为白色 */
  border-radius: 16px;
  height: 80px;
}

p {
  color: white;
  font-size: 0.75rem;
  text-align: center;
}
```


</glyphix>



::: tip

The codepoint color ( `color` ) and background ( `background-color` ) styles of high-contrast barcode components should always be set explicitly. To avoid deviations between the device's default style theme and inherited style attributes, resulting in reduced recognition.


At the same time, please set a large enough padding (`padding`) to ensure easy scanning and recognition.
:::


============================================================
FILE_PATH: src/transl/EN/components/button.md

# button


The button component is an inline element by default. When the component is touched, the corresponding event can be triggered.


## property


### `checkable`  <decl type="boolean" set />


When set to `true`, it means that one touch only responds to one state change, that is: from pressed to lifted state or from lifted to pressed state. And the monitoring value of pressed state `press` is `true` and raised state is `false`.


### `toggleable` <decl type="boolean" set />


When set to `true`, it means that the monitoring value of `press` can be changed. Press it to `true` and lift it to `false`.


### `press` <decl type="boolean" get set listen />


When setting the `press` attribute, you can change the state of the component. You can also monitor the status of the component through the `on` command. By default, it is completed with one touch. The callback parameter is `ture`. You can use the `checkable` `toggleable` attribute to obtain different monitoring values ​​and status.


## Functional limitations


### `click` event invalid


When the `button` component is not used, the click event of any native component is usually monitored through the [`click`](/framework/generic/properties.md#click) attribute. But this approach generally doesn't work with `button`. For example this code:
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
    // Prevent events from bubbling up so that outer buttons don't respond to click events
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



You might expect that clicking on the `"inner"` text will trigger the `onInnerClick` method and block `onOuterClick`. But you will find that this is not the case (it is best to open the browser console to view the log): The `onInnerClick` method will not be triggered at all, only the outer `button` component will respond to the click, that is:
- When clicking the `inner` text, the `inner click` log will not appear, only the `outer click` log;
- `button` The interaction on press is triggered (transparency reduced).


It's like clicking outside `outer text`. The reason for this is that the `button` component responds first to the entire life cycle of the press gesture (from press to release), while the `click` event is triggered when the hand is released. This means that whether or not the inner element's `click` event handler prevents bubbling does not change this behavior.


#### Solution


To solve this problem, you should listen to the `press` event of the outer `button` and listen to the `touchstart` event of the inner element:


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
    // Prevent events from bubbling up so that outer buttons don't respond to click events
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



Try the above example, you will find that only the `onInnerClick` method is triggered when the `inner` text is clicked, `onOuterClick` will not be triggered, and `button` will not show the effect when pressed.


::: tip

The `press` event is also typically fired when the button is released, but it requires that the button press event has never been blocked. So preventing the inner element's `touchstart` event from bubbling can prevent the outer button's `press` event from firing.
:::



#### Other triggering times


The limitation of this method is that the `touchstart` event of the inner element is triggered when pressed. You can also use the `touchend` event to trigger it, but the function of preventing bubbling of the `touchstart` event must be retained. This ensures that the outer button's `press` event does not fire when pressed.


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
    // There is no need to prevent bubbling here because it has been blocked in touchstart
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



Open the browser console and click the `inner` text again. You will find that the log of `onInnerClick` will be printed only when you let go, and it can also prevent the outer layer `button` from responding to the gesture.

============================================================
FILE_PATH: src/transl/EN/components/canvas.md

# canvas


Canvas component, by using scripts in JavaScript, you can draw graphics, etc. on `canvas`.


### `context`


**Value type**: context content obtained by canvas API


**Action**: Setup


Sets the canvas context in which graphics are to be drawn.

============================================================
FILE_PATH: src/transl/EN/components/checkbox.md

# checkbox


The `checkbox` (checkbox) element displays a checked (tickled) box when activated, indicating that an item is selected.


<glyphix id="checkbox-1" :height="65" title="单个复选框">


``` html
<div>
  <checkbox id="checkbox" ::checked="checked" />
  <label target="checkbox">Check me!</label>
  <p>checked: {{ checked }}</p>
</div>
```


``` js
export default {
  data: {
    checked: true
  }
}
```
</glyphix>



::: note

`checkbox` is usually a square that can be ticked, but the exact effect depends on the device. Developers currently cannot modify the color and other styles of `checkbox` through CSS.
:::



## property


### `checked` <decl type="boolean" get set listen />


This property indicates whether this check box is selected. Setting the `checked` attribute can switch the selected state of the check box: when the value is `true`, it is displayed in the selected state. You can also operate on individual checkboxes via two-way binding:
``` html
<checkbox model:checked="yes" />
```


The example earlier in this article demonstrates the use of this binding, please note that you do not bind to the [`value`](#value) attribute, but to `checked`.


The event is only fired when the user clicks on the checkbox, causing the `checked` attribute to change.


::: warning

Do not set the `checked` attribute in [复选框组](#group) to avoid confusion.
:::



### `value` <decl type="any" get set />


A JavaScript value that identifies the checkbox value, usually a string or number. This value is not displayed, but it can be used in [分组操作](#group).


### `group` <decl type="any[]" get set listen />


If you have multiple associated `checkbox` components, you can combine the `group` and `value` attributes; checkboxes within the same group form an array of selected values. Please refer to the following example:


<glyphix id="checkbox-group" :height="65" title="复选框组" >


``` html
<div>
  <p>selected colors: {{selected.join(', ')}}</p>
  <div>
    <checkbox id="red" value="red" model:group="selected" />
    <label target="red">red</label>
    <checkbox id="blue" value="blue" model:group="selected" />
    <label target="blue">blue</label>
    <checkbox id="yellow" value="yellow" model:group="selected" />
    <label target="yellow">yellow</label>
  </div>
</div>
```


``` js
export default {
  data: {
    selected: ['yellow']
  }
}
```


``` css
label {
  margin-right: 0.5rem;
}
```


</glyphix>



This can be achieved by bidirectionally binding the `group` attribute to a reactive array (`selected` in the example) using `model:group` or `::group`:
- When the user operates a checkbox in the group, the value of the responsive array will be updated;
- When the elements of the reactive array change, it will be reflected in the performance of `checkbox`.


As shown in the example above: In the initial state, the grouping checkbox is selected based on the value of the `group` attribute. Specifically, for a checkbox like:
``` html
<checkbox value="red" model:group="selected" />
```
Since the `value` attribute specifies the `"red"` value, the checkbox will be checked when the value of the reactive attribute `selected` contains `"red"` (such as `["red"]` ). Clicking the checkbox again causes it to become unchecked and the `"red"` element is removed from the `selected` array.


::: tip

If you don't want to group checkboxes, you can also use the [`checked`](#checked) attribute to operate individually. But don't use `checked` and `group` at the same time, Glyphix doesn't take this case into account.
:::



### `indeterminate` <decl type="boolean" get set />


The `indeterminate` attribute indicates that the checkbox is in an undefined state. When this property is `true`, the checkbox has a horizontal line like a minus sign in the middle to indicate uncertainty about its status.


The indeterminate state can be used when an item has multiple options: if all children are selected, the parent will also be selected; if all are unselected, the parent will not be selected either. If some of the children are selected, the parent will be in an indeterminate state.


The following example demonstrates this usage. This example demonstrates crafting a list of enchantment tables so that when you select a partial recipe, the "Enchantment table" checkbox will be partially selected. As you can see, this example allows you to use the parent checkbox to check or uncheck all of its children.


<glyphix id="checkbox-indeterminate" :height="140" title="三态复选框" >


``` html
<div>
  <div>
    <!--
      当 selected.length == 3 时，entirety 就会选中，否则：
      - 如果 selected.length == 0，那么未选中；
      - 其他情况意味着选择了部分配方，因此处于 indeterminate 状态。
      -->
    <checkbox id="entirety"
              :indeterminate="selected.length && selected.length < 3"
              :checked="selected.length == 3"
              on:checked="selectEntirety" />
    <label target="entirety">
      &nbsp;Enchantment table:
    </label>
  </div>
  <div class="group">
    <div for="x in parts">
      •
      <checkbox :id="x" :value="x" model:group="selected" />
      <label :target="x">&nbsp;{{x}}</label>
    </div>
  </div>
</div>
```


``` js
export default {
  data: {
    selected: ['Diamonds'],
  },
  parts: ['Book', 'Diamonds', 'Obsidian'],
  // This function is called when the entirety checkbox is clicked to set the selected state of all recipes
  selectEntirety(status) {
    // Use [... this.parts ] to copy the list to avoid modifying it in place
    this.selected = status ? [...this.parts] : []
  },
}
```


``` css
.group {
  margin-left: 0.4rem;
}
```


</glyphix>



::: tip

When the `checked` attribute is set (note that it is not cleared), the `indeterminate` attribute is automatically cleared. Even if a checkbox has both properties, it will appear selected rather than in an indeterminate state.
:::



### CSS behavior


The checkbox is an inline element by default, its display size is determined by the `font-size` CSS property, and it will be aligned with the display baseline of the text. Please do not manually specify attributes such as `width` and `height`, otherwise the display may be confused.

============================================================
FILE_PATH: src/transl/EN/components/collapsible-header.md

# collapsible-header


The `collapsible-header` component is used to add a collapsible title bar to the scrolling list. This effect is used to provide an interactive effect that saves the view area for watch-type devices and improves the user experience.


::: warning

<experimental /> This is an experimental component, do not use it in ways not demonstrated in this document.
:::



## property


This component supports [通用属性](/framework/generic/properties.md) and has no dedicated attributes.


## How to use


There must be two subcomponents in the `collapsible-header` component, otherwise unexpected effects may occur. Specific examples are as follows:


```html
<collapsible-header>
  <p>这是可折叠的标题</p>
  <scroll> ... </scroll>
</collapsible-header>
```


The first child element is a collapsible title, and the second element must be a scrollable container such as [`scroll`](/components/scroll.md). Here is a specific example:


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



### Principle description


`collapsible-header` accepts two child components, the first of which is a collapsible title bar, and the second must be a scrollable component similar to `scroll`. `collapsible-header` combines these two components and manipulates the display of the collapsible title bar as the list scrolls.


You can use something like Fluid Layout to control the position of the title bar, for example:


```css
/* 元素的顶部间距为 48px，左右居中，适用于圆形屏幕。 */
margin: 48px auto auto;
/* 元素左侧和顶部间距为 12px，适用于方型屏幕。 */
margin: 12px auto auto 12px;
```


Set the above style to the title bar element according to actual needs to achieve a specific alignment effect. You can also use a complex component containing child elements as a title bar, for example using a component containing a back button and page title text. But be aware that when the title bar is clicked, the click event can be sent to both the scroll list and the title bar. If there is a conflict, it can be resolved by preventing the event from bubbling.


### Things to note


You must provide both subcomponents for `collapsible-header` as specified above, and in the correct order. In addition, since the collapsible title bar and the underlying scrolling list are displayed stacked, this may cause the first element of the list to overlap with the title bar. When necessary, developers should consider some kind of placeholder method to avoid overlap, and centered `scroll` [吸附模式](/components/scroll.md#scrollsnap) ( `scroll-snap="center"` ) can also avoid overlap.

============================================================
FILE_PATH: src/transl/EN/components/div.md

# div


`div` is the most basic container component. `div` supports subcomponents and layout, but does not support scrolling (content will be cropped directly if it exceeds the boundary). If you want content to scroll, use the [scroll](scroll) component.


## Things to note


### text display


The `div` component cannot be used directly to display text. Instead, text components such as `p` must be used to display text, for example:


```html
<!-- 错误的写法，不会显示文本 -->
<div>text content.</div>
<!-- 正确的写法 -->
<p>text content.</p>
```


However, if `div` has multiple child elements, you can use text as its child element:


```html
<div>
  first element,
  <span style="color: #f0f">second element.</span>
</div>
```


<Glyphix id="components-div-text-element" height="48" width="360" inline >



```html
<div>
  first element,
  <span style="color: #f0f">second element.</span>
</div>
```


</Glyphix>


============================================================
FILE_PATH: src/transl/EN/components/drawer-navigation.md

# drawer-navigation


A subcomponent of [`drawer`](drawer), used to display specific drawer contents.


## property


### `direction` <decl type=" 'left' | 'right' | 'up' | 'down' " set />


The `direction` attribute is used to set the direction of `drawer-navigation`. The optional values ​​are `'left'`, `'right'`, `'up'`, and `'down'`.


| value | description |
| :-------: | ------------------------------------------------ |

| `'left'` | The drawer-navigation on the left side of the screen is used to respond to the gesture of sliding from left to right. |
| `'right'` | The drawer-navigation on the right side of the screen is used to correspond to the gesture of sliding from right to left. |
| `'up'` | The drawer-navigation at the bottom of the screen is used to respond to the gesture of sliding from bottom to top. |
| `'down'` | The drawer-navigation on the top of the screen is used to respond to the gesture of sliding from top to bottom. |


============================================================
FILE_PATH: src/transl/EN/components/drawer.md

# drawer


The drawer component is hidden by default and can display content by sliding.
drawer is the basic drawer component. Drawer supports sub-components and layouts. You can set up 4 drawer-navigation components in the drawer to display drawers in four positions: top, bottom, left and right.


[`drawer`](drawer) The sliding speed of the component follows the sliding speed of the gesture. The faster the sliding speed of the gesture, the faster the sliding speed of the component.


### Example


The following example demonstrates the functionality of the drawer


<glyphix id="components-drawer" height="360" width="360" >



``` html
 <drawer class="drop-down">
      <drawer-navigation direction="down" class="drop-down1">
        <p>dawn panel</p>
      </drawer-navigation>
      <drawer-navigation direction="up" class="drop-down1">
        <p>up panel</p>
      </drawer-navigation>
       <drawer-navigation direction="left" class="drop-down1">
        <p>left panel</p>
      </drawer-navigation>
       <drawer-navigation direction="right" class="drop-down1">
        <p>right panel</p>
      </drawer-navigation>
</drawer>
```
``` css
.drop-down {
    background-color: pink;
  }
.drop-down1 {
    background-color: blue;
  }
p {
  background-color: lightgreen;
  text-align: center;
  margin: 10px;
}
```
</glyphix>


============================================================
FILE_PATH: src/transl/EN/components/image-animator.md

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

============================================================
FILE_PATH: src/transl/EN/components/image.md

# image


The picture component is used to display picture elements and is centered by default. `image` components are inline elements by default.


## property


### `src` <decl type="string" get set />


Set the [URI](/framework/application/resource.md) of the image. For asset images in the application package, relative paths and absolute paths are supported. The `image` component supports the common image formats PNG and JPEG.


::: tip

The `image` component only supports local image resources, unlike the Web's `img` element which can directly display network image resources. See How to [显示网络图片](#显示网络图片) in Glyphix for details.
:::



### `noCache` <decl type="boolean" get set />


Set whether the image should be cached. By default, caching will be used to optimize image loading speed. The `image` component will not use the cache when the `noCache` attribute is turned on, and the image will always be reloaded from the file after changing the [`src`](#src) attribute.


Image caching is a technology that optimizes loading speed and reduces memory usage. When an image with the same URI is already loaded in the system, the `image` component with caching enabled will directly use the resource. However, image files downloaded from the Internet with fixed names and possibly changing contents (such as `internal://cache/avatar.png` for user avatars) usually need to enable the `noCache` attribute to ensure correct behavior.


Even if the `noCache` attribute is turned on, the `image` component still will not detect updates to the image file content. In this case, you need to manually change the [`src`](#src) attribute. Considering that reactive frameworks filter identical assignments, you have to use a trick like this:
``` html
<!-- 假设这是需要更新显示的图片，no-cache 属性是必须的。 -->
<image :src="avatarImage" no-cache />
```


``` js
const avatarImage = 'internal:// cache/ avatar.png ' // Assume this is a picture downloaded from the Internet

export default {
  data: {
    avatarImage: avatarImage
  },
  // Call this method after the avatar download is completed to update the interface
  onAvatarDownloaded() {
    this.avatarImage = null // A new value must be assigned first
    this.avatarImage = avatarImage // Reassign to the correct URI
  }
}
```
In the above example, the responsive attribute `this.avatarImage` is first changed to `null` and then reassigned, so that the value changes, thereby bypassing the optimization mechanism of the responsive framework and enabling image updates.




::: warning

Resources with fixed URIs must be updated using this technique, otherwise the displayed content may not change. To be on the safe side, if the resource paths obtained from the network may be duplicated, you also need to use this technique to ensure that the interface is updated.


In addition, you must wait for the image download or file writing to be completed before updating the `src` attribute of the `image` component, otherwise the interface cannot be updated normally.
:::



### `async` <decl type="boolean" get set />


Load image resources asynchronously. This mode can ensure that image loading will not block the UI thread and improve the smoothness of the interface. However, compared to the default synchronous loading mode, images loaded asynchronously do not display the actual content, so they are not suitable for all interfaces.


Asynchronous loading mode is suitable for images downloaded from the network. Unlike image assets that are automatically optimized when the application is packaged, web images are usually common formats such as PNG or JPEG that are slow to decode. Synchronously decoding network images will be very laggy, and in such scenarios there is usually no need to display images immediately.


`async` can be used together with the [`noCache`](#nocache) attribute, since the latter is also mainly used for web images:
``` html
<image :src="avatarImage" no-cache async />
```


## Inherited properties


These properties are inherited from the native component's [generic properties](/framework/generic/properties.md), but the`image` component handles these properties specially.


### `opacity` <decl type="number" set />


Set the transparency of the image, the value range is $[0, 1]$, where $0$ means completely transparent, $1$ means completely opaque, and the default value is $1$.


### `transform` <decl type="string" set />


Set the transformation effect of the image, which is equivalent to the [`transform`](/framework/generic/styles.md#transform) attribute of CSS.


## CSS description


### Unsupported common properties


Compared with other native components, `image` is special. It does not support common attributes such as `background-color` and `border`. This is also very different from web standards. Specifically, the following CSS properties are not supported:


- [`background-color`](/framework/generic/styles.md#background-color), [`background-image`](/framework/generic/styles.md#background-image)
- [`border`](/framework/generic/styles.md#border), [`border-top`](/framework/generic/styles.md#border-top), [`border-right`](/framework/generic/styles.md#border-right), [`border-bottom`](/framework/generic/styles.md#border-bottom), [`border-left`](/framework/generic/styles.md#border-left)


This means that you cannot add a background color or image to the `image` component by setting CSS properties, nor can you set a border style for it. However, the `image` component supports the [`border-radius`](/framework/generic/styles.md#border-radius) attribute.


### Special properties


The `image` component supports other CSS properties that can be used with non-container components, but several properties can be used to achieve special effects.


#### `transform`


Set the transformation of the image. When this CSS attribute is used for `image`, it has a similar effect to [`transform`](/framework/generic/styles.md#transform) for other elements, but it can be displayed normally without setting the [`transparent`](/framework/generic/styles.md#transparent) attribute.


#### `opacity`


Set the transparency of the image, which has the same effect as the [`opacity`](#opacity) attribute.


#### `border-radius`


Set the corner radius of the picture. You can use this property to add rounded corners to the picture. The usage method is the same as the general [`border-radius`](/framework/generic/styles.md#border-radius). The `image` component will always apply rounded corners to the four corners of the image, regardless of whether the aspect ratio of the image is consistent with the aspect ratio of the `image` component itself.


#### `object-fit`


The `image` component's `object-fit` attribute defaults to `none`, which differs from the web standard (which defaults to `fill` ). By default, the image will not be automatically scaled, but will be displayed centered at the original size. If the size exceeds the container, it will be cropped. This design is based on the consideration of MCU device characteristics:
- **Performance first**: Image scaling usually requires additional calculations, and some devices even implement interpolation scaling through software, which will significantly reduce the frame rate.
- **Image quality consistency**: On some devices, even scaling down can cause noticeable blurring or aliasing. The default of no scaling ensures pixel-level rendering without distortion.
- **Memory Restricted**: Default scaling can mask resource usage issues, resulting in inadvertently loading images that are too large, wasting valuable storage and memory space.


It is recommended to provide image resources that match the display area during the design stage, so that the image can be displayed correctly in the default state; only when necessary, the display effect should be adjusted by explicitly setting `object-fit` (such as `contain`).


## Tips


### Show network pictures


#### Avatar scenes


This section demonstrates a method that requires loading images from the network. This method is mainly used in situations such as user avatars. That is, the images have a fixed storage location locally, but the content may change. Due to the caching policy of the Glyphix runtime, you need to use the techniques in this example to ensure that the display content is updated.


``` html
<template>
  <image :src="avatar" no-cache />
</template>
```


``` js
import request from '@system.request'

export default {
  data: {
    avatar: null
  },
  onInit() {
    this.downloadAvatar()
  },
  async downloadAvatar() {
    const saveFile = 'internal://files/avatar.png'
    await request.download({
      url: 'https://example.com/url/to/avatar.png',
      filename: saveFile,
    }).complete
    // For details on the techniques here, see the description of the noCache attribute.
    this.avatar = null
    this.avatar = saveFile
  }
}
```


============================================================
FILE_PATH: src/transl/EN/components/input.md

# input


The default is an inline element, which provides an interactive interface and receives user input.


## property


### `type` <decl type="'checkbox' | 'radio'" set />


Controls that can be set to the above value types, the actual form of the final `input` component is determined according to the set type.


### `name` <decl type="string" set />


Set the `input` component name.


### `checked` <decl type="boolean" set />


The checked status of the current component can trigger the checked pseudo-class, which takes effect when the type is checkbox. When set to `on`, the checkbox is checked by default.


### `value` <decl type="string" set />


Set the value of the `input` component.

============================================================
FILE_PATH: src/transl/EN/components/label.md

# label


The `label` component is used to display text or markup information, and is an inline element by default. `label` can display mark information with the following form components:
- [input](input)
- [radio](radio)
- [switch](switch)
- [checkbox](checkbox)


When `label` is associated with a supported form component, clicking the `label` component will also trigger the value update of the form component.


## property


### `text` <decl type="string" set get />


The text content of the label supports attribute syntax or text subelement syntax:
``` html
<label text="label text"></label>
<label>label text</label>
```


### `target` <decl type="string" set get />


The ID of the target component. For example:
```html
<radio id="red" /><label target="red">red</label>
```
Clicking on the `label` component in the example will also trigger the update of the `radio` component with ID `red`, but clicking on the `label` component will not trigger touch events such as `click` on the target component.


Considering performance issues, only target components that are at the same level as the `label` component (i.e. have the same parent component) are supported.


::: warning

Changing the target component is not currently supported.
:::


============================================================
FILE_PATH: src/transl/EN/components/list-item.md

# list-item


The subcomponent of `list` is used to display specific items in the list. It supports subcomponents and layout, but does not support scrolling.


::: tip

Glyphix does not provide the same list container component as Quick Apps, but uses [`scroll`](scroll.md) to implement rolling containers. Similarly, there is no need to use the `list-item` component. Please use [`div`](div.md) or any other component directly as the list item element.
:::


============================================================
FILE_PATH: src/transl/EN/components/mapview.md

# mapview


Map component, used to load and display tile-based maps. `mapview` supports gesture panning, zoom level switching, current location display and route navigation drawing, and is a core component for building map applications.


`mapview` defaults to block-level elements.


::: tip

`mapview` is a runtime extension component. Before using it, you need to confirm that the target platform has integrated the `mapview` module.
:::



## property


### `baseUri` <decl type="string" get set />


The **base path** URI of the tile image resource. The tile files will be stored in a fixed hierarchical structure in this directory. `mapview` will automatically calculate the required tile file path based on the current zoom level and coordinates. The format is:


```
{baseUri}/{zoomLevel}/{tileX}/{tileY}/normal.png     (标准地图)
{baseUri}/{zoomLevel}/{tileX}/{tileY}/satellite.png  (卫星地图)
```


Typical usage is to cache map tiles to the local storage of the device, and then point `baseUri` to the corresponding directory:


```html
<mapview baseUri="internal://files/tiles/map_provider" />
```


### `tileType` <decl type="number" get set />


The layer type of the tile map, the values ​​are as follows:


| value | description |
| :-: | :-- |

| `0` | Standard map (default), load `normal.png` tile file |
| `1` | Satellite map, load `satellite.png` tile file |


### `loadPlace` <decl type="string" get set />


The **placeholder** URI displayed when the tile image is loading. When the corresponding tile file has not been cached locally, `mapview` will display the image at the tile location until the [`reload()`](#reload) refresh is triggered after the tile is downloaded.


```html
<mapview loadPlace="/assets/imgs/loading.png" />
```


### `zoomLevel` <decl type="number" get set />


Map zoom level, the value range is $[3, 23]$, the default value is $17$. The higher the level, the more detailed the map; the lower the level, the wider the visible range.


::: info

This attribute corresponds to the Zoom Level in the map tile standard, which is consistent with the level definition of mainstream tile services such as Bing Maps and Google Maps.
:::



### `arrowIcon` <decl type="string" get set />


Image URI for the current location icon. The icon will be drawn at the screen position corresponding to the longitude and latitude specified by [`navCoordinate`](#navcoordinate) or [`setLocation()`](#setlocation), and the icon will be aligned with the coordinate point with the center point.


```html
<mapview arrowIcon="/assets/imgs/location.png" />
```


### `navCoordinate` <decl type="{ x: number, y: number }" get set />


The latitude and longitude coordinates of the current location, in the format `{ x: latitude, y: longitude }`, where `x` is the latitude and `y` is the longitude. Setting this property only updates the icon position and does not automatically move the map center to these coordinates. If you need to position the map center to the current location at the same time, please use the [`setLocation()`](#setlocation) method and pass in `force: true`.


::: tip

For scenarios where real-time position tracking is required, it is recommended to use the [`setLocation()`](#setlocation) method instead of directly assigning this attribute to control whether to automatically return to center through the `force` parameter.
:::



### `arrowLineWidth` <decl type="number" get set />


The line width of the navigation route, in pixels. The default value is `12`.


### `arrowLineBackgroundColor` <decl type="color" get set />


The **background color** of the navigation route (the color of the traveled part), accepts CSS color values, and the default value is `#898b90`.


### `arrowLineForgeColor` <decl type="color" get set />


The foreground color of the navigation route (the color of the remaining route portion), accepts CSS color values, and defaults to `#4b73ec`.


### `smallMem` <decl type="boolean" get set />


Whether to enable low memory device mode, the default value is `false`.


When enabled, `mapview` will merge and scale four 256×256 tiles into a 512×512 picture for drawing, reducing the number of tiles cached in memory at the same time to adapt to devices with limited memory.


::: warning

Low memory mode will sacrifice some map clarity and should only be turned on when the device is obviously low on memory.
:::



### `missTiles` <decl type="Array<{ z: number, x: number, y: number }>" get listen />


Read-only attribute, triggers monitoring when the map finds a local missing tile file. The callback parameter is an array, each element describes a missing tile:


| Field | Type | Description |
| :-- | :-- | :-- |

| `z` | `number` | Zoom Level |
| `x` | `number` | Tile X coordinate (column number) |
| `y` | `number` | Tile Y coordinate (row number) |


After receiving this event, the application usually needs to download the corresponding tile file from the server and call [`reload()`](#reload) to refresh the map after the download is completed:


```js
export default {
  missTileHandler(tiles) {
    // tiles: [{ z: 17, x: 105234, y: 49832 }, ...]
    downloadTiles(tiles).then(() => {
      this.$element('mapview').reload()
    })
  }
}
```


```html
<mapview id="mapview" on:missTiles="missTileHandler" />
```


### `directionInfo` <decl type="{ event: string, stepIndex?: number, distance?: number }" get listen />


Read-only property of the map event, the listener is triggered when the following operations occur on the map:


| `event` value | Trigger timing | Additional fields |
| :-- | :-- | :-- |

| `"move"` | Triggered when the user gestures to pan the map | None |
| `"calc"` | Triggered when the position and yaw distance are recalculated in navigation | `stepIndex` (current route segment index), `distance` (deviation distance from the current position to the route, in meters) |


```js
export default {
  onDirectionInfo(info) {
    if (info.event === 'move') {
      // If the user manually drags the map, the automatic return to center can be paused.
    } else if (info.event === 'calc') {
      console.log(`Current step: ${info.stepIndex}, yaw distance: ${info.distance} meters`)
    }
  }
}
```


## method


### `reload()`


Reload all tiles. After the new tile file is written to the local storage, this method needs to be called to refresh the map display.


```js
this.$element('mapview').reload()
```


### `locate()`


Moves the center of the map to the current location (the coordinates specified by [`navCoordinate`](#navcoordinate)) for the "return to current location" function.


```js
this.$element('mapview').locate()
```


### `setLocation(location)`


Sets the current location coordinates and optionally moves the map center to that location.


| Parameter fields | Type | Description |
| :-- | :-- | :-- |

| `latitude` | `number` | Latitude |
| `longitude` | `number` | Longitude |
| `force` | `boolean` | If it is `true`, the map center will be positioned to this coordinate immediately (equivalent to calling [`locate()`](#locate)), if it is `false`, only the icon position will be updated |


```js
// Only updates the icon position, does not move the map
this.$element('mapview').setLocation({
  latitude: 39.9042,
  longitude: 116.4074,
  force: false,
})

// Update the icon position and move the map center to that coordinate
this.$element('mapview').setLocation({
  latitude: 39.9042,
  longitude: 116.4074,
  force: true,
})
```


### `startNav(linePoints)`


Set navigation route and start navigation. After calling, the map will automatically locate the starting point of the route and draw the complete route.


`linePoints` is an array of route points, and each element is a binary array in the format of `[经度, 纬度]`:


```js
const route = [
  [116.397428, 39.909736],  // [longitude, latitude]
  [116.404730, 39.913370],
  [116.410072, 39.918933],
]
this.$element('mapview').startNav(route)
```


::: warning

Note the order of parameters: the first value of each coordinate point is longitude, and the second value is latitude, contrary to the common "latitude first" convention.
:::



### `insetNavPoint(linePoints)`


Appends a route point to an existing navigation route, in the same format as [`startNav()`](#startnav). Suitable for scenarios where route data is received in segments. After appending, you need to call [`reload()`](#reload) to refresh the display.


```js
this.$element('mapview').insetNavPoint(newPoints)
this.$element('mapview').reload()
```


## Usage example


### Basic map display


The following example shows how to configure a basic map component to listen for missing tile events and trigger downloads.


```html
<template>
  <mapview
    id="map"
    :zoomLevel="zoom"
    :baseUri="tileBaseUri"
    :tileType="tileType"
    loadPlace="/assets/imgs/tile-loading.png"
    arrowIcon="/assets/imgs/location.png"
    on:missTiles="onMissTiles"
    on:directionInfo="onDirectionInfo"
  />
</template>
```


```js
export default {
  data: {
    zoom: 17,
    tileType: 0,
    tileBaseUri: 'internal://files/tiles/my_provider',
  },

  onReady() {
    // Initialize current location
    this.$element('map').setLocation({
      latitude: 39.9042,
      longitude: 116.4074,
      force: true,
    })
  },

  onMissTiles(tiles) {
    // tiles: Missing tile list, initiate a download request to the server
    fetchTilesFromServer(tiles).then(() => {
      this.$element('map').reload()
    })
  },

  onDirectionInfo(info) {
    if (info.event === 'move') {
      // User panned the map
    }
  },
}
```


```css
mapview {
  width: 100%;
  height: 100%;
}
```


### Navigation route drawing


```html
<template>
  <stack>
    <mapview
      id="map"
      :baseUri="tileBaseUri"
      :zoomLevel="zoom"
      arrowIcon="/assets/imgs/location.png"
      arrowLineWidth="10"
      arrowLineBackgroundColor="#888888"
      arrowLineForgeColor="#1a73e8"
      on:missTiles="onMissTiles"
    />
    <button @click="startNavigation">开始导航</button>
  </stack>
</template>
```


```js
export default {
  data: {
    zoom: 16,
    tileBaseUri: 'internal://files/tiles/my_provider',
  },

  startNavigation() {
    const route = [
      [116.397428, 39.909736],
      [116.404730, 39.913370],
      [116.410072, 39.918933],
    ]
    this.$element('map').startNav(route)
  },

  onMissTiles(tiles) {
    fetchTilesFromServer(tiles).then(() => {
      this.$element('map').reload()
    })
  },
}
```


### Low memory device adaptation


```html
<mapview
  id="map"
  :baseUri="tileBaseUri"
  :zoomLevel="zoom"
  :smallMem="isLowEndDevice"
/>
```


```js
import SysDevice from '@system.device'

export default {
  data: {
    zoom: 17,
    tileBaseUri: 'internal://files/tiles/my_provider',
    isLowEndDevice: false,
  },
  onInit() {
    // Determine whether to enable low memory mode based on the archive bit in the device
    this.isLowEndDevice = SysDevice.memoryProfile <= 4096
  },
}
```

============================================================
FILE_PATH: src/transl/EN/components/marquee.md

# marquee


The `marquee` component is used to display scrolling text content and only supports single-line display. The `marquee` component does not support any subcomponents including `span`.


`marquee` supports common CSS properties, but due to implementation reasons, the `text-align` property may not be supported at this time. Since `marquee` only displays a single line of text and will scroll when the text content is too long, attributes such as `max-lines` also have no effect.


## property


### `text` <decl type="string" get set/>


Set the text content in the same way as the [`text`](p.md#text) attribute of the `p` component. When the length of the text content exceeds the width of `marquee`, the text will automatically scroll.

============================================================
FILE_PATH: src/transl/EN/components/p.md

# p


Text component. `p` is a block-level element by default. Unlike [`span`](span), the `p` component does not support text crossing lines when set as an inline element. If you need to implement rich text typesetting, you should consider using components such as `span`.


## property


### `text` <decl type="string" get set/>


Set text content and support the following two writing methods.


``` html
<p text="Hello Glyphix"></p>
<p>Hello Glyphix</p>
```


<glyphix id="p" :height="70" inline>



``` html
<div>
  <p text="Hello Glyphix"></p>
  <p>Hello Glyphix</p>
</div>
```


</glyphix>



### `color` <decl type="string" get set/>


Set text color. Only hexadecimal color codes are supported, such as `#f00`, `#e8bb80ff`, etc. This property is a shortcut for modifying the CSS inline property [`color`](/framework/generic/styles.md#color).


### `lines` <decl type="number" get set/>


Set the maximum number of lines of text. Text exceeding this number will be truncated or omitted. This property is a shortcut for modifying the CSS inline property [`max-lines`](/framework/generic/styles.md#max-lines).


### `text-align` <decl type="string" set/>


Set the text alignment, supporting `left`, `center`, `right` and other values. This property is a shortcut for modifying the CSS inline property [`text-align`](/framework/generic/styles.md#text-align).


### `font-size` <decl type="string" set/>


Set the text font size, supporting `12px`, `1.5em` and other CSS font size values. This property is a shortcut for modifying the CSS inline property [`font-size`](/framework/generic/styles.md#font-size).


### `font-weight` <decl type="number" set/>


Set the text font weight. Currently, only integer values ​​are supported, such as `400`, `600`, etc. This property is a shortcut for modifying the CSS inline property [`font-weight`](/framework/generic/styles.md#font-weight).


## Tips


### size control


In general, do not manually set the height of the `p` component, e.g.
``` css
p.my-paragraph {
  height: 48px;
  font-size: 32px;
}
```
On the face of it, this sets a height for the `p` component that is larger than the font size, but what happens is:
- For single-line text, the actual height of some fonts may exceed the font size, and even heights of `48px` may appear vertically clipped.
- For multi-line text, setting a fixed height will cause the multi-line text to be cropped and cannot be displayed completely.


If you wish to control the number of lines of text displayed, you should use [`max-lines`](/framework/generic/styles.md#max-lines) and [`text-overflow`](/framework/generic/styles.md#text-overflow) to implement text truncation and omission instead of setting a fixed height.


### Text clipping animation <version-badge since="0.9"/>


You can use the [`width`](/framework/generic/styles.md#width) attribute with the [`transition`](/framework/component/prop-modifier.md#transition-修饰符) modification to implement text clipping animation. For example:


``` html
<p :width="state ? 240 : 0"
   width.transition="{duration: 2.0}">
  Hello Glyphix!
</p>
```


With the `max-lines: 1` style, you can achieve text cropping animation from left to right. But there is a problem with this animation: when the width is insufficient, the last character will be discarded instead of being cropped. The current workaround is to put the text content in a child component and animate the width of the parent component:


``` html
<div :width="state ? 240 : 1"
     width.transition="{duration: 2.0}">
  <p style="max-lines: 1">Hello Glyphix!</p>
</div>
```


<glyphix id="p-width-transition" title="文字裁剪动画" height="120">


``` html
<div class="container">
  <p class="animated-text"
     :width="state ? 240 : 0"
     width.transition="{duration: 2.0}">
    Hello Glyphix!
  </p>
  <div class="animated-text"
       :width="state ? 240 : 1"
       width.transition="{duration: 2.0}">
    <p>Hello Glyphix!</p>
  </div>
</div>
```


``` js
export default {
  data: {
    state: false
  },
  onReady() {
    setInterval(() => this.state = !this.state, 2500)
  }
}
```


```css
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.animated-text {
  margin: 4px;
  border: 1px solid #f00;
}

p {
  max-lines: 1;
  text-overflow: clip;
}
````


</glyphix>



However, when using a `div` element as a parent component, there is a problem with the animation: when the width is `0`, the layout size is calculated as `(width: 0, height: 0)`, which causes the element to be unable to occupy the vertical space and vertical jumps at the beginning of the animation. The solution is to set the width to a very small value (e.g. `1px` ) instead of `0` so that the element can occupy the vertical space and thus avoid the bounce problem.

============================================================
FILE_PATH: src/transl/EN/components/picker.md

# picker


Text selector component. This component displays a group of text. Clicking on the middle text item will trigger the selection event, and the sliding operation can make all text items scroll and display.


::: warning

`picker` The functionality of the component has not been verified and it is not maintained.
:::



## property


### `range` <decl type="string[]" set />


All strings in the `range` attribute value will be displayed in the `picker` component. The user can manipulate the `picker` component to scroll or select these strings.


`range` refers to [`index` 属性](#index) for the indexing method of strings in attribute values.


### `loop` <decl type="boolean" set />


Configure whether the `picker` component is displayed in a loop (i.e. infinitely long). When the value of this attribute is `true`, the loop display is enabled, and the default is `false`.


### `value` <decl type="string" listen />


Monitor the text of the current selected item. This monitoring will be triggered when the selected item changes during scrolling operation. The function of this attribute can also be implemented through the `on:index="handle(rangeData[$event])"` method.


### `index` <decl type="Integer" get set listen />


`picker` The selected item index value of the component. The indexing rules are: [`range` 属性](#range) The index value of the first string item in the attribute value array is $0$, and the indexes of other strings are increased by one in sequence. Setting the `index` attribute can specify the selected item of the `picker` component, and you can also listen to changes in this attribute to detect changes in the selected item caused by scrolling operations.


### `scroll` <decl type="{ x: number y: number }" get set listen />


The scrolling operation can be monitored through the `scroll` attribute, and the `picker` component can also be manipulated in code to display the scrolling effect. Similar to aligned list components, the `picker` operation of `scroll` also aligns to the nearest item.


Since the `picker` component only supports vertical mode, the `x` field of the `scroll` attribute value is always `0`.


### `scrolled` <decl type="boolean" read listen />


Monitor whether `picker` is in the scrolling state through the `scrolled` attribute. The attribute value triggered by the event is `true` which means that `picker` is scrolling, otherwise it means that `picker` has stopped scrolling.


The scrolling operation caused by user touch and scrolling through the `scroll` attribute will trigger the `scrolled` event. When `picker` stops from the scrolling state, the parameter value of the `scrolled` event is `false`.


### `damping` <decl type="number" set />


Set the damping coefficient of `picker` scroll animation. The valid value range is $[ 0.1, 50]$ (unsupported values ​​will be automatically modified to the upper and lower limits). The default value is $ 1.5 $. A larger damping coefficient will cause the animation to stop faster, and the default damping coefficient value can produce an inertial effect with a longer distance and longer duration.


The damping coefficient should be set to a constant and not modified. Modifying the damping coefficient will not affect the rebound animation.

============================================================
FILE_PATH: src/transl/EN/components/progress-arc.md

# progress-arc


The `progress-arc` component is used to display a circular progress bar and defaults to a block-level element.


## property


### `max` <decl type="number" set />


The maximum progress value that the [`value`](#value) attribute will not be greater than.


### `min` <decl type="number" get setet />


The minimum progress value that the [`value`](#value) attribute will not be less than.


### `value` <decl type="number" get set listen />


Set the progress value. The display ratio of the progress depends on the ratio of the `value` attribute in the interval from `min` to `max`, and the display ratio will be limited to $0\% \sim 100\%$. The `value` value is an integer. If a floating point value is set, only the integer part will be truncated.


### `busy` <decl type="boolean" get set />


Set whether the `progress-arc` component is in a busy state. In the busy state, a loading animation will be displayed instead of displaying the value of the `value` attribute. The following example demonstrates how to use a circular progress bar to simulate a loading animation:


<glyphix id="components-progress-arc-busy" height="100" width="300" title="模拟加载动画">


``` html
<progress-arc busy :startAngle="0" :stopAngle="360" />
```


</glyphix>



In this example, the difference between the start angle and the end angle of the progress bar is $360^\circ$. At this time, the typical loading animation effect can be displayed through the `busy` attribute.


::: tip

As long as the progress bar is circular, it will display a fixed busy animation effect, and the starting and ending angles have no effect.
:::



### `startAngle` <decl type="number" get set />


The starting angle of the arc-shaped progress bar. The default value is $135$. For more information, please refer to the [角度配置](#角度配置) chapter.


### `stopAngle` <decl type="number" get set />


The end angle of the arc-shaped progress bar. The default value is $405$. For more information, please refer to the [角度配置](#角度配置) chapter.


## Instructions for use


### angle configuration


Unlike linear [`progress`](progress.md), arc-shaped or circular progress bars need to be properly configured with `startAngle` attributes and `stopAngle` attributes to display properly. Both properties use angle units. In the screen coordinate system, $0^\circ$ points to the horizontal right direction, that is, the $3$ o'clock direction of the clock, and increases in the clockwise direction, and vice versa decreases.


The display of `progress-arc` is a linear interpolation of the angular range based on the scale of `value` in $[\texttt{min}, \texttt{max}]$. Specifically, the user will see the highlighted angle of progress starting at `startAngle` and ending at `valueAngle`:


$$

\begin{aligned}

  k &= \frac{\texttt{value} - \texttt{min}}{\texttt{max}-\texttt{min}}\\

  \texttt{valueAngle} &= (1-k)\texttt{startAngle} + k\cdot\texttt{stopAngle}

\end{aligned}

$$



Therefore, if you want to display a full circle of circular progress bar, you need to make the starting and ending angles differ by $360^\circ$, even though the two angles are visually the same. Alternatively, the starting angle can be larger than the ending angle, which will reverse the direction of the progress.


The examples below show various angle configurations in action, please note that the second example shows the reverse progress display technique.


<glyphix id="components-progress-arc-angles" height="120" width="720" title="角度配置示例">


``` html
<div>
  <p class="progress-label">{{value}}%</p>
  <stack>
    <p>default</p>
    <progress-arc :value="value" />
  </stack>
  <stack>
    <p>405~135</p>
    <progress-arc :startAngle="405" :stopAngle="135" :value="value" />
  </stack>
  <stack>
    <p>-45~225</p>
    <progress-arc :startAngle="-45" :stopAngle="225" :value="value" />
  </stack>
  <stack>
    <p>0~360</p>
    <progress-arc :startAngle="0" :stopAngle="360" :value="value" />
  </stack>
  <stack>
    <p>-90~270</p>
    <progress-arc :startAngle="-90" :stopAngle="270" :value="value" />
  </stack>
</div>
```


``` js
export default {
  data: { value: 0 },
  onInit() {
    setInterval(() => {
      this.value = this.value + 5
      if (this.value > 100)
        this.value = 0
    }, 500)
  }
}
```


``` css
div {
  display: flex;
}

progress-arc {
  width: 200px;
  padding: 0 8px 0 8px;
  stroke-width: 0.5rem;
}

p {
  text-align: center;
  font-size: 0.7rem;
}

.progress-label {
  width: 3.5rem;
}
```


</glyphix>



## CSS specifications


### Size calculation


The display size of `progress-arc` is determined by its `width` and `height` attributes. `progress-arc` will occupy the shorter axis, and the center of the arc-shaped progress bar will be the center of the element. By default, the size of `progress-arc` may be close to one character, which will lead to very weird display effects, so it is usually necessary to explicitly specify the width and height in CSS, or use other reasonable layout strategies.


::: tip

It's best to specify a reasonable width and height for the `progress-arc` component, otherwise it may not be recognized. At a minimum, the `width` CSS property should also be set, and the component's layout strategy will automatically use the $1:1$ aspect ratio.
:::



### CSS properties


The appearance of the `progress-arc` component can be adjusted via CSS.


#### `stroke-width`


This property specifies the arc outline width of the `progress-arc` component. The value type is [长度](/framework/render/style-and-layout.md#长度) and does not support percentage units.


::: tip

If you want the drawing width of the `progress-arc` component to be proportional to the font size, it is recommended to use the [`rem`](/framework/application/font-config.md#rem-字号单位) length unit, such as `0.15rem`.
:::



#### `color`


Set `progress-arc` to highlight the color of the progress bar. By default, the system theme color will be used.


#### `background-color`


Set the color of the `progress-arc` background progress bar, which will be configured according to the system theme by default.


### CSS pseudo-elements


#### `value`


============================================================
FILE_PATH: src/transl/EN/components/progress.md

# progress


The `progress` component is used to display the progress bar and defaults to a block-level element.


## property


### `max` <decl type="number" set />


The maximum progress value that the [`value`](#value) attribute will not be greater than.


### `min` <decl type="number" set />


The minimum progress value that the [`value`](#value) attribute will not be less than.


### `value` <decl type="number" set get listen />


Set the progress value. The display ratio of the progress depends on the ratio of the `value` attribute in the interval from `min` to `max`, and the display ratio will be limited to $0\% \sim 100\%$. The `value` value is an integer. If a floating point value is set, only the integer part will be truncated.


### `vertical` <decl type="boolean" set />


If the value of the `vertical` attribute is `true`, the `progress` component will be displayed vertically, otherwise it will be displayed horizontally. The default value is `false`.


## CSS specifications


Developers can adjust the appearance of the `progress` component through CSS.


### Size calculation


The default width and height of `progress` are the same as the element's font size, which is set by the [`font-size`](/framework/generic/styles.md#font-size) attribute (can also be inherited). The size of `progress` can be customized through the [`width`](/framework/generic/styles.md#width) and [`height`](/framework/generic/styles.md#height) attributes.


### CSS properties


The following CSS properties may be useful:
- [`background-color`](/framework/generic/styles.md#background-color) can control the background color of `progress`;
- [`color`](/framework/generic/styles.md#color) can control the color of the progress bar of `progress`;
- [`border-radius`](/framework/generic/styles.md#border-radius) can set `progress` to a rounded border, for example `50%` will produce a semicircular border;


Other CSS properties may be useful, such as the [`border`](/framework/generic/styles.md#border) property to style the border.


### CSS pseudo-elements


#### `value`


This pseudo-element can define the `progress` progress bar alone without containing the style of the background part. For example, you can set the corner radius of the scroll bar background and the progress bar part separately to achieve the effect that the outer border has a circular line cap and the progress bar has a straight cap.


``` css
progress {
  border-radius: 50%; /* 滚动条背景圆角 */
}

progress::value {
  border-radius: 0; /* 滚动条的进度条没有圆角 */
}
```


### CSS example


The following example demonstrates some ways to customize the appearance of the progress bar through CSS.


<glyphix id="components-progress-styles" height="140" width="480" title="进度条样式">


``` html
<div>
  <!-- 默认样式 -->
  <progress :value="40" />
  <!-- 直头进度条样式 -->
  <progress class="flat" :value="50" />
  <progress class="more-style" :value="60" />
</div>
```


``` css
div > * {
  margin: 8px;
}

.flat::value {
  /* value 伪元素的圆角半径设置为 0 即可实现进度条直头效果 */
  border-radius: 0;
}

.more-style {
  /* 自定义圆角半径 */
  border-radius: 30%;
  /* 进度条背景色 */
  background-color: #b3c5d7;
  /* 进度条前景颜色 */
  color: #b5179e;
  /* padding 可以调整进度条前景的边距 */
  padding: 6px;
  height: 1.25rem;
}
```


</glyphix>


============================================================
FILE_PATH: src/transl/EN/components/pullable.md

# pullable


The `pullable` component is used to add the function of triggering incremental loading or refreshing interactions during top pull-down and bottom pull-up in the scrolling list. `pullable` components are block-level elements by default.


::: warning

<experimental /> This is an experimental component, the function of `pullable` is not stable, and the animation may not be natural enough.
:::



`pullable` should be the first or last child component of [`scroll`](scroll.md). When it is the first child component, continuing to pull down at the head of the `scroll` content will trigger the `pulling` event; conversely, when `pullable` is the last child component of `scroll`, pulling up at the bottom will trigger the `pulling` event.


The `pullable` component is hidden by default and will only be displayed when it is pulled up/down. The following example demonstrates the use of the `pullable` component.


<glyphix id="components-pullable-1" height="360" width="360" title="上/下拉加载更多">


```html
<scroll scrollbar>
  <pullable :hold="pulldown" on:pulling="onPulldown">
    <progress-arc busy start-angle="0" stop-angle="360" />
    <p>{{pulldown || 'keep pull down...'}}</p>
  </pullable>
  <p for="item in items">item ({{item}})</p>
  <pullable :hold="pullup" on:pulling="onPullup">
    <progress-arc busy start-angle="0" stop-angle="360" />
    <p>{{pullup || 'keep pull up...'}}</p>
  </pullable>
</scroll>
```


```js
export default {
  data: {
    pulldown: null,
    pullup: null,
    items: []
  },
  first: 0,
  last: 0,
  onInit() {
    this.update(0, 10)
  },
  update(first, last) {
    for (let i = this.first; i > first; --i)
      this.items.unshift(i)
    for (let i = this.last; i < last; ++i)
      this.items.push(i)
    this.first = first
    this.last = last
  },
  onPulldown(event) {
    this.pulldown = event ? 'please release' : 'updating...'
    if (!event) {
      setTimeout(() => {
        this.update(this.first - 5, this.last)
        this.pulldown = null
      }, 1000)
    }
  },
  onPullup(event) {
    this.pullup = event ? 'please release' : 'updating...'
    if (!event) {
      setTimeout(() => {
        this.update(this.first, this.last + 5)
        this.pullup = null
      }, 1000)
    }
  }
}
```


```css
scroll {
  display: flex;
  flex-direction: column;
}

scroll > p {
  background-color: #ddd;
  border-radius: 32px;
  margin: 12px;
  padding: 32px;
  text-align: center;
}

pullable {
  display: flex;
  justify-content: center;
  margin: 32px;
}

pullable > progress-arc {
  stroke-width: 0.25rem;
  margin-right: 16px;
}
```


</glyphix>



Please refer to [使用说明](#使用说明) for detailed usage.


## property


### `hold` <decl type="bool" get set />


By default, `pullable` is only visible when pulling down at the top or pulling up at the bottom, but when the `hold` attribute is `true`, the `pullable` component will remain visible. This property is typically set when a [`pulling`](#pulling) event results in a content update, and is canceled when the content update is complete.


### `pulling` <decl type="bool" get listen />


When `pullable` is completely pulled out, the `pulling` event will be triggered, and the meaning of its event value is:
- `true`: This event is triggered when the pull-down/pull-up reaches the full pull-out trigger distance of `pullable`;
- `false`: This event is triggered when the user lets go after reaching the above-mentioned complete pull-out condition.


The following example shows when the `pulling` event value is triggered. You can try slowly scrolling down from the top of the list and pay attention to the toast popup message when the `pulling` event is triggered.


<glyphix id="components-pullable-pulling" height="360" width="360" title="pulling 事件">


```html
<scroll scrollbar>
  <pullable :hold="refresh" on:pulling="onPulling">
    <p>pulling...</p>
  </pullable>
  <p for="item in 10">item {{item}}</p>
</scroll>
```


```js
import prompt from '@system.prompt'

export default {
  data: {
    refresh: false
  },
  onPulling(event) {
    prompt.showToast({
      message: `pulling: ${event ? 'trigged' : 'release'}`
    })
    if (!event) {
      this.refresh = true
      setTimeout(() => this.refresh = false, 1000)
    }
  }
}
```


```css
scroll {
  display: flex;
  flex-direction: column;
}

scroll > p {
  background-color: #ddd;
  border-radius: 32px;
  margin: 12px;
  padding: 32px;
  text-align: center;
}

pullable {
  text-align: center;
  margin: 32px;
}
```


</glyphix>



## Instructions for use


### Component location


The `pullable` component must be the first or last child of vertical `scroll`. It automatically determines the action mode based on position: detecting the user pulling down from the top of the list when it is the first child element, and vice versa.


For lists that only need to be refreshed by pulling down, the following usage will work:
```html
<scroll>
  <pullable :hold="refresh" on:pulling="onPulling">
    <p>pulling...</p>
  </pullable>
  <div for="item in items">
    ...
  </div>
</scroll>
```


JavaScript code can listen to the `pulling` event and control the `refresh` attribute:
``` js
export default {
  data: {
    refresh: false
  },
  onPulling(hold) {
    if (!hold) { // hold is false when the user lets go
      this.refresh = true // Indicates refreshing
      // In this example, a timer is used to simulate the loading operation and stop loading after 1s.
      setTimeout(() => this.refresh = false, 1000)
    }
  }
}
```


For specific effects, please refer to the example of the [`pulling`](#pulling) event document.


### Prompt content control


The `pullable` component can accommodate various components to display prompt content. As in the current example in this article, you can combine a loading animation with tooltip text. In addition, the value of the `pulling` event can be used to control the prompt content. It is generally recommended to use this state handling method:
1. Set a reactive attribute (such as `refresh` ) for each `pullable` component. The default value is `null`. The `refresh` attribute is also used to control the [`hold`](#hold) attribute of `pullable`.
2. In the initial state (i.e. `refresh` is false), the prompt content of `pullable` should remind the user to "continue pulling to update".
3. When the user pulls down, the `pulling` event is fired, taking 4 or 5 steps depending on its event value.
4. When `pulling` is `true`, the user should be prompted to "let go to start refreshing".
5. When `pulling` is `false`, it means that the user has let go. At this time, `refresh` should be set to `true` and start refreshing the content. And should remind the user "refreshing".
6. After the content refresh is completed, set `refresh` to `false` again and return to the initial state.


You can also refer to the first example in this document, which implements the continue loading function of pulling down at the head of the list and pulling up at the tail at the same time. This example uses a trick to control all the state of `pullable` using just one reactive property.


This trick sets the initial value of the `refresh` reactive attribute to `null` (similar to `false` ) and uses template code like this:
``` html
<pullable :hold="refresh" on:pulling="onPulling">
  <p>{{refresh || 'Continue to drop down'}}</p>
</pullable>
```
When `refresh` is not set, the default "continue pulling down" prompt content will be displayed once `pullable` is pulled out. Then, the `onPulling` event callback function should be written like this:
``` js
export default {
  async onPulling(event) {
    this.refresh = event ? 'please let go' : '更新中'
    if (!event) { // Trigger refresh operation when letting go
        await runRefreshJobs()
        this.refresh = null // Reset status after refresh completes
    }
  }
}
```


### limit


There are currently some limitations with the `pullable` component. In addition to having to be used in a vertical `scroll` component, you also need to ensure that the number of list elements exceeds the size of the `scroll` visible area, otherwise problems may occur. In addition, the interaction effect of `pullable` may be stiff.

============================================================
FILE_PATH: src/transl/EN/components/qrcode.md

# qrcode


The `qrcode` component is used to display the [QR Code](https://en.wikipedia.org/wiki/QR_code) QR code. This component can display any text data and is suitable for displaying information such as website addresses, payment codes, login scan code links, etc.


In a fluid layout, the `qrcode` component defaults to a block-level element (`block`) and will be displayed on a separate line.


## property


### `value` <decl type="string" get set />


Set the text data to be displayed as a QR code. The `qrcode` component will automatically select the appropriate version based on the length and length of the data. Currently, the highest supported version is $12$.


## CSS description


To make the QR code easy to scan, the CSS properties of the `qrcode` component should be set correctly, including:
- `color`: The code point color of the QR code, generally set to black (`black` or `#000`);
- `background-color`: The background color of the QR code is usually white (`white` or `#fff`);
- `padding` / `margin`: Sufficient internal and external margins can avoid confusion between the QR code and other elements and increase the scanning recognition rate;
- `width` / `height`: The size of the QR code must be large enough to facilitate shooting.


By default, each code point (module) of the QR code component will occupy the range of $4\rm{px}\times 4\rm{px}$, which may only be a barely recognizable size on a watch. However, layout strategies such as flex may reduce the size of the QR code, so developers are recommended to manually set the `width` / `height` properties of the QR code component as needed and test on the device.


The following example shows how to use the QR code component. Please note that various margins are set for the `qrcode` component in CSS. This is to ensure that there is enough space between the QR code and other interface elements to avoid interfering with scanning.


<glyphix id="qrcode-1" :height="450" :width="350">



``` html
<div>
  <qrcode :value="text"/>
  <p>{{ text }}</p>
</div>
```


``` js
export default {
  data: {
    text: 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array'
  }
}
```


``` css
div {
  background-color: black;
  padding: 8px;
}

qrcode {
  margin: 16px;
  padding: 16px;
  color: black; /* 将二维码前景色设置为黑色 */
  background-color: white; /* 将二维码背景色设置为白色 */
  border-radius: 16px;
}

p {
  color: white;
  font-size: 0.75rem;
}
```


</glyphix>



::: tip

The codepoint color ( `color` ) and background ( `background-color` ) styles of **high contrast** QR code components should always be set explicitly. To avoid deviations between the device's default style theme and inherited style attributes, resulting in reduced recognition.


At the same time, please set a large enough padding (`padding`) to ensure easy scanning and recognition.
:::


============================================================
FILE_PATH: src/transl/EN/components/radio.md

# radio


Radio buttons, which are inline elements by default, are often used in a **radio group**, which contains a set of radio buttons that describe a series of related options. Only one radio button in the group can be selected at a time. Radio buttons are typically rendered as small circles that are filled to highlight when selected.


<glyphix id="radio-1" :height="65" title="单选按钮">


``` html
<div>
  <p>picked color: {{color}}</p>
  <div>
    <radio id="red" value="red" model:group="color" />
    <label target="red">red</label>
    <radio id="blue" value="blue" model:group="color" />
    <label target="blue">blue</label>
    <radio id="yellow" value="yellow" model:group="color" />
    <label target="yellow">yellow</label>
  </div>
</div>
```


``` js
export default {
  data: {
    color: 'blue'
  }
}
```


``` css
label {
  margin-right: 0.5rem;
}
```


</glyphix>



::: tip

Radio buttons are similar to [`checkbox`](checkbox.md), but `radio` can only select one value from the group, while `checkbox` allows multiple values ​​to be selected.
:::



## property


### `checked` <decl type="boolean" get set listen />


This property indicates whether this radio button is selected. Setting the `checked` attribute can toggle the selected state of the radio button: when the value is `true`, it is displayed in the selected state.


The `checked` event is triggered when the user clicks on a radio button and causes its selected state to change.


::: tip

Manipulating the `checked` attribute is not a recommended use of `radio`, please use the [单选组](#group) method.
:::



### `value` <decl type="any" get set />


A JavaScript value that identifies the radio button value, usually a string or number. This value is not displayed, but it can be used in [单选组](#group).


### `group` <decl type="any" get set listen />


If you have multiple associated `radio` components, you can combine the `group` and `value` attributes. Radio buttons within the same group are mutually exclusive: the value of the `group` bound responsive property is equal to the `value` property of the selected radio button. For example:
``` html
<radio value="red" model:group="color" />
<radio value="blue" model:group="color" />
<radio value="yellow" model:group="color" />
```
Where `color` is a responsive attribute, and when the second radio button is selected, the value of `color` is `"blue"`. If all radio buttons' `value` and `color` do not match, then the radio button will not be selected. For example:
``` html
<p on:click="color = null">reset select</p>
```
The selected state will be cleared:


<glyphix id="radio-reset" :height="65" title="清除选中状态">


``` html
<div>
  <p on:click="color = null">picked color: {{color}} (click to reset)</p>
  <div>
    <radio id="red" value="red" model:group="color" />
    <label target="red">red</label>
    <radio id="blue" value="blue" model:group="color" />
    <label target="blue">blue</label>
    <radio id="yellow" value="yellow" model:group="color" />
    <label target="yellow">yellow</label>
  </div>
</div>
```


``` js
export default {
  data: {
    color: 'blue'
  }
}
```


``` css
label {
  margin-right: 0.5rem;
}
```


</glyphix>



### CSS behavior


The radio button is an inline element by default, its display size is determined by the `font-size` CSS property, and it will be aligned with the display baseline of the text. Please do not manually specify attributes such as `width` and `height`, otherwise the display may be confused.

============================================================
FILE_PATH: src/transl/EN/components/README.md

# Native components

============================================================
FILE_PATH: src/transl/EN/components/scroll-bar.md

# scroll-bar


Scroll bar component. This component can display a scroll bar when there is a lot of scrolling content, and the user can control the scrolling of the content through the scroll bar.


## property


### `value` <decl type="number" set get listen />


The current value of the scroll bar, which is a value between `min` and `max`. The default value is $0$.


### `min` <decl type="number" set />


The minimum value of the scroll bar, which should be no greater than `max`. The default value is $0$.


### `max` <decl type="number" set />


The maximum value of the scroll bar. This value should be no less than `min`. The default value is $100$.


### `pagestep` <decl type="number" set />


The scroll step size of the scroll bar, that is, the distance of each scroll. The default value is $10$.

============================================================
FILE_PATH: src/transl/EN/components/scroll.md

# scroll


A scrolling list container that supports any subcomponent. The scrolling direction of the list is specified by the specific layout method: when using fluid layout or `column` direction flex layout, the elements are laid out in the vertical direction, and the list can be scrolled vertically; when using `row` direction flex layout, the elements are laid out in the horizontal direction, and the list can be scrolled horizontally. The `scroll` component does not support bidirectional scrolling (that is, horizontal and vertical scrolling at the same time).


`scroll` components are block-level elements using fluid layout by default.


The `scroll` component can be scrolled using gesture interaction, and the vertical `scroll` component also supports encoder (rotating crown on the watch, mouse wheel on the simulator) scrolling.


::: tip

Some of the interactive examples in this document support mouse wheel interaction (mouse icon icon to the right of the title): you can hover the pointer inside the example and use the mouse wheel to scroll the list.
:::



## property


### `scroll` <decl type="{ scrollX: number, scrollY: number, scrollState: number }" get listen />


The `scroll` attribute value is an object containing the following fields: `scrollX`, `scrollY`, and `scrollState`. The `scrollX` and `scrollY` attributes represent the horizontal and vertical scrolling positions respectively, in pixels; the `scrollState` attribute represents the scrolling state, and its value is $0$, $1$ or $2$. The specific meaning is as shown in the following table. Changes to the `scroll` attribute can be monitored through the `on` directive. Any change in content location caused by user operations and API operations will trigger monitoring.


| `scrollState` value | Effect description |
| :--------------: | ------------------------------------------------------------------- |

| $0$ | Stopped sliding |
| $1$ | Swiping via user's gesture |
| $2$ | The user has let go, sliding caused by method calls such as [`scrollTo`](#scrollto) or inertia |


::: info

`scroll` The area where the child elements are located is called the "content" area, and the part actually displayed by the list component is called the "view" area. Elements are laid out in the content area, and their size may exceed the view area, and the display position of the content can be changed by scrolling.
:::



The range of the scroll position is usually within the content area, that is, `scrollX` for horizontal lists is within the range of $[0, \texttt{contentWidth}]$, and `scrollY` for vertical lists is within the range of $[0, \texttt{contentHeight}]$. But when the list is scrolled before the head of the content, `scrollX` or `scrollY` will be less than $0$; similarly, when the list is scrolled to the end of the content, the value of `scrollX` or `scrollY` will be greater than `contentWidth` or `contentHeight`.


::: warning

The `scroll` event will be triggered every frame during the scrolling process. Listening to this event in JavaScript code may cause obvious frame drops, so try to avoid using it.
:::



### `scrollTop` <decl type="number" set get listen />


The vertical scroll position, that is, the distance from the top of the content of the `scroll` component to the top of the viewport, in pixels. You can set the scroll position through this property, and you can also listen for changes in the scroll position through this property.


Unlike the [`scroll`](#scroll) attribute, the listener `scrollTop` attribute itself cannot distinguish between scrolling by the user's gestures and scrolling caused by API calls or inertia.


### `scrollLeft` <decl type="number" set get listen />


The vertical scroll position, that is, the distance from the left side of the content of the `scroll` component to the left side of the viewport, in pixels. You can set the scroll position through this property, and you can also listen for changes in the scroll position through this property.


Unlike the [`scroll`](#scroll) attribute, the listener `scrollLeft` attribute itself cannot distinguish between scrolling by the user's gestures and scrolling caused by API calls or inertia.


### `scrollWidth` <decl type="number" get listen />


`scroll` The width of the component's content area. The width of `scroll` in vertical layout is equal to the view width, while the width of `scroll` in horizontal layout is the sum of the widths of all elements. You can use this to monitor content width changes.


### `scrollHeight` <decl type="number" get listen />


`scroll` The height of the component's content area. The height of `scroll` in vertical layout is equal to the view height, while the height of `scroll` in horizontal layout is the sum of the heights of all elements. You can use this to monitor content height changes.


### `damping` <decl type="number" set />


Set the damping coefficient of the list scroll animation. The valid value range is $[0.1, 50]$ (unsupported values ​​will be automatically modified to the upper and lower limits). The default value is $1.5$. A larger damping coefficient will cause the animation to stop faster, and the default damping coefficient value can produce an inertial effect with a longer distance and longer duration.


<glyphix id="components-scroll-damping" height="360" width="360" title="阻尼效果" wheel>


``` html
<div>
  <span>damping: {{damping}}</span>
  <button on:click="increase">+</button>
  <button on:click="decrease">-</button>
  <scroll :damping="damping">
    <p for="x in 50" class="item">
      Item {{ x + 1 }}
    </p>
  </scroll>
</div>
```


``` js
export default {
  data: {
    damping: 1
  },
  increase() {
    this.damping += 1
    if (this.damping > 20)
      this.damping = 1
  },
  decrease() {
    this.damping -= 1
    if (this.damping < 1)
      this.damping = 19.5
  }
}
```


``` css
span {
  color: #404040;
}

scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  height: 300px;
  width: 360px;
}

.item {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px 5px;
  margin: 10px;
  border-radius: 16px;
}

button {
  color: #fafafa;
  background-color: #adadad;
  border-radius: 12px;
  margin-left: 16px;
  margin-bottom: 16px;
  width: 1.2rem;
}
```


</glyphix>



::: tip

The damping coefficient should be set to a constant and not modified. Modifying the damping coefficient will not affect the rebound animation.
:::



### `snapshot` <decl type="boolean" get set />


When the `snapshot` attribute is turned on, the subcomponents in the list will turn on snapshot mode. For related demonstrations, please refer to the [`quiescent`](/framework/generic/properties.md#quiescent) attribute of native components.


Enabling snapshots may increase the frame rate of complex interfaces. For example, when a list item contains a large amount of text and contains a non-transparent background, snapshot mode can cache and merge a large number of drawing operations into a small number of snapshots. The Glyphix framework caches these snapshots across repeated draws to further improve performance.


However, the `snapshot` attribute does not provide a guarantee that snapshots will be used for subcomponents. This attribute may be ignored when the system has insufficient memory or when there is no need to use snapshots.


### `deformation` <decl type="string | function" set />


Set the deformation effect of the list. Through the deformation effect, you can achieve fish-eye and other appearances. A built-in morph effect can be specified by name (a string), or a morph effect can be defined through a JavaScript function.


| Value | Effect Description |
| :---------: | :------------------------------: |

| `'none'` | No deformation effect (default value) |
| `'fisheye'` | Built-in fisheye effect |
| function | Specify deformation effects through JavaScript functions |


The deformation effect should be constant and not modified.


When the list is set to fisheye deformation effect, it is recommended to set the [`scrollSnap`](#scrollsnap) attribute to `'center'` to get the most reasonable effect.


The picture below demonstrates the fisheye deformation effect. You can adjust whether to center the image through the "center" switch.


<glyphix id="components-scroll-deformation" height="360" width="360" title="鱼眼效果" wheel>


``` html
<div>
  <p>center <switch ::value="center" /></p>
  <scroll deformation="fisheye" :scroll-snap="center ? 'center' : null">
    <p for="x in 15">
      Item {{ x + 1 }}
    </p>
  </scroll>
</div>
```


``` css
div {
  color: #404040;
  display: flex;
  flex-direction: column;
}

scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  flex: 1;
}

scroll > p {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 40px 10px;
  margin: 5px;
  border-radius: 50%;
}
```


``` js
export default {
  data: {
    center: true
  }
}
```


</glyphix>



::: tip

Deformation effects generally use snapshots, so there is no need to repeatedly set `snapshot` when setting the `deformation` attribute.
:::



### `scrollSnap` <decl type="'none' | 'start' | 'center' | 'edge'" get set />


Set the alignment and snapping mode of list items. For example, you can center-align the element or snap it to the edge of the element.


| value | description |
| :--------: | -------------------------------------------------------------------------------------------------------------- |

| `'none'` | The element has no suction alignment and attachment effects, that is, the child elements can stop at any position according to scroll inertia. |
| `'start'` | The starting position of the element is aligned to the starting position of the viewport when scrolling stops. This mode is currently not supported. |
| `'center'` | The scroll stop is when the center of the element is aligned to the center of the viewport. |
| `'edge'` | When scrolling stops, the start or end position of the element is aligned to the start or end position of the viewport. But if the scroll does not cross the element boundary, it will not cause adsorption. |


The `scrollSnap` attribute does not adjust the element size, but can use mechanisms such as layout to implement a list of equal-sized items.


::: warning

This property should be set when the component is initialized and cannot be changed, otherwise interaction errors may occur.
:::



### `index` <decl type="number" get set listen />


The index of the currently displayed subcomponent. When the `index` attribute is set, the component will scroll to the specified subcomponent through animation. Position changes can be monitored through the `on` directive, and changes in subcomponent index can be monitored through the `index` attribute.


The value of `index` is automatically restricted to ensure that it points to a valid element. When using `index`, you must ensure that all elements of the `scroll` component are static (that is, the [`position`](/framework/generic/styles.md#position) attribute of CSS is the default `static`), otherwise an error will occur.


### `finalChanged` <decl type="bool" get set />


Set whether the [`index`](#index) change event is only triggered when scrolling stops. By default (that is, `finalChanged` is `false`), whenever the scroll gesture or other reasons cause the `index` attribute of the `scroll` component to change, its listening event will be triggered. However, doing so can easily cause animation frames to drop, or trigger too frequent and unnecessary events. When `finalChanged` is set, the `index` changed event will only be triggered when scrolling stops.


::: tip

When implementing effects such as point indicators by monitoring the `index` attribute, it is recommended to set `finalChanged` to `true`. This can avoid frame drops caused by event-triggered rendering updates during the sliding process.
:::



The following example demonstrates the effect of `finalChanged`. You can try switching the "final-changed" checkbox, then slide the list and observe the frequency and timing of changes to `index`.


<glyphix id="components-scroll-final-changed" height="360" width="360" title="延迟 index 事件" wheel>


``` html
<div>
  <p>
    <checkbox id="checkbox" ::checked="finalChanged" />
    <label target="checkbox">final-changed</label>
    index: {{index}}
  </p>
  <scroll :final-changed="finalChanged" ::index="index">
    <p for="x in 50">
      Item {{ x + 1 }}
    </p>
  </scroll>
</div>
```


``` css
div {
  color: #404040;
  display: flex;
  flex-direction: column;
}

scroll {
  display: flex;
  flex-direction: column;
  flex: 1;
}

scroll > p {
  background-color: #f0f0f0;
  border-radius: 12px;
  text-align: center;
  margin: 8px;
  padding: 20px;
}
```


``` js
export default {
  data: {
    index: 0,
    finalChanged: true
  }
}
```


</glyphix>



### `bounces` <decl type="'none' | 'start' | 'end' | 'edge'" get set />


Set whether to trigger rebound after scrolling `scroll` to the boundary through gestures. The initial value of this property is `edge`, which allows rebounding of the start and end positions.


| value | description |
| :-------: | -------------------------------------- |

| `'none'` | Disables all boundary bounce. |
| `'start'` | Only allows rebound after dragging to the starting position of the content. |
| `'end'` | Only allows rebound after dragging to the end of the content. |
| `'edge'` | Allows rebound after dragging to the start or end of the content. |


The following example shows the role of each `bounces` value. You can try sliding each item left or right beyond the boundary and observe the corresponding interaction behavior.


<glyphix id="components-scroll-bounces" height="360" width="400" title="拖拽回弹动画">


``` html
<scroll class="column-box">
  <scroll for="item in items" class="row-box"
          :bounces="item" scroll-snap="edge">
    <p class="item-body">bounces: {{item}}</p>
    <p class="slide-button">×</p>
  </scroll>
</scroll>
```


```js
export default {
  data: {
    items: ['none', 'start', 'end', 'edge']
  }
}
```


```css
.column-box {
  display: flex;
  flex-direction: column;
}

.row-box {
  display: flex;
  flex-direction: row;
}

.row-box > p {
  border-radius: 12px;
  text-align: center;
  margin: 8px;
  padding: 16px;
}

.item-body {
  background-color: #f0f0f0;
  width: 100%;
}

.slide-button {
  width: 30%;
  color: #ffffff;
  background-color: #f04040;
}
```


</glyphix>





::: note

Currently the `bounces` attribute only affects the rebound of gesture operations, but ignores the rebound of fast inertial animations. The example above uses a trick to avoid unexpected behavior:
- `.row-box` Use edge snapping strategy ( `snap-type="edge"` ) to avoid gesture animations with bounce.
- Each element of `.row-box` does not exceed the width of `100%`, ensuring that the edge snapping strategy does not cause internal boundary rebound.


This technique can be used for interfaces such as sliding delete menus.
:::



The `bounces` attribute will also play a similar role to [`weakGesture`](#weakgesture). Specifically, when the edge that prohibits rebounding is crossed, scroll gesture events are automatically allowed to bubble up and be delivered. Therefore, there is no need to set both the `bounces` and `weakGesture` attributes.


::: tip

The scroll gesture bubbling behavior of `bounces` and `weakGesture` is "opposite". For example, the `end` mode bounce policy allows the user to bounce back after scrolling past the end position of the list, and this policy allows the scroll gesture to bubble at the starting position. This corresponds to the effect of the `weakGesture` attribute with value `'start'`.
:::



### `weakGesture` <decl type="'none' | 'start' | 'end' | 'edge'" get set />


Set the circumstances under which the `scroll` component will bubble scroll gestures. By default `scroll` blocks bubbling of gestures it responds to, so its parent element cannot receive gestures that cause `scroll` to scroll. `weakGesture` allows bubbling of gesture events when dragging into content boundaries, allowing the parent element to receive these gestures.


| value | description |
| :-------: | ------------------------------------------------ |

| `'none'` | Do not bubble the corresponding gesture event. |
| `'start'` | Bubbles the corresponding gesture event after dragging to the starting position of the content. |
| `'end'` | Bubbles the corresponding gesture event after dragging to the end of the content. |
| `'edge'` | Bubbles the corresponding gesture event after dragging to the beginning or end of the content. |


If the underlying element of the page is a horizontal `scroll` component, but you want the right swipe gesture to return the page, you can configure it like this:
``` html
<scroll weak-gesture="start"> ... </scroll>
```
When the user slides to the head of the `scroll` component and continues to slide right to exit the page.


::: warning

This property should be set when the component is initialized and cannot be changed, otherwise interaction errors may occur.
:::



### `scrollbar` <decl type="boolean" get set />


Mark whether the `scroll` component should display scroll bars (not displayed by default). Only the `scroll` component with vertical layout is supported. The `scrollbar` attribute must be a constant and cannot be modified with reactive attributes, for example:
``` html
<scroll scrollbar>
  ...
</scroll>
```
A `scroll` component with a scrollbar will be created. For the effect of the scroll bar, please refer to the example of the [`setIndex`](#setindex) method.


The style of the scroll bar is determined by the system. For example, it may appear as an arc on a circular screen, or as a straight bar on a rectangular screen.


### `scrolled` <decl type="boolean" listen />


Monitor whether the list is in scrolling state through the `scrolled` attribute. An event-triggered attribute with a value of `true` means that the list is scrolling, otherwise it means that the list has stopped scrolling.


The scrolling operation caused by user touch and scrolling through the `scroll` attribute will trigger the `scrolled` event. When the list stops scrolling, the parameter value of the `scrolled` event is `false`.


### `setIndex`
<decl method><pre>

(options: {

  index: number,

  behavior?: 'instant' | 'smooth'

}): void

</pre></decl>



Moves the viewport to the child component specified by index. If this movement crosses the viewport boundary, the viewport position will stay at the first or last component. The function of `options` parameter attribute is:
- `index`: The index of the target subcomponent to be moved, $0$ represents the first subcomponent.
- `behavior`: Use animation transition when `'smooth'`, move to the specified sub-component position immediately when `'instant'` (default value).


When calling `setIndex()`, you must ensure that all elements of the `scroll` component are static, otherwise an error will occur.


<glyphix id="components-scroll-setindex" height="360" width="400" title="setIndex 方法">


``` html
<div class="window">
  <scroll id="scroll"
          :scroll-snap="center ? 'center' : null"
          scrollbar>
    <p for="x in 50" class="item">Item {{ x }}</p>
  </scroll>
  <div class="controls">
    <button on:click="setIndex('smooth')">smooth</button>
    <button on:click="setIndex('instant')">instant</button>
    center <switch ::value="center" />
  </div>
</div>
```


``` js
import prompt from '@system.prompt'

export default {
  data: { center: false },
  setIndex(behavior) {
    let el = this.$element('scroll')
    let index = parseInt(Math.random() * 50)
    prompt.showToast({message: `${behavior}ly set index to ${index}`})
    el.setIndex({ index: index, behavior: behavior })
  }
}
```


``` css
.window {
  display: flex;
  flex-direction: column;
}

scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
  flex: 1;
}

.item {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px 5px;
  border-radius: 16px;
  margin: 8px;
}

.controls {
  display: flex;
  align-items: center;
  color: #404040;
}

button {
  color: #fafafa;
  background-color: #adadad;
  border-radius: 12px;
  padding: 4px 10px;
  margin-left: 16px;
  margin-bottom: 16px;
  flex: 1;
  margin: 8px;
  padding: 8px;
  text-align: center;
}
```


</glyphix>



### `scrollTo`
<decl method><pre>

(options: {

  left?: number,

  top?: number,

  behavior?: 'instant' | 'smooth'

}): void

</pre></decl>



Scrolls the content to the specified position. The function of `options` parameter attribute is:
- `left`: Specifies the position where the content scrolls along the y-axis. If `left` is ignored or the scroll component has a vertical layout, scrolling on the y-axis will not occur.
- `top`: Specifies the position where the content scrolls along the x-axis. If `top` is ignored or the scroll component has a horizontal layout, scrolling on the x-axis will not occur.
- `behavior`: Specifies the transition effect of scrolling. `'instant'` (default value) means jumping directly to the target position without a transition effect, while `'smooth'` will scroll smoothly and produce a transition effect.


The `scrollTo` method ignores the adsorption effect of elements.


### `scrollBy`
<decl method><pre>

(options: {

  left?: number,

  top?: number,

  behavior?: 'instant' | 'smooth'

}): void

</pre></decl>



Scroll content a certain distance. Unlike [`scrollTo()`](#scrollTo), `scrollBy()` scrolls relative to the current content position. The function of `options` parameter attribute is:
- `left`: Specifies the distance for scrolling the content along the y-axis. If `left` is ignored or the scroll component has a vertical layout, scrolling on the y-axis will not occur.
- `top`: Specifies the distance for scrolling the content along the x-axis. If `top` is ignored or the scroll component has a horizontal layout, scrolling on the x-axis will not occur.
- `behavior`: Specifies the transition effect of scrolling. `'instant'` (default value) means jumping directly to the target position without a transition effect, while `'smooth'` will scroll smoothly and produce a transition effect.


The `scrollBy` method ignores the adsorption effect of elements.


## CSS specifications


### Layout direction control


The scrolling direction of the `scroll` component is determined by its layout method. When using fluid layout (default layout) or `column` direction flex layout, the elements are laid out in the vertical direction, and the list can be scrolled vertically; when using the `row` direction flex layout, the elements are laid out in the horizontal direction, and the list can be scrolled horizontally.


<glyphix id="components-scroll-layout" height="360" width="740" title="布局方式控制滚动方向">


``` html
<div>
  <scroll>
    <p for="20">vertical scroll</p>
  </scroll>
  <!-- 用于占位元素，因为 flex 布局现在还不支持 gap -->
  <div style="width: 20px"></div>
  <scroll style="display: flex; flex-direction: row;">
    <p for="20">horizontal<br>scroll</p>
  </scroll>
</div>
```


``` css
div {
  display: flex;
}

scroll {
  background-color: #f0f0f0;
  flex: 1;
}

p {
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px;
  margin: 4px;
  border-radius: 16px;
}
```


</glyphix>



### `padding` and `overflow` <version-badge since="0.9" />


By default ( `overflow: clip` ), the `scroll` component's padding directly clips the visible area. When content is scrolled, the padding area is always invisible. Setting `overflow: visible` allows the padding area to remain visible as the content scrolls.


<glyphix id="components-scroll-padding-overflow-visible" height="360" width="740" title="overflow: visible 的内边距">


``` html
<div>
  <scroll :index="2">
    <p for="20">overflow: clip</p>
  </scroll>
  <!-- 用于占位元素，因为 flex 布局现在还不支持 gap -->
  <div style="width: 20px"></div>
  <scroll style="overflow: visible;" :index="2">
    <p for="20">overflow: visible</p>
  </scroll>
</div>
```


``` css
div {
  display: flex;
}

scroll {
  padding: 20px;
  background-color: #f0f0f0;
  flex: 1;
}

p {
  background-color: #bdbdbd;
  text-align: center;
  padding: 20px;
  margin: 4px;
  border-radius: 16px;
}
```


</glyphix>



Even if `overflow: visible` is set, `scroll` will clip the content to the padding-box instead of allowing it to exceed that range, unlike regular elements like `div`. This is because the scrolling behavior and layout mechanism of `scroll` need to ensure that the content scrolls within a certain area, rather than allowing the content to expand unlimitedly to the outside area.


In a similar situation to `overflow: visible`, the content of ordinary containers such as `div` can exceed the scope of the entire `div` (such as outside the red `border`):


<glyphix id="components-scroll-overflow-div" height="360" width="360" title="div 的 overflow: visible">


``` html
<div style="overflow: visible;">
  <p for="20">div {overflow: visible}</p>
</div>
```


``` css
div {
  display: flex;
  flex-direction: column;
  padding: 20px;
  margin-bottom: 100px;
  border: 2px solid red;
  background-color: #f0f0f0;
}

p {
  background-color: #bdbdbd;
  text-align: center;
  padding: 8px;
  margin: 4px;
  border-radius: 16px;
  flex-shrink: 0;
}
```


</glyphix>



#### Recommended settings for i18n scenarios


In i18n (internationalization) scenarios, the text within `scroll` may need to be overflowed to avoid possible truncation. For this case, the recommended setting is `overflow: visible`, to allow the [文本溢出](/framework/application/i18n.md#文本溢出) content to exceed the content boundaries of `scroll` when scrolled, to maximize the use of space for text display.


#### Relationship to HTML/CSS specifications


The behavior of `scroll` when setting `overflow: visible` is similar to `div { overflow-y: scroll; }` in the HTML/CSS specification. The padding at this time can keep the content visible during scrolling, such as this CSS:


```css
div {
  padding: 20px;
  overflow-y: scroll;
}
```


The following effect will be obtained, that is, the padding area will not crop the content when scrolling:


<div style="padding: 20px; background-color: var(--vp-c-grey-bg); overflow-y: scroll; height: 100px; width: 200px; border: 2px dotted red; font-family: sans-serif;">

  Michaelmas term lately over, and the Lord Chancellor sitting in Lincoln's Inn Hall.

  Implacable November weather. As much mud in the streets as if the waters had but

  newly retired from the face of the earth.

</div>



HTML's `div` does not directly correspond to the behavior of `scroll` in `overflow: clip`.

============================================================
FILE_PATH: src/transl/EN/components/slider-arc.md

# slider-arc


The arc sliding selector defaults to a block-level element and does not support style modification.


## property


Inherit the properties of the [slider](slider) component


### `arc-center` <decl type="{ x: number, y: number }" set />


Set the position of the arc center.


### `start-angle` <decl type="number" set />


Set the arc starting angle, default value: $-90$.


### `progress-angle` <decl type="number" set />


Set the maximum rotation angle of the arc, default value: $360$, one circle of arc.


### `arc-width` <decl type="number" set />


Set arc width.


### `arc-radius` <decl type="number" set />


Set the arc radius.

============================================================
FILE_PATH: src/transl/EN/components/slider.md

# slider


Sliding selector, defaults to block-level elements.


## property


### `value` <decl type="number" get set listen />


Current value, default: $10$.


When setting the `value` attribute, the current value of the component will be changed. You can monitor changes in the current value through the `on` instruction, which will be triggered every time the current value changes.


### `min` <decl type="number" set />


Minimum value, default value: $0$.


### `max` <decl type="number" set />


Maximum value, default value: $100$.


### `vertical` <decl type="boolean" set />


If the value of the `vertical` attribute is `true`, the `slider` component will be displayed vertically, otherwise it will be displayed horizontally. The default value is `false`.


## CSS specifications


Developers can adjust the appearance of the `slider` component through CSS.


### Size calculation


The default width and height of `slider` are the same as the element's font size, which is set by the [`font-size`](/framework/generic/styles.md#font-size) attribute (can also be inherited). The size of `progress` can be customized through the [`width`](/framework/generic/styles.md#width) and [`height`](/framework/generic/styles.md#height) attributes.


### CSS properties


The following CSS properties may be useful:
- [`background-color`](/framework/generic/styles.md#background-color) can control the background color of `slider`;
- [`color`](/framework/generic/styles.md#color) can control the color of the progress bar of `slider`;
- [`border-radius`](/framework/generic/styles.md#border-radius) can set `slider` to a rounded border, for example `50%` will produce a semicircular border;


Other CSS properties may be useful, such as the [`border`](/framework/generic/styles.md#border) property to style the border.


### CSS pseudo-elements


#### `value`


This pseudo-element can define the `slider` progress bar alone without containing the style of the background part. For example, you can set the corner radius of the scroll bar background and the progress bar part separately to achieve the effect that the outer border has a circular line cap and the progress bar has a straight cap.


``` css
slider {
  border-radius: 50%; /* 滚动条背景圆角 */
}

slider::value {
  border-radius: 0; /* 滚动条的进度条没有圆角 */
}
```


#### `thumb` <experimental/>


The `thumb` pseudo-element is used to define the style of the `slider` slider. By default `slider` does not contain handles. To display handles you must specify the width and height of the `thumb` element:
``` css
slider::thumb {
  width: 150%;
  height: 150%;
  border-radius: 50%;
}
```
The percentage units of `width` and `height` are calculated relative to the size of the element itself. The horizontal `slider` slider width and height are calculated as a percentage based on the `height` of the element's CSS, while the vertical `slider` handle width and height are calculated as a percentage based on the `width` attribute of the element's CSS. For example, the element CSS is
``` css
slider {
  width: 200px;
  height: 24px;
}
```
At this time, the width and height of the slider corresponding to `slider::thumb` above are both $24\rm{px} \times 150\% = 36\rm{px}$. The handle's fillet radius percentage size is calculated based on the handle's own size. In this example, the calculated value of the `50%` pseudo-element fillet radius of `thumb` is $36\rm{px} \times 50\%=18\rm{px}$.


The `thumb` pseudo-element supports the `border` CSS property, but the border will not exceed the dimensions of the `thumb` pseudo-element.


### CSS example


The following example demonstrates some ways to customize the appearance of the progress bar through CSS.
<glyphix id="components-slider-styles" height="180" width="480" title="Slider 样式">


``` html
<div>
  <!-- 默认样式 -->
  <slider ::value="value" />
  <!-- 直头进度条样式 -->
  <slider class="flat" ::value="value" />
  <slider class="more-style" ::value="value" />
  <p>value: {{value}}</p>
</div>
```


``` css
div > * {
  margin: 8px;
  padding: 6px;
}

.flat::value {
  /* value 伪元素的圆角半径设置为 0 即可实现进度条直头效果 */
  border-radius: 0;
}

.more-style {
  /* 自定义圆角半径 */
  border-radius: 30%;
  /* slider 背景色 */
  background-color: #b3c5d7;
  /* slider 前景颜色 */
  color: #b5179e;
  /* padding 可以调整 slider 前景的边距 */
  padding: 6px;
  height: 1rem;
}

/* 定义滚动条滑块样式 */
.more-style::thumb {
  width: 300%; /* 宽高比 2:1 的胶囊形滑块 */
  height: 150%;
  background-color: white;
  border: 4px solid #f3722c; /* 滑块边框 */
  border-radius: 50%;
}
```


``` js
export default {
  data: { value: 50 }
}
```


</glyphix>


============================================================
FILE_PATH: src/transl/EN/components/span.md

# span


`span` is also a text component. Unlike [`p` 组件](p), `span` components are inline elements by default and can span lines. [`label` ](label) components and [`a`](a) components also have similar effects. Text spanning means that elements can be laid out across multiple lines instead of occupying an entire "box".


The `span` component can be used to implement [富文本排版](/framework/render/rich-text.md#富文本显示).


<glyphix id="span" :height="36">



``` html
<div>
  Hello Glyphix, this is <span style="color: #f0f">span</span> label!
</div>
```


</glyphix>


============================================================
FILE_PATH: src/transl/EN/components/stack.md

# stack


`stack` stacked layout components. In the stacked layout, the size and position of each subcomponent are the same as the `stack` component, and they are stacked and displayed in order. The following example shows two overlapping text elements within a `stack` component.


<glyphix id="components-stack-layout" height="100" width="200" title="堆叠布局">


``` html
<stack>
  <p class="text1">Text 1</p>
  <p class="text2">Text 2</p>
</stack>
```


``` css
* {
  text-align: center;
}

.text1 {
  font-size: 64px;
  color: #fff;
}

.text2 {
  font-size: 48px;
  color: #f008;
}

stack {
  background-color: gray;
}
```


</glyphix>



::: tip

The `stack` component always uses the stacked display layout strategy and cannot be changed to other layouts (such as flex layout or fluid layout) through CSS properties such as `display`.
:::



## layout behavior


`stack` components have a fixed stacking layout strategy. Its size is determined by two constraints:
1. The dimensions of `stack` are first specified by size CSS properties such as [`width`](../framework/generic/styles.md#width) or [`height`](../framework/generic/styles.md#width);
2. The layout of the parent element may directly determine the layout of `stack`, such as `align-items: stretch`, `flex: 1` and other attributes in flex layout;
3. Otherwise the size of the `stack` component is determined by the maximum width and maximum height of the child elements.


Once the size of `stack` is determined, all its child elements will have the same outer box size (that is, the size of the child element plus `border` and `margin`). This sometimes causes trouble, for example, if an image is used as the background through `stack`, and the size of the upper element is too large, the image may not fit.

============================================================
FILE_PATH: src/transl/EN/components/swiper.md

# swiper


Card view container, supporting any sub-component. The scrolling direction of the card view is specified by the specific layout method: the list using `flex-column` layout is vertical, while the list using `flex-row` layout is horizontal.


## property


### `scroll` <decl type="{ scrollX: number, scrollY: number, scrollState: number }" get listen />


The `scroll` attribute value is an object containing the following fields: `scrollX`, `scrollY`, and `scrollState`. The `scrollX` and `scrollY` attributes represent the horizontal and vertical scrolling positions respectively, in pixels; the `scrollState` attribute represents the scrolling state, and its value is $0$, $1$ or $2$. The specific meaning is as shown in the following table. Changes to the `scroll` attribute can be monitored through the `on` directive. Any change in content location caused by user operations and API operations will trigger monitoring.


| `scrollState` value | Effect description |
| :--------------: | ------------------------------------------------------------------- |

| $0$ | Stopped sliding |
| $1$ | Swiping via user's gesture |
| $2$ | The user has let go, sliding caused by method calls such as [`scrollTo`](#scrollto) or inertia |


### `scrollTop` <decl type="number" get listen />


The vertical scroll position, that is, the distance from the top of the content of the `swiper` component to the top of the viewport, in pixels. Changes in the scroll position can be monitored through this property. Unlike the [`scroll`](#scroll) attribute, the listener `scrollTop` attribute itself cannot distinguish between scrolling by the user's gestures and scrolling caused by API calls or inertia.


### `scrollLeft` <decl type="number" get listen />


The scroll position in the horizontal direction, that is, the distance from the left side of the content of the `swiper` component to the left side of the viewport, in pixels. You can use this property to monitor changes in the scroll position. Unlike the [`scroll`](#scroll) attribute, the listener `scrollLeft` attribute itself cannot distinguish between scrolling by the user's gestures and scrolling caused by API calls or inertia.


### `scrollWidth` <decl type="number" get listen />


`swiper` The width of the component's content area. The width of `swiper` in vertical layout is equal to the view width, while the width of `swiper` in horizontal layout is the sum of the widths of all elements. You can use this to monitor content width changes.


### `scrollHeight` <decl type="number" get listen />


`swiper` The height of the component's content area. The height of `swiper` in vertical layout is equal to the view height, while the height of `swiper` in horizontal layout is the sum of the heights of all elements. You can use this to monitor content height changes.


### `snapshot` <decl type="boolean" get set />


When the `snapshot` attribute is enabled, the subcomponents of `swiper` will enable snapshot mode. Please refer to the [`snapshot`](scroll.md#snapshot) attribute of the `scroll` component.


### `deformation` <decl type="string" set />


Set the deformation effect of the sub-element, and use the deformation effect to achieve fish-eye and other appearances. A built-in morph effect can be specified by name (a string), or a morph effect can be defined through a JavaScript function.


| Value | Effect Description |
| :-: | :- |

| `'none'` | No deformation effect (default). |
| `'fade'` | Fade zoom switching effect, this effect highlights the "focus" of elements within the current viewport and makes elements outside the viewport appear to take a back seat. See the effects of the examples in this section for details. |
| `'fisheye'` | Built-in fisheye effect, this attribute component is used for [`scroll`](scroll.md) component instead of `swiper`. |
| function | Specify the deformation effect through JavaScript function. |


The deformation effect should be constant and not modified.


If the content of `swiper`'s child elements changes frequently, it is recommended to add the [`quiescent`](/framework/generic/properties.md#quiescent) attribute to the element when using the transformation effect to avoid updating when switching and improve performance. You can refer to the following examples:


<glyphix id="components-swiper-deformation" height="360" width="360" title="元素形变效果">


```html
<swiper deformation="fade" indicator>
  <div for="x in 5" :quiescent="x != 0">
    <progress-arc busy :start-angle="0" :stop-angle="360" />
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```


``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

progress-arc {
  width: 30%;
  height: 30%;
  margin-bottom: 5%;
}
```


</glyphix>



The first child element in the example does not have the `quiescent` attribute turned on, so it will continue to update during the switching process, while other elements will stop updating.


### `vertical` <decl type="boolean" set />


Set whether the `swiper` component is vertically laid out. When the default is `false`, horizontal layout will be used. The following example demonstrates the `swiper` interaction effect under vertical layout (note that vertical scrolling is required, horizontal sliding is unresponsive).


<glyphix id="components-swiper-vertical" height="360" width="360" title="垂直布局">


``` html
<swiper vertical deformation="fade" indicator>
  <p for="x in 5">
    pane {{ x + 1 }}
    {{ x == 0 ? '(swipe up)' : x == 4 ? '(swipe down)' : '' }}
  </p>
</swiper>
```


``` css
p {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
}
```


</glyphix>



### `indicator` <decl type="boolean" get set />


Set whether the `swiper` component displays the point indicator. The display position of the point indicator is determined by the `vertical` attribute: the point indicator displays in the middle of the right side when the layout is vertical, and the point indicator displays in the middle of the bottom when the layout is horizontal. Please refer to the examples of [`deformation`](#deformation) and [`vertical`](#vertical) attributes for specific effects.


See [点指示器 CSS 属性](#点指示器-css-属性) to learn how to customize the display style of point indicators.


### `pageLength`  <decl type="number" set />


Set the size or proportion of the subpage. When it is a percentage, set the size of the subcomponent in the sliding direction (relative to the component itself); when it is other numbers, set the size of the subcomponent in the sliding direction.


### `index`  <decl type="number" get set listen />


The index of the currently displayed subcomponent. When the `index` attribute is set, the component will scroll to the specified subcomponent through animation. Position changes can be monitored through the `on` directive, and changes in subcomponent index can be monitored through the `index` attribute.


### `finalChanged` <decl type="bool" get set />


Set whether the [`index`](#index) change event is only triggered when scrolling stops. By default (that is, `finalChanged` is `false`), whenever the scroll gesture or other reasons cause the `index` attribute of the `swiper` component to change, its listening event will be triggered. However, doing so can easily cause animation frames to drop, or trigger too frequent and unnecessary events. When `finalChanged` is set, the `index` changed event will only be triggered when scrolling stops.


::: tip

When implementing effects such as point indicators by monitoring the `index` attribute, it is recommended to set `finalChanged` to `true`. This can avoid frame drops caused by event-triggered rendering updates during the sliding process.
:::



### `weakGesture` <decl type="'none' | 'start' | 'end' | 'edge'" get set />


Set the circumstances under which the `swiper` component will bubble scroll gestures. By default `swiper` blocks bubbling of gestures it responds to, so its parent element cannot receive gestures that cause `swiper` to scroll. `weakGesture` allows bubbling of gesture events when dragging into content boundaries, allowing the parent element to receive these gestures.


| value | description |
| :-------: | ------------------------------------------------ |

| `'none'` | Do not bubble the corresponding gesture event. |
| `'start'` | Bubbles the corresponding gesture event after dragging to the starting position of the content. |
| `'end'` | Bubbles the corresponding gesture event after dragging to the end of the content. |
| `'edge'` | Bubbles the corresponding gesture event after dragging to the beginning or end of the content. |


If the underlying element of the page is a horizontal `swiper` component, but you want the right swipe gesture to return the page, you can configure it like this:
``` html
<swiper weak-gesture="start"> ... </swiper>
```
When the user slides to the head of the `swiper` component and continues to slide right to exit the page.


### `bounces` <decl type="'none' | 'start' | 'end' | 'edge'" get set />


Set whether to trigger rebound after scrolling `swiper` to the boundary through gestures. The initial value of this property is `edge`, which allows rebounding of the start and end positions. The `bounces` attribute of `swiper` is similar to the [`bounces`](scroll.md#bounces) attribute of the [`scroll`](scroll.md) component. Please refer to the relevant documentation for more instructions.


### `scrolled` <decl type="boolean" listen />


Monitor whether the `swiper` component is in a scrolling state through the `scrolled` attribute. The attribute value triggered by the event is `true`, which means scrolling, otherwise it means that scrolling has stopped.


The scrolling operation caused by user touch and scrolling through the `scroll` attribute will trigger the `scrolled` event. When stopping from a scrolling state, the parameter value of the `scrolled` event is `false`.


### `setIndex`
<decl method><pre>

(options: {

  index: number,

  behavior?: 'instant' | 'smooth'

}): void

</pre></decl>



Moves the viewport to the child component specified by index. If this movement crosses the viewport boundary, the viewport position will stay at the first or last component. The function of `options` parameter attribute is:
- `index`: The index of the target subcomponent to be moved, $0$ represents the first subcomponent.
- `behavior`: Use animation transition when `'smooth'`, move to the specified sub-component position immediately when `'instant'` (default value).


### `scrollTo` <decl type="(position: number): void" method />


Scroll the content to the specified position. The scrolling direction is consistent with the layout direction of the scroll component.


The `scrollTo` method ignores the adsorption effect of elements.


## CSS specifications


### Point indicator CSS property


This section introduces the CSS properties available after the `swiper` component turns on the [`indicator`](#indicator) attribute. They are used to control part of the display style of the point indicator. `swiper`'s point indicator always appears as a set of dots arranged horizontally or vertically, and can only be customized by the developer.


#### `indicator-color`


Defines the color of the unselected point indicator. The effect is as follows:


<glyphix id="components-swiper-indicator-color" height="360" width="360" title="点指示器颜色">


```html
<swiper indicator>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```


``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-color: #333;
  indicator-selected-color: #ff60ff;
  indicator-bottom: 16px;
}
```


</glyphix>



#### `indicator-selected-color`


Defines the color of the selected point indicator. You can refer to the example of the [`indicator-color`](#indicator-color) attribute for the effect. You can observe that the point indicator corresponding to the selected page displays the color defined by the CSS attribute.


#### `indicator-size`


Defines the size of each indicator point in the point indicator, in pixels. The default value is `10px`. The following example demonstrates the effect of setting the point indicator size to `16px`:


<glyphix id="components-swiper-indicator-size" height="360" width="360" title="点指示器大小">


```html
<swiper indicator>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```


``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-color: #333;
  indicator-selected-color: #ff60ff;
  indicator-bottom: 24px;
  indicator-size: 16px;
}
```


</glyphix>



#### `indicator-top`


When `swiper` has [水平布局](#vertical), use the `indicator-top` attribute to specify the distance of the point indicator from the top. By default, the point indicator will be displayed at the bottom center, this property can be used to display it at the top:


<glyphix id="components-swiper-indicator-top" height="360" width="360" title="顶部点指示器">


```html
<swiper indicator>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```


``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-top: 16px;
}
```


</glyphix>



::: warning

Do not set `indicator-left`, `indicator-top`, `indicator-right` and `indicator-bottom` at the same time, otherwise the point indicator position will be unpredictable.
:::



#### `indicator-left`


When `swiper` has [垂直布局](#vertical), use the `indicator-left` attribute to specify the distance of the point indicator from the left. By default, the point indicator will be displayed in the middle position on the right, this property can display it on the left:


<glyphix id="components-swiper-indicator-left" height="360" width="360" title="左侧点指示器">


```html
<swiper indicator vertical>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```


``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-left: 16px;
}
```


</glyphix>



#### `indicator-right`


When `swiper` has [垂直布局](#vertical), use the `indicator-right` attribute to specify the distance of the point indicator from the right. The effect is as follows:


<glyphix id="components-swiper-indicator-right" height="360" width="360" title="右侧点指示器">


```html
<swiper indicator vertical>
  <div for="x in 5">
    <p>pane {{ x + 1 }}</p>
  </div>
</swiper>
```


``` css
div {
  background-color: #eee;
  text-align: center;
  margin: 10px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

swiper {
  indicator-right: 32px;
}
```


</glyphix>



#### `indicator-bottom`


When `swiper` has [水平布局](#vertical), use the `indicator-bottom` attribute to specify the distance of the point indicator from the bottom. The effect can be seen in the examples of the [`indicator-color`](#indicator-color) and [`indicator-size`](#indicator-size) attributes.


### `padding` and `overflow` <version-badge since="0.9" />


See the description of [scroll 组件](scroll.md#padding-和-overflow). The `padding` and `overflow` attributes of the `swiper` component have the same behavior specifications as the attributes of the same name of the `scroll` component. For more instructions, please refer to the relevant documentation.

============================================================
FILE_PATH: src/transl/EN/components/switch.md

# switch


Switch selects components, defaulting to inline elements. Used to represent on/off status and allow the user to switch between the two statuses. The function of `switch` is similar to that of `checkbox`, but the interaction effects and intentions are different, that is, they express switches and checks respectively.


<glyphix id="components-switch" height="30">



``` html
<div>
  <switch ::value="enabled" />
  <span>switch state: {{ enabled ? 'on' : 'off' }}</span>
</div>
```


``` js
export default {
  data: {
    enabled: false
  }
}
```
</glyphix>



::: note

The `switch` component is typically styled as shown in the example, but may vary depending on the device. In particular, it should be noted that the width of `switch` may be different on different devices, and developers should reserve appropriate layout margin.
:::



## property


### `value` <decl type="boolean" set get listen/>


Indicates the status of `switch`. When the value is `true`, `switch` is in the on state, otherwise it is in the off state. When the `value` attribute is not specified, the `switch` component is turned off by default.


### `checked` <decl type="boolean" set get/>


This is a Quick App compatibility attribute, and it is usually more recommended to use [`value`](#value)


### `change` <decl type="{ checked: boolean }" get listen/>


This is a Quick App compatibility attribute, and it is usually more recommended to use [`value`](#value)


## CSS behavior


The overall style of the `switch` component is determined by the system and is not controlled by the developer, just like the style differences between [Fluent 2](https://fluent2.microsoft.design/components/web/react/switch/usage) and [Material 3](https://m3.material.io/components/switch/overview). Glyphix allows the color of `switch` to be customized in CSS, and the size of `switch` to be resizable.


### CSS properties


#### `color`


Set the slider color of the `switch` component. Unlike the general CSS [`color`](/framework/generic/styles.md#color), the `color` attribute of `switch` does not support inheritance, so you must define it on the current `switch` component.


<glyphix id="components-switch-color" height="36" title="siwtch 滑块颜色">


``` html
<div>
  red color: <switch class="red"/>,
  not inherited: <switch/>
</div>
```


``` css
div {
  color: red; /* 注意 switch 不会继承 color 属性 */
}

.red {
  color: red; /* 必须在 switch 组件的样式上定义 color */
}
```
</glyphix>



#### `background-color`


Controls the background color of the `switch` component, see the documentation of the [`active`](#active) pseudo-class for details.


#### `font-size`


You can adjust the size of `switch` through the [`font-size`](/framework/generic/styles.md#font-size) CSS property to match the inline text size. The following example demonstrates the relationship between `font-size` and `switch` sizes:


<glyphix id="components-switch-size" height="100" title="font-size 与 siwtch 大小">


``` html
<div>
  <p class="title">
    title text: <switch/> (1.25rem)
  </p>
  <p>
    content text: <switch/> (1rem)
  </p>
</div>
```


``` css
div {
  line-height: 1.8rem;
}

.title {
  color: #415a77; /* 注意 switch 不会继承 color 属性 */
  font-size: 1.25rem;
}
```
</glyphix>



::: warning

The display size of `switch` is not controlled by attributes such as `width` and `height`, but is always determined by `font-size`. Therefore, please do not manually specify size attributes such as `width` to avoid abnormal display.
:::



### CSS pseudo-class


#### `active`


The `active` pseudo-class is used to define the style in which `switch` is turned on. As shown in the following example, it is usually configured along with regular style rules:


<glyphix id="components-switch-colors" height="36" title="siwtch 滑块颜色设置">


``` html
<div>
  color switch: <switch/>
</div>
```


``` css
/* switch 关闭状态下的样式 */
switch {
  color: #415a77;
  background-color: #bde0fe;
}

/* switch 打开状态下的样式 */
switch:active {
  color: #fefae0;
  background-color: #ffafcc;
}
```
</glyphix>



This example uses the `color` and `background-color` CSS properties to control the color style when switching `switch`. The `switch` component will only respond to the configuration of these two CSS properties when the `active` pseudo-class is activated.


::: tip

Please define the `color` and `background-color` attributes in the normal state and `active` state at the same time, otherwise there will be no corresponding color change when `switch` is switched.
:::


============================================================
FILE_PATH: src/transl/EN/components/text-field.md

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

============================================================
FILE_PATH: src/transl/EN/components/text.md

# text


Text components, `text` components and [`p` 组件](p) are identical except for the component name.

============================================================
FILE_PATH: src/transl/EN/components/textarea.md

# textarea


`textarea` <experimental/> <version-badge since="0.9" /> is a multi-line text input component that is displayed as a block-level element by default. Unlike similar GUI elements on mobile phones or PCs, `textarea` currently does not respond to input devices such as keyboards, nor does it pop up the input method interface, so you must manually edit its content. `textarea` supports operating the cursor through touch gestures (such as clicking and scrolling), and provides methods to move the cursor up, down, left, and right.


`textarea` is suitable as a low-level component for multi-line text input, and can implement soft keyboard and cursor control according to your needs. For details, please refer to [示例](#基本示例).


::: important compatibility
`textarea` is an experimental extension component that is currently only available in Glyphix 0.9 and above, and is only supported by some devices.
:::



## property


### `text` <decl type="string" get set listen />


The `text` attribute is a string that is the currently edited text content of `textarea`. Reading or listening to this value can obtain the input text, and you can also set this property.


Usually `text` is bidirectionally bound to a specific responsive attribute, or the text can be set through the content inside the element, such as:


```html
<textarea ::text="inputText" />
```


or


```html
<textarea @text="onTextChanged">{{ inputText }}</textarea>
```


:::tip

The `text` attribute of `textarea` functions similarly to the [`value`](text-field.md#value) attribute of [`text-field`](text-field.md).
:::



### `placeholder` <decl type="string" set get />


When the content of `textarea` is empty, `placeholder` can be used to provide a brief prompt to the user, such as a phrase such as "Please enter text."


`placeholder` is automatically displayed when the input text is empty, so usually only a fixed content is needed, such as:


```html
<textarea ::text="inputText" placeholder="type here" />
```


### `insert` <decl type="(text: string): void" method />


Insert a piece of text with the content `text` at the cursor, and the cursor will automatically move after the inserted text. Calling this function will trigger the `text` listening event.


### `backspace` <decl type="(): void" method />


Delete the character at the cursor and the cursor will automatically move forward. Calling this function will trigger the `text` listening event.


### `moveCaret` <decl type="(direction: 'up' | 'down' | 'left' | 'right'): void" method />


Moves the cursor one position in the specified direction. The optional values ​​​​of the `direction` parameter are `'up'`, `'down'`, `'left'`, and `'right'`, which correspond to the four directions of up, down, left, and right respectively.


## Instructions for use


### basic example


The following example shows basic usage of `textarea`. Users can directly enter multiple lines of text in the text box, or use the virtual keyboard below to edit content: click the letter/symbol key to insert characters; the "`×`" key to delete the content at the cursor; the "`Aa`" key to switch to uppercase and lowercase; the "`1#`" key to switch to the symbol keyboard; the "`Enter`" key to insert a newline character; the arrow keys to move the cursor.


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



We first obtain the `textarea` component object through the `$element` method in the component's `onReady()` life cycle function, because then we need to use the [`insert()`](#insert), [`backspace`](#backspace) and [`moveCaret`](#movecaret) methods to edit content and move the cursor.


On this basis, we can call the `textarea` method in the touch event listener of the `button` component, for example:


```html
<button on:touchstart="ta.insert('A')">A</button>
```


Since there is no physical keyboard, developers usually need to provide a custom keyboard implementation. This example implements a complete QWERTY keyboard layout, supporting uppercase and lowercase switching and a symbol keyboard. Call the corresponding method in the touch event listening function of each key to edit the text. The arrow keys move the cursor (up, down, left, and right) through the [`moveCaret()`](#movecaret) method, and the line feed key inserts a newline character `\n` through [`insert()`](#insert).


### The difference between text-field and text-field


`textarea` and `text-field` are both text input components. The main differences are as follows:


| Features | `textarea` | `text-field` |
|------|-----------|-------------|

| Number of lines of text | Single or multiple lines | Single line |
| Line feed support | Support `\n` line feed | Line feed not supported |
| Cursor movement | Up and down movement | Left and right movement |
| Content attributes | `text` | `value` |
| Password mode | Not supported | Supported `password` attribute |
| Default display | Block-level elements | Inline elements |

