# Console 模块

`console` 模块的功能和浏览器中的 `console` 功能类似，用于实现日志记录。本模块无需导入就可以直接使用，所有属性都绑定到 `console` 全局变量，例如：
``` js
console.log('Hello world!')
```


## 接口定义

### `backtrace` <decl type="boolean" />

把 `backtrace` 设置为 `true` 之后，所有的日志打印将携带调用栈信息。默认值为 `false`，此时只有 `console.warn()` 及更高级的 API 会输出调用栈。

### `log` <decl type="(...data: any[]): void" method />

### `dir` <decl type="(...data: any[]): void" method />

### `debug` <decl type="(...data: any[]): void" method />

### `info` <decl type="(...data: any[]): void" method />

### `warn` <decl type="(...data: any[]): void" method />

### `error` <decl type="(...data: any[]): void" method />

## 日志过滤级别

`console` 模块的日志过滤级别由系统底层的日志过滤机制决定，无法在 JavaScript 代码中配置。
