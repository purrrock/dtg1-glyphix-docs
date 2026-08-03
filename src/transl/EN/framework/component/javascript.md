# JavaScript Script

JavaScript is the scripting language used for Glyphix application development. Developers can place JavaScript code inside the `<script>` tag of a UX file, or reference `*.js` script files directly.

## Syntax Support

ES6 syntax is supported.

## Importing Modules

Reference other JS files in your code by importing modules. Typically, developer-defined modules are imported via paths using one of two methods:
``` js
import utils from '../Common/utils.js' // Using the import keyword
const utils = require('../Common/utils.js' ) // Using the require function
```
For rules regarding module paths, please refer to [Paths and URIs](../application/resource). Additionally, the `.js` file extension can be omitted in module paths, so the import statements above can also be written as:
``` js
import utils from '../Common/utils' // Using the import keyword
const utils = require('../Common/utils') // Using the require function
```

To import built-in system modules, use the module name prefixed with the `@` character. All system modules start with the `@` character:
``` js
import router from '@system.router' // Using the import keyword
const router = require('@system.router') // Using the require function
```

::: warning
Developers must not start module names with the `@` character, as these names are reserved for system modules.
:::

# Exporting Modules

Use ES6 `export` syntax to export modules, for example:
``` js
// Export the default value
export default {
  method() {
    // ...
  }
  props: {
    // ...
  }
}

// Export named values
export function process(args) {
  // ...
}
```