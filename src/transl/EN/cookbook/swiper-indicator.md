# Swiper page indicator


<Glyphix id="cookbook-swiper-indicator" height="466" width="466" designWidth="466" title="Swiper 指示器">


``` html
<stack>
  <swiper ::index="index">
    <p for="i in panels">Panel {{i + 1}}</p>
  </swiper>
  <div class="indicator">
    <image for="x in indicator" :src="x" />
  </div>
</stack>
```


``` js
export default {
  data: {
    panels: 5,
    index: 2
  },
  computed: {
    indicator() {
      let result = []
      for (let i = 0; i < this.panels; i++) {
        let suffix = i == this.index ? '1' : '0'
        result.push(`/assets/images/ind-${suffix}.png`)
      }
      return result
    }
  }
}
```


``` css
swiper > p {
  background-color: #888;
  margin: 32px;
  border-radius: 32px;
  text-align: center;
}

.indicator {
  display: flex;
  justify-content: center;
  align-items: flex-end;
}

.indicator > * {
  margin: 0 4px 56px 4px;
}
```


</Glyphix>
