# Управление яркостью

## Импорт модуля

``` js
import brightness from '@system.brightness'
```

## API

### `getValue` <decl type="(): number" method />

Получение значения яркости экрана, диапазон составляет $[0, 1]$.

### `setValue` <decl type="(value: number): void" method />

Установка значения яркости экрана. Диапазон `value` составляет $[0, 1]$.

### `getMode` <decl type="(): string" method />

Получение режима яркости экрана.

### `setMode` <decl type="(mode: number): void" method />

Установка режима яркости экрана. Если `number` установлен в `0`, это стандартный режим; если `number` установлен в $1$, это автоматический режим.

### `setKeepScreenOn` <decl type="(mode: Boolean): void" method />

Установка параметра поддержания экрана во включенном состоянии. Если `mode` равен `true`, экран постоянно включен; если `mode` равен `false`, постоянное включение экрана отменяется.

### `wakeScreenOn`
<decl method><pre>
(options: { 
  screenOn: boolean, 
  timeout?: number,
}): void
</pre></decl>

Включение или выключение экрана. Назначение полей параметра `options`:
- `screenOn`: включать ли экран
- `timeout`: время до автоматического выключения, если не указано, время не ограничено