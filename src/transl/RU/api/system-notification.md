# Уведомления

## Импорт модуля

``` js
import notification from '@system.notification'
```

Разработчикам необходимо объявить разрешение на доступ приложения к `watch.permission.NOTIFICATION` в файле [`manifest.json`](/framework/application/manifest.md#permissions).

## API

### `publish`
<decl method><pre>
(options: {
  icon: string,
  id?: number,
  contentType: number,
  content: object,
  deliveryTime: number,
  actionUri: string
}): void
</pre></decl>

Публикация уведомления. Назначение полей параметра `options`:
- `icon`：URI иконки уведомления;
- `id`：уникальный идентификатор (id) уведомления приложения;
- `contentType`：тип содержимого. 1: тип обычного текстового уведомления. 2: тип уведомления с изображением; уведомления с изображениями временно не поддерживаются;
- `content`：используется в сочетании с `contentType`, задает содержимое уведомления;
  - Когда `contentType` равен 1, задает содержимое обычного текстового уведомления; тип object, содержит следующие поля:
    - `title`：заголовок обычного текстового уведомления; тип string;
    - `text`：текст обычного текстового уведомления; тип string;
- `deliveryTime`：время отправки уведомления;
- `actionUri`：URI, на который осуществляется переход при нажатии на уведомление.

### `remove` 
<decl method><pre>
(options: {
  query:{
    id?: number
  }
}): void
</pre></decl>

Удаление уведомления. Параметр `options` содержит следующие поля:
- query：критерии поиска для удаления,
  - id：удаление уведомления с указанным id; если id не передан, удаляются все уведомления.