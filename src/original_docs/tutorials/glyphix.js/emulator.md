---
icon: watch-import-variant
---
# 模拟器和调试

要运行模拟器，你需要在命令行中切换到项目的根目录，然后运行 `gx emu` 子命令来启动模拟器。Glyphix 模拟器拥有和真实设备运行时高度一致的环境，因此可以利用模拟器开发和调试大部分界面和功能，而不需要频繁地将应用安装到真实设备上。

::: tip
由于当前 [`glyphix`](https://www.npmjs.com/package/glyphix) npm 包的限制，请务必配置 [`glyphix.config.js`](/tutorials/nodejs.md#glyphix-config-js-配置)，否则在执行 `gx emu` 时无法看到错误信息的源代码行号。
:::


## `gx emu` 子命令

使用上次的构建目标设备配置来运行模拟器。该命令需要在 Glyphix 项目的根目录中执行。它会自动构建项目并创建模拟器所需的资源文件，因此无需先执行 `gx build`。

#### 命令选项

- `-d --device=NAME`：指定模拟的设备名称，默认为 `default`（分辨率为 $410 \times 502\rm px$）。
- `-e --emulator-exe=CMD`：指定模拟器的可执行文件，默认为 `glyphix-emu`。通常不需要修改。
- `-l --language=NAME`：指定模拟器的语言环境，默认为 `zh-CN`（简体中文）。通过 `gx list language` 命令可以查看支持的语言列表。
- `--target=URI`：设置模拟器启动时的包名或者 deeplink，例如 `app://com.example.app/SomePage?query=value` 或者 `com.example.app`。
- `-i --inspector`：在运行模拟器时启用检查器，检查器是一个 Web 页面，可以在浏览器中调试模拟器中的界面元素。
- `-m --mobile-network`：（尚未实现）仅在模拟器中启用手机 SDK 的网络代理，而不直接访问网络。
- `-w --watch`：运行模拟器时监听项目目录，当源文件发生变动时自动重新构建并刷新模拟器界面。
- `-r --real-scale`：使用真实尺寸显示模拟器窗口，而不是按设备分辨率缩放显示。此选项建议在 HiDPI 屏幕上使用。
- `-t --top`：保持模拟器窗口置顶。
- `-p --profiling`：启用性能分析模式。由于模拟器和设备性能差异较大，该选项通常不是很有用。

## 启动模式

默认情况下，`gx emu` 会按照上次构建时使用的设备配置来启动模拟器。还可以通过命令选项来调整模拟器的启动行为。

### 指定设备型号

使用 `-d` 或 `--device` 选项可以指定希望模拟的设备型号，例如：
```bash
gx emu -d generic-watch-466x466
```
将会为 `generic-watch-466x466` 这款设备启动模拟器。可以使用 `gx list device` 命令查看已安装的设备列表。

如果不指定该选项，则会使用上次指定过的设备。第一次或 `gx clean` 之后启动模拟器时会使用 `default` 设备。

### Deeplink 启动

默认情况下，模拟器会启动当前项目的应用，或是启动一个应用菜单界面。但在调试 [`onRoute()`](/framework/component/life-cycle.md#onroute) 生命周期函数时，可能希望通过 deeplink 启动应用，以确保 `onRoute()` 接收到特定参数。可以使用 `--target` 选项来指定 deeplink，例如：
```bash
gx emu --target app://com.example.app/SomePage?query=value
```
这会启动包名为 `com.example.app` 的应用，而 Deeplink URI 的 path（含根目录 `/`，即 `/SomePage`）和 query 字段会被传递给该应用的 `onRoute()` 函数。

### 模拟设备尺寸

默认情况下，模拟器会使用设备的实际像素分辨率，这会导致电脑上的显示尺寸大于设备的实际屏幕尺寸，并使开发者难以确认 UI 元素（包括设计稿）在设备上的具有较佳尺寸。`-r` 或 `--real-scale` 选项可以按真实设备尺寸来模拟：
```bash
gx emu -r
```
使用此选项时，您不需要将应用安装到设备上即可确认 UI 的实际尺寸。但考虑到大部分手表的 DPI 超过 300，1080p 显示器在使用 real-scale 模式时会导致界面过于模糊，建议在 HiDPI 显示器（如 4K 显示器，或者 macOS 上的 Retina 屏幕）上使用此选项。

::: tip
使用 real-scale 模式时，您应该通过 `--device` 选项来指定希望模拟的目标设备。值得注意的是：由于 DPI 不同，两款相同的分辨率设备可能有不同的屏幕尺寸，因此 real-scale 模式的显示尺寸也会不同。
:::

### 自动刷新

`-w` 或 `--watch` 选项可以在运行模拟器时监听项目目录，当源文件发生变动时自动重新构建并重启应用。通常建议配合 `--top` 选项使用，例如：
```bash
gx emu -wt
```
这样可以保持模拟器窗口置顶，并且在修改源文件后自动重启应用。这对于开发调试非常有用：直接从代码编辑器切换到模拟器，不需要手动重启模拟器，也不需要频繁切换窗口。

::: tip
目前不支持热更新页面，而是在修改源文件后重启整个应用。如果想要更快的调试速度，可以将 [`manifest.router.entry`](/framework/application/manifest.md#entry) 调整为正在开发的页面，这样每次重启应用时都会直接进入该页面。
:::

## 连接手机

可以通过 [Glyphix Debug](https://www.pgyer.com/KLeBQFv6) Android 手机应用连接模拟器，以便于调试真实设备和手机互联相关的功能。

### 准备工作

你需要在手机上安装 Glyphix Debug 应用，并确保手机和电脑处于同一局域网内，例如连接到同一个 Wi-Fi。启动模拟器并打开打开 Glyphix Debug 应用后，点击“Socket 连接”按钮，应用会显示一个连接界面，你可以选择搜索到的模拟器 IP 地址，或手动输入电脑 IP 和模拟器端口进行连接。

模拟器默认监听 7768 网络端口，如果该端口被占用（通常是启动了多个模拟器），则自动选择下一个可用端口，并在启动时打印实际使用的端口号。例如：
```bash
$ gx emu
[simulator.socket] MAS TCP server bind port 7768 successful 
```

::: tip
一旦模拟器端口被占用并选择了非 7768 端口号，Glyphix Debug 应用将无法自动搜索到该模拟器，必须手动输入正确的 IP 地址和端口号进行连接。
:::

强烈建议模拟器开启下一节的手机网络代理模式，以免同时使用电脑网络和手机网络。否则可能会干扰 [`@system.interconnect`](/api/system-interconnect.md) 之类依赖手机互联 API 的正常工作。

### 手机网络代理

使用 `-m` 或者 `--mobile-network` 选项可以只启用手机 SDK 的网络代理功能，这类似于真实设备的网络环境。使用此选项时，模拟器不会自动启动目标应用，而是显示一个应用列表界面。

在手动启动应用之前，应通过 Glyphix Debug 手机应用通过“Socket 网络”连接模拟器，然后再点击目标应用。否则应用将无法访问网络。

::: tip
在使用 `-m` 手机网络代理时，可以通过杀死手机调试应用、重新连接模拟器等方式来模拟网络中断的情况。否则模拟器会自动切换到电脑网络。
:::

### 常见连接问题

如果无法通过 Glyphix Debug 应用连接模拟器，请检查电脑和手机是否连接到同一个局域网，且模拟器程序和端口未被防火墙规则屏蔽。如果你连接到了公共网络，那么和可能因为防火墙或者网络隔离而无法连接。

如果你使用了 VPN 或者代理软件，请确保局域网内的流量不被代理，否则也会无法连接。

## 其他操作

### 清除应用数据

你可以使用 [`gx clean`](README.md#gx-clean) 清除模拟器运行时的应用数据，之后再启动模拟器时将从首次安装的状态开始运行。

### 组合命令选项

你可以将多个选项组合在一起使用，例如：
```bash
gx emu -rwt -d default-watch-466x466
```
等效于分开使用
```bash
gx emu -r -w -t -d devault-watch-466x466
gx emu --real-scale --watch --top --device default-watch-466x466
```
建议按 [`gx completion`](#gx-completion) 中介绍的方法安装自动补全脚本，以便在终端中选择设备名称和命令选项。
