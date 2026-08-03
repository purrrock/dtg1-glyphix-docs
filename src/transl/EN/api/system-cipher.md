# Cipher Algorithm

## Import Module

``` js
import cipher from '@system.cipher'
```

## API

### `aes`
<decl method><pre>
(options: {
  action: string,
  text: string,
  key: string,
  transformation?: string,
  iv?: string,
  ivOffset?: number,
  ivLen?: number
  }): Promise&lt;{ text: string }>
</pre></decl>

`aes` encryption and decryption. The functions of each field in the `options` parameter are as follows:
- `action`: The type of encryption or decryption, with two optional values: `'encrypt'` for encryption, and `'decrypt'` for decryption;
- `text`: The text content to be encrypted or decrypted. Text to be encrypted should be plain text, and text to be decrypted should be binary data encoded in `base64`;
- `key`: The key used for encryption or decryption, generated as a string after `base64` encoding. Before being decoded from `base64`, the key must be a multiple of $16$ bytes;
- `transformation`: The encryption mode (`'ECB'`, `'CBC'`, `'CFB'`, `'CTR'`, `'OFB'`) and padding scheme for the `AES` algorithm, defaulting to `'AES/CBC/PKCS5Padding'`. The available AES padding options are:
  - `'PKCS5Padding'`
  - `'PKCS7Padding'`
  - `'NoPadding'`
  - `'OneAndZerosPadding'`
  - `'ZerosAndLenPadding'`
  - `'ZerosPadding'` 
- `iv`: The initialization vector (IV) for AES encryption/decryption, as a Base64-encoded string, defaulting to the value of the `key` field;
- `ivOffset`: The initialization vector offset for AES encryption/decryption, defaulting to $0$;
- `ivLen`: The byte length of the initialization vector for AES encryption/decryption, defaulting to $16$;

::: details Sample Code

``` js
let signKey = "TkQRXv9xfAU65sxGmx4Xz2tQP7fwwdyxAGIZ9HMtc+c="

async function AesTest() {
  const encrypt = await cipher.aes({
    action: "encrypt",
    text: "this is a test project!",
    key: signKey,
    iv: "MTIzNDU2NzgxMjM0NTY3OA==",
    transformation:"AES/CBC/ZerosAndLenPadding",
    ivOffset: 0,
    ivLen: 16
  })
  console.log(`encrypt text: ${encrypt.text}`)

  const decrypt = await cipher.aes({
    action: "decrypt",
    text: encrypt.text,
    key: signKey,
    iv: "MTIzNDU2NzgxMjM0NTY3OA==",
    transformation:"AES/CBC/ZerosAndLenPadding",
    ivOffset: 0,
    ivLen: 16
  })
  console.log(`decrypto text: ${decrypt.text}`)
}

AesTest() // Print the encrypted and decrypted text, console output
// encrypt text: yI4dWJzQNCQfXq5P8du1dtYWZuBvbl9F9Vh15Fh9qjg=
// decrypto text: this is a test project!
```
:::

### `rsa`
<decl method><pre>
(options: {
  action: string,
  text: string,
  key: string,
  transformation?: string
}): Promise&lt;{ text: string }>
</pre></decl>

`rsa` encryption and decryption. The functions of the fields in the `options` parameter are as follows:
- `action`: The type of encryption or decryption, with two optional values: `'encrypt'` for encryption, and `'decrypt'` for decryption;
- `text`: The text content to be encrypted or decrypted. The text to be decrypted should be binary data encoded in Base64;
- `key`: The `RSA` key, which is a string generated after `base64` encoding. When encrypting, `key` is the public key; when decrypting, `key` is the private key;
- `transformation`: The padding scheme of the RSA algorithm, defaulting to `RSA/None/OAEPwithSHA-256andMGF1Padding`. The available RSA padding options are:
  - `'PKCS_v15andMGF1Padding'`
  - `'OAEPwithMD5andMGF1Padding'`
  - `'OAEPwithSHA-1andMGF1Padding'`
  - `'OAEPwithSHA-256andMGF1Padding'`

::: details Sample Code
``` js
let publicKey =
  'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCirfSt9f49F/BtPqextDlyoUEQ' +
  'qN+NUNxkYB5DY4FmJuI0gQSaK8hlGvnoA5T/seTGylHn95/PPTl5hW+riYtWaKfM' +
  'CXI2scstXA0S5vcYfc9917tRsrFzrDfJW+WD/HmmcvgI6rcbivokDikep3gVX0df' +
  'ktYtsAs158kMs4bBpwIDAQAB'

let privateKey = 
  'MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAKKt9K31/j0X8G0+' +
  'p7G0OXKhQRCo341Q3GRgHkNjgWYm4jSBBJoryGUa+egDlP+x5MbKUef3n889OXmF' +
  'b6uJi1Zop8wJcjaxyy1cDRLm9xh9z33Xu1GysXOsN8lb5YP8eaZy+AjqtxuK+iQO' +
  'KR6neBVfR1+S1i2wCzXnyQyzhsGnAgMBAAECgYAuH23w6H7FqYTkJFB9RKDJDEkb' +
  'RRXkxhlGaC4MYyjr4nhd9Hpuj51IdSaHjoRvHmvDpNcmEoH/ytcBykBH/T5As68M' +
  'L1OmzuJsD3BYMZpOOSFC9m7o6VMRf/T/ZTG6EDMtQekxlBV66QpiFmhQMjDs3jJY' +
  'TyR3OnZN9BWNBNotWQJBAOnLUpMT53HbFtw9vCRtVgAJ8JFjL4ZzYzrHj4mloKF3' +
  'P/r6faYUjgULoaHiD+BZB/Avru2h74Ghhr26CD3gMR0CQQCyIXzjSCrQiyCEdg1I' +
  '//IWLAALsfVITrlCN0rVeMkjTbc0KFEDUKG9y6MGAGX4AJNnos7y+zLpi6PcgwlU' +
  'zWaTAkBx5+fRVK88n5uhrkpODR8LYcxdaU+sV+eOqc/bJmD+ihUX+JbjJbyT5LjZ' +
  'IETP71CYywKVMIJ6S/JT2aFOVD5ZAkEAsfqFtu2fYbjw54iwY3TfpEmYThcj9Xg6' +
  '4C8wxTQm+/AlkaaKs144DNPPciqpt26T2WOxlNNqHjFYqvX+N832owJAaM5d4x2a' +
  'SDfC5GQFNfZ3WjATXkDE86q3m/88RBFFy8fWByyGiXtp4z5LCtMzI63X3ao0asVK' +
  'mjZxB+T+lMqa3w=='

async function rsaTest() {
  const res = await cipher.rsa({
    action: "encrypt",
    text: "this is a Rsa test.",
    key: publicKey,
    transformation: "RSA/None/OAEPwithSHA-256andMGF1Padding"
  })
  console.log(`encrypt text: ${res.text}`)

  const decrypt = await cipher.rsa({
    action: "decrypt",
    text: res.text,
    key: privateKey,
    transformation: "RSA/None/OAEPwithSHA-256andMGF1Padding"
  })
  console.log(`decrypt text: ${decrypt.text}`)
}

rsaTest() // Print the encrypted and decrypted text, console output sample
// encrypt text: FF+4R3iJ9pjeozZ6/Oulz9LUBH/uGQbIesJ7JbYRWvxGIHpJKNiEB+4MT/JcKs8ddN/ZQ4ts+YWMgUeglRBugRx+T4kqq0rKBdQrYdiMP58deCViSJjXJS+joPppwLDPL1Lg0VxpW89B+gA1jfC+9N8tvEHPhcX+nF8uAKRcW0M=
// decrypt text: this is a Rsa test.
```
:::

### `sign`
<decl method><pre>
(options: {
  text: string,
  key: string,
  algorithm?: string,
}): Promise&lt;{ sign: string }>
</pre></decl>

`sign` signature. The functions of each field in the `options` parameter are as follows:
- `text`: The content to be signed;
- `key`: The RSA private key;
- `algorithm`: The signature algorithm, defaulting to `'SHA256withRSA'`. The available signature algorithms are:
  - `'MD5withRSA'`
  - `'SHA1withRSA'`
  - `'SHA256withRSA'`
  - `'SHA512withRSA'`

::: details Sample Code

``` js
let signKey1 = "-----BEGIN RSA PRIVATE KEY-----\n" +
  "MIIEpAIBAAKCAQEA5hoGkpvqxJdssvqAYuvCWdTRrOdzZyx/ZyMev5Qyt2JKLy1C\n" +
  "7DuKrFGF5T5BDxN81o/OK+AQ6G1ASmwWfv5C1mk7sv6/glibPt9Gyr1OFMxviauy\n" +
  "ZMF8sgHVGkFyy1GsCsaM9anT1OEPoNeqrTHt+xB3Pq6FdH9RLMVbY0QNem5zv816\n" +
  "Hb6AJvMSnbGqMdd9fI1ARithrqnr9p+achP+Hc2Pj61PRviKJpFGLzBrU1BgBEbN\n" +
  "hscGRPebn4kTSy8flYau9lnDyLs5yyy0MHKBhot5Ja3tWTKhaqymFyJL2K6gE6Xn\n" +
  "bDAT6YFvo1TE9R7r9y+8prOR8oznJP19yxEWCQIDAQABAoIBAEbolkXvznUuxMyS\n" +
  "7aWOSaItN0A1Qxb0W36JEByxqr9ghsPrCsiJwL5BkSWH/byLoNjuD/btYch+gmVs\n" +
  "0bHo4Of6He+XGaUtcQn6/HHVzI4UQfsG8j6ica7ZabZhnOKTFJVtglriLulXQd2r\n" +
  "GGmvDUtlU5n5Zh70bSuC1hrNCepEMbJWqRZ4dvrdVqZ5RtARd3PYUAiPzwisQF9q\n" +
  "ZPAayyqmDUBReXS71RKRGn47RST+d50fZ3USP1jTAXMxf+X41ml3l7G1zd90IsWL\n" +
  "aIeHIaxi8BVkQogxqfZH8PAzmqtgLEWDfMgWU879qicBW4FB/PoBkP0P6Qlis/50\n" +
  "yY/80UECgYEA+zAkOshLUSJ4MDRMpkpf1WIZABH2lZhhIFw2A/VYnrmCJj3kxJYJ\n" +
  "ELNm82nFVIJGadSarOpownKUteHcJ7Zzv65WoEEZwZBO453I9tL6Fbh64hPp8VdB\n" +
  "4WMvK+0XqhzBL67ehghFNXc9ud4ZIQOXz6KUASxb+Iz0L02iqWIj+RUCgYEA6oJ5\n" +
  "Sh6Ez1lnWDKI5ZEQ1jn+kgcVHObV1o8sB5/5V0/Lihgma+Lpkei333sQsYImWQMD\n" +
  "8BT4JMCpPph5AwM0ZehUF7d2RCtQ+r0A/pUyiXjtMYHDrmAX94zDtf35QUJOL17z\n" +
  "don0weI/vZ71VYX3saa3EvVJLERwpSr0TswfPiUCgYEArLo8D5fwAsjbMPqlwqve\n" +
  "HpOocV3o3JG+KEyAcFRkLjGOh9GD4JLzhOJ45uVS5nv3A4tJGaLPivbTwAaiJ0TV\n" +
  "b3fo5aYemfYr6WV07hXCFvGWvqPG+UhxaxWTOHd/EGFZjvqG1lAVl2B5t7g8O3GH\n" +
  "ESbQ88WXMOFsgKK4OhXceskCgYEA0W/JJvruncg41bn8LRpLsSeGRaBxqKg33jFr\n" +
  "nzuuEd4/54r99WhoNVljrgFYvU+BNAnPYIE5xIkUHcVKffhEuaauQ6gjxWnyHpzh\n" +
  "4Hwa8E/Bdm9v9bH4dauPtl+mVjQDY6cnRHyczPNk/dKTRNgqiMxdwF60BQbym3Ar\n" +
  "VJxUYskCgYA6HWzf+9uHS98Hhr9zW0akjSZbcZclKR53wFMOjE1mFIxp/dC+d6mf\n" +
  "uVcUDTyo/LygzRBA5sd1euBhm5lXPyEHxIHZvwfBhIZWKlCZWlio1UvDbUp1f32u\n" +
  "JMT6q3KeJFJXp7nf5YmrPOKlh1Lm53hiXLSKF/q6Lcnn2lzRD2JDFw==\n" +
  "-----END RSA PRIVATE KEY-----"

async function signTest() {
  let res = await cipher.sign({
    text: "this is a sign test project.",
    key: signKey1
  })

  console.log(`sign text: ${res.sign}`)
}

signTest() 

```
:::

### `hash`
<decl method><pre>
(options: {
  data: string | ArrayBuffer,
  algorithm: string,
  encode?: string
}): Promise&lt;string | ArrayBuffer>
</pre></decl>

`hash` encryption. The functions of each field in the `options` parameter are as follows:
- `data`: The raw data used to generate the digest;
- `algorithm`: The digest algorithm, with optional values `'md5'`, `'sha1'`, `'sha224'`, `'sha256'`, `'sha384'`, `'sha512'`;
- `encode`: The encoding and type of the returned data, with optional values:
  - `'hex'`: Default value, returns a hex-encoded string;
  - `'base64'`: Returns a Base64-encoded string of the encryption result;
  - `'arraybuffer'`: Returns data of type ArrayBuffer;

::: details Sample Code

``` js
async function md5Test(){
  const res = await cipher.hash({
    algorithm: 'md5',
    data: 'hello'
  })
  console.log(res)
}
md5Test() // Print the generated digest, console output
// output：5d41402abc4b2a76b9719d911017c592
```
:::

### `hmac`
<decl method><pre>
(options: {
  data: string | ArrayBuffer,
  algorithm: string,
  key: string | ArrayBuffer,
  encode?: string
}): Promise&lt;string | ArrayBuffer>
</pre></decl>

Generates a keyed-hash message authentication code (HMAC) using the HMAC algorithm. The functions of each field in the `options` parameter are as follows:
- `data`: The raw data used to generate the digest;
- `algorithm`: The digest algorithm, with optional values `'md5'`, `'sha1'`, `'sha224'`, `'sha256'`, `'sha384'`, `'sha512'`;
- `key`: The key;
- `encode`: The encoding and type of the returned data, with optional values:
  - `'hex'`: Default value, returns a hex-encoded string;
  - `'base64'`: Returns a Base64-encoded string of the encryption result;
  - `'arraybuffer'`: Returns data of type `ArrayBuffer`;

::: details Sample Code

``` js
async function hmacTest() {
  let res = await cipher.hmac({
    data: 'hello',
    algorithm: 'sha1',
    key: '1234567890'
  })
  console.log(res)
}
hmacTest() // Print the generated digest, console output
// output：6fce0a55cf8bae80e2cf479b50035f773491c5ad
```
:::

### `base64Encode` <decl type="(data: string | ArrayBuffer): Promise&lt;string>" method />

Performs Base64 encoding on the input data.

### `base64Decode` <decl type="(data: string | ArrayBuffer): Promise&lt;ArrayBuffer>" method />

Performs Base64 decoding on the input data.

::: details Sample Code

``` js
async function base64Test() {
  const originalData = 'Hello, World!';
  const encodedData = await cipher.base64Encode(originalData); // Encode data

  console.log('Encoded Data:', encodedData);

  const decodedArrayBuffer = await cipher.base64Decode(encodedData); // Decode data

  const uint8Array = new Uint8Array(decodedArrayBuffer);
  let decodedData = '';

  for (let i = 0; i < uint8Array.length; i++) {
    decodedData += String.fromCharCode(uint8Array[i]);
  }

  console.log('Decoded Data:', decodedData);
}

base64Test()  // Print the results of encoding and decoding
// Encoded Data: SGVsbG8sIFdvcmxkIQ==
// Decoded Data: Hello, World!
```
:::