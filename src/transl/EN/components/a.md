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
