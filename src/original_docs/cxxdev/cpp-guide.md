# C++ 学习建议

这篇文档不是 C++ 教程，而是为准备阅读本目录文档的开发者提供前置知识的快速学习建议。

它假设你已经长期使用 C 开发，熟悉 MCU、RTOS、驱动、LVGL 或类似的嵌入式框架；你应该有大量的编程经验，但可能并不熟悉 Glyphix 所需的那部分 C++ 知识。

::: tip
如果你的目标是开发 Native Module、异步功能或 Native Widget，请先看完本文，再继续阅读[对象系统](./object-system.md)和其他章节。这样能避开很多“代码看得懂，但就是写不出来”的问题。
:::

## C++ 能力子集

Glyphix 项目禁用了一些 C++ 特性，开发者完全不需要学习它们：

- 禁用 **RTTI**：不能用 `dynamic_cast`、`typeid` 这一套运行时类型识别机制。需要安全向下转型时，请直接使用 [`dyn_cast`](object-system.md#动态类型转换)。
- 禁用**异常**：不需要把 `try` / `catch` / `throw` 作为主路径来学习。错误处理优先使用返回值、状态码、对象状态和显式检查。这一点和 C 的错误处理习惯类似。


除此之外，Glyphix 的运行时还有一些特殊约束，这主要是 MCU 系统的碎片化和兼容性限制导致的：
1. `std::thread` 和 `std::mutex` 等 C++ 标准库的并发工具在 MCU 上不可用。
2. `std::chrono` 等时间库在 MCU 上也不可用。
3. 不要使用静态局部变量（function-local static），C++11 起保证的原子初始化在 MCU 上**大概率不可靠**。
4. 不要使用带堆分配的全局变量（对象），因为 MCU 上的全局构造阶段可能不受控，且堆内存可能不可用。

其中，3 和 4 是很常见的情况，要格外注意。

## 需要掌握的 C++ 知识

下面这些内容，足以支撑本目录的大部分文档。

### 类和面向对象编程

至少要能读懂并编写这样的代码：

```cpp
class MyWidget : public Widget {
public:
    explicit MyWidget(Widget *parent = nullptr)
        : Widget(parent) {}

    void setValue(int value);
    int value() const;
};
```

你需要理解：

- 类和结构体的区别（没太大区别，主要是默认访问权限）
- 公有继承的含义（一般只用公有继承）
- 构造函数和初始化列表
- 成员函数、**`const` 成员函数**
- 什么时候是覆写基类接口，什么时候只是声明一个普通成员函数

这些知识会直接出现在[对象系统](./object-system.md)、[控件开发指南](./widget.md)和[控件注册与导出](./widget-export.md)中。

### 指针、引用和 `const`

如果你熟悉 C，这部分最容易“自认为已经会了”，但 C++ 用法比 C 更严格。

必须真正掌握的点：

- `T *` 和 `T &` 的区别
- 何时传指针，何时传引用
- **`const T *`**、`T *const`、**`const T &`** 的含义
- 为什么 `const` 成员函数很常见
- 为什么对象不应该像 C 那样随意按字节处理

在 Glyphix 里，这些知识直接关系到接口设计和生命周期安全。

### 生命周期与资源管理

这是从 C 迁移到 C++ 时最重要的一节。

你需要建立这样的习惯：

- 对象会在离开作用域时自动析构
- 构造函数负责建立有效状态
- 析构函数负责释放资源
- 不要把“清理资源”放到函数尾部手动收尾
- 不要把复杂对象当作普通内存块去 `memset` / `memcpy`


Glyphix 的大量设施和特性都建立在 C++ 的对象生命周期模型之上，这包括 RAII 等主题。

### 模板的基础用法

这部分不需要深入理解，但至少要能看懂：

- `Signal<int>`
- `Pointer<Label>`
- `SharedRef<MyData>`
- `async::ResultSession<Client>`
- `std::vector<T>`

并知道“模板是带类型参数的代码生成机制”，而不是某种只有库作者才会碰的高级技巧。

在 Glyphix 文档中，模板主要以两种形式出现：

- **泛型容器/工具类型**，例如 `Signal<T>`、`Pointer<T>`
- **特化点**，例如为自定义类型补充 `js_cast<T>`

开发者至少应该理解基础术语如“模板参数”、“实例化”、“特化”，并能够读懂模板类型的声明和使用。但不要求能够定义自己的模板类或函数。

### lambda 表达式

在现代 C++ 中，lambda 是一种很实用的一次性函数写法。你至少要能读懂：

```cpp
mod["double"] = [](JsCtx ctx) -> JsValue {
    return ctx.arg(0).asInt(0) * 2;
};
```

以及：

```cpp
int factor = readScaleFactorFromConfig();
mod["scale"] = [factor](JsCtx ctx) -> JsValue {
    return ctx.arg(0).asInt(0) * factor;
};
```

首先应该熟悉 lambda 的基本语法和捕获机制，并重点理解：

- lambda 是匿名函数对象
- 无捕获 lambda 常可当普通函数指针用
- 带捕获 lambda 会携带状态
- 一旦 lambda 被异步持有，捕获对象的生命周期就变得非常重要

这直接影响[Native Module 开发](./native-module.md)和[异步开发示例](./async-examples.md)中的代码安全性。

::: tip lambda 非常常见
lambda 实际上完全占据了回调函数的生态位，这意味着它们到处都是。从某种程度上说，lambda 可能是最重要的 C++ 语法点。

**无捕获**的 lambda 表达式几乎等同于 C 函数指针，只是语法不同并能够缓解“起名困难症”。
:::

### 标准库的最小工作集

不用系统学习整套 STL，但建议先熟悉这些最常见部件：

- `std::vector`
- `std::array`
- `std::move`
- 基本算法 `<algorithm>`、迭代器和范围 `for`

::: tip 关联容器
Glyphix 自己实现了 `HashMap` 和 `HashSet`，它们和 `std::unordered_map` 非常相似。但不推荐使用 `std::map`，`std::unordered_map` 等关联容器，因为它们的性能较差，并且 `std::map` 的代码膨胀明显。
:::

### C 与 C++ 互操作

如果你要对接底层 SDK，这部分几乎一定会用到。

至少要会：

- `extern "C"` 的作用
- C 回调函数指针
- `void *` 上下文参数，以及 `void *` 在 C++ 中的隐式转换限制
- C 结构体与 C++ 包装层的分工

你在[异步开发示例](./async-examples.md)里会看到很典型的模式：C API 负责真正的异步执行，C++ 层只做参数包装、生命周期管理和结果回传。

::: tip 难度预期
这部分不难，但很容易出链接错误。你可能需要学会解决混用 C/C++ 头文件时的 `extern "C"` 等导致的各种问题。
:::

## 推荐的学习顺序

建议按下面的顺序补齐，而不是从一本大部头教材从第一页开始读。

### 先建立“从 C 到 C++”的迁移视角

[ISO C++ FAQ](https://isocpp.org/faq)
- 优先看“Learning C++ if you already know C”和“How to mix C and C++”相关条目。
- 这套内容很适合有经验的 C 开发者，因为它默认你已经理解内存、接口、构建和底层约束。

### 快速建立 Modern C++ 印象

[A Tour of C++](https://www.stroustrup.com/Tour.html)
- 如果你愿意接受一本短书，这是最值得投入的一本。
- 它不是“零基础编程教学”，而是给有经验开发者看的现代 C++ 总览。
- 目标不是全部记住，而是知道 C++ 的主要构件有哪些，各自解决什么问题。

### 语法和标准库查询手册

[cppreference](https://en.cppreference.com/w/cpp)
- 适合边做边查，不适合顺序通读。
- 当你在阅读 Glyphix 文档时遇到 `override`、lambda、初始化列表、模板特化、`std::vector` 等语法或库名，可以直接查这里。
- 如果你需要回顾 C 语言的某些细节，也可以在这里查。

### 把编码习惯切换到现代 C++

[C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- 这不是教程，而是工程实践指南，也有出版物版本。
- 不建议全文顺序阅读；优先看这些章节：
  - `P`：总原则
  - `I`：接口设计
  - `F`：函数
  - `C`：类与对象
  - `R`：资源管理
  - `ES`：表达式与语句
  - `CPL`：与 C 互操作
  - `SF`：源文件组织
  - `SL`：标准库使用
  - `CP`：并发，按需阅读

[Embedded Artistry 的 C++ 相关文章](https://embeddedartistry.com/blog/tag/cpp/)
- 更适合作为专题阅读，而不是系统课程。
- 比较值得关注的话题包括：不用堆时如何使用 C++、强类型寄存器封装、程序在 `main()` 之前发生了什么。

## 建议怎样把这些资源用起来

比较高效的方式不是“先学一阵子 C++ 再开始看 Glyphix”，而是并行进行：

1. 先通读本文，知道要补哪些知识。
2. 读一遍[A Tour of C++](https://www.stroustrup.com/Tour.html)或 FAQ 中和 C 迁移相关的部分。
3. 开始阅读[对象系统](./object-system.md)和[Native Module 开发](./native-module.md)。
4. 遇到看不懂的语法时，用 [cppreference](https://en.cppreference.com/w/cpp) 精确查询。
5. 遇到“为什么现代 C++ 倾向这样写”这类问题，再去看 [C++ Core Guidelines]。(https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) 的对应章节。

这样学习的节奏更接近真实工作，也更适合已经有嵌入式经验的开发者。

## 把本文和 cxxdev 文档对应起来

如果你准备继续往下读，可以这样对应重要知识点：

- [对象系统](./object-system.md)：类、继承、生命周期、引用、模板基础
- [SDK 项目配置](./sdk-setup.md)：头文件、源文件、构建系统、最基本的类声明知识
- [Native Module 开发](./native-module.md)：函数接口、lambda、对象生命周期、C/C++ 互操作
- [异步功能开发](./async.md)：模板、线程模型、对象所有权、回调约束
- [控件开发指南](./widget.md)：继承、成员函数、事件处理、对象树和绘制流程
