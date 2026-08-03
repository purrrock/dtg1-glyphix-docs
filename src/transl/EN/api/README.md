# API

Glyphix provides a complete set of runtime JavaScript APIs, including [`setInterval`](timer.md), [`console`](console.md) and other APIs similar to the browser environment, as well as various system capability interfaces used to implement the entire application.

However, unlike the browser environment, Glyphix does not provide a DOM interface, so there are no `window`, `document` and other objects, and no DOM operations can be performed.

## Quick App asynchronous interface

Glyphix supports the watch Quick App standard, but we mainly use the Promise style asynchronous interface instead of the callback function style. For example, the callback mode of the `file.readText()` interface in the watch quick app is used like this:
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
But Promise style is often used in Glyphix:
``` js
import file from '@system.file'

// Assume that in an asynchronous function
try {
  const content = await file.readText({ uri: 'internal://files/test.txt' })
  console.log(content)
} catch (e) {
  console.error('read text failed:', e)
}
```
Since the Promise style API is more in line with usage habits after the ES6 standard, this document only retains the type signature of the Promise version.

### Promise vs. callback interface

Unless otherwise specified, all interfaces with a return type of `Promise<...>` support callback functions (lower versions of Quick App standards) and Promise asynchronous interface styles. Callback function-style asynchronous interfaces typically have the following types:
``` ts
type CallbackAPI = (options: {
  success: (data: any) => void,
  fail: (data: any, code: number) => void,
  complete: () => void,
  // Other parameters...
}) => void
```
The asynchronous interface in Promise style is of the following types:
``` ts
type PromiseAPI = (options: any) => Promise<any>
```

When any `success`, `fail` or `complete` attribute exists in the parameter `options`, the API will automatically use the callback function style (no return value), otherwise it will use the Promise return value style.

::: warning
When using the callback function style, the asynchronous API does not return any value, so the `await` syntax cannot be used. So make sure you don't pass in any `success`/`fail` or `complete` callback functions when using Promise/`await` syntax.
:::

### API Example

Taking the [`system.file`](system-file.md) module as an example, all its functions support both Promise and callback-style asynchronous calling modes. The code snippet below gives a comparison of the two API usages.

::: code-tabs#js

@tab async/await

``` js
import file from '@system.file'

// async/await is actually syntactic sugar for Promise
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
  .then(console.log) // Tip: The console.log() type matches Promise.then() and there is no need to use arrow functions.
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

This document will only give Promise-style API types, and examples of asynchronous operations only use await/async syntax.

::: tip
It is not recommended that developers additionally encapsulate the Glyphix API, especially manually encapsulate its callback function compatibility style into Promise mode. This practice requires writing additional code and hurts performance.
:::

## Subscription interface

The API of the subscription class registers a callback function with a module instead of returning the result directly. Unlike general asynchronous interfaces, the callback function of the subscription interface can be executed multiple times. All subscription interfaces support the registration of multiple subscription callback functions, and will return a subscription ID, and you can use the corresponding interface to cancel the subscription.

Glyphix currently does not support the quick app style subscription `fail` callback function, but it may directly throw an exception when the subscription fails.
