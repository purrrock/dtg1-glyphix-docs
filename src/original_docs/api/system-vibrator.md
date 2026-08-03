# 震动

## 导入模块

``` js
import vibrator from '@system.vibrator'
```

## API

### `vibrate`
<decl method><pre>
(options: {
  mode: string
}): bool
</pre></decl> 

触发震动。`option` 参数的各字段功能为：
- `mode`：振动模式，`long` 表示长振动，`short` 表示短振动。默认值为 `long`。
