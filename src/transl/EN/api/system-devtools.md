# Debug interface

## Import module

``` js
import devtools from '@system.devtools'
```

## API

### `command` <decl type="(cmd: string, fn: (argv: string[]) => void): void" method />

Register a function `fn` as a shell command named `cmd`. After registration, you can use the `dev` command on the device terminal to call it. For example
``` bash
dev cmd arg1 arg2
```
A command named `'cmd'` is called with the argument list `['arg1', 'arg2']`.
