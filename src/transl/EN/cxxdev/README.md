# Native C++ Development

Glyphix is an application framework designed for embedded devices, providing a JavaScript-centric application development experience with a Vue Options API-like style. However, the core runtime of the framework is implemented in C++, allowing hardware vendors to extend and customize framework features using C++ — and this is where "Native C++ Development" comes into play.

This documentation is intended for C++ developers with embedded development experience. It aims to help you understand Glyphix's C++ extension mechanism and enable you to implement the following two types of features:

- **Native Module**: Encapsulates C++ functionalities into JavaScript-callable APIs, such as file access, hardware sensor reading, Bluetooth communication, and other system capabilities.
- **Native Widget**: Implements custom UI widgets using C++ and registers them as framework [components](/framework/component/native-component.md) for applications to use directly in their user interfaces, just like the built-in `div`, `image`, and `button` components.

::: tip
In application development, we use "component" to refer to UI elements, while at the C++ layer, we use "widget" to refer to UI elements. This documentation distinguishes between these two terms: **widgets** are concepts at the C++ layer, and **components** are concepts within the reactive framework.
:::

## Framework Runtime Model

The Glyphix runtime consists of multiple layers. The diagram below illustrates the complete layered architecture:

<ArchDiagram max-width="560px">
  <div>
    Application Sandbox (Applet × N)
    <div class="remark">Independent JavaScript Realm · Lifecycle Isolation</div>
  </div>
  <div>
    Reactive Framework (C++)
    <div class="group row">
      <div>AppletKit<div class="remark">App Routing · Background Management</div></div>
      <div>Component System<div class="remark">Template · Reactive Render</div></div>
      <div>JsVM Bridge Layer<div class="remark">JerryScript / QuickJS</div></div>
    </div>
    <div class="group row">
      <div>Applet<div class="remark">C++ ↔ JavaScript Sandbox</div></div>
      <div>Asynchronous Session<div class="remark">ResultSession · Signals</div></div>
      <div>Native Module<div class="remark">System API Extension</div></div>
    </div>
  </div>
  <div>
    C++ Core Framework
    <div class="group row">
      <div>Widget System<div class="remark">Object · Widget</div></div>
      <div>Layout Engine<div class="remark">Flex · Flow · Stack</div></div>
      <div>Style Engine<div class="remark">CSS · Transition</div></div>
    </div>
    <div class="group row">
      <div>Event System<div class="remark">Touch · Key · Wheel</div></div>
      <div>Painter<div class="remark">2D Drawing</div></div>
      <div>Animation Engine<div class="remark">Property · Ease</div></div>
      <div>Signal / Slot</div>
    </div>
  </div>
  <div>
    Platform Abstraction Layer
    <div class="group row">
      <div>Graphics Backend<div class="remark">Framebuffer · GPU</div></div>
      <div>Input Driver<div class="remark">Touch · Key · Wheel</div></div>
      <div>File System<span class="remark">File · Dir</span></div>
      <div>IO/Time<span class="remark">Logger · Time</span></div>
    </div>
  </div>
  <div>
    Hardware / OS
    <div class="remark">RTOS · Linux · WASM</div>
  </div>
</ArchDiagram>

The bottom layer is the **Platform Abstraction Layer**, which is responsible for platform-dependent abstractions such as graphics rendering, input events, and the file system. This layer is typically implemented by device vendors or provided as a reference implementation for the corresponding platform by Glyphix.

Above it is the **C++ Core Framework**, containing the complete widget system (`Widget`), event dispatching, animation engine, layout system, and style engine. All UI elements are ultimately organized and rendered in the form of a C++ widget tree.

The next layer up is the **Reactive Framework**, which is responsible for bridging C++ core capabilities to JavaScript applications. It embeds a JavaScript engine (JerryScript or QuickJS) and implements bidirectional interaction between C++ and JavaScript via the `JsVM` and `JsValue` classes. AppletKit manages the complete lifecycle of applications (Applets), the component system implements reactive data binding and template rendering, and the asynchronous session framework maps C++ asynchronous operations to JavaScript Promises. The reactive framework itself is also implemented in C++.

The top layer is the **Application Sandbox**. Each running application (Applet) has an independent JavaScript execution environment (Realm) that is completely isolated from others. When an application exits, all resources within its sandbox are automatically reclaimed.

### System Collaboration Principles

The architectural diagram illustrates module partitioning but intentionally conceals the collaboration and coupling relationships between modules. In reality, the entire framework operates through a set of shared underlying mechanisms. Understanding these mechanisms helps you know "what you are doing and why you are doing it" in practice.

The entire framework is underpinned by a **Object System** that endows classes with runtime perception capabilities, including C++ class property reflection and event notification capabilities, as well as necessary lifecycle safety. Widgets, Native Modules, application frameworks, and asynchronous sessions all rely on this same foundation. For details, see the [Object System](./object-system.md).

**Widgets** form the UI skeleton through an object tree combined with drawing and event dispatching; the JavaScript application layer uses a **componentized** declarative programming model, and the two are naturally connected via object reflection capabilities such properties. Complex features like **Asynchronous Sessions** also rely on the object system's lifecycle model to ensure correctness.

Through the **Meta-Object Compiler** and other abstraction mechanisms, Glyphix does not require developers to handwrite binding code to expose C++-developed widget classes for JavaScript usage. At the same time, functional completeness is retained on the C++ side; theoretically speaking, you can develop a complete application directly in C++ (although it is not recommended).

### Programming Model

The Glyphix project does not restrict specific programming paradigms. For example, the object system is a classic object-oriented model, while the reactive framework provides application developers with a declarative, component-based development experience.

We do not encourage developers to practice "everything is an object," deliberately force design patterns, or pursue unnecessary abstractions. Our design principles lean more toward **pragmatism**, prioritizing the **resource constraints** and development efficiency of embedded systems.

## Documentation Conventions

### What is this document?

This is a guide for Glyphix Native C++ Development, **not** an API reference document. It introduces the framework's design philosophy, core mechanisms, and development workflow to help you understand how to extend framework capabilities, demonstrating specific implementation details through sample code.

During actual development, please be sure to refer to the API documentation distributed alongside the SDK; please contact your vendor for access.

### Sample Code Notes

All C++ code within the Glyphix framework resides under the `gx` namespace. The documentation assumes `using namespace gx;` by default, so class and function names do not carry the `gx::` prefix. For example:

```cpp
#include "gx_widget.h"

using namespace gx; // Assumed to be imported by default in documentation

class MyWidget : public Widget {
    // ...
};
```

Here, `Widget` is actually `gx::Widget`, but for brevity, we omit the namespace prefix.

::: tip C++ Learning Resources
If you primarily use C, are familiar with MCUs, RTOS, drivers, or LVGL, but have not systematically studied C++, we recommend reading the [C++ Learning Guide](./cpp-guide.md) first. It covers only the subset of C++ truly needed to enter Glyphix native development and organizes external resources suitable for embedded developers.
:::

## Development Path

Regardless of your goal, it is recommended to first thoroughly read the basic usage of `GX_OBJECT`, `GX_PROPERTY`, and `Signal` in the [Object System](./object-system) — they are used across all development scenarios.

Choose the appropriate documentation to continue reading based on your goals:

- [SDK Project Configuration](./sdk-setup): How to configure the build environment for an SDK project, including `glyphix_add_meta_objects()` registration, host building, and cross-compilation.
- [Native Module Development](./native-module): How to provide new system APIs for applications, such as fetching sensor data or calling underlying SDK functions.
- [Asynchronous Feature Development](./async): How to extend asynchronous features for applications, such as network requests, file IO, and time-consuming computations.
- [Widget Development Guide](./widget.md): How to implement new UI widgets (such as custom charts, special animation lists, etc.).
- [Widget Registration and Export](./widget-export.md): Registering custom widgets as framework components for direct application usage.