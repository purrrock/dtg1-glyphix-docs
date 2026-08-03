# SDK Project Configuration

Glyphix is distributed to device manufacturers in the form of pre-compiled libraries. This article describes how to configure the build environment in an SDK project to develop Native Modules, Native Widgets, or platform adaptation code on top of it.

### Prerequisites

Before you begin, ensure that the following are installed:
- CMake 3.14 or higher
- A C++ compiler supporting C++14 (GCC, Clang, or MSVC)
- The Glyphix meta-object compiler `meta` (must match the SDK version; see below for how to obtain it)
- A cross-compilation toolchain (if building for embedded targets)

::: tip System Requirements
- The MSVC toolchain requires Visual Studio 2022 or higher.
- For Linux, a distribution with a desktop environment, such as Ubuntu 22.04 or higher, is recommended.
- Ubuntu 20.04 is not recommended because its package versions are generally too old, frequently requiring manual installation of newer software.
- Environments without a graphical interface, such as WSL or Docker, will not be able to run simulators and GUI examples.
- Currently, the host environment only provides Linux pre-compiled libraries; pre-compiled libraries for Windows and macOS are not yet ready.
:::

## SDK Package Structure

The extracted SDK contains the following directories:

```
glyphix-sdk/
├── libs/
│   └── <target-triple>/       # Pre-compiled libraries organized by target triple
│       ├── include/           # Glyphix header files (gx_*.h)
│       └── lib/               # Static libraries (libglyphix-core.a, etc.)
├── cmake/
│   ├── GlyphixSDK.cmake       # Main SDK configuration script
│   ├── meta.cmake             # Meta-object compiler integration (glyphix_add_meta_objects)
│   ├── cross-compile.cmake    # Cross-compilation toolchain loading
│   ├── arch/                  # Compilation parameters for various architectures (mips-linux-gnu, cortex-m33, etc.)
│   └── toolchain/             # CMake toolchain files for various toolchains
├── wrapper/                   # Platform adaptation layer (host implementations for network, filesystem, etc.)
├── app/                       # Example application entries (emulator, async, etc.)
└── vendor/                    # Third-party dependency libraries
```

### `libs/<target-triple>/`

The SDK's pre-compiled libraries are distinguished by platform using **target triples** as directory names, for example:

- `x86_64-linux-gnu/`: 64-bit Linux host development/simulation
- `mips-linux-gnu/`: MIPS Linux embedded target
- `cortex_m55-none-gnu/`: Cortex-M55 bare-metal target

The `include/` directory contains all Glyphix public header files, all prefixed with `gx_`. The `lib/` directory contains static libraries, with core libraries including:

| Library File | Description |
|:---|:---|
| `libglyphix-core.a` | Core framework (object system, widget tree, events, etc.) |
| `libglyphix-widgets.a` | Built-in widget library |
| `libglyphix-reactive.a` | Reactive framework (JavaScript bridge layer) |
| `libglyphix-platform.a` | Platform abstraction layer interface |
| `libglyphix-service.a` | System service layer |

::: tip Pre-compiled Vendor Libraries
The SDK distribution package also contains some pre-compiled third-party libraries, such as `libfreetype.a`. For convenience, we do not distribute the source code of these libraries directly, but you can choose to build them directly from source instead of using the pre-compiled libraries.
:::

## Getting Started

### Configuring the Meta-Object Compiler

The `meta` meta-object compiler is distributed separately from the SDK as an independent archive. Extracting it yields two directories: `bin/` and `lib/`. **Both must be kept in the same directory**, as the `meta` executable depends on the runtime libraries in `lib/`.

On Linux and macOS, it is recommended to extract it to `/usr/local` so that `meta` is automatically in your `PATH`:

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

Alternatively, you can extract it to any directory and add its `bin/` directory to your `PATH`. Once completed, verify that it is available with the following command:

```bash
meta --version
```

If you prefer not to modify your `PATH`, you can explicitly specify the full path to the executable during CMake configuration using `-DGX_META=/path/to/bin/meta`.

## Configuring CMakeLists.txt

### Minimal Configuration

::: tip
The CMake configuration introduced in this section resembles the standard example template of the Glyphix SDK project, which you can refer to directly from the SDK source files.
:::

Below is a minimal runnable `CMakeLists.txt` demonstrating the standard configuration skeleton for a project:

```cmake
cmake_minimum_required(VERSION 3.14)

# Must be loaded before project() so that the toolchain is in place when project() detects compilers
include(cmake/cross-compile.cmake)

project(my_glyphix_app)
set(CMAKE_CXX_STANDARD 14)

# Load the Glyphix SDK (sets header paths, link directories, and the glyphix::sdk target)
include(cmake/GlyphixSDK.cmake)

add_subdirectory(vendor)  # Third-party dependencies (if any)
add_subdirectory(src)     # Your source code
```

In `src/CMakeLists.txt`, create a target and link the SDK:

```cmake
add_executable(my_app
  main.cpp
  my_module.cpp
  my_widget.cpp
)

# Link the Glyphix SDK
target_link_libraries(my_app PRIVATE glyphix::sdk)

# Generate metadata for header files containing GX_OBJECT
glyphix_add_meta_objects(my_app
  my_module.h
  my_widget.h
)
```

### Registering Meta Objects (`glyphix_add_meta_objects`)

As mentioned in the [Object System](./object-system) documentation, any class declaring `GX_OBJECT` must be registered with the build system so that the meta-object compiler can generate the corresponding `*_meta.cpp` file for it. `glyphix_add_meta_objects()` is the CMake function that accomplishes this step:

```cmake
glyphix_add_meta_objects(<target> [header1.h header2.h ...])
```

It accepts the target name and a set of **header file** paths as arguments. For each header file, the `meta` tool generates a corresponding `*_meta.cpp` in the `meta/` subdirectory of the build directory and automatically adds it to the target's source file list for compilation.

**Example:** Suppose your project has the following structure:

```
src/
├── CMakeLists.txt
├── main.cpp
├── sensors/
│   ├── step_counter.h       # Contains GX_OBJECT
│   └── step_counter.cpp
└── widgets/
    ├── activity_ring.h      # Contains GX_OBJECT
    └── activity_ring.cpp
```

The corresponding `CMakeLists.txt`:

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

::: tip Pass Header Files Only, Not .cpp Files
`glyphix_add_meta_objects()` only requires **header files** (`.h`) containing `GX_OBJECT` declarations. The meta-object compiler reads the macro declarations in the header files to generate code and does not need to parse implementation files. Conversely, `.cpp` files must not define classes containing `GX_OBJECT`.
:::

::: warning Do Not Omit Registration
If a class declares `GX_OBJECT` but is not registered via `glyphix_add_meta_objects()`, it will result in a **linker error** (symbols such as `staticMetaObject` cannot be found). Remember to update `CMakeLists.txt` whenever you add a new header file containing `GX_OBJECT`.
:::

### The `glyphix::sdk` Interface Target

`GlyphixSDK.cmake` defines the `glyphix::sdk` CMake interface library target, which encapsulates all linking dependencies of the SDK. In your `CMakeLists.txt`, you only need to link this single target:

```cmake
target_link_libraries(my_target PRIVATE glyphix::sdk)
```

Internally, this is equivalent to:

```cmake
# Pseudo-code — actually managed automatically by GlyphixSDK.cmake
target_include_directories(... ${GLYPHIX_INCLUDE_DIRS} wrapper/include)
target_link_libraries(... -Wl,--start-group ${glyphix-*.a} glyphix-wrapper -Wl,--end-group)
target_link_libraries(... m pthread dl)  # UNIX system libraries
```

Wrapping static libraries with `-Wl,--start-group ... -Wl,--end-group` is done to resolve circular dependency linking issues between static libraries on embedded platforms.

::: tip Link Order Issues
If your project contains its own static libraries (e.g., `add_library(my_module STATIC ...)`), they should be linked **inside** `glyphix::sdk`, otherwise the scope of `--start-group` will not cover them, potentially causing linker errors. The method is to append your static library path after the `GLYPHIX_LIBS` variable in `GlyphixSDK.cmake` is defined and before the `glyphix-sdk` target is created, or directly have the final executable link both `my_module` and `glyphix::sdk` and manually specify `--start-group`.
:::

## Host Build

Host builds are used to run Glyphix example programs on your development machine, allowing you to quickly verify widget and module logic without connecting hardware.

```bash
mkdir build && cd build
cmake -G Ninja ..
cmake --build .
```

The `app/` directory of the SDK contains multiple examples, with each subdirectory corresponding to an independent executable target. For example:

| Subdirectory | Build Artifact | Description |
|:---|:---|:---|
| `app/emulator/` | `demo` | Simulator with GUI, depends on the MiniFB window backend |
| `app/async/` | `async-demo` | Headless asynchronous service example, demonstrating Native Modules and asynchronous callbacks |

`GlyphixSDK.cmake` automatically detects the host compiler's target triple (via `gcc -dumpmachine` or `clang -dumpmachine`) and uses it as a key to look up the corresponding pre-compiled libraries in the `libs/` directory. For example, on an x86_64 Linux development machine, it automatically resolves to `libs/x86_64-linux-gnu/`.

If the automatically detected target triple does not match the actual library directory, you can specify it manually:

```bash
cmake -G Ninja -DTARGET_TRIPLE=x86_64-linux-gnu ..
```

If you only need to build a specific example, you can specify the target name:

```bash
cmake --build . --target demo
cmake --build . --target async-demo
```

## CMake Cross-Compilation

For embedded targets, you need to specify the target architecture using the `-DARCH` parameter. The SDK presets the following architecture configurations:

| `-DARCH` Value | Target Platform | Toolchain Prefix |
|:---:|:---:|:---:|
| `mips-linux-gnu` | MIPS Linux | `mips-linux-gnu-` |
| `cortex_m33-gnu` | ARM Cortex-M33 (GNU) | `arm-none-eabi-` |
| `cortex_m7-gnu` | ARM Cortex-M7 (GNU) | `arm-none-eabi-` |

### MIPS Linux Example

```bash
export MIPS_TOOLCHAIN_DIR="/opt/mips-gcc720-glibc229"

mkdir build-mips && cd build-mips
cmake -G Ninja .. \
  -DARCH=mips-linux-gnu \
  -DMIPS_TOOLCHAIN_DIR="$MIPS_TOOLCHAIN_DIR" \
  -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

If the toolchain is already in your `PATH` (i.e., `mips-linux-gnu-gcc` can be invoked directly), `-DMIPS_TOOLCHAIN_DIR` can be omitted, and CMake will locate it automatically.

### ARM Cortex-M Example

```bash
mkdir build-cm33 && cd build-cm33
cmake -G Ninja .. \
  -DARCH=cortex_m33-gnu \
  -DARM_TOOLCHAIN_DIR="/opt/arm-none-eabi-gcc" \
  -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

During cross-compilation, `GlyphixSDK.cmake` does not attempt to automatically detect the target triple—architecture files (such as `cmake/arch/cortex_m33-gnu.cmake`) directly set `TARGET_TRIPLE`, pointing to the correct library directory.

### Supported Target Architectures

The SDK provides pre-compiled libraries only for the architectures listed in the table above. If your target platform is not among them, you need to contact Glyphix to obtain an SDK package for the corresponding architecture, and you cannot add support on top of the existing SDK by yourself.

## Other Build Systems

While the SDK uses CMake as its primary build system, Glyphix also provides support for other build systems to partner manufacturers. This typically involves just importing the pre-built SDK libraries and header files, and adding porting layer source files.

### Project Limitations

This approach is suitable for projects that only require standard SDK features. Once custom widgets, Native Modules, or other capabilities are needed, you must introduce the `meta` meta-object compiler to generate the necessary binding code. CMake is currently the only supported build system for this.

Several alternative solutions are available:
1. Build custom code using the SDK CMake project, and then link the generated libraries into your main project.
2. Build custom code using the SDK CMake project, and then include the generated source files (`*_meta.cpp`) into your main project.
3. Call the `meta` tool directly within your build system to generate binding code.

Among these, the Glyphix SDK itself is built using Method 1. However, this is not suitable for downstream manufacturers' internal development workflows because it requires maintaining a separate project outside of the main firmware project and linking the generated binary libraries back to the main project, which creates severe version management issues.

Method 3 is also generally undesirable because manufacturers typically do not want to introduce an external tool into their main project's build system.

### Recommended Approach

Therefore, Method 2 is recommended. This approach copies the source code; although it requires manual operations, it is easy to audit and integrate into existing build pipelines. You can build custom code in the SDK's CMake project to generate `*_meta.cpp` files, then copy these files into your main project and compile them within your main project's build system.

Another limitation of this approach is that the custom source files must be able to successfully build within the SDK project environment. Specifically, this requires them to be buildable independently of the main project, which includes:
- Include paths and preprocessor definitions must be set correctly, and the header files of custom components must not include main-project-specific header files.
- It is best if the `.cpp` files of custom components can also compile successfully; while this does not affect the generation of `*_meta.cpp` files, it facilitates rapid iteration and debugging in the host environment.

::: tip
This is generally not an issue for most [custom widgets](widget.md). It may be a bit more cumbersome for [Native Modules](native-module.md), and care should be taken: header files declaring `GX_OBJECT` should not include main-project-specific header files.
:::