# 日历

## 导入模块

``` js
import calendar from '@system.calendar'
```

## 接口定义

### `getLunar` <decl method type="(date: Date): LunarDate" />

获取一个 `Date` 对象的农历日期信息，返回 [`LunarDate`](#lunardate) 类型的农历日期描述。

### `getLunar` <decl method type="(year: number, month: number, day: number): LunarDate" />

获取指定公历年、月、日对应的农历信息，返回 [`LunarDate`](#lunardate) 类型的农历日期描述。参数含义如下：
- `year`：年份的完整编号，例如 `2024`；
- `month`：月份编号，从 `0` 开始，12 月的编号为 $11$；
- `day`：日期编号，从 `1` 开始。

## 类型定义

### `LunarDate`

``` ts
type LunarDate = {
  month: string,    // 农历月份名称
  day: string,      // 农历日期名称
  festival?: string // 节日名称，可能未定义
}
```

- `month`：农历月份的名称，例如 `'正月'`，`'二月'`。
- `day`：农历日期的名称，例如 `'初一'`，`'十五'`。
- `festival`：节日名称，如果没有节日则属性未定义。
