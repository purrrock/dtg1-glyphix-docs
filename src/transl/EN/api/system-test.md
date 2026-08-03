# Test framework

## Import module

``` js
import test from '@system.test'
```

## Introduction

The `system.test` module is an end-to-end testing framework that can simulate user operations through programming and check whether the interface behavior is as expected.

A simple code to simulate user operations is as follows:
``` js
await test.getByClass('play-button').click()
await test.getByClass('more-button').click()
await test.getByClass('download-button').click()
await test.getByClass('close-button').click()
await test.getByClass('menu-button').click()
await test.getHasText('Download list').click()
await test.getByTag('Scroll').scroll(0, -200, 0.3)
await test.getHasText(/[a-z]/).click()
```
This code will automatically wait for the elements in the interface to be rendered, use scrolling gestures to bring the occluded elements into the visible area, and then perform gestures such as clicking or scrolling on them.

## API

### Auxiliary functions

These functions provide auxiliary functions in testing, such as delays, etc.

#### `wait` <decl method type="(duration: number): Promise<void>" />

The time specified by the asynchronous delay is used to wait for certain operations in the test, or to simulate user pauses.

### Locator

The locator finds elements (native components) from the top-level page of the application, for example, based on the element's tag or id. For further introduction to locators, please refer to [`Locator` object](#locator-object).

#### `getByTag` <decl method type="(tag: string): Locator" />

Locate elements via `tag`. Currently, only big camel case names are supported, such as `'P'`, `'Swiper'`, etc.

#### `getByClass` <decl method type="(class: string): Locator" />

Locate elements via the `class` attribute.

#### `getById` <decl method type="(id: string): Locator" />

Locate elements via the `id` attribute.

#### `getHasText` <decl method type="(text: RegExp | string): <Locator>" />

Locate elements by whether their `text` attribute matches the `text` parameter. The `text` parameter is a regular expression, for example:
- `/hello/` tests whether the `text` attribute value of the element contains the `'hello'' string;
- `/^hello/` tests whether the value of the element's `text` attribute starts with `'hello'';
- `/^hello$/` tests whether the element's `text` attribute value is `'hello'`.

The matching rules for the `text` parameter are the same as [`RegExp.test()`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/RegExp/test).

### `Locator` object

`Locator` objects are returned by the locator API and can be used for further operations. All locator operations attempt to automatically wait for the element to appear and move it into view.

#### `click` <decl method type="(): Promise<void>" />

When the element exists and has been scrolled into the visible area, simulate a click gesture at the element's position.

#### `scroll` <decl method type="(dx: number, dy: number, duration?: number): Promise<void>" />

When the element exists and has been scrolled into the visible area, simulate a scroll gesture at the element's position. `dy` and `dy` are the $(x, y)$ offset of the scrolling, in pixels; the optional `duration` is the duration of the gesture, in seconds, and the default value is $0.5 \rm s$.

This method will wait for the element's `scrolled` attribute to become `false` before polyfilling the returned Promise object. Therefore, for components such as `scroll` and `swiper`, the `scroll()` method will not trigger the next operation until the inertial animation of these components has stopped.

#### `wait` <decl method type="(): Promise<void>" />

Waits for the element to exist and scroll into view, but does not simulate any gestures or other operations.
