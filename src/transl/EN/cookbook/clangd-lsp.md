# Clangd Configuration

When developing firmware using a cross-compilation toolchain such as `arm-none-eabi-gcc` along with a build system like CMake, you can configure the Clangd language server to enhance your development experience. Specifically, you will benefit from the following features:
- Accurate navigation to declarations or definitions based on the actual project structure;
- Viewing API documentation (documentation comments written in Doxygen formats such as `/**` and `//!`);
- Support for code formatting rules defined by `.clang-format`;
- Real-time static analysis or error checking without the need for compilation;
- Code suggestions and completion as you type;
- Finding references, code refactoring, and more.

## Preparation

First, you need an editor that supports the LSP (Language Server Protocol), such as Visual Studio Code, and then install clangd and its related extensions. If you need to install clangd manually, you can download a suitable version from [LLVM](https://github.com/llvm/llvm-project/releases) or use your operating system's package manager.

After installing the necessary extensions, clangd may work out-of-the-box for simple native host projects, but further configuration is required in complex cross-compilation environments.

## Cross-Compilation Environment Configuration

### CMake Options

If you use CMake as your build system, you need to enable the `CMAKE_EXPORT_COMPILE_COMMANDS` option. You can do this via a command-line argument:
``` bash
cmake .. -DCMAKE_EXPORT_COMPILE_COMMANDS=ON # Command-line argument during the CMake configuration stage
```
If using command-line arguments is inconvenient, you can also define this variable in any `CMakeLists.txt` file:
``` cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```
Then, when you configure or build the project using CMake, a `compile_commands.json` file will be generated in the output directory, which will be used by clangd.

### Clangd Configuration

After configuring CMake and generating `compile_commands.json`, clangd may work partially, but you are likely to encounter the following issues:
- `compile_commands.json` is located deep within the directory hierarchy, so clangd cannot find it;
- clangd cannot find standard headers suitable for the cross-compilation environment, such as `stdint.h`.

To resolve these issues, you first need to create a `.clangd` file in the root directory of your project (i.e., the directory opened by your editor, usually where the `.git` folder is located). This is a YAML file; populate it with the following content:
``` yaml
CompileFlags:
  CompilationDatabase: "Relative path to the directory containing compile_commands.json"
  Add: 
    - -resource-dir=C:/gcc-arm-none-eabi-9-2020-q2/arm-none-eabi/include
    - -IC:/gcc-arm-none-eabi-9-2020-q2/arm-none-eabi/include
    - -IC:/gcc-arm-none-eabi-9-2020-q2/arm-none-eabi/include/c++/9.3.1
    - -IC:/gcc-arm-none-eabi-9-2020-q2/arm-none-eabi/include/c++/9.3.1/arm-none-eabi
    - -IC:/gcc-arm-none-eabi-9-2020-q2/lib/gcc/arm-none-eabi/9.3.1/include
  Remove:
    - -fno-reorder-functions
```
Please modify the file paths according to your actual setup. Next, add the following command-line option to clangd's startup arguments:
``` bash
--query-driver=C:/gcc-arm-none-eabi-9-2020-q2/bin/arm-none-eabi-g++.exe # Fill in the path according to your actual setup
```
Then restart the clangd language server, and it should work properly.

In VS Code, you can add arguments via `clangd.arguments` in the project's `.vscode/settings.json`:
``` json
{
  "clangd.arguments": [
    "--query-driver=C:/gcc-arm-none-eabi-9-2020-q2/bin/arm-none-eabi-g++.exe"
  ]
}
```