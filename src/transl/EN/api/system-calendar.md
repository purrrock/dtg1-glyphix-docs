# calendar

## Import module

``` js
import calendar from '@system.calendar'
```

## Interface definition

### `getLunar` <decl method type="(date: Date): LunarDate" />

Get the lunar date information of a `Date` object and return the lunar date description of type [`LunarDate`](#lunardate).

### `getLunar` <decl method type="(year: number, month: number, day: number): LunarDate" />

Get the lunar calendar information corresponding to the specified Gregorian calendar year, month, and day, and return the lunar calendar date description of type [`LunarDate`](#lunardate). The parameter meanings are as follows:
- `year`: the complete number of the year, such as `2024`;
- `month`: month number, starting from `0`, the number of December is $11$;
- `day`: date number, starting from `1`.

## Type definition

### `LunarDate`

``` ts
type LunarDate = {
  month: string, // lunar month name
  day: string, // Lunar date name
  festival?: string // Festival name, may be undefined
}
```

- `month`: The name of the lunar month, such as `'first month'`, `'February'`.
- `day`: The name of the lunar calendar date, such as `'the first day of the lunar month'`, `'the fifteenth day'`.
- `festival`: Festival name, if there is no festival, the attribute is undefined.
