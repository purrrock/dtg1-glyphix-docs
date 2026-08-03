# button

The button component is an inline element by default and can trigger corresponding events when touched.

## Properties

### `checkable`  <decl type="boolean" set />

When set to `true`, it means a single touch only responds to one state change, i.e., transitioning from the pressed state to the released state, or from the released state to the pressed state. Additionally, the listening value for the `press` state is `true` when pressed and `false` when released.

### `toggleable` <decl type="boolean" set />

When set to `true`, it indicates that the `press` listening value can be changed, with `true` for pressed and `false` for released.

### `press` <decl type="boolean" get set listen />

When setting the `press` property, the state of the component can be changed. You can also listen to the component's state using the `on` directive. By default, upon completing a touch, the callback parameter is `true`. You can use it with the `checkable` and `toggleable` properties to get different listening values and states.

## Limitations

### `click` Event Invalidation

When not using the `button` component, you typically listen for click events on any native component via the [`click`](/framework/generic/properties.md#click) property. However, this method generally does not work for `button`. For example, consider the following code:
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
    // Prevent event bubbling to avoid the outer button responding to the click event
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

You might expect that clicking the `"inner"` text would trigger the `onInnerClick` method and prevent `onOuterClick`. However, you will find that this is not the case (it is best to open the browser console to view the logs): the `onInnerClick` method is not triggered at all, and only the outer `button` component responds to the click, meaning:
- When clicking the `inner` text, the `inner click` log does not appear, only the `outer click` log;
- The interaction for when the `button` is pressed is triggered (opacity is reduced).

This is just like clicking the outer `outer text`. The reason for this behavior is that the `button` component takes priority in responding to the entire lifecycle of the press gesture (from pressing down to releasing), while the `click` event is triggered upon release. This means that regardless of whether the inner element's `click` event handler stops propagation or not, this behavior cannot be changed.

#### Solution

To resolve this issue, you should listen to the `press` event of the outer `button` and the `touchstart` event of the inner element:

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
    // Prevent event bubbling to avoid the outer button responding to the click event
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

Try the example above, and you will find that clicking the `inner` text only triggers the `onInnerClick` method, `onOuterClick` will not be triggered, and the `button` will not render the pressed state effect.

::: tip
The `press` event is also typically triggered upon release, but it requires that the button's press event has never been prevented. Therefore, stopping the propagation of the inner element's `touchstart` event can prevent the outer button's `press` event from being triggered.
:::

#### Alternative Trigger Timing

The limitation of this method is that the inner element's `touchstart` event is triggered upon pressing down. You can alternatively use the `touchend` event to trigger the action, but you must retain the propagation-stopping functionality of the `touchstart` event. This ensures that the outer button's `press` event is not triggered when pressing down.

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
    // No need to stop propagation here, as it was already stopped in touchstart
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

Open the browser console and click the `inner` text again. You will find that the `onInnerClick` log is only printed upon release, and it still successfully prevents the outer `button` from responding to the gesture.