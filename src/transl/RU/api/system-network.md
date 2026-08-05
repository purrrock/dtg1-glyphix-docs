# Состояние сети

## Импорт модуля

```js
import network from '@system.network';
```

## Определение интерфейсов

### `subscribe` <decl type="(callback: (status: NetworkState) => void): number" method/>

Прослушивание изменений состояния сети. Параметр `status` функции `callback` представляет собой новое [состояние сети](#networkstate). ID, возвращаемый этим методом, можно использовать в методе [`unsubscribe()`](#unsubscribe) для отмены подписки.

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Отмена прослушивания состояния сети. `subscribeID` — это значение ID, возвращаемое методом [`subscribe()`](#subscribe).

### `getType` <decl type="(): Promise<NetworkState>" method/>

Получение текущего состояния сети, возвращает значение [`NetworkState`](#networkstate).

## Определения типов

### `NetworkState`

Этот объект используется для представления текущего состояния сети, сигнатура типа выглядит следующим образом:

```ts
type NetworkState = {
  device: string; // Имя сетевого устройства
  type: string; // Тип сетевого устройства
  linkUp: boolean; // Включено ли сетевое устройство
  online: boolean; // В сети ли устройство (доступен ли интернет)
};
```

Обычно для проверки подключения устройства к интернету используется свойство `online` объекта `NetworkState`.