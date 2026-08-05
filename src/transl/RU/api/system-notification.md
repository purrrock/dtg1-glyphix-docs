# 消息通知

## 导入模块

``` js
import notification from '@system.notification'
```

开发者需要在 [`manifest.json`](/framework/application/manifest.md#permissions) 文件中声明应用对 `watch.permission.NOTIFICATION` 的访问权限。

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

发布消息通知。`options` 参数的各字段功能为：
- `icon`：消息图标的 URI；
- `id`：应用通知的唯一 id；
- `contentType`：正文类型。 1：普通文本通知类型。 2：图片通知类型；暂时不支持图片通知；
- `content`：与 `contentType` 配合使用，表示通知的正文内容；
  - 当 `contentType` 为 1 时，表示普通文本通知的正文内容；object 类型，包含以下字段：
    - `title`：普通文本通知标题；string 类型；
    - `text`：普通文本通知内容；string 类型；
- `deliveryTime`：通知发送时间；
- `actionUri`：点击通知时跳转的 URI。

### `remove` 
<decl method><pre>
(options: {
  query:{
    id?: number
  }
}): void
</pre></decl>

清除消息通知。`options` 参数包含以下字段：
- query：清除的查询条件，
  - id：清除指定 id 的消息通知，如果不传入 id，则清除所有消息通知。