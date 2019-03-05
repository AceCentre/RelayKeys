# Loading Queue (Running Rabbit)

The Directus app uses a global loading indicator. The rabbit runs as long as there's active requests in the queue which is stored in the [store](./store.md).

## Usage

This queue is  an array of objects containing a unique ID and optional other fields. All other fields are ignored right now, but might be used in the future to list the active requests in a human readable way.

To add something to this queue, you can use the `loadingStart` action in the store:

```js
const id = this.$helpers.shortid.generate();
this.$store.dispatch("loadingStart", { id });
```

::: warning
It's important that you use a globally unique ID for the loading queue.
:::

To remove something from the queue, dispatch the `loadingFinished` action:

```js
this.$store.dispatch("loadingFinished", id);
```

**Full example**
```js
const id = this.$helpers.shortid.generate();
this.$store.dispatch("loadingStart", { id });

this.$api.getItems("projects")
  .then(res => {
    this.$store.dispatch("loadingFinished", id);
  })
  .catch(error => {
    this.$store.dispatch("loadingFinished", id);
  });
```

::: tip
Don't forget to dispatch the loadingFinished action in case of an error too! If you don't, the rabbit might run indefinitely. The poor thing!
:::
