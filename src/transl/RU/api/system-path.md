# Операции с путями

Данный модуль предоставляет интерфейсы для работы с путями, включая объединение, разделение, нормализацию путей и другие функции.

## Импорт модуля

``` js
import path from '@system.path'
```

## Определение интерфейсов

#### `path.basename` <decl type="(path: string, suffix?: string): string" method />

Возвращает имя файла из пути `path`. Указание параметра `suffix` позволяет удалить определенное расширение файла. Например:
``` js
path.basename('/foo/bar/baz.txt') // 'baz.txt'
path.basename('/foo/bar/baz.txt', '.txt') // 'baz'
```

#### `path.dirname` <decl type="(path:string): string" method />

Возвращает директорию пути `path` (в отличие от `basename()`, эта функция отбрасывает имя файла). Например:
``` js
path.dirname('/foo/bar/baz') // '/foo/bar'
```

#### `path.extname` <decl type="(path: string): string" method />

Возвращает расширение файла из пути `path`. Например:
``` js
path.extname('table.json') // '.json'
path.extname('/images/icon.png') // '.png'
```

#### `path.isAbsolute` <decl type="(path: string): boolean" method />

Определяет, является ли путь `path` абсолютным. Например:
``` js
path.isAbsolute('/foo/bar'); // true
path.isAbsolute('/baz/..');  // true
path.isAbsolute('qux/');     // false
path.isAbsolute('.');        // false
```

#### `path.join` <decl type="(...paths: string[]): string" method />

Объединяет несколько путей и нормализует результат. Например:
``` js
path.join('/foo', 'bar', 'baz/asdf', 'quux', '..') // '/foo/bar/baz/asdf'
```

#### `path.normalize` <decl type="(path: string): string" method />

Приводит путь `path` к наиболее лаконичному виду, разрешая сегменты `..` и `.` и удаляя лишние разделители пути `/`.

``` js
path.normalize('/foo///bar/.././/baz') // '/foo/baz'
```

#### `path.relative` <decl type="(from: string, to: string): string" method />

Вычисляет относительный путь от `from` до `to`.

``` js
path.relative('/data/orandea/test/aaa', '/data/orandea/impl/bbb') // '../../impl/bbb'
```