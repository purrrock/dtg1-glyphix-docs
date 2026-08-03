# Pop-up window

## Import module

``` js
import prompt from '@system.prompt'
```

## Interface definition

#### `showToast`
<decl method><pre>
(options: {
  message: string,
  duration?: number,
  important?: boolean
}): void
</pre></decl>

Display a toast pop-up box. Toast is a text pop-up box placed on top of the interface. Only one instance of toast is displayed in the interface. If there are multiple toast contents, they will be queued and displayed in sequence.

Description of the `options` parameter field:
- `message`: requires realistic text.
- `duration`: the display duration of the toast, in ms. The toast will be automatically hidden after the timeout period is reached.
- `important`: Whether it is an important toast, the default is `false`. If set to `true`, allows this toast to pop up when the app is in the background.

The toast display style (font, color, etc.) is determined by the firmware and cannot be modified in the application. There is also a limit on how long a toast can be displayed, ranging from $200$ to $5000$ milliseconds.

#### `showPopup` <decl type="(options: { uri: string, params?: Object }): Promise<any>" method />

Display a floating page pop-up window. `options` parameter field description:
- `uri`: The name of the target page, which needs to be registered in `router` of `mainfest.json`.
- `params`: The data that needs to be passed when jumping. The attribute of the `params` parameter will replace the `data` attribute value of the target page.

A floating page is a system-level pop-up window (similar to a toast or a dialog box), but a floating page is a fully functional page with the highest customizability. Unlike ordinary pages, floating pages are displayed in the system's floating page stack instead of applying their own page stack. Therefore, APIs such as `router.back()` in the [Page Routing](api/system-router) mechanism cannot operate floating pages. If you want to close the floating page, you can use the [`router.close()`](system-router.md#close) method.

The display level of the pop-up window is higher than that of the application, so the floating page will be displayed on top of all application pages. All applications use the same floating page stack. The display level of floating pages is determined by the pop-up order, that is, the page that popped up earlier is at the top. The display level of the floating page is the same as the dialog box, lower than the toast.

Like `router.push()`, `showPopup()` also returns a Promise object, which will be honored and return a custom result after the floating page exits. Please refer to [`router.push()`](system-router.md#push) and [`router.close()`](system-router.md#close) for details.
