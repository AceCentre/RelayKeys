# Global Settings Inconsistency

The global settings page within the App works a bit different from the other detail pages. The problem with global settings is that there can be a potentially infinite number of fields (1 per setting) with only one row per setting (there can only be one value per field).

This means we either have to:

* Create a table with a very large number of columns and enforce the fact that there is only one row, or:
* Create a table where the rows are treaded _as if they were columns_, where the columns are treated as key-value:

#### First option:

| id | cms_user_auto_sign_out | project_name | project_url          | rows_per_page | thumbnail_quality |
|----|------------------------|--------------|----------------------|---------------|-------------------|
| 1  | 60                     | Directus 7   | demo.getdirectus.com | 200           | low               |

#### Second option:

| id | key                    | value                |
|----|------------------------|----------------------|
| 1  | cms_user_auto_sign_out | 60                   |
| 2  | project_name           | Directus 7           |
| 3  | project_url            | demo.getdirectus.com |
| 4  | rows_per_page          | 200                  |
| 5  | thumbnail_quality      | low                  |

We felt the second is cleaner and is easier to update and extend with new options without having to update the database schema.

However, this structure introduces the problem where the edit view that is being used to edit the values of a single row now expects the wrong data. Instead of dealing with individual rows, the page should deal with the whole table at once. This is the main reason behind the big differences between the "regular" edit view (/routes/Edit.vue) and the global settings view (/routes/SettingsGlobal.vue). The global settings view "mangles" the settings table to work with the EditForm component (/containers/EditForm.vue).