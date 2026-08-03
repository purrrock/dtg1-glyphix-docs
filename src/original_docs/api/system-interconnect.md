# 设备互联

## 导入模块

``` ts
import interconnect from '@system.interconnect'
```

## 接口定义

### `instance` <decl type="(options: {package: string, fingerprint: string}): Connect" method/>

创建 [`Connect`](#connect-接口) 实例

```js
const connect = interconnect.instance({
  package: "com.xxxx.xxx",
  fingerprint: "xxxxx"
})
```

- package: 手机应用的的包名
- fingerprint: 指纹信息，需要与手机应用创建连接时传入的指纹信息一致

## `Connect` 接口

### `onopen` <decl type="?: () => void" set />

用于指定连接打开时的回调

```js
connect.onopen = () => {
  console.info("onopen")
}
```

### `onclose` <decl type="?: () => void" set />

用于指定连接关闭时回调

```js
connect.onclose = () => {
  console.info("onclose")
}
```

### `onerror` <decl type="?: () => void" set />

用于指定连接失败后的回调

```js
connect.onerror = (data: any) => {
  console.info("onerror", data)
}
```

### `onmessage` <decl type="?: () => " set />

用于指定接收手机 App 端数据的回调

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

发送数据到手机 App 端

```js
connect.send({
  data: {
    name: "zhangsan"
  }
})
```
