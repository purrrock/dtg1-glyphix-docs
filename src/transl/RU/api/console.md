# Модуль Console

Функционал модуля `console` аналогичен объекту `console` в браузере и используется для логирования. Данный модуль можно использовать напрямую без предварительного импорта, все его свойства привязаны к глобальной переменной `console`, например:
``` js
console.log('Hello world!')
```


## Определение интерфейсов

### `backtrace` <decl type="boolean" />

Если установить `backtrace` в значение `true`, все вызовы логирования будут содержать информацию о стеке вызовов. По умолчанию значение равно `false`. В этом случае стек вызовов выводят только `console.warn()` и более высокие уровни API.

### `log` <decl type="(...data: any[]): void" method />

### `dir` <decl type="(...data: any[]): void" method />

### `debug` <decl type="(...data: any[]): void" method />

### `info` <decl type="(...data: any[]): void" method />

### `warn` <decl type="(...data: any[]): void" method />

### `error` <decl type="(...data: any[]): void" method />

## Уровни фильтрации логов

Уровень фильтрации логов модуля `console` определяется низкоуровневым механизмом фильтрации системы и не может быть настроен в коде JavaScript.