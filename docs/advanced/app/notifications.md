# Notifications

At times, you'll need to let the user know that something succeeded or went wrong. You could choose to [use an `alert` component](./modals), but 9 out of 10 times this is overkill.

Instead, you can use notifications.

![Notification example](/img/notifications/notification.png)

Notifications are small message boxes that you can use to convey an (important) message to the user. They're most often used for small confirmations or warnings like "Saved successfully" or "Failed to load extensions X".

## Usage

Directus uses [the Notyf library](https://github.com/caroso1222/notyf) under the hood. This plugin is available in `this.$notify` key.

```vue
<script>
export default {
  name: "my-component",
  created() {
    this.$notify.confirm("Component created!");
  }
}
```

Please checkout [the documentation of the Notyf library](https://github.com/caroso1222/notyf) for more information on how to use it.

::: warning
The Notyf library is not actively supported and leaves some things to be desired. We're considering creating our own implementation instead.
:::
