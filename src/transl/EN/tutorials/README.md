---
title: Glyphix Application Development Tutorial
index: false
icon: routes
category:
  - Guide
---

## What is Glyphix

Glyphix is an efficient, lightweight application development framework designed for MCU (Microcontroller Unit) devices. It provides developers with a declarative UI development paradigm similar to the Web ecosystem: through HTML templates, CSS, and JavaScript, developers can easily build pages and components, and deploy applications to various smart devices (such as smartwatches).

For more information, please refer to the [Framework](/framework/README.md) chapter.

### Web-like Framework

Unlike traditional MCU firmware development, Glyphix is closer to frameworks based on the Web technology stack. Application developers need to be familiar with JavaScript, CSS, and basic HTML knowledge. You do not need to master the complete Web development technology stack, such as browser DOM, standard HTML tags, and complex build toolchains. However, if you are familiar with Web UI frameworks such as [Vue.js](https://vuejs.org/) ([Options API](https://vuejs.org/guide/introduction#options-api)), you will find it very easy to get started with Glyphix.

::: tip
It should be noted that Glyphix is not a "low-code" platform. During the development process, you will still encounter challenges such as logic abstraction, interface organization, user experience, and performance trade-offs. Therefore, a solid foundation in JavaScript and a good frontend mindset will help you fully unleash the potential of Glyphix.
:::

### Declarative UI Framework

Traditional interface development is usually imperative: it requires step-by-step function calls to create controls, update states, and refresh interfaces. This approach is flexible, but business and interface logic are highly coupled. As the application scale expands, the code quickly becomes complex and difficult to maintain. Patterns such as MVC and MVVM were proposed precisely to solve this complexity.

Glyphix adopts a declarative UI paradigm. Developers only need to describe "what the interface should look like," and the framework automatically completes rendering and updates based on data and state changes. This approach significantly reduces the complexity of interface logic and state management, allowing developers to focus their main energy on functionality and interaction design rather than maintaining UI hierarchies and refresh processes.

### Application Container

Glyphix is not just a UI framework; it also provides functions such as application lifecycle management, permission isolation, and system APIs. Applications run in an independent container and are isolated from each other, ensuring system stability and security.

Please read the [Getting Started](getting-started.md) tutorial to start Glyphix application development right away.

## Other Questions

### Do I need to be familiar with MCU and embedded development?

Application developers generally do not need to understand the specific knowledge of MCU and embedded development. However, you should have some understanding of the resource constraints of the device. For example, the memory capacity of an MCU is usually only a few megabytes, and the memory for running JavaScript code is also limited. This means you might encounter situations where you cannot request very large JSON data from the network, or you cannot encode an entire image into Base64 and retrieve it via a GET request.

These limitations, which are completely different from Web development, are indeed caused by the limited resources of MCU devices, but they are not part of typical MCU knowledge systems.

Intuitively speaking, it is best to confirm whether the application experience is good enough by running the app on the device. You can run it on real hardware multiple times at different stages of development to ensure the experience.

### Do I need to use C/C++ for application development?

Glyphix application development uses HTML, CSS, and JavaScript exclusively, so there is no need to use the C/C++ language.

### How can embedded developers get started with Glyphix application development?

Embedded developers can follow the [Getting Started](getting-started.md) tutorial to gradually understand the core concepts of Glyphix. The framework adopts a componentization and data-binding mechanism similar to the Vue Options API. This may be somewhat different for readers accustomed to imperative GUIs such as [LVGL](https://lvgl.io/) or Qt widgets, but Glyphix's declarative design also brings a more intuitive interface control experience.

Developers do not need to fully master HTML, CSS, and JavaScript, but familiarity with basic JavaScript syntax (such as variables, conditional statements, function calls, etc.) will help in understanding Glyphix's rendering logic and event handling. You can familiarize yourself with these contents and accelerate your development process through sample code and practical operations in the tutorials and documentation.

### Do I need to pay attention to application performance optimization?

Our framework has been deeply optimized for the resource constraints of embedded systems, allowing it to adapt well to various hardware environments. Most applications can achieve sufficiently smooth and stable running performance under default settings, so you generally do not need to spend extra time on performance optimization.

If there is a need to understand specific optimization solutions in the future, we will provide dedicated performance optimization documentation to help developers further improve the runtime efficiency of their applications.

### Is the Glyphix environment different from a browser?

Yes, the Glyphix environment is significantly different from a browser. Glyphix does not have a DOM structure like browsers, nor does it provide objects such as `window` or `document`. Instead, it directly and exclusively provides a set of declarative interfaces through which developers can perform component development and interface interaction. This design simplifies the development process and is more suitable for embedded environments.