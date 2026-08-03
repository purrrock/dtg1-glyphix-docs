---
icon: watch-import-variant
---
# Simulator and debugging

To run the emulator, you need to switch to the root directory of your project on the command line and run the `gx emu` subcommand to start the emulator. The Glyphix simulator has a highly consistent environment with the real device runtime, so you can use the simulator to develop and debug most interfaces and functions without the need to frequently install applications on the real device.

::: tip
Due to the limitations of the current [`glyphix`](https://www.npmjs.com/package/glyphix) npm package, please be sure to configure [`glyphix.config.js`](/doc_en/nodejs.md#glyphix-config-js-configuration), otherwise the source code line number of the error message cannot be seen when executing `gx emu`.
:::

## `gx emu` subcommand

Run the emulator using the last build target device configuration. This command needs to be executed in the root directory of the Glyphix project. It automatically builds the project and creates the resource files required by the emulator, so there is no need to perform `gx build` first.

#### Command options

- `-d --device=NAME`: Specify the simulated device name, the default is `default` (resolution is $410 \times 502\rm px$).
- `-e --emulator-exe=CMD`: Specify the executable file of the emulator, the default is `glyphix-emu`. Usually no modification is required.
- `-l --language=NAME`: Specify the language environment of the simulator, the default is `zh-CN` (Simplified Chinese). The list of supported languages ​​can be viewed through the `gx list language` command.
- `--target=URI`: Set the package name or deeplink when the emulator is started, such as `app://com.example.app/SomePage?query=value` or `com.example.app`.
- `-i --inspector`: Enables the inspector when running the simulator. The inspector is a web page that can debug interface elements in the simulator in the browser.
- `-m --mobile-network`: (not yet implemented) Enable the mobile SDK's network proxy only in the emulator, without direct access to the network.
- `-w --watch`: Monitor the project directory when running the simulator, and automatically rebuild and refresh the simulator interface when the source files change.
- `-r --real-scale`: Display the emulator window using real size instead of scaling the display to the device resolution. This option is recommended for HiDPI screens.
- `-t --top`: Keep the emulator window on top.
- `-p --profiling`: Enable profiling mode. Due to the large differences in emulator and device performance, this option is generally not very useful.

## Startup mode

By default, `gx emu` will start the emulator with the device configuration it was last built with. You can also adjust the emulator's startup behavior through command options.

### Specify device model

Use the `-d` or `--device` option to specify the device model you wish to emulate, for example:
```bash
gx emu -d generic-watch-466x466
```
Will start the emulator for the device `generic-watch-466x466`. You can view the list of installed devices using the `gx list device` command.

If this option is not specified, the last device specified will be used. The `default` device will be used when starting the emulator for the first time or after `gx clean`.

### Deeplink startup

By default, the simulator will launch the application of the current project, or launch an application menu interface. But when debugging the [`onRoute()`](/framework/component/life-cycle.md#onroute) lifecycle function, you may want to launch the application through a deeplink to ensure that `onRoute()` receives specific parameters. Deeplinks can be specified using the `--target` option, for example:
```bash
gx emu --target app://com.example.app/SomePage?query=value
```
This will start the application with the package name `com.example.app`, and the path and query fields of the Deeplink URI will be passed to the `onRoute()` function of the application.

### Analog device size

By default, the simulator uses the actual pixel resolution of the device, which causes the display size on the computer to be larger than the actual screen size of the device and makes it difficult for developers to confirm that UI elements (including design drafts) are sized optimally on the device. The `-r` or `--real-scale` option can simulate real device dimensions:
```bash
gx emu -r
```
When using this option, you don't need to install the app on the device to confirm the actual size of the UI. However, considering that the DPI of most watches exceeds 300, a 1080p display will cause the interface to be too blurry when using real-scale mode. It is recommended to use this option on HiDPI displays (such as 4K displays, or Retina screens on macOS).

::: tip
When using real-scale mode, you should specify the target device you wish to emulate via the `--device` option. It is worth noting that due to different DPI, two devices with the same resolution may have different screen sizes, so the display sizes in real-scale mode will also be different.
:::

### Automatic refresh

The `-w` or `--watch` option can monitor the project directory when running the simulator and automatically rebuild and restart the application when the source files change. It is usually recommended to use it with the `--top` option, for example:
```bash
gx emu -wt
```
This keeps the simulator window on top and automatically restarts the application after modifying the source file. This is very useful for development and debugging: switch directly from the code editor to the simulator, no need to manually restart the simulator, and no need to switch windows frequently.

::: tip
Currently, hot update pages are not supported. Instead, the entire application is restarted after modifying the source file. If you want faster debugging, you can adjust [`manifest.router.entry`](/framework/application/manifest.md#entry) to the page under development, so that you will go directly to the page every time you restart the application.
:::

## Connect to mobile phone

You can connect to the emulator through the [Glyphix Debug](https://www.pgyer.com/KLeBQFv6) Android mobile application to facilitate debugging functions related to the real device and mobile phone interconnection.

### Preparation

You need to install the Glyphix Debug app on your phone and make sure your phone and computer are on the same LAN, such as connected to the same Wi-Fi. After starting the simulator and opening the Glyphix Debug application, click the "Socket Connection" button. The application will display a connection interface. You can select the searched simulator IP address, or manually enter the computer IP and simulator port to connect.

The emulator listens to network port 7768 by default. If the port is occupied (usually multiple emulators are started), the next available port is automatically selected and the actual port number used is printed when starting. For example:
```bash
$ gx emu
[simulator.socket] MAS TCP server bind port 7768 successful
```

::: tip
Once the emulator port is occupied and a non-7768 port number is selected, the Glyphix Debug application will not be able to automatically search for the emulator and must manually enter the correct IP address and port number to connect.
:::

It is strongly recommended that the simulator turns on the mobile network proxy mode in the next section to avoid using the computer network and mobile network at the same time. Otherwise, it may interfere with the normal work of [`@system.interconnect`](/api/system-interconnect.md) and other dependent mobile phone interconnection APIs.

### Mobile network proxy

Use the `-m` or `--mobile-network` option to enable only the network proxy function of the mobile SDK, which is similar to the network environment of a real device. When using this option, the emulator does not automatically launch the target application, but displays an application list interface.

Before manually launching the app, you should connect to the emulator via "Socket Network" via the Glyphix Debug mobile app and then click on the target app. Otherwise the application will not be able to access the network.

::: tip
When using `-m` mobile network proxy, you can simulate network interruption by killing the mobile debugging application and reconnecting the emulator. Otherwise the simulator will automatically switch to the computer network.
:::

### Common connection issues

If you cannot connect to the emulator through the Glyphix Debug app, please check whether the computer and mobile phone are connected to the same LAN, and the emulator program and port are not blocked by firewall rules. If you are connected to a public network, you may not be able to connect due to a firewall or network isolation.

If you use VPN or proxy software, please ensure that the traffic within the LAN is not proxied, otherwise you will not be able to connect.

## Other operations

### Clear application data

You can use [`gx clean`](README.md#gx-clean) to clear the application data when the emulator is running. Then when you start the emulator, it will start from the state of first installation.

### Combine command options

You can combine multiple options together, for example:
```bash
gx emu -rwt -d default-watch-466x466
```
Equivalent to using separately
```bash
gx emu -r -w -t -d devault-watch-466x466
gx emu --real-scale --watch --top --device default-watch-466x466
```
It is recommended to install an auto-completion script as described in [`gx completion`](#gx-completion) to select device names and command options in the terminal.