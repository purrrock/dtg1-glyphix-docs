# 亮度管理

## 导入模块

``` js
import brightness from '@system.brightness'
```

## API

### `getValue` <decl type="(): number" method />

获取屏幕的亮度值，范围为 $[0, 1]$。

### `setValue` <decl type="(value: number): void" method />

设置屏幕的亮度值。`value` 的范围为 $[0, 1]$。

### `getMode` <decl type="(): string" method />

获取屏幕的亮度模式。

### `setMode` <decl type="(mode: number): void" method />

设置屏幕的亮度模式。设置 `number` 为 `0` 时，为标准模式，设置 `number` 为 $1$ 时，为自动模式。

### `setKeepScreenOn` <decl type="(mode: Boolean): void" method />

设置是否保持屏幕常亮。设置 `mode` 为 `true` 时，屏幕常亮，设置 `mode` 为 `false` 时，取消屏幕常亮。

### `wakeScreenOn`
<decl method><pre>
(options: { 
  screenOn: boolean, 
  timeout?: number,
}): void
</pre></decl>

点亮或熄灭屏幕。options 参数的各字段功能为：
- `screenOn`：是否点亮屏幕
- `timeout`：自动熄灭时间，不填则不限时间
