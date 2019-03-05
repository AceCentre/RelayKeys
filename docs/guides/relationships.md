# Relationships

> If certain collections within your project are related then you can connect them with Relationships. There are multiple types of relationships but technically Directus only needs to store one: the **Many-to-One**.

## Many-to-One

A many-to-one (M2O) relationship exists when an item of **Collection A** is linked to one single item of **Collection B**, but an item of **Collection B** may be linked to many items of **Collection A**. For example, a movie has one director, but directors have many movies.

### Setup

This setup is specific to the `movies → directors` (M2O) field. The following steps assume you already have two collections: `movies` and `directors`. Each collection has the default `id` primary key and a `name` field.

::: v-pre
1. Go to **Settings > Collections & Fields > Movies**
2. Click **New Field**
3. Interface: Choose **Many-to-One**
4. Schema: **Name** your field (we're using `director`)
5. Relation: Select **Directors** as the Related Collection
6. Options: Enter a **Dropdown Template** (we're using `{{name}}`)
    * This can be any [MicroMustache](https://www.npmjs.com/package/micromustache) string containing field names available within `directors`
:::

:::tip Matching MySQL Datatype
In this example the `directors` collection uses the default `id` primary key, which has a Database DataType of `INT`. If you're using a different primary key type, such as `STRING`, make sure that your relational field's DataType/Length matches that of the primary key it will store. This can be adjusted under "Advanced Options" in the Field Modal.
:::

#### Screenshots

Both dropdowns under "This Collection" are disabled since those refer to the field we're configuring now. The Related Field is also disabled since it must be the collection's Primary Key. All you need to do is choose which collection you want to relate to... in this case: `directors`.

<img src="../img/m2o/relation.png">

<img src="../img/m2o/field.png" width="100">
<img src="../img/m2o/interface.png" width="100">
<img src="../img/m2o/name.png" width="100">
<img src="../img/m2o/relation.png" width="100">
<img src="../img/m2o/options.png" width="100">
<img src="../img/m2o/done.png" width="100">

## One-to-Many

A one-to-many (O2M) relationship exists when an item of **Collection A** may be linked to many items of **Collection B**, but an item of **Collection B** is linked to only one single item of **Collection A**. For example, directors have many movies, but a movie only has one director. As you can see, this is the _same relationship_ as the M2O above... but looking at it from the opposite direction.

### Setup

This setup is specific to the `directors → movies` (O2M) field. The following steps assume you already have two collections: `movies` and `directors`. Each collection has the default `id` primary key and a `name` field. Additionally, we're assuming you have already created the M2O relationship above, which creates the `movies.director` field.

::: v-pre
1. Go to **Settings > Collections & Fields > Directors**
2. Click **New Field**
3. Interface: Choose **One-to-Many**
4. Schema: **Name** your field (we're using `movies`)
5. Relation: Select **Movies** as the Related Collection and **Director** as the Related Field
    * The `movie.director` field was created during M2O setup above
:::

:::tip Alias Fields
Technically, this process does not create a new field, it remotely manages the relational data using the `movies.director` field. So if you were to look in the database you would not see an actual `directors.movies` column. That is why we call this an "alias", because it simply _represents_ a field.
:::

#### Screenshots

Both dropdowns under "This Collection" are disabled since those refer to the field we're configuring now. First, choose the Related Collection, in this case `movies`. Once that is selected the Field dropdown will update to show the allowed options and you can choose the field that will store the foreign key in the related collection. In this example, `movies.director` will store `director.id` so we choose `director`.

<img src="../img/o2m/relation.png">

<img src="../img/o2m/field.png" width="100">
<img src="../img/o2m/interface.png" width="100">
<img src="../img/o2m/name.png" width="100">
<img src="../img/o2m/relation.png" width="100">
<img src="../img/o2m/relation.png" width="100"> <!-- done -->

## Direction Matters

Now we understand that a M2O and O2M are the _exact_ same relationship... just viewed from opposite directions. The `movies` form shows a M2O dropdown to choose the director, and the `directors` form has a O2M listing to select their movies. But if you were to peek behind the scenes you would only see one entry in `directus_relations` defining this duplex relationship.

:::tip
An easy way to remember which side is which: the "many" is an actual column that stores the foreign key, while the "one" side is a simulated column using the `ALIAS` datatype.
:::

![O2M + M2O](../img/o2m-m2o.png)

## Many-to-Many

A many-to-many (M2M) is a slightly more advanced relationship that allows you to link _any_ items within **Collection A** and **Collection B**. For example, movies can have many genres, and genres can have many movies.

Technically this is not a new relationship type, it is a O2M and M2O _working together_ across a "junction" collection. Each item in the junction (eg: `movie_genres`) is a single link between one item in `movies` and one item in `genres`.

### Setup

This setup is specific to the `movies → genres` (M2M) field. The following steps assume you already have two collections: `movies` and `genres`. Each collection has the default `id` primary key and a `name` field.

::: v-pre
1. Go to **Settings > Collections & Fields**
2. Click **New Collection**
3. **Name** your junction collection (we're using `movie_genres`)
4. Set the junction collection to be _Hidden_ (Optional)
5. Click **New Field** — Add `movie_genres.movie` (basic numeric type)
6. Click **New Field** — Add `movie_genres.genre` (basic numeric type)
7. Go to **Settings > Collections & Fields > Movies**
8. Click **New Field**
9. Interface: Choose **Many-to-Many**
10. Schema: **Name** your field (we're using `genres`)
11. Relation: Select **Genres** as the Related Collection
    * Select **Movie Genres** as the Junction Collection
    * Map `movies.id` to **Movie** under the junction
    * Map `genres.id` to **Genre** under the junction
12. Options: **Visible Columns** sets the columns the interface shows (we're using `name`)
    * **Display Template** sets the columns the interface shows (we're using `{{name}}`)
:::

![M2M](../img/m2m.png)

#### Screenshots

Both dropdowns under "This Collection" are disabled since those refer to the field we're configuring now. The Related Field is also disabled since it must be the collection's Primary Key. First, choose the collection you want to relate to. Now select a junction collection and connect its keys by following the arrows.

<img src="../img/m2m/relation.png">

<img src="../img/m2m/create_junction.png" width="100">
<img src="../img/m2m/junction.png" width="100">
<img src="../img/m2m/interface.png" width="100">
<img src="../img/m2m/relation.png" width="100">
<img src="../img/m2m/options.png" width="100">
<img src="../img/m2m/done.png" width="100">

:::tip Relation Arrows
During relationship setup the App shows arrows between each field to help visualize the data model. *Each arrow points from the primary key field to the foreign key field.*
:::

## Many-to-Any

The many-to-any (M2X) allows you to connect items within **Collection A** to many items from **any collection**. It is essentially the same as a M2M, but requires connected collections to use a Universally Unique Identifier (UUID) for the primary key. The Directus relational architecture supports this type of relationship, but there is no dedicated M2X interface yet.

This type of relationship goes by many different names, and is often referred to by its specific purpose. Some names include: matrix field, replicator, M2MM, M2X, M2N, etc.

![M2M](../img/m2mm.png)

## Translations

The translation interface is a standard O2M relation, but it expects a specific data model to ensure things work properly. Below are the basic collections and fields this interface uses.

### Languages Collection

This is the collection that contains all of the languages your project uses. In this example we'll name it `languages` and make it hidden since this content will be accessed through the parent collection. It requires at least these two fields:

* `code` — This is the primary key. We recommend setting this to a string so it can store the country or locale code. eg: `en` or `en-US`
* `name` — This is the human-readable name shown in the App

:::tip
While it is most common to suport one global set of languages per project, you _could_ create multiple language collections to support different locales throughout your project.
:::

### Translation Collections

Every parent collection (eg: `articles`) contains all language-agnostic fields, such as: _Publish Date_, _Author_, and a _Featured Toggle_. But we also need to create a related collection (eg: `article_translations`) with any fields that will be translated, such as the _Title_ and _Body_. Let's go over the required fields in these translation collections.

* Parent Foreign Key — This is the field that stores the parent item's primary key. So in our example we would add an `article` field to store the article's ID. This is a utility field so typically you will want to enable "Hidden On Detail" so it doesn't appear.
* Language Foreign Key — This is the field that stores the language code. We recommend calling this field `language`. This is a utility field so typically you will want to enable "Hidden On Detail" so it doesn't appear.
* Translated Fields — You can add any number of other fields, each will be translated within the interface.

### Setup

These setup instructions are specific to the _Articles_ example above. It assumes you already have setup these collections: `articles`, `article_translations`, `languages`.

::: v-pre
1. Go to **Settings > Collections & Fields > Articles**
2. Click **New Field**
3. Interface: Choose **Translation**
4. Schema: **Name** your field (we're using `translations`)
5. Relation: Select **Article Translations** as the Related Collection and **Article** as the Related Field
    * The `article_translations.article` field was created during _Translation Collections_ setup above
12. Options: **Languages Collection** is the collection created during _Translations_ setup above (we're using `languages`)
    * **Language Primary Key Field** the Language Foreign Key field created during _Translation Collections_ setup above (we're using `language`)
:::