# Audio player manager

## Import module

``` ts
import audiokit from '@system.audiokit'
```

## Interface definition

### `getPlayers` <decl type="(): AudioPlayer" method />

Query the list of audio player [`AudioPlayer`](#AudioPlayer) objects available in the system.

### `getActivePlayer` <decl type="(): AudioPlayer" method />

Query the active audio player [`AudioPlayer`](#AudioPlayer) object in the system.

### `subscribe` <decl type="(callback: (PlayerEvent) => void): number" method/>

Listen for changes in the audio player on the system. The parameter `PlayerEvent` of `callback` is [notification event](#PlayerEvent). The ID returned by this method can be used to unsubscribe using the [`unsubscribe()`](#unsubscribe) method.

Type signature of `PlayerEvent`:

```ts
type PlayerEvent = {
  notify: string; // Change event type
  player: string; // Change player name
}
```

Change event type

- `active`: The currently active player in the system has changed
- `append`: The player is added to the system
- `remove`: The player has been removed from the system

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancel player change monitoring. `subscribeID` is the ID value returned by the [`subscribe()`](#subscribe) method.

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

- The `AudioPlayer` object (hereinafter referred to as: `audiokit.Player`) and the `AudioPlayer` object (hereinafter referred to as: `media.Player`) created in the `system.media` module are different js objects, but they manage the same player. At the same time, the `audiokit.Player` object has more functions than the `media.Player` object, such as: `next()`, `previous()` and other methods. Users can use Operations such as `play()` performed by the `audiokit.Player` object will also be notified to the listener of the `media.Player` object.

### `src` <decl type="string" set get />

Set or read the url that needs to play audio. Supports [local resource path](/framework/application/resource.md#uri-and path) and network resource path using http and https protocols (for example: `https://www.rt-thread.com/service/test/001.mp3`). Here's a simple example of setting src and then starting playback:

```ts
import audiokit from '@system.audiokit'
//Query the active audio players in the system
let player = audiokit.getActivePlayer()
if (player != null) {
  //First stop the currently playing audio
  player.stop()
  //Set the audio url to be played
  player.src = 'https://www.rt-thread.com/service/test/001.mp3'
  // Start playing audio
  player.play()
}
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

Read the current playback status

- `play`: playing status
- `pause`: Pause playback state
- `stop`: Stop playing status
- `ended`: playback end status
- `error`: playback error status

### `duration` <decl type="number" get />

Total audio duration, unit: seconds

### `position` <decl type="number" set get />

The time position of the current audio playback, unit: seconds

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
import audiokit from '@system.audiokit'
//Query the active audio players in the system
let player = audiokit.getActivePlayer()
if (player != null) {
  //First stop the currently playing audio
  player.stop()
  //Set the audio url to be played
  player.src = 'https://www.rt-thread.com/service/test/001.mp3'
  //Set onplay event
  player.onplay = () => { console.dir("Start playing") }
  //Set onerror event
  player.onerror = () => { console.dir("Playback error") }
  // Start playing audio
  player.play()
}
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
import audiokit from '@system.audiokit'
//Query the active audio players in the system
let player = audiokit.getActivePlayer()
if (player != null) {
  // Get the audio focus of the media music type
  player.requestFocus({ volumeType: 'media', acquireType: 'gain' });
}
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
