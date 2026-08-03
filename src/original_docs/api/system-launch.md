# 应用跳转

## 导入模块

``` js
import launch from '@system.launch'
```

## 接口定义

### `launch` <decl type="(app: string): Promise<bool>" method/>

启动指定应用并切换到前台。`app` 是一个已经安装的应用 ID 字符串。返回的 Promise 表示应用是否加载成功。

### `inactive` <decl type="(app?: string): Promise<void>" method/>

将应用切换到后台。`app` 是一个已启动应用的 ID，不指定参数时会将当前应用切换到后台。只有前台应用可以切换到后台。

### `exit` <decl type="(app?: string): Promise<void>" method />

退出一个应用。参数 `app` 是一个已启动应用的 ID，不指定参数时会退出当前应用。

### `getRunning` <decl type="(): string[]" method />

获取正在运行的应用包名列表，包括那些在后台的应用。
