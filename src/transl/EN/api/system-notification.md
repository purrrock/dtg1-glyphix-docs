# Message Notification

## Import Module

``` js
import notification from '@system.notification'
```

Developers need to declare access permission for `watch.permission.NOTIFICATION` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

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

Publishes a message notification. The fields in the `options` parameter are described as follows:
- `icon`: URI of the message icon;
- `id`: Unique ID of the application notification;
- `contentType`: Content type. `1`: Plain text notification type. `2`: Image notification type (image notifications are not currently supported);
- `content`: Used in conjunction with `contentType` to represent the content of the notification;
  - When `contentType` is `1`, it represents the content of a plain text notification (`object` type), containing the following fields:
    - `title`: Title of the plain text notification (`string` type);
    - `text`: Content of the plain text notification (`string` type);
- `deliveryTime`: Notification delivery time;
- `actionUri`: URI to jump to when the notification is clicked.

### `remove` 
<decl method><pre>
(options: {
  query:{
    id?: number
  }
}): void
</pre></decl>

Clears message notifications. The `options` parameter contains the following fields:
- `query`: Query conditions for clearing,
  - `id`: Clears the message notification with the specified ID. If no ID is passed, all message notifications are cleared.