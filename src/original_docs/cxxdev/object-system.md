# 对象系统

Glyphix 的 C++ 框架有一套以 `PrimitiveObject` 为根基的对象模型，理解它是后续开发的基础。

对象系统由三个相互配合的部分构成：**对象基类体系**定义了所有托管对象的公共能力与生命周期规则；**元对象系统**通过构建期的元对象编译器为 C++ 类生成元数据，赋予它反射、属性绑定和 JavaScript 导出的能力；**内存安全机制**则通过守卫指针和引用计数解决 GUI 框架中普遍存在的悬空指针问题。

<ArchDiagram max-width="540px">
  <div>
    JavaScript 脚本层
    <div class="remark">属性绑定 · 方法调用 · 事件响应</div>
  </div>
  <div>
    元对象系统
    <div class="group row">
      <div>GX_OBJECT<div class="remark">元编译器注册</div></div>
      <div>GX_PROPERTY<div class="remark">属性/方法反射</div></div>
      <div>Variant<div class="remark">C++ ↔ JS 类型桥接</div></div>
      <div>dyn_cast<div class="remark">安全向下转型</div></div>
    </div>
  </div>
  <div class="subject">
    对象基类体系
    <div class="group row">
      <div>PrimitiveObject<div class="remark">反射支持 · 生命周期管理</div></div>
      <div>Object<div class="remark">父子树结构 · 级联销毁</div></div>
      <div>Widget<div class="remark">UI 控件基类</div></div>
    </div>
  </div>
  <div>
    内存安全机制
    <div class="group row">
      <div>Signal&lt;&gt;<div class="remark">事件通知 · 自动断联</div></div>
      <div>Pointer&lt;T&gt;<div class="remark">守卫弱引用</div></div>
      <div>SharedRef&lt;T&gt;<div class="remark">侵入式共享引用</div></div>
    </div>
  </div>
</ArchDiagram>

## 反射与元对象编译器

标准 C++ 的类是 “沉默” 的：拿到一个对象指针，你无法在运行时知道它有哪些成员、叫什么名字、怎么读写。这对于不需要脚本化的静态 C++ 开发来说不是障碍。

但 Glyphix 的工作方式不同。当应用的页面模板写下 `:value="progress"`，响应式框架需要在运行时按字符串 `"value"` 找到控件对应的属性，并在数据变化时自动刷新。这种 "程序运行时能了解自己的结构" 的能力叫做**反射（Reflection）**，标准 C++ 并不支持。

Glyphix 的解决方案是在构建流程中加入一个**元对象编译器（Meta Compiler）**。它在正式的 C++ 编译之前扫描源代码，为需要参与对象系统的类生成元数据。开发者只需在类定义开头放上 **`GX_OBJECT`** 宏，元对象编译器就会处理这个类——此后框架就能按名称读写它的属性或调用方法，并能在 JavaScript 中访问它。

你暂时不需要了解元对象系统的内部原理。记住一条规则就够了：凡是需要反射能力的类，都必须在定义时加上 `GX_OBJECT` 宏，并继承自 `PrimitiveObject` 或 `Object`。

## `PrimitiveObject` 与 `Object`

框架的对象体系分为两级：

**`PrimitiveObject`** 是所有**托管对象**的根基类。继承它的类就拥有了属性反射、动态转型、安全延迟销毁等框架能力。但 `PrimitiveObject` 本身**没有**父子树结构——它就是一个“框架可以感知的 C++ 对象”。`AsyncSession`、`BindableObject` 等类型都继承自它，因为这些类不需要组成树。

**`Object`** 继承自 `PrimitiveObject`，额外增加了**父子树结构**：构造时传入 `parent` 指针，父对象销毁时所有子对象也会递归销毁。控件树（Widget Tree）就是通过这一机制组织的。

::: tip 类比其他框架
如果你有 Qt 开发经验，可以将 Glyphix 的元对象系统类比为 Qt 的 MOC 系统：`GX_OBJECT` 对应 `Q_OBJECT`。但也有许多差异，如 Glyphix 将 Qt 中 `QObject` 的能力拆分成了两层；`Signal` 也只是一个不依赖元对象编译器的普通模板类。

其他框架如 Unreal Engine 的 UCLASS 也有类似的反射系统。
:::

选择哪个基类取决于你的类是否需要成为树的一部分：

```cpp
// 需要参与对象树 → 继承 Object
class MySensor : public Object {
    GX_OBJECT
public:
    explicit MySensor(Object *parent = nullptr) : Object(parent) {}
};

// 只需框架感知，不参与树 → 继承 PrimitiveObject
class MyNetworkSession : public PrimitiveObject {
    GX_OBJECT_KINDS(ExplicitDeleteKind)
public:
    MyNetworkSession() = default;
};
```

代码中的 `GX_OBJECT_KINDS(ExplicitDeleteKind)` 是一个附加声明，它和 `GX_OBJECT` 宏一样声明元对象类，但告知框架这个对象的生命周期由开发者负责，不会被 JavaScript 自动回收。`AsyncSession` 等生命周期敏感的类型都使用了它。

## 属性与信号

**`GX_PROPERTY`** 宏用于声明一个可被框架感知的属性，关联对应的 getter 和 setter。声明后属性可以由框架的响应式系统驱动——值变化时依赖它的 UI 自动刷新，动画系统也可以对它做插值：

```cpp
class MyWidget : public Widget {
    GX_OBJECT
public:
    int value() const { return m_value; }
    void setValue(int v) { m_value = v; update(); }

    GX_PROPERTY(int value, get value, set setValue)

private:
    int m_value = 0;
};
```

### 信号（Signal）

**`Signal<>`** 是事件通知机制，直接声明为类成员。事件发生时“发射”它，其他对象通过“连接”来接收通知（[lambda 表达式](https://en.cppreference.com/w/cpp/language/lambda)是 C++ 的匿名函数语法）：

```cpp
class MyWidget : public Widget {
    GX_OBJECT
public:
    Signal<int> valueChanged;

    void setValue(int v) {
        m_value = v;
        valueChanged(v);  // 发射信号
    }
private:
    int m_value = 0;
};

// 连接到成员函数
myWidget->valueChanged.connect(this, &MyClass::onValueChanged);

// 或者连接到 lambda
auto slot = make_slot([](int v) { /* 响应变化 */ });
myWidget->valueChanged.connect(slot);
```

::: tip 和 Qt 的信号槽对比
Qt 的经典信号槽机制需要 MOC 生成代码支持，但 `Signal<>` 是一个纯 C++ 模板类，不依赖元对象编译器。因此不一定要在特定类中使用 `Signal<...>` 对象，你可以在任何地方使用它。

由于 `Signal` 是一个类，它会占据内存空间（即便没有连接），因此建议尽量使用事件类型枚举和单一信号成员变量来节约内存，而不是为每个事件都声明一个 `Signal` 成员。
:::

### `GX_PROPERTY` 的完整形式

`GX_PROPERTY` 除了 `get` / `set` 之外，还支持声明关联的变化信号（`signal`），这是响应式框架订阅属性变化的标准接口：

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    int value() const { return m_value; }
    void setValue(int v) {
        if (m_value == v) return;
        m_value = v;
        update();
        valueChanged(v);
    }

    Signal<int> valueChanged;

    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)

private:
    int m_value = 0;
};
```

声明了 `signal` 的属性，其变化会通过响应式框架自动传递给绑定了该属性的 JavaScript 表达式。这是控件属性与应用数据双向同步的基础。

`GX_PROPERTY` 中的 `signal` 字段不依赖 `Signal<T>` 的参数类型，框架只关心它是否存在以及何时被发射。相反，此时必须提供 `get` 字段来让框架在 JavaScript 侧读取属性值。

## 守卫指针与内存安全

GUI 框架中，异步场景容易引发悬空指针崩溃。一个典型案例：
```cpp
void onNetworkResponse(const String &data) {
    // 网络请求耗时 2 秒才返回
    // 但在这 2 秒内，用户可能已经退出当前页面，label 已被销毁
    this->label->setText(data); // Segmentation Fault!
}
```
定时器回调、IO 回调等所有异步场景都面临同等风险。在脚本化框架中，这种用例是结构性不可避免的，因此必须提供一种安全的生命周期观察机制。

### `Pointer<T>` 守卫指针

Glyphix 为 `PrimitiveObject` 的所有派生类内置了弱引用计数支持。使用 `Pointer<T>` 持有非所有权的跨对象引用，当目标对象被销毁时，`Pointer<T>` 会自动被置空，解引用前检查即可安全使用：

```cpp
Pointer<Label> m_label; // 声明为成员变量

// ...构造后赋值...
m_label = label;

// 在任何可能导致 label 被销毁的异步回调中：
void onNetworkResponse(const String &data) {
    if (!m_label)
        return; // label 已被销毁，安全退出
    m_label->setText(data); // 此时访问是安全的
}
```

::: tip 何时使用
跨对象持有指针但不拥有其生命周期时，用 `Pointer<T>` 代替裸指针 `T *` 来追踪生命周期。`Signal` 的 `connect` 机制也依赖守卫指针——当接收者（slot 所在对象）被销毁时，连接自动断开，不会触发悬空回调。
:::

::: warning 线程限制
守卫指针不支持跨线程访问，它们基本仅限于 UI 线程使用，同时也不是零开销抽象，每次构造都会涉及引用计数操作。
:::

### `SharedRef<T>` 侵入式引用计数

对于不继承自 `PrimitiveObject` 的普通值对象（如自定义数据结构），框架提供了侵入式的共享引用计数。让值类型继承 `SharedValue`，再用 `SharedRef<T>` 持有它，即可获得类似 [`std::shared_ptr`](https://en.cppreference.com/w/cpp/memory/shared_ptr) 的共享语义，同时避免额外的控制块分配：

```cpp
class MyData : public SharedValue {
public:
    int x = 0;
    String name;
};

auto ref1 = make_shared<MyData>();
ref1->x = 42;

SharedRef<MyData> ref2 = ref1; // 引用计数增加，共享同一对象
```

`SharedRef` 还支持写时复制（COW）语义：在对拷贝版本进行修改前，创建一个独立副本，确保多个持有者之间互不干扰。该机制使用原子引用计数实现线程安全。

## 动态类型转换

标准 C++ 的 [`dynamic_cast`](https://en.cppreference.com/w/cpp/language/dynamic_cast) 依赖 RTTI（运行时类型信息），而嵌入式环境通常以 `-fno-rtti` 编译。`dyn_cast` 利用元对象系统提供了等效的运行时安全向下转型能力。

`dyn_cast<T *>()` 的目标类型 `T` 必须满足两个条件：
1. 继承自 `PrimitiveObject`
2. 声明了 `GX_OBJECT`/`GX_OBJECT_KINDS` 宏

```cpp
PrimitiveObject *obj = getSomeObject();

// 安全的向下转型，转型失败返回 nullptr
auto *btn = dyn_cast<Button *>(obj);
if (btn)
    btn->setText("OK");

// const 版本同样支持
const auto *constBtn = dyn_cast<const Button *>(obj);
```

::: warning `GX_OBJECT` 是前提
`dyn_cast` 的类型检查依赖目标类的静态元对象信息（`staticMetaObject`）。如果目标类没有声明 `GX_OBJECT`，则缺乏必要的运行时类型信息，并出现编译错误。
:::

在 Native Module 开发中，`dyn_cast` 尤为常用：框架经常将对象以基类指针（`PrimitiveObject *` 或 `Object *`）传入，需要 `dyn_cast` 来安全地还原为具体类型再操作。

考虑到沙箱安全策略不信任脚本传入的对象，我们不能假设传入的运行时对象指针是正确的类型，因此必须用 `dyn_cast` 来验证类型并安全地访问其成员。

### 内存泄漏陷阱

典型的 `dyn_cast` 使用模式暗含一个内存泄漏风险，如：
```cpp
auto *session = dyn_cast<Session *>(takeObjectOwnership());
if (session) {
    // 成功转型，访问 session 的成员并转移所有权
}
```
问题在于，如果 `takeObjectOwnership()` 返回的对象不是 `Session` 类型，`dyn_cast` 会返回 `nullptr`，但原始对象的所有权已经被转移了——如果没有其他机制来回收这个对象，就会导致内存泄漏。

在开发 Native Module API 时，有时会遇到这种问题，相关框架提供更好的 API 来避免这种情况。但开发者应该意识到这个潜在风险，不要被 `dyn_cast` 的安全性误导。

### `GX_OBJECT` 是否必要

并非所有继承自 `PrimitiveObject` 的类都需要 `GX_OBJECT`。`GX_OBJECT` 宏的作用是将类注册到元对象系统，启用反射、属性绑定和 `dyn_cast` 等能力。如果你的类：

- 不需要暴露给 JavaScript
- 不需要 `GX_PROPERTY`、`GX_METHOD` 等反射机制
- 不需要被 `dyn_cast` 安全转型

那么可以省略 `GX_OBJECT`，只继承基类并正常使用 C++ 特性即可：

```cpp
// 不需要任何元对象能力的内部辅助类，省略 GX_OBJECT
class InternalBufferManager : public PrimitiveObject {
public:
    explicit InternalBufferManager() = default;
    void flush();
private:
    // ...
};
```

省略 `GX_OBJECT` 的类仍然具有 `PrimitiveObject` 的基础能力，包括 `deleteLater()` 和守卫指针支持，只是失去了反射和动态类型识别能力。

另一种情况是，你的最终类型需要元对象能力，但中间的某些基类不需要，那么中间基类可以不声明 `GX_OBJECT`。这会丢失一些运行时类型信息，但能减小代码量。

::: tip
如果你不确定是否需要 `GX_OBJECT`，通常建议保守地加上它。
:::

最后一个重要的差异在于：一旦使用 `GX_OBJECT` 标记，类必须位于头文件（`*.h`）中，并使用 `glyphix_add_meta_objects()` CMake 宏注册到构建系统中。没有 `GX_OBJECT` 的类则没有这个要求，可以直接在 `.cpp` 文件中定义。

## 运行时类型系统

在前面所有关于 `GX_PROPERTY` 的讨论中，有一个问题从未被回答：

```cpp
GX_PROPERTY(int value, get value, set setValue)
```

JavaScript 怎么知道 `int` 是什么？当 JavaScript 侧写下 `widget.value = 42`，这个 `42` 是 JavaScript 的 `number` 类型。而 `setValue(int v)` 接受的是 C++ 的 `int`。这之间发生了什么？反过来，`getValue()` 返回的 `int` 又怎么变成了 JavaScript 中的 `number`？

在没有任何胶水代码的情况下，框架显然需要在幕后做一些工作来桥接 C++ 静态类型和动态的脚本类型。这是一个相当透明的过程，本节将解释中间发生了什么。

### 通用类型容器 `Variant`

答案在于 `Variant`。它是一个可以容纳任意类型值的类型擦除容器，是连接 C++ 静态类型系统和 JavaScript 动态类型的核心桥梁。

每当框架需要跨越这道界限，它都走 `Variant` 这条路：

1. **属性读写中间层**：`GX_PROPERTY` 声明的属性通过反射 API 读写时，值以 `Variant` 传递。框架将 JavaScript 的 `JsValue` 转换成 `Variant`，再由 `Variant` 转换成 C++ setter 的实际参数类型；读取时方向相反。
2. **方法调用参数编组**：`GX_METHOD` 的参数和返回值在传递给 C++ 之前，都先经过 `Variant` 表示。

```cpp
Variant v1;                  // 空值（null）
Variant v2{42};              // 存储 int
Variant v3{3.14};            // 存储 double
Variant v4{String("Hello")}; // 存储 String
// Variant 必须显式构造，不支持隐式转换
// Variant v5 = 42; // 错误，必须写 Variant v5{42};

// 类型检查
if (v2.is<int>()) { /* ... */ }
// 不建议检查可转换性，而是直接 to<T>() 后判断是否为非法值
if (v3.convertible<double>()) { /* ... */ }

// 按引用读取（最快，要求类型精确匹配）
int n = v2.as<int>();
// 按引用读取，类型不匹配时返回默认值
double d = v2.as<double>(0.0); // int != double，返回 0.0
// 带类型转换的读取（按值）
int fromDouble = v3.to<int>();   // 3.14 -> 3
String fromInt = v2.to<String>(); // 42 -> "42"
```

::: tip
这不是 C++17 的 [`std::variant`](https://en.cppreference.com/w/cpp/utility/variant)，更像是支持运行时类型识别和自动类型转换的 [`std::any`](https://en.cppreference.com/w/cpp/utility/any)。

通常你不需要在业务代码中直接操作 `Variant`，框架自动完成所有转换。只有在实现低层框架扩展、编写通用工具函数，或需要直接操作运行时反射 API 时，才会直接与它打交道。
:::

### 内置类型映射

框架为常见的 C++ 基础类型内置了与 JavaScript 的双向映射：

| C++ 类型 | JavaScript 类型 | 备注 |
|:---:|:---:|:---:|
| `int`、`float`、`double` 等 | `number` | 数值类型直接映射 |
| `bool` | `boolean` | |
| `String` | `string` | |
| `PrimitiveObject *` 的子类 | JavaScript 对象引用 | 由框架管理对象生命周期 |
| `Color`、`Length` 等值类型 | `string` | 通过特定格式的字符串表示 |

这就是为什么你写下 `GX_PROPERTY(int value, ...)` 后，JS 侧能直接做 `widget.value = 42`：`int` 在内置映射表中，框架知道如何转换类型。

::: note 不要使用 C 字符串
`Variant` 要求存储类型 `T` 具有所有权，因此 C 字符串（`const char *`）、字符串切片（`String::View`）等非拥有类型不能存储在 `Variant` 中。请始终使用 `String` 来表示文本数据，必要时需要显式转换为 `String` 后存储到 `Variant`。

如果使用了不受支持的字符串类型，会导致编译错误。
:::

::: important
内置类型映射表没有注册 `std::string` 相关的映射，因此也不建议在 `Variant` 中存储 `std::string`。未映射的类型可以正常存储，但它会被当作一个不透明的 C++ 对象处理，无法在 JavaScript 中使用。
:::

### 复杂类型反射

对于使用 `GX_OBJECT` 声明的类，还可以利用 `GX_ENUM` 和 `GX_STRUCT` 来导出枚举和结构体成员类型，让它们也能在 JavaScript 中以自然的方式使用。这种类型导出是自动的，不需要再手写额外的绑定代码。

#### 枚举反射 `GX_ENUM`

当属性或方法的参数类型是 C++ 枚举时，直接以整数暴露给 JavaScript 既不直观也容易出错。`GX_ENUM` 将枚举导出为字符串常量，让 JavaScript 用可读字符串而非魔法数字来操作：

```cpp
class ScrollArea : public Widget {
    GX_OBJECT
public:
    enum GX_ENUM ScrollBarStyle {
        RemoveScrollBar GX_ALIAS("hidden"),
        LinearScrollBar GX_ALIAS("line"),
        DotsScrollBar   GX_ALIAS("dots")
    };

    GX_PROPERTY(ScrollBarStyle indicator, set setScrollBar)
};
```

`GX_ENUM` 放在 `enum` 关键字后，告诉元对象编译器这个枚举需要导出。`GX_ALIAS("...")` 为每个枚举成员指定 JavaScript 可见的字符串名称——如果省略，则默认使用 C++ 成员的原始名称。应用开发者在 JavaScript 中这样使用：

```js
scroll.indicator = "hidden"; // 对应 RemoveScrollBar
scroll.indicator = "dots";   // 对应 DotsScrollBar
```

框架在读取 `indicator` 属性时，将字符串 `"dots"` 转换为 `DotsScrollBar` 枚举值后再传给 setter；读取时将枚举值转回字符串。整个过程对 C++ 侧完全透明，C++ 代码始终操作的是具体枚举类型。

#### 结构体参数反射 `GX_STRUCT`

对于方法参数，有时一个操作需要多个相关配置项。此时可以将参数封装成结构体，并用 `GX_STRUCT` 导出，让 JavaScript 侧传入一个对象字面量：

```cpp
class Scroll : public ScrollArea {
    GX_OBJECT
public:
    struct GX_STRUCT ScrollOptions {
        Length left;
        Length top;
        ScrollBehavior behavior;
    };
    struct GX_STRUCT IndexOptions {
        int index;
        ScrollBehavior behavior;
    };

    GX_METHOD void scrollTo(const ScrollOptions &options);
    GX_METHOD void scrollBy(const ScrollOptions &options);
    GX_METHOD void setIndex(const IndexOptions &options);
};
```

`GX_STRUCT` 放在 `struct` 关键字后，结构体的每个字段按其类型（同样经由内置类型映射或嵌套的 `GX_ENUM`）自动导出。JS 侧可以直接传入对象：

```js
scroll.scrollTo({ left: 0, top: 200, behavior: "smooth" });
scroll.setIndex({ index: 3, behavior: "instant" });
```

C++ 侧的 `scrollTo` 接收到的始终是强类型的 `ScrollOptions` 对象，不需要在 C++ 侧做任何解析。

::: warning 不要遗忘标注
在声明 `GX_PROPERTY` 或 `GX_METHOD` 时，如果相关类型是一个自定义的枚举或结构体，务必正确标注 `GX_ENUM` 或 `GX_STRUCT`。否则 JavaScript 侧无法使用这些属性或方法，并且没有任何编译错误提示。
:::

### 存在一种“中间表示”吗？

使用 `Variant` 来桥接 C++ 和 JavaScript 时，框架是否会将 JavaScript 对象转换成一个通用的中间表示，如某种类似 JSON 的序列化结构？

答案是否定的。`Variant` 直接存储 C++ 对象（包括 `JsValue`），这也包括该对象的所有类型信息和操作语义。系统会根据 `Variant` 值的运行时类型标记来正确地进行类型转换和方法调用，而不需要特定的中间表示或者序列化过程。
