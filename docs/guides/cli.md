# Command-Line Interface

> Directus CLI provides commands that allow you to perform various tasks such as installation, resetting a user's email, or upgrading the database to the most recent Directus schema.

## Commands List

| Name                                                  | Description
| ----------------------------------------------------- | -----------------------------
| [`install:config`](#configure-directus)               | Create a configuration file
| [`install:database`](#populate-the-database-schema)   | Create the default tables and data
| [`install:install`](#install-initial-configurations)  | Create initial configuration data
| [`db:upgrade`](#upgrade-directus-schema)              | Upgrade the Database Schema
| [`user:password`](#change-user-password)              | Change a user password
| [`log:prune`](#prune-old-log-files)                   | Remove old logs files

## Help

You can use the `help` command at any time to learn about available CLI actions:

```bash
# this will provide information about the current modules
php bin/directus help
```

To get more information on an specific command you can type "help" followed by the command:

```bash
# this provide information about the **install** module
php bin/directus help install
```

## Install Module

Includes commands to install and configure Directus.

### Configure Directus:

Creates the `config.api.php` file.

:::warning
This command will overwrite any existing default configuration file at `config.api.php`.
:::

```bash
php bin/directus install:config -h <db_host> -n <db_name> -u <db_user> -p <db_pass> -e <directus_email> -s <db_unix_socket>
```

| Option         | Description
| -------------- | -----------------------------
| `t`            | Database type. (**Only `mysql` supported**)
| `h`            | Database host
| `P`            | Database port
| `n`            | Database name (it must already exist)
| `u`            | Database user's name
| `p`            | Database user's password
| `e`            | (Optional) The Directus email that will be used as sender in the mailing process
| `s`            | Database unix socket
| `c`            | Enable/Disable CORS
| `N`            | Unique Project's name
| `timezone`     | API Server default timezone
| `f`            | Force file overwritten

#### Example: http://example.local

```bash
php bin/directus install:config -h localhost -n directus -u root -p pass
```

#### Example: http://example.local/directus

```bash
php bin/directus install:config -h localhost -n directus -u root -p pass -d directus
```

### Populate the Database Schema:

Creates all of the Directus Core tables based on the configuration files: `/config/api.php`.

```bash
php bin/directus install:database
```

### Install Initial Configurations:

Create the default admin user and the site's default settings.

```bash
php bin/directus install:install -e <admin_email> -p <admin_password> -t <site_name>
```

| Option         | Description
| -------------- | -----------------------------
| `e`            | Admin email
| `p`            | Admin password
| `T`            | Admin Static Auth Token
| `t`            | Project title
| `a`            | Project's Application URL
| `N`            | Unique Project's name
| `timezone`     | Admin timezone
| `locale`       | Admin locale
| `f`            | Recreate Directus core tables. Also remove all Directus data

#### Example

```bash
php bin/directus install:install -e admin@directus.local -p password -t "Directus Example"
```

## User Module

Includes commands to manage Directus users

### Change User Password:

```bash
php bin/directus user:password -e <user_email> -p <new_password>
```

* `user_email` - The user's email
* `new_password` - The user's new password

#### Example

```bash
php bin/directus user:password -e admin@directus.local -p newpassword
```

## Database Module

Includes commands to manage Directus database schema

:::tip
This requires that Directus has a valid connection configured in `config/api.php`.
:::

:::warning
Always backup your database before running the database module to prevent data loss.
:::

### Upgrade Directus Schema

```
$ bin/directus db:upgrade
```

The command above will upgrade the default project database, to update an specific project the option `N` can be used.

```
$ bin/directus db:upgrade -N <project-name>
```

## Log Module

### Prune Old Log Files

```bash
php bin/directus log:prune <days>
```

`<days>` is optional. The default value is `30` days.

Removes all the logs that were last modified `<days>` ago. it uses [`filemtime`](http://php.net/manual/en/function.filemtime.php) function to determine the last modified time.

:::tip
You can setup a cronjob to clean old files at a set frequency
:::
