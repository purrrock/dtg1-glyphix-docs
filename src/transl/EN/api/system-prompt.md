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

Description of `options` parameter fields:
- `message`: The text to be displayed.
- `duration`: The display duration of the toast in milliseconds (ms). The toast will automatically hide after reaching this timeout.
- `important`: Whether it is an important toast. The default is `false`. If set to `true`, the application is allowed to pop up this toast while in the background.

The display style of the toast (font, color, etc.) is determined by the firmware and cannot be modified within the application. There is also a limit on the display duration of the toast, which ranges from $200$ to $5000$ milliseconds.

#### `showPopup` <decl type="(options: { uri: string, params?: Object }): Promise<any>" method />

Displays a floating page pop-up. Description of `options` parameter fields:
- `uri`: The name of the target page, which needs to be registered in `router` of `manifest.json`.
- `params`: Data to be passed during navigation. The properties of the `params` parameter will replace the `data` property values of the target page.

A floating page is a system-level pop-up (similar to a toast or dialog box), but it is a fully functional page with the highest level of customizability. Unlike general pages, a floating page is displayed in the system's floating page stack rather than the application's own page stack. Therefore, APIs such as `router.back()` in the [page routing](api/system-router) mechanism cannot operate on floating pages. To close a floating page, you can use the [`router.close()`](system-router.md#close) method.

The display hierarchy of a pop-up is higher than that of the application, so floating pages will be displayed above all application pages. All applications share the same floating page stack, and the display hierarchy of floating pages is determined by their pop-up order, meaning that earlier popped-up pages are located at the top. The display hierarchy of a floating page is the same as that of a dialog box, and lower than that of a toast.

Just like `router.push()`, `showPopup()` also returns a Promise object, which will be fulfilled and return a custom result after the floating page exits. For details, please refer to [`router.push()`](system-router.md#push) and [`router.close()`](system-router.md#close).