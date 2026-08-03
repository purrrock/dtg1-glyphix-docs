# Resource Access

## URIs and Paths

Resources within an application can be accessed via URIs or paths. These resources include files within the application installation package, the application's runtime data files, and shared data files. Unlike Web environments, URIs and paths in Glyphix applications are primarily used to access local files rather than resources on the network.

Many [APIs](/api/README.md) and [native components](/components/README.md) use URIs or paths to access resources, and these two can generally be used interchangeably in these interfaces.

### URI

The format of a URI is similar to a [URL](https://developer.mozilla.org/docs/Glossary/URL), and its syntax is defined as shown in the figure below:

![](./figures/uri-syntax.svg)

Descriptions of each field:
- **scheme**: Specifies the protocol for resource access, such as `app`, `internal`, etc.;
- **authority**: Usually represents the package name or domain name, and its meaning is determined by the specific resource protocol;
- **path**: The path of the resource inside the resource package, which must be a string starting with the `/` character (just like paths in Unix);
- **query**: Specifies query data, generally used only to pass parameters during application navigation.

Here are some examples of URIs:
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

URIs can be used to locate resources in other applications as well as system resources, and can also access application caches or temporary files. Pay attention to whether the application has the corresponding permissions when accessing external resources. Unlike the Web platform, Glyphix URIs are usually used to access local resources and cannot access network resources. Please use the [`system.fetch`](/api/system-fetch.md) or [`system.request`](/api/system-request.md) module instead.

### Paths

A path is another way to locate resources, and it can only define resources inside the application package. There are two ways to write a path: one is an absolute path starting with `/`, such as `/assets/images/icon.png`; the other is a relative path, such as `images/icon.png`. Absolute paths are relative to the root directory of the application resource package (which is the project's `src` directory), while relative paths are relative to the current resource file. Therefore, in
``` js
// in file: /Common/module-a.js
import x from '/Common/module-b.js'
import y from 'module-b.js'
```
`x` and `y` actually import the same module.

`..` can be used to locate the parent directory, such as `../fonts/Times.ttf` or `/images/../fonts/Times.ttf`. However, `..` cannot go beyond the root directory of the project, so `/a/../..` will be restricted to `/`.

Absolute paths can be used for the path field of a URI.

## URI Protocols

### `app`

Under this protocol, the authority field is the application's package name, which is the `manifest.package` field. The `path` field is the path of the resource within the application resource package.

Resources of other applications can be accessed using the `app` protocol.

### `file`

To be added

### `pkg`

To be added

### `internal`

The `internal` URI protocol is used to access resource files inside the application, especially those that cannot be accessed through regular static [paths](#paths). For example, an application might generate temporary files, cache files, or private files that cannot be accessed via paths (paths can only access static resources within the resource package) and should instead be accessed and managed through the internal protocol.

The basic format of common `internal` URI protocols is as follows:
``` ebnf
internal://<authority>/<path>
```
- **authority**: Determines the storage location of the resource file, see below for specific functions.
- **path**: The path relative to the specified storage location, pointing to the specific file.

#### authority Field

The **authority** field determines the category and storage location of the internal resource. Depending on its value, the meaning of the `authority` field is as follows:
- `cache`: Indicates that the URI points to the application's cache directory, usually used to store cache files. Files in this directory are temporary files generated during application runtime and can be deleted or rebuilt at any time.
- `files`: Indicates that the URI points to the application's private file directory. This is a storage location dedicated to the application for saving file data that needs to be persisted.
- `mass`: Indicates that the URI points to a file directory shared by all applications. This is usually a public directory where multiple applications can store and read files.
- `tmp`: Indicates that the URI points to the system's temporary file directory, usually used to store short-term temporary files. Files stored here have a short lifespan and may be cleared when the system or application restarts.

For example, `internal://cache/images/avatar.png` represents accessing the image file `avatar.png` in the cache directory. This URI can be used in multiple scenarios such as the [image](/components/image.md) component:
``` html
<image src="internal://cache/images/avatar.png" />
```

::: warning
The **authority** field does not support URI encoding and must directly use literal values such as `cache` and `files`, rather than encodings in the form of `%63%61%63%68%65`. The **path** field supports URI encoding (though not recommended), but in addition to regular file path rules, it must comply with the following restrictions: the `%` character must not appear in the path, and it cannot traverse up to the root directory using `..`.

These restrictions are designed to prevent bypassing internal resource access rules through encoding or path traversal, thereby avoiding potential security risks.
:::

#### Application File Isolation

When using the `internal` URI protocol, the `cache`, `files`, and `tmp` categories are all private storage areas of the application, and only the current application can access the files in these directories. Therefore, the same `internal` URI may point to different files in different applications. Each application has an independent private storage space for caches, files, and temporary files, ensuring file isolation and data security between applications.

Suppose there are two different applications A and B, both using the same URI to access a private file:
```
internal://files/config/settings.json
```
Then
- In **Application A**, this URI points to the `settings.json` file in its private file directory.
- In **Application B**, this URI points to the `settings.json` file in its private file directory.

This mechanism ensures that applications manage their own files independently without interfering with each other, and also avoids potential data leaks.

In contrast, `internal://mass/` is a public file storage area shared by all applications. The same `internal` URI points to the same file in different applications. Therefore, files under the `mass` directory can be jointly accessed and shared by multiple applications. For example, if both Application A and Application B use:
```
internal://mass/public/shared_image.png
```
Then the URI points to the same public file `shared_image.png` in both applications, allowing them to share this file resource.

::: warning
If an application stores sensitive data in the `mass` space, other applications may read that data. Therefore, developers should avoid storing any sensitive or private information in the `mass` directory, and ensure that the files stored therein are publicly accessible and shareable resources.
:::

## Resource APIs

The [`URI`](/api/global.md#uri) global function, [`@system.path`](/api/system-path.md), [`@system.file`](/api/system-file.md), and other interfaces provide the capability to manipulate resources in JavaScript. Please refer to the relevant documentation for details.