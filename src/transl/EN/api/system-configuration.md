# App Configuration

## Import Module

```js
import configuration from '@system.configuration'
```

## Interface Definition

### `getLocale`
<decl method><pre>
(): {
  language: string,
  countryOrRegion: string,
}
</pre></decl>

Gets the current locale of the application. The system locale is used by default and may change due to settings or system locale changes.
 - `language` represents the current language, such as 'zh', 'en', etc.
 - `countryOrRegion` represents the current country or region, such as 'CN', 'US', etc.