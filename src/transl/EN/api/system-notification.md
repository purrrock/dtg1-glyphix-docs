# Message notification

## Import module

``` js
import notification from '@system.notification'
```

Developers need to declare their application's access permissions to `watch.permission.NOTIFICATION` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

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

Post a message notification. The functions of each field of the `options` parameter are:
- `icon`: the URI of the message icon;
- `id`: the unique id of the application notification;
- `contentType`: text type. 1: Ordinary text notification type. 2: Picture notification type; picture notification is not supported temporarily;
- `content`: used in conjunction with `contentType` to represent the text content of the notification;
  - When `contentType` is 1, it represents the body content of a normal text notification; object type, including the following fields:
    - `title`: ordinary text notification title; string type;
    - `text`: ordinary text notification content; string type;
- `deliveryTime`: notification sending time;
- `actionUri`: URI to jump to when clicking the notification.

### `remove`
<decl method><pre>
(options: {
  query:{
    id?: number
  }
}): void
</pre></decl>

Clear message notification. The `options` parameter contains the following fields:
- query: cleared query conditions,
  - id: Clear the message notification with the specified id. If no id is passed in, all message notifications will be cleared.
