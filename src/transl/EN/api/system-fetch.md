# Data Request fetch

## Import Module

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

Initiates an asynchronous network data request. The fields of the `options` parameter are described as follows:
- `url`: The URL of the website to access.
- `method`: Supports `'GET'`, `'POST'`, and `'PUT'`, with `'GET'` as the default.
- `header`: An object containing HTTP request header information, with keys and values as strings. Typical HTTP header fields include `Authorization`, `Content-Type`, etc.
- `params`: Request parameters, all properties of which will be appended to the URL part of the request.
- `data`: The body content of an HTTP POST request.
- `responseType`: The response data type in the HTTP request. The default is `'text'`, and it can take the following values:
  - `'text'`: The response returns text data, meaning the `data` property of the returned data is of type `string`.
  - `'json'`: The response returns JSON data, and the returned `data` property will parse this JSON data into the corresponding JavaScript value.
  - `arraybuffer`: The response returns binary data, meaning the returned data is stored using an `ArrayBuffer` object.
- `timeout`: The timeout duration for the request response in milliseconds, with a default value of $6000 \rm ms$.

#### `data` Parameter

`data` is the request body, used only in POST requests. It typically comes in three types: a string, an `ArrayBuffer` object, or a JSON object. When `data` is a string or an `ArrayBuffer` object, the request body will be text or binary data respectively. When the body is a JSON object, it will be serialized into text form. The serialization format is determined by the `Content-Type` field of the request method (`method` parameter):
- When `Content-Type` is `application/json`, the `data` parameter object is serialized into a JSON string and used as the request body;
- In other cases, the `data` parameter object is serialized into the `application/x-www-form-urlencoded` format.

::: warning
Many HTTP APIs use JSON-formatted POST request bodies. Please ensure that the request header's `Content-Type` is correctly set to `application/json`. For details, please refer to this [example](#post-request-json-body).
:::

#### Return Value

Returns a `Promise` object. Upon fulfillment of the request, the properties of the resolved value are as follows:
- [`code`](#code-response-code) is the server response code. A successful request typically has a response code of `200`.
- `header` is the server response headers.
- `data` is the return value of the requested data, and its specific content is determined by the `options.responseType` parameter.

When the request fails, the returned `Promise` object is rejected.

## Instructions for Use

### `code` Response Code

The meanings of the response codes returned by the server are:
- `200`: Indicates the request was successful;
- `1002`: Parameter validation error;
- `1005`: Incomplete input parameters;
- `5000`: Request failed, response error;
- `5001`: Failed to read data buffer;
- `5002`: Request failed, response error;
- Others: Other HTTP/HTTPS response codes, such as `404`, etc.

When the response code returned by [`fetch`](#fetch) is `200`, it indicates that the network request was successful. Other values indicate that an error occurred during the request.

### Precautions

## Examples

### GET Request

This is a basic GET request example:

``` js
const res = await fetch.fetch({
  url: 'http://www.rt-thread.com/service/rt-thread.txt',
  method: 'GET', // Since the default mode is GET, method is optional here
  responseType: 'text'
})
console.log(`the status code of the response: ${res.code}`)
console.log(`the data of the response: ${res.data}`)
```

### POST Request

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

### POST Request (JSON Body)
