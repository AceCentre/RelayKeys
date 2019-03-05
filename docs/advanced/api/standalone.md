# Standalone API

> Our decoupled architecture allows you to install just the Directus API, without the admin App. This is useful if you want one App to manage multiple APIs.

## Requirements

Directus is quite flexible and can be installed on many different varieties of server/database setups. Learn more about the [Directus Requirements](/advanced/requirements.md).

* HTTP/Web Server
* MySQL 5.2+
    * Database (empty or existing)
    * Database User (with access to database)
* PHP 7.1+
    * `pdo` + `mysql`
    * `curl`
    * `gd`
    * `fileinfo`
    * `mbstring`
    * `xml` (Only if you are installing PHPUnit)

## Installation

Installation will vary depending on your specific server and project goals. This guide with walk you through three of the most common installation methods.

### Using Git

The easiest way of installing and updating the API is through Git. By using the build branch on our repo, you're assured to have the latest version pre-bundled and ready to go.

To install the pre-bundled build version through Git, run

```bash
git clone -b build https://github.com/directus/api.git
```

### Manually

If you don't have access to the command line for your server, you can download the static bundle manually as a zip. Head over to [the releases page](https://github.com/directus/api/releases) to download a fresh copy of the latest version.

### Web Server Setup

Directus API should work on any HTTP Server, but most testing has been done on Apache 2, NGINX, and Caddy.

1. The root directory for Directus API should be set the `/public` directory.
2. Make sure the directory ownership is set to user the web server is running under. Usually the user is `www-data`
    * eg: `sudo chown -R www-data:www-data /var/www/api`
3. The following files/folders should have write permission:
    * `/logs`
    * `/public/uploads` (or your configured upload directory)

#### Specific Server Setup

[Apache 2 Setup](/advanced/server-setup.md#apache)

[NGINX Setup](/advanced/server-setup.md#nginx)

[Caddy Setup](/advanced/server-setup.md#caddy)

::: tip
For local development environments you can use WAMP, XAMP or MAMP
:::

::: tip
We appreciate any pull-requests outlining steps for new server-types. Just submit them to [these Docs on GitHub](https://github.com/directus/docs).
:::

## Configuration

Lastly, we need to generate a project config file and add the system boilerplate data to the database.

[Configure with App](/advanced/api/configuration.md#configure-with-app)

[Configure with Script](/advanced/api/configuration.md#configure-with-script)

[Configure Manually](/advanced/api/configuration.md#configure-manually)

Once you've finished configuration then you have successfully installed the Directus API and can now access secure endpoints with your Admin credentials. To learn more about the many Directus API endpoints you can browse our [API Reference](/api/reference.md).

## Updating

With a versionless API, nothing is ever removed or changed—only added. This means that you never have to worry about breaking your integrations when upgrading to the latest version. We've thoroughly vetted every endpoint and parameter in our new decoupled API to ensure there is no need for deprecations in the foreseeable future. You'll also notice that our API URLs don't include a version number, but you can still reference the technical API version in code to know which new features are available.

### Using Git

If you're using a direct clone of the `build` branch, all you need to do to update the API is run

```bash
$ git pull
```

### Manually

Updating is basically the same as installing fresh. You can download a copy of the latest version from [the releases page](https://github.com/directus/api/releases) and overwrite the files you had before. **Make sure not to override any uploads within `/public/uploads/`, logs within `/logs`, or config files within `/config/*.php`**.

### Upgrade Database

After you update the Directus API code, there may be changes in the database, such as a new field, a field with a different interface or new options.

You can upgrade the database using the [terminal](/guides/cli.md) or the [endpoint](/api/reference.md#update)
