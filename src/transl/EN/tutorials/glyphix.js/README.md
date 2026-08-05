---
icon: package-variant-closed
---
# Glyphix.js Packaging Tool

glyphix.js is the packaging tool for Glyphix applications. It includes a command-line tool named `gx`, which can be used to create, build, and run Glyphix applications. The tool also includes a graphical emulator to simulate running Glyphix applications on your computer.

This document provides installation and usage instructions for glyphix.js. The [Getting Started](/tutorials/getting-started.md) tutorial serves as a simpler introductory guide. Please also read [Building and Running](#building-and-running) to learn how to develop, build, and publish a Glyphix application.

## Installation

This section describes how to install the glyphix.js packaging tool. For general purposes, you only need to know the [npm Installation](#npm-installation) method. The [Manual Installation](#manual-installation) method is suitable for special scenarios, such as network-restricted environments or CI builds.

### npm Installation

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
Before performing a global installation with pnpm, you may need to run `pnpm setup` to configure environment variables. The `pnpm install -g` command will prompt you on how to configure them.
:::

Once installed, you can run `gx --version` in your terminal to check if the installation was successful. For example:
```bash
$ npm install -g glyphix-cli
$ gx --version
gx v0.10.1 - The Glyphix applet development toolchain
commit a9337cf1 - Tue Sep 23 10:03:48 2025 +0800
```

In addition, [pngquant](#pngquant) must be installed to package application assets for certain devices.

### Manual Installation

You can also manually install the glyphix.js packaging tool from its archive: add the `bin` directory from the extracted folder to your `PATH` environment variable. The installation methods for mainstream operating systems are introduced below.

::: tip
The glyphix.js tool is not just a single executable file. Do not omit other resource files (including all files in the `bin` and `share` directories).
:::

#### macOS / Linux

For macOS or Linux, you can use the `tar` command to install the glyphix.js packaging tool. Before doing so, you also need to install tools like `xz`:

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

After downloading the glyphix.js archive, use the following command to extract and install it:
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
Please replace the `.tar.xz` filename with the actual downloaded filename corresponding to your operating system and CPU architecture. After extraction, commands like `gx` will be located in the `~/.local/bin` directory. Add this directory to your `PATH` environment variable, for example, by updating your `.bashrc` like this:
```bash
# If ~/.local/bin is not in PATH, add it
echo "$PATH" | grep -q "$HOME/.local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc # Reload bash configuration
```

::: tip
When using `Zsh`, your `.zshrc` configuration file may import `.bashrc`, so updating `.bashrc` is sufficient. Otherwise, update `.zshrc` according to the method above.

It is recommended to install the glyphix.js packaging tool in the user's `~/.local` directory to avoid installing with root privileges.
:::

#### Windows

To install glyphix.js on Windows, download the corresponding Windows version archive, and then use an extraction tool that supports the `7z` format (such as [7-Zip](https://www.7-zip.org/)) to extract it to a directory, such as `C:\glyphix`. Then add `C:\glyphix\bin` to your system's [`PATH` environment variable](https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)).

You can also use the `7z` command-line tool to extract it, for example:
```shell
7z x -y glyphix-v0.7.2-windows-x64.7z -oC:/glyphix
```
This is similar to the installation method on macOS and other systems.

### Installing System Dependencies

#### pngquant

Linux and macOS users need to install `pngquant` additionally. You can use `npm` to install it:
```bash
npm install -g pngquant-bin # pngquant-bin can only be installed using npm
```
The Windows version of `glyphix-cli` includes `pngquant.exe`, so no additional installation is required.

::: tip
You can also download precompiled binaries from [pngquant.org](https://pngquant.org/) or install them via your system's package manager.
:::

#### Linux System Dependencies

The Linux installation package of glyphix.js is distro-agnostic and currently only has a `linux-x86_64` architecture build. We have tested that it runs on Ubuntu 20.04 (or newer) and Arch Linux.

If you only use the `gx` command for packaging (which is commonly used in CI builds), headless Linux distributions should work out of the box. Running the graphical emulator relies on the X Window System, so you may need to install xorg-related packages. Especially under a Wayland environment, you also need to install the `xwayland` package (the emulator does not yet support native Wayland).

### Uninstallation

For glyphix.js globally installed via a package manager like npm, you can use the corresponding package manager to uninstall it, for example:
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
For non-global installations using package managers like npm, simply remove the `glyphix-cli` dependency from `package.json` and run `npm install` (or `pnpm install`, `yarn install`) to update the `node_modules` directory.
:::

For manual installations, simply delete the files from the installation archive. For example, for `tar.xz` installation files on macOS and Linux:
```bash
tar -tf glyphix-v0.7.2-darwin-arm64.tar.xz > filelist.txt
cat filelist.txt # Inspect the list of files to be deleted
xargs -I {} rm -f "~/.local/{}" < filelist.txt # Execute deletion after confirmation
```
The `tar -tf` command lists the files in the archive. Replace `glyphix-xxx.tar.xz` with your actual installation file. Manual uninstallation on Windows is similar.

## Building and Running

After installing glyphix.js, use the [`gx build`](#gx-build) command in the root directory of your application source code to build the application package, or use the [`gx emu`](#gx-emu) command to run the emulator.

After building the application, please refer to the [Submitting Application Packages](#submitting-application-packages) section to learn how to install the application onto a device or submit it to an app publishing platform.

## Command-Line Arguments

### General Options

#### `gx --help`

View help information. Help information can also be used with specific subcommands, for example, using `gx build --help` to view help exclusively for the `build` subcommand.

#### `gx --version`

The `-V --version` option is used to view the version number of the `gx` command.

#### `gx --verbose`

`-v --verbose` enables detailed log output. Application developers generally do not need to use this.

#### `gx --numeric-version`

Outputs the pure numeric version number of the `gx` command, such as `0.10.1`.

#### `gx --quiet`

`-q --quiet` enables quiet mode, suppressing most non-warning and non-error log outputs. This includes build progress logs when using `gx build`. This mode is typically used in CI environments where a large number of application packages need to be built.

View the version number.

### `gx new`

Creates a new project. For example, `gx new myapp` creates a new project named `myapp`.

### `gx build`

Builds the project (default operation). You can use the `--device` or `-d` option to specify the target device, for example:
``` bash
gx build -d default # Specify building for the default device
```
Use the `--dump` option to print compilation details of UX files.

glyphix.js supports incremental builds; when source code changes, only the modified parts are rebuilt.

The `-r --image-rules` parameter can specify the image packaging rules file, which defaults to `config/image-rules.json`. The value of this parameter will be cached, and subsequent executions of `gx build` or `gx emu` will follow the previous configuration.

#### Command Options

- `-d --device=NAME`: Specifies the target device name, which must be an installed device configuration name. You can use the `gx list device` command to view the list of installed devices. If this option is not specified, the `default` device is used.
- `-f --full`: Forces a full rebuild of the project instead of an incremental build.
- `-e --emulator`: Builds the project for the emulator rather than an actual device. The `gx emu` command automatically uses this option.
- `-r --image-rules=PATH`: Specifies the image packaging rules file, defaulting to `config/image-rules.json`.

#### Submitting Application Packages

After building with `gx build`, a `.glyphix-work/dist/<device-name>/<package-name>` directory will be generated in the project directory, containing the built application package files (`.pkg` file). You can install this file onto a device for testing via mobile debugging or submit it to an app publishing platform.

You should use the `-d` option to build application packages separately for all supported devices. Here is an example directory structure:
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
When submitting an application package, please compress and upload the **entire** `.glyphix-work/dist` directory rather than just the `.pkg` file or any single subdirectory. The platform identifies applications based on the information in `manifest.json` and may require `icon.png` as a preview icon.

::: tip
For Linux or macOS users, you can use a command like this to package applications for a specific category of devices:
```bash
gx list device | grep "^generic-" | xargs -n 1 gx build -d
```
This builds application packages for all devices whose names start with `generic-`.

Under Windows, you can also use a similar PowerShell command for batch building:
```shell
gx list device | ? { $_ -match "^generic-" } | % { gx build -d $_ }
```
:::

### `gx emu`

See the [Emulator and Debugging](/tutorials/glyphix.js/emulator.md) documentation.

### `gx clean`

Cleans build artifacts. This command deletes the `.glyphix-work` directory under the project folder.

### `gx config`

This command starts a Web interface for editing image packaging rules files. Follow the command prompts to open the page in your browser for operation. This command has two usages:
``` bash
gx config # When inside a Glyphix project, no source directory needs to be specified (currently can only be used in the project root directory)
gx config path/to/dir # Configures a specified directory, which can be used for configuring non-project image resources
```

The `-r --image-rules` parameter can specify the image packaging rules file, which defaults to `config/image-rules.json`.

### `gx image-forge`

Converts loose image files. This command can specify arbitrary source and output paths and does not need to be executed inside a Glyphix project:
``` bash
gx image-forge src -o dist
```

Option Descriptions:
- `src` is the source path to be converted. The `image-forge` command recursively converts all images and generates them into the target path specified by `-o, --output` (defaults to `dist`) while maintaining the relative directory structure.
- `-r --image-rules` parameter can specify the image packaging rules file, which defaults to `config/image-rules.json`.
- `-d --device` specifies the target device for image conversion.

### `gx list`

Lists certain information. Currently supports three operations:
``` bash
gx list device # List all installed device configurations
gx list template # List all installed project templates
gx list image # List relative paths of all image resources in the current directory (similar to the find command)
```

Detailed description text for certain information can be listed using `-d, --detailed`, for example:
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

This command is used to generate shell auto-completion scripts for the `gx` command. It currently supports [Zsh](https://www.zsh.org/) and [PowerShell 7+](https://github.com/PowerShell/PowerShell). Using `gx completion [SHELL]` outputs the auto-completion script for the specified shell (if the `SHELL` parameter is not specified, the current shell is detected). To install the completion script, use:
```bash
gx completion --install
```
After successful installation, it will prompt the installation path of the command completion script. Restarting your shell session will enable auto-completion, or you can use these commands to take effect immediately:
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

When using the auto-completion script, you can select `gx emu` devices, command-line options, etc., in the terminal without manual typing.

PowerShell uses cycle completion by default. It is recommended to change it to menu completion:
```shell
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
```
Adding this command to your [`$PROFILE`](https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/creating-profiles#adding-customizations-to-your-profile) configuration file will make it permanent.

::: note
If the `--install` option fails to install automatically, you can also manually install the completion script using the `gx completion` command, for example:
```shell
gx completion zsh > ~/.zsh/completion/_gx.zsh
```
:::

## Default Configuration Paths

Configurations, project templates, device information, etc., in the glyphix.js tool can be stored in the following paths:
- System-level configuration: The `share/glyphix` directory relative to the parent directory of the `gx`/`gx.exe` executable file. For example, assuming the path of the `gx` executable is `/usr/local/glyphix`, the system-level configuration resource path is `/usr/local/share/glyphix`.
- User-level configuration: `~/.local/share/glyphix` on Unix-like systems, and `%APPDATA%\AppData\Roaming\glyphix` on Windows.

Configuration files can be stored in either of the above paths, with user-level configuration having a higher priority. `gx.js` comes with default configuration files upon installation.

## Project Templates

Project templates are stored in the `templates` directory of the configuration path. Currently, only the `simple` template is supported, and customization is not supported.

## Device Configuration Files

Device configuration files are stored in the `devices` directory of the configuration path. Each device has a YAML configuration file named `<device-name>.yml`. The format of the configuration file is described as follows:

``` yaml
# file: default.yml
description:
  Device description information for developers to view.

screen: # Fields describing device screen configuration, all of which are mandatory (affects UI layout and asset scaling)
  width: 454 # Horizontal pixels of the screen
  height: 454 # Vertical pixels of the screen
  dpi: 326 # Pixel density of the screen, in pixels/inch

ui: # Global interface configuration, all are optional fields
  font-family: sans-serif # System default font family name (defaults to serif)
  font-size: 3.5 # System default font size, in points (pt), note: not pixels!!
  font-map: true # Whether to use a global font configuration mapping file. If true, font-faces.css
                 # must exist in system resources.

# Optional path for the system's global asset package. The following configuration implies that the global 
# asset package is stored in the `default-global` folder parallel to `default.yml`. The global asset package 
# contains pre-installed fonts and font configuration mapping files, etc.
global-assets: default-global

# Optional image conversion script. The script file path is relative to where the current device description 
# file is stored. If not specified, original PNG assets will be output during packaging, but resolution 
# scaling will be applied.
image-build: image-convert.scm

# Command to run the emulator, which executes glyphix-emu by default. The emulator command's executable file 
# must be located in a directory within the PATH environment variable, otherwise it will fail to execute.
emulator: glyphix-emu
```