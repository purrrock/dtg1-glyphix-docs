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