# Setup Development Environment

> If you would like to make contributions to the Directus codebase then you'll need to install the App and API from source. However, you do not need to do this to build new extensions.

## API Source

In order to work on the API, you'll need to install the source version locally. The application sourcecode is being hosted in the [directus/api](https://github.com/directus/api) repo on GitHub.

### Requirements

* A HTTP Web Server that supports URL rewrites
    * _Comes with .htaccess included for Apache_
* MySQL 5.2+
    * Database (empty or existing)
    * Database User (with access to database)
* PHP 7.1+
    * `pdo` + `mysql`
    * `curl`
    * `gd`
    * `fileinfo`
    * `mbstring`
    * `xml` (Only if you are installing phpunit)
* [Node.js](https://nodejs.org) v8.11.3 or higher (preferably v10.6+)
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to fetch the source code from GitHub
* [Composer](https://getcomposer.org/doc/00-intro.md#installation-linux-unix-osx) to install dependencies

:::warning Important
[Click here to learn more about these system requirements, neccesary permissions, and other important and server-specific prerequisites.](/advanced/requirements.md)
:::

### Setup Steps

#### 1. Clone the repo

Clone the repo by running

```bash
git clone https://github.com/directus/api.git
```

OR

```bash
git clone git@github.com:directus/api.git
```

::: warning Fork
If you want to work on your fork of the project, remember to replace `directus` with your GitHub username in the url above
:::

#### 2. Install the Composer dependencies

```bash
composer install
```

If you don't want to install any development package use the `--no-dev` option.

```bash
composer install --no-dev
```

#### 3. Install the npm dependencies of and build the extensions

```bash
cd extensions
npm install
npm run build
```

::: tip Development mode
Just like the app, if you'd like to actively work on Extensions, use `npm run dev` instead of `npm run build`.
:::

#### 4. Create a database

On your local server, create a new database to use with the API.

##### Boilerplate SQL

If you'd rather skip the installer (next step), you can simply import the boilerplate schema file from [the included schema.sql file](https://github.com/directus/api/blob/master/src/schema.sql).

##### Demo SQL

This file comes with the boilerplate schema as well as some dummy collections, fields, data, and Settings. You can [download a demo SQL schema](https://sql.directus.app/demo.sql) to skip the API's installation process.

::: tip Credentials
If you are skipping the installer and adding the SQL directly to your database, the default login credentials are:

* **User:** `admin@example.com`
* **Password:** `password`
:::

#### 5. Config File Installer

The API uses a config file to know which database to connect to. Copy or rename the `/config/api_sample.php` file to `/config/api.php` (default project) and edit the settings as indicated.

[Learn more about configuring the API](/advanced/api/standalone.md)

## Application Source

In order to work on the app, you'll need to install the application locally.

::: tip
To quickly debug the application you can use [our demo API](https://next.demo-api.directus.app) by authenticating with the credentials: `admin@example.com` and `password`.
:::

### Requirements

The application is built with [Vue.js](https://vuejs.org) and heavily relies on [Node.js](https://nodejs.org) to be bundled / transpiled to browser-usable code. In order to work on Directus, you need [Node.js](https://nodejs.org) v8.11.3 or higher (preferably v10.6+).

The application source code is being hosted in the [directus/app](https://github.com/directus/app) repo on GitHub.

### Steps

#### 1. Clone the repo

Clone the repo by running

```bash
git clone https://github.com/directus/app.git
```

OR

```bash
git clone git@github.com:directus/app.git
```

::: warning Fork
If you want to work on your fork of the project, remember to replace `directus` with your GitHub username in the url above.
:::

#### 2. Install the [npm](https://npmjs.com) dependencies

```bash
npm install
```

#### 3. Add a config file

The application makes use of a config file that's found in the `public` folder in the root of the folder. To prevent issues when upgrading the app, we decided to ignore the default version of this config file. We do provide an example that you can duplicate. Move or rename the `/public/config_example.js` file to `/public/config.js` file to your hearts content.

::: tip
The default config file lets you test the app using the live Directus Demo API. Don't forget to add the address of your local API in order to test it.
:::

#### 4. Build / run the app

The production version of the application is a static html file that can be hosted on any static file server. In order to build the app for production, run

```bash
npm run build
```

To checkout the app itself, you'll need a static file server. Any static file server, like MAMP, local Apache or Caddy, should work. If you don't have a quick server at hand, I recommend using [`http-server`](https://www.npmjs.com/package/http-server).

Install `http-server` globally, run

```bash
npm install --global http-server
```

When it's installed, you can serve the app by running `http-server` from the `dist` folder that has been created by the `build` command:

```bash
cd dist
http-server
```

::: tip Development Mode
If you're actively working on the application, we recommend using the development mode. By using `npm run dev` instead of `npm run build`, the buildchain will launch a local file server and will auto-rebuild the code and auto-refresh the browser on save of a file.
:::