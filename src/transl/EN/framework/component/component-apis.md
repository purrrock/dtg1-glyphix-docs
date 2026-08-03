# Built-in Component Interfaces

The Glyphix framework provides built-in properties for components, all of which are accessed using the `this.$xxx` format. These built-in properties offer features beyond the reactive framework for components.

All built-in properties are read-only.

## Properties

### `$app` <decl type="Applet" get />

The application object exported in `app.js` can be accessed via the `$app` property.

### `$page` <decl type="Component" get />

The component object of the page to which the component belongs can be accessed via the `$page` property. For page components, the value of `this.$page` is `this`.

### `$valid` <decl type="boolean" get />

Determines whether the component object is valid. A value of `false` indicates that the component has been destroyed.

::: tip
For destroyed components, any operations other than accessing the `$valid` property are illegal.
:::

#### Destroyed Components

The component lifecycle is controlled by the rendering framework, and properly written code typically does not access destroyed components. However, if you forget to cancel timers or listeners when destroying a component, for example:

``` js
setInterval(() => {
  this.secondCounter += 1
}, 1000)
```

If the component object is destroyed, you may encounter an error like this:

```
the component object has been destroyed
  stack backtrace:
    at <anonymous> (pkg://com.example.app/main/index.js:50)
TypeError: proxy: cannot set property
  stack backtrace:
    at <anonymous> (pkg://com.example.app/main/index.js:52)
```

If it is indeed difficult to delete timers or cancel listeners when the component is destroyed, you can use the `$valid` property to safely check whether the component has been destroyed. The following example suppresses the above runtime error:

``` js
let timer = setInterval(() => {
  if (this.$valid) {
    this.secondCounter += 1
  } else {
    clearTimeout(timer) // Delete the timer after the component is destroyed
  }
})
```
Such scenarios (such as recurring timers, event listener functions) generally follow a fixed code structure:
1. Use `this.$valid` to check whether the component is valid before accessing component properties;
2. Execute normal component property access operations in the valid branch;
3. Clear the timer or cancel the listener in the invalid branch, and **return immediately** to ensure that component properties are no longer accessed.

::: warning
When using the `$valid` property to determine whether a component has been destroyed, special attention should be paid to closures in listener functions, which may lead to memory leaks. Failing to correctly cancel event listeners or timers may result in the closure still being referenced by the system after the component is destroyed, preventing it from being garbage collected.
:::

#### Memory Leak Risk

In JavaScript, a closure refers to the association between a function and variables in its outer scope. When a function is created, it captures variables in the outer scope and maintains references to them, even if the outer scope has finished executing. This means that variables referenced inside the closure remain in memory until the closure itself is garbage collected.

In the component framework, when you register an event listener or start a timer, you typically pass a callback function, which may capture certain component properties or context (such as `this`).

Although the component object itself is correctly destroyed and memory is freed by the framework, these closure functions are not cleared. If event listener or timer callbacks are not actively removed, these closures may persist and accumulate over time, leading to memory leaks, especially in long-running applications. Such leaks can be difficult to detect.

The following example demonstrates a potential memory leak:
``` js
let timer = setInterval(() => {
  if (this.$valid) {
    this.secondCounter += 1;
  }
}, 1000)
```
Although `if (this.$valid)` is used inside the callback function to check whether the component is still valid, thereby avoiding throwing errors after the component is destroyed, this approach does not prevent memory leaks. The reason is that `$valid` only checks validity; checking this property prevents accessing an already destroyed component object. However, the problem is that because the timer is not turned off, the closure of the callback function itself is still referenced, and the closure cannot be garbage collected.

::: tip
To avoid such subtle memory leaks, you should actively cancel timers or remove event listeners when the component is [destroyed](./life-cycle.md#ondestroy), rather than relying solely on `$valid`. Even though `$valid` prevents improper operations after a component is destroyed, it cannot clean up the closure of the callback function itself.

All JavaScript memory is released after the application exits, so such memory leaks will not accumulate indefinitely.
:::

## Methods

### `$component` <decl type="(name: string, url: string): void" method />

Dynamically imports a component (the `<import>` tag can only import components statically), for example:
``` js
this.$component("Name", "url")
```
The string `"Name"` is the name of the imported component and must use PascalCase; the string `"url"` is the URI of the imported component.

### `$element` <decl type="(id: string): Element | undefined" method />

Returns the [native subcomponent](native-component.md#原生组件对象) object with the specified ID in the component, or `undefined` if no such subcomponent exists. The `$element()` method traverses all child nodes of the component, so component instances in other UX files can also be found.

The `$element()` method matches IDs across the entire rendered subcomponent tree and is not limited to subcomponents in the current [component template](template.md). Sometimes you need to be especially careful with this feature. For example, given the following template:
``` html
<scroll>
  <MyComponent />
  <div id="panel">...</div>
</scroll>
```
When an element with `id="panel"` also exists inside the custom component `MyComponent`, using `this.$element('panel')` will find the child element inside `MyComponent` instead of the `div` element in the example.

::: tip
The `$element()` method cannot be used for custom components, even if the `id` property is set for the custom component. Because `$element()` accesses the rendered component tree, it must be used in or after the [`onReady()`](life-cycle.md#onready) lifecycle method, and cannot be used in [`onInit()`](life-cycle.md#oninit).
:::

Please refer to [this documentation](README.md#组件对象和方法) to learn how to access the component object returned by the `$element()` method.

### `$emit` <decl type="(event: string, value: any): void" method />

See [Inter-component Communication](communicate) for details.
