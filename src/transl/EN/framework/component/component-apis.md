# Component Built-in Interfaces

The Glyphix framework provides several built-in properties for components, all of which are accessed using the `this.$xxx` format. These built-in properties offer functionalities beyond the reactive framework.

All built-in properties are read-only.

## Properties

### `$app` <decl type="Applet" get />

The `$app` property allows you to access the application object exported from `app.js`.

### `$page` <decl type="Component" get />

The `$page` property allows you to access the component object of the page to which the component belongs. For page components, the value of `this.$page` is `this`.

### `$valid` <decl type="boolean" get />

Determines whether the component object is valid. A value of `false` indicates that the component has been destroyed.

::: tip
For destroyed components, any operation other than accessing the `$valid` property is illegal.
:::

#### Destroyed Components

The component lifecycle is controlled by the rendering framework. Well-written code typically does not access destroyed components, but if you forget to cancel timers or listeners upon component destruction, for example:

``` js
setInterval(() => {
  this.secondCounter += 1
}, 1000)
```

If the component object is destroyed, you might encounter an error like this:

```
the component object has been destroyed
  stack backtrace:
    at <anonymous> (pkg://com.example.app/main/index.js:50)
TypeError: proxy: cannot set property
  stack backtrace:
    at <anonymous> (pkg://com.example.app/main/index.js:52)
```

If it is indeed difficult to clear timers or cancel listeners when the component is destroyed, you can use the `$valid` property to safely check whether the component has been destroyed. The following example suppresses the aforementioned runtime error:

``` js
let timer = setInterval(() => {
  if (this.$valid) {
    this.secondCounter += 1
  } else {
    clearTimeout(timer) // Clear the timer after the component is destroyed
  }
})
```
Such scenarios (such as recurring timers or event listener functions) generally follow a fixed code structure:
1. Use `this.$valid` to check if the component is valid before accessing component properties;
2. Execute normal component property access operations in the valid branch;
3. Clear timers or cancel listeners in the invalid branch, and **return immediately** to ensure component properties are no longer accessed.

::: warning
When using the `$valid` property to determine whether a component has been destroyed, pay special attention to the possibility that closures in listener functions may cause memory leaks. Failing to properly cancel event listeners or timers can cause the system to retain references to these closures even after the component is destroyed, preventing them from being garbage-collected.
:::

#### Memory Leak Risks

In JavaScript, a closure refers to the association between a function and variables in its outer scope. When a function is created, it captures variables in the outer scope and maintains references to them, even after the outer scope has finished executing. This means that variables referenced inside the closure remain in memory until the closure itself is garbage-collected.

In the component framework, when you register an event listener or start a timer, you typically pass a callback function, which may capture certain properties or the context of the component (such as `this`).

Although the component object itself is correctly destroyed and its memory freed by the framework, these closure functions are not cleared. If event listener or timer callbacks are not actively removed, these closures may persist and accumulate over time, leading to memory leaks—especially in long-running applications. Such leaks can be difficult to notice.

The following example demonstrates a potential memory leak:
``` js
let timer = setInterval(() => {
  if (this.$valid) {
    this.secondCounter += 1;
  }
}, 1000)
```
Although `if (this.$valid)` is used inside the callback function to check whether the component is still active, thereby avoiding errors thrown after component destruction, this approach does not prevent memory leaks. The reason is that `$valid` only checks validity; checking this property prevents access to already destroyed component objects. However, because the timer is not stopped, the closure of the callback function itself is still referenced, and that closure cannot be garbage-collected.

::: tip
To avoid this subtle memory leak, you should actively cancel timers or remove event listeners when the component is [destroyed](./life-cycle.md#ondestroy), rather than relying solely on the `$valid` check. Even though `$valid` prevents improper operations from executing after component destruction, it cannot clean up the closures of the callback functions themselves.

All JavaScript memory is released after the application exits, so such memory leaks do not accumulate indefinitely.
:::

## Methods

### `$component` <decl type="(name: string, url: string): void" method />

Dynamically imports a component (the `<import>` tag can only import components statically), for example:
``` js
this.$component("Name", "url")
```
The string `"Name"` is the name of the imported component and must use PascalCase; the string `"url"` is the URI of the imported component.

### `$element` <decl type="(id: string): Element | undefined" method />

Returns the [native sub-component](native-component.md#原生组件对象) object with the specified ID within the component, or `undefined` if no such sub-component exists. The `$element()` method traverses all child nodes of the component, allowing component instances in other UX files to be found as well.

The `$element()` method matches IDs across the entire rendered sub-component tree, not limiting itself to sub-components in the current [component template](template.md). Sometimes you need to be very careful with this feature. For example, consider the following template:
``` html
<scroll>
  <MyComponent />
  <div id="panel">...</div>
</scroll>
```
When an element with `id="panel"` also exists inside the custom component `MyComponent`, using `this.$element('panel')` will find the child element inside `MyComponent` rather than the `div` element in the example.

::: tip
The `$element()` method cannot be used on custom components, even if the `id` property is set for the custom component. Because `$element()` accesses the rendered component tree, it must be used in or after the [`onReady()`](life-cycle.md#onready) lifecycle method, and cannot be used in [`onInit()`](life-cycle.md#oninit).
:::

Please refer to [this documentation](README.md#组件对象和方法) to learn how to access the component object returned by the `$element()` method.

### `$emit` <decl type="(event: string, value: any): void" method />

For details, see [Inter-component Communication](communicate).