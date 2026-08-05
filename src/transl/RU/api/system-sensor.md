# Датчики

## Импорт модуля

```js
import sensor from '@system.sensor';
```

Разработчикам необходимо объявить разрешение на доступ приложения к `watch.permission.ACCESS_SENSORS` в файле [`manifest.json`](/framework/application/manifest.md#permissions).

## Определение интерфейсов

### `subscribeAccelerometer`
<decl method><pre>
(options: { 
  interval?: 'game' | 'ui' | 'normal', 
  callback: (data: AccelerometerValue) => void,
}): number
</pre></decl>

Прослушивание изменений данных акселерометра. Назначение полей параметра `options`:
- `interval`：частота опроса, по умолчанию `'normal'`, возможные значения:
  - `'game'`：игровой режим, частота 20 мс/раз;
  - `'ui'`：режим пользовательского интерфейса, частота 60 мс/раз;
  - `'normal'`：обычный режим, частота 200 мс/раз.
- `callback`：обратный вызов при обновлении данных акселерометра. Сигнатура типа данных акселерометра `AccelerometerValue`:
  ``` ts
  type AccelerometerValue = {
    x: number   // ускорение по оси x
    y: number   // ускорение по оси y
    z: number   // ускорение по оси z
  }
  ```

Пример:
```js
const id = sensor.subscribeAccelerometer({
  interval: 'normal',
  callback(ret) {
    console.log(`gyroscope data, x = ${ret.x}, y = ${ret.y}, z = ${ret.z}`)
  }
})

// Отмена подписки
sensor.unsubscribeAccelerometer(id)
```

### `unsubscribeAccelerometer` <decl type="(id: number): void" method/>

Отмена прослушивания данных акселерометра. Параметр `id` — это идентификатор подписки, возвращаемый методом [`subscribeAccelerometer`](#subscribeaccelerometer).

### `subscribeCompass`
<decl method><pre>
(options: { 
  callback: (data: CompassValue) => void,
}): number
</pre></decl>

Прослушивание изменений данных компаса. Возвращает идентификатор подписки, который используется для ее отмены. Назначение полей параметра `options`:
- `callback`：обратный вызов при изменении данных компаса.

Сигнатура `CompassValue`:
``` ts
  type CompassValue = {
    direction: number   // угол между осью y и магнитным северным полюсом (в радианах)
    accuracy: number    // точность
  }
```
- `direction`：угол в радианах между осью Y устройства и магнитным северным полюсом Земли. Диапазон значений: $(-\pi,\pi]$, где:
  - `0`：направление на север
  - $\pi$` / 2` (около 1.57)：направление на восток
  - $\pi$ (около 3.14)：направление на юг
  - -$\pi$` / 2` (около -1.57)：направление на запад
- `accuracy`：уровень точности данных компаса
  - `3`：высокая точность
  - `2`：средняя точность
  - `1`：низкая точность
  - `0`：недоступно (причина неизвестна)
  - `-1`：недоступно (датчик потерял соединение)

Пример:
```js
const id = sensor.subscribeCompass({
  callback(ret) {
    console.log(`direction=${ret.direction}, accuracy=${ret.accuracy}`)
  }
})

// Отмена подписки
sensor.unsubscribeCompass(id)
```

### `unsubscribeCompass`<decl type="(id: number): void" method/>

Отмена прослушивания данных компаса. Параметр `id` — это идентификатор подписки, возвращаемый методом [`subscribeCompass`](#subscribecompass).

### `calibrationCompass` <decl type="(): Promise<void>" method/>

Запуск процесса калибровки компаса. Когда точность компаса низкая, направьте пользователя выполнить действия и вызовите этот метод для калибровки компаса.

Функция возвращает объект Promise без результата, который разрешается после завершения калибровки системой.

### `getCompassValue` <decl type="(): Promise<CompassValue>" method/>

Получение текущих данных компаса. Возвращает асинхронный результат — объект Promise, содержащий направление компаса и информацию о точности типа `CompassValue`.

### `subscribeStepCounter`
<decl method><pre>
(options: { 
  callback: (data: StepCounterValue) => void,
}): number
</pre></decl>

Прослушивание изменений данных шагомера. Назначение полей параметра `options`:
- `callback`：обратный вызов при изменении данных шагов. Сигнатура типа данных шагомера `StepCounterValue`:
  ``` ts
  type StepCounterValue = {
    steps: number     // текущее количество шагов (начинается с 0 после перезагрузки)
  }
  ```

Пример:
```js
const id = sensor.subscribeStepCounter({
  callback(ret) {
    console.log(`steps=${ret.steps}`)
  }
})

// Отмена подписки
sensor.unsubscribeStepCounter(id)
```

### `unsubscribeStepCounter` <decl type="(id: number): void" method/>

Отмена прослушивания данных шагомера. Параметр `id` — это идентификатор подписки, возвращаемый методом [`subscribeStepCounter`](#subscribestepcounter).

### `subscribeOnBodyState`
<decl method><pre>
(options: { 
  callback: (data: OnBodyStateValue) => void,
}): number
</pre></decl>

Прослушивание изменений состояния ношения устройства. Назначение полей параметра `options`:
- `callback`：обратный вызов при изменении состояния ношения устройства. Сигнатура типа данных состояния ношения `OnBodyStateValue`:
  ``` ts
  type OnBodyStateValue = {
    value: boolean  // надето ли устройство
  }
  ```

Пример:
```js
const id = sensor.subscribeOnBodyState({
  callback(ret) {
    console.log(`onBody=${ret.value}`)
  }
})

// Отмена подписки
sensor.unsubscribeOnBodyState(id)
```

### `unsubscribeOnBodyState` <decl type="(): void" method/>

Отмена прослушивания состояния ношения. Параметр `id` — это идентификатор подписки, возвращаемый методом [`subscribeOnBodyState`](#subscribeonbodystate).

### `getOnBodyState` <decl type="(): Promise<OnBodyStateValue>" method/>

Получение текущего состояния ношения устройства.

Пример:
``` js
async function getOnBodyStat() {
  const data = await sensor.getOnBodyState()
  console.log(`onBody: ${data.value}`)
}
```

### `subscribeGyroscope`
<decl method><pre>
(options: { 
  callback: (data: GyroscopeValue) => void,
}): number
</pre></decl>

Прослушивание изменений данных гироскопа. Назначение полей параметра `options`:
- `callback`：обратный вызов при изменении данных гироскопа. Сигнатура типа данных гироскопа `GyroscopeValue`:
  ``` ts
  type GyroscopeValue = {
    x: number   // угловая скорость по оси x
    y: number   // угловая скорость по оси y
    z: number   // угловая скорость по оси z
  }
  ```

Пример:
```js
const id = sensor.subscribeGyroscope({
  callback(ret) {
    console.log(`gyroscope data, x = ${ret.x}, y = ${ret.y}, z = ${ret.z}`)
  }
})

// Отмена подписки
sensor.unsubscribeGyroscope(id)
```

### `unsubscribeGyroscope` <decl type="(id: number): void" method/>

Отмена прослушивания данных гироскопа. Параметр `id` — это идентификатор подписки, возвращаемый методом [`subscribeGyroscope`](#subscribegyroscope).

### `subscribeBarometer`
<decl method><pre>
(options: { 
  callback: (data: BarometerValue) => void,
}): number
</pre></decl>

Прослушивание изменений данных датчика атмосферного давления. Назначение полей параметра `options`:
- `callback`：обратный вызов при изменении данных давления. Сигнатура типа данных давления `BarometerValue`:
  ``` ts
  type BarometerValue = {
    pressure: number   // значение атмосферного давления, единица: Па (Pa)
  }
  ```

Пример:
```js
sensor.subscribeBarometer({
  callback(ret) {
    console.log("get barometer:", ret.pressure)
  }
})

// Отмена подписки
sensor.unsubscribeBarometer(id)
```

### `unsubscribeBarometer` <decl type="(id: number): void" method/>

Отмена прослушивания барометра. Параметр `id` — это идентификатор подписки, возвращаемый методом [`subscribeBarometer`](#subscribebarometer).

### `subscribeWristLift`
<decl method><pre>
(options: { 
  callback: () => void,
}): number
</pre></decl>

Прослушивание события поднятия запястья. Назначение полей параметра `options`:
- `callback`：обратный вызов для прослушивания события поднятия запястья.

Пример:
```js
const id = sensor.subscribeWristLift({
  callback: () => {
    console.log('wrist lift')
  }
});

// Отмена подписки
sensor.unsubscribeWristLift(id)
```

### `unsubscribeWristLift` <decl type="(id: number): void" method/>

Отмена прослушивания поднятия запястья. Параметр `id` — это идентификатор подписки, возвращаемый методом [`subscribeWristLift()`](#subscribewristlift).

## Ограничения использования

Если текущее устройство не поддерживает соответствующие возможности датчиков, вызов интерфейса приведет к выбросу исключения, и прослушивание не будет активировано.
Пример лога с информацией об исключении: `the device does not support accelerometer sensor`

Пример перехвата исключения:

```js
try {
  const id = sensor.subscribeCompass({
    callback(ret) {
      console.log(`direction=${ret.direction}, accuracy=${ret.accuracy}`)
    }
  })
} catch (e) {
  console.error(e.message)
}
```

## Рекомендации

Рекомендуется своевременно отменять подписку, когда данные датчиков больше не нужны. В частности, следует отменять подписку при уничтожении страницы (в обратном вызове `onDestroy`), чтобы избежать излишнего потребления ресурсов и разряда батареи.