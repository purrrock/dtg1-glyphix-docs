# application framework


The Glyphix application is a standalone, interactive application designed for MCU (Microcontroller) devices. It consists of a series of pages, components and related logic, and is supported and managed by the runtime environment. With the Glyphix application framework, developers can build and organize applications using HTML templates, CSS, and JavaScript in a way close to web development.


You can think of apps as standalone programs like mobile apps: they can be installed, launched, switched, and uninstalled. Each application has its own resources and data storage space, and runs in a controlled environment.


## runtime


The runtime is a native system integrated into the device firmware. It provides a standard application running environment and manages all system resources required by the application. This section introduces the various responsibilities of the runtime and their standards of behavior.


### Start application


The runtime can launch an application through native or JavaScript interfaces. Each application has an independent running environment, which means:
- Applications run in independent JavaScript execution environments and do not interfere with each other.
- Each application's resource access is independent, including page structure, file resources, data storage and other resources.
- No underlying permissions: The application's running environment has nothing to do with the underlying system, so it cannot access underlying resources beyond the runtime.


However, some resources are globally unique, such as the visible area of ​​the screen, public file directories, etc. As the user operates, some applications will become interactive in the foreground, while other applications will switch to the background.


### Page management


The interface of the Glyphix application is mainly provided by the page, so the page object of each application will be maintained during runtime and the global pop-up page will be managed. These management mechanisms include page switching, rendering and life cycle control.


### Memory resource management


The runtime system uniformly manages memory and various system resources between the application itself and multiple applications to optimize overhead and avoid leaks:
- Delay the loading of images, text and other resources to reduce the delay in interface loading.
- Cache and optimize page and component files to accelerate hot loading performance.
- Maintain resource and underlying file mapping to implement device-independent IO and resource access.
- Optimize memory usage to avoid exhausting MCU memory.


### Resource recovery


When the app exits, the runtime reclaims all resources, releasing system usage to the level it was before the app was launched. This is a system mechanism that cannot be controlled at the application level, which also means:
- Pending Promise objects are not honored when the app exits, so asynchronous operations may never get results. Please pay attention to do the necessary processing in the application's [`onDestroy`](/framework/component/life-cycle.md#ondestroy-1) life cycle function.
- The underlying system may kill the application at any time and has full and complete operating rights. Absolute keepaliveness cannot be achieved at the application level, and the application scheduling policy of the device cannot be assumed.


### Standard interface


The runtime provides a standard set of [API](/api/README.md) s that abstract differences in Bluetooth, network, sensor, and system functionality on specific devices. Most APIs are supported by all devices, but some are only supported by specific devices.


### Backend management


The application framework supports background running of applications, which allows users to return to the current application after returning to interfaces such as the application list without restarting the application. Applications running in the background will be subject to some restrictions, such as:
- Background applications cannot jump to pages, and APIs such as [`router.push()`](/api/system-router.md#push) will hang directly.
- The background application may automatically return to the main page (that is, the bottom page), just like the user returns manually.
- Most apps can only stay in the background briefly and are killed by the system in about half a minute to free up resources.
- Apps that are performing specific tasks such as audio playback can continue to run in the background.


::: tip

If your application needs to play audio in the background (such as a podcast application), please make sure to start the audio playback task in the main page or interface-independent script, rather than playing it in a deep page. Otherwise, audio playback may be interrupted and background persistence lost when the background app returns to the home page.
:::



The background mechanism of the application involves a series of life cycle management, see [Application life cycle](../component/life-cycle.md) for details.


## page


The application will be divided into multiple pages, which is similar to an HTML page: each page implements a type of interactive logic, and multiple pages can jump to each other.


A page is an interface element that fills the entire screen, so only one page can be displayed on the device at the same time. To this end, the application framework provides a page stack mechanism: each application can open some pages during runtime. These pages are maintained in a stack manner, and only the top page is displayed. Because the page stack is a stack, it supports push and pop operations, which allow you to add new pages to the application's page stack or close the top page. In addition, the application framework has also expanded some practical page operations.


Most pages exist in the application's page stack. When the application is in the foreground (that is, it is the displayed application), the page at the top of the page stack is displayed, while all pages in the background application are not displayed. The page stacks between each application are completely independent.


A page consists of a **page component** and several sub-components. All pages must be declared in [`manifest.json`](manifest.md#router) before they can be used. Pages within the application are navigated and switched through the [`system.router`](/api/system-router.md) API, which includes a set of routing mechanisms and data transfer methods between pages.


The page uses a stacked layout by default, just like the [`stack`](/components/stack.md) component, so use a template like this in the page component:
``` html
<scroll>
  <p>background</p>
</scroll>
<p>overlay</p>
```


Has the same effect as placing it inside a `stack` component:
``` html
<stack>
  <scroll>
    <p>Background</p>
  </scroll>
  <p>Overlay</p>
</stack>
```


This stacking effect can be observed using the interactive demo below, where you can use your mouse or touchpad to scroll through the "Background" text and observe the stacked levels.


<glyphix id="application-page-component" height="200" width="300" title="页面组件堆叠效果">


``` html
<scroll>
  <p>Background</p>
</scroll>
<p>Overlay</p>
```


``` css
p {
  text-align: center;
  color: #f088;
  font-size: 1.5rem;
}

scroll>p {
  height: 100%;
  color: black;
  font-size: 1.25rem;
}
```


</glyphix>



## components


See [component framework](/framework/component/README.md) for details.