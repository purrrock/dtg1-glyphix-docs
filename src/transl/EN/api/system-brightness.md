# Brightness management

## Import module

``` js
import brightness from '@system.brightness'
```

## API

### `getValue` <decl type="(): number" method />

Get the brightness value of the screen, the range is $[0, 1]$.

### `setValue` <decl type="(value: number): void" method />

Set the brightness value of the screen. The range of `value` is $[0, 1]$.

### `getMode` <decl type="(): string" method />

Get the brightness mode of the screen.

### `setMode` <decl type="(mode: number): void" method />

Set the screen brightness mode. When `number` is set to `0`, it is standard mode. When `number` is set to $1$, it is automatic mode.

### `setKeepScreenOn` <decl type="(mode: Boolean): void" method />

Set whether to keep the screen always on. When `mode` is set to `true`, the screen is always on. When `mode` is set to `false`, the screen is always on.

### `wakeScreenOn`
<decl method><pre>
(options: {
  screenOn: boolean,
  timeout?: number,
}): void
</pre></decl>

Turn the screen on or off. The functions of each field of the options parameter are:
- `screenOn`: whether to light up the screen
- `timeout`: automatic extinguishing time, no time limit if not filled in
