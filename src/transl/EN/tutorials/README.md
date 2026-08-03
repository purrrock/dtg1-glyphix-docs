---
title: Glyphix 应用开发教程
index: false
icon: routes
category:
  - Guide
---

## What is Glyphix

Glyphix is ​​an efficient, lightweight application development framework for MCU (microcontroller) devices. It provides developers with a declarative UI development paradigm similar to the Web ecosystem: through HTML templates, CSS, and JavaScript, developers can easily build pages and components and publish applications to various smart devices (such as smart watches).

For more information, please refer to the [Framework](/framework/README.md) chapter.

### Web-like framework

Unlike traditional MCU firmware development, Glyphix is ​​closer to a framework based on a web technology stack. App developers need to be familiar with JavaScript, CSS, and basic HTML knowledge. You don’t need to master the complete web development technology stack, such as browser DOM, standard HTML tags, and complex build tool chains. But if you are familiar with Web UI frameworks such as [Vue.js](https://vuejs.org/) ([Options API](https://vuejs.org/guide/introduction#options-api)), it will be easy to get started with Glyphix.

::: tip
To be clear, Glyphix is not a “low-code” platform. During the development process, you will still encounter challenges such as logic abstraction, interface organization, user experience, and performance trade-offs. Therefore, mastering a solid JavaScript foundation and a good front-end way of thinking will help you fully realize the potential of Glyphix.
:::

### Declarative UI framework

Traditional interface development is usually imperative: functions need to be called step by step to create controls, update state, and refresh the interface. This method is very flexible, but the business and interface logic are highly coupled. As the application scale expands, the code will quickly become complex and difficult to maintain. Patterns such as MVC and MVVM were proposed precisely to solve this complexity.

Glyphix adopts the declarative UI paradigm. Developers only need to describe "what the interface should look like", and the framework will automatically complete rendering and updates based on changes in data and state. This approach greatly reduces the complexity of interface logic and state management, and allows developers to focus on function and interaction design instead of maintaining the UI hierarchy and refresh process.

### Application container

Glyphix is ​​not just a UI framework, it also provides functions such as application life cycle management, permission isolation and system API. Applications run in an independent container and are isolated from each other to ensure system stability and security.

Please read the [Quick Start](getting-started.md) tutorial to get started with Glyphix application development immediately.

## Other questions

### Need to be familiar with MCU and embedded development?

Application developers generally do not need specific knowledge of MCUs and embedded development. But you should have some understanding of the device's resource limitations. For example, the memory capacity of MCUs is usually only a few MB, and there are also limits on the memory for running JavaScript code. This means that there may be an inability to request very large JSON data from the network, or to encode the entire image as Base64 and obtain it through a GET request.

These limitations, which are completely different from web development, are indeed caused by the limited resources of the MCU device, but this is not included in the typical MCU body of knowledge.

Intuitively, it's best to confirm that the app experience is good enough by running the app on the device. You can run it multiple times on a real device at different stages of development to ensure the best experience.

### Should C/C++ be used for application development?

Glyphix application development is done entirely using HTML, CSS, and JavaScript, so there is no need to use C/C++ languages.

### How can embedded developers get started with Glyphix application development?

Embedded developers can use this tutorial [Quick Start](getting-started.md) to gradually understand the core concepts of Glyphix. The framework uses a componentization and data binding mechanism similar to the Vue Options API, which will be a little different for readers who are used to imperative GUIs such as [LVGL](https://lvgl.io/) and Qt widgets. However, Glyphix's declarative design can also bring a more intuitive interface control experience.

Developers do not need to fully master HTML, CSS and JavaScript, but familiarity with the basic syntax of JavaScript (such as variables, conditional judgments, function calls, etc.) will help understand Glyphix's rendering logic and event processing. You can familiarize yourself with these contents through sample code and practical operations in tutorials and documents to speed up the development process.

### Do you want to pay attention to application performance optimization?

Our framework has been deeply optimized for the resource constraints of embedded systems and can adapt well to a variety of hardware environments. Most applications can run smoothly and stably enough under default settings, so there is usually no need to spend extra time on performance optimization.

If there is a need for in-depth understanding of specific optimization solutions in the future, we will provide special performance optimization documents to help developers further improve the operating efficiency of applications.

### Is there a difference between the Glyphix environment and the browser?

Yes, there are significant differences between the Glyphix environment and the browser. Glyphix does not have the DOM structure in the browser, nor does it provide objects such as `window` and `document`. Instead, it directly and uniquely provides a set of declarative interfaces through which developers can develop components and interact with interfaces. This design simplifies the development process and is more suitable for embedded environments.