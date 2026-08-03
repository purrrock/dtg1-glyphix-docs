# a

锚点组件，默认为行内元素，用于跳转到指定的页面。

## 属性

### `href` <decl type="string" get set />

指定需要跳转的[页面名称](/framework/application/manifest.md#pages)或者 URI 字符串。

``` html
<a href="page1">跳转到 page1 页面</a>
``` 

与 Web 中的 `<a>` 标签不同，`a` 组件只支持页面跳转而不支持超链接跳转。

`href` 属性还支持形如 `PageName?key=value` 的 [URI](/framework/application/resource.md#uri) 字符串，即由页面名称（作为 path 字段）和 query 字段构成的 URI。该 URI 的 query 字段会被解析为页面的跳转参数。如点击这个 `<a>` 元素时：

``` html
<a href="page1?text=test-text&message=hello">跳转到 page1 页面</a>
```

等效于调用以下 [`router.push()`](/api/system-router.md#push) 方法：

``` js
router.push({
  uri: 'page1',
  params: {text: 'test-text', message: 'hello'}
})
```

::: tip
请注意，URI 中 query 字段的值只会被解析为字符串类型，因此 `page1?size=100` 中的 `100` 会被解析为字符串 `'100'`，而不是数字 `100`。如果需要传递特定类型的参数，请使用 [`router`](/api/system-router.md) API。
:::
