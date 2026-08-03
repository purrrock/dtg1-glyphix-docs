# testing framework


Glyphix provides an automated testing framework for applications that simulates user operations and checks interface behavior. This testing framework does not simulate random operations, but requires developers to write test cases.


## Basic concepts


Glyphix's testing framework is actually a set of JavaScript APIs that generally implement the following functions:


- Register test case
- Find interface elements
- Simulate user operations or actions
- Assertions and verification logic


### Test steps


The basic principles of a test step are to **find a specific element**, **perform a simulated action** and (optionally) **validate the content**. For example:


1. Find an element with CSS class `play-button`;
2. Click on this element;
3. Content is not verified.


In the actual interface, `.play-button` may be a play button. Clicking this button will start playing music. The JavaScript code corresponding to this test is as follows:


```js
await tc.getByClass("play-button").click();
```


The test code automatically waits for the `.play-button` element to appear and moves it into the interface viewport before clicking the element. These test APIs will automatically wait for animations or gestures in the interface, and will honor `await` when the click gesture is fully completed. Therefore, there is usually no need to manually move elements or explicitly wait for the operation to complete.


### Find elements


The testing framework provides a series of interfaces to find elements in the interface, such as:


- `tc.getByClass()`: Find elements based on class names;
- `tc.getByTag()`: Find elements based on tag names.


These interfaces will wait for the element to appear and try to move the element into the visible area before taking the next step.


### Simulate user operations


## Start writing tests


### test case file


Glyphix's test cases are JavaScript code and are stored in the application's resource bundle. It is recommended to store test cases separately in the `src/tests` directory of the project, for example:


```shell
<app-name>
├─ README.md         # 项目自述文件
└─ src               # 项目的源代码目录
    ├─ app.js        # app 入口脚本文件
    ├─ manifest.json # 配置应用基本信息
    ├─ tests         # 存放所有的测试用例
    │  └─ spec.js    # 测试用例代码
    └─ Main          # 存放主页面的目录
        └─ index.ux  # 主页面的界面描述文件
```


The test code in this example is the `src/tests/spec.js` file. You can also create multiple test files as needed.


::: tip

The file name of the test case is usually spec, which is the abbreviation of specification. A spec file is used to define and describe the expected behavior of the software and its functionality. It usually contains a set of test cases to verify that the software works as expected.
:::



### Write test cases


Assume that our application has a main page and there is a `span` element with a class name of `clickable`:


```html
<div>
  <span class="clickable" on:click="console.log('click span')"> click me </span>
</div>
```


Now, we are going to write an automated test script that will click the `span` component every second and end the test after 3 clicks. To do this, we add the following code in `src/tests/spec.js`:


```js
// Import the @system.test module to provide the API of the testing framework
import tc from "@system.test";

// Register an automated test case named click-test
tc.testcase("click-test", async () => {
  for (let i = 0; i < 3; ++i) {
    // Find an element with class="clickable" and click on it
    await tc.getByClass("clickable").click();
    // wait one second
    await tc.wait(1);
  }
});
```


Next, you need to register this test script and start the test.


### Register test script


In general code, statements like `import 'tests/spec.js'` are usually used to introduce scripts, but this will cause the JavaScript module to always be loaded. In order to optimize the application's loading speed and memory usage, we do not need to introduce these scripts in non-test environments. To do this, you can register the test script in the App object in the `src/app.js` file:


```js
export default {
  // Use the testsuite attribute to register a list of test scripts
  testsuite: ["tests/spec.js"],
  onCreate() {
    /* ... */
  },
  // ...
};
```


This method does not import these test scripts immediately, but delays the import until the test is executed. Therefore, when tests are not executed, using the `testsuite` attribute does not increase overhead, and developers do not need to consider the performance burden caused by optimizing the loading of test scripts.


::: warning

Even if there is only one test script, the `testsuite` attribute must be a `Array` object with the path to the test script included in it, as in the examples in this section. The path to the test script is always relative to the directory where the `app.js` file is located, you can also use an absolute path, such as `/tests/spec.js`.
:::



## Run test case


### emulator


To run test cases, the simulator should be started using the `gx emu -i` command. You will see something like this in the terminal:


```shell
❯ gx emu -i
[emu] Open inspector http://localhost:14200 in browser.
```


Next open the `http://localhost:14200` link in your browser and enter the "Console" tab, then enter the following text in the "RPC" bar at the bottom:
```json
{"fn": "test.start", "name": "click-test"}
```
You can start the `click-test` test case written earlier. At this time, you should see the following log in the log browser:


```log
19:14:33.320 [inspector] test com.example.app . click-test started
19:14:33.640 [js] 'click span'
19:14:35.090 [js] 'click span'
19:14:36.510 [js] 'click span'
19:14:37.600 [tester] com.example.app testcase click-test finished
```


This indicates that the test executed successfully and the `span` element was indeed clicked $3$ times.