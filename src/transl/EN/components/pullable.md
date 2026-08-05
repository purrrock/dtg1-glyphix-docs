# pullable

The `pullable` component is used within a scrolling list to add incremental loading or refresh interaction triggered by pulling down at the top or pulling up at the bottom. The `pullable` component is a block-level element by default.

::: warning
<experimental /> This is an experimental component. The functionality of `pullable` is not yet stable, and the animation effects may not feel entirely natural.
:::

`pullable` should be the first or the last child component of [`scroll`](scroll.md). When it is the first child component, continuing to pull down at the top of the `scroll` content will trigger the `pulling` event; conversely, when `pullable` is the last child component of `scroll`, pulling up at the bottom will trigger the `pulling` event.

The `pullable` component is hidden by default and is only displayed when being pulled up/down. The following example demonstrates how to use the `pullable` component.

<glyphix id="components-pullable-1" height="360" width="360" title="Pull Down/Up to Load More">

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

For detailed usage, please refer to [Instructions](#instructions).

## Attributes

### `hold` <decl type="bool" get set />

By default, `pullable` is only visible when pulling down at the top or pulling up at the bottom. However, when the `hold` attribute is set to `true`, the `pullable` component will remain visible. This attribute is typically set when the [`pulling`](#pulling) event triggers a content update, and is cleared once the content update is complete.

### `pulling` <decl type="bool" get listen />

The `pulling` event is triggered when `pullable` is fully pulled out. The meanings of its event values are:
- `true`: Triggered when pulling down/up reaches the distance required to fully pull out the `pullable` component.
- `false`: Triggered when the user releases their hand after the above full pull-out condition has been met.

The following example shows when the `pulling` event values are triggered. You can try slowly pulling down from the top of the list and observe the toast popup message when the `pulling` event is triggered.

<glyphix id="components-pullable-pulling" height="360" width="360" title="pulling Event">

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

## Instructions

### Component Positioning

The `pullable` component must be the first or last child element of a vertical `scroll`. It automatically determines its operation mode based on its position: when it is the first child element, it detects the user pulling down from the top of the list, and vice versa.

For a list that only requires pull-down to refresh, the following usage is sufficient:
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

In the JavaScript code, you can listen to the `pulling` event and control the `refresh` attribute:
``` js
export default {
  data: {
    refresh: false
  },
  onPulling(hold) {
    if (!hold) { // hold is false when the user releases their hand
      this.refresh = true // Indicates that a refresh is in progress
      // This example uses a timer to simulate a loading operation and stops loading after 1s
      setTimeout(() => this.refresh = false, 1000)
    }
  }
}
```

For the specific visual effect, please refer to the example in the [`pulling`](#pulling) event documentation.

### Prompt Content Control

The `pullable` component can contain various components inside to display prompt content. As shown in the earlier example in this document, you can combine a loading animation with prompt text. In addition, the value of the `pulling` event can be used to control the prompt content. The following state handling approach is generally recommended:
1. Set a reactive property (such as `refresh`) for each `pullable` component with a default value of `null`. The `refresh` property is also used to control the [`hold`](#hold) property of `pullable`.
2. In the initial state (i.e., when `refresh` is falsy), the prompt content of `pullable` should remind the user to "keep pulling to update".
3. When the user pulls down, the `pulling` event is triggered. Proceed to step 4 or 5 based on its event value.
4. When `pulling` is `true`, it should prompt the user to "release to start refreshing".
5. When `pulling` is `false`, it indicates that the user has released their hand. At this point, `refresh` should be set to `true`, the content update should begin, and the user should be prompted that it is "updating".
6. Once the content refresh is complete, reset `refresh` to `false` to return to the initial state.

You can also refer to the first example in this document, which implements both pull-down at the head and pull-up at the tail of the list for continuous loading. That example uses a trick to control all states of `pullable` using just a single reactive property.

This trick sets the initial value of the `refresh` reactive property to `null` (similar to `false`) and uses template code like this:
``` html
<pullable :hold="refresh" on:pulling="onPulling">
  <p>{{refresh || 'Keep pulling down'}}</p>
</pullable>
```
When `refresh` is not set, once `pullable` is pulled out, it will display the default "Keep pulling down" prompt content. Then, the `onPulling` event callback function should be written as follows:
``` js
export default {
  async onPulling(event) {
    this.refresh = event ? 'Please release' : 'Updating'
    if (!event) { // Trigger the refresh operation upon release
        await runRefreshJobs()
        this.refresh = null // Reset the state after refresh is complete
    }
  }
}
```

### Limitations

Currently, there are some limitations to the `pullable` component. In addition to having to be used within a vertical `scroll` component, you also need to ensure that the number of list items exceeds the size of the `scroll` viewport, otherwise issues may occur. Furthermore, the interaction effects of `pullable` may feel somewhat rigid.