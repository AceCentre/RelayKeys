# 🤔 Troubleshooting

> Below are solutions to some common issues that you may experience when working with Directus. You can also post questions to [StackOverflow](https://stackoverflow.com/questions/tagged/directus) or reach out to the members of our [Slack](https://slack.directus.io) community!

::: warning Premium Support
Due to the enormous number of people using Directus, our Core Team can only provide support to paying Directus Cloud customers or clients who purchase support hours.
:::

## Installation Issues

### The app shows an error saying that there aren't any system extensions installed

This is shown when the API you're trying to connect to doesn't have any extensions installed. This often occurs when you've installed the API from source, but forgot to build the extensions. You can fix this by going in the `extensions` folder in your `api` directory and running `npm install && npm run build`

### When I refresh, I get a 404

The application is a single-page webapp, meaning that all routing is done client side. By default, the app tries using pretty URLs for it's pages. If your webserver doesn't route all requests to `/index.html` correctly, there's no page to return and you'll end up with a 404. To fix this, you can either update your servers routing setup _or_ switch the app's [`routerMode` to `hash`](../advanced/app/configuration.md).

### My MAMP installation returns 403s for everything

MAMP has a known issue where it strips out the `Authorization` header which Directus uses to provide the API with the user token. To fix this, change MAMP's PHP setting from CGI to Module mode.

## Buildchain Issues

If for some reason the buildchain is acting up, or you're not seeing the changes you've made reflected in the browser, please try the following things:

### Restart the buildchain

If you're running the application in development mode (by running `npm run dev`), stop the buildchain by pressing Ctrl+C and re-start it by running `npm run dev` again.

### Delete the caches

The buildchain caches the changes in the `node_modules/.cache` folder. Stop the buildchain by pressing Ctrl+C, delete that folder and restart the buildchain.

### Delete and re-install node_modules

This will both delete the cache and makes sure you're using the latest versions of the dependencies that Directus uses.

### Re-clone the project

If all else fails, a full reinstall of everything has to work. If it doesn't work after a reinstall, something else in the code is broken.
