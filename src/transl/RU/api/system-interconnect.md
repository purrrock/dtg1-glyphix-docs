# Взаимодействие устройств (设备互联)

## Импорт модуля

``` ts
import interconnect from '@system.interconnect'
```

## Определение интерфейсов

### `instance` <decl type="(options: {package: string, fingerprint: string}): Connect" method/>

Создает экземпляр [`Connect`](#connect-интерфейс).

```js
const connect = interconnect.instance({
  package: "com.xxxx.xxx",
  fingerprint: "xxxxx"
})
```

- package: Имя пакета мобильного приложения.
- fingerprint: Информация об отпечатке, которая должна совпадать с информацией об отпечатке, переданной при создании соединения мобильным приложением.

## Интерфейс `Connect`

### `onopen` <decl type="?: () => void" set />

Используется для указания回调 (обратного вызова) при открытии соединения.

```js
connect.onopen = () => {
  console.info("onopen")
}
```

### `onclose` <decl type="?: () => void" set />

Используется для указания回调 при закрытии соединения.

```js
connect.onclose = () => {
  console.info("onclose")
}
```

### `onerror` <decl type="?: () => void" set />

Используется для указания回调 при сбое соединения.

```js
connect.onerror = (data: any) => {
  console.info("onerror", data)
}
```

### `onmessage` <decl type="?: () => " set />

Используется для указания回调 при получении данных от мобильного приложения.

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

Отправка данных в мобильное приложение.

```js
connect.send({
  data: {
    name: "zhangsan"
  }
})
```