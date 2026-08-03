# Inter-component Communication

Communication between components is achieved through component parameters and event binding. For example:
``` html
<scroll scroll-snap="center" on:scroll="scrolled($event)" />
```
This passes the `scroll-snap` attribute parameter to the `scroll` component instance to center-align the element, and listens for changes to the `scroll` property.

## Attribute Parameters

You can pass parameters to child components through the **attribute** fields of component nodes. For example:
``` html
<p text="A message"></p>
```
This passes an attribute named `text` with the value `"A message"` to a `p` component instance. Multiple attributes can be passed according to XML/HTML syntax. Evaluated values can be passed to component attributes using [Interpolation Expressions](template#插值表达式).

## Event Response

[Native components](native-component) encapsulate many UI input events, such as responses to touch gestures and UI change events. All these events can be listened to via the [`on` command](../commands/on.md).

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
- `name`: The name of the attribute to send the event, which must use lower camelCase (the corresponding template attribute can be in kebab-case or lower camelCase).
- `value`: Optional parameter, the value of the event attribute, which will be used as the value of the `$event` variable in the `on` command.

If the view-model of the component object has a property named `name`, the `$emit` method will not modify the property value to `value`.