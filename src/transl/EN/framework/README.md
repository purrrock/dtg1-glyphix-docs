# frame


Glyphix is ​​an efficient, lightweight application development framework for MCU (microcontroller) devices, aiming to provide developers with an application development solution that is close to the web development experience. With a declarative UI framework using HTML templates, CSS, and JavaScript, developers can easily build components and pages and publish apps to a variety of smart devices, such as smartwatches. Glyphix solves the complexity and stability issues of UI and application development for traditional MCU systems and provides critical cross-device application development and publishing capabilities, giving developers unprecedented flexibility and ease of use.


In addition to an efficient development framework, Glyphix pays special attention to the safety and stability of applications. We have implemented powerful memory management and security mechanisms in the underlying architecture to avoid common memory errors and resource waste, and provide developers with a more reliable runtime environment. This kind of security ensures the stability of application operation and will also significantly shorten the debugging cycle during the development process.


At the same time, Glyphix excels in performance, running applications with near-native fluency and resource usage even in resource-constrained MCU environments. The framework has deeply optimized the runtime, automatically manages resources and utilizes them efficiently. Therefore, developers can focus on implementing features and optimizing user experience without worrying about performance issues.


## Core features


### Web development experience


- **Declarative UI paradigm**: Similar to [Vue Options API](https://vuejs.org/guide/introduction#options-api), using HTML templates, CSS and JavaScript, allowing developers to write applications in a way close to web development, reducing learning costs.
- **Component-based development**: Supports modular and component-based development methods to facilitate code reuse and maintenance, making application development efficiency and readability higher.
- **Standardized interface**: Supports Quick App standard system APIs, such as [HTTP network](/api/system-fetch.md) and [audio streaming](/api/system-media.md) bodies, which can easily develop device-independent Internet applications.


### Cross-device support


- **Multi-device compatibility**: Glyphix supports applications running on a variety of smart devices (such as smart watches, bracelets, etc.), achieving true cross-device development and deployment, and reducing the difficulty of adapting to different hardware platforms.
- **Unified runtime** environment: With the help of Glyphix framework capabilities, applications can be automatically managed and executed on different devices and ensure a consistent application interaction experience.
- **Quick App Standard** support: Developers can publish their applications to other ecosystems that support Quick Apps to further expand the coverage of their applications.


### Efficient performance


- **Native-level performance**: Deeply optimized for the MCU environment, it can achieve near-native fluency and low resource usage even when resources are limited.
- **Native responsive framework**: A responsive framework and GUI system implemented entirely in C++, avoiding the performance overhead issues of JavaScript implementation.


### stability


- **Memory Management**: The underlying automatic memory management mechanism prevents common memory errors and the waste and inefficiency of manual allocation of memory.
- **Life cycle model**: The application framework provides a complete resource life cycle model to ensure that there is no resource leakage after the application exits, reducing stability risks.


### Debugging support


- **Full-featured simulator**: Provides a simulator environment that is consistent with real devices, including simulation of multiple device screen sizes. Applications can be developed without a real device.
- **Hot update application**: Developers can update and test applications without restarting the device, and there is no need to flash the firmware at all, which greatly improves development efficiency.


### Release process


- **Cross-device publishing**: Supports developing applications once and publishing them to different device platforms multiple times. Glyphix publishing tools support automatic packaging and optimization for target devices to ensure that applications run stably on each device.
- **App Store Distribution**: Supports app distribution through post-installation channels such as app stores. Users can browse, download and install apps without the need for OTA firmware upgrades.
- **Independent application management**: Supports independent application installation and uninstallation without unified firmware integration and version control.


## Comparison with other options


### Embedded C/C++ GUI library


Glyphix is ​​not a GUI library that provides a C++ API, but a standard application runtime framework. It not only provides UI rendering capabilities, but also manages the application life cycle, event processing, and data binding, giving it more complete application running and management capabilities.


Using C/C++ to develop application logic usually requires recompiling and deploying the entire program. However, Glyphix supports hot updates of applications. Developers can quickly release and test updates without restarting the device, which greatly improves development and maintenance efficiency.


On the other hand, traditional C/C++ development methods usually require customization for different hardware and operating systems, while Glyphix provides a unified runtime environment that can achieve a consistent application development experience on a variety of MCU devices and reduce adaptation work.


### system level solution


A complete firmware system solution usually covers all functions such as the entire device operating system, drivers, and communications, while Glyphix focuses on providing an efficient application runtime framework. It does not need to replace or reconstruct the device's firmware system, but serves as a component on the device to manage and run applications, ensuring the independence and flexibility of applications and firmware systems.


In a complete firmware system, applications are usually deeply coupled with the system, and the costs of development, updates, and maintenance are high. Glyphix runs as an independent application, allowing developers to quickly add, update and manage applications in a standard environment, reducing complexity and maintenance costs.


In addition, firmware systems are often deeply bound to specific hardware, while Glyphix can run in different systems, providing a unified development and operating environment to achieve true cross-device support.


### Other application frameworks


Unlike application runtime frameworks such as Web, React Native or Flutter, although Glyphix provides a development experience similar to Vue, it is designed for resource-constrained MCU environments to ensure that it can still run efficiently even with limited memory and computing power. It provides near-native performance with lower resource usage and adapts to the needs of small embedded devices.


Other application runtime frameworks usually need to run in more powerful hardware environments (such as mobile phones or computers), requiring more system resources to start and run. The Glyphix runtime is extremely lightweight and can run on small devices such as smart watches with extremely low power consumption and memory usage.


## Developer revenue


Glyphix is ​​a friendly framework for web developers. Developers can use familiar HTML, CSS and JavaScript to develop without having to learn C/C++ language and complex MCU hardware development knowledge in depth. This lowers the threshold for MCU application development, allowing more web developers to get started quickly, saving learning costs and time.


### Improve development efficiency


- **Web development experience**: Through a web-like technology stack and hot update support, developers can write MCU applications just like developing web applications, making full use of existing skills and greatly improving efficiency.
- **Develop once, run across devices**: Glyphix provides strong cross-device compatibility. You only need to write code once, and the system will automatically adapt and optimize resources according to the characteristics of different devices. There is no need to develop independently for each device. This effectively reduces maintenance costs and complexity caused by equipment fragmentation.
- **Deeply optimized system**: Developers do not need to invest a lot of energy in optimizing interaction smoothness and lag issues, nor do they need to constantly pay attention to device crashes, so they can focus on function implementation and user experience.


### Continuous iteration


- **Long-term application availability**: Glyphix’s cross-device nature and long-term support for MCU devices ensure that applications can continue to run on multiple generations of devices. Even if a certain device is withdrawn from the market, developers do not need to worry about losing the running environment of the application and can easily migrate it to other devices to extend the life cycle of the application.
- **Compatibility of future devices**: The framework will continue to be iteratively updated to maintain compatibility with new hardware. Developers' applications can automatically adapt to future devices to avoid additional maintenance costs caused by hardware updates.
- **Tools and documentation support**: In addition to development tools, documentation will also be continuously maintained as the framework is updated to ensure accuracy and timeliness, so that developers can always access the latest framework features and best practices, helping with continuous iteration and optimization of applications.
