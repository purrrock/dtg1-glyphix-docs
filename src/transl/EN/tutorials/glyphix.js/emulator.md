---
icon: watch-import-variant
---
# Simulator and Debugging

To run the simulator, you need to switch to the root directory of your project in the command line and run the `gx emu` subcommand. The Glyphix simulator provides an environment that is highly consistent with the runtime on a real device, allowing you to develop and debug most interfaces and features using the simulator without frequently installing the application onto a physical device.

::: tip
Due to limitations of the current [`glyphix`](https://www.npmjs.com/package/glyphix) npm package, please make sure to configure [`glyphix.config.js`](/tutorials/nodejs.md#glyphix-config-js-配置), otherwise source code line numbers for error messages will not be available when running `gx emu`.
:::


## The `gx emu` Subcommand

Runs the simulator using the device configuration from the last build. This command must be executed in the root directory of the Glyphix project. It automatically builds the project and creates the resource files required by the simulator, so there is no need to run `gx build` beforehand.

#### Command Options

- `-d --device=NAME`: Specifies the name of the simulated device. Defaults to `default` (with a resolution of $410 \times 502\rm px$).
- `-e --emulator-exe=CMD`: Specifies the emulator executable file. Defaults to `glyphix-emu`. Usually, this does not need to be modified.
- `-l --language=NAME`: Specifies the emulator's locale, defaulting to `zh-CN` (Simplified Chinese). You can view the list of supported languages using the `gx list language` command.
- `--target=URI`: Sets the package name or deeplink when the simulator starts, for example, `app://com.example.app/SomePage?query=value` or `com.example.app`.
- `-i --inspector`: Enables the inspector when running the simulator. The inspector is a web page that allows you to debug UI elements in the simulator via a browser.
- `-m --mobile-network`: (Not implemented yet) Enables only the mobile SDK's network proxy in the simulator rather than accessing the network directly.
- `-w --watch`: Watches the project directory while running the simulator, automatically rebuilding and refreshing the simulator interface when source files change.
- `-r --real-scale`: Displays the simulator window at real scale rather than scaling it according to the device resolution. This option is recommended for use on HiDPI screens.
- `-t --top`: Keeps the simulator window always on top.
- `-p --profiling`: Enables profiling mode. Due to significant performance differences between the simulator and the device, this option is usually not very useful.

## Startup Modes

By default, `gx emu` starts the simulator using the device configuration used in the last build. You can also adjust the startup behavior of the simulator using command options.

### Specifying the Device Model

You can use the `-d` or `--device` option to specify the device model you wish to simulate, for example:
```bash
gx emu -d generic-watch-466x466
```
This will start the simulator for the `generic-watch-466x466` device. You can use the `gx list device` command to view the list of installed devices.

If this option is not specified, the device specified last time will be used. When starting the simulator for the first time or after `gx clean`, the `default` device will be used.

### Deeplink Startup

By default, the simulator will start the application of the current project or an application menu interface. However, when debugging the [`onRoute()`](/framework/component/life-cycle.md#onroute) lifecycle function, you might want to start the application via a deeplink to ensure `onRoute()` receives specific parameters. You can use the `--target` option to specify a deeplink, for example:
```bash
gx emu --target app://com.example.app/SomePage?query=value
```
This will start the application with the package name `com.example.app`, and the path (including the root directory `/`, i.e., `/SomePage`) and query fields of the Deeplink URI will be passed to the application's `onRoute()` function.

### Simulating Device Dimensions

By default, the simulator uses the actual pixel resolution of the device, which may make the display size on your computer larger than the actual screen size of the device, making it difficult for developers to confirm whether UI elements (including design drafts) have optimal sizes on the device. The `-r` or `--real-scale` option allows you to simulate based on the real device dimensions:
```bash
gx emu -r
```
When using this option, you do not need to install the application onto a device to confirm the actual size of the UI. However, considering that the DPI of most watches exceeds 300, a 1080p monitor will cause the interface to appear too blurry in real-scale mode. It is recommended to use this option on HiDPI displays (such as 4K monitors or Retina screens on macOS).

::: tip
When using real-scale mode, you should use the `--device` option to specify your desired target device. Note that due to differing DPIs, two devices with the same resolution may have different screen sizes, so the display size in real-scale mode will also vary.
:::

### Auto-Refresh

The `-w` or `--watch` option monitors the project directory while running the simulator, automatically rebuilding and restarting the application when source files change. It is usually recommended to use this in combination with the `--top` option, for example:
```bash
gx emu -wt
```
This keeps the simulator window on top and automatically restarts the application after modifying source files. This is very useful for development and debugging: you can switch directly from your code editor to the simulator without manually restarting the simulator or frequently switching windows.

::: tip
Hot reloading of pages is currently not supported; instead, the entire application is restarted when source files are modified. If you want faster debugging speeds, you can set [`manifest.router.entry`](/framework/application/manifest.md#entry) to the page currently under development, so that every time the application restarts, it will directly enter that page.
:::

## Connecting to a Phone

You can connect to the simulator using the [Glyphix Debug](https://www.pgyer.com/KLeBQFv6) Android mobile app to facilitate debugging real devices and features related to phone-watch interconnection.

### Preparation

You need to install the Glyphix Debug app on your phone and ensure that your phone and computer are on the same local area network (LAN), such as connected to the same Wi-Fi. After starting the simulator and opening the Glyphix Debug app, tap the "Socket Connection" button. The app will display a connection interface where you can select the discovered simulator IP address or manually enter the computer IP and simulator port to connect.

The simulator listens on network port 7768 by default. If this port is occupied (usually when multiple simulators are started), it will automatically select the next available port and print the actually used port number upon startup. For example:
```bash
$ gx emu
[simulator.socket] MAS TCP server bind port 7768 successful 
```

::: tip
Once the simulator port is occupied and a port other than 7768 is selected, the Glyphix Debug app will not be able to automatically discover the simulator. You must manually enter the correct IP address and port number to connect.
:::

It is strongly recommended to enable the mobile network proxy mode of the simulator (covered in the next section) to avoid using the computer network and mobile network simultaneously. Otherwise, it may interfere with the normal operation of APIs that rely on phone-watch interconnection, such as [`@system.interconnect`](/api/system-interconnect.md).

### Mobile Network Proxy

Using the `-m` or `--mobile-network` option enables only the mobile SDK's network proxy feature, simulating a network environment similar to a real device. When using this option, the simulator will not automatically start the target application, but instead display an application list interface.

Before manually starting the application, you should connect the simulator via the "Socket Network" in the Glyphix Debug mobile app, and then tap the target application. Otherwise, the application will not be able to access the network.

::: tip
When using the `-m` mobile network proxy, you can simulate network interruptions by killing the mobile debugging app and reconnecting to the simulator. Otherwise, the simulator will automatically switch to the computer network.
:::

### Common Connection Issues

If you cannot connect to the simulator via the Glyphix Debug app, please check whether your computer and phone are connected to the same LAN, and ensure that the simulator program and port are not blocked by firewall rules. If you are connected to a public network, connection failures may occur due to firewalls or network isolation.

If you are using a VPN or proxy software, please ensure that traffic within the LAN is not proxied, otherwise connection will also fail.

## Other Operations

### Clearing Application Data

You can use [`gx clean`](README.md#gx-clean) to clear the application data of the running simulator. The next time you start the simulator, it will run as if it were in its initial installation state.

### Combining Command Options

You can combine multiple options together, for example:
```bash
gx emu -rwt -d default-watch-466x466
```
This is equivalent to using them separately:
```bash
gx emu -r -w -t -d default-watch-466x466
gx emu --real-scale --watch --top --device default-watch-466x466
```
It is recommended to install the auto-completion script as described in [`gx completion`](#gx-completion) to easily select device names and command options in the terminal.
