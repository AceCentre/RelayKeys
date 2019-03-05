# Projects

> Each project represents a database. Projects can be used to organize different application schemas or environments.

## Multitenancy

Directus allows for one instance of the API/App to manage any number of project databases. Each project has its own database and is configured in its dedicated API config file, where all options can be configured.

::: tip
[View all project options available within the API configuration.](/advanced/api/configuration.html#config-file-options)
:::

::: tip
[Learn how to connect to your different project APIs.](/api/reference.html#project-prefix)
:::

## Creating a New Project

1. Create a new database and database user
1. Create a new API config file
1. Add the API URL to your App config file
1. Run the Directus Installer or manually setup

## Deleting a Project

As of now, this can only be done manually.

1. Delete the project's database
1. Delete the project's API config file
1. Delete the project from your App's config file
1. Delete any files in that project's storage adapter
