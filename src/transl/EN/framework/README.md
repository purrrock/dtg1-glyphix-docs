# Framework

Glyphix is an efficient, lightweight application development framework designed for MCU (Microcontroller Unit) devices, aiming to provide developers with an application development experience close to Web development. Through a declarative UI framework using HTML templates, CSS, and JavaScript, developers can easily build components and pages, and deploy applications to various smart devices (such as smartwatches). Glyphix solves the complexity and stability issues of UI and application development in traditional MCU systems, and provides critical cross-device application development and publishing capabilities, thereby empowering developers with unprecedented flexibility and ease of use.

In addition to an efficient development framework, Glyphix places special emphasis on application safety and stability. We have implemented robust memory management and security mechanisms in the underlying architecture to avoid common memory errors and resource waste, providing developers with a more reliable runtime environment. This safety guarantees application stability and significantly shortens the debugging cycle during development.

At the same time, Glyphix exhibits exceptional performance, capable of running applications with near-native fluency and resource utilization even in resource-constrained MCU environments. The runtime is deeply optimized by the framework, which automatically manages resources and utilizes them efficiently. Therefore, developers can focus on implementing features and optimizing user experience without worrying about performance issues.

## Core Features

### Web Development Experience

- **Declarative UI Paradigm**: Similar to the [Vue Options API](https://vuejs.org/guide/introduction#options-api), using HTML templates, CSS, and JavaScript, allowing developers to write applications in a way close to Web development, lowering the learning curve.
- **Component-Based Development**: Supports modular, component-based development for easy code reuse and maintenance, making application development more efficient and readable.
- **Standardized Interfaces**: Supports Quick App standard system APIs, such as [HTTP Network](/api/system-fetch.md) and [Audio Streaming](/api/system-media.md), making it easy to develop device-agnostic internet applications.

### Cross-Device Support

- **Multi-Device Compatibility**: Glyphix supports running applications on various smart devices (such as smartwatches, smart bands, etc.), achieving true cross-device development and deployment, and reducing the difficulty of adapting to different hardware platforms.
- **Unified Runtime Environment**: Leveraging the capabilities of the Glyphix framework, applications can be automatically managed and executed across different devices while ensuring a consistent user interaction experience.
- **Quick App Standard Support**: Developers can publish applications to other ecosystems that support Quick Apps, further expanding the reach of their applications.

### High Performance

- **Native-Like Performance**: Deeply optimized for MCU environments, achieving near-native fluency and low resource consumption even under limited resources.
- **Native Reactive Framework**: A fully C++ implemented reactive framework and GUI system, avoiding the performance overhead issues of JavaScript implementations.

### Stability

- **Memory Management**: An underlying automated memory management mechanism prevents common memory errors as well as the waste and inefficiency of manual memory allocation.
- **Lifecycle Model**: The application framework provides a comprehensive resource lifecycle model, ensuring no resource leaks after the application exits and reducing stability risks.

### Debugging Support

- **Full-Featured Simulator**: Provides a simulator environment consistent with real devices, including simulation of multi-device screen sizes, enabling application development without physical devices.
- **Hot-Updating Applications**: Developers can update and test applications without restarting the device or flashing firmware, greatly improving development efficiency.

### Publishing Workflow

- **Cross-Device Publishing**: Supports developing an application once and publishing it multiple times to different device platforms. The Glyphix publishing tool supports automatic packaging and optimization for target devices, ensuring stable application execution across devices.
- **App Store Distribution**: Supports application distribution through after-market channels such app stores. Users can browse, download, and install applications without OTA firmware upgrades.
- **Independent Application Management**: Supports independent application installation and uninstallation without the need for unified firmware integration and version control.

## Comparison with Other Solutions

### Embedded C/C++ GUI Libraries

Glyphix is not just a GUI library providing a C++ API, but a complete standard application runtime framework. It not only provides UI rendering capabilities but also manages application lifecycles, event handling, and data binding, giving it more comprehensive application execution and management capabilities.

Developing application logic using C/C++ typically requires recompiling and deploying the entire program, whereas Glyphix supports hot-updating of applications, allowing developers to quickly release and test updates without restarting the device, significantly enhancing development and maintenance efficiency.

On the other hand, traditional C/C++ development methods usually require customization for different hardware and operating systems, whereas Glyphix provides a unified runtime environment, enabling a consistent application development experience across various MCU devices and reducing adaptation efforts.

### System-Level Solutions

Complete firmware system solutions typically cover the entire device operating system, drivers, communications, and all other functions, whereas Glyphix focuses on providing an efficient application runtime framework. It does not replace or refactor the device's firmware system; instead, it acts as a component on the device to manage and run applications, ensuring the independence and flexibility of applications relative to the firmware system.

In complete firmware systems, applications are usually tightly coupled with the system, leading to high development, update, and maintenance costs. As an independent application runtime, Glyphix allows developers to quickly add, update, and manage applications in a standard environment, reducing complexity and maintenance costs.

Furthermore, firmware systems are often deeply bound to specific hardware, whereas Glyphix can run across different systems, providing a unified development and execution environment to achieve true cross-device support.

### Other Application Frameworks

Unlike application runtimes such as Web, React Native, or Flutter, Glyphix—while providing a Vue-like development experience—is specifically designed for resource-constrained MCU environments, ensuring efficient operation under limited memory and computing power. It delivers near-native performance with lower resource consumption, adapting to the needs of small embedded devices.

Other application runtime frameworks typically require more powerful hardware environments (such as smartphones or computers) to run, and both startup and operation demand significantly more system resources. In contrast, the Glyphix runtime is extremely lightweight, capable of running on small devices like smartwatches with very low power consumption and memory footprint.

## Developer Benefits

Glyphix is a framework friendly to Web developers, allowing them to use familiar HTML, CSS, and JavaScript for development without needing an in-depth study of C/C++ languages and complex MCU hardware development knowledge. This lowers the barrier to MCU application development, enabling more Web developers to get started quickly and saving learning costs and time.

### Improving Development Efficiency

- **Web Development Experience**: Through a Web-like tech stack and hot-update support, developers can write MCU applications just like Web apps, making full use of their existing skills and dramatically increasing efficiency.
- **Develop Once, Run Across Devices**: Glyphix provides robust cross-device compatibility. Developers only need to write code once, and the system automatically adapts and optimizes resources based on different device characteristics, eliminating the need for independent development for each device. This effectively reduces the maintenance costs and complexity brought by device fragmentation.
- **Deeply Optimized System**: Developers do not need to invest massive effort into optimizing interaction fluency and stutter issues, nor do they need to constantly worry about device crashes, allowing them to focus entirely on feature implementation and user experience.

### Continuous Iteration

- **Long-Term Availability of Applications**: Glyphix's cross-device features and long-term support for MCU devices ensure that applications can run continuously across multiple generations of devices. Even if a specific device is discontinued, developers do not need to worry about the application losing its runtime environment and can easily migrate to other devices, extending the application's lifecycle.
- **Compatibility with Future Devices**: The framework will continuously iterate and update to maintain compatibility with new hardware, allowing developers' applications to automatically adapt to future devices and avoiding extra maintenance costs caused by hardware updates.
- **Tooling and Documentation Support**: Alongside development tools, documentation will be continuously maintained along with framework updates to ensure accuracy and timeliness, enabling developers to always access the latest framework features and best practices to support continuous application iteration and optimization.