---
title: Glyphix Application Development Tutorial
index: false
icon: routes
category:
  - Guide
---

## What is Glyphix

Glyphix is an efficient and lightweight application development framework designed for MCU (Microcontroller Unit) devices. It provides developers with a declarative UI development paradigm similar to the Web ecosystem: through HTML templates, CSS, and JavaScript, developers can easily build pages and components, and deploy applications to various smart devices (such as smartwatches).  

For more information, please refer to the [Framework](/framework/README.md) section.

### Web-like Framework

Unlike traditional MCU firmware development, Glyphix is closer to frameworks based on Web technology stacks. Application developers need to be familiar with JavaScript, CSS, and basic HTML knowledge. You do not need to master the complete Web development technology stack, such as the browser DOM, standard HTML tags, and complex build toolchains. However, if you are familiar with Web UI frameworks such as [Vue.js](https://vuejs.org/) ([Options API](https://vuejs.org/guide/introduction#options-api)), you will find it very easy to get started with Glyphix.

::: tip
It should be noted that Glyphix is not a "low-code" platform. During the development process, you will still encounter challenges such as logic abstraction, interface organization, user experience, and performance trade-offs. Therefore, mastering a solid foundation in JavaScript and a good frontend mindset will help you fully unleash the potential of Glyphix.
:::

### Declarative UI Framework

Traditional interface development is usually imperative: it requires step-by-step function calls to create controls, update states, and refresh interfaces. While flexible, this approach leads to tight coupling between business and interface logic. As the application scale grows, the code quickly becomes complex and difficult to maintain. Patterns such as MVC and MVVM were proposed precisely to solve this complexity.  

Glyphix adopts a declarative UI paradigm. Developers only need to describe "what the interface should look like," and the framework automatically completes rendering and updates based on data and state changes. This approach significantly reduces the complexity of interface logic and state management, allowing developers to focus primarily on functionality and interaction design rather than maintaining the UI hierarchy and refresh pipeline.

### Application Container

Glyphix is not just a UI framework; it also provides features such as application lifecycle management, permission isolation, and system APIs. Applications run within independent containers and are isolated from one another, ensuring system stability and security.

Please read the [Getting Started](getting-started.md) tutorial to start developing Glyphix applications right away.

## Other Questions

### Do I need to be familiar with MCU and embedded development?

Application developers generally do not need to understand the specific details of MCU and embedded development. However, they should have some awareness of device resource constraints. For example, MCU memory capacity is usually only a few megabytes, and there are also limits on the memory available for running JavaScript code. This means you might encounter situations where you cannot request very large JSON data from the network, or you cannot encode an entire image into Base64 and fetch it via a GET request.

These limitations, which are completely different from Web development, are indeed caused by the limited resources of MCU devices, but they are not part of typical MCU knowledge systems.

Intuitively, the best way to confirm whether your application's experience is good enough is to run it on the actual device. You can run it on real hardware multiple times at different stages of development to ensure the experience.

### Do I need to use C/C++ for application development?

Glyphix application development uses HTML, CSS, and JavaScript exclusively, so there is no need to use C/C++.

### How can embedded developers get started with Glyphix application development?

Embedded developers can follow the [Getting Started](getting-started.md) tutorial to gradually understand the core concepts of Glyphix. The framework adopts componentization and data-binding mechanisms similar to the Vue Options API. This may feel a bit different for readers accustomed to imperative GUIs like [LVGL](https://lvgl.io/) or Qt widgets, but Glyphix's declarative design also brings a more intuitive interface control experience.

Developers do not need to completely master HTML, CSS, and JavaScript, though familiarity with basic JavaScript syntax (such as variables, conditional statements, and function calls) will help in understanding Glyphix's rendering logic and event handling. You can familiarize yourself with these aspects through sample code and practical operations in tutorials and documentation to accelerate your development workflow.

### Do I need to focus on application performance optimization?

Our framework has been deeply optimized for the resource constraints of embedded systems, making it well-suited for a variety of hardware environments. Most applications can achieve sufficiently smooth and stable running performance under default settings, so there is usually no need to spend extra time on performance optimization.

If there is a need in the future to dive deeper into specific optimization solutions, we will provide dedicated performance optimization documentation to help developers further improve application runtime efficiency.

### Is the Glyphix environment different from a browser?

Yes, the Glyphix environment is significantly different from a browser. Glyphix does not have the DOM structure found in browsers, nor does it provide objects like `window` or `document`. Instead, it directly and exclusively provides a set of declarative interfaces through which developers can perform component development and interface interaction. This design simplifies the development process and is more suitable for embedded environments.