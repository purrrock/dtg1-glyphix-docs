# 全局对象

## 全局函数

### `encodeURIComponent` <decl type="(str: string): string" function />

`encodeURIComponent()` 全局函数用于对 URI 组件 `str` 进行编码。它会将某些特殊字符转义成 UTF-8 编码后对应的百分号（`%`）转义序列，这可确保组件在用作 URL 的一部分时可被正确解释，特别是在查询字符串参数、路径或片段中。 

字母、数字、`- _ . ! ~ * ' ( )` 不会被编码。其他字符会被编码成百分号的转义序列（例如空格被编码为 `%20`）。

`encodeURIComponent()` 与 Web 中的[同名函数](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent)行为一致。

示例：
```js
console.log(encodeURIComponent("https://example.com/page?id=100"));
// output: https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100
```

### `decodeURIComponent` <decl type="(str: string): string" function />

`decodeURIComponent()` 全局函数用于解码由 `encodeURIComponent()` 编码的 URI 组件 `str`。它会将百分号（`%`）转义序列转换回其原始字符形式，从而恢复原始的 URI 组件。例如，它会将 `%20` 转换回空格。

`decodeURIComponent()` 与 Web 中的[同名函数](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/decodeURIComponent)行为一致。

示例：
```js
console.log(decodeURIComponent("https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100"));
// output: https://example.com/page?id=100
```

### `URI` <decl type="(uri: string | Uri): Uri" function />

此函数接受一个字符串，并将其解析为 `Uri` 对象用于后续处理。参数 `uri` 是待解析的 URI 字符串。

返回值是一个对象，包含以下字段：
- `scheme: string`：从参数中解析到的 scheme 字段；
- `authority: string`：从参数中解析到的 authority 字段；
- `path: string`：从参数中解析到的 path 字段；
- `query: string`：从参数中解析到的 query 字段；
- `origin: string`：参数中的原始 URI 字符串
- `toString: ( string`：此方法可以将本对象重新编码为 URI 字符串。

例如：
``` js
console.log(URI("https://app-name/icon.png"))
// {
//   scheme: 'https',
//   authority: 'app-name',
//   path: '/icon.png',
//   query: '',
//   origin: 'https://app-name/icon.png',
//   toString: <function>
// }
```

`URI` 函数还接受对象作为参数，这种情况下 `URI` 函数会给参数对象增加一个 `toString` 方法，通过该方法可以将 URI 对象编码为字符串：
``` js
let uri = {
  scheme: 'https',
  authority: 'app-name',
  path: '/icon.png',
  query: ''
}
console.log(URI(uri).toString()) // 'https://app-name/icon.png'
```
