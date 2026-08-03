# drawer


The drawer component is hidden by default and can display content by sliding.
drawer is the basic drawer component. Drawer supports sub-components and layouts. You can set up 4 drawer-navigation components in the drawer to display drawers in four positions: top, bottom, left and right.


[`drawer`](drawer) The sliding speed of the component follows the sliding speed of the gesture. The faster the sliding speed of the gesture, the faster the sliding speed of the component.


### Example


The following example demonstrates the functionality of the drawer


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
