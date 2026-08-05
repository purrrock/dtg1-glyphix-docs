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
- `mode`: режим вибрации, `long` означает длинную вибрацию, `short` — короткую. Значение по умолчанию — `long`.