# 电池状态

## 导入模块

``` js
import battery from '@system.battery'
```

## API

### `getStatus` <decl type="(): Promise<{charge: ChargeState, level: number}>" method />

获取电池的充电状态 `charge` （[`ChargeState`](#chargestate) 类型）和电量值 `level`。电量值是 $[0, 100]$ 间的整数。

## 类型

### `ChargeState`

`ChargeState` 枚举所有的电池充电状态，其定义如下：
``` ts
type ChargeState = 'charging' | 'discharging' | 'not-charging' | 'full'
```
各个值的含义为：
- `'charging'`：电池处于充电状态；
- `'discharging'`：断开充电状态；
- `'not-charging'`：未处于充电状态；
- `'full'`：电池已经充满电。
