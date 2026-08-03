# Framework

Glyphix is an efficient, lightweight application development framework designed for MCU (Microcontroller Unit) devices, aiming to provide developers with an application development experience close to Web development. Through a declarative UI framework using HTML templates, CSS, and JavaScript, developers can easily build components and pages, and publish applications to various smart devices (such as smart watches). Glyphix solves the complexity and stability issues of UI and application development in traditional MCU systems, and provides critical cross-device application development and publishing capabilities, thereby empowering developers with unprecedented flexibility and ease of use.

In addition to an efficient development framework, Glyphix places special emphasis on application safety and stability. We have implemented robust memory management and security mechanisms in the underlying architecture to avoid common memory errors and resource waste, providing developers with a more reliable runtime environment. This security guarantees the operational stability of applications and significantly shortens the debugging cycle during development.

At the same time, Glyphix boasts exceptional performance, capable of running applications with near-native fluency and resource utilization even in resource-constrained MCU environments. The runtime has been deeply optimized by the framework, automatically managing resources and utilizing them efficiently. Consequently, developers can focus on feature implementation and user experience optimization without worrying about performance issues.

## Core Features

### Web Development Experience

- **Declarative UI Paradigm**: Similar to [Vue Options API](https://vuejs.org/guide/introduction#options-api), using HTML templates, CSS, and JavaScript, allowing developers to write applications in a way close to Web development and lowering the learning curve.
- **Component-Based Development**: Supports modular and component-based development, facilitating code reuse and maintenance, and making application development more efficient and readable.
- **Standardized Interfaces**: Supports Quick App standard system APIs, such as [HTTP Network](/api/system-fetch.md) and [Audio Streaming](/api/system-media.md), making it easy to develop device-agnostic internet applications.

### Cross-Device Support

- **Multi-Device Compatibility**: Glyphix supports running applications on various smart devices (such as smart watches, smart bands, etc.), achieving true cross-device development and deployment, and reducing the difficulty of adapting to different hardware platforms.
- **Unified Runtime Environment**: Leveraging Glyphix framework capabilities, applications can be automatically managed and executed across different devices, ensuring a consistent application interaction experience.
- **Quick App Standard Support**: Developers can publish applications to other ecosystems that support Quick Apps, further expanding the application's coverage.

### High Performance

- **Native-Level Performance**: Deeply optimized for MCU environments, achieving near-native fluency and low resource consumption even under limited resources.
- **Native Reactive Framework**: A reactive framework and GUI system implemented entirely in C++, avoiding the performance overhead issues of JavaScript implementations.

### Stability

- **Memory Management**: An underlying automated memory management mechanism prevents common memory errors, as well as the waste and inefficiency of manual memory allocation.
- **Lifecycle Model**: The application framework provides a comprehensive resource lifecycle model to ensure no resource leaks after the application exits, reducing stability risks.

### Debugging Support

- **Full-Featured Simulator**: Provides a simulator environment consistent with real devices, including simulations of multi-device screen sizes, enabling application development without physical devices.
- **Hot-Reloading Applications**: Developers can update and test applications without restarting the device, completely eliminating the need to flash firmware, which greatly improves development efficiency.

### Publishing Workflow

- **Cross-Device Publishing**: Supports developing an application once and publishing it multiple times across different device platforms. The Glyphix publishing tool supports automatic packaging and optimization for target devices, ensuring applications run stably on various devices.
- **App Store Distribution**: Supports aftermarket channel distribution such as app stores. Users can browse, download, and install applications without OTA firmware upgrades.
- **Independent Application Management**: Supports independent application installation and uninstallation, eliminating the need for unified firmware integration and version control.

## Comparison with Other Solutions

### Embedded C/C++ GUI Libraries

Glyphix is not just a GUI library providing C++ APIs, but a complete standard application runtime framework. It not only provides UI rendering capabilities but also manages application lifecycles, event handling, and data binding, endowing it with more complete application running and management capabilities.

Developing application logic using C/C++ typically requires recompiling and redeploying the entire program, whereas Glyphix supports application hot-reloading, allowing developers to quickly release and test updates without restarting the device, greatly enhancing development and maintenance efficiency.

On the other hand, traditional C/C++ development approaches usually require customization for different hardware and operating systems, whereas Glyphix provides a unified runtime environment capable of delivering a consistent application development experience across multiple MCU devices, reducing adaptation work.

### System-Level Solutions

Complete firmware system solutions typically cover the entire device OS, drivers, communications, and all other functions, whereas Glyphix focuses on providing an efficient application runtime framework. It does not replace or reconstruct the device's firmware system; instead, it acts as a component on the device to manage and run applications, ensuring the independence and flexibility of the applications relative to the firmware system.

In complete firmware systems, applications are usually tightly coupled with the system, resulting in high costs for development, updates, and maintenance. In contrast, as an independent application runtime, Glyphix allows developers to quickly add, update, and manage applications in a standard environment, reducing complexity and maintenance costs.

Furthermore, firmware systems are often deeply bound to specific hardware, whereas Glyphix can run across different systems, providing a unified development and runtime environment to achieve true cross-device support.

### Other Application Frameworks

Unlike application runtimes like Web, React Native, or Flutter, Glyphix—while offering a Vue-like development experience—is specifically designed for resource-constrained MCU environments, ensuring efficient operation even when memory and computing power are limited. It delivers near-native performance with lower resource consumption, adapting to the needs of small embedded devices.

Other application runtimes usually require execution in more powerful hardware environments (such as mobile phones or PCs), requiring more system resources for startup and operation. In contrast, the Glyphix runtime is extremely lightweight, capable of running on small devices like smart watches with ultra-low power consumption and memory footprint.

## Benefits for Developers

Glyphix is a friendly framework oriented toward Web developers. Developers can use familiar HTML, CSS, and JavaScript for development, eliminating the need to deeply learn C/C++ languages and complex MCU hardware development knowledge. This lowers the barrier to entry for MCU application development, enabling more Web developers to get started quickly and saving learning costs and time.

### Improving Development Efficiency

- **Web Development Experience**: Through a Web-like technology stack and hot-reloading support, developers can write MCU applications just like Web apps, fully leveraging their existing skills and dramatically increasing efficiency.
- **Write Once, Run Across Devices**: Glyphix provides robust cross-device compatibility. Code needs to be written only once, and the system automatically adapts and optimizes resources based on different device characteristics, without requiring independent development for each device. This effectively reduces the maintenance costs and complexity brought by device fragmentation.
- **Deeply Optimized System**: Developers do not need to invest a massive amount of energy into optimizing interaction fluency and lag issues, nor do they need to constantly watch out for device crashes, allowing them to focus entirely on feature implementation and user experience.

### Continuous Iteration

- **Long-Term Usability of Applications**: Glyphix's cross-device capabilities and long-term support for MCU devices ensure that applications can run continuously across multiple generations of devices. Even if a specific device is discontinued, developers do not need to worry about the application losing its runtime environment and can easily migrate to other devices, extending the application's lifecycle.
- **Compatibility with Future Devices**: The framework will continuously iterate and update to maintain compatibility with new hardware, and developers' applications can automatically adapt to future devices, avoiding extra maintenance costs caused by hardware updates.
- **Tooling and Documentation Support**: Alongside development tools, documentation will be continuously maintained along with framework updates to ensure accuracy and timeliness, enabling developers to always access the latest framework features and best practices to empower continuous application iteration and optimization.