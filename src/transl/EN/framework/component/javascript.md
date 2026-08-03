# JavaScript script


JavaScript is the scripting language used for Glyphix application development. Developers can place JavaScript code in the `<script>` tag of the UX file, or directly reference the `*.js` script file.


## Grammar support


Supports ES6 syntax.


## Import module


Reference other js files in your code by importing modules. Usually, there are two ways to import developer-defined modules through paths:
``` js
import utils from '../Common/utils.js' // Use the import keyword
const utils = require('../Common/utils.js') // Use require function
```
Please refer to [Paths and URIs](../application/resource) for module path rules. In addition, the `.js` appearing as the file suffix name can be omitted in the module path, so the above import statement can be written as
``` js
import utils from '../Common/utils' // Use the import keyword
const utils = require('../Common/utils') // Use require function
```


Use the module name to import the system's built-in modules. All system modules begin with the `@` character:
``` js
import router from '@system.router' // Use the import keyword
const router = require('@system.router') // Use require function
```


::: warning

Developers should not start module names with the `@` character; these names are reserved for system modules.
:::



# export module


Use the ES6 `export` syntax to export modules, for example:
``` js
// Export default value
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