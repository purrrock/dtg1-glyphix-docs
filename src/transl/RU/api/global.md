# Глобальный объект

## Глобальные функции

### `encodeURIComponent` <decl type="(str: string): string" function />

Глобальная функция `encodeURIComponent()` используется для кодирования компонента URI `str`. Она экранирует определенные специальные символы в соответствующие шестнадцатеричные escape-последовательности с символом процента (`%`) в кодировке UTF-8, что гарантирует правильную интерпретацию компонента при использовании его в составе URL, особенно в параметрах строки запроса, путях или фрагментах. 

Буквы, цифры и `- _ . ! ~ * ' ( )` не кодируются. Остальные символы кодируются в escape-последовательности с процентом (например, пробел кодируется как `%20`).

Поведение `encodeURIComponent()` идентично [одноименной функции](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent) в веб-среде.

Пример:
```js
console.log(encodeURIComponent("https://example.com/page?id=100"));
// output: https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100
```

### `decodeURIComponent` <decl type="(str: string): string" function />

Глобальная функция `decodeURIComponent()` используется для декодирования компонента URI `str`, закодированного с помощью `encodeURIComponent()`. Она преобразует escape-последовательности с символом процента (`%`) обратно в их исходную форму символов, восстанавливая оригинальный компонент URI. Например, она преобразует `%20` обратно в пробел.

Поведение `decodeURIComponent()` идентично [одноименной функции](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/decodeURIComponent) в веб-среде.

Пример:
```js
console.log(decodeURIComponent("https%3A%2F%2Fexample.com%2Fpage%3Fid%3D100"));
// output: https://example.com/page?id=100
```

### `URI` <decl type="(uri: string | Uri): Uri" function />

Эта функция принимает строку и преобразует ее в объект `Uri` для дальнейшей обработки. Параметр `uri` — это строка URI, которую необходимо распарсить.

Возвращаемое значение представляет собой объект, содержащий следующие поля:
- `scheme: string` — поле scheme, извлеченное из параметра;
- `authority: string` — поле authority, извлеченное из параметра;
- `path: string` — поле path, извлеченное из параметра;
- `query: string` — поле query, извлеченное из параметра;
- `origin: string` — исходная строка URI из параметра;
- `toString: ( string` — этот метод позволяет перекодировать данный объект обратно в строку URI.

Пример:
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

Функция `URI` также принимает в качестве параметра объект. В этом случае функция `URI` добавляет к объекту-параметру метод `toString`, с помощью которого объект URI можно закодировать в строку:
``` js
let uri = {
  scheme: 'https',
  authority: 'app-name',
  path: '/icon.png',
  query: ''
}
console.log(URI(uri).toString()) // 'https://app-name/icon.png'
```