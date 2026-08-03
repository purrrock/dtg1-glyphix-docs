# Планировщик задач (定时任务)

## Импорт модуля

``` js
import schedule from "@system.schedule"
// Или
const schedule = require("@system.schedule")
```

Разработчикам необходимо объявить разрешение на доступ к `watch.permission.SCHEDULE` в файле [`manifest.json`](/framework/application/manifest.md#permissions).

## API

### `scheduleJob`
<decl method><pre>
(options: {
  type: number,
  timeout: number,
  triggerMethod: String,
  interval?: number,
  params?: Object,
}): number
</pre></decl>

Установка таймера для задачи. Назначение полей в параметре `options`:
- `type`:	
  - 1: Аппаратное время. Изменение системного времени может привести к вызову `triggerMethod`;
  - 2: Реальное истечение времени. Время учитывается даже в спящем режиме;
- `timeout`:
  - Если `type` равен 1, это метка времени (timestamp) для первого выполнения, то есть количество миллисекунд с 1970/01/01 00:00:00 GMT до текущего момента;
  - Если `type` равен 2, это интервал от текущего момента до первого выполнения в миллисекундах;
- `triggerMethod`: Имя метода, определенного в `app.js`, который вызывается фоновым сервисом при достижении времени срабатывания;
- `interval`: Интервал периодического выполнения в миллисекундах. Если не передано, задача не повторяется;
- `params`: Параметры задачи;

::: tip
Хотя точность `timeout` и `interval` составляет миллисекунды, срабатывание задач происходит с точностью до секунды. Интервал до первого выполнения и период повторения не могут быть меньше 60 секунд, в противном случае интерфейс выбросит исключение.
:::

Возвращаемое значение — это ID задачи, который используется для ее отмены. Возвращаемое значение `-1` означает сбой при создании.

``` js
let id = schedule.scheduleJob({
  type: 1,
  timeout: new Date('2025-03-14T23:00:00').getTime(),  // Метка времени для первого выполнения
  interval: 60000,     // Интервал периодического выполнения не менее 60 секунд
  triggerMethod: 'scheduleFunc',
  params: {
    food: 'apple',
  },
})

// app.js
export default {
  scheduleFunc(params) {
    console.log('scheduleFunc', params)
  },
}
```

### `cancel` <decl type="(id: number): void" method/>

Отмена запланированной задачи.

``` js
schedule.cancel(id)
```