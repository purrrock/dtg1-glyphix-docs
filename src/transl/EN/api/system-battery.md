# Battery Status

## Importing Modules

``` js
import battery from '@system.battery'
```

## API

### `getStatus` <decl type="(): Promise<{charge: ChargeState, level: number}>" method />

Gets the battery charging state `charge` (of type [`ChargeState`](#chargestate)) and the battery level `level`. The battery level is an integer between $[0, 100]$.

## Types

### `ChargeState`

`ChargeState` enumerates all battery charging states, defined as follows:
``` ts
type ChargeState = 'charging' | 'discharging' | 'not-charging' | 'full'
```
The meanings of each value are:
- `'charging'`: The battery is charging;
- `'discharging'`: The battery is discharging (disconnected from power);
- `'not-charging'`: The battery is not charging;
- `'full'`: The battery is fully charged.