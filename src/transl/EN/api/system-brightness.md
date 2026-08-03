# Brightness Management

## Import Module

``` js
import brightness from '@system.brightness'
```

## API

### `getValue` <decl type="(): number" method />

Gets the screen brightness value, ranging from $[0, 1]$.

### `setValue` <decl type="(value: number): void" method />

Sets the screen brightness value. The range of `value` is $[0, 1]$.

### `getMode` <decl type="(): string" method />

Gets the screen brightness mode.

### `setMode` <decl type="(mode: number): void" method />

Sets the screen brightness mode. When `number` is set to `0`, it is standard mode; when `number` is set to `1`, it is automatic mode.

### `setKeepScreenOn` <decl type="(mode: Boolean): void" method />

Sets whether to keep the screen on. When `mode` is set to `true`, the screen stays on; when `mode` is set to `false`, the screen is no longer kept on.

### `wakeScreenOn`
<decl method><pre>
(options: { 
  screenOn: boolean, 
  timeout?: number,
}): void
</pre></decl>

Turns the screen on or off. The fields of the `options` parameter are as follows:
- `screenOn`: Whether to turn on the screen
- `timeout`: Automatic screen-off time, leaving it blank means no time limit