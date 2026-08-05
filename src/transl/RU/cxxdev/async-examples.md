# Пример асинхронной разработки

Если вам кажется, что раздел [Разработка асинхронного функционала](async.md) слишком объемный и недостаточно интуитивный, в этом документе приведены типичные и более простые примеры, которые помогут вам справиться с распространенными сценариями асинхронной разработки.

Эти сценарии не являются предельно сложными, но они фокусируются на следующих аспектах:
- Типичный паттерн асинхронного вызова с акцентом на межпоточный и межъязыковой характер взаимодействия;
- Более мелкие задачи, предполагающие интеграцию с большим количеством системных API, что делает код чувствительным к раздуванию (code bloat);
- Наличие типичных требований к взаимодействию с C API, а не со стандартными интерфейсами C++.

Вы можете найти полную реализацию этих сценариев в примерах SDK и запустить их в эмуляции на ПК.

## Сценарий: Интеграция с интерфейсом C-будильника

Распространенным асинхронным паттерном в встраиваемых системах является «C-коллбэк» (C Callback): вызывающий код передает задачу и указатель на функцию в качестве уведомления о завершении, а после завершения операции поток worker вызывает этот коллбэк.

::: important async поддерживает только модель потоков
Асинхронный функционал фреймворка Glyphix поддерживает только обычный контекст потоков и не может использоваться в прерываниях (interrupts). Если ваш асинхронный контекст — это обработчик прерывания, вам следует выделить отдельный поток для перенаправления.
:::

Рассмотрим в качестве примера службу будильника. Предоставляемый ею асинхронный C API выглядит следующим образом:

```c
// На примере alarm_async_create, остальные операции устроены аналогично
void alarm_async_create(AlarmService *svc, uint32_t interval_ms, ...,
                        alarm_create_cb_t done_cb, void *done_ctx);

// Тип указателя на функцию завершения (коллбэк), вызывается в потоке worker
typedef void (*alarm_create_cb_t)(alarm_err_t err, alarm_id_t id, void *ctx);
```

Далее мы расскажем, как связать подобные типичные C-коллбэки с JavaScript Promise.

### Совместное использование типа Session для нескольких операций

Служба будильника имеет набор операций: `create`, `cancel`, `setEnabled`, `update`, `snooze`, `getInfo`, `list`, `count` и т. д. Если определять отдельный класс клиента (client) для каждой операции, это приведет к огромному количеству инстациаций шаблонов.

Для таких сценариев, когда «вся реальная логика выполняется на стороне C, а в C++ происходит лишь передача параметров», можно определить легкий клиент, содержащий только маппинг кодов ошибок, и позволить всем операциям совместно использовать один экземпляр `ResultSession`:

```cpp
struct AlarmClient {
    // Преобразует alarm_err_t из C-уровня в читаемую строку ошибки,
    // которая передается в catch на стороне JavaScript при отклонении (reject) Promise.
    static const char *errorMessage(async::Status status) {
        status_t err = status.value();
        switch (err) {
        case ALARM_OK:              return "ok";
        case ALARM_ERR_NOT_FOUND:   return "not_found";
        case ALARM_ERR_TABLE_FULL:  return "table_full";
        case ALARM_ERR_INVALID_ARG: return "invalid_arg";
        default:                    return "unknown_error";
        }
    }
};

// Все операции с будильником используют один и тот же тип Session
using AlarmSession = async::ResultSession<AlarmClient>;
```

`AlarmClient` не нужно реализовывать метод `resolve()`, поскольку здесь не используется стандартный пул потоков-исполнителей (executor): фактическая асинхронная операция выполняется потоком worker службы будильника, а сторона C++ отвечает лишь за доставку результата обратно в поток UI.

### Базовый паттерн привязки (Binding)

На примере `alarm.create()` рассмотрим полный процесс привязки:

```cpp
static JsValue jsAlarmCreate(JsCtx ctx) {
    auto *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1 || !ctx.arg(0).isObject())
        return JsValue{};

    // Чтение параметров из объекта options, переданного из JavaScript
    const JsValue &opts = ctx.arg(0);
    uint32_t intervalMs = static_cast<uint32_t>(opts["interval"].toInt());
    String label        = opts["label"].toString();
    alarm_repeat_t mask = parseRepeatMask(opts["repeat"]);

    // Создание сессии и извлечение коллбэков resolve/reject из объекта options (поддерживает два стиля асинхронности)
    auto *session = async::make<AlarmSession>(applet);
    session->setResolver(opts);

    // C-коллбэк: вызывается в потоке worker, уведомляет JavaScript через resolve() кросс-потоково
    auto done = +[](alarm_err_t err, alarm_id_t id, void *data) {
        auto *s = static_cast<AlarmSession *>(data);
        s->resolve(err == ALARM_OK
            ? async::Result<int>(id) // Успех: resolve с ID нового будильника
            : async::Status(err));   // Ошибка: reject, сообщение об ошибке берется из errorMessage()
    };

    // Вызов асинхронного C API создания будильника, передача коллбэка и указателя на сессию
    alarm_async_create(AppletAlarmService::instance(),
                       intervalMs, mask, label.c_str(), /*...*/,
                       onAlarmFired, nullptr, done, session);
    // Возврат объекта Promise в JavaScript, фреймворк автоматически разрешит его при вызове resolve()
    return session->promise();
}
```

Здесь есть несколько стандартных шаблонов, которые можно использовать повторно:

- `async::make<AlarmSession>(applet)` создает сессию и привязывает ее к текущему апплету (Applet) для соблюдения требований жизненного цикла.
- `session->setResolver(opts)` позволяет одному и тому же коду одновременно поддерживать [стиль коллбэков и стиль Promise](/api/README.md#快应用异步接口) асинхронных вызовов.
- `+[](... void *data)` превращает лямбду в обычный указатель на функцию с помощью унарного оператора `+`, удовлетворяя требованиям типа C-коллбэка.
- Передача `session` в качестве `void *` в C API, с последующим приведением типов обратно в коллбэке и вызовом `resolve()`.
- `resolve()` является потокобезопасным (thread-safe): он упаковывает результат в событие и отправляет его обратно в поток UI, который затем разрешает Promise.

::: tip Использование лямбда-выражений для написания коллбэков
В C коллбэк обычно представляет собой статическую функцию. Вы можете использовать лямбда-выражения C++ для вложенного определения функции обратного вызова прямо на месте, например:
```cpp
auto done = +[](alarm_err_t err, alarm_id_t id, ...) { ... }
alarm_async_create(..., done, session);
```
Это позволяет избежать определения большого количества отдельных статических функций, делая код более компактным и понятным.
:::

Структура остальных операций (`cancel`, `setEnabled`, `snooze` и т.д.) абсолютно одинакова, различаются только чтение параметров и вызовы C API:

```cpp
static JsValue jsAlarmCancel(JsCtx ctx) {
    auto *applet = Applet::current(ctx.vm());
    if (!applet || ctx.argc() < 1)
        return JsValue{};

    alarm_id_t id = ctx.arg(0).toInt();

    auto *session = async::make<AlarmSession>(applet);
    session->setResolver(ctx.arg(0));

    auto done = +[](alarm_err_t err, void *data) {
        // Когда нет возвращаемого значения, просто используйте resolve<void>
        static_cast<AlarmSession *>(data)->resolve<void>(async::Status(err));
    };
    alarm_async_cancel(AppletAlarmService::instance(), id, done, session);

    return session->promise();
}
```

::: important Не пропускайте проверку параметров
`session->setResolver(ctx.arg(0))` зависит от проверки `ctx.argc()`. Если в начале функции нет проверки количества параметров, вам нужно проверить его при вызове `setResolver()`:
```cpp
session->setResolver(ctx.argc() ? ctx.arg(0) : JsValue{});
```
:::

### Регистрация преобразования типов для пользовательских C-структур

`alarm.getInfo()` возвращает структуру `alarm_info_t`, которую необходимо преобразовать в объект JavaScript. Для этого сначала специализируйте `js_cast<T>` в пространстве имен `gx`:

```cpp
template<> JsValue gx::js_cast<alarm_info_t>(const alarm_info_t &info) {
    JsValue obj = JsVM::current().newObject();
    obj["id"]          = info.id;
    obj["label"]       = info.label;
    obj["interval"]    = double(info.interval_ms);
    obj["repeatMask"]  = info.repeat_mask;
    obj["enabled"]     = bool(info.enabled);
    obj["remaining"]   = double(info.remaining_ms);
    obj["fireCount"]   = int(info.fire_count);
    obj["snooze"]      = int(info.snooze_ms);
    obj["snoozed"]     = bool(info.snoozed);
    return obj;
}
```

После завершения специализации просто передайте экземпляр структуры в `resolve()` внутри функции привязки:

```cpp
auto done = +[](alarm_err_t err, const alarm_info_t *info, void *data) {
    auto *s = static_cast<AlarmSession *>(data);
    if (err != ALARM_OK || !info) {
        // Путь ошибки: возврат статуса ошибки для вызова reject, сообщение из errorMessage()
        s->resolve<alarm_info_t>(async::Status(err));
        return;
    }
    s->resolve<alarm_info_t>(*info);  // Фреймворк автоматически вызывает js_cast в потоке UI
};
alarm_async_get_info(AppletAlarmService::instance(), id, done, session);
```

::: tip
`js_cast()` вызывается фреймворком после того, как результат возвращается в поток UI, а не в потоке worker. Это означает, что внутри `js_cast()` можно безопасно использовать специфичные для потока UI API, такие как `JsVM::current()`.
:::

Для таких операций, как `alarm.list()`, возвращающих массив, вы можете напрямую сконструировать `std::vector<int>` и сделать resolve без определения дополнительных преобразований типов:

```cpp
auto done = +[](alarm_err_t /*err*/, const alarm_id_t *ids, int count, void *data) {
    auto *s = static_cast<AlarmSession *>(data);
    s->resolve<std::vector<int>>(std::vector<int>{ids, ids + count});
};
alarm_async_list(AppletAlarmService::instance(), done, session);
```

### Коллбэк срабатывания будильника: передача событий обратно в JavaScript

Когда будильник срабатывает, уровень C вызывает коллбэк `alarm_fire_cb_t` из потока worker. Этот сценарий немного отличается от предыдущего «результата запроса» и требует специального проектирования механизма уведомления о событиях.

#### Почему не используются коллбэки JavaScript

Интуитивно кажется разумным позволить приложению передавать функцию обратного вызова при создании будильника:

```javascript
// ❌ Это не работает в сценарии с будильником
alarm.create({ interval: 60000, onFired: (event) => { /* ... */ } })
```

Проблема в том, что будильники выходят за рамки жизненного цикла приложения: после создания будильника приложение может быть уничтожено в любой момент до его срабатывания; кроме того, многие устройства поддерживают срабатывание будильника после перезагрузки.

Функция обратного вызова JavaScript (`JsValue`) действительна только в среде выполнения JavaScript текущего экземпляра приложения. Как только приложение закрывается, эта среда выполнения вместе со всеми `JsValue` уничтожается. В этот момент у стороны C++ нет возможности продолжать хранить этот JavaScript-коллбэк, не говоря уже о его вызове при срабатывании будильника.

Это проблема не только будильников: **любое событие, которое может произойти в течение жизненного цикла за пределами работы приложения, не может быть разрешено с помощью коллбэков JavaScript**, например, задачи по расписанию, офлайн-пуш-уведомления, уведомления о завершении фоновой загрузки и т. д.

#### Использование предопределенных имён методов вместо ссылок на коллбэки

Самое простое решение: приложение не «регистрирует коллбэк», а система проактивно **запускает** приложение при возникновении события и вызывает метод обработки на объекте приложения с заранее оговоренным именем.

Это согласуется с идеологией функций жизненного цикла приложения (`onCreate`, `onShow` и т.д.) — система запускает приложение по требованию, вызывая известную точку входа, вместо того чтобы хранить заранее зарегистрированный коллбэк. Приложение реализует соответствующий метод согласно соглашению:

```javascript
// app.js — метод обработки, экспортируемый объектом модели приложения (реализуется по соглашению)
export default {
  onAlarmFired(event) {
    // event: { id, label, interval, ... }
    console.log('alarm fired:', event)
  }
}
```

Реализация на стороне C++: сначала чтение снимка состояния (snapshot) в потоке worker, затем переключение обратно в главный поток для запуска приложения и вызова метода:

```cpp
static void onAlarmFired(alarm_id_t id, void * /*user_data*/) {
    // Чтение снимка состояния в потоке worker во избежание межпоточного доступа к таблице будильников
    alarm_info_t info{};
    alarm_get_info(id, &info);

    // Переключение обратно в главный поток перед взаимодействием с JavaScript
    App()->postTask([info] {
        auto *svc = AppletAlarmService::instance();
        // Запуск (или пробуждение) целевого приложения с помощью launch(), даже если оно сейчас не запущено
        auto *applet = AppletKit::instance()->launch(svc->alarmAppletName);
        if (!applet) return;

        auto &vm = JsVM::current();
        // Вызов согласованного метода на экспортированном объекте app.js, параметры события — объект JS с информацией о будильнике
        JsValue event = js_cast(info);
        applet->modelObject().callMethod("onAlarmFired", {event}).reportError();
    });
}
```

Несколько ключевых моментов:

- **Не** взаимодействуйте с `JsValue` и не вызывайте никакие JavaScript API напрямую из потока worker, их можно использовать только в потоке UI.
- Используйте `App()->postTask()` для отправки замыкания в главный цикл событий — это самый простой способ вернуться в поток UI.
- Используйте `AppletKit::launch()` вместо поиска существующего экземпляра; `launch()` перезапускает приложение, если оно не существует, и возвращает существующий экземпляр, если оно уже запущенно.
- Метод `.reportError()` у возвращаемого значения `callMethod()` запишет возможные исключения JavaScript в лог, вместо того чтобы игнорировать их молча.

::: tip Согласованные имена методов — самый простой способ обработки событий
Этот паттерн можно понимать так: экспортируемый объект `app.js` — это «набор точек входа», которые приложение предоставляет системе, и система вызывает методы в нем по мере необходимости, точно так же, как вызывает `onCreate` или `onShow`.

Этот метод не является универсальным, но его вполне достаточно для контролируемых системных приложений. Он прост в реализации и не требует сложной персистентности и механизмов управления коллбэками.
:::

### Регистрация загрузчика библиотек (Library Loader)

После написания всех функций привязки их необходимо «собрать» в [объект библиотеки](native-module.md#library-loader), который может импортировать JavaScript, и зарегистрировать во фреймворке.

Загрузчик библиотек — это функция C++, которая вызывается, когда приложение вызывает `app.loadLibrary('vendor.alarm')`. Она отвечает за создание и возврат объекта JavaScript, содержащего все экспортируемые методы:

```cpp
static JsValue libAlarmLoader(Applet *applet) {
    // Здесь можно проверить имя пакета приложения и отклонить неавторизованные приложения. Также можно проверить поля.
    if (!applet || applet->objectName() != "com.vendor.alarm")
        return JsValue{};

    JsValue lib = JsVM::current().newObject();

    // Привязка функций к объекту библиотеки, имя свойства — это имя метода, вызываемого со стороны JavaScript
    lib["create"]     = jsAlarmCreate;
    lib["cancel"]     = jsAlarmCancel;
    lib["list"]       = jsAlarmList;
    lib["count"]      = jsAlarmCount;
    // ...
    return lib;
}
```

Затем зарегистрируйте загрузчик в `AppletKit` на этапе инициализации:

```cpp
AppletKit kit{&window};
kit.setLibraryLoader("vendor.alarm", libAlarmLoader);
```

На стороне JavaScript импорт осуществляется через `app.loadLibrary()`, а возвращаемое значение — это объект библиотеки, возвращенный загрузчиком:

```javascript
const alarm = app.loadLibrary('vendor.alarm')

const id = await alarm.create({ interval: 60000, label: 'Подъем' })
```