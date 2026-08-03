# drawer

The drawer component is hidden by default and can display content through sliding gestures.
The drawer is a basic drawer component. It supports sub-components and layouts, and you can place up to four `drawer-navigation` components inside a drawer to display drawers from the top, bottom, left, and right positions.

The sliding speed of the [`drawer`](drawer) component follows the gesture sliding speed: the faster the gesture, the faster the component slides.

### Example

The following example demonstrates the functionality of the drawer.

<glyphix id="components-drawer" height="360" width="360" >

``` html
 <drawer class="drop-down">
      <drawer-navigation direction="down" class="drop-down1">
        <p>dawn panel</p>
      </drawer-navigation>
      <drawer-navigation direction="up" class="drop-down1">
        <p>up panel</p>
      </drawer-navigation>
       <drawer-navigation direction="left" class="drop-down1">
        <p>left panel</p>
      </drawer-navigation>
       <drawer-navigation direction="right" class="drop-down1">
        <p>right panel</p>
      </drawer-navigation>
</drawer>
```
``` css
.drop-down {
    background-color: pink;
  }
.drop-down1 {
    background-color: blue;
  }
p {
  background-color: lightgreen;
  text-align: center;
  margin: 10px;
}
```
</glyphix>