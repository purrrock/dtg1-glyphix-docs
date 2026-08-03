# drawer

抽屉组件，默认隐藏，可以通过滑动的方式展示内容。
drawer 是基本的抽屉组件。drawer 支持子组件及布局，可以在drawer内设置4个drawer-navigation组件用于显示上下左右四个位置的抽屉。

[`drawer`](drawer)组件滑动速度跟随手势滑动速度，手势滑动速度越快，组件滑动速度越快。

### 示例

下面的例子演示了drawer的功能

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
