# Clangd configuration


When developing firmware with a cross-compilation tool chain, if you use the arm-none-eabi-gcc tool chain, and when using a build system such as CMake, you can configure the Clangd language server to improve the development experience. Specifically you will get these benefits:
- Accurately jump to declaration or definition based on actual project structure;
- View the API documentation (documentation comments written using `/**`, `//!` and other Doxygen format comments);
- Support code formatting rules defined by `.clange-format`;
- No compilation required, real-time static checking or error checking;
- Code prompts and completion during input;
- Find usage, code refactoring, and more.


## Preparation


Start by using an editor that supports LSP (Language Server Protocol), such as Visual Studio Code, and then install clangd and related plugins. If you need to install clangd manually, you can download the appropriate version of [LLVM](https://github.com/llvm/llvm-project/releases) or install it using your operating system's package manager.


After installing the necessary plugins, clangd may be able to be used in simple host projects without any configuration, but further configuration will be required in complex cross-compilation environments.


## Cross-compilation environment configuration


### CMake options


If using CMake as your build system, then to turn on the `CMAKE_EXPORT_COMPILE_COMMANDS` option you can do this via the command line argument:
``` bash
cmake .. -DCMAKE_EXPORT_COMPILE_COMMANDS=ON # CMake 配置阶段的命令行参数
```
If it is not convenient to use command line parameters, you can also define this variable in any `CMakeLists.txt` file:
``` cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```
Then when using CMake to configure or build the project, a `compile_commands.json` file will be generated in the output directory, which will be used by clangd.


### Clangd configuration


After configuring CMake and generating `compile_commands.json`, clangd may work partially, but you may encounter the following problems:
- `compile_commands.json` is located very deep in the directory hierarchy and clangd cannot find it;
- clangd cannot find standard header files suitable for cross-compilation environments, such as `stdint.h` etc.


To solve these problems, first create a `.clangd` file in the root directory of the project (that is, the directory opened by the editor, usually the directory where the `.git` folder is located). It is a YAML file and fill in the following content:
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
Please modify the file path according to the actual situation. Then add the following command line options to clangd's startup arguments:
``` bash
--query-driver=C:/gcc-arm-none-eabi-9-2020-q2/bin/arm-none-eabi-g++.exe # 路径根据实际情况填写
```
Then restart the language clangd and it should work normally.


vscode can add parameters through `clangd.arguments` in `.vscode/settings.json` of the project:
``` json
{
  "clangd.arguments": [
    "--query-driver=C:/gcc-arm-none-eabi-9-2020-q2/bin/arm-none-eabi-g++.exe"
  ]
}
```