# Collections

> A Collection is a grouping of similar Items. Each collection represents a table in your database.

## Creating Collections

To create a collection, head over to the _Collections & Fields_ page in the _Admin Settings_. From here, click the "New" button ("+") in the top right and enter a new for your collection. This is the technical name used in the database and API. After the collection has been created you're taken to the settings page for this new collection. From here you can [setup the fields](./fields.md) and configure the collection's settings:

### Note

The collection's note field is for internal use only. It helps your administrators understand the purpose of each collection.

### Hidden

Some helper collections are not used directly (eg: junctions) and can be globally hidden. As the name implies, this will only _hide_ the collections. It doesn't restrict access to its data. In order to restrict access to this collection, you can use [Permissions](./permissions.md).

### Single

In certain schema architectures, you may find it helpful to have a collection that can only contain one item. For example, the "About" or "Settings" of your project might be managed within the fields of a single item (also known as a "singleton"). When enabled, clicking the collection in the navigation will open the Item Detail page directly, skipping the Items Browse page.

## Managing Collections

Collections added through Directus are automatically managed, however collections added directly to the database are unmanaged by default. This avoids issues with dynamically created temporary tables or any tables outside the scope of your project. Directus completely ignores any unmanaged collections.

## Deleting Collections

To destroy a collection and all of its data you can click the Delete Button ("×") in the header of the collection detail page. You will be asked only once to confirm this permanent action.

::: warning
It is possible to irreverisbly delete massive amounts of data with this feature. Proceed with extreme caution.
:::