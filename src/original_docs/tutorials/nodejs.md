---
icon: nodejs
---
# Node.js 包管理器

除了独立使用，`gx` 打包工具可以配合 npm、pnpm 或者 yarn 等 JavaScript 包管理器使用。前提是安装 `glyphix` 包：

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

否则在执行 `gx build` 时可能会遇到这样的报错：
```bash
$ gx build
fatal: glyphix not found, please install it by `npm install -D glyphix' or other package manager.
```

在 Glyphix 应用的开发中使用 JavaScript 包管理器主要有以下好处：
- 用 TypeScript，而不是 JavaScript 作为开发语言，提供类型安全和更好的开发体验
- 使用 Node.js 生态中适用于嵌入式开发的 JavaScript 库（如算法库、数据处理工具等）
- 使用 ESLint、Prettier 等工具来提升代码质量和开发效率
- 便于团队协作和项目维护

::: warning
目前仅支持通过包管理器来管理普通的 JavaScript 或 TypeScript 依赖，无法复用 Glyphix 组件。在选择第三方库时，请确保它们适用于嵌入式环境，避免使用依赖 DOM、Node.js 特定 API 或过于庞大的库。
:::

::: tip
如果 [Glyphix.js](glyphix.js/README.md) devtools 是全局安装的，那么可以直接用 `gx build` 这样的命令来打包，否则要在 `package.json` 中添加 `scripts` 配置。
:::

## 项目配置

### `package.json` 配置

当使用 Node.js 包管理器时，建议在 `package.json` 中添加必要的脚本和配置：

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

### `tsconfig.json` 配置

如果使用 TypeScript，需要在项目根目录创建 `tsconfig.json` 文件：

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
Glyphix 打包工具自动处理 TypeScript 文件的编译，上述配置主要用于 IDE 的类型检查和代码提示。
:::

## `glyphix.config.js` 配置

建议在项目根目录（`src/` 或 `package.json` 所在的目录）创建 `glyphix.config.js` 文件，以便自定义打包选项：
```js
module.exports = {
  minify: false, // 关闭代码压缩，便于调试获取源代码行号
};
```
如果你使用 TypeScript，可以改为创建 `glyphix.config.ts` 文件。

::: tip
一定要创建该文件并配置 `minify: false`，否则打包后的代码会被压缩混淆，导致调试时无法对应到源代码行号。
:::

## 使用 TypeScript

Glyphix 框架提供实验性的 TypeScript 支持，让您能够在应用开发中享受类型安全和现代 JavaScript 语法的优势。

### 基本组件示例

下面是一个使用 TypeScript 编写的组件示例：

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

相比于默认的 JavaScript 组件脚本，使用 TypeScript 需要做以下调整：
1. `<script>` 标签中使用 `lang="ts"` 标注语言类型为 TypeScript。
2. 从 `glyphix` 模块导入 `defineComponent` 函数。
3. 待导出的组件对象要作为 `defineComponent` 的参数，并导出该函数的返回值。

使用 TypeScript 之后，`defineComponent` 函数会让 IDE 中的代码提示和类型检查更加准确。

### `app.ts`

将 `app.js` 重命名 `app.ts` 即可改用 TypeScript 应用入口文件，打包工具会自动处理。
