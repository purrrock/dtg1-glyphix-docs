# resource access


## URIs and paths


You can access resources in the application through URI or path. These resources include files in the application installation package, application runtime data files and shared data files, etc. Unlike the web environment, URIs and paths in Glyphix applications are mainly used to access local files and cannot access resources on the network.


Many [API](/api/README.md) and [Native components](/components/README.md) use URIs or paths to access resources, and URIs or paths can generally be mixed in these interfaces.


### URI


The format of URI is similar to [URL](https://developer.mozilla.org/docs/Glossary/URL), and the syntax definition is as shown in the figure below:


![](./figures/uri-syntax.svg)



The description of each field is:
- **scheme**: Specifies the protocol for resource access, such as `app`, `internal`, etc.;
- **authority**: usually represents the package name or domain name, and its meaning is determined by the specific resource agreement;
- **path**: The path of the resource inside the resource package, which must be a string starting with the `/` character (just like the path in Unix);
- **query**: Specify query data, generally only used to pass parameters when application jumps.


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


URIs can be used to locate resources in other applications and system resources, and can also access the application's cache or temporary files. When accessing external resources, pay attention to whether the application has the corresponding permissions. Unlike the web platform, Glyphix URIs are typically used to access local resources and cannot access network resources. Please use the [`system.fetch`](/api/system-fetch.md) or [`system.request`](/api/system-request.md) module.


### path


Path is another way to locate resources, it can only define resources inside the application package. There are two ways to write paths, one is an absolute path starting with `/`, such as `/assets/images/icon.png`; the other is a relative path, such as `images/icon.png`. Absolute paths are relative to the root directory of the application resource bundle (that is, the project's `src` directory), while relative paths are relative to the current resource file. therefore
``` js
// in file: /Common/module-a.js
import x from '/Common/module-b.js'
import y from 'module-b.js'
```
, `x` and `y` actually import the same module.


Use `..` to locate the upper directory, such as `../fonts/Times.ttf` or `/images/../fonts/Times.ttf`. However, `..` cannot transcend the level of the project root directory, so `/a/../..` will be limited to `/`.


Absolute paths can be used in the path field of a URI.


## URI protocol


### `app`


Under this protocol, the authority field is the application package name, which is the `mainfest.package` field. The `path` field is the path to the resources in the application resource package.


Use the `app` protocol to access resources from other applications.


### `file`


To be added


### `pkg`


To be added


### `internal`


The `internal` URI protocol is used to access resource files within an application, especially those that are not accessible through regular static [path](#路径). For example, an application may generate temporary files, cache files, or private files that cannot be accessed through paths (paths can only access static resources within resource bundles), but should be accessed and managed through the internal protocol.


The basic format of the common `internal` URI protocol is as follows:
``` ebnf
internal://<authority>/<path>
```
- **authority**: Determines the storage location of resource files. See below for specific functions.
- **path**: The path relative to the specified storage location, pointing to a specific file.


#### authority field


The **authority** field determines the category and storage location of internal resources. Depending on the value, the meaning of the `authority` field is as follows:
- `cache`: Indicates that this URI locates the cache directory of the application, usually used to store cache files. The files in this directory are temporary files generated when the application is running and can be deleted or rebuilt at any time.
- `files`: Indicates that the URI locates the private file directory of the application. This is an application-specific storage location for file data that needs to be persisted.
- `mass`: Indicates that the URI locates the file directory shared by all applications. This is usually a common directory where multiple applications can store and read files.
- `tmp`: Indicates that this URI locates the temporary file directory of the system, which is usually used to store temporary files for short-term use. Files are stored here for a short period of time and may be cleared when the system or application is restarted.


For example, `internal://cache/images/avatar.png` means accessing the image file `avatar.png` in the cache directory. This URI can be used in multiple scenarios such as [image](/components/image.md) components:
``` html
<image src="internal://cache/images/avatar.png" />
```


::: warning

The **authority** field does not support URI encoding. Literal values ​​such as `cache` and `files` must be used directly, and encoding in the form of `%63%61%63%68%65` cannot be used. The **path** field supports URI encoding (but is not recommended), but is subject to the following restrictions in addition to the normal file path rules: `%` characters cannot appear in the path, and the root directory cannot be traced back as `..`.


These restrictions are intended to prevent potential security risks by preventing bypassing of internal resource access rules through encoding or path uptracing.
:::



#### Apply file isolation


When using the `internal` URI protocol, the `cache`, `files` and `tmp` categories are private storage areas for applications, and only the current application can access files in these directories. Therefore, the same `internal` URI may point to different files in different applications. Each application has independent private cache, file and temporary file storage space, ensuring file isolation and data security between applications.


Suppose there are two different applications A and B, each using the same URI to access private files:
```
internal://files/config/settings.json
```
So
- The URI in **Application A** points to the `settings.json` file in its private file directory.
- This URI in **Application B** points to the `settings.json` file in its private file directory.


This mechanism ensures that applications manage their own files without interfering with each other, and avoids potential data leaks.


Different from this, `internal://mass/` is a common file storage area shared by all applications. The same `internal` URI points to the same file in different applications. Therefore, files in the `mass` directory can be accessed and shared by multiple applications. For example, both application A and application B use:
```
internal://mass/public/shared_image.png
```
Then the URI points to the same common file `shared_image.png` in both applications, allowing them to share the file resource.


::: warning

If one application stores sensitive data in `mass` space, other applications may be able to read that data. Therefore, developers should avoid storing any sensitive or private information in the `mass` directory and ensure that files stored there are publicly accessible and shareable resources.
:::



## Resource API


[`URI`](/api/global.md#uri) global function, [`@system.path`](/api/system-path.md), [`@system.file`](/api/system-file.md) and other interfaces provide the ability to operate resources in JavaScript. Please refer to the relevant documentation for details.