---
icon: nodejs
---
# Node.js Package Managers

In addition to standalone usage, the `gx` build tool can be used in conjunction with JavaScript package managers such as npm, pnpm, or yarn. The prerequisite is installing the `glyphix` package:

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

Otherwise, you may encounter an error like this when running `gx build`:
```bash
$ gx build
fatal: glyphix not found, please install it by `npm install -D glyphix' or other package manager.
```

Using a JavaScript package manager in Glyphix application development mainly offers the following benefits:
- Use TypeScript instead of JavaScript as the development language, providing type safety and a better development experience
- Use JavaScript libraries from the Node.js ecosystem suitable for embedded development (such as algorithm libraries, data processing tools, etc.)
- Use tools like ESLint and Prettier to improve code quality and development efficiency
- Facilitate team collaboration and project maintenance

::: warning
Currently, only standard JavaScript or TypeScript dependencies can be managed via package managers; Glyphix components cannot be reused. When choosing third-party libraries, please ensure they are suitable for embedded environments and avoid using libraries that depend on the DOM, Node.js-specific APIs, or are excessively large.
:::

::: tip
If [Glyphix.js](glyphix.js/README.md) devtools is installed globally, you can directly run commands like `gx build` to bundle the app; otherwise, you need to add `scripts` configuration in `package.json`.
:::

## Project Configuration

### `package.json` Configuration

When using a Node.js package manager, it is recommended to add the necessary scripts and configurations to `package.json`:

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

### `tsconfig.json` Configuration

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
The Glyphix build tool automatically handles the compilation of TypeScript files. The above configuration is mainly used for IDE type checking and code completion.
:::

## `glyphix.config.js` Configuration

It is recommended to create a `glyphix.config.js` file in the project root directory (the directory containing `src/` or `package.json`) to customize build options:
```js
module.exports = {
  minify: false, // Disable code minification for easier debugging with source line numbers
};
```
If you use TypeScript, you can create a `glyphix.config.ts` file instead.

::: tip
Be sure to create this file and configure `minify: false`; otherwise, the bundled code will be minified and obfuscated, making it impossible to map back to source line numbers during debugging.
:::

## Using TypeScript

The Glyphix framework provides experimental TypeScript support, allowing you to enjoy the benefits of type safety and modern JavaScript syntax in application development.

### Basic Component Example

Below is an example of a component written in TypeScript:

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

Compared to default JavaScript component scripts, using TypeScript requires the following adjustments:
1. Use `lang="ts"` in the `<script>` tag to specify the language type as TypeScript.
2. Import the `defineComponent` function from the `glyphix` module.
3. Pass the component object to be exported as an argument to `defineComponent`, and export the return value of this function.

After using TypeScript, the `defineComponent` function will make code completion and type checking in the IDE more accurate.

### `app.ts`

Simply rename `app.js` to `app.ts` to switch to a TypeScript application entry file, and the build tool will handle it automatically.