# 电池状态

## 导入模块

``` js
import battery from '@system.battery'
```

## API

### `getStatus` <decl type="(): Promise<{charge: ChargeState, level: number}>" method />

Получение состояния зарядки батареи `charge` (тип [`ChargeState`](#chargestate)) и уровня заряда `level`. Уровень заряда представляет собой целое число в диапазоне $[0, 100]$.

## Типы

### `ChargeState`

Перечисление `ChargeState` содержит все возможные состояния зарядки батареи, его определение выглядит следующим образом:
``` ts
type ChargeState = 'charging' | 'discharging' | 'not-charging' | 'full'
```
Значения и их смысл:
- `'charging'`: батарея заряжается;
- `'discharging'`: зарядка отключена (разрядка);
- `'not-charging'`: зарядка не происходит;
- `'full'`: батарея полностью заряжена.