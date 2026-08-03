# Battery status

## Import module

``` js
import battery from '@system.battery'
```

## API

### `getStatus` <decl type="(): Promise<{charge: ChargeState, level: number}>" method />

Get the battery's charge state `charge` ([`ChargeState`](#chargestate) type) and power value `level`. The power value is an integer between $[0, 100]$.

## type

### `ChargeState`

`ChargeState` enumerates all battery charging states, which are defined as follows:
``` ts
type ChargeState = 'charging' | 'discharging' | 'not-charging' | 'full'
```
The meaning of each value is:
- `'charging'`: The battery is in charging state;
- `'discharging'`: Disconnect charging state;
- `'not-charging'`: not in charging state;
- `'full'`: The battery is fully charged.
