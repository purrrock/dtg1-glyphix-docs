# Device Interconnection

## Import Module

``` ts
import interconnect from '@system.interconnect'
```

## Interface Definition

### `instance` <decl type="(options: {package: string, fingerprint: string}): Connect" method/>

Creates a [`Connect`](#connect-interface) instance.

```js
const connect = interconnect.instance({
  package: "com.xxxx.xxx",
  fingerprint: "xxxxx"
})
```

- package: The package name of the mobile application.
- fingerprint: Fingerprint information, which must match the fingerprint information passed when creating the connection in the mobile application.

## `Connect` Interface

### `onopen` <decl type="?: () => void" set />

Used to specify the callback when the connection is opened.

```js
connect.onopen = () => {
  console.info("onopen")
}
```

### `onclose` <decl type="?: () => void" set />

Used to specify the callback when the connection is closed.

```js
connect.onclose = () => {
  console.info("onclose")
}
```

### `onerror` <decl type="?: () => void" set />

Used to specify the callback after a connection failure.

```js
connect.onerror = (data: any) => {
  console.info("onerror", data)
}
```

### `onmessage` <decl type="?: () => " set />

Used to specify the callback for receiving data from the mobile App side.

```js
connect.onmessage = (msg => {
  if (msg.isFileType) {
    this.msg = "recv a file " + msg.fileUri
  } else {
    this.msg = "recv a text message " + msg.data
  }
})
```

### `send` <decl type="(options: {data: any}): Promise<any>" method />

Sends data to the mobile App side.

```js
connect.send({
  data: {
    name: "zhangsan"
  }
})
```