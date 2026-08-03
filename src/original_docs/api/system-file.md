# 文件系统操作

本模块提供 Promise 风格的文件系统操作 API。相比于 callback 风格，Promise 风格可避免回调地狱以降低代码复杂度。

::: warning
由于回调式文件 API 在时序、并发和错误处理上极易埋坑，强烈建议使用 [Promise/`await` API](./README.md#快应用异步接口)；详细建议请参考[常见陷阱和建议](#常见陷阱和建议)。

`@system.file` 中的 API 都是[异步文件操作](#异步文件操作)，这和同步的 IO 访问有本质区别。请务必理解异步编程的基本概念，并且熟悉 Promise 和 `async/await` 的用法。
:::

## 导入模块

``` js
import file from '@system.file'
```

## 使用说明

### 错误码

返回的错误码含义为：
- `202`：参数错误；
- `300`：IO 操作失败；
- `400`：权限不足；

## 接口定义

### `readText`
<decl method><pre>
(params: {
  uri: string
}): Promise&lt;string>
</pre></decl>

读取文本文件的内容。`params` 参数字段描述：
- `uri`：待读取文件的 URI。

### `writeText`
<decl method><pre>
(params: {
  uri: string,
  text: string,
  append?: boolean
}): Promise&lt;void>
</pre></decl>

将文本写入到文件中，如果文件不存在则会创建新文件。此函数还会自动创建父级目录。`params` 参数字段：
- `uri`：待写入文件的 URI。
- `text`：要写入文件的文本内容。
- `append`：值为 `true` 将数据追加写入到文件的尾部，值为 `false` 覆盖原有内容。默认 `false`。

### `read`
<decl method><pre>
(params: {
  uri: string,
  position?: number,
  length?: number
}): Promise&lt;ArrayBuffer>
</pre></decl>

读取文件内容到一个 `ArrayBuffer` 对象中。`params` 参数字段：
- `uri`：待读取文件的 URI。
- `position`：文件读取位置的偏移量，默认为 $0$。
- `length`：期望读取的字节数，如果不指定则读取到文件尾部。

### `write`
<decl method><pre>
(params: {
  uri: string,
  data: ArrayBuffer,
  position?: number,
  append?: boolean
}): Promise&lt;void>
</pre></decl>

将 `ArrayBuffer` 中的字节数据写入到文件中，如果文件不存在则会创建新文件。此函数还会自动创建父级目录。

`params` 参数字段说明：
- `uri`：待写入文件的 URI。
- `data`：待写入的数据。
- `position`：文件写入位置的偏移量，默认为 $0$。
- `append`：值为 `true` 将数据追加写入到文件尾部并忽略 `position` 参数。

### `copy`
<decl method><pre>
(params: {
  srcUri: string,
  dstUri: string
}): Promise&lt;void>
</pre></decl>

将源文件复制到指定位置，会自动创建目标目录。`params` 参数字段：
- `srcUri`：源文件的 URI。
- `dstUri`：目标文件的 URI。

### `rename`
<decl method><pre>
(params: {
  oldUri: string,
  newUri: string
}): Promise&lt;void>
</pre></decl>

重命名文件或者目录，会自动创建目标目录。`params` 参数字段：
- `oldUri`：重命名之前文件或者目录的 URI。
- `newUri`：重命名之后的 URI。

### `list`
<decl method><pre>
(params: {
  uri: string,
}): Promise&lt;Array>
</pre></decl>

列出指定目录下的所有项目（文件或目录）列表。`params` 参数字段：
- `uri`：带列举的目录 URI，应用资源包中的文件不支持列举。

`Promise` 的参数是一个包含文件信息的数组，形如
``` js
[
  {
    uri: 'fonts'
  },
  {
    uri: 'font-faces'
  },
]
```

::: tip
你不能列举应用资源包内的文件，因此 `await file.list({ uri: "/assets/images" })` 等直接使用[路径](/framework/application/resource.md#uri-和路径)的用法都是无效的。事实上，应该使用各种 [`internal`](/framework/application/resource.md#internal) URI 协议。
:::

### `access`
<decl method><pre>
(params: {
  uri: string
}): Promise&lt;boolean>
</pre></decl>

检查一个文件是否存在。`params` 参数字段：
- `uri`：待检测的文件 URI。

### `mkdir`
<decl method><pre>
(params: {
  uri: string,
  recursive?: boolean
}): Promise&lt;void>
</pre></decl>

创建一个目录。`params` 参数字段：
- `uri`：待创建目录的 URI。
- `recursive`：是否要递归创建（如果父级目录不存在则先创建父级目录），默认为 `false`。

### `remove`
<decl method><pre>
(params: {
  uri: string,
  recursive?: boolean
}): Promise&lt;void>
</pre></decl>

删除一个目录或文件。`params` 参数字段：
- `uri`：待创建目录的 URI。
- `recursive`：是否要递归删除，默认为 `false`。不递归删除时只能删除文件或者空的目录。

### `stat`
<decl method><pre>
(options: {
  uri: string
}): Promise&lt;{size: number}>
</pre></decl>

获取文件的属性信息。`options` 参数各字段描述如下：
- `uri`：待获取属性的文件 URI。

`stat()` 异步返回一个对象，包含以下文件属性：
- `size`：文件的尺寸，单位为字节。

## 常见陷阱和建议

以下示例均基于“回调式”写法的典型问题，展示其在文件 IO 中为何极易失效或难以维护，并给出 Promise/`await` 的等价重写。

### 异步文件操作

`@system.file` 模块中的所有 API 都是**异步操作**。这意味着当你调用文件操作函数时，函数会**立即返回**，而不会等待实际的 I/O 操作完成。文件的读写操作会在后台进行，操作完成后会通过 Promise 通知你结果。

::: danger 新手必读
如果你不熟悉异步编程，请务必认真阅读本节内容。**忽略异步操作的返回值**或**不等待 Promise 完成**会导致严重的程序错误，这些错误在模拟器中可能不会表现出来，但在真实设备上会导致数据丢失或程序错误。
:::

#### 什么是异步操作？

在同步编程中，代码按顺序执行，每一行代码执行完毕后才会执行下一行：

```js
// 同步代码示例（伪代码，file API 不提供同步版本）：阻塞等待文件读取
const text = file.readTextSync({ uri: 'internal://files/data.txt' });
console.log(text); // 必然会输出文件内容
console.log('读取完成');
```

但在异步编程中，I/O 操作不会阻塞代码执行。当你调用异步函数时，它会立即返回一个 Promise 对象，实际的文件操作在后台进行：

```js
// 错误：忽略 Promise，不等待操作完成（调用立即返回）
file.readText({ uri: 'internal://files/data.txt' });
console.log('这行代码会立即执行，此时文件可能还没读完！');

// 正确：使用 await 等待操作完成
const text = await file.readText({ uri: 'internal://files/data.txt' });
console.log(text); // 此时文件已经读取完成，可以安全使用
console.log('读取完成');
```

#### 为什么必须使用 await？

不使用 `await` 等待异步操作完成会导致以下严重问题。

数据尚未准备好就被使用：
```js
// 错误示例：忽略返回值
function loadConfig() {
  let config = null;
  file.readText({ uri: 'internal://files/config.json' })
    .then(text => config = JSON.parse(text)); // 这个回调函数会在未来某个时刻执行
  // 这里 config 仍然是 null，因为文件读取还没完成！
  console.log(config.theme); // 错误：试图访问 null.theme，会崩溃
  return config; // 返回 null
}

// 正确示例：等待数据准备好
async function loadConfig() {
  const text = await file.readText({ uri: 'internal://files/config.json' });
  const config = JSON.parse(text);
  console.log(config.theme); // 正确：文件已读取，可以安全访问
  return config; // 返回实际的配置对象
}
```

操作顺序混乱：
```js
// 错误示例：不等待写入完成
async function saveAndLoad() {
  // 写入新数据，但不等待完成
  file.writeText({ uri: 'internal://files/score.txt', text: '100' });
  
  // 立即读取，此时写入可能还没完成，读到的可能是旧数据！
  const score = await file.readText({ uri: 'internal://files/score.txt' });
  console.log(score); // 可能输出旧值，而不是 '100'
}

// 正确示例：等待写入完成后再读取
async function saveAndLoad() {
  // 用 await 等待写入完成
  await file.writeText({ uri: 'internal://files/score.txt', text: '100' });
  
  // 现在读取，确保读到的是刚写入的数据
  const score = await file.readText({ uri: 'internal://files/score.txt' });
  console.log(score); // 输出 '100'
}
```

资源竞争和数据损坏：

```js
// 错误示例：多次并发写入同一个文件
async function appendLog(message) {
  const log = await file.readText({ uri: 'internal://files/log.txt' });
  // 不用 await 等待写入完成，继续执行
  file.writeText({ uri: 'internal://files/log.txt', text: log + message + '\n' });
}

// 并发调用：不 await appendLog
appendLog('事件A'); // 读取 -> 写入 A
appendLog('事件B'); // 读取 -> 写入 B
// 结果：两次读取可能都读到同样的旧内容，后一次写入会覆盖前一次，导致 '事件A' 丢失

// 正确示例：等待每次写入完成
async function appendLog(message) {
  const log = await file.readText({ uri: 'internal://files/log.txt' });
  await file.writeText({ uri: 'internal://files/log.txt', text: log + message + '\n' });
}

// 串行调用
await appendLog('事件A'); // 完整的读取 -> 写入 -> 完成
await appendLog('事件B'); // 完整的读取 -> 写入 -> 完成
// 结果：两个事件都被正确记录
```

#### 模拟器陷阱

::: warning 模拟器无法暴露所有异步问题
在开发用的模拟器中，由于电脑的 I/O 速度极快，文件操作几乎是瞬间完成的。因此，即使代码没有正确使用 `await`，在模拟器中也可能看起来“正常工作”。
:::

真实的嵌入式设备上的文件系统 I/O 则存在以下限制：
- Flash 存储器的读写速度较慢；
- 文件系统缓存能力弱，读写文件通常直接访问存储介质；
- 系统资源有限，I/O 操作会被排队延迟。

没有使用 `await` 的代码在真实设备上**几乎必然会出错**！ 不要因为模拟器测试通过就忽略异步编程规范。

#### 正确使用 async/await 的规则

1. 任何调用文件 API 的函数都应该声明为 `async`：
   ```js
   async function saveData(data) {
     await file.writeText({ uri: 'internal://files/data.txt', text: data });
   }
   ```
2. 所有文件操作前都加上 `await` 关键字：
   ```js
   const content = await file.readText({ uri: 'internal://files/data.txt' });
   ```
3. 使用 `try/catch` 处理可能的错误：
   ```js
   try {
     await file.writeText({ uri: 'internal://files/data.txt', text: 'hello' });
   } catch (err) {
     console.error('写入失败:', err);
   }
   ```
4. 需要顺序执行的操作必须依次 `await`：
   ```js
   // 正确：先写入，再读取验证
   await file.writeText({ uri: 'internal://files/data.txt', text: 'test' });
   const verify = await file.readText({ uri: 'internal://files/data.txt' });
   console.log(verify === 'test' ? '验证成功' : '验证失败');
   ```
5. 不相关的操作可以并行执行，但要等待全部完成：
   ```js
   // 正确：并行读取多个文件，但等待全部完成
   const [file1, file2, file3] = await Promise.all([
     file.readText({ uri: 'internal://files/a.txt' }),
     file.readText({ uri: 'internal://files/b.txt' }),
     file.readText({ uri: 'internal://files/c.txt' })
   ]);
   ```

#### 完整示例：用户配置管理

```js
import file from '@system.file'

const CONFIG_URI = 'internal://files/user-config.json';

// 正确的异步配置管理
class ConfigManager {
  async load() {
    try {
      const text = await file.readText({ uri: CONFIG_URI });
      return JSON.parse(text);
    } catch (err) {
      // 文件不存在或格式错误，返回默认配置
      console.warn('加载配置失败，使用默认值:', err.message);
      return { theme: 'dark', language: 'zh-CN' };
    }
  }

  async save(config) {
    try {
      const text = JSON.stringify(config, null, 2);
      await file.writeText({ uri: CONFIG_URI, text });
      console.log('配置已保存');
    } catch (err) {
      console.error('保存配置失败:', err.message);
      throw err; // 重新抛出，让调用者知道保存失败
    }
  }

  async update(changes) {
    // 读取 -> 修改 -> 保存的完整流程
    const config = await this.load();
    Object.assign(config, changes);
    await this.save(config);
    return config;
  }
}

// 使用示例
async function main() {
  const manager = new ConfigManager();
  // 加载配置
  const config = await manager.load();
  console.log('当前主题:', config.theme);
  // 更新配置
  await manager.update({ theme: 'light' });
  console.log('主题已更新');
}

// 注意：main 本身也是异步的，需要正确调用
main().catch(err => {
  console.error('程序执行出错:', err);
});
```

#### 小结

- 所有 `@system.file` API 都是异步的，必须使用 `await` 等待完成。
- 不使用 `await` 会导致严重问题，例如数据未准备、操作乱序、错误丢失、数据损坏。
- 模拟器测试通过不等于代码正确，真实设备上 I/O 更慢，问题会暴露。
- 使用 `async/await` + `try/catch` 是正确且最简洁的写法。
- 永远不要忽略 Promise 的返回值。

### 回调陷阱

#### 回调顺序错觉与竞态覆盖

该类场景涉及一组文件被读-改-写的操作序列。这是使用回调参数触发回调风格的问题代码：
```js
// 期望对计数文件 +1，但两个并发调用可能相互覆盖
function increment(uri, done) {
  file.readText({
    uri,
    success(text) {
      const n = Number(text || '0') + 1;
      console.log(`read ${text}, write ${n}`);
      // readText() 成功回调中嵌套写文件操作
      file.writeText({
        uri,
        text: String(n),
        success() { done && done(); },
        fail(msg, code) { done && done(new Error(`${msg}:${code}`)); }
      });
    },
    fail(msg, code) { done && done(new Error(`${msg}:${code}`)); }
  });
}

// 先建 counter 文件，然后并发触发两次 +1
file.writeText({
  uri: 'internal://files/counter',
  text: '0',
  success() {
    // 并发触发两次 increment，但是不做任何同步
    increment('internal://files/counter');
    increment('internal://files/counter');
  }
})
```
运行该脚本后，可能只会看到两条 `read 0, write 1` 日志，并且最终 `counter` 文件内容为 `1`，而不是期望的 `2`。失败机制为：两次 read 都读到相同旧值，后写覆盖先写，导致结果只 +1。

::: note
上面的脚本看起来十分复杂，难以正确地传递 `done` 回调函数，这很容易诱导为错误的实现。实际上，使用 `async/await` 重写后，代码会变得非常简洁且易于理解。
:::

一个复杂的技巧是使用互斥 + 串行化技术，这可以完全保留原有的并发 `increment` 语义，并保证整个读文件 + 递增计数操作的原子性：
```js
// 基于 Promise 链的按 key 互斥执行
const lock = new Map();

/**
 * 串行地执行同一个 key 的异步任务。这是一个工具函数。
 * @param {string} key
 * @param {() => Promise<any>} fn
 * @returns {Promise<any>} 返回 fn 的结果
 */
function withLock(key, fn) {
  // 取到该 key 之前的“尾巴”（没有则用已完成的 Promise）
  const prev = lock.get(key) || Promise.resolve();
  // 即便 prev 失败，也要继续后续队列，所以先 .catch(() => {})
  const p = prev.catch(() => {}).then(async () => {
    try {
      return await fn(); // 真正的任务只在轮到它时才执行
    } finally {
      // 如果自己仍是当前尾巴，说明没有新的任务进来，可以清理
      if (lock.get(key) === p) lock.delete(key);
    }
  });
  lock.set(key, p); // 把新的尾巴挂上去
  return p;
}

// 现在，increment 内部的实际 IO 由 withLock 串行化：
async function increment(uri) {
  await withLock(uri, async () => {
    const n = Number(await file.readText({ uri })) || 0;
    console.log(`read ${n}, write ${n + 1}`);
    await file.writeText({ uri, text: `${n + 1}` });
  });
}

file.writeText({
  uri: 'internal://files/counter',
  text: '0'
}).then(() => {
  // 并发触发两次 increment，同样不做任何同步
  increment('internal://files/counter');
  increment('internal://files/counter');
});
```
运行该脚本后，`counter` 文件内容必然为 `2`，且日志顺序必然为 `read 0, write 1` → `read 1, write 2`。

但是这样的代码看起来十分复杂，最简单的办法是直接 `await increment()` 调用（表现为 `await` 传染）：
```js
async function increment(uri) {
  const n = Number(await file.readText({ uri })) || 0;
  console.log(`read ${n}, write ${n + 1}`);
  await file.writeText({ uri, text: `${n + 1}` });
}

file.writeText({
  uri: 'internal://files/counter',
  text: '0'
}).then(async () => {
  // 使用 await 等待 increment，保证顺序
  await increment('internal://files/counter');
  await increment('internal://files/counter');
})
```

#### 回调层级与资源泄漏

以下示例展示了回调式写法中，因多层嵌套和分支过多而导致的资源泄漏和逻辑错误：

```js
function exportReport(uri, cb) {
  startBusyIndicator();
  file.readText({
    uri,
    success(t) {
      transformCb(t, (err2, out) => {
        if (err2) {
          stopBusyIndicator();
          return cb && cb(err2);
        }
        file.writeText({
          uri: `${uri}.bak`,
          text: out,
          complete() {
            // 某些分支忘记 stopBusyIndicator() 或 cb()
          }
        });
        // 这也是错的，因为 writeText() 是异步的，并可能尚未完成
        stopBusyIndicator();
        cb && cb(null);
      });
    },
    fail(msg, code) {
      stopBusyIndicator();
      cb && cb(new Error(`${msg}:${code}`));
    }
  });
}
```

由于回调嵌套层级太深，`stopBusyIndicator()` 和 `cb()` 容易出现遗漏或误用：
- 遗漏清理逻辑，导致“忙指示器”永远不停止，或者调用方永远得不到回调；
- 过早调用了清理逻辑，导致调用方误以为写入已完成。

推荐写法（结构化清理）：

```js
async function exportReport(uri) {
  startBusyIndicator();
  try {
    const t = await file.readText({ uri });
    const out = await transform(t);
    await file.writeText({ uri: `${uri}.bak`, text: out });
  } finally {
    stopBusyIndicator(); // 总是在文件 IO 都完成（或异常）后调用
  }
}
```

#### 混用 await 与回调导致风格切换（await 失效）

任何回调处理函数都不会返回 Promise 对象，使 `await` 等待失效：

```js
// 因为传入了 complete 回调，该调用会启用回调风格，不会返回 Promise
await file.writeText({
  uri: 'internal://files/a.txt',
  text: 'x',
  complete() {}, // 不要传入 success/fail/complete 参数字段
});
// 上面这行不会真正等待写入完成，后续代码可能提前执行
```

推荐写法：

```js
// 使用 await 时不要传入 success/fail/complete
await file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
```

### 最佳实践

#### 明确的顺序与错误处理

```js
import file from '@system.file'

export async function updateConfig(uri, patch) {
  try {
    const text = await file.readText({ uri });
    const json = JSON.parse(text || '{}');
    Object.assign(json, patch);
    await file.writeText({ uri, text: JSON.stringify(json, null, 2) });
  } catch (err) {
    // 统一处理/记录错误，不要吞没
    console.error('updateConfig failed:', uri, err);
    throw err;
  }
}
```

要点是通过 `await` 明确串行时序；用 `try/catch` 保证错误被感知与上抛。如果完全不处理错误，运行时会记录异常日志，并中断整个调用链。

#### 避免 TOCTTOU（检查-使用竞态）

不要先 `access()` 后 `write*()` 再依赖两者之间的状态不变。例如这样的代码：

```js
file.access({
  uri: 'internal://files/a.txt',
  success(exists) {
    if (exists) {
      file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
    } else {
      // 如果文件不存在，先 mkdir 再写文件
      file.mkdir({
        uri: '/data',
        recursive: true,
        complete() {
          file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
        }
      });
    }
  }
});
```

推荐的写法是直接尝试写入，运行时会自动创建父目录：
```js
async function safeWriteText(uri, text) {
  try {
    await file.writeText({ uri, text });
  } catch (e) {
    // 这里应该处理错误，并且不需要 mkdir 后写文件
  }
}
```

#### 半写与崩溃中断

在 MCU 设备上，系统异常通常直接复位，应用不会在“半崩溃”状态下继续执行。即使应用被杀死，已经提交的文件写入操作也不会中断（但可能完全不执行），因此通常不需要担心“写一半文件”的问题：
```js
// 直接覆盖写，在电源中断/系统崩溃可能留下半写文件
file.writeText({ uri: '/data/config.json', text: bigJson });
```

对于关键的配置文件更新，可以使用“临时文件 + 同目录 rename”模式来加固稳定性：
```js
async function atomicWriteText(uri, text) {
  const tmp = `${uri}.tmp`;
  await file.writeText({ uri: tmp, text });
  await file.rename({ oldUri: tmp, newUri: uri });
}
```

