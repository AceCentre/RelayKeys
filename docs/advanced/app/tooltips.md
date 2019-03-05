# Tooltips

![Tooltip example 1](/img/tooltips/tooltip-1.png)

Directus uses the [`v-tooltip`](https://github.com/Akryum/v-tooltip) library to provide helpful information to users on hover. You can easily add tooltips to any element by adding the `v-tooltip` directive:

```vue
<p v-tooltip="€1">$1.17</p>
```

## Inverse colors

When rendering a tooltip on a dark background, you can render the tooltip with the `inverted` class added. This will render the tooltip with a light-gray background and dark text to maintain contrast and visibility:

```vue
<button v-tooltip="{ classes: ['inverted'], content: 'Click to save!' }">Save</button>
```

## Advanced Configuration

Please checkout the `v-tooltip` [docs](https://github.com/Akryum/v-tooltip) for more advanced usage instructions.
