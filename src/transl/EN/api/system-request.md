# Upload download request

## Import module

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

Download files through the HTTP/HTTPS protocol. The functions of each field of the `options` parameter are:
- `url`: the URL of the website to be accessed;
- `header`: an object containing HTTP request header information, the key and value are strings. Typical HTTP header fields can be `Authorization`, `Content-Type`, etc.;
- `filename`: URI that stores downloaded files, such as: `internal://files/download.txt`;
- `callback`: Download progress callback function. This function will be called multiple times during downloading. `progress` is the progress value of the download, ranging from $[0, 100]$.

The `download()` method returns a [`DownloadTask`](#downloadtask) object, which can be used to wait for the download to complete or control the download task.

::: warning
Please do not use the download progress to reach $100\%$ in the `callback` function as the trigger condition for the operation after the download is completed. For details, please refer to [Waiting for downloading to complete](#Waiting for downloading to complete).

The current implementation does not automatically parse the `filename` parameter attribute based on `url`. Please be sure to fill in `filename`.
:::

## type

### `DownloadTask`

`DownloadTask` is the return type of the `download` method, and its signature is:

``` ts
interface DownloadTask {
  complete: Promise<void>,
  cancel(): void
}
```

The `complete` property is a `Promise` object that can be used to wait for the download to complete. The `cancel()` method is used to cancel the ongoing download task. If the download has been completed, the `cancel()` method has no effect.

#### Wait for download to complete

Use `DownloadTask.complete` to wait for the download to complete. When the `Promise` is fulfilled, it will ensure that the file has been written, so it is safe to proceed to the next step. In contrast, when the download progress of `callback` reaches $100\%$, it does not mean that the file writing is completed. It is only suitable for UI progress display and other needs.

In actual use, considering that the download may fail, it is recommended to use the `try...catch` statement to handle download errors. The following examples will introduce usage.

## Example

Here is a simple example of downloading a file from the network:

``` js
request.download({
  url: "http://www.rt-thread.com/service/rt-thread.txt",
  filename: "internal://tmp/rt-thread.txt",
})
```

You can wait for the download to complete through the `complete` attribute of the `download()` method return value:
``` js
try {
  await request.download({
    url: "http://www.rt-thread.com/service/rt-thread.txt",
    filename: "internal://tmp/rt-thread.txt"
  }).complete // When complete is rejected, it means the download failed
  console.log('download finished.')
} catch (e) {
  console.error('download failed:', e)
}
```

The `try...catch` block here is used to catch exceptions when the download fails. This exception is actually an error thrown when `DownloadTask.complete` is rejected, so you should use `awiat` to wait for the `complete` attribute, otherwise the exception cannot be caught.
