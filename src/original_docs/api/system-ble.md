# 低功耗蓝牙模块

本模块提供了基于低功耗蓝牙（Bluetooth Low Energy，BLE）技术的蓝牙能力，支持发起BLE扫描、以及基于通用属性协议（Generic Attribute Profile，GATT）的连接和传输数据（目前仅支持创建 GattClient，暂不支持创建 GattServer）。

::: warning
`@system.bluetooth.ble` 中的 API 大部分都是[Promise异步操作](#Promise异步操作)，这和同步的 IO 访问有本质区别。请务必理解异步编程的基本概念，并且熟悉 Promise 和 `async/await` 的用法。
:::

## 导入模块

``` js
import ble from '@system.bluetooth.ble'
```

## 权限

::: tip
使用该模块应用需要声明权限：watch.permission.BLUETOOTH 
:::

## ble接口定义

### `ResultCode`

Promise中返回的结果枚举

- `0`：成功；
- `1`：低功耗蓝牙未开启；
- `2`：参数错误；
- `3`：低功耗蓝牙开启失败；
- `4`：没有可用的蓝牙适配器；
- `5`：连接失败；
- `6`：断开连接失败；
- `7`：暂不支持设置此属性；
- `8`：未知错误；

### `startBLEScan`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

启动扫描，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

下面是一个启动扫描的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    async scanStart() {
        // 启动扫描
        await ble.startBLEScan().then(async (result) => {
            if (result == 0) {
                console.dir('startBLEScan success')
            } else {
                console.dir('startBLEScan failed' + result)
            }
        }).catch((error) => {
            console.dir('startBLEScan error:' + JSON.stringify(error))
        })
    },
}
```

### `stopBLEScan`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

停止扫描，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

下面是一个停止扫描的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    async scanStop() {
        // 停止扫描
        await ble.stopBLEScan().then(async (result) => {
            if (result == 0) {
                console.dir('stopBLEScan success')
            } else {
                console.dir('stopBLEScan failed' + result)
            }
        }).catch((error) => {
            console.dir('stopBLEScan error:' + JSON.stringify(error))
        })
    },
}
```

### `ScanResult`

此对象用于表示上报的扫描结果，类型签名如下：

```ts
/**
 * 扫描结果对象定义
 */
type ScanResult = {
    deviceId: string; // 设备 ID（例如："AA:BB:CC:DD:EE:FF"）
    rssi: number; // 信号强度，单位 dBm
    data: ArrayBuffer; // 广播报文原始数据
    deviceName: string; // 设备名称（如果有）
    connectable: boolean; // 是否可连接，true 表示可连接
}
```

### `getBLEScanResults`
<decl method><pre>
(): Promise&lt;Array&lt;ScanResult&gt;&gt;
</pre></decl>

查询扫描结果，使用Promise异步回调。该接口异步返回一个包含 [`ScanResult`](#scanresult) 对象的数组（即Array&lt;[`ScanResult`](#scanresult)&gt;）。

::: warning
因为底层的蓝牙适配器是单例的，所以可能会出现多个应用同时操作蓝牙设备的情况。就会存在：应用A 开启扫描一段时间后之后，应用B 再次开启扫描，此时 应用B 监听到的扫描结果是不完整的。为了处理这种情况，建议所有应用开启扫描之后，立即查询一下当前的扫描结果。
:::

下面是一个启动扫描后查询扫描结果的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        scanList: [],
    },
    async scanStart() {
        // 启动扫描
        await ble.startBLEScan().then(async (result) => {
            console.dir('startBLEScan success')
            // 查询扫描结果
            await ble.getBLEScanResults().then((results) => {
                this.scanList = results
            });
        }).catch((error) => {
            console.dir('startBLEScan error:' + JSON.stringify(error))
        })
    },
}
```

### `subscribeScanStatus`
<decl type="(callback: Callback<{ scan: boolean }> => void): number" method/>

订阅扫描状态变化，使用Callback异步回调。当扫描状态改变时，会自动调用 `callback` 回调函数。该接口同步返回一个订阅ID，用于取消订阅。

回调函数参数字段说明：
- `scan`：当前扫描状态。true表示正在扫描，false表示已经停止扫描。

下面是一个订阅扫描状态变化的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        
    },
    scanListener: null,
    async onInit() {
        if (!this.scanListener) {
            this.scanListener = ble.subscribeScanStatus((result) => {
                console.dir('scan status:' + JSON.stringify(result))
            })
        }
    },
}
```

### `unsubscribeScanStatus` <decl type="(subscribeId: number): void" method/>

取消订阅扫描状态变化。参数 `subscribeId` 为 [`subscribeScanStatus`](#subscribescanstatus) 方法返回的订阅ID。

下面是一个取消订阅扫描状态变化的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        
    },
    scanListener: null,
    async onInit() {
        if (!this.scanListener) {
            ble.unsubscribeScanStatus(this.scanListener)
            this.scanListener = null
        }
    },
}
```

### `subscribeBLEDeviceFind`
<decl type="(callback: Callback<ScanResult> => void): number" method/>

订阅扫描结果上报事件，使用Callback异步回调。每当扫描到一个新的设备时，都会自动调用 `callback` 回调函数。该接口同步返回一个订阅ID，用于取消订阅。

::: tip
扫描结果上报为增量模式，既发现一个上报一个，监听此事件后需要用户自己存储扫描结果。
:::

回调函数参数字段说明：
- [`ScanResult`](#scanresult) ：扫描到的新设备对象。

下面是一个订阅扫描结果上报事件的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        scanList: [],
    },
    scanListener: null,
    async onInit() {
        this.scanList = []
        if (!this.scanListener) {
            this.scanListener = ble.subscribeBLEDeviceFind((result) => {
                console.dir('scan found:' + JSON.stringify(result))
                this.scanList.push(result)
            })
        }
    },
}
```

### `unsubscribeBLEDeviceFind` <decl type="(subscribeId: number): void" method/>

取消订阅扫描结果上报事件。参数 `subscribeId` 为 [`subscribeBLEDeviceFind`](#subscribebledevicefind) 方法返回的订阅 ID。

下面是一个取消订阅扫描结果上报事件的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    scanListener: null,
    onHide() {
        if (this.scanListener) {
            ble.unsubscribeBLEDeviceFind(this.scanListener)
            this.scanListener = null
        }
    },
}
```

### `GattClientDevice`

此对象用于表示 Gatt 协议中的 Client 对象，类型签名如下：

```ts
/**
 * GattClientDevice对象类型定义
 */
type GattClientDevice = {
    connect(): Promise<number>,
    disconnect(): Promise<number>,
    close(): Promise<number>,
    getDeviceName(): Promise<string>,
    getServices(): Promise<Array<GattService>>,
    readCharacteristicValue(BLECharacteristic): Promise<BLECharacteristic>,
    writeCharacteristicValue(BLECharacteristic, GattWriteType): Promise<number>,
    readDescriptorValue(BLEDescriptor): Promise<BLEDescriptor>,
    writeDescriptorValue(BLEDescriptor): Promise<number>,
    getRssiValue(): Promise<number>,
    getBLEMtuSize(): Promise<number>,
    setBLEMtuSize(number): Promise<number>,
    setCharacteristicChangeNotification(BLECharacteristic): Promise<number>,
    setCharacteristicChangeIndication(BLECharacteristic): Promise<number>,
    subscribeBLECharacteristicChange(callback: (BLECharacteristic) => void): number,
    unsubscribeBLECharacteristicChange(number): void,
    subscribeBLEConnectionStateChange(callback: (BLEConnectionChangeState) => void): number,
    unsubscribeBLEConnectionStateChange(number): void,
    subscribeBLEMtuChange(callback: (number) => void): number,
    unsubscribeBLEMtuChange(number): void,
}
```

### `createGattClientDevice` <decl type="(deviceId: string): GattClientDevice" method />

创建 [`GattClientDevice`](#gattclientdevice) 实例，表示GATT连接中的client端，该接口同步返回一个 [`GattClientDevice`](#gattclientdevice) 实例。

 - 通过该实例可以操作client端行为，如调用 [`connect`](#connect) 向对端设备发起连接，调用 [`getServices`](#getservices) 获取对端设备支持的所有服务能力。
 - 创建该实例所需要的 deviceId(设备地址) 表示server端设备地址。可以通过 [`startBLEScan`](#startblescan) 接口获取server端设备地址，且需保证server端设备的BLE广播是可连接的。

下面是一个创建 [`GattClientDevice`](#gattclientdevice) 实例的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    create() {
        // 请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
    },
}
```

## GattClientDevice接口定义

### `connect`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

client端主动发起和server蓝牙设备的GATT协议连接，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

 - 使用该类的方法前，需通过 [`createGattClientDevice`](#creategattclientdevice) 方法构造该类的实例。
 - 通过创建不同的该类实例，可以管理多路GATT连接。

下面是一个发起GATT协议连接的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async connect() {
        // 请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
    },
}
```

### `disconnect`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

client端主动断开和server蓝牙设备的GATT协议连接，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

下面是一个断开GATT协议连接的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        address: null,
    },
    gattClient: null,
    async connect() {
        // 请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.address = 'XX:XX:XX:XX:XX:XX'
        this.gattClient = ble.createGattClientDevice(this.address)
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
    },
    async disconnect() { 
        if (this.gattClient) {
            await this.gattClient.disconnect().then((result) => {
                if (result == 0) {
                    console.log('disconnect from' + this.address);
                } else {
                    console.dir('disconnect failed:' + JSON.stringify(result))
                }
            }).catch((error) => {
                console.log('disconnect error:' + JSON.stringify(error));
            });
        }
    },
}
```

### `close`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

关闭client端实例，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

### `getDeviceName`
<decl method><pre>
(): Promise&lt;string&gt;
</pre></decl>

client获取远端蓝牙低功耗设备的名称，使用Promise异步回调。该接口异步返回一个&lt;string&gt;类型的设备名。

下面是一个GATT连接成功后，获取设备名字的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async name() {
        let clientName = 'N/A'
        // 请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
        if (this.gattClient) {
            await this.gattClient.getDeviceName().then((name) => {
                clientName = name || 'N/A'
                console.dir('device name:' + name)
            })
        }
    },
}
```

### `GattService`

此对象用于表示 GATT 服务结构，类型签名如下：

```ts
/**
 * GATT服务结构定义，可包含多个特征值BLECharacteristic和依赖的其他服务。
 */
type GattService = {
    serviceUuid: string; // 服务UUID，标识一个GATT服务。例如：00001888-0000-1000-8000-00805f9b34fb。
    isPrimary: boolean; // 是否是主服务。true表示是主服务，false表示是次要服务。
    characteristics: Array<BLECharacteristic>; // 当前服务包含的特征值列表。
    includeServices: Array<GattService>; // 当前服务依赖的其它服务。
}
```

### `getServices`
<decl method><pre>
(): Promise&lt;Array&lt;GattService&gt;&gt;
</pre></decl>

client端获取蓝牙低功耗设备的所有服务，即服务发现，使用Promise异步回调。该接口异步返回一个包含所有服务的Array&lt;[`GattService`](#gattservice)&gt;类型的数组。

下面是一个GATT连接成功后，获取该设备所有服务的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    async onShow() {
        // 请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
        if (this.gattClient) {
            await this.gattClient.getServices().then((result) => {
                this.services = result;
            }).catch((error) => {
                console.dir('gatt services error: ' + JSON.stringify(error))
            });
        }
    },
}
```

### `GattProperties`

此对象用于表示GATT特征值支持的属性，类型签名如下：

```ts
/**
 * 描述GATT特征值支持的属性。决定了特征值内容和描述符如何被使用和访问。
 */
type GattProperties = {
    write: boolean; // 该特征值是否支持写入操作。true表示支持，且被写入时需要回复对端设备，false表示不支持。
    writeNoResponse: boolean; // 该特征值是否支持写入操作。true表示支持，且被写入时无需回复对端设备，false表示不支持。
    read: boolean; // 该特征值是否支持读取操作。true表示支持，false表示不支持。
    notify: boolean; // 该特征值是否支持主动向对端设备通知特征值内容。true表示支持，且对端设备不需要回复确认，false表示不支持。
    indicate: boolean; // 该特征值是否支持向对端设备指示特征值内容。true表示支持，对端设备需要回复确认，false表示不支持。
    broadcast: boolean; // 该特征值是否支持作为广播内容由server端发送。true表示支持，server端可将特征值内容以ServiceData类型在广播报文中携带，false表示不支持。
    authenticatedSignedWrite: boolean; // 该特征值是否支持签名写入操作，通过对写入内容进行签名校验替代加密流程。true表示支持，false表示不支持。
    extendedProperties: boolean; //该特征值是否存在扩展属性。true表示存在扩展属性，false表示不存在。
}
```

### `BLECharacteristic`

此对象用于表示GATT特征值，类型签名如下：

```ts
/**
 * GATT特征值类型定义, 是服务GattService的核心数据单元
 */
type BLECharacteristic = {
    serviceUuid: string; // 特征值所属的服务UUID, 例如：00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // 特征值UUID, 例如：00002a11-0000-1000-8000-00805f9b34fb
    characteristicValue: ArrayBuffer; // 特征值的数据内容, 读取写数据时使用
    descriptors: Array<BLEDescriptor>; // 特征值包含的描述符列表
    properties: GattProperties; // 特征值支持的属性
    characteristicValueHandle: number; // 特征值的唯一标识句柄。当server端BLE蓝牙设备提供了多个相同UUID特征值时，可以通过此句柄区分不同的特征值
}
```

### `readCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic): Promise&lt;BLECharacteristic&gt;
</pre></decl>

client端从指定的server端特征值读取数据，使用Promise异步回调。该接口异步返回一个 [`BLECharacteristic`](#blecharacteristic) 类型的对象。

 - 该接口需要传入一个 [`BLECharacteristic`](#blecharacteristic) 类型的对象，表示需要读取哪一个特征值

下面是一个GATT连接成功后，从指定的特征值读取数据的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async read() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 调用: connect 接口发起连接
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. 服务发现，获取需要读取的：characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // 测试只尝试读取第一个服务的第一个特征值，如果需要读取其它特征值，请自行修改
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. 读取指定特征值
        if (this.gattClient && this.characteristic) {
            await this.gattClient.readCharacteristicValue(this.characteristic).then((result) => {
                console.log('characteristic read result:' + JSON.stringify(result))
            }).catch((error) => {
                console.dir('characteristic read error:' + JSON.stringify(error))
            })
        }
    },
}
```

### `GattWriteType`

特征值写入方式枚举

- `1`：写入特征值后，对端蓝牙设备需要回复确认。
- `2`：写入特征值后，对端蓝牙设备不需要回复。

### `writeCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic, writeType: GattWriteType): Promise&lt;number&gt;
</pre></decl>

client端向指定的server端特征值写入数据，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

 - 该接口需要传入一个 [`BLECharacteristic`](#blecharacteristic) 类型的对象，表示需要写哪一个特征值
 - 该接口需要传入一个 [`GattWriteType`](#gattwritetype) 枚举值，用来表示数据的写入方式

下面是一个GATT连接成功后，从指定的特征值写入数据的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    
    randomArrayBuffer(length) {
        const randomArray = new Array(length)
        for (let i = 0; i < length; i++) {
            randomArray[i] = Math.floor(Math.random() * 256);
        }
        return new Uint8Array(randomArray).buffer
    },

    async write() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 调用: connect 接口发起连接
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. 服务发现，获取需要操作的：characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // 测试只尝试操作第一个服务的第一个特征值，如果需要操作其它特征值，请自行修改
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. 写指定特征值
        if (this.gattClient && this.characteristic) {
            // 生成指定长度且携带随机数的 ArrayBuffer
            let value = this.randomArrayBuffer(15)
            this.characteristic.characteristicValue = value
            await this.gattClient.writeCharacteristicValue(this.characteristic, 1).then((result) => {
                if (result === 0) {
                    console.log('characteristic write success')
                } else {
                    console.log('characteristic write failed:' + result)
                }
            }).catch((error) => {
                console.dir('characteristic write error:' + JSON.stringify(error))
            })
        }
    },
}
```

### `BLEDescriptor`

此对象表示GATT描述符，其类型定义如下：

```ts
/**
 * GATT描述符类型定义, 是特征值BLECharacteristic的数据单元，用于描述特征值的附加信息和属性
 */
type BLEDescriptor = {
    serviceUuid: string; // 特征值所属的服务UUID, 例如：00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // 特征值UUID, 例如：00002a11-0000-1000-8000-00805f9b34fb
    descriptorUuid: string; // 描述符UUID, 例如：00002902-0000-1000-8000-00805f9b34fb
    descriptorValue: ArrayBuffer; // 描述符的数据内容, 读取写数据时使用
    descriptorHandle: number; // 描述符的唯一标识句柄, 当server端BLE蓝牙设备提供了多个相同UUID描述符时，可以通过此句柄区分不同的描述符。
}
```

### `readDescriptorValue`
<decl method><pre>
(descriptor: BLEDescriptor): Promise&lt;BLEDescriptor&gt;
</pre></decl>

client端从指定的server端描述符读取数据，使用Promise异步回调。该接口异步返回一个 [`BLEDescriptor`](#bledescriptor) 类型的对象。

 - 该接口需要传入一个 [`BLEDescriptor`](#bledescriptor) 类型的对象，表示需要读取哪一个描述符

下面是一个GATT连接成功后，从指定的描述符中读取数据的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    descriptor: null,
    async read() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 调用: connect 接口发起连接
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. 服务发现，获取需要读取的：characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        console.dir("gatt client found:" + JSON.stringify(this.services))
        if (this.services.length > 0) {
            // 测试只尝试读取第一个服务的第一个特征值的第一个描述符，如果需要读取其它描述符，请自行修改
            // 需要注意的是，不是所有的特征值都有描述符，这里可以自行调整，选取有描述符且有读写权限的服务测试
            this.descriptor = this.services[0].characteristics[0].descriptors[0];
        }
        // 4. 读取指定描述符
        if (this.gattClient && this.descriptor) {
            await this.gattClient.readDescriptorValue(this.descriptor).then((result) => {
                console.log('descriptor read result:' + JSON.stringify(result))
            }).catch((error) => {
                console.dir('descriptor read error:' + JSON.stringify(error))
            })
        }
    },
}
```

### `writeDescriptorValue`
<decl method><pre>
(descriptor: BLEDescriptor): Promise&lt;number&gt;
</pre></decl>

client端向指定的server端描述符写入数据，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

 - 该接口需要传入一个 [`BLEDescriptor`](#bledescriptor) 类型的对象，表示需要写哪一个描述符

下面是一个GATT连接成功后，从指定的特征值写入数据的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    descriptor: null,
        
    randomArrayBuffer(length) {
        const randomArray = new Array(length)
        for (let i = 0; i < length; i++) {
            randomArray[i] = Math.floor(Math.random() * 256);
        }
        return new Uint8Array(randomArray).buffer
    },

    async write() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 调用: connect 接口发起连接
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. 服务发现，获取需要读取的：characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        console.dir("gatt client found:" + JSON.stringify(this.services))
        if (this.services.length > 0) {
            // 测试只尝试操作第一个服务的第一个特征值的第一个描述符，如果需要操作其它描述符，请自行修改
            // 需要注意的是，不是所有的特征值都有描述符，这里可以自行调整，选取有描述符且有读写权限的服务测试
            this.descriptor = this.services[0].characteristics[0].descriptors[0];
        }
        // 4. 写指定描述符
        if (this.gattClient && this.descriptor) {
            let value = randomArrayBuffer(15)
            this.descriptor.descriptorValue = value
            await this.gattClient.writeDescriptorValue(this.descriptor).then((result) => {
                if (result === 0) {
                    console.log('descriptor write success')
                } else {
                    console.log('descriptor write failed:' + result)
                }
            }).catch((error) => {
                console.dir('descriptor write error:' + JSON.stringify(error))
            })
        }
    },
}
```

### `getRssiValue`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

client端获取GATT连接链路信号强度 (Received Signal Strength Indication, RSSI)，使用Promise异步回调。该接口异步返回一个&lt;number&gt;类型的信号强度，单位：dBm

下面是一个GATT连接成功后，获取设备信号强度的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async rssi() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        if (this.gattClient) {
            await this.gattClient.getRssiValue().then((rssi) => {
                console.dir('device rssi:' + rssi)
            })
        }
    },
}
```

### `getBLEMtuSize`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

client端获取GATT连接链路MTU（最大传输单元）大小，使用Promise异步回调。该接口异步返回一个&lt;number&gt;类型的长度，单位：byte

下面是一个GATT连接成功后，获取GATT连接链路MTU（最大传输单元）大小：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async mtu() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        if (this.gattClient) {
            await this.gattClient.getBLEMtuSize().then((mtu) => {
                console.dir('device mtu:' + mtu)
            })
        }
    },
}
```

### `setBLEMtuSize`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

client端同server端协商MTU（最大传输单元）大小，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

### `setCharacteristicChangeNotification`
<decl method><pre>
(characteristic: BLECharacteristic, enable: boolean): Promise&lt;number&gt;
</pre></decl>

client端启用或者禁用接收server端特征值内容变更通知的能力，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

 - 该接口需要传入一个 [`BLECharacteristic`](#blecharacteristic) 类型的对象，表示需要操作哪一个特征值
 - 该接口需要传日一个 boolean 值，表示开启还是关闭内容变更通知能力，true表示开启，false表示关闭

下面是一个GATT连接成功后，开启特征值内容变更通知的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async notify() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 调用: connect 接口发起连接
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. 服务发现，获取需要读取的：characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // 测试只尝试操作第一个服务的第一个特征值，如果需要操作其它特征值，请自行修改
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. 操作指定特征值
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeNotification(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Notification success')
                } else {
                    console.log('该特征值不允许设置开启监听，ResultCode:' + result);
                }
            }).catch((error) => {
                console.error('set characteristic Notification error: ' + JSON.stringify(error))
            })
        }
    },
}
```

### `setCharacteristicChangeIndication`
<decl method><pre>
(characteristic: BLECharacteristic, enable: boolean): Promise&lt;number&gt;
</pre></decl>

client端启用或者禁用接收server端特征值内容变更指示的能力，使用Promise异步回调。该接口异步返回一个 [`ResultCode`](#resultcode) ，用来判断执行成功还是失败。

 - 该接口需要传入一个 [`BLECharacteristic`](#blecharacteristic) 类型的对象，表示需要操作哪一个特征值
 - 该接口需要传日一个 boolean 值，表示开启还是关闭内容变更指示的能力，true表示开启，false表示关闭

下面是一个GATT连接成功后，开启特征值内容变更指示的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async indication() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 调用: connect 接口发起连接
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. 服务发现，获取需要读取的：characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // 测试只尝试操作第一个服务的第一个特征值，如果需要操作其它特征值，请自行修改
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. 写指定特征值
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeIndication(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Indication success')
                } else {
                    console.log('该特征值不允许设置开启监听，ResultCode:' + result);
                }
            }).catch((error) => {
                console.error('set characteristic Indication error:' + JSON.stringify(error))
            })
        }
    },
}
```

### `subscribeBLECharacteristicChange`
<decl method><pre>
(callback: Callback(characteristic: BLECharacteristic) => void): number
</pre></decl>

client端订阅server端特征值变化事件。当特征值发生变化时，会自动调用 `callback` 回调函数。该接口同步返回一个订阅ID，用于取消订阅。

回调函数参数字段说明：
- [`BLECharacteristic`](#blecharacteristic) ：发生变化的特征值对象。

下面是一个GATT连接成功后，开启特征值内容变更指示的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 调用: connect 接口发起连接
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. 订阅特征值变化
        this.listener = this.gattClient.subscribeBLECharacteristicChange((result) => {
            let characteristicUuid = result.characteristicUuid
            let hexString = arrayBufferToHex(result.characteristicValue)
            console.log('characteristic changed uuid:' + characteristicUuid + ' value:' + hexString)
        })
    },
}
```

### `unsubscribeBLECharacteristicChange`
<decl method><pre>
(subscribeId: number): void
</pre></decl>

client端取消订阅server端特征值变化事件。参数 `subscribeId` 为 [`subscribeBLECharacteristicChange`](#subscribeblecharacteristicchange) 方法返回的订阅ID。

下面是一个GATT连接成功后，开启特征值内容变更指示的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 调用: connect 接口发起连接
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. 取消订阅特征值变化
        if (this.listener) {
            this.gattClient.unsubscribeBLECharacteristicChange(this.listener)
            this.listener = null
        }
    },
}
```

### `ConnectionState`

蓝牙连接状态枚举

- `0`：已断开连接
- `1`：正在连接
- `2`：已连接
- `3`：正在断开连接 

### `GattDisconnectReason`

GATT链路断开原因枚举

- `0`：原因不可用
- `1`：连接超时
- `2`：对端设备主动断开连接
- `3`：本端设备主动断开连接
- `4`：未知断连原因

### `BLEConnectionChangeState`

此对象用于表示蓝牙连接状态，其类型签名如下：

```ts
/**
 * 蓝牙连接状态类型定义
 */
type BLEConnectionChangeState = {
    deviceId: string; // 设备 ID（例如："AA:BB:CC:DD:EE:FF"）
    state: ConnectionState; // 蓝牙连接状态
    reason: GattDisconnectReason; // GATT链路断开的原因
}
```

### `subscribeBLEConnectionStateChange` 
<decl method><pre>
(callback: Callback(connectionChangeState: BLEConnectionChangeState) => void): number
</pre></decl>

client端订阅GATT协议的连接状态变化事件。当连接状态发生变化时，会自动调用 `callback` 回调函数。该接口同步返回一个订阅ID，用于取消订阅。

回调函数参数字段说明：
- [`BLEConnectionChangeState`](#bleconnectionchangestate) ：连接状态。

下面是一个GATT连接成功后，订阅连接状态的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 调用: connect 接口发起连接
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. 订阅连接状态的变化
        this.listener = this.gattClient.subscribeBLEConnectionStateChange((result) => {
            console.log('connect changed:' + JSON.stringify(result))
        })
    },
}
```

### `unsubscribeBLEConnectionStateChange`
<decl method><pre>
(subscribeId: number): void
</pre></decl>

client端取消订阅GATT协议的连接状态变化事件。参数 `subscribeId` 为 [`subscribeBLEConnectionStateChange`](#subscribebleconnectionstatechange) 方法返回的订阅ID。

下面是一个取消订阅连接状态的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 调用: connect 接口发起连接
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. 订阅连接状态的变化
        this.listener = this.gattClient.subscribeBLEConnectionStateChange((result) => {
            console.log('connect changed:' + JSON.stringify(result))
        })
        // 4. 取消订阅连接状态的变化
        if (this.gattClient && this.listener) {    
            this.gattClient.unsubscribeBLEConnectionStateChange(this.listener)
            this.listener = null
        }
    },
}
```

### `subscribeBLEMtuChange`
<decl method><pre>
(callback: Callback(mtu: number) => void): number
</pre></decl>

client端订阅MTU（最大传输单元）大小变更事件。当MTU发生变化时，会自动调用 `callback` 回调函数。该接口同步返回一个订阅ID，用于取消订阅。

回调函数参数字段说明：
- mtu ：MTU（最大传输单元）大小。

下面是一个GATT连接成功后，订阅MTU变化的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 订阅MTU的变化
        this.listener = this.gattClient.subscribeBLEMtuChange((mtu) => {
            console.log('mtu changed:' + mtu)
        })
    },
}
```

### `unsubscribeBLEMtuChange`
<decl method><pre>
(subscribeId: number): void
</pre></decl>

client端取消订阅MTU（最大传输单元）大小变更事件。参数 `subscribeId` 为 [`subscribeBLEMtuChange`](#subscribeblemtuchange) 方法返回的订阅ID。

下面是一个取消订阅MTU变化的示例：
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. 构造: gattClient 实例，请将下列：'XX:XX:XX:XX:XX:XX' 修改为需要连接的设备地址
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. 订阅MTU的变化
        this.listener = this.gattClient.subscribeBLEMtuChange((mtu) => {
            console.log('mtu changed:' + mtu)
        })
        // 3. 取消订阅MTU的变化
        if (this.gattClient && this.listener) {    
            this.gattClient.unsubscribeBLEMtuChange(this.listener)
            this.listener = null
        }
    },
}
```
