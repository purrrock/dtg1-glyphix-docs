---
title: 开发速览：从 Web 到 Glyphix
icon: compass
---

# 开发速览：从 Web 到 Glyphix

本文档专为熟悉 Web 前端（特别是 Vue.js）的开发者设计。我们将跳过基础语法教学，直接切入 Glyphix 框架的核心机制，帮助你快速建立正确的心智模型。

## 核心概念与运行环境

Glyphix 是一个运行在 MCU（微控制器）设备上的应用框架。虽然它使用 HTML/CSS/JS 进行开发，但它**不是**一个浏览器。本框架用于开发完整应用，而不是可刷新的页面，每个应用运行在独立的沙箱容器中。

你需要理解以下几个核心差异：
- **无 DOM**：底层由 C++ 原生引擎直接渲染，不存在 DOM 树。
- **无 Web API**：不支持 `window`、`document`、`localStorage` 等浏览器 API。系统能力（网络、存储、传感器）通过 `@system.*` 模块提供。
- **JS 引擎**：使用轻量级 JS 引擎（支持 ES6 标准），但内存极其受限。

### 资源限制

资源限制是与 Web 开发最大的不同点。MCU 设备的 RAM 通常仅有几 MB。这意味着不要使用网络请求加载超大 JSON 数据，或者直接 [`fetch`](../api/system-fetch.md) 一张图片。请牢记以下几点：
- 可以使用 [`@system.request`](../api/system-request.md) 模块将资源下载为文件，`fetch` 则会将响应加载到内存中。
- 图片资源通常存放在应用包内，尺寸尽可能与屏幕分辨率匹配。
- **后台冻结**：应用进入后台（`onHide`）后，通常会在几十秒内被系统挂起或销毁。请注意保存状态。

### 设备形态

Glyphix 应用通常运行在智能手表等小屏设备上。手表的屏幕尺寸通常为 1.5 到 2 英寸左右，典型分辨率为 466×466 像素，但存在圆形、矩形屏幕。低端设备的像素密度可能更低，但尺寸基本相似。这类设备常用触摸屏进行交互，可能支持物理按键或者旋钮，系统透明地处理了大部分交互细节。

通常使用模拟器进行开发和调试，因为真机部署和调试流程还比较碎片化，耗时较长。

### 典型项目结构

这是我们推荐的项目文件结构，这也是快应用标准的结构：
```bash
src/
├─ manifest.json  # 应用清单：配置权限、注册页面路由
├─ app.js         # 应用入口：全局生命周期 (onCreate, onDestroy)
├─ pages/         # 页面目录
│  └─ Main/
│     └─ index.ux # 页面组件
└─ assets/        # 公共资源
  └─ icon.png
```
你可以根据需要引入 [Node.js](nodejs.md) 工具链来管理依赖。也可以按照需要调整目录结构，但 [`src/manifest.json`](/framework/application/manifest.md) 和 `src/app.js` 必须固定在此位置。

## UI 开发

Glyphix 采用 [`.ux`](../framework/component/README.md) 单文件组件（类似 Vue SFC），风格接近 Vue Options API，但也有显著差异。

### Flexbox 布局优先

Web 默认是流式布局（Flow Layout），而 Glyphix 的页面默认为堆叠布局：如果你在页面中放两个 `div`，它们会**重叠**在一起，而不是上下排列。这是因为本框架支持在 `<template>` 中使用多个根节点，例如：
```html
<template>
  <image class="background" src="/assets/bg.png" />
  <div class="content"> ... </div>
</template>
```
默认的堆叠布局对于这种场景通常非常合适。

尽管 `div` 等容器默认使用流式布局，但推荐使用 Flexbox 来进行布局控制。绝大多数容器都应该显式声明 `display: flex`，再结合 `flex-direction` 控制子元素排列方式。

考虑到设备屏幕尺寸差异较大，请特别注意长度单位的使用：
- 在较小的尺寸中使用 `px` 单位，它是逻辑像素，会根据屏幕密度自动缩放。
- 字体应总是使用 `rem` 单位，它由设备厂商定义基准，更符合系统 UX 规范的一致性要求。
- 可以使用百分比（`%`）单位来实现响应式布局，但是目前限制和缺陷较多，请注意调试。

由于屏幕太小，你可能特别需要 [`scroll`](../components/scroll.md) 组件来实现滚动区域。和 Web 不同，`div` 容器本身不支持滚动，也无法使用 `overflow` 属性来控制。

### 模板语法差异

虽然长得像 Vue 模板，但请注意以下区别：
- 指令无 `v-` 前缀：如 `<div if="show">` 或 `<div for="item in items">`
- 事件绑定用 `on`、`@` 均可，如：`<p on:click="handler">`
- 必须使用 `<p>` 等文本组件：`<text>Hello</text>` 可以正常显示，但是 `<div>Hello</div>` 不会渲染任何内容。
- 支持用 `model:prop="state"` 或 `::prop="state"` [双向绑定](../framework/commands/model.md)任意组件属性，只要有和属性同名的事件触发即可。

### 样式限制

CSS 支持是子集：
- 支持类 (`.class`)、ID (`#id`)、标签 (`div`) 和后代 (`.a .b`)。**不支持** `~`、`+`、`>` 等复杂关系选择器。
- **效果限制**：不支持渐变、阴影等效果。暂不支持 `transition` 动画。
- **性能限制**：避免使用 `transform` 来移动或对齐元素。`object-fit` 默认为 `none` 并推荐保持默认。
- 目前不支持动态 `class` 绑定，也不支持 CSS 变量。

## 组件与逻辑

### 脚本模型

组件脚本非常接近 Vue Options API，以下示范指出了主要差异：
```js
export default {
  // 数据模型 (Data)，不需要声明属性，data 属性自动导出为属性
  data: {
    count: 0, // 修改 this.count 会自动触发视图更新
  },
  timer: null, // 非响应式字段直接定义在组件实例上，也可以不声明
  // 生命周期
  onInit() {}, // 数据已初始化，可发起网络请求
  onReady() {}, // 界面已渲染完成
  onDestroy() {}, // 务必在此清理定时器、订阅事件

  // 方法 (Methods)，直接定义在组件对象中
  handleTap() {
    this.count++
    // 触发自定义事件给父组件
    this.$emit('change', { value: this.count })
  }
}
```
其中 `data` 对象中的字段为响应式属性，它目前只支持 JSON 兼容的类型（不支持 `Date`、`Map`、`Set` 等）。如果不需要响应式更新，推荐将字段定义在组件实例（`this`）上。

::: tip
不要使用 `methods` 对象包裹方法，直接定义在组件对象中即可。也不需要使用 `props` 定义属性，`data` 对象中的字段会自动导出为属性。

也不能用 `document.getElementById` 等 DOM API 查找元素。可以使用 [`this.$element()`](../framework/component/component-apis.md#element) 方法获取指定 ID 的元素实例。
:::

### 页面与路由

Glyphix 应用由多个页面组成，页面间通过路由导航。所有页面均需在 `manifest.json` 中的 [`router.pages`](../framework/application/manifest.md#pages) 字段中静态注册。页面组件与普通组件类似，但支持 `onShow` 和 `onHide` 生命周期钩子。

使用 `system.router` 系统模块进行跳转：
```js
import router from '@system.router'

// 跳转并传递参数
router.push({ uri: 'pages/Detail', params: { id: 123 } })
```
::: tip
不要使用其他的路由库，也不要假装在开发单页面应用（SPA）。否则将无法利用转场动效、页面栈管理等现有功能。
:::

### TypeScript 支持

如果使用 Node.js 脚手架创建项目，使用 npm、pnpm 等安装 `glyphix` 和 `typescript` 等依赖后，可以在项目中使用 TypeScript 进行开发。

对于 `.ux` 单文件组件，可以在 `<script>` 标签上添加 `lang="ts"` 属性启用 TypeScript 支持。例如：
```html
<script lang="ts">
import { defineComponent } from 'glyphix'

export default defineComponent({
  data() {
    count: 0: number
  },
  increment() { this.count++ },
})
</script>
```

## 系统能力集成

不要尝试使用浏览器 API，请使用 Glyphix [标准库](../api/README.md)。

### 常用模块速查

| 功能 | Glyphix 模块 | 说明 |
| :--- | :--- | :--- |
| **网络** | [`@system.fetch`](../api/system-fetch.md) | 必须处理异步回调或 Promise |
| **弹窗** | [`@system.prompt`](../api/system-prompt.md) | 提供 Toast 和 Dialog |
| **存储** | [`@system.storage`](../api/system-storage.md) | 同步本地存储，直接读写对象而非字符串 |
| **路由** | [`@system.router`](../api/system-router.md) | 管理页面栈 |
| **日志** | `console.log` | 输出到调试终端，和浏览器一样 |

### 异步编程模式

系统 API 通常支持异步回调和 Promise 两种风格。推荐使用 `async/await` 以保持代码整洁。

```js
import fetch from '@system.fetch'
import prompt from '@system.prompt'

export default {
  onReady() { this.loadData() },
  async loadData() {
    try {
      const response = await fetch.fetch({
        url: 'https://api.example.com/data',
        method: 'GET', // 默认为 GET
        responseType: 'json', // 这样不需要 JSON.parse 手动解析
      })

      if (response.data.code === 200)
        this.data = response.data.data
    } catch (err) {
      prompt.showToast({ message: 'Network Error' })
    }
  }
}
```

## 构建和运行

使用 [`gx emu`](../tutorials/glyphix.js/README.md) 命令启动模拟器，或使用 `gx build` 构建应用包。如果使用了 Node.js 脚手架，也可以直接使用 `gx` 命令。

请参考[快速开始](getting-started.md)教程了解详细步骤。 

## 综合示例

以下是一个完整的组件示例，展示了布局、数据绑定、事件处理和系统 API 的综合使用。你可以直接在浏览器中查看此示例，点击 `>` 按钮来查看完整代码。

<glyphix id="quick-orientation-example" title="计数器组件示例" height="240">

```html
<!-- 根容器推荐使用 Flex 布局，加载中不允许操作 -->
<div class="container" :disabled="loading">
  <text class="title">Hello, {{ name }}</text>

  <div class="card">
    <text class="count">{{ count }}</text>
    <text class="btn" value="+1" on:click="increment">Add</text>
  </div>
</div>

<!-- 利用页面的堆叠布局来叠加加载状态提示 -->
<text if="loading" class="loading">Loading...</text>
```

```css
.container {
  /* 页面组件不需要设置宽高，它们总是铺满 */
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  /* 注意一般不设置页面背景，这只是演示 */
  background-color: #f5f5f5;
  border-radius: 16px;
  padding: 10%; /* 百分比边距 */
}

.title {
  font-size: 1.25rem; /* 字体使用 rem 单位 */
  color: #333333;
  align-self: center;
}

.card {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 16px;
}

.count {
  font-size: 1.5rem;
  color: #007aff;
  min-width: 80px;
}

.btn {
  width: 120px;
  background-color: #007aff;
  color: #ffffff;
  border-radius: 50%; /* 圆形按钮 */
  text-align: center;
}

.loading {
  color: #3d3d3d;
  font-size: 0.8rem;
  text-align: center;
}

/* disabled 状态的淡化样式 */
*:disabled {
  opacity: 0.5;
}
```

```js
import prompt from '@system.prompt'

export default {
  // 组件数据
  data: {
    name: 'Glyphix',
    count: 0,
    loading: false
  },
  // 生命周期：组件初始化完成
  onInit() {
    console.log('Component initialized')
    this.simulateFetch()
  },
  // 方法定义
  increment() {
    this.count++
    if (this.count % 5 === 0) {
      prompt.showToast({
        message: `Count reached ${this.count}!`
      })
    }
  },
  async simulateFetch() {
    this.loading = true
    // 模拟异步操作，这会产生加载状态
    setTimeout(() => {
      this.loading = false
      this.name = 'Developer'
    }, 1000)
  }
}
```

</glyphix>