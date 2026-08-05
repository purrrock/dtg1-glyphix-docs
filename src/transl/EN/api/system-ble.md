# Bluetooth Low Energy Module

This module provides Bluetooth capabilities based on Bluetooth Low Energy (BLE) technology, supporting BLE scanning initiation as well as connections and data transmission based on the Generic Attribute Profile (GATT) (currently, only creating a `GattClient` is supported; creating a `GattServer` is not yet supported).

::: warning
Most APIs in `@system.bluetooth.ble` are [Promise-based asynchronous operations](#Promise异步操作), which are fundamentally different from synchronous I/O access. Please make sure you understand the basic concepts of asynchronous programming and are familiar with the usage of Promises and `async/await`.
:::

## Importing the Module

``` js
import ble from '@system.bluetooth.ble'
```

## Permissions

::: tip
Using this module requires declaring the following permission in the application: `watch.permission.BLUETOOTH`
:::

## BLE Interface Definitions

### `ResultCode`

Result enumeration returned in Promises

- `0`: Success;
- `1`: BLE is not enabled;
- `2`: Parameter error;
- `3`: Failed to enable BLE;
- `4`: No available Bluetooth adapter;
- `5`: Connection failed;
- `6`: Disconnection failed;
- `7`: Setting this property is not currently supported;
- `8`: Unknown error;

### `startBLEScan`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

Starts scanning using a Promise-based asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

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

Stops scanning using a Promise-based asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

Here is an example of stopping a scan:
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

This object is used to represent the reported scan results, with the following type signature:

```ts
/**
 * Definition of the scan result object
 */
type ScanResult = {
    deviceId: string; // Device ID (e.g., "AA:BB:CC:DD:EE:FF")
    rssi: number; // Signal strength in dBm
    data: ArrayBuffer; // Raw advertising packet data
    deviceName: string; // Device name (if available)
    connectable: boolean; // Whether connectable, true indicates connectable
}
```

### `getBLEScanResults`
<decl method><pre>
(): Promise&lt;Array&lt;ScanResult&gt;&gt;
</pre></decl>

Queries scan results using a Promise-based asynchronous callback. This interface asynchronously returns an array containing [`ScanResult`](#scanresult) objects (i.e., `Array<`[`ScanResult`](#scanresult)`>`).

::: warning
Since the underlying Bluetooth adapter is a singleton, multiple applications may operate Bluetooth devices simultaneously. This can lead to a scenario where: App A starts scanning for a period of time, and then App B starts scanning again. In this case, the scan results monitored by App B will be incomplete. To handle this situation, it is recommended that all applications immediately query the current scan results after starting a scan.
:::

Here is an example of querying scan results after starting a scan:
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
            // Query scan results
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

Subscribes to scan status changes using a Callback-based asynchronous callback. When the scan status changes, the `callback` function is automatically invoked. This interface synchronously returns a subscription ID used for unsubscribing.

Description of callback function parameter fields:
- `scan`: Current scan status. `true` indicates scanning is in progress, `false` indicates scanning has stopped.

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

Unsubscribes from scan status changes. The `subscribeId` parameter is the subscription ID returned by the [`subscribeScanStatus`](#subscribescanstatus) method.

Here is an example of unsubscribing from scan status changes:
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

Subscribes to scan result reporting events using a Callback-based asynchronous callback. Whenever a new device is scanned, the `callback` function is automatically invoked. This interface synchronously returns a subscription ID used for unsubscribing.

::: tip
Scan results are reported in an incremental mode—each discovered device is reported as it is found. After listening to this event, users need to store the scan results themselves.
:::

Description of callback function parameter fields:
- [`ScanResult`](#scanresult): The newly discovered device object.

Here is an example of subscribing to scan result reporting events:
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

Unsubscribes from scan result reporting events. The `subscribeId` parameter is the subscription ID returned by the [`subscribeBLEDeviceFind`](#subscribebledevicefind) method.

Here is an example of unsubscribing from scan result reporting events:
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

This object is used to represent the Client object in the GATT protocol, with the following type signature:

```ts
/**
 * GattClientDevice object type definition
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

Creates a [`GattClientDevice`](#gattclientdevice) instance, representing the client side in a GATT connection. This interface synchronously returns a [`GattClientDevice`](#gattclientdevice) instance.

 - Through this instance, you can operate client-side behaviors, such as calling [`connect`](#connect) to initiate a connection to the peer device, and calling [`getServices`](#getservices) to retrieve all service capabilities supported by the peer device.
 - The `deviceId` (device address) required to create this instance represents the server-side device address. You can obtain the server-side device address via the [`startBLEScan`](#startblescan) interface, and you must ensure that the server-side device's BLE advertising is connectable.

Here is an example of creating a [`GattClientDevice`](#gattclientdevice) instance:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    create() {
        // Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
    },
}
```

## GattClientDevice Interface Definitions

### `connect`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

The client actively initiates a GATT protocol connection with the server Bluetooth device, using a Promise-based asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

 - Before using the methods of this class, you must construct an instance of this class via the [`createGattClientDevice`](#creategattclientdevice) method.
 - By creating different instances of this class, you can manage multiple GATT connections.

Here is an example of initiating a GATT protocol connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async connect() {
        // Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
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

The client actively disconnects the GATT protocol connection with the server Bluetooth device, using a Promise-based asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

Here is an example of disconnecting a GATT protocol connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        address: null,
    },
    gattClient: null,
    async connect() {
        // Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
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

Closes the client-side instance using a Promise-based asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

### `getDeviceName`
<decl method><pre>
(): Promise&lt;string&gt;
</pre></decl>

The client retrieves the name of the remote BLE device using a Promise-based asynchronous callback. This interface asynchronously returns a device name of type `<string>`.

Here is an example of getting the device name after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async name() {
        let clientName = 'N/A'
        // Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
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
 * Definition of the GATT service structure, which can contain multiple BLECharacteristics and other dependent services.
 */
type GattService = {
    serviceUuid: string; // Service UUID, identifying a GATT service. For example: 00001888-0000-1000-8000-00805f9b34fb.
    isPrimary: boolean; // Whether it is a primary service. true indicates a primary service, false indicates a secondary service.
    characteristics: Array<BLECharacteristic>; // List of characteristics contained in the current service.
    includeServices: Array<GattService>; // Other services depended on by the current service.
}
```

### `getServices`
<decl method><pre>
(): Promise&lt;Array&lt;GattService&gt;&gt;
</pre></decl>

The client retrieves all services of the BLE device (service discovery) using a Promise-based asynchronous callback. This interface asynchronously returns an array of type `Array<`[`GattService`](#gattservice)`>` containing all services.

Here is an example of getting all services of the device after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    async onShow() {
        // Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
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

This object is used to represent the properties supported by a GATT characteristic, with the following type signature:

```ts
/**
 * Describes the properties supported by a GATT characteristic. Determines how the characteristic content and descriptors are used and accessed.
 */
type GattProperties = {
    write: boolean; // Whether this characteristic supports write operations. true indicates support, and the peer device needs to send a response when written; false indicates no support.
    writeNoResponse: boolean; // Whether this characteristic supports write operations. true indicates support, and no response is needed from the peer device when written; false indicates no support.
    read: boolean; // Whether this characteristic supports read operations. true indicates support, false indicates no support.
    notify: boolean; // Whether this characteristic supports actively notifying the peer device of its content. true indicates support, and the peer device does not need to send an acknowledgment; false indicates no support.
    indicate: boolean; // Whether this characteristic supports indicating its content to the peer device. true indicates support, and the peer device needs to send an acknowledgment; false indicates no support.
    broadcast: boolean; // Whether this characteristic supports being sent by the server as advertising data. true indicates support, and the server can carry the characteristic content as ServiceData in the advertising packet; false indicates no support.
    authenticatedSignedWrite: boolean; // Whether this characteristic supports signed write operations, replacing the encryption process with signature verification of the written content. true indicates support, false indicates no support.
    extendedProperties: boolean; // Whether the characteristic has extended properties. true indicates extended properties exist, false indicates they do not.
}
```

### `BLECharacteristic`

This object is used to represent a GATT characteristic, with the following type signature:

```ts
/**
 * GATT characteristic type definition, which is the core data unit of the GattService
 */
type BLECharacteristic = {
    serviceUuid: string; // Service UUID to which the characteristic belongs, e.g., 00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // Characteristic UUID, e.g., 00002a11-0000-1000-8000-00805f9b34fb
    characteristicValue: ArrayBuffer; // Data content of the characteristic, used when reading/writing data
    descriptors: Array<BLEDescriptor>; // List of descriptors contained in the characteristic
    properties: GattProperties; // Properties supported by the characteristic
    characteristicValueHandle: number; // Unique identification handle of the characteristic. When the server BLE device provides multiple characteristics with the same UUID, this handle can be used to distinguish between them
}
```

### `readCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic): Promise&lt;BLECharacteristic&gt;
</pre></decl>

The client reads data from a specified server characteristic using a Promise-based asynchronous callback. This interface asynchronously returns an object of type [`BLECharacteristic`](#blecharacteristic).

 - This interface requires passing an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic needs to be read.

Here is an example of reading data from a specified characteristic after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async read() {
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, get the characteristic to read
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // For testing, we only try to read the first characteristic of the first service. Modify as needed to read other characteristics.
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Read the specified characteristic
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

Characteristic write type enumeration

- `1`: After writing to the characteristic, the peer Bluetooth device needs to send an acknowledgment response.
- `2`: After writing to the characteristic, the peer Bluetooth device does not need to respond.

### `writeCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic, writeType: GattWriteType): Promise&lt;number&gt;
</pre></decl>

The client writes data to a specified server characteristic using a Promise-based asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

 - This interface requires passing an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic needs to be written.
 - This interface requires passing a [`GattWriteType`](#gattwritetype) enumeration value to indicate the data writing mode.

Here is an example of writing data to a specified characteristic after a successful GATT connection:
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
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, get the characteristic to operate on
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // For testing, we only try to operate on the first characteristic of the first service. Modify as needed for other characteristics.
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Write to the specified characteristic
        if (this.gattClient && this.characteristic) {
            // Generate an ArrayBuffer of the specified length containing random numbers
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

This object represents a GATT descriptor, with the following type definition:

```ts
/**
 * GATT descriptor type definition, which is a data unit of the BLECharacteristic, used to describe additional information and properties of the characteristic
 */
type BLEDescriptor = {
    serviceUuid: string; // Service UUID to which the characteristic belongs, e.g., 00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // Characteristic UUID, e.g., 00002a11-0000-1000-8000-00805f9b34fb
    descriptorUuid: string; // Descriptor UUID, e.g., 00002902-0000-1000-8000-00805f9b34fb
    descriptorValue: ArrayBuffer; // Data content of the descriptor, used when reading/writing data
    descriptorHandle: number; // Unique identification handle of the descriptor. When the server BLE device provides multiple descriptors with the same UUID, this handle can be used to distinguish between them.
}
```

### `readDescriptorValue`
<decl method><pre>
(descriptor: BLEDescriptor): Promise&lt;BLEDescriptor&gt;
</pre></decl>

The client reads data from a specified server descriptor using a Promise-based asynchronous callback. This interface asynchronously returns an object of type [`BLEDescriptor`](#bledescriptor).

 - This interface requires passing an object of type [`BLEDescriptor`](#bledescriptor) to indicate which descriptor needs to be read.

Here is an example of reading data from a specified descriptor after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    descriptor: null,
    async read() {
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, get the characteristic to read
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        console.dir("gatt client found:" + JSON.stringify(this.services))
        if (this.services.length > 0) {
            // For testing, we only try to read the first descriptor of the first characteristic of the first service. Modify as needed.
            // Note that not all characteristics have descriptors. You can adjust this to select services that have descriptors and read/write permissions for testing.
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

The client writes data to a specified server descriptor using a Promise-based asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

 - This interface requires passing an object of type [`BLEDescriptor`](#bledescriptor) to indicate which descriptor needs to be written.

Here is an example of writing data to a specified descriptor after a successful GATT connection:
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
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, get the characteristic to read
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        console.dir("gatt client found:" + JSON.stringify(this.services))
        if (this.services.length > 0) {
            // For testing, we only try to operate on the first descriptor of the first characteristic of the first service. Modify as needed.
            // Note that not all characteristics have descriptors. Adjust accordingly to test services with descriptors and read/write permissions.
            this.descriptor = this.services[0].characteristics[0].descriptors[0];
        }
        // 4. Write to the specified descriptor
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

The client retrieves the Received Signal Strength Indication (RSSI) of the GATT connection link using a Promise-based asynchronous callback. This interface asynchronously returns a signal strength of type `<string>` `<number>`, unit: dBm.

Here is an example of getting the device signal strength after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async rssi() {
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
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

The client retrieves the MTU (Maximum Transmission Unit) size of the GATT connection link using a Promise-based asynchronous callback. This interface asynchronously returns a length of type `<number>`, unit: bytes.

Here is an example of getting the GATT connection link MTU size after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async mtu() {
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
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

The client negotiates the MTU (Maximum Transmission Unit) size with the server using a Promise-based asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

### `setCharacteristicChangeNotification`
<decl method><pre>
(characteristic: BLECharacteristic, enable: boolean): Promise&lt;number&gt;
</pre></decl>

The client enables or disables the capability to receive server characteristic value change notifications, using a Promise-based asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

 - This interface requires passing an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic needs to be operated on.
 - This interface requires passing a boolean value to indicate whether to enable or disable the content change notification capability (`true` to enable, `false` to disable).

Here is an example of enabling characteristic value change notifications after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async notify() {
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, get the characteristic to read
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // For testing, we only try to operate on the first characteristic of the first service. Modify as needed for other characteristics.
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Operate on the specified characteristic
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeNotification(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Notification success')
                } else {
                    console.log('This characteristic does not allow setting notification, ResultCode:' + result);
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

The client enables or disables the capability to receive server characteristic value change indications, using a Promise-based asynchronous callback. This interface asynchronously returns a [`ResultCode`](#resultcode) to determine whether the execution succeeded or failed.

 - This interface requires passing an object of type [`BLECharacteristic`](#blecharacteristic) to indicate which characteristic needs to be operated on.
 - This interface requires passing a boolean value to indicate whether to enable or disable the content change indication capability (`true` to enable, `false` to disable).

Here is an example of enabling characteristic value change indications after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async indication() {
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Service discovery, get the characteristic to read
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // For testing, we only try to operate on the first characteristic of the first service. Modify as needed for other characteristics.
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Write to the specified characteristic
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeIndication(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Indication success')
                } else {
                    console.log('This characteristic does not allow setting indication, ResultCode:' + result);
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

The client subscribes to server characteristic change events. When a characteristic changes, the `callback` function is automatically invoked. This interface synchronously returns a subscription ID used for unsubscribing.

Description of callback function parameter fields:
- [`BLECharacteristic`](#blecharacteristic): The characteristic object that changed.

Here is an example of subscribing to characteristic changes after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Subscribe to characteristic changes
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

The client unsubscribes from server characteristic change events. The `subscribeId` parameter is the subscription ID returned by the [`subscribeBLECharacteristicChange`](#subscribeblecharacteristicchange) method.

Here is an example of unsubscribing from characteristic changes after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Unsubscribe from characteristic changes
        if (this.listener) {
            this.gattClient.unsubscribeBLECharacteristicChange(this.listener)
            this.listener = null
        }
    },
}
```

### `ConnectionState`

Bluetooth connection state enumeration

- `0`: Disconnected
- `1`: Connecting
- `2`: Connected
- `3`: Disconnecting

### `GattDisconnectReason`

GATT link disconnection reason enumeration

- `0`: Reason not available
- `1`: Connection timeout
- `2`: Peer device actively disconnected
- `3`: Local device actively disconnected
- `4`: Unknown disconnection reason

### `BLEConnectionChangeState`

This object is used to represent the Bluetooth connection state, with the following type signature:

```ts
/**
 * Bluetooth connection state type definition
 */
type BLEConnectionChangeState = {
    deviceId: string; // Device ID (e.g., "AA:BB:CC:DD:EE:FF")
    state: ConnectionState; // Bluetooth connection state
    reason: GattDisconnectReason; // Reason for GATT link disconnection
}
```

### `subscribeBLEConnectionStateChange` 
<decl method><pre>
(callback: Callback(connectionChangeState: BLEConnectionChangeState) => void): number
</pre></decl>

The client subscribes to GATT protocol connection state change events. When the connection state changes, the `callback` function is automatically invoked. This interface synchronously returns a subscription ID used for unsubscribing.

Description of callback function parameter fields:
- [`BLEConnectionChangeState`](#bleconnectionchangestate): Connection state.

Here is an example of subscribing to the connection state after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Subscribe to connection state changes
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

The client unsubscribes from GATT protocol connection state change events. The `subscribeId` parameter is the subscription ID returned by the [`subscribeBLEConnectionStateChange`](#subscribebleconnectionstatechange) method.

Here is an example of unsubscribing from the connection state:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Call the connect interface to initiate a connection
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Subscribe to connection state changes
        this.listener = this.gattClient.subscribeBLEConnectionStateChange((result) => {
            console.log('connect changed:' + JSON.stringify(result))
        })
        // 4. Unsubscribe from connection state changes
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

The client subscribes to MTU (Maximum Transmission Unit) size change events. When the MTU changes, the `callback` function is automatically invoked. This interface synchronously returns a subscription ID used for unsubscribing.

Description of callback function parameter fields:
- `mtu`: MTU (Maximum Transmission Unit) size.

Here is an example of subscribing to MTU changes after a successful GATT connection:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
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

The client unsubscribes from MTU (Maximum Transmission Unit) size change events. The `subscribeId` parameter is the subscription ID returned by the [`subscribeBLEMtuChange`](#subscribeblemtuchange) method.

Here is an example of unsubscribing from MTU changes:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Construct gattClient instance. Please replace 'XX:XX:XX:XX:XX:XX' below with the device address you want to connect to
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Subscribe to MTU changes
        this.listener = this.gattClient.subscribeBLEMtuChange((mtu) => {
            console.log('mtu changed:' + mtu)
        })
        // 3. Unsubscribe from MTU changes
        if (this.gattClient && this.listener) {    
            this.gattClient.unsubscribeBLEMtuChange(this.listener)
            this.listener = null
        }
    },
}
```