# pullable

`pullable` 组件用于在滚动列表内添加在顶部下拉和底部上拉时触发增量加载或者刷新交互的功能。`pullable` 组件默认是块级元素。

::: warning
<experimental /> 这是一个实验性组件，`pullable` 的功能并不稳定，并且动效可能不够自然。
:::

`pullable` 应该是 [`scroll`](scroll.md) 的第一个或者最后一个子组件。当它是第一个子组件时，在 `scroll` 内容的头部继续下拉将会触发 `pulling` 事件；相反，当 `pullable` 是 `scroll` 的最后一个子组件时，在底部上拉会触发 `pulling` 事件。

`pullable` 组件默认处于隐藏状态，只在被上/下拉的时候才会显示。下面的例子演示了 `pullable` 组件的使用方法。

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

详细的用法请参考[使用说明](#使用说明)。

## 属性

### `hold` <decl type="bool" get set />

默认情况下，`pullable` 仅仅在顶部下拉或底部上拉时可见，但是当 `hold` 属性为 `true` 时，`pullable` 组件将保持显示状态。该属性通常在 [`pulling`](#pulling) 事件导致了内容更新时设置，并在内容更新完成后取消。

### `pulling` <decl type="bool" get listen />

当 `pullable` 在完全被拉出时会触发 `pulling` 事件，其事件值的含义为：
- `true`：在下拉/上拉达到 `pullable` 的完全拉出触发距离时触发此事件；
- `false`：在达到上述完全拉出条件后，用户松手时触发此事件。

下面的示例展示了 `pulling` 事件值的触发时机。你可以尝试缓慢地从列表顶部下拉，并注意触发 `pulling` 事件时的 toast 弹窗信息。

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

## 使用说明

### 组件位置

`pullable` 组件必须是垂直 `scroll` 的第一个或者最后一个子元素。它会根据位置自动决定操作模式：当是第一个子元素是检测用户从列表顶部下拉的操作，反之亦然。

对于只需要下拉刷新的列表来说，以下用法就可以了：
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

JavaScript 代码中可以监听 `pulling` 事件，并控制 `refresh` 属性：
``` js
export default {
  data: {
    refresh: false
  },
  onPulling(hold) {
    if (!hold) { // 用户松手时 hold 为 false
      this.refresh = true // 表示正在刷新
      // 本示例中用一个定时器模拟加载操作，并在 1s 后停止加载
      setTimeout(() => this.refresh = false, 1000)
    }
  }
}
```

具体的效果请参考 [`pulling`](#pulling) 事件文档的示例。

### 提示内容控制

`pullable` 组件内部可以容纳各种组件来显示提示内容。如本文当前面的示例那样，你可以将加载动画和提示文本结合起来。此外，`pulling` 事件的值可以用于控制提示内容，通常建议使用这样的状态处理方式：
1. 为每个 `pullable` 组件设置一个响应式属性（例如 `refresh`），默认值为 `null`，`refresh` 属性还用于控制 `pullable` 的 [`hold`](#hold) 属性。
2. 处于初始状态时（即 `refresh` 为假），`pullable` 的提示内容应该提醒用户“继续拉拽以进行更新”。
3. 当用户下拉时，会触发 `pulling` 事件，根据其事件值采取 4 或 5 步骤。
4. `pulling` 为 `true` 时，应该提示用户“松手以开始刷新”。
5. `pulling` 为 `false` 时表示用户已经松手，此时应该将 `refresh` 置为 `true` 并开始刷新内容。并应该提醒用户“正在刷新中”。
6. 内容刷新完成后，重新将 `refresh` 置为 `false`，回到初始状态。

你也可以参考本文档的第一个示例，它同时实现了在列表头部下拉和尾部上拉的继续加载功能。该示例使用了一个技巧，仅使用一个响应式属性来控制 `pullable` 的所有状态。

该技巧将 `refresh` 响应式属性的初始值设置为 `null`（类似于 `false`），并使用这样的模板代码：
``` html
<pullable :hold="refresh" on:pulling="onPulling">
  <p>{{refresh || '继续下拉'}}</p>
</pullable>
```
当 `refresh` 没有设置时，一旦 `pullable` 被拉出来就会显示默认的“继续下拉”提示内容。然后，`onPulling` 事件回调函数应该这样编写：
``` js
export default {
  async onPulling(event) {
    this.refresh = event ? '请松手' : '更新中'
    if (!event) { // 松手时触发刷新操作
        await runRefreshJobs()
        this.refresh = null // 刷新完成后重置状态
    }
  }
}
```

### 限制

目前 `pullable` 组件存在一些限制。除了必须在垂直的 `scroll` 组件中使用外，你还需要保证列表元素的数量超出 `scroll` 可视区域的尺寸，否则可能会出现问题。此外，`pullable` 的交互效果可能也比较生硬。
