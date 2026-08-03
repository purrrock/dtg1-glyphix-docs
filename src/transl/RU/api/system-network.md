# Сетевое состояние

## Импорт модуля

```js
import network from '@system.network';
```

## Определение интерфейсов

### `subscribe` <decl type="(callback: (status: NetworkState) => void): number" method/>

Прослушивание изменений сетевого состояния. Параметр `status` функции `callback` представляет собой новое [состояние сети](#networkstate). ID, возвращаемый данным методом, можно использовать для отмены подписки с помощью метода [`unsubscribe()`](#unsubscribe).

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Отмена прослушивания сетевого состояния, где `subscribeID` — это значение ID, возвращенное методом [`subscribe()`](#subscribe).

### `getType` <decl type="(): Promise<NetworkState>" method/>

Получение текущего сетевого состояния, возвращает значение [`NetworkState`](#networkstate).

## Определения типов

### `NetworkState`

Этот объект используется для представления текущего сетевого состояния, сигнатура типа выглядит следующим образом:

```ts
type NetworkState = {
  device: string; // Имя сетевого устройства
  type: string; // Тип сетевого устройства
  linkUp: boolean; // Включено ли сетевое устройство
  online: boolean; // Находится ли устройство в сети (есть ли доступ к интернету)
};
```

Обычно для проверки того, имеет ли устройство доступ в интернет, можно использовать свойство `online` объекта `NetworkState`.