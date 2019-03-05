# Configuring the API

> Each API project configuration is contained within a dedicated file in the `/config` directory. Additionally, this process adds a boilerplate system schema into the project's database.

::: tip
If you are using Apache, make sure `mod_rewrite` and `AllowOverride` are enabled. [Read more](../advanced/server-setup.md#apache)
:::

## Project Config Files

Each API instance can manage multiple projects. Each project has its own config, database, and file storage. Any extensions installed in the API will be available for all projects it manages.

The first project you create must be the default. Default projects are defined by their config file name: `config/api.php` and use the `_` API URL project scope, eg: `https://api.example.com/_/collections`

Subsequent projects can be added with new config files, using this naming convention: `config/api.[project-name].php`. Each project's config should point to a dedicated database and unique storage paths. Once configured, the API URL will be scoped to the project, eg: `https://api.example.com/project-name/collections`

## Configure Manually

::: tip
After configuring, if you would like to login to your custom project using the Directus Frontend, you'll need to add your new project as an entry into the `config.js` file.
:::

### Create Config File

Create a copy of [`config/api_sample.php`](https://github.com/directus/api/blob/master/config/api_sample.php) and change the name to `config/api.php` (for default project).

### Database Details

Next, update the `database` values with your own:

```php
'database' => [
    'type' => 'mysql',
    'host' => 'localhost',
    'port' => 3306,
    'name' => 'directus_test',
    'username' => 'root',
    'password' => 'root',
    'engine' => 'InnoDB',
    'charset' => 'utf8mb4'
]
```

### Auth Keys

These keys can be anything, but we recommend a “strong” and unique value. They are unique identifiers that ensure your auth tokens are only able to be used within this project.

```
'auth' => [
  'secret_key' => '<secret-authentication-key>',
  'public_key' => '<public-authentication-key>',
  'social_providers' => [ ... ]
```

### Boilerplate System Database

Finally, we must import the Directus system tables and data primer into the database by importing this SQL file: `/src/schema.sql`. With this method, your initial Admin user credentials will be:

* **User:** `admin@example.com`
* **Password:** `password`

## Configure with Script

### Create Config File

```bash
$ bin/directus install:config -n <database-name> -u <mysql-user> -p <mysql-password>
```

### Options

| Name    | Description                                                           |
|---------|-----------------------------------------------------------------------|
| `-h`    | Hostname or IP address of the database server (Default: `localhost`)  |
| `-P`    | Port of the database server (Default: `3306`)                         |
| `-t`    | Type of the database (Default: `mysql`)                               |
| `-n`    | Name of the database                                                  |
| `-u`    | Username for the database connection                                  |
| `-p`    | Password for the database connection                                  |
| `-c`    | Tell to enable or disable CORS (Default: `false`)                     |
| `-e`    | Email used by the Mailer as From/Sender (Default: `admin@example.com`)|
| `-N`    | Name of the project (Default: `_`)                                    |

### Boilerplate System Database

```bash
$ bin/directus install:database
```

### Create Admin User

```bash
$ bin/directus install:install -e <admin-email> -p <admin-password> -t <project-title>
```

#### Options

| Name    | Description                                                           |
|---------|-----------------------------------------------------------------------|
| `-e`    | Email of the Directus user (Default: `admin@example.com`)             |
| `-p`    | Password of the Directus user (Default: `password`)                   |
| `-T`    | Token of the Directus user                   |
| `-t`    | Title of the project (Default: `Directus`)                            |
| `-N`    | Name of the project (Default: `_`)                                    |

### Testing

Test that everything is working by making a request to the `users` endpoint using the `access_token`.

```
GET http://localhost/_/users?access_token=admin_token
```

## Configure with App

@TODO

## Config File Options

### `app`

The API application settings

| Name          | Description   |
| ------------- | ------------- |
| `env`         | Defines the detail of PHP error reporting (errors, warning, and notices). Options: `development` (default) or `production` |
| `timezone`    | PHP default timezone  |

### `settings`

The settings for [Slim](https://www.slimframework.com/), the micro-framework used by Directus

| Name          | Description   |
| ------------- | ------------- |
| `logger`      | The Directus [Monolog]() logger configuration. Settings: `path` - where the log should be stored |

::: tip
Currently the logger only works on the server's filesystem
:::

### `database`

Settings for the database connection

| Name          | Description   |
| ------------- | ------------- |
| `type`        | Database type. `mysql` and any drop-in replacements (MariaDB, Percona) are supported |
| `host`        | Database server host |
| `port`        | Database server port number |
| `name`        | Database name |
| `username`    | Database user username |
| `password`    | Database user password |
| `engine`      | Database storage engine |
| `charset`     | Database connection charset |
| `socket`      | Unix socket used for connection. It shouldn't be used with `host` |

### `cache`

Enables caching to speed-up API responses

| Name          | Description   |
| ------------- | ------------- |
| `enabled`     | Whether or not the cache is enabled. Default: `false`
| `response_ttl`| How long the cache will exists in seconds
| `pool`        | Where the cache will be stored: `filesystem`, `redis`, `apc`, `apcu` or `memcached`


#### APC

It uses PHP [Alternative PHP Cache (APC)](https://secure.php.net/manual/en/book.apc.php) extension to store the cache data.

| Name          | Description   |
| ------------- | ------------- |
| `adapter`     |  Name of the adapter. Must be `apc`

#### APCU

It uses PHP [APC User Cache (APCu)](https://secure.php.net/manual/en/book.apcu.php) extension to store the cache data. APCu is the same extension as APC, the only different is that doesn't have OPCache. Directus only needs the data store feature.

| Name          | Description   |
| ------------- | ------------- |
| `adapter`     |  Name of the adapter. Must be `apcu`

#### Filesystem

It stores cache data in the server's filesystem.

| Name          | Description   |
| ------------- | ------------- |
| `adapter`     |  Name of the adapter. Must be `filesystem`
| `path`        |  Where on the cache will be stored relative to the API root path. Prepend with `/` for absolute

#### Memcached

It uses [Memcached](https://memcached.org) caching system and [PHP Memcached](http://php.net/manual/en/book.memcached.php) extension to store cache data.

| Name          | Description   |
| ------------- | ------------- |
| `adapter`     |  Name of the adapter. Must be `memcached`
| `host`        |  Memcached host
| `port`        |  Memcached server port number

**Note:** Memcached and PHP Memcached extension must be installed.

```
# Ubuntu example
sudo apt-get install memcached
sudo apt-get install php-memcached
```

#### Redis

It uses [Redis](https://redis.io) and [PHP Redis](https://github.com/phpredis/phpredis) extension to store cache data.

| Name          | Description   |
| ------------- | ------------- |
| `adapter`     |  Name of the adapter. Must be `redis`
| `host`        |  Redis server host
| `port`        |  Redis server port number

**Note:** Redis Server and PHP Redis extension must be installed.

```
# Ubuntu example
sudo apt-get install redis-server
sudo apt-get install php-redis
```

### `storage`

Choose where files can be uploaded. Currently we support local and Amazon-S3

| Name          | Description   |
| ------------- | ------------- |
| `adapter`     | `local` for local filesystem or `s3` for Amazon-S3 (Default:  `local`)
| `root`        | Root path where files are uploaded (Default: `./public/uploads/_/originals`)
| `root_url`    | Public URL with access to `root` files (Default: `/uploads/_/originals`)
| `thumb_root`  | Root path where the generated thumbnails images are stored (Default: `./public/uploads/_/thumbnails`)
| `key`         | S3 Bucket Key
| `secret`      | S3 Bucket Secret
| `region`      | S3 Bucket Region
| `version`     | S3 API version
| `bucket`      | S3 Bucket name
| `endpoint`    | Custom S3 endpoint, e.g. `http://minio.acme.com`
| `options`     | S3 Options

:::tip NOTE
If you are using the `s3` storage adapter, you must install the `aws/aws-sdk-php` package. Run `composer require aws/aws-sdk-php` in the terminal.
:::

### `mail`

A list of key-value-pairs (array) mail configurations. Currently only the `default` key is supported. Each value must have at least the following information:

| Name          | Description   |
| ------------- | ------------- |
| `transport`   | `smtp`, `sendmail` or your own class name resolution string (Ex: `\My\Namespace\MyTransport`). This class must extends from `\Directus\Mail\Transports\AbstractTransport`.
| `from`        | The global "from" email address

When the `transport` is set to one of the transports mentioned below, any of those options can be used.

#### `smtp`

| Name          | Description   |
| ------------- | ------------- |
| `host`        | Server's host. Default: `localhost`
| `port`        | Server's port. Default: `25`
| `username`    | Authentication username
| `password`    | Authentication password
| `encryption`  | Connection encryption type, Example: `ssl` or `tls`

#### `sendmail`

| Name          | Description   |
| ------------- | ------------- |
| `sendmail`    | The location of the sendmail command. This value is only required if the path is not `/usr/sbin/sendmail` (default).

::: tip
You can extend `Directus\Mail\Transports\AbstractTransport` class to create your own Swift Mailer transport. All options that exists in your mailer config will be passed to your transport.
:::

### `cors`

Cross-Origin Resource Sharing (CORS) is a mechanism that allows you to restricted access of Directus API from other domains

| Name              | Description   |
| ----------------- | ------------- |
| `enabled`         | Indicate whether or not CORS is enabled
| `origin`          | One more more URI allowed access to the API resource. Default: `*` (All).
| `methods`         | Method or methods allowed to access the API resource. Default: `GET,PUT,PATCH,POST,DELETE,HEAD`.
| `headers`         | List of headers are allowed when making the actual request. Default: `Access-Control-Allow-Headers,Content-Type,Authorization`.
| `exposed_headers` | List of headers the browser are allowed to access. Default: `none`.
| `max_age`         | How long in seconds a preflight request can be cached. Default: `none`.
| `credentials`     | Indicate whether or not to include credentials in the request. Default: `false`.

### `rate_limit`

| Name              | Description   |
| ----------------- | ------------- |
| `enabled`         | Enable or disable the rate limit
| `limit`           | The request limit within the `interval`
| `interval`        | Time to reset the `limit`
| `adapter`         | `redis`, `memory` available
| `host`            | Redis host
| `port`            | Redis port
| `timeout`         | Redis connection timeout

### `actions`

Actions hooks allow you to execute custom code when a Directus Event happens. You can register functions or classes to a hook name and when the event happens it will execute that code. For example:

```php
'hooks' => [
    'actions' => [
        'item.create.articles' => function ($data) {
            $content = 'New article was created with the title: ' . $data['title'];
            // pesudo function
            notify('admin@example.com', 'New Article', $content);
        }
    ]
]
```

The example above will execute the `notify` function after an item has been inserted into the `articles` table.

A class that implements the `__invoke` method or inherits from `\Directus\Hook\HookInterface` can also be used, and instead of passing a function you must pass the fully qualified class name resolution. For example: `\MyApplication\Events\NotifyNewArticles::class`.

### `filters`

Filters work the same as hooks except that you can manipulate the data being passed. This is a nice way to add, remove, or manipulate the data before it is sent to the database. Filters always pass a `\Directus\Hook\Payload` object as the first parameter and it must return a payload object. An example would be generating a new UUID every time an article is created:

```php
'hooks' => [
    'filters' => [
        'item.create.articles:before' => function (\Directus\Hook\Payload $payload) {
            $payload->set('uuid', \Directus\generate_uuid4());

            return $payload;
        }
    ]
]
```

### `feedback`

It doesn't do anything on version 2.0, but it was created to ping our server to understand approximately how many instances of Directus exists.

### `tableBlacklist`

It doesn't do anything, but it was meant to blacklist tables from being used by Directus.

### `auth`

Out-of-the-box Directus supports `Okta`, `GitHub`, `Facebook`, `Twitter` and `Google` Single-Sign-On (SSO), but also allows you to create your own providers.

| Name          | Description   |
| ------------- | ------------- |
| `secret_key`  | This key is used by the JWT encode function to encode tokens |
| `public_key`  | This key is used by the JWT as identifier for all project tokens |
| `social_providers` | List of available third-party authentication providers |

:::tip
The `secret_key` and `public_key` can be anything, but we recommend a "strong" and unique value. They are used to uniquely identify your project so that all your tokens can be more secure by only being able to be used in the same project it was created.
:::

#### Okta

Okta offers both SSO as well as external user management through SCIM. [Learn more about configuring Okta auth](../../guides/sso.md#okta).

| Name            | Description   |
| --------------- | ------------- |
| `client_id`     | Your Okta client id key |
| `client_secret` | Your Okta client secret key |
| `base_url`      | Your okta application base URL |

#### GitHub

| name            | Description   |
| --------------- | ------------- |
| `client_id`     | Your application client id |
| `client_secret` | Your application client secret key |

#### Google

| Name                | Description   |
| ------------------- | ------------- |
| `client_id`         | Your application client id |
| `client_secret`     | Your application client secret key |
| `hosted_domain`     | Your application allowed hosted domain |
| `use_oidc_mode`     | (`true`/`false`) Whether you want to use the Google+ API or the OpenID Connect API. The only main different is that Google+ API needs to be enable before using it. |

#### Twitter

| Name                | Description   |
| ------------------- | ------------- |
| `identifier`        | Your application identifier key |
| `secret`            | Your application secret key |

#### Facebook

| Name                | Description   |
| ------------------- | ------------- |
| `client_id`         | Your application client id |
| `client_secret`     | Your application client secret key |
| `graph_api_version` | Facebook graph API version |
