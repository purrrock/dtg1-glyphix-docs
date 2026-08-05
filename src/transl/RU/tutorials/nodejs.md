---
icon: nodejs
---
# Менеджер пакетов Node.js

Помимо автономного использования, инструмент сборки `gx` может применяться совместно с менеджерами пакетов JavaScript, такими как npm, pnpm или yarn. Обязательным условием является установка пакета `glyphix`:

::: code-tabs
@tab npm
```bash
npm install -D glyphix
```

@tab pnpm
```bash
pnpm i -D glyphix
```

@tab yarn
```bash
yarn add -D glyphix
```
:::

В противном случае при выполнении команды `gx build` вы можете столкнуться со следующей ошибкой:
```bash
$ gx build
fatal: glyphix not found, please install it by `npm install -D glyphix' or other package manager.
```

Использование менеджера пакетов JavaScript при разработке приложений Glyphix дает следующие основные преимущества:
- Использование TypeScript вместо JavaScript в качестве языка разработки, что обеспечивает типобезопасность и лучший опыт разработки.
- Использование библиотек JavaScript из экосистемы Node.js, подходящих для встраиваемой разработки (например, библиотек алгоритмов, инструментов обработки данных и т. д.).
- Использование таких инструментов, как ESLint и Prettier, для повышения качества кода и эффективности разработки.
- Удобство командной работы и сопровождения проектов.

::: warning
В настоящее время поддерживается управление только обычными зависимостями JavaScript или TypeScript, повторное использование компонентов Glyphix невозможно. При выборе сторонних библиотек убедитесь, что они подходят для встраиваемых сред, и избегайте использования библиотек, зависящих от DOM, специфичных API Node.js или имеющих слишком большой размер.
:::

::: tip
Если инструменты разработчика [Glyphix.js](glyphix.js/README.md) установлены глобально, вы можете напрямую использовать такие команды, как `gx build`, в противном случае вам нужно добавить скрипты (`scripts`) в файл `package.json`.
:::

## Конфигурация проекта

### Настройка `package.json`

При использовании менеджера пакетов Node.js рекомендуется добавить необходимые скрипты и конфигурации в файл `package.json`:

```json
{
  "name": "my-glyphix-app",
  "version": "1.0.0",
  "scripts": {
    "build": "gx build",
    "emu": "gx emu",
    "clean": "gx clean"
  },
  "devDependencies": {
    "glyphix": "^1.0.41",
    "typescript": "^5.8.3"
  }
}
```

### Настройка `tsconfig.json`

Если вы используете TypeScript, вам нужно создать файл `tsconfig.json` в корневой директории проекта:

```json
{
  "compilerOptions": {
    "target": "ES2021",
    "module": "commonjs",
    "baseUrl": "./",
    "paths": {
      "/*": ["src/*"],
      "/assets": ["src/assets/*"]
    },
    "types": ["glyphix", "node"],
    "allowImportingTsExtensions": true,
    "checkJs": true,
    "declaration": true,
    "declarationMap": true,
    "emitDeclarationOnly": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "noImplicitAny": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "skipLibCheck": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*.ts", "src/**/*.ux"]
}
```

::: info
Инструмент сборки Glyphix автоматически обрабатывает компиляцию файлов TypeScript. Указанная выше конфигурация в основном используется для проверки типов в IDE и подсказок по коду.
:::

## Конфигурация `glyphix.config.js`

Рекомендуется создать файл `glyphix.config.js` в корневой директории проекта (в директории `src/` или там, где находится `package.json`), чтобы настроить параметры сборки:
```js
module.exports = {
  minify: false, // Отключить минификацию кода для удобства отладки и получения номеров строк исходного кода
};
```
Если вы используете TypeScript, вы можете вместо этого создать файл `glyphix.config.ts`.

::: tip
Обязательно создайте этот файл и установите параметр `minify: false`, иначе упакованный код будет минифицирован и обфусцирован, из-за чего при отладке будет невозможно сопоставить его со строками исходного кода.
:::

## Использование TypeScript

Фреймворк Glyphix обеспечивает экспериментальную поддержку TypeScript, позволяя вам использовать преимущества типобезопасности и современного синтаксиса JavaScript при разработке приложений.

### Пример базового компонента

Ниже приведен пример компонента, написанного на TypeScript:

```html
<template>
  <p on:click="onClick">{{count}}</p>
</template>

<script lang="ts">
import { defineComponent } from "glyphix"

export default defineComponent({
  data: {
    count: 0
  },
  onClick() {
    this.count++
  }
})
</script>
```

По сравнению со скриптом компонента JavaScript по умолчанию, использование TypeScript требует следующих изменений:
1. В теге `<script>` используется `lang="ts"` для указания языка TypeScript.
2. Функция `defineComponent` импортируется из модуля `glyphix`.
3. Экспортируемый объект компонента должен передаваться в качестве параметра в `defineComponent`, при этом экспортируется результат выполнения этой функции.

После внедрения TypeScript функция `defineComponent` сделает подсказки кода и проверку типов в IDE более точными.

### `app.ts`

Просто переименуйте `app.js` в `app.ts`, чтобы переключиться на использование TypeScript в качестве входного файла приложения, и инструмент сборки обработает его автоматически.