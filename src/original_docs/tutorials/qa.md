---
icon: help-circle-outline
---
# 常见问题解答

## 打包工具

### 项目构建问题

#### `Lisp Error: thread killed` 报错

具体的现象是出现类似以下的报错信息：

``` log
[ 47%] Process image src/assets/images/frame1.png
error: Lisp Error: thread killed
```

这个问题是由于前面某一项构建出错，导致正在执行的图片转换构建操作被取消。只需要修复 `fatal` 报错的构建操作即可恢复，无需专门处理。

### 模拟器

#### 模拟器默认语言

模拟器默认语言为 `zh-CN`。因此，如果你添加了[国际化](/framework/component/i18n.md)配置将默认使用 `zh-CN.json` 翻译文件。用 `gx` 命令运行模拟器可以使用 `-l` 或 `--language` 选项来指定语言：
``` shell
gx emu -l en-US # 使用美式英语
```
你也可以在模拟器运行时用 inspector 调试工具动态更改语言。
