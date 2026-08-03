# Native Module 开发

Native Module 是连接 C++ 与应用层 JavaScript 代码的桥梁。当你需要向应用暴露系统能力——例如读取传感器数据、调用三方 SDK、接入系统能力，就需要编写 Native Module。

Glyphix 框架已经通过这种机制实现了众多内置模块，如文件系统（`@system.file`）、路由（`@system.router`）等。你可以用同样的方式为自己的设备添加专属能力。

下图展示了 Native Module 在框架中的位置——它处于响应式框架层，通过 JsVM 桥接层向上为 JavaScript 应用提供系统 API，向下调用 C++ 核心框架或平台能力：

<ArchDiagram max-width="480px">
  <div>
    应用沙箱（Applet × N）
    <div class="remark">独立 JavaScript Realm · 生命周期隔离</div>
  </div>
  <div>
    响应式框架（C++）
    <div class="group row">
      <div>JsVM 桥接层<div class="remark">JsValue · JsCallContext</div></div>
      <div class="subject">Native Module<div class="remark">系统 API 扩展</div></div>
      <div>Applet<div class="remark">沙箱 · 生命周期</div></div>
    </div>
  </div>
  <div>
    C++ 核心框架 / 平台适配层
    <div class="remark">驱动 · SDK · 硬件抽象</div>
  </div>
</ArchDiagram>

编写一个 Native Module 需要用到三组概念：**JsVM 桥接层**提供 C++ 与 JavaScript 之间的类型转换和函数调用能力；**模块注册宏**将 C++ 代码组装为 JavaScript 可 `import` 的模块；**Applet 沙箱**为模块提供应用级的上下文和资源生命周期管理。本章按这个顺序逐步展开。

::: warning 安全风险
当你计划为 Glyphix 开发“系统级扩展”时，不要忽视这也意味着高安全风险。稍有不慎就可能引入漏洞，导致恶意应用利用这些能力攻击系统或其他应用。请务必遵循安全编码规范，限制模块的权限和访问范围，并进行充分的安全测试。
:::

## JsVM 桥接层

在编写具体的模块之前，需要先了解 C++ 与 JavaScript 之间的交互工具。JsVM 桥接层是整个 Native Module 的基础设施，它提供 `JsValue` 类型系统和 `JsCallContext` 调用上下文，使 C++ 代码能够创建、读取和操作 JavaScript 值。

### `JsValue` 类型系统

`JsValue` 是框架中表示 JavaScript 值的 C++ 类型，覆盖了所有 JavaScript 基础类型。它采用引用计数管理生命周期，可以像 `int`、`String` 等 C++ 值类型一样直接赋值和拷贝。

从 C++ 创建 JavaScript 值：

```cpp
JsValue undefined;               // undefined
JsValue boolVal{true};           // boolean
JsValue intVal{42};              // number（整数）
JsValue floatVal{3.14};          // number（浮点）
JsValue strVal{"hello"};         // string
```

这些构造函数都是隐式的，因此模块函数可以直接 `return "hello"` 或 `return 42`，无需手动包装。

从 `JsValue` 读取 C++ 值时，使用 `as*` 系列方法。它们在类型不匹配时返回指定的默认值，避免了手动做类型检查：

```cpp
int    count  = value.asInt(0);       // 若非数字则返回 0
double ratio  = value.asNumber(1.0);  // 若非数字则返回 1.0
String label  = value.asString();     // 若非字符串则返回空串
```

如果需要按 JavaScript 语义做强制类型转换（例如将任意值转为布尔），使用 `to*` 系列方法：

```cpp
bool   enable = value.toBoolean();    // 任何值都可以转换为 bool
int    num    = value.toInt();        // 按 ECMAScript 规范转换为整数
String str    = value.toString();     // 按 ECMAScript 规范转换为字符串
```

当需要判断值的具体类型时，使用 `is*` 系列方法：

```cpp
value.isUndefined()   // 是否为 undefined
value.isNumber()      // 是否为数字
value.isString()      // 是否为字符串
value.isObject()      // 是否为对象
value.isArray()       // 是否为数组
value.isFunction()    // 是否为函数
```

### `JsCallContext` 上下文

每个被 JavaScript 调用的 C++ 函数都有固定的签名：

```cpp
JsValue myFunction(JsCtx ctx);
```

`JsCtx` 是 `const JsCallContext &` 的别名。`JsCallContext` 提供三个核心能力：

- **`ctx.argc()`**：获取 JavaScript 传入的参数数量；
- **`ctx.arg(index)`**：获取第 `index` 个参数（返回 `const JsValue &`）；
- **`ctx.vm()`**：获取当前 JavaScript 引擎实例（`JsVM &`）。

一个典型的参数读取模式：

```cpp
static JsValue setVolume(JsCtx ctx) {
    // 一定先检查参数数量，再验证类型，不然 ctx.arg(0) 可能越界
    if (ctx.argc() < 1 || !ctx.arg(0).isNumber())
        return JsValue();  // 参数不合法，返回 undefined

    int level = ctx.arg(0).asInt(0);
    level = std::max(0, std::min(100, level));
    audioSetVolume(level);
    return JsValue(true);  // 返回成功标志
}
```

很多内置模块的函数接收一个对象参数，这是一种灵活的约定，它允许参数有默认值，也方便未来扩展：

```js
// JavaScript 侧调用
setConfig({ brightness: 80, contrast: 50 })
```

在 C++ 侧通过 `operator[]` 读取对象属性：

```cpp
static JsValue setConfig(JsCtx ctx) {
    if (ctx.argc() < 1) return {}; // 记得检查参数数量

    JsValue params = ctx.arg(0);
    int brightness = params["brightness"].asInt(100);
    int contrast   = params["contrast"].asInt(50);
    // ...
    return {}; // 返回 undefined
}
```

### 将函数导出为 `JsValue`

模块函数不一定要是具名静态函数。`JsValue` 可以从任意可调用对象构造：**无捕获 lambda** 会被自动解析为函数指针，效率等同于具名函数；**带捕获 lambda** 则被包装为 callable 对象，适合在工厂函数内闭包模块级的运行时状态：

```cpp
static JsValue createMathModule(JsVM &vm) {
    JsValue mod = vm.newObject();

    // 无捕获 lambda：自动退化为函数指针，无额外开销
    mod["double"] = +[](JsCtx ctx) -> JsValue {
        return ctx.arg(0).asInt(0) * 2;
    };

    // 带捕获 lambda：在模块创建时读取一次配置，后续调用直接使用
    int factor = readScaleFactorFromConfig();
    mod["scale"] = [factor](JsCtx ctx) -> JsValue {
        return ctx.arg(0).asInt(0) * factor;
    };

    return mod;
}
```

Lambda 形式的优势在于可以将相关逻辑就近书写在工厂函数中，避免大量短小的具名函数分散在文件各处。对于逻辑简单、不需要在 C++ 侧复用的函数，推荐优先使用 lambda。

### 创建与返回对象

许多场景下需要返回一个包含多个字段的结果对象。使用 `JsVM::newObject()` 创建一个新的 JavaScript 对象，再通过 `operator[]` 设置属性：

```cpp
static JsValue getSystemInfo(JsCtx ctx) {
    JsValue result = ctx.vm().newObject();
    result["model"] = "GX-Watch-2";
    result["firmware"] = "2.1.0";
    result["memory"] = 512; // KB
    return result;
}
```

`JsVM` 还提供其他工厂方法，如 `newArray()`、`newArrayBuffer()`、`newPromise()` 等，可根据需要创建各种 JavaScript 类型。

### 异常与错误处理

如果模块函数遇到错误，可以通过 `JsVM::newError()` 抛出一个 JavaScript 异常：

```cpp
static JsValue setConfig(JsCtx ctx) {
    if (ctx.argc() < 1)
        return ctx.vm().newError("missing parameters");
    // ...
}
```

但是我们一般不在函数参数检查等简单场景中使用异常，因为异常信息文本会占用代码量。对于非关键错误，返回 `undefined` 或 `false` 通常更合适。

### 函数互操作性

如果需要在 C++ 中主动执行 JavaScript 函数或对象方法，可以使用 `JsValue::call()` 或 `callMethod()`。这就像在 C++ 里直接调用 JavaScript 函数一样简单，参数可通过初始化列表传入，并获取返回值：

```cpp
static JsValue printDemo(JsCtx ctx) {
    JsVM &vm = ctx.vm();
    JsValue obj = vm.newObject();
    obj["value"] = 42;
    
    // 调用控制台对象的方法，相当于 JS 中的 console.log("Object is:", obj)
    auto result = vm.globalObject()["console"]
                    .callMethod("log", {"Object is:", obj});
    
    // print() 可用于向控制台直接输出 JsValue 的内容，方便调试
    result.print(); // undefined 
    
    // 如果你只关心执行过程而不需要返回值，并希望在发生错误时打印警告：
    result.reportError(); // 返回 bool 值表示是否是一个异常
    
    return {}; // 返回 undefined
}
```

如果是调用一个由参数传入的独立函数对象（而非附加在对象上的方法），需要使用 `call()` 并指定 `this` 绑定对象，通常可以使用全局对象 `globalObject()`：

```cpp
static JsValue doMathAndCallback(JsCtx ctx) {
    if (ctx.argc() < 1 || !ctx.arg(0).isFunction()) return JsValue();
    
    auto &callback = ctx.arg(0); // 这里可以取引用，以免引用计数开销
    // 这个是 JS 函数调用时的 this 对象，如果为 {} 则相当于 undefined
    JsValue thisObj = ctx.vm().globalObject();
    // 相当于 JS 中的 callback.call(globalThis, 10, 20)
    JsValue result = callback.call(thisObj, { 10, 20 });
    
    return result;
}
```

::: warning 危险的反面模式：异步回调泄漏
如果你的初衷是将 JavaScript 传入的 `callback` 长期保存，比如传递给底层硬件并用来订阅事件，请务必当心：

```cpp
// ❌ 错误示范：会导致内存泄漏！
static JsValue onButtonPress(JsCtx ctx) {
    auto callback = callback = ctx.arg(0);
    // 直接从参数获取 JavaScript 回调并捕获在一个 lambda 中，传递给底层驱动
    HardwareButton::onPress([callback]() mutable {
        callback.call({}, {...});
    });
    return {};
}
```

这是一个典型的**严重陷阱**：`JsValue` 拥有基于引用计数的生命周期管理。一旦这个闭包被底层驱动随全局状态持久持有，且没有提供明确的取消机制（例如对应的 `offPress` 方法解绑），那么这个 JavaScript 回调以及它绑定的整个应用沙箱上下文将被**永久泄漏**！

如需实现跨事件循环的长生命周期回调（如事件订阅），必须结合**应用沙箱**的生命周期机制来管理 C++ 对象，并在不用时安全解绑，或者直接使用专用的 `AsyncSession` 设施（请参阅[异步功能开发](./async.md)）。
:::

对于更复杂的异步场景（如需要返回 Promise，或需要多次回调），请参阅[异步功能开发](./async)。

::: tip 完整 API 参考
本节仅覆盖了 JsVM 桥接层最常用的能力。`JsVM` 和 `JsValue` 还提供了许多本节未涉及的接口，例如：JSON 解析与序列化（`parseJSON()`、`stringifyJSON()`）、属性枚举（`properties()`）、Promise 操作（`newPromise()`、`promiseResolve()`/`promiseReject()`）、以及直接执行 JS 代码（`eval()`、`importModule()`）等。完整接口说明请参阅随 SDK 分发的 API 文档。
:::

### 导出 C++ 对象

前面的例子都是“函数返回基础类型或普通 JavaScript 对象”，本质上是通过 C++ API 操作 JavaScript。但有时候需要将一个 **C++ 对象导出给 JavaScript**，以便脚本后续持续操作同一个底层实例。

有几种不同的实现方式：

- **`vm.newMetaObject(object)`**：最直接，自动把 `GX_PROPERTY` / `GX_METHOD` 暴露给 JavaScript；
- **`vm.newObject(object)` + 手动挂函数**：更接近“带原生句柄的普通 JS 对象”；
- **`vm.newProxy()`**：最灵活，但属性拦截逻辑分散，维护成本也最高。

大多数业务场景里，推荐优先使用 `newMetaObject()`。只有当你明确需要手写一层 JavaScript 形状，或需要拦截非常动态的属性访问时，再考虑另外两种方法。

#### `newMetaObject()` 导出

这是最简单的办法。先定义一个原生对象类型，再直接把它包装成可反射的 JavaScript 对象。

下面这个例子导出一个可读写的计数器对象。它必须继承 `PrimitiveObject`，并用 `GX_OBJECT` 声明到元对象系统中：

```cpp
#include "gx_jsvm.h"
#include "gx_object.h"

using namespace gx;

class NativeCounter final : public PrimitiveObject {
    GX_OBJECT

public:
    explicit NativeCounter(int initial = 0) : m_value(initial) {}

    int value() const { return m_value; }
    void setValue(int value) { m_value = value; }

    GX_METHOD void reset() { m_value = 0; }

    // 需要暴露给 JavaScript 作为“构造函数”。
    static JsValue constructor(JsCtx ctx) {
        int initial = ctx.argc() ? ctx.arg(0).asInt(0) : 0;
        auto *counter = new NativeCounter(initial);
        return ctx.vm().newMetaObject(counter);
    }

    GX_PROPERTY(int value, get value, set setValue)

private:
    int m_value = 0;
};
```

::: tip GX_METHOD 的类型
`GX_METHOD` 标记的函数可以具有任意可以和 `JsValue` 互转的 `Variant` 可托管类型参数和返回值，并可以是引用。例如：`int`、`const String &` 等。

不要忘了，`JsValue` 本身也是可以使用的。
:::

然后在模块工厂函数里把这个“构造函数”导出出去：

```cpp
static JsValue createCounterModule(JsVM &vm) {
    JsValue mod = vm.newObject();
    mod["createCounter"] = NativeCounter::constructor;
    return mod;
}
```

JavaScript 侧这样使用：

```js
import counter from '@vendor.counter'

const c = counter.createCounter(10)
console.log(c.value) // 10
c.value = 42
c.reset()
console.log(c.value) // 0
```

这里 `c` 看起来像普通 JavaScript 对象，但底层实际关联的是一个 `NativeCounter` 实例。由于使用的是 `newMetaObject()`，JavaScript 可以直接读写 `GX_PROPERTY` 声明的属性，也可以调用 `GX_METHOD` 暴露的方法。

如果你只需要“把一个 C++ 对象自然地暴露为 JavaScript 对象”（包括属性和方法），通常做到这里就够了。

#### 处理 Applet 上下文

`newMetaObject()` 有一个常见限制：通过元对象系统导出的 `GX_METHOD` 是普通 C++ 成员函数，它拿不到 `JsCtx` / `JsCallContext`，因此也就不能像模块函数那样直接写 `Applet::current(ctx.vm())`。

如果你的对象方法需要访问当前应用上下文，例如：

- 解析应用私有 URI；
- 读取应用权限或配置；
- 在对象方法内部继续绑定其他资源到当前沙箱；

那么更合适的做法是让这个对象继承 `BindableObject`，在对象创建时就和当前 `Applet` 绑定。这样后续的 `GX_METHOD` 内部可以直接通过 `applet()` 访问宿主应用。

示例：

```cpp
#include "gx_applet.h"
#include "gx_bindableobject.h"
#include "gx_jsvm.h"

using namespace gx;

class NativeFile final : public BindableObject {
    GX_OBJECT_KINDS(NoneKind)

public:
    NativeFile(Applet *applet, const String &uri)
        : BindableObject(applet), m_uri(uri) {}

    GX_METHOD String resolvedUri() const {
        auto *host = applet();
        return host ? host->resolveUri(m_uri) : String();
    }

    static JsValue constructor(JsCtx ctx) {
        auto *applet = Applet::current(ctx.vm());
        if (!applet) return {};

        String uri = ctx.argc() ? ctx.arg(0).toString() : String();
        return ctx.vm().newMetaObject(new NativeFile(applet, uri));
    }

private:
    String m_uri;
};
```

::: warning 沙箱安全性
不要真的实现 `resolvedUri()` 这种直接暴露底层资源路径的功能，这只是个示例。实际开发中请务必做好权限检查和访问控制，避免将敏感信息泄漏到 JavaScript 侧。
:::

JavaScript 侧使用时和普通 `newMetaObject()` 对象没有区别：

```js
const file = native.createFile('internal://files/config.json')
console.log(file.resolvedUri())
```

这个例子里，`resolvedUri()` 没有 `JsCtx` 参数，但它仍然可以访问 `applet()`，因为对象在创建时已经绑定到了当前应用。

::: warning `BindableObject` 的两个前提
使用 `BindableObject` 时要额外注意两点：

- `BindableObject` 默认带有 `ExplicitDeleteKind`。这意味着它**不会**因为 JavaScript 对象被 GC 而自动销毁。如果你希望它回到普通 Native Object 那样的 GC 行为，可以像上面的示例一样，用 `GX_OBJECT_KINDS(NoneKind)` 覆盖这个默认值。
- `BindableObject` 必须和 `Applet` 绑定，否则 `applet()` 永远是空指针，上下文也无从谈起。最简单的做法是在构造函数里调用 `BindableObject(applet)`，或者在创建后立刻绑定到当前 `Applet`。
:::

::: important 旧版行为
v0.8.0 正式版之前 `PrimitiveObject::objectKinds()` 行为与本文档不一致，请勿参考旧版本的实现细节。
:::

`BindableObject` 不是 [`newMetaObject()` 导出](#newmetaobject-导出)的替代品，而是“当对象方法需要记住所属应用上下文时”的专门方案。只有确实需要在 `GX_METHOD` 内访问 `Applet` 时，再引入这个概念。

#### `newObject()` 并手动导出方法

有时你并不想把整个元对象接口都暴露出去，而是只想把 C++ 对象作为一个不透明句柄挂到 JavaScript 对象上，再手动决定哪些方法可以调用。此时可以使用 `vm.newObject()` 来导出对象。

这种方式下，`GX_PROPERTY` 和 `GX_METHOD` **不会**自动暴露，所以你需要自己把方法挂到对象上：

```cpp
class CounterCore final : public PrimitiveObject {
    GX_OBJECT

public:
    explicit CounterCore(int initial = 0) : m_value(initial) {}

    int value() const { return m_value; }
    void add(int delta) { m_value += delta; }

private:
    int m_value = 0;
};

static JsValue createManualCounter(JsCtx ctx) {
    int initial = ctx.argc() >  ? ctx.arg(0).asInt(0) : 0;

    JsVM &vm = ctx.vm();
    JsValue obj = vm.newObject(new CounterCore(initial));

    obj["add"] = [](JsCtx ctx) -> JsValue {
        auto *counter = dyn_cast<CounterCore *>(ctx.thisObject().object());
        if (!counter)
            return {};
        counter->add(ctx.arg(0).asInt(0));
        return {};
    };

    obj["get"] = [](JsCtx ctx) -> JsValue {
        auto *counter = dyn_cast<CounterCore *>(ctx.thisObject().object());
        if (!counter)
            return {};
        return counter->value();
    };

    return obj;
}
```

JavaScript 侧看到的是一个普通对象：

```js
const c = counter.createManualCounter(10)
c.add(5)
console.log(c.get()) // 15
```

这种写法的特点是：JavaScript API 形状完全由你决定，但每个方法内部都要自己从 `this` 对象里取回底层 C++ 指针，并用 `dyn_cast` 检查类型。相比 `newMetaObject()`，样板代码更多，也更容易漏掉检查。

不过它也有一个直接的好处：这些手动挂上的函数本质上就是普通的 `JsCtx` 回调，因此可以像模块函数一样直接通过 `Applet::current(ctx.vm())` 获取当前应用上下文。这也是它和 `GX_METHOD` 的一个重要区别。

这个方法还不能导出属性访问器（getter / setter），而只能导出固定的属性值。

#### 使用 `newProxy()` 导出对象

如果你需要把属性读写、方法查找、惰性生成字段等行为全部接管，也可以使用 `vm.newProxy()`。这种方式可以实现非常动态的接口，例如：访问任意属性名时转发到底层字典、按需生成子对象、拦截写入做校验。

但它也有明显代价：

- 读属性、写属性、方法调用的行为都分散在代理逻辑里；
- API 形状不再像 `newMetaObject()` 那样由类定义直接表达；
- 一旦行为复杂，排查问题会比较麻烦。

因此，`newProxy()` 更适合少量非常动态的桥接场景，而不适合拿来替代常规的对象导出。

#### 生命周期规则

Native Object 的销毁规则不是由 `newMetaObject()` 单独决定的，而是由 C++ 对象的 `objectKinds()` 决定：

- 如果对象包含 `RootKind`，且**没有** `ExplicitDeleteKind`，那么对应的 JavaScript 对象被 GC 回收时，C++ 对象也会被自动销毁；
- 如果对象是别的对象的子节点，或者声明了 `ExplicitDeleteKind`，那么它的生命周期仍由 C++ 侧负责。

对大多数“独立包装对象”来说，直接继承 `PrimitiveObject` 且不额外声明 `ExplicitDeleteKind`，通常就能得到合适的默认行为，也就是随 GC 自动销毁。

如果你不熟悉这些对象生命周期标记，建议先阅读[对象系统](./object-system.md)中关于 `PrimitiveObject` 的章节，再决定是否把对象交给 JavaScript GC 管理。

#### 从 `JsValue` 取回 Native Object

有时另一个 Native Module 函数会接收这个对象作为参数，此时可以从 `JsValue` 临时取回底层 C++ 指针：

```cpp
static JsValue getCounterValue(JsCtx ctx) {
    if (ctx.argc() < 1 || !ctx.arg(0).isObject())
        return {};

    auto *counter = dyn_cast<NativeCounter *>(ctx.arg(0).object());
    if (!counter)
        return {};
    return counter->value();
}
```

`object()` 只提供**临时访问**，不会转移所有权。如果你确实需要把对象从 JavaScript 一侧“拿走”，应使用模板形式的 `moveObject<T>()`：

```cpp
auto *counter = value.moveObject<NativeCounter>();
```

**不要**写成下面这种形式：

```cpp
auto *counter = dyn_cast<NativeCounter *>(value.moveObject());
```

一旦类型不匹配，这段代码会在转型失败后丢失对象所有权，造成泄漏。API 文档也明确建议优先使用 `moveObject<T>()`，把“类型检查”和“所有权转移”合并成一步。

::: warning 什么时候不要导出 Native Object
如果你只是想返回一份简单结果数据，例如设备信息、一次性计算结果、配置快照，优先返回普通 `newObject()` 构造的 JavaScript 对象即可。只有当 JavaScript 需要在后续持续操作同一个 C++ 实例时，才值得引入 Native Object。
:::

## 模块的定义与注册

掌握了 JsVM 桥接层的基本工具之后，就可以将 C++ 函数组装为一个完整的 Native Module。一个模块由两部分组成：一个**工厂函数**，负责创建模块对象并将 C++ 函数挂载到其上；以及一个**注册宏**，负责将工厂函数注册到框架的模块系统中。

::: tip
如果是开发非标准的系统扩展，建议优先考虑使用 [Library Loader](#library-loader) 机制。
:::

### 模块结构

以实现一个设备信息模块 `@vendor.device` 为例：

```cpp
#include "gx_jsvm.h"

using namespace gx;

// 模块中的 C++ 函数
static JsValue getDeviceName(JsCtx ctx) {
    return "MyDevice-Pro";
}

static JsValue getBatteryLevel(JsCtx ctx) {
    int level = /* 从驱动读取电量 */ 85;
    return level;
}

// 工厂函数：构建模块对象并返回
static JsValue createDeviceModule(JsVM &vm) {
    JsValue mod = vm.newObject();
    mod["getDeviceName"] = getDeviceName;
    mod["getBatteryLevel"] = getBatteryLevel;
    return mod;
}

// 注册模块，使其在 JavaScript 中以 @vendor.device 路径可访问
GX_JSVM_MODULE(vendor_device, "vendor.device", createDeviceModule)
```

`GX_JSVM_MODULE` 宏接受三个参数：C++ 变量名、JavaScript 模块路径（不含 `@` 前缀）、工厂函数。工厂函数在模块首次被 `import` 时调用，返回的 `JsValue` 对象即为 JavaScript 侧拿到的模块。

在 JavaScript 侧，应用这样使用该模块：

```js
import device from '@vendor.device'

const name = device.getDeviceName()
const battery = device.getBatteryLevel()
```

::: tip 这是个 Demo!
这看起来相当简单，只是忽视了一个大问题：大部分 API 都是异步的！我们根本不应该在 JavaScript 执行上下文，也就是 UI 线程读取电量，除非真的在做 demo。对于异步 API，请参阅[异步功能开发](./async.md)章节，那里有更合适的模式和示例。
:::

### 启用模块

仅仅声明模块还不够，还需要在框架初始化时将其“安装”到 JavaScript 引擎中。这通过 `GX_JSVM_MODULE_IMPORT` 宏完成：

```cpp
GX_JSVM_MODULE_IMPORT(vendor_device)
```

`GX_JSVM_MODULE` 在文件作用域声明一个全局变量，`GX_JSVM_MODULE_IMPORT` 查找并调用这个变量的 `install()` 方法。两个宏的名称参数（第一个参数）必须一致。

一个常见的做法是将所有 `GX_JSVM_MODULE_IMPORT` 调用集中在一个函数中，方便管理：

```cpp
void installVendorModules() {
    GX_JSVM_MODULE_IMPORT(vendor_device)
    GX_JSVM_MODULE_IMPORT(vendor_sensor)
    GX_JSVM_MODULE_IMPORT(vendor_bluetooth)
}
```

在 `AppletKit` 初始化之后调用 `installVendorModules()`，确保模块在应用启动时就可用。

## Library Loader

Native Module 适合实现框架级的、对所有应用普遍可用的系统 API。但对于**非标准的系统定制功能**，例如厂商专属的数据访问、私有 SDK 封装，或只对特定授权应用开放的能力，更推荐使用 **Library Loader** 机制。

Library Loader 通过 `@system.app` 模块提供的 [`loadLibrary()`](/api/system-app.md#loadlibrary) 方法按名称加载：

```js
import app from '@system.app'

const lib = app.loadLibrary('custom-library')
lib.someFunction()
```

与 Native Module 相比，Library Loader 有两个显著优势：

- **无需全局注册**：不依赖 `GX_JSVM_MODULE` 宏和 `GX_JSVM_MODULE_IMPORT`，模块对象在调用时才按需创建；
- **易于模拟器回退**：应用侧可以通过检测 `loadLibrary()` 的返回值是否为 `undefined`，在通用模拟器环境中优雅地降级到脚本实现的 stub，而 `import lib from '...'` 这类模块导入的 stub 技巧则较为 hacky 且反模式。

```js
import app from '@system.app'

// 尝试加载原生库，在模拟器中回退到脚本 stub
const nativeLib = app.loadLibrary('custom-library')
const lib = nativeLib || {
    someFunction() { /* 模拟器实现 */ }
}
```

除了注册方式和 JavaScript 侧的使用方式不同，Library Loader 与 Native Module 的其他方面基本相同。

### 注册 Library Loader

在 C++ 侧，通过 `AppletKit::setLibraryLoader()` 注册一个加载器函数。加载器接收发起调用的 `Applet` 实例，返回库对象（一个 `JsValue`）：

```cpp
#include "gx_appletkit.h"
#include "gx_jsvm.h"

using namespace gx;

static JsValue getDeviceName(JsCtx ctx) {
    return "MyDevice-Pro";
}

void installLibraries() {
    AppletKit::instance()->setLibraryLoader(
        "custom-library",
        [](Applet *applet) -> JsValue {
            JsVM &vm = JsVM::current();
            JsValue lib = vm.newObject();
            lib["someFunction"] = getDeviceName;
            return lib;
        }
    );
}
```

`setLibraryLoader()` 在 `AppletKit` 初始化之后调用即可，无需在每次应用启动时重复注册。

Library Loader 的加载器接收的是 `Applet *`，因此可以直接在入口处进行**应用权限验证**，对未授权的应用拒绝提供功能，而不必在每个模块函数内部重复检查：

```cpp
AppletKit::instance()->setLibraryLoader(
    "custom-library",
    [](Applet *applet) -> JsValue {
        // 权限检查：在入口处统一拦截未授权访问
        if (!applet || !applet->permission(vendor::Permission::AccessCustomLib))
            return vm.newError("permissions denied"); // 返回 undefined

        JsVM &vm = JsVM::current();
        JsValue lib = vm.newObject();
        lib["someFunction"] = getDeviceName;
        return lib;
    }
);
```

如果加载器返回 `undefined`（即默认构造的 `JsValue()`），`app.loadLibrary()` 在 JavaScript 侧同样得到 `undefined`，应用可以据此进行回退处理。

::: tip
加载器函数在权限检查失败时不建议抛出异常，而是默认返回 `undefined`。除了让 JavaScript 侧能够简单降级之外，这还能避免泄漏模块存在性信息（如果不希望未授权应用知道这个库的存在）。
:::

## 与应用沙箱协作

前面章节介绍的模块函数都是无状态的——接收参数、返回结果、不持有任何上下文。但很多实际场景需要模块与当前运行的应用产生关联：读取应用的资源路径、语言设置，或者将一个长生命周期的 C++ 对象托管在应用沙箱中。这就需要用到 `Applet` 提供的能力。

### 获取当前应用上下文

通过 `Applet::current()` 获取调用方所属的应用实例：

```cpp
#include "gx_applet.h"

static JsValue readPreference(JsCtx ctx) {
    auto applet = Applet::current(ctx.vm());
    // 由于后续操作依赖 applet，务必检查是否成功获取到上下文
    if (!applet) return JsValue();

    // 读取应用私有的存储路径
    String storagePath = applet->resolveUri("internal://files/preferences.json");
    // ...
}
```

`Applet` 实例由框架自动管理，每个应用在各自独立的 JavaScript Realm 中运行。`Applet::current()` 通过当前 Realm 推导出对应的应用实例，因此同一个模块函数在不同应用中调用时，获取到的是各自独立的上下文。

### 资源生命周期管理

如果模块函数需要分配一个长期存活的 C++ 对象（例如一个持续监听硬件状态的后台任务），**绝不要**使用全局变量或裸指针跨调用持有资源——这会让资源逃逸应用沙箱的追踪，既导致应用退出后资源无法释放，也同时失去了沙箱赋予你的关键安全保证。

这里存在一个严肃的安全要求：**Native Module 必须保证，所有访问 C++ 对象的操作路径都经过严格的所有权和类型校验**，而不是仅仅提供"合法路径"、留下能够绕过它的可能。做到这一点的正确方法是将对象生命周期完全委托给 `Applet` 沙箱管理，并在**每一个**接收整数句柄的模块函数中强制使用 `takeObject<T>()` 进行校验——这是不可省略的不变式，下文会展开说明。

以下以持续监听传感器状态的功能为例，演示这种安全的生命周期绑定机制。

::: tip
本节代码实际上是 [异步功能开发](./async.md) 章节中 `AsyncSession` 原理的一个简陋平替，仅用于演示概念。在实际的业务开发中，强烈推荐直接使用成熟的 `AsyncSession` 相关设施来处理异步任务，它们在底层也是基于本节介绍的方法实现的。
:::

假设我们有一个传感器，应用需要在初始化时开启监听，随后多次读取最新数据，并在不需要时手动停止监听。首先，我们定义这个后台任务的载体：

```cpp
class SensorListener : public PrimitiveObject {
    GX_OBJECT
public:
    SensorListener() {
        // 启动传感器，请求底层驱动硬件资源...
    }
    ~SensorListener() override {
        // 停止传感器，释放相关硬件资源...
    }
    int latestValue() const { return m_value; }

private:
    int m_value = 0;
};
```

#### 绑定对象到沙箱

使用 `Applet::bindObject()` 将实例绑定到当前应用沙箱，返回一个整数句柄供 JavaScript 侧持有：

```cpp
static JsValue startSensor(JsCtx ctx) {
    auto applet = Applet::current(ctx.vm());
    if (!applet) return {};

    auto *listener = new SensorListener();
    // 将对象交由 Applet 管理，并获得一个整数句柄 (ID)
    int bindId = applet->bindObject(listener);

    // 将 ID 返回给 JavaScript，用作后续操作该对象的唯一凭证
    return bindId;
}
```

由于对象现在是被沙箱**托管**的，即使应用在任务途中退出或被系统强杀，沙箱也会在销毁时自动清理所有绑定的对象，从而避免资源泄漏。

#### 安全地取回对象

当 JavaScript 侧需要操作之前创建的对象时，**必须**通过 `Applet::takeObject<T>()` 根据句柄取回实例，而不能做任何形式的“裸转换”：

```cpp
static JsValue readSensor(JsCtx ctx) {
    auto applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1) return {};

    int bindId = ctx.arg(0).asInt();
    auto *listener = applet->takeObject<SensorListener>(bindId);
    if (!listener) return {}; // 若 ID 无效或类型不匹配，返回 nullptr

    return listener->latestValue();
}
```

`applet->takeObject<T>()` 仅访问属于**当前沙箱**的 ID（防止跨应用越权访问），然后通过对象元信息验证**类型匹配**。只有两层都通过才返回非空指针。

::: danger 必须通过 `takeObject<T>()` 访问对象
来自 JavaScript 的整数 ID 在 C++ 侧是完全不可信的——它可能是伪造的，或者是过期引用。缺乏校验的做法会导致严重的安全漏洞：

```cpp
// ❌ 绝对不要这样做！
static JsValue readSensor(JsCtx ctx) {
    auto bindId = ctx.arg(0).asInt();
    // 只用非模板版本的 takeObject + static_cast，绕过了类型检查和沙箱边界检查
    auto *binded = applet->takeObject(bindId);
    // 危险：static_cast 没有运行时检查，这里的 binded 可能根本不是 SensorListener！
    auto *listener = static_cast<SensorListener *>(binded);
    return listener->latestValue(); // 可导致任意内存读写
}
```
:::

#### 解绑与销毁

当需要从 C++ 侧主动终止任务并彻底释放资源时，先用 `takeObject<T>()` 取回并校验类型，再 `unbindObject()` 解除托管，最后手动销毁：

```cpp
static JsValue stopSensor(JsCtx ctx) {
    Applet *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1) return {};

    int bindId = ctx.arg(0).asInt();
    auto *listener = applet->takeObject<SensorListener>(bindId);
    if (listener) {
        applet->unbindObject(listener); // 从自动管理列表中解除绑定
        delete listener;                // 手动销毁
    }
    return {};
}
```

JavaScript 前端侧的完整使用流程：

```javascript
import sensor from '@vendor.sensor'

// 启动并暂存凭证
const id = sensor.startSensor()
// ...多次读取
const value = sensor.readSensor(id)
// 任务结束，释放资源
sensor.stopSensor(id)
```

由于 `bindObject` 提供的托底支持，即使应用忘记调用 `stopSensor()`，沙箱退出时也会自动释放所有绑定的对象。


::: important 必须自动解绑
由于不信任 JavaScript 代码，所以也不能假设其调用释放资源的函数。对恶意应用来说，由 JavaScript 引用泄漏导致的沙箱泄漏是有效的攻击手段。因此，**所有绑定到沙箱的对象都必须在沙箱销毁时自动解绑**，以确保无论 JavaScript 如何操作，都不会导致资源泄漏。

任何要求 JavaScript 侧解绑的设计都是危险的，必须避免。
:::

### 安全防护

尽管前面强调了许多安全要求，但这也许不足以消除所有风险。为了进一步加固安全防线，我们建议直接将扩展模块的访问权限限制在受信任的应用中。可以直接在模块工厂函数中检查 `Applet` 的权限标识或身份信息，拒绝不符合条件的访问：

```cpp
static JsValue createDeviceModule(JsVM &vm) {
    auto applet = Applet::current(vm);
    if (!applet || !applet->permission(
                    vendor::Permission::AccessDeviceInfo)) {
        // 如果没有权限，返回一个空对象或抛出异常
        return vm.newError("permissions denied");
    }

    // 只有授权后才能创建模块对象并暴露功能
    JsValue mod = vm.newObject();
    mod["getDeviceName"] = getDeviceName;
    // ...
    return mod;
}
```

这种策略可以在入口处有效阻止未经授权的访问。即便模块函数本身不够健壮，攻击者也无法利用它来获取敏感信息或执行恶意操作。

Library Loader 的入口权限检查已经在相关文档中介绍过。
