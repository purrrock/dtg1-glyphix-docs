---
icon: nodejs
---
# Node.js Package Manager

In addition to being used independently, the `gx` packaging tool can be used with JavaScript package managers such as npm, pnpm or yarn. The prerequisite is to install the `glyphix` package:

::: code-tabs
@tab npm
```bash
npm install -D glyphix
```

@tab pnpm
```bash
pnpm i -D glyphix

@tab yarn
```bash
yarn add -D glyphix
```
:::

Otherwise, you may encounter an error like this when executing `gx build`:
```bash
$ gx build
fatal: glyphix not found, please install it by `npm install -D glyphix' or other package manager.
```

The main benefits of using the JavaScript package manager in the development of Glyphix applications are as follows:
- Use TypeScript instead of JavaScript as the development language to provide type safety and a better development experience
- Use JavaScript libraries in the Node.js ecosystem suitable for embedded development (such as algorithm libraries, data processing tools, etc.)
- Use tools such as ESLint and Prettier to improve code quality and development efficiency
- Facilitates team collaboration and project maintenance

::: warning
Currently, only common JavaScript or TypeScript dependencies are managed through the package manager, and Glyphix components cannot be reused. When choosing third-party libraries, make sure they are suitable for embedded environments and avoid libraries that rely on the DOM, Node.js-specific APIs, or are too bulky.
:::

::: tip
If [Glyphix.js](glyphix.js/README.md) devtools is installed globally, you can directly use a command like `gx build` to package it, otherwise you need to add `scripts` configuration in `package.json`.
:::

## Project configuration

### `package.json` configuration

When using the Node.js package manager, it is recommended to add the necessary scripts and configuration in `package.json`:

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

### `tsconfig.json` configuration

If using TypeScript, you need to create a `tsconfig.json` file in the project root directory:

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
The Glyphix packaging tool automatically handles the compilation of TypeScript files. The above configuration is mainly used for IDE type checking and code prompts.
:::

## `glyphix.config.js` configuration

It is recommended to create a `glyphix.config.js` file in the project root directory (`src/` or the directory where `package.json` is located) to customize packaging options:
```js
module.exports = {
  minify: false, // Turn off code compression to facilitate debugging and obtain source code line numbers
};
```
If you use TypeScript, you can create a `glyphix.config.ts` file instead.

::: tip
Be sure to create this file and configure `minify: false`, otherwise the packaged code will be compressed and obfuscated, resulting in the inability to correspond to the source code line number during debugging.
:::

## Using TypeScript

The Glyphix framework offers experimental TypeScript support, allowing you to take advantage of type safety and modern JavaScript syntax in app development.

### Basic component example

Here's an example of a component written in TypeScript:

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

Compared with the default JavaScript component script, using TypeScript requires the following adjustments:
1. Use `lang="ts"` in the `<script>` tag to mark the language type as TypeScript.
2. Import the `defineComponent` function from the `glyphix` module.
3. The component object to be exported should be used as a parameter of `defineComponent`, and the return value of this function should be exported.

After using TypeScript, the `defineComponent` function will make code hints and type checking in the IDE more accurate.

### `app.ts`

Rename `app.js` to `app.ts` to use the TypeScript application entry file, which will be processed automatically by the packaging tool.