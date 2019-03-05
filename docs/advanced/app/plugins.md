# Plugins

## Lodash

Lodash is available in every Vue component. It's accessible under the `$lodash` property:

```js
{
  computed: {
    fields() {
      return this.$lodash.keyBy(this.fields, "field");
    }
  }
}
```

## Directus SDK

Accessing the API is done through the Directus JavaScript SDK. The whole SDK is available in the `$api` property:

```js
{
  created() {
    this.$api.getItems("projects")
      .then(res => res.data)
      .then(fields => {
        this.fields = fields;
        this.loading = false;
      });
  }
}
```

::: tip
For more info on using the SDK, checkout [Working with the API](#)
:::

## Notifications

You can use [Notyf](https://github.com/caroso1222/notyf) To show notifications / alerts on screen. Notyf is available in the `$notify` key:

```js
{
  methods: {
    save() {
      // ...

      this.$notify.confirm("Saved succesfully!");
    }
  }
}
```
