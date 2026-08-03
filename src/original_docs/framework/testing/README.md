# 测试框架

Glyphix 提供了一套应用的自动化测试框架，用于模拟用户操作并检查界面行为。该测试框架并不是随机模拟操作，而是需要开发者编写测试用例。

## 基本概念

Glyphix 的测试框架实际上是一组 JavaScript API，它们大体上实现以下功能：

- 注册测试用例
- 查找界面元素
- 模拟用户操作或动作
- 断言和验证逻辑

### 测试步骤

一个测试步骤的基本原理是**查找特定元素**、**执行模拟动作**和（可选的）**验证内容**。例如：

1. 查找一个 CSS 类为 `play-button` 的元素；
2. 点击这个元素；
3. 不验证内容。

在实际界面中，`.play-button` 也许是一个播放按钮，点击此按钮后会开始播放音乐。这个测试对应的 JavaScript 代码如下：

```js
await tc.getByClass("play-button").click();
```

该测试代码会自动等待 `.play-button` 元素出现并将其移动到界面视口内，然后再点击该元素。这些测试 API 会自动等待界面中的动画或者手势，并且会在点击手势完全完成后兑现 `await`。因此，通常不需要手动移动元素，也不需要显式地等待操作完成。

### 查找元素

测试框架提供了一系列接口来查找界面中的元素，例如：

- `tc.getByClass()`：根据类名查找元素；
- `tc.getByTag()`：根据 tag 名查找元素。

这些接口都会等待元素出现并会在下一步操作之前尝试将元素移动到可视区域内。

### 模拟用户操作

## 开始编写测试

### 测试用例文件

Glyphix 的测试用例是一些 JavaScript 代码，并且存储在应用的资源包内。建议将测试用例单独存放在项目的 `src/tests` 目录下，例如：

```shell
<app-name>
├─ README.md         # 项目自述文件
└─ src               # 项目的源代码目录
    ├─ app.js        # app 入口脚本文件
    ├─ manifest.json # 配置应用基本信息
    ├─ tests         # 存放所有的测试用例
    │  └─ spec.js    # 测试用例代码
    └─ Main          # 存放主页面的目录
        └─ index.ux  # 主页面的界面描述文件
```

这个例子中的测试代码就是 `src/tests/spec.js` 文件，还可以根据需要创建多个测试文件。

::: tip
测试用例的文件名通常是 spec，即 specification 的缩写。spec 文件用于定义和描述软件的预期行为及其功能，通常包含一组测试用例，用于验证软件是否按照预期工作。
:::

### 编写测试用例

假设我们的应用有一个主页面，并且存在一个类名为 `clickable` 的 `span` 元素：

```html
<div>
  <span class="clickable" on:click="console.log('click span')"> click me </span>
</div>
```

现在，我们要编写一个自动测试脚本，它会点每隔一秒钟点击一次 `span` 组件，并且在点击 3 次之后结束测试。为此，我们要在 `src/tests/spec.js` 中添加以下代码：

```js
// 导入 @system.test 模块提供测试框架的 API
import tc from "@system.test";

// 注册一个名为 click-test 的自动化测试用例
tc.testcase("click-test", async () => {
  for (let i = 0; i < 3; ++i) {
    // 查找 class="clickable" 的元素并点击它
    await tc.getByClass("clickable").click();
    // 等待一秒钟
    await tc.wait(1);
  }
});
```

接下来还需要注册这个测试脚本并启动测试。

### 注册测试脚本

一般的代码中通常会使用 `import 'tests/spec.js'` 这样的语句来引入脚本，但这会导致总是加载该 JavaScript 模块。为了优化应用的加载速度和内存占用，我们不需要在非测试环境中引入这些脚本。为此，你可以在 `src/app.js` 文件中的 App 对象中注册测试脚本：

```js
export default {
  // 使用 testsuite 属性来注册测试脚本列表
  testsuite: ["tests/spec.js"],
  onCreate() {
    /* ... */
  },
  // ...
};
```

这种方法不会立即导入这些测试脚本，而是会延迟到执行测试的时候再导入。因此在不执行测试的时候，使用 `testsuite` 属性并不会增加开销，开发者也无需考虑优化加载测试脚本带来的性能负担。

::: warning
即便只有一个测试脚本，`testsuite` 属性也要是一个 `Array` 对象，而测试脚本的路径包含在其中，就像本节的示例一样。测试脚本的路径总是相对于 `app.js` 文件所在的目录，你也可以使用绝对路径，例如 `/tests/spec.js`。
:::

## 运行测试用例

### 模拟器

要运行测试用例，应使用 `gx emu -i` 命令来启动模拟器。你会在终端中看到这样的信息：

```shell
❯ gx emu -i
[emu] Open inspector http://localhost:14200 in browser.
```

接下来在浏览器中打开 `http://localhost:14200` 链接，并进入“Console” 选项卡，然后在底部的“RPC”栏输入以下文本：
```json
{"fn": "test.start", "name": "click-test"}
```
即可启动前面编写的 `click-test` 测试用例，此时你应该在日志浏览器中看到以下日志：

```log
19:14:33.320 [inspector] test com.example.app . click-test started
19:14:33.640 [js] 'click span'
19:14:35.090 [js] 'click span'
19:14:36.510 [js] 'click span'
19:14:37.600 [tester] com.example.app testcase click-test finished
```

这表明测试已经成功执行，并且 `span` 元素确实被点击了 $3$ 次。
