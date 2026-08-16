# Context File: 01_glyphix_framework_core_EN.md
Ограничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.

============================================================
FILE_PATH: src/transl/EN/framework/README.md

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

============================================================
FILE_PATH: src/transl/EN/framework/testing/api.md

# API

## Content Targeting



============================================================
FILE_PATH: src/transl/EN/framework/testing/README.md

# Testing Framework

Glyphix provides an automated application testing framework for simulating user actions and inspecting UI behavior. This testing framework does not simulate actions randomly; instead, it requires developers to write test cases.

## Basic Concepts

The Glyphix testing framework is essentially a set of JavaScript APIs that generally implement the following functions:

- Registering test cases
- Finding UI elements
- Simulating user actions or gestures
- Assertions and verification logic

### Test Steps

The basic principle of a test step is to **find a specific element**, **execute a simulated action**, and (optionally) **verify the content**. For example:

1. Find an element with the CSS class `play-button`;
2. Click this element;
3. Do not verify the content.

In an actual UI, `.play-button` might be a play button, and clicking it will start playing music. The JavaScript code corresponding to this test is as follows:

```js
await tc.getByClass("play-button").click();
```

The test code automatically waits for the `.play-button` element to appear and moves it into the UI viewport before clicking it. These test APIs automatically wait for animations or gestures in the interface and fulfill the `await` only after the click gesture is fully completed. Therefore, it is generally unnecessary to manually move elements or explicitly wait for operations to complete.

### Finding Elements

The testing framework provides a series of interfaces to find elements in the UI, such as:

- `tc.getByClass()`: Find elements by class name;
- `tc.getByTag()`: Find elements by tag name.

These interfaces wait for the element to appear and attempt to move the element into the visible area before the next operation.

### Simulating User Actions

## Getting Started with Writing Tests

### Test Case Files

Glyphix test cases are written in JavaScript and stored within the application's resource package. It is recommended to store test cases separately in the project's `src/tests` directory, for example:

```shell
<app-name>
├─ README.md         # Project README
└─ src               # Project source code directory
    ├─ app.js        # App entry script file
    ├─ manifest.json # Configuration of basic app information
    ├─ tests         # Directory storing all test cases
    │  └─ spec.js    # Test case code
    └─ Main          # Directory storing the home page
        └─ index.ux  # Home page UI description file
```

The test code in this example is the `src/tests/spec.js` file, and multiple test files can be created as needed.

::: tip
The file name for test cases is usually `spec`, which is short for specification. A spec file is used to define and describe the expected behavior and functionality of software, and typically contains a set of test cases used to verify whether the software works as expected.
:::

### Writing Test Cases

Suppose our application has a home page containing a `span` element with the class name `clickable`:

```html
<div>
  <span class="clickable" on:click="console.log('click span')"> click me </span>
</div>
```

Now, we want to write an automated test script that clicks the `span` component once every second and ends the test after 3 clicks. To do this, add the following code to `src/tests/spec.js`:

```js
// Import the @system.test module which provides the testing framework API
import tc from "@system.test";

// Register an automated test case named click-test
tc.testcase("click-test", async () => {
  for (let i = 0; i < 3; ++i) {
    // Find the element with class="clickable" and click it
    await tc.getByClass("clickable").click();
    // Wait for one second
    await tc.wait(1);
  }
});
```

Next, you need to register this test script and start the test.

### Registering Test Scripts

In regular code, statements like `import 'tests/spec.js'` are typically used to import scripts, but this would cause the JavaScript module to always be loaded. To optimize application loading speed and memory usage, we don't need to import these scripts in non-test environments. To achieve this, you can register test scripts in the App object within the `src/app.js` file:

```js
export default {
  // Use the testsuite property to register a list of test scripts
  testsuite: ["tests/spec.js"],
  onCreate() {
    /* ... */
  },
  // ...
};
```

This method does not import the test scripts immediately, but defers their import until the tests are executed. Therefore, when tests are not being run, using the `testsuite` property introduces no overhead, and developers do not need to worry about the performance burden of loading test scripts.

::: warning
Even if there is only a single test script, the `testsuite` property must be an `Array` object containing the path of the test script, as shown in the example in this section. The path of the test script is always relative to the directory where the `app.js` file is located. You can also use an absolute path, such as `/tests/spec.js`.
:::

## Running Test Cases

### Simulator

To run test cases, use the `gx emu -i` command to start the simulator. You will see information like this in your terminal:

```shell
❯ gx emu -i
[emu] Open inspector http://localhost:14200 in browser.
```

Next, open the link `http://localhost:14200` in your browser, go to the "Console" tab, and enter the following text in the "RPC" bar at the bottom:
```json
{"fn": "test.start", "name": "click-test"}
```
This will start the `click-test` test case written previously. You should then see the following logs in the log viewer:

```log
19:14:33.320 [inspector] test com.example.app . click-test started
19:14:33.640 [js] 'click span'
19:14:35.090 [js] 'click span'
19:14:36.510 [js] 'click span'
19:14:37.600 [tester] com.example.app testcase click-test finished
```

This indicates that the test executed successfully and the `span` element was indeed clicked $3$ times.

============================================================
FILE_PATH: src/transl/EN/framework/generic/properties.md

---
icon: xml
---
# Properties and Events

This section introduces the common property interfaces and events provided by all native components.

## Property List

### Common Properties

#### `top` <decl type="number" get set listen />

The position of the top of the component relative to the parent native component, in pixels. This property is actually a shorthand for the `top` property in inline styles. For more usage methods, see [Component Position Operation](#component-position-operation).

Reading or listening to the `top` property returns the calculated position of the component, which is the actual measured value after layout.

#### `left` <decl type="number" get set listen />

The position of the left side of the component relative to the parent native component, in pixels. This property is actually a shorthand for the `left` property in inline styles. For more usage methods, see [Component Position Operation](#component-position-operation).

Reading or listening to the `left` property returns the calculated position of the component, which is the actual measured value after layout.

#### `width` <decl type="number" get set listen />

The width of the component. When setting the `width` property, the [`width`](styles.md#width) property in the inline styles will be updated. Since CSS width uses the border-box model, the actually stored style value will automatically include the element's current `padding` and `border` sizes to ensure that the content width after layout matches the set value.

Reading or listening to the `width` property returns the layout-calculated content width, excluding `padding` and `border`.

#### `height` <decl type="number" get set listen />

The height of the component. When setting the `height` property, the [`height`](styles.md#height) property in the inline styles will be updated. Since CSS height uses the border-box model, the actually stored style value will automatically include the element's current `padding` and `border` sizes to ensure that the content height after layout matches the set value.

Reading or listening to the `height` property returns the layout-calculated content height, excluding `padding` and `border`.

#### `show` <decl type="boolean" get set/>

Sets whether the component is visible. Hidden components are neither displayed nor occupy layout space.

#### `quiescent` <decl type="boolean" get set/>

Sets whether the component snapshot updates automatically (quiescent snapshot). If a component is displayed via a snapshot, when this property value is `false` (default), the snapshot will be refreshed immediately to update the view when the component content updates; otherwise, the snapshot will not be updated immediately. Setting this property to `true` can improve UI performance, but will cause a lag in the displayed content.

The following example demonstrates the role of the `quiescent` property. Two `p` elements are placed inside a `scroll` container, and the `scroll` container has [snapshot mode](../../components/scroll.md#snapshot) enabled. When the user scrolls the `scroll` component, snapshots of the elements within it are taken. Since the first `p` element uses the normal snapshot mode while the second `p` element uses the quiescent snapshot mode, only the content update of the first `p` element can be observed during scrolling.

<glyphix id="generic-properties-quiescent" height="200" title="Lazy Snapshot">

``` html
<scroll snapshot scroll-snap="center">
  <p>normal snapshot {{ count }}</p>
  <p quiescent>quiescent snapshot {{ count }}</p>
</scroll>
```

``` css
scroll {
  display: flex;
  flex-direction: column;
  background-color: lightgray;
}

p {
  background-color: lightgreen;
  text-align: center;
  padding: 10px;
  margin: 10px;
}
```

``` js
export default {
  data: {
    count: 0
  },
  onReady(event) {
    setInterval(() => this.count++, 500)
  }
}
```

</glyphix>

#### `style` <decl type="string" set />

Sets the inline style of the component. Currently, only [CSS properties](./styles.md) with the <badge type="info" text="inline" /> tag are supported.

#### `z-index` <decl type="number" get set />

The `z-index` property sets the Z-axis order of elements. Overlapping elements with a larger `z-index` will cover elements with a smaller one. This property value will be overridden by the [`z-index`](styles.md/#z-index) property in CSS.


#### `opacity` <decl type="number" get set />

Specifies the opacity of the component. The value range is $[0, 1]$, where $0$ represents completely transparent. It has the same effect as the CSS property [`opacity`](styles.md#opacity).

::: warning
The `opacity` value will affect the rendering performance of the element. For details, please refer to the description of the [`opacity`](styles.md#opacity) CSS property.
:::

#### `transform` <decl type="string" set />

Sets the transformation of the component, equivalent to the CSS [`transform`](styles.md#transform) property.

#### `disabled` <decl type="boolean" get set />

Used to set or get the disabled state of the component. When the property value is `true`, the element is in a disabled state, the user cannot interact with it, and the element will not respond to any gestures (such as clicks, drags, etc.). When the property value is the **default** `false`, the component is in an available state, and the user can interact with it normally.

The following example demonstrates the usage of the `disabled` property, while also using the [`:disabled`](styles.md#disabled) CSS pseudo-class to control styles. This example shows that a `div` element can respond to click gestures in the normal state, but does not respond to any gestures in the `disabled` state.

<glyphix id="generic-properties-disabled" height="200" title="disabled Property">

``` html
<div :disabled="disabled" on:click="onClick">
  {{disabled ? 'disabled' : 'normal'}} <switch />
</div>
```

``` css
div {
  background-color: lightgray;
  text-align: center;
  display: flex;
  justify-content: center;
}

/* :disabled pseudo-class can control the style of elements in the disabled state */
div:disabled {
  opacity: 0.5;
}
```

``` js
import prompt from '@system.prompt'

export default {
  data: {
    disabled: false
  },
  onInit() {
    setInterval(() => {
      this.disabled = !this.disabled
    }, 2000)
  },
  onClick() {
    prompt.showToast({ message: 'clicked!', duration: 250 })
  }
}
```

</glyphix>

### Common Events

Most native components support common events, which can be listened to using the [`on` directive](../commands/on.md). The value types of these events are introduced in the [Event Types](#event-types) section.

#### `touchstart` <decl type="TouchEvent" listen />

Triggered when the user starts touching the component. The event value is of type [`TouchEvent`](#touchevent).

#### `touchmove` <decl type="TouchEvent" listen />

Triggered when the user's touch point moves on the component. During the movement, this event will continue to trigger even if the touch point leaves the range of the current native component. The event value is of type [`TouchEvent`](#touchevent).

There is a certain "dead zone for movement" when transitioning the touch state from `touchstart` to `touchmove`. If the user's touch sliding distance is less than the dead zone range, `touchmove` will not be triggered. The movement dead zone range varies by device. The following example illustrates the movement dead zone.

<glyphix id="generic-properties-touchmove" height="200" title="Movement Dead Zone">

``` html
<p on:touchstart="state = 'start'"
   on:touchmove="onTouchMove($event)"
   on:touchend="onTouchEnd">
  {{ `state: ${state} \ndead area: (${dx}, ${dy})` }}
</p>
```

``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```

``` js
export default {
  data: {
    state: null,
    dx: null,
    dy: null
  },
  onTouchMove(event) {
    if (!this.dx && !this.dy) {
      this.state = 'move'
      this.dx = event.touches[0].offsetX
      this.dy = event.touches[0].offsetY
    }
  },
  onTouchEnd() {
    this.state = 'end'
    this.dx = this.dy = null
  }
}
```

</glyphix>

#### `touchend` <decl type="TouchEvent" listen />

When the user's touch point leaves the screen, a `touchend` event is sent to the previously touched native component. The event value is of type [`TouchEvent`](#touchevent).

#### `touchcancel` <decl type="TouchEvent" listen />

Triggered when the touch on the native component is interrupted. The event value is of type [`TouchEvent`](#touchevent). There are multiple reasons that can cause a touch interruption, such as the component being hidden or the touch event being forcibly responded to by other elements.

#### `click` <decl type="ClickEvent" listen />

Triggered when the native component is clicked and released. The event value is of type [`ClickEvent`](#clickevent).

<glyphix id="generic-properties-click" height="100">

``` html
<p on:click="click = JSON.stringify($event)">
  {{ click }}
</p>
```

``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```

``` js
export default {
  data: {
    click: null
  }
}
```

</glyphix>

#### `longpress` <decl type="LongPressEvent" listen />

Triggered when the native component is pressed for a long time. The event value is of type [`LongPressEvent`](#longpressevent). The interactive example below shows the triggering timing of `longpress` and other events:

<glyphix id="generic-properties-longpress" height="100">

``` html
<p on:touchstart="state = 'touching...'"
   on:longpress="state = `longpress: ${JSON.stringify($event)}`"
   on:click="state = 'clicked.'">
  {{ state }}
</p>
```

``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```

``` js
export default {
  data: {
    state: null
  }
}
```

</glyphix>

The triggering timing and duration of the `longpress` event vary by device, usually triggered after pressing for $500 \rm ms$. Unlike the [`click`](#click) event, `longpress` is triggered during the press, rather than upon release. For the above example, you will find that:
- When the press time is less than the long-press trigger time, releasing the touch triggers the `click` event;
- When pressed long enough, the `longpress` event is triggered, and releasing the touch triggers the `click` event (displayed as the "clicked." state);
- Moving during the press will not trigger the `longpress` or `click` events.

#### `swipe` <decl type="SwipeEvent" listen />

Triggered when the component is swiped quickly. The event value is of type [`SwipeEvent`](#swipeevent).

<glyphix id="generic-properties-swipe" height="250" >

``` html
<p on:swipe="onSwipe($event)">
  {{ swipe }}
</p>
```

``` css
p {
  background-color: lightgreen;
  text-align: center;
}
```

``` js
export default {
  data: {
    swipe: null
  },
  onSwipe(event) {
    this.swipe = event.direction
    event.strongResponse()
  }
}
```

</glyphix>

#### `keydown` <decl type="KeyEvent" listen />

Triggered when a key is pressed down. The `keydown` and `keyup` events are used to capture physical key operations. To capture events, the native component must be in focus. The root element of the page always automatically gets focus, so the following code can capture `keydown` and `keyup` events:
``` html
<!-- Assuming this is the root element of the page -->
<div on:keydown="console.log($event)" on:keyup="console.log($event)">
  ...
</div>
```
Please refer to [`KeyEvent`](#keyevent) for the event value type.

Watch devices usually register [default key handlers](/api/system-internal.md#setdefaultkeyhandler), so application code can interact even if it does not respond to these types of events (for example, some watches return to the previous page when the Power button is pressed). To prevent default key responses, you can use the `stopPropagation()` method of the `KeyEvent` object to stop bubbling.

#### `keyup` <decl type="KeyEvent" listen />

Triggered when a key is released. For more details, please refer to the [`keydown`](#keydown) event.

#### `wheel` <decl type="WheelEvent" listen />

Triggered when the user operates a rotating wheel. Wheel devices include the rotating bezel of a watch or a mouse wheel. To capture this event, the native component must be in focus. The root element of the page always automatically gets focus, so the following code can capture the `wheel` event:
``` html
<!-- Assuming this is the root element of the page -->
<div on:wheel="console.log($event)">
  ...
</div>
```
Please refer to [`WheelEvent`](#wheelevent) for the event value type.

## Event Types

### `BaseEvent`

The `BaseEvent` event object provides methods to control event propagation. Its prototype is:
``` ts
interface BaseEvent {
  strongResponse(): void, // Force response to the event
  stopPropagation(): void // Stop event bubbling
}
```

### `TouchEvent`

The prototype of the `TouchEvent` event object is:
``` ts
interface TouchEvent extends BaseEvent {
  isTarget: boolean, // Whether the event target is the current component
  touches: { // All touch point data for this event
    clientX: number, // X coordinate of the touch point relative to the target component's content area
    clientY: number, // Y coordinate of the touch point relative to the target component's content area
    offsetX: number, // Displacement of the touch point in the X direction during the touch process
    offsetY: number  // Displacement of the touch point in the Y direction during the touch process
  }[];
}
```

### `ClickEvent`

The prototype of the `SwipeEvent` event object is:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Whether the event target is the current component
  clientX: number, // X coordinate of the click touch point relative to the target component's content area
  clientY: number // Y coordinate of the click touch point relative to the target component's content area
}
```

### `LongPressEvent`

The prototype of the `LongPressEvent` event object is:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Whether the event target is the current component
  clientX: number, // X coordinate of the long-press touch point relative to the target component's content area
  clientY: number // Y coordinate of the long-press touch point relative to the target component's content area
}
```

### `SwipeEvent`

The prototype of the `SwipeEvent` event object is:
``` ts
interface SwiperEvent extends BaseEvent  {
  isTarget: boolean, // Whether the event target is the current component
  direction: 'left' | 'right' | 'up' | 'down' // Swipe direction
}
```

### `KeyEvent`

The `KeyEvent` object describes the user's interaction events with physical keys. This type is used for the event properties of elements [`keydown`](#keydown) and [`keyup`](#keyup). The prototype of the `KeyEvent` event object is:
``` ts
interface KeyEvent  {
  type: 'keydown' | 'keyup', // Type of key event
  key: string, // Name of the key
  timestamp: number, // Timestamp when the key event was reported, in milliseconds
  stopPropagation(): void // Call this method to prevent event bubbling
}
```

The following key names are currently supported:
- `'Power'`: The power button of the watch;
- `'Fn'`: The function button of the watch;
- Keys for other printable characters consist of a single character as the key name, such as the letter `'A'`, hyphen `'-'`, etc.

### `WheelEvent`

The `WheelEvent` object describes the user's interaction events with a rotating wheel. This type is used for the event properties of elements [`wheel`](#wheel). The signature of the `WheelEvent` event object is:
``` ts
interface WheelEvent {
  deltaY: number, // Scrolling increment of the wheel in the Y direction
  stopPropagation(): void // Call this method to prevent event bubbling
}
```

Unlike the Web's [wheel event](https://developer.mozilla.org/en-US/docs/Web/API/Element/wheel_event), the `WheelEvent` in Glyphix currently only contains the `deltaY` property.

## Event Response Mechanism

### Event Bubbling

Touch and gesture events support bubbling. Bubbling means that when an event occurs on an element, it first executes the handler on that element, then executes the handler on its parent element, and so on up to handlers on other ancestors. In the example below, both the green `p` component and the gray `div` component listen for touch events. When clicking the `p` component, you can observe that both the `p` component and the `div` component receive the event.

<glyphix id="generic-event-bubbling" height="250" title="Touch Event Bubbling">

``` html
<div on:touchstart="onTouch('div', $event)"
     on:touchmove="onTouch('div', $event)"
     on:touchend="onRelease('div', $event)">
  <p on:touchstart="onTouch('p', $event)"
     on:touchmove="onTouch('p', $event)"
     on:touchend="onRelease('p', $event)">
    {{ `touchs: ${touchs.div ? 'div' : '-'} ${touchs.p ? 'p' : '-'}, target: ${target}` }}
  </p>
</div>
```

``` css
div {
  display: flex;
  flex-direction: column;
  background-color: lightgray;
  justify-content: space-around;
}

p {
  background-color: lightgreen;
  text-align: center;
  height: 150px;
}
```

``` js
export default {
  data: {
    touchs: { div: false, p: false },
    target: null
  },
  onTouch(name, event) {
    this.touchs[name] = true
    // isTarget property can distinguish whether the target of the event is the current component listening to the event
    if (event.isTarget)
      this.target = name
  },
  onRelease(name, event) {
    this.touchs[name] = false
    if (event.isTarget)
      this.target = null
  }
}
```

</glyphix>

In Glyphix, only the touch and gesture events in this document will bubble. Event capture cannot be performed in JavaScript code at present.

### Stopping Event Bubbling

Use the `stopPropagation()` method of `BaseEvent` to prevent the event from bubbling up to the parent.

### Strong Response Events

In Glyphix, touch or gesture events have two response priorities: strong response and weak response. When an event has multiple targets waiting to respond at the same time, the strong response has a higher priority than the weak response. Suppose there are 3 levels of parent-child elements on the interface: `A -> B -> C`, where `C` has a weak response to the event and `B` has a strong response. Then the event will be dispatched to `B` and will no longer be dispatched to `C`. An element that originally had a strong response event will re-dispatch events after being changed to a weak response.

The touch and gesture events in [Common Events](#common-events) are weakly responsive by default. In the example below, a green `p` component is placed inside a gray `scroll`, and all touch events of the `p` component are listened to. Since `scroll` strongly responds to up and down sliding gestures by default, weakly responds to left and right sliding gestures, and does not respond to other gestures, you can observe during operation that:
- Clicking the `p` component triggers the `touchstart` event, and releasing it triggers the `touchend` event;
- Dragging the `p` component horizontally triggers the `touchmove` event;
- Dragging the `p` component vertically—since the parent `scroll` component has a strong response to vertical sliding, while the `p` component in the template code only has a weak response to `touchmove`—results in the vertical sliding being responded to by the `scroll` component, and the `p` component receives a `touchcancel` event.

<glyphix id="generic-event-strong-response-1" height="250" title="Strong Response Events">

``` html
<scroll>
  <p on:touchstart="state = 'touchstart'"
     on:touchmove="state = 'touchmove'"
     on:touchend="state = 'touchend'"
     on:touchcancel="state = 'touchcancel'">
    {{ `p.state: ${state}` }}
  </p>
</scroll>
```

``` css
scroll {
  background-color: lightgray;
}

p {
  background-color: lightgreen;
  text-align: center;
  height: 150px;
  margin: 50px;
}
```

``` js
export default {
  data: {
    state: null
  }
}
```

</glyphix>

The default gesture event handling mechanism of many native components is strongly responsive. Using the `strongResponse()` method of the `BaseEvent` object can specify the event as strong response mode in JavaScript code. In the example below, the outer gray `div` component will strongly respond to gestures, so even if the inner `p` element is touched, the event will only be dispatched to the `div` component after the gesture starts.

<glyphix id="generic-event-strong-response-2" height="250" title="Strong Response Events">

``` html
<div on:touchstart="onTouch('div', 'start', $event)"
     on:touchmove="onTouch('div', 'move', $event)"
     on:touchend="onTouch('div', 'end', $event)"
     on:touchcancel="onTouch('div', 'cancel', $event)">
  <p on:touchstart="onTouch('p', 'start', $event)"
     on:touchmove="onTouch('p', 'move', $event)"
     on:touchend="onTouch('p', 'end', $event)"
     on:touchcancel="onTouch('p', 'cancel', $event)">
    {{ `div state: ${touchs.div}, p state: ${touchs.p}, target: ${target}` }}
  </p>
</div>
```

``` css
div {
  display: flex;
  flex-direction: column;
  background-color: lightgray;
  justify-content: space-around;
}

p {
  background-color: lightgreen;
  text-align: center;
  height: 150px;
}
```

``` js
export default {
  data: {
    touchs: { div: null, p: null },
    target: null
  },
  onTouch(name, state, event) {
    console.log(name, state, event.isTarget)
    this.touchs[name] = state
    // isTarget property can distinguish whether the target of the event is the current component listening to the event.
    // Do not record the target if it is a cancel event.
    if (event.isTarget && state != 'cancel')
      this.target = name
    if (name == 'div')
      event.strongResponse()
  }
}
```

</glyphix>

### Default Event Handling of Pages

Pages weakly respond to gesture events by default and prevent event bubbling, so gesture events cannot be dispatched and transmitted through the page. In addition, pages will exit when receiving a rightward `touchmove` gesture. Developers can also intercept gestures to disable this feature.

The specific approach is to listen to the `touchmove` gesture of the page component and prevent bubbling:
``` html
<!-- This div is the root component of the page -->
<div on:touchmove="$event.stopPropagation()">
  ...
</div>
```
In this way, the page cannot be returned from via a right-swipe operation, but can be returned from by pressing the physical Power button. To also prevent users from returning via keypress, you can use the following method:
``` html
<!-- This div is the root component of the page -->
<div on:keydown="onKeyup">
  ...
</div>
```

``` js
export default {
  onKeyup(event) {
    // Prevent event bubbling to block page exit when key value is 'Power'
    if (event.key == 'Power')
      event.stopPropagation()
  }
}
```

::: warning
Exercise caution when overriding the default event handling mechanism of pages to avoid situations where users cannot return from the page.
:::

::: tip
In previous versions, the `swipe` gesture event was used to prevent the page's default return behavior, but this approach was deprecated in version 0.6.4. Please use the aforementioned `touchmove` event handling instead. This adjustment was made because the page's interactive return animation (i.e., follow-finger exit) is completely incompatible with the semantics of `swipe` preventing page returns.
:::

## Tips and Tricks

### Component Position Operation

You can easily modify the component position by utilizing the `top` and `left` properties of native components:
``` html
<div :top="40" :left="20"> ... </div>
```
`top` and `left` are actually shorthands for CSS properties of the same name, so they only take effect in absolute layouts, which can be achieved via the following CSS:
``` css
div {
  position: absolute;
}
```

You can then use reactive properties to modify the component's position. The example below shows animated random component position movement implemented in combination with the [`transition` modifier](/framework/component/prop-modifier.md#transition-modifier).

<glyphix id="generic-widget-position" height="250" title="Random Component Position">

``` html
<div id="pane">
  <p id="tile" :top="top" :left="left"
     top.transition left.transition>
    Tile
  </p>
</div>
```

``` css
div {
  background-color: lightgray;
}

p {
  /* Absolute positioning is required to use the component's top / left properties */
  position: absolute;
  background-color: lightgreen;
  text-align: center;
  width: 3rem;
  height: 3rem;
  border: 4px solid red;
  border-radius: 10%;
}
```

``` js
export default {
  data: {
    top: 0,
    left: 0
  },
  timer: null,
  onReady() {
    // Get component object, position range should not exceed the #pane container
    const pane = this.$element("pane")
    const tile = this.$element("tile")
    const width = pane.width - tile.width
    const height = pane.height - tile.height
    this.timer = setInterval(() => {
      this.top = Math.random() * height
      this.left = Math.random() * width
    }, 2000)
  },
  onDestroy() {
    clearInterval(this.timer)
  }
}
```

</glyphix>

This example randomly sets the position of the `#tile` component every two seconds, ensuring it stays within the boundaries of the container `#pane`. The default `transition` modifier plays a $1$-second transition animation.

============================================================
FILE_PATH: src/transl/EN/framework/generic/styles.md

---
icon: layers-outline
---
# CSS Properties

This section introduces all the CSS properties supported by the Glyphix framework. For an introduction to the styling and layout mechanism, please refer to [this document](/framework/render/style-and-layout.md).

## Layout Control

### Basic Properties

#### `display`

The `display` property sets an element's layout scheme. Currently, it can be set to the following values:

- `inline`: Default value. The element generates one or more inline element boxes that do not generate line breaks before or after them. In normal flow, if there is space, the next element will be on the same line.
- `block`: The element generates a block-level element box, generating line breaks before and after the element in normal flow.
- `flex`: The element behaves like a block-level element and lays out its contents using `Flex` layout.
- `inline-flex` and `inline flex`: The element behaves like an inline element and lays out its contents using `Flex` layout.
- `none`: The element is not displayed in this mode (not recommended).

#### `width`

The `width` property specifies the width of an element, including `padding` and `border` (border-box). If the element is located in a layout container or has other constraints, the final element size may not match the value of the `width` property.

::: tip
Glyphix currently only supports the [border-box](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-sizing) mode, and the value of `width` always includes `padding` and `border`.
:::

The value of the `width` property is a CSS [length](/framework/render/style-and-layout.md#长度), with the following specific values:

- `auto`: Default value. This mode automatically calculates the width of the element based on content size and layout constraints. For example, a text element determines its width based on the size of the text content, while a container element determines its width based on the layout size of its internal elements.
- `value [unit]`: Specifies the element width using a certain length unit. Layout or other constraints may adjust the actual size of the element.

The `width` property of an element in a flex layout serves as its initial width, which will be further adjusted to the optimal actual width during the layout process.

#### `height`

The `height` property specifies the height of an element, including `padding` and `border` (border-box). This property behaves similarly to [`width`](#width).

### Flex Layout

#### `flex-direction`

Sets the main axis direction (horizontal or vertical) when using a flex layout container. Values include:

- `row`: Default value. The main axis runs horizontally.
- `column`: The main axis runs vertically.

The `flex-direction` property is only effective when the element uses a flex layout, for example:

```css
display: flex;
flex-direction: column;
```

#### `flex-flow`

`flex-flow` is a shorthand for `flex-direction` and `flex-wrap`. The syntax is:

```css
flex-flow: <flex-direcion> <flex-wrap>;
```

Currently, the `flex-wrap` property has not been implemented yet, so this part will have no effect.

#### `justify-content`

Specifies the alignment of child elements along the main axis of the container when using a flex layout.

Property values:

- `flex-start`: Default value. The first element is flush against the start of the container's main axis, and subsequent elements are arranged sequentially. No extra space is filled between elements.
- `flex-end`: The last element is flush against the end of the container's main axis, and preceding elements are arranged sequentially. No extra space is filled between elements.
- `center`: All elements are arranged sequentially in the middle of the container's main axis, leaving remaining space at both ends of the main axis. No extra space is filled between elements.
- `space-between`: Elements are evenly distributed; the first element is placed at the start, the last element is placed at the end, and the remaining space is evenly distributed between the elements.
- `space-around`: Elements are evenly distributed with equal space around each element, leaving remaining space before the first element and after the last element.

#### `align-items` <badge type="info" text="Inline" />

Specifies the alignment of child elements along the cross axis of the container when using a flex layout. Supports the following values:

- `stretch`: Default value. Elements are stretched to fill all available space in the container's cross axis.
- `flex-start`: Elements are flush against the start of the container's cross axis and are not stretched.
- `flex-end`: Elements are flush against the end of the container's cross axis and are not stretched.
- `center`: Elements are centered along the container's cross axis and are not stretched.
- `baseline`: The cross axis of the elements is aligned according to the font baseline.


**Baseline alignment** allows text, images, or elements like [`switch`](/components/switch.md) and [`checkbox`](/components/checkbox.md) to align according to the text baseline position, thereby ensuring a neat visual effect. Note that `align-items: baseline` is only effective when the main axis direction is [`row`](#flex-direction).

#### `align-self` <badge type="info" text="Inline" />

Specifies the alignment of a flex item itself along the cross axis. This property has a higher priority than `align-items`. Supports the following values:

- `auto`: Default value. Uses the cross-axis alignment of the flex container.
- `stretch`: The element is stretched to fill all available space in the container's cross axis.
- `flex-start`: The element is flush against the start of the container's cross axis and is not stretched.
- `flex-end`: The element is flush against the end of the container's cross axis and is not stretched.
- `center`: The element is centered along the container's cross axis and is not stretched.
- `baseline`: `align-self` does not support the `baseline` value and has the same effect as `flex-start`.

::: tip
Unlike `align-items`, you cannot use the `baseline` value in `align-self`. Therefore, cross-axis baseline alignment can currently only be set via the flex container's `align-items` property.
:::

#### `flex-grow`

Specifies the flex growth factor of a flex item along the main axis. It is an integer between $[0, 100]$ with a default value of $0$. If there is remaining space along the main axis, each element will grow in proportion to its growth factor. Therefore, if elements all have a `flex-grow` of $1$, they will evenly divide the remaining space on the main axis, while elements with a growth factor of $0$ will not grow.

#### `flex-shrink`

Specifies the flex shrinkage rate of a flex item along the main axis. It is an integer between $[0, 100]$ with a default value of $1$. If there is insufficient remaining space on the main axis, elements will shrink. The actual reduced size is determined by the element's initial size, the ratio of its own shrinkage rate to the sum of all elements' shrinkage rates, and the remaining space. A larger shrinkage rate or initial size will cause the element to shrink by a larger amount. Elements with a `flex-shrink` of $0$ will not shrink.

#### `flex`

`flex` is a shorthand for `flex-grow` and `flex-shrink`. The syntax is:

```css
flex: <flex-grow> <flex-shrink>;
```

Currently, Glyphix does not introduce the `flex-basis` property, so no extra values are required.

#### `max-height` (Not yet supported)

Sets the maximum height of an element (the max-height property does not include padding, borders, or margins). The `max-height` property is specified as a single [length](/framework/render/style-and-layout.md#长度) value.

**Default value**: Maximum height of the parent control

#### `max-width` (Not yet supported)

Sets the maximum width of an element (the max-width property does not include padding, borders, or margins). The `max-width` property is specified as a single [length](/framework/render/style-and-layout.md#长度) value.

**Default value**: Maximum width of the parent control

#### `min-height` (Not yet supported)

Sets the minimum height of an element (the min-height property does not include padding, borders, or margins). The `min-height` property is specified as a single [length](/framework/render/style-and-layout.md#长度) value.

**Default value**: `0`

#### `min-width` (Not yet supported)

Sets the minimum width of an element (the min-width property does not include padding, borders, or margins). The `min-width` property is specified as a single [length](/framework/render/style-and-layout.md#长度) value.

**Default value**: `0`

### Positioning

#### `position`

Specifies how an element is positioned in a document. Can be set to the following values:

- `static`: Default value. Specifies that the element uses normal layout behavior, meaning the element is at its current layout position in the document's regular flow. In this case, the `top`, `right`, `bottom`, and `left` properties have no effect.
- `absolute`: The element is removed from the normal document flow and no space is reserved for it. The position of the element is determined by specifying offsets relative to its parent element. Absolutely positioned elements can have margins.

#### `left`

Specifies the offset of an element relative to the left edge of its containing element.

The value of the `left` property is a CSS [length](/framework/render/style-and-layout.md#长度), and the default value is `auto`.

#### `right`

Specifies the offset of an element relative to the right edge of its containing element.

The value of the `right` property is a CSS [length](/framework/render/style-and-layout.md#长度), and the default value is `auto`.

#### `top`

Specifies the offset of an element relative to the top edge of its containing element.

The value of the `top` property is a CSS [length](/framework/render/style-and-layout.md#长度), and the default value is `auto`.

#### `bottom`

Specifies the offset of an element relative to the bottom edge of its containing element.

The value of the `bottom` property is a CSS [length](/framework/render/style-and-layout.md#长度), and the default value is `auto`.

## Text and Fonts

### Basic Properties

#### `font-family` <badge type="info" text="Inherited" />

Specifies a prioritized list of font family names for an element. Multiple fonts are separated by commas. If a font name contains spaces, it must be enclosed in quotes:

```css
font-family: serif;
font-family: "Times New Roma", serif;
```

Font names are defined by the [`@font-face`](#font-face-rule) rule. If `font-family` is not defined, the element inherits the font family of its parent element; if no parent defines a font family, the [system default font](/framework/application/font-config.md#默认字体) will be used.

#### `font-size` <badge type="info" text="Inherited" />

Specifies the font size of the element, which is a [length](/framework/render/style-and-layout.md#长度) value. Similar to `font-family`, `font-size` is also inherited from parent elements. If no parent element defines a font size, the font size of the [system default font](/framework/application/font-config.md#默认字体) will be used.

#### `font-weight` <badge type="info" text="Inherited" />

Specifies the font weight, i.e., the boldness of the font. The value is an integer in the range $[100, 900]$, with a default value of `400`. If the parent element does not define a font weight, the default weight `400` is used. If the specified font weight is not found, the system uses the closest available font weight.

::: tip
The `font-weight` property only supports integer multiples of `100`, such as `100`, `200`, `300`, etc. Values with remainders (such as `450`) are rounded to the nearest integer multiple. Currently released devices only support the `400` font weight.
:::

#### `line-height` <badge type="info" text="Inherited" />

This property is used to set the amount of space used for lines of text, such as the spacing between multiple lines of text. The `line-height` property is specified as a single [length](/framework/render/style-and-layout.md#长度) value or a **number** value. The **default** is `auto`.

In addition to length values, `line-height` can also use numeric values, representing a multiple of the font size. For example, `line-height: 1.5` means a line height 1.5 times the font size. Older versions used `line-height: 150%` to achieve the same effect. <version-badge since="0.9" />

::: important Value Range
The valid range for the computed `line-height` value is $[0, 1000\rm px]$. A line height of $0$ falls back to the default line height (rather than no line height at all). Regardless of whether length or a number (ratio) is used, the computed line height cannot exceed $1000\rm px$. For example, the computed result of `line-height: 2.0; font-size: 32px` is $64\rm px$, making it a valid line height value.
:::

##### Auto Line Height <experimental /> <version-badge since="0.9" />

An `auto` value for `line-height` indicates that the line height will be automatically calculated based on the font size, behaving as follows:
- Under normal circumstances, the default line height is close to 1.2 times the font size.
- For special scripts such as Arabic and Tibetan, the default line height is automatically increased to prevent overlapping between lines; this means different lines within a piece of text may have different line heights.
- Using any non-`auto` `line-height` value overrides the default line height behavior, causing all lines to have the same line height.
- `auto` is semantically similar to CSS's `normal` line height, though direct use of the `normal` keyword is not yet supported.

For details on line height behavior in internationalization scenarios, please refer to the [i18n documentation](/framework/application/i18n.md#自动行高).

::: note Rendering Consistency <version-badge since="0.9" />
Text rendering behavior varies across devices, and the default line height value for `line-height: auto` may differ. Some devices do not automatically adjust line heights for special fonts, but simply use a fixed line height, which may lead to overlapping lines when using auto line height.
:::

##### Line Height Inheritance

When an element does not set `line-height`, it inherits the parent element's line height value. The inherited line height is the raw value, not the computed line height value. For example, if the parent element's `line-height` is `1.5`, the child element inherits `1.5`, not the parent element's computed line height (i.e., $1.5$ times the parent font size). If the parent element's `line-height` is `auto`, the child element also inherits `auto`, not the parent element's computed default line height value.

::: tip `auto` Line Height and Inheritance
`line-height: auto` does not inherit the parent element's line height, but rather defaults to the default line height. To use inherited line height, the `line-height` property must be omitted. Explicitly inheriting via the `inherit` keyword is currently not supported.
:::

#### `text-align` <badge type="info" text="Inherited" />

Defines how text is aligned relative to its block parent element. `text-align` does not control the alignment of the block element itself, only the alignment of its inline text.

Supports the following values:

- `left`: Left alignment
- `right`: Right alignment
- `hcenter`: Horizontal center alignment
- `justify`: Justified alignment
- `top`: Top alignment
- `bottom`: Bottom alignment
- `vcenter`: Vertical center alignment
- `baseline`: Baseline alignment
- `center`: Horizontal and vertical center alignment

::: tip
`text-align: center` centers alignment in both horizontal and vertical directions simultaneously, which differs from CSS where `text-align: center` only centers horizontally. Note this distinction. If you only need horizontal center alignment, please use `text-align: hcenter`.
:::

**Default value**: `left`

#### `max-lines`

Specifies the maximum number of lines to display for text, with overflowing content handled according to what is specified by [`text-overflow`](#text-overflow). The value type is a number, and the default value is `0`, indicating no limit on the maximum number of lines.

Syntax and examples:

```css
max-lines: 0; /* No limit on maximum lines */
max-lines: 1; /* Fixed to single-line display */
max-lines: 2; /* Display at most 2 lines of text */
max-lines: <number>; /* Specify the maximum number of text lines displayed */
```

This property is compatible with the Quick App standard `lines` property.

#### `text-overflow`

Specifies how to signal to users that hidden overflow text content exists. It can either be directly clipped or display an ellipsis (`...`). This property is used in conjunction with [`max-lines`](#max-lines), meaning the overflow behavior is only triggered when the text line count reaches the `max-lines` limit; other clipping caused by layout height limits is not taken into account.

Property values:

- `clip`: Overflowing text is simply hidden;
- `ellipsis`: When text overflows, an ellipsis is added after the displayed text.

**Default value**: `clip`

<glyphix id="css-prop-text-overflow" height="100" width="600" title="Comparison between clip and ellipses">

```html
<div>
  <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>
  <p class="ellipsis">
    Lorem ipsum dolor sit amet, consectetur adipisicing elit.
  </p>
</div>
```

```css
div {
  display: flex;
}

p {
  background-color: #ddd;
  margin: 8px;
  padding: 8px;
  max-lines: 2;
}

.ellipsis {
  text-overflow: ellipsis;
}
```

</glyphix>

### `@font-face` Rule

The `@font-face` CSS at-rule specifies a custom font for displaying text. This font can be used as a font name in the [`font-family`](#font-family) property.

```css
@font-face {
  font-family: sans-serif;
  src: url("fonts/Roboto-Regular.ttf");
  font-weight: 400;
  font-style: normal;
}
```

It is recommended to define `@font-face` rules in the [app-level font mapping file](/framework/application/font-config.md#应用级字体). This section introduces the property definitions within the `@font-face` rule block.

#### `font-family`

The specified font name will be used for the [`font-family`](#基本属性-1) property. Note that this can only be a single font name, not a list of font names. For example: `font-family: <family-name>`.

#### `src`

Specifies the URI of the font file. The value of this property is a list, allowing developers to specify multiple font files for a font. For example:

```css
src: url("fonts/Roboto-Regular.ttf"), url("font/Other-Font.ttf");
```

Currently, the `src` property only supports the `url()` function or a list of strings; web-available functions like `local()` and `format()` are not supported.

## Animation

For more knowledge about animations, please refer to the [Animation](../render/animation.md) section.

### Basic Properties

#### `animation`

Defines the animation effect to be executed by the element. Currently supported formats are:

```css
animation: <name>;
animation: <duration> <timing> <name>;
```

Descriptions of placeholders:

- `<name>`: A keyframe sequence name defined by the [`@keyframes` rule](#keyframes-规则);
- `<duration>`: The duration of the animation, in seconds or milliseconds, e.g., `1000ms`, `0.2s`, defaults to `1s`;
- `<timing>`: [Easing function](../render/animation.md#缓动函数), defaults to `ease`.

### `@keyframes` Rule

Please refer to MDN's [`@keyframes`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@keyframes) documentation.

## Transformation and Display Effects

#### `transform`

The `transform` property allows developers to rotate, scale, skew, or translate elements. This property applies visual transformation effects to the element without altering its layout properties. The value of the `transform` property can be a cascade of various transformation functions from the table below:

|           Value           | Description                                                                 |
| :-----------------------: | --------------------------------------------------------------------------- |
|     `scale(x, y)`      | Scale transformation, $x$ and $y$ specify the horizontal and vertical scale factors respectively. |
|    `rotate(angle)`     | Rotation transformation, $\it angle$ specifies the rotation angle in `deg` or `rad`. |
|     `shear(h, y)`      | Shear transformation, $h$ is the horizontal shear distance, $v$ is the vertical shear distance. |
| `skew(angleX, angleY)` | Skews the element along the $x$ and $y$ axes.                                |
|   `translate(x, y)`    | Translation transformation, moves the element along the $x$ and $y$ axes.    |

For example, the following code will first scale the element by $(2, 0.5)$ and then rotate it by $100^{\circ}$:

```css
transform: scale(2, 0.5) rotate(100deg);
```

**Default value**: `none`

Transformed elements may be clipped by parent elements or occluded by elements located behind them. You can use the [`z-index`](#z-index) property to elevate the element's Z-axis order to avoid occlusion by sibling elements. Currently, the `transform` property may need to work with the [`transparent`](#transparent) property to function properly; otherwise, an incorrect black background may be generated.

#### `z-index`

The `z-index` property sets the Z-axis order of an element. Overlapping elements with a larger `z-index` will cover elements with a smaller one.

#### `opacity`

This property specifies the opacity of an element. It is a numeric value in the range $[0, 1.0]$.

**Default value**: $1.0$ (completely opaque)

::: warning
`opacity` values other than `0` or `1` impact element rendering performance; it is recommended to use this property only when necessary. If you only need to make text or backgrounds semi-transparent, you should use the RGBA format for color values, such as `rgba(255, 0, 0, 0.5)` or `#ff000080` for semi-transparent red.
:::

#### `object-fit`

Used to specify the strategy for how an image should be resized to fit its container determined by height and width.

Property values:

- `none`: Default value. The image retains its original size.
- `contain`: The image is scaled to maintain its aspect ratio while filling the content box of the element. The entire object preserves its aspect ratio while filling the box.
- `cover`: The image fills the entire content box of the element while maintaining its aspect ratio. If the aspect ratio of the object does not match the content box, the object will be clipped to fit.
- `fill`: The image exactly fills the content box of the element. The entire object will completely fill the box. If the aspect ratio of the object does not match the content box, the object will be stretched to fit.
- `scale-down`: The image is scaled down maintaining its aspect ratio to fit the content box dimensions if it is larger than the content box; otherwise, it is not scaled. The actual scale factor for `scale-down` is equivalent to the smaller of `none` and `contain`.

::: note
Unlike the [Web standard](https://developer.mozilla.org/docs/Web/CSS/Reference/Properties/object-fit), the default value of the `object-fit` property is `none` rather than `fill`. For details, please refer to the description of the [`image`](/components/image.md#object-fit) component.
:::

#### `transparent`

Sets whether an element is transparent. This property usually does not affect the display effect of an element, but elements with snapshots may need to configure this property according to actual transparency conditions.

Property values:

- `false`: Marks this element as opaque;
- `true`: Marks the element as transparent.

**Default value**: `false`

#### `stroke-width`

Specifies the brush width when certain components are rendered, such as [`progress-arc`](/components/progress-arc.md). The value type is a [length](/framework/render/style-and-layout.md#长度).

#### `visibility` <badge type="info" text="Inherited" />

Sets whether an element is displayed. This property does not affect layout.

Property values:

- `hidden`: Hides the element;
- `visible`: Displays the element.

**Default value**: `visible`

#### `filter` <experimental />

Applies blur and other effects to an element. Currently supported values:

- `blur(<length>)`: Applies a blur effect to the element, e.g., `blur(5px)`.

::: warning Experimental Feature
On existing devices, using filter effects like `blur()` may cause severe performance issues. Note that the `blur()` function is not strictly a Gaussian blur, and its supported blur radius $r$ range is $r \in [8, 300]\,\rm px$. Specifically:
- When $r \lt 8\rm px$, no blur effect is produced;
- The degree of blur does not vary continuously with changes in $r$.

To improve performance, where visual effects permit, you should choose a larger blur radius (recommended $r \ge 50\rm px$), as Glyphix optimizes for this scenario.
:::

Due to the high overhead of blur effects, it is recommended to use them in conjunction with the native component's [`quiescent`](/framework/generic/properties.md#quiescent) property to avoid frequent rendering updates.

#### `overflow` <experimental /> <version-badge since="0.9" />

The `overflow` property is used to specify how to handle content when it exceeds an element's dimensions. The value of this property can be one of the following:
```css
overflow: auto | clip | visible;
```
- `auto`: Default value. Overflowing content is clipped, equivalent to `clip`.
- `clip`: Overflowing content is clipped, and parts exceeding the element's content-box dimensions will not be visible.
- `visible`: Overflowing content is not clipped by the element's own content-box, but continues to be displayed.

When `overflow` is set to `visible`, content can be drawn within the content-box range of the nearest `clip` ancestor, unaffected by the clipping of itself and intermediate visible containers.

::: tip Differences from Web CSS Standard
The default value of the `overflow` property is not `visible`, but clipping by default. Also, Glyphix does not support values like `scroll` and `hidden`; nor does it support sub-properties like `overflow-x` and `overflow-y`.
:::

##### `overflow` Behavior in Multi-Level Containers

`overflow: visible` is not an inherited property. If you want the overflowing content of the innermost element not to be clipped, every level of container along the path from the root to the target element must have `overflow: visible` set. For example:
```html
<!-- The overflowing content of the innermost item can be displayed completely -->
<div style="width:100px; height:100px; overflow:visible">     <!-- Intermediate container -->
  <p style="width:200px; line-height:100%; overflow:visible"> <!-- Overflowing element itself -->
    Long text in Tibetan, Thai, etc. won't go out of bounds
  </p>
</div>
```

##### Overflow Issues with i18n Text

In internationalization scenarios, text in many languages has a large height, making it prone to exceeding the reserved line height range and suffering vertical clipping. For such cases, it is recommended to set the `overflow` of text elements to `visible` and pair it with an appropriate `line-height` to ensure text content displays completely.

The example below shows the effect when line height is too small under both `overflow: visible` and `overflow: clip` conditions:

<glyphix id="css-overflow-visible" height="80" width="640" title="Text overflow">

```html
<div>
  <p>Some i18n text with large line height.</p>
  <p style="overflow: visible">Some i18n text with large line height.</p>
</div>
```

```css
div {
  font-size: 1.2rem;
  display: flex;
  flex-direction: column;
}

p {
  line-height: 22px;
  margin: 6px;
  border: 1px solid gray;
}
```

</glyphix>

The text above is clipped at `line-height: 22px` (e.g., the lower half of the letter 'g' is cut off), whereas setting `overflow: visible` allows the text to display completely.

For more explanations, please refer to the [i18n documentation](/framework/application/i18n.md#文本溢出).

##### Component-Specific Behavior

Details of how individual components handle `overflow` also vary; please refer to the documentation for components such as [`scroll`](/components/scroll.md#padding-和-overflow), [`p`](/components/p.md), and [`marquee`](/components/marquee.md).

## Color and Background

#### `color` <badge type="info" text="Inherited" /> <badge type="info" text="Inline" />

Sets the text color (foreground color) of an element. For the syntax of color values, please refer to [Color Values](/framework/render/style-and-layout.md#颜色值).

**Default value**: `#ff0000`

#### `background-color` <badge type="info" text="Inline" />

Specifies the background color, which is mutually exclusive with the [`background-image`](#background-image) property. For the syntax of color values, please refer to [Color Values](/framework/render/style-and-layout.md#颜色值).

**Default value**: `#ff0000` (black background)

#### `background-image`

Sets the background image, which is mutually exclusive with [`background-color`](#background-color). Supports the following writing style:

- `background-image: url("path/to/image")`: The `url()` function provides the [URI](../application/resource.md#uri-和路径) of the background image.

Background images are fixed and aligned to the top-right corner of the element for display, and stretching or scaling background images using properties similar to [`object-fit`](#object-fit) is not supported. For such complex scenarios, it is recommended to use a combination of [`stack`](/components/stack.md) and [`image`](/components/image.md) elements.

## Margins and Borders

#### `margin`

Sets the outer margins of an element in all four directions. The `margin` property accepts $1\sim4$ values, following this syntax:

- `margin: x`: Sets top, bottom, left, and right margins all to `x`
- `margin: v h`: Sets top and bottom margins to `v`, and left and right margins to `h`
- `margin: t h b`: Sets top margin to `t`, bottom margin to `b`, and left and right margins to `h`
- `margin: t r b l`: Sets top, right, bottom, and left margins to `t`, `r`, `b`, and `l` respectively.

The type of each value is a [length](/framework/render/style-and-layout.md#长度).

**Default value**: `0`. In fluid layout, setting the left and right margins of block-level elements to `auto` can make the margins fill the width of the container, for example:

```css
.center-box {
  margin: 0 auto;
}
```

This centers block-level elements with the class `center-box` in the container. Similarly, if only the left or right margin is set to `auto`, that margin of the element will expand to fill the space, resulting in right-aligned or left-aligned effects.

<glyphix id="css-margin-auto" height="120" width="360" title="auto margin">

```html
<div>
  <p class="auto">margin: 0 auto</p>
  <p class="left-auto">margin: 0 0 0 auto</p>
  <p class="right-auto">margin: 0 auto 0 0</p>
</div>
```

```css
div {
  background-color: lightgreen;
}

.auto {
  margin: 0 auto;
}

.left-auto {
  margin: 0 0 0 auto;
}

.right-auto {
  margin: 0 auto 0 0;
}

div > p {
  border: 1px solid gray;
  margin-top: 4px;
  margin-bottom: 4px;
}
```

</glyphix>

#### `margin-left`

Sets the left outer margin of an element.

#### `margin-top`

Sets the top outer margin of an element.

#### `margin-right`

Sets the right outer margin of an element.

#### `margin-bottom`

Sets the bottom outer margin of an element.

#### `padding`

Sets the inner padding of an element in all four directions. The `padding` property accepts $1\sim4$ values, following this syntax:

- `padding: x`: Sets top, bottom, left, and right padding all to `x`
- `padding: v h`: Sets top and bottom padding to `v`, and left and right padding to `h`
- `padding: t h b`: Sets top padding to `t`, bottom padding to `b`, and left and right padding to `h`
- `padding: t r b l`: Sets top, right, bottom, and left padding to `t`, `r`, `b`, and `l` respectively.

The type of each value is a [length](/framework/render/style-and-layout.md#长度).

**Default value**: `auto`. Under the default value, the element's `padding` is $0$.

#### `padding-left`

Sets the left inner padding of an element.

#### `padding-top`

Sets the top inner padding of an element.

#### `padding-right`

Sets the right inner padding of an element.

#### `padding-bottom`

Sets the bottom inner padding of an element.

#### `border`

Sets the border styles of an element. Supports the following writing styles:

- `border: <length>`: Represents a border with a outline width of `<length>` and a black color;
- `border: solid`: Represents a border with an outline width of `1 px` and a black color;
- `border: <length> solid <color>`: Represents a border with an outline width of `<length>` and a color of `<color>`.

Where `<length>` is a [length](/framework/render/style-and-layout.md#长度), and `<color>` is a [color value](/framework/render/style-and-layout.md#颜色值).

Glyphix only supports elements having all borders or one of the top, bottom, left, or right borders. For example, `border: solid` gives the element all borders, while `border-top: solid` gives the element only a top border. When multiple border properties coexist in CSS, only the last one takes effect.

#### `border-top`

Specifies the top border style of an element. The value format matches the [`border`](#border) property.

#### `border-right`

Specifies the right border style of an element. The value format matches the [`border`](#border) property.

#### `border-bottom`

Specifies the bottom border style of an element. The value format matches the [`border`](#border) property.

#### `border-left`

Specifies the left border style of an element. The value format matches the [`border`](#border) property.

#### `border-radius`

**Default value**: `0 px`

Sets the border corner radius. Currently supports a single [length](/framework/render/style-and-layout.md#长度) value. The `border-radius` property only takes effect when the element has all borders (see the [`border`](#border) property).

## Pseudo-classes

### `active`

Elements such as buttons will have this pseudo-class when in the pressed state.

### `disabled`

An element has this pseudo-class when it is in the [`disabled`](properties.md#disabled) state, at which point the element does not respond to gesture events. You can typically reduce the element's opacity to communicate this state to the user, for example:

```css
<some-selector>:disabled {
  opacity: 0.5;
}
```

For a more complete example, please refer to the [`disabled`](properties.md#disabled) property.

============================================================
FILE_PATH: src/transl/EN/framework/application/applet-object.md

# Application Object

Each application has an `app.ux` or `app.js` file.

============================================================
FILE_PATH: src/transl/EN/framework/application/cross-device.md

# Cross-Device Adaptation

When your application needs to run on multiple types of devices, you may encounter various interaction compatibility issues. For example:
- Different devices have different screen resolutions and sizes, so applications should layout and scale appropriately across them;
- System fonts and font sizes vary across devices, and applications should adhere to the system style;
- Interface layouts must account for different screen shapes, such as circular screens often using fisheye-warped lists;
- Safe margins of pages may differ under different screen shapes and resolutions.

This document introduces how to develop watch applications compatible with a wide range of devices using the Glyphix application framework with minimal adaptation code.

## Simulator Parameters

When starting the simulator using the `gx emu` command, the `-d` or `--device` parameter can specify the simulated device. For example, `gx emu -d default-watch-466x466` will simulate a circular screen device with a resolution of $466\times 466$ pixels. `gx emu` will remember the device specified by the last `-d` instead of automatically falling back to the default device.

::: tip
If you have installed the PowerShell or Zsh completion script for the `gx` command, typing `gx emu -d` allows you to tab-complete available device names using the `Tab` key. Otherwise, please use `gx list device` first to view the device list, for example:
``` bash
$ gx list device
default-watch-466x466
default
```
:::

By default, the simulator's screen resolution is the same as the actual device. You can use the `-r` or `--real-scale` parameter (`gx emu -r`) to simulate the device's actual physical screen size rather than its resolution. It is not recommended to use the `-r` parameter on non-high-resolution displays, as it will cause the display to appear overly blurry.

Using the `-d` and `-r` parameters allows you to test the display effects of multiple devices through the simulator without needing physical devices.

## Multi-Resolution Adaptation

In Web development, developers usually rely on media queries and units like `px` for fine-grained layout and style adjustments. However, on wearable devices, the optimal font sizes vary too greatly between devices to be precisely planned during development. More importantly, ensuring consistent readability and operational experience for all applications on a device through a unified visual specification is one of the core issues in wearable UI design.

Taking smartwatches as an example, the screen width of different devices may range between $360\rm px$ and $466\rm px$, while the height ranges between $450\rm px$ and $500\rm px$ or so. Therefore, despite the existence of the [`designWidth`](manifest.md#designwidth) configuration, you generally cannot specify the sizes of most interface elements using `px` units. No matter how it is scaled, the `px` unit always presents these problems:
- Different device DPIs or sizes make it impossible to achieve ideal font sizes through fixed pixel dimensions;
- The large aspect ratio differences between circular and rectangular screens make it difficult to specify large padding gaps using pixel values.

This section will introduce layout techniques for addressing these issues.

### Font Size Specification

Please refer to the [`rem` Font Size Units](font-config.md#rem-字号单位) guide in the font specifications to standardize font sizes in your application. **Do not** use `px` as a font size unit.

### Margin Configuration

You can use `px` or any other [length](/framework/render/style-and-layout.md#长度) units to specify smaller margin values, for example:

``` css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  padding: 8px; /* Use px as margin unit */
  margin: 8px;
}
```

<glyphix id="font-config-margins-pixel" height="80" width="300" inline>

```html
<p>The message text.</p>
```

```css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  padding: 8px;
  margin: 8px;
}
```

</glyphix>

Except for `font-size` which uses `rem`, the other properties use `px` units. This is because Glyphix automatically scales the proportion of `px` units for the target device, and smaller `px` values typically carry no risk of overflow or clipping.

However, when size values are large, it is recommended to use percentage values instead, for example:

``` css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  /* Use percentage unit for left padding, please note the margin on the left side of the sample text */
  padding: 8px 8px 8px 40%;
}
```

<glyphix id="font-config-margins-percent" height="80" width="300" inline>

```html
<p>Message</p>
```

```css
p {
  border: 2px solid gray;
  font-size: 1.25rem;
  padding: 8px 8px 8px 40%;
}
```

</glyphix>

This allows better adaptation to devices with vastly different resolutions.

::: warning
Watch device screen heights vary significantly, and large vertical margins require greater attention to compatibility issues.
:::

### Flex Layout

In addition to percentage length units, flex layout provides more flexible interface adaptability. Flex layout should be prioritized over percentage length units. Manual layout—directly specifying the `width` and `height` CSS properties of elements—should be avoided.

An exception where manual layout should be used is an interface displaying network icons, for example:
``` html
<scroll>
  <div class="item" for="item in items">
    <image :src="item.icon" />
    <p>{{ item.title }}</p>
  </div>
</scroll>
```
If the image size pointed to by `item.icon` is not fixed, specifying appropriate width and height for the `image` element will look better, for example:
``` css
scroll {
  display: flex;
  flex-direction: column;
}

.item {
  display: flex;
}

/* Specify fixed width and height for network icons */
.item > image {
  width: 92px;
  height: 92px;
  border-radius: 10px;
  object-fit: fill; /* Stretch or scale image when necessary */
}

/* Text in item takes up remaining space in the row */
.item > p {
  flex: 1;
}
```

Since the [`image`](/components/image.md) component automatically centers images, you don't need to worry about differences in image aspect ratios.

### Media Queries

When no layout strategy can accommodate resolution differences, [media queries](/framework/render/media-query.md) can also be used for targeted adjustments.

## Screen Shape Adaptation

Smartwatches typically come in two screen shapes: circular and rectangular. Circular screens require larger safe margins in the four corners and may use fisheye-effect lists.

### Media Queries

Taking the top bar as an example, circular screens may require the top bar text to be center-aligned, whereas rectangular screen top bar text is left-aligned. The following example demonstrates the layout differences corresponding to the two screen shapes.

<glyphix id="circle-square-screens" height="400" width="800" title="Non-Standard Screen Layout">

```html
<div class="screens">
  <div class="square-screen">
    <p>TITLE BAR</p>
  </div>
  <div class="circle-screen">
    <p>TITLE BAR</p>
  </div>
</div>
```

```css
p {
  font-size: 1.25rem;
  color: #353535;
  margin: 32px;
}

.screens {
  display: flex;
}

.screens > div {
  display: flex;
  flex-direction: column;
  background-color: #adb5bd;
  flex: 1;
  margin: 10px;
}

.square-screen {
  border-radius: 10%;
}

.circle-screen {
  border-radius: 50%;
  /* Left and right sides of circular screens are usually left blank to improve display effects */
  padding: 0 48px;
}

.square-screen > p {
}

.circle-screen > p {
  text-align: center;
}
```

</glyphix>

You can use the [`shape`](/framework/render/media-query.md#shape) feature of media queries to handle the two screen shapes respectively, for example:
``` css
.title {
  font-size: 1.25rem;
  color: #353535;
  /* By default, the title simply leaves a 32px safe margin around it. */
  margin: 32px;
}

/* These style rules only apply to circular screens. */
@media (shape: circle) {
  .title {
    /* On circular screens, the title text should be centered. Other properties are inherited from the .title rule above. */
    text-align: center;
  }
}
```
This CSS code first defines the style rules for square screens and then overrides them for circular screens within a media query block.

### Template Macros

While media queries can be used to define CSS rules for different types of devices, combining [template macros](/framework/component/template-macro.md) with the [`media-query` attribute](/framework/render/media-query.md#组件的-media-query-属性) allows applying different UX template structures to different devices. This technique can automatically add fisheye warping effects to list interfaces on circular devices.

For specific usage methods, please refer to the [Template Macros](/framework/component/template-macro.md) section.

## JavaScript Adaptation

If you need to write different logic for different devices, you can also retrieve [device information](/api/system-device.md). For example, you can get the screen shape enumeration value of the device at runtime via [`device.screenShape`](/api/system-device.md#screenshape).

============================================================
FILE_PATH: src/transl/EN/framework/application/README.md

# Application Framework

A Glyphix application is an interactive program that can run independently, designed specifically for MCU (Microcontroller Unit) devices. It consists of a series of pages, components, and related logic, and is supported and managed by a runtime environment. Through the Glyphix application framework, developers can build and organize applications using HTML templates, CSS, and JavaScript in a way that is close to Web development.

You can think of an application as a standalone program like a mobile app: they can be installed, launched, switched, and uninstalled. Each application has its own resources and data storage space, and runs in a controlled environment.

## Runtime

The runtime is a native system integrated into the device firmware. It provides a standard application runtime environment and manages all system resources required by the application. This section introduces the various responsibilities of the runtime and its behavioral standards.

### Launching Applications

The runtime can launch an application via native or JavaScript APIs. Each application has an independent runtime environment, which means:
- Applications run in independent JavaScript execution environments without interfering with each other.
- Each application has independent resource access, including page structures, file resources, data storage, and various other resources.
- No low-level privileges: The application's runtime environment is unrelated to the underlying system and therefore cannot bypass the runtime to access low-level resources.

However, certain resources are globally unique, such as the visible area of the screen and public file directories. As user operations occur, some applications will enter the **foreground** interactive state, while others will switch to the background.

### Page Management

The interface of a Glyphix application is primarily provided by **pages**. Therefore, the runtime maintains the page objects for each application and manages global popup pages. These management mechanisms include page switching, rendering, and lifecycle control.

### Memory Resource Management

The runtime system uniformly manages memory and various system resources for individual applications and across multiple applications, thereby optimizing overhead and avoiding leaks:
- Postponing loading operations for resources such as images and text to reduce interface loading latency.
- Caching and optimizing page and component files to accelerate hot-loading performance.
- Maintaining resource and low-level file mappings to achieve device-agnostic I/O and resource access.
- Optimizing memory footprint to avoid exhausting MCU memory.

### Resource Reclamation

When an application exits, the runtime reclaims all resources, releasing system consumption back to the level before the application was launched. This is a system-level mechanism that cannot be controlled at the application level, which also means:
- Applications will not fulfill pending Promise objects upon exit, so asynchronous operations may never yield a result. Please note that necessary handling should be done in the application's [`onDestroy`](/framework/component/life-cycle.md#ondestroy-1) lifecycle function.
- The underlying system may kill the application at any time and has complete operational permissions. Absolute persistence cannot be guaranteed at the application level, nor can you assume the device's application scheduling policy.

### Standard APIs

The runtime provides a set of standard [APIs](/api/README.md) that abstract differences in Bluetooth, networking, sensors, and system functions across specific devices. Most APIs are supported by all devices, but some are only supported on specific devices.

### Background Management

The application framework supports running applications in the background, which allows users to return to interfaces like the app list and then return to the current application without restarting it. Background-running applications are subject to certain limitations, such as:
- Background applications cannot navigate pages; APIs such as [`router.push()`](/api/system-router.md#push) will be directly suspended.
- Background applications may automatically return to the main page (i.e., the bottommost page), just like a user returning manually.
- Most applications can only remain in the background briefly and will be killed by the system in about half a minute to release resources.
- Applications performing specific tasks such as audio playback can continue running in the background.

::: tip
If your application needs to play audio in the background (such as a podcast app), please ensure that you start the audio playback task on the main page or in an interface-agnostic script, rather than playing it on deep pages. Otherwise, when the background application returns to the main page, audio playback may be interrupted and lose background residency.
:::

The application background mechanism involves a series of lifecycle management; for details, see [Application Lifecycle](../component/life-cycle.md).

## Pages

Applications are divided into multiple pages, similar to HTML pages: each page implements a category of interaction logic, and users can navigate between multiple pages.

A page is an interface element that fills the entire screen, so only one page can be displayed on the device at a time. To support this, the application framework provides a page stack mechanism: each application can open several pages at runtime, which are maintained in a stack manner, displaying only the top-most page at any given time. Because the page stack is a stack, it supports `push` and `pop` operations, through which new pages can be pushed into the application's page stack or the top page can be closed. In addition, the application framework extends several practical page operations.

Most pages reside in the application's page stack. When the application is in the foreground (i.e., it is the currently displayed application), the page at the top of the page stack is displayed, while all pages of background applications are hidden. The page stacks of different applications are completely independent.

A page consists of a **page component** and several sub-components. All pages must be declared in [`manifest.json`](manifest.md#router) before they can be used. Pages within the application navigate and switch via the [`system.router`](/api/system-router.md) API, which includes a routing mechanism and a data transfer method between pages.

Pages use a stack layout by default, just like the [`stack`](/components/stack.md) component. Therefore, using a template like this within a page component:
``` html
<scroll>
  <p>background</p>
</scroll>
<p>overlay</p>
```

has the same effect as placing it inside a `stack` component:
``` html
<stack>
  <scroll>
    <p>Background</p>
  </scroll>
  <p>Overlay</p>
</stack>
```

You can observe this stacking effect using the interactive demo below. You can use your mouse or touchpad to scroll the "Background" text and observe the stacking layer effect.

<glyphix id="application-page-component" height="200" width="300" title="Page Component Stacking Effect">

``` html
<scroll>
  <p>Background</p>
</scroll>
<p>Overlay</p>
```

``` css
p {
  text-align: center;
  color: #f088;
  font-size: 1.5rem;
}

scroll>p {
  height: 100%;
  color: black;
  font-size: 1.25rem;
}
```

</glyphix>

## Components

For details, see [Component Framework](/framework/component/README.md).

============================================================
FILE_PATH: src/transl/EN/framework/application/i18n.md

# Internationalization

Internationalization is used to translate the user interface into different languages so that users of various languages can use it.

## Internationalization Resources

The internationalization mechanism requires developers to first create the application's internationalization resource files and then use them in component code. Internationalization resources are JSON files stored in the `src/i18n` directory of the application (developers need to create this folder first), with each file named after a language code, for example:
``` bash
src                # Project source code path
└─ i18n            # Internationalization resource folder
   ├─ default.json # Default fallback language
   ├─ ja.json      # Japanese translation file
   ├─ it.json      # Italian translation file
   └─ zh-CN.json   # Simplified Chinese translation file
```
As shown in the example, `default.json` is the translation file for the default fallback language. Its translation rules are used when the text to be translated is not found in the selected language.

The content of an internationalization resource file is a JSON object in the following format:
``` json
// default.json
{
  "helloWorld": "Hello, world!"
}
// zh-CN.json
{
  "helloWorld": "你好，世界！"
}
```
The values of this JSON object are the translated texts in the target language, and the keys are used to index the translated texts in the code. Each key corresponds to translated texts with the same meaning in internationalization resource files of multiple languages. For example, the `helloWorld` key corresponds to the translated text `Hello, world!` in English and `你好，世界！` in Chinese.

### `default.json`

Unlike general language internationalization files, `default.json` is also used as a fallback for translation texts that are undefined in the current language. That is, if a key for an internationalization string is not defined in the JSON file of the target language, but exists in `default.json`, the translation from the latter will be used.

When a key does not exist in any of the above internationalization files, the internationalization framework will directly return the key itself.

## Using Internationalized Text

### `$t()` Function

`$t()` is a global function used to retrieve internationalized text, with the following signature:
``` ts
function $t(key: string): string
```
`key` is the key to be translated, and the return value is the corresponding internationalized text in the current language. If this key-value pair does not exist in the internationalization resources, the `key` itself will be returned.

This function is typically used in component code, for example:
``` html
<p>{{ $t('helloWorld') }}</p>
```

It can also be used in JavaScript code:
``` js
console.log($t('helloWorld'))
```

### `t` Command

Native components support the `t` command for automatic translation of internationalized text:
``` html
<p t>helloWorld</p>
```
The `<p>` component in the example contains an attribute named `t` (which is actually a command). This command is equivalent to automatically calling the `$t()` function using the text child node `helloWorld` as the parameter and using the returned internationalized text to set the text content of the `<p>` component. In template code, the `t` command is simpler to use than the `$t()` function.

The `t` command also supports being used as an attribute prefix for native components, for example:
``` html
<p t:text="helloWorld" />
```
Similar to the standalone `t` command, the attribute value string `helloWorld` will be used as a key to query the corresponding internationalized text. This is also more convenient than the equivalent code using the `$t()` function:
``` html
<p :text="$t('helloWorld')" />
```

::: tip
The `t` command currently only supports native components and has no effect in custom components.

Where the `t` command can be used, please prioritize using the `t` command over the `$t()` function, because the implementation of the `t` directive results in better performance.
:::

### Switching Languages

When the application switches languages, all reactive properties of all components will be recalculated, at which point the internationalized text will be re-queried, so there is no need to manually update the interface. However, `$t()` functions called outside of the reactivity framework do not have this effect.

Cached computed property values are not recalculated when switching languages, so calling `$t()` within a computed property's `get()` method will not re-fetch the translated text.

### Getting Internationalization Configuration

You can access the application's internationalization configuration through the [`@system.i18n`](/api/i18n.md) module. You can also listen to locale changes through the application's [`onLocaleChanged()`](/framework/component/life-cycle.md#onlocalechanged) lifecycle function.

## Layout and Rendering

### Automatic Line Height

[[To be completed]]

### Text Overflow <version-badge since="0.9"/>

In some UI design layouts with limited height, certain internationalized texts may not display completely because the required line height is too large. This can occur when UIs designed for languages like Chinese or English are translated into other languages—for example, the same text content in Tibetan requires a larger line height to display completely.

The following example shows how the same piece of Tibetan text will be clipped due to default rendering behavior at `line-height: 1` (red box on the left):

<div style="display:flex; gap:20px; font-family:monospace; font-size:22px">
<span style="border:1px solid red; width:220px; line-height:1; overflow:clip; background:#fff8f8;white-space:nowrap">
  &#x0F40;&#x0FB5; བོད་ཡིག་གི་ཚིག་ཐུང་།
</span>
<div style="border:1px solid green; width:220px; line-height:1; overflow:visible; background:#f8fff8;white-space:nowrap">
  &#x0F40;&#x0FB5; བོད་ཡིག་གི་ཚིག་ཐུང་།
</div>
</div>

The reserved line height for UIs designed for Chinese or English may not be sufficient, meaning that simply setting a larger `line-height` or using `line-height: auto` may not solve this problem. Therefore, the only solution is to allow text to overflow using `overflow: visible` (green box on the right).

In internationalization scenarios, it is recommended to use [`overflow: visible`](/framework/generic/styles.md#overflow) to prevent text from being clipped.

The [`scroll` component](/components/scroll.md#i18n-场景的推荐设置) documentation also contains i18n configuration instructions regarding the `overflow` property. Please refer to the related documentation for more details.

============================================================
FILE_PATH: src/transl/EN/framework/application/resource.md

# Resource Access

## URIs and Paths

Resources within an application can be accessed via URIs or paths. These resources include files in the application installation package, runtime data files, and shared data files. Unlike Web environments, URIs and paths in Glyphix applications are primarily used to access local files rather than resources on the network.

Many [APIs](/api/README.md) and [native components](/components/README.md) use URIs or paths to access resources, and these interfaces generally allow URIs and paths to be used interchangeably.

### URIs

The format of a URI is similar to a [URL](https://developer.mozilla.org/docs/Glossary/URL), and its syntax is defined in the diagram below:

![](./figures/uri-syntax.svg)

Descriptions of each field are as follows:
- **scheme**: Specifies the protocol for resource access, such as `app`, `internal`, etc.;
- **authority**: Usually represents the package name or domain name, and its meaning is determined by the specific resource protocol;
- **path**: The path of the resource inside the resource package, which must be a string starting with the `/` character (just like paths in Unix);
- **query**: Specifies query data, generally used only to pass parameters during application navigation.

Here are some examples of URIs:
```
      authority
      ↓
app://com.example.app/icon.png
↑                    ↑
scheme               path
           authority
           ↓
internal://files/favicon.png
↑                ↑
scheme           path
      authority                query
      ↓                        ↓
app://com.example.app/icon.png?key=value
↑                    ↑
scheme               path
```

URIs can be used to locate resources in other applications as well as system resources, and can also access application cache or temporary files. Pay attention to whether the application has the appropriate permissions when accessing external resources. Unlike the Web platform, Glyphix URIs are typically used to access local resources and cannot access network resources. Please use the [`system.fetch`](/api/system-fetch.md) or [`system.request`](/api/system-request.md) modules instead.

### Paths

Paths are another way to locate resources, and they can only define resources inside the application package. There are two ways to write a path: one is an absolute path starting with `/`, such as `/assets/images/icon.png`; the other is a relative path, such as `images/icon.png`. Absolute paths are relative to the root directory of the application resource package (which is the project's `src` directory), while relative paths are relative to the current resource file. Therefore, in
``` js
// in file: /Common/module-a.js
import x from '/Common/module-b.js'
import y from 'module-b.js'
```
`x` and `y` actually import the same module.

You can use `..` to locate the parent directory, such as `../fonts/Times.ttf` or `/images/../fonts/Times.ttf`. However, `..` cannot go beyond the project root directory level, so `/a/../..` will be restricted to `/`.

Absolute paths can be used for the path field of a URI.

## URI Protocols

### `app`

Under this protocol, the authority field is the application's package name, which is the `manifest.package` field. The `path` field is the path of the resource within the application resource package.

The `app` protocol can be used to access resources of other applications.

### `file`

To be added.

### `pkg`

To be added.

### `internal`

The `internal` URI protocol is used to access internal resource files of the application, especially those that cannot be accessed via conventional static [paths](#paths). For example, an application might generate temporary files, cache files, or private files that cannot be accessed via paths (paths can only access static resources within the resource package), and should instead be accessed and managed via the internal protocol.

The basic format of common `internal` URI protocols is as follows:
``` ebnf
internal://<authority>/<path>
```
- **authority**: Determines the storage location of the resource file; see below for specific functions.
- **path**: The path relative to the specified storage location, pointing to the specific file.

#### authority Field

The **authority** field determines the category and storage location of internal resources. Depending on its value, the meaning of the `authority` field is as follows:
- `cache`: Indicates that the URI points to the application's cache directory, typically used to store cache files. Files in this directory are temporary files generated during application runtime and can be deleted or rebuilt at any time.
- `files`: Indicates that the URI points to the application's private file directory. This is a storage location dedicated to the application for saving file data that needs to be persisted.
- `mass`: Indicates that the URI points to a file directory shared by all applications. This is usually a public directory where multiple applications can store and read files.
- `tmp`: Indicates that the URI points to the system's temporary file directory, typically used to store short-lived temporary files. Files stored here have a brief lifespan and may be cleared when the system or application restarts.

For example, `internal://cache/images/avatar.png` represents accessing the image file `avatar.png` in the cache directory. This URI can be used in multiple scenarios such as the [image](/components/image.md) component:
``` html
<image src="internal://cache/images/avatar.png" />
```

::: warning
The **authority** field does not support URI encoding and must use literal values like `cache` and `files` directly, rather than encoded forms such as `%63%61%63%68%65`. The **path** field supports URI encoding (though not recommended), but in addition to regular file path rules, it must comply with the following restrictions: the `%` character must not appear in the path, and it cannot use `..` to traverse up to the root directory.

These restrictions are designed to prevent bypassing internal resource access rules through encoding or path traversal, thereby avoiding potential security risks.
:::

#### Application File Isolation

When using the `internal` URI protocol, the `cache`, `files`, and `tmp` categories are all private storage areas of the application, and only the current application can access files in these directories. Therefore, the same `internal` URI may point to different files in different applications. Each application has an independent private cache, file, and temporary file storage space, ensuring file isolation and data security between applications.

Suppose there are two different applications A and B, both using the same URI to access a private file:
```
internal://files/config/settings.json
```
Then:
- In **Application A**, this URI points to the `settings.json` file in its private file directory.
- In **Application B**, this URI points to the `settings.json` file in its private file directory.

This mechanism ensures that applications manage their own files independently without interfering with each other, and avoids potential data leaks.

In contrast, `internal://mass/` is a public file storage area shared by all applications. The same `internal` URI points to the same file across different applications. Therefore, files in the `mass` directory can be accessed and shared by multiple applications. For example, if both Application A and Application B use:
```
internal://mass/public/shared_image.png
```
Then this URI points to the same public file `shared_image.png` in both applications, allowing them to share that file resource.

::: warning
If an application stores sensitive data in the `mass` space, other applications may read that data. Therefore, developers should avoid storing any sensitive or private information in the `mass` directory, ensuring that the files stored within it are publicly accessible and shareable resources.
:::

## Resource APIs

The [`URI`](/api/global.md#uri) global function, [`@system.path`](/api/system-path.md), [`@system.file`](/api/system-file.md), and other interfaces provide the ability to manipulate resources in JavaScript. Please refer to the relevant documentation for details.

============================================================
FILE_PATH: src/transl/EN/framework/application/manifest.md

# manifest File

The `manifest.json` file contains information such as application descriptions, interface declarations, and page routing.

`manifest.json` is a JSON file, and its content must be a JSON Object. This document introduces the functions of each field in `manifest.json`.

## Field Descriptions

### Root Properties

These fields are properties of the root JSON object in the `manifest.json` file.

::: details Type Signature
``` ts
interface Manifest {
  package: string,
  name: string,
  icon: string,
  versionName: string,
  versionCode: number,
  config?: Config,
  permissions?: PermissionInfo[],
  router: Router,
  display?: Display,
  dial?: Dial,
  widgets?: Widget[]
}
```
:::

#### `package` <decl type="string" />

The `package` field is the application's package name and is a required field. It is recommended to use the format `com.company.module`, such as `com.example.demo`. Application package names must be unique within the system.

::: important
App stores of many device manufacturers do not support hyphens `-` as part of the package name, so please avoid using them. We also do not recommend using underscores `_` or `.` as replacements; in such cases, simply connect the words directly, e.g., `com.wateralert.demo`.
:::

#### `name` <decl type="string" />

The display name of the application, which is a required field. It should be within 6 Chinese characters and match the name saved in the app store. It is used to display the application name on desktop icons, pop-up windows, etc. This field can use `${}` expressions to reference [internationalized strings](i18n.md), for example:
``` json
{
  "name": "${appName}"
}
```
Here, `appName` is the key for an internationalized string. Internationalized application names allow the device's application list to display the app name in the current language rather than a fixed language.

#### `icon` <decl type="string" />

The path to the application icon, for example `/assets/icon.png`.

#### `versionName` <decl type="string" />

The application version string.

#### `versionCode` <decl type="number" />

The application version code, which is an integer. It is recommended to increment the version code by one every time an application is released.

#### `config` <decl type="?: Config" />

An optional field describing system configuration information. See the [`Config` Object](#config-object).

#### `permissions` <decl type="?: PermissionInfo[]" />

An array consisting of `PermissionInfo` objects, representing the list of permissions used by the application. When the app needs to access capabilities such as location information, sensors, device information, audio recording, Bluetooth, or health data, the corresponding permissions must be declared in this field, for example:

``` json
{
  "permissions": [
    { "name": "watch.permission.LOCATION" },
    { "name": "watch.permission.RECORD" }
  ]
}
```
The `PermissionInfo` object describes the permission information required by the application, and currently it only has a `name` field. Its signature is as follows:
``` ts
type PermissionInfo = {
  name: string; // Permission name, uniquely identifying a permission item
}
```
The `name` field identifies the specific permission name. The permission names correspond to the system module interface list as follows:

| Permission Name                       | Corresponding System Module                         | Permission Description                             |
| ------------------------------------- | --------------------------------------------------- | -------------------------------------------------- |
| `watch.permission.FOREGROUND_SERVICE` | [`@system.app`](/api/system-app.md)                 | Keep the application running in the foreground     |
| `watch.permission.LOCATION`           | [`@system.geolocation`](/api/system-geolocation.md) | Location information                               |
| `watch.permission.ACCESS_SENSORS`     | [`@system.compass`](/api/system-sensor.md)         | Built-in sensors (e.g., compass, accelerometer)    |
| `watch.permission.DEVICE_INFO`        | [`@system.device`](/api/system-device.md)           | Device information                                 |
| `watch.permission.RECORD`             | [`@system.media`](/api/system-media.md)             | Permissions required only for audio recording APIs |
| `watch.permission.BLUETOOTH`          | [`@system.bluetooth.ble`](/api/system-ble.md)       | Allow the use of device Bluetooth                  |
| `watch.permission.READ_HEALTH_DATA`   | Not supported yet                                   | Read health data (e.g., step count, heart rate)    |
| `watch.permission.SCHEDULE`           | [`@system.schedule`](/api/system-schedule.md)       | Set scheduled tasks                                |
| `watch.permission.NOTIFICATION`       | [`@system.notification`](/api/system-notified.md)   | Allow application notification reminders           |

#### `router` <decl type="Router" />

A required field describing the in-app page routing information. See the [`Router` Object](#router-object) for details.

#### `display` <decl type="?: Display" />

Configuration for in-app display effects. See the [`Display` Object](#display-object) for details.

#### `dial` <decl type="?: Dial" />

If the `dial` field is present, it indicates that this project is a watch face package rather than an application. The exclusive metadata of the watch face is described by the [`Dial` Object](#dial-object). Watch face packages do not use the [`icon`](#icon) field.

#### `widgets` <decl type="?: Widget[]" />

Represents the configuration information for the list of widgets and small components. See the [`Widget` Object](#widget-object) for configuration field details.

### `Config` Object

::: details Type Signature
``` ts
interface Config {
  designWidth?: number,
  designImageScale?: number,
  fontFaces?: string,
  assets?: string | string[]
}
```
:::

#### `designWidth` <decl type="?: number" />

The baseline width for page design (in pixels), with a default value of `750`. The `px` length unit in CSS is scaled based on the ratio of the actual device width to `designWidth`. For example, when `designWidth` is `466`, the pixel length on a device with an actual width of `410` pixels will be scaled by a factor of $410/466$.

It is recommended to use the screen size of the device you are currently designing for, rather than the default `750`, to avoid a large amount of conversion during development.

#### `designImageScale` <decl type="?: number" />

The slice scaling factor for image resources, with a default value of $1.0$. To meet multi-device resolution adaptation requirements, designers need to scale up images according to the design draft before slicing to ensure the quality after packaging.

`designImageScale` is the ratio between the size of the original resource image in the project and the logical resolution of the scaled image. Specifically, the scaling factor $\it{scale}$ of the resource image on the actual device is:
$$
\it{scale} = \tt{designImageScale}\frac{\tt{deviceWidth}}{\tt{designWidth}}
$$
where $\tt{deviceWidth}$ is the actual width of the device screen. Therefore, the actual display size $(w', h')$ of the image is:
$$
(w', h') = \it{scale} \cdot (w, h)
$$
where $(w, h)$ is the size of the original resource image.

::: tip
Do not use a `designImageScale` configuration smaller than $1$, as this means resource images will be upscaled during packaging, resulting in noticeable blurring and distortion. If you want your application to display images exquisitely across multiple devices, you should prepare resource images at a larger size than actually required and set the correct `designImageScale` parameter.

For example, if the image size displayed on the actual device (assuming $\tt{designWidth} == \tt{deviceWidth}$) is $96\rm px \times 96\rm px$, you can prepare $192\rm px \times 192\rm px$ assets with double the resolution, and set `designImageScale` to $2$.
:::

#### `fontFaces` <decl type="?: string" />

Specifies the file path of the application-level font mapping table, where defined fonts can be used directly within the application. This path can be a relative path to `manifest.json` or an absolute path to the root directory of the application resource package.

Refer to [Font Configuration](font-config.md).

#### `assets` <decl type="?: string | string[]" />

Specifies the glob pattern (file wildcard) for custom resource paths. For example:
``` json
{
  "config": {
    "assets": [ "assets/**", "**/data.bin" ]
  }
}
```
This will package all files under the `assets` directory in the project and all `data.bin` files in the project. These files will only be packaged in the form of static resource files (i.e., copied directly).

File wildcards can be the same as paths, but have the following special forms:
- `*` matches a path component, excluding path separators (`/`).
- `**` matches any number of path components and can include path separators.

For example:
- `test.js` can match the `test.js` file under the project root directory.
- `**/*-data.bin` can match files with the `-data.bin` suffix under any path.
- `*/*.bin` matches files with the `.bin` suffix under any level of directory in the project root.

### `Router` Object

Defines the page composition and related configuration information.

::: details Type Signature
``` ts
interface Router {
  entry?: string,
  pages: { [name: string]: PageInfo }
}
```
:::

#### `entry` <decl type="?: string" />

The name of the application's home page. When the application starts, it will first navigate to this page. Defaults to `"main"`.

#### `pages` <decl type="{ [name: string]: PageInfo }" />

Declares information for each page. The key `name` of the `pages` property is the page name, and the property value, the [`PageInfo` Object](#pageinfo-object), is the detailed configuration information of the page. For example:
``` json
{
  "router": {
    "entry": "Main",
    "pages": {
      "Main": {
        "path": "/Path/To/Main",
        "component": "index",
        "launchMode": "singleTask"
      }
    }
  }
}
```

All pages in the application must be entered into the routing table before they can be used, and each page must also have a unique name.

### `Display` Object

#### `pageAnimation` <decl type="?: PageAnimation" />

The default transition animation configuration for pages within the app. The value is a [`PageAnimation` Object](#pageanimation-object).

## `PageInfo` Object

The page configuration object is the property value of the `router.pages` object. The type of the page configuration object is Object. This section introduces the property field definitions of the page configuration object.

::: details Type Signature
``` ts
interface PageInfo {
  path?: string,
  component?: string,
  pageAnimation?: PageAnimation,
  launchMode?: 'standard' | 'singleTask'
}
```
:::

#### `path` <decl type="?: string" />

The path of the page directory (the path of the folder where page components are stored). Defaults to the same as the page name, which is the key of the `Router` object.

#### `component` <decl type="?: string" />

The name of the page component, which matches the UX file name without the *.ux* extension. For example, the component name `"index"` corresponds to the `index.ux` file.

#### `pageAnimation` <decl type="?: PageAnimation" />

The transition animation configuration for the page. The value is a [`PageAnimation` Object](#pageanimation-object). This configuration takes precedence over the `display.pageAnimation` configuration in `manifest.json`.

#### `launchMode` <decl type="?: 'standard' | 'singleTask'" version="0.8" />

The launch mode of the page, defaulting to `standard`. When a page's `launchMode` is configured as `singleTask`, if you attempt to open a page instance that is already in the back stack, all pages above that instance will be popped, and the app will return to the page where that instance resides (similar to [`router.back('<page-name>')`](/api/system-router.md#back)), rather than creating a new page instance.

When "opening" and returning to an existing page in `singleTask` mode, the [`onRefresh`](../component/life-cycle.md#onrefresh) lifecycle function will be triggered.

### `PageAnimation` Object

The properties of this object configure the behavior of page transition animations. Transition animations are only valid for the top-most page; pages that are not on top will not play transition animations.

::: details Type Signature
``` ts
interface PageAnimation {
  openEnter?: string,
  closeEnter?: string,
  openExit?: string,
  closeExit?: string
}
```
:::

Each property can take the following values:
- `"none"`: No transition animation, which is the default value for all properties.
- `"slide"`: The page transitions with a sliding animation. This transition effect varies depending on the transition configuration property, where:
  - For `openEnter` transitions, the slide effect is that the page enters from the left side of the screen towards the right until it completely covers the screen.
  - For `closeExit` transitions, the slide effect is that the page slides to the right starting from its position completely covering the screen until it completely leaves the screen.
  - For `closeEnter` and `openExit` transitions, the slide effect has no animation.

Default transition animations for pages and applications are defined by the device. If `pageAnimation`-related fields are not specified in `manifest.json`, some devices may not play transition animations, while other devices may use custom animation effects provided by the manufacturer.

::: warning
The simulator will always play slide page transition animations regardless of which device it is emulating. If you want to ensure that page transition animations are disabled, use a syntax like:
``` json
{
  "pageAnimation": { "openEnter": "none" }
}
```
instead of `"pageAnimation": {}`, as the latter does not work for unknown reasons.
:::

#### `openEnter` <decl type="?: string" />

This property configures the transition animation for a new page when it is opened.

#### `closeEnter` <decl type="?: string" />

This property configures the transition animation for the old page underneath that will be covered when a new page is opened.

#### `openExit` <decl type="?: string" />

This property configures the exit transition animation for a page when it is closed.

#### `closeExit` <decl type="?: string" />

This property configures the transition animation for the page that will be re-displayed beneath the closed page when it is closed.

### `Dial` Object

The `Dial` object describes configuration information related to watch faces.

::: details Type Signature
``` ts
interface Dial {
  component: string,
  preview: string
}
```
:::

#### `component` <decl type="string" />

The path to the watch face entry component. This can be an absolute path within the package or a relative path to the `manifest.json` file.

#### `preview` <decl type="string" />

The path to the watch face preview image. This can be an absolute path within the package or a relative path to the `manifest.json` file.

### `Widget` Object

The `Widget` object describes configuration information for widgets or small components.

::: details Type Signature
``` ts
interface Widget {
  name: string,
  component: string,
  preview: string
}
```
:::

#### `name` <decl type="string" />

The name of the widget/small component. Widgets within the same application package cannot share duplicate names.

#### `component` <decl type="string" />

The path to the widget/small component entry component. This can be an absolute path within the package or a relative path to the `manifest.json` file.

#### `preview` <decl type="string" />

The path to the widget/small component preview image. This can be an absolute path within the package or a relative path to the `manifest.json` file.

============================================================
FILE_PATH: src/transl/EN/framework/application/font-config.md

# Font Specifications

The Glyphix framework comes with built-in system fonts, and applications can also define their own custom fonts.

## System-Level Fonts

These system fonts are guaranteed to be provided in all environments running Glyphix:
- `sans-serif`: The default sans-serif font.

The actual font files provided by different devices may vary, but these font names are always available.

### Default Font

If a UI element does not specify all font properties (font family, font size, etc.), the remaining properties will take the system default values. Therefore, when a UI element has no font properties specified, the system default font is used. The default font properties are specified by the device and have the following values:
- [`font-family`](/framework/generic/styles.md#font-family) is `sans-serif`;
- [`font-size`](/framework/generic/styles.md#font-size) is `1rem`.

### Glyph Fallback Issue

Due to device performance limitations, it is not possible to pre-install complete fonts for all languages and character sets. We only provide "primary fonts" for specific languages, which typically include common letters, numbers, and symbols. However, if you attempt to use uncommon characters, special symbols, or characters not included in these primary fonts, a "glyph fallback" phenomenon will occur.

When a character cannot be rendered by the currently supported font, it falls back to display as a "box". For example, here is the effect of displaying the text "Hello, 世界。" using the Roboto font, which does not support Chinese:

<glyphix id="font-config-fallback" height="30" width="300" inline>

```html
<p>Hello, 世界。</p>
```

</glyphix>

Among them, the three characters "世界。" are not supported and are therefore rendered as three boxes.

## Application-Level Fonts

### Font Mapping File

The [`manifest.config.fontFaces`](manifest.md#fontfaces) field can be used to configure application-level font mapping files. This is a CSS file containing only [`@font-face` rules](/framework/generic/styles.md#font-face-规则). Fonts defined here can be used directly within the application without referencing the CSS file.

Assuming the font mapping file path in the project is `src/assets/font-faces.css`, the `manifest.config.fontFaces` field should be configured as follows:
``` json
{
  "config": {
    "fontFaces": "assets/font-faces.css"
  }
}
```
The following is an example of the contents of the `src/assets/font-faces.css` file:
``` css
@font-face {
  font-family: Montserrat;
  src: url("fonts/Montserrat-Regular.ttf");
  font-weight: 400;
  font-style: normal;
}
```
Other CSS files can also be imported via `@import` rules, but only `@font-face` rule information will be retained in the font mapping file.

### `@font-face` Rules

You can also define and use fonts directly in CSS using [`@font-face` rules](/framework/generic/styles.md#font-face-规则). This approach is similar to standard web development workflows.

::: tip
Compared to defining fonts in individual CSS files, application-level fonts defined in the font mapping file run more efficiently and should be preferred.
:::

### When to Use Application-Level Fonts

For performance- and resource-constrained devices, the default fonts provided by the system have a lower resource footprint and better performance, and developers should prioritize using them. Custom fonts are recommended only for specific requirements. Here are the specific guidelines:
- **Prioritize system-level fonts**: System-level fonts are optimized to reduce storage footprint and processing overhead. In most cases, they can meet the needs of ordinary text display, such as menus, main pages, and descriptive text.
- **Use custom fonts for specific design requirements**: If an application needs to conform to a specific visual design style or brand requirement, custom fonts can be used. For example, an application might need to display a digital clock with a unique style, or emphasize text in certain headings and buttons; using custom fonts can achieve an effect that better matches the design language.
- **Custom fonts should have a streamlined character set**: To avoid unnecessary storage and processing overhead, the character set of custom fonts should be kept as lean as possible. Generally, it only needs to include Latin letters, numbers, and necessary punctuation marks. For example, when designing a digital clock, the custom font should only include the numeric characters $0 \sim 9$.

::: warning
Do not use large font files (such as Chinese fonts) in your application. Large font files can pose severe performance and resource risks. Typically, system-level fonts already include the character support required for the current language, eliminating the need to supplement the character set with custom fonts.
:::

## The `rem` Font Size Unit

To achieve a font style consistent with the system across different devices, we introduce the `rem` unit, which is slightly different from web development. `1rem` is the system body text size defined by the device manufacturer. When the [`font-size`](/framework/generic/styles.md#font-size) property is not defined in CSS, the default font size of an element is `1rem`. There is no fixed conversion ratio between `rem` and [length](/framework/render/style-and-layout.md#长度) units such as `px` or `pt`. A font size of `1rem` typically corresponds to around `24px` to `32px`.

Using `rem` as the font size unit ensures consistent rendering of all applications in the system. **Do not** use units like `px` to set font sizes, otherwise, they may not scale properly across devices. Specifically, the following configurations are recommended:
- **Headings** use `1.25rem`, and multi-level headings can choose other appropriate sizes;
- **Body text** uses the default font size, which is `1rem`, and generally should not be explicitly specified;
- **Footnotes** use `0.85rem`.

Developers are advised to choose a small, fixed set of font size tiers and use our recommended sizes in the $3$ scenarios mentioned above.

============================================================
FILE_PATH: src/transl/EN/framework/render/style-and-layout.md

# Styles and Layout

The styling system in Glyphix is similar to CSS in web technologies. Typically, CSS is defined directly inside the `<style>` tag of a UX file.

## Writing CSS

You can write CSS inside the `<style>` tag:

``` html
<style>
  div { display: flex; }
</style>
```

You can use the `@import` command to import CSS files:

``` html
<style>
  @import 'style.css';
  div { display: flex; }
</style>
```

Glyphix also provides limited support for inline styles, which are written directly in the `style` attribute of a component:
``` html
<div style="background: #f00; color: #fff"> ... </div>
```
The value of an inline style is a string, and you can update the styles by changing this string. [CSS properties](/framework/generic/styles.md) that support being used in inline styles are tagged with <badge type="info" text="Inline" />.

::: warning
Inline styles in the current version are relatively inefficient and should only be used as a solution for updating component styles via JS logic. Heavy usage may cause performance issues. In general, you should use CSS rules defined within the `<style>` tag.
:::

## Style Selectors

Currently, the styling framework supports the following selectors:

- Class selector
- Type selector
- ID selector
- Pseudo-class (rarely used)
- Pseudo-element (rarely used)
- Descendant selector and direct descendant selector, such as `div > .title` or `div .title`
- Compound selector, such as `#id.class` or `div.class`

### Class Selector

A class selector selects components with the corresponding `class` attribute. A component can have multiple class values, for example:
``` html
<p class="ceil content">...</p>
```
This will match the following two style definitions:
``` css
.ceil {
  background-color: #222;
  border-radius: 12px;
}

.content {
  font-size: 24px;
  padding: 12px;
}
```

### Grouping Selectors

You can use `,` to specify multiple selectors for a rule-set:
``` css
#id, .class, div {
  display: flex;
  flex-direction: column;
  color: red;
}
```

### Inherited Properties

Certain CSS properties can be inherited from parent elements down to child elements. Taking `font-size` as an example:
``` html
<div>
  <p>Text</p>
</div>
```

``` css
div {
  font-size: 1.25rem;
}
```
Even though the `font-size` property is not explicitly set on the `<p>` element, it will still display with a font size of `1.25rem`. This is because the `<p>` element inherits the font size setting from its parent `<div>`. In other words, once an inheritable style property is set on a container, all child elements will also inherit that property setting. However, note that the priority of the CSS property inheritance mechanism is very low, and inherited values are only used when the element has no specified style property of its own. Suppose the following CSS is applied to the example above:
``` css
* {
  font-size: 1rem;
}
div {
  font-size: 1.25rem;
}
```
Due to the presence of the `*` rule style block, the `<p>` element's font size will now be `1rem` instead of using the inherited value.

In the [CSS Properties](/framework/generic/styles.md) documentation, properties that support inheritance are tagged with <badge type="info" text="Inherited" />.

### Reactive Support

Currently, neither the `class` attribute nor the `id` attribute supports reactivity. Therefore:
``` html
<div class="{{expr}}" id="{{expr}}"> ... </div>
```
Neither of these is supported; you can only write static `class` and `id` attribute values directly.

::: warning
Developers must be aware of the limitation that `class` and `id` do not support reactive properties!
:::

## Color Values

### Color Codes

Color values support RGB or RGBA color codes starting with the `#` character. Valid color codes include:

- `#RRGGBB[AA]`, for example, `#102000`, `#00ff0080`
- `#RGB[A]`, for example, `#0f0`, `#ff08`

If a color code does not contain an alpha channel, its value defaults to `ff` (for `#RRGGBB` format) or `f` (for `#RGB` format). Each digit in a color code is a hexadecimal number, with available characters being `0-9`, `A-F`, and `a-f`. `#RGB[A]` is a shorthand method for `#RRGGBB[AA]` codes; for example, the color `#0f38` is identical to `#00ff3388`.

### Color Functions

Currently, CSS blocks support defining color values using the `rgb()` and `rgba()` functions. HSL color formats are not supported.

### Standard Color Names

You can use standard web color names within CSS blocks, for example:
``` css
color: brown;
color: lightgray;
```

### Colors in Inline Styles

Inline styles only support color codes starting with `#`, for example:
``` html
<p style="color: #ff00ff">...</p> <!-- Supported -->
<p style="color: gray">...</p> <!-- Not supported, cannot be parsed -->
```

## Lengths

The general format for length values is `<value><unit>`, where `value` is the numeric value of the length, and `unit` is the length unit, such as `15px`. There should be no space between `value` and `unit`.

A special length value `auto` is also supported. This length value has no specific numerical value or unit, and its actual rendered length is determined by the specific scenario and rules.

The following length units are available:

- `px`: Pixels as the length unit
- `pt`: Points as the length unit, where one point is $1/72$ of an inch
- `%`: Percentage length unit; the specific value varies in conversion relation depending on the property and layout
- [`rem`](/framework/application/font-config.md#rem-字号单位): Length unit relative to the system default font size, for example, `1rem` equals the size of the system default font, and $1.5\rm rem$ is $1.5$ times the former.

Among them, `pt` is an absolute length unit—for example, `72pt` corresponds to $1''$ (inch) or $25.4\rm mm$—which is device-independent. On the other hand, `px` is device-dependent, though it does not directly correspond to physical pixels; please refer to the [`manifest.config.designWidth`](/framework/application/manifest.md#designwidth) field description for conversion relations. Percentage length units are usually calculated relative to the dimensions of the parent element or the element itself; for example, percentage values for CSS properties like `width` and `margin` are calculated based on the parent element's dimensions, while `border-radius` is calculated based on the element's own dimensions.

The `rem` unit is specifically used for font sizes (i.e., the `font-size` property), serving as a simple cross-device font consistency solution. For more details, please refer to the [`rem` Font Size Unit](/framework/application/font-config.md#rem-字号单位).

## Layout

The layout framework can automatically arrange elements based on interface content and screen geometry information, eliminating the need for developers to manually specify element positions and sizes. The layout framework is a powerful mechanism that allows interfaces to adapt to devices of varying resolutions or sizes, while also handling dynamic content. Most native Glyphix components support two automatic layout modes: flow layout and flexbox layout, while also supporting manual layout. Certain native components have enforced special layouts; for example, the children of the [`swiper`](/components/swiper.md) component are always as large as the viewport, whereas the [`stack`](/components/stack.md) component is designed entirely to provide a stacking layout.

The concepts of flow layout and flexbox layout originate from web standards, but have been adjusted for low-performance devices.

## Media Queries

In CSS, [media queries](media-query.md) are primarily used via [`@media` rules](media-query.md#css-media-规则) to control CSS styles based on specific device or media types. For specific details regarding media queries, please refer to the relevant [documentation](media-query.md).

## Less Extensions

If you want to use [less](https://lesscss.org/) as your CSS preprocessor, you must first install the `less` package via a [package manager](/tutorials/nodejs.md):

::: code-tabs
@tab npm
```bash
npm install -D less
```

@tab pnpm
```bash
pnpm i -D less
```

@tab yarn
```bash
yarn add -D less
```
:::

::: tip
Globally installed `less` (such as `npm install -g less`) will not be recognized by the Glyphix bundling tool, so you must install the `less` package within your project using the method above.
:::

You can then use the `lang="less"` attribute in the `<style>` tag of your UX file to specify the style type:

``` html
<style lang="less">
@color: #4D926F;

.header {
  color: @color;
  .nested {
    font-size: 0.75rem;
  }
}
</style>
```

============================================================
FILE_PATH: src/transl/EN/framework/render/media-query.md

# Media Queries

Media queries allow developers to use different styles for different device types. Currently, media queries support CSS `@media` rules, while the component `media` property is not yet supported.

## CSS `@media` Rules

The syntax of the `@media` rule is:
``` css
@media <query> {
  <css-rules>
}
```
[`<query>`](#query-conditions) is used to query media types and media features, and can be combined using various logical operators. When the media query condition is met, the CSS rules within `<css-rules>` will take effect. For example:
``` css
@media screen and (shape: circle) {
  @import "circle.css";
}
```
The `@import "circle.css"` rule is only applied on devices with circular screens. `<css-rules>` can be any CSS rules, which include any number of `@import`, `@font-face`, selectors, and `@media` rules, etc.

## Component `media-query` Property

The `media-query` property can be used on any component to determine whether the component should be rendered based on media [query conditions](#query-conditions). For example:
``` html
<div media-query="(shape: circle)">
  ...
</div>
```
The `<div>` here is a component that will only be rendered on devices with circular screens.

The `media-query` property is only processed during the packaging stage, and components that do not meet the media query conditions will be directly removed. When the elements selected using the `media-query` property are relatively complex, consider using [Template Macros](../component/template-macro.md).

## Query Conditions

A query condition is an expression with the following structure:
``` ebnf
(* Media query expression *)
<query> := <query> and | or | , <query>  (* Logical combination using and, or, , *)
         | (not <query>) (* not expression *)
         | <media-type>  (* Media type *)
         | (<feature>: <value>)
         | (<feature> <relop> <value>)
         | (<value> <relop> <feature> <relop> <value>)
(* Relational operators *)
<relop> := < | <= | > | >=
```
Where `<media-type>` is a [media type](#media-types), `<feature>` is any [media feature](#media-features), and `<value>` is the value supported by that media feature. The following are all valid query condition expressions:
``` css
@media screen { ... }
@media screen and (shape: rect) and (width < 500px) { ... }
@media not (shape: rect) { ... } /* This is equivalent to selecting a circular screen */
```

### Logical Operators

Multiple query condition expressions can be combined using `and`, `or`, and `,`, and the `not` operator can be used to negate a query condition. Parentheses can also be used to increase operator precedence:
``` css
@media (not (width < 500px)) or (orientation: portrait) { ... }
```
The meanings of various operators are as follows:
- `A and B` is met when both `A` and `B` are met;
- `A and B` (note: typically referring to `or` logic) and `A, B` are met when either `A` or `B` is met;
- `not A` is met when `A` is not met, and vice versa.

### Relational Operators

Some media features support relational operators, such as `width`:
``` css
@media (width > 500px) { ... } /* Select devices with a width greater than 500px */
@media (400px < width <= 600px) { ... } /* Range comparison is supported */
```
There are 4 relational operators: `<`, `<=`, `>`, `>=`.

## Query Properties

### Media Types

A media type is a name. Currently, only the `screen` media type is supported. `screen` is also the default media type, so it can be omitted.

### Media Features

#### `width`

Queries the width of the device screen, supporting relational operators. The unit of the value must be `px`, for example, `500px`.

#### `max-width`

Specifies the maximum width of the screen; the unit of the value must be `px`. `(max-width: 500px)` is equivalent to `(width <= 500px)`.

#### `min-width`

Specifies the minimum width of the screen; the unit of the value must be `px`. `(min-width: 500px)` is equivalent to `(width >= 500px)`.

#### `height`

Queries the height of the device screen, supporting relational operators. The unit of the value must be `px`, for example, `500px`.

#### `max-height`

Specifies the maximum height of the screen; the unit of the value must be `px`. `(max-height: 500px)` is equivalent to `(height <= 500px)`.

#### `min-height`

Specifies the minimum height of the screen; the unit of the value must be `px`. `(min-height: 500px)` is equivalent to `(height >= 500px)`.

#### `shape`

Specifies the shape of the screen. Supported values are:
- `rect`: Represents a rectangular screen;
- `circle`: Represents a circular screen;

#### `aspect-ratio`

Queries the aspect ratio of the screen, supporting relational operators. The value can be a number or a fraction, for example, `1.5` and `3/2` both represent an aspect ratio of $3 / 2$.

#### `max-aspect-ratio`

Specifies the maximum screen aspect ratio of the device.

#### `min-aspect-ratio`

Specifies the minimum screen aspect ratio of the device.

#### `orientation`

Specifies the orientation of the screen. Supported values are:
- `portrait`: Represents a portrait device;
- `landscape`: Represents a landscape device.

#### `memory-profile`

The memory-profile property is a reference value used to guide developers in trimming features under different memory budgets. It is set based on parameters such as the device's actual memory capacity and screen resolution. The memory profile helps developers optimize and adjust features based on a set memory budget to ensure that the application runs smoothly even on low-end devices.

The `memory-profile` property supports the following syntax:
``` ebnf
 memory-profile := <number>   (* Memory configuration size, default unit is KiB *)
                 | <number> K (* Memory configuration size, unit is KiB *)
                 | <number> M (* Memory configuration size, unit is MiB, decimals allowed *)
```

Note that `memory-profile` is not the true physical memory capacity of the device. Generally, the values of this property are tiered as follows:
- $2048$ ($2\rm M$): Less than $2\rm MiB$ belongs to low-end devices, where applications should drop fish-eye lists, long lists with a large number of images, etc. Some complex pages may also need to be simplified or removed.
- $4096$ ($4\rm M$): Less than $4\rm MiB$ belongs to mid-to-low-end devices, where a small number of fish-eye lists can be used in the application, but excessively long lists with images are not recommended.
- $8192$ ($8\rm M$): Less than $8\rm MiB$ belongs to mid-to-high-end devices, where basically all features can be used, though performance may still improve with larger capacities.

For example, the following media query statement matches devices with a memory profile between $2{\rm MiB}\sim 4{\rm MiB}$:

``` css
@media (2M < memory-profile <= 4M) {
  /* Specific CSS rule-set */
}
```

If you need to get the device's memory profile in JavaScript, please use the [`memoryProfile`](/api/system-device.md#memoryprofile) property of the `@system.device` module.

============================================================
FILE_PATH: src/transl/EN/framework/render/README.md

# Rendering Mechanism

============================================================
FILE_PATH: src/transl/EN/framework/render/animation.md

# Animation

## Basics

"Animation" creates transition effects for the interface over a period of time by playing a sequence of frames continuously and rapidly. There are two ways to implement animations in Glyphix:
- **Slideshow animation**, which rapidly plays a set of images;
- **Keyframe animation**, where the program automatically calculates the intermediate frames.

### Keyframe Animation

Slideshow animations are implemented using dedicated components, and their principle is similar to videos. This section primarily introduces keyframe animations. The following example demonstrates a keyframe animation:

<div class="animation-example-box">
  <div style="visibility: hidden">Hello World!</div>
  <div class="animation-span">Hello World!</div>
  <div class="keyframes-from">Hello World</div>
  <div class="keyframes-to">Hello World</div>
</div>

To implement this animation, developers need to define the starting frame (red text) and ending frame (green text) of the animation. The program then automatically calculates each frame in between. The start and end frames specified by the developer are called **keyframes**, and keyframe animations also allow defining intermediate keyframes. The frames calculated by the program are called **interpolated frames**. In this example, the initial keyframe is the original text component, while the final keyframe translates the text by $200\rm px$ and scales it by $0.75$. The interpolated frame is the intermediate transformation value calculated based on the animation progress. For example, the interpolated frame at $50\%$ animation progress translates the original text by $100\rm px$ and scales it by $0.875$.

Compared to slideshows, keyframe animations are easier to create and are suitable for interface element transitions (such as button press effects).

Keyframe animations are mainly defined by several elements:
- Keyframes: Manually specified frames, typically used at $0\%$ and $100\%$ progress;
- Duration: The time required for the animation progress to go from $0\%$ to $100\%$;
- Easing function: Defines the progress adjustment curve of the interpolated frames; linear animation effects tend to look poor visually;
- Repeat count, delay, playback direction (forward, reverse, alternate), etc.

### Property Animation

The keyframe animations used in Glyphix are primarily **property animations**. That is, keyframes are defined by the element's properties, and interpolated frames calculate the intermediate property values. For example, as achieved by the [`transition` property modifier](../component/prop-modifier.md#transition-modifier): the animation system automatically handles transition effects for property changes.

Property animations are mainly divided into two categories:
- Component property animations: Add animation transitions to component properties, implemented via the `transition` property modifier;
- CSS animations: Add animations to style properties.

## Easing Functions

Easing functions define the adjustment curve of the animation progress, avoiding monotonous linear interpolation effects. Readers can experience the effects of easing functions at https://cubic-bezier.com/.

In the [`transition` property modifier](../component/prop-modifier.md#transition-modifier) and CSS [`animation` property](../generic/styles.md#animation), the easing function is a string, the contents of which are shown in the table below.

|              Value              | Description                                                                                                                                              |
| :-----------------------------: | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
|             `ease`              | Default value. The animation starts slowly, then accelerates, and slows down before ending.                                                              |
|            `ease-in`            | The animation starts slowly.                                                                                                                           |
|           `ease-out`            | The animation ends slowly.                                                                                                                               |
|          `ease-in-out`          | The animation starts and ends slowly.                                                                                                                  |
|            `linear`             | The animation has the same speed from start to finish.                                                                                                   |
|            `spring`             | Simulates a spring rebound animation effect, equivalent to `spring(1,1,1)`.                                                                             |
| `cubic-bezier(x1, y1, x2, y2)`  | Defines the easing function using a [cubic Bézier curve](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function#cubic_b%C3%A9zier_easing_function). |
| `spring(spring, damping, mass)` | Simulates a spring rebound animation effect, allowing you to specify elasticity, damping, and mass parameters (documentation needed).                   |

For most animations, the `ease` easing function yields good results, while complex requirements can use the `cubic-bezier()` function. The `spring()` function is suitable for scenarios requiring physical rebound effects, such as rotating pointers.

## Examples

### Button Animation

As shown below, the default button effect has no press animation:

<Glyphix id="render-animation-button1" width="200" height="80">

``` html
<div>
  <button>Button</button>
</div>
```

``` css
button {
  display: block;
  background-color: #8af;
  padding: 8px 16px;
  border-radius: 50%;
  margin: 16px;
}

button:active {
  transform: scale(1.1, 1.1);
}
```
</Glyphix>

You can use the CSS [`animation`](../generic/styles.md#animation) property to add interactive animations to this button:

<Glyphix id="render-animation-button2" width="200" height="80">

``` html
<div>
  <button>Button</button>
</div>
```

``` css
/* Define active pseudo-class keyframes. If from / 0% keyframe is omitted,
   the animation will start playing from the component's current state */
@keyframes button-active {
  to {
    transform: scale(1.1, 1.1);
  }
}

/* Define non-pseudo-class keyframes. If from / 0% keyframe is omitted,
   the animation will start playing from the component's current state */
@keyframes button-normal {
  to {
    transform: scale(1, 1);
  }
}

button {
  display: block;
  background-color: #8af;
  padding: 8px 16px;
  border-radius: 50%;
  margin: 16px;
  /* Animate the button to scale to 100% in the non-pseudo-class style */
  animation: 0.2s ease button-normal;
}

button:active {
  /* Animate the button to scale to 120% in the active pseudo-class style */
  animation: 0.2s ease button-active;
}
```
</Glyphix>

Currently, the CSS `transition` property is not supported, so animations must be defined separately in the button's non-pseudo-class style and `active` pseudo-class style.


### `spring` Animation Effect

The `spring` easing function provides an interpolation effect similar to spring-damped vibration, which can be used for moving pointers. The following example demonstrates two ways to implement pointer animations: the left side uses uniform pointer rotation, while the right side uses the `spring` easing function.

<Glyphix id="render-animation-spring" width="400" height="200">

``` html
<div class="window">
  <div class="clock">
    <div class="pointer"
      transform="translate(0, -40%) rotate({{angle}}deg) translate(0, 50%)"
      transform.transition="{curve: 'linear', duration: 1}" />
    <div class="pointer invisible"></div>
  </div>
  <div class="clock">
    <div class="pointer"
      transform="translate(0, -40%) rotate({{angle}}deg) translate(0, 50%)"
      transform.transition="{curve: 'spring(1.2,1,1.2)', duration: 1}" />
    <div class="pointer invisible"></div>
  </div>
</div>
```

``` css
.window {
  display: flex;
}

.clock {
  background-color: gray;
  border-radius: 50%;
  flex: 1;
  margin: 4px;
}


.pointer {
  background-color: #0f0;
  width: 12px;
  height: 50%;
  margin: 4px auto;
  border-radius: 50%;
}

.invisible {
  visibility: hidden;
}
```

``` js
export default {
  data: {
    angle: 0
  },
  onInit() {
    setInterval(() => this.angle += 5, 1000)
  }
}
```

</Glyphix>

Both animations update the pointer angle at $1$-second intervals, but the component property's `transition` modifier automatically adds the rotation animation.

<style scoped>
@keyframes animation-example {
  to {
    transform: translate(200px, 0) scale(0.75);
  }
}

.animation-example-box {
  position: relative;
  width: 320px;
  margin: 0 auto;
  font-family: sans-serif;
  font-size: 24px;
  user-select: none;
}

.animation-span {
  position: absolute;
  left: 0;
  top: 0;
  animation: 5s ease infinite animation-example;
}

.keyframes-from, .keyframes-to {
  color: red;
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0.5;
}

.keyframes-to {
  color: green;
  transform: translate(200px, 0) scale(0.75);
}
</style>


============================================================
FILE_PATH: src/transl/EN/framework/render/rich-text.md

# Rich Text

When using a flow layout, inline elements such as [`a`](/components/a.md), [`span`](/components/span.md), and [`checkbox`](/components/checkbox.md) can be laid out along lines and can wrap. The text of components like `span` can even span multiple lines, which can be utilized to achieve rich text display.

## Plain Text Display

Let's first look at how Glyphix displays plain text. The [`p`](/components/a.md) and [`text`](/components/text.md) components can be used for plain text display. You simply need to specify the text string as the `text` attribute of these components:
``` html
<p text="plain text string." />
<text text="plain text string." />
```
Web-style text nodes (i.e., where text is a child node of the element) are also supported:
``` html
<p>plain text string."</p>
<text>plain text string."</text>
```
Glyphix converts the only text child node of a component into the `text` attribute, so these two syntaxes are essentially identical. In other words, as long as a custom component supports the `text` attribute, it can use text child nodes just like the `p` component.

## Rich Text Display

The `p` and `text` components cannot be used for rich text because they always form a complete box and cannot layout across multiple lines. To achieve rich text, you first need a container with a flow layout, and then use components like `span` to display the text. For example:
``` html
<div>
  <span>rich&nbsp;</span>
  <span style="color: red">text&nbsp;</span>
  <span>string.</span>
</div>
```
Many components use flow layout by default, such as `div`, `p`, etc. For simplicity, the `<span>` tags can also be omitted:
``` html
<div>
  rich <span style="color: red">text</span> string.
</div>
```
When a component has multiple child elements, the text child elements among them will be automatically converted into `span` components.

============================================================
FILE_PATH: src/transl/EN/framework/commands/if.md

---
icon: file-tree
---
# if / elif / else Directives

The `if` / `elif` / `else` directives are used for conditional rendering. These directives control whether a component is rendered. For example, the `if` directive renders the component only when the condition is true, otherwise it deletes the component. This is different from the component's `show` attribute, which controls whether the component is displayed but does not delete it.

## Syntax

### if Directive

``` html
<p if="cond">if: true</p>
```
If the `cond` expression is true, the component is rendered; otherwise, it is not rendered.

## elif and else Directives

Components with `elif` and `else` directives must follow a component with an `if` or `elif` directive, and use the negation of the previous condition to control whether the component is rendered:
``` html
<p if="cond1">if cond1: true</p> 
<p elif="cond2">elif cond2: true</p>
<p elif="cond3">elif cond3: true</p>
<p else>else</p> <!-- The else directive does not support attribute values -->
```
The behavior of this code is as follows:
- If the `cond1` condition is true, only the `if cond1: true` text is rendered;
- Otherwise, if `cond2` is true, only `elif cond2: true` is rendered;
- Otherwise, if `cond3` is true, only `elif cond3: true` is rendered;
- If all conditions are false, the `else` text is rendered.

The attribute values of the `if` / `elif` / `else` directives support the [Directive Attribute Values](/framework/component/template.md#指令属性值) syntax.

============================================================
FILE_PATH: src/transl/EN/framework/commands/model.md

---
icon: swap-horizontal
---
# model Directive

The `model` directive is used to implement two-way binding for component properties.

## Syntax

``` html
<com model:prop="value"></com>
<com ::prop="value"></com>
```
You can use the `model:` prefix or the shorthand `::` to decorate a property, enabling two-way binding with the `model` directive. Here, `prop` is the name of the target component's property, and `value` is the name of the view-model property in the current component to be bound.

## Two-Way Binding

Using the [`on` directive](on.md) and [property binding expressions](/framework/component/template.md#属性绑定表达式), you can achieve two-way binding between component properties and view-model properties:
``` html
<div>
  <switch :value="state" on:value="state = $event"/> value: {{state}}
</div>
```

``` js
export default {
  data: {
    state: false
  },
  onReady() {
    setInterval(() => this.state = !this.state, 2000)
  }
}
```

<Glyphix id="commands-model-1" height="32" inline>

``` html
<div>
  <switch :value="state" on:value="state = $event"/> value: {{state}}
</div>
```

``` js
export default {
  data: {
    state: false
  },
  onReady() {
    setInterval(() => this.state = !this.state, 2000)
  }
}
```

</Glyphix>

When the value of `this.state` is modified in the JavaScript code, the `:value="state"` expression inside the `switch` tag updates the display state of the `switch` element, while the `on` directive expression updates the value of `state` after the user clicks the `switch` element.

Throughout this process, the UI display state (the `switch` component and the text `value: {{state}}`) remains consistent with the `state` property in the view-model. We call this mechanism **two-way binding**.

Essentially, the `model` directive is syntactic sugar for the syntax shown above, simplifying two-way binding:
``` html
<div>
  <switch ::value="state"/> value: {{state}}
</div>
```

<Glyphix id="commands-model-2" height="32" inline>

``` html
<div>
  <switch ::value="state"/> value: {{state}}
</div>
```

``` js
export default {
  data: {
    state: false
  },
  onReady() {
    setInterval(() => this.state = !this.state, 2000)
  }
}
```

</Glyphix>

## Two-Way Binding for Custom Components

Two-way binding is commonly used for form components, but the `model` directive also supports custom components. To use it, simply provide an event with the same name as the custom component's property and trigger it when the property changes. For example:

``` js
// file: com.ux
export default {
  data: {
    prop: 0 // Assuming we want two-way binding for the prop property
  },
  watch: {
    prop(x) { // Trigger an event with the same name when the prop property value changes
      this.$emit('prop', x)
    }
  }
}
```
Assume this is part of the component object for a custom component, where the `prop` property is used for two-way binding. In this example, the `watch` object is used to monitor changes to the `prop` property and trigger an event named `'prop'` when it changes. In the parent component, you can simply perform two-way binding like this:
``` html
<com ::prop="valueName"></com>
```

============================================================
FILE_PATH: src/transl/EN/framework/commands/for.md

---
icon: format-list-bulleted
---
# for Directive

The `for` directive is used for list rendering.

## Syntax

``` html
<div for="expr"></div> <!-- Without defining index and iteration variables -->
<div for="value in expr"></div> <!-- Without defining index variable -->
<div for="index, value in expr"></div>
<div for="(index, value) in expr"></div>
```
The value expressed by `expr` is an [`Array` object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array) or a number. The `for` directive will iterate through the entire list and pass the index and the value of the iteration item during the iteration process. If you do not define an index variable or iteration variable, the default name for the index variable is `$idx`, and the default name for the iteration variable is `$item`.

When both the `for` directive and the `if` directive are present on the same element, the `if` directive has a higher priority. This means that if the `if` directive evaluates to false, the entire list will not be rendered at all.

The attribute value of the `for` directive supports the [directive attribute value](/framework/component/template.md#directive-attribute-value) syntax, so expressions enclosed in double curly braces can also be used.

::: warning
It is not recommended to use the `if` and `for` directives simultaneously in order to improve code readability.
:::

## List Rendering

Render a [JavaScript array](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/First_steps/Arrays) into a list using the `for` directive. It is typically used on child components of [`scroll`](/components/scroll.md), for example:
``` html
<scroll :damping="damping">
  <p for="item in items" class="item">
    {{ item.message }}
  </p>
</scroll>
```
The `for` directive on the `p` component iterates over the `items` array and generates a `p` component node for each iteration item. `item` is the variable name for the iteration item, and its `message` property is accessed within the `{{ item.message }}` [interpolation expression](/framework/component/template.md#interpolation-expression).

`items` is a [component object property](/framework/component/component-object.md) of type array, for example:
``` js
export default {
  data: {
    items: [
      { message: 'Foo' },
      { message: 'Bar' },
      { message: 'Baz' },
    ]
  }
}
```

This code will render the following interface:

<glyphix id="commands-for-1" height="200" width="360" inline>

``` html
<scroll :damping="damping">
  <p for="item in items" class="item">
    {{ item.message }}
  </p>
</scroll>
```

``` js
export default {
  data: {
    items: [
      { message: 'Foo' },
      { message: 'Bar' },
      { message: 'Baz' },
    ]
  }
}
```

``` css
scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
}

.item {
  color: #fafafa;
  background-color: #bdbdbd;
  text-align: center;
  padding: 40px 10px;
  margin: 10px;
  border-radius: 16px;
}
```

</glyphix>

The rendering result is a scrollable list containing three items with the contents "Foo", "Bar", and "Baz". You can use the `for` directive on native [components](/framework/component/README.md) or custom components to achieve list rendering.

You can also use the default `$item` iteration variable name:
``` html
<scroll :damping="damping">
  <p for="items" class="item">
    {{ $item.message }}
  </p>
</scroll>
```
The rendering result of this is the same as above.

## Nesting and Scope

In the same tag, the index and iteration variables can only be accessed after the `for` directive, so you need to pay attention to the order of related attributes:
``` html
<panel for="value in expr" title="value.title"></panel> <!-- Correct -->
<panel title="value.title" for="value in expr"></panel> <!-- Incorrect -->
```
The incorrect order will not cause a compilation error, but will instead try to look up the `value` property in the `this` scope. In other words, variables defined in the `for` directive will shadow names in the outer scope, which include:
- The component's view-model (i.e., accessed via properties of `this`)
- Global objects

Considering variable scope and directive priority issues, the `if` directive should be placed before the `for` directive, otherwise it may cause confusing behavior.

For the current component node, variables defined in the `for` directive are only visible in attributes that come after it. They are also visible in static child components, for example:
``` html
<panel for="value in expr" title="value.title">
  <p>message: {{value.message}}</p>
</panel>
<p>{{value.message}}</p> <!-- Accessing this.value.message here -->
```
Except for the last `{{value.message}}` expression, `value` in all other places is within the scope of the `for` directive.

The `for` directive can be used nested, and the scoping rules in this case are the same as above. Note that the scope of index and iteration variables with the same name will be shadowed by the inner `for` directive, so these variables need to be explicitly defined.

## Array Change Detection

The `for` directive can detect changes to [reactive](/framework/component/component-object.md#reactive-programming) arrays and update the UI. The following operations will trigger `for` rendering updates:
- Replacing with a new array;
- Calling array mutation methods, such as [`push()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/push), [`pop()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/pop), [`shift()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/shift), [`unshift()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/unshift), [`splice()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/splice), [`sort()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/sort), and [`reverse()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/reverse).

### Replacing an Array

You can replace the reactive property used for list rendering with a new array to trigger a UI update. For example:
``` js
this.items = this.items.filter((item) => item.message.match(/Foo/))
```
In this way, `this.items` is assigned a new array, and the `for` directive will re-render the new list after this operation.

::: tip
Arrays have some immutable methods, such as `filter()`, `concat()`, and `slice()`, which do not mutate the original array but always **return a new array**. When encountering immutable methods, you need to use the method above to replace the old array with the new one.
:::

### Array Mutation Methods

Using array mutation methods can also trigger view updates, for example:
``` js
// Insert a new element with the content "Grault" at the bottom of the original list
this.items.push({ message: 'Grault' })
```

You can also truncate the array by directly modifying its length, such as:
``` js
// Delete elements after the third item in the list
this.items.length = 2
```

You can also modify elements of the list:
``` js
// Change the content of the second element to "Grault"
this.items[1] = { message: 'Grault' }
```

::: warning
The `for` directive currently cannot track property changes of list elements. See [List Element Updates](#list-element-updates) for details.
:::

## Caveats and Limitations

### List Element Updates

The `for` directive cannot listen to deep property updates of array items, which means
``` js
this.items[1].message = 'Grault'
```
will not correctly trigger a UI update. To solve this problem, you must replace the array item with a new object:
``` js
this.items[1] = { message: 'Grault' }
```

When an item object has many properties, but you only want to update a few of them, it is recommended to first use the [spread syntax (`...`)](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to copy the object, and then update the properties:
``` js
this.items[1] = {
  ...this.items[1], // Copy all properties of the second element
  message: 'Grault' // Update the message property
}
```

::: warning
The number of properties in array item objects will affect performance. When you notice stuttering in list updates, please refer to [Unnecessary Updates](#unnecessary-updates).

Due to reasons such as other elements in the interface updating simultaneously, the UI might update after directly modifying deep properties of an item, but this behavior is unstable. Please avoid doing this.
:::

### List Index Issues

Although the `for` directive supports getting the item index during rendering, such as:
``` html
<p for="index, value in items">
  {{ index }} - {{ value }}
</p>
```
It currently does not support reactively updating the index. Modifications to the `items` array may cause display disorder. Updating the entire array can avoid this problem.

However, due to certain optimization mechanisms, it is difficult for developers to guarantee that the `items` array is **truly** updated entirely, which can lead to strange unexpected index disorder issues.

### Unnecessary Updates

List rendering can be a bottleneck for smoothness and performance, especially the rendering speed of long lists which can be slow. Reducing unnecessary list updates can be an effective optimization technique.

#### Directly Updating the List

Consider a list like this:
``` html
<div for="(idx, task) in tasks" on:click="process(idx)">
  <p>{{ task.name }}</p>
  <p>{{ task.progress }}%</p>
</div>
```
This is a task processing interface that displays a list of tasks and processes a specific task when the user clicks it. For simplicity, we initialize this task list as follows:
``` js
this.tasks = Array.from({ length: 10 },
  (_, i) => ({ name: `Task #${i + 1}`, progress: 0 }))
```
At this point, you will see a task list containing 10 items. The following `process()` method simply implements the update of task progress:
``` js
process(idx) { // idx is the index of the clicked task item
  this.tasks[idx].progress = 0
  // Create a timer to simulate processing progress
  let timer = setInterval(() => {
    // Since the for directive does not support deep property updates, copy an object first
    let task = {...this.tasks[idx]}
    task.progress += 10
    this.tasks[idx] = task
    if (task.progress >= 100)
      clearInterval(timer) // Delete the timer when processing is complete
  }, 100)
}
```
As shown below, this implementation can be interacted with normally.

<glyphix id="commands-for-tasklist-1" height="360" width="360" title="Task List">

``` html
<scroll>
  <div for="(idx, task) in tasks" on:click="process(idx)">
    <p>{{ task.name }}</p>
    <p>{{ task.progress }}%</p>
  </div>
</scroll>
```

``` js
export default {
  data: {
    tasks: []
  },
  onInit() {
    this.tasks = Array.from({ length: 10 },
      (_, i) => ({ name: `Task #${i + 1}`, progress: 0 }))
  },
  process(idx) {
    this.tasks[idx].progress = 0
    let timer = setInterval(() => {
      let task = {...this.tasks[idx]}
      task.progress += 10
      this.tasks[idx] = task
      if (task.progress >= 100)
        clearInterval(timer)
    }, 100)
  }
}
```

``` css
scroll {
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
}

div {
  color: #fafafa;
  background-color: #bdbdbd;
  display: flex;
  justify-content: space-between;
  padding: 40px 10px;
  margin: 10px;
  border-radius: 16px;
}
```

</glyphix>

This simple approach may become very laggy in complex and long list interfaces, at which point you might observe:
- Frame drops in animations such as progress bars in the interface;
- Scrolling up and down in the list becomes noticeably laggy.

#### Optimization via Child Components

An optimization approach is to split items into independent components. In this example, a `Task` component can be added:
``` html
<div on:click="process">
  <p>{{ name }}</p>
  <p>{{ progress }}%</p>
</div>
```
The JavaScript script of the `Task` component can handle its own `process()` operation:
``` js
export default {
  data: {
    name: null, // Task name needs to be passed from the outside
    progress: 0
  },
  // Each Task component instance handles its own process operation
  // and accesses its own reactive properties via this.
  process() {
    this.progress = 0
    let timer = setInterval(() => {
      this.progress += 10
      if (this.progress >= 100)
        clearInterval(timer)
    }, 100)
  }
}
```

Compared to the previous method, the new solution can be used directly after [importing the `Task` component](/framework/component/README.md#importing-components):
``` html
<task for="task in tasks" :name="task.name" />
```
And the parent component's JavaScript code can be simpler:
``` js
export default {
  data: {
    tasks: []
  },
  onInit() {
    for (let i = 0; i < 10; ++i)
      this.tasks.push({ name: `Task #${i + 1}` })
  }
}
```
Compared to directly updating the list, this introduces the following changes:
- The inserted array items do not have a `progress` property, because it only needs to be handled within the `Task` child component;
- The `process()` method is removed and moved inside the `Task` component;
- There is no need to use the `idx` index variable to distinguish different items.

This approach can achieve the same task list interface, except that the handling of `progress` is moved into the `Task` child component, thereby avoiding updating the task array when modifying the progress. Using this method can optimize the internal UI update problem of list elements while reducing code complexity.

============================================================
FILE_PATH: src/transl/EN/framework/commands/on.md

---
icon: alternate-email
---
# on Directive

The `on` directive is used to listen for changes in property values that support listening.

## Syntax

``` html
<div on:attribute="expr"></div>
<div onattribute="expr"></div> <!-- Syntax compatible with Quick App -->
<div @attribute="expr"></div>  <!-- Vue-style syntax -->
```

`attribute` is the name of the property whose changes need to be listened to, and `expr` is the expression to be executed when the property changes. The standard `on` directive uses the `on:` prefix, while the `on` and `@` character prefixes are also supported.

The property value of the `on` directive supports the [Directive Property Value](/framework/component/template.md#指令属性值) syntax.

::: tip
It is recommended to use the `on:attribute` format. `onattribute` can easily lead developers to unconsciously confuse the `on` directive with ordinary properties. In addition, property names like `oneself` will be parsed as the `on:eself` directive, which requires special attention.
:::

## Listening Expressions

### Basic Usage

The following code listens to a touch event on a `div` component:
``` html
<div on:touchmove="console.log($event)"></div>
```
In this example, the [`touchmove`](../generic/properties.md#touchmove) event is listened to, and the [touch event object](../generic/properties.md#touchevent) is printed directly here. The `$event` variable is used to get the event value, which is a variable defined by the `on` directive (its scope is limited to the `on` directive expression).

You can also call methods defined in the component object:
``` html
<div on:touchmove="onTouch('move', $event)"></div>
```

``` js
export default {
  onTouch(type, event) {
    console(`touch ${type}:`, event)
  }
}
```

For methods on custom events, please refer to [Inter-component Communication](../component/communicate.md).

### Function Expressions

If the value of the listening expression is a function, that function will be called automatically:
``` html
<div on:click="onClick" />
```

``` js
export default {
  onClick(event) {
    console.log(event)
  }
}
```
As shown in the example, the event value will be passed as the sole argument to the function.

::: tip
The listening expression does not have to be a function variable; it can also be a complex expression (such as an expression containing a function call). As long as the value of the expression is a function, it will be invoked by the `on` directive.
:::

## Listening for Component Property Value Changes

The property values of some components generate events when they change, which can be listened to via the `on` directive:

``` html
<list on:index="indexChanged($event)">
  <content/>
</list>
```

As described in the [Property Documentation Specification](../component/README.md#属性文档规范), properties that support **listening** can have their value changes listened to using the `on` directive.

============================================================
FILE_PATH: src/transl/EN/framework/component/life-cycle.md

# Lifecycle

Components, pages, and applications all have lifecycles. You can invoke specific features during particular lifecycle stages using **lifecycle functions**.

## Component and Page Lifecycles

Lifecycle functions can be triggered by defining them within component and page objects. For example:
``` html
<script>
export default {
  onInit() {
    console.log("onInit() called!")
  }
}
</script>
```
The `onInit()` lifecycle function is called after the component is instantiated. Lifecycle functions do not take any parameters and do not use return values.

### Component Lifecycle Functions

These lifecycle functions are shared between components and pages.

#### `onInit` <decl type="(): Promise<any> | void" method />

At this point, the component has been instantiated, and the data in the view-model is ready. You can access this data using the `this` keyword. Developer-defined initialization logic is typically executed within this lifecycle function.

#### `onReady` <decl type="(): Promise<any> | void" method />

At this point, the component has been rendered. The component tree now has a corresponding control tree (similar to a DOM tree).

#### `onDestroy` <decl type="(): Promise<any> | void" method />

The component is about to be destroyed. Data in the view-model can still be accessed at this point. Custom resource release operations are typically executed in `onDestroy()`.

### Page Lifecycle Functions

These lifecycle functions only exist in pages.

#### `onShow` <decl type="(): Promise<any> | void" method />

Called when the page is about to be displayed. When returning using `router.back()`, `onShow()` is called when the underlying page is about to be displayed; it is also called before a newly created page is displayed for the first time.

#### `onHide` <decl type="(): Promise<any> | void" method />

Called when the page is about to be hidden. `onHide()` is called when the underlying page is hidden due to a call to `router.push()`. However, the page is not hidden before it is destroyed, so `onHide()` will not be called in that case.

When the device screen is turned off, `onHide()` of the foreground page is also called. For details, see [Screen State Changes](#screen-state-changes).

#### `onBackPress` <decl type="(): boolean" method />

Called when the user swipes back from the edge. Developers can handle the return logic in this function. Returning `true` indicates that the developer has handled the back operation, and the system will not execute the default back behavior; returning `false` indicates that the developer has not handled the back operation, and the system will execute the default back behavior (i.e., close the current page and return to the previous page).

::: warning
This lifecycle function disables interactive edge-swipe navigation (i.e., following the gesture). It is generally **not recommended** to use this lifecycle function, nor should you define a regular method named `onBackPress`. If you want to prevent the default back interaction, please refer to [Default Event Handling for Pages](/framework/generic/properties.md#default-event-handling-for-pages), which preserves interaction animations.
:::

#### `onRefresh` <decl type="(): Promise<any> | void" version="0.8" method />

Called when a page is opened in `singleTask` mode and returns to an existing page. For details, see [`launchMode`](../application/manifest.md#launchmode). Page data can be refreshed in this function.

## Application Lifecycle

### Application Lifecycle Functions

#### `onCreate` <decl type="(): Promise<any> | void" method />

Called when the application is loaded.

#### `onDestroy` <decl type="(): Promise<any> | void" method />

Called when the application is about to be destroyed.

#### `onShow` <decl type="(): Promise<any> | void" method />

Called when the application switches from the background to the foreground. The application's `onShow()` lifecycle function is always called after the page's `onShow()`. When the device screen is turned back on, the foreground application's `onShow()` is also called. For details, see [Screen State Changes](#screen-state-changes).

#### `onHide` <decl type="(): Promise<any> | void" method />

Called before the application is hidden from the foreground to the background.

If you do not want the application to remain active in the background, you can call [`launch.exit()`](/api/system-launch.md#exit) in `onHide()` to exit the application itself. For example:
```js
// in src/app.js
import launch from '@system.launch'

export default {
  onHide() {
    launch.exit()
  },
}
```

The application's `onHide()` lifecycle function is always called after the page's `onHide()`. When the device screen is turned off, the foreground application's `onHide()` is also called. For details, see [Screen State Changes](#screen-state-changes).

#### `onRoute` <decl type="(page: string, query: {[key: string]: string}): Promise<any> | void" method />

Called when the application is launched via a deeplink URI. The parameters `page` and `query` are the decoded URI fields. For example:
``` js
// file: app.ux
export default {
  // Assuming launched via app://example.app/page/to/deeplink?key=value&query=result
  onRoute(page, query) {
    console.log(page)  // Prints string '/page/to/deeplink'
    console.log(query) // Prints object {deeplink: 'key', query: 'result'}
  }
}
```

`onRoute()` is called after `onCreate()` and before `onShow()`. Developers can perform initialization in `onRoute()` based on the parameters specified by the deeplink (such as navigating to a specific page).

#### `onLocaleChanged` <decl type="(locale: {language: string}): void" method />

Called when the application's locale changes. The `locale` parameter is an object containing a `language` field representing the current locale (Language Tag), such as `'en-US'`, `zh-CN`, etc.

## Asynchronous Lifecycle Functions <experimental/>

Lifecycle functions for components, pages, or applications can be asynchronous (i.e., `async` functions or returning a `Promise` object). For example:
``` js
import fs from "@system.file"

export default {
  async onInit() {
    // Wait for asynchronous file reading to complete before proceeding.
    let text = await fs.readText({ uri: "internal://files/test.txt" })
    console.log(text)
  }
}
```
Assuming this is the `onInit()` lifecycle function of a component, component rendering will only proceed after the asynchronous file reading is complete. The following restrictions apply during the execution of asynchronous lifecycle functions:
- Component rendering will not be executed repeatedly, and any operations on reactive properties during this period will not cause UI updates;
- User input is temporarily blocked, and touches and key presses will not be responded to (otherwise, repeated user taps would lead to repeated responses).

The main purpose of asynchronous lifecycle functions is to wait for asynchronous I/O and resource operations, avoiding the premature display of unloads interfaces. In particular, when opening a new page, the system will wait for all of the page's `onInit()`, `onReady()`, and `onShow()` lifecycle functions to complete before displaying the page or playing transition animations.

::: warning
Asynchronous lifecycle functions are currently experimental and may cause various issues, including crashes. Closing a page while it is rendering during the execution of an asynchronous lifecycle function will cause a crash.

Firmware on most devices does not enable support for asynchronous lifecycle functions, and their behavior may not meet expectations. Please use asynchronous lifecycle functions with caution.
:::

## Screen State Changes

Changes in the device's screen state affect the lifecycle function calls of applications and pages. When the device screen is turned off, the `onHide()` lifecycle functions of the foreground application and page are called; when the screen is turned back on, the `onShow()` lifecycle functions of the foreground application and page are called. Developers can use these lifecycle functions to pause or resume network requests to reduce power consumption.

::: tip
Some devices switch applications to the background after the screen is turned off and kill them after a period of time. For applications that need to run continuously in the background, please pay attention to the [Background Management](../application/README.md#background-management) methods for keeping them alive.
:::

============================================================
FILE_PATH: src/transl/EN/framework/component/template.md

# Template Syntax

Templates are the contents inside the `<template>` tag of a UX file. Overall, templates use standard HTML syntax; however, the template syntax also introduces syntax limitations and new syntax that differ from HTML, which will be introduced in this document.

## Tags

Tag nesting is supported in templates, but all tags must be closed. Therefore, the following writing is valid:
``` html
<div> <p>message</p> </div>
```
However, the following is invalid:
``` html
<div> <p>message</p> <!-- <div> tag is not closed -->
```

## Text Values

Text elements and attribute values in templates are text values. For example, in:
``` html
<com name="value">A message</com>
```
both `A message` and `value` are text. The `A message` text value will be passed to the `text` attribute of the `com` component, so the text node (the `A message` part) is actually syntactic sugar for the `text` attribute:
``` html
<p>text</p>
```
is equivalent to
``` html
<p text="text"></p>
```
Text values are represented internally as JavaScript strings.

### Text Child Nodes

Text child nodes can be used not only for native components, but also for custom components with a `text` attribute, such as:
```html
<p>The text element of P.</p>
<MyCom>The text element of MyCom.</MyCom>
```
You only need to provide a `text` [reactive property](component-object.md#reactive-properties) for the `MyCom` component to receive the content of the text node, without going through `<slot>` slots or other mechanisms.

::: warning
Some components do not have a `text` attribute (such as `div`), and placing text nodes as their children will not display anything! Make sure to place text nodes as children of native components such as `p`, `text`, or `span`.
:::

You can also use multiple text child nodes in a component, such as:
```html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```
which will mixed-display text and the [`switch`](/components/switch.md) component inside the `div`:

<glyphix id="component-template-text-1" height="32" inline>

``` html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```

</glyphix>

When a text node is mixed with other nodes, the text node will be translated into a [`span`](/components/span.md) node rather than being passed to a component's `text` attribute. Therefore, the above example is equivalent to this code:
```html
<div>
  <span>The switch&nbsp;</span>
  <switch />
  <span>&nbsp;and&nbsp;</span>
  <checkbox />
  <span>&nbsp;checkbox.</span>
</div>
```
Such implicit `span` elements can also have CSS styles assigned, but class selectors cannot be used (because there is no `class` attribute).

### Whitespace

All whitespace characters, such as line breaks and tabs, in the source code of text child nodes are treated as spaces. The rules for processing spaces are as follows:
- Leading spaces at the beginning of the first text child node are removed.
- Trailing spaces at the end of the last text child node are removed.
- Multiple consecutive spaces at other positions are treated as a single space.

::: tip
When there is only a single text node, it is both the first and the last text child node, so spaces before and after it are removed. If a text node has no content (including when there is no content left after removing spaces), it will be deleted.
:::

Therefore, writing like `<p>  spances </p>` will not display any spaces, while
```html
<div>
  The switch <switch /> and <checkbox /> checkbox.
</div>
```
will remove the spaces (and line breaks) between `<div>` and `The switch`, as well as between `checkbox.` and `</div>`. However, a single space between `The switch` and `<switch />`, etc., will be preserved.

When you find that you cannot control whitespace using the above rules, you should consider using [HTML character references](https://developer.mozilla.org/en-US/docs/Glossary/Character_reference) to represent them.

::: tip
When mixing [interpolation expressions](#interpolation-expressions) within text nodes, keep in mind that the latter are JavaScript expressions, and strings within them must follow JavaScript [escape character](https://developer.mozilla.org/en-US/docs/Glossary/Escape_character) rules.
:::

## Attributes and Interpolation

### Interpolation Expressions

You can enclose an expression in double braces within text, which is an **interpolation** expression:
``` html
<p>Message: {{ msg }}!</p>
```
During rendering, the expression inside the double braces is evaluated and concatenated with the text before and after it. If there is no text before and after the expression, it forms an **unconcatenated** interpolation expression; in this case, the value of the expression is used directly without being converted to text.

Interpolation expressions can also be used in attribute values, for example:
``` html
<div visible="{{true}}"></div>
```
Here, `{{true}}` evaluates directly to the boolean value `true`, rather than a string.

::: tip
Attributes like `visible` require a boolean value type, so you need to use unconcatenated syntax like `visible="{{ expr }}"` to prevent text around the curly braces from causing the interpolation expression to turn into text. Due to JavaScript's value conversion rules, `visible="false"` would cause the attribute to evaluate to `true` (non-empty strings convert to boolean `true`). Of course, [implicit attribute values](#implicit-attribute-values) can also be used for this scenario.
:::

If you need to pass a numeric constant, either of the following two writings will work:
``` html
<scroll damping="{{1.5}}"></scroll>
<scroll damping="1.5"></scroll>
```
Because the string `"1.5"` can be automatically converted to the number `1.5`. We recommend the first approach because it requires no extra type conversion and is more semantically explicit.

The type of an unconcatenated interpolation expression attribute value is the type of the interpolation expression itself, such as the type of `{{1 + 2}}`, which is a number. Other interpolation expressions are text values.

### Attribute Binding Expressions

If a component's attribute is not of a text type, you can use an unconcatenated interpolation expression:
``` html
<com items="{{ [1, 2, 3] }}" />
```
You can also use the attribute binding expression syntax:
``` html
<com :items="[1, 2, 3]" />
```
Compared to regular attributes, attribute binding expressions require adding a `:` character before the attribute name. In this case, the attribute value is compiled as an expression rather than a string. This method avoids writing `{{ }}` and offers better readability.

### Implicit Attribute Values

If an element's attribute is specified with only its name and no value, it is equivalent to the boolean `true`:
``` html
<com focus></com>
```
is equivalent to
``` html
<com :focus="true"></com>
```
Implicit attribute values are suitable for various option attributes: specifying the attribute name means enabling the option, while omitting it means disabling the option. If you need to pass an empty string via an attribute, you should explicitly write an empty attribute value:
``` html
<com empty-property=""></com>
```
The rule for implicit attribute values applies to ordinary attributes and does not apply to [directive attributes](#directive-attribute-values), which should always have their attribute values written out.

### Directive Attribute Values

For [directives](/framework/commands/README.md) such as `if`, `for`, and `on`, the attribute value is not a text string, so interpolation expressions concatenated with text cannot be used. For example,
``` html
<div on:click="console.dir({{$event}})"></div>
```
is invalid. Instead, you can use an unconcatenated interpolation expression:
``` html
<div on:click="{{console.dir($event)}}"></div>
```
All directive attributes support omitting the double curly braces, so the code above can be shortened to:
``` html
<div on:click="console.dir($event)"></div>
```
Note, however, that regular attributes must pass non-text type values via unconcatenated interpolation expressions or attribute binding expressions.

### `this` Binding

In interpolation expressions (including attribute binding expressions), identifiers generally automatically bind to the properties of the component object. That is, the expression `callback` in
``` html
<div on:visible="callback"></div>
```
is equivalent to the JavaScript code `this.callback`.

Identifiers appearing within the template syntax scope will not bind `this`, which is primarily reflected in the `for` directive. For example,
``` html
<p for="v in ['one', 'two']">{{ v }}</p>
```
The identifier `v` in the interpolation expression `{{ v }}` binds to the iteration variable `v` defined in the `for` directive, rather than binding to the `this` property of the component object.

Identifiers used by certain global objects and reserved names will also not bind to the `this` property of the component object. These names include:

- `this`, `true`, `false`, `undefined`, `null`
- `console`
- `Math`, `Date`, `Number`, `Array`, `Object`, `Boolean`, `String`, `RegExp`, `JSON`
- `NaN`, `Infinity`
- `isNaN`, `isFinite`
- `parseFloat`, `parseInt`

## Interpolation Expression Syntax

Interpolation expressions support most JavaScript expression syntax, but do not support statements or other syntaxes. This section lists all supported expressions.

`}}` cannot appear inside interpolation expressions, so writings like `{key: {a: 1.0}}` cannot be compiled. This can be resolved by adding spaces: `{ key: { a: 1.0 } }`.

### Basic Expressions

- Numbers: Numeric literals such as `1`, `1.0`, `1e10`, etc.
- Identifiers: Variable names, as well as primitive enum values like `true`, `null`, etc.
- Strings: String literals enclosed in single or double quotes (double quotes are not very convenient in XML/HTML environments)
- Parentheses: `( expr )`, using parentheses to raise the evaluation priority of internal expressions

### Unary Expressions

- Negative numbers: `- expr`
- Positive numbers: `+ expr`
- Logical NOT: `! expr`

### Binary Expressions

Binary expressions formed by operators and operands: `+`, `-`, `*`, `/`, `%`, `==`, `!=`, `>`, `>=`, `<`, `<=`, `&&`, `||`. The precedence and associativity of these operators are the same as in JavaScript.

Assignment operators `=`, `+=`, `-=`, `*=`, `/=`, `%=` are supported.

### Ternary Expressions

Ternary conditional expressions: `cond ? expr : expr`.

### Other Expressions

- Function calls: Same as JavaScript syntax
- Member expressions: `object.prop`
- Subscript expressions: `array[index]`
- Array literals: `[1, expr, ...]`, same as JavaScript syntax
- Object literals: `{ a: 1, b: expr }`, same as JavaScript syntax

### Template Literals

Interpolation expressions partially support [template literal](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Template_literals) syntax. For example, in the following template literal:
``` js
`head ${ expr } tail`
```
The `}` character cannot appear within the expression `expr`, which means you cannot use JavaScript object literals and template literals containing expressions within it. Other expressions mentioned in this section can all be used inside template literals.

Template literals in interpolation expressions do not support line breaks.

::: tip
Syntax errors in expressions can be viewed and located using the glyphix.js tool.
:::

## Other Tips

============================================================
FILE_PATH: src/transl/EN/framework/component/reuse.md

# Component Reuse

Application-level component reuse is mainly achieved through custom components.

## Child Components

Assume that the structure within the `<template>` tag of a certain [UX file](/framework/component/README.md#ux-file) describes the organization of the user interface, for example:
``` html
<template>
  <div>
    <p>text</p>
    <image src="path/to/image.png" />
    <qrcode value="hello world!" />
  </div>
</template>
```
At runtime, this corresponds to the following component tree structure:
``` mermaid
flowchart TB
  div --- p
  div --- image
  div --- qrcode
```
This component tree has one parent node `div` and $3$ child nodes: `p`, `image`, and `qrcode`. The `div` component is the outermost component within the `<template>` tag. We refer to this type of component as the **root component**. Sometimes root components are not unique, for example:
``` html
<template>
  <p>text</p>
  <image src="path/to/image.png" />
  <qrcode value="hello world!" />
</template>
```
has 3 root components. In addition, using the [`for` directive](/framework/commands/for.md) may also result in multiple root component instances, for example:
``` html
<template>
  <p for="x in ['one', 'two', 'three']">
    label: {{x}}
  </p>
</template>
```
will be rendered as $3$ `p` component instances.

============================================================
FILE_PATH: src/transl/EN/framework/component/communicate.md

# Inter-Component Communication

Communication between components is achieved through component properties and event bindings. For example:
``` html
<scroll scroll-snap="center" on:scroll="scrolled($event)" />
```
This passes the `scroll-snap` attribute parameter to the `scroll` component instance to center-align the element, and listens for changes to the `scroll` property.

## Properties and Parameters

Parameters can be passed to child components via the **attribute** fields of component nodes. For example:
``` html
<p text="A message"></p>
```
This passes an attribute named `text` with the value `"A message"` to a `p` component instance. Multiple attributes can be passed according to XML/HTML syntax. Computed values can be passed to component properties using [interpolation expressions](template#interpolation-expressions).

## Event Handling

[Native components](native-component) encapsulate many UI input events, such as responses to touch gestures and UI change events. All of these events can be listened to using the [`on` directive](../commands/on.md).

## Triggering Events

For custom components, you can use the component object's [`$emit(name, value)`](/framework/component/component-apis.md#emit) method to trigger an event:
``` html
<panel on:some-event="console.log(`the event ${$event} was emited!`)">
```

``` js
// in panel.ux
export default {
  emitEvent() {
    this.$emit('someEvent', 'hello')
  }
}
```

The `$emit` method takes two parameters:
- `name`: The name of the property to send the event. It must use lower camelCase (the corresponding template attribute can be kebab-case or lower camelCase).
- `value`: An optional parameter, which is the value of the event property and will be used as the value of the `$event` variable in the `on` directive.

If the view-model of the component object has a property named `name`, the `$emit` method will not modify the property value to `value`.

============================================================
FILE_PATH: src/transl/EN/framework/component/native-component.md

# Native Components

Native components refer to components implemented in C++. The main design goal of these components is to implement specific UI elements, such as buttons or list effects, without carrying business logic. Unlike Web technologies, native components themselves do not provide DOM interfaces, but only reactive component interfaces.

Native components in Glyphix provide a large number of configuration interfaces to achieve rich visual effects. In addition, built-in components feature optimizations designed specifically for embedded platforms.

In this documentation, **native components** refer to components implemented in C++; the term **built-in components** refers to component packages provided by WearOS, though these components are not necessarily implemented in C++.

::: tip
While this documentation distinguishes between native components and built-in components in its descriptions, readers generally do not need to worry about the difference between the two.
:::

## UI Functional Mechanisms

Most UI-related mechanisms are only available in native components. These mechanisms include:
- CSS style sheets, layout, and other mechanisms
- Gestures and touch events
- Rendering and drawing mechanisms

While certain native component mechanism interfaces can be simulated in custom components through parameter/event passing between components, these capabilities are fundamentally implemented by native components.

## UI Rendering

## Component Snapshots

Snapshots are a frame rate optimization technique. Enabling snapshots for complex components can speed up drawing and thus improve frame rate. Essentially, a snapshot is a "screenshot" of a component, and rendering is accelerated by directly drawing these screenshots. Therefore, snapshots are an effective technique for components with complex content that update infrequently. For other scenarios where updates are frequent but lagging or skipped frames can be tolerated, there are corresponding APIs to disable snapshot updates.

## Native Component Objects

You can obtain the native component object using the component's [`$element()`](component-apis#element) method, which allows you to access native component properties or call its methods, for example:

``` js
let el = this.$element('scroll-id')
console.log(`width: ${el.width}`) // Get the component's width via the native component object
el.scrollTo({ top: 100 }) // Scroll the list via API
```

============================================================
FILE_PATH: src/transl/EN/framework/component/javascript.md

# JavaScript Scripts

JavaScript is the scripting language for Glyphix application development. Developers can place JavaScript code inside the `<script>` tag of a UX file, or reference `*.js` script files directly.

## Syntax Support

ES6 syntax is supported.

## Importing Modules

Reference other JS files in your code by importing modules. Generally, developer-defined modules are imported via paths using one of two methods:
``` js
import utils from '../Common/utils.js' // Using the import keyword
const utils = require('../Common/utils.js') // Using the require function
```
For module path rules, please refer to [Paths and URIs](../application/resource). Additionally, the `.js` file extension can be omitted in module paths, so the import statements above can be written as:
``` js
import utils from '../Common/utils' // Using the import keyword
const utils = require('../Common/utils') // Using the require function
```

Import built-in system modules using module names. All system modules start with the `@` character:
``` js
import router from '@system.router' // Using the import keyword
const router = require('@system.router') // Using the require function
```

::: warning
Developers should not start module names with the `@` character, as these names are reserved for system modules.
:::

# Exporting Modules

Use ES6 `export` syntax to export modules, for example:
``` js
// Export default value
export default {
  method() {
    // ...
  }
  props: {
    // ...
  }
}

// Export named values
export function process(args) {
  // ...
}
```

============================================================
FILE_PATH: src/transl/EN/framework/component/template-macro.md

# Template Macros

Template macros are a way to simplify repetitive code. They are top-level `<template>` elements in UX files with a `macro:` attribute:
``` html
<template macro:scroll>
  <scroll #props media-query="(shape: rect)">
    <slot />
  </scroll>
  <scroll #props deformation="fisheye"
          scroll-snap="center" media-query="(shape: circle)">
    <slot />
  </scroll>
</template>
```
For example, a macro named `scroll` is defined here. The macro replaces components with the same name inside the `<template>` template of the current UX file, and:
- All attributes of the component with the same name replace the `#props` placeholder in the template macro;
- The child elements of the component with the same name replace the `<slot />` node in the template macro.

For example:
``` html
<template>
  <scroll :index="3" on:index="onIndexChange">
    <p for="i in 10">item {{i + 1}}</p>
  </scroll>
</template>
```
will be replaced by the `scroll` template macro with:
``` html
<template>
  <scroll :index="3" on:index="onIndexChange" media-query="(shape: rect)">
    <p for="i in 10">item {{i + 1}}</p>
  </scroll>
  <scroll :index="3" on:index="onIndexChange" deformation="fisheye"
          scroll-snap="center" media-query="(shape: circle)">
    <p for="i in 10">item {{i + 1}}</p>
  </scroll>
</template>
```

::: tip
In this example, the macro name is `scroll`, and the macro content also contains the `scroll` tag, but the macro replacement is only performed once and will not be recursively replaced.
:::

## Purpose

As can be seen from the above example, template macros can statically replace ordinary components into another form. The replaced code is usually inconvenient to write by hand and understand. For instance:
``` html
<scroll :index="3" on:index="onIndexChange">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
```
is replaced by:
``` html
<scroll :index="3" on:index="onIndexChange" media-query="(shape: rect)">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
<scroll :index="3" on:index="onIndexChange" deformation="fisheye"
        scroll-snap="center" media-query="(shape: circle)">
  <p for="i in 10">item {{i + 1}}</p>
</scroll>
```
The replaced code actually statically selects different `scroll` component attributes based on [media queries](/framework/render/media-query.md) for screen shapes. Specifically, it adds two attributes to the [`scroll`](/components/scroll.md) component on circular screens:
- [`deformation="fisheye"`](/components/scroll.md#deformation): Enables the fisheye effect for circular screens;
- [`scroll-snap="center"`](/components/scroll.md#scrollsnap): Centers the `scroll` child elements on circular screens.

This template macro adds adaptation for non-standard screen shapes to the original hand-written code. This modification does not require changing the template source code, making it non-intrusive.

## Usage

Currently, there is no way to export template macros for use in other UX files. Therefore, you need to repeatedly write template macros in every UX file that requires them, i.e., top-level elements like:
``` html
<template macro:scroll>
  ...
</template>
```
Template macro nodes and `<template>` nodes can be in any order, but do not define template macros with the same name within a single UX file.

============================================================
FILE_PATH: src/transl/EN/framework/component/README.md

# Component Framework

Components are a technology in Glyphix used to achieve functional reuse in App UI development. By nesting HTML-like elements, multiple components can be combined to form the overall appearance and function of an interface. On the other hand, a certain amount of content and logic is encapsulated within each component, which, when used properly, can reduce code complexity and maintenance costs.

Components are divided into built-in [**native components**](../render/native-component.md) and **custom components** implemented by developers. Native components are generally encapsulations of UI elements, which can be used to display specific UI content or for layout and interaction, such as `text`, `image`, `div`, `list`, etc. Custom components, however, focus on logic implementation and functional encapsulation, because the interfaces implemented within custom components are ultimately hosted by native components.

## Defining Components

Each custom component is defined in a separate `.ux` file:

``` html
<template>
  <p>{{text}}</p>
</template>

<style>
  * {
    font-size: 48;
    text-align: center;
  }
</style>

<script>
  export default {
    data: {
      text: "Hello, World!"
    }
  }
</script>
```

As can be seen, a component consists of styles, a JavaScript script, and a "template" that describes the interface.

## UX Files

A UX (UI XML) file is a component description using the XML format. Each UX file defines a component, and pages are also a type of component.

The following root nodes can exist in a UX file:

- **`<import>`** tag: Used to introduce other components. This tag can be defined multiple times;
- **`<template>`** tag: Defines the content and structure of the component interface. There is one and only one such node;
- **`<template>`** macro tag: Defines repeatedly usable template structures. There can be multiple such nodes, see [Template Macros](./template-macro.md);
- **`<style>`** tag: Defines CSS style sheets. There is one and only one such node;
- **`<script>`** tag: A JavaScript script that implements the logical functions of the component. There is one and only one such node.

The arrangement order of the above nodes is arbitrary. Among them, the `<import>` node never contains child nodes. Note that the insides of the `<style>` node and `<script>` node do not follow XML syntax; symbols such as `>` and `&` do not need to use XML escape rules, but instead follow CSS and JavaScript syntax (similar to HTML).

UX files require all tags to be closed; for example, `<div>...</div>` or `<div/>` are both valid, but a standalone `<div>` or `</div>` will result in an error.

## Page Components

Components declared in the `router.pages` field of `manifest.json` can be used directly as pages.

Compared to general components, page components have more [lifecycle functions](life-cycle#组件和页面的生命周期), while other functions are basically the same. Component code that has already been used for page components can also be used directly as ordinary components.

## Importing Components

### Custom Components

Defined components can be referenced in other components. Fill in the `<import>` tag in the UX file to reference the specified component:
``` xml
<import name="Panel" src="path/to/Panel">
```

The `src` attribute is the path URL of the component, where `Panel` is the file name of the component (excluding the `.ux` suffix); the `name` attribute is an optional component name. If this attribute is not defined, the component's file name will be used as the component name.

`src` supports relative paths, absolute paths, and external paths:

- Relative paths are paths relative to the current UX file.
- Absolute paths are paths relative to the app's `src` path.
- External paths can import resource components outside the app. The specific path is the `package` value in the `appdb.json` of the resource component's app plus the absolute path.

### Global Components

Global components are non-native components defined in the framework. In an application, you can use the `<import>` tag, specify only the `name` attribute, and omit the `src` attribute to import a global component:
``` html
<import name="TopBar" />
```

Applications can only import global components and cannot register new global components. System developers can use the [`globalComponent()`](/api/system-internal.md#globalcomponent) API to register global components.

## Property Documentation Specification

Component property documentation titles take the following form:

<div class="example-block">
  <h3 style="margin-bottom: 0.5rem">
    <span>
      <code>value</code>
      <decl type="number" get set listen />
    </span>
  </h3>
</div>

Where:
- `value` is the name of the property;
- `number` is the property value type;
- <span style="color:#666">Read • Set • Listen</span> on the right indicates the access modes supported by this property.

### Access Modes

A property can support the following access modes:
- **Read**: The value of the property is readable;
- **Set**: The value of the property is writable;
- **Listen**: The property is [listenable](../commands/on.md). Listenable properties typically trigger a listening event when their value changes.

Taking the [`index`](/components/scroll.md#index) property of the [scroll](/components/scroll.md) component as an example, this property supports reading, setting, and listening simultaneously. You can manipulate the `index` property in template syntax:
``` html
<scroll id="scroll1" :index="5" on:index="console.log($event)">
  ...
</scroll>
```
Here, `:index="5"` assigns `5` to the `index` property, while `on:index="console.log($event)"` listens for changes to the `index` property. For more descriptions, please refer to [Inter-component Communication](/framework/component/communicate.md) and the [`on` Directive](../commands/on.md).

### Component Objects and Methods

You can also obtain the component object via the [`$element()`](component-apis.md#element) method to access properties:
``` js
const el = this.$element('scroll1') // Get the component object
console.log(el.index) // Read the index property of the scroll component
el.index = 4 // Set the index property of the scroll component
```
If supported, you can **read** or **set** the object returned by the `$element()` method. The `$element()` method does not support binding event listener functions to properties.

A component's property can also be a **function** or **method**. In this case, the documentation title takes the following form:

<div class="example-block">
  <h3 style="margin-bottom: 0.5rem">
    <span>
      <code>method</code>
      <decl type="(x: number, y: number): void" method />
    </span>
  </h3>
</div>

Where:
- `(x: number, y: number): void` is the signature of the function or method.
- <span style="color:#666">Method</span> on the right indicates that this property is a method.

Component methods can only be accessed through the component object. For example, taking the [`setIndex`](/components/scroll.md#setindex) property of the scroll component:
``` js
const el = this.$element('scroll1') // Get the component object
el.setIndex(4) // Call the setIndex() method
```
Methods do not support read, set, and listen access modes, so such properties only have the <span style="color:#666">Method</span> tag.

### Two-way Binding

When a property simultaneously supports the <span style="color:#666">Set • Listen</span> access modes, it is capable of [two-way binding](../commands/model.md).

============================================================
FILE_PATH: src/transl/EN/framework/component/prop-modifier.md

# Property Modifiers

Standard property operations allow you to set and observe properties. However, certain scenarios have common requirements for property operations. For example, you might want a component's property value not to change immediately when set, but rather transition smoothly using an animation. A direct solution is to write custom logic to achieve the transition effect, but in reality, such logic is common to any property.

To simplify or reuse code for certain common property operations, Glyphix includes several built-in property modifiers. Modifiers are property suffixes denoted by `.`, for example:

``` html
<progress :value="progress" value.transition="{curve: 'ease'}"/>
```

The property modifier key-value pair `value.transition="{curve: 'ease'}"` and the property key-value pair `value="{{progress}}"` written in the component's XML attributes are independent of each other, and they may require completely different parameters.

This document will introduce the functions of each property modifier.

## `transition` Modifier

This modifier proxies property assignment operations, transforming the direct property assignment process into a gradient assignment following the animation transition method specified by the `transition` modifier. For example:

``` html
<!-- The transition modifier defines the transition effect for the value property -->
<progress :max="1000" :value="progress" value.transition="{curve: 'ease'}"/>
<!-- No transition effect -->
<progress :max="1000" :value="progress" />
```


<glyphix id="prop-modifier-transition" height="68" width="480" inline>

``` html
<div>
  <progress :max="1000" :value="progress" value.transition="{curve: 'ease'}"/>
  <progress :max="1000" :value="progress" />
</div>
```

``` css
div > * {
  margin: 8px;
  height: 0.75rem;
}
```

``` js
export default {
  data: {
    progress: 500
  },
  onInit() {
    setInterval(() => this.progress = parseInt(Math.random() * 1000), 3000)
  }
}
```

</glyphix>

Because the `value.transition` modifier is defined for the [`progress`](/components/progress.md) component, every time `this.progress` is modified, the displayed value of the `progress` component does not jump directly to the new value, but rather transitions smoothly via an animation. This effect can be achieved without writing any animation logic.

::: tip
The `value` property of the `progress` component in the example is an integer. Since the default $[0, 100]$ range is prone to stuttering during transition animations, the example uses `:max="1000"` to increase the value range of `value`, thereby making the animation smoother.
:::

### Interpolation Calculation

Currently, only some properties of native components support the `transition` modifier. Supported properties must have "interpolatable" value types. Specifically: for all property value types $a$ and $b$ and progress $p \in [0,1]$, the operation $(1-p)*a+p*b$ must be valid.

The JavaScript `number` type is interpolatable. In addition, transforms and color values can also be interpolated.

#### Transforms

Transforms are usually defined using strings, such as `scale(2) rotate(30deg)`. The string itself is not interpolatable, but when used as a transform property, it is interpolatable (because these strings are parsed into a sequence of transform operations, which are interpolatable). Generally speaking, interpolation is performed step-by-step for each transform operation. For example, during the interpolation of `scale(2) rotate(30deg)` and `scale(1) rotate(90deg)`, the transform in each frame contains two steps: scaling and rotation. The scale factor transitions from $2$ to $1$, while the rotation angle transitions from $30\deg$ to $90\deg$.

#### Colors

Colors are usually represented using string codes, such as `#ff0000`. Color interpolation is calculated channel by channel for red, green, blue, and alpha (transparency).

### `Transition` Object

The value type of the `transition` modifier is the `Transition` object:
``` ts
interface Transition {
  curve?: string,
  duration?: number
}
```

#### `curve` <decl type="?: string"/>

Specifies the [easing function](../render/animation.md#easing-curves) for the transition animation. The default is `'ease'`.

#### `duration` <decl type="?: number"/>

The duration of the animation in seconds. The default is `1`.

============================================================
FILE_PATH: src/transl/EN/framework/component/component-object.md

# Component Object

The `<script>` tag inside a UX file defines and exports a component object. A typical component object is defined as follows:
``` js
export default {
  data: {
    text: "Hello world"
  },
  onInit() {
    console.log("component onInit()")
  },
  clicked(event) {
    console.log(`clicked: ${event}`)
  }
}
```
The component framework allows developers to populate component objects with certain properties to implement functionality. This document will introduce these properties.

## Reactive Programming

**Reactive programming** is a programming paradigm used to dynamically update the user interface and data state. Through **reactive properties**, developers can automatically track data changes and update the user interface without manually triggering and managing these updates. This keeps data and the UI constantly synchronized, enabling a concise and efficient UI programming experience.

### Reactive Properties

Properties defined within the [`data` property](#data-property) and [`computed` property](#computed-property) objects of a component object are the **reactive properties** of the component, also known as view-model properties:
- **`data` Property**: Directly reflects the state of the component. For example, temperature values, display text, or button states can all be defined in `data`. When these property values change, the framework automatically synchronizes them to the view.
- **`computed` Property**: Used to define derived properties calculated based on `data` or other `computed` properties. Computed properties are automatically updated when their dependent data changes, making complex logical expressions more intuitive and concise.

In summary, when a component's reactive property values change, content dependent on these properties is automatically updated and rendered, ensuring that the displayed content remains consistent with the data.

### Automatic Data Binding

**Automatic data binding** is the core concept of reactive programming. It allows data changes to be directly reflected on the user interface without requiring manual handling by the developer.

Since each reactive property is automatically bound to the relevant part of the UI, when the property value changes, the UI updates automatically without the need to call property update functions on specific elements.

For example, defining a reactive property named `counter`:
``` js
export default {
  data: { // Define the counter reactive property in the data object
    counter: 0 // Initial value is 0
  }
}
```

Whenever the value of `counter` changes, the UI referencing this property will also update automatically. The following [template](template) code demonstrates this mechanism:
``` html
<p on:click="counter += 1">
  counter: {{ counter }}
</p>
```
This example demonstrates a counter where clicking the `<p>` tag increments the displayed value of `counter` by 1. You can test it by clicking the online demo below:

<glyphix id="component-object-reactive" height="50" width="200" inline>

``` html
<p on:click="counter += 1">
  counter: {{ counter }}
</p>
```

``` js
export default {
  data: {
    counter: 0
  }
}
```

``` css
p {
  border: 2px solid gray;
  border-radius: 16px;
  padding: 2px 8px;
  text-align: center;
  height: 100%;
}
```

</glyphix>

`{{ counter }}` inside the `<p>` tag is a template [interpolation expression](template.md#interpolation-expression), and its dependency on `counter` is automatically bound. Meanwhile, the [`on:click` listener](/framework/commands/on.md) in the `<p>` tag modifies the `counter` property value upon click. As you can see, automatic data binding eliminates the manual **data**-to-**UI** update operations typical in traditional GUI development, making interface logic cleaner and more straightforward.

## `data` Property

The `data` property is used to declare reactive data properties for the component. This property is an object, for example:
``` js
export default {
  data: {
    text: "Hello world"
  }
}
```
The value of the `data` property must be serializable via `JSON.stringify()`. Specifically, it must meet the following conditions:
- Primitive type values: `number`, `string`, `boolean`, `null`, or `undefined`
- For `Object` and `Array` with recursive structures, the values of the deepest layer of elements must belong to one of the above types

This means that properties of the `data` object in the source code cannot contain functions or other special types of values, which also includes objects like `Date`.

::: note
The `data` object does not support non-JSON-compatible data types, such as `Date`, `Proxy` objects, etc.; this is a known limitation. If you need to use these types of data, you can define them as [custom properties](#custom-properties); otherwise, it will lead to unexpected behavior.
:::

All properties in `data` are view-model properties of the component, so the data within them can be used for reactive programming. Within the component object, you can directly access properties in the `data` object using `this.prop`. Therefore, in the following component object:
``` js
export default {
  data: {
    onInit: true
  },
  onInit() {}
}
```
The code `this.onInit` will access the `onInit` property within the `data` object, rather than the lifecycle function `onInit`.

::: tip
To optimize performance, only define data used for UI rendering and state management within the `data` object. For non-reactive data, you can define them as [custom properties](#custom-properties). For example: timer IDs (return values of `setTimeout()`), [audio player](/api/system-media.md#createaudioplayer) handles, WebSocket connection objects, etc. Such objects generally do not need to be reactive properties and will not function properly if treated as such.
:::

## `computed` Property

The `computed` property object of a component object declares computed properties within the component. Compared to reactive properties in `data`, computed properties allow for properties that require some calculation to obtain their results. For example:
``` html
<text> reversed message: {{ reversedMessage }}
```

``` js
export default {
  data: {
    message: "hello"
  },
  computed: {
    reversedMessage() { // This is the getter method for the reversedMessage computed property
      return this.message.split('').reverse().join('')
    }
  }
}
```
Here, a computed property named `reversedMessage` is declared, which implements a getter function to retrieve the property value. You can directly use `this.reversedMessage` (the `this.` can be omitted in templates) to get the value of this computed property.

Computed properties are also view-model properties of the component. The values of computed properties are cached, so retrieving a computed property's value multiple times will not trigger repeated calculations. On the other hand, computed properties will automatically update when their dependent view-model properties change. In this example, the value of the computed property is calculated from the `message` property, so when the `message` property changes, the value of the `reversedMessage` property will automatically update.

### Setter Method for Computed Properties

By default, computed properties only have a getter method, but you can also provide a setter method for a computed property:
``` js
export default {
  data: {
    message: "hello"
  },
  computed: {
    reversedMessage: {
      get() { // This is the getter method for the reversedMessage computed property
        return this.message.split('').reverse().join('')
      },
      set(value) {
        this.message = value.split('').reverse().join('')
      }
    }
  }
}
```
In this case, the value of the computed property `reversedMessage` is no longer a function, but an object containing two methods: a getter method `get` and a setter method `set`. The parameter of the `set` method is the new value to be set for the computed property.

## `watch` Property

The `watch` object method is used to observe changes in view-model properties, for example:
``` js
export default {
  data: {
    value: 0
  },
  watch: {
    value(newValue, oldValue) {
      console.log(`value change: ${oldValue} -> ${newValue}`)
    }
  }
}
```
The methods in the `watch` object monitor changes to view-model properties of the same name, so `watch.value()` monitors changes to the `value` property. Changes to computed properties can also be monitored by `watch`.

## Lifecycle Functions

See the [Lifecycle](life-cycle.md) documentation for details.

## Custom Properties

Users can also define custom properties in the component object. These properties are not in the view-model (i.e., not in the `data` or `computed` objects) and therefore are not reactive. Developers can define methods as custom properties and use custom properties to store data that does not need to be reactive. For example:
``` html
<p on:click="onClick()">{{ text }}</p>
```

``` js
export default {
  data: {
    text: "some text"
  },
  // Custom properties are not in the data or computed objects, defined directly inside the component object
  timer: null, // Stores the timer handle. It doesn't need to be predefined; assigning to this.timer will automatically create this property
  onInit() {
    // New properties assigned to this are custom properties
    this.timer = setInterval(() => this.text += "?", 1000)
  },
  onDestroy() {
    clearInterval(this.timer)
  },
  onClick() {
    this.text += "." // Operate on view-model properties within custom methods
  }
}
```

In the example, the `text` property is reactive, while `timer` is a non-reactive custom property. The `timer` property is used to store the timer handle; this value has nothing to do with the UI view, so it does not need to be a view-model property. For code consistency, custom properties can also be predefined in the component object:
``` js
export default {
  data: {
    text: "some text"
  },
  timer: null, // Custom properties are direct properties of the component object
  // ...
}
```
As shown in the example, custom properties can be defined directly within the component object. The custom properties of each component are separate instances and are not shared.

::: warning
Custom properties, the `data` object, the `computed` object, lifecycle functions, and other properties must not share duplicate names; otherwise, certain properties will be overwritten and become inaccessible.
:::

### Methods

Custom properties and methods are both direct properties of the component object, and the two are essentially equivalent. When you assign a function to a property of the component object, that property becomes a method. This section demonstrates this equivalence through two examples.

Approach 1: Define methods directly, which is the most common and recommended writing style.
``` js
export default {
  data: {
    count: 0
  },
  increment() {
    this.count++
  }
}
```

Approach 2: Define a property and assign a function to it.
``` js
export default {
  data: {
    count: 0
  },
  increment: function() {
    this.count++
  }
}
```
Both writing styles are completely identical in functionality and can be called via `this.increment()`. They are also used the same way in templates:
``` html
<button on:click="increment()">Count: {{ count }}</button>
```

::: tip
It is recommended to use Approach 1, which is the object method syntax supported by the ES6+ standard, making it more concise and straightforward.
:::

### Dynamically Assigning Methods

In addition to directly defining methods in the component object, you can also dynamically assign methods after the component is instantiated (such as in the `onInit` lifecycle). The key feature of this approach is that the dynamic methods of each component instance are independent and can capture and maintain different states via closures.

Consider a timer component where each instance has its own counter and can be stopped independently. This is a typical use case for dynamically assigned methods:
``` html
<div>
  <text>timeout: {{ counter }}</text>
  <button on:click="stopTimer">Stop</button>
</div>
```

``` js
export default {
  data: {
    counter: 0,
  },
  stopTimer: null, // Optional: predefine the stopTimer method
  onInit() {
    const timer = setInterval(() => {
      this.counter++
    }, 1000)
    // Dynamically create the stopTimer method, capturing the timer variable via closure
    this.stopTimer = () => {
      clearInterval(timer)
      this.stopTimer = null // Set the method to null after stopping
    }
  },
}
```

The example below instantiates 4 timer components simultaneously; you can try stopping any of them independently:

<glyphix id="component-object-dynamic-method" height="200" width="300" inline>
</glyphix>

The implementation of this dynamic method assignment relies on the following key points:
- **Closure Capture**: The `timer` constant created in `onInit` is a local variable, and the `stopTimer` method captures this variable via a closure.
- **Instance Independence**: Each component instance creates its own `timer` and `stopTimer` when calling `onInit`, and they do not interfere with each other.
- **State Isolation**: Clicking the "Stop" button of a specific instance only stops that instance's timer without affecting other instances.

Of course, for this example, a more common practice is to define the `stopTimer` method directly in the component object:
``` js
export default {
  data: {
    counter: 0,
  },
  timer: null,
  onInit() {
    // In this case, timer needs to be stored as a custom property
    this.timer = setInterval(() => {
      this.counter++
    }, 1000)
  },
  stopTimer() {
    // The stopTimer method accesses this.timer to stop the timer
    clearInterval(this.timer)
    this.timer = null // Clear the timer reference
  }
}
```
This is usually more intuitive for timers, but in some scenarios with complex contexts that require dynamic dispatch strategies, dynamically assigned methods can be used to implement more flexible logic. The table below compares direct method definition versus dynamic method assignment:

| Feature | Direct Method Definition | Dynamic Method Assignment |
|---------|--------------------------|---------------------------|
| Shareability | All instances share the same function object | Each instance has an independent function copy |
| Closure Capture | Does not capture local variables in scope | Can capture local variables in scope |
| Memory Usage | Less (shared) | Slightly more (one per instance) |
| Use Case | General, stateless operations | Operations requiring local state capture |

============================================================
FILE_PATH: src/transl/EN/framework/component/component-apis.md

# Component Built-in Interfaces

The Glyphix framework provides several built-in properties for components, all of which are accessed using the `this.$xxx` format. These built-in properties offer functionalities beyond the reactive framework.

All built-in properties are read-only.

## Properties

### `$app` <decl type="Applet" get />

The `$app` property allows you to access the application object exported from `app.js`.

### `$page` <decl type="Component" get />

The `$page` property allows you to access the component object of the page to which the component belongs. For page components, the value of `this.$page` is `this`.

### `$valid` <decl type="boolean" get />

Determines whether the component object is valid. A value of `false` indicates that the component has been destroyed.

::: tip
For destroyed components, any operation other than accessing the `$valid` property is illegal.
:::

#### Destroyed Components

The component lifecycle is controlled by the rendering framework. Well-written code typically does not access destroyed components, but if you forget to cancel timers or listeners upon component destruction, for example:

``` js
setInterval(() => {
  this.secondCounter += 1
}, 1000)
```

If the component object is destroyed, you might encounter an error like this:

```
the component object has been destroyed
  stack backtrace:
    at <anonymous> (pkg://com.example.app/main/index.js:50)
TypeError: proxy: cannot set property
  stack backtrace:
    at <anonymous> (pkg://com.example.app/main/index.js:52)
```

If it is indeed difficult to clear timers or cancel listeners when the component is destroyed, you can use the `$valid` property to safely check whether the component has been destroyed. The following example suppresses the aforementioned runtime error:

``` js
let timer = setInterval(() => {
  if (this.$valid) {
    this.secondCounter += 1
  } else {
    clearTimeout(timer) // Clear the timer after the component is destroyed
  }
})
```
Such scenarios (such as recurring timers or event listener functions) generally follow a fixed code structure:
1. Use `this.$valid` to check if the component is valid before accessing component properties;
2. Execute normal component property access operations in the valid branch;
3. Clear timers or cancel listeners in the invalid branch, and **return immediately** to ensure component properties are no longer accessed.

::: warning
When using the `$valid` property to determine whether a component has been destroyed, pay special attention to the possibility that closures in listener functions may cause memory leaks. Failing to properly cancel event listeners or timers can cause the system to retain references to these closures even after the component is destroyed, preventing them from being garbage-collected.
:::

#### Memory Leak Risks

In JavaScript, a closure refers to the association between a function and variables in its outer scope. When a function is created, it captures variables in the outer scope and maintains references to them, even after the outer scope has finished executing. This means that variables referenced inside the closure remain in memory until the closure itself is garbage-collected.

In the component framework, when you register an event listener or start a timer, you typically pass a callback function, which may capture certain properties or the context of the component (such as `this`).

Although the component object itself is correctly destroyed and its memory freed by the framework, these closure functions are not cleared. If event listener or timer callbacks are not actively removed, these closures may persist and accumulate over time, leading to memory leaks—especially in long-running applications. Such leaks can be difficult to notice.

The following example demonstrates a potential memory leak:
``` js
let timer = setInterval(() => {
  if (this.$valid) {
    this.secondCounter += 1;
  }
}, 1000)
```
Although `if (this.$valid)` is used inside the callback function to check whether the component is still active, thereby avoiding errors thrown after component destruction, this approach does not prevent memory leaks. The reason is that `$valid` only checks validity; checking this property prevents access to already destroyed component objects. However, because the timer is not stopped, the closure of the callback function itself is still referenced, and that closure cannot be garbage-collected.

::: tip
To avoid this subtle memory leak, you should actively cancel timers or remove event listeners when the component is [destroyed](./life-cycle.md#ondestroy), rather than relying solely on the `$valid` check. Even though `$valid` prevents improper operations from executing after component destruction, it cannot clean up the closures of the callback functions themselves.

All JavaScript memory is released after the application exits, so such memory leaks do not accumulate indefinitely.
:::

## Methods

### `$component` <decl type="(name: string, url: string): void" method />

Dynamically imports a component (the `<import>` tag can only import components statically), for example:
``` js
this.$component("Name", "url")
```
The string `"Name"` is the name of the imported component and must use PascalCase; the string `"url"` is the URI of the imported component.

### `$element` <decl type="(id: string): Element | undefined" method />

Returns the [native sub-component](native-component.md#原生组件对象) object with the specified ID within the component, or `undefined` if no such sub-component exists. The `$element()` method traverses all child nodes of the component, allowing component instances in other UX files to be found as well.

The `$element()` method matches IDs across the entire rendered sub-component tree, not limiting itself to sub-components in the current [component template](template.md). Sometimes you need to be very careful with this feature. For example, consider the following template:
``` html
<scroll>
  <MyComponent />
  <div id="panel">...</div>
</scroll>
```
When an element with `id="panel"` also exists inside the custom component `MyComponent`, using `this.$element('panel')` will find the child element inside `MyComponent` rather than the `div` element in the example.

::: tip
The `$element()` method cannot be used on custom components, even if the `id` property is set for the custom component. Because `$element()` accesses the rendered component tree, it must be used in or after the [`onReady()`](life-cycle.md#onready) lifecycle method, and cannot be used in [`onInit()`](life-cycle.md#oninit).
:::

Please refer to [this documentation](README.md#组件对象和方法) to learn how to access the component object returned by the `$element()` method.

### `$emit` <decl type="(event: string, value: any): void" method />

For details, see [Inter-component Communication](communicate).

