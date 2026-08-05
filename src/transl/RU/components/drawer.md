# drawer

Компонент выдвижной панели (drawer), скрытый по умолчанию, содержимое которого можно отобразить с помощью свайпа.
drawer — это базовый компонент выдвижной панели. drawer поддерживает дочерние компоненты и верстку, внутри drawer можно настроить 4 компонента `drawer-navigation` для отображения панелей с четырех сторон: сверху, снизу, слева и справа.

Скорость прокрутки компонента [`drawer`](drawer) зависит от скорости движения жеста: чем быстрее движение жеста, тем выше скорость прокрутки компонента.

### Пример

В следующем примере продемонстрирована работа компонента drawer.

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