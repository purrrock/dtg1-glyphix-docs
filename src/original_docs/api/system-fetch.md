# 数据请求 fetch

## 导入模块

``` js
import fetch from '@system.fetch'
```

## API

### `fetch`
<decl method><pre>
(options: {
  url: string,
  method?: 'GET' | 'POST' | 'PUT',
  header?: {[key: string]: string},
  params?: {[key: string]: string | number},
  data?: string | ArrayBuffer | {[key: string]: any},
  responseType?: 'text' | 'json' | 'arraybuffer',
  timeout?: number
}): Promise<{
  code: number,
  headers: {[key: string]: string},
  data: string | ArrayBuffer | any,
}>
</pre></decl>

发起异步的网络数据请求。`options` 参数的各字段功能为：
- `url`：要访问的网站的网址 URL。
- `method`：支持 `'GET'` 、`'POST'` 和 `'PUT'`，默认是 `'GET'`。
- `header`：一个包含 HTTP 请求头信息的对象，键和值为字符串。典型的 HTTP 头部字段可以是 `Authorization`、`Content-Type` 等。
- `params`：请求的参数，会将其所有属性设置到请求的 URL 部分。
- `data`：HTTP POST 请求中的主体（body）部分内容。
- `responseType`：HTTP 请求中的响应数据类型，默认是 `'text'`，可以有以下取值。
  - `'text'`：响应返回文本数据，即返回数据的 `data` 属性为 `string` 类型。
  - `'json'`：响应返回 JSON 数据，返回的 `data` 属性会将该 JSON 数据解析为对应的 JavaScript 值。
  - `arraybuffer`：响应返回二进制数据，即返回的数据是，以 `ArrayBuffer` 对象来存储的。
- `timeout`: 请求响应的超时时间，单位为毫秒，默认值为 $6000 \rm ms$。

#### `data` 参数

`data` 是请求的主体（body），仅在 POST 请求中使用。它通常是三种类型：字符串、`ArrayBuffer` 对象或者 JSON 对象。当 `data` 为字符串或者 `ArrayBuffer` 对象时，请求的主体将分别是文本或者二进制数据。当主体是一个 JSON 对象时，它会被序列化为文本形式。序列化的格式由请求方法（`method` 参数）的 `Content-Type` 字段决定：
- `Content-Type` 为 `application/json` 时，将 `data` 参数对象序列化为 JSON 字符串后作为请求主体；
- 其他情况下将 `data` 参数对象序列化为 `application/x-www-form-urlencoded` 的格式。

::: warning
很多 HTTP API 使用 JSON 格式的 POST 请求主体，请注意要正确设置请求头的 `Content-Type` 为 `application/json`，具体请参考此[示例](#post-请求-json-body)。
:::

#### 返回值

返回一个 `Promise` 对象，它在请求完后兑现值的属性如下：
- [`code`](#code-响应代码) 为服务器响应代码，请求成功的响应代码一般是 `200`。
- `header` 为服务器的响应头。
- `data` 为请求数据的返回值，具体的内容由 `options.responseType` 参数决定。

当请求失败后，返回的 `Promise` 对象会被拒绝。

## 使用说明

### `code` 响应代码

服务器返回的响应代码含义为：
- `200`：表示请求成功；
- `1002`：参数校验错误；
- `1005`：输入的参数不完整；
- `5000`：请求失败，响应错误；
- `5001`：读取数据缓冲区失败；
- `5002`：请求失败，响应错误；
- 其他：其他 HTTP/HTTPS 响应代码，如 `404` 等。

当 [`fetch`](#fetch) 返回的响应代码为 `200` 时表示网络请求成功，为其他值时表示请求出现错误。

### 注意事项

## 示例

### GET 请求

这是一个基本的 GET 请求示例：

``` js
const res = await fetch.fetch({
  url: 'http://www.rt-thread.com/service/rt-thread.txt',
  method: 'GET', // 由于默认的模式就是 GET，此时 method 是可选的
  responseType: 'text'
})
console.log(`the status code of the response: ${res.code}`)
console.log(`the data of the response: ${res.data}`)
```

### POST 请求

``` js
const res = await fetch.fetch({
  url: 'https://www.rt-thread.com/service/echo',
  method: 'POST',
  data: {
    key1: 'hello',
    key2: 'world'
  },
  responseType: 'text'
})
console.log(`the status code of the response: ${res.code}`)
console.log(`the data of the response: ${res.data}`)
```

### POST 请求（JSON Body）
