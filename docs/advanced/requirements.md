# Directus Requirements

## HTTP Web Server

Directus has been developed and tested on [Apache 2](/advanced/server-setup.md#apache).

::: tip Alternate Web Servers
In theory, Directus should work on any HTTP Server, including [NGINX](/advanced/server-setup.md#nginx) and [Caddy](/advanced/server-setup.md#caddy). However these are not officially supported so you should proceed at your own risk.
:::

### Routing

The Directus API requires URL rewriting for routing requests. On Apache this means having `mod_rewrite` enabled for `.htaccess` files.

### Permissions

1. The root directory for Directus API should be `public` directory.
2. Make sure the directory ownership is set to user the web server is running under. Usually the user is `www-data`
    * eg: `sudo chown -R www-data:www-data /var/www/api`
3. The following files/folders should have write permission:
    * `/logs`
    * `/public/uploads` (or your configured upload directory)

## SQL

Directus has been developed and tested on MySQL and requires version 5.2+.

::: tip Alternate SQL Vendors
In theory, Directus should work with MySQL drop-in alternatives such as MariaDB or Percona Server. However these are not officially supported so you should proceed at your own risk.
:::

### Database

To install Directus you will first need a database and a database-user with access to it. You can create a blank database, or install Directus on an existing database that already has a schema and content.

Directus can manage your database's schema, this requires the user to have privileges to create, alter and drop tables in your database. Also the user must have the privilege to insert, update and delete items in the database.

[Learn more about creating a database](/guides/database.md#creating-a-database)

## PHP

Directus requires PHP 7.1+, though we recommend using the most recent/stable version possible.

## PHP Extensions

While most of these PHP extensions are typically included by default, you should confirm that all are installed by checking the `php.ini` of your php (_not CLI_) installation, or using `phpinfo()`.

* `pdo` + `mysql` – PHP Data Objects (PDO) enables safer _parameterized_ queries
* `curl` – cURL fetches metadata (eg: title and thumbnail) from embed services like YouTube and Vimeo
* `gd` – GD allows the [Thumbnailer](https://github.com/directus/directus-thumbnailer) to generate images. To add thumbnail support for SVG, PDF, PSD and TIF/TIFF you must also install the `imagick` extension.
* `fileinfo` – Fetches metadata (eg: charset and file-type) and [IPTC Info](https://iptc.org/standards/photo-metadata/) (eg: location and keywords) for uploaded images.
* `mbstring` – The multibyte string functions helps php to work multibyte encoding. These functions are used by Directus to get the correct string's length or a correct comparison with another string.
* `xml` - Used by PHPUnit (Only required if you are installing PHPUnit)
