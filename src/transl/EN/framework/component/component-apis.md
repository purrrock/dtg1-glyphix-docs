# Component built-in interface


The Glyphix framework has some built-in properties for components, which are accessed using the `this.$xxx` format. These built-in properties provide components with some functionality outside of the reactive framework.


All built-in properties are read-only.


## property


### `$app` <decl type="Applet" get />


Application objects exported in `app.js` can be accessed through the `$app` attribute.


### `$page` <decl type="Component" get />


The component object of the page to which the component belongs can be accessed through the `$page` attribute. For page components, the value of `this.$page` is `this`.


### `$valid` <decl type="boolean" get />


Determine whether the component object is valid. A value of `false` indicates that the component has been destroyed.


::: tip

For a component that has been destroyed, all operations other than accessing the `$valid` attribute are illegal.
:::



#### Component destroyed


The life cycle of components is controlled by the rendering framework. Reasonably written code usually does not access destroyed components, but if you forget to cancel the timer or listener when destroying the component, for example:


``` js
setInterval(() => {
  this.secondCounter += 1
}, 1000)
```


If the component object is destroyed, you may encounter this error:


```
the component object has been destroyed
  stack backtrace:
    at <anonymous> (pkg://com.example.app/main/index.js:50)
TypeError: proxy: cannot set property
  stack backtrace:
    at <anonymous> (pkg://com.example.app/main/index.js:52)
```


If it is really difficult to delete the timer or cancel the listener when the component is destroyed, you can safely determine whether the component is destroyed through the `$valid` attribute. The following example can suppress the above runtime error:


``` js
let timer = setInterval(() => {
  if (this.$valid) {
    this.secondCounter += 1
  } else {
    clearTimeout(timer) // Delete timer after component is destroyed
  }
})
```
Such scenarios (such as multiple timers and event listening functions) generally have a fixed code structure:
1. Use `this.$valid` before accessing component properties to determine whether the component is valid;
2. Perform normal component property access operations in the effective branch;
3. Clean the timer or cancel the listener in the invalid branch, and return immediately to ensure that the component properties are no longer accessed.


::: warning

When using the `$valid` attribute to determine whether a component has been destroyed, special attention needs to be paid to the fact that the closure of the listening function may cause memory leaks. Failure to properly cancel the event listener or timer may cause the closure to still be referenced by the system after the component is destroyed, and thus cannot be garbage collected.
:::



#### Memory leak risk


In JavaScript, a closure refers to the association between a function and variables in its outer scope. When a function is created, it captures the variables in the outer scope and keeps references to those variables even if the outer scope is no longer executing. This means that variables referenced inside the closure still exist in memory until the closure itself is garbage collected.


In the component framework, when you register an event listener or start a timer, you usually pass in a callback function and may capture some properties or context of the component (such as `this` ).


Although the component object itself is properly destroyed by the framework and the memory is released, these closure functions are not cleared. If the event listener or timer callback is not actively removed, these closures may still exist and accumulate over time, causing memory leaks, especially in long-running applications. This leakage may be difficult to detect.


The following example demonstrates a possible memory leak:
``` js
let timer = setInterval(() => {
  if (this.$valid) {
    this.secondCounter += 1;
  }
}, 1000)
```
Although `if (this.$valid)` is used in the callback function to determine whether the component is still valid, thus avoiding errors being thrown after the component is destroyed, this approach does not avoid the problem of memory leaks. The reason is that `$valid` only determines the validity, and judging this attribute can avoid accessing the destroyed component object. But the problem is that because the timer is not closed, the closure of the callback function itself is still referenced, and the closure cannot be garbage collected.


::: tip

In order to avoid this hidden memory leak, you should actively cancel the timer or remove the event listener when the component [destroy](./life-cycle.md#ondestroy), instead of simply relying on `$valid 判断`. Even though `$valid` can prevent inappropriate actions after the component is destroyed, it cannot clean up the closure of the callback function itself.


All JavaScript memory is released when the app exits, so this memory leak does not accumulate over time.
:::



## method


### `$component` <decl type="(name: string, url: string): void" method />


Import a component dynamically (the `<import>` tag can only import components statically), for example:
``` js
this.$component("Name", "url")
```
The string `"Name"` is the name of the imported component, which must be named in camel case; the string `"url"` is the URI of the imported component.


### `$element` <decl type="(id: string): Element | undefined" method />


Returns the [Native child component](native-component.md#原生组件对象) object with the specified ID in the component, or `undefined` if no such subcomponent exists. The `$element()` method will traverse all child nodes of the component, so component instances from other UX files can also be found.


The `$element()` method will match IDs on the entire child component tree after rendering, and is not limited to the child components in the current [component template](template.md). Sometimes you need to be especially careful with this feature, for example with the following template:
``` html
<scroll>
  <MyComponent />
  <div id="panel">...</div>
</scroll>
```
When elements of `id="panel"` also exist in the custom component `MyComponent`, using `this.$element('panel')` will find the child elements in `MyComponent` instead of the `div` elements in the example.


::: tip

The `$element()` method does not work with custom components, even if the `id` attribute is set for the custom component. Since `$element()` accesses the rendered component tree, it must be used in the [`onReady()`](life-cycle.md#onready) life cycle function and after, but cannot be used in [`onInit()`](life-cycle.md#oninit).
:::



Please refer to [this document](README.md#组件对象和方法) to learn how to access the component object returned by the `$element()` method.


### `$emit` <decl type="(event: string, value: any): void" method />


See [Communication between components](communicate) for details.