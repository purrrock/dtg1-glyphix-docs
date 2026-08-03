# Apply configuration

## Import module

```js
import configuration from '@system.configuration'
```

## Interface definition

### `getLocale`
<decl method><pre>
(): {
  language: string,
  countryOrRegion: string,
}
</pre></decl>

Get the current locale of the application. By default, the system locale is used, which may change due to settings or system locale changes.
 - `language` represents the current language, such as 'zh', 'en', etc.,
 - `countryOrRegion` represents the current country or region, such as 'CN', 'US', etc.
