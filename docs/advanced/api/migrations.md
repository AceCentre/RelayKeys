# Migrations

The migration and seeder files are created using [Phinx](https://phinx.org). They define a database schema programmatically, making it easier to make and apply changes. Each migration file represents a table.

To create a new migration file use the following command: 
```sh
vendor/bin/phinx create MyNewMigration -c config/migrations.php
``` 
It will create a new migration in the format `YYYYMMDDHHMMSS_my_new_migration.php`, where the first 14 characters are replaced with the current timestamp down to the second.

Once you have the schema updated you'll want to update the content within it. Seeders are a way to insert data into tables, with each seeder representing the default data for a table. Seeders run directly after the migrations, when the database install command is executed.

To [create a new seeder file](http://docs.phinx.org/en/latest/seeding.html#creating-a-new-seed-class) use the following command: 
```sh 
php vendor/bin/phinx seed:create UsersSeeder -c config/migrations.php
``` 
It will create a new file in `migrations/db/seeds` named `UsersSeeder.php` with the similar template shown below.

## Seeder Template

```php
<?php

use Phinx\Seed\AbstractSeed;

class UsersSeeder extends AbstractSeed
{
    /**
     * Run Method.
     *
     * Write your database seeder using this method.
     *
     * More information on writing seeders is available here:
     * http://docs.phinx.org/en/latest/seeding.html
     */
    public function run()
    {

    }
}
```

## Example — Insert Data into `directus_users`

```php
<?php

use Phinx\Seed\AbstractSeed;

class UsersSeeder extends AbstractSeed
{
    public function run()
    {
        $data = [
            [
                'email'    => 'admin@example.com'
            ],[
                'email'    => 'user@example.com'
            ]
        ];

        $posts = $this->table('directus_users');
        $posts->insert($data)
              ->save();
    }
}
```
