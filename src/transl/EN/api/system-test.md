# Test Framework

## Importing Modules

``` js
import test from '@system.test'
```

## Introduction

The `system.test` module is an end-to-end testing framework that allows you to programmatically simulate user operations and check whether the UI behavior matches expectations.

Here is a simple example of code that simulates user operations:
``` js
await test.getByClass('play-button').click()
await test.getByClass('more-button').click()
await test.getByClass('download-button').click()
await test.getByClass('close-button').click()
await test.getByClass('menu-button').click()
await test.getHasText('下载列表').click()
await test.getByTag('Scroll').scroll(0, -200, 0.3)
await test.getHasText(/[a-z]/).click()
```
This code automatically waits for elements in the UI to be rendered, brings occluded elements into the visible area via scrolling gestures, and then performs gestures such as clicking or scrolling on them.

## API

### Helper Functions

These functions provide auxiliary features in tests, such as delays.

#### `wait` <decl method type="(duration: number): Promise<void>" />

Asynchronously delays for a specified time, used to wait for certain operations in tests or to simulate user pauses.

### Locators

Locators find elements (native components) from the top-level page of the application, such as by element tag or ID. For more information about locators, please refer to the [`Locator` Object](#locator-object).

#### `getByTag` <decl method type="(tag: string): Locator" />

Locates elements by `tag`. Currently, only UpperCamelCase is supported, such as `'P'`, `'Swiper'`, etc.

#### `getByClass` <decl method type="(class: string): Locator" />

Locates elements by the `class` attribute.

#### `getById` <decl method type="(id: string): Locator" />

Locates elements by the `id` attribute.

#### `getHasText` <decl method type="(text: RegExp | string): <Locator>" />

Locates elements based on whether their `text` attribute matches the `text` parameter. The `text` parameter is a regular expression, for example:
- `/hello/` tests whether the `text` attribute value of the element contains the substring `'hello'`;
- `/^hello/` tests whether the `text` attribute value of the element starts with `'hello'`;
- `/^hello$/` tests whether the `text` attribute value of the element is `'hello'`.

The matching rules for the `text` parameter are the same as [`RegExp.test()`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/RegExp/test).

### `Locator` Object

`Locator` objects are returned by locator APIs and can be used for further operations. All locator operations attempt to automatically wait for the element to appear and bring it into the visible area.

#### `click` <decl method type="(): Promise<void>" />

Simulates a click gesture at the element's position after the element exists and has been scrolled into the visible area.

#### `scroll` <decl method type="(dx: number, dy: number, duration?: number): Promise<void>" />

Simulates a scroll gesture at the element's position after the element exists and has been scrolled into the visible area. `dx` and `dy` are the $(x, y)$ scroll offsets in pixels; the optional `duration` is the duration of the gesture in seconds, with a default value of $0.5 \rm s$.

This method waits for the element's `scrolled` property to become `false` before resolving the Promise object returned. Therefore, for components such as `scroll` and `swiper`, the `scroll()` method will trigger the next operation only after the inertia animation of these components has stopped.

#### `wait` <decl method type="(): Promise<void>" />

Waits for the element to exist and be scrolled into the visible area, without simulating any gestures or other operations.