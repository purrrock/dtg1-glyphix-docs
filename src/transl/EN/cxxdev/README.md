# C++ 原生开发

Glyphix 是一个面向嵌入式设备的应用框架，它提供了一套以 JavaScript 为主、类 Vue Options API 风格的应用开发体验。然而，框架的核心运行时是用 C++ 实现的，因此硬件厂商可以通过 C++ 来扩展和定制框架功能——这正是 “C++ 原生开发” 的用武之地。

这份文档面向具有嵌入式开发经验的 C++ 开发者，旨在帮助你理解 Glyphix 的 C++ 扩展机制，并能够动手实现以下两类功能：

- **Native Module（原生模块）**：将 C++ 功能封装为 JavaScript 可调用的 API，例如文件访问、硬件传感器读取、蓝牙通信等系统能力。
- **Native Widget（原生控件）**：用 C++ 实现自定义 UI 控件，并将其注册为框架[组件](/framework/component/native-component.md)，供应用在界面中直接使用，就如同使用内置的 `div`、`image`、`button` 组件一样。

::: tip
在应用开发中，我们使用“组件”来指代 UI 元素，而在 C++ 层使用“控件（Widget）”来指代 UI 元素。本文档会区分这两个术语：**控件**是 C++ 层的概念，**组件**是响应式框架中的概念。
:::

## 框架运行模型

Glyphix 的运行时由多个层次构成，下图展示了完整的分层架构：

<ArchDiagram max-width="560px">
  <div>
    应用沙箱（Applet × N）
    <div class="remark">独立 JavaScript Realm · 生命周期隔离</div>
  </div>
  <div>
    响应式框架（C++）
    <div class="group row">
      <div>AppletKit<div class="remark">应用路由 · 后台管理</div></div>
      <div>组件系统<div class="remark">Template · Reactive Render</div></div>
      <div>JsVM 桥接层<div class="remark">JerryScript / QuickJS</div></div>
    </div>
    <div class="group row">
      <div>Applet<div class="remark">C++ ↔ JavaScript Sandbox</div></div>
      <div>异步会话<div class="remark">ResultSession · Signals</div></div>
      <div>Native Module<div class="remark">系统 API 扩展</div></div>
    </div>
  </div>
  <div>
    C++ 核心框架
    <div class="group row">
      <div>控件系统<div class="remark">Object · Widget</div></div>
      <div>布局引擎<div class="remark">Flex · Flow · Stack</div></div>
      <div>样式引擎<div class="remark">CSS · Transition</div></div>
    </div>
    <div class="group row">
      <div>事件系统<div class="remark">Touch · Key · Wheel</div></div>
      <div>Painter<div class="remark">2D 绘制</div></div>
      <div>动画引擎<div class="remark">Property · Ease</div></div>
      <div>Signal / Slot</div>
    </div>
  </div>
  <div>
    平台适配层
    <div class="group row">
      <div>图形后端<div class="remark">Framebuffer · GPU</div></div>
      <div>输入驱动<div class="remark">Touch · Key · Wheel</div></div>
      <div>文件系统<span class="remark">File · Dir</span></div>
      <div>IO/时间<span class="remark">Logger · Time</span></div>
    </div>
  </div>
  <div>
    硬件 / OS
    <div class="remark">RTOS · Linux · WASM</div>
  </div>
</ArchDiagram>

最底层是**平台适配层**，负责图形渲染、输入事件、文件系统等平台相关的抽象。这一层通常由设备厂商实现，或由 Glyphix 提供对应平台的参考实现。

其上是 **C++ 核心框架**，包含完整的控件系统（`Widget`）、事件分发、动画引擎、布局系统和样式引擎。所有的 UI 元素最终都以 C++ 控件树的形式组织和渲染。

再上层是**响应式框架**，负责将 C++ 核心能力桥接到 JavaScript 应用。它内嵌 JavaScript 引擎（JerryScript 或 QuickJS），通过 `JsVM` 和 `JsValue` 类实现 C++ 与 JavaScript 的双向交互。AppletKit 管理应用（Applet）的完整生命周期，组件系统实现响应式数据绑定和模板渲染，异步会话框架则将 C++ 的异步操作映射为 JavaScript 的 Promise。响应式框架本身也是用 C++ 实现的。

最上层是**应用沙箱**，每个运行的应用（Applet）拥有独立的 JavaScript 执行环境（Realm），彼此完全隔离。应用退出时，其沙箱内的所有资源会被自动回收。

### 系统协作原理

架构题呈现了模块划分，但刻意隐藏了模块间的协作和耦合关系。实际上，整个框架由一套共同的底层机制协作运转。理解这些机制，能帮助你在实践中知道“自己在做什么、为什么这么做”。

整个框架由一套**对象系统**贯穿，它赋予类运行时感知能力，包括 C++ 类的属性反射与事件通知能力，以及必要的生命周期安全性。Widget、Native Module、应用框架和异步会话都依赖这同一套地基，详见[对象系统](./object-system.md)。

**Widget** 以对象树加上绘制与事件分发构成 UI 骨架；JavaScript 应用层则使用**组件化**的声明式编程模型，两者通过对象的属性等反射能力自然衔接。**异步会话**等复杂的功能也依赖对象系统的生命周期模型来保证正确性。

通过**元对象编译器**和其他抽象机制，Glyphix 并不需要开发者手写绑定代码，即可将 C++ 开发的控件类暴露给 JavaScript 使用。同时，C++ 侧也保留功能完整性，理论上讲你可以直接用 C++ 开发一个完整的应用（虽然不建议这么做）。

### 编程模型

Glyphix 项目不限制特定的编程范式，例如对象系统是一个经典的面向对象模型，但响应式框架则为应用开发者提供声明式的组件化开发体验。

我们不建议开发者去实践“一切皆对象”、刻意套用设计模式，或者追求不必要的抽象。我们的设计原则更倾向于**实用主义**，以满足嵌入式系统的**资源限制**和开发效率为首要目标。

## 文档约定

### 这份文档是什么？

这是 Glyphix C++ 原生开发的指南文档，而**不是** API 参考文档。它介绍框架的设计理念、核心机制和开发流程，帮助你理解如何扩展框架功能，并通过示例代码展示具体实现细节。

在实际开发中，请务必参考 API 文档，它跟随 SDK 一起分发，请联系你的厂商获取访问权限。

### 示例代码说明

Glyphix 框架中的所有 C++ 代码都在 `gx` 命名空间下，文档中默认假设已经 `using namespace gx;`，因此类名和函数名不带 `gx::` 前缀。例如：

```cpp
#include "gx_widget.h"

using namespace gx; // 文档中默认假设已经引入 gx 命名空间

class MyWidget : public Widget {
    // ...
};
```

中，`Widget` 实际上是 `gx::Widget`，但为了简洁起见，我们省略了命名空间前缀。

::: tip C++ 学习资源
如果你主要使用 C 开发，熟悉 MCU、RTOS、驱动或 LVGL，但没有系统学习过 C++，建议先阅读 [C++ 学习建议](./cpp-guide.md)。它只覆盖进入 Glyphix 原生开发真正需要的那部分 C++，并整理了适合嵌入式开发者的外部资源。
:::

## 开发路径

无论你的目标是什么，建议先通读[对象系统](./object-system)中关于 `GX_OBJECT`、`GX_PROPERTY` 和 `Signal` 的基本用法——它们在所有开发场景中都会用到。

根据你的目标，选择合适的文档继续阅读：

- [SDK 项目配置](./sdk-setup)：如何配置 SDK 项目的构建环境，包括 `glyphix_add_meta_objects()` 注册、宿主机构建和交叉编译。
- [Native Module 开发](./native-module)：如何为应用提供新的系统 API，例如获取传感器数据、调用底层 SDK 功能。
- [异步功能开发](./async)：如何为应用扩展异步功能，例如网络请求、文件 IO、耗时计算等。
- [控件开发指南](./widget.md)：如何实现新的 UI 控件（如自定义图表、特殊的动效列表等）。
- [控件注册与导出](./widget-export.md)：将自定义控件注册为框架组件，供应用直接使用。
