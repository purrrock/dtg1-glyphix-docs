# Вибрация

## Импорт модуля

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

Запуск вибрации. Назначение полей параметра `options`:
- `mode`: режим вибрации, значение `long` означает длинную вибрацию, `short` — короткую вибрацию. Значение по умолчанию — `long`.