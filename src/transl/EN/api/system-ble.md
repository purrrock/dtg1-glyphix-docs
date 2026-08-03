# Low power Bluetooth module

This module provides Bluetooth capabilities based on Bluetooth Low Energy (BLE) technology, supports initiating BLE scans, and connects and transmits data based on the Generic Attribute Profile (GATT) (currently only the creation of GattClient is supported, and the creation of GattServer is not supported at the moment).

::: warning
Most of the APIs in `@system.bluetooth.ble` are [Promise asynchronous operations](#Promise asynchronous operations), which are essentially different from synchronous IO access. Be sure to understand the basic concepts of asynchronous programming and be familiar with the use of Promise and `async/await`.
:::

## Import module

``` js
import ble from '@system.bluetooth.ble'
```

## Permissions

::: tip
Applications using this module need to declare permission: watch.permission.BLUETOOTH
:::

## ble interface definition

### `ResultCode`

Result enumeration returned in Promise

- `0`: success;
- `1`: Bluetooth Low Energy is not turned on;
- `2`: Parameter error;
- `3`: Failed to enable Bluetooth Low Energy;
- `4`: No Bluetooth adapter available;
- `5`: Connection failed;
- `6`: Failed to disconnect;
- `7`: Setting this attribute is not supported yet;
- `8`: unknown error;

### `startBLEScan`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

Start scanning and use Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

Here is an example of starting a scan:
```ts
import ble from '@system.bluetooth.ble'
export default {
    async scanStart() {
        // Start scanning
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

Stop scanning and use Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

Here's an example of stopping a scan:
```ts
import ble from '@system.bluetooth.ble'
export default {
    async scanStop() {
        // Stop scanning
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

This object is used to represent the reported scan results. The type signature is as follows:

```ts
/**
 * Scan result object definition
 */
type ScanResult = {
    deviceId: string; // Device ID (for example: "AA:BB:CC:DD:EE:FF")
    rssi: number; // signal strength in dBm
    data: ArrayBuffer; // Original data of broadcast message
    deviceName: string; // device name (if any)
    connectable: boolean; // Whether it can be connected, true means it can be connected
}
```

### `getBLEScanResults`
<decl method><pre>
(): Promise&lt;Array&lt;ScanResult&gt;&gt;
</pre></decl>

Query the scan results and use Promise asynchronous callback. This interface asynchronously returns an array containing [`ScanResult`](#scanresult) objects (i.e. Array&lt;[`ScanResult`](#scanresult)&gt;).

::: warning
Because the underlying Bluetooth adapter is a singleton, multiple applications may operate Bluetooth devices at the same time. It will exist: After application A starts scanning for a period of time, application B starts scanning again. At this time, the scan results monitored by application B are incomplete. In order to handle this situation, it is recommended that all applications immediately query the current scan results after starting scanning.
:::

Here is an example of querying the scan results after starting the scan:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        scanList: [],
    },
    async scanStart() {
        // Start scanning
        await ble.startBLEScan().then(async (result) => {
            console.dir('startBLEScan success')
            //Query scan results
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

Subscribe to scan status changes and use Callback asynchronous callback. When the scan status changes, the `callback` callback function is automatically called. This interface synchronously returns a subscription ID, which is used to cancel the subscription.

Callback function parameter field description:
- `scan`: current scanning status. true means scanning is in progress, false means scanning has stopped.

Here is an example of subscribing to scan status changes:
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

Unsubscribe from scanning status changes. The parameter `subscribeId` is the subscription ID returned by the [`subscribeScanStatus`](#subscribescanstatus) method.

Here is an example of unsubscribing from a scan status change:
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

Subscribe to scan result reporting events and use Callback asynchronous callback. Whenever a new device is scanned, the `callback` callback function is automatically called. This interface synchronously returns a subscription ID, which is used to cancel the subscription.

::: tip
The scanning results are reported in incremental mode. Each discovery is reported one by one. After monitoring this event, the user needs to store the scanning results himself.
:::

Callback function parameter field description:
- [`ScanResult`](#scanresult): The new device object scanned.

The following is an example of subscribing to scan result reporting events:
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

Unsubscribe from scanning result reporting events. The parameter `subscribeId` is the subscription ID returned by the [`subscribeBLEDeviceFind`](#subscribebledevicefind) method.

The following is an example of unsubscribing from scanning result reporting events:
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

This object is used to represent the Client object in the Gatt protocol. The type signature is as follows:

```ts
/**
 *GattClientDevice object type definition
 */
typeGattClientDevice = {
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

Create a [`GattClientDevice`](#gattclientdevice) instance to represent the client in the GATT connection. This interface synchronously returns a [`GattClientDevice`](#gattclientdevice) instance.

- Through this instance, you can operate the client-side behavior, such as calling [`connect`](#connect) to initiate a connection to the peer device, and calling [`getServices`](#getservices) to obtain all service capabilities supported by the peer device.
 - The deviceId (device address) required to create this instance represents the server-side device address. You can obtain the server device address through the [`startBLEScan`](#startblescan) interface, and you must ensure that the BLE broadcast of the server device is connectable.

Here is an example of creating an instance of [`GattClientDevice`](#gattclientdevice):
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    create() {
        // Please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
    },
}
```

## GattClientDevice interface definition

### `connect`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

The client actively initiates a GATT protocol connection with the server Bluetooth device and uses Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

- Before using the methods of this class, you need to construct an instance of this class through the [`createGattClientDevice`](#creategattclientdevice) method.
 - Multiple GATT connections can be managed by creating different instances of this class.

The following is an example of initiating a GATT protocol connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async connect() {
        // Please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

The client actively disconnects the GATT protocol connection with the server Bluetooth device and uses Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

Here is an example of disconnecting the GATT protocol:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        address: null,
    },
    gattClient: null,
    async connect() {
        // Please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

Close the client instance and use Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

### `getDeviceName`
<decl method><pre>
(): Promise&lt;string&gt;
</pre></decl>

The client obtains the name of the remote Bluetooth low energy device and uses Promise asynchronous callback. This interface asynchronously returns a device name of type &lt;string&gt;.

The following is an example of obtaining the device name after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async name() {
        let clientName = 'N/A'
        // Please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

This object is used to represent the GATT service structure, with the following type signature:

```ts
/**
 * GATT service structure definition, which can contain multiple characteristic values BLECharacteristic and other dependent services.
 */
type GattService = {
    serviceUuid: string; // Service UUID, identifies a GATT service. For example: 00001888-0000-1000-8000-00805f9b34fb.
    isPrimary: boolean; // Whether it is the primary service. true means it is the primary service, false means it is the secondary service.
    characteristics: Array<BLECharacteristic>; // List of characteristic values ​​contained in the current service.
    includeServices: Array<GattService>; // Other services that the current service depends on.
}
```

### `getServices`
<decl method><pre>
(): Promise&lt;Array&lt;GattService&gt;&gt;
</pre></decl>

The client side obtains all services of Bluetooth low energy devices, that is, service discovery, using Promise asynchronous callback. This interface asynchronously returns an array of type Array&lt;[`GattService`](#gattservice)&gt; containing all services.

The following is an example of obtaining all services of the device after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    async onShow() {
        // Please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

This object is used to represent the attributes supported by GATT characteristic values. The type signature is as follows:

```ts
/**
 * Describes the attributes supported by GATT eigenvalues. Determines how characteristic value contents and descriptors are used and accessed.
 */
type GattProperties = {
    write: boolean; // Whether this characteristic value supports writing operations. true means it is supported and needs to reply to the peer device when being written, false means it is not supported.
    writeNoResponse: boolean; // Whether this characteristic value supports writing operations. true means it is supported, and there is no need to reply to the peer device when being written, false means it is not supported.
    read: boolean; // Whether this characteristic value supports read operations. true means supported, false means not supported.
    notify: boolean; //Whether this characteristic value supports actively notifying the peer device of the characteristic value content. true means it is supported and the peer device does not need to reply to confirm, false means it is not supported.
    indicate: boolean; // Whether this characteristic value supports indicating the characteristic value content to the peer device. true means it is supported and the peer device needs to reply to confirm, false means it is not supported.
    broadcast: boolean; // Whether this characteristic value supports being sent as broadcast content by the server. true means it is supported, the server can carry the characteristic value content in the broadcast message as ServiceData type, false means it is not supported.
    authenticatedSignedWrite: boolean; //Whether this characteristic value supports signed writing operations, replacing the encryption process by performing signature verification on the written content. true means supported, false means not supported.
    extendedProperties: boolean; //Whether there are extended properties for this characteristic value. true indicates that the extended attribute exists, false indicates that it does not exist.
}
```

### `BLECharacteristic`

This object is used to represent GATT characteristic values. The type signature is as follows:

```ts
/**
 * GATT characteristic value type definition, which is the core data unit of service GattService
 */
type BLECharacteristic = {
    serviceUuid: string; // The service UUID to which the characteristic value belongs, for example: 00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // Characteristic value UUID, for example: 00002a11-0000-1000-8000-00805f9b34fb
    characteristicValue: ArrayBuffer; //The data content of the characteristic value, used when reading and writing data
    descriptors: Array<BLEDescriptor>; // List of descriptors contained in the characteristic value
    properties: GattProperties; // Properties supported by characteristic values
    characteristicValueHandle: number; // The unique identification handle of the characteristic value. When the server-side BLE Bluetooth device provides multiple identical UUID feature values, you can use this handle to distinguish different feature values.
}
```

### `readCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic): Promise&lt;BLECharacteristic&gt;
</pre></decl>

The client side reads data from the specified server side characteristic value and uses Promise asynchronous callback. This interface asynchronously returns an object of type [`BLECharacteristic`](#blecharacteristic).

- This interface needs to pass in an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic value needs to be read.

The following is an example of reading data from a specified characteristic value after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async read() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, obtain what needs to be read: characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // The test only attempts to read the first characteristic value of the first service. If you need to read other characteristic values, please modify it yourself.
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Read the specified characteristic value
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

Characteristic value writing method enumeration

- `1`: After writing the characteristic value, the peer Bluetooth device needs to reply with confirmation.
- `2`: After writing the characteristic value, the peer Bluetooth device does not need to reply.

### `writeCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic, writeType: GattWriteType): Promise&lt;number&gt;
</pre></decl>

The client writes data to the specified server-side characteristic value and uses Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

- This interface needs to pass in an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic value needs to be written
 - This interface needs to pass in a [`GattWriteType`](#gattwritetype) enumeration value to indicate the way to write data.

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

This object represents a GATT descriptor and its type is defined as follows:

```ts
/**
 * GATT descriptor type definition, which is the data unit of the characteristic value BLECharacteristic, is used to describe the additional information and attributes of the characteristic value
 */
type BLEDescriptor = {
    serviceUuid: string; // The service UUID to which the characteristic value belongs, for example: 00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // Characteristic value UUID, for example: 00002a11-0000-1000-8000-00805f9b34fb
    descriptorUuid: string; // Descriptor UUID, for example: 00002902-0000-1000-8000-00805f9b34fb
    descriptorValue: ArrayBuffer; //The data content of the descriptor, used when reading and writing data
    descriptorHandle: number; // The unique identification handle of the descriptor. When the server-side BLE Bluetooth device provides multiple same UUID descriptors, this handle can be used to distinguish different descriptors.
}
```

### `readDescriptorValue`
<decl method><pre>
(descriptor: BLEDescriptor): Promise&lt;BLEDescriptor&gt;
</pre></decl>

The client reads data from the specified server descriptor and uses Promise asynchronous callback. This interface asynchronously returns an object of type [`BLEDescriptor`](#bledescriptor).

- This interface needs to pass in an object of type [`BLEDescriptor`](#bledescriptor) to indicate which descriptor needs to be read.

The following is an example of reading data from the specified descriptor after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    descriptor: null,
    async read() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, obtain what needs to be read: characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        console.dir("gatt client found:" + JSON.stringify(this.services))
        if (this.services.length > 0) {
            // The test only tries to read the first descriptor of the first characteristic value of the first service. If you need to read other descriptors, please modify it yourself.
            // It should be noted that not all characteristic values have descriptors. You can adjust it yourself and select a service test that has descriptors and read and write permissions.
            this.descriptor = this.services[0].characteristics[0].descriptors[0];
        }
        // 4. Read the specified descriptor
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

The client writes data to the specified server descriptor and uses Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

- This interface needs to pass in an object of type [`BLEDescriptor`](#bledescriptor) to indicate which descriptor needs to be written.

The following is an example of writing data from a specified characteristic value after a successful GATT connection:
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

The client side obtains the GATT connection link signal strength (Received Signal Strength Indication, RSSI) and uses Promise asynchronous callback. This interface asynchronously returns a signal strength of type &lt;number&gt;, unit: dBm

The following is an example of obtaining the device signal strength after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    asyncrssi() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

The client side obtains the MTU (maximum transmission unit) size of the GATT connection link and uses Promise asynchronous callback. This interface asynchronously returns the length of a &lt;number&gt; type, unit: byte

The following is the method to obtain the MTU (maximum transmission unit) size of the GATT connection link after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async mtu() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
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

The client negotiates the MTU (maximum transmission unit) size with the server and uses Promise asynchronous callback. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

### `setCharacteristicChangeNotification`
<decl method><pre>
(characteristic: BLECharacteristic, enable: boolean): Promise&lt;number&gt;
</pre></decl>

The client side enables or disables the ability to receive server side feature value content change notifications, using Promise asynchronous callbacks. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

- This interface needs to pass in an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic value needs to be operated
 - This interface needs to pass a boolean value, indicating whether to turn on or off the content change notification capability. true means turned on, false means turned off.

The following is an example of turning on feature value content change notification after the GATT connection is successful:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async notify() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, obtain what needs to be read: characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // The test only attempts to operate the first characteristic value of the first service. If you need to operate other characteristic values, please modify it yourself.
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Operate the specified characteristic value
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeNotification(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Notification success')
                } else {
                    console.log('This characteristic value does not allow setting to enable monitoring, ResultCode:' + result);
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

The client side enables or disables the ability to receive server side characteristic value content change instructions, using Promise asynchronous callbacks. This interface returns a [`ResultCode`](#resultcode) asynchronously, which is used to determine whether the execution is successful or failed.

- This interface needs to pass in an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic value needs to be operated
 - This interface needs to pass a boolean value, indicating whether to turn on or off the ability to indicate content change. True means turned on, false means turned off.

The following is an example of turning on the characteristic value content change indication after the GATT connection is successful:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async indication() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, obtain what needs to be read: characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // The test only attempts to operate the first characteristic value of the first service. If you need to operate other characteristic values, please modify it yourself.
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Write the specified feature value
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeIndication(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Indication success')
                } else {
                    console.log('This characteristic value does not allow setting to enable monitoring, ResultCode:' + result);
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

The client subscribes to server-side characteristic value change events. When the characteristic value changes, the `callback` callback function is automatically called. This interface synchronously returns a subscription ID, which is used to cancel the subscription.

Callback function parameter field description:
- [`BLECharacteristic`](#blecharacteristic): The changed characteristic value object.

The following is an example of turning on the characteristic value content change indication after the GATT connection is successful:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Subscribe to feature value changes
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

The client unsubscribes from the server-side characteristic value change event. The parameter `subscribeId` is the subscription ID returned by the [`subscribeBLECharacteristicChange`](#subscribeblecharacteristicchange) method.

The following is an example of turning on the characteristic value content change indication after the GATT connection is successful:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Unsubscribe from feature value changes
        if (this.listener) {
            this.gattClient.unsubscribeBLECharacteristicChange(this.listener)
            this.listener = null
        }
    },
}
```

### `ConnectionState`

Bluetooth connection status enumeration

- `0`: disconnected
- `1`: Connecting
- `2`: Connected
- `3`: Disconnecting

### `GattDisconnectReason`

GATT link disconnection reason enumeration

- `0`: Reason is not available
- `1`: connection timeout
- `2`: The peer device actively disconnects
- `3`: The local device actively disconnects
- `4`: Unknown reason for disconnection

### `BLEConnectionChangeState`

This object is used to represent the Bluetooth connection status, and its type signature is as follows:

```ts
/**
 * Bluetooth connection status type definition
 */
type BLEConnectionChangeState = {
    deviceId: string; // Device ID (for example: "AA:BB:CC:DD:EE:FF")
    state: ConnectionState; // Bluetooth connection status
    reason: GattDisconnectReason; //The reason why the GATT link is disconnected
}
```

### `subscribeBLEConnectionStateChange`
<decl method><pre>
(callback: Callback(connectionChangeState: BLEConnectionChangeState) => void): number
</pre></decl>

The client subscribes to the connection status change event of the GATT protocol. When the connection status changes, the `callback` callback function is automatically called. This interface synchronously returns a subscription ID, which is used to cancel the subscription.

Callback function parameter field description:
- [`BLEConnectionChangeState`](#bleconnectionchangestate): connection state.

The following is an example of subscribing to the connection status after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Subscribe to changes in connection status
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

The client unsubscribes from the connection status change event of the GATT protocol. The parameter `subscribeId` is the subscription ID returned by the [`subscribeBLEConnectionStateChange`](#subscribebleconnectionstatechange) method.

Here's an example of unsubscribing from a connection state:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call: connect interface to initiate connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Subscribe to changes in connection status
        this.listener = this.gattClient.subscribeBLEConnectionStateChange((result) => {
            console.log('connect changed:' + JSON.stringify(result))
        })
        // 4. Unsubscribe from changes in connection status
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

The client subscribes to MTU (Maximum Transmission Unit) size change events. When the MTU changes, the `callback` callback function is automatically called. This interface synchronously returns a subscription ID, which is used to cancel the subscription.

Callback function parameter field description:
- mtu: MTU (maximum transmission unit) size.

The following is an example of subscribing to MTU changes after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Construction: gattClient instance, please change the following: 'XX:XX:XX:XX:XX:XX' to the address of the device to be connected
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Subscribe to MTU changes
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

The client unsubscribes from the MTU (Maximum Transmission Unit) size change event. The parameter `subscribeId` is the subscription ID returned by the [`subscribeBLEMtuChange`](#subscribeblemtuchange) method.

Here is an example of unsubscribing from MTU changes:
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
