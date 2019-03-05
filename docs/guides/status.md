# Status

> The Status interface adds soft-delete and workflow options to its parent collection. Let's take a look at how to properly configure it to take full advantage of its power and flexibility.

## Status Mapping

There are three status options added by default, however you can add as many as you'd like. Each option has paramenters that define how it will look and work.

Option              | Description
------------------- | -----------------------------------
`key`               | String (Numbers can be used as strings). Each option object is defined by a key, this key is the value that is saved into the database
`name`              | String. The name presented to the user in the App
`text_color`        | Directus Color Name. The text color of the badge on the browse items page
`background_color`  | Directus Color Name. The background color of the badge (or dot if using the Simple Badge option)
`browse_badge`      | Boolean. Whether to show the badge on the browse items page or not
`soft_delete`       | Boolean. If true, items will not be returned by default in the App or API. Only Admin users have access to soft-deleted items

### Example

```json
"published": {
  "name": "Published",
  "text_color": "white",
  "background_color": "accent",
  "browse_badge": false,
  "soft_delete": false
},
"draft": {
  "name": "Draft",
  "text_color": "white",
  "background_color": "blue-grey-200",
  "browse_badge": true,
  "soft_delete": false
},
"deleted": {
  "name": "Deleted",
  "text_color": "white",
  "background_color": "red",
  "browse_badge": true,
  "soft_delete": true
}
```

## Soft Delete

As mentioned above, Soft Delete is meant to _feel_ like an item has been deleted without permanently removing it from the database. They are hidden from both the App and API responses unless explicitely requested by an Admin [using the `status` parameter](/api/reference.md#status). Non-admin users do not have access to soft-deleted items.

## Workflow

The status interface also enables extended permission options that allow [setting permissions based on an item's status](/guides/permissions.md#status-level).

## Custom Status Interfaces

The core status interface should work for 90% of use-cases, but you can still take advantage of the functionality with different styling or interactions. To do this you would [create a custom interface](/extensions/interfaces.md) that uses the `status` [field type](/guides/field-types.md).

## Soft-Delete Flow

When soft-deleting an item, the API does the following:

1. Check if the collection has a status field
2. Check if the delta data has the status field (_Meaning the status was changed_)
3. Look for all status values with `soft_delete = true`
4. Checks if the new status value (_from delta data_) is one of status values from Step 3
5. Sets `action` to `SOFT_DELETE`
