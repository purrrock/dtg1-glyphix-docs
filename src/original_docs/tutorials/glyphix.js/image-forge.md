---
icon: image-filter
---
# 图片管理

glyphix.js 打包工具会管理项目中所有的 PNG 图片资源（ `src` 目录）。相关模块主要提供以下功能：
- 支持图片资源的配置文件，并提供相关配置界面
- 打包时将图片转换为为设备优化的尺寸和格式

应用开发者只需要按自己的需要配置图片资源的打包参数，而设备供应商需要为设备定义具体的图片转换策略。

## 应用开发配置

在应用开发中需要配置图片打包参数才可以正确生成资源包
在应用开发中配置 `config/image-rules.json` 以及 `src/menifest.json` 的 `config.designWidth` 等属性均会影响图片资源的打包行为。`config/image-rules.json` 一般用来配置质量和性能参数，而 `menifest.json` 中的字段影响图片的全局缩放比例（用于适配不同分辨率的设备）。

::: tip
`config/image-rules.json` 可以使用 `gx config` 命令或其他方式配置，但不建议直接用文本编辑器编辑。
:::

如果使用 `gx config` 命令，开发者将主要会关注两个参数：transparent 和 quality。

### Transparent 参数

Transparent 表示图片是否包含透明像素，如果为配置为否（`false`）并且资源图片是包含透明像素的，那么生成时会将这些像素转换为不透明（通常是叠加到一个黑色背景上）。因此需要将必要的图片标记为保留透明像素，否则会显示不正确的覆盖效果。由于某些平台上不透明图片的性能更好，且不透明图片的数据量更少，transparent 选项默认关闭。

### Quality 参数

Quality 参数代表打包后图片的品质，是一个 $[0, 100]$ 范围的整数。不过通常只使用 3 个大致的品质级别：
- High：100，表示最高品质
- Middle：50，中等品质，默认值
- Low：0，低品质

转换图片资源时会根据品质参数进行优化。通常而言，中等品质是在目标平台上平衡了显示效果、绘制/加载性能以及内存资源占用等因素后的转换策略，因此推荐使用。使用高品质可能有更好的质量，但可能产生性能下降。低品质可用于可以损失质量以提升性能的图片（例如如照片）。具体的目标平台也可能忽略 quality 参数而使用统一策略。

## 设备和平台适配

假设设备和平台开发商已经针对具体目标平台实现了优化的图片资源格式并支持多种品质和像素格式，为了在 glyphix.js 中可以生成这些图片格式需要做以下工作：
- 实现**单张图片**转换所需的命令行工具
  - 必须提供从 PNG 图片转换为自定义格式的命令行接口，支持输出到指定路径（包括覆盖原文件）
  - 最好提供从自定义格式转换为 PNG 图片的的命令行接口，支持输出到指定路径（包括覆盖原文件），缺失此功能将无法实现 PC 断预览
- 编写设备描述文件和图片转换脚本

### 图片转换脚本

图片转换脚本是一个 scheme 文件，需要转换图片时 glyphix.js 会调用此脚本，后者可以根据这些变量确定如何转换图片：
- `env.image-path`：待转换图片的绝对路径，转换后的图片覆盖写入到此路径
- `env.transparent`：此图片的透明参数
- `env.quailty`：此图片的品质参数
- `env.target`：转换目标模式，见后文描述
- `env.verbose`：是否开启 verbose 模式，如果是则可以输出详细的日志，否则不应输出日志
- `env.script-dir`：当前脚本文件所在的绝对路径，如果转换所需的命令是相对于此脚本文件而不在 `PATH` 环境变量中，可以利用此参数进行拼接

`env.target` 表示图片转换的**目标模式**，它的值决定具体应用何种转换方式：
- `"device"`：执行针对目标设备的完整转换流程，例如将不透明图片的透明通道移除，然后将其按照品质参数转换为 PGF 格式（Glyphix 图片格式）
- `"emulator"`：执行针对模拟器的转换流程，由于模拟器并不支持特定硬件的纹理格式（例如 ETC2 等），为了保证图片在模拟器中正常显示，可以只移除不透明图片的透明通道而不进一步转换为目标设备格式（或者转换为软件支持的 PGF 格式）
- `"preprocess"`：只执行预处理步骤，也就是移除不透明图片的透明通道，并且要将结果输出为 PNG 格式
- `"preview"`：生成预览的 PNG 图片，首先要按照 `"device"` 目标的转换流程将图片转换为自定义目标格式，然后将输出图片转回 PNG 供预览使用

::: tip
如果图片转换的命令行工具不支持将自定义格式转换为 PNG，那么不要实现 `"preprocess"` 和 `"preview"` 目标模式。
:::

### image-forge 命令行工具

image-forge 是 Glyphix 提供的 PGF 图片格式命令行工具，具有以下功能：
- 支持 PNG 图片转换为 PGF 格式，以及将 PGF 转换为 PNG 图片
- 支持常见的 ARGB 和 PAL 像素格式，且区分 premultiplied alpha 模式
- 支持将透明的 ARGB 图片混合到指定的纯色背景上使之转换为不透明图片（不是直接丢弃 alpha 通道）
- 支持行按像素或字节对齐
- 支持 LZ4 压缩，并可以设置最小压缩阈值（低于阈值的图片数据不会压缩）

对于使用其他自定义图片格式的平台，也可以利用 image-forge 来移除透明通道。

## 图片转换脚本示例

以下示例演示如何利用 image-forge 等命令将 PNG 转换为 PGF 图片，并且优先使用查色表（PAL）格式。

首先定义不透明和透明情况下的目标格式：
``` scheme
; 定义不透明颜色的像素格式规则
(define (opaque-formats q)
  (cond ((<= q 50) "pal-rgb")
        (else "rgb24")))

; 定义透明颜色的像素格式规则
(define (transparent-formats q)
  (cond ((<= q 50) "pal-argb-premul")
        (else "argb32-premul")))

; 计算透明和品质参数作用下的目标像素格式
(define pixel-format
  ((if env.transparent
      transparent-formats opaque-formats)
    env.quailty))

; 图片是否转换为查色表格式
(define palette (<= env.quailty 50))
```

以上代码会在品质小于等于 50 时使用查色表格式，并且会根据是否透明使用 `pal-rgb` 或 `pal-argb`。质量高于 50 时使用 RGB 或 ARGB 8bit 位采样的像素格式。最终，`pixel-format` 变量即实际使用的像素格式名称，`palette` 表示是否使用查色表格式。

接下来定义各种情况下需要使用的命令：

``` scheme
; 是否添加 --verbose 命令行参数
(define if-verbose (if env.verbose "--verbose " ""))

; 调用 pngquant 命令将图片颜色缩减至 256 色以内，系统中需要安装 pngquant
(define color-reduction
  (string-append "pngquant --ext=.png --force " if-verbose env.image-path))

; 转换图片为 PGF 格式
(define convert (string-append "image-forge "
  "--format=" pixel-format " " ; 指定输出像素格式
  "--compress --min-compress-ratio=5 " ; 压缩图像数据减小文件尺寸，最小压缩比为 5
  "--align=16 --pixel-align " ; 图片按 16 像素对齐
  if-verbose
  env.image-path))

; 移除图片 Alpha 通道并添加背景
(define remove-alpha (string-append "image-forge --bypass "
  ; 在 bes2500ibp 手表上，非透明图片可以移除 alpha 通道并用黑色背景混合，这种操作可以提高 PAL 颜色缩减后的图像质量
  (if env.transparent "" "--background black ")
  if-verbose
  env.image-path))

; 将 PGF 图像转回 PNG 的命令
(define decode
  (string-append "image-forge --decode " if-verbose env.image-path))
```

以下代码中，`execute-try` 在命令非 0 退出后调用指定的 `f` 函数，`execute` 函数在命令非 0 退出后打印错误日志并异常退出脚本。`run-convert` 函数执行完整的目标设备图像转换流程（调用 `remove-alpha` 和 `convert` 的命令）。

``` scheme
; 执行一个命令并在 verbose 模式中打印命令内容，如果命令以非 0 异常退出则调用函数 f
(define (execute-try cmd f)
  (begin
    (if env.verbose ; 如果为 verbose 模式则打印命令内容
      (display (string-append "Run command: " cmd "\n")))
    (let ((r (system (string-append env.script-dir "/bin/" cmd))))
      (if (= r 0) 0 (f r)))
  ))

; 执行一个命令，并会在 verbose 模式打印命令内容，如果命令异常退出则退出程序
(define (execute cmd)
  (execute-try cmd (lambda (x)
    (begin ; 失败时打印错误码并异常退出
      (display (string-append "subprocess failed (" (number->string x) "): " cmd "\n"))
      (exit-fail)
  ))))

; 转换图像
(define (run-convert)
  (begin
    (execute remove-alpha) ; 先移除透明通道
    (if palette (execute color-reduction)) ; 如果是查色表格式则缩减图片的像素数量
    (execute convert) ; 执行图片转换命令
  ))
```

`targets` 宏定义所有目标模式的处理方法，例如 `"device"` 模式将调用 `run-convert` 函数等。

``` scheme
; 定义目标对应的转换策略
(targets env.target
  ; 设备模式：最终用于目标设备的图片转换流程
  ("device" (run-convert))
  ; 模拟器模式：仅移除非透明图片的 alpha 通道，不转换格式
  ("emulator" (execute remove-alpha))
  ; 预处理模式：移除非透明图片的 alpha通道并添加背景
  ("preprocess" (execute remove-alpha))
  ; 预览模式：生成和实际设备显示效果一致的 PNG 预览图片
  ("preview" (begin
    (run-convert) ; 先把图片转换为 PGF 格式
    (execute decode))) ; 再把图片转回 PNG
  )
```

### 使用图片转换脚本

要使用图片转换脚本，需要在设备型号描述文件中增加一个字段：

``` yaml
description: default watch

screen:
  width: 454 # pixels
  height: 454 # pixels
  dpi: 326 # pixels per inch

#...
image-build: image-convert-pal.scm # 图片转换脚本相对于本 Yaml 文件的路径
```

### 更复杂的策略

由于图片转换脚本是完整的编程语言而不是 Yaml、JSON 等配置语言，我们可以实现更复杂的自定义转换策略而不会受限于框架提供的功能。以上面的查色表格式转换为例：PAL 格式在颜色丰富的图片上效果不好，此时可以将图片转换为在这类场景中表现更好的格式。具体的思路为：
1. `pngquant` 命令支持在转换 PAL 格式后质量低于指定值的情况下异常退出，因此按照此目的配置命令参数
2. 在 `run-convert` 函数由 `execute` 执行的 `color-reduction` 的操作改为由 `execute-try` 执行，并在后者的异常处理函数中使用替代格式的转换操作
3. `preview` 等目标的处理方式类似，但要注意，在将输出格式转换为 PNG 的时候，也需要识别命令异常退出并改由后续的命令继续尝试

总而言之类似于 shell 脚本的思路，利用命令的异常退出码来控制流程。
