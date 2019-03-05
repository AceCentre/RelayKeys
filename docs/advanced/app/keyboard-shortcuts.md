# Keyboard Shortcuts

Directus has Mousetrap available to add and manage keyboard shortcuts. Mousetrap is available under `this.$helpers.mousetrap`.

## Adding a shortcut

See [the Mousetrap documentation](https://craig.is/killing/mice) for a more detailed explanation of all available options.

In general, you'd add shortcuts as follows:

```vue
<script>
export default {
  name: "my-component",
  mounted() {
    this.$helpers.mousetrap.bind("mod+a", () => this.selectAll());
  },
  beforeDestroy() {
    this.$helpers.mousetrap.unbind("mod+a");
  },
  methods: {
    selectAll() {}
  }
}
</script>
```

::: warning
Make sure to `unbind` the listener when your component is about to be destroyed. Otherwise you'll run into conflicts and other bugs when the system is trying to execute your callbacks.
:::
