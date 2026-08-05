# Inter-Component Communication

Communication between components is achieved through component properties and event bindings. For example:
``` html
<scroll scroll-snap="center" on:scroll="scrolled($event)" />
```
This passes the `scroll-snap` attribute parameter to the `scroll` component instance to center-align the element, and listens for changes to the `scroll` property.

## Properties and Parameters

Parameters can be passed to child components via the **attribute** fields of component nodes. For example:
``` html
<p text="A message"></p>
```
This passes an attribute named `text` with the value `"A message"` to a `p` component instance. Multiple attributes can be passed according to XML/HTML syntax. Computed values can be passed to component properties using [interpolation expressions](template#interpolation-expressions).

## Event Handling

[Native components](native-component) encapsulate many UI input events, such as responses to touch gestures and UI change events. All of these events can be listened to using the [`on` directive](../commands/on.md).

## Triggering Events

For custom components, you can use the component object's [`$emit(name, value)`](/framework/component/component-apis.md#emit) method to trigger an event:
``` html
<panel on:some-event="console.log(`the event ${$event} was emited!`)">
```

``` js
// in panel.ux
export default {
  emitEvent() {
    this.$emit('someEvent', 'hello')
  }
}
```

The `$emit` method takes two parameters:
- `name`: The name of the property to send the event. It must use lower camelCase (the corresponding template attribute can be kebab-case or lower camelCase).
- `value`: An optional parameter, which is the value of the event property and will be used as the value of the `$event` variable in the `on` directive.

If the view-model of the component object has a property named `name`, the `$emit` method will not modify the property value to `value`.