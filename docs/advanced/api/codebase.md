# API Codebase Overview

> The Directus API core codebase is written in PHP. It is organized with a "flat" directory structure so that developers can quickly find what they're looking for, making contributions easier.

* [`/bin`](https://github.com/directus/api/blob/master/bin) — Directus-specific script files used on the command line (eg: running tests or installing)
* [`/config`](https://github.com/directus/api/blob/master/config) — Project configuration files for each database
* [`/docker`](https://github.com/directus/api/blob/master/docker) — Server specific files for Docker containers
* [`/extensions`](https://github.com/directus/api/blob/master/extensions) —
  * [`/core`](https://github.com/directus/api/blob/master/extensions/core) —
  * [`/mixins`](https://github.com/directus/api/blob/master/extensions/mixins) —
* [`/logs`](https://github.com/directus/api/blob/master/logs) — Error and access logs
* [`/migrations`](https://github.com/directus/api/blob/master/migrations) — Database migrations and seeders are used during installation and version upgrades
  * [`/db`] — Installation Migrations and Seeders
  * ['/upgrades] — Upgrade Migrations and Seeders
* [`/public`](https://github.com/directus/api/blob/master/public) — The entry point of the API (index.php) and public files (assets, uploads, and extensions)
  * [`/extensions`](https://github.com/directus/api/blob/master/public/extensions) — API Core and Custom Extensions (such as interfaces, pages, hooks, etc)
    * [`/core`](https://github.com/directus/api/blob/master/public/extensions/core) — Core Extensions
    * [`/custom`](https://github.com/directus/api/blob/master/public/extensions/custom) — User-defined extensions
  * [`/thumbnail`](https://github.com/directus/api/blob/master/public/thumbnail) — Thumbnail generator
  * [`/uploads`](https://github.com/directus/api/blob/master/public/uploads) — API uploaded files
    * [`/_`](https://github.com/directus/api/blob/master/public/uploads/_) — Default Project uploaded files
* [`/src`](https://github.com/directus/api/blob/master/src) — The main Directus API codebase
  * [`/core/Directus`](https://github.com/directus/api/blob/master/src/core/Directus) — Core libraries
  * [`/endpoints`](https://github.com/directus/api/blob/master/src/endpoints) — Endpoint controllers
  * [`/helpers`](https://github.com/directus/api/blob/master/src/helpers) — Function helpers
  * [`/mail`](https://github.com/directus/api/blob/master/src/mail) — Email templates
  * [`/services`](https://github.com/directus/api/blob/master/src/services) — Business logic (service-layer)
  * [`schema.sql`](https://github.com/directus/api/blob/master/src/schema.sql) — The empty MySQL database boilerplate
  * [`web.php`](https://github.com/directus/api/blob/master/src/web.php) — The http/web entry-point bootstrap
* [`/tests`](https://github.com/directus/api/blob/master/tests) — HTTP response tests with actual requests, and PHPUnit code tests
  * [`/api`](https://github.com/directus/api/blob/master/tests/api) — Code tests
  * [`/assets`](https://github.com/directus/api/blob/master/tests/assets) — Assets used for testings purposes
  * [`/io`](https://github.com/directus/api/blob/master/tests/io) — Request and Response Tests (HTTP Response Tests)
  * [`/utils`](https://github.com/directus/api/blob/master/tests/utils) — Tests Utils functions
  * [`db.sql`](https://github.com/directus/api/blob/master/tests/db.sql) — Tests database dump
* [`.editorconfig`](https://github.com/directus/api/blob/master/.editorconfig) — Defines the Directus code styling
* [`.gitignore`](https://github.com/directus/api/blob/master/.gitignore) — Defines which files/directories should not be committed to git
* [`.scrutinizer.yml`](https://github.com/directus/api/blob/master/.scrutinizer.yml) — Scrutinizer configuration to analyze the php code
* [`.travis.yml`](https://github.com/directus/api/blob/master/.travis.yml) — Travis CI configuration to run tests
* [`LICENSE.md`](https://github.com/directus/api/blob/master/LICENSE.md) — This is the GPLv3 license
* [`composer.json`](https://github.com/directus/api/blob/master/composer.json) — Defines all PHP dependencies
* [`docker-compose.yml`](https://github.com/directus/api/blob/master/docker-compose.yml) — Docker configuration to compose a container
* [`package.json`](https://github.com/directus/api/blob/master/package.json) — 
* [`phpunit.php`](https://github.com/directus/api/blob/master/phpunit.php) — PHPUnit bootstrap file
* [`phpunit.xml.dist`](https://github.com/directus/api/blob/master/phpunit.xml.dist) — PHPunit configuration
