# Deploying Versions

> Deploying (building) new versions of Directus is a multifaceted process. The Application and API should be treated as two separate entities, which are only bundled together as the Directus Suite in the final step.

The output of the deploy process is the full "Directus Suite", which is located within the combined build ([`directus/directus`](https://github.com/directus/directus)) repository. This codebase is essentially the Directus API ([`directus/api`](https://github.com/directus/api)) with the Directus App ([`directus/app`](https://github.com/directus/app)) included in the `/public/admin/` directory. All other differences can be referenced in the following deploy steps.

::: warning
These steps need to be followed precisely. Any deviation will cause breaking changes.
:::

::: tip Automated
Eventually, we want to automate these steps in some sort of deploy script to make sure the build is the same each time.
:::

## Deploying the Application

1. Clone the app repo

```bash
$ git clone git@github.com:directus/app.git
$ cd app
```

2. Bump the version in `package.json`

3. Install npm dependencies

```bash
$ npm install
```

4. Build the app

```bash
npm run build
```

5. Clone the build branch of the app

```bash
$ cd ../
$ git clone -b build git@github.com:directus/app.git app-build
```

6. Delete everything in `app-build` except the `.git` folder

7. Copy everything from `app/dist` to `app-build`

```bash
$ cp -r app/dist/. app-build
```

8. Delete all .DS_Store files

```bash
$ cd app-build
$ find . -name '.DS_Store' -type f -delete
```

9. Add-commit-push

```bash
$ git add .
$ git commit -m "<VERSION NUMBER>"
$ git push origin build
```

10. Create release on GH

11. Delete local repos

```bash
$ cd ..
$ rm -rf app
$ rm -rf app-build
```

## Deploying the API

1. Clone the api repo

```bash
$ git clone git@github.com:directus/api.git
$ cd api
```

2. Bump the version in `package.json` and `src/core/Directus/Application/Application.php`

3. Install the composer dependencies

```bash
$ composer install -a
```

4. Install and build the system extensions

```bash
$ cd extensions
$ npm install
$ npm run build
$ cd ..
```

5. Clone the build branch of the api

```bash
$ cd ..
$ git clone -b build git@github.com:directus/api.git api-build
```

6. Delete everything in `api-build` except the `.git` folder and `composer.json` file

7. Delete all nested .git folders (prevent submodules)

```bash
$ cd api/vendor
$ ( find . -type d -name ".git" \
  && find . -name ".gitignore" \
  && find . -name ".gitmodules" ) | xargs rm -rf
$ cd ..
```

8. Move these files into `api-build`:

* bin/
* config/
* logs/
* migrations/
* public/
* src/
* vendor/
* LICENSE.md
* README.md
* composer.json


9. Delete all .DS_Store files

```bash
$ cd api-build
$ find . -name '.DS_Store' -type f -delete
```

10. Add this .gitignore file:

```
Icon
.DS_Store
*.log
.cache

# Ignore dev files
/.idea
node_modules

package-lock.json

# Don't track composer phar/vendors
composer.phar
composer.lock

# Ignore configuration files
/config/*
!/config/migrations.php
!/config/migrations.upgrades.php
!/config/api_sample.php

# PHPUnit
/phpunit.xml
/documents

# Custom extensions
/public/extensions/custom/*/*

##  Auth
/public/extensions/custom/auth

##  Endpoints
!/public/extensions/custom/endpoints/_directory/
!/public/extensions/custom/endpoints/_example.php

##  Hashers
!/public/extensions/custom/hashers/_CustomHasher.php

##  Hooks
!/public/extensions/custom/hooks/_products
!/public/extensions/custom/hooks/_webhook

# Storage
/public/uploads/*/
!public/uploads/_/originals/.gitignore
!public/uploads/_/thumbnails/.gitignore

# Keep gitkeep files
# This will make sure empty directories has at least one file so it can be tracked by git
!**/.gitkeep
```

11. Add-commit-push

```bash
$ git add .
$ git commit -m "<VERSION NUMBER>"
$ git push origin build
```

12. Create release on GH

13. Delete local repos

```bash
$ cd ..
$ rm -rf api
$ rm -rf api-build
```

## Deploying the Suite

_AKA The Combined Build_

1. Clone the directus/directus repo

```bash
$ git clone git@github.com:directus/directus.git
```

2. Delete everything in it except the `.git` and `.github` folders

3. Clone the api build

```bash
$ git clone -b build git@github.com:directus/api.git api-build
```

4. Remove the `.git` folder from the `api-build` folder

```bash
$ rm -rf api-build/.git
```

5. Copy everything in the api-build folder to the main directus/directus repo

```bash
$ cp -r api-build/* directus
```

6. Clone the app build

```bash
$ git clone -b build git@github.com:directus/app.git app-build
```

7. Make the public/admin directory in directus/directus

```bash
$ mkdir directus/public/admin
```

8. Delete the `.git` folder from the app-build

```bash
$ rm -rf app-build/.git
```

9. Copy everything from app-build to directus/public/admin

```bash
$ cp -r app-build/* directus/public/admin
```

10. Duplicate the `directus/public/admin/config_example.js` file to `directus/public/admin/config.js`

```bash
$ cp directus/public/admin/config_example.js directus/public/admin/config.js
```

11. Change the `directus/public/admin/config.js` file to point to the relative API

```js
api: {
  "../_/": "Directus API"
}
```

12. Delete all .DS_Store files

```bash
$ cd directus
$ find . -name '.DS_Store' -type f -delete
```

13. Add-commit-push

```bash
$ git add .
$ git commit -m "<VERSION NUMBER>"
$ git push origin master
```

14. Create release on GH

15. Delete local repos

```bash
$ cd ..
$ rm -rf directus
$ rm -rf api-build
$ rm -rf app-build
```

## Tagging Docs Releases

When releasing a new major or minor version (not a patch) we should also create a git release tag on `directus/docs`. This will ensure that users of previous versions can go back and look at the specific docs from that version.

It's also important to _flag_ each new feature in the Docs with a version number (eg: `7.1+`) so that users can tell when a new feature was made available.
