# Standalone Application

> Our decoupled architecture allows you to install just the Directus Application, without the API. This is useful if you want one App to manage multiple APIs.

## Requirements

The Directus App is comprised of static files and does not have any special requirements. However if you would like to use "history" mode for clean URLs then you will need a way to route all traffic to the App's `/public/index.html` file.

## Installation

The Directus application is a static single-page webapp (SPA) and can be installed in three ways:

### Using Git

The easiest way of installing and updating the app is through Git. By using the build branch on our repo, you're assured to have the latest version pre-bundled and ready to go.

To install the pre-bundled build version through Git, run

```bash
$ git clone -b build https://github.com/directus/app.git directus
```

### Manually

If you don't have access to the command line in your server, you can download the static bundle manually as a zip. Head over to [the releases page](https://github.com/directus/app/releases) to download a fresh copy of the latest version.

::: tip
For instructions on how to setup a local development copy, checkout our [dev install guide](https://docs.directus.io/app/contributor/install-dev.html#decoupled)
:::

### Using Docker

See [https://github.com/directus/docker](https://github.com/directus/docker)

## Configuration

After you've installed the application, you need to create a config file. This file controls what API instances the app tries to connect to. The easiest way to create this file is by renaming or duplicating the `config_example.js` file to `config.js` and adjusting the default settings within.

## Updating

### Using Git

If you're using a direct clone of the `build` branch, all you need to do to update the application is run

```bash
$ git pull
```

### Manually

Updating is basically the same as installing fresh. You can download a copy of the latest version from [the releases page](https://github.com/directus/app/releases) and overwrite the files you had before. **Make sure not to override your `config.js` file**.

### Using Docker

Updating the application is the same as in the manual way. Download a fresh copy of the application from the [releases page](https://github.com/directus/app/releases) and overwrite all the files in use. Remember to restart your Docker process.
