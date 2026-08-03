# 弹窗

## 导入模块

``` js
import prompt from '@system.prompt'
```

## 接口定义

#### `showToast`
<decl method><pre>
(options: {
  message: string,
  duration?: number,
  important?: boolean
}): void
</pre></decl>

显示一个 toast 弹框，toast 是一种置于界面顶层的文本弹框。toast 在界面中只显示一个实例，有多个 toast 内容时会依次排队显示。

`options` 参数字段的描述：
- `message`：需要现实的文本。
- `duration`：toast 的显示时长，单位为 ms，达到超时时长后 toast 会自动隐藏。
- `important`：是否为重要的 toast，默认为 `false`。如果设置为 `true`，则允许应用在后台时弹出该 toast。

toast 的显示样式（字体、颜色等）由固件决定，无法在应用中修改。toast 的显示时长也有限制，为 $200$ 到 $5000$ 毫秒。

#### `showPopup` <decl type="(options: { uri: string, params?: Object }): Promise<any>" method />

显示一个悬浮页面弹窗。`options` 参数字段描述：
- `uri`：目标页面的名字，需要在 `mainfest.json` 的 `router` 中注册。
- `params`：跳转时需要传递的数据，`params` 参数的属性会替换目标页面的 `data` 属性值。

悬浮页面是一种系统级的弹窗（类似于 toast 或者对话框），但悬浮页面是功能完整的页面，具有最高的可定制性。和一般的页面不同，悬浮页面在系统的悬浮页面栈中显示而不是应用自己的页面栈，因此[页面路由](api/system-router)机制中的 `router.back()` 等 API 无法操作悬浮页面。想要关闭悬浮页面，可以使用 [`router.close()`](system-router.md#close) 方法。

弹窗的显示层级比应用高，因此悬浮页面会显示在所有应用的页面之上。所有的应用都使用同一个悬浮页面栈，悬浮页面按照弹出顺序决定显示层级，即早弹出的页面位于顶部。悬浮页面的显示层级和对话框相同，低于 toast。

和 `router.push()` 一样，`showPopup()` 也返回一个 Promise 对象，它会在悬浮页面退出之后兑现并返回自定义的结果。详情请参考 [`router.push()`](system-router.md#push) 和 [`router.close()`](system-router.md#close)。
