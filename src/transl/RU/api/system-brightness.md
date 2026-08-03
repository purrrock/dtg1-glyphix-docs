# Управление яркостью

## Импорт модуля

``` js
import brightness from '@system.brightness'
```

## API

### `getValue` <decl type="(): number" method />

Получает значение яркости экрана, диапазон составляет $[0, 1]$.

### `setValue` <decl type="(value: number): void" method />

Устанавливает значение яркости экрана. Диапазон параметра `value` составляет $[0, 1]$.

### `getMode` <decl type="(): string" method />

Получает режим яркости экрана.

### `setMode` <decl type="(mode: number): void" method />

Устанавливает режим яркости экрана. Если установить `number` в значение `0`, включится стандартный режим, а если в значение $1$ — автоматический режим.

### `setKeepScreenOn` <decl type="(mode: Boolean): void" method />

Устанавливает, должен ли экран оставаться включенным. Если установить `mode` в значение `true`, экран будет постоянно включен; если в `false`, постоянное включение отменяется.

### `wakeScreenOn`
<decl method><pre>
(options: { 
  screenOn: boolean, 
  timeout?: number,
}): void
</pre></decl>

Включает или выключает экран. Назначение полей параметра options:
- `screenOn`: включать ли экран
- `timeout`: время до автоматического выключения, если не указано — время не ограничено