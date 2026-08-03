# scroll-bar


Scroll bar component. This component can display a scroll bar when there is a lot of scrolling content, and the user can control the scrolling of the content through the scroll bar.


## property


### `value` <decl type="number" set get listen />


The current value of the scroll bar, which is a value between `min` and `max`. The default value is $0$.


### `min` <decl type="number" set />


The minimum value of the scroll bar, which should be no greater than `max`. The default value is $0$.


### `max` <decl type="number" set />


The maximum value of the scroll bar. This value should be no less than `min`. The default value is $100$.


### `pagestep` <decl type="number" set />


The scroll step size of the scroll bar, that is, the distance of each scroll. The default value is $10$.