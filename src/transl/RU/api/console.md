# Модуль Console

Функционал модуля `console` аналогичен объекту `console` в браузере и используется для логирования. Этот модуль можно использовать напрямую без предварительного импорта, все его свойства привязаны к глобальной переменной `console`, например:
``` js
console.log('Hello world!')
```


## Определение интерфейсов

### `backtrace` <decl type="boolean" />

Если установить для параметра `backtrace` значение `true`, все вызовы логирования будут содержать информацию о стеке вызовов (backtrace). Значение по умолчанию — `false`, в этом случае стек вызовов выводят только `console.warn()` и более высокие уровни API.

### `log` <decl type="(...data: any[]): void" method />

### `dir` <decl type="(...data: any[]): void" method />

### `debug` <decl type="(...data: any[]): void" method />

### `info` <decl type="(...data: any[]): void" method />

### `warn` <decl type="(...data: any[]): void" method />

### `error` <decl type="(...data: any[]): void" method />

## Уровни фильтрации логов

Уровень фильтрации логов модуля `console` определяется низкоуровневым механизмом фильтрации системы и не может быть настроен в коде JavaScript.