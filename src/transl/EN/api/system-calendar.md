# Calendar

## Import Module

``` js
import calendar from '@system.calendar'
```

## Interface Definition

### `getLunar` <decl method type="(date: Date): LunarDate" />

Obtains the lunar date information for a given `Date` object, and returns a lunar date description of type [`LunarDate`](#lunardate).

### `getLunar` <decl method type="(year: number, month: number, day: number): LunarDate" />

Obtains the lunar information corresponding to the specified Gregorian year, month, and day, and returns a lunar date description of type [`LunarDate`](#lunardate). The parameters are defined as follows:
- `year`: Full year number, for example, `2024`;
- `month`: Month number, starting from `0`, where December is numbered $11$;
- `day`: Day number, starting from `1`.

## Type Definition

### `LunarDate`

``` ts
type LunarDate = {
  month: string,    // Lunar month name
  day: string,      // Lunar day name
  festival?: string // Festival name, may be undefined
}
```

- `month`: Name of the lunar month, for example, `'正月'`, `'二月'`.
- `day`: Name of the lunar day, for example, `'初一'`, `'十五'`.
- `festival`: Name of the festival. If there is no festival, this property is undefined.