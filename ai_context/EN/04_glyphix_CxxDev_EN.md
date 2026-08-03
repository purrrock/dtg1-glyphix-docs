# Context File: 04_glyphix_CxxDev_EN.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/transl/EN/cxxdev/applet-install-flow.md

# 应用安装流程

Glyphix 是一个面向嵌入式设备的应用框架。设备出厂后，最终用户或厂商仍需要向设备添加应用——就像手机上安装 App 一样。但在资源受限的 MCU 上，“安装应用”具体意味着什么、框架如何找到并启动它，并不像手机那样广为人知。

本文档将介绍一个应用包在设备上安装 → 启动 → 卸载的完整流程，并解释目录配置如何影响应用的查找、更新与卸载。

## 在设备上“安装应用”

一个 Glyphix 应用在交付时是一个 `.pkg` 文件——这是一个只读的资源容器，内部包含应用的清单（`manifest.json`）、JavaScript 代码、图片等资源。应用运行时不会解包，框架直接从 `.pkg` 中按需读取文件。

**安装**一个应用，本质上做两件事：把这个 `.pkg` 文件放到设备上某个框架会扫描的目录里，并把它的包名登记到包数据库中。登记之后，框架就能通过包名找到对应的 `.pkg` 并启动它。**卸载**则是反向操作：删除 `.pkg` 文件、清理应用产生的数据、从数据库中注销。

::: tip 资源 bundle 格式
运行时使用完整的 `.pkg` 资源文件，而不是解压后的目录。这种 bundle 模式也常见于游戏引擎，因为应用资源包只会读取而不会写入，bundle 模式可以减少文件系统的碎片化，并避免一堆小文件过度占用文件系统的 inode。
:::

这里涉及两个角色，本教程面向后者：
- **应用开发者**：用 JavaScript 编写应用，通过 `gx build` 命令构建出 `.pkg` 文件并交付。
- **平台开发者**：在设备上集成 Glyphix 运行时，配置存放应用的目录，在 C++ 中调用安装与启动接口。你拿到的是一个 `.pkg` 文件，目标是让它跑起来。

::: tip
本教程假设你已有一个可运行的 Glyphix 平台骨架（`Application` + `JsVM` + `AppletKit`）。如果你还没有，参考 SDK 自带的 `examples/emulator` 示例。
:::

## 准备工作

开始前请确认以下条件就绪：

- 一个可运行的 Glyphix 平台。最小骨架如下，后续所有操作都在这个上下文里进行。
- 一个待安装的 `.pkg` 文件。可以从应用开发者处获取，或用 `gx build` 自行构建一个示例应用。本教程假设文件名为 `com.example.demo.pkg`，包名为 `com.example.demo`（包名写在应用的 [`manifest.json`](/framework/application/manifest.md#package) 里）。
- 设备上一个可写分区，用于存放 `.pkg` 文件与应用运行期数据。下文用 `/data` 代表这个分区。

一个简单的 Glyphix 平台骨架是这样的（这不是伪代码，就是这么简单）：

```cpp
#include "gx_application.h"
#include "gx_appletkit.h"
#include "gx_jsvm.h"
#include "gx_widget.h"

using namespace gx;

int main() {
    Application app{new MyPlatform}; // 平台适配，需按设备接入
    JsVM vm;                         // JavaScript 运行时
    Widget window;                   // 所有应用的父窗口
    AppletKit kit(&window, "/pkgs.db"); // 第二个参数是包数据库路径
    // ...本教程的配置与安装代码写在这里
    return app.exec();
}
```

::: tip `AppletKit` 的第二个参数
它指向一个“包数据库”文件（如 `/pkgs.db`）。`AppletKit` 用它记录已安装应用的信息。可以通过 `kit.database(ADBT_Applet)` 拿到一个 `PackageDatabase` 对象来查询已装应用列表，后文会用到。
:::

## 告诉框架应用放在哪里

在安装任何应用之前，必须先告诉 Glyphix 两类目录的位置：**应用包目录**（存放 `.pkg` 文件）和**应用数据目录**（存放应用运行时产生的数据）。二者职责不同，不要混淆。

### 应用包目录

应用包目录由 `EnvPath::packages()` 管理。它是一个列表，列表中每个条目指向一个存放 `.pkg` 的目录。这个列表同时承担多个语义，理解它们是后续一切配置的基础：

- **查找**：当框架需要加载 `pkg://com.example.demo/...` 这样的资源时，会**从前向后**遍历列表，在每目录下找 `com.example.demo.pkg`，首个命中即加载。
- **安装**：调用安装接口时，新包**固定写入列表的最后一个目录**。
- **卸载**：卸载时**从前向后**扫描，从第一个包含该包的目录中删除。

因为安装总是落在列表末尾、而查找与卸载从列表头部开始，目录在列表中的顺序就决定了它的角色：靠前的目录适合放“出厂自带、不希望被覆盖”的应用；靠后的目录适合放“用户后续安装”的应用。

::: important 前置条件
调用安装接口之前，`packages()` 列表必须至少有一个目录，且列表最后一个目录（即安装目标）必须存在且可写。否则安装会直接失败。
:::

配置方法是在平台初始化阶段向列表追加目录：

```cpp
#include "gx_environment.h"
using namespace gx;

// 在 Application 构造之后、安装/启动之前调用
EnvPath::packages().emplace_back("/data/apps");
```

### 应用数据目录

应用运行时需要可写的空间来存缓存、文件、临时数据等。这些目录由 `EnvPath::setEntry(role, path)` 配置，每个角色对应一种用途。它们的语义契约如下：

| 角色 | 含义 | 典型路径 |
|:---|:---|:---|
| `AppletCache` | 应用可写的缓存，框架可在空间紧张时清理重建 | `/data/cache` |
| `AppletFiles` | 应用私有文件，持久保留，不被自动清理 | `/data/files` |
| `AppletMass` | 大文件存储（如媒体资源），容量大 | `/data/mass` |
| `AppletTemp` | 临时文件，应用退出后可清理 | `/data/temp` |
| `AppletStorage` | 应用持久存储 | `/data/storage` |
| `LoggingDirectory` | 框架日志目录 | `/logs` |

**数据隔离**：框架按包名为每个应用在上述目录下创建独立子目录。例如应用 `com.example.demo` 的私有文件落在 `/data/files/com.example.demo/` 下。你无需手动管理这些子目录，框架在安装与卸载时会自动创建和清理它们。

此外还有一个特殊角色 `GlobalPackage`，它指向一个全局共享的 `.pkg`（如 `/global.pkg`），所有应用可通过 `pkg:///...` 协议读取其中的字体、图标等公共资源。它不属于某个应用，通常随固件一起烧录。

配置示例：

```cpp
EnvPath::setEntry(EnvPath::AppletCache,   "/data/cache");
EnvPath::setEntry(EnvPath::AppletFiles,   "/data/files");
EnvPath::setEntry(EnvPath::AppletMass,    "/data/mass");
EnvPath::setEntry(EnvPath::AppletTemp,    "/data/temp");
EnvPath::setEntry(EnvPath::AppletStorage, "/data/storage");
EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
```

::: tip 时机
`Application` 构造时会重置 `EnvPath` 为默认配置，因此自定义配置应紧随 `Application` 构造之后、任何 `installPackage`/`launch` 调用之前完成。配置晚了会导致意外情况。
:::

### 配置示例

把两类目录合起来，最小可用的初始化片段如下：

```cpp
Application app;
// 应用包目录：至少一个可写目录
EnvPath::packages().emplace_back("/data/apps");
// 应用数据目录：按设备实际分区调整
EnvPath::setEntry(EnvPath::AppletFiles,   "/data/files");
EnvPath::setEntry(EnvPath::AppletCache,   "/data/cache");
EnvPath::setEntry(EnvPath::AppletTemp,    "/data/temp");
EnvPath::setEntry(EnvPath::AppletStorage, "/data/storage");
EnvPath::setEntry(EnvPath::AppletMass,    "/data/mass");

JsVM vm;
Widget window;
AppletKit kit(&window, "/pkgs.db");
```

## 安装一个应用

在调用 `installPackage` 之前，需要确认：

1. `EnvPath::packages()` 列表非空，且其最后一个目录存在且可写。
2. `AppletKit` 已构造（安装需要写入它管理的包数据库）。
3. 待安装的 `.pkg` 文件已存在于设备文件系统中（例如位于 `/tmp/com.example.demo.pkg`）。
4. 若使用默认的版本校验策略（`NormalVerify`），设备的 vendor/product ID 应已配置；否则安装会因设备 ID 校验失败而返回 `InvalidDevice`。

### 调用安装

安装接口是 `AppletKit::installPackage(fileUri, policy)`，第一个参数是 `.pkg` 文件路径，第二个是校验策略，可省略（默认 `NormalVerify`）：

```cpp
auto status = kit.installPackage("/tmp/com.example.demo.pkg");
if (status != AppletKit::ValidPackage) {
    LogError() << "install failed:" << AppletKit::packageStatusMessage(status);
    return;
}
LogInfo() << "install ok";
```

返回值是 `PackageStatus`，常见的几种含义：

| 状态 | 含义 |
|:---|:---|
| `ValidPackage` | 安装成功 |
| `FileNotExists` | `.pkg` 文件路径不存在 |
| `InvalidPackage` | 包损坏或清单不可读 |
| `InvalidVersion` | 版本不满足校验策略 |
| `InvalidDevice` | 设备 vendor/product ID 不匹配 |
| `FileIOError` | 拷贝失败，通常是安装目录不可写或空间不足 |

校验策略 `PackageVerify` 决定框架对安装包的严格程度：

| 策略 | 版本校验 | 设备 ID 校验 |
|:---|:---|:---|
| `NormalVerify`（默认） | 新版本不得低于已装版本 | 必须 |
| `UpgradeOnly` | 必须严格高于已装版本 | 必须 |
| `IgnoreVersion` | 跳过 | 必须 |
| `NoVerify` | 全部跳过，只要包合法即可 | 跳过 |

::: tip
首次安装调试时如果遇到 `InvalidDevice` 或 `InvalidVersion`，可临时用 `AppletKit::NoVerify` 排除校验干扰，确认安装流程本身没问题，再恢复正式策略。
:::

### 安装会做什么

`installPackage` 对外保证以下效果：

- 校验 `.pkg` 文件合法，并按所选策略检查版本与设备 ID。
- 若同名应用正在运行，会先退出（terminate）它，避免文件占用或数据冲突。
- 把 `.pkg` 文件拷贝到 `packages()` 列表的最后一个目录下，文件名为 `<package-name>.pkg`。若已存在同名文件则覆盖。
- 在包数据库中登记该应用，记录其安装路径与 `pkg://<package-name>` 访问 URI。
- 若应用清单声明了 URI scheme（例如把自己注册为 `ime` 输入法的处理者），一并登记。
- 发出“包已变更”通知，使框架其他部分感知到新应用。

::: important 包校验能力
`AppletKit::installPackage()` 本身没有文件完整性或签名校验能力。设备厂商需要自行开发相关功能，并在调用 `installPackage()` 之前对 `.pkg` 文件进行校验，并对安装过程的文件系统断电保护、回滚等做一致性保障。框架只保证在 `.pkg` 文件合法、可读、可写的前提下完成安装。
:::

### 观察清单

安装返回 `ValidPackage` 后，可以用以下方式验证效果：

- 在安装目录下应能看到文件：`/data/apps/com.example.demo.pkg`。
- `kit.database(ADBT_Applet)->contains("com.example.demo")` 应返回 `true`。
- `kit.installedApplets()` 返回的列表应包含 `"com.example.demo"`。

```cpp
EXPECT_TRUE(File::exists("/data/apps/com.example.demo.pkg"));
EXPECT_TRUE(kit.database(ADBT_Applet)->contains("com.example.demo"));
EXPECT_NE(std::find(kit.installedApplets().begin(),
                    kit.installedApplets().end(),
                    "com.example.demo"),
          kit.installedApplets().end());
```

## 启动并观察

安装只是把包放到位，要让应用真正显示出来，需要调用 `AppletKit::launch(name)`，`name` 就是清单里的包名：

```cpp
Applet *applet = kit.launch("com.example.demo");
if (!applet)
    LogError() << "launch failed";
```

`launch` 返回指向应用对象的指针，失败返回 `nullptr`。成功后应用会进入前台显示。

::: tip 依赖说明
`launch()` 能否让应用真正显示，还取决于 JavaScript 引擎、窗口系统、平台图形适配以及应用自身代码是否就绪。如果 `launch()` 返回非空但屏幕无显示，问题通常出在上述其他系统，而非安装流程。
:::

启动成功后可验证：

- 应用界面出现在窗口中（依赖上述系统就绪）。
- 应用运行并写入数据后，其私有目录出现：`/data/files/com.example.demo/`。
- 通过 `pkg://com.example.demo/<asset-path>` 可访问应用包内资源（可以通过 `File` 类操作）。

## 卸载一个应用

卸载接口是 `AppletKit::removePackage(package)`，传入包名，返回 `bool` 表示是否找到并删除了包文件：

```cpp
if (!kit.removePackage("com.example.demo"))
    LogError() << "uninstall failed: package not found";
```

卸载对外保证的效果：

- 若该应用正在运行，先结束它。
- 从 `packages()` 列表第一个含该包的目录中删除 `.pkg` 文件。
- 删除该应用在各数据目录下的子目录（`AppletCache`/`AppletFiles`/`AppletTemp`/`AppletStorage` 下的 `<package-name>/`）。
- 从包数据库中注销该应用。

卸载后验证：

- 安装目录下的 `/data/apps/com.example.demo.pkg` 已消失。
- `/data/files/com.example.demo/` 等数据子目录已被清除。
- `kit.installedApplets()` 不再包含 `"com.example.demo"`。

## 进阶：系统预装应用目录

许多设备需要区分两类应用：**出厂预装、不可卸载**的系统应用，与**用户后续安装、可卸载**的用户应用。利用 `packages()` 列表的顺序语义，可以用两个目录实现这种分层。

### 使用场景

出厂预装的应用（如系统表盘、设置应用）通常烧录在只读闪存中，不应被用户卸载或覆盖。用户安装的应用则应落在可写分区，可随时增删。如果只用一个目录混放两者，后续的应用更新或卸载管理会变得复杂。

### 推荐布局

向 `packages()` 追加两个目录，顺序敏感，预装只读目录在前，用户可写目录在后：

```cpp
EnvPath::packages().emplace_back("/system/apps");  // 只读预装，置于前
EnvPath::packages().emplace_back("/data/apps");    // 可写用户安装，置于后
```

回看第一步的[应用包目录](#应用包目录)，这个布局下三种操作的语义如下：

- **查找**从前向后，预装目录在前，出厂应用优先命中，保证稳定加载。
- **安装**写列表最后一个目录，即用户区，新装应用不会污染预装目录。
- **卸载**从前向后，从首个含该包的目录删除。

### 保护机制：调用侧白名单

顺序语义只决定应用的存储路径和启动查找流程，并不能阻止用户卸载预装应用，内置的 <code>AppletKit&#8203;::&#8203;removePackage</code> 没有“预装”或“受保护”的概念。因此设备的卸载入口应由 native 代码实现，在其中维护一份预装包名白名单，在调用 `removePackage` 前拦截：命中白名单则拒绝卸载。

安装侧不需要白名单。设备厂商的安装渠道（应用商店、预置推送等）本身受控，应用包名的合法性由签名机制保证，不属本层职责；并且由于前向 resolve 的遮蔽（见下方“已知限制”），预装应用的运行时升级本就无法生效，无需额外阻止覆盖安装。因此安装可直接调用 `kit.installPackage`。

一个 native 卸载包裹层的示意：

```cpp
#include "gx_hashset.h"

class PackageManager {
public:
    PackageManager(AppletKit &kit, HashSet<String> preinstalled)
        : m_kit(kit), m_preinstalled(std::move(preinstalled)) {}

    auto install(const String &packageUri) {
        return m_kit.installPackage(packageUri);
    }

    bool uninstall(const String &packageName) {
        if (m_preinstalled.count(packageName)) {
            LogWarning() << "refuse to uninstall protected package:" << packageName;
            return false;
        }
        return m_kit.removePackage(packageName);
    }

private:
    AppletKit &m_kit;
    HashSet<String> m_preinstalled;
};
```

::: tip 只读挂载与白名单
把预装分区以只读方式挂载仍是推荐做法（防止意外写入），但它不是卸载保护的依赖项。即便预装目录可写，白名单也会在调用 `removePackage` 前拦截。

`EnvPath::Entry` 的 permission 字段不参与应用包目录的决策，只对应用数据目录约束 JavaScript 代码的访问。
:::

### 恢复出厂设置

利用预装目录与用户目录的分离，恢复出厂设置可以实现为：删除用户目录下的所有 `.pkg` 文件，并重置 `pkgs.db`；系统目录中的预装包不受影响。运行时安装固定写入 `packages().back()`（用户目录），从不覆盖系统目录中的预装副本，因此清空用户目录并重置数据库后，预装应用仍能被 `pkg://` 正常解析加载。

可选地，可实现“卸载预装应用的更新”——即删除某个预装应用在用户目录中的更新副本，使其回退到系统目录中的出厂版本。该能力目前仅具备实现可能，尚未正式支持。

### 已知限制

以下框架行为需要 native 业务层主动规避或留意：

1. **预装应用的应用商店升级无法实现**。当前 `pkg://<name>` 的资源解析对 `packages()` 列表做前向遍历，而运行时安装固定写 `packages().back()`（用户目录）。若尝试通过运行时安装升级预装应用，新版会落到用户目录，却因前向命中被系统目录的旧版遮蔽，永远无法生效。该升级能力待实现。
2. **卸载无“受保护”概念**。`removePackage` 只按“首个删除成功”定位，会无差别删除任何目录中的包，没有“是否为预装包”的标记。白名单拦截必须由 native 调用方实现，框架不提供该判断。
3. **表盘包卸载未清理数据库**。`removePackage` 只从应用表（`ADBT_Applet`）注销，对表盘包（`ADBT_Dial`）的数据库条目不做清理，会留下陈旧记录。这是框架的待办项，native 卸载逻辑如需支持表盘需自行处理。
4. **应用包目录条目的 permission 字段无效**。`EnvPath::Entry` 的 permission 不参与 `packages()` 列表的查找/安装/卸载决策，只对应用数据目录约束 JavaScript 代码的访问。无法用它表达“此目录禁止安装”。

## 平台初始化模板

下面给出三种典型场景的完整 `EnvPath` 配置，可直接复制后按设备路径调整。所有配置都必须在 `Application` 构造之后、<code>AppletKit&#8203;::&#8203;launch</code>/`installPackage` 之前完成。

### 宿主模拟器

最简配置，单目录存放应用：

```cpp
os::chroot(".");
EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
EnvPath::packages().emplace_back("/apps");
```

### 嵌入式目标（单分区）

只有一个可写分区的设备，应用与数据共置：

```cpp
EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
EnvPath::setEntry(EnvPath::AppletCache,   "/data/cache");
EnvPath::setEntry(EnvPath::AppletFiles,   "/data/files");
EnvPath::setEntry(EnvPath::AppletMass,    "/data/mass");
EnvPath::setEntry(EnvPath::AppletTemp,    "/data/temp");
EnvPath::setEntry(EnvPath::AppletStorage, "/data/storage");
EnvPath::packages().emplace_back("/data/apps");
```

### 带预装分区的设备

预装只读分区与用户可写分区分离：

```cpp
EnvPath::setEntry(EnvPath::GlobalPackage, "/system/global.pkg");
EnvPath::setEntry(EnvPath::AppletCache,   "/data/cache");
EnvPath::setEntry(EnvPath::AppletFiles,   "/data/files");
EnvPath::setEntry(EnvPath::AppletMass,    "/data/mass");
EnvPath::setEntry(EnvPath::AppletTemp,    "/data/temp");
EnvPath::setEntry(EnvPath::AppletStorage, "/data/storage");

// 顺序敏感：预装只读目录在前，用户可写目录在后
EnvPath::packages().emplace_back("/system/apps");
EnvPath::packages().emplace_back("/data/apps");
```

完成配置后，即可按第二、三步安装并启动应用。建议第一次跑通时用 `AppletKit::NoVerify` 装一个简单的示例包，确认 `/data/apps` 下出现 `.pkg`、`launch` 返回非空，再逐步恢复正式校验策略与预装布局。


============================================================
FILE_PATH: src/transl/EN/cxxdev/async-examples.md

# 异步开发示例

如果你感觉[异步功能开发](async.md)的章节内容过多且不够直观，本文档将提供一些典型的、较为简单的示例，帮助你应对一些常见的异步开发场景。

这些场景并不极端复杂，但侧重于：
- 一个典型的异步调用模式，重点在于跨线程、跨语言的调用关系；
- 这些场景可能更琐碎，存在一大批需要对接的系统 API，对代码膨胀较为敏感；
- 存在典型的 C API 交互需求，而不是标准的 C++ 接口。

你可以在 SDK 示例中找到这些场景的完整实现，并可以直接在 PC 上模拟运行。

## 场景：对接 C 闹钟接口

嵌入式系统中常见的异步模式是“C 回调”：调用方提交一个任务，并传入一个函数指针作为完成通知，操作完成后由 worker 线程调用该回调。

::: important async 只支持线程模型
Glyphix 框架的异步功能只支持普通的线程上下文，不能在中断中使用。如果你的异步上下文是中断处理程序，那么应该配备一个线程来中转。
:::

这里以一个闹钟服务为例。它提供的 C 异步接口是这样的：

```c
// 以 alarm_async_create 为例，其他操作的形式类似
void alarm_async_create(AlarmService *svc, uint32_t interval_ms, ...,
                        alarm_create_cb_t done_cb, void *done_ctx);

// 完成回调的函数指针类型，在 worker 线程被调用
typedef void (*alarm_create_cb_t)(alarm_err_t err, alarm_id_t id, void *ctx);
```

接下来说明如何将这类典型的 C 回调接口桥接到 JavaScript 的 Promise。

### 多个操作共用 Session 类型

闹钟服务有 `create`、`cancel`、`setEnabled`、`update`、`snooze`、`getInfo`、`list`、`count` 等一批操作。如果为每个操作单独定义一个客户端类（client），会产生大量模板实例化。

对于这类“实际逻辑均在 C 层完成，C++ 侧只做参数传递”的场景，可以定义一个只包含错误码映射的轻量客户端，让所有操作共用一个 `ResultSession` 实例化：

```cpp
struct AlarmClient {
    // 将 C 层的 alarm_err_t 转换为可读的错误字符串，
    // 供 Promise 被 reject 时传给 JavaScript 侧的 catch。
    static const char *errorMessage(async::Status status) {
        switch (status.value()) {
        case ALARM_OK:              return "ok";
        case ALARM_ERR_NOT_FOUND:   return "not_found";
        case ALARM_ERR_TABLE_FULL:  return "table_full";
        case ALARM_ERR_INVALID_ARG: return "invalid_arg";
        default:                    return "unknown_error";
        }
    }
};

// 所有闹钟操作共用这一个 Session 类型
using AlarmSession = async::ResultSession<AlarmClient>;
```

`AlarmClient` 不需要实现 `resolve()` 方法，因为这里不使用默认的线程池执行器，实际的异步操作由闹钟服务的 worker 线程完成，C++ 侧只负责将结果投递回 UI 线程。

### 基本绑定模式

以 `alarm.create()` 为例，展示完整的绑定流程：

```cpp
static JsValue jsAlarmCreate(JsCtx ctx) {
    auto *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1 || !ctx.arg(0).isObject())
        return JsValue{};

    // 从 JavaScript 传入的 options 对象中读取参数
    const JsValue &opts = ctx.arg(0);
    uint32_t intervalMs = static_cast<uint32_t>(opts["interval"].toInt());
    String label        = opts["label"].toString();
    alarm_repeat_t mask = parseRepeatMask(opts["repeat"]);

    // 创建会话，并从 options 对象中提取 resolve/reject 回调（支持两种异步风格）
    auto *session = async::make<AlarmSession>(applet);
    session->setResolver(opts);

    // C 回调：在 worker 线程中被调用，通过 resolve() 跨线程通知 JavaScript
    auto done = +[](alarm_err_t err, alarm_id_t id, void *data) {
        auto *s = static_cast<AlarmSession *>(data);
        s->resolve(err == ALARM_OK
            ? async::Result<int>(id) // 成功：resolve 新建的闹钟 ID
            : async::Status(err));   // 失败：reject，错误消息来自 errorMessage()
    };

    // 调用 C 服务的异步闹钟创建接口，传入回调和会话指针
    alarm_async_create(AppletAlarmService::instance(),
                       intervalMs, mask, label.c_str(), /*...*/,
                       onAlarmFired, nullptr, done, session);
    // 返回 Promise 对象给 JavaScript，框架会在 resolve() 被调用时自动决议它
    return session->promise();
}
```

这里有几个固定的套路，可以直接复制使用：

- `async::make<AlarmSession>(applet)` 创建会话并绑定到当前 Applet，以满足生命周期要求。
- `session->setResolver(opts)` 让同一套代码同时支持[回调风格和 Promise 风格](/api/README.md#快应用异步接口)的异步调用。
- `+[](... void *data)` 通过一元 `+` 将 lambda 转换为普通函数指针，满足 C 回调的类型要求。
- 将 `session` 作为 `void *` 透传给 C API，在回调中转型回来再调用 `resolve()`。
- `resolve()` 是线程安全的，它将结果封装为事件投递回 UI 线程，再驱动 Promise 的决议。

::: tip 利用 lambda 表达式写回调
在 C 中，回调函数通常是一个静态函数，可以使用 C++ 的 lambda 表达式直接就近嵌套定义回调函数，例如：
```cpp
auto done = +[](alarm_err_t err, alarm_id_t id, ...) { ... }
alarm_async_create(..., done, session);
```
这样可以避免定义一大批单独的静态函数，代码更紧凑清晰。
:::

其余操作（`cancel`、`setEnabled`、`snooze` 等）的结构完全相同，只有参数读取和 C API 调用不同：

```cpp
static JsValue jsAlarmCancel(JsCtx ctx) {
    auto *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1)
        return JsValue{};

    alarm_id_t id = ctx.arg(0).toInt();

    auto *session = async::make<AlarmSession>(applet);
    session->setResolver(ctx.arg(0));

    auto done = +[](alarm_err_t err, void *data) {
        // 没有返回值时，用 resolve<void> 即可
        static_cast<AlarmSession *>(data)->resolve<void>(async::Status(err));
    };
    alarm_async_cancel(AppletAlarmService::instance(), id, done, session);

    return session->promise();
}
```

::: important 不要遗漏参数检查
`session->setResolver(ctx.arg(0))` 依赖对 `ctx.argc()` 的检查。如果函数开头没有检查参数数量，那么要在调用 `setResolver()` 时检查参数数量：
```cpp
session->setResolver(ctx.argc() ? ctx.arg(0) : JsValue{});
```
:::

### 注册自定义 C 结构体的类型转换

`alarm.getInfo()` 返回一个 `alarm_info_t` 结构体，需要将它转换为 JavaScript 对象。为此，先在 `gx` 命名空间中特化 `js_cast<T>`：

```cpp
template<> JsValue gx::js_cast<alarm_info_t>(const alarm_info_t &info) {
    JsValue obj = JsVM::current().newObject();
    obj["id"]          = info.id;
    obj["label"]       = info.label;
    obj["interval"]    = double(info.interval_ms);
    obj["repeatMask"]  = info.repeat_mask;
    obj["enabled"]     = bool(info.enabled);
    obj["remaining"]   = double(info.remaining_ms);
    obj["fireCount"]   = int(info.fire_count);
    obj["snooze"]      = int(info.snooze_ms);
    obj["snoozed"]     = bool(info.snoozed);
    return obj;
}
```

特化完成后，在绑定函数中直接将结构体实例传给 `resolve()` 即可：

```cpp
auto done = +[](alarm_err_t err, const alarm_info_t *info, void *data) {
    auto *s = static_cast<AlarmSession *>(data);
    if (err != ALARM_OK || !info) {
        // 异常路径，返回错误状态触发 reject，错误消息来自 errorMessage()
        s->resolve<alarm_info_t>(async::Status(err));
        return;
    }
    s->resolve<alarm_info_t>(*info);  // 框架在 UI 线程自动调用 js_cast
};
alarm_async_get_info(AppletAlarmService::instance(), id, done, session);
```

::: tip
`js_cast()` 由框架在结果回到 UI 线程之后才调用，不在 worker 线程中执行。这意味着在 `js_cast()` 内部可以安全地使用 `JsVM::current()` 等 UI 线程专属 API。
:::

对于 `alarm.list()` 这种返回数组的情况，可以直接构造 `std::vector<int>` 并 resolve，无需定义额外的类型转换：

```cpp
auto done = +[](alarm_err_t /*err*/, const alarm_id_t *ids, int count, void *data) {
    auto *s = static_cast<AlarmSession *>(data);
    s->resolve<std::vector<int>>(std::vector<int>{ids, ids + count});
};
alarm_async_list(AppletAlarmService::instance(), done, session);
```

### 闹钟触发回调：将事件送回 JavaScript

闹钟触发时，C 层会从 worker 线程调用 `alarm_fire_cb_t` 回调。这个场景和前面的“查询结果”有些不同，需要专门设计事件通知机制。

#### 为什么不用 JavaScript 回调函数

直觉上，让应用在注册闹钟时传入一个回调函数似乎合理：

```javascript
// ❌ 这在闹钟场景下行不通
alarm.create({ interval: 60000, onFired: (event) => { /* ... */ } })
```

问题是，闹钟是跨越应用生命周期的：闹钟创建后，应用可能会在闹钟触发之前的任意时刻被杀死；许多设备还支持重启后触发闹钟。

一个 JavaScript 回调函数（`JsValue`）只在当前应用实例的 JavaScript 运行时中有效。一旦应用被关闭，这个运行时连同所有 `JsValue` 都会被销毁。此时 C++ 侧没办法继续保留这个 JavaScript 回调，更别说在闹钟触发时调用它了。

这不只是闹钟的问题，**任何可能在跨应用存活期触发的事件，都无法通过 JavaScript 回调解决**，例如定时任务、离线消息推送、后台下载完成通知等。

#### 使用约定方法名代替回调引用

最简单的解决方法是：不由应用“注册回调”，而是系统在事件发生时主动**启动**应用，并以约定好的方法名调用应用对象上的处理方法。

这与应用生命周期函数（`onCreate`、`onShow` 等）的思路一致——系统按需启动应用，调用已知的入口方法，而不是持有事先注册的回调。应用侧按约定实现对应方法即可：

```javascript
// app.js — 应用模型对象导出的处理方法（按约定实现）
export default {
  onAlarmFired(event) {
    // event: { id, label, interval, ... }
    console.log('alarm fired:', event)
  }
}
```

C++ 侧的实现：先在 worker 线程读取快照，再切回主线程启动应用并调用方法：

```cpp
static void onAlarmFired(alarm_id_t id, void * /*user_data*/) {
    // 在 worker 线程读取快照，避免跨线程访问闹钟表
    alarm_info_t info{};
    alarm_get_info(id, &info);

    // 切换回主线程再操作 JavaScript
    App()->postTask([info] {
        auto *svc = AppletAlarmService::instance();
        // 用 launch() 启动（或唤醒）目标应用，即使它当前不在运行
        auto *applet = AppletKit::instance()->launch(svc->alarmAppletName);
        if (!applet) return;

        auto &vm = JsVM::current();
        // 调用 app.js 导出对象上的约定方法，事件参数为闹钟信息的 JavaScript 对象
        JsValue event = js_cast(info);
        applet->modelObject().callMethod("onAlarmFired", {event}).reportError();
    });
}
```

几个要点：

- **不要**在 worker 线程中直接操作 `JsValue` 或调用任何 JavaScript API，它们只能在 UI 线程中使用。
- 使用 `App()->postTask()` 将闭包投递到主事件循环中执行，这是切回主线程最简单的方式。
- 用 `AppletKit::launch()` 而不是查找现有实例；`launch()` 在应用不存在时会重新启动它，在应用已经运行时则返回现有实例。
- `callMethod()` 返回值上的 `.reportError()` 会将可能发生的 JavaScript 异常打印到日志，而不是静默忽略。

::: tip 约定方法名是最简单的事件处理方式
可以将这种模式理解为：app.js 的导出对象就是应用暴露给系统的“入口点集合”，系统在需要时调用其中的方法，就像调用 `onCreate`、`onShow` 一样。

这种方法不太通用，但对受控的系统应用来说基本够用，且实现简单，不需要复杂的持久化和回调管理机制。
:::

### 注册库加载器

所有绑定函数编写完成后，还需要将它们“装配”成一个 JavaScript 可以导入的[库对象](native-module.md#library-loader)，并注册到框架中。

库加载器是一个在应用调用 `app.loadLibrary('vendor.alarm')` 时被触发的 C++ 函数，它负责创建并返回一个包含所有导出方法的 JavaScript 对象：

```cpp
static JsValue libAlarmLoader(Applet *applet) {
    // 可以在这里检查应用的包名，拒绝未授权的应用访问。也可以检查字段。
    if (!applet || applet->objectName() != "com.vendor.alarm")
        return JsValue{};

    JsValue lib = JsVM::current().newObject();

    // 将绑定函数挂载到库对象上，属性名就是 JavaScript 侧调用的方法名
    lib["create"]     = jsAlarmCreate;
    lib["cancel"]     = jsAlarmCancel;
    lib["list"]       = jsAlarmList;
    lib["count"]      = jsAlarmCount;
    // ...
    return lib;
}
```

然后在初始化阶段将加载器注册到 `AppletKit`：

```cpp
AppletKit kit{&window};
kit.setLibraryLoader("vendor.alarm", libAlarmLoader);
```

JavaScript 侧通过 `app.loadLibrary()` 导入，返回值就是加载器返回的库对象：

```javascript
const alarm = app.loadLibrary('vendor.alarm')

const id = await alarm.create({ interval: 60000, label: '起床' })
```


============================================================
FILE_PATH: src/transl/EN/cxxdev/async.md

# 异步功能开发

在嵌入式系统中，许多操作都是耗时的——读取闪存、访问网络、等待硬件响应。如果这些操作在 UI 线程（同时也是渲染线程）执行，就会冻结 UI，导致应用无响应。

Glyphix 通过将异步操作与 JavaScript 的 `Promise` 机制无缝对接来解决这个问题。C++ 侧负责真正的异步逻辑（通常在另一个线程或通过事件驱动），JavaScript 侧通过 `async/await` 或 `.then()` 等待结果，而 UI 在等待期间保持流畅。

## 核心机制

异步功能的核心是“会话（Session）”模型。当一个 JavaScript 异步调用发起时，C++ 侧创建一个**会话对象**（`AsyncSession`），立即返回一个 `Promise` 给 JavaScript；当操作完成时，会话驱动 `Promise` 的决议（resolve 或 reject），JavaScript 侧的 `then/catch` 或 `await` 随之得到执行。

会话对象绑定到发起调用的 `Applet`，当应用退出时会话会自动清理，开发者无需手动管理内存。

下图展示了异步会话在框架中的位置和核心组件：

<ArchDiagram max-width="520px">
  <div>
    JavaScript 应用层
    <div class="group row">
      <div>async/await<div class="remark">调用模块函数</div></div>
      <div>Promise<div class="remark">等待异步结果</div></div>
    </div>
  </div>
  <div class="subject">
    异步会话（C++）
    <div class="group row">
      <div>ResultSession<div class="remark">单次查询 · Promise 桥接</div></div>
      <div>Signal&lt;T&gt;<div class="remark">全局事件广播</div></div>
    </div>
    <div class="group row">
      <div>Client 类<div class="remark">纯 C++ · 无 JS 依赖</div></div>
      <div>SingleTimer<div class="remark">超时控制</div></div>
    </div>
  </div>
  <div>
    异步执行器
    <div class="group row">
      <div>线程池<div class="remark">默认后台执行</div></div>
      <div>自定义上下文<div class="remark">硬件驱动 · 事件循环</div></div>
    </div>
  </div>
</ArchDiagram>

异步框架的实现在 `gx_async.h` 中，并封装在 `gx::async` 命名空间内。该框架提供几种有用的设施：
- **`async::ResultSession`**：用于单次异步查询，适合读取文件、发起网络请求等场景。
- **`async::make_timeout()`**：用于创建一个单次定时器，为单次会话附加超时功能。
- **`async::Signal<T>`**：用于全局事件广播，适合设备状态变化、外部事件通知等场景。

## 单次查询 ResultSession

`async::ResultSession<T>` 适合“发起查询，等待单个结果”的场景，例如读取一个文件、发起一次网络请求。它是最常用的异步模式，工作方式类似于异步函数调用。

### 工作模型

一个 `ResultSession` 的完整生命周期如下：

1. **创建**：模块函数通过 `async::make<ResultSession<T>>(applet)` 创建会话，会话自动绑定到当前 `Applet`。
2. **配置**：通过 `session->client()` 访问客户端对象，设置任务所需的纯 C++ 参数。
3. **提交**：调用 `session->request(resolver)` 提交任务，立即返回一个 `Promise` 给 JavaScript。
4. **执行**：框架将客户端的 `resolve()` 方法转发到**异步执行器**（默认为后台线程池）执行。
5. **回报**：`resolve()` 返回后，结果被**自动调度回 UI 线程**，驱动 `Promise` 的 resolve 或 reject。
6. **清理**：会话对象在回报完成后自动销毁，或随 `Applet` 退出时自动清理。

::: important Client 类的隔离要求
客户端类（即模板参数 `T`）运行在异步上下文中，**不得持有或访问任何与 JavaScript 交互的对象**，包括 `JsValue`、`Applet *` 等任何 UI 线程专属对象。

客户端类应当是一个**纯 C++ 数据处理单元**，只持有执行任务所需的值类型数据（如 `String`、`int`、或自定义结构等），并在 `resolve()` 方法中完成全部工作。UI 线程与异步线程之间的所有交互由框架自动处理。
:::

### 基本用法

首先，定义一个客户端类，实现 `resolve()` 方法。该方法在异步上下文中被调用，返回 `async::Result<T>` 包装的结果：

```cpp
#include "gx_async.h"
#include "gx_file.h"

using namespace gx;

// 客户端类：纯 C++ 数据处理，不持有任何 JS 对象
class ReadTextClient {
public:
    void setPath(const String &path) { m_path = path; }

    // 在异步上下文中调用，返回操作结果
    async::Result<String> resolve() {
        File file(m_path);
        if (!file.open(File::ReadOnly | File::Text))
            return async::Status(300);  // IO 错误
        int size = int(file.size());
        String text(size);
        text.resize(file.read(text.data(), size));
        return text;  // 成功：返回文件内容
    }

    // 可选：自定义错误消息（当 Promise 被 reject 时使用）
    static const char *errorMessage(async::Status status) {
        switch (status.value()) {
        case 300: return "io error";
        default:  return "unknown error";
        }
    }

private:
    String m_path;  // 已经过安全校验的绝对路径
};
```

然后，在模块函数中创建会话并返回 `Promise`。注意：**必须**使用 `Applet::resolveUri()` 对 JavaScript 传入的路径进行安全校验，而不是直接信任应用提供的字符串：

```cpp
static JsValue readText(JsCtx ctx) {
    Applet *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1 || !ctx.arg(0).isObject())
        return {};

    // ✅ 安全：通过 resolveUri 校验并转换路径
    auto uri = applet->resolveUri(ctx.arg(0)["uri"].toString());
    if (uri.empty())
        return {};  // URI 校验失败，拒绝访问

    using Session = async::ResultSession<ReadTextClient>;
    auto *session = async::make<Session>(applet);
    session->client().setPath(uri);  // 传入校验后的安全路径

    // 提交异步任务，传入完整的 options 对象以兼容快应用回调接口
    session->request(ctx.arg(0));
    return session->promise();
}
```

::: tip 为什么传入 `ctx.arg(0)`？
`request()` 接收 JavaScript 侧传入的整个 `options` 对象，即 `ctx.arg(0)`，用于自动适配快应用异步接口的两种[调用风格](/api/README.md#快应用异步接口)：

- 若 `options` 中包含 `success`、`fail` 或 `complete` 任意属性，判定为**回调风格**，直接调用对应函数，`request()` 不返回有意义的值；
- 否则判定为 **Promise 风格**，将创建一个新的 `Promise`，`session->promise()` 返回该对象供调用方 `await`。

这使得同一个 C++ 实现无需任何额外代码，就能同时支持快应用标准的回调接口和现代 Promise/async-await 接口。如果确定只支持 Promise 风格，也可以传入空值 `{}`。
:::

::: danger 不要跳过 URI 校验
直接使用 JavaScript 传入的字符串作为文件路径是严重的安全漏洞：

```cpp
// ❌ 危险！绕过了沙箱的路径安全检查
session->client().setPath(ctx.arg(0)["uri"].toString());
```

恶意应用可以通过路径穿越（如 `../../etc/passwd`）访问沙箱外的文件系统。所有来自 JavaScript 的路径**必须**经过 `Applet::resolveUri()` 消毒，它会检测路径穿越攻击、跨应用越权访问和非法 URI 格式，校验失败时返回空字符串。
:::

JavaScript 侧的用法：

```javascript
import file from '@system.file'

async function loadConfig() {
    try {
        const text = await file.readText({
          uri: 'internal://files/config.json'
        })
        console.log('config:', text)
    } catch (err) {
        console.error('read failed:', err.message)
    }
}
```

### 错误与状态码

`async::Status` 封装了一个整数状态码，`0`（即 `async::OK`）表示成功，其他值为业务自定义错误码：

```cpp
// 成功：直接返回值，状态码自动为 OK
return async::Result<String>{std::move(content)};
// 失败：仅返回状态码，值部分被忽略
return async::Status(404);
// 同时携带部分结果和非 OK 状态（例如 HTTP 206 Partial Content）
return async::Result<ByteArray>{
  std::move(partialData),
  async::Status(206)
};
```

当 `resolve()` 返回错误状态时，`Promise` 会被 reject，JavaScript 的 `catch` 块会收到一个包含 `message` 和 `code` 字段的错误对象。`message` 来自客户端类的 `errorMessage()` 静态方法。

`errorMessage()` 支持多种签名，框架会自动识别：

```cpp
// 形式一：接收 Status（推荐，简洁）
static const char *errorMessage(async::Status status);

// 形式二：接收完整的 Result，可根据值和状态生成消息
static String errorMessage(const async::Result<MyType> &result);
```

若客户端类没有定义 `errorMessage()`，框架会使用默认的 `"unknown async error"`。

### 值类型与 JavaScript 转换

`resolve()` 返回的值不会原样传给 JavaScript，框架通过 `js_cast()` 函数将 C++ 类型自动转换为 `JsValue`，再驱动 `Promise` 的 resolve。这个过程在框架内部完成，看起来“透明”，但实际上依赖一套**隐式约定**：只有实现了 `js_cast()` 特化的类型才能正确转换，对于自定义的枚举、结构体等类型，需要显式建立转换关系，否则编译将会失败。

#### 内置支持的类型

下列类型可以直接作为 `Result<T>` 的类型参数，无需额外工作：

| C++ 类型 | 对应的 JavaScript 类型 | 备注 |
| --- | --- | --- |
| `int`、`double`、`float` | `number` | 数值直接映射 |
| `bool` | `boolean` | 布尔值直接映射 |
| `String`、`StringView`、`const char *` | `string` | 字符串直接映射 |
| `ByteArray` | `ArrayBuffer` | 二进制数据 |
| `JsonValue` | `object` / `array` | JSON 对象或数组 |
| [`std::vector<T>`](https://en.cppreference.com/w/cpp/container/vector) | `Array` | 数组，元素递归转换（`T` 本身也需可转换） |
| `JsValue` | 任意 | 直接传递，不做转换 |
| `void`（即 `Result<void>`） | `undefined` | 无返回值 |

这些类型均在 JsVM 框架中内置了 `js_cast<T>()` 特化，它们一部分是 `JsValue` 可直接构造的类型，一部分则通过特化实现了转换逻辑。

#### 为自定义类型添加转换支持

如果使用的类型不在上述列表中，编译器会报错提示无法构造 `JsValue`。有两种方式解决：

**方式一：定义 `operator JsValue()` 成员函数**

这适合可以修改定义的自定义结构体，好处是转换逻辑内置在类型定义中，紧密耦合：

```cpp
struct DeviceInfo {
    String model;
    int version;

    // 将结构体转换为 JavaScript 对象
    // 注意：转换在 UI 线程执行，此时有合法的 JsVM 上下文
    operator JsValue() const {
        JsVM &vm = JsVM::current();
        JsValue obj = vm.newObject();
        obj["model"] = JsValue(model);
        obj["version"] = JsValue(version);
        return obj;
    }
};
```

定义后，`Result<DeviceInfo>` 可以直接使用：

```cpp
async::Result<DeviceInfo> resolve() {
    return DeviceInfo{"ModelX", 3};  // 框架自动调用 operator JsValue()
}
```

`operator JsValue()` 内部使用的 `JsVM::current()`、`vm.newObject()` 等 API 属于 JsVM 桥接层，详见 [Native Module 开发文档](./native-module.md#创建与返回对象)。

**方式二：在 `gx` 命名空间中[特化](https://en.cppreference.com/w/cpp/language/template_specialization) `js_cast<T>`**

适合不能修改原始类型定义的情况（例如来自外部定义的类型或枚举）：

```cpp
// 必要时在使用前声明该特化
template<>
JsValue gx::js_cast<ConnectionState>(const ConnectionState &x);

// 在 gx 命名空间内特化
template<>
JsValue gx::js_cast<ConnectionState>(const ConnectionState &x) {
    switch (x) {
    case ConnectionState::Connected:    return "connected";
    case ConnectionState::Connecting:   return "connecting";
    case ConnectionState::Disconnected: return "disconnected";
    default:                            return "unknown";
    }
}
```

特化完成后，`Result<ConnectionState>` 和 `Signal<ConnectionState>` 均可正常工作。

::: tip 整数枚举的简便做法
如果枚举值直接对应整数，在 `resolve()` 中手动转换为 `int` 是最省力的方式，无需任何特化：

```cpp
async::Result<int> resolve() {
    return async::Result<int>{int(myEnum)};
}
```
:::

#### 运行时转换开销

`js_cast()` 在异步结果投递回 UI 线程**之后**才执行，不在异步线程中运行。转换的时间开销完全发生在 UI 线程，对于复杂结构需要确保足够快以避免卡帧。各类型的实际代价如下：

- **零开销类型**：`int`、`double`、`bool`、`String`、`const char *` 通过 `JsValue` 构造函数直接映射，无额外拷贝或堆分配。`operator JsValue()` 方式和 `js_cast<T>` 特化同样在编译期内联，没有虚调用或间接层。
- **线性开销类型**：`std::vector<T>` 需要逐元素调用 `setIndex()`，开销与元素数量成正比。如果返回结构是固定字段的对象，优先用 `operator JsValue()` 手动构造 JS 对象，比数组更高效也更易读。
- **树形遍历类型**：`JsonValue` 在转换时递归遍历整棵树，逐一构造 JavaScript 节点，是内置类型中开销最大的。如果数据结构在编译期已知，`operator JsValue()` 直接构造对象通常更快，且没有 `JsonValue` 本身的构建成本。
- **自定义结构体**：如果使用 `operator JsValue()` 或 `js_cast()` 特化，转换性能取决于各成员类型的转换开销，即构造对象的复杂度。

::: tip 简单判定标准
如果你的异步数据结构简单（数值、简单结构体对象，或小的 `JsonValue`），那么转换开销通常不会影响 UI 流畅性。
:::

#### 无序列化中间层

某些异步框架要求在 worker 线程和 UI 线程之间传递数据时，必须先将结果序列化为 JSON 或其他自描述格式，再在 UI 线程反序列化，这是为了实现线程间的“类型擦除”传递，但代价是每次调用都要承担字符串（或二进制数据流）的拼接、传输和解析开销。更糟的是可能构造多份数据副本（序列化的中间数据和原始数据等）。

async 框架**不依赖序列化中间层。** 结果通过 `async::Result<T>` 以 C++ 原生值的形式在线程间移动，完全绕过序列化过程：

```
worker thread                  UI thread
resolve(Result<MyType>{...}) → js_cast(result.value()) → JsValue (JavaScript)
                  ↑
             直接内存移动，无 JSON 字符串
```

`js_cast()` 仅在结果已经安全地回到 UI 线程之后才执行，它的职责是将 C++ 值映射为 JavaScript 引擎的内部表示，而不是充当线程间的通信协议。

如果你主动选择将 `JsonValue` 作为 `Result<T>` 的类型参数（用于缓解模板代码膨胀），那么你引入的是 `JsonValue` 的**构建和树遍历**开销，而不是字符串序列化，`JsonValue` 本身也是一种内存中的树形结构，不是文本格式。

#### 模板代码体积

`ResultSession<T>` 是模板类，编译器会为每个不同的客户端类型 `T` 生成一份独立的代码。不过框架已将绝大多数与 `T` 无关的逻辑（如 `Promise` 管理、事件投递、`Applet` 生命周期绑定）提取到非模板基类 `detail::ResultSession` 中，因此每个 `T` 实际额外增加的代码量主要集中在薄薄的 `Resolver` 适配层。

但如果项目中存在**大量仅使用一次的细粒度客户端类型**，累积的实例化数量仍会带来可观的代码量增长。

一种常见的压缩手段是以 `JsonValue` 作为类型擦除媒介，将多个零散的小函数合并到单一的客户端类型中：

```cpp
// 合并前：每个操作都是独立的客户端类 + 独立的模板实例化
struct GetVersionClient { ... };   // ResultSession<GetVersionClient>
struct GetModelClient   { ... };   // ResultSession<GetModelClient>
struct GetSerialClient  { ... };   // ResultSession<GetSerialClient>

// 合并后：共享同一个模板实例化，仅在运行时区分操作
struct DeviceQueryClient {
    enum Kind { Version, Model, Serial } kind;

    // 这里演示用 switch 分派，实际也可以用函数指针。但是不要用 BaseClient
    // 配合派生类重写 resolve() 来实现多态，会比函数指针方案多一些虚表膨胀。
    async::Result<JsonValue> resolve() {
        switch (kind) {
        case Kind::Version: return JsonValue{getVersion()};
        case Kind::Model:   return JsonValue{getModel()};
        case Kind::Serial:  return JsonValue{getSerial()};
        }
    }
};

// 三个模块函数共用 ResultSession<DeviceQueryClient> 这一个实例化
static JsValue getVersion(JsCtx ctx) {
    using Session = async::ResultSession<DeviceQueryClient>;
    auto *session = async::make<Session>(applet);
    session->client().kind = DeviceQueryClient::Version;
    return session->request(ctx.arg(0));
}
```

这种做法的代价是：返回类型退化为 `JsonValue`，需要承担额外的转换运行时开销（见上文）。因此它适合**数据量小、函数数量多**的场景，用少量运行时开销换取有意义的代码体积收益。对于数据量较大或性能敏感的操作，仍应保留独立的强类型客户端类。

### 自定义异步上下文

默认情况下，`session->request()` 将 `resolve()` 提交到框架的**异步执行器**——通常是一个后台线程池。但有些场景需要使用不同的异步上下文，例如自定义事件循环或 AIO 多路复用机制，它们均不希望占用额外的线程资源。

这时可以跳过 `request()`，直接手动控制异步执行流程，客户端类也不需要实现 `resolve()` 执行函数。关键是：**在异步上下文中完成工作后，调用 `session->resolve()` 将结果投递回 UI 线程**。

```cpp
// 客户端类：不需要实现 resolve()，因为不使用默认线程池
struct FirmwareCheckClient {
    // 仅定义 errorMessage() 用于错误描述
    static const char *errorMessage(async::Status status) {
        switch (status.value()) {
        case 1: return "firmware not found";
        case 2: return "check failed";
        default: return "unknown error";
        }
    }
};

static JsValue checkFirmwareUpdate(JsCtx ctx) {
    Applet *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1) return {};

    using Session = async::ResultSession<FirmwareCheckClient>;
    auto *session = async::make<Session>(applet);
    auto version = ctx.arg(0).asString();

    // 手动设置 resolver（不调用 request，不使用默认线程池）
    session->setResolver(ctx.arg(0));
    JsValue promise = session->promise();

    // 提交到自定义的硬件驱动线程
    HardwareDriver::checkUpdate(
        version,
        // 回调可能在任意线程——框架会自动调度回 UI 线程
        [session](bool available) {
            session->resolve<bool>(available);
        },
        [session](int errorCode) {
            session->resolve<bool>(async::Status(errorCode));
        }
    );

    return promise;
}
```

这里的核心区别：
- `request()` 同时完成“设置 resolver”和“提交到异步执行器”两个动作；
- 手动模式下，你需要自己调用 `setResolver()` 设置响应目标，然后在任意时机通过 `session->resolve()` 推送结果或者错误状态。

`resolve()` 是线程安全的，它将结果封装为事件投递回 UI 线程，再完成 `Promise` 的决议。

::: tip 何时使用自定义上下文
- 底层驱动已提供回调接口，你不想再创建额外的线程：直接在驱动回调中 `resolve`。
- 需要与现有的 AIO/epoll 事件循环集成：在事件完成回调中 `resolve`。
- 需要串行化执行（如操作必须按顺序）：用自己的任务队列调度，完成后 `resolve`。

只要保证最终调用一次 `session->resolve()` 即可，框架不关心结果是从哪个线程投递的。
:::

### 值类型语义

由于 `resolve()` 返回（或自定义异步上下文主动投递）的 `async::Result<T>` 值会被投递到 UI 线程再转换为 `JsValue`，因此数据类型 `T` 必须是可移动的。内置支持的类型均满足这一要求，对于自定义类型：
- 如果是一个仅包含内置支持类型成员的结构体，那么 C++ 标准保证它是可移动的。
- 如果使用了裸指针并自己控制其所有权，那么你需要正确实现[移动构造函数](https://en.cppreference.com/w/cpp/language/move_constructor)。
- [平凡类型](https://en.cppreference.com/w/cpp/named_req/TrivialType)（如纯 C 结构体、枚举等）默认满足值类型语义。

需要注意的是，非平凡类型通常包含堆上的资源，以下写法可能面临内存峰值问题：

```cpp
auto *session = getFetchLargeDataSession();
std::vector<uint32_t> data = fetchDataFromNetwork(url);
session->resolve<decltype(data)>(data);  // 会有一次 data 的完整复制
```
这是因为 `session->resolve()` 的参数是按值传递的，传入 `data` 时会调用[复制构造函数](https://en.cppreference.com/w/cpp/language/copy_constructor)，导致完整复制一份。如果 `data` 数据量很大，这会导致内存使用量翻倍。此时会出现这类编译警告：
```
'...' is deprecated:
avoid use copy semantics of Result<T> if T is not trivially copyable
```
正确的做法是使用 [`std::move()`](https://en.cppreference.com/w/cpp/utility/move) 显式启用移动语义：

```cpp
auto *session = getFetchLargeDataSession();
std::vector<uint32_t> data = fetchDataFromNetwork(url);
session->resolve<decltype(data)>(std::move(data));  // 使用移动语义
```

### 超时控制

对于可能长时间无响应的异步操作，使用 `async::make_timeout()` 为会话添加超时保护。超时后会自动 reject `Promise`，避免 JavaScript 侧永久挂起。

以下代码片段展示了一个基本示例，演示如何在网络请求中使用超时控制：

```cpp
static JsValue fetchData(JsCtx ctx) {
    Applet *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1) return {};

    String url = ctx.arg(0)["url"].asString();
    int timeoutMs = ctx.arg(0)["timeout"].asInt(5000);

    using Session = async::ResultSession<HttpClient>;
    auto *session = async::make<Session>(applet);
    session->client().setUrl(url);
    session->setResolver(ctx.arg(0));
    JsValue promise = session->promise();

    // 创建超时保护：超时后自动 reject Promise
    auto handle = async::make_timeout(session, timeoutMs,
        [](Session *s) {
            // 超时处理：应当在此取消正在进行的异步操作
            s->fulfill(async::Status(408));  // 408 Request Timeout
            
        });

    // 将 handle 移动到异步执行上下文
    NetworkDriver::fetch(url,
        [handle = std::move(handle)](auto &response) {
            // 若已超时，resolve 会被安全忽略
            handle->resolve<String>(std::move(response.body));
        });

    return promise;
}
```

#### 工作原理

`make_timeout()` 的关键工作流程：

1. 将 `session` 的客户端数据**移动**到一个内部类中，此后不得再访问 `session->client()`。
2. 启动一个单次定时器，返回 `SharedRef<SingleTimer>` 句柄。
3. **正常路径**：在超时前调用 `handle->resolve()`，内部原子地取走 session 所有权并投递结果事件，之后定时器触发时发现 session 已为空便不作处理。
4. **超时路径**：定时触发，**在 UI 线程**执行回调，开发者在回调中调用 `session->fulfill()` 投递错误状态；回调返回后，timer 负责 `delete session`。
5. **应用退出**：`Applet` 被销毁时，timer 自动解绑，session 被删除，回调不会被触发。

该机制特别适用于异步操作没有内置超时机制的场景，如某些网络请求的实现。众所周知，正确地实现超时保护有些棘手，你必须正确处理所有路径的竞争条件和生命周期安全问题。

`make_timeout()` 依赖这些前提来保证安全性：
- 客户端类型（也就是 `ResultSession<T>` 中的 `T`）必须是**可移动的**，这算是一个历史遗留限制。
- 异步操作必须支持在 UI 线程中安全地取消，这意味着删除任务监听器并释放对 `handle` 的引用。

#### 回调线程与 `fulfill()`

超时回调（`make_timeout()` 的第三个参数）**始终在 UI 线程执行**，因为它由定时器（`Timer`）触发，而定时器事件由主事件循环分发。

这一点决定了回调中**只能**使用 `session->fulfill()` 而不能使用 `session->resolve()`：

| 方法 | 可调用线程 | 对 session 的影响 |
| --- | --- | --- |
| `resolve(result)` | 任意线程 | 投递 Consume 事件，session 在 UI 线程处理后**被删除** |
| `fulfill(result)` | **仅限 UI 线程** | 直接分发结果，**不删除** session |

`make_timeout()` 的超时路径由 timer 自身负责在回调结束后 `delete session`。如果在回调中调用 `session->resolve()`，它会同样投递一个删除 session 的事件，与 timer 的 `delete` 形成**双重释放（double free）**，导致未定义行为。`fulfill()` 只投递结果、不触及 session 生命周期，因此是回调中唯一安全的选择。

`fulfill()` 接受 `async::Result<R>` 或直接接受 `async::Status`（无结果值时的简写）：

```cpp
auto handle = async::make_timeout(session, 5000, [](Session *s) {
    s->fulfill(async::Status(408)); // 仅填充错误状态
    // 或携带值和状态：
    s->fulfill(async::Result<String>{"partial", async::Status(206)});
    // ❌ 不要调用 s->resolve()，会与 timer 的 delete session 形成双重释放
});
```

::: tip
判断规则很简单：session 的所有权在哪里，由谁负责删除？
- **正常路径**：`handle->resolve()` 内部原子地接管 session 所有权，session 随 Consume 事件处理后删除。
- **超时回调**：timer 接管 session 所有权，回调结束后删除。因此回调中只能用 `fulfill()` 投递结果。
:::

#### 访问客户端数据

如果超时回调需要读取客户端数据来决定错误策略，使用扩展回调签名 `(Session *, const T &)`。**不要**在回调中调用 `session->client()`——客户端已被移动到 timer 中：

```cpp
auto handle = async::make_timeout(session, 3000,
    [](Session *s, const HttpClient &client) { // 也可用 auto &client
        // ✅ 通过第二个参数访问客户端数据
        LogWarn() << "request timeout: " << client.url();
        s->fulfill(async::Status(408));
    }
);
```

#### 资源生命周期管理

超时发生时，你需要在回调中取消正在进行的异步任务，以释放对 `handle` 的引用。`SingleTimer` 使用引用计数管理生命周期——如果异步操作持有 `handle` 的引用但永远不会完成，就会产生内存泄漏：

```cpp
auto task = AioTask::create();
auto handle = async::make_timeout(session, 5000,
    [task](auto *s) {
        task->cancel();     // 取消任务，释放对 handle 的引用
        s->fulfill(async::Status(408)); // reject Promise
    });

// 任务完成回调持有 handle 引用
task->start([handle = std::move(handle)](auto &result) {
    handle->resolve(result);
});
```

::: important
`make_timeout()` 返回的 `handle` 还**必须**被异步任务引用（上例中由 lambda 捕获），以确保在任务完成前定时器不会被销毁。否则会立即触发超时回调和 Promise reject，导致任务无法正常完成。
:::

这种内存泄漏由两种原因导致：
1. **async 框架泄漏**：`handle` 引用被遗忘，导致相关会话对象无法释放。
2. **底层任务泄漏**：异步任务本身阻塞在未完成的状态，相关资源也不会被清理。

### 应用退出时的自动清理

当 `Applet` 被销毁时（例如用户关闭应用、系统回收资源），所有绑定到该 `Applet` 的异步会话会被自动清理：

- 会话的 `unbind()` 方法被调用，它会关闭会话并释放 `Promise` 引用。
- 如果正在使用 `make_timeout`，timer 同样会被解绑，内部持有的 session 被删除。
- JavaScript 侧的 `Promise` 将永远不会被 resolve 或 reject——但此时 JavaScript 环境本身也在被销毁，所以这是安全的。

这意味着你**不需要**手动跟踪和取消异步任务——框架保证不会出现以下情况：
- 向已销毁的 `Applet` 投递结果导致访问悬空指针。
- 在已释放的 JavaScript 环境中执行回调。
- 异步会话在应用退出后泄漏。

具体来说，当后台线程调用 `resolve()` 投递结果到 UI 线程后，处理函数会检查 `applet()` 是否仍然有效。如果 `Applet` 已被销毁导致 `applet()` 返回 `nullptr`，框架会安全地丢弃结果，不执行任何 JavaScript 操作。

::: tip 异步上下文中的安全返回
由于 `resolve()` 是纯数据投递（通过事件队列），即使 `Applet` 已经销毁，在后台线程中调用 `resolve()` 也不会崩溃。后台线程不需要关心 `Applet` 的存活状态，这是框架的职责。
:::

唯一需要注意的是，如果你派生了 `ResultSession` 并引入了其他 `JsValue` 成员变量，则需要在 `unbind()` 中清理这些成员，以避免内存泄漏：

```cpp
class MySession : public async::ResultSession<MyClient> {
public:
    void unbind() override {
        m_callbacks = {}; // 清理任何持有的 JsValue，避免泄漏
        async::ResultSession::unbind(); // 调用基类清理
    }

private:
    JsValue m_callbacks; // 需要手动清理的成员
};
```

::: important `ResultSession` 的生命周期延长
如果应用退出时仍有未完成的异步会话，框架仅会清理与应用相关的资源（如 `Promise` 引用、绑定关系等），但**不会销毁会话对象本身**，这表现为 `ResultSession` 的生命周期被延长到异步操作完成为止。

这本身是为了保证内存安全，但会造成部分资源释放不及时。因此异步任务必须保证在有限的时间内完成，不能无限期地挂起。
:::

## 多次查询 ListenSession

该类 API 尚不稳定，暂不开放使用。

## 全局事件广播 async::Signal

如果一个 C++ 事件需要广播给**多个应用**（而不是针对某一个特定的调用方），使用 `async::Signal<T>`。它将底层的硬件或系统事件“多播”给所有订阅了它的 JavaScript 监听者。

`async::Signal<T>` 和 `ResultSession` 的定位不同：

| 特性 | ResultSession | Signal |
| --- | :---: | :---: |
| 通信方向 | 一对一（调用方 → 结果） | 一对多（事件源 → 所有订阅者） |
| 触发次数 | 单次 | 多次 |
| 绑定对象 | 单个 Applet | 跨 Applet |
| 适用场景 | 异步查询、请求 | 系统事件、状态变化 |

### 基本用法

假设有一个电池点亮变化的事件需要通知所有订阅者：

```cpp
// 定义一个全局信号，通常为对应服务的成员变量
async::Signal<int> batteryChanged;

// 当硬件事件发生时触发信号（可在任意线程调用）
void onBatteryLevelChanged(int newLevel) {
    batteryChanged(newLevel);  // 通知所有订阅者
}
```

#### 绑定 & 解绑

该模块函数允许 JavaScript 侧订阅该信号，它还返回一个绑定 ID 供 JavaScript 侧取消订阅：

```cpp
static JsValue subscribeBatteryChange(JsCtx ctx) {
    if (ctx.argc() < 1 || !ctx.arg(0).isFunction())
        return {};
    // 必须在有效的 applet 环境中才能订阅
    auto *applet = Applet::current(ctx.vm());
    if (applet == nullptr) return {};

    // 将 slot 绑定到应用，随应用退出而自动取消订阅
    auto *slot = batteryChanged.connect(ctx.arg(0));
    return applet->bindObject(slot); // 返回 slot ID 供 JavaScript 取消
}
```

还需要实现一个取消订阅的模块函数。无论何种 `async::Signal` 类型，解绑函数的实现都是非常固定的：

```cpp
static JsValue unsubscribeBatteryChange(JsCtx ctx) {
    auto *applet = Applet::current(ctx.vm());
    if (applet && ctx.argc()) {
        // slotId 默认为 0，可以被安全地忽略而不执行任何操作
        auto slotId = ctx.arg(0).toInt();
        // 将 slot 与 applet 解绑后还需要删除 slot 对象
        delete applet->unbindObject<async::Slot>(slotId);
    }
    return {};
}
```

#### JavaScript 导出

只需要定义一个 [Native Module](./native-module.md) 来导出这些函数即可：

```cpp
static JsModule *createBatteryModule(JsVM &vm) {
    auto mod = vm.newObject();
    // battery 模块通常还有 getLevel() 之类的函数，这里不展开
    mod["subscribe"] = subscribeBatteryChange;
    mod["unsubscribe"] = unsubscribeBatteryChange;
    return mod;
}
// 别忘了用 GX_JSVM_MODULE_IMPORT 导入模块
GX_JSVM_MODULE(vendor_battery, "vendor.battery", createBatteryModule)
```

::: tip 复用 `unsubscribe` 函数
由于解绑函数的实现非常通用，你可以定义一个通用的 `unsubscribe` 函数，然后多次导入到各个模块中使用。
:::

JavaScript 侧：

```js
import battery from '@vendor.battery'

const sid = battery.subscribe((level) => {
  console.log('battery level:', level)
})

// 需要取消订阅时调用
battery.unsubscribe(sid)
```

### 信号传递模式

`Signal` 支持两种传递模式，通过第二个参数控制：

```cpp
// 普通模式（默认）：通知所有订阅者
batteryChanged(newLevel, async::NormalSignal);

// 跳过不可见应用：仅通知前台可见的应用，减少不必要的消耗
batteryChanged(newLevel, async::SkipInvisible);
```

`SkipInvisible` 模式适用于仅在 UI 可见时才有意义的事件（如界面刷新通知）。对于需要后台感知的事件（如电池低电量警告），应使用默认的 `NormalSignal`。

### 信号值类型

`Signal<T>` 的类型参数 `T` 与 `ResultSession` 遵循完全相同的转换规则：触发信号时，框架通过相同的 `js_cast()` 机制将 C++ 值转换为 JavaScript 回调的参数。`int`、`bool`、`String`、`JsonValue` 等内置类型可以直接使用；如需传递自定义结构体或枚举，请参阅[值类型与 JavaScript 转换](#值类型与-javascript-转换) 一节中的方法。

## 线程安全说明

异步框架的线程安全模型遵循以下规则：

- **`resolve()` 是线程安全的**：`ResultSession::resolve()` 和 `SingleTimer::resolve()` 可以在任意线程调用。它们通过事件系统将结果投递到 UI 线程，不直接操作 JavaScript 对象。
- **`JsValue` 不是线程安全的**：`JsValue` 基于引用计数管理生命周期，其引用计数操作非原子性。不得在异步线程中创建、拷贝、销毁或访问 `JsValue`。这正是客户端类不得持有 `JsValue` 的原因。
- **`Promise` 决议在 UI 线程执行**：无论 `resolve()` 从哪个线程调用，最终的 JavaScript `Promise` 回调总是在 UI 线程执行，保证 UI 操作的安全性。
- **`async::Signal` 通知在 UI 线程分发**：`async::Signal::operator()` 虽然可以跨线程调用，但 JavaScript 回调始终在 UI 线程执行。

如果客户端类需要与 UI 线程共享状态（例如提供取消标志），使用 [`std::atomic`](https://en.cppreference.com/w/cpp/atomic/atomic) 等原子操作或互斥量保护共享数据：

```cpp
class CancellableClient {
public:
    void cancel() { m_cancelled.store(true); }

    async::Result<String> resolve() {
        for (int i = 0; i < 100 && !m_cancelled.load(); ++i) {
            // 执行分步任务，定期检查取消标志
            processChunk(i);
        }
        if (m_cancelled.load())
            return async::Status(499);  // 客户端取消
        return std::move(m_result);
    }

private:
    std::atomic_bool m_cancelled{false};
    String m_result;
};
```

特别的，Glyphix 框架的许多值类型在**本异步框架中**是可以安全地跨线程传递的，如：
- `String`：可以直接在多线程中赋值、访问，无需额外同步机制。
- `JsonValue`：该类也是值类型，并具有与 `String` 同等的线程安全特性。
- `ByteArray`：与 `String` 类似，支持跨线程使用。
- `SharedRef<T>`：引用计数智能指针本身可以跨线程传递，但托管对象 `T` 的线程安全性取决于其定义。
- `String::View` 等非拥有类型**不能**跨线程使用。

这也是前面所有示例中我们总是直接跨异步上下文捕获和传递 `String` 等类型，使用它们不需要特别处理。也不需要使用 mutex 等同步机制来保护。

::: important
上述类型的线程安全性实际上依赖于具体的异步框架内存模型，这意味着它们在所有场景中**并不是自动线程安全**的。本文档中的异步框架保证了这一点，但不能推广到任何情况。
:::


============================================================
FILE_PATH: src/transl/EN/cxxdev/cpp-guide.md

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


============================================================
FILE_PATH: src/transl/EN/cxxdev/global-assets-migrate.md

# 全局资源迁移指南

本文面向 Glyphix 下游集成项目，帮助你将历史项目中的全局资源加载方式升级到最新方案，获得易于管理、编辑的全局资源布局，不再依赖厂商的打包或转换工具支持。

早期 Glyphix 采用 `global.pkg` 二进制归档包管理全局资源（字体文件、字体映射表等），后来逐步演进为直接使用未打包资源文件，最终字体映射文件的格式也从二进制转为标准 JSON <version-badge since="0.9" /> 。如果你维护的入口代码仍沿用旧写法，可以按本文升级。

::: tip
使用旧模式存在维护麻烦、难以管理和编辑全局资源的问题，建议立即升级。
:::

## 去除 `global.pkg`

### 旧代码特征

如果你的入口代码中存在类似以下任一模式，说明你正在使用 `global.pkg`：

```cpp
EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
static String globalUri(const String &path) { return "pkg:///" + path; }
```

这两行的效果是：将所有 `pkg:///` 协议的资源请求路由到 `/global.pkg` 这个二进制归档包内部的文件。

为什么需要去除：
- 每次更换字体等资源，都必须重新运行打包工具生成 `.pkg` 文件
- 调试时无法直接查看或替换 `.pkg` 内部的单个文件，也难以核对内容
- 打包流程依赖专用工具，增加沟通和维护成本

### 迁移操作

**第一步：解出 `global.pkg` 中的资源。**

如果你已经没有 `.pkg` 源文件，可以从 `global.pkg` 中解出内容（使用 Glyphix 命令行工具或索取原始资源文件）。通常需要解出以下内容：

```
fonts/
    NotoSans-Regular.ttf
    NotoSansSC-Regular.ttf
    ...
    font-faces          ← 字体映射文件（后续会升级为 JSON）
```

将解出的目录放置到你的项目资源目录中，例如 `/fonts/`。

**第二步：移除 `global.pkg` 相关代码。**

1. 删除 `EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg")` 整行
2. 删除 `globalUri()` 这类包装函数
3. 将所有 `pkg:///xxx` 的资源引用改为直接文件路径，即 `/xxx`

**第三步：修改字体加载代码。**

假设你的初始化代码原本类似：

```cpp
static String globalUri(const String &path) { return "pkg:///" + path; }

static void setupFont(const String &fontMap) {
    String uri = globalUri(fontMap);
    FontFaceMap &map = App()->fontManager()->faces();
    if (!map.readFile(uri))
        LogError() << "Failed to load font face map: " << fontMap;
}

int main() {
    Application app;
    EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
    setupFont("font-faces");
    // ...
}
```

改为直接使用文件路径（没有 `globalUri()` 函数和 `GlobalPackage` 注册）：

```cpp
static void setupFont(const String &fontMap) {
    auto &map = App()->fontManager()->faces();
    if (!map.readFile(fontMap))
        LogError() << "Failed to load font face map: " << fontMap;
}

int main() {
    Application app;
    setupFont("/fonts/font-faces");
    // ...
}
```

此时资源布局变为：

```
/fonts/
    font-faces          ← 二进制格式
    NotoSans-Regular.ttf
    ...
```

这个阶段你仍然使用二进制的 `font-faces` 文件，下一节将其升级为 JSON。

## 改用 JSON 字体映射文件

### 旧代码特征

```cpp
FontFaceMap &map = App()->fontManager()->faces();
map.readFile("/fonts/font-faces");
```

`readFile` 读取的是自定义二进制格式文件，这个二进制文件不能手工编辑，必须从 CSS 文件用打包工具转换生成。

### JSON 格式说明

现在我们直接用 JSON 文件描述字体映射关系。你只需要创建一个 `font-faces.json` 文件，格式如下：

```json
{
  "font-faces": [
    {
      "family": "sans-serif",
      "weight": 400,
      "style": "normal",
      "urls": [
        "NotoSans-Regular.ttf",
        "NotoSansSC-Regular.ttf",
        "NotoSansJP-Regular.ttf"
      ]
    },
    {
      "family": "sans-serif",
      "weight": 700,
      "style": "normal",
      "urls": [
        "NotoSans-Bold.ttf"
      ]
    },
    {
      "family": "serif",
      "weight": 400,
      "style": "normal",
      "urls": [
        "NotoSerif-Regular.ttf"
      ]
    }
  ]
}
```

字段说明：

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `family` | 字符串 | 是 | - | 字体族名，如 `sans-serif`、`serif` |
| `weight` | 整数 | 否 | 400 | CSS 字重值（100-900），400 为常规，700 为加粗 |
| `style` | 字符串 | 否 | normal | 字体样式，可选 `italic` 或 `oblique` |
| `urls` | 字符串数组 | 是 | - | 字体文件路径，相对于 JSON 文件所在目录 |

下面对关键字段做进一步说明。

**weight 字段**

weight 直接填 CSS 字重数值，会舍入到最近的标准值：

- `100` Thin
- `400` Regular（默认值，不填即可）
- `700` Bold
- `900` Black

**urls 路径解析**

`urls` 中的路径相对于 JSON 文件所在的目录解析。例如 JSON 文件位于 `/fonts/font-faces.json`，则 `urls` 中写 `"fonts/NotoSans-Regular.ttf"` 最终解析为 `/fonts/fonts/NotoSans-Regular.ttf`。

因此建议 JSON 文件直接放置在字体文件同级目录，这样 URL 可以直接写文件名。例如目录布局为：

```
/fonts/
    font-faces.json
    NotoSans-Regular.ttf
    NotoSansSC-Regular.ttf
    NotoSans-Bold.ttf
```

此时 JSON 内容如上述代码所示。

### 代码修改

将初始化代码中的 `readFile` 替换为 `readJSON`：

```cpp
#include "gx_fontmanager.h"

static void setupFont() {
    auto &map = App()->fontManager()->faces();
    if (!map.readJSON("/fonts/font-faces.json"))
        LogError() << "Failed to load font-faces.json";
    App()->setFont(Font("sans-serif", 24));
}

int main() {
    Application app;
    setupFont();
    // ...
}
```

就这一处 API 调用变更，其余代码无需修改。之后你可以直接编辑 `font-faces.json` 来增删字体或调整映射关系，不再需要任何转换工具。

## FAQ

**如何处理同一个 family 有 Regular、Bold、Italic 等多个变体？**

在 `font-faces` 数组中为每个变体添加独立条目，用 `weight` 和 `style` 区分：

```json
{
  "font-faces": [
    {
      "family": "sans-serif",
      "weight": 400,
      "style": "normal",
      "urls": ["NotoSans-Regular.ttf"]
    },
    {
      "family": "sans-serif",
      "weight": 700,
      "style": "normal",
      "urls": ["NotoSans-Bold.ttf"]
    },
    {
      "family": "sans-serif",
      "weight": 400,
      "style": "italic",
      "urls": ["NotoSans-Italic.ttf"]
    }
  ]
}
```

MCU 项目通常只使用 `normal` 字重的 Regular `sans-serif` 字体，系统会自动回退。

**`urls` 数组里可以放多个文件吗？什么时候需要？**

可以。当一个字体族需要覆盖多语种字符时，将多个字体文件放入同一个 `urls` 数组。例如 `sans-serif` 需要同时支持拉丁字母、中日韩文字、阿拉伯文：

```json
{
  "family": "sans-serif",
  "weight": 400,
  "style": "normal",
  "urls": [
    "NotoSans-Regular.ttf",
    "NotoSansSC-Regular.ttf",
    "NotoSansJP-Regular.ttf",
    "NotoSansArabic.ttf"
  ]
}
```

引擎渲染文本时会按顺序在这些文件中查找字符字形，第一个匹配到的字形将被使用。

**字体文件必须和 JSON 放在同一目录吗？**

不是。`urls` 中的路径相对于 JSON 文件所在目录解析，你可以使用相对路径将字体放在子目录中。也可以使用绝对路径，此时不受 JSON 目录影响。

**可以直接在代码中传入 JSON 字符串吗？**

可以。使用两参数重载版本：

```cpp
map.readJSON("/fonts/", R"({
  "font-faces": [
    {"family": "sans-serif", "urls": ["NotoSans-Regular.ttf"]}
  ]
})");
```

第一个参数是 baseUri，用于解析 `urls` 中的相对路径。


============================================================
FILE_PATH: src/transl/EN/cxxdev/native-module.md

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


============================================================
FILE_PATH: src/transl/EN/cxxdev/object-system.md

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


============================================================
FILE_PATH: src/transl/EN/cxxdev/platform-font-fallback.md

# 平台字体回退

Glyphix 框架内置了一套基于 font-face / font-family 的字体加载与回退机制。但目标平台通常自带完善的字体管线（如 Windows DirectWrite、macOS CoreText），它们已实现系统字体回退与相关优化。

为充分利用平台字体管线，Glyphix 允许你接管字体回退：当框架内字体无法覆盖某个字符时，转交平台去查找并渲染合适的系统字体。本文面向 Glyphix 的系统开发者，带你一步步完成对接。

涉及的公共头文件：
- `gx_unite.h`：含 UniTE 公共接口，以及引擎安装函数 `installEngine()`；
- `gx_shapingadapter.h`：此为主要接口；
- `gx_fontdriver.h`：提供 `FontDriver` 封装机制；
- `gx_fontloader.h`：提供字体加载器接口。

## 整体思路

一段文本要在屏幕上显示，会经过下面这条管线：应用文本交由**段落布局引擎**分行、定位；每段同脚本、同方向的文本被**塑形**成字形；缺字时由**字体回退**补齐；字形再交**字体驱动**渲染成位图；而所有字体都来自**字体管理**层的注册、加载与复用。

<ArchDiagram max-width="560px">
  <div>应用文本<div class="remark">段落 · 字符串 · 样式</div></div>
  <div>
    段落布局引擎
    <div class="group row">
      <div>轻量引擎 LiTE<div class="remark">简单排版（默认引擎）</div></div>
      <div>UniTE 引擎<div class="remark">BiDi · Shape · 复杂脚本</div></div>
    </div>
  </div>
  <div>
    塑形 · 字体回退
    <div class="group row">
      <div>HarfBuzz<div class="remark">GSUB / GPOS</div></div>
      <div>Simple Shape<div class="remark">字符 → 字形</div></div>
      <div class="subject">FontFallbackShaper<div class="remark">family 回退 · 平台系统字体</div></div>
    </div>
  </div>
  <div>
    字体渲染
    <div class="group row">
      <div>FontDriver<div class="remark">TTF / FreeType</div></div>
      <div>FontDriverFamily<div class="remark">多 face 级联</div></div>
      <div class="subject">PlatformFont 包装器<div class="remark">绘制平台回退字形</div></div>
    </div>
    <div>GlyphCache - 字形位图缓存</div>
  </div>
  <div>
    字体管理 FontManager
    <div class="group row">
      <div>注册 / 查找<div class="remark">face · family · 属性</div></div>
      <div class="subject">FontLoader<div class="remark">加载 face，注入包装器</div></div>
    </div>
  </div>
</ArchDiagram>

图中高亮的三部分即本文涉及内容：
1. 回退策略 `FontFallbackShaper`，用于找出缺字并回退塑形；
2. 负责绘制平台回退字体的 `PlatformFont` 包装器，与 `FontFallbackShaper` 配套使用；
3. 用于加载平台回退字体包装器的 `FontLoader`，将注册到 `FontManager` 中。

其余各层框架已实现，文本塑形（`ShapingAdapter`）通常无需重头实现，直接复用参考实现即可。

### 前置条件

按本文档实现平台字体回退功能前，需要：

- 启用 UniTE 文本引擎（相比默认轻量引擎，它支持复杂脚本塑形与多级回退）。
- 目标平台支持完整的字体管线，能提供系统字体的塑形、脚本映射等高级功能。这通常是一个复杂的子系统，大部分 MCU RTOS 平台不具备。

::: important
相比于默认的 LiTE 引擎，启用 UniTE 以及完整的字体管线需要更多的内存和固件空间。且该引擎的性能较轻量的 LiTE 要差，需要评估是否需要为了完整的 Unicode 支持和国际化需求而启用它。
:::

## 复用塑形后端

`ShapingAdapter` 负责把字符塑形成字形。自带的 `HarfBuzzShaper`（`gx_harfbuzz_shaper.cpp`）已实现完整的 OpenType 塑形，它调用 HarfBuzz 塑形，再把字形索引、advance、偏移按目标像素尺寸写入输出。

`HarfBuzzShaper` 依赖 Freetype 读取字体文件，因此需要同时引入 HarfBuzz 和 Freetype 库。若目标平台已经存在这些库，请保证版本一致，否则可能出现链接或运行时错误。

::: tip
和 HarfBuzz 的[职责](https://harfbuzz.github.io/what-harfbuzz-doesnt-do.html)类似，`ShapingAdapter` 也不处理包含不同字体的文本 run，这也包括下文介绍的“字体回退”机制情况。因此，只要 shaping 中使用的字体缺字，`ShapingAdapter` 实现就会返回 `.notdef` 字形（索引 `0`），并由回退策略去处理。
:::

## 实现回退策略

`FontFallbackShaper` 是回退的核心。引擎每塑形一截文本就调用它一次，要求交回一份**不含缺字**的字形序列作为塑形结果。与 `ShapingAdapter` 不同，它不只是针对单一 font-face 的塑形，而是设计用于两级回退。

### 两级回退级联

`FontFallbackShaper::shape()` 回退按“由近及远”分两级：

- **第一级**：在当前 family 内部用其它字体互相补字。框架已实现，你只需调用 `builtinShape()`。
- **第二级**：第一级仍补不上的缺字，交给平台系统字体。这一级由你实现。

缺字在数据里表现为字形索引为 `0`，即 `.notdef`。`shape()` 的返回值 `FallbackResult` 用位标志表达结果：`result & NotNeeded` 为真表示已无缺字、可直接结束；否则常见返回 `FullyResolved`（全部处理完）或 `PartiallyResolved`（仍有残留 `.notdef`）。

### `shape()` 函数骨架

先调用第一级；若已无缺字就返回，否则进入第二级的平台字体回退。`m_shaper` 是这个回退器持有的 `ShapingAdapter`（通常就是 `HarfBuzzShaper`）。

```cpp
FallbackResult shape(GlyphRunBundle &storage,
                     TextSpan text,
                     FontDriver *font) override {
    // 第一级：使用 builtin API 处理 family 内的回退
    auto r = builtinShape(storage, text, font, &m_shaper);
    if (r & NotNeeded)
        return r;                                  // 已无缺字，结束
    return resolveByPlatform(storage, text, font); // 第二级，见下
}
```

`builtinShape()` 是唯一依赖 `ShapingAdapter` 的地方，这种情况下你通常需要将 `PlatformFallbackShaper` 实现如下：
```cpp
class PlatformFallbackShaper : public FontFallbackShaper {
    HarfBuzzShaper m_shaper; // 直接定义成员变量，不需要指针引用

public:
    PlatformFallbackShaper() = default;
    FallbackResult shape(GlyphRunBundle &storage,
                         TextSpan text, FontDriver *font) override;
};
```
请注意，`m_shaper` 仅仅是你的平台回退策略的私有成员变量，完全不需要暴露给外部使用。`shape()` 内部调用 `builtinShape()` 时传入 `&m_shaper` 即可。

::: tip
极端情况下（如初步适配阶段）可以不管 family 内的回退，直接跳过 `builtinShape()`，只处理第二级平台回退。此时可以省去 `m_shaper` 成员变量。

无论如何，`ShaperAdapter` 具体类通常不能定义为局部变量，因为它可能持有 HarfBuzz 的缓存状态，若每次塑形都重新创建会导致严重的性能下降。
:::

### 取得平台字体

第二级要把缺字交给平台，并最终让包装器去渲染。`fallbackFont(font)` 返回注册在 family 末项的那个包装器（见后文）。它的静态类型是 `FontDriver *`，你需要转回自己的包装器类型，才能调用你自定义的登记、查询接口。

```cpp
// 转型也可用 dyn_cast，但如果只有一个包装器类型，static_cast 也安全
auto *wrapper = static_cast<PlatformFont *>(fallbackFont(font));
if (wrapper == nullptr)
    return PartiallyResolved; // family 末项没有包装器，无法继续
```

::: warning 必须成对实现
回退策略与包装器是配套的一对：上面的 `static_cast` 要求 `fallbackFont()` 返回的正是你自己的包装器类型。务必保证安装的回退器与注册的包装器相互匹配。
:::

### 简单回退塑形

最常见且适合起步的情形是：整段 run 都可用同一平台字体塑形（即某一系统字体文件完全覆盖该脚本）。此时按 `storage.run().spec.script` 选定平台字体，对整 run 重塑一次，整段写入同一个 `faceId`，**直接覆盖第一级结果**，无需与已解析字形做合并。

UniTE 按 script 切分 run，同一段文本里的拉丁与 CJK 本就是不同 run。当主字体主打拉丁、遇到 CJK, Arabic, Devanagari 等 script 时，该 run 经 `builtinShape()` 后往往整段都是 `.notdef`，整段重塑并覆盖不会丢失任何已解析字形。所以多语言排版绝大多数走这条路径，并非退化特例。

```cpp
// 按脚本选定平台字体（平台字体句柄，非 FontDriver），登记得 faceId
auto sysFont = platformFontForScript(storage.run().spec.script);
uint32_t faceId = wrapper->registerFont(sysFont);
// 你的塑形步骤产出 glyphCount 个字形（此处以 HarfBuzz 产物演示）
auto &run = storage.resize(glyphCount);
for (int i = 0; i < glyphCount; ++i) {
    run.data.glyphIds[i]   = GlyphIds::encodeFallback(gid[i], faceId);
    run.data.xAdvances[i]  = uint16_t(scale(pos[i].x_advance));
    run.data.xOffsets[i]   = int16_t(scale(pos[i].x_offset));
    run.data.yOffsets[i]   = int16_t(scale(pos[i].y_offset));
    run.data.clusterMap[i] = static_cast<int>(info[i].cluster);
}
```

`pos`, `info`, `gid` 和 `scale` 字段来自你的塑形步骤，上面用 HarfBuzz 的输出作演示。

::: tip 平台塑形能力
平台通常自带塑形能力（如 DirectWrite、CoreText），是否复用 HarfBuzz 按具体平台决定；演示中的 HarfBuzz 产物替换为平台塑形输出即可。RTL run（`spec.bidiLevel & 1`）需把方向传给塑形器。
:::

此方法的前提是整段 run 映射到单一平台字体。它**不适用 Common script**（Emoji、符号等）：同一 run 内不同字符可能分属多种平台字体，需要下文的复杂回退。

### 复杂回退塑形

当一个 run 内需要多种平台字体、或仅部分簇需要回退时，简单方案不再适用。考虑到具体的回退和合并算法取决于平台 API，本文档只约束合并后 `GlyphRun` 必须满足的语义，实现需自行处理：

- 第一级已解析的字形**原样保留**，第二级只替换仍为 `.notdef` 的簇。
- 每个字形槽填齐 `glyphIds`, `xAdvances`, `xOffsets`, `yOffsets`, `clusterMap`；回退字形用 `encodeFallback(gid, faceId)` 标记。
- `clusterMap[i]` 为该字形对应源码点相对**本 run** 的偏移（与 `spec.text` 一致，范围 `[0, text.length())`），供绘制回映与按行裁剪。
- 字形数量可变：用 `storage.resize()/reset()` 调整存储，然后逐槽写入。`GlyphRunBundle` 内部会自动更新 `run().glyphCount`。
- 同一源簇映射到多个字形时，顺序与 advance 之和须正确；GSUB 合簇吞并的码点应产出零 advance 字形，避免空隙或错位。
- `faceId` 须为包装器登记过、全生命周期稳定的 ID；RTL run 的字形顺序与塑形方向须一致。
- 返回值：全部补齐返回 `FullyResolved`，仍有残留返回 `PartiallyResolved`。

只要输出满足上述约束，框架即可正确渲染，具体是分段查询平台 API、还是复用 HarfBuzz 逐字体塑形，可按平台选择。

### 行高与缓存

行高取决于每个字形**实际由哪个字体绘制**。`builtinLineMetrics()` 负责 family 内字形的部分；带回退标记（`isFallback()`）的字形则向包装器查询其系统字体的升降部并入。回退字形在 `GlyphIds` 里由 `encodeFallback` 编码，其 `fontIndex()` 即写入的 `faceId`，据此向包装器取回对应平台字体。

```cpp
VerticalMetrics resolveLineMetrics(const GlyphIds *gids, int count,
                                   FontDriver *font) const override {
    // 处理 family 内的字形
    VerticalMetrics m = builtinLineMetrics(gids, count, font);
    // 处理平台回退字形
    auto *wrapper = static_cast<PlatformFont *>(fallbackFont(font));
    if (wrapper == nullptr)
        return m;
    // 对 gids[i].isFallback() 的字形，向包装器查 asc/descent 并入 m
    for (auto gid : utils::span<const GlyphIds>(gids, count)) {
        if (!gid.isFallback())
            continue; // 只处理回退字形
        uint32_t faceId = gid.fontIndex(); // 回退字形的 fontIndex() 即 faceId
        auto face = wrapper->fontForFaceId(faceId); // 平台字体句柄（非 FontDriver）
        if (face == nullptr)
            continue;
        m.ascent = max(face->ascender(), m.ascent);
        m.descent = min(face->descender(), m.descent);
    }
    return m;
}
```

也可以汇总整行的回退字体并一次性查询它们的 asc/descent，避免循环中逐字形查询。

`flush()` 用来释放包装器缓存的系统字体：

```cpp
void flush(FontDriver *font) override {
    if (auto *w = static_cast<PlatformFont *>(fallbackFont(font)))
        w->releaseFonts();
}
```

::: tip
`flush()` 在段落销毁或内存紧张时由框架调用，请在其中清理包装器持有的平台资源。
:::

## 回退字体 `FontDriver` 包装器

包装器负责把上一步塑形的字形渲染成位图。它继承 `FontDriver`，构造时带上 `PlatformFallback` 标记，这样框架就知道它是回退字体。

```cpp
class PlatformFont : public FontDriver {
public:
    PlatformFont(const String &family, const FontAttribute &attr)
        : FontDriver(family, attr, Vector | PlatformFallback) {}
    // ... bitmapOf / metricsOf ...
protected:
    void requestHandler(int) override {}
};
```

该字体包装器并不用于加载某种字体文件（如 `FontDriverTTF` 那样）。它的作用是把回退字形交给平台字体管线去处理，而内部实现对 Glyphix 是不透明的。

### 双模式查询

包装器收到的 `code` 有两种含义，用 `CodeAsGlyphId` 位区分：

- **带标记**：按字形索引查询，高位携带 `faceId`，低位为字形索引。解出后路由到对应平台字体，再以 `glyphId` 查询对应的 `GlyphBitmap`。
- **不带标记**：Unicode 字符查询，按 codepoint 在已登记平台字体里兜底查找，内部自己转换为字形索引再查询。

常见的 `bitmapOf()` 实现如下：

```cpp
bool bitmapOf(uint32_t code, GlyphBitmap *bitmap) override {
    if (code & CodeAsGlyphId) { // 按字形索引
        uint32_t faceId  = (code >> 16) & 0x3ff;
        uint32_t glyphId =  code & 0xffff;
        auto face = fontForFaceId(faceId); // 平台字体句柄（非 FontDriver）
        return face && face->bitmapOf(glyphId, bitmap);
    }
    // Unicode 字符查找，这里遍历已注册字体，也可以用更高效的映射表
    for (auto *face : registeredFonts()) {
        uint32_t glyphId = face->glyphIndexOf(code);
        if (face->bitmapOf(glyphId, bitmap))
            return true;
    }
    return false;
}
```

::: tip
`fontForFaceId()` 返回的是平台字体句柄，**并非 `FontDriver`**；上述 `face->bitmapOf(...)`、`face->glyphIndexOf(...)` 是对该句柄操作的伪代码，分别表示“按 `glyphId` 取 `GlyphBitmap`”，“按码点取 `glyphId`”。
:::

`metricsOf()` 用同样的双模式逻辑；`advancesOf()`、`baseline()` 等也从平台字体计算。`duplicate()` 复制一份映射表即可。

### `faceId` 映射

包装器维护一张 `faceId` → 平台字体的映射，供回退策略登记、渲染时查回。

`faceId` 是 $10$ 位整数（$[0, 1023]$），含义完全由实现定义，唯一要求是**全生命周期稳定**。有两种常见做法：

- **按脚本固定**：直接用 `Script` 枚举值作 `faceId`，包装器按脚本持有对应平台字体，登记时即按脚本写入，无需运行时分配。
- **按需分配**：每遇到一个新平台字体就分配下一个索引，维护一张增长表。

按脚本固定的例子（`faceId` 即脚本值）：
```cpp
PlatformFontHandle fontForScript(Script script) {
    switch (script) {
    case Script::Han:    return sysHanFont;
    case Script::Arabic: return sysArabicFont;
    case Script::Latin:  return sysLatinFont;
    // ...
    }
    return sysDefaultFont;
}
```
你需要自行处理脚本→字体映射、`faceId` 分配与平台字体对象缓存。

::: tip
`faceId` 是回退策略与包装器之间的契约：`PlatformFallbackShaper` 用它编码字形，`PlatformFont` 用它解码回系统字体。两端对 `faceId` 的解释必须一致，并且要保证可以由 $10\rm bit$ 整数表示。
:::

## 注册包装器

最后让框架把包装器纳入 family 加载。实现 `FontLoader::load()`，对某个通用 family 名返回包装器，再装进 `FontManager`：

```cpp
struct PlatformFontLoader : public FontLoader {
    FontDriver *load(const String &face, const FontAttribute &attr) override {
        if (face == "sans-serif")
            return new PlatformFont(face, attr);
        return nullptr;
    }
};

CoreApp()->fontManager()->install(new PlatformFontLoader);
```

应用以 `"<primary-face>,sans-serif"` 形式请求字体时，框架按逗号顺序把各部分合并进同一个 family，包装器作为最后一项成为兜底 face，`fallbackFont()` 便能取到它。

`PlatformFont` 和 `PlatformFontLoader` 通常只注册为 `sans-serif` 这类通用 family 名的字体，而不是某个具体的系统字体名。这样应用就可以在不同平台上使用同一 family 名，而不需要知道平台的具体字体。

::: warning 功能限制
包装器总在 family 末项目前依赖应用按上述顺序书写 family 名。自动保证该顺序的机制尚在完善中。
:::

## 安装并装配

`gx_unite.h` 的 `installEngine()` 把你的回退策略接入引擎：

```cpp
unite::installEngine(*CoreApp()->typesetCore(),
                     std::make_unique<PlatformFallbackShaper>());
```

完整装配顺序：

1. `fontManager()->install(new PlatformFontLoader)`：注册包装器加载器。
2. `installEngine(...)`：安装持有塑形后端的回退策略。
3. 以 `"<primary-face>,sans-serif"` 形式请求字体，照常布局、绘制。

## 注意事项

- advance / 偏移一律为 Q26.6 定点（值 = 像素 × 64）。
- 仍未补齐的 `.notdef`（字形索引为 $0$）在渲染时被跳过，对应位置会显示空白或豆腐块。
- `faceId` 仅 $10$ 位，单个 family 同时活跃的系统字体上限为 $1024$ 个。
- 回退策略与包装器必须成对实现并保持类型一致（依赖 `static_cast`）。
- 在 `flush()` 中务必释放包装器持有的平台字体缓存。


============================================================
FILE_PATH: src/transl/EN/cxxdev/README.md

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


============================================================
FILE_PATH: src/transl/EN/cxxdev/sdk-setup.md

# SDK 项目配置

Glyphix 以预编译库的形式分发给设备厂商，本文介绍如何在 SDK 项目中配置构建环境，以便在其基础上开发 Native Module、Native Widget 或平台适配代码。

### 前置条件

开始之前请确保已安装：
- CMake 3.14 或更高版本
- 支持 C++14 的 C++ 编译器（GCC、Clang 或 MSVC）
- Glyphix 元对象编译器 `meta`（与 SDK 匹配，获取方式详见下文）
- 交叉编译工具链（如需构建嵌入式目标）

::: tip 系统要求
- MSVC 工具链需要安装 Visual Studio 2022 或更高版本。
- Linux 建议使用带桌面环境的发行版，如 Ubuntu 22.04 或更高版本。
- 不建议使用 Ubuntu 20.04，因为它的包版本通常过旧，经常要手动安装新版软件。
- 使用 WSL、Docker 等不带图形界面的环境将无法运行模拟器和 GUI 示例。
- 目前宿主环境仅提供 Linux 预编译库，目前尚未准备好 Windows 和 macOS 的预编译库。
:::

## SDK 包结构

解压后的 SDK 包含以下目录：

```
glyphix-sdk/
├── libs/
│   └── <target-triple>/       # 按目标三元组区分的预编译库
│       ├── include/           # Glyphix 头文件（gx_*.h）
│       └── lib/               # 静态库（libglyphix-core.a 等）
├── cmake/
│   ├── GlyphixSDK.cmake       # SDK 主配置脚本
│   ├── meta.cmake             # 元对象编译器集成（glyphix_add_meta_objects）
│   ├── cross-compile.cmake    # 交叉编译工具链加载
│   ├── arch/                  # 各架构的编译参数（mips-linux-gnu、cortex-m33 等）
│   └── toolchain/             # 各工具链的 CMake 工具链文件
├── wrapper/                   # 平台适配层（网络、文件系统等宿主机实现）
├── app/                       # 示例应用入口（emulator、async 等）
└── vendor/                    # 第三方依赖库
```

### `libs/<target-triple>/`

SDK 的预编译库以**目标三元组**（target triple）为目录名区分平台，例如：

- `x86_64-linux-gnu/`： 64 位 Linux 宿主机开发/模拟
- `mips-linux-gnu/`：MIPS Linux 嵌入式目标
- `cortex_m55-none-gnu/`：Cortex-M55 裸机目标

`include/` 目录下包含所有 Glyphix 公共头文件，均以 `gx_` 为前缀。`lib/` 目录下为静态库，核心库包括：

| 库文件 | 说明 |
|:---|:---|
| `libglyphix-core.a` | 核心框架（对象系统、控件树、事件等） |
| `libglyphix-widgets.a` | 内置控件库 |
| `libglyphix-reactive.a` | 响应式框架（JavaScript 桥接层） |
| `libglyphix-platform.a` | 平台抽象层接口 |
| `libglyphix-service.a` | 系统服务层 |

::: tip 预编译 vendor 库
SDK 分发包中还包含一些预编译的第三方库，例如 `libfreetype.a` 等。方便起见，我们没有直接分发这些库的源代码，但你可以不使用预编译库，而是直接使用源码构建。
:::

## 准备工作

### 配置元对象编译器

`meta` 元对象编译器与 SDK 分开分发，以独立压缩包的形式提供。解压后会得到 `bin/` 和 `lib/` 两个目录，**两者都必须保留在同一目录下**，`meta` 可执行文件依赖 `lib/` 中的运行时库。

在 Linux 和 macOS 中，推荐解压到 `/usr/local`，这样 `meta` 会自动位于 `PATH` 中：

::: code-tabs#bash

@tab Linux

```bash
sudo tar -xJf glyphix-meta-vX.X-linux-x86_64.tar.xz -C /usr/local
```

@tab macOS

```bash
sudo tar -xJf glyphix-meta-vX.X-darwin-arm64.tar.xz -C /usr/local
```

:::

也可以解压到任意目录，然后将其中的 `bin/` 目录加入 `PATH`。完成后通过以下命令确认是否可用：

```bash
meta --version
```

如果不希望修改 `PATH`，可以在 CMake 配置时通过 `-DGX_META=/path/to/bin/meta` 显式指定可执行文件的完整路径。

## 配置 CMakeLists.txt

### 最小配置

::: tip
本节介绍的 CMake 配置类似 Glyphix SDK 项目的标准示例模板，你可以直接参考 SDK 的源文件。
:::

以下是一个最小可运行的 `CMakeLists.txt`，展示了项目的标准配置骨架：

```cmake
cmake_minimum_required(VERSION 3.14)

# 必须在 project() 之前加载，以便在 project() 探测编译器时工具链已就位
include(cmake/cross-compile.cmake)

project(my_glyphix_app)
set(CMAKE_CXX_STANDARD 14)

# 加载 Glyphix SDK（设置头文件路径、链接目录、glyphix::sdk 目标）
include(cmake/GlyphixSDK.cmake)

add_subdirectory(vendor)  # 第三方依赖（如有）
add_subdirectory(src)     # 你的源代码
```

在 `src/CMakeLists.txt` 中创建目标并链接 SDK：

```cmake
add_executable(my_app
  main.cpp
  my_module.cpp
  my_widget.cpp
)

# 链接 Glyphix SDK
target_link_libraries(my_app PRIVATE glyphix::sdk)

# 为含有 GX_OBJECT 的头文件生成元数据
glyphix_add_meta_objects(my_app
  my_module.h
  my_widget.h
)
```

### 注册元对象（`glyphix_add_meta_objects`）

[对象系统](./object-system)文档中提到，任何声明了 `GX_OBJECT` 的类都必须注册到构建系统，由元对象编译器为其生成 `*_meta.cpp` 文件。`glyphix_add_meta_objects()` 是完成这一步骤的 CMake 函数：

```cmake
glyphix_add_meta_objects(<target> [header1.h header2.h ...])
```

它接受目标名称和一组**头文件**路径作为参数。对每个头文件，`meta` 工具会在构建目录下的 `meta/` 子目录中生成对应的 `*_meta.cpp`，并自动加入目标的源文件列表参与编译。

**示例：** 假设项目有如下结构：

```
src/
├── CMakeLists.txt
├── main.cpp
├── sensors/
│   ├── step_counter.h       # 包含 GX_OBJECT
│   └── step_counter.cpp
└── widgets/
    ├── activity_ring.h      # 包含 GX_OBJECT
    └── activity_ring.cpp
```

对应的 `CMakeLists.txt`：

```cmake
include(${CMAKE_CURRENT_SOURCE_DIR}/../cmake/meta.cmake)

add_executable(my_app
  main.cpp
  sensors/step_counter.cpp
  widgets/activity_ring.cpp
)
target_link_libraries(my_app PRIVATE glyphix::sdk)

glyphix_add_meta_objects(my_app
  sensors/step_counter.h
  widgets/activity_ring.h
)
```

::: tip 只传头文件，不传 .cpp
`glyphix_add_meta_objects()` 只需要传入包含 `GX_OBJECT` 声明的**头文件**（`.h`）。元对象编译器读取头文件中的宏声明来生成代码，不需要解析实现文件。相反，`.cpp` 文件中不能定义含 `GX_OBJECT` 的类。
:::

::: warning 不要遗漏注册
如果一个类声明了 `GX_OBJECT` 但没有通过 `glyphix_add_meta_objects()` 注册，会导致**链接错误**（找不到 `staticMetaObject` 等符号）。每当新增含有 `GX_OBJECT` 的头文件时，记得同步更新 `CMakeLists.txt`。
:::

### `glyphix::sdk` 接口目标

`GlyphixSDK.cmake` 定义了 `glyphix::sdk` CMake 接口库目标，它封装了 SDK 的所有链接依赖。在你的 `CMakeLists.txt` 中只需链接这一个目标：

```cmake
target_link_libraries(my_target PRIVATE glyphix::sdk)
```

它内部等价于：

```cmake
# 伪代码——实际由 GlyphixSDK.cmake 自动管理
target_include_directories(... ${GLYPHIX_INCLUDE_DIRS} wrapper/include)
target_link_libraries(... -Wl,--start-group ${glyphix-*.a} glyphix-wrapper -Wl,--end-group)
target_link_libraries(... m pthread dl)  # UNIX 系统库
```

使用 `-Wl,--start-group ... -Wl,--end-group` 包裹静态库是为了解决嵌入式平台上静态库之间的循环依赖链接问题。

::: tip 链接顺序问题
如果项目中有自己的静态库（如 `add_library(my_module STATIC ...)`），应该将其链接到 `glyphix::sdk` **内部**，否则 `--start-group` 的范围不会覆盖它，可能引发链接错误。方法是在 `GlyphixSDK.cmake` 的 `GLYPHIX_LIBS` 变量被定义之后、`glyphix-sdk` 目标被创建之前，将你的静态库路径追加进去，或者直接让最终可执行文件同时链接 `my_module` 和 `glyphix::sdk` 并手动指定 `--start-group`。
:::

## 宿主机构建

宿主机构建用于在开发机上运行 Glyphix 的示例程序，无需连接硬件即可快速验证控件和模块逻辑。

```bash
mkdir build && cd build
cmake -G Ninja ..
cmake --build .
```

SDK 的 `app/` 目录下包含多个示例，每个子目录对应一个独立的可执行目标。例如：

| 子目录 | 构建产物 | 说明 |
|:---|:---|:---|
| `app/emulator/` | `demo` | 带图形界面的模拟器，依赖 MiniFB 窗口后端 |
| `app/async/` | `async-demo` | 无图形界面的异步服务示例，演示 Native Module 和异步回调 |

`GlyphixSDK.cmake` 会自动检测宿主机的编译器三元组（通过 `gcc -dumpmachine` 或 `clang -dumpmachine`），并以此为键在 `libs/` 目录下查找对应的预编译库。例如在 x86_64 Linux 开发机上，会自动解析到 `libs/x86_64-linux-gnu/`。

如果自动检测的三元组与实际库目录不匹配，可以手动指定：

```bash
cmake -G Ninja -DTARGET_TRIPLE=x86_64-linux-gnu ..
```

如果只需要构建某个特定示例，可以指定目标名称：

```bash
cmake --build . --target demo
cmake --build . --target async-demo
```

## CMake 交叉编译

对于嵌入式目标，需要通过 `-DARCH` 参数指定目标架构。SDK 预置了以下架构配置：

| `-DARCH` 值 | 目标平台 | 工具链前缀 |
|:---:|:---:|:---:|
| `mips-linux-gnu` | MIPS Linux | `mips-linux-gnu-` |
| `cortex_m33-gnu` | ARM Cortex-M33（GNU） | `arm-none-eabi-` |
| `cortex_m7-gnu` | ARM Cortex-M7（GNU） | `arm-none-eabi-` |

### MIPS Linux 示例

```bash
export MIPS_TOOLCHAIN_DIR="/opt/mips-gcc720-glibc229"

mkdir build-mips && cd build-mips
cmake -G Ninja .. \
  -DARCH=mips-linux-gnu \
  -DMIPS_TOOLCHAIN_DIR="$MIPS_TOOLCHAIN_DIR" \
  -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

如果工具链已经在 `PATH` 中（即 `mips-linux-gnu-gcc` 可直接调用），则可以省略 `-DMIPS_TOOLCHAIN_DIR`，CMake 会自动定位。

### ARM Cortex-M 示例

```bash
mkdir build-cm33 && cd build-cm33
cmake -G Ninja .. \
  -DARCH=cortex_m33-gnu \
  -DARM_TOOLCHAIN_DIR="/opt/arm-none-eabi-gcc" \
  -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

在交叉编译中，`GlyphixSDK.cmake` 不会尝试自动检测三元组——架构文件（如 `cmake/arch/cortex_m33-gnu.cmake`）会直接设置 `TARGET_TRIPLE`，指向正确的库目录。

### 支持的目标架构

SDK 只为上表列出的架构提供预编译库。如果你的目标平台不在其中，需要联系 Glyphix 获取对应架构的 SDK 包，而不能在现有 SDK 基础上自行添加支持。

## 其他构建系统

SDK 使用 CMake 作为主要构建系统，Glyphix 同时会为合作厂商提供其他构建系统的支持。这通常只是引入预构建的 SDK 库和头文件，并添加 porting 层源文件。

### 工程限制

该方案适用于只需要标准 SDK 功能的项目。一旦需要定制控件、Native Module 等能力，就必须引入 `meta` 元对象编译器来生成必要的绑定代码，目前 CMake 是唯一支持的构建系统。

有几种可用的替代方案：
1. 使用 SDK CMake 项目构建定制代码，然后将生成的库链接到你的主项目中。
2. 使用 SDK CMake 项目构建定制代码，然后将生成的源文件（`*_meta.cpp`）包含到你的主项目中。
3. 直接在你的构建系统中调用 `meta` 工具生成绑定代码。

其中，Glyphix SDK 本身是通过方法 1 构建的。但它不适用于下游厂商的内部开发流程，因为它需要在主固件项目外维护一个单独的项目，并将生成的二进制库链接回主项目。这会造成严重的版本管理问题。

方法 3 通常也不理想，因为厂商通常不想在主项目的构建系统中引入一个外部工具。

### 推荐方案

因此，建议使用方法 2，这种方式拷贝源代码，虽然需要手动操作，但易于审核和集成到现有的构建流程中。你可以在 SDK 的 CMake 项目中构建定制代码，生成 `*_meta.cpp` 文件，然后将这些文件复制到你的主项目中，并在主项目的构建系统中编译它们。

这种方法的另一个限制是需要定制源文件可以在 SDK 项目环境中成功构建。具体来说，这要求它可以独立于主项目构建，包括：
- 需要正确设置包含路径和预处理器定义，定制组件的头文件中不能包含主项目特有的头文件。
- 定制组件的 cpp 文件最好也能编译通过，虽然这不影响生成 `*_meta.cpp` 文件，但可以方便在主机环境中进行快速迭代和调试。

::: tip
对于大多数[定制控件](widget.md)来说这不是问题。对于[Native Module](native-module.md)来说可能会更麻烦一些，应该注意：声明 `GX_OBJECT` 的头文件中不要包含主项目特有的头文件。
:::


============================================================
FILE_PATH: src/transl/EN/cxxdev/widget-export.md

# 控件注册与框架集成

在[控件开发指南](./widget.md)中，我们实现了一个 C++ 控件类。但此时它还只是一个普通的 C++ 对象，应用开发者无法在页面代码中直接使用。本文介绍如何将控件注册到框架，使其成为可在应用中使用的组件。本文档的许多概念涉及[对象系统](./object-system.md)，建议先阅读相关内容。

## 运行环境

控件注册依赖一组**运行环境对象**。它们是响应式框架运行所必需的依赖，必须在 `main()` 或平台启动代码中显式创建，并且其生命周期要覆盖整个应用运行期间：

```cpp
Application app(/* platform */);
JsVM vm;
Window window;
AppletKit kit(&window, "pkgs.db");
```

这几个对象负责整个应用的运行环境：
- `Application` 框架应用对象负责所有底层服务并维护事件循环，在初始化的最后调用 `app.exec()` 进入事件循环；
- `JsVM` 是内嵌的 JavaScript 引擎，承载响应式框架的运行，**必须**在 `AppletKit` 之前创建；
- `Window` 是顶层窗口，作为渲染输出目标；
- `AppletKit` 是应用（Applet）管理器，负责应用生命周期与控件注册。

::: warning 不要省略这些对象
`vm`、`window`、`kit` 等是 RAII 对象，框架通过它们的构造/析构来管理运行环境。即使代码里看不到对 `vm` 的直接调用，它的**存在本身**就是必需的——提前销毁或不创建会导致框架无法工作。
:::

`Window window` 有时候也可以替换成 `Wigdet window` 等，区别在于 `Window` 默认绘制不透明背景，而 `Widget` 默认透明。

## 注册控件

控件的注册通过 `AppletKit::installWidget<T>()` 完成，在 `AppletKit` 实例化之后、`launch()` 启动第一个应用**之前**调用：

```cpp
// 注册自定义控件（在 launch 之前）
kit.installWidget<ProgressRing>(); // 无参数，以类名注册，模板中写作 <progress-ring>
kit.installWidget<MySpecialChart>("SpecialChart"); // 或用自定义名称注册（见下文）

kit.launch("com.example.app");     // 启动应用
return app.exec();                 // 进入事件循环
```

::: tip 内置控件默认已注册
框架自带的按钮、标签等内置控件由 `installBuiltinWidgets()` 注册。只要 SDK 构建时启用了 CMake 选项 `GX_BUILTIN_BINDINGS`（默认 `ON`），`AppletKit` 构造时就会**自动调用**它，无需手动处理。仅当显式关闭该选项时，才需要自己调用 `kit.installBuiltinWidgets()`。
:::

注册后，框架会根据控件类的 `GX_OBJECT` 元数据，自动导出其属性、事件、方法，以及它们用到的枚举、结构体类型，使其在应用层可用。

### 在应用页面中使用

注册成功后，应用开发者可以在页面模板中像使用内置控件那样使用它：

```xml
<!-- 以 progress-ring 组件为例 -->
<progress-ring
  class="ring"
  :value="progress"
  @completed="onDone">
</progress-ring>
```

这里 `:value="progress"` 把控件的 `value` 属性绑定到应用数据 `progress`；`@completed` 监听控件暴露的 `completed` 事件。框架自动完成 JavaScript 值与 C++ 属性的互相转换，开发者无需写任何"桥接代码"。

### 自定义组件名称

默认情况下，控件以**类名**注册。如果类名不适合直接作为组件名，可以在注册时指定一个自定义名称：

```cpp
// 将 VendorWaveformGraph 以 WaveformGraph 注册，模板中写作 <waveform-graph>
kit.installWidget<VendorWaveformGraph>("WaveformGraph");
```

自定义名称要使用**大驼峰（PascalCase）**形式，与 C++ 类名风格一致。

### C++ ↔ UX 命名转换

组件标签名对应注册时的名称（默认为 `GX_OBJECT` 声明的**类名**，或注册时指定的自定义名称）。模板里习惯用短横线（kebab-case）书写，**ux 打包工具在编译期负责名称转换**：

- 标签名：模板中的 kebab-case ↔ 注册名的大驼峰（PascalCase）。如 `<progress-ring>` 对应类 `ProgressRing`。自定义注册名也如此。
- 属性名：模板中的 kebab-case ↔ C++ 中的 camelCase。如 `ring-color` 对应属性 `ringColor`。

也就是说，运行时框架按 C++ 中声明的原始名称（camelCase / PascalCase）精确匹配，而短横线写法只是模板侧的书写习惯，由 ux 工具转换后对接。

ux 组件中也可以使用与 C++ 相同的标签 PascalCase 和属性 camelCase，参见[组件命名规范](/tutorials/name-spec.md)。

## 属性和事件导出

`GX_PROPERTY` 声明的属性会被自动导出，规则如下：

- 属性名即框架组件中的属性名，二者直接对应
- 声明了 setter 的属性（`set xxx`）可以被应用赋值
- 声明了 getter 的属性（`get xxx`）可以被应用读取
- 声明了 signal（`signal xxxChanged`）时，属性变化的信号会被传递给绑定

例如以下完整的属性声明：

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
    GX_PROPERTY(Color ringColor, get ringColor, set setRingColor)
    GX_PROPERTY(bool showLabel, get showLabel, set setShowLabel)
    // ...
};
```

在应用层对应的用法：

```xml
<progress-ring
  :value="jobProgress"
  ring-color="#409EFF"
  :show-label="true">
</progress-ring>
```

模板里属性以短横线（kebab-case）书写，对应 C++ 中的 camelCase 属性名：`ring-color` → `ringColor`，`show-label` → `showLabel`（转换由 ux 打包工具完成，见上文）。`:value`、`:show-label` 是动态绑定（值为表达式），而 `ring-color="#409EFF"` 这样的字面量则是静态赋值。

### 事件导出

组件事件是通过**带变化信号的属性**导出的，而不是直接导出 `Signal<>` 成员。导出一个事件需要两步：

1. 声明一个 `Signal<...>` 成员（C++ 内部使用）；
2. 在某个 `GX_PROPERTY` 的 `signal` 字段中引用它。

关键规则是：应用侧监听的事件名是**属性名**，而**不是**信号成员的名字。

### 带值的属性变化事件

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    int value() const;
    void setValue(int v);

    Signal<int> valueChanged;   // 内部信号，这个名字对应用不可见
    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
};
```

应用侧用 `@属性名` 监听变化，因此这里写 `@value`（属性名），而**不是** `@value-changed`：尽管信号成员叫 `valueChanged`，应用看到的事件名始终是属性名 `value`。

```xml
<progress-ring :value="progress" @value="onProgressChanged"></progress-ring>
```

这一点和框架内置控件完全一致。例如 `Slider` 的值变化信号成员叫 `changed`，但应用侧监听的仍是属性名 `value`（`@value` 或双向绑定 `::value`）。

### 无值的纯事件

对于不携带数值、只表示“某件事发生了”的事件（如“完成”），用 `invalid_t` 作为属性类型声明一个只有信号、没有读写值的属性：

```cpp
Signal<>  completed;   // 进度完成时发射
GX_PROPERTY(invalid_t completed, signal completed)
```

应用侧可以这样监听（没有事件值）：

```xml
<progress-ring @completed="onDone"></progress-ring>
```

你无法将一个 `GX_PROPERTY` 声明为 `void` 类型，即便它根本没有 `get`/`set`，因此要用 `invalid_t` 作为占位类型。如果你希望事件携带值，必须声明为一个具体类型，并提供 `get` 方法——`Signal<T>` 的参数类型不会自动成为事件值，而是始终来自属性的 getter。

::: warning `Signal<>` 不会自动成为事件
只声明一个 `Signal<>` 成员、却不在任何 `GX_PROPERTY` 中用 `signal` 字段引用它，这个信号是**无法**在应用侧用 `@some-event` 监听的。框架只会把“属性的变化信号”，也就是 `signal` 字段暴露为事件，事件名始终来自属性名。
:::

## 方法导出

用 `GX_METHOD` 声明的成员函数会作为组件方法导出，供应用在 JavaScript 中调用：

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    GX_METHOD void reset();               // 无参方法
    GX_METHOD void animateTo(int target); // 带参方法
};
```

与属性、事件不同，方法不通过模板标签使用，而是先用 [`$element()`](../framework/component/component-apis.md#element) 取得原生组件对象，再在其上调用。对应模板需要给组件设置 `id`：

```xml
<progress-ring id="ring" :value="progress"/>
```

```js
onReady() {
  const ring = this.$element('ring'); // 'ring' 为模板中组件的 id
  ring.reset();
  ring.animateTo(80);
}
```

方法的参数与返回值由框架经 `Variant` 自动编组，无需手写转换代码（类型桥接的细节见[对象系统](./object-system.md#运行时类型系统)）。注意 `$element()` 须在 [`onReady()`](../framework/component/life-cycle.md#onready) 生命周期及之后调用，详见[原生组件](../framework/component/native-component.md)。

## 枚举与结构体类型

当属性或方法参数的类型是自定义的 C++ 枚举或结构体时，用 `GX_ENUM` / `GX_STRUCT` 标注即可一并导出，[注册控件](#注册控件)时框架会自动安装相应的类型转换，无需手写绑定代码。枚举在 JavaScript 侧表现为字符串常量，结构体表现为对象字面量：

```cpp
class ProgressRing : public Widget {
    GX_OBJECT
public:
    // 注意为值定义别名，否则 JavaScript 侧会使用
    // 'Solid' / 'Dashed' 名称，而不是预期的 'solid' / 'dashed'
    enum GX_ENUM LineStyle {
        Solid GX_ALIAS("solid") = 0,
        Dashed GX_ALIAS("dashed"),
    };
    // 结构体注意写默认值，以免在 JavaScript 侧创建时出现未定义字段
    struct GX_STRUCT Range { int min = 0; int max = 100; };

    GX_METHOD void setRange(const Range &range);

    GX_PROPERTY(LineStyle lineStyle, get lineStyle, set setLineStyle)
};
```

```xml
<progress-ring line-style="dashed"/>
```

```js
this.$element('ring').setRange({ min: 0, max: 100 });
```

枚举别名、结构体字段映射、嵌套类型等完整语义见[对象系统 · 复杂类型反射](./object-system.md#复杂类型反射)，此处不再展开。

::: warning 不要遗忘标注
属性或方法用到自定义枚举/结构体时，务必标注 `GX_ENUM` / `GX_STRUCT`，否则 JavaScript 侧无法使用，且没有任何编译错误提示。
:::

## 容纳子控件（容器型控件）

如果控件需要容纳应用声明的子内容，只需把它实现为一个**容器型控件**：在 C++ 侧负责子控件的布局，框架会自动把模板里嵌套声明的子组件创建为子控件并挂载到它下面。Glyphix 没有 HTML 那样的具名插槽（slot），模板中嵌套的标签会直接成为该控件的子控件。

容器的布局有两种实现方式（详见[控件开发指南](./widget.md)的「布局与尺寸」一节）：

- 使用框架现成的布局类，例如在构造函数中 `setLayout(new FlexLayout())`；
- 或覆写 `layoutEvent()`，在其中遍历 `children()` 手动设置每个子控件的几何。

在应用层，像嵌套子标签一样使用即可（这里 `card-panel` 是开发者实现并注册的容器控件，`text` 为内置控件）：

```xml
<card-panel>
  <text>标题</text>
  <progress-ring :value="progress"/>
</card-panel>
```

## 一个完整的例子

以下定义一个简单的数字显示控件，并将其注册为框架组件：

```cpp
// number_display.h
#pragma once
#include "gx_widget.h"
#include "gx_color.h"

class NumberDisplay : public Widget {
    GX_OBJECT
public:
    explicit NumberDisplay(Widget *parent = nullptr);

    int value() const { return m_value; }
    Color textColor() const { return m_color; }

    void setValue(int v);
    void setTextColor(const Color &c);

    bool event(Event *event) override;   // 唯一需要覆写的虚函数

    Signal<int> valueChanged;            // 内部信号；应用侧通过属性名 value 监听

    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
    GX_PROPERTY(Color textColor, get textColor, set setTextColor)

protected:
    // paintEvent / sizeHint 都不是虚函数，不能加 override
    void paintEvent(PaintEvent *event);
    Size sizeHint() const;

    // EventDispatch 需要访问 protected 处理函数
    friend struct EventTraits<NumberDisplay>;

private:
    int m_value = 0;
    Color m_color{0, 0, 0};
};
```

```cpp
// number_display.cpp
#include "number_display.h"
#include "gx_format.h"
#include "gx_painter.h"
#include "gx_widgetevent.h"   // EventDispatch

NumberDisplay::NumberDisplay(Widget *parent)
    : Widget(parent) {}

bool NumberDisplay::event(Event *event) {
    // 把事件分发给 paintEvent；声明 PaintEvent 可在编译期检查遗漏
    return EventDispatch<Widget, PaintEvent>{}(this, event);
}

void NumberDisplay::setValue(int v) {
    if (m_value == v) return;
    m_value = v;
    update();
    valueChanged(v);
}

void NumberDisplay::setTextColor(const Color &c) {
    if (m_color == c) return;
    m_color = c;
    update();
}

Size NumberDisplay::sizeHint() const {
    return Size(60, 30);
}

void NumberDisplay::paintEvent(PaintEvent *) {
    Painter p(this);
    p.setBrush(m_color);   // 文本颜色由画刷（Brush）决定，而非画笔
    p.setFont(Font(20));
    p.drawText(rect(), format("{}", m_value), AlignCenter);
}
```

注册：

```cpp
kit.installWidget<NumberDisplay>();
```

应用层使用：

```xml
<number-display
  :value="count"
  text-color="#333333"
  @value="onCountChanged">
</number-display>
```

至此，从 C++ 实现到应用使用，整个流程完整：`<number-display>` 标签经 ux 工具转换为注册名 `NumberDisplay` 而被识别。

每当应用数据 `count` 变化时，`:value` 绑定会调用 `NumberDisplay::setValue()`；当控件内部发射 `valueChanged` 信号时，框架触发名为 `value` 的事件（事件名取属性名），从而调用应用的 `onCountChanged`。若希望 `count` 与控件双向同步，可改用 `::value="count"`。


============================================================
FILE_PATH: src/transl/EN/cxxdev/widget-slider-demo.md

# 自定义 Widget 实战

`slider-demo` 是 Glyphix SDK 附带的一个完整示例，展示了如何用 C++ 从头实现一个**定制控件**：`WaveSlider`。这个控件在标准 `Slider` 的基础上增加了水波纹填充效果和点击涟漪动效，同时示例还涉及 `StyleEngine` 定制、直接用 C++ 构建 UI 界面等内容。

本文以此示例为线索，结合[控件开发指南](./widget.md)中的核心概念，完整地演示定制一个新 Widget 所需的全部步骤。

## 示例结构

示例的文件结构如下：

```
app/slider-demo/
├── CMakeLists.txt
├── main.cpp           # 应用入口，用 C++ 直接构建 UI
├── styleengine.h/.cpp # 定制 StyleEngine
└── waveslider.h/.cpp  # WaveSlider 控件的实现
```

直接编译运行 `slider-demo` 目标即可看到效果，无需配合前端项目。

### 构建说明

[配置好 SDK](sdk-setup.md#准备工作) 后，使用以下命令构建并运行示例：

```bash
mkdir build && cd build
cmake .. && cmake --build . -j
bin/slider-demo
```

::: important 宿主系统
必须在支持桌面环境的 Linux 系统上构建和运行此示例。
:::

## 用 C++ 直接构建 UI

在 `main.cpp` 中，应用的 UI 完全在构造函数中用 C++ 代码搭建，风格类似 Qt Widgets 或 LVGL：通过 `new` 创建子控件并传入父控件指针，无需声明式模板。

```cpp
int main() {
    Application app(new BSPPlatform(500, 500));
    app.setFont(Font(GX_EXAMPLE_ASSETS "/roboto.ttf", 32));
    app.setStyleEngine(new MyStyleEngine);

    Window window;
    window.setFlowLayout(true);

    MyWidget widget(&window);
    StyleModifier(&widget)->setSize(
      Length::fromPercent(100), Length::fromPercent(100));
    StyleModifier(&widget)->setMargin(Margin(10));
    return app.exec();
}
```

`Application` 接收一个平台后端对象（`BSPPlatform`）和分辨率。`Window` 是根控件，启用 `setFlowLayout(true)` 后，其子控件将按照流式布局自动排列。

`setStyleEngine` 挂载自定义的样式引擎，这不是必须的（否则使用默认样式）。只有当你需要定制控件外观（如下文中对 `Switch` 的改造）时才需要提供自己的实现。

### `MyWidget` 类

`MyWidget` 继承 `ScrollArea`，在构造函数中创建并添加子控件：

```cpp
class MyWidget : public ScrollArea {
public:
    explicit MyWidget(Widget *parent = nullptr) : ScrollArea(parent) {
        addItem(&m_switch);
        addItem(&m_label);
        addItem(&m_slider);
        // ...
    }
    // ...
private:
    Label  m_label;
    Switch m_switch;
    Slider m_slider;
};
```

子控件作为成员变量声明，构造时自动初始化（父控件在 `addItem` 中建立）。成员变量的生命周期由 `MyWidget` 管理，无需手动 `delete`。

`ScrollArea` 提供开箱即用的滚动、惯性、回弹等能力，`MyWidget` 不需要手写任何滚动逻辑。

::: tip `addItem()` 的作用
一般情况下，可以直接将子控件通过 `setParent()` 挂到父控件上，但 `ScrollArea` 内部实际上还有一个专门的内容容器（`contentWidget()`），普通元素不能直接添加到 `ScrollArea` 上，而是要通过 `addItem()` 添加到内容容器中。

对于简单的容器，`setParent()` 和 `addItem()` 的效果相同；但对于 `ScrollArea` 这类特殊容器，则**必须**使用 `addItem()` 添加元素。
:::

### 信号连接

控件之间通过信号连接同步状态：

```cpp
m_slider.changed.connect(this, &MyWidget::onSlider);
m_switch.checked.connect(this, &MyWidget::onSwitch);

// 双向同步两个 Slider 的值
waveSlider->changed.connect<AbstractSlider>(&m_slider, &Slider::setValue);
m_slider.changed.connect<AbstractSlider>(waveSlider, &WaveSlider::setValue);

// 开关切换 WaveSlider 的波形模式
m_switch.checked.connect(waveSlider, &WaveSlider::setWaveMode);
```

::: tip Signal 用法
信号连接的语法是 `signal.connect(receiver, &Type::method)`。当 `Slider::setValue` 和 `WaveSlider::setValue` 签名不完全一致时，可以通过模板参数声明公共基类（`AbstractSlider`）来消歧义。

当你不确定某个槽函数的实际所属类型时，可以通过 IDE 提示来检查，例如检查 `Slider::setValue` 时，IDE 通常会提示：
```cpp
public method
void setValue(int value) in class AbstractSlider 
```
这说明 `setValue` 实际上是声明在 `AbstractSlider` 中的。在连接时就需要指定 `AbstractSlider` 以消除歧义：
```cpp
m_slider.changed.connect<AbstractSlider>(waveSlider, &WaveSlider::setValue);
```
:::

### 用 StyleModifier 设置样式

`StyleModifier` 是在 C++ 中以编程方式设置控件样式的工具，效果等价于在模板中通过样式属性配置：

```cpp
StyleModifier m(waveSlider);
m->setSize(120, 300);
m->setMargin(Style::Margin{Length::fromAuto(), 20});
m->setColor(Color{"#35a7ff"});
```

`setColor` 为 `WaveSlider` 设置前景颜色，它会被 `paintEvent` 中读取并用于绘制进度填充色。

## 定制 StyleEngine

内置的 [`Switch`](/components/switch.md) 是一个功能完整的开关控件，但其默认外观类似 [Fluent 2](https://fluent2.microsoft.design/components/web/react/core/switch/usage)，可能不适合特定设备或品牌的视觉风格。

`StyleEngine` 是解决这个问题的机制。设备厂商可以实现自己的 `StyleEngine`，定制所有内置控件的外观，同时保留它们的交互逻辑，无需修改框架代码。

定制后的 `Switch` 不仅仅是换了主题颜色，相反，整套开关动效（滑块位移、颜色过渡、按压缩放）均可以通过**程序化插值**实现，而非预录序列帧图片。这意味着：

- 动效完全流畅，帧率与渲染系统一致；
- 颜色、尺寸可以被应用开发者通过样式属性覆盖，`StyleEngine` 提供的是可被覆盖的默认值；
- 无需为每种分辨率准备不同的图片素材。

### `StyleEngine` 的职责

`StyleEngine` 是 Glyphix 样式系统的核心，负责三件事：

1. **提供调色板**（palette）：全局颜色变量，类似 CSS 自定义属性，供所有内置控件和自定义控件读取。
2. **绘制控件外观**（paint）：框架内置控件（如 `Switch`、`Slider`）的视觉效果全部委托给 `StyleEngine::paint()` 绘制，开发者可以在派生类中重写，实现完全不同的外观。
3. **推荐尺寸**（size hint）：控件在不同样式状态下的推荐尺寸，供布局系统参考。

### 定义 MyStyleEngine

继承 `StyleEngine` 并重写 `sizeHint()` 和 `paint()`：

```cpp
class MyStyleEngine : public StyleEngine {
public:
    MyStyleEngine();
    Size sizeHint(StyleOption::Type type, const Widget *widget) const override;
    void paint(Painter &painter, Widget *widget, StyleOption &option) override;
};
```

构造函数中设置调色板：

```cpp
MyStyleEngine::MyStyleEngine() {
    setPalette(SwitchDark,  Color(0xff565656));
    setPalette(SwitchLight, Color(0xff2f5cff));
    setPalette(SwitchThumb, Color(0xffffffff));
}
```

`SwitchDark`、`SwitchLight`、`SwitchThumb` 是 `StyleEngine` 枚举中预定义的语义颜色键。不同的主题引擎可以赋予它们不同的颜色，控件始终通过键名读取而不是硬编码颜色值。

### 重写 `sizeHint()`

`sizeHint()` 告知框架内置控件在给定样式状态下的**推荐尺寸**。以 `Switch` 为例，其宽高应与字体像素大小成比例：

```cpp
Size MyStyleEngine::sizeHint(StyleOption::Type type, const Widget *widget) const {
    // 定制的 Switch 尺寸比例可以与内置策略不同
    if (type == StyleOption::OptionSwitch) {
        float f = widget->font().pixelSize();
        int d = int(round(f));
        return {int(round(f * SwitchAspectRatio)), d};
    }
    return StyleEngine::sizeHint(type, widget); // 其余类型交给基类
}
```

在函数末尾务必调用 `StyleEngine::sizeHint(type, widget)` 回退到默认实现，否则其他类型的控件会得到零尺寸。

### 重写 `paint()`

`paint()` 通过 `StyleOption` 的 `option()` 类型分发到对应的绘制逻辑，未处理的类型同样要回退：

```cpp
void MyStyleEngine::paint(Painter &painter, Widget *widget, StyleOption &option) {
    switch (option.option()) {
    case StyleOption::OptionSwitch:
        drawSwitch(this, painter, widget, static_cast<StyleOptionSwitch &>(option));
        break;
    default:
        StyleEngine::paint(painter, widget, option);
    }
}
```

`StyleOptionSwitch` 是 `StyleOption` 的派生类，添加了 Switch 特有的状态字段。它携带了两个关键的动画进度值：

- `option.transition`：Switch 开关过渡进度，`0.0` 为关闭状态，`1.0` 为打开状态，中间值表示动画进行中。
- `option.scale`：按下时的缩放系数，用于绘制按压反馈效果。

利用这两个值可以在 `drawSwitch` 中实现平滑的状态过渡：

```cpp
// 在打开和关闭颜色之间插值
color = color.blend(checked.background().color(), option.transition);

// thumb 指示器的位置随过渡进度移动
float pos = option.transition * (box.width() - size - len);
```

`StyleEngine` 负责动画的驱动，开发者只需在 `paint()` 中根据进度值插值，即可得到完整的过渡动效。

::: tip 仅定制部分控件
默认的 `StyleEngine` 实现了所有内置控件的绘制逻辑，其中一部分相当复杂。如果你只对其中一部分控件的外观不满意，应当在派生类中仅重写这些控件的绘制逻辑，其他控件直接回退到基类实现。

应优先考虑通过调色板来满足定制颜色，只有在需要完全不同的视觉效果时才重写 `paint()`。
:::

### VectorPath 绘制圆角胶囊形

默认的 `Switch` 的背景和 thumb 都是圆角胶囊形状。示例中使用 `VectorPath` 配合两段圆弧来绘制，这是一种比 `drawRoundedRect` 更灵活的方式，适合需要对两端分别控制弧度的场景：

```cpp
static void indicatorBar(Painter &p, const RectF &rect) {
    float radius = rect.height() * 0.5f;
    float x1 = rect.left() + radius;
    float x2 = rect.right() - radius;
    float y = rect.top() + radius;
    VectorPath path;
    path.arcTo(PointF(x1, y), radius, radius, 90, 270);   // 左端半圆
    path.arcTo(PointF(x2, y), radius, radius, -90, 90);   // 右端半圆
    p.fillPath(path);
}
```

两段圆弧首尾相接，`arcTo` 在路径中自动连线，无需额外 `lineTo`。

## WaveSlider：自定义控件完整实践

`WaveSlider` 是本示例的核心，展示了定制控件的完整开发流程。与上文中的 `StyleEngine` 定制类似，`WaveSlider` 的设计目标也是在不破坏已有能力的前提下**叠加**新的视觉效果：

- **波浪填充**模式：进度区域以动态波浪填充，而不是普通的矩形进度条；
- **点击涟漪**效果：按下时产生扩散振荡，使波浪短暂增强再恢复；
- **`waveMode` 属性**：可在运行时切换波形模式和普通模式，并支持应用层绑定和属性动画；
- **完整回退兼容**：波形模式关闭时，`WaveSlider` 直接调用 `Slider::paintEvent()` 回退到默认外观，复用父类的拖拽、`value`/`changed` 等全部能力，应用侧无需改动任何代码。

### 类定义与继承

`WaveSlider` 继承自 `Slider`（而非直接继承 `Widget`），可以复用 `Slider` 已有的手势拖拽逻辑、`value`/`minimum`/`maximum` 等属性，以及 `changed` 信号：

```cpp
// waveslider.h
#include "gx_slider.h"
#include "gx_valueanimation.h"

class WaveSlider : public Slider {
    GX_OBJECT
public:
    explicit WaveSlider(Widget *parent = nullptr);
    ~WaveSlider() override = default;

    GX_NODISCARD bool isWaveMode() const { return m_waveMode; }
    void setWaveMode(bool enabled);
    bool event(Event *event) override;

    GX_PROPERTY(bool waveMode, get isWaveMode, set setWaveMode)
    // ...
};
```

`GX_OBJECT` 必须放在类定义最开始，它触发元对象编译器为此类生成元数据。`GX_PROPERTY` 将 `waveMode` 暴露给属性系统，使其可被应用层绑定（如 `<wave-slider :wave-mode="enabled"/>`）和属性动画驱动。

### 成员变量

控件的运行时状态保存在成员变量中：

```cpp
private:
    bool  m_waveMode = false;       // 当前是否为波形模式
    float m_rippleProgress = 1.0f;  // 涟漪进度 [0, 1]，初始为 1（表示未激活）
    float m_waveOffset = 0.0f;      // 波形相位偏移 [0, 1]，由动画驱动
    ValueAnimation<float> m_animation;        // 波浪循环动画
    ValueAnimation<float> m_rippleAnimation;  // 涟漪动画
    friend struct EventTraits<WaveSlider>;    // 允许事件分发访问 protected 方法
```

`ValueAnimation<float>` 直接作为成员变量（而非指针），生命周期由 `WaveSlider` 管理，无需手动 `delete`。

### 构造函数：初始化动画

构造函数配置两个动画并设置方向：

```cpp
WaveSlider::WaveSlider(Widget *parent) : Slider(parent) {
    // 波浪动画：无限循环，每秒一个完整周期
    m_animation.setRepeat(AbstractAnimation::Infinity);
    m_animation.setValueLimits(0.f, 1.f);
    m_animation.setDuration(1000);
    m_animation.value.connect(this, &WaveSlider::onWaveAnimation);
    m_animation.start();

    // 涟漪动画：按下时一次性播放，持续 800ms
    m_rippleAnimation.setValueLimits(0.f, 1.f);
    m_rippleAnimation.setDuration(800);
    m_rippleAnimation.value.connect(this, &WaveSlider::onRippleAnimation);

    setVertical(true);  // 竖向滑动条
}
```

`m_animation` 在启动后一直运行，每帧将 `m_waveOffset` 从 $0$ 推进到 $1$，再循环回 $0$。这个值最终转换为波形的相位偏移，使波浪持续流动。

`m_rippleAnimation` 仅在按下时触发，播放一遍即停止，不设置 `Infinity`。两个动画的回调分别只做一件事：更新状态变量并调用 `update()` 请求重绘。

```cpp
void WaveSlider::onWaveAnimation(float value) {
    m_waveOffset = value;
    update();
}
void WaveSlider::onRippleAnimation(float value) {
    m_rippleProgress = value;
    update();
}
```

### 事件处理

#### 配置 EventDispatch

`event()` 中使用 [`EventDispatch`](widget.md#处理事件) 路由事件，模板参数列出了当前控件实际处理的事件类型，起到编译期检查的作用：

```cpp
bool WaveSlider::event(Event *event) {
    return EventDispatch<Widget,
        GestureEvent, PaintEvent>{}(this, event);
}
```

#### 处理手势：触发涟漪

`gestureEvent()` 拦截 `Press` 手势的开始时刻来触发涟漪，其余情况委托给 `Slider` 的手势处理（实现拖拽调值）：

```cpp
bool WaveSlider::gestureEvent(GestureEvent *event) {
    if (!event->isHitTest() && event->gesture()->type() == Gesture::Press) {
        auto g = static_cast<PressGesture *>(event->gesture());
        if (g->isStarted())
            startRipple(g->clientPoint());
    }
    return Slider::gestureEvent(event); // 将事件继续交给 Slider 处理
}

void WaveSlider::startRipple(const Point &) {
    m_rippleProgress = 0.f;      // 从头开始
    m_rippleAnimation.start();   // 重新播放
}
```

`isHitTest()` 为 `true` 时表示这是一次命中测试（框架用于检测事件是否应该落在此控件上），不代表真正的用户交互，应跳过。

::: tip 关于 `isHitTest()`
命中测试是事件分发的前置步骤，`gestureEvent()` 在命中测试阶段也会被调用，但此时不应有任何副作用（如启动动画）。永远先判断 `!event->isHitTest()` 再处理交互逻辑。
:::

#### 样式读取接口

`paintEvent()` 中会读取控件对应的样式数据，这里先介绍两个涉及的接口：

- `style()` / `style(Styles::Xxx)` 返回当前控件某个样式伪类的 `Style` 对象，可以从中读取颜色、背景等属性；
- `se->palette(StyleEngine::Xxx)` 从 `StyleEngine` 读取全局调色板颜色，当控件未设置自定义颜色时作为默认值。

两者配合实现“有自定义配置时用自定义颜色，否则回退到主题默认色”的逻辑：

```cpp
auto contentStyle = style(Styles::Content);
p.setBrush(contentStyle.hasProperty(style::Background)
               ? contentStyle.background()
               : se->palette(StyleEngine::ProgressRange));
```

### 绘制实现

`paintEvent()` 是 WaveSlider 的核心。根据 `m_waveMode` 决定走哪条绘制路径：

```cpp
void WaveSlider::paintEvent(PaintEvent *event) {
    discard(event);  // PaintEvent 本身不携带有用信息，明确丢弃以消除编译警告

    if (!isWaveMode())
        return Slider::paintEvent(event);  // 普通模式：直接调用父类绘制

    auto se = App()->styleEngine();
    RectF box = rect();
    float radius = min(box.width(), box.height()) * 0.5f;
    float progress = sliderRange ? float(value() - minimum()) / float(sliderRange) : 0.f;

    Painter p(this);

    // 绘制背景（空轨道）
    p.setBrush(/* 背景色 */);
    p.fillRoundedRect(box, radius);

    // 绘制波浪填充（进度区域）
    p.setBrush(/* 前景色 */);
    VectorPath path;
    buildWaveFillPath(path, box, radius, progress, m_waveOffset, m_rippleProgress);
    if (!path.isEmpty())
        p.fillPath(path);
}
```

整个绘制分两步：先用 `fillRoundedRect` 画出完整的背景圆角矩形，再用 `fillPath` 在其上方画出波形填充，两层叠加形成“有波纹的进度条”。

#### 波形路径生成

`buildWaveFillPath()` 是一个独立的辅助函数（不在类内），负责在给定几何约束下构造波形路径：

```cpp
static void buildWaveFillPath(VectorPath &path, const RectF &box, float radius,
                              float progress, float waveOffset, float rippleProgress)
```

其核心逻辑分三步：

1. **计算水位和振幅**：`waterLevel` 从底部按 `progress` 比例上升；振幅取决于宽高比例，并被限制在离顶底圆弧足够远的范围内，避免波形越界。
2. **采样波形**：从左到右均匀采样，对每个 $x$ 坐标计算 $y$ 值。
   波形由三部分叠加：常规正弦波（`m_waveOffset` 控制相位）+ 涟漪增益（`m_rippleProgress` 控制衰减振荡）+ 圆角约束（确保路径不超出圆角矩形的边界）。
3. **封闭路径**：从波形顶部到圆角矩形底部沿底边返回，形成封闭多边形，供 `fillPath` 填充。

算法细节属于教学性质的效果演示，实际产品中可以根据设计需求替换为任意自定义的路径生成逻辑。

::: tip 路径绘制的效率
采样点数量（`sampleCount`）与控件宽度成正比（约每 `4px` 一个点），在典型屏幕分辨率下性能消耗可以接受。如果 CPU 较弱，可以降低采样密度或换用贝塞尔曲线近似。
:::

### waveMode 属性

`setWaveMode()` 的实现很简单：状态变化时更新成员值并标记重绘：

```cpp
void WaveSlider::setWaveMode(bool enabled) {
    if (m_waveMode != enabled) {
        m_waveMode = enabled;
        update();
    }
}
```

`GX_PROPERTY` 宏的声明使 `waveMode` 成为框架可见属性：

```cpp
GX_PROPERTY(bool waveMode, get isWaveMode, set setWaveMode)
```

此处没有声明 `signal` 字段，因为它通常由使用方驱动值变化，而非交互触发。

### 生产级优化

`WaveSlider` 的实现主要面向教学演示，并缺少一些优化，例如：
- 波形动画始终播放，即使 `waveMode` 关闭时也在 `update()`，这会反复触发 `paintEvent()`；
- 仅支持竖向滑动条，未对水平模式进行适配（按产品需求自行决定）；
- 固定绘制胶囊形轨道，实际产品可能需要使用圆角矩形或其他形状。

## 各部分协作关系

以下是 `slider-demo` 中各组件在运行时的协作关系：

```
用户按下屏幕
    ├─ WaveSlider::gestureEvent() 检测到 Press.isStarted()
    │       └─ startRipple() 重置 m_rippleProgress 并启动 m_rippleAnimation
    └─ Slider::gestureEvent() 继续处理，根据触点位置调整 value
            └─ changed 信号发射 → MyWidget::onSlider() 更新 Label 文字

每帧渲染循环
    ├─ m_animation 持续推进 m_waveOffset (0→1 循环)
    │       └─ update() → paintEvent() 用新 offset 重绘波形
    └─ m_rippleAnimation 推进 m_rippleProgress (0→1 播完停止)
            └─ update() → paintEvent() 用新 rippleProgress 重绘涟漪衰减

Switch 切换
    └─ waveSlider->setWaveMode(true/false)
            └─ update() → paintEvent() 切换为普通模式或波形模式
```

各信号连接在 `MyWidget` 的构造函数中一次性建立，之后运行时完全由事件和信号驱动，控件之间没有直接调用。

## 关键模式总结

通过 `slider-demo`，可以归纳出在 Glyphix 中实现定制控件的典型模式：

| 需求 | 做法 |
|---|---|
| 继承现有控件，复用其交互逻辑 | 继承对应基类（如 `Slider`），在 `EventDispatch` 中控制回退基类 |
| 自定义绘制 | 实现 `paintEvent()`，`isWaveMode()` 为 `false` 时调用 `Slider::paintEvent()` 回退 |
| 持续循环的动画 | `ValueAnimation::setRepeat(Infinity)` |
| 一次性触发动画 | 保存状态变量，在 `gestureEvent()` 中调用 `anim.start()` 重新播放 |
| 向应用层暴露属性 | `GX_PROPERTY` 宏，配合 getter/setter 和可选的信号 |
| 读取用户配色或主题色 | `style().hasProperty()` 检查后回退到 `se->palette()` |
| 自定义全局控件外观 | 继承 `StyleEngine`，重写 `paint()` 和 `sizeHint()` |

这些模式在[控件开发指南](widget.md)中均有详细阐述，`slider-demo` 是它们的综合实践。

## 与其他 GUI 框架的对比

::: important C++ 控件开发的定位
Glyphix 的主流开发方式是通过 [`.ux` 单文件组件](../tutorials/quick-orientation.md)以声明式模板构建界面。C++ 控件开发的用途是实现**设备端的底层控件库**（例如设备厂商定制的 `WaveSlider`），这些控件随后会被前端应用层通过模板和数据绑定使用。直接用 C++ 搭建完整 UI（如 `main.cpp` 中的示范）在框架中是**可以实现的，但并非推荐工作流**，相关工具链支持（调试、热更新、布局预览）也不如应用层完善。

因此，评估 Glyphix 的整体开发效率时，应以前端应用层为基准；本节讨论的 C++ 控件开发体验仅代表底层控件库的开发场景。
:::

Glyphix 的 C++ 控件开发在心智模型上更接近 Qt Widgets 而非 LVGL：信号机制、属性宏、继承式扩展、`paintEvent` 的命名和职责划分都与 Qt Widgets 基本对应，有 Qt 背景的开发者可以快速建立直觉。

LVGL 开发者则需要从 C 句柄风格向 C++ OOP 风格转换，差距相对更大，但控件树组织、`update()` 重绘触发等核心范式是共通的。本节以 `slider-demo` 为参照，具体说明各框架之间的相似之处与关键差异。

### 相似之处

无论是 Qt Widgets、LVGL 还是 Glyphix，它们共享一套经过验证的 UI 框架核心范式：

- **控件树**：UI 以父子树形结构组织，子控件的坐标相对于父控件。`MyWidget(&window)` 和 Qt 的 `new QWidget(&parent)`、LVGL 的 `lv_obj_create(parent)` 在语义上对应。
- **自定义绘制**：通过“覆写”绘制方法实现控件外观。Qt 重写 `paintEvent(QPaintEvent *)`，LVGL 注册 `LV_EVENT_DRAW_MAIN` 回调，Glyphix 实现 `paintEvent(PaintEvent *)`，三者设计思路一致。
- **信号/槽机制**：控件间通过信号传递状态变化，接收方以成员函数响应。
  - Glyphix：`m_slider.changed.connect(this, &MyWidget::onSlider)`；
  - Qt：`connect(&slider, &QSlider::valueChanged, this, &MyWidget::onSlider)`；
  - LVGL：通过事件回调函数实现类似功能。
- **继承复用**：扩展现有控件时通过继承实现。`WaveSlider : public Slider` 复用了父类的所有拖拽和取值逻辑，只重写绘制部分，与大部分 OOP GUI 框架的设计一致。
- **按需重绘**：状态变化时调用 `update()` 标记脏区，由框架在下一帧统一重绘，而非立即绘制。主流框架均采用此策略以避免帧内重复绘制。

### 与 Qt Widgets 的差异

#### 事件分发

Qt 通过虚函数重写来分发事件，每个事件方法都是 `virtual`，子类用 `override` 覆盖：

```cpp
// Qt
class MySlider : public QSlider {
    void paintEvent(QPaintEvent *event) override { ... }
    void mousePressEvent(QMouseEvent *event) override { ... }
};
```

Glyphix 的 `paintEvent()`、`gestureEvent()` 等事件处理函数**不是虚函数**，不能加 `override`，事件路由由 `EventDispatch` 在编译期完成：

```cpp
// Glyphix
bool WaveSlider::event(Event *event) {
    return EventDispatch<Widget, GestureEvent, PaintEvent>{}(this, event);
}
// paintEvent 和 gestureEvent 均为普通成员函数，无 override
```

这是为了避免了虚函数的间接跳转，在嵌入式设备的高频事件处理中有性能优势；同时模板参数列表起到编译期文档和漏项检查的作用。如果你声明了处理 `PaintEvent` 但忘记实现 `paintEvent()`，编译器会报错，而不是静默回退到基类。

#### 对象和属性系统

Qt 使用 `Q_PROPERTY` 宏配合 MOC（元对象编译器）生成属性元数据；Glyphix 使用 `GX_PROPERTY` 配合 `GX_OBJECT`，机制类似，但生成方式和运行时接口不同：

```cpp
// Qt
Q_PROPERTY(int value READ value WRITE setValue NOTIFY valueChanged)
// Glyphix
GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
```

两者都支持通过属性名字符串进行动画驱动（`QPropertyAnimation` / `PropertyAnimation`）。但在实现控件自身时，Glyphix 更推荐直接使用 `ValueAnimation<T>`，避免属性名查找的开销，并避免与应用层驱动的属性动画产生冲突。

#### 信号和槽

如[对象系统](object-system.html#信号-signal)描述，Glyphix 也有信号机制，但是它更接近 boost::signals2，不依赖 MOC 生成代码。这是有意为之的设计，因为 Glyphix 生态的[构建系统](sdk-setup.md#其他构建系统)较为碎片化，我们假设下游完全不使用元对象编译器。

#### 样式与外观定制

Qt 的控件外观定制有两条路：`QStyle` 子类化（较复杂）或 QSS 样式表（类 CSS 字符串，运行时解析）。Glyphix 使用 `StyleEngine`：厂商实现 `StyleEngine` 子类，在 `paint()` 中以 C++ 代码绘制全部内置控件的外观，在 `sizeHint()` 中提供推荐尺寸。这种方式适用于全局的系统级样式定制，而非单个控件的局部样式调整。

在单个控件的样式设置上，Glyphix 使用 `StyleModifier` 辅助对象以编程方式赋值，而不常用 CSS 字符串：

```cpp
StyleModifier m(waveSlider);
m->setSize(120, 300);
m->setColor(Color{"#35a7ff"});

// 也支持 inline style 字符串
waveSlider->setStyle(Style{"background-color: #35a7ff; color: #cce;"});
```

Glyphix 的样式和布局属性更多地通过样式属性来设置，而非直接调用控件方法。这是因为 C++ 主要定位于底层控件库开发，并不直接面向应用开发。

#### 内存与生命周期

Qt 的父子控件所有权模型下，`new QWidget(parent)` 后由父控件负责销毁子控件。Glyphix 同样支持这种模式（`new WaveSlider` 后 `addItem()`），也推荐将子控件声明为成员变量（如 `MyWidget` 中的 `m_label`、`m_slider`），生命周期随宿主对象自动管理，无需手动 `delete`，也不依赖父子树销毁机制。

### 与 LVGL 的差异

#### 编程模型

LVGL 是以 C 实现的框架，控件通过 `lv_obj_t *` 句柄操作，函数命名通常遵循 `lv_<类型>_<操作>()` 约定：

```c
// LVGL
lv_obj_t *slider = lv_slider_create(parent);
lv_slider_set_value(slider, 50, LV_ANIM_ON);
lv_obj_add_event_cb(slider, my_event_cb, LV_EVENT_VALUE_CHANGED, NULL);
```

Glyphix 是原生 C++ OOP 框架，方法通过对象调用，`this` 天然携带上下文：

```cpp
// Glyphix
auto *slider = new Slider(parent);
slider->setValue(50);
slider->changed.connect(this, &MyWidget::onSlider);
```

对 LVGL 开发者来说，这里的主要变化不是能力本身，而是表达方式：以前你是在对象句柄外部调用函数，现在则是在控件类内部组织状态、事件和绘制逻辑。类型系统也会在编译期帮助你避免一部分句柄类型误用。

#### 事件系统

LVGL 的事件处理通常通过单一回调函数接收多种事件，在回调内用 `lv_event_get_code()` 枚举分支：

```c
// LVGL
static void event_cb(lv_event_t *e) {
    lv_event_code_t code = lv_event_get_code(e);
    if (code == LV_EVENT_PRESSED) { ... }
    else if (code == LV_EVENT_VALUE_CHANGED) { ... }
}
```

Glyphix 则按事件类型分发到独立的处理函数，不同事件之间完全隔离，参数也各自携带类型正确的数据：

```cpp
// Glyphix
bool WaveSlider::gestureEvent(GestureEvent *event) { ... }
void WaveSlider::paintEvent(PaintEvent *event) { ... }
```

此外，Glyphix 的 `isHitTest()` 机制在 LVGL 中没有完全等价的对应物。LVGL 可以通过 `LV_EVENT_HIT_TEST` 处理相近问题，但通常仍需要在同一回调中自行分支。

::: tip Glyphix 内部的事件分发机制
`EventDispatch` 内部也是一个 switch-case 分发，但是我们不建议开发者手写 switch 分支，而是总是使用固定的 `EventDispatch<Widget, ...>{}(this, event)` 模式，方便代码审核。
:::

#### 动画

LVGL 的动画通过 `lv_anim_t` 结构体配置，目标值通过函数指针和 `void *` 用户数据传递：

```c
// LVGL
lv_anim_t a;
lv_anim_init(&a);
lv_anim_set_exec_cb(&a, anim_cb);
lv_anim_set_var(&a, obj);
lv_anim_set_values(&a, 0, 100);
lv_anim_set_time(&a, 800);
lv_anim_start(&a);
```

Glyphix 的 `ValueAnimation<T>` 通过模板参数在编译期确定插值类型，通过信号连接消除 `void *` 转型：

```cpp
// Glyphix
m_rippleAnimation.setValueLimits(0.f, 1.f);
m_rippleAnimation.setDuration(800);
m_rippleAnimation.value.connect(this, &WaveSlider::onRippleAnimation);
```

`ValueAnimation<T>` 内置了对 `Color`、`Point`、`Transform` 等复合类型的插值支持，而 LVGL 原生只支持整数范围，复合类型需要自行实现插值回调。

#### 矢量路径绘制

LVGL 的绘制 API 以矩形、弧形等基础图元为主，矢量路径支持（`lv_draw_vector`）是较新加入的能力，接口相对底层。Glyphix 的 `VectorPath` 是标准的路径构建接口，`moveTo`、`lineTo`、`arcTo`、`conicTo`、`cubicTo` 完整覆盖常见曲线类型，`WaveSlider` 中的波形即完全依赖此接口实现，无需引入额外的图形库。

#### 内存与生命周期

两者都支持对象树管理：子控件挂在父控件下，父对象销毁时子对象也会一起销毁。

Glyphix 还可以把子控件、动画和运行时状态直接写成类成员，交给 C++ 的 RAII 自动管理。例如 `MyWidget` 中的 `m_label`、`m_slider`，以及 `WaveSlider` 中的两个 `ValueAnimation<float>`，都可以随宿主对象构造和析构，而不必像 LVGL 那样主要围绕句柄、`user_data` 和回调上下文来组织状态。


============================================================
FILE_PATH: src/transl/EN/cxxdev/widget.md

---
headerDepth: 2
---
# 控件开发指南

在 Glyphix 中，所有可见的 UI 元素都是 `Widget`（控件）。框架内置了按钮、标签、图片、滚动区域等常用控件，但设备厂商往往需要根据自己的产品特色开发定制化的控件。例如，智能手表可能因为较小的圆形屏幕而定制特殊的列表动效，仪表设备则需要定制专门的图表控件。这篇文档介绍如何用 C++ 实现一个新控件。

## 控件基础

`Widget` 是一个矩形区域，它有位置、大小、可见性、透明度等基本属性，可以接收事件，并负责绘制自身的内容。控件以树形结构组织：一个父控件包含若干子控件，子控件的坐标相对于父控件。

每个控件都有一个**逻辑更新周期**：当控件的状态发生变化（例如数据更新了），调用 `update()` 标记为"需要重绘"，框架会在下一个渲染帧统一重绘所有已标记的控件，而不是立即重绘——这避免了同一帧内多次重复绘制。

### 控件与组件系统

UI 控件通常实现为一个 C++ 类，继承自 `Widget`，并符合标准的 C++ 面向对象设计。Glyphix 的响应式框架和组件系统则支持将这些 C++ 控件直接暴露为原生组件，并以模板化、声明式的方式来使用。

这种设计使得 C++ 侧的控件开发和前端组件使用可以相对独立，并保持双方习惯的开发方式。例如，在 C++ 中，你可以使用类似 LVGL 或者 Qt Widgets 的方式来构建界面，而完全不需要接受前端框架流行的声明式风格。

### 与其他框架的对比

Glyphix 控件系统在设计上类似于 Qt Widgets 或 LVGL 等传统 C/C++ UI 框架。所以你会发现开发一个新控件的方式和知识体系与这些框架非常相似：
- 通过继承 `Widget` 来创建新控件类；
- 存在布局系统、事件系统、绘制系统等核心机制；
- 通过属性系统和信号机制实现数据绑定和事件通知；
- 具有坐标系、尺寸等几何概念，并且支持嵌套的控件树结构。

::: tip 不建议使用 C++ 控件开发 UI
Glyphix 的设计初衷并非直接在 C++ 侧开发 UI，因此我们不会提供相关的文档和示例。
:::

## 创建自定义控件

本节以一个环形进度条控件（`ProgressRing`）为例，逐步说明开发一个自定义控件所需的各个要素。

::: tip 控件综合示例
SDK 附带的 [slider-demo](./widget-slider-demo.md) 示例是本文档所有知识点的完整实践，包括继承现有控件、绘制、事件处理、属性声明、`ValueAnimation` 动画，以及 `StyleEngine` 定制。建议在阅读完本文档后参阅。
:::

### 定义控件类

新建一个控件，继承 `Widget`，在类定义最开始加上 `GX_OBJECT` 宏，并**覆写 `event()`** 虚函数作为事件处理的入口：

```cpp
// progressring.h
#include "gx_widget.h"

class ProgressRing : public Widget {
    GX_OBJECT
public:
    explicit ProgressRing(Widget *parent = nullptr)
        : Widget(parent), m_value(0) {}

    int value() const { return m_value; }
    void setValue(int v);
    bool event(Event *event) override;

    GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
    Signal<int> valueChanged;

protected:
    void paintEvent(PaintEvent *event);

    // EventDispatch 需要访问 protected 方法，声明友元
    friend struct EventTraits<ProgressRing>;

private:
    int m_value;  // [0, 100]
};
```

`GX_OBJECT` 是必不可少的，它触发元对象编译器为此类生成元数据，使控件可以被框架的属性系统、动画系统和组件系统正确感知（详见[对象系统](./object-system.md)）。

### 绘制控件

在 `.cpp` 文件中包含 `gx_widgetevent.h`，实现 `event()` 和 `paintEvent()`：

```cpp
// progressring.cpp
#include "progressring.h"
#include "gx_widgetevent.h"

bool ProgressRing::event(Event *event) {
    return EventDispatch<Widget>{}(this, event);
}

void ProgressRing::paintEvent(PaintEvent *event) {
    Widget::paintEvent(event);
    Painter p(this);
    // ... 详见绘制章节
}
```

自定义绘制通过实现 `paintEvent()` 完成；构造 `Painter` 时传入 `this` 指针，即可获得与当前控件关联的绘图上下文，然后调用各类绘制方法进行绘制。有关 `Painter` API 的完整说明，参见[绘制](./painting.md)章节。

### 处理事件

Glyphix 的事件系统**并不依赖虚函数继承**来分发事件，`paintEvent()`、`gestureEvent()` 等方法都不是 `virtual` 的，**不要**在声明时加 `override`（会编译报错）。框架通过 `EventDispatch` 在**编译期**按事件类型将调用路由到正确的处理函数。

唯一需要（也必须）覆写的虚函数是 **`event()`**，在其中委托给 `EventDispatch`：

```cpp
bool ProgressRing::event(Event *event) {
    return EventDispatch<Widget>{}(this, event);
}
```

`EventDispatch` 的第一个模板参数通常是**直接基类**（也就是 `ProgressRing` 继承的那个类，此处为 `Widget`）。它会在编译期检查当前类是否直接声明了对应的处理函数，有则调用，否则自动回退到基类实现。处理函数的返回值为 `bool` 时表示是否消费了该事件；返回 `void` 时视为已消费。

::: tip 基类选择技巧
`EventDispatch` 的基类参数选择有一些优化技巧，通常可以选择直接基类，但也可以用更高层的祖先类，这会造成细微的代码大小和性能差异。但一般不需要过于纠结，也不用担心误用出错——只要编译通过了，事件分发就会正确工作。
:::

::: important
下文中提到“覆写 `xxxEvent()`”的说法时，请注意仅仅是在派生控件类中**声明**了一个与基类事件处理函数签名相同但**非虚**的成员函数。这**不是**虚函数，不能加 `override`，也不依赖虚函数机制来分发事件。

IDE 可能提示将这些成员函数改为虚函数，不要理会这个提示。
:::

如果要处理手势输入，声明 `gestureEvent()` 并在类中实现：

```cpp
// 在头文件 protected 区域增加声明：
bool gestureEvent(GestureEvent *event);

// 在 .cpp 中实现：
bool ProgressRing::gestureEvent(GestureEvent *event) {
    if (event->type() == Event::Press) {
        // ...
        return true;   // 返回 true 表示事件已消费，不再向父控件传递
    }
    return false;
}
```

可处理的事件类型：

| 方法签名 | 触发时机 |
|---|---|
| `bool gestureEvent(GestureEvent *)` | 手势事件，包括 Press、Pan、Swipe 等 |
| `bool wheelEvent(WheelEvent *)` | 滚轮或旋钮输入（如表冠） |
| `bool keyEvent(KeyEvent *)` | 实体按键 |
| `void resizeEvent(ResizeEvent *)` | 控件尺寸变化 |
| `void moveEvent(MoveEvent *)` | 控件位置变化 |
| `bool focusEvent(FocusEvent *)` | 焦点变化 |
| `void paintEvent(PaintEvent *)` | 重绘请求 |
| `bool layoutEvent(LayoutEvent *)` | 布局请求 |
| `void tickEvent(TickEvent *)` | 逐帧 tick（需主动调用 `requestNextTick()` 启用） |

如果某些事件处理函数对当前控件是**必须实现**的，可以在 `EventDispatch` 的模板参数中声明，遗漏或签名不匹配时编译报错：

```cpp
bool MyButton::event(Event *event) {
    // 若未正确声明 paintEvent 或 gestureEvent，编译失败
    return EventDispatch<Widget, PaintEvent, GestureEvent>{}(this, event);
}
```

::: tip 声明必要事件处理函数
尽管可以使用 `EventDispatch<Widget>` 来自动分发所有事件，但是**强烈建议**显式声明当前控件需要处理的事件类型，这样可以在编译期尽可能地检查遗漏或笔误，并减少人工审核的负担。
:::

### 属性与信号

使用 `GX_PROPERTY` 宏向框架暴露属性，使其可被应用层绑定、也可作为属性动画的目标：

```cpp
// 声明 value 属性，getter 为 value()，setter 为 setValue()
// signal 字段关联变化信号，供响应式框架订阅
GX_PROPERTY(int value, get value, set setValue, signal valueChanged)
```

声明后，`value` 属性可以：
- 被应用层模板直接绑定（如 `<progress-ring :value="progress"/>`）
- 被属性动画系统平滑过渡（当属性类型支持插值时）

在 setter 中调用 `update()` 触发重绘，在合适时机发射信号通知外部：

```cpp
void ProgressRing::setValue(int v) {
    if (m_value == v) return;
    m_value = v;
    update();          // 标记下一帧重绘
    valueChanged(v);   // 发射信号
}
```

`Signal<T>` 是普通的模板成员变量，直接像函数调用一样发射。无参信号使用 `Signal<>`，调用时不传参数。关于属性与信号的完整语义，参见[对象系统](./object-system.md)中的相关章节。

### 布局

控件实例化后，通过 `setGeometry()` 手动指定位置和大小；如果父控件使用自动布局，则覆写 `sizeHint()` 来声明控件的期望大小：

```cpp
Size ProgressRing::sizeHint() const {
    return Size(80, 80);
}
```

对于自身需要管理子控件布局的容器控件，在 `layoutEvent()` 中完成子控件的几何计算，或通过 `setLayout()` 挂载框架提供的布局类（如 `FlexLayout`）。详见[布局与尺寸](#布局与尺寸)章节。

## 绘制

### Painter 初始化

在控件的 `paintEvent()` 成员函数中构造 `Painter` 即可开始绘制：

```cpp
void ProgressRing::paintEvent(PaintEvent *event) {
    Painter p(this);
    // 后续所有绘制通过 p 完成
}
```

绘制坐标系以**控件左上角为原点**，向右为 $+x$，向下为 $+y$，单位为像素。`rect()` 返回当前控件的本地矩形 `(0, 0, width(), height())`，是绘制时最常用的参考区域。

如果控件通过应用层样式或 `StyleModifier` 设置了背景色等框架管理的样式属性，可以在绘制自定义内容之前先调用基类来处理这些背景：

```cpp
void ProgressRing::paintEvent(PaintEvent *event) {
    Widget::paintEvent(event);  // 先绘制框架管理的背景（如有）
    Painter p(this);
    // ...
}
```

不调用基类时，框架管理的背景样式将被忽略，控件完全由自己的 `paintEvent` 负责全部视觉呈现。

### 绘制状态

`Painter` 维护一组当前绘制状态，每次绘制调用都使用当前状态，直到下次修改。

#### 画刷（Brush）

画刷决定**填充类**方法（`fillRect`、`fillRoundedRect`、`fillPath` 等），以及**文本**使用的颜色：

```cpp
p.setBrush(Color(200, 200, 200));   // RGB 灰色
p.setBrush(Color{"#35a7ff"});       // 十六进制字符串
p.setBrush(Color::White);           // 预定义常量
p.setBrush(Color(0xff4486ff));      // ARGB 十六进制整数（0xff 为完全不透明）
```

#### 画笔（Pen）

画笔决定**描边类**方法（`drawRect`、`drawArc`、`drawLine` 等）使用的颜色和线宽：

```cpp
Pen pen(Color(64, 156, 255));
pen.setSize(6);    // 线宽 6px
p.setPen(pen);
```

#### 其他状态

```cpp
p.setFont(Font(18));     // 18px 字号，影响 drawText()
p.setOpacity(127);      // 透明度 [0, 255]，影响此后所有绘制
```

所有状态仅作用于当前 `Painter` 实例，不同控件各自构造的 `Painter` 完全独立，互不干扰。

### 基础形状

#### 矩形

```cpp
p.setBrush(Color::White);
p.fillRect(rect());                    // 填充整个控件区域
p.fillRect(Rect(10, 10, 60, 20));      // 填充指定矩形

p.fillRoundedRect(rect(), 8.0f);       // 圆角填充，圆角半径 8px
p.drawRoundedRect(rect(), 8.0f);       // 圆角描边（不填充，使用 Pen 颜色）
```

圆角半径等于宽高较小值的一半时，矩形变成胶囊形状，这在按钮和进度条中非常常见：

```cpp
float radius = min(box.width(), box.height()) * 0.5f;
p.fillRoundedRect(box, radius);
```

#### 直线

```cpp
p.drawLine(Point(0, cy), Point(width(), cy));   // 水平分隔线
```

#### 圆弧

`drawArc` 以圆心坐标和半径指定弧形，`startAngle`/`endAngle` 单位为度数，$0°$ 对应 $3$ 点钟方向，顺时针增大：

```cpp
float cx = width() / 2.0f;
float cy = height() / 2.0f;
float radius = min(cx, cy) - 4.0f;

// 绘制完整圆弧（背景圆环），从 -90°（12 点钟）绕一圈
Pen bgPen(Color(200, 200, 200));
bgPen.setWidth(6);
p.setPen(bgPen);
p.drawArc({cx, cy}, radius, -90.0f, -90.0f + 360.0f);

// 绘制进度弧（从 12 点钟顺时针到 progress 对应位置）
if (m_value > 0) {
    Pen fgPen(Color(64, 156, 255));
    fgPen.setWidth(6);
    p.setPen(fgPen);
    p.drawArc({cx, cy}, radius, -90.0f, -90.0f + 360.0f * m_value / 100.0f);
}
```

弧的视觉粗细由当前 `Pen` 的线宽决定。

### 矢量路径 `VectorPath`

对于矩形和圆弧无法描述的复杂形状，使用 `VectorPath` 构建任意轮廓，再通过 `fillPath()` 或 `drawPath()` 渲染。

```cpp
#include "gx_vectorpath.h"
```

`VectorPath` 的工作方式类似“画笔轨迹”：用 `moveTo` 落笔、`lineTo` 直线段、`arcTo` 圆弧段依次描述轮廓，最后由 `Painter` 统一渲染。

#### 直线段路径

```cpp
VectorPath path;
path.moveTo(x0, y0);   // 落笔（不绘制）
path.lineTo(x1, y1);   // 直线到 (x1, y1)
path.lineTo(x2, y2);
path.lineTo(x0, y0);   // 回到起点，形成封闭三角形

p.fillPath(path, Color(64, 156, 255)); // 填充封闭区域
```

`fillPath()` 自动将路径作为封闭区域处理，即使最后没有显式回到起点。`drawPath()` 则用当前 `Pen` 绘制路径轮廓而不填充。

#### 圆弧段路径

`arcTo` 参数为圆心、$x/y$ 半径（椭圆时两者不等）、起始角度和扫过角度（角度制，顺时针为正）：

```cpp
// 绘制水平胶囊形：左端半圆 + 右端半圆，arcTo 自动用连线衔接两段
float r  = rect.height() * 0.5f;
float x1 = rect.left() + r;
float x2 = rect.right() - r;
float y  = rect.top() + r;

VectorPath path;
path.arcTo(PointF(x1, y), r, r, 90.0f, 270.0f);    // 左端半圆（从 9 点到 3 点逆时针）
path.arcTo(PointF(x2, y), r, r, -90.0f, 90.0f);    // 右端半圆（从 3 点到 9 点逆时针）
p.fillPath(path);
```

`arcTo` 会在路径当前终点和新圆弧起点之间自动插入一条直线，因此两段圆弧首尾自然衔接，无需额外调用 `lineTo`。

#### 曲线

使用 `conicTo` 或 `cubicTo` 可以构建二次或三次贝塞尔曲线段，配合 `moveTo` 和 `lineTo` 可以描述复杂的轮廓：

```cpp
VectorPath path;
path.moveTo(x0, y0);
// 二次贝塞尔曲线，(cx, cy) 为控制点
path.conicTo(cx, cy, x1, y1);
// 三次贝塞尔曲线，(cx1, cy1) 和 (cx2, cy2) 为控制点
path.cubicTo(cx1, cy1, cx2, cy2, x2, y2);
// 使用指定画刷填充路径
p.fillPath(path, brush);
```

#### 组合路径示例

将多段指令组合，可以构建任意复杂的形状。以 `WaveSlider` 中波浪填充区域为例，路径包含顶部波形折线和底部圆角边：

```cpp
VectorPath path;
path.moveTo(leftX, waveY(leftX));
for (int i = 1; i <= sampleCount; ++i) {
    float x = leftX + (rightX - leftX) * float(i) / sampleCount;
    path.lineTo(x, waveY(x));           // 顶部波浪轮廓
}
path.lineTo(rightX, bottomEdge(rightX)); // 右侧下降
for (int i = sampleCount - 1; i >= 0; --i) {
    float x = leftX + (rightX - leftX) * float(i) / sampleCount;
    path.lineTo(x, bottomEdge(x));       // 底边（沿圆角矩形底部返回）
}
path.lineTo(leftX, waveY(leftX));        // 回到起点
p.fillPath(path);
```

### 文字

`drawText()` 在矩形范围内排列并绘制文本，文字颜色由当前 `Brush` 决定，字体由 `setFont()` 设置：

```cpp
p.setFont(Font(18));
p.setBrush(Color(50, 50, 50));
p.drawText(rect(), format("{}%", m_value), AlignCenter);
```

::: tip 格式化字符串
`format()` 是框架提供的格式化函数，语法类似 [`std::format`](https://en.cppreference.com/w/cpp/utility/format/format)，可跨平台使用。
:::

对齐标志可自由组合：

| 标志 | 含义 |
|---|---|
| `AlignLeft` | 水平左对齐 |
| `AlignHCenter` | 水平居中 |
| `AlignRight` | 水平右对齐 |
| `AlignTop` | 垂直顶对齐 |
| `AlignVCenter` | 垂直居中 |
| `AlignBottom` | 垂直底对齐 |
| `AlignCenter` | 水平 + 垂直居中（等同于 `AlignHCenter \| AlignVCenter`）|

`font()` 方法返回控件当前从样式系统继承的字体，在绘制中使用它可以使控件自动跟随应用字号变化：

```cpp
p.setFont(font());   // 使用控件继承的样式字体，而非固定字号
```

`drawText()` 还支持更复杂的文本布局，例如多行文本、自动换行等，详见 API 文档。

### 图片

`drawImage()` 将图片绘制到指定矩形内：

```cpp
Image img{"file://path/to/icon.png"};
p.drawImage(widget->rect(), img); // 将图片绘制到指定区域，不会自动缩放
```

实际使用中图片通常来自资源系统，加载方式取决于平台和打包配置。

### 完整示例

以下是 `ProgressRing` 的完整 `paintEvent`，综合运用了上述绘制能力：

```cpp
void ProgressRing::paintEvent(PaintEvent *event) {
    // 若控件有背景样式由框架管理，先调用基类
    // Widget::paintEvent(event);

    Painter p(this);

    float cx = width() / 2.0f;
    float cy = height() / 2.0f;
    float radius = min(cx, cy) - 4.0f;
    float startAngle = -90.0f;   // 从 12 点钟方向开始

    // 绘制灰色背景圆环
    Pen bgPen(Color(200, 200, 200));
    bgPen.setWidth(6);
    p.setPen(bgPen);
    p.drawArc({cx, cy}, radius, startAngle, startAngle + 360.0f);

    // 绘制彩色进度弧
    if (m_value > 0) {
        Pen fgPen(Color(64, 156, 255));
        fgPen.setWidth(6);
        p.setPen(fgPen);
        p.drawArc({cx, cy}, radius,
          startAngle, startAngle + 360.0f * m_value / 100.0f);
    }

    // 在圆环中心绘制百分比数字
    p.setFont(Font(18));
    p.setBrush(Color(50, 50, 50));
    p.drawText(rect(), format("{}%", m_value), AlignCenter);
}
```

## 布局与尺寸

覆写 `sizeHint()` 告知布局系统控件的"期望大小"。当父控件使用自动布局时，布局系统会参考这个值来分配空间：

```cpp
Size ProgressRing::sizeHint() const {
    return Size(80, 80);  // 建议显示为 80×80px
}
```

如果控件是高度随宽度变化的（例如等比缩放的图片），覆写 `heightForWidth()`：

```cpp
int AspectWidget::heightForWidth(int width) const {
    return width; // 正方形比例
}
```

对于需要手动管理子控件布局的情况，覆写 `layoutEvent()` 并在其中设置子控件的几何：

```cpp
bool ContainerWidget::layoutEvent(LayoutEvent *event) {
    // 将子控件从上往下排列
    int y = 0;
    for (auto *child : children()) {
        auto *w = dyn_cast<Widget *>(child);
        if (w && w->isVisible()) {
            w->setGeometry(0, y, width(), w->sizeHint().height());
            y += w->height();
        }
    }
    return true;
}
```

也可以使用框架提供的现成布局类（如 `FlexLayout`、`StackLayout`），通过 `setLayout(new FlexLayout())` 挂载。

::: tip 使用现成的布局类
除非你要制作特殊布局的容器控件，否则建议使用框架提供的布局类来管理子控件的布局，这种情况下不需要覆写 `layoutEvent()`。

实现一个完整的布局算法是比较复杂的，需要处理 `sizeHint()` 等多个方面的交互，并且还要考虑性能优化。
:::

## 动画

框架提供了三类动画机制：**样式动画**、**属性动画**和 **`ValueAnimation`**。样式动画和属性动画主要用于**应用层**（即使用控件的一侧），而在实现自定义控件时，最常直接用到的是 `ValueAnimation`。

### ValueAnimation

`ValueAnimation<T>` 是一个对任意类型 `T` 进行插值的动画类。每一帧它会根据当前进度计算出插值结果，并通过 `value` 信号发射出来。你只需将信号连接到自己的更新逻辑即可：

```cpp
#include "gx_valueanimation.h"

// 在控件成员中声明动画对象，一般使用指针以便在需要时动态创建和销毁
ValueAnimation<int> *m_animation = nullptr;
```

```cpp
// 在某处初始化并启动
m_animation = new ValueAnimation<int>;
m_animation->setValueLimits(0, 100);  // 从 0 插值到 100
m_animation->setDuration(800);        // 800 毫秒
m_animation->value.connect(this, &MyWidget::onAnimationValue);
m_animation->start();

// 帧回调：接收每帧计算出的插值
void MyWidget::onAnimationValue(int v) {
    m_currentValue = v;
    update();  // 触发重绘
}
```

动画结束时发射 `finished` 信号。如果不需要手动管理生命周期，可以用 `DeleteOnStop` 策略让动画在播放完毕后自动销毁：

```cpp
// 动画对象不需要外部访问，直接 new 后自动销毁
auto *anim = new ValueAnimation<int>;
anim->setValueLimits(0, 100);
anim->setDuration(500);
anim->value.connect(this, &MyWidget::onValue);
anim->start(AbstractAnimation::DeleteOnStop);  // 播完自动 delete
```

框架内置了以下类型的插值支持：`int`、`float`（以及其他数值类型）、`Color`、`Point`、`Pen`、`Brush`、`Length`、`Transform` 等。

其他常用配置：

```cpp
// 无限循环播放
anim->setRepeat(AbstractAnimation::Infinity);

// 来回交替播放（正放→倒放→正放……）
anim->setDirection(AbstractAnimation::Alternate);

// 设置缓动曲线
#include "gx_easecurve.h"
anim->setEaseCurve(easing::make_curve<easing::Ease>());
```

### 样式动画与属性动画

**样式动画**（`StyleAnimation`）通过类似 CSS transition 的方式定义过渡效果，当控件的样式状态切换时由框架自动播放，主要在应用层组件的样式配置中使用。

**属性动画**（`PropertyAnimation`）通过属性名字符串驱动 `GX_PROPERTY` 声明的属性，常用于应用层对控件属性做动画：

```cpp
#include "gx_propertyanimation.h"

auto *anim = new PropertyAnimation(widget, "value");
anim->setStartValue(Variant{0});
anim->setStopValue(Variant{100});
anim->setDuration(1000);
anim->start(AbstractAnimation::DeleteOnStop);
```

在实现控件本身时，通常不需要使用属性动画，因为 `ValueAnimation` 更直接，也没有按名称查找属性的开销。

## 文本显示控件

实现带有文本内容的控件时，除了基本的绘制逻辑外，还需要处理文本测量、布局缓存、样式联动等问题。`Label` 是框架最典型的文本控件，其实现可以作为类似控件的参考模板。

### 使用 `updateLayout()`

`update()` 仅标记控件需要**重绘**，不影响布局系统。而文本内容变化时，控件的期望大小（`sizeHint()` 返回值）通常也会随之改变，此时必须同时调用 `updateLayout()` 来触发父控件的布局重新计算：

```cpp
void MyTextWidget::setText(const String &text) {
    if (m_text == text)
        return;
    m_text = text;
    update();        // 触发重绘
    updateLayout();  // 通知父布局重新计算（因为 sizeHint 变了）
}
```

仅调用 `update()` 的后果是：文本内容已更新，但控件大小仍是旧文本计算出来的值，排版会错乱。

### 文本测量与 `sizeHint()`

`FontMetrics` 是文本测量的核心工具，用它来实现 `sizeHint()` 和 `heightForWidth()`：

```cpp
#include "gx_fontmetrics.h"

Size MyTextWidget::sizeHint() const {
    if (m_text.empty())
        return Size{0, int(font().pixelSize() * 1.2f)};
    FontMetrics fm(font());
    // 单行文本：直接测量宽度
    return Size{fm.width(m_text), int(font().pixelSize() * 1.2f)};
}
```

对于支持自动换行的多行文本，还需要实现 `heightForWidth()`，告知布局系统在给定宽度下控件的高度：

```cpp
int MyTextWidget::heightForWidth(int width) const {
    if (width == 0) return 0;
    FontMetrics fm(font());
    float lineHeight = font().pixelSize() * 1.2f;
    // boundingRect 计算给定宽度下文本的实际边界
    return fm.boundingRect(m_text, width, 1024 * 1024, 0, 0, lineHeight).height();
}
```

如果控件是严格的单行（不随宽度换行），`heightForWidth()` 返回 `-1` 表示不依赖宽度：

```cpp
int SingleLineWidget::heightForWidth(int) const { return -1; }
```

### 响应样式与尺寸变化

字体、颜色等样式属性变化时，文本的测量结果也会改变。覆写 `styleEvent()` 来响应样式变化，调用基类实现后刷新与样式相关的缓存，再触发布局更新：

```cpp
void MyTextWidget::styleEvent(StyleEvent *event) {
  // 必须先调用基类，它会更新内部样式数据
    Widget::styleEvent(event);
    // 字体等样式改变后，sizeHint 的返回值可能变化
    updateLayout();
}
```

同样，控件尺寸变化时如果有依赖宽度的文本换行计算，需要在 `resizeEvent()` 中触发更新：

```cpp
void MyTextWidget::resizeEvent(ResizeEvent *event) {
    Widget::resizeEvent(event); // 调用基类
    update();                   // 尺寸变化后重绘内容
}
```

::: important
`styleEvent()`、`resizeEvent()` 等事件处理函数的基类实现通常有不可省略的副作用，**必须调用**。调用时机取决于你的逻辑需要：大多数情况下先调用基类，再执行自己的逻辑。
:::

### 覆写 `event()`

将 `StyleEvent`、`ResizeEvent` 等需要处理的事件类型全部列入 `EventDispatch` 的模板参数，以获得编译期检查：

```cpp
bool MyTextWidget::event(Event *event) {
    return EventDispatch<Widget,
        PaintEvent, ResizeEvent, StyleEvent>{}(this, event);
}
```

### 流式布局与行内元素

`setFlowLayout(true)` 将**容器控件**设置为流式布局（flow layout）模式，效果类似 CSS 的块级流，框架会自动将子元素按行排布，无需通过 `setLayout()` 创建独立的布局对象。`Label` 在构造函数中就启用了这一模式，从而使自己可以作为 `SpanLabel` 容器（内嵌多个带不同样式的子标签）：

```cpp
Label::Label(Widget *parent) : Widget(parent) {
    setFlowLayout(true);
}
```

`setInlineWidget(true)` 则是针对**子元素**的设置，将该控件标记为行内（inline）元素，使其像文字一样嵌入父容器的文本流中参与排版。例如，在富文本行内嵌入一个图标控件：

```cpp
auto *icon = new ImageBox(label);
// 作为行内元素与文字混排。ImageBox 默认已经是行内的了，这里只是示例说明。
icon->setInlineWidget(true);
```

当 `Label` 作为容纳行内子元素的 `SpanLabel` 容器使用时，布局系统会自动协调 `Label` 自身的文本测量逻辑和作为容器时对子元素的排布。两者共用同一套布局机制，开发者不需要手动干预这一过程。

## AbstractScrollArea 与可滚动控件

当控件需要滚动行为时，不必从头实现手势识别、惯性滚动和回弹效果，直接继承 `AbstractScrollArea` 即可获得这些能力。框架内置的 `ScrollArea`（列表滚动）和 `TextField`（单行文本输入）都基于它实现。

### 基本结构

继承 `AbstractScrollArea` 的控件遵循一个固定的结构：控件本身是"视口"，内部有一个**内容控件**（content widget）负责承载实际内容，滚动时移动的是内容控件而非视口本身。

构造函数中完成初始化：

```cpp
// myticker.h
#include "gx_abstractscorllarea.h"

class MyTicker : public AbstractScrollArea {
    GX_OBJECT
public:
    explicit MyTicker(Widget *parent = nullptr);
    bool event(Event *event) override;

protected:
    bool layoutEvent(LayoutEvent *event);
    friend struct EventTraits<MyTicker>;
};
```

```cpp
// myticker.cpp
#include "myticker.h"
#include "gx_widgetevent.h"

MyTicker::MyTicker(Widget *parent) : AbstractScrollArea(parent) {
    setDirection(Horizontal);     // 水平滚动
    setDamping(5);                // 调整阻尼（数值越大摩擦越强）

    auto *content = new Widget;   // 创建内容控件
    setContentWidget(content);
}

bool MyTicker::event(Event *event) {
    return EventDispatch<AbstractScrollArea, LayoutEvent>{}(this, event);
}
```

将 `EventDispatch` 的基类参数设为 `AbstractScrollArea`（而非 `Widget`），可以让未被当前类处理的事件（手势、滚轮、resize 等）自动回退到 `AbstractScrollArea` 的实现，从而保留完整的滚动行为。

### 配置滚动参数

```cpp
setDirection(Vertical);          // 垂直滚动（默认）
setDirection(Horizontal);        // 水平滚动
setDamping(3);                   // 较低阻尼：惯性更强，滑行更远
setDamping(20);                  // 较高阻尼：惯性较弱，接近无惯性
setScrollBar(true);              // 显示滚动条
setBouncesPolicy(SnapType::SnapEdge);  // 边缘回弹策略
```

`AbstractScrollArea` 还提供了 `scrollTo(x, y, behavior)` 来以编程方式控制滚动位置，`behavior` 为 `Instant`（立即跳转）或 `Smooth`（带动画）。

::: tip 惯性阻尼
对于 `TextField` 这类需要精确控制滚动位置的控件，通常会设置较高的阻尼值以弱化惯性；而对于 `ScrollArea` 这类以浏览为主的控件，则可以设置较低的阻尼以获得更流畅的滚动体验。

阻尼不要设置得太低，否则超长距离的滚动可能导致内容缓存失效，出现卡顿。
:::

### 在事件分发中调用基类

有时需要对某事件做额外处理，再将控制权交给 `AbstractScrollArea` 的默认实现。典型的做法是在处理函数中直接调用基类方法：

```cpp
// TextField 的做法：只在有文字时才转发手势给滚动区
bool TextField::gestureEvent(GestureEvent *event) {
    if (text().empty()) // 无文字时直接忽略
        return false;
    // 其余情况交给基类滚动逻辑
    return AbstractScrollArea::gestureEvent(event);
}
```

这种模式下，`EventDispatch` 的基类参数使用 `Widget`，当前类自行决定何时调用哪个基类方法：

```cpp
bool TextField::event(Event *event) {
    // 用 Widget 作为基类，完全由自己控制 AbstractScrollArea 行为的调用时机
    return EventDispatch<Widget, GestureEvent, ResizeEvent>{}(this, event);
}
```

### 内容控件的事件过滤

内容控件负责布局和承载子控件，但它的某些事件（如布局请求）有时需要容器来拦截和自定义处理。通过 `setEventFilter(this)` 将容器注册为内容控件的事件过滤器，然后覆写 `eventFilter()` 处理感兴趣的事件：

```cpp
// 在构造函数中注册
content->setEventFilter(this);

// 拦截内容控件的布局请求
bool MyTicker::eventFilter(Object *receiver, Event *e) {
    if (receiver == contentWidget() && e->type() == Event::Layout) {
        auto *lv = static_cast<LayoutEvent *>(e);
        if (lv->isLayoutRequest()) {
            // 自定义布局逻辑……
            return true; // 返回 true 阻止事件继续传递
        }
    }
    // 其余情况交给基类
    return AbstractScrollArea::eventFilter(receiver, e);
}
```

::: tip
未被处理的事件应回退给 `AbstractScrollArea::eventFilter()`，它负责与滚动条等内部机制的交互。
:::

### 设置行内控件

调用 `setInlineWidget(true)` 可以让控件参与行内布局（inline layout），适合嵌入文本流中的场景，`TextField` 就是这样处理使其可以像文字一样嵌入行内。

### ScrollArea 及派生类

`ScrollArea` 是 `AbstractScrollArea` 的一个派生类，在滚动基础上增加了**索引导航**（`index()`/`setIndex()`）、**吸附模式**（snap）和**视觉特效**（visual effect）等能力，是列表、走马灯等场景的首选基类。`Swiper` 则在 `ScrollArea` 之上进一步增加了分页（`pageLength`）和指示点（indicator）等功能，适合轮播图等模式。

这些类通常**不需要进一步派生**，大多数定制需求可以通过配置参数和挂载周边设施来实现，而无需子类化。

#### 视觉特效 VisualEffect

`ScrollArea` 支持通过 `setVisualEffect()` 挂载一个 `VisualEffect` 对象，在绘制每个子控件之前对其施加透明度、缩放、位移等视觉变换，从而实现滚动时的动态效果。框架内置了以下几种效果：

| 类名 | 效果 |
|---|---|
| `FisheyeVisualEffect` | 鱼眼效果，中心元素放大，边缘缩小 |
| `FadeVisualEffect` | 边缘渐隐，距离视口中心越远透明度越低 |
| `CollapseVisualEffect` | 折叠效果，元素向上（或向下）边缘聚拢缩小 |
| `BlendVisualEffect` | 在两种效果之间按进度插值过渡 |

```cpp
#include "gx_visualeffect.h"

scrollArea->setVisualEffect(make_shared<FisheyeVisualEffect>());
```

如需自定义效果，继承 `VisualEffect` 并实现 `resolve()` 方法。`resolve()` 接收目标子控件、视口矩形和子控件中心点，返回一个 `PaintModifier`，其中可设置 `opacity`、`scale`、`translate` 等属性。

有关 `ScrollArea` 和 `Swiper` 的完整参数说明，以及如何实现自定义 `VisualEffect`，将在[滚动区域](./scroll-area.md)中单独介绍。

## 控件树与生命周期

在 C++ 中创建控件时，通过构造函数的 `parent` 参数建立父子关系：

```cpp
// parent 销毁时，child 也会随之销毁
auto *parent = new Widget(window);
auto *child  = new ProgressRing(parent);
child->setGeometry(10, 10, 80, 80);
```

无论是手动 `delete` 父控件，还是框架在应用退出时清理控件树，所有子控件都会被自动销毁。你不需要在析构函数中 `delete` 子控件。

如果需要延迟销毁（例如在事件处理函数内部），可以使用 `deleteLater()`，它会在当前事件处理完成后再销毁对象，避免"在回调中销毁自己"这类问题。

在响应式框架中，控件树由组件框架维护，定制开发时只需要[注册控件类](./widget-export.md)。


