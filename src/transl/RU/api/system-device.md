# Информация об устройстве

## Импорт модуля

``` js
import device from '@system.device'
```

Разработчикам необходимо заявить о доступе приложения к权限 `watch.permission.DEVICE_INFO` в файле [`manifest.json`](/framework/application/manifest.md#permissions).

## Определение интерфейсов

### `getInfo`
<decl method><pre>
(): Promise<{
  brand: string,
  manufacturer: string,
  model: string,
  product: string,
  osType: string,
  osVersionName: string,
  platformVersionName: string,
  platformVersionCode: number,
  language: string,
  region: string,
  deviceName: string
}>
</pre></decl>

Получение базовой информации об устройстве. Значения полей возвращаемого объекта:
- `brand`: бренд устройства.
- `manufacturer`: производитель устройства.
- `model`: модель устройства.
- `product`: кодовое имя устройства.
- `osType`: название операционной системы.
- `osVersionName`: название версии операционной системы.
- `platformVersionName`: название версии платформы выполнения.
- `platformVersionCode`: номер версии платформы выполнения.
- `language`: системный язык.
- `region`: системный регион.
- `deviceName`: имя устройства.

### `getId`
<decl method><pre>
(types: ('device' | 'mac' | 'user' | 'advertising')[])
: Promise<{
  device?: string,
  mac?: string,
  user?: string,
  advertising?: string
}>
</pre></decl>

Пакетное получение информации об идентификаторах устройства. Параметр `types` задает категории запрашиваемой информации и представляет собой объект Array, состоящий из элементов `'device'`, `'mac'`, `'user'` или `'advertising'`. В зависимости от значений `types`, поля возвращаемого объекта имеют следующие значения:
- `type`: .
- `device`: уникальный идентификатор устройства, присутствует только в том случае, если `types` содержит элемент `'device'`.
- `mac`: MAC-адрес устройства, присутствует только в том случае, если `types` содержит элемент `'mac'`.
- `user`: уникальный идентификатор пользователя, присутствует только в том случае, если `types` содержит элемент `'user'`.
- `advertising`: уникальный рекламный идентификатор, присутствует только в том случае, если `types` содержит элемент `'advertising'`.

### `getDeviceId` <decl type="(): Promise<{deviceId: string}>" method />

Получение уникального идентификатора устройства.

### `getSerial` <decl type="(): Promise<{serial: string}>" method />

Получение серийного номера устройства.

### `getTotalStorage` <decl type="(): Promise<{totalStorage: number}>" method />

Получение общего объема памяти в байтах.

### `getAvailableStorage` <decl type="(): Promise<{availableStorage: number}>" method />

Получение доступного объема памяти в байтах.

::: tip
Значения, возвращаемые методами `getTotalStorage()` и `getAvailableStorage()` на эмуляторе, могут быть неточными и не изменяются по мере изменения свободного пространства памяти.
:::

### `screenWidth` <decl type="number" get />

Ширина экрана устройства в пикселях.

### `screenHeight` <decl type="number" get />

Высота экрана устройства в пикселях.

### `screenDensity` <decl type="number" get />

Плотность пикселей экрана устройства в $\rm PPI$.

### `screenShape` <decl type="'rect' | 'circle'" get />

Форма экрана устройства, возможные значения:
- `'rect'`: устройство имеет прямоугольный экран.
- `'circle'`: устройство имеет круглый экран.

### `memoryProfile` <decl type="number" get />

Получение свойства профиля памяти устройства. Это свойство представляет собой JavaScript API версию свойства медиа-запроса [`memory-profile`](/framework/render/media-query.md#memory-profile), подробности см. в документации по медиа-запросам.

В отличие от свойства медиа-запроса `memory-profile`, значение свойства `memoryProfile` представляет собой целое число, а единица измерения фиксирована в $\rm KiB$.