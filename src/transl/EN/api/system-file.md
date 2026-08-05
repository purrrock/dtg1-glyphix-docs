# File System Operations

This module provides Promise-style file system operation APIs. Compared to the callback style, the Promise style avoids callback hell and reduces code complexity.

::: warning
Since callback-style file APIs are extremely prone to pitfalls in terms of timing, concurrency, and error handling, it is strongly recommended to use the [Promise/`await` API](./README.md#quickapp-asynchronous-interfaces). For detailed suggestions, please refer to [Common Pitfalls and Recommendations](#common-pitfalls-and-recommendations).

All APIs in `@system.file` are [asynchronous file operations](#asynchronous-file-operations), which are fundamentally different from synchronous I/O access. Please make sure you understand the basic concepts of asynchronous programming and are familiar with the usage of Promises and `async/await`.
:::

## Importing the Module

``` js
import file from '@system.file'
```

## Instructions

### Error Codes

The returned error codes mean:
- `202`: Parameter error;
- `300`: I/O operation failed;
- `400`: Insufficient permissions;

## API Definitions

### `readText`
<decl method><pre>
(params: {
  uri: string
}): Promise&lt;string>
</pre></decl>

Reads the content of a text file. Description of `params` fields:
- `uri`: The URI of the file to be read.

### `writeText`
<decl method><pre>
(params: {
  uri: string,
  text: string,
  append?: boolean
}): Promise&lt;void>
</pre></decl>

Writes text to a file. If the file does not exist, a new file will be created. This function also automatically creates parent directories. `params` fields:
- `uri`: The URI of the file to be written.
- `text`: The text content to write to the file.
- `append`: If `true`, data is appended to the end of the file; if `false`, it overwrites the original content. Default is `false`.

### `read`
<decl method><pre>
(params: {
  uri: string,
  position?: number,
  length?: number
}): Promise&lt;ArrayBuffer>
</pre></decl>

Reads file contents into an `ArrayBuffer` object. `params` fields:
- `uri`: The URI of the file to be read.
- `position`: The offset of the file reading position, defaulting to $0$.
- `length`: The expected number of bytes to read. If not specified, it reads to the end of the file.

### `write`
<decl method><pre>
(params: {
  uri: string,
  data: ArrayBuffer,
  position?: number,
  append?: boolean
}): Promise&lt;void>
</pre></decl>

Writes byte data from an `ArrayBuffer` into a file. If the file does not exist, a new file will be created. This function also automatically creates parent directories.

Description of `params` fields:
- `uri`: The URI of the file to be written.
- `data`: The data to be written.
- `position`: The offset of the file writing position, defaulting to $0$.
- `append`: If `true`, data is appended to the end of the file and the `position` parameter is ignored.

### `copy`
<decl method><pre>
(params: {
  srcUri: string,
  dstUri: string
}): Promise&lt;void>
</pre></decl>

Copies the source file to the specified location and automatically creates the target directory. `params` fields:
- `srcUri`: The URI of the source file.
- `dstUri`: The URI of the target file.

### `rename`
<decl method><pre>
(params: {
  oldUri: string,
  newUri: string
}): Promise&lt;void>
</pre></decl>

Renames a file or directory and automatically creates the target directory. `params` fields:
- `oldUri`: The URI of the file or directory before renaming.
- `newUri`: The URI after renaming.

### `list`
<decl method><pre>
(params: {
  uri: string,
}): Promise&lt;Array>
</pre></decl>

Lists all items (files or directories) under the specified directory. `params` fields:
- `uri`: The URI of the directory to list. Listing files inside the application resource package is not supported.

The parameter of the `Promise` is an array containing file information, formatted as follows:
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
You cannot list files within the application resource package, so direct usages of paths such as `await file.list({ uri: "/assets/images" })` are invalid. In fact, you should use various [`internal`](/framework/application/resource.md#internal) URI schemes.
:::

### `access`
<decl method><pre>
(params: {
  uri: string
}): Promise&lt;boolean>
</pre></decl>

Checks whether a file exists. `params` fields:
- `uri`: The URI of the file to check.

### `mkdir`
<decl method><pre>
(params: {
  uri: string,
  recursive?: boolean
}): Promise&lt;void>
</pre></decl>

Creates a directory. `params` fields:
- `uri`: The URI of the directory to be created.
- `recursive`: Whether to create recursively (create parent directories first if they do not exist), defaulting to `false`.

### `remove`
<decl method><pre>
(params: {
  uri: string,
  recursive?: boolean
}): Promise&lt;void>
</pre></decl>

Deletes a directory or file. `params` fields:
- `uri`: The URI of the directory to be deleted.
- `recursive`: Whether to delete recursively, defaulting to `false`. When not recursive, it can only delete files or empty directories.

### `stat`
<decl method><pre>
(options: {
  uri: string
}): Promise&lt;{size: number}>
</pre></decl>

Gets the attribute information of a file. The fields of `options` are described below:
- `uri`: The URI of the file whose attributes are to be retrieved.

`stat()` asynchronously returns an object containing the following file attributes:
- `size`: The size of the file in bytes.

## Common Pitfalls and Recommendations

The following examples are based on typical problems of "callback-style" code, demonstrating why they easily fail or become difficult to maintain in file I/O, and providing equivalent rewrites using Promise/`await`.

### Asynchronous File Operations

All APIs in the `@system.file` module are **asynchronous operations**. This means that when you call a file operation function, it will **return immediately** without waiting for the actual I/O operation to complete. File read and write operations take place in the background, and you will be notified of the result via a Promise once the operation completes.

::: danger Must Read for Beginners
If you are not familiar with asynchronous programming, please read this section carefully. **Ignoring the return value of an asynchronous operation** or **not waiting for the Promise to complete** will lead to severe program bugs. These bugs may not manifest in the simulator, but they will cause data loss or program errors on real devices.
:::

#### What is an Asynchronous Operation?

In synchronous programming, code executes sequentially, and each line of code waits for the previous one to finish before executing:

```js
// Synchronous code example (pseudo-code, the file API does not provide synchronous versions): blocks and waits for file reading
const text = file.readTextSync({ uri: 'internal://files/data.txt' });
console.log(text); // Will definitely output the file content
console.log('Read complete');
```

However, in asynchronous programming, I/O operations do not block code execution. When you call an asynchronous function, it immediately returns a Promise object while the actual file operation runs in the background:

```js
// Error: Ignoring the Promise, not waiting for the operation to complete (returns immediately)
file.readText({ uri: 'internal://files/data.txt' });
console.log('This line of code executes immediately, at which point the file may not have been fully read yet!');

// Correct: Using await to wait for the operation to complete
const text = await file.readText({ uri: 'internal://files/data.txt' });
console.log(text); // At this point the file has been read, and it is safe to use
console.log('Read complete');
```

#### Why Must You Use `await`?

Failing to use `await` to wait for asynchronous operations to complete leads to the following severe issues.

Data being used before it is ready:
```js
// Incorrect example: Ignoring the return value
function loadConfig() {
  let config = null;
  file.readText({ uri: 'internal://files/config.json' })
    .then(text => config = JSON.parse(text)); // This callback function will execute at some point in the future
  // config is still null here because file reading is not finished yet!
  console.log(config.theme); // Error: Trying to access null.theme will crash
  return config; // Returns null
}

// Correct example: Waiting for data to be ready
async function loadConfig() {
  const text = await file.readText({ uri: 'internal://files/config.json' });
  const config = JSON.parse(text);
  console.log(config.theme); // Correct: File is read, safe to access
  return config; // Returns the actual configuration object
}
```

Confused operation order:
```js
// Incorrect example: Not waiting for the write to complete
async function saveAndLoad() {
  // Write new data, but do not wait for completion
  file.writeText({ uri: 'internal://files/score.txt', text: '100' });
  
  // Read immediately; at this point the write might not be finished, and you might read old data!
  const score = await file.readText({ uri: 'internal://files/score.txt' });
  console.log(score); // Might output an old value instead of '100'
}

// Correct example: Wait for the write to complete before reading
async function saveAndLoad() {
  // Use await to wait for the write to finish
  await file.writeText({ uri: 'internal://files/score.txt', text: '100' });
  
  // Now read, ensuring you get the freshly written data
  const score = await file.readText({ uri: 'internal://files/score.txt' });
  console.log(score); // Outputs '100'
}
```

Race conditions and data corruption:

```js
// Incorrect example: Concurrent writes to the same file multiple times
async function appendLog(message) {
  const log = await file.readText({ uri: 'internal://files/log.txt' });
  // Proceed without using await to wait for the write to complete
  file.writeText({ uri: 'internal://files/log.txt', text: log + message + '\n' });
}

// Concurrent calls: without awaiting appendLog
appendLog('Event A'); // Read -> Write A
appendLog('Event B'); // Read -> Write B
// Result: Both reads might read the same old content, and the later write will overwrite the earlier one, causing 'Event A' to be lost

// Correct example: Wait for each write to complete
async function appendLog(message) {
  const log = await file.readText({ uri: 'internal://files/log.txt' });
  await file.writeText({ uri: 'internal://files/log.txt', text: log + message + '\n' });
}

// Sequential calls
await appendLog('Event A'); // Complete Read -> Write -> Finish
await appendLog('Event B'); // Complete Read -> Write -> Finish
// Result: Both events are correctly recorded
```

#### Simulator Pitfalls

::: warning The Simulator Cannot Expose All Asynchronous Issues
In development simulators, due to the computer's extremely fast I/O speed, file operations complete almost instantaneously. Therefore, even if code does not correctly use `await`, it may appear to "work properly" in the simulator.
:::

File system I/O on real embedded devices has the following limitations:
- Flash storage read and write speeds are slower;
- File system caching capabilities are weak, and reading/writing files usually accesses storage media directly;
- System resources are limited, and I/O operations are queued and delayed.

Code without `await` **will almost certainly fail** on real devices! Do not ignore asynchronous programming practices just because tests pass in the simulator.

#### Rules for Correctly Using `async/await`

1. Any function that calls file APIs should be declared as `async`:
   ```js
   async function saveData(data) {
     await file.writeText({ uri: 'internal://files/data.txt', text: data });
   }
   ```
2. Add the `await` keyword before all file operations:
   ```js
   const content = await file.readText({ uri: 'internal://files/data.txt' });
   ```
3. Use `try/catch` to handle potential errors:
   ```js
   try {
     await file.writeText({ uri: 'internal://files/data.txt', text: 'hello' });
   } catch (err) {
     console.error('Write failed:', err);
   }
   ```
4. Operations that need to be executed sequentially must be `await`ed in order:
   ```js
   // Correct: Write first, then read to verify
   await file.writeText({ uri: 'internal://files/data.txt', text: 'test' });
   const verify = await file.readText({ uri: 'internal://files/data.txt' });
   console.log(verify === 'test' ? 'Verification successful' : 'Verification failed');
   ```
5. Unrelated operations can be executed in parallel, but you must wait for all of them to complete:
   ```js
   // Correct: Read multiple files in parallel, but wait for all to complete
   const [file1, file2, file3] = await Promise.all([
     file.readText({ uri: 'internal://files/a.txt' }),
     file.readText({ uri: 'internal://files/b.txt' }),
     file.readText({ uri: 'internal://files/c.txt' })
   ]);
   ```

#### Complete Example: User Configuration Management

```js
import file from '@system.file'

const CONFIG_URI = 'internal://files/user-config.json';

// Correct asynchronous configuration management
class ConfigManager {
  async load() {
    try {
      const text = await file.readText({ uri: CONFIG_URI });
      return JSON.parse(text);
    } catch (err) {
      // File does not exist or format error, return default configuration
      console.warn('Failed to load config, using default values:', err.message);
      return { theme: 'dark', language: 'zh-CN' };
    }
  }

  async save(config) {
    try {
      const text = JSON.stringify(config, null, 2);
      await file.writeText({ uri: CONFIG_URI, text });
      console.log('Configuration saved');
    } catch (err) {
      console.error('Failed to save configuration:', err.message);
      throw err; // Re-throw to let the caller know saving failed
    }
  }

  async update(changes) {
    // Complete read -> modify -> save flow
    const config = await this.load();
    Object.assign(config, changes);
    await this.save(config);
    return config;
  }
}

// Usage example
async function main() {
  const manager = new ConfigManager();
  // Load configuration
  const config = await manager.load();
  console.log('Current theme:', config.theme);
  // Update configuration
  await manager.update({ theme: 'light' });
  console.log('Theme updated');
}

// Note: main itself is also asynchronous and needs to be called correctly
main().catch(err => {
  console.error('Program execution error:', err);
});
```

#### Summary

- All `@system.file` APIs are asynchronous and must use `await` to wait for completion.
- Failing to use `await` leads to severe issues such as unprepared data, out-of-order operations, lost errors, and data corruption.
- Passing simulator tests does not mean the code is correct; I/O is slower on real devices and issues will surface.
- Using `async/await` + `try/catch` is the correct and cleanest approach.
- Never ignore the return value of a Promise.

### Callback Pitfalls

#### Callback Order Illusion and Race Condition Overwriting

This scenario involves a sequence of read-modify-write operations on a set of files. Here is problematic code using callback parameters:
```js
// Expected to increment a counter file by +1, but two concurrent calls might overwrite each other
function increment(uri, done) {
  file.readText({
    uri,
    success(text) {
      const n = Number(text || '0') + 1;
      console.log(`read ${text}, write ${n}`);
      // Nesting write file operation inside readText() success callback
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

// Create counter file first, then trigger two concurrent +1 increments
file.writeText({
  uri: 'internal://files/counter',
  text: '0',
  success() {
    // Trigger two increments concurrently without any synchronization
    increment('internal://files/counter');
    increment('internal://files/counter');
  }
})
```
After running this script, you may only see two `read 0, write 1` logs, and the final `counter` file content will be `1` instead of the expected `2`. The failure mechanism is: both reads fetch the exact same old value, and the later write overwrites the earlier one, resulting in a single +1 increment.

::: note
The script above looks extremely complex and makes it hard to correctly pass the `done` callback function, easily leading to incorrect implementations. In fact, when rewritten using `async/await`, the code becomes very concise and easy to understand.
:::

A complex technique is to use mutual exclusion + serialization, which completely preserves the original concurrent `increment` semantics while guaranteeing atomicity for the entire read-file + increment operation:
```js
// Key-based mutual exclusion execution using Promise chains
const lock = new Map();

/**
 * Serially execute asynchronous tasks for the same key. This is a utility function.
 * @param {string} key
 * @param {() => Promise<any>} fn
 * @returns {Promise<any>} Returns the result of fn
 */
function withLock(key, fn) {
  // Get the previous "tail" for this key (or a resolved Promise if none)
  const prev = lock.get(key) || Promise.resolve();
  // Even if prev fails, we must continue the subsequent queue, so .catch(() => {}) first
  const p = prev.catch(() => {}).then(async () => {
    try {
      return await fn(); // The actual task only runs when its turn comes
    } finally {
      // If we are still the current tail, it means no new tasks came in, so we can clean up
      if (lock.get(key) === p) lock.delete(key);
    }
  });
  lock.set(key, p); // Hang the new tail
  return p;
}

// Now, the actual I/O inside increment is serialized by withLock:
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
  // Trigger two increments concurrently, again without any synchronization
  increment('internal://files/counter');
  increment('internal://files/counter');
});
```
After running this script, the `counter` file content will definitely be `2`, and the log order will strictly be `read 0, write 1` → `read 1, write 2`.

However, such code looks quite complex. The simplest approach is to directly call `await increment()` (which manifests as `await` propagation):
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
  // Use await to wait for increment, ensuring order
  await increment('internal://files/counter');
  await increment('internal://files/counter');
})
```

#### Callback Nesting and Resource Leaks

The following example demonstrates resource leaks and logic errors caused by multi-level nesting and too many branches in callback-style code:

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
            // Some branch forgets stopBusyIndicator() or cb()
          }
        });
        // This is also wrong, because writeText() is asynchronous and may not have completed yet
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

Due to deep callback nesting levels, `stopBusyIndicator()` and `cb()` are prone to being missed or misused:
- Omitting cleanup logic causes the "busy indicator" to never stop, or the caller never receives a callback;
- Prematurely calling cleanup logic makes the caller think the write has already completed.

Recommended writing style (structured cleanup):

```js
async function exportReport(uri) {
  startBusyIndicator();
  try {
    const t = await file.readText({ uri });
    const out = await transform(t);
    await file.writeText({ uri: `${uri}.bak`, text: out });
  } finally {
    stopBusyIndicator(); // Always called after file I/O completes (or throws an error)
  }
}
```

#### Mixing `await` and Callbacks Leading to Style Switching (`await` Becomes Ineffective)

Callback handler functions do not return Promise objects, rendering `await` ineffective:

```js
// Because the complete callback is passed, this call enables callback style and does not return a Promise
await file.writeText({
  uri: 'internal://files/a.txt',
  text: 'x',
  complete() {}, // Do not pass success/fail/complete parameter fields
});
// The line above will not truly wait for the write to finish, and subsequent code may execute prematurely
```

Recommended writing style:

```js
// Do not pass success/fail/complete when using await
await file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
```

### Best Practices

#### Clear Ordering and Error Handling

```js
import file from '@system.file'

export async function updateConfig(uri, patch) {
  try {
    const text = await file.readText({ uri });
    const json = JSON.parse(text || '{}');
    Object.assign(json, patch);
    await file.writeText({ uri, text: JSON.stringify(json, null, 2) });
  } catch (err) {
    // Handle/log errors uniformly; do not swallow them
    console.error('updateConfig failed:', uri, err);
    throw err;
  }
}
```

The key points are using `await` to clarify sequential timing and using `try/catch` to ensure errors are noticed and propagated. If errors are completely unhandled, the runtime will log exception anomalies and interrupt the entire call chain.

#### Avoiding TOCTTOU (Time-of-Check to Time-of-Use Race Conditions)

Do not call `access()` followed by `write*()` while relying on the state between them remaining unchanged. For example, code like this:

```js
file.access({
  uri: 'internal://files/a.txt',
  success(exists) {
    if (exists) {
      file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
    } else {
      // If the file does not exist, mkdir first then write file
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

The recommended approach is to attempt writing directly; the runtime will automatically create parent directories:
```js
async function safeWriteText(uri, text) {
  try {
    await file.writeText({ uri, text });
  } catch (e) {
    // Errors should be handled here, and there is no need to mkdir before writing files
  }
}
```

#### Partial Writes and Crash Interruptions

On MCU devices, system exceptions usually trigger a direct reset, and applications do not continue executing in a "semi-crashed" state. Even if an application is killed, file write operations that have already been committed will not be interrupted (though they might not execute at all), so there is usually no need to worry about "half-written files":
```js
// Direct overwrite write; power interruption / system crash may leave a half-written file
file.writeText({ uri: '/data/config.json', text: bigJson });
```

For critical configuration file updates, you can use the "temporary file + same-directory rename" pattern to enhance stability:
```js
async function atomicWriteText(uri, text) {
  const tmp = `${uri}.tmp`;
  await file.writeText({ uri: tmp, text });
  await file.rename({ oldUri: tmp, newUri: uri });
}
```