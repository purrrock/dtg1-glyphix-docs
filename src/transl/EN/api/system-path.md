# Path Operations

This module provides interfaces for path operations, including path joining, splitting, and normalization.

## Import Module

``` js
import path from '@system.path'
```

## Interface Definitions

#### `path.basename` <decl type="(path: string, suffix?: string): string" method />

Returns the file name portion of the `path`. The specified file name suffix can also be removed by specifying the `suffix` parameter. For example:
``` js
path.basename('/foo/bar/baz.txt') // 'baz.txt'
path.basename('/foo/bar/baz.txt', '.txt') // 'baz'
```

#### `path.dirname` <decl type="(path:string): string" method />

Returns the directory name portion of the `path` (unlike `basename()`, this discards the file name portion). For example:
``` js
path.dirname('/foo/bar/baz') // '/foo/bar'
```

#### `path.extname` <decl type="(path: string): string" method />

Gets the file extension in the `path`. For example:
``` js
path.extname('table.json') // '.json'
path.extname('/images/icon.png') // '.png'
```

#### `path.isAbsolute` <decl type="(path: string): boolean" method />

Determines whether the `path` is an absolute path. For example:
``` js
path.isAbsolute('/foo/bar'); // true
path.isAbsolute('/baz/..');  // true
path.isAbsolute('qux/');     // false
path.isAbsolute('.');        // false
```

#### `path.join` <decl type="(...paths: string[]): string" method />

Joins and normalizes multiple paths. For example:
``` js
path.join('/foo', 'bar', 'baz/asdf', 'quux', '..') // '/foo/bar/baz/asdf'
```

#### `path.normalize` <decl type="(path: string): string" method />

Normalizes the given `path`, resolving `..` and `.`, and removing redundant path separators `/`.

``` js
path.normalize('/foo///bar/.././/baz') // '/foo/baz'
```

#### `path.relative` <decl type="(from: string, to: string): string" method />

Calculates the relative path from `from` to `to`.

``` js
path.relative('/data/orandea/test/aaa', '/data/orandea/impl/bbb') // '../../impl/bbb'
```