# 测试框架

## 导入模块

``` js
import test from '@system.test'
```

## 简介

`system.test` 模块是一个端到端测试框架，可以通过编程来模拟用户操作，并检查界面行为是否符合预期。

一个简单的模拟用户操作的代码如下：
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
这段代码会自动等待界面中的元素被渲染，并通过滚动手势让被遮挡的元素进入可视区域内，然后对其执行点击或滚动等手势。

## API

### 辅助函数

这些函数在测试中提供辅助功能，如延时等。

#### `wait` <decl method type="(duration: number): Promise<void>" />

异步延时指定的时间，用来在测试中等待某些操作，或者模拟用户的停顿。

### 定位器

定位器从应用的顶层页面查找元素（原生组件），例如根据元素的 tag 或者 id 来查找。定位器的进一步介绍请参考 [`Locator` 对象](#locator-对象)。

#### `getByTag` <decl method type="(tag: string): Locator" />

通过 `tag` 定位元素。目前只支持大驼峰命名，如 `'P'`、`'Swiper'` 等。

#### `getByClass` <decl method type="(class: string): Locator" />

通过 `class` 属性定位元素。

#### `getById` <decl method type="(id: string): Locator" />

通过 `id` 属性定位元素。

#### `getHasText` <decl method type="(text: RegExp | string): <Locator>" />

通过元素的 `text` 属性是否与 `text` 参数匹配来定位元素。`text` 参数是一个正则表达式，例如：
- `/hello/` 测试元素的 `text` 属性值中是否包含 `'hello'` 字串；
- `/^hello/` 测试元素的 `text` 属性值的开头是否为 `'hello'`；
- `/^hello$/` 测试元素 `text` 属性值是否为 `'hello'`。

`text` 参数的匹配规则和 [`RegExp.test()`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/RegExp/test) 相同。

### `Locator` 对象

`Locator` 对象由定位器 API 返回，可用于进一步的操作。所有的定位器操作都会尝试自动等待元素出现并会将其移动到可视范围内。

#### `click` <decl method type="(): Promise<void>" />

当元素存在并已经滚动到可视区域内后，后在元素的位置上模拟一个点击手势。

#### `scroll` <decl method type="(dx: number, dy: number, duration?: number): Promise<void>" />

当元素存在并已经滚动到可视区域内后，后在元素的位置上模拟一个滚动手势。`dy` 和 `dy` 是滚动的 $(x, y)$ 偏移量，单位为像素；可选的 `duration` 为手势的时间，单位为秒，默认值为 $0.5 \rm s$。

该方法会等待元素的 `scrolled` 属性变为 `false` 才会 polyfill 返回的 Promise 对象。因此对于 `scroll`、`swiper` 等组件来说，`scroll()` 方法会在这些组件的惯性动画已经停止之后才会触发下一步操作。

#### `wait` <decl method type="(): Promise<void>" />

等待元素存在并滚动到可视区域内，但是不模拟任何手势或其他操作。
