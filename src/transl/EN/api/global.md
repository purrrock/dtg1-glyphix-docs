# Global Objects

## Global Functions

### `encodeURIComponent` <decl type="(str: string): string" function />

The `encodeURIComponent()` global function is used to encode a URI component `str`. It escapes certain special characters into their corresponding UTF-8 percentage (`%`) escape sequences, ensuring that the component can be correctly interpreted when used as part of a URL, particularly in query string parameters, paths, or fragments.

Letters, numbers, and `- _ . ! ~ * ' ( )` are not encoded. Other characters are encoded into percentage escape sequences (for example, a space is encoded as `%20`).

The behavior of `encodeURIComponent()` is consistent with the [function of the same name](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent) in the Web.

Example:
```js
console.log(encodeURIComponent("https://example.com/page?id=100"));
// output: https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100
```

### `decodeURIComponent` <decl type="(str: string): string" function />

The `decodeURIComponent()` global function is used to decode a URI component `str` encoded by `encodeURIComponent()`. It converts percentage (`%`)-encoded sequences back to their original character forms, thereby restoring the original URI component. For example, it converts `%20` back to a space.

The behavior of `decodeURIComponent()` is consistent with the [function of the same name](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/decodeURIComponent) in the Web.

Example:
```js
console.log(decodeURIComponent("https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100"));
// output: https://example.com/page?id=100
```

### `URI` <decl type="(uri: string | Uri): Uri" function />

This function takes a string and parses it into a `Uri` object for subsequent processing. The `uri` parameter is the URI string to be parsed.

The return value is an object containing the following fields:
- `scheme: string`: The scheme field parsed from the parameter;
- `authority: string`: The authority field parsed from the parameter;
- `path: string`: The path field parsed from the parameter;
- `query: string`: The query field parsed from the parameter;
- `origin: string`: The original URI string from the parameter;
- `toString: () => string`: This method can re-encode the object back into a URI string.

For example:
``` js
console.log(URI("https://app-name/icon.png"))
// {
//   scheme: 'https',
//   authority: 'app-name',
//   path: '/icon.png',
//   query: '',
//   origin: 'https://app-name/icon.png',
//   toString: <function>
// }
```

The `URI` function also accepts an object as a parameter. In this case, the `URI` function adds a `toString` method to the parameter object, which can be used to encode the URI object into a string:
``` js
let uri = {
  scheme: 'https',
  authority: 'app-name',
  path: '/icon.png',
  query: ''
}
console.log(URI(uri).toString()) // 'https://app-name/icon.png'
```