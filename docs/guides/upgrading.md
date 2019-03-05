# Upgrading

Each new release of Directus comes with migration files that make upgrading as easy as possible. The standard upgrade process is as follows:

1. Navigate (`cd`) to the root diretory of Directus
2. Run `git pull origin` to get the latest code
3. Run `bin/directus db:upgrade` to update your database with the migration script
    * You can also run the migration script by clicking: _Settings > Upgrade_

::: tip Versionless API
The Directus API is "versionless", which means that new releases will only include fixes and improvements, but no deprecations or breaking changes.
:::

::: warning Legacy Upgrades
Directus 7 is a major release with significant breaking changes from previous versions. Therefore there is no automated way to migrate your settings and configuration from v6 to v7. However, because Directus stores your content as pure SQL, that data is always portable between versions. [Learn More About Legacy Upgrades](/advanced/legacy-upgrades.md)
:::

## Manually Upgrading FTP Installs

If you do not have access to git on your server and installed Directus via FTP, then your upgrade process is as follows:

1. Download the [latest release of Directus](https://github.com/directus/directus/releases/latest)
2. Upload/replace existing Directus files **making sure not to replace**:
    * [API](https://github.com/directus/directus/tree/master/config) config files (`api.php`, `api.[project].php`, etc)
    * [App](https://github.com/directus/directus/blob/master/public/admin/config.js) config file
    * [File storage directory](https://github.com/directus/directus/tree/master/public/uploads)
    * [Custom extensions](https://github.com/directus/directus/tree/master/public/extensions/custom)
    * [Log files](https://github.com/directus/directus/tree/master/logs)
    * Overrides for [CSS](https://github.com/directus/directus/blob/master/public/admin/style.css) and [Javascript](https://github.com/directus/directus/blob/master/public/admin/script.js)
3. Run the database migration script by clicking: _Settings > Upgrade_

## How can I find my current version of Directus?

You can see your App version by hovering over "Powered by Directus" at the bottom of the Login page. The API and App versions are also included in the response from the [Server Information endpoint](/api/reference#information) (located at `/`).
