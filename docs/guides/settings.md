# Settings

> Restricted to members of the administrator role, Settings is where you create the data model, choose interfaces, define permissions, and configure the Directus App and API.

## Global Settings

These are settings that apply to the entire project environment. They are stored as key-value-pairs within `directus_settings`.

Key               | Description
----------------- | ---------------------------------------------------------------
`project_name`    | The title of the project
`project_url`     | The URL of the API's project
`app_url`         | URL of the Project's application
`auto_sign_out`   | The number of seconds until inactive users will be automatically logged out of the application. (auth token expiration)
`default_limit`   | Number of items per request
`logo`            | If you would like to use your own logo you can upload it here. 200px by 60px, PNG or SVG, with a white foreground and transparent background
`sort_null_last`  | Set the null values at last when sorting. Default `1`.
`file_naming`     | Naming convention for uploaded files. `uuid` (default, universally unique identifier), `id` (`directus_files.id` left-padded with `0`), or the original name (sanitized: spaces become underscores, leading `.` becomes `dot-`, incremented as needed for uniqueness)
`youtube_api_key` | Youtube API key used by to fetch video information when upload a youtube link
`thumbnail_not_found_location` | This image will be used when trying to generate a thumbnail with invalid options or an error happens on the server trying to create the image) | Returns 404
`thumbnail_dimensions`      | Comma separate value of dimensions in [width]x[height] format | 200x200
`thumbnail_quality_tags`    | Key-Value json string of qualities tagged with a name. Ex: `{"best": 100}`. Ranging from 0 to 100. 0 = Worst quality and smaller file size to 100 best quality biggest file size. | `{"poor": 25, "good": 50, "better":  75, "best": 100}`
`thumbnail_actions`         | **WIP**; List options to perform different thumbnail generation actions. | `contain` and `crop`
`thumbnail_cache_ttl`       | Cache time to live in seconds. It sets HTTP `max-age` and `Expires` datetime. Default: `86400` seconds = 1 day
`trusted_proxies` | Trusted proxies IP address. By default all are trusted

::: tip UUID
The `uuid` file naming uses UUID v5, and `6ba7b810-9dad-11d1-80b4-00c04fd430c8` as the namespace DNS. A constant value defined in [ramsey/uuid](https://github.com/ramsey/uuid/blob/5cadea8447ea1734b66e402aeb1a1739957d59f6/src/Uuid.php#L44) package.
:::

::: tip Data Model
This data is structured quite differently than other browse/detail pages. Learn more at: [Global Settings Data Model](/advanced/app/global-settings-data-model.md)
:::

## Collections and Fields

## Roles and Permissions

## Update Database

## Interfaces

## About Directus

## Activity Log

## Report Issue

## Request Feature

## Connection

## Server Details

## Versions and Updates