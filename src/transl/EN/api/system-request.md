# Upload and Download request

## Import Module

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

Downloads a file via the HTTP/HTTPS protocol. The fields of the `options` parameter are described as follows:
- `url`: The URL of the website to access;
- `header`: An object containing HTTP request header information, with keys and values as strings. Typical HTTP header fields can be `Authorization`, `Content-Type`, etc.;
- `filename`: The URI for storing the downloaded file, e.g., `internal://files/download.txt`;
- `callback`: The download progress callback function. This function will be called multiple times during the download, where `progress` is the download progress value ranging from $[0, 100]$.

The `download()` method returns a [`DownloadTask`](#downloadtask) object, which can be used to wait for the download to complete or to control the download task.

::: warning
Please do not use the download progress reaching $100\%$ in the `callback` function as the trigger condition for operations after the download is complete. For details, please refer to [Waiting for Download Completion](#waiting-for-download-completion).

The current implementation does not automatically resolve the `filename` parameter property based on the `url`, so please make sure to fill in `filename`.
:::

## Types

### `DownloadTask`

`DownloadTask` is the return type of the `download` method, and its signature is:

``` ts
interface DownloadTask {
  complete: Promise<void>,
  cancel(): void
}
```

The `complete` property is a `Promise` object that can be used to wait for the download to complete. The `cancel()` method is used to cancel an ongoing download task. If the download has already completed, the `cancel()` method has no effect.

#### Waiting for Download Completion

Use `DownloadTask.complete` to wait for the download to complete. When this `Promise` is fulfilled, it guarantees that the file has been completely written, making it safe to proceed to the next step. In contrast, the download progress reaching $100\%$ in `callback` does not mean the file writing is complete; it is only suitable for requirements such as UI progress display.

In practical use, considering that downloads may fail, it is recommended to use a `try...catch` statement to handle download errors. The example below demonstrates the usage.

## Examples

Here is a simple example of downloading a file from the network:

``` js
request.download({
  url: "http://www.rt-thread.com/service/rt-thread.txt",
  filename: "internal://tmp/rt-thread.txt",
})
```

You can use the `complete` property of the return value of `download()` to wait for the download to complete:
``` js
try {
  await request.download({
    url: "http://www.rt-thread.com/service/rt-thread.txt",
    filename: "internal://tmp/rt-thread.txt"
  }).complete // When complete is rejected, it indicates that the download failed
  console.log('download finished.')
} catch (e) {
  console.error('download failed:', e)
}
```

The `try...catch` block here is used to catch exceptions caused by download failures. This exception is actually the error thrown when `DownloadTask.complete` is rejected, so `await` must be used with the `complete` property, otherwise the exception cannot be caught.