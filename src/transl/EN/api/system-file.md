# File system operations

This module provides a Promise-style file system operation API. Compared with callback style, Promise style can avoid callback hell and reduce code complexity.

::: warning
Since the callback file API is prone to pitfalls in timing, concurrency and error handling, it is strongly recommended to use [Promise/`await` API](./README.md#Quick Application Asynchronous Interface); for detailed suggestions, please refer to [Common Traps and Suggestions](#Common Traps and Suggestions).

The APIs in `@system.file` are all [asynchronous file operations](#asynchronous file operations), which are essentially different from synchronous IO access. Be sure to understand the basic concepts of asynchronous programming and be familiar with the use of Promise and `async/await`.
:::

## Import module

``` js
import file from '@system.file'
```

## Instructions for use

### Error code

The error code returned means:
- `202`: Parameter error;
- `300`: IO operation failed;
- `400`: Insufficient permissions;

## Interface definition

### `readText`
<decl method><pre>
(params: {
  uri: string
}): Promise&lt;string>
</pre></decl>

Read the contents of a text file. `params` parameter field description:
- `uri`: URI of the file to be read.

### `writeText`
<decl method><pre>
(params: {
  uri: string,
  text: string,
  append?: boolean
}): Promise&lt;void>
</pre></decl>

Writes text to a file, or creates a new file if it does not exist. This function also automatically creates the parent directory. `params` parameter field:
- `uri`: URI of the file to be written.
- `text`: The text content to be written to the file.
- `append`: The value is `true` to append data to the end of the file, the value is `false` to overwrite the original content. Default `false`.

### `read`
<decl method><pre>
(params: {
  uri: string,
  position?: number,
  length?: number
}): Promise&lt;ArrayBuffer>
</pre></decl>

Read the contents of the file into an `ArrayBuffer` object. `params` parameter field:
- `uri`: URI of the file to be read.
- `position`: the offset of the file reading position, the default is $0$.
- `length`: The number of bytes expected to be read. If not specified, it will be read to the end of the file.

### `write`
<decl method><pre>
(params: {
  uri: string,
  data: ArrayBuffer,
  position?: number,
  append?: boolean
}): Promise&lt;void>
</pre></decl>

Writes the bytes in the `ArrayBuffer` to a file, or creates a new file if it does not exist. This function also automatically creates the parent directory.

`params` parameter field description:
- `uri`: URI of the file to be written.
- `data`: data to be written.
- `position`: the offset of the file writing position, default is $0$.
- `append`: A value of `true` will append the data to the end of the file and ignore the `position` parameter.

### `copy`
<decl method><pre>
(params: {
  srcUri: string,
  dstUri: string
}): Promise&lt;void>
</pre></decl>

Copy the source file to the specified location and the target directory will be automatically created. `params` parameter field:
- `srcUri`: URI of the source file.
- `dstUri`: URI of the target file.

### `rename`
<decl method><pre>
(params: {
  oldUri: string,
  newUri: string
}): Promise&lt;void>
</pre></decl>

Renaming a file or directory will automatically create the target directory. `params` parameter field:
- `oldUri`: URI of the file or directory before renaming.
- `newUri`: URI after renaming.

### `list`
<decl method><pre>
(params: {
  uri: string,
}): Promise&lt;Array>
</pre></decl>

List all items (files or directories) in the specified directory. `params` parameter field:
- `uri`: Directory URI with enumeration. Files in the application resource package do not support enumeration.

The parameter of `Promise` is an array containing file information, in the form
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
You cannot enumerate files in the application resource package, so `await file.list({ uri: "/assets/images" })` and other methods that directly use [path](/framework/application/resource.md#uri-and path) are invalid. In fact, various [`internal`](/framework/application/resource.md#internal) URI protocols should be used.
:::

### `access`
<decl method><pre>
(params: {
  uri: string
}): Promise&lt;boolean>
</pre></decl>

Check if a file exists. `params` parameter field:
- `uri`: URI of the file to be detected.

### `mkdir`
<decl method><pre>
(params: {
  uri: string,
  recursive?: boolean
}): Promise&lt;void>
</pre></decl>

Create a directory. `params` parameter field:
- `uri`: URI of the directory to be created.
- `recursive`: Whether to create recursively (if the parent directory does not exist, create the parent directory first), the default is `false`.

### `remove`
<decl method><pre>
(params: {
  uri: string,
  recursive?: boolean
}): Promise&lt;void>
</pre></decl>

Delete a directory or file. `params` parameter field:
- `uri`: URI of the directory to be created.
- `recursive`: Whether to delete recursively, the default is `false`. Without recursive deletion, only files or empty directories can be deleted.

### `stat`
<decl method><pre>
(options: {
  uri: string
}): Promise&lt;{size: number}>
</pre></decl>

Get the attribute information of the file. Each field of the `options` parameter is described as follows:
- `uri`: the file URI of the attribute to be obtained.

`stat()` returns an object asynchronously containing the following file attributes:
- `size`: The size of the file, in bytes.

## Common pitfalls and suggestions

The following examples are all based on the typical problems of "callback-style" writing, showing why it is easily invalid or difficult to maintain in file IO, and provide equivalent rewriting of Promise/`await`.

### Asynchronous file operations

All APIs in the `@system.file` module are **asynchronous operations**. This means that when you call a file operation function, the function returns immediately without waiting for the actual I/O operation to complete. The read and write operations of the file will be performed in the background, and you will be notified of the result through Promise after the operation is completed.

:::danger A must-read for newbies
If you are new to asynchronous programming, be sure to read this section carefully. **Ignoring the return value of an asynchronous operation** or **Not waiting for a Promise to complete** can lead to serious program errors that may not manifest in the simulator, but can result in data loss or program errors on a real device.
:::

#### What is an asynchronous operation?

In synchronous programming, code is executed sequentially, and each line of code is executed before the next line is executed:

```js
// Synchronous code example (pseudocode, file API does not provide a synchronous version): blocking waiting for file reading
const text = file.readTextSync({ uri: 'internal://files/data.txt' });
console.log(text); // The file content will definitely be output
console.log('Reading completed');
```

But in asynchronous programming, I/O operations do not block code execution. When you call an asynchronous function, it returns a Promise object immediately, and the actual file operations occur in the background:

```js
// Error: Ignore Promise, do not wait for operation to complete (call returns immediately)
file.readText({ uri: 'internal://files/data.txt' });
console.log('This line of code will be executed immediately, and the file may not be finished reading at this time!');

// Correct: use await to wait for the operation to complete
const text = await file.readText({ uri: 'internal://files/data.txt' });
console.log(text); // At this point the file has been read and can be used safely
console.log('Reading completed');
```

#### Why must we use await?

Not using `await` to wait for an asynchronous operation to complete can lead to the following serious problems.

Data is used before it is ready:
```js
// Error example: ignore return value
function loadConfig() {
  let config = null;
  file.readText({ uri: 'internal://files/config.json' })
    .then(text => config = JSON.parse(text)); // This callback function will be executed at some point in the future
  // Here config is still null because the file reading has not been completed yet!
  console.log(config.theme); // Error: Trying to access null.theme will crash
  return config; // return null
}

// Correct example: wait for data to be ready
async function loadConfig() {
  const text = await file.readText({ uri: 'internal://files/config.json' });
  const config = JSON.parse(text);
  console.log(config.theme); // Correct: the file has been read and is safe to access
  return config; // Return the actual configuration object
}
```

The order of operations is confusing:
```js
// Error example: Not waiting for write to complete
async function saveAndLoad() {
  //Write new data, but don't wait for completion
  file.writeText({ uri: 'internal://files/score.txt', text: '100' });

  // Read immediately. The writing may not be completed at this time, and the old data may be read!
  const score = await file.readText({ uri: 'internal://files/score.txt' });
  console.log(score); // Might output the old value instead of '100'
}

// Correct example: wait for writing to complete before reading
async function saveAndLoad() {
  // Use await to wait for writing to complete
  await file.writeText({ uri: 'internal://files/score.txt', text: '100' });

  // Now read, make sure you read the data just written
  const score = await file.readText({ uri: 'internal://files/score.txt' });
  console.log(score); // Output '100'
}
```

Resource contention and data corruption:

```js
//Error example: multiple concurrent writes to the same file
async function appendLog(message) {
  const log = await file.readText({ uri: 'internal://files/log.txt' });
  // No need to wait for writing to complete, continue execution
  file.writeText({ uri: 'internal://files/log.txt', text: log + message + '\n' });
}

// Concurrent calls: no await appendLog
appendLog('Event A'); // Read -> Write A
appendLog('Event B'); // Read -> Write B
// Result: Two reads may read the same old content, and the later write will overwrite the previous one, causing 'event A' to be lost

// Correct example: wait for each write to complete
async function appendLog(message) {
  const log = await file.readText({ uri: 'internal://files/log.txt' });
  await file.writeText({ uri: 'internal://files/log.txt', text: log + message + '\n' });
}

// serial call
await appendLog('Event A'); // Complete read -> write -> complete
await appendLog('Event B'); // Complete read -> write -> complete
// Result: Both events were logged correctly
```

#### Emulator trap

::: warning The simulator cannot expose all asynchronous issues
In a development simulator, file operations are almost instantaneous due to the extremely fast I/O speed of the computer. Therefore, code may appear to "just work" in the simulator even if it does not use `await` correctly.
:::

File system I/O on real embedded devices has the following limitations:
- The read and write speed of Flash memory is slow;
- The file system cache capability is weak, and reading and writing files usually directly accesses the storage medium;
- System resources are limited and I/O operations will be queued and delayed.

Code that does not use `await` will almost certainly break on a real device! Don't ignore asynchronous programming conventions just because the simulator tests pass.

#### Rules for correct use of async/await

1. Any function calling the file API should be declared as `async`:
   ```js
   async function saveData(data) {
     await file.writeText({ uri: 'internal://files/data.txt', text: data });
   }
   ```
2. Add the `await` keyword before all file operations:
   ```js
   const content = await file.readText({ uri: 'internal://files/data.txt' });
   ```
3. Use `try/catch` to handle possible errors:
   ```js
   try {
     await file.writeText({ uri: 'internal://files/data.txt', text: 'hello' });
   } catch (err) {
     console.error('Writing failed:', err);
   }
   ```
4. Operations that need to be performed sequentially must `await` in order:
   ```js
   // Correct: write first, then read and verify
   await file.writeText({ uri: 'internal://files/data.txt', text: 'test' });
   const verify = await file.readText({ uri: 'internal://files/data.txt' });
   console.log(verify === 'test' ? 'Verification successful' : 'Verification failed');
   ```
5. Irrelevant operations can be executed in parallel, but wait for all to complete:
   ```js
   // Correct: read multiple files in parallel, but wait for them all to complete
   const [file1, file2, file3] = await Promise.all([
     file.readText({ uri: 'internal://files/a.txt' }),
     file.readText({ uri: 'internal://files/b.txt' }),
     file.readText({ uri: 'internal://files/c.txt' })
   ]);
   ```

#### Complete example: User configuration management

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
      //The file does not exist or has a wrong format, return to the default configuration
      console.warn('Failed to load configuration, use default value:', err.message);
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
      throw err; // Rethrow to let the caller know the save failed
    }
  }

  async update(changes) {
    // Read -> Modify -> Save the complete process
    const config = await this.load();
    Object.assign(config, changes);
    await this.save(config);
    return config;
  }
}

// Usage example
async function main() {
  const manager = new ConfigManager();
  //Load configuration
  const config = await manager.load();
  console.log('Current theme:', config.theme);
  //Update configuration
  await manager.update({ theme: 'light' });
  console.log('Theme has been updated');
}

// Note: main itself is also asynchronous and needs to be called correctly
main().catch(err => {
  console.error('Program execution error:', err);
});
```

#### Summary

- All `@system.file` APIs are asynchronous and must use `await` to wait for completion.
- Not using `await` can lead to serious problems, such as unprepared data, out-of-order operations, lost errors, and data corruption.
- Passing the simulator test does not mean that the code is correct. I/O on the real device is slower and problems will be exposed.
- Using `async/await` + `try/catch` is the correct and most concise way of writing.
- Never ignore the return value of a Promise.

### Callback trap

#### Callback order illusion and race coverage

This type of scenario involves a sequence of operations in which a set of files are read-modified-written. Here is the code in question using callback parameters to trigger the callback style:
```js
// Expect +1 to count file, but two concurrent calls may overwrite each other
function increment(uri, done) {
  file.readText({
    uri,
    success(text) {
      const n = Number(text || '0') + 1;
      console.log(`read ${text}, write ${n}`);
      // Nested file writing operation in readText() success callback
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

//Create the counter file first, and then trigger it twice concurrently +1
file.writeText({
  uri: 'internal://files/counter',
  text: '0',
  success() {
    //Trigger increment twice concurrently, but without any synchronization
    increment('internal://files/counter');
    increment('internal://files/counter');
  }
})
```
After running the script, you may only see two `read 0, write 1` logs, and the final `counter` file content is `1` instead of the expected `2`. The failure mechanism is: both reads read the same old value, and the later write overwrites the first write, resulting in a result of only +1.

::: note
The above script looks very complicated, and it is difficult to pass the `done` callback function correctly, which can easily lead to incorrect implementation. In fact, after rewriting it using `async/await`, the code becomes very concise and easy to understand.
:::

A complex trick is to use mutual exclusion + serialization technology, which can completely retain the original concurrency `increment` semantics and ensure the atomicity of the entire read file + increment count operation:
```js
// Mutually exclusive execution by key based on Promise chain
const lock = new Map();

/**
 * Execute asynchronous tasks for the same key serially. This is a utility function.
 * @param {string} key
 * @param {() => Promise<any>} fn
 * @returns {Promise<any>} returns the result of fn
 */
function withLock(key, fn) {
  // Get the "tail" before the key (if not, use the completed Promise)
  const prev = lock.get(key) || Promise.resolve();
  // Even if prev fails, the subsequent queue must continue, so first .catch(() => {})
  const p = prev.catch(() => {}).then(async () => {
    try {
      return await fn(); // The real task is only executed when it is its turn
    } finally {
      // If you are still the current tail, it means that no new tasks have come in and you can clean it up.
      if (lock.get(key) === p) lock.delete(key);
    }
  });
  lock.set(key, p); // Hang the new tail
  return p;
}

// Now, the actual IO inside the increment is serialized by withLock:
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
  // Trigger increment twice concurrently without any synchronization
  increment('internal://files/counter');
  increment('internal://files/counter');
});
```
After running this script, the content of the `counter` file must be `2`, and the log sequence must be `read 0, write 1` → `read 1, write 2`.

But such code looks very complicated. The simplest way is to call `await increment()` directly (shown as `await` infection):
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
  // Use await to wait for increment to ensure order
  await increment('internal://files/counter');
  await increment('internal://files/counter');
})
```

#### Callback levels and resource leaks

The following example shows resource leaks and logic errors caused by multiple levels of nesting and too many branches in callback writing:

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
            // Some branches forget stopBusyIndicator() or cb()
          }
        });
        // This is also wrong because writeText() is asynchronous and may not have completed yet
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

Because the callback nesting level is too deep, `stopBusyIndicator()` and `cb()` are prone to omission or misuse:
- Missing cleanup logic, causing the "busy indicator" to never stop, or the caller never getting a callback;
- The cleanup logic was called prematurely, causing the caller to mistakenly believe that the write was completed.

Recommended writing method (structured cleaning):

```js
async function exportReport(uri) {
  startBusyIndicator();
  try {
    const t = await file.readText({ uri });
    const out = await transform(t);
    await file.writeText({ uri: `${uri}.bak`, text: out });
  } finally {
    stopBusyIndicator(); // Always called after file IO is completed (or abnormal)
  }
}
```

#### Mixing await and callback leads to style switching (await fails)

Any callback handler function will not return a Promise object, making `await` wait invalid:

```js
// Because the complete callback is passed in, this call will enable the callback style and will not return a Promise
await file.writeText({
  uri: 'internal://files/a.txt',
  text: 'x',
  complete() {}, // Do not pass in the success/fail/complete parameter field
});
//The above line will not actually wait for the writing to complete, and subsequent code may be executed in advance
```

Recommended writing method:

```js
// Do not pass in success/fail/complete when using await
await file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
```

### Best Practices

#### Clear order and error handling

```js
import file from '@system.file'

export async function updateConfig(uri, patch) {
  try {
    const text = await file.readText({ uri });
    const json = JSON.parse(text || '{}');
    Object.assign(json, patch);
    await file.writeText({ uri, text: JSON.stringify(json, null, 2) });
  } catch (err) {
    // Handle/record errors uniformly, don't swallow them
    console.error('updateConfig failed:', uri, err);
    throw err;
  }
}
```

The key point is to use `await` to clarify the serial timing; use `try/catch` to ensure that errors are sensed and thrown up. If the error is not handled at all, the runtime will log the exception and interrupt the entire call chain.

#### Avoid TOCTTOU (check-use race conditions)

Don't do `access()` first and then `write*()` and then rely on the state between the two to remain unchanged. For example this code:

```js
file.access({
  uri: 'internal://files/a.txt',
  success(exists) {
    if (exists) {
      file.writeText({ uri: 'internal://files/a.txt', text: 'x' });
    } else {
      // If the file does not exist, mkdir first and then write the file
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

The recommended way to write is to directly try to write, and the parent directory will be automatically created when running:
```js
async function safeWriteText(uri, text) {
  try {
    await file.writeText({ uri, text });
  } catch (e) {
    // Errors should be handled here and there is no need to write files after mkdir
  }
}
```

#### Half-write and crash interrupt

On MCU devices, system exceptions are usually directly reset and the application will not continue executing in a "semi-crash" state. Even if the app is killed, already committed file writes will not be interrupted (but may not be executed at all), so you generally don't need to worry about the "half-written file" problem:
```js
// Direct overwrite, which may leave half-written files in case of power interruption/system crash
file.writeText({ uri: '/data/config.json', text: bigJson });
```

For critical configuration file updates, you can use the "temporary file + same directory rename" mode to enhance stability:
```js
async function atomicWriteText(uri, text) {
  const tmp = `${uri}.tmp`;
  await file.writeText({ uri: tmp, text });
  await file.rename({ oldUri: tmp, newUri: uri });
}
```
