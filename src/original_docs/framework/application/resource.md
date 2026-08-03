# 资源访问

## URI 和路径

可以在应用中通过 URI 或者路径访问应用中的资源。这些资源包括应用安装包中的文件、应用的运行时数据文件和共享数据文件等。与 Web 环境不同，Glyphix 应用中的 URI 和路径主要用于访问本地文件，而不能访问网络上的资源。

许多 [API](/api/README.md) 和[原生组件](/components/README.md)都使用 URI 或者路径访问资源，在这些接口中 URI 或者路径一般可以混用。

### URI

URI 的格式和 [URL](https://developer.mozilla.org/docs/Glossary/URL) 类似，语法定义如下图所示：

![](./figures/uri-syntax.svg)

各字段的说明为：
- **scheme**：指定资源访问的协议，例如 `app`、`internal` 等；
- **authority**：通常表示包名或者域名，其意义由具体的资源协议决定；
- **path**：资源在资源包内部的路径，必须是 `/` 字符开头的字符串（就像 Unix 中的路径一样）；
- **query**：指定查询数据，一般只用于应用跳转时传递参数。

这是一些 URI 的实例：
```
      authority
      ↓
app://com.example.app/icon.png
↑                    ↑
scheme               path
           authority
           ↓
internal://files/favicon.png
↑                ↑
scheme           path
      authority                query
      ↓                        ↓
app://com.example.app/icon.png?key=value
↑                    ↑
scheme               path
```

使用 URI 可以定位其他应用中的资源以及系统资源，也可以访问应用的缓存或临时文件，在访问外部资源时要注意应用是否有相应的权限。与 Web 平台不同，Glyphix URI 通常用于访问本地资源，而无法访问网络资源。请使用 [`system.fetch`](/api/system-fetch.md) 或者 [`system.request`](/api/system-request.md) 模块。

### 路径

路径是另一种定位资源的方式，它只能定义应用包内部的资源。路径有两种写法，一种是使用 `/` 开始的绝对路径，例如 `/assets/images/icon.png`；另一种是相对路径，例如 `images/icon.png`。绝对路径相对于应用资源包的根目录（也就是项目的 `src` 目录），而相对路径则相对于当前资源文件。因此
``` js
// in file: /Common/module-a.js
import x from '/Common/module-b.js'
import y from 'module-b.js'
```
中，`x` 和 `y` 实际上引入了同一个模块。

使用 `..` 可以定位上一级目录，例如 `../fonts/Times.ttf` 或 `/images/../fonts/Times.ttf`。不过 `..` 无法超越项目根目录的层次，因此 `/a/../..` 会被限制为 `/`。

绝对路径可以用于 URI 的 path 字段。

## URI 协议

### `app`

此协议下 authority 字段为应用的包名，也就是 `mainfest.package` 字段。`path` 字段为应用资源包内资源的路径。

使用 `app` 协议可以访问其他应用的资源。

### `file`

待补充

### `pkg`

待补充

### `internal`

`internal` URI 协议用于访问应用内部的资源文件，尤其是那些无法通过常规静态[路径](#路径)访问的文件。例如，应用程序可能生成临时文件、缓存文件或私有文件，这些文件无法通过路径访问（路径只能够访问资源包内的静态资源），而应通过 internal 协议来访问和管理。

常见的 `internal` URI 协议的基本格式如下：
``` ebnf
internal://<authority>/<path>
```
- **authority**：决定资源文件的存储位置，具体作用见下文。
- **path**：相对于指定存储位置的路径，指向具体的文件。

#### authority 字段

**authority** 字段决定了内部资源的类别和存储位置。依据不同的取值，`authority` 字段的含义如下：
- `cache`：表示该 URI 定位到应用程序的缓存目录，通常用于存储缓存文件。此目录下的文件是应用运行时生成的临时文件，可以随时被删除或重建。
- `files`：表示该 URI 定位到应用程序的私有文件目录。这是应用程序专用的存储位置，用于保存需要持久化的文件数据。
- `mass`：表示该 URI 定位到所有应用共享的文件目录。这通常是一个公用目录，多个应用可以在此目录下存储和读取文件。
- `tmp`：表示该 URI 定位到系统的临时文件目录，通常用于存储短期使用的临时文件。文件在这里存储的时间是短暂的，可能会在系统或应用重启时被清除。

例如，`internal://cache/images/avatar.png` 表示访问缓存目录中的图片文件 `avatar.png`。该 URI 可用于 [image](/components/image.md) 组件等多个场景：
``` html
<image src="internal://cache/images/avatar.png" />
```

::: warning
**authority** 字段不支持 URI 编码，必须直接使用 `cache`、`files` 这样的字面值，而不能用 `%63%61%63%68%65` 形式的编码。**path** 字段支持 URI 编码（但不推荐），但除了常规文件路径规则外，还需遵守以下限制：路径中不能出现 `%` 字符，且不能以 `..` 形式上溯根目录。

这些限制旨在防止通过编码或路径上溯等方式绕过内部资源访问规则，从而避免潜在的安全风险。
:::

#### 应用文件隔离

使用 `internal` URI 协议时，`cache`、`files` 和 `tmp` 类别都是应用的私有存储区域，只有当前应用可以访问这些目录下的文件。因此，同一个 `internal` URI 在不同的应用中可能指向不同的文件。每个应用都有独立的私有缓存、文件和临时文件存储空间，确保了应用之间的文件隔离和数据安全。

假设有两个不同的应用 A 和 B，分别使用同一个 URI 来访问私有文件：
```
internal://files/config/settings.json
```
那么
- **应用 A** 中该 URI 指向其私有文件目录中的 `settings.json` 文件。
- **应用 B** 中该 URI 指向其私有文件目录中的 `settings.json` 文件。

这种机制确保了应用之间各自管理自己的文件，互不干扰，也避免了潜在的数据泄露。

于此不同 `internal://mass/` 是所有应用共享的公共文件存储区域。同一个 `internal` URI 在不同的应用中指向相同的文件。因此，`mass` 目录下的文件可以被多个应用共同访问和共享。例如应用 A 和应用 B 都使用：
```
internal://mass/public/shared_image.png
```
那么该 URI 在两个应用中指向同一个公用文件 `shared_image.png`，允许它们共享该文件资源。

::: warning
如果一个应用将敏感数据存储在 `mass` 空间中，其他应用可能会读取该数据。因此，开发者应避免在 `mass` 目录中存储任何敏感或私密的信息，确保存储在其中的文件是可公开访问和共享的资源。
:::

## 资源 API

[`URI`](/api/global.md#uri) 全局函数、[`@system.path`](/api/system-path.md)、[`@system.file`](/api/system-file.md) 等接口提供在 JavaScript 中操作资源的能力。请参考相关文档了解详情。
