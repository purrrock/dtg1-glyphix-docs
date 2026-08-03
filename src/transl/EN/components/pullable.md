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