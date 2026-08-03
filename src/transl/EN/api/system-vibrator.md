# Vibration

## Import Module

``` js
import vibrator from '@system.vibrator'
```

## API

### `vibrate`
<decl method><pre>
(options: {
  mode: string
}): bool
</pre></decl> 

Triggers vibration. The fields of the `options` parameter are described as follows:
- `mode`: Vibration mode. `long` indicates a long vibration, and `short` indicates a short vibration. The default value is `long`.