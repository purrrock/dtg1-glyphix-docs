---
icon: nodejs
---
# Пакетные менеджеры Node.js

Помимо автономного использования, сборщик `gx` можно использовать совместно с пакетными менеджерами JavaScript, такими как npm, pnpm или yarn. Предварительным условием является установка пакета `glyphix`:

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

В противном случае при выполнении `gx build` вы можете столкнуться со следующей ошибкой:
```bash
$ gx build
fatal: glyphix not found, please install it by `npm install -D glyphix' or other package manager.
```

Использование пакетного менеджера JavaScript при разработке приложений Glyphix дает следующие основные преимущества:
- Использование TypeScript вместо JavaScript в качестве языка разработки, что обеспечивает типобезопасность и более удобный процесс разработки
- Использование библиотек JavaScript из экосистемы Node.js, подходящих для встраиваемой разработки (например, библиотек алгоритмов, инструментов обработки данных и т. д.)
- Использование таких инструментов, как ESLint и Prettier, для повышения качества кода и эффективности разработки
- Упрощение командной работы и поддержки проекта

::: warning
В настоящее время через пакетный менеджер поддерживается только управление обычными зависимостями JavaScript или TypeScript; повторное использование компонентов Glyphix невозможно. При выборе сторонних библиотек убедитесь, что они подходят для встраиваемых сред, и избегайте использования библиотек, зависящих от DOM, специфичных API Node.js или имеющих слишком большой размер.
:::

::: tip
Если devtools для [Glyphix.js](glyphix.js/README.md) установлены глобально, вы можете использовать команду `gx build` напрямую для сборки. В противном случае необходимо добавить конфигурацию `scripts` в `package.json`.
:::

## Конфигурация проекта

### Конфигурация `package.json`

При использовании пакетного менеджера Node.js рекомендуется добавить необходимые скрипты и конфигурацию в `package.json`:

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

### Конфигурация `tsconfig.json`

Если вы используете TypeScript, вам необходимо создать файл `tsconfig.json` в корневой директории проекта:

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
Сборщик Glyphix автоматически обрабатывает компиляцию файлов TypeScript. Приведенная выше конфигурация в основном используется для проверки типов и автодополнения кода в IDE.
:::

## Конфигурация `glyphix.config.js`

Рекомендуется создать файл `glyphix.config.js` в корневой директории проекта (где находятся `src/` или `package.json`), чтобы настроить параметры сборки:
```js
module.exports = {
  minify: false, // Отключение минификации кода для удобства отладки и получения номеров строк исходного кода
};
```
Если вы используете TypeScript, вы можете вместо этого создать файл `glyphix.config.ts`.

::: tip
Обязательно создайте этот файл и настройте `minify: false`, иначе собранный код будет сжат и обфусцирован, что сделает невозможным сопоставление номеров строк с исходным кодом при отладке.
:::

## Использование TypeScript

Фреймворк Glyphix предоставляет экспериментальную поддержку TypeScript, что позволяет вам использовать преимущества типобезопасности и современного синтаксиса JavaScript при разработке приложений.

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

По сравнению со стандартным скриптом компонента на JavaScript, при использовании TypeScript необходимо внести следующие изменения:
1. Используйте `lang="ts"` в теге `<script>`, чтобы указать, что языком является TypeScript.
2. Импортируйте функцию `defineComponent` из модуля `glyphix`.
3. Экспортируемый объект компонента должен передаваться в качестве аргумента `defineComponent`, и должен экспортироваться результат работы этой функции.

После использования TypeScript функция `defineComponent` сделает подсказки кода и проверку типов в IDE более точными.

### `app.ts`

Просто переименуйте `app.js` в `app.ts`, чтобы переключиться на входной файл приложения TypeScript — сборщик обработает его автоматически.