# Device interconnection

## Import module

``` ts
import interconnect from '@system.interconnect'
```

## Interface definition

### `instance` <decl type="(options: {package: string, fingerprint: string}): Connect" method/>

Create a [`Connect`](#connect-interface) instance

```js
const connect = interconnect.instance({
  package: "com.xxxx.xxx",
  fingerprint: "xxxxx"
})
```

- package: the package name of the mobile application
- fingerprint: fingerprint information, which needs to be consistent with the fingerprint information passed in when the mobile application creates a connection.

## `Connect` interface

### `onopen` <decl type="?: () => void" set />

Used to specify a callback when the connection is opened

```js
connect.onopen = () => {
  console.info("onopen")
}
```

### `onclose` <decl type="?: () => void" set />

Used to specify a callback when the connection is closed

```js
connect.onclose = () => {
  console.info("onclose")
}
```

### `onerror` <decl type="?: () => void" set />

Used to specify a callback after a connection failure

```js
connect.onerror = (data: any) => {
  console.info("onerror", data)
}
```

### `onmessage` <decl type="?: () => " set />

Used to specify the callback for receiving data from the mobile app

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

Send data to mobile app

```js
connect.send({
  data: {
    name: "zhangsan"
  }
})
```
