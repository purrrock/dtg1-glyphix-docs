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
