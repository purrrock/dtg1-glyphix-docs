# 路径操作

本模块提供路径操作的接口。包括路径拼接、分割以及化简等功能。

## 导入模块

``` js
import path from '@system.path'
```

## 接口定义

#### `path.basename` <decl type="(path: string, suffix?: string): string" method />

返回路径 `path` 的文件名部分，通过指定 `suffix` 参数还可以去除指定的文件名后缀。例如
``` js
path.basename('/foo/bar/baz.txt') // 'baz.txt'
path.basename('/foo/bar/baz.txt', '.txt') // 'baz'
```

#### `path.dirname` <decl type="(path:string): string" method />

返回 `path` 的路径部分（和 `basename()` 相反，它会丢弃文件名部分）。例如
``` js
path.dirname('/foo/bar/baz') // '/foo/bar'
```

#### `path.extname` <decl type="(path: string): string" method />

获取 `path` 中的文件后缀。例如
``` js
path.extname('table.json') // '.json'
path.extname('/images/icon.png') // '.png'
```

#### `path.isAbsolute` <decl type="(path: string): boolean" method />

判定 `path` 是否为绝对路径。例如
``` js
path.isAbsolute('/foo/bar'); // true
path.isAbsolute('/baz/..');  // true
path.isAbsolute('qux/');     // false
path.isAbsolute('.');        // false
```

#### `path.join` <decl type="(...paths: string[]): string" method />

将多个路径进行拼接并化简，例如
``` js
path.join('/foo', 'bar', 'baz/asdf', 'quux', '..') // '/foo/bar/baz/asdf'
```

#### `path.normalize` <decl type="(path: string): string" method />

将路径 `path` 化为最简，会解析 `..` 和 `.`，并移除多余的路径分隔符 `/`。

``` js
path.normalize('/foo///bar/.././/baz') // '/foo/baz'
```

#### `path.relative` <decl type="(from: string, to: string): string" method />

计算从 `from` 到 `to` 的相对路径。

``` js
path.relative('/data/orandea/test/aaa', '/data/orandea/impl/bbb') // '../../impl/bbb'
```
