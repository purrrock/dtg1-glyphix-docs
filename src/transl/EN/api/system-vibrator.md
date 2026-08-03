# vibration

## Import module

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

Trigger vibration. The functions of each field of the `option` parameter are:
- `mode`: vibration mode, `long` means long vibration, `short` means short vibration. The default value is `long`.
