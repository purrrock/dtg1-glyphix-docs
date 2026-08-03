---
icon: nodejs
---
# Node.js Package Manager

In addition to using it independently, the `gx` packaging tool can be used with JavaScript package managers such as npm, pnpm, or yarn. This requires the `glyphix` package to be installed:

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

The main benefits of using a JavaScript package manager in Glyphix app development include:
- Using TypeScript instead of JavaScript as the development language, providing type safety and a better developer experience
- Using JavaScript libraries from the Node.js ecosystem suitable for embedded development (such as algorithm libraries, data processing tools, etc.)
- Using tools like ESLint and Prettier to improve code quality and development efficiency
- Facilitating team collaboration and project maintenance

::: warning
Currently, package managers are only supported for managing standard JavaScript or TypeScript dependencies; Glyphix components cannot be reused in this way. When choosing third-party libraries, make sure they are suitable for embedded environments and avoid libraries that depend on the DOM, Node.js-specific APIs, or are overly bloated.
:::

::: tip
If the [Glyphix.js](glyphix.js/README.md) devtools are installed globally, you can directly run commands like `gx build` to package your project. Otherwise, you need to add `scripts` configuration in `package.json`.
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
The Glyphix packaging tool automatically handles the compilation of TypeScript files. The configuration above is primarily used for IDE type checking and code hints.
:::

## `glyphix.config.js` Configuration

It is recommended to create a `glyphix.config.js` file in the project root directory (the directory where `src/` or `package.json` is located) to customize packaging options:
```js
module.exports = {
  minify: false, // Disable code minification to facilitate debugging and mapping to source code line numbers
};
```
If you are using TypeScript, you can create a `glyphix.config.ts` file instead.

::: tip
Be sure to create this file and configure `minify: false`. Otherwise, the packaged code will be minified and obfuscated, making it impossible to map to source code line numbers during debugging.
:::

## Using TypeScript

The Glyphix framework provides experimental TypeScript support, allowing you to enjoy the benefits of type safety and modern JavaScript syntax in your app development.

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

Compared to the default JavaScript component script, using TypeScript requires the following adjustments:
1. Use `lang="ts"` in the `<script>` tag to specify TypeScript as the language type.
2. Import the `defineComponent` function from the `glyphix` module.
3. Pass the component object to be exported as an argument to `defineComponent` and export the return value of this function.

When using TypeScript, the `defineComponent` function makes code hints and type checking in your IDE much more accurate.

### `app.ts`

Rename `app.js` to `app.ts` to switch to the TypeScript app entry file, and the packaging tool will handle it automatically.