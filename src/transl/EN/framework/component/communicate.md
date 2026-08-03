# Communication between components


Communication between components is achieved by component parameters and event bindings. For example:
``` html
<scroll scroll-snap="center" on:scroll="scrolled($event)" />
```
The `scroll-snap` attribute parameter is passed to the `scroll` component instance to center-align the element, and changes to the `scroll` attribute will be monitored.


## Property parameters


Parameters can be passed to subcomponents through the attribute field of the component node, for example:
``` html
<p text="A message"></p>
```
A `p` component instance is passed a property named `text` with a value of `"A message"`. Multiple attributes can be passed following XML/HTML syntax. You can pass a calculated value to a component's properties via [interpolation expression](template#插值表达式).


## incident response


[Native components](native-component) encapsulates many UI input events, such as touch gesture responses and UI change events. These events can be monitored through [`on` directive](../commands/on.md).


## trigger event


For custom components, you can use the [`$emit(name, value)`](/framework/component/component-apis.md#emit) method of the component object to trigger an event:
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


The `$emit` method has two parameters:
- `name`: The attribute name that needs to send the event must use camel case naming (the corresponding template attribute is snake naming or camel case naming)
- `value`: Optional parameter, the value of the event attribute, will be used as the value of the `$event` variable of the `on` instruction


If there is a property named `name` in the component object's view-model, the `$emit` method will not modify the property value to `value`.