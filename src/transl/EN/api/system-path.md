# Path operations

This module provides an interface for path operations. Including path splicing, segmentation and simplification functions.

## Import module

``` js
import path from '@system.path'
```

## Interface definition

#### `path.basename` <decl type="(path: string, suffix?: string): string" method />

Returns the file name part of path `path`. The specified file name suffix can also be removed by specifying the `suffix` parameter. For example
``` js
path.basename('/foo/bar/baz.txt') // 'baz.txt'
path.basename('/foo/bar/baz.txt', '.txt') // 'baz'
```

#### `path.dirname` <decl type="(path:string): string" method />

Returns the path part of `path` (as opposed to `basename()`, which discards the filename part). For example
``` js
path.dirname('/foo/bar/baz') // '/foo/bar'
```

#### `path.extname` <decl type="(path: string): string" method />

Get the file suffix in `path`. For example
``` js
path.extname('table.json') // '.json'
path.extname('/images/icon.png') // '.png'
```

#### `path.isAbsolute` <decl type="(path: string): boolean" method />

Determine whether `path` is an absolute path. For example
``` js
path.isAbsolute('/foo/bar'); // true
path.isAbsolute('/baz/..');  // true
path.isAbsolute('qux/');     // false
path.isAbsolute('.');        // false
```

#### `path.join` <decl type="(...paths: string[]): string" method />

Splice and simplify multiple paths, for example
``` js
path.join('/foo', 'bar', 'baz/asdf', 'quux', '..') // '/foo/bar/baz/asdf'
```

#### `path.normalize` <decl type="(path: string): string" method />

Reduce path `path` to its simplest form, parsing `..` and `.` and removing redundant path separators `/`.

``` js
path.normalize('/foo///bar/.././/baz') // '/foo/baz'
```

#### `path.relative` <decl type="(from: string, to: string): string" method />

Computes the relative path from `from` to `to`.

``` js
path.relative('/data/orandea/test/aaa', '/data/orandea/impl/bbb') // '../../impl/bbb'
```
