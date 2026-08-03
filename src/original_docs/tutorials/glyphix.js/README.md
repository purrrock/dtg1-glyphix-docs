---
icon: package-variant-closed
---
# Glyphix.js 打包工具

glyphix.js 是 Glyphix 应用的打包工具，它包含一个名为 `gx` 的命令行工具，可以用来创建、构建和运行 Glyphix 应用。该工具还包含一个图形化的模拟器，可以在电脑上模拟运行 Glyphix 应用。

本文档提供 glyphix.js 的安装和使用说明，[快速开始](/tutorials/getting-started.md)教程则是一份更简单的入门指南。另请阅读[构建和运行](#构建和运行)来了解如何开发、构建和发布一个 Glyphix 应用。

## 安装

本节介绍 glyphix.js 打包工具的安装方法。对于一般用途，只需要了解 [npm 安装](#npm-安装)方法。[手动安装](#手动安装)方法适用于特殊场景，例如网络受限的环境、CI 构建等。

### npm 安装

可以使用 [npm](https://nodejs.org) 包管理器来安装 glyphix.js 打包工具，建议使用 `-g` 选项来进行全局安装：
::: code-tabs
@tab npm
```bash
npm install -g glyphix-cli
```

@tab pnpm
```bash
pnpm install -g glyphix-cli
```

@tab yarn
```bash
yarn global add glyphix-cli
```
:::

::: tip
使用 pnpm 全局安装前，可能要执行 `pnpm setup` 来配置环境变量，`pnpm install -g` 命令会提示如何配置环境变量。
:::

安装完成后，可以在终端中执行 `gx --version` 来查看安装是否成功。例如：
```bash
$ npm install -g glyphix-cli
$ gx --version
gx v0.10.1 - The Glyphix applet development toolchain
commit a9337cf1 - Tue Sep 23 10:03:48 2025 +0800
```

此外，还必须安装 [pngquant](#pngquant) 才能为某些设备打包应用资源。

### 手动安装

还可以从 glyphix.js 打包工具的压缩包手动安装：将解压后目录中的 `bin` 目录添加到 `PATH` 环境变量中。下面将介绍主流操作系统上的安装方法。

::: tip
glyphix.js 工具并不只是一个可执行文件，请勿遗漏其他资源文件（包括 `bin` 和 `share` 目录中的所有文件）。
:::

#### macOS / Linux

对于 macOS 或 Linux，可以使用 `tar` 命令来安装 glyphix.js 打包工具。在此之前，还需要安装 `xz` 等工具：

::: code-tabs
@tab macOS
```bash
brew install xz
```

@tab Ubuntu / Debian
```bash
sudo apt update
sudo apt install xz-utils
```

@tab Arch Linux
```bash
sudo pacman -S xz
```
:::

下载好 glyphix.js 的压缩包后，使用以下命令解压并安装：
::: code-tabs
@tab macOS
```bash
tar -xvJf glyphix-v0.7.2-darwin-arm64.tar.xz -C ~/.local
```

@tab Linux
```bash
tar -xvJf glyphix-v0.7.2-linux-x86_64.tar.xz -C ~/.local
```
:::
请注意将 `.tar.xz` 文件名替换为实际下载的、对应于操作系统和 CPU 架构的文件名。解压后，`gx` 等命令会位于 `~/.local/bin` 目录下，请将该目录添加到 `PATH` 环境变量中，例如这样更新 `.bashrc`：
```bash
# 如果 ~/.local/bin 不在 PATH 中，则添加
echo "$PATH" | grep -q "$HOME/.local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc # 重新加载 bash 配置
```

::: tip
在使用 `Zsh` 时，`.zshrc` 配置文件可能导入了 `.bashrc`，因此只需要更新 `.bashrc` 即可。否则请按上述方法更新 `.zshrc`。

建议将 glyphix.js 打包工具安装在用户的 `~/.local` 目录中，这样可以避免使用 root 权限安装。
:::

#### Windows

要在 Windows 上安装 glyphix.js，请下载对应的 Windows 版本压缩包，然后使用支持 `7z` 格式的解压工具（例如 [7-Zip](https://www.7-zip.org/)）将其解压到某个目录下，例如 `C:\glyphix`。然后将 `C:\glyphix\bin` 添加到系统的 [`PATH` 环境变量](https://learn.microsoft.com/zh-cn/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14))中。

也可以使用 `7z` 命令行工具来解压，例如：
```shell
7z x -y glyphix-v0.7.2-windows-x64.7z -oC:/glyphix
```
这和 macOS 等系统的安装方法类似。

### 安装系统依赖

#### pngquant

Linux 和 macOS 用户需要额外安装 `pngquant`，你可以使用 `npm` 来安装它：
```bash
npm install -g pngquant-bin # pngquant-bin 只支持用 npm 安装
```
Windows 的 `glyphi-cli` 包含了 `pngquant.exe`，因此不需要额外安装。

::: tip
还可以从 [pngquant.org](https://pngquant.org/) 下载预编译的二进制文件，或者从系统的包管理器安装。
:::

#### Linux 系统依赖

glyphix.js 的 Linux 安装包不区分具体发行版，目前仅有 linux-x86_64 架构的构建包。我们测试其可以在 Ubuntu 20.04（或更新）和 Arch Linux 上运行。

如果你仅使用 `gx` 命令进行打包（这常用于 CI 打包），那么无桌面环境的 Linux 发行版应该可以直接使用。运行图形化的模拟器则依赖 X 窗口系统，因此您可能要安装 xorg 相关的软件包，尤其是 Wayland 环境下，您还需要安装 `xwayland` 软件包（模拟器尚不支持原生 Wayland）。

### 卸载

对于通过 npm 等包管理器全局安装的 glyphix.js，可以使用相应的包管理器来卸载，例如：
::: code-tabs
@tab npm
```bash
npm uninstall -g glyphix-cli
```

@tab pnpm
```bash
pnpm uninstall -g glyphix-cli
```

@tab yarn
```bash
yarn global remove glyphix-cli
```
:::

::: tip
对于使用 npm 等包管理器的非全局安装，只需要删除 `package.json` 中的 `glyphix-cli` 依赖，并执行 `npm install`（或 `pnpm install`、`yarn install`）来更新 `node_modules` 目录。
:::

对于手动安装，删除安装压缩包中的文件即可，例如对于 macOS 和 Linux 的 `tar.xz` 安装文件：
```bash
tar -tf glyphix-v0.7.2-darwin-arm64.tar.xz > filelist.txt
cat filelist.txt # 检查要删除的文件列表
xargs -I {} rm -f "~/.local/{}" < filelist.txt # 确认无误后执行删除
```
`tar -tf` 命令会列出压缩包中的文件列表，应该将 `glyphix-xxx.tar.xz` 替换为实际的安装文件。Windows 上的手动卸载操作也类似。

## 构建和运行

安装后 glyphix.js 后，在应用源代码的根目录中使用 [`gx build`](#gx-build) 命令来构建应用包，或使用 [`gx emu`](#gx-emu) 命令运行模拟器。

构建应用以后，请参考[提交应用包](#提交应用包)章节来了解如何将应用安装到设备上，或是提交到应用发布平台。

## 命令行参数

### 通用选项

#### `gx --help`

查看帮助信息。在具体的子命令中也可以使用帮助信息，例如使用 `gx build --help` 可以单独查看 `build` 子命令的帮助信息。

#### `gx --version`

`-V --version` 选项用于查看 `gx` 命令的版本号。

#### `gx --verbose`

`-v --verbose` 启用详细日志输出，应用开发者通常无需使用。

#### `gx --numeric-version`

输出 `gx` 命令的纯数字版本号，例如 `0.10.1`。

#### `gx --quiet`

`-q --quiet` 启用安静模式，抑制大部分非警告、错误的日志输出。这包括使用 `gx build` 时的构建进度日志，这种模式通常在需要构建大量应用包的 CI 环境中使用。

查看版本号。

### `gx new`

创建一个新项目，例如 `gx new myapp` 会创建一个名为 `myapp` 的新项目。

### `gx build`

构建项目（默认操作），使用 `--device` 或 `-d` 选项可以指定目标设备，例如
``` bash
gx build -d default # 指定为 default 设备构建
```
使用 `--dump` 选项可以打印 UX 文件的编译细节信息。

glyphix.js 支持增量构建，当源代码发生变动时，只有变化的部分会重新构建。

`-r --image-rules` 参数可以指定图片打包规则文件，默认为 `config/image-rules.json`。此参数的值会被缓存，后续执行 `gx build` 或 `gx emu` 将会按照先前的配置执行。

#### 命令选项

- `-d --device=NAME`：指定目标设备名称，必须是已安装的设备配置名称。可以使用 `gx list device` 命令查看已安装的设备列表。如果不指定该选项，则默认使用 `default` 设备。
- `-f --full`：强制完全重新构建项目，而不是增量构建。
- `-e --emulator`：为模拟器构建项目，而不是为实际设备构建。执行 `gx emu` 命令时会自动使用该选项。
- `-r --image-rules=PATH`：指定图片打包规则文件，默认为 `config/image-rules.json`。

#### 提交应用包

使用 `gx build` 构建后，将会在项目目录下生成 `.glyphix-work/dist/<device-name>/<package-name>` 目录，里面包含了构建好的应用包文件（`.pkg` 文件）。可以将该文件通过手机调试应用安装到设备上运行，也可以提交到应用发布平台。

应使用 `-d` 选项为所有需要支持的设备分别构建应用包。这是一个示例目录结构：
```bash
.glyphix-work/dist
├─ generic-watch-368x448
│  └─ com.example.app
│     ├─ bundle.pkg
│     ├─ icon.png
│     └─ manifest.json
└─ generic-watch-466x466
   └─ com.example.app
      ├─ bundle.pkg
      ├─ icon.png
      └─ manifest.json
```
在提交应用包时，请将**整个** `.glyphix-work/dist` 目录打包上传，而不是仅上传 `.pkg` 文件，或是任一子目录。平台会根据 `manifest.json` 文件中的信息来识别应用，并可能需要 `icon.png` 作为预览图标。

::: tip
对于 Linux 或 macOS 用户，可以使用这样的命令来打包某类设备的应用：
```bash
gx list device | grep "^generic-" | xargs -n 1 gx build -d
```
这会为所有名称以 `generic-` 开头的设备构建应用包。

Windows 下也可以使用类似的 PoweShell 命令批量构建：
```shell
gx list device | ? { $_ -match "^generic-" } | % { gx build -d $_ }
```
:::

### `gx emu`

相见[模拟器和调试](/tutorials/glyphix.js/emulator.md)文档。

### `gx clean`

清理构建产物，此命令会将项目文件夹下的 `.glyphix-work` 目录删除。

### `gx config`

此命令启动一个编辑图片打包规则文件的 Web 界面，按照命令提示可在浏览器中打开页面进行操作。该命令有两种用法：
``` bash
gx config # 在 Glyphix 项目中时，不用指定源目录（目前只能在项目根目录下使用）
gx config path/to/dir # 对指定的目录进行配置，可用于非项目图片资源的配置
```

`-r --image-rules` 参数可以指定图片打包规则文件，默认为 `config/image-rules.json`。

### `gx image-forge`

对游离的图片文件进行转换。该命令可以指定任意的源路径和输出路径，不需要在 Glyphix 项目中执行：
``` bash
gx image-forge src -o dist
```

选项说明：
- `src` 是要转换的源路径，`image-forge` 命令递归地转换所有的图片并按照相对目录结构生成到 `-o, --output` 指定的目标路径中（默认为 `dist`）。
- `-r --image-rules` 参数可以指定图片打包规则文件，默认为 `config/image-rules.json`。
- `-d --device` 指定图片转换的目标设备。

### `gx list`

列出某些信息。目前支持三种操作：
``` bash
gx list device # 列出所有已安装的设备配置
gx list template # 列出所有已安装的项目模板
gx list image # 列出当前目录下所有图片资源的相对路径（类似于 find 命令）
```

某些信息可以使用 `-d, --detailed` 来列出详细的说明文本，例如：
```
$ gx list device -d
The following devices have been found:
  default
    Default virtual device, for debugging purposes only.

  rtt-watch
    A smartwatch from RT-Thread. With a 1.43 inch screen
    and 4 GB of storage.
```

### `gx completion`

此命令用于生成 `gx` 命令的 shell 的自动补全脚本，目前支持 [Zsh](https://www.zsh.org/) 和 [PowerShell 7+](https://github.com/PowerShell/PowerShell)。使用 `gx completion [SHELL]` 会输出指定 shell 的自动补全脚本（不指定 `SHELL` 参数时会检测当前 Shell）。如果要安装补全脚本，请使用：
```bash
gx completion --install
```
安装成功后会提示命令补全脚本的安装路径，重启 Shell 会话即可使用自动补全，也可以使用这些命令立即生效：
::: code-tabs
@tab Oh My Zsh
```bash
omz reload
```

@tab PowerShell
```shell
Import-Module glyphix -Force
```
:::

使用自动补全脚本时可以在终端中选择 `gx emu` 的设备、命令行选项等，而不需要手动输入。

PowerShell 默认使用循环补全，建议更改为补全菜单：
```shell
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
```
将该命令添加到 [`$PROFILE`](https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/creating-profiles#adding-customizations-to-your-profile) 配置文件即可永久生效。

::: note
如果 `--install` 选项无法自动安装，还可以用 `gx completion` 命令手动安装补全脚本，例如：
```shell
gx completion zsh > ~/.zsh/completion/_gx.zsh
```
:::

## 默认配置路径

glyphix.js 工具中的配置、项目模板、设备信息等信息可以存储在以下路径中：
- 系统级配置：相对于 `gx`/`gx.exe` 可执行文件上级目录的 `share/glyphix` 目录。假设例如 `gx` 可执行文件的路径在 `/usr/local/glyphix`，那么系统级配置配置的资源路径是 `/usr/local/share/glyphix`
- 用户级配置：在类 Unix 系统中为 `~/.local/share/glyphix`，在 Windows 中为 `%APPDATA%\AppData\Roaming\glyphix`

可以将配置文件存放在以上路径之一，其中用户级配置的优先级更高。`gx.js` 安装时会自带默认配置文件。

## 工程模板

项目模板存储在配置路径的 `templates` 目录下，目前只支持 `simple` 模板，并且不支持自定义。

## 设备配置文件

设备配置文件存储在配置路径的 `devices` 目录下。每个设备都一个 YAML 配置文件，配置文件的名称为 `<device-name>.yml`。配置文件的格式说明如下：

``` yaml
# file: default.yml
description:
  供开发者查看的设备描述信息。

screen: # 描述设备屏幕配置的字段，这些字段都是必填的（会影响 UI 布局和资源缩放）
  width: 454 # 屏幕水平像素数
  height: 454 # 屏幕垂直像素数
  dpi: 326 # 屏幕的像素密度，单位是像素/英寸

ui: # 全局界面配置，都是可选字段
  font-family: sans-serif # 系统默认的字体族名称（默认为 serif）
  font-size: 3.5 # 系统默认的字号，单位是磅（pt、点），注意不是像素！！
  font-map: true # 是否使用全局字体配置映射文件，如果是，则系统资源中必须存在
                 # font-faces.css 文件

# 可选的系统的全局资源包路径，以下配置意味着全局资源包存储在 default.yml 同级的
# default-global 文件夹下。全局资源包包含系统中预置的字体和字体配置映射文件等。
global-assets: default-global

# 可选的图片转换脚本，脚本文件路径相对于当前设备描述文件存放。如果不指定图片转换
# 脚本打包时会输出原始 PNG 素材，但是会应用分辨率缩放。
image-build: image-convert.scm

# 运行模拟器的命令，默认会执行 glyphix-emu。模拟器命令的可执行文件必须位于 PATH
# 环境变量的路径下，否则会无法执行。
emulator: glyphix-emu
```
