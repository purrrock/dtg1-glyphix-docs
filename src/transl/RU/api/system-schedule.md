# Планировщик задач (定时任务)

## Импорт модуля

``` js
import schedule from "@system.schedule"
// Или
const schedule = require("@system.schedule")
```

Разработчикам необходимо объявить разрешение на доступ к `watch.permission.SCHEDULE` для приложения в файле [`manifest.json`](/framework/application/manifest.md#permissions).

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

Установка задачи по расписанию. Назначение полей параметра `options`:
- `type`:	
  - 1: Аппаратное время, `triggerMethod` может быть вызван путем изменения системного времени;
  - 2: Реальное течение времени, время рассчитывается даже в спящем режиме;
- `timeout`:
  - Если `type` равен 1, это метка времени (timestamp) первого выполнения, то есть количество миллисекунд от 1970/01/01 00:00:00 GMT до текущего момента;
  - Если `type` равен 2, это интервал от текущего времени до первого выполнения в миллисекундах;
- `triggerMethod`: имя метода, определенного в `app.js`, который вызывается фоновым сервисом при достижении времени тайм-аута;
- `interval`: интервал периодического выполнения в миллисекундах; если не передан, задача не повторяется;
- `params`: параметры задачи.

::: tip
Хотя точность `timeout` и `interval` составляет миллисекунды, таймер срабатывает с точностью до секунды. Интервал времени до первого выполнения и период повторения не могут быть менее 60 секунд, в противном случае интерфейс выбросит исключение.
:::

Возвращаемое значение — это ID задачи, который используется для ее отмены. Возвращаемое значение `-1` означает сбой при создании.

``` js
let id = schedule.scheduleJob({
  type: 1,
  timeout: new Date('2025-03-14T23:00:00').getTime(),  // Метка времени первого выполнения
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