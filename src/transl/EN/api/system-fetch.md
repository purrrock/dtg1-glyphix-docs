# Data request fetch

## Import module

``` js
import fetch from '@system.fetch'
```

## API

### `fetch`
<decl method><pre>
(options: {
  url: string,
  method?: 'GET' | 'POST' | 'PUT',
  header?: {[key: string]: string},
  params?: {[key: string]: string | number},
  data?: string | ArrayBuffer | {[key: string]: any},
  responseType?: 'text' | 'json' | 'arraybuffer',
  timeout?: number
}): Promise<{
  code: number,
  headers: {[key: string]: string},
  data: string | ArrayBuffer | any,
}>
</pre></decl>

Initiate an asynchronous network data request. The functions of each field of the `options` parameter are:
- `url`: The URL of the website to be accessed.
- `method`: supports `'GET'`, `'POST'` and `'PUT'`, the default is `'GET'`.
- `header`: an object containing HTTP request header information, the key and value are strings. Typical HTTP header fields can be `Authorization`, `Content-Type`, etc.
- `params`: The parameters of the request, which will set all its properties to the URL part of the request.
- `data`: The body part of the HTTP POST request.
- `responseType`: The response data type in the HTTP request. The default is `'text'`, which can have the following values.
  - `'text'`: The response returns text data, that is, the `data` attribute of the returned data is of type `string`.
  - `'json'`: The response returns JSON data, and the returned `data` attribute will parse the JSON data into the corresponding JavaScript value.
  - `arraybuffer`: The response returns binary data, that is, the returned data is stored in an `ArrayBuffer` object.
- `timeout`: request response timeout, in milliseconds, the default value is $6000 \rm ms$.

#### `data` parameter

`data` is the body of the request and is only used in POST requests. It is usually of three types: string, `ArrayBuffer` object or JSON object. When `data` is a string or an `ArrayBuffer` object, the body of the request will be text or binary data respectively. When the body is a JSON object, it is serialized into text form. The format of the serialization is determined by the `Content-Type` field of the request method (`method` parameter):
- When `Content-Type` is `application/json`, serialize the `data` parameter object into a JSON string as the request body;
- Serialize the `data` parameter object to the format of `application/x-www-form-urlencoded` in other cases.

::: warning
Many HTTP APIs use the POST request body in JSON format. Please note that the `Content-Type` of the request header must be correctly set to `application/json`. Please refer to this [example](#post-request-json-body) for details.
:::

#### Return value

Returns a `Promise` object whose properties are as follows:
- [`code`](#code-response code) is the server response code. The response code for a successful request is generally `200`.
- `header` is the response header of the server.
- `data` is the return value of the request data, and the specific content is determined by the `options.responseType` parameter.

When the request fails, the returned `Promise` object will be rejected.

## Instructions for use

### `code` response code

The response code returned by the server means:
- `200`: indicates that the request is successful;
- `1002`: Parameter verification error;
- `1005`: The input parameters are incomplete;
- `5000`: Request failed, response error;
- `5001`: Failed to read data buffer;
- `5002`: Request failed, response error;
- Others: Other HTTP/HTTPS response codes, such as `404`, etc.

When the response code returned by [`fetch`](#fetch) is `200`, it means that the network request is successful, and if it is other values, it means that there is an error in the request.

### Notes

## Example

### GET request

Here is a basic GET request example:

``` js
const res = await fetch.fetch({
  url: 'http://www.rt-thread.com/service/rt-thread.txt',
  method: 'GET', // Since the default mode is GET, method is optional at this time
  responseType: 'text'
})
console.log(`the status code of the response: ${res.code}`)
console.log(`the data of the response: ${res.data}`)
```

### POST request

``` js
const res = await fetch.fetch({
  url: 'https://www.rt-thread.com/service/echo',
  method: 'POST',
  data: {
    key1: 'hello',
    key2: 'world'
  },
  responseType: 'text'
})
console.log(`the status code of the response: ${res.code}`)
console.log(`the data of the response: ${res.data}`)
```

### POST request (JSON Body)
