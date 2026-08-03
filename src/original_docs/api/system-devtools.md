# 调试接口

## 导入模块

``` js
import devtools from '@system.devtools'
```

## API

### `command` <decl type="(cmd: string, fn: (argv: string[]) => void): void" method />

将一个函数 `fn` 注册为名为 `cmd` 的 shell 命令。注册后可以在设备终端上使用 `dev` 命令来调用。例如
``` bash
dev cmd arg1 arg2
```
会调用名为 `'cmd'` 的命令，而参数列表为 `['arg1', 'arg2']`。

