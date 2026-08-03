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
