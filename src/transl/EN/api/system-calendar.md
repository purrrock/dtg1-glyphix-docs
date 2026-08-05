# Calendar

## Import Module

``` js
import calendar from '@system.calendar'
```

## Interface Definition

### `getLunar` <decl method type="(date: Date): LunarDate" />

Obtains the lunar date information for a `Date` object, returning a lunar date description of type [`LunarDate`](#lunardate).

### `getLunar` <decl method type="(year: number, month: number, day: number): LunarDate" />

Obtains the lunar information corresponding to the specified Gregorian year, month, and day, returning a lunar date description of type [`LunarDate`](#lunardate). The parameters are defined as follows:
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

- `month`: The name of the lunar month, for example, `'正月'` (First Month), `'二月'` (Second Month).
- `day`: The name of the lunar day, for example, `'初一'` (First Day), `'十五'` (Fifteenth Day).
- `festival`: The name of the festival. If there is no festival, this property is undefined.