# Console Module

The functionality of the `console` module is similar to the `console` feature in browsers, used for logging. This module can be used directly without importing. All properties are bound to the `console` global variable, for example:
``` js
console.log('Hello world!')
```


## API Definitions

### `backtrace` <decl type="boolean" />

When `backtrace` is set to `true`, all log printouts will include call stack information. The default value is `false`, in which case only `console.warn()` and higher-level APIs will output the call stack.

### `log` <decl type="(...data: any[]): void" method />

### `dir` <decl type="(...data: any[]): void" method />

### `debug` <decl type="(...data: any[]): void" method />

### `info` <decl type="(...data: any[]): void" method />

### `warn` <decl type="(...data: any[]): void" method />

### `error` <decl type="(...data: any[]): void" method />

## Log Filtering Levels

The log filtering level of the `console` module is determined by the underlying system's log filtering mechanism and cannot be configured in JavaScript code.