# Отладка (Debugging)

## Импорт модуля

``` js
import devtools from '@system.devtools'
```

## API

### `command` <decl type="(cmd: string, fn: (argv: string[]) => void): void" method />

Регистрирует функцию `fn` в качестве shell-команды с именем `cmd`. После регистрации ее можно вызывать из терминала устройства с помощью команды `dev`. Например:
``` bash
dev cmd arg1 arg2
```
вызовет команду с именем `'cmd'` и списком аргументов `['arg1', 'arg2']`.