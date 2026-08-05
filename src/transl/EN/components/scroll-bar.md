# scroll-bar

Scroll bar component. This component displays a scroll bar when there is a large amount of scrollable content, allowing users to control content scrolling through the scroll bar.

## Attributes

### `value` <decl type="number" set get listen />

The current value of the scroll bar, which is a value between `min` and `max`. The default value is $0$.

### `min` <decl type="number" set />

The minimum value of the scroll bar, which should not be greater than `max`. The default value is $0$.

### `max` <decl type="number" set />

The maximum value of the scroll bar, which should not be less than `min`. The default value is $100$.

### `pagestep` <decl type="number" set />

The scroll step size of the scroll bar, which is the distance scrolled per step. The default value is $10$.