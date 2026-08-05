# Audio Player Manager

## Import Module

``` ts
import audiokit from '@system.audiokit'
```

## Interface Definitions

### `getPlayers` <decl type="(): AudioPlayer" method />

Queries the list of available audio player [`AudioPlayer`](#AudioPlayer) objects in the system.

### `getActivePlayer` <decl type="(): AudioPlayer" method />

Queries the active audio player [`AudioPlayer`](#AudioPlayer) object in the system.

### `subscribe` <decl type="(callback: (PlayerEvent) => void): number" method/>

Listens for changes to audio players in the system. The `callback` parameter `PlayerEvent` is the [notification event](#PlayerEvent). The ID returned by this method can be used with the [`unsubscribe()`](#unsubscribe) method to remove the listener.

Type signature for `PlayerEvent`:

```ts
type PlayerEvent = {
  notify: string; // Change event type
  player: string; // Name of the changed player
}
```

Change event types:

- `active`: The currently active player in the system has changed  
- `append`: A player has been added to the system
- `remove`: A player has been removed from the system

### `unsubscribe` <decl type="(subscribeID: number): void" method/>

Cancels the player change listener. `subscribeID` is the ID value returned by the [`subscribe()`](#subscribe) method.

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

- The `AudioPlayer` object (hereinafter referred to as `audiokit.Player`) and the `AudioPlayer` object created in the `system.media` module (hereinafter referred to as `media.Player`) are different JS objects, but they manage the same player. Additionally, the `audiokit.Player` object provides some extra functionality compared to the `media.Player` object, such as `next()`, `previous()`, etc. Operations like `play()` executed by users through the `audiokit.Player` object will also notify the listeners of the `media.Player` object.

### `src` <decl type="string" set get />

Sets or gets the URL of the audio to be played. Supports [local resource paths](/framework/application/resource.md#uri-和路径) and network resource paths using HTTP and HTTPS protocols (e.g., `https://www.rt-thread.com/service/test/001.mp3`). Below is a simple example of setting the src and starting playback:

```ts
import audiokit from '@system.audiokit'
// Query the active audio player in the system
let player = audiokit.getActivePlayer()
if (player != null) {
  // First, stop the currently playing audio
  player.stop()
  // Set the audio URL to be played
  player.src = 'https://www.rt-thread.com/service/test/001.mp3'
  // Start playing audio
  player.play()
}
```

### `name` <decl type="string" set get />

The name of the player object. If not set, it defaults to the name of the application that created the player. Note that the player object name is not globally unique, and names cannot be used to uniquely identify player objects.

### `icon` <decl type="string" set get />

The icon URL of the player object. Supports [local resource paths](/framework/application/resource.md#uri-和路径).

### `mode` <decl type="string" set get />

Playback mode. The functionality corresponding to this property should be implemented by the player application; the player object does not process it by default and only provides this property.

- `sequential`: Sequential playback  
- `random`: Random playback  
- `singleloop`: Single track loop  
- `listloop`: List loop  

### `status` <decl type="string" get />

Reads the current playback status.

- `play`: Playing status  
- `pause`: Paused status  
- `stop`: Stopped status 
- `ended`: Playback ended status  
- `error`: Playback error status  

### `duration` <decl type="number" get />

Total audio duration in seconds.

### `position` <decl type="number" set get />

Current audio playback position in seconds.

### `songAttribute` <decl type="songAttribute" set get />

Song attribute object.

::: details Type Signature
```ts
type songAttribute = {
  title: string; // Song title
  artist: string; // Performer's name, can be an individual or a band
  album: string; // Name of the album the song belongs to
  year: string; // Release year of the song
  genre: string; // Genre of the song, such as pop, rock, classical, etc.
  track: string; // Current track number in the album, e.g., "1/12" means track 1 of 12
  coverArt: string; // URL of the song cover image
  lyrics: string; // URL of the lyrics text
  comments: string; // Additional information, such as copyright notes
}
```
:::

Like the AudioPlayer object, the songAttribute object is a Proxy object, meaning it cannot be serialized/deserialized with JSON, nor can it be referenced in a reactive framework. Below is a simple usage example:

```ts
// Set the song title
this.player.songAttribute.title = "Unknown"
// Set the song artist
this.player.songAttribute.artist = "Unknown"
// View the song title
console.dir(this.player.songAttribute.title)
```

### `volume` <decl type="number" set get />

Current player volume, range: [0.0, 1.0].

### `nextAvailable` <decl type="bool" set get />

Sets or queries whether skipping to the next track is available.

### `prevAvailable` <decl type="bool" set get />

Sets or queries whether skipping to the previous track is available.

### `play` <decl type="(): void" method />

Starts playing the audio specified in the src property.

- If the src property is not set before calling this method, playback will fail and trigger the onerror event;
- This method is a synchronous interface. After executing this interface, you need to wait for the onplay event or onerror event to determine whether the playback succeeded or failed. Other operations executed before the event is triggered will be ignored;  

Below is a simple example of calling the `play()` interface:

```ts
import audiokit from '@system.audiokit'
// Query the active audio player in the system
let player = audiokit.getActivePlayer()
if (player != null) {
  // First, stop the currently playing audio
  player.stop()
  // Set the audio URL to be played
  player.src = 'https://www.rt-thread.com/service/test/001.mp3'
  // Set the onplay event
  player.onplay = () => { console.dir("Started playing") }
  // Set the onerror event
  player.onerror = () => { console.dir("Playback error") }
  // Start playing audio
  player.play()
}
```

### `pause` <decl type="(): void" method />

Pauses the currently playing audio.  

- This method is a synchronous interface. After executing this interface, you need to wait for the onpause event or onerror event to determine whether the pause succeeded or failed. Other operations executed before the event is triggered will be ignored;  

### `stop` <decl type="(): void" method />

Stops audio playback. Playback can be resumed using play.  

- This method is a synchronous interface. After executing this interface, you need to wait for the onstop event or onerror event to determine whether the stop succeeded or failed. Other operations executed before the event is triggered will be ignored;  

### `release` <decl type="(): void" method />

Releases audio resources.  

- Executing this interface will stop playing the current audio. You need to wait for the onstop event or onerror event to determine whether the stop succeeded or failed. Other operations executed before the event is triggered will be ignored;   

### `next` <decl type="(): void" method />

Notifies the player application to play the next track. Executing this interface triggers the onnext event to notify the player application listening to this event, and the player application executes the track-switching logic.

### `previous` <decl type="(): void" method />

Notifies the player application to play the previous track. Executing this interface triggers the onprevious event to notify the player application listening to this event, and the player application executes the track-switching logic.

### `requestFocus` <decl type="({acquireType: string，volumeType: string}): void" method />

Requests audio focus. Executing this interface notifies the underlying system to request or release audio focus, and the underlying system controls the switching and interruption logic for different types of audio.

The `acquireType` parameter indicates the request type:
- `gain`: Request audio focus
- `loss`: Release audio focus

The `volumeType` parameter indicates the audio type:
- `system`: System prompts
- `media`: Media music
- `tts`: Text-to-speech voice broadcasts

The following example demonstrates how to request audio focus using the `requestFocus` function:
``` ts
import audiokit from '@system.audiokit'
// Query the active audio player in the system
let player = audiokit.getActivePlayer()
if (player != null) {
  // Acquire audio focus for media music type
  player.requestFocus({ volumeType: 'media', acquireType: 'gain' });
}
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

Callback event when an error occurs while executing interfaces such as `play`, `pause`, `stop`, or `position`. When an error occurs, corresponding events like `onplay` will not be triggered.

### `ontimeupdate` <decl type="?: () => void" set />

Callback event triggered when the `position` property is updated. This event is only triggered when the application is in the foreground and stops dispatching when the application goes to the background.

### `oninterrupt` <decl type="?: (action: {interruptHint: number}) => void" set />

Callback function when an audio interruption event occurs, notifying temporary or permanent interruption when the current audio is preempted by audio of the same or another type.

The `interruptHint` parameter of `action` indicates the type of interruption event:
- `1`: Transient interruption (can recover automatically, e.g., music interrupted by a notification)
- `2`: Permanent interruption (cannot recover automatically, e.g., NetEase Cloud Music interrupted by Himalaya)

The following example demonstrates how to register the `oninterrupt` callback function, which will be called when the event occurs:
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