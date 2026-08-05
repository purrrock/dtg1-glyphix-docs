# Конфигурация приложения

## Импорт модуля

```js
import configuration from '@system.configuration'
```

## Определение интерфейсов

### `getLocale`
<decl method><pre>
(): {
  language: string,
  countryOrRegion: string,
}
</pre></decl>

Получает текущую локаль приложения. По умолчанию используется системная локаль, которая может изменяться при изменении настроек или системного языка.
 - `language` указывает текущий язык, например 'zh', 'en' и т. д.
 - `countryOrRegion` указывает текущую страну или регион, например 'CN', 'US' и т. д.