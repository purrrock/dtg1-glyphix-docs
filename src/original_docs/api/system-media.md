# 多媒体

## 导入模块

``` ts
import media from '@system.media'
```

## 接口定义

### `createAudioPlayer` <decl type="(): AudioPlayer" method />

创建一个 [`AudioPlayer`](#audioplayer-对象) 对象。

### `createAudioRecord` <decl type="(): AudioRecorder" method />

创建一个 [`AudioRecorder`](#audiorecorder-对象) 对象。

开发者需要在 [`manifest.json`](/framework/application/manifest.md#permissions) 文件中声明应用对 `watch.permission.RECORD` 的访问权限。

### `setVolume` <decl type="(volume: number): void" method />

设置系统媒体音量，参数 `volume` 是 $[0.0, 1.0]$ 之间的音量值。此属性用于系统媒体音量的控制，具体功能取决于平台实现，调整音量应优先使用`AudioPlayer`对象的`volume`属性。

### `getVolume` <decl type="(): number" method />

获取系统媒体音量，结果是 $[0.0, 1.0]$ 之间的音量值。此属性用于系统媒体音量的获取，具体功能取决于平台实现，获取音量应优先使用`AudioPlayer`对象的`volume`属性。

## `AudioPlayer` 对象

::: details 类型签名
``` ts
interface AudioPlayer {
  src: string,
  name: string,
  icon: string,
  mode: string,
  status: string,
  duration: number,
  position: number,
  openSystemNotification: bool,
  songAttribute: object,
  volume: number,
  nextAvailable: bool,
  prevAvailable: bool,

  play(): void,
  pause(): void,
  stop(): void,
  release(): void,
  next(): void,
  previous(): void,
  requestFocus({acquireType: string, volumeType: string}): void,
  releaseFocus(): void,

  onplay?: () => void,
  onpause?: () => void,
  onstop?: () => void,
  onended?: () => void,
  onerror?: (err: {msg: string})=> void,
  ontimeupdate?: () => void,
  oninterrupt?: (action: {interruptHint: number}) => void,
  onnext?: () => void,
  onprevious?: () => void,
  onrequestplay?: () => void,
  onrequestpause?: () => void,
  onrequeststop?: () => void,
  onsongattribute?: () => void,
  onposition?: () => void,
  onrequestfocus?: () => void,
  onreleasefocus?: () => void,
  onmodechanged?: () => void,
  onvolumechange?: () => void,
}
```
:::

### `src` <decl type="string" set get />

设置或读取需要播放音频的 url。支持[本地资源路径](/framework/application/resource.md#uri-和路径)与使用http、https协议的网络资源路径（例如：`https://www.rt-thread.com/service/test/001.mp3`）。下面是一个设置 src 然后开始播放的简单示例：

```ts
import media from '@system.media'
// 创建音频播放器
let player = media.createAudioPlayer()
// 设置需要播放的音频url
player.src = 'https://www.rt-thread.com/service/test/001.mp3'
// 开始播放音频
player.play()
```

### `name` <decl type="string" set get />

播放器对象的名字，如果不设置，默认为创建播放器的应用名。需要注意的是，播放器对象的名字并不是全局不唯一，并不能使用名字来标识播放器对象。

### `icon` <decl type="string" set get />

播放器对象的图标 url。支持[本地资源路径](/framework/application/resource.md#uri-和路径)

### `mode` <decl type="string" set get />

播放模式。该属性对应的功能应由播放器应用实现，播放器对象默认不处理，只提供该属性。

- `sequential`：顺序播放  
- `random`：随机播放  
- `singleloop`：单曲循环  
- `listloop`：列表循环  

### `status` <decl type="string" get />

读取当前播放器状态

- `play`：正在播放状态  
- `pause`：暂停播放状态  
- `stop`：停止播放状态 
- `ended`：播放结束状态  
- `error`：播放错误状态  

### `duration` <decl type="number" get />

音频总时长，单位：秒

### `position` <decl type="number" set get />

当前音频播放的时间位置，单位：秒

### `openSystemNotification` <decl type="bool" set get />

是否开启系统通知，默认不开启。开启后，此播放器对象才可以被[音频播放器管理器](/framework/application/system-audioPlayerManager.md#音频播放器管理器)查询到。

### `songAttribute` <decl type="songAttribute" set get />

歌曲属性对象

::: details 类型签名
```ts
type songAttribute = {
  title: string; // 歌曲的名称
  artist: string; // 表演者的名称，可以是个人或者乐队
  album: string; // 歌曲所属的专辑名称
  year: string; // 歌曲的发行年份
  genre: string; // 歌曲的类型，例如流行、摇滚、古典等
  track: string; // 当前歌曲在专辑中的编号，例如："1/12" 表示第1首，共12首
  coverArt: string; // 歌曲封面图片的url
  lyrics: string; // 歌词文本的 url
  comments: string; // 额外信息，如版权备注等
}
```
:::

songAttribute对象与AudioPlayer对象一样是一个Proxy对象，即不能使用JSON序列化与反序列化，也不能在响应式框架中引用。下面是一个简单的使用示例：

```ts
// 设置歌曲的名字
this.player.songAttribute.title = "未知"
// 设置歌曲演唱者
this.player.songAttribute.artist = "未知"
// 查看歌曲的名字
console.dir(this.player.songAttribute.title)
```

### `volume` <decl type="number" set get />

当前播放器的音量，范围：[0.0, 1.0]

### `nextAvailable` <decl type="bool" set get />

设置或查询是否可以切换下一曲

### `prevAvailable` <decl type="bool" set get />

设置或查询是否可以切换上一曲

### `play` <decl type="(): void" method />

开始播放在 src 属性中指定的音频

- 如果在调用此方法之前未设置 src 属性，会导致播放失败，触发 onerror 事件；
- 此方法为同步接口，执行此接口后，需要等待 onplay 事件或者 onerror 事件来判定播放成功或失败，在事件未触发之前，执行的额其它操作会被忽略；  

下面是一个调用play() 接口的简单示例：

```ts
import media from '@system.media'
// 创建音频播放器
let player = media.createAudioPlayer()
// 设置需要播放的音频url
player.src = 'https://www.rt-thread.com/service/test/001.mp3'
// 设置 onplay 事件
player.onplay = () => { console.dir("开始播放") }
// 设置 onerror 事件
player.onerror = () => { console.dir("播放错误") }
// 开始播放音频
player.play()
```

### `pause` <decl type="(): void" method />

暂停播放当前音频  

- 此方法为同步接口，执行此接口后，需要等待 onpause 事件或者 onerror 事件来判定暂停成功或失败，在事件未触发之前，执行的额其它操作会被忽略；  

### `stop` <decl type="(): void" method />

停止音频播放，可以通过 play 重新播放音频  

- 此方法为同步接口，执行此接口后，需要等待 onstop 事件或者 onerror 事件来判定停止成功或失败，在事件未触发之前，执行的额其它操作会被忽略；  

### `release` <decl type="(): void" method />

释放音频资源  

- 执行此接口会停止播放当前音频，需要等待 onstop 事件或者 onerror 事件来判定停止成功或失败，在事件未触发之前，执行的额其它操作会被忽略；   

### `next` <decl type="(): void" method />

通知播放器应用，播放下一首。执行此接口后，会触发 onnext 事件通知监听此事件的播放器应用，由播放器应用执行歌曲切换的逻辑。

### `previous` <decl type="(): void" method />

通知播放器应用，播放下一首。执行此接口后，会触发 onprevious 事件通知监听此事件的播放器应用，由播放器应用执行歌曲切换的逻辑。

### `requestFocus` <decl type="({acquireType: string，volumeType: string}): void" method />

请求音频焦点。执行此接口后，会通知底层请求或者释放音频焦点，由底层控制不同类型音频的切换与打断逻辑。

`acquireType` 参数指示请求类型：
- `gain`：请求音频焦点
- `loss`：释放音频焦点

`volumeType` 参数指示音频类型：
- `system`：系统提示
- `media`：媒体音乐
- `tts`：语音播报

以下示例演示 `requestFocus` 函数请求音频焦点的方法：
``` ts
import media from '@system.media'
// 创建音频播放器
let player = media.createAudioPlayer()
// 获取媒体音乐类型的音频焦点
player.requestFocus({ volumeType: 'media', acquireType: 'gain' });
```

### `releaseFocus` <decl type="(): void" method />

释放音频焦点。执行此接口后，会通知底层释放音频焦点，由底层控制不同类型音频的切换与打断逻辑。

### `onplay` <decl type="?: () => void" set />

在音频 play 成功后的回调事件

### `onpause` <decl type="?: () => void" set />

在音频 pause 成功后的回调事件

### `onstop` <decl type="?: () => void" set />

在音频 stop 成功后的回调事件

### `onended` <decl type="?: () => void" set />

在音频播放结束后的回调事件

### `onerror` <decl type="?: () => void" set />

执行`play` `pause` `stop` `position`等接口发生错误的回调事件，发生错误时， 对应的 onplay 等事件不会被触发

### `ontimeupdate` <decl type="?: () => void" set />

在 position 属性更新时会触发的回调事件，此事件只有应用处于前台时才会触发，当应用处于后台时会停止派发。

### `oninterrupt` <decl type="?: (action: {interruptHint: number}) => void" set />

发生音频打断事件时的回调函数，当前音频被相同音频类型或其它音频类型的音频抢夺时，被暂时打断或彻底打断的通知。

`action` 参数的 `interruptHint` 指示打断事件的类型：
- `1`：短暂打断 （可以自动恢复，如：音乐被打断）
- `2`：彻底打断 （不可自动恢复，如：网易云被喜马拉雅打断）

以下示例演示注册 `oninterrupt` 回调函数的方法，该函数会在事件发生时调用：
``` js
player.oninterrupt = (action) => {
  console.log(action.interruptHint)
}
```

### `onnext` <decl type="?: () => void" set />

需要播放下一曲时的回调事件

### `onprevious` <decl type="?: () => void" set />

需要播放上一曲时的回调事件

### `onrequestplay` <decl type="?: () => void" set />

底层需要启动播放时触发该回调事件通知js应用，由js应用执行启动播放的逻辑

### `onrequestpause` <decl type="?: () => void" set />

底层需要暂停播放时触发该回调事件通知js应用，由js应用执行暂停播放的逻辑

### `onrequeststop` <decl type="?: () => void" set />

底层需要停止播放时触发该回调事件通知js应用，由js应用执行停止播放的逻辑

### `onsongattribute` <decl type="?: () => void" set />

歌曲属性对象发生变化时的回调事件

### `onposition` <decl type="?: () => void" set />

执行 `position` 设置当前音频播放的时间位置成功的回调事件

### `onrequestfocus` <decl type="?: () => void" set />

请求音频焦点成功时的回调事件

### `onreleasefocus` <decl type="?: () => void" set />

释放音频焦点成功时的回调事件

### `onmodechanged` <decl type="?: () => void" set />

播放模式发生变化时的回调事件

### `onvolumechange` <decl type="?: () => void" set />

播放器音量发生变化时的回调事件


## `AudioRecorder` 对象

::: details 类型签名
``` ts
interface AudioRecorder {
    start({
      uri: string, 
      sample?: 8000 | 16000 | 44100 | 48000,
      layout?: 8 | 16 | 32,
      channel?: 1 | 2,
      bitrate?: 16 | 32 | 64,
      codec?: "pcm" | "mp3" | "opus" | "silk",
      format?: "ogg",
    }): Promise<void>,
    read({callback: (ArrayBuffer) => void}): void,
    stop(): void,
    release(): void,
    onstart?: () => void,
    onstop?: () => void,
    onrelease?: () => void,
    onavailable?: (ArrayBuffer) => void,
    onerror?: ({error: string})=> void
}
```
:::

### `start`
<decl method><pre>
(options: {
  uri: string,
  sample?: 8000 | 16000 | 44100 | 48000,
  layout?: 8 | 16 | 32,
  channel?: 1 | 2,
  bitrate?: 16 | 32 | 64,
  codec?: "pcm" | "mp3" | "opus" | "silk",
  format?: "ogg",
}): Promise&lt;void>
</pre></decl>

开始录制音频，`options` 参数的各字段功能为：
- `uri`：需要存储的录音文件 URI，只支持 `internal` 协议，会自动创建目录；
- `sample`：音频采样率，单位为 $\rm Hz$，默认为 $8000$；
- `layout`：音频数据位深度，默认为 $16$；
- `channel`：音频声道数，默认为 $1$；
- `bitrate`：音频码率，单位为 $\rm kbps$，默认为 $16$，码率越高，音质越好但文件也越大。
- `codec`：音频编码格式，字符串类型，如果不填写，则根据`format`参数自动匹配一个合适的编码；
- `format`：音频封装格式，字符串类型，如果不填写，则根据`uri`参数的后缀名自动匹配一个合适的封装；

  常用的录音格式、编码格式以及封装格式的支持关系如下（表格中的无，表示对应的参数可以不用填写）：

  | 常用的录音格式 | codec(编码格式) | format(封装格式) |
  | -------------- | --------------- | ---------------- |
  | pcm            | 无              | 无               |
  | mp3            | mp3             | 无               |
  | opus           | opus            | 无               |
  | opus-ogg       | opus            | ogg              |
  | silk           | silk            | 无               |

以下启动录音的示例代码：

``` js
let recorder = media.createAudioRecord()
recorder.start({
  uri: "internal://tmp/media_test.mp3",
  sample: 16000,
  layout: 16,
  channel: 1,
  bitrate: 16
})
```

::: info
关于 `internal` URI 协议的更多说明请参考[资源访问](/framework/application/resource.md)文档。
:::

在录制完成后，请调用 [stop()](#stop-1) 方法来结束录制。

### `read`
<decl method><pre>
(options: {
  callback: (buffer: ArrayBuffer) => void,
}): void
</pre></decl>

读取录制的音频数据（每次读取到的数据为从上次读取结束的位置开始到目前为止所有可用的数据）

### `stop` <decl type="(): void" method />

停止录制音频。调用此接口后，可以由其他模块读取 [`start()`](#start) 方法录制的音频文件（由 `uri` 参数指定）。

### `release` <decl type="(): void" method />

释放录制音频资源

### `onstart` <decl type="?: () => void" set />

在录制 start 后的回调事件

### `onstop` <decl type="?: () => void" set />

在录制 stop 后的回调事件

### `onrelease` <decl type="?: () => void" set />

在录制 release 后的回调事件

### `onavailable` <decl type="(data: ArrayBuffer) => void" set />

在录制开始后有新数据产生的回调事件

### `onerror` <decl type="?: () => void" set />

`start`、`stop` 或 `release` 事件发生错误的回调事件，发生错误时，对应的 onstart 等不会被触发

## 示例

### 录音

以下代码演示了录制 3 秒钟音频的最简单示例：
``` js
import media from "@system.media"

async function record() {
  // 创建录音对象
  let record = media.createAudioRecord()
  console.log('start record')
  // 只填写了 uri 参数，其他参数使用默认值
  await record.start({
    uri: 'internal://tmp/test.mp3'
  })
  setTimeout(() => {
    console.log('stop record')
    record.stop() // 延时 3 秒后停止录音
  }, 3000)
}

record()
```

调用 `record()` 函数时会创建一个录音对象，然后开始录音，并在 3 秒钟之后停止录音。录音会被记录到 `internal://tmp/test.mp3` 文件中，并以 MP3 格式编码。

该示例只为 [`AudioPlayer.start()`](#start) 方法传入了 `uri` 参数，`sample`、`layout` 、 `channel` 和 `bitrate` 均使用默认配置。

::: tip
使用模拟器时，可以到应用的数据目录找到录音文件并播放。`internal://tmp/test.mp3` 对应的文件路径是 `.glyphix-work/image/{device}/data/temp/{app-id}/test.mp3` 其中 `{device}` 和 `{app-id}` 是模拟时的设备名称和应用名称。
:::
