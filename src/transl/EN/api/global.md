# global object

## Global function

### `encodeURIComponent` <decl type="(str: string): string" function />

The `encodeURIComponent()` global function is used to encode the URI component `str`. It escapes certain special characters to their UTF-8 encoded equivalent percent sign (`%`) escape sequences, which ensures that the component is interpreted correctly when used as part of a URL, especially within a query string parameter, path, or fragment.

Letters, numbers, `- _ . ! ~ * ' ( )` will not be encoded. Other characters are encoded as percent sign escape sequences (e.g. spaces are encoded as `%20`).

`encodeURIComponent()` behaves the same as the function of the same name in Web.

Example:
```js
console.log(encodeURIComponent("https://example.com/page?id=100"));
// output: https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100
```

### `decodeURIComponent` <decl type="(str: string): string" function />

The `decodeURIComponent()` global function is used to decode the URI component `str` encoded by `encodeURIComponent()`. It converts percent sign (`%`) escape sequences back to their original character forms, thereby restoring the original URI components. For example, it will convert `%20` back to a space.

`decodeURIComponent()` behaves the same as the function of the same name in Web.

Example:
```js
console.log(decodeURIComponent("https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100"));
// output: https://example.com/page?id=100
```

### `URI` <decl type="(uri: string | Uri): Uri" function />

This function accepts a string and parses it into a `Uri` object for subsequent processing. The parameter `uri` is the URI string to be parsed.

The return value is an object with the following fields:
- `scheme: string`: the scheme field parsed from the parameter;
- `authority: string`: the authority field parsed from the parameter;
- `path: string`: the path field parsed from the parameter;
- `query: string`: query field parsed from the parameter;
- `origin: string`: the original URI string in the parameter
- `toString: (string`: This method can re-encode this object into a URI string.

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

The `URI` function also accepts an object as a parameter. In this case, the `URI` function will add a `toString` method to the parameter object, through which the URI object can be encoded into a string:
``` js
let uri = {
  scheme: 'https',
  authority: 'app-name',
  path: '/icon.png',
  query: ''
}
console.log(URI(uri).toString()) // 'https://app-name/icon.png'
```
