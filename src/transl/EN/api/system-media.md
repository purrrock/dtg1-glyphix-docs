# multimedia

## Import module

``` ts
import media from '@system.media'
```

## Interface definition

### `createAudioPlayer` <decl type="(): AudioPlayer" method />

Create an [`AudioPlayer`](#audioplayer-object) object.

### `createAudioRecord` <decl type="(): AudioRecorder" method />

Create an [`AudioRecorder`](#audiorecorder-object) object.

Developers need to declare the application's access permissions to `watch.permission.RECORD` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

### `setVolume` <decl type="(volume: number): void" method />

Set the system media volume. The parameter `volume` is a volume value between $[0.0, 1.0]$. This property is used to control the system media volume. The specific function depends on the platform implementation. To adjust the volume, the `volume` property of the `AudioPlayer` object should be used first.

### `getVolume` <decl type="(): number" method />

Get the system media volume, the result is a volume value between $[0.0, 1.0]$. This attribute is used to obtain the system media volume. The specific function depends on the platform implementation. To obtain the volume, the `volume` attribute of the `AudioPlayer` object should be used first.

## `AudioPlayer` object

::: details type signature
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

Set or read the url that needs to play audio. Supports [local resource path](/framework/application/resource.md#uri-and path) and network resource path using http and https protocols (for example: `https://www.rt-thread.com/service/test/001.mp3`). Here's a simple example of setting src and then starting playback:

```ts
import media from '@system.media'
//Create audio player
let player = media.createAudioPlayer()
//Set the audio url to be played
player.src = 'https://www.rt-thread.com/service/test/001.mp3'
// Start playing audio
player.play()
```

### `name` <decl type="string" set get />

The name of the player object. If not set, it defaults to the name of the application that created the player. It should be noted that the name of the player object is not globally unique, and the name cannot be used to identify the player object.

### `icon` <decl type="string" set get />

The player object's icon url. Support [local resource path](/framework/application/resource.md#uri-and path)

### `mode` <decl type="string" set get />

playback mode. The function corresponding to this attribute should be implemented by the player application. The player object does not process it by default and only provides this attribute.

- `sequential`: play sequentially
- `random`: play randomly
- `singleloop`: single loop
- `listloop`: list loop

### `status` <decl type="string" get />

Read the current player status

- `play`: playing status
- `pause`: Pause playback state
- `stop`: Stop playing status
- `ended`: playback end status
- `error`: playback error status

### `duration` <decl type="number" get />

Total audio duration, unit: seconds

### `position` <decl type="number" set get />

The time position of the current audio playback, unit: seconds

### `openSystemNotification` <decl type="bool" set get />

Whether to turn on system notifications, not turned on by default. After it is turned on, this player object can be queried by [Audio Player Manager](/framework/application/system-audioPlayerManager.md#Audio Player Manager).

### `songAttribute` <decl type="songAttribute" set get />

Song property object

::: details type signature
```ts
type songAttribute = {
  title: string; // The name of the song
  artist: string; //The name of the performer, which can be an individual or a band
  album: string; // The name of the album to which the song belongs
  year: string; // The year the song was released
  genre: string; // The type of song, such as pop, rock, classical, etc.
  track: string; // The number of the current song in the album, for example: "1/12" means the 1st song, a total of 12 songs
  coverArt: string; // URL of the song cover image
  lyrics: string; // URL of lyrics text
  comments: string; // Additional information, such as copyright remarks, etc.
}
```
:::

The songAttribute object is a Proxy object like the AudioPlayer object. It cannot be serialized and deserialized using JSON, and cannot be referenced in the responsive framework. Here's a simple usage example:

```ts
//Set the name of the song
this.player.songAttribute.title = "Unknown"
//Set the singer of the song
this.player.songAttribute.artist = "Unknown"
// Check the name of the song
console.dir(this.player.songAttribute.title)
```

### `volume` <decl type="number" set get />

The volume of the current player, range: [0.0, 1.0]

### `nextAvailable` <decl type="bool" set get />

Set or query whether the next song can be switched

### `prevAvailable` <decl type="bool" set get />

Set or query whether the previous song can be switched

### `play` <decl type="(): void" method />

Start playing the audio specified in the src attribute

- If the src attribute is not set before calling this method, playback will fail and the onerror event will be triggered;
- This method is a synchronous interface. After executing this interface, you need to wait for the onplay event or onerror event to determine whether the playback is successful or failed. Before the event is triggered, other operations performed will be ignored;

The following is a simple example of calling the play() interface:

```ts
import media from '@system.media'
//Create audio player
let player = media.createAudioPlayer()
//Set the audio url to be played
player.src = 'https://www.rt-thread.com/service/test/001.mp3'
//Set onplay event
player.onplay = () => { console.dir("Start playing") }
//Set onerror event
player.onerror = () => { console.dir("Playback error") }
// Start playing audio
player.play()
```

### `pause` <decl type="(): void" method />

Pause the current audio

- This method is a synchronous interface. After executing this interface, you need to wait for the onpause event or onerror event to determine whether the pause is successful or failed. Before the event is triggered, other operations performed will be ignored;

### `stop` <decl type="(): void" method />

Stop audio playback and replay the audio via play

- This method is a synchronous interface. After executing this interface, you need to wait for the onstop event or onerror event to determine whether the stop is successful or failed. Before the event is triggered, other operations performed will be ignored;

### `release` <decl type="(): void" method />

Release audio resources

- Executing this interface will stop playing the current audio. You need to wait for the onstop event or onerror event to determine whether the stop is successful or failed. Before the event is triggered, other operations performed will be ignored;

### `next` <decl type="(): void" method />

Notify the player application to play the next song. After executing this interface, the onnext event will be triggered to notify the player application that listens to this event, and the player application will execute the logic of song switching.

### `previous` <decl type="(): void" method />

Notify the player application to play the next song. After executing this interface, the onprevious event will be triggered to notify the player application that listens to this event, and the player application will execute the song switching logic.

### `requestFocus` <decl type="({acquireType: string，volumeType: string}): void" method />

Request audio focus. After executing this interface, the underlying layer will be notified to request or release the audio focus, and the underlying layer will control the switching and interruption logic of different types of audio.

The `acquireType` parameter indicates the request type:
- `gain`: Request audio focus
- `loss`: Release audio focus

The `volumeType` parameter indicates the audio type:
- `system`: system prompt
- `media`: media music
- `tts`: voice broadcast

The following example demonstrates how the `requestFocus` function requests audio focus:
``` ts
import media from '@system.media'
//Create audio player
let player = media.createAudioPlayer()
// Get the audio focus of the media music type
player.requestFocus({ volumeType: 'media', acquireType: 'gain' });
```

### `releaseFocus` <decl type="(): void" method />

Release audio focus. After executing this interface, the bottom layer will be notified to release the audio focus, and the bottom layer will control the switching and interruption logic of different types of audio.

### `onplay` <decl type="?: () => void" set />

Callback event after audio play is successful

### `onpause` <decl type="?: () => void" set />

Callback event after audio pause is successful

### `onstop` <decl type="?: () => void" set />

Callback event after audio stop is successful

### `onended` <decl type="?: () => void" set />

Callback event after audio playback ends

### `onerror` <decl type="?: () => void" set />

Execute callback events for interface errors such as `play` `pause` `stop` `position` and other interfaces. When an error occurs, the corresponding onplay and other events will not be triggered.

### `ontimeupdate` <decl type="?: () => void" set />

A callback event that will be triggered when the position property is updated. This event will only be triggered when the application is in the foreground, and will stop dispatching when the application is in the background.

### `oninterrupt` <decl type="?: (action: {interruptHint: number}) => void" set />

The callback function when an audio interruption event occurs. When the current audio is snatched by audio of the same audio type or other audio types, it will be notified that it is temporarily interrupted or completely interrupted.

The `interruptHint` of the `action` parameter indicates the type of interrupt event:
- `1`: brief interruption (can be automatically restored, such as: music is interrupted)
- `2`: Completely interrupted (cannot be automatically restored, such as: NetEase Cloud was interrupted by Himalaya)

The following example demonstrates how to register an `oninterrupt` callback function, which is called when an event occurs:
``` js
player.oninterrupt = (action) => {
  console.log(action.interruptHint)
}
```

### `onnext` <decl type="?: () => void" set />

Callback event when the next song needs to be played

### `onprevious` <decl type="?: () => void" set />

Callback event when the previous song needs to be played

### `onrequestplay` <decl type="?: () => void" set />

When the bottom layer needs to start playback, the callback event is triggered to notify the js application, and the js application executes the logic of starting playback.

### `onrequestpause` <decl type="?: () => void" set />

When the bottom layer needs to pause playback, the callback event is triggered to notify the js application, and the js application executes the logic of pausing playback.

### `onrequeststop` <decl type="?: () => void" set />

When the bottom layer needs to stop playing, the callback event is triggered to notify the js application, and the js application executes the logic of stopping the playback.

### `onsongattribute` <decl type="?: () => void" set />

Callback event when the song attribute object changes

### `onposition` <decl type="?: () => void" set />

Execute `position` to set the time and position of the current audio playback. The callback event is successful.

### `onrequestfocus` <decl type="?: () => void" set />

Callback event when requesting audio focus successfully

### `onreleasefocus` <decl type="?: () => void" set />

Callback event when audio focus is released successfully

### `onmodechanged` <decl type="?: () => void" set />

Callback event when playback mode changes

### `onvolumechange` <decl type="?: () => void" set />

Callback event when player volume changes


## `AudioRecorder` object

::: details type signature
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

Start recording audio. The functions of each field of the `options` parameter are:
- `uri`: URI of the recording file that needs to be stored, only supports the `internal` protocol, and the directory will be automatically created;
- `sample`: audio sampling rate, unit is $\rm Hz$, default is $8000$;
- `layout`: audio data bit depth, default is $16$;
- `channel`: number of audio channels, default is $1$;
- `bitrate`: Audio bitrate, the unit is $\rm kbps$, the default is $16$, the higher the bitrate, the better the sound quality but the larger the file.
- `codec`: audio encoding format, string type, if not filled in, a suitable code will be automatically matched according to the `format` parameter;
- `format`: audio encapsulation format, string type, if not filled in, a suitable encapsulation will be automatically matched based on the suffix name of the `uri` parameter;

The support relationships for commonly used recording formats, encoding formats and encapsulation formats are as follows (None in the table means that the corresponding parameters do not need to be filled in):

| Commonly used recording formats | codec (encoding format) | format (encapsulation format) |
  | -------------- | --------------- | ------------- |
  | pcm | None | None |
  | mp3 | mp3 | none |
  | opus | opus | none |
  | opus-ogg | opus | ogg |
  | silk | silk | none |

The following example code starts recording:

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
For more information on the `internal` URI protocol, please refer to the [Resource Access](/framework/application/resource.md) document.
:::

After the recording is completed, call the [stop()](#stop-1) method to end the recording.

### `read`
<decl method><pre>
(options: {
  callback: (buffer: ArrayBuffer) => void,
}): void
</pre></decl>

Read the recorded audio data (the data read each time is all available data so far from the end of the last read)

### `stop` <decl type="(): void" method />

Stop recording audio. After calling this interface, the audio file recorded by the [`start()`](#start) method (specified by the `uri` parameter) can be read by other modules.

### `release` <decl type="(): void" method />

Release recording audio resources

### `onstart` <decl type="?: () => void" set />

Callback event after recording start

### `onstop` <decl type="?: () => void" set />

Callback event after recording stop

### `onrelease` <decl type="?: () => void" set />

Callback event after recording release

### `onavailable` <decl type="(data: ArrayBuffer) => void" set />

Callback event generated when new data is generated after recording starts

### `onerror` <decl type="?: () => void" set />

The callback event when an error occurs in the `start`, `stop` or `release` event. When an error occurs, the corresponding onstart, etc. will not be triggered.

## Example

### Recording

The following code demonstrates the simplest example of recording 3 seconds of audio:
``` js
import media from "@system.media"

async function record() {
  //Create recording object
  let record = media.createAudioRecord()
  console.log('start record')
  //Only fill in the uri parameter, other parameters use default values
  await record.start({
    uri: 'internal://tmp/test.mp3'
  })
  setTimeout(() => {
    console.log('stop record')
    record.stop() // Stop recording after a delay of 3 seconds
  }, 3000)
}

record()
```

When the `record()` function is called, a recording object is created, then starts recording, and stops recording after 3 seconds. The recording will be recorded to the file `internal://tmp/test.mp3` and encoded in MP3 format.

This example only passes the `uri` parameter to the [`AudioPlayer.start()`](#start) method, and `sample`, `layout`, `channel` and `bitrate` all use the default configuration.

::: tip
When using the simulator, you can find the recording file in the application's data directory and play it. The corresponding file path of `internal://tmp/test.mp3` is `.glyphix-work/image/{device}/data/temp/{app-id}/test.mp3` where `{device}` and `{app-id}` are the device name and application name during simulation.
:::
