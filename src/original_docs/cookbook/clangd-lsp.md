# Clangd 配置

在用交叉编译工具链开发固件时，如果使用 arm-none-eabi-gcc 工具链，并且使用 CMake 等构建系统时，可以配置 Clangd 语言服务器以提升开发体验。具体而言你将得到这些好处：
- 基于实际项目结构准确地跳转到声明或者定义；
- 查看 API 文档（使用 `/**`、`//!` 等 Doxygen 格式的注释写的文档注释）；
- 支持 `.clange-format` 定义的的代码格式化规则；
- 无需编译，实时的静态检查或者错误检查；
- 输入时的代码提示和补全；
- 查找用法，代码重构等。

## 准备工作

首先要使用一种支持 LSP（语言服务器协议）的编辑器，如 Visual Studio Code，然后安装 clangd 及相关插件。如果需要手动安装 clangd，那么可以下载 [LLVM](https://github.com/llvm/llvm-project/releases) 的合适版本，或者使用操作系统的包管理器进行安装。

在安装必要的插件之后，clangd 可能不需要任何配置就可以在简单的主机项目中使用，但是在复杂的交叉编译环境中还需要进一步配置。

## 交叉编译环境配置

### CMake 选项

如果使用 CMake 作为构建系统，那么要打开 `CMAKE_EXPORT_COMPILE_COMMANDS` 选项，你可以通过命令行参数做到：
``` bash
cmake .. -DCMAKE_EXPORT_COMPILE_COMMANDS=ON # CMake 配置阶段的命令行参数
```
如果不方便使用命令行参数，也可以在任意一个 `CMakeLists.txt` 文件中定义这个变量：
``` cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```
然后在使用 CMake 配置或者构建项目时会在输出目录生成一个 `compile_commands.json` 文件，这个文件将会供 clangd 使用。

### Clangd 配置

在配置好 CMake 并生成 `compile_commands.json` 之后，clangd 可能可以部分工作，但是很可能遇到如下问题：
- `compile_commands.json` 处在很深的目录层级，clangd 找不到它；
- clangd 找不到适用于交叉编译环境的标准头文件，如 `stdint.h` 等。

要解决这几个问题，首先要在项目的根目录（也就是编辑器所打开的目录，通常是 `.git` 文件夹所在的目录）创建一个 `.clangd` 文件，它是一个 YAML 文件，并填写内容如下：
``` yaml
CompileFlags:
  CompilationDatabase: "包含 compile_commands.json 的目录的相对路径"
  Add: 
    - -resource-dir=C:/gcc-arm-none-eabi-9-2020-q2/arm-none-eabi/include
    - -IC:/gcc-arm-none-eabi-9-2020-q2/arm-none-eabi/include
    - -IC:/gcc-arm-none-eabi-9-2020-q2/arm-none-eabi/include/c++/9.3.1
    - -IC:/gcc-arm-none-eabi-9-2020-q2/arm-none-eabi/include/c++/9.3.1/arm-none-eabi
    - -IC:/gcc-arm-none-eabi-9-2020-q2/lib/gcc/arm-none-eabi/9.3.1/include
  Remove:
    - -fno-reorder-functions
```
请根据实际情况修改文件路径。然后在 clangd 的启动参数中添加以下命令行选项：
``` bash
--query-driver=C:/gcc-arm-none-eabi-9-2020-q2/bin/arm-none-eabi-g++.exe # 路径根据实际情况填写
```
然后重启语言 clangd 应该就可以正常工作了。

vscode 可以在项目的 `.vscode/settings.json` 中通过 `clangd.arguments` 来添加参数：
``` json
{
  "clangd.arguments": [
    "--query-driver=C:/gcc-arm-none-eabi-9-2020-q2/bin/arm-none-eabi-g++.exe"
  ]
}
```
