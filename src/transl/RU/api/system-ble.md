# Модуль Bluetooth с низким энергопотреблением (BLE)

Этот модуль предоставляет возможности Bluetooth на базе технологии Bluetooth Low Energy (BLE). Он поддерживает запуск BLE-сканирования, а также подключение и передачу данных на основе протокола общего профиля атрибутов (Generic Attribute Profile, GATT) (в настоящее время поддерживается только создание `GattClient`, создание `GattServer` пока не поддерживается).

::: warning
Большинство API в `@system.bluetooth.ble` являются [асинхронными операциями Promise](#Promise异步操作), что принципиально отличается от синхронного ввода-вывода (IO). Пожалуйста, обязательно усвойте основные концепции асинхронного программирования и ознакомьтесь с использованием Promise и `async/await`.
:::

## Импорт модуля

``` js
import ble from '@system.bluetooth.ble'
```

## Права (Permissions)

::: tip
Для использования этого модуля приложение должно запросить разрешение: `watch.permission.BLUETOOTH` 
:::

## Определение интерфейсов ble

### `ResultCode`

Перечисление результатов, возвращаемых в Promise:

- `0`: Успешно;
- `1`: BLE не включен;
- `2`: Ошибка параметров;
- `3`: Не удалось включить BLE;
- `4`: Нет доступных адаптеров Bluetooth;
- `5`: Ошибка подключения;
- `6`: Ошибка отключения;
- `7`: Установка этого свойства пока не поддерживается;
- `8`: Неизвестная ошибка;

### `startBLEScan`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

Запуск сканирования с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает [`ResultCode`](#resultcode), используемый для определения успешности или неуспешности выполнения.

Ниже приведен пример запуска сканирования:
```ts
import ble from '@system.bluetooth.ble'
export default {
    async scanStart() {
        // Запуск сканирования
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

Остановка сканирования с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает [`ResultCode`](#resultcode), используемый для определения успешности или неуспешности выполнения.

Ниже приведен пример остановки сканирования:
```ts
import ble from '@system.bluetooth.ble'
export default {
    async scanStop() {
        // Остановка сканирования
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

Этот объект используется для представления отправленных результатов сканирования, сигнатура его типа выглядит следующим образом:

```ts
/**
 * Определение объекта результатов сканирования
 */
type ScanResult = {
    deviceId: string; // Идентификатор устройства (например, "AA:BB:CC:DD:EE:FF")
    rssi: number; // Уровень сигнала в дБм (dBm)
    data: ArrayBuffer; // Исходные данные широковещательного пакета
    deviceName: string; // Имя устройства (если имеется)
    connectable: boolean; // Возможность подключения, true означает, что подключение возможно
}
```

### `getBLEScanResults`
<decl method><pre>
(): Promise&lt;Array&lt;ScanResult&gt;&gt;
</pre></decl>

Запрос результатов сканирования с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает массив объектов [`ScanResult`](#scanresult) (т.е. Array&lt;[`ScanResult`](#scanresult)&gt;).

::: warning
Поскольку фоновый адаптер Bluetooth является синглтоном, могут возникать ситуации, когда несколько приложений работают с Bluetooth-устройствами одновременно. Возможен такой сценарий: Приложение А запускает сканирование на некоторое время, после чего Приложение Б снова запускает сканирование — в этом случае результаты сканирования, отслеживаемые Приложением Б, могут быть неполными. Чтобы справиться с этой ситуацией, рекомендуется всем приложениям сразу после запуска сканирования запрашивать текущие результаты сканирования.
:::

Ниже приведен пример запроса результатов сканирования после его запуска:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        scanList: [],
    },
    async scanStart() {
        // Запуск сканирования
        await ble.startBLEScan().then(async (result) => {
            console.dir('startBLEScan success')
            // Запрос результатов сканирования
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

Подписка на изменение статуса сканирования с использованием асинхронного Callback. Когда статус сканирования изменяется, функция обратного вызова `callback` вызывается автоматически. Этот интерфейс синхронно возвращает ID подписки, который используется для отмены подписки.

Описание полей параметров функции обратного вызова:
- `scan`: Текущий статус сканирования. true означает, что сканирование выполняется, false — сканирование остановлено.

Ниже приведен пример подписки на изменение статуса сканирования:
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

Отмена подписки на изменение статуса сканирования. Параметр `subscribeId` — это ID подписки, возвращенный методом [`subscribeScanStatus`](#subscribescanstatus).

Ниже приведен пример отмены подписки на изменение статуса сканирования:
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

Подписка на событие обнаружения устройств при сканировании с использованием асинхронного Callback. При обнаружении нового устройства функция обратного вызова `callback` вызывается автоматически. Этот интерфейс синхронно возвращает ID подписки, используемый для отмены подписки.

::: tip
Результаты сканирования сообщаются в инкрементном режиме: устройство обнаруживается — результат передается. После прослушивания этого события пользователю необходимо самостоятельно сохранять результаты сканирования.
:::

Описание полей параметров функции обратного вызова:
- [`ScanResult`](#scanresult): Объект найденного нового устройства.

Ниже приведен пример подписки на событие обнаружения устройств:
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

Отмена подписки на событие обнаружения устройств. Параметр `subscribeId` — это ID подписки, возвращенный методом [`subscribeBLEDeviceFind`](#subscribebledevicefind).

Ниже приведен пример отмены подписки на событие обнаружения устройств:
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

Этот объект используется для представления клиентского объекта (Client) в протоколе GATT, сигнатура его типа выглядит следующим образом:

```ts
/**
 * Определение типа объекта GattClientDevice
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

Создание экземпляра [`GattClientDevice`](#gattclientdevice), представляющего клиентскую сторону в GATT-соединении. Этот интерфейс синхронно возвращает экземпляр [`GattClientDevice`](#gattclientdevice).

 - С помощью этого экземпляра можно управлять поведением клиента, например, вызывать [`connect`](#connect) для инициирования подключения к удаленному устройству, или вызывать [`getServices`](#getservices) для получения всех сервисов, поддерживаемых удаленным устройством.
 - Необходимый для создания этого экземпляра `deviceId` (адрес устройства) представляет адрес серверного устройства. Адрес серверного устройства можно получить через интерфейс [`startBLEScan`](#startblescan), при этом необходимо убедиться, что BLE-вещание серверного устройства доступно для подключения.

Ниже приведен пример создания экземпляра [`GattClientDevice`](#gattclientdevice):
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    create() {
        // Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = ble.createGattClientDevice('XX:XX:XX:XX:XX:XX')
    },
}
```

## Определение интерфейсов GattClientDevice

### `connect`
<decl method><pre>
(): Promise&lt;number&gt;
</pre></decl>

Клиентская сторона инициирует GATT-подключение к серверному Bluetooth-устройству с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает [`ResultCode`](#resultcode), используемый для определения успешности или неуспешности выполнения.

 - Перед использованием методов этого класса необходимо создать его экземпляр с помощью метода [`createGattClientDevice`](#creategattclientdevice).
 - Создавая различные экземпляры этого класса, можно управлять несколькими GATT-соединениями.

Ниже приведен пример инициирования GATT-подключения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async connect() {
        // Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
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

Клиентская сторона разрывает GATT-подключение с серверным Bluetooth-устройством с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает [`ResultCode`](#resultcode), используемый для определения успешности или неуспешности выполнения.

Ниже приведен пример разъединения GATT-подключения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        address: null,
    },
    gattClient: null,
    async connect() {
        // Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
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

Закрытие экземпляра клиентской стороны с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает [`ResultCode`](#resultcode), используемый для определения успешности или неуспешности выполнения.

### `getDeviceName`
<decl method><pre>
(): Promise&lt;string&gt;
</pre></decl>

Получение клиентом имени удаленного BLE-устройства с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает имя устройства типа &lt;string&gt;.

Ниже приведен пример получения имени устройства после успешного установления GATT-соединения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async name() {
        let clientName = 'N/A'
        // Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
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

Этот объект используется для представления структуры сервиса GATT, сигнатура его типа выглядит следующим образом:

```ts
/**
 * Определение структуры GATT-сервиса, может содержать несколько характеристик BLECharacteristic и другие зависимые сервисы.
 */
type GattService = {
    serviceUuid: string; // UUID сервиса, идентифицирует GATT-сервис. Например: 00001888-0000-1000-8000-00805f9b34fb.
    isPrimary: boolean; // Является ли основным сервисом. true означает основной сервис, false — вторичный.
    characteristics: Array<BLECharacteristic>; // Список характеристик, содержащихся в текущем сервисе.
    includeServices: Array<GattService>; // Другие сервисы, от которых зависит текущий сервис.
}
```

### `getServices`
<decl method><pre>
(): Promise&lt;Array&lt;GattService&gt;&gt;
</pre></decl>

Получение клиентом всех сервисов BLE-устройства (обнаружение сервисов) с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает массив типа Array&lt;[`GattService`](#gattservice)&gt;, содержащий все сервисы.

Ниже приведен пример получения всех сервисов устройства после успешного установления GATT-соединения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    async onShow() {
        // Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
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

Этот объект используется для представления свойств, поддерживаемых характеристикой GATT, сигнатура его типа выглядит следующим образом:

```ts
/**
 * Описывает свойства, поддерживаемые характеристикой GATT. Определяет, как содержимое характеристики и дескрипторы могут использоваться и запрашиваться.
 */
type GattProperties = {
    write: boolean; // Поддерживает ли характеристика операцию записи. true означает поддержку, причем при записи требуется отправить ответное подтверждение удаленному устройству; false — не поддерживает.
    writeNoResponse: boolean; // Поддерживает ли характеристика операцию записи. true означает поддержку, причем при записи отвечать удаленному устройству не требуется; false — не поддерживает.
    read: boolean; // Поддерживает ли характеристика операцию чтения. true означает поддержку, false — не поддерживает.
    notify: boolean; // Поддерживает ли характеристика отправку уведомлений об изменении содержимого удаленному устройству. true означает поддержку, причем удаленному устройству не требуется отправлять подтверждение; false — не поддерживает.
    indicate: boolean; // Поддерживает ли характеристика отправку индикации об изменении содержимого удаленному устройству. true означает поддержку, удаленному устройству требуется отправить подтверждение; false — не поддерживает.
    broadcast: boolean; // Поддерживает ли характеристика передачу сервером в качестве содержимого широковещательного сообщения. true означает поддержку, сервер может передавать содержимое характеристики в широковещательном пакете в виде ServiceData; false — не поддерживает.
    authenticatedSignedWrite: boolean; // Поддерживает ли характеристика операцию подписанной записи, заменяя процесс шифрования проверкой подписи содержимого записи. true означает поддержку, false — не поддерживает.
    extendedProperties: boolean; // Имеет ли характеристика расширенные свойства. true означает наличие расширенных свойств, false — отсутствие.
}
```

### `BLECharacteristic`

Этот объект используется для представления характеристики GATT, сигнатура его типа выглядит следующим образом:

```ts
/**
 * Определение типа характеристики GATT, является основной единицей данных сервиса GattService
 */
type BLECharacteristic = {
    serviceUuid: string; // UUID сервиса, которому принадлежит характеристика, например: 00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // UUID характеристики, например: 00002a11-0000-1000-8000-00805f9b34fb
    characteristicValue: ArrayBuffer; // Содержимое данных характеристики, используется при чтении и записи данных
    descriptors: Array<BLEDescriptor>; // Список дескрипторов, содержащихся в характеристике
    properties: GattProperties; // Свойства, поддерживаемые характеристикой
    characteristicValueHandle: number; // Уникальный дескриптор-идентификатор (handle) характеристики. Когда BLE-устройство сервера предоставляет несколько характеристик с одинаковым UUID, этот хэндл позволяет различать их
}
```

### `readCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic): Promise&lt;BLECharacteristic&gt;
</pre></decl>

Клиентская сторона считывает данные из указанной характеристики сервера с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает объект типа [`BLECharacteristic`](#blecharacteristic).

 - В этот интерфейс необходимо передать объект типа [`BLECharacteristic`](#blecharacteristic), указывающий, какую характеристику нужно прочитать.

Ниже приведен пример чтения данных из указанной характеристики после успешного установления GATT-соединения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async read() {
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Вызов интерфейса connect для установления соединения
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Обнаружение сервисов, получение характеристики, которую необходимо прочитать: characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // В тесте предпринимается попытка прочитать первую характеристику первого сервиса; если нужно прочитать другие характеристики, измените код самостоятельно
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Чтение указанной характеристики
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

Перечисление режимов записи характеристик:

- `1`: После записи характеристики удаленное Bluetooth-устройство должно отправить ответное подтверждение.
- `2`: После записи характеристики удаленному Bluetooth-устройству не требуется отправлять ответ.

### `writeCharacteristicValue`
<decl method><pre>
(characteristic: BLECharacteristic, writeType: GattWriteType): Promise&lt;number&gt;
</pre></decl>

Клиентская сторона записывает данные в указанную характеристику сервера с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает [`ResultCode`](#resultcode), используемый для определения успешности или неуспешности выполнения.

 - В этот интерфейс необходимо передать объект типа [`BLECharacteristic`](#blecharacteristic), указывающий, в какую характеристику нужно произвести запись.
 - В этот интерфейс необходимо передать значение перечисления [`GattWriteType`](#gattwritetype), указывающее способ записи данных.

Ниже приведен пример записи данных в указанную характеристику после успешного установления GATT-соединения:
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
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Вызов интерфейса connect для установления соединения
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Обнаружение сервисов, получение характеристики для работы: characteristic
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // В тесте предпринимается попытка работы только с первой характеристикой первого сервиса; если нужно работать с другими, измените код самостоятельно
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Запись в указанную характеристику
        if (this.gattClient && this.characteristic) {
            // Генерация ArrayBuffer заданной длины, содержащего случайные числа
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

Этот объект представляет дескриптор GATT, его определение типа выглядит следующим образом:

```ts
/**
 * Определение типа дескриптора GATT, является единицей данных характеристики BLECharacteristic, используется для описания дополнительной информации и свойств характеристики
 */
type BLEDescriptor = {
    serviceUuid: string; // UUID сервиса, которому принадлежит характеристика, например: 00001888-0000-1000-8000-00805f9b34fb
    characteristicUuid: string; // UUID характеристики, например: 00002a11-0000-1000-8000-00805f9b34fb
    descriptorUuid: string; // UUID дескриптора, например: 00002902-0000-1000-8000-00805f9b34fb
    descriptorValue: ArrayBuffer; // Содержимое данных дескриптора, используется при чтении и записи данных
    descriptorHandle: number; // Уникальный хэндл дескриптора. Когда BLE-устройство сервера предоставляет несколько дескрипторов с одинаковым UUID, этот хэндл позволяет различать их.
}
```

### `readDescriptorValue`
<decl method><pre>
(descriptor: BLEDescriptor): Promise&lt;BLEDescriptor&gt;
</pre></decl>

Клиентская сторона считывает данные из указанного дескриптора сервера с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает объект типа [`BLEDescriptor`](#bledescriptor).

 - В этот интерфейс необходимо передать объект типа [`BLEDescriptor`](#bledescriptor), указывающий, какой дескриптор нужно прочитать.

Ниже приведен пример чтения данных из указанного дескриптора после успешного установления GATT-соединения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    descriptor: null,
    async read() {
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Вызов интерфейса connect для установления соединения
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Обнаружение сервисов, получение характеристики, которую необходимо прочитать
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        console.dir("gatt client found:" + JSON.stringify(this.services))
        if (this.services.length > 0) {
            // В тесте предпринимается попытка прочитать первый дескриптор первой характеристики первого сервиса; если нужно прочитать другие, измените код самостоятельно
            // Обратите внимание, что не каждая характеристика имеет дескрипторы. Здесь вы можете самостоятельно настроить выбор сервисов, имеющих дескрипторы и права на чтение/запись для тестирования
            this.descriptor = this.services[0].characteristics[0].descriptors[0];
        }
        // 4. Чтение указанного дескриптора
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

Клиентская сторона записывает данные в указанный дескриптор сервера с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает [`ResultCode`](#resultcode), используемый для определения успешности или неуспешности выполнения.

 - В этот интерфейс необходимо передать объект типа [`BLEDescriptor`](#bledescriptor), указывающий, в какой дескриптор нужно произвести запись.

Ниже приведен пример записи данных в дескриптор после успешного установления GATT-соединения:
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
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Вызов интерфейса connect для установления соединения
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Обнаружение сервисов, получение характеристики для чтения
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        console.dir("gatt client found:" + JSON.stringify(this.services))
        if (this.services.length > 0) {
            // В тесте предпринимается попытка работы только с первым дескриптором первой характеристики первого сервиса; если нужно работать с другими, измените код самостоятельно
            // Обратите внимание, что не каждая характеристика имеет дескрипторы. Здесь вы можете настроить выбор сервисов, имеющих дескрипторы и права на чтение/запись
            this.descriptor = this.services[0].characteristics[0].descriptors[0];
        }
        // 4. Запись в указанный дескриптор
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

Клиентская сторона получает уровень сигнала линии связи GATT (Received Signal Strength Indication, RSSI) с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает уровень сигнала типа &lt;number&gt;, единица измерения: дБм (dBm).

Ниже приведен пример получения уровня сигнала устройства после успешного установления GATT-соединения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async rssi() {
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
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

Клиентская сторона получает размер MTU (максимального размера блока передачи данных) линии связи GATT с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает длину типа &lt;number&gt;, единица измерения: байт (byte).

Ниже приведен пример получения размера MTU линии связи GATT после успешного установления соединения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    async mtu() {
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
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

Клиентская сторона согласовывает с сервером размер MTU (максимального размера блока передачи данных) с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает [`ResultCode`](#resultcode), используемый для определения успешности или неуспешности выполнения.

### `setCharacteristicChangeNotification`
<decl method><pre>
(characteristic: BLECharacteristic, enable: boolean): Promise&lt;number&gt;
</pre></decl>

Клиентская сторона включает или отключает возможность получения уведомлений об изменении содержимого характеристики от сервера с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает [`ResultCode`](#resultcode), используемый для определения успешности или неуспешности выполнения.

 - В этот интерфейс необходимо передать объект типа [`BLECharacteristic`](#blecharacteristic), указывающий, с какой характеристикой нужно произвести действие.
 - В этот интерфейс необходимо передать булево значение (`boolean`), указывающее на включение или выключение уведомлений об изменении содержимого: `true` — включить, `false` — выключить.

Ниже приведен пример включения уведомлений об изменении характеристики после успешного установления GATT-соединения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async notify() {
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Вызов интерфейса connect для установления соединения
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Обнаружение сервисов, получение характеристики для чтения
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // В тесте предпринимается попытка работы только с первой характеристикой первого сервиса; если нужно работать с другими, измените код самостоятельно
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Действие с указанной характеристикой
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeNotification(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Notification success')
                } else {
                    console.log('Данная характеристика не разрешает включение прослушивания, ResultCode:' + result);
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

Клиентская сторона включает или отключает возможность получения индикаций об изменении содержимого характеристики от сервера с использованием асинхронного callback-вызова Promise. Этот интерфейс асинхронно возвращает [`ResultCode`](#resultcode), используемый для определения успешности или неуспешности выполнения.

 - В этот интерфейс необходимо передать объект типа [`BLECharacteristic`](#blecharacteristic), указывающий, с какой характеристикой нужно произвести действие.
 - В этот интерфейс необходимо передать булево значение (`boolean`), указывающее на включение или выключение индикаций об изменении содержимого: `true` — включить, `false` — выключить.

Ниже приведен пример включения индикаций об изменении характеристики после успешного установления GATT-соединения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {
        services: [],
    },
    gattClient: null,
    characteristic: null,
    async indication() {
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Вызов интерфейса connect для установления соединения
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Обнаружение сервисов, получение характеристики для чтения
        await this.gattClient.getServices().then((result) => {
            this.services = result;
        }).catch((error) => {
            console.dir('gatt get services error: ' + JSON.stringify(error))
        });
        if (this.services.length > 0) {
            // В тесте предпринимается попытка работы только с первой характеристикой первого сервиса; если нужно работать с другими, измените код самостоятельно
            this.characteristic = this.services[0].characteristics[0];
        }
        // 4. Запись в указанную характеристику
        if (this.gattClient && this.characteristic) {
            await this.gattClient.setCharacteristicChangeIndication(this.characteristic, true).then((result) => {
                if (result === 0) {
                    console.log('set characteristic Indication success')
                } else {
                    console.log('Данная характеристика не разрешает включение прослушивания, ResultCode:' + result);
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

Клиентская сторона подписывается на событие изменения характеристики сервера. Когда характеристика изменяется, функция обратного вызова `callback` вызывается автоматически. Этот интерфейс синхронно возвращает ID подписки, используемый для отмены подписки.

Описание полей параметров функции обратного вызова:
- [`BLECharacteristic`](#blecharacteristic): Объект изменившейся характеристики.

Ниже приведен пример включения индикаций изменения характеристики после успешного установления GATT-соединения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Вызов интерфейса connect для установления соединения
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Подписка на изменение характеристики
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

Клиентская сторона отменяет подписку на событие изменения характеристики сервера. Параметр `subscribeId` — это ID подписки, возвращенный методом [`subscribeBLECharacteristicChange`](#subscribeblecharacteristicchange).

Ниже приведен пример включения индикаций изменения характеристики после успешного установления GATT-соединения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Вызов интерфейса connect для установления соединения
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Отмена подписки на изменение характеристики
        if (this.listener) {
            this.gattClient.unsubscribeBLECharacteristicChange(this.listener)
            this.listener = null
        }
    },
}
```

### `ConnectionState`

Перечисление состояний подключения Bluetooth:

- `0`: Отключено
- `1`: Подключение...
- `2`: Подключено
- `3`: Отключение... 

### `GattDisconnectReason`

Перечисление причин разрыва связи GATT:

- `0`: Причина недоступна
- `1`: Тайм-аут подключения
- `2`: Удаленное устройство инициативно разорвало соединение
- `3`: Локальное устройство инициативно разорвало соединение
- `4`: Неизвестная причина разрыва соединения

### `BLEConnectionChangeState`

Этот объект используется для представления состояния подключения Bluetooth, сигнатура его типа выглядит следующим образом:

```ts
/**
 * Определение типа состояния подключения Bluetooth
 */
type BLEConnectionChangeState = {
    deviceId: string; // Идентификатор устройства (например, "AA:BB:CC:DD:EE:FF")
    state: ConnectionState; // Состояние подключения Bluetooth
    reason: GattDisconnectReason; // Причина разрыва линии связи GATT
}
```

### `subscribeBLEConnectionStateChange` 
<decl method><pre>
(callback: Callback(connectionChangeState: BLEConnectionChangeState) => void): number
</pre></decl>

Клиентская сторона подписывается на событие изменения состояния подключения по протоколу GATT. Когда состояние подключения изменяется, функция обратного вызова `callback` вызывается автоматически. Этот интерфейс синхронно возвращает ID подписки, используемый для отмены подписки.

Описание полей параметров функции обратного вызова:
- [`BLEConnectionChangeState`](#bleconnectionchangestate): Состояние подключения.

Ниже приведен пример подписки на состояние подключения после успешного установления GATT-соединения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Вызов интерфейса connect для установления соединения
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Подписка на изменение состояния подключения
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

Клиентская сторона отменяет подписку на событие изменения состояния подключения по протоколу GATT. Параметр `subscribeId` — это ID подписки, возвращенный методом [`subscribeBLEConnectionStateChange`](#subscribebleconnectionstatechange).

Ниже приведен пример отмены подписки на состояние подключения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Вызов интерфейса connect для установления соединения
        await this.gattClient.connect().then(async (result) => {
            if (result == 0) {
                console.dir('connect success')
            } else {
                console.dir('connect failed:' + JSON.stringify(result))
            }
        }).catch((error) => {
            console.dir('connect error:' + JSON.stringify(error))
        })
        // 3. Подписка на изменение состояния подключения
        this.listener = this.gattClient.subscribeBLEConnectionStateChange((result) => {
            console.log('connect changed:' + JSON.stringify(result))
        })
        // 4. Отмена подписки на изменение состояния подключения
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

Клиентская сторона подписывается на событие изменения размера MTU (максимального размера блока передачи данных). Когда MTU изменяется, функция обратного вызова `callback` вызывается автоматически. Этот интерфейс синхронно возвращает ID подписки, используемый для отмены подписки.

Описание полей параметров функции обратного вызова:
- mtu: Размер MTU (максимального размера блока передачи данных).

Ниже приведен пример подписки на изменение MTU после успешного установления GATT-соединения:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async listen() {
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Подписка на изменение MTU
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

Клиентская сторона отменяет подписку на событие изменения размера MTU (максимального размера блока передачи данных). Параметр `subscribeId` — это ID подписки, возвращенный методом [`subscribeBLEMtuChange`](#subscribeblemtuchange).

Ниже приведен пример отмены подписки на изменение MTU:
```ts
import ble from '@system.bluetooth.ble'
export default {
    data: {

    },
    gattClient: null,
    listener: null,
    async unlisten() {
        // 1. Создание экземпляра gattClient. Пожалуйста, замените следующее 'XX:XX:XX:XX:XX:XX' на адрес подключаемого устройства
        this.gattClient = getGattClient('XX:XX:XX:XX:XX:XX');
        // 2. Подписка на изменение MTU
        this.listener = this.gattClient.subscribeBLEMtuChange((mtu) => {
            console.log('mtu changed:' + mtu)
        })
        // 3. Отмена подписки на изменение MTU
        if (this.gattClient && this.listener) {    
            this.gattClient.unsubscribeBLEMtuChange(this.listener)
            this.listener = null
        }
    },
}
```