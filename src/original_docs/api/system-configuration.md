# 应用配置

## 导入模块

```js
import configuration from '@system.configuration'
```

## 接口定义

### `getLocale`
<decl method><pre>
(): {
  language: string,
  countryOrRegion: string,
}
</pre></decl>

获取应用当前的语言环境。默认会使用系统的语言环境，可能因为设置或系统语言环境改变而发生变化。
 - `language` 表示当前的语言，如 'zh'、'en' 等, 
 - `countryOrRegion` 表示当前国家或地区，如 'CN'、'US' 等。
