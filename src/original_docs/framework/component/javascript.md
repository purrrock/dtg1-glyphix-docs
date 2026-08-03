# JavaScript 脚本

JavaScript 是 Glyphix 应用开发的脚本语言。开发者可以将 JavaScript 代码放在 UX 文件的 `<script>` 标签中，也可以直接引用 `*.js` 脚本文件。  

## 语法支持

支持 ES6 语法。

## 导入模块

通过导入模块在代码中引用其他 js 文件。通常，通过路径来导入开发者定义的模块，有两种导入方式：
``` js
import utils from '../Common/utils.js' // 使用 import 关键字
const utils = require('../Common/utils.js') // 使用 require 函数
```
模块的路径规则请参考[路径和 URI](../application/resource)。此外，模块路径中可以省略作为文件后缀名出现的 `.js`，因此上面的导入语句可以写成
``` js
import utils from '../Common/utils' // 使用 import 关键字
const utils = require('../Common/utils') // 使用 require 函数
```

使用模块名导入系统内置的模块，所有的系统模块都是以 `@` 字符开头的：
``` js
import router from '@system.router' // 使用 import 关键字
const router = require('@system.router') // 使用 require 函数
```

::: warning
开发者不要将模块名使用 `@` 字符开头，这些名称都是为系统模块保留的。
:::

# 导出模块

使用 ES6 的 `export` 语法来导出模块，例如：
``` js
// 导出 default 值
export default {
  method() {
    // ...
  }
  props: {
    // ...
  }
}

// 导出具名值
export function process(args) {
  // ...
}
```
