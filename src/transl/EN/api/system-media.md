# Multimedia

## Import Module

``` ts
import media from '@system.media'
```

## Interface Definitions

### `createAudioPlayer` <decl type="(): AudioPlayer" method />

Creates an [`AudioPlayer`](#audioplayer-object) object.

### `createAudioRecord` <decl type="(): AudioRecorder" method />

Creates an [`AudioRecorder`](#audiorecorder-object) object.

Developers need to declare the access permission for `watch.permission.RECORD` in the [`manifest.json`](/framework/application/manifest.md#permissions) file.

### `setVolume` <decl type="(volume: number): void" method />

Sets the system media volume. The `volume` parameter is a value between $[0.0, 1.0]$. This property is used to control the system media volume, and its specific functionality depends on the platform implementation. Adjusting the volume should preferably use the `volume` property of the `AudioPlayer` object.

### `getVolume` <decl type="(): number" method />

Gets the system media volume. The result is a value between $[0.0, 1.0]$. This property is used to get the system media volume, and its specific functionality depends on the platform implementation. Getting the volume should preferably use the `volume` property of the `AudioPlayer` object.

## `AudioPlayer` Object

::: details Type Signature
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

Sets or reads the URL of the audio to be played. Supports [local resource paths](/framework/application/resource.md#uri-and-paths) and network resource paths using http and https protocols (e.g., `https://www.rt-thread.com/service/test/001.mp3`). Below is a simple example of setting the src and starting playback:

```ts
import media from '@system.media'
// Create an audio player
let player = media.createAudioPlayer()
// Set the audio URL to be played
player.src = 'https://www.rt-thread.com/service/test/001.mp3'
// Start playing audio
player.play()
```

### `name` <decl type="string" set get />

The name of the player object. If not set, it defaults to the name of the application that created the player. Note that the name of the player object is not globally unique, and you cannot use the name to identify a player object.

### `icon` <decl type="string" set get />

The icon URL of the player object. Supports [local resource paths](/framework/application/resource.md#uri-and-paths).

### `mode` <decl type="string" set get />

Playback mode. The functionality corresponding to this property should be implemented by the player application. The player object does not handle it by default and only provides this property.

- `sequential`: Sequential playback  
- `random`: Shuffle playback  
- `singleloop`: Single track loop  
- `listloop`: List loop  

### `status` <decl type="string" get />

Reads the current player status.

- `play`: Playing status  
- `pause`: Paused playback status  
- `stop`: Stopped playback status 
- `ended`: Playback ended status  
- `error`: Playback error status  

### `duration` <decl type="number" get />

Total duration of the audio, in seconds.

### `position` <decl type="number" set get />

Current audio playback time position, in seconds.

### `openSystemNotification` <decl type="bool" set get />

Whether to enable system notifications. Disabled by default. Once enabled, this player object can be queried by the [Audio Player Manager](/framework/application/system-audioPlayerManager.md#audio-player-manager).

### `songAttribute` <decl type="songAttribute" set get />

Song attribute object.

::: details Type Signature
```ts
type songAttribute = {
  title: string; // Name of the song
  artist: string; // Name of the performer, can be an individual or a band
  album: string; // Name of the album the song belongs to
  year: string; // Release year of the song
  genre: string; // Genre of the song, e.g., pop, rock, classical, etc.
  track: string; // Current song number in the album, e.g., "1/12" means track 1 of 12
  coverArt: string; // URL of the song cover image
  lyrics: string; // URL of the lyrics text
  comments: string; // Additional information, such as copyright notes
}
```
:::

Like the AudioPlayer object, the songAttribute object is a Proxy object, meaning it cannot be serialized or deserialized using JSON, nor can it be referenced within a reactive framework. Below is a simple usage example:

```ts
// Set the song title
this.player.songAttribute.title = "Unknown"
// Set the song artist
this.player.songAttribute.artist = "Unknown"
// View the song title
console.dir(this.player.songAttribute.title)
```

### `volume` <decl type="number" set get />

Current volume of the player, range: [0.0, 1.0].

### `nextAvailable` <decl type="bool" set get />

Sets or queries whether switching to the next track is available.

### `prevAvailable` <decl type="bool" set get />

Sets or queries whether switching to the previous track is available.

### `play` <decl type="(): void" method />

Starts playing the audio specified in the src property.

- If the src property is not set before calling this method, playback will fail and trigger the onerror event;
- This method is a synchronous interface. After executing this interface, you need to wait for the onplay event or onerror event to determine whether the playback succeeded or failed. Any other operations performed before the event is triggered will be ignored;  

Below is a simple example of calling the play() interface:

```ts
import media from '@system.media'
// Create an audio player
let player = media.createAudioPlayer()
// Set the audio URL to be played
player.src = 'https://www.rt-thread.com/service/test/001.mp3'
// Set the onplay event
player.onplay = () => { console.dir("Started playing") }
// Set the onerror event
player.onerror = () => { console.dir("Playback error") }
// Start playing audio
player.play()
```

### `pause` <decl type="(): void" method />

Pauses the playback of the current audio.  

- This method is a synchronous interface. After executing this interface, you need to wait for the onpause event or onerror event to determine whether the pause succeeded or failed. Any other operations performed before the event is triggered will be ignored;  

### `stop` <decl type="(): void" method />

Stops audio playback. You can resume playback using play.  

- This method is a synchronous interface. After executing this interface, you need to wait for the onstop event or onerror event to determine whether stopping succeeded or failed. Any other operations performed before the event is triggered will be ignored;  

### `release` <decl type="(): void" method />

Releases audio resources.  

- Executing this interface will stop the current audio playback. You need to wait for the onstop event or onerror event to determine whether stopping succeeded or failed. Any other operations performed before the event is triggered will be ignored;   

### `next` <decl type="(): void" method />

Notifies the player application to play the next track. Executing this interface triggers the onnext event to notify the player application listening to this event, and the player application executes the song switching logic.

### `previous` <decl type="(): void" method />

Notifies the player application to play the previous track. Executing this interface triggers the onprevious event to notify the player application listening to this event, and the player application executes the song switching logic.

### `requestFocus` <decl type="({acquireType: string, volumeType: string}): void" method />

Requests audio focus. Executing this interface notifies the underlying system to request or release audio focus, and the underlying system controls the switching and interruption logic for different types of audio.

The `acquireType` parameter indicates the request type:
- `gain`: Request audio focus
- `loss`: Release audio focus

The `volumeType` parameter indicates the audio type:
- `system`: System prompts
- `media`: Media music
- `tts`: Voice broadcast

The following example demonstrates how the `requestFocus` function requests audio focus:
``` ts
import media from '@system.media'
// Create an audio player
let player = media.createAudioPlayer()
// Acquire audio focus for media music type
player.requestFocus({ volumeType: 'media', acquireType: 'gain' });
```

### `releaseFocus` <decl type="(): void" method />

Releases audio focus. Executing this interface notifies the underlying system to release audio focus, and the underlying system controls the switching and interruption logic for different types of audio.

### `onplay` <decl type="?: () => void" set />

Callback event when audio play succeeds.

### `onpause` <decl type="?: () => void" set />

Callback event when audio pause succeeds.

### `onstop` <decl type="?: () => void" set />

Callback event when audio stop succeeds.

### `onended` <decl type="?: () => void" set />

Callback event when audio playback ends.

### `onerror` <decl type="?: () => void" set />

Callback event when errors occur during interfaces such as `play`, `pause`, `stop`, `position`. When an error occurs, corresponding events like onplay will not be triggered.

### `ontimeupdate` <decl type="?: () => void" set />

Callback event triggered when the position property is updated. This event is only triggered when the application is in the foreground and stops dispatching when the application is in the background.

### `oninterrupt` <decl type="?: (action: {interruptHint: number}) => void" set />

Callback function when an audio interruption event occurs, notifying temporary or permanent interruption when the current audio is preempted by audio of the same or another type.

The `interruptHint` in the `action` parameter indicates the type of interruption event:
- `1`: Brief interruption (can recover automatically, e.g., music being interrupted)
- `2`: Complete interruption (cannot recover automatically, e.g., NetEase Cloud Music interrupted by Ximalaya)

The following example demonstrates how to register the `oninterrupt` callback function, which is called when the event occurs:
``` js
player.oninterrupt = (action) => {
  console.log(action.interruptHint)
}
```

### `onnext` <decl type="?: () => void" set />

Callback event when the next track needs to be played.

### `onprevious` <decl type="?: () => void" set />

Callback event when the previous track needs to be played.

### `onrequestplay` <decl type="?: () => void" set />

Callback event triggered when the underlying system needs to start playback, notifying the JS application to execute the start playback logic.

### `onrequestpause` <decl type="?: () => void" set />

Callback event triggered when the underlying system needs to pause playback, notifying the JS application to execute the pause playback logic.

### `onrequeststop` <decl type="?: () => void" set />

Callback event triggered when the underlying system needs to stop playback, notifying the JS application to execute the stop playback logic.

### `onsongattribute` <decl type="?: () => void" set />

Callback event when the song attribute object changes.

### `onposition` <decl type="?: () => void" set />

Callback event when setting the current audio playback position via `position` succeeds.

### `onrequestfocus` <decl type="?: () => void" set />

Callback event when requesting audio focus succeeds.

### `onreleasefocus` <decl type="?: () => void" set />

Callback event when releasing audio focus succeeds.

### `onmodechanged` <decl type="?: () => void" set />

Callback event when the playback mode changes.

### `onvolumechange` <decl type="?: () => void" set />

Callback event when the player volume changes.


## `AudioRecorder` Object

::: details Type Signature
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

Starts recording audio. The functions of the fields in the `options` parameter are:
- `uri`: The URI of the recording file to be stored. Only the `internal` protocol is supported, and directories will be created automatically;
- `sample`: Audio sampling rate in $\rm Hz$, defaults to $8000$;
- `layout`: Audio data bit depth, defaults to $16$;
- `channel`: Number of audio channels, defaults to $1$;
- `bitrate`: Audio bitrate in $\rm kbps$, defaults to $16$. Higher bitrates yield better sound quality but larger file sizes.
- `codec`: Audio encoding format as a string. If left blank, a suitable encoding is automatically matched based on the `format` parameter;
- `format`: Audio container/封装 format as a string. If left blank, a suitable container is automatically matched based on the suffix of the `uri` parameter;

  The support relationships for common recording formats, encoding formats, and container formats are as follows (an empty value in the table indicates that the corresponding parameter can be left blank):

  | Common Recording Formats | codec (Encoding Format) | format (Container Format) |
  | ------------------------ | ----------------------- | ------------------------- |
  | pcm                      | None                    | None                      |
  | mp3                      | mp3                     | None                      |
  | opus                     | opus                    | None                      |
  | opus-ogg                 | opus                    | ogg                       |
  | silk                     | silk                    | None                      |

Here is sample code to start recording:

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
For more descriptions regarding the `internal` URI protocol, please refer to the [Resource Access](/framework/application/resource.md) documentation.
:::

After recording is complete, please call the [stop()](#stop-1) method to end the recording.

### `read`
<decl method><pre>
(options: {
  callback: (buffer: ArrayBuffer) => void,
}): void
</pre></decl>

Reads the recorded audio data (each read retrieves all available data from the end of the previous read up to the current moment).

### `stop` <decl type="(): void" method />

Stops recording audio. After calling this interface, other modules can read the audio file recorded by the [`start()`](#start) method (specified by the `uri` parameter).

### `release` <decl type="(): void" method />

Releases audio recording resources.

### `onstart` <decl type="?: () => void" set />

Callback event after recording starts.

### `onstop` <decl type="?: () => void" set />

Callback event after recording stops.

### `onrelease` <decl type="?: () => void" set />

Callback event after recording is released.

### `onavailable` <decl type="(data: ArrayBuffer) => void" set />

Callback event when new data is generated after recording starts.

### `onerror` <decl type="?: () => void" set />

Callback event when errors occur during `start`, `stop`, or `release` events. When an error occurs, corresponding events like onstart will not be triggered.

## Examples

### Recording

The following code demonstrates a simple example of recording audio for 3 seconds:
``` js
import media from "@system.media"

async function record() {
  // Create a recording object
  let record = media.createAudioRecord()
  console.log('start record')
  // Only the uri parameter is provided; other parameters use default values
  await record.start({
    uri: 'internal://tmp/test.mp3'
  })
  setTimeout(() => {
    console.log('stop record')
    record.stop() // Stop recording after a 3-second delay
  }, 3000)
}

record()
```

When the `record()` function is called, it creates a recording object, starts recording, and stops recording after 3 seconds. The recording will be saved to the `internal://tmp/test.mp3` file and encoded in MP3 format.

This example only passes the `uri` parameter to the [`AudioPlayer.start()`](#start) method; `sample`, `layout`, `channel`, and `bitrate` all use their default configurations.

::: tip
When using the simulator, you can find and play the recording file in the application's data directory. The file path corresponding to `internal://tmp/test.mp3` is `.glyphix-work/image/{device}/data/temp/{app-id}/test.mp3`, where `{device}` and `{app-id}` are the device name and application name during simulation.
:::