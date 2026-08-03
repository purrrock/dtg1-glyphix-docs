---
icon: package-variant-closed
---
# Glyphix.js packaging tool

glyphix.js is a packaging tool for Glyphix applications. It contains a command line tool called `gx` that can be used to create, build and run Glyphix applications. The tool also includes a graphical simulator that can simulate running Glyphix applications on your computer.

This document provides installation and usage instructions for glyphix.js, and the [Quick Start](/doc_en/getting-started.md) tutorial is a simpler getting started guide. Also read [Build and Run](#buildandrun) to learn how to develop, build, and publish a Glyphix application.

## Install

This section introduces how to install the glyphix.js packaging tool. For general use, just know the [npm install](#npm-install) method. [Manual installation](#manual-installation) method is suitable for special scenarios, such as network-limited environments, CI builds, etc.

### npm installation

You can use the [npm](https://nodejs.org) package manager to install the glyphix.js packaging tool. It is recommended to use the `-g` option for global installation:
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
Before using pnpm to install globally, you may need to execute `pnpm setup` to configure environment variables. The `pnpm install -g` command will prompt how to configure environment variables.
:::

After the installation is complete, you can execute `gx --version` in the terminal to check whether the installation is successful. For example:
```bash
$ npm install -g glyphix-cli
$ gx --version
gx v0.10.1 - The Glyphix applet development toolchain
commit a9337cf1 - Tue Sep 23 10:03:48 2025 +0800
```

Additionally, [pngquant](#pngquant) must be installed to package app resources for some devices.

### Manual installation

You can also install it manually from the compressed package of the glyphix.js packaging tool: add the `bin` directory in the unzipped directory to the `PATH` environment variable. The following will introduce the installation methods on mainstream operating systems.

::: tip
The glyphix.js tool is not just an executable file, do not leave out other resource files (including all files in the `bin` and `share` directories).
:::

#### macOS/Linux

For macOS or Linux, you can use the `tar` command to install the glyphix.js packaging tool. Before that, you also need to install tools such as `xz`:

::: code-tabs
@tab macOS
```bash
brew install xz
```

@tab Ubuntu/Debian
```bash
sudo apt update
sudo apt install xz-utils
```

@tab Arch Linux
```bash
sudo pacman -S xz
```
:::

After downloading the compressed package of glyphix.js, use the following commands to decompress and install:
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
Please be careful to replace the `.tar.xz` file name with the actual downloaded file name that corresponds to your operating system and CPU architecture. After decompression, commands such as `gx` will be located in the `~/.local/bin` directory. Please add this directory to the `PATH` environment variable, for example, update `.bashrc` like this:
```bash
# If ~/.local/bin is not in PATH, add
echo "$PATH" | grep -q "$HOME/.local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc # Reload bash configuration
```

::: tip
When using `Zsh`, the `.zshrc` configuration file may import `.bashrc`, so only `.bashrc` needs to be updated. Otherwise, please update `.zshrc` as above.

It is recommended to install the glyphix.js packaging tool in the user's `~/.local` directory to avoid using root privileges for installation.
:::

#### Windows

To install glyphix.js on Windows, please download the corresponding Windows version compressed package, and then use an decompression tool that supports `7z` format (such as [7-Zip](https://www.7-zip.org/)) to extract it to a directory, such as `C:\glyphix`. Then add `C:\glyphix\bin` to the system's [`PATH` environment variable](https://learn.microsoft.com/zh-cn/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)).

You can also use the `7z` command line tool to decompress, for example:
```shell
7z x -y glyphix-v0.7.2-windows-x64.7z -oC:/glyphix
```
This is similar to the installation method for systems such as macOS.

### Install system dependencies

#### pngquant

Linux and macOS users need to install `pngquant` additionally, you can use `npm` to install it:
```bash
npm install -g pngquant-bin # pngquant-bin only supports installation with npm
```
The Windows `glyphi-cli` includes `pngquant.exe`, so no additional installation is required.

::: tip
You can also download precompiled binaries from [pngquant.org](https://pngquant.org/) or install from your system's package manager.
:::

#### Linux system dependencies

The Linux installation package of glyphix.js does not distinguish between specific distribution versions. Currently, there are only build packages for the linux-x86_64 architecture. We tested it running on Ubuntu 20.04 (or newer) and Arch Linux.

If you just use the `gx` command for packaging (which is commonly used for CI packaging), Linux distributions without a desktop environment should work out of the box. Running the graphical simulator relies on the X Window System, so you may need to install xorg-related software packages, especially for Wayland environments. You also need to install the `xwayland` software package (the simulator does not yet support native Wayland).

### uninstall

For glyphix.js installed globally through a package manager such as npm, you can use the corresponding package manager to uninstall, for example:
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
For non-global installation using a package manager such as npm, just remove the `glyphix-cli` dependency in `package.json` and execute `npm install` (or `pnpm install`, `yarn install`) to update the `node_modules` directory.
:::

For manual installation, just delete the files in the installation compressed package, such as the `tar.xz` installation file for macOS and Linux:
```bash
tar -tf glyphix-v0.7.2-darwin-arm64.tar.xz > filelist.txt
cat filelist.txt # Check the file list to be deleted
xargs -I {} rm -f "~/.local/{}" < filelist.txt # Execute deletion after confirmation
```
The `tar -tf` command will list the files in the compressed package, and `glyphix-xxx.tar.xz` should be replaced with the actual installation file. Manual uninstallation on Windows is similar.

## Build and run

After installing glyphix.js, use the [`gx build`](#gx-build) command in the root directory of the app source code to build the app package, or use the [`gx emu`](#gx-emu) command to run the emulator.

After building the application, please refer to the [Submit Application Package](#submit-application-package) chapter to learn how to install the application on the device or submit it to the application publishing platform.

## Command line parameters

### General options

#### `gx --help`

View help information. Help information can also be used in specific subcommands. For example, use `gx build --help` to view the help information of the `build` subcommand separately.

#### `gx --version`

The `-V --version` option is used to view the version number of the `gx` command.

#### `gx --verbose`

`-v --verbose` enables verbose logging output, which application developers generally do not need to use.

#### `gx --numeric-version`

Output the purely numeric version number of the `gx` command, for example `0.10.1`.

#### `gx --quiet`

`-q --quiet` enables quiet mode and suppresses most non-warning and error log output. This includes build progress logs when using `gx build`, a mode commonly used in CI environments where a large number of application packages need to be built.

View the version number.

### `gx new`

Creating a new project, for example `gx new myapp` will create a new project named `myapp`.

### `gx build`

Build the project (default action), use the `--device` or `-d` option to specify the target device, e.g.
```bash
gx build -d default # Specify the default device build
```
Use the `--dump` option to print compilation details of the UX file.

Glyphix.js supports incremental builds. When the source code changes, only the changed parts will be rebuilt.

The `-r --image-rules` parameter can specify the image packaging rule file, the default is `config/image-rules.json`. The value of this parameter will be cached, and subsequent executions of `gx build` or `gx emu` will be executed according to the previous configuration.

#### Command options

- `-d --device=NAME`: Specify the target device name, which must be the installed device configuration name. You can view the list of installed devices using the `gx list device` command. If this option is not specified, the `default` device is used by default.
- `-f --full`: Force a complete rebuild of the project instead of an incremental build.
- `-e --emulator`: Build the project for the emulator instead of the actual device. This option is automatically used when executing the `gx emu` command.
- `-r --image-rules=PATH`: Specify the image packaging rule file, the default is `config/image-rules.json`.

#### Submit application package

After building with `gx build`, the `.glyphix-work/dist/<device-name>/<package-name>` directory will be generated in the project directory, which contains the built application package file (`.pkg` file). This file can be installed and run on the device through the mobile phone debugging application, or it can be submitted to the application publishing platform.

Application packages should be built separately for all devices that need support using the `-d` option. Here is an example directory structure:
```bash
.glyphix-work/dist
├─ generic-watch-368x448
│ └─ com.example.app
│ ├─ bundle.pkg
│ ├─ icon.png
│ └─ manifest.json
└─ generic-watch-466x466
   └─ com.example.app
      ├─ bundle.pkg
      ├─ icon.png
      └─ manifest.json
```
When submitting an application package, please package and upload the entire `.glyphix-work/dist` directory instead of just uploading the `.pkg` file or any subdirectory. The platform identifies the app based on information in the `manifest.json` file and may require `icon.png` as a preview icon.

::: tip
For Linux or macOS users, you can use this command to package applications for certain types of devices:
```bash
gx list device | grep "^generic-" | xargs -n 1 gx build -d
```
This will build app packages for all devices whose names start with `generic-`.

You can also use similar PoweShell commands to build in batches under Windows:
```shell
gx list device | ? { $_ -match "^generic-" } | % { gx build -d $_ }
```
:::

### `gx emu`

Meet the [Emulator and Debugging](/doc_en/glyphix.js/emulator.md) documentation.

### `gx clean`

Clean the build product. This command will delete the `.glyphix-work` directory under the project folder.

### `gx config`

This command starts a web interface for editing image packaging rule files. Follow the command prompts to open the page in the browser for operation. This command has two uses:
```bash
gx config # When in a Glyphix project, there is no need to specify the source directory (currently it can only be used in the project root directory)
gx config path/to/dir # Configure the specified directory, which can be used to configure non-project image resources
```

The `-r --image-rules` parameter can specify the image packaging rule file, the default is `config/image-rules.json`.

### `gx image-forge`

Convert free image files. This command can specify any source path and output path, and does not need to be executed in the Glyphix project:
```bash
gx image-forge src -o dist
```

Option description:
- `src` is the source path to be converted. The `image-forge` command recursively converts all images and generates them according to the relative directory structure to the target path specified by `-o, --output` (default is `dist`).
- The `-r --image-rules` parameter can specify the image packaging rule file, the default is `config/image-rules.json`.
- `-d --device` specifies the target device for image conversion.

### `gx list`

List some information. Currently three operations are supported:
```bash
gx list device # List all installed device configurations
gx list template # List all installed project templates
gx list image # List the relative paths of all image resources in the current directory (similar to the find command)
```

Some information can use `-d, --detailed` to list detailed description text, for example:
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

This command is used to generate a shell auto-completion script for the `gx` command. It currently supports [Zsh](https://www.zsh.org/) and [PowerShell 7+](https://github.com/PowerShell/PowerShell). Using `gx completion [SHELL]` will output the auto-completion script for the specified shell (when the `SHELL` parameter is not specified, the current shell will be detected). If you want to install a completion script, use:
```bash
gx completion --install
```
After the installation is successful, you will be prompted for the installation path of the command completion script. You can use automatic completion by restarting the shell session, or you can use these commands to take effect immediately:
::: code-tabs
@tab Oh My Zsh
```bash
omz reload
```

@tab PowerShell
```shell
Import-Module glyphix-Force
```
:::

When using the auto-completion script, you can select the device, command line options, etc. of `gx emu` in the terminal without manual input.

PowerShell uses loop completion by default. It is recommended to change to the completion menu:
```shell
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
```
Add this command to the [`$PROFILE`](https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/creating-profiles#adding-customizations-to-your-profile) profile to make it permanent.

::: note
If the `--install` option cannot be installed automatically, you can also use the `gx completion` command to manually install the completion script, for example:
```shell
gx completion zsh > ~/.zsh/completion/_gx.zsh
```
:::

## Default configuration path

Configuration, project templates, device information and other information in the glyphix.js tool can be stored in the following path:
- System-level configuration: `share/glyphix` directory relative to the directory above the `gx`/`gx.exe` executable file. Suppose, for example, that the path of the `gx` executable file is in `/usr/local/glyphix`, then the resource path of the system-level configuration configuration is `/usr/local/share/glyphix`
- User-level configuration: `~/.local/share/glyphix` on Unix-like systems, `%APPDATA%\AppData\Roaming\glyphix` on Windows

The configuration file can be stored in one of the above paths, where user-level configuration has higher priority. `gx.js` will come with a default configuration file when installed.

## Project template

Project templates are stored in the `templates` directory of the configuration path. Currently, only the `simple` template is supported and customization is not supported.

## Device configuration file

Device configuration files are stored in the `devices` directory of the configuration path. Each device has a YAML configuration file, and the name of the configuration file is `<device-name>.yml`. The format of the configuration file is described as follows:

```yaml
# file: default.yml
description:
  Device description information for developers to view.

screen: # Fields describing the device screen configuration, these fields are required (will affect UI layout and resource scaling)
  width: 454 # Number of horizontal pixels on the screen
  height: 454 # Number of vertical pixels on the screen
  dpi: 326 # The pixel density of the screen, in pixels/inch

ui: # Global interface configuration, all optional fields
  font-family: sans-serif # System default font family name (default is serif)
  font-size: 3.5 # The system default font size, the unit is points (pt, points), note not pixels! !
  font-map: true # Whether to use the global font configuration mapping file, if so, it must exist in the system resources
                 # font-faces.css file

# Optional system global resource package path, the following configuration means that the global resource package is stored at the same level as default.yml
# Under the default-global folder. The global resource package contains preset fonts and font configuration mapping files in the system.
global-assets: default-global

# Optional image conversion script, the script file path is stored relative to the current device description file. If you do not specify image conversion
# When the script is packaged, it will output the original PNG material, but resolution scaling will be applied.
image-build: image-convert.scm

# The command to run the emulator will execute glyphix-emu by default. The executable file for the emulator command must be in PATH
# The path of the environment variable, otherwise it will not be executed.
emulator: glyphix-emu
```