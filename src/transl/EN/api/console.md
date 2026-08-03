# Console module

The function of the `console` module is similar to the `console` function in the browser and is used to implement logging. This module can be used directly without importing. All properties are bound to the `console` global variable, for example:
``` js
console.log('Hello world!')
```


## Interface definition

### `backtrace` <decl type="boolean" />

After setting `backtrace` to `true`, all log printouts will carry call stack information. The default value is `false`, at which time only `console.warn()` and higher-level APIs will output the call stack.

### `log` <decl type="(...data: any[]): void" method />

### `dir` <decl type="(...data: any[]): void" method />

### `debug` <decl type="(...data: any[]): void" method />

### `info` <decl type="(...data: any[]): void" method />

### `warn` <decl type="(...data: any[]): void" method />

### `error` <decl type="(...data: any[]): void" method />

## Log filtering level

The log filtering level of the `console` module is determined by the underlying log filtering mechanism of the system and cannot be configured in JavaScript code.
