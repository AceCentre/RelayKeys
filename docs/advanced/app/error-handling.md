# Error Handling

In general, every time you work with user input or work with an / the API, you should expect the interaction to fail. Even seemingly small/safe interactions can fail in multiple ways.

If you're working on the application code itself (in the `directus/app` repo), you can use a global error handler function. This function will log the full error in the console, show an optional notification to the user and (in the future) log the error to a centralized error-collection server.

This error handler can be used by firing a global `error` event:

```js
this.$events.emit("error", {
  notify: "Yikes! Something went wrong..",
  error: {}
});
```

Real-life example:

```js
this.$store
  .dispatch("saveBookmark", preferences)
  .then(() => {
    this.$store.dispatch("loadingFinished", id);
    this.bookmarkModal = false;
    this.bookmarkTitle = "";
  })
  .catch(error => {
    this.$store.dispatch("loadingFinished", id);

    this.$events.emit("error", {
      notify: this.$t("something_went_wrong_body"),
      error
    });

  });
```

::: tip
[Click here to learn more about the global events](./events.md)
:::
