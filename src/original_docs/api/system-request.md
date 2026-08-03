# 上传下载 request

## 导入模块

``` js
import request from '@system.request'
```

## API

### `download`
<decl method><pre>
(options: {
  url: string,
  header?: {[key: string]: string},
  filename?: string,
  callback: (progress: number) => void
}): DownloadTask
</pre></decl>

通过 HTTP/HTTPS 协议下载文件，`options` 参数的各字段功能为：
- `url`：要访问的网站的网址 URL；
- `header`：一个包含 HTTP 请求头信息的对象，键和值为字符串。典型的 HTTP 头部字段可以是 `Authorization`、`Content-Type` 等；
- `filename`：存储下载文件的 URI，如：`internal://files/download.txt`；
- `callback`：下载进度回调函数，下载时会多次调用此函数，`progress` 为下载的进度值，范围为 $[0, 100]$。

`download()` 方法返回一个 [`DownloadTask`](#downloadtask) 对象，可用于等待下载完成或控制下载任务。

::: warning
请不要在 `callback` 函数中以下载进度达到 $100\%$ 作为下载完成后的操作触发条件，详情请参考[等待下载完成](#等待下载完成)。

当前实现没有自动根据 `url` 解析 `filename` 参数属性，请务必填写 `filename`。
:::

## 类型

### `DownloadTask`

`DownloadTask` 是 `download` 方法的返回类型，它的签名为：

``` ts
interface DownloadTask {
  complete: Promise<void>,
  cancel(): void
}
```

`complete` 属性是一个 `Promise` 对象，可用于等待下载完成。`cancel()` 方法用于取消正在进行的下载任务，如果下载已经完成，`cancel()` 方法没有效果。

#### 等待下载完成

使用 `DownloadTask.complete` 等待下载完成，该 `Promise` 兑现（fulfilled）时会保证文件已写入完成，因此可以安全地进行下一步操作。相比之下，`callback` 的下载进度达到 $100\%$ 也并不意味着文件写入完成，它仅适合用于 UI 进度显示等需求。

实际使用时，考虑到下载可能会失败，建议使用 `try...catch` 语句来处理下载错误。下面的实例会介绍用法。

## 示例

这是从网络中下载一个文件的简单示例：

``` js
request.download({
  url: "http://www.rt-thread.com/service/rt-thread.txt",
  filename: "internal://tmp/rt-thread.txt",
})
```

可以通过 `download()` 方法返回值的 `complete` 属性来等待下载完成：
``` js
try {
  await request.download({
    url: "http://www.rt-thread.com/service/rt-thread.txt",
    filename: "internal://tmp/rt-thread.txt"
  }).complete // complete 被拒绝时表示下载失败
  console.log('download finished.')
} catch (e) {
  console.error('download failed:', e)
}
```

这里的 `try...catch` 块用于捕获下载失败的异常。该异常实际是 `DownloadTask.complete` 被拒绝时抛出的错误，所以应该用 `awiat` 等待 `complete` 属性，否则无法捕获到异常。
