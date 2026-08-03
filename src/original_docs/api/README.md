# API

Glyphix 提供一整套运行时 JavaScript API，包括与浏览器环境类似的 [`setInterval`](timer.md)、[`console`](console.md) 等 API，也有用于实现整个应用必须的各种系统能力接口。

但是与浏览器环境不同，Glyphix 不提供 DOM 接口，因此没有 `window`、`document` 等对象，也不能进行任何 DOM 操作。

## 快应用异步接口

Glyphix 支持手表快应用标准，但我们主要使用 Promise 风格的异步接口，而不是回调函数风格。例如手表快应用中的 `file.readText()` 接口的回调模式是这样使用的：
``` js
import file from '@system.file'

file.readText({
  uri: 'internal://files/test.txt',
  success(data) {
    console.log(data)
  },
  fail(data, code) {
    console.log(`read text failed: ${code}`)
  }
})
```
但是在 Glyphix 中常使用 Promise 风格：
``` js
import file from '@system.file'

// 假设在某个异步函数中
try {
  const content = await file.readText({ uri: 'internal://files/test.txt' })
  console.log(content)
} catch (e) {
  console.error('read text failed:', e)
}
```
由于 Promise 风格 API 更符合 ES6 标准之后的使用习惯，所以本文档只保留 Promise 版本的类型签名。

### Promise vs. 回调接口

如无特别说明，所以返回类型为 `Promise<...>` 的接口都支持回调函数（低版本快应用标准），以及 Promise 两种异步接口风格。回调函数风格的异步接口通常具有以下类型：
``` ts
type CallbackAPI = (options: {
  success: (data: any) => void,
  fail: (data: any, code: number) => void,
  complete: () => void,
  // 其他参数...
}) => void
```
而 Promise 风格下的异步接口则是以下类型：
``` ts
type PromiseAPI = (options: any) => Promise<any>
```

当参数 `options` 中存在任意 `success`、`fail` 或 `complete` 属性时，API 会自动使用回调函数风格（没有返回值），否则使用 Promise 返回值风格。

::: warning
使用回调函数风格时，异步 API 不会返回任何值，因此无法使用 `await` 语法。所以要确保使用 Promise/`await` 语法时，不要传入任何 `success`/`fail` 或 `complete` 回调函数。
:::

### API 示例

以 [`system.file`](system-file.md) 模块为例，的所有函数同时支持 Promise 和回调风格的异步调用模式。下面的代码片段给出了两种 API 用法对比。

::: code-tabs#js

@tab async/await

``` js
import file from '@system.file'

// async/await 实际上是 Promise 的语法糖
async function readFile() {
  let text = await file.readText({ uri: '/app.js' })
  console.log(text)
}

readFile()
```

@tab Promise

``` js
import file from '@system.file'

file.readText({ uri: '/app.js' })
  .then(console.log) // 提示：console.log() 类型和 Promise.then() 是匹配的，不需要使用箭头函数
  .fail((error) => console.log(`${error.message}: ${error.code}`))
```

@tab callback

``` js
import file from '@system.file'

file.readText({
  uri: '/app.js',
  success(data) {
    console.log(data)
  },
  fail(msg, code) {
    console.log(`${msg}: ${code}`)
  },
  complete() {
    console.log("complete")
  }
})
```

:::

本文档只会给出 Promise 风格的 API 类型，并且异步操作的示例只用 await/async 语法。

::: tip
不建议开发者额外对 Glyphix API 进行封装，尤其是手动将其回调函数兼容风格封装成 Promise 模式。这种做法需要编写额外的代码，并会损害性能。
:::

## 订阅接口

订阅类的 API 向某个模块注册一个回调函数，而不是直接返回结果。与一般的异步接口不同，订阅接口的回调函数可以被多次执行。所有的订阅接口都支持注册多个订阅回调函数，并且会返回一个订阅 ID，并可以用对应的接口取消订阅。

Glyphix 目前不支持快应用风格的订阅 `fail` 回调函数，但可能在订阅失败时直接抛出异常。
