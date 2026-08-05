# Pop-up

## Import Module

``` js
import prompt from '@system.prompt'
```

## Interface Definition

#### `showToast`
<decl method><pre>
(options: {
  message: string,
  duration?: number,
  important?: boolean
}): void
</pre></decl>

Displays a toast pop-up. A toast is a text pop-up placed at the top layer of the interface. Only one toast instance is displayed in the interface at a time; when there are multiple toast contents, they will be queued and displayed sequentially.

Description of the `options` parameter fields:
- `message`: The text to be displayed.
- `duration`: The duration for which the toast is displayed, in milliseconds (ms). The toast will automatically hide after the timeout duration is reached.
- `important`: Whether it is an important toast, defaulting to `false`. If set to `true`, the application is allowed to pop up the toast while running in the background.

The display style of the toast (font, color, etc.) is determined by the firmware and cannot be modified within the application. There is also a limit on the display duration of the toast, ranging from $200$ to $5000$ milliseconds.

#### `showPopup` <decl type="(options: { uri: string, params?: Object }): Promise<any>" method />

Displays a floating page pop-up. Description of the `options` parameter fields:
- `uri`: The name of the target page, which needs to be registered in `router` within `manifest.json`.
- `params`: Data to be passed during navigation. The properties of the `params` parameter will replace the `data` property values of the target page.

A floating page is a system-level pop-up (similar to a toast or a dialog box), but it is a fully functional page with the highest level of customizability. Unlike regular pages, floating pages are displayed in the system's floating page stack rather than the application's own page stack. Therefore, APIs such as `router.back()` in the [page routing](api/system-router) mechanism cannot operate on floating pages. To close a floating page, you can use the [`router.close()`](system-router.md#close) method.

The display hierarchy of a pop-up is higher than that of the application, so floating pages will be displayed above all application pages. All applications share the same floating page stack, and floating pages determine their display hierarchy based on the order in which they are popped up, meaning that pages popped up earlier are located at the top. The display hierarchy of floating pages is the same as that of dialog boxes, and lower than toasts.

Like `router.push()`, `showPopup()` also returns a Promise object, which is fulfilled after the floating page exits and returns a custom result. For details, please refer to [`router.push()`](system-router.md#push) and [`router.close()`](system-router.md#close).