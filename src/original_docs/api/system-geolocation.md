# 地理位置

## 导入模块

```js
import geolocation from '@system.geolocation';
```

开发者需要在 [`manifest.json`](/framework/application/manifest.md#permissions) 文件中声明应用对 `watch.permission.LOCATION` 的访问权限。

## 接口定义

### `getLocation` 
<decl method><pre>
(options: {
  mode?: string
  timeout?: number
}): Promise&lt;Location>
</pre></decl>

单次获取当前位置经纬度，返回一个异步的[位置信息](#location)。

`options` 参数说明
- `mode` : 声明定位精度， `fine` 为精确定位， `coarse` 为模糊定位，默认值为  `coarse`
- `timeout` : 定位超时时间， 单位为 `ms` ，默认为 30000

### `subscribe` <decl type="(callback: (location: Location) => void): number" method/>

监听位置变化。 `callback` 的参数 `location` 为当前[位置信息](#location)，此方法返回的 ID 可使用 [`unsubscribe()`](#unsubscribe) 方法来解除监听。

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

取消监听位置变化。

## 类型定义

### `Location`

用于表示定位的位置信息数据。

```ts
type Location = {
  code: number; // 定位状态代码，表示当前位置信息是否有效
  msg: string; // 定位错误信息
  data: {
    // 位置信息的数据
    longitude: number; // 纬度值
    latitude: number; // 经度值
    coordType: string; // 坐标系类型，例如 'WGS84'、'GCJ02' 等
  };
};
```

`code` 字段的定位状态代码如下：

- `200`: 当前定位信息有效；
- `1002`: 当前未连接手机蓝牙网络
- `1300`: 手机无法获取定位服务
- `1301`: 手机未开启定位服务
- `1302`: 手机应用未授予定位权限
- `1399`: 未知错误
