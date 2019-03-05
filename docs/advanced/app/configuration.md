# Configuring the App

> The App uses a client side config file in order to set certain behavioral settings. The config file is a JavaScript file that adds an object into the window's global scope, which the application in turn uses.

## Allowed APIs

The `api` key allows you to set the API URL the application tries to connect to. The object follows the format `"url": "name"`:

```js
{
  // ...

  api: {
    "https://demo-api.directus.app/_/": "Directus Demo API"
  }

  // ...
}
```

You can add multiple API urls by adding multiple keys to this object. This will result in the application rendering a dropdown on the login page which the user can use to pick between the different available APIs.

```js
{
  // ...

  api: {
    "https://demo-api.directus.app/_/": "Directus Demo API",
    "http://localhost:8080/_/": "Local Test",
    "https://api.example.com/prod/": "Example Production"
  }

  // ...
}
```

::: warning
Don't forget to add the [API Project](#) in the URL!
:::

## Allow Other API

By setting the `allowOtherAPI` to true, the application will render an additional "Other" option in the API picker dropdown, which allows the user to log into any API by providing it's URL manually.

## Router Mode

The `routerMode` option controls the way in which the applications creates it's links. By default, this option is set to `history`. In `history` mode, links will be "absolute".

These "absolute" links mean that your server will have to route every request to the `/index.html` file. If it doesn't, the user will get a 404 error when refreshing or directly opening a URL.

The alternative value for this option is `hash`. In `hash` mode, every link will be prepended with a `#` character, which results in the browser treating every link as the same page. This fixes the routing problem mentioned above, and allows you to use the application on servers where you can't control the routing rules on the server.

**History Mode**
```url
https://directus.app/collections/projects/2
https://directus.app/settings/roles/5
https://directus.app/ext/dashboard
```

**Hash Mode**
```url
https://directus.app/#/collections/projects/2
https://directus.app/#/settings/roles/5
https://directus.app/#/ext/dashboard
```