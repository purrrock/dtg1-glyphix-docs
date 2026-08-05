# API

Glyphix provides a complete set of runtime JavaScript APIs, including browser-like APIs such as [`setInterval`](timer.md) and [`console`](console.md), as well as various system capability interfaces essential for implementing the entire application.

However, unlike the browser environment, Glyphix does not provide DOM interfaces. Therefore, objects like `window` and `document` do not exist, and no DOM operations can be performed.

## QuickApp Asynchronous Interfaces

Glyphix supports the Watch QuickApp standard, but we primarily use Promise-style asynchronous interfaces rather than callback-style ones. For example, the callback pattern for the `file.readText()` interface in Watch QuickApps is used like this:
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
However, in Glyphix, the Promise style is commonly used:
``` js
import file from '@system.file'

// Assuming inside an async function
try {
  const content = await file.readText({ uri: 'internal://files/test.txt' })
  console.log(content)
} catch (e) {
  console.error('read text failed:', e)
}
```
Since Promise-style APIs better align with modern usage habits post-ES6, this documentation only retains the type signatures for the Promise version.

### Promise vs. Callback Interfaces

Unless otherwise specified, all interfaces with a return type of `Promise<...>` support both callback functions (older QuickApp standards) and Promise asynchronous interface styles. Callback-style asynchronous interfaces typically have the following type:
``` ts
type CallbackAPI = (options: {
  success: (data: any) => void,
  fail: (data: any, code: number) => void,
  complete: () => void,
  // Other parameters...
}) => void
```
While Promise-style asynchronous interfaces have the following type:
``` ts
type PromiseAPI = (options: any) => Promise<any>
```

When any `success`, `fail`, or `complete` property is present in the `options` parameter, the API automatically uses the callback function style (with no return value); otherwise, it uses the Promise return value style.

::: warning
When using the callback function style, the asynchronous API does not return any value, making it impossible to use the `await` syntax. Therefore, make sure not to pass any `success`, `fail`, or `complete` callback functions when using the Promise/`await` syntax.
:::

### API Examples

Taking the [`system.file`](system-file.md) module as an example, all of its functions support both Promise and callback styles of asynchronous invocation patterns. The code snippet below compares the two API usages.

::: code-tabs#js

@tab async/await

``` js
import file from '@system.file'

// async/await is actually syntactic sugar for Promises
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
  .then(console.log) // Tip: The console.log() type matches Promise.then(), so arrow functions are not needed
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

This documentation will only provide Promise-style API types, and examples of asynchronous operations will exclusively use the `await`/`async` syntax.

::: tip
Developers are not recommended to write additional wrappers around Glyphix APIs, especially manually wrapping their callback-compatible styles into Promise patterns. This practice requires writing extra code and will hurt performance.
:::

## Subscription Interfaces

Subscription-style APIs register a callback function with a module instead of returning a result directly. Unlike general asynchronous interfaces, the callback function of a subscription interface can be executed multiple times. All subscription interfaces support registering multiple subscription callback functions, return a subscription ID, and allow unsubscribing using the corresponding interface.

Glyphix currently does not support QuickApp-style subscription `fail` callback functions, but may throw exceptions directly when a subscription fails.