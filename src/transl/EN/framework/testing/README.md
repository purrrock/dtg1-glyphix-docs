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