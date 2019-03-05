---
sidebarDepth: 2
---

# API Reference

## Introduction

The Directus API is a quick and easy way to add a RESTful API layer to a new or existing SQL database. It perfectly mirrors the database architecture which allows for flexible content modeling and dynamic endpoints even when changing the schema or data directly. Below is a comprehensive reference of each endpoint and parameter alongside helpful examples that showcase typical request and response formats.

[Get the latest version of the Directus API here](https://github.com/directus/api/releases)

### Versioning

The Directus API uses [SemVer](https://semver.org/) for version labeling within the repo and for files which mention a specific version (eg: `package.json`). The API will _not_ include the version in the URL because the API is "versionless". Being versionless means that existing API behavior will not be removed or changed, only new features and enhancements will be added. Therefore, no breaking changes will ever be introduced and you can safely keep your APIs up-to-date.

### Project Prefix

All endpoints are prefixed with a project key based on the configuration file name. The API will attempt to find a configuration file that matches the provided project key and use its settings. The underscore (`_`) is reserved as the _default_ project key.

Below are few examples of API requests when your API is located in the root directory:

```
# API
https://example.com/server/ping

# Default Project — uses the default config file: api.php
https://example.com/_/collections

# Custom Project — uses "prod" config file: api.prod.php
https://example.com/prod/collections
```

::: tip App Location
For the combined build the Directus App would be located at: `https://example.com/admin`
:::

::: tip Project Config File
The naming format of the configuration file is `api.<project-key>.php`
:::

::: warning Default Config File
A default API project (`api.php`) is required for the API to function properly.
:::

### Response Format

All output will adhere to the same general JSON structure:

```json
{
    "error": {
        "code": [Number],
        "message": [String]
    },
    "data": [Object | Array],
    "meta": [Object]
}
```

### HTTP Status Codes

The API uses HTTP status codes in addition to the message value. Everything in the 200 range is a valid response.

| Code   | Description           |
| ------ | --------------------- |
| `200`  | OK                    |
| `201`  | Created               |
| `204`  | No Content            |
| `400`  | Bad Request           |
| `401`  | Unauthorized          |
| `403`  | Forbidden             |
| `404`  | Not Found             |
| `409`  | Conflict              |
| `422`  | Unprocessable Entity  |
| `500`  | Internal Server Error |
| `503`  | Service Unavailable   |

### Error Codes

The API uses numeric codes to avoid the need for translated error messages based on locale. The `error` property is only present when an error has occurred.

#### General Error Codes

- `0000` - Internal Error (500)
- `0001` - Not Found (404)
- `0002` - Bad Request (400)
- `0003` - Unauthorized (401)
- `0004` - Invalid Request (400) (_Validation_)
- `0005` - Endpoint Not Found (404)
- `0006` - Method Not Allowed (405)
- `0007` - Too Many Requests (429)
- `0008` - API Project Configuration Not Found (404)
- `0009` - Failed Generating SQL Query (500)
- `0010` - Forbidden (403)
- `0011` - Failed to Connect to the Database (500)
- `0012` - Unprocessable Entity (422)
- `0013` - Invalid or Empty Payload (400)
- `0014` - Default Project Not Configured Properly (503)
- `0015` - Batch Upload Not Allowed (400)
- `0016` - Invalid Filesystem Path (500)
- `0017` - Invalid Configuration Path (422)
- `0018` - Project Name Already Exists (409)
- `0018` - Unauthorized Location Access (401)
- `0019` - Installation Invalid database information (400)
- `0020` - Missing Storage Configuration (500)

#### Authentication Error Codes

- `0100` - Invalid Credentials (404)
- `0101` - Invalid Token (401)
- `0102` - Expired Token (401)
- `0103` - Inactive User (401)
- `0104` - Invalid Reset Password Token (401)
- `0105` - Expired Reset Password Token (401)
- `0106` - User Not Found (404)
- `0107` - User with Provided Email Not Found (404)
- `0108` - User Not Authenticated (401)

#### Items Error Codes

- `0200` - Collection Not Found (404)
- `0201` - Not Allow Direct Access To System Table (401)
- `0202` - Field Not Found (404)
- `0203` - Item Not Found (404)
- `0204` - Duplicate Item (409)
- `0205` - Collection Not Managed by Directus
- `0206` - Field Not Managed by Directus
- `0207` - Revision Not Found (404)
- `0208` - Revision Has Invalid Delta
- `0209` - Field Invalid (400) - _A field that doesn't exist for an action such as filtering and sorting_
- `0210` - Can Not Create Comment for Item
- `0211` - Can Not Update Comment for Item
- `0212` - Can Not Delete Comment from Item
- `0213` - Field does not allow object or array as value (422)
- `0214` - Unknown Filter (422)
- `0215` - Unable to access data from a related collection (403)
- `0216` - Delete/Disable last admin is forbidden (403)

#### Collections Error Codes

- `0300` - Reading Items Denied (403)
- `0301` - Creating Items Denied (403)
- `0302` - Updating Items Denied (403)
- `0303` - Deleting Items Denied (403)
- `0304` - Reading Field Denied (403)
- `0305` - Updating Field Denied (403)
- `0306` - Altering Collection Denied (403)
- `0307` - Collection Already Exists (422)
- `0308` - Field Already Exists (422)
- `0309` - Unable to Find Items Owned by User (403)

#### Schema Error Codes

- `0400` - Unknown Error (500)
- `0401` - Unknown Data Type (400)
- `0402` - Field Type Missing Length (422)
- `0403` - Field Type Do Not Support Length (422)

#### Mail Error Codes

- `0500` - Mailer Transport Not Found (500)
- `0501` - Invalid Transport Option (500)
- `0502` - Invalid Transport Instance (500)

#### Filesystem Error Codes

- `0600` - Unknown Error (500)
- `0601` - Uploaded File Exceeds Server's Max Upload Size (500)
- `0602` - Uploaded File Exceeds Client's Max Upload Size (500)
- `0603` - File Only Partially Uploaded (500)
- `0604` - No File Uploaded (500)
- `0605` - _Not yet defined_
- `0606` - Missing Temporary Upload Directory (500)
- `0607` - Failed to Write File to Disk (500)
- `0608` - File Upload Stopped by PHP Extension (500)

#### Utils Error Codes

- `1000` - Hasher Not Found (400)

### Validation

The API performs two types of validation on submitted data:

*   **Data Type** – The API checks the submitted value's type against the Directus or database's field type. For example, a String submitted for an INT field will result in an error.
*   **RegEx** – The API checks the submitted value against its column's `directus_fields.validation` PCRE RegEx pattern (must include delimiters). If the value doesn't match then an error will be returned. Read more about [PCRE patterns](http://php.net/manual/en/pcre.pattern.php) and [delimiters](http://php.net/manual/en/regexp.reference.delimiters.php).

## Authentication

Most endpoints are checked against permissions. If a user is not authenticated or isn’t allowed to access certain endpoints then the API will respond with either a `401 Unauthorized` or a `403 Forbidden` respectively. In addition to these status codes, the API returns a specific reason in the `error.message` field.

### Tokens

To gain access to protected data, you must include an access token with every request. There are two types of tokens.

#### JWT Access Tokens

These tokens are generated upon the user's request and follow the [JWT spec](https://jwt.io).

The JWT token payload contains the user ID, type of token (`auth`), and an expiration date, which is signed with a secret key using the `HS256` hashing algorithm. You can generate one of these tokens using the _Get Auth Token_ below.

#### Static Tokens

The JWT access tokens are the safest way to authenticate into Directus. However, the tokens expire really quickly and you need to login using a users credentials to retrieve it. This is not the most convenient when using Directus on the server side.

You can assign a static token to any user by adding a value to the `token` column in the `directus_users` table in the database directly. As of right now, it's not (yet) possible to set this token from the admin application, as it's rather easy to create a huge security leak for unexperienced users.

The token will never expire and should be considered top secret.

::: danger
This token doesn't expire and doesn't auto refresh. Only use this feature if you know what you're doing.
:::

#### Sending the token

There are several ways to include the access token in a request:

##### 1. Bearer Token in Authorization Header

```
curl -H "Authorization: Bearer Py8Rumu.LD7HE5j.uFrOR5" https://example.com/api/
curl -H "Authorization: Bearer staticToken" https://example.com/api/
```

::: warning NOTE
For security reasons certain Apache installations hide the Authorization header to prevent other scripts from seeing the credentials used to access the server. Make sure your Apache is passing the `Authentication` header. [Read more](https://httpd.apache.org/docs/2.4/en/mod/core.html#cgipassauth)
:::

##### 2. HTTP Basic Auth

```
curl -u Py8Ru.muLD7HE.5juFrOR5: https://example.com/api/
curl -u staticToken: https://example.com/api/
```

Notice that the token is `Py8Ru.muLD7HE.5juFrOR5` and has a colon `:` at the end. Using Basic auth, the auth user is the token and the auth password should be either blank or the same token.

##### 3. Query Parameter

```
curl https://example.com/api/?access_token=Py8RumuLD.7HE5j.uFrOR5
curl https://example.com/api/?access_token=staticToken
```

### Get Auth Token

Gets a token after validating the Directus user's credentials.

```http
POST /[project]/auth/authenticate
```

#### Body

The users credentials.

```json
{
    "email": "rijk@directus.io",
    "password": "supergeheimwachtwoord"
}
```

::: warning
The access token that is returned through this endpoint must be used with any subsequent requests except for endpoints that don’t require auth.
:::

#### Protected Endpoints

| Endpoint                         | Protected
| -------------------------------- | -----------------------
| `/[project]/`                    | **Yes**
| `/[project]/activity`            | **Yes**
| `/[project]/auth`                | No
| `/[project]/collections`         | **Yes**
| `/[project]/collection_presets`  | **Yes**
| `/[project]/custom`              | No
| `/[project]/fields`              | **Yes**
| `/[project]/files`               | **Yes**
| `/[project]/items`               | **Yes**
| `/[project]/interfaces`          | **Yes**
| `/[project]/mail`                | **Yes**
| `/[project]/pages`               | **Yes**
| `/[project]/permissions`         | **Yes**
| `/[project]/relations`           | **Yes**
| `/[project]/revisions`           | **Yes**
| `/[project]/roles`               | **Yes**
| `/[project]/scim/v2`             | **Yes**
| `/[project]/settings`            | **Yes**
| `/[project]/users`               | **Yes**
| `/[project]/utils`               | **Yes**
| `/`                              | **Yes**
| `/projects`                      | No
| `/interfaces`                    | **Yes**
| `/layouts`                       | **Yes**
| `/pages`                         | **Yes**
| `/server/ping`                   | No
| `/types`                         | **Yes**

The proctected endpoints that doesn't starts with `/[project]`, requires the user to send the project name via HTTP header or query string when using static tokens. JWT tokens already has this information in their payloads.

#### Project via Query String

```
curl https://example.com/api/types?access_token=staticToken&project=_
```

#### Project via Header

curl -H "Authorization: Bearer staticToken" -H "X-Directus-Project: _" https://example.com/api/

### Refresh Auth Token

Gets a new fresh token using a valid JWT auth token.

```http
POST /[project]/auth/refresh
```

#### Body

A valid token

```json
{
    "token": "123abc456def"
}
```

::: warning
The access token that is returned through this endpoint must be used with any subsequent requests except for endpoints that don’t require authentication.
:::

### Password Reset Request

The API will send an email to the requested user’s email containing a link with a short-lived reset token link. This reset token can be used to finish the password reset flow.

The reset token is a JWT token that includes the user ID, email, type (`reset_password`), and expiration time.

```http
POST /[project]/auth/password/request
```

#### Body

The user's email address and the app URL from which the reset is requested.

```json
{
    "email": "rijk@directus.io"
}
```

### Password Reset

The API checks the validity of the reset token, that it hasn't expired, and that the email address contained in the token payload matches one in the database. It uses a GET request so users can access it from links within their email clients. This endpoint generates a random password for the user and sends it to their email address.

```http
GET /[project]/auth/password/reset/[reset-token]
```

### SSO

Directus supports modular Single Sign-On (SSO) authentication services, such as Google and Facebook.

#### Get SSO Services

A list of third-party SSO authentication services available for this project.

```http
GET /[project]/auth/sso
```

#### Authorization Redirect

Automatically redirects to the authorization url if the origin host is allowed by the API, otherwise it will return the authorization url.

```http
GET /[project]/auth/sso/[provider]
```

#### OAuth Authentication

When the server has authorized the user after being authenticated, it returns an `oauth_token` and `oauth_verifier` (version 1.0) or `code` (version 2.0).

```http
POST /[project]/auth/sso/[provider]
```

::: warning
This endpoint is only useful when the callback is not handled by the API. See: /[project]/auth/sso/[provider]/callback.
:::

##### Body

The user's email address and the app URL from which the reset is requested.

_OAuth 1.0_

```json
{
    "oauth_token": "[oauth-token]",
    "oauth_verifier": "[oauth-verifier]"
}
```

_Or, for OAuth 2.0:_

```json
{
    "code": "[verification-code]"
}
```

#### Callback

Set this URL as the callback for the Single Sign-On (SSO) OAuth service and it will return a "request token" that the client can use to request the access token.

```http
GET /[project]/auth/sso/[provider]/callback
```

#### Get Access Token

Using the request token that was returned by the `/[project]/auth/sso/[provider]/callback` endpoint to get the access token.

```http
POST /[project]/auth/sso/access_token
```

##### Body

```json
{
    "request_token": "<request-token>"
}
```

## Query Parameters

The API has a set of query parameters that can be used for specific actions, such as: filtering, sorting, limiting, and choosing fields. These supported query parameters are listed below:

| Name          | Description                                                                |
| ------------- | -------------------------------------------------------------------------- |
| `meta`        | Include metadata related to the result
| `fields`      | Include only specific fields in the result
| `limit`       | The maximum number of items in the result
| `offset`      | The results offset, in combination with `limit`
| `single`      | Returns the first item
| `sort`        | Sorting the results by one or multiple fields
| `status`      | Filter items by the provided statuses
| `filter`      | Search for items that matches the filters
| `lang`        | Include translation information
| `q`           | Search for items that matches the given string in any of their fields*
| `groups`      | Groups the items by one or more fields
| `activity_skip` | Disable activity logging for the request
| `comment`     | An activity message to explain the reason of an action.

### Metadata

The `meta` parameter is a CSV of metadata fields to include. This parameter supports the wildcard (`*`) to return all metadata fields.

#### Options

*   `collection` - The name of the collection
*   `type`
    *   `collection` If it is a collection of items
    *   `item` If it is a single item
*   `result_count` - Number of items returned in this response
*   `total_count` - Total number of items in this collection
*   `status_count` - Number of items per status

```
# Here is an example of all meta data enabled
{
    "collection":"movies",
    "type":"collection",
    "result_count":20,
    "total_count":962,
    "status_count":{
        "deleted":94,
        "draft":90,
        "coming soon":159,
        "published":181
    }
}
```

### Fields

`fields` is a CSV of columns to include in the result. This parameter supports dot notation to request nested relational fields. You can also use a wildcard (`*`) to include all fields at a specific depth.

#### Examples

```
# Get all top-level fields
?fields=*

# Get all top-level fields and all second-level relational fields
?fields=*.*

# Get all top-level fields and second-level relational fields within images
?fields=*,images.*

# Get only the first_name and last_name fields
?fields=first_name,last_name

# Get all top-level and second-level relational fields, and third-level fields within images.thumbnails
?fields=*.*,images.thumbnails.*
```

### Limit

Using `limit` can be set the maximum number of items that will be returned. You can also use `-1` to return all items, bypassing the default limits.

#### Examples

```
# Returns a maximum of 10 items
?limit=10

# Returns an unlimited number of items
?limit=-1
```

::: warning
Fetching unlimited data may result in degraded performance or timeouts, use with caution.
:::

### Offset

Using `offset` the first `offset` number of items can be skipped.

#### Examples

```
# Returns a maximum of 10 items, but skips the first 3 items on the list
?offset=3&limit=10
```

### Single

Using `single` the first element will be returned.

::: tip NOTE
Instead of returning a list, the result data will be a single object representing the first item.
:::

#### Examples

```
# Returns the first item of the result set
?single=1&offset=3&limit=10
```

### Sorting

`sort` is a CSV of fields used to sort the fetched items. Sorting defaults to ascending (ASC) order but a minus sign (`-`) can be used to reverse this to descending (DESC) order. Fields are prioritized by their order in the CSV. You can also use a `?` to sort randomly.

#### Examples

```
# Sorts randomly
?sort=?

# Sorts by name ASC
?sort=name

# Sorts by name ASC, followed by age DESC
?&sort=name,-age

# Sorts by name ASC, followed by age DESC, followed by random sorting
?sort=name,-age,?
```

### Status

This parameter is useful for filtering items by their status value. It is only used when the collection has a field with the `status` type. The value should be a CSV.

By default all statuses are included except those marked as `soft_delete`. To include statuses marked as `soft_delete`, they should be explicitly requested or an asterisk wildcard (`*`) should be used.

Example:

```
/_/items/projects?status=*
/_/items/projects?status=published,under_review,draft
```

### Filtering

Used to search items in a collection that matche the filter's conditions. Filters follow the syntax `filter[<field-name>][<operator>]=<value>`. The `field-name` supports dot-notation to filter on nested relational fields.

#### Filter Operators

| Operator             | Description                            |
| -------------------- | -------------------------------------- |
| `=`, `eq`            | Equal to                               |
| `<>`, `!=`, `neq`    | Not equal to                           |
| `<`, `lt`            | Less than                              |
| `<=`, `lte`          | Less than or equal to                  |
| `>`, `gt`            | Greater than                           |
| `>=`, `gte`          | Greater than or equal to               |
| `in`                 | Exists in one of the values            |
| `nin`                | Not in one of the values               |
| `null`               | It is null                             |
| `nnull`              | It is not null                         |
| `contains`, `like`   | Contains the substring                 |
| `ncontains`, `nlike` | Doesn't contain the substring          |
| `rlike`              | Contains a substring using a wildcard  |
| `nrlike`             | Not contains a substring using a wildcard |
| `between`            | The value is between two values        |
| `nbetween`           | The value is not between two values    |
| `empty`              | The value is empty (null or falsy)     |
| `nempty`             | The value is not empty (null or falsy) |
| `all`                | Contains all given related item's IDs  |
| `has`                | Has one or more related items's IDs    |

##### Filter: Raw Like

The wildcards character for `rlike` and `nrlike` are `%` (percentage) and `_` (underscore).

> From MySQL Docs: https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like
> % matches any number of characters, even zero characters.
> _ matches exactly one character.
>
>`JOHN%` will return matches `John`, `Johnson`, `Johnny`, `Johnathan`, etc. \
>`JO%N%` will return the above matches, as well as `Jon`, `Jonny`, `Joan`, `Joanne`, `Jones`, etc. \
>`J_N%` will return `Janice`, `Jane`, `Jones`, `Jinn`, `Jennifer`, `Junior`, etc. \
>`J_N__` will return `Jonas`, `Jenny`, `Janie`, `Jones`, etc.

##### Filter: Relational

You can use dot notation on relational field. Using the same format: `filter[<field-name>][<operator>]=<value>` with the only difference `<field-name>` can reference a field from the related collection.

If you have a `projects` collection with a field named `author` that's related to another collection named `users` you can reference any `users` field using dot notation; Example: `author.<any-users-field>`.

The example below uses the `rlike` filter to get all projects that belongs to users that has a `@directus.io` domain email. In other words ends with `@directus.io`

```
GET /items/projects?filter[author.email][rlike]=%@directus.io
```

::: tip
Make sure the field is a relational field before using the dot-notation, otherwise the API will return a error saying the field cannot be found.
:::

You can reference as many field as possible, as long as they are all relational field, except the last one, it could be either relational or non-relational.

```
GET /items/users?filter[comments.thread.title][like]=Directus
```

In the example above it will returns all users that have comments in a thread that has `Directus` in its title.

There's two filter `has` and `all` that only works on `O2M`-type fields, any other type of fields used will throw an error saying the field cannot be found.

The `all` filter will returns items that contains all IDs passed.

```
GET /items/projects?filter[contributors][all]=1,2,3
```

The example above will return all projects that have the user with ID 1, 2, and 3 as collaborator.

Using `has` will return items that has at least the mininum number given as related items. 

Example of requesting projects with at least one contributor:

```
GET /items/projects?filter[contributors][has]=1
```

Example of requesting projects with at least three contributors:

```
GET /items/projects?filter[contributors][has]=3
```

#### AND vs OR

By default, all chained filters are treated as ANDs, which means _all_ conditions must match. To create an OR combination, you can add the `logical` operator, as shown below:

```
GET /items/projects?filter[category][eq]=development&filter[title][logical]=or&filter[title][like]=design
```

::: tip
In many cases, it makes more sense to use the `in` operator instead of going with the logical-or. For example, the above example can be rewritten as

```
GET /items/projects?filter[category][in]=development,design
```

:::

#### Filtering by Dates and Times

The format for date is `YYYY-MM-DD` and for datetime is `YYYY-MM-DD HH:MM:SS`. This formats translate to `2018-08-29 14:51:22`.

- Year in `4` digits
- Months, days, minutes and seconds in two digits, adding leading zero padding when it's a one digit month
- Hour in 24 hour format

```
# Equals to
GET /items/comments?filter[datetime]=2018-05-21 15:48:03

# Greater than
GET /items/comments?filter[datetime][gt]=2018-05-21 15:48:03

# Greater than or equal to
GET /items/comments?filter[datetime][gte]=2018-05-21 15:48:03

# Less than
GET /items/comments?filter[datetime][lt]=2018-05-21 15:48:03

# Less than or equal to
GET /items/comments?filter[datetime][lte]=2018-05-21 15:48:03

# Between two date
GET /items/comments?filter[datetime][between]=2018-05-21 15:48:03,2018-05-21 15:49:03
```

For `date` and `datetime` type, `now` can be used as value for "currrent server time".

```
# Equals to
GET /items/comments?filter[datetime]=now

# Greater than
GET /items/comments?filter[datetime][gt]=now

# Between two date
GET /items/comments?filter[datetime][between]=2018-05-21 15:48:03,now
```

When the field belongs to a Directus collection, `now` is converted to a UTC date/datime.

### Language

The `lang` parameter is a CSV of languages that should be returned with the response. This parameter can only be used when a Translation field has been included in the collection. This parameter supports the wildcard (`*`) to return all language translations.

In order to receive the translated values you **must** specify the [`fields`](#fields) parameter (e.g. `lang=*&fields=*.*` or `lang=en&fields=article_translations.*`).

### Search Query

The `q` parameter allows you to perform a search on all `string` and `number` type fields within a collection. It's an easy way to search for an item without creating complex field filters – though it is far less optimized. It only searches the root item's fields, related item fields are not included.

### Groups

The `groups` parameter allows grouping the result by one or more fields.

This parameter is a raw parameter, it adds all the fields you pass to the [`GROUP BY`](https://dev.mysql.com/doc/refman/5.6/en/group-by-modifiers.html) in SQL. This can result in SQL errors when the [`ONLY_FULL_GROUP_BY`](https://dev.mysql.com/doc/refman/5.6/en/sql-mode.html#sqlmode_only_full_group_by) mode is enabled in MySQL, and there's columns in `ORDER BY` that doesn't exists in the `GROUP BY`.

#### Examples

Users table:

| name      | country  |
| --------- | -------- |
| John      | US       |
| Joseph    | GB       |
| John      | GB       |

Grouping the Users table by `name` will result in the following:

```
groups=name
```

```json
{
  "data": [
    {
      "name": "John"
    },
    {
      "name": "Joseph"
    }
  ]
}
```

All items that has the same fields in `groups` will be merged together.

Grouping by both `name` and `country` will result on all items to be returned, because none of them match another record with the same `name` and `country` combined.

### Skip Activity Logging

The `activity_skip` parameter prevent the activity logging to be saved in the `directus_actity` table. `activity_skip=1` means to ignore the logging any other value means record the activity.

#### Examples

If there's collection used to logs a project specific activity and that happens frequently and you want to avoid this activity from filling the `directus_activity` collection, you use the `activity_skip=1` query parameter to skip saving this activity.

```http
POST /_/items/doors_access_logs?activity_skip=1
```

```json
{
  "door": "D190",
  "user": 1,
  "datetime": "2018-12-19 14:58:21"
}
```

### Activity Comment

The `comment` parameter is used to add a message to explain why the request is being made. This value is stored in the activity record. This can be either optional, required or forbidden, based on permissions.

This parameter will not work when `activity_skip` is enabled.

#### Examples

If you want to keep track of the reason why a project from the `projects` collection went from `active` to `cancelled`, you can add a comment explaning the reason.

```http
PATCH /_/items/projects/1?comment=Client business closed doors
```

```json
{
  "status": "cancelled"
}
```

## Items

Items are essentially individual database records which each contain one or more fields (database columns). Each item belongs to a specific collection (database table) and is identified by the value of its primary key field. In this section we describe the different ways you can manage items.

This endpoint is dedicated to all user-defined collections only. Accessing system tables is forbidden. See [Systems Endpoints](#system) for more information.

### Create Items

Creates one or more items in a given collection.

```http
POST /[project]/items/[collection-name]
```

#### Body

A single item or an array of multiple items to be created. Field keys must match the collection's column names.

```json
{
    "title": "Project One",
    "category": "Design"
}
```

_Or, for batch creating multiple items:_

```json
[
    {
        "title": "Project One",
        "category": "Design"
    },
    {
        "title": "Project Two",
        "category": "Development"
    }
]
```

::: tip
The API may not return any data for successful requests if the user doesn't have adequate read permission. Instead, `204 NO CONTENT` is returned.
:::

### Get Item

Get a single item from a given collection using its primary key (PK).

```http
GET /[project]/items/[collection-name]/[pk]
```

#### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |
| `status`      | [Read More](#status)       |
| `lang`        | [Read More](#language)     |

#### Examples

*   Return the project item with an primary key of `1`
    ```bash
    curl -u <token>: https://api.directus.io/_/items/projects/1
    ```

### Get Multiple Items

Get multiple items from a given collection using their primary keys (PK).

```http
GET /[project]/items/[collection-name]/[pk1],[pk2],[pk3]
```

#### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |
| `status`      | [Read More](#status)       |
| `lang`        | [Read More](#language)     |

#### Examples

*   Return project items with primary keys of `1`, `3`, `11`
    ```bash
    curl -u <token>: https://api.directus.io/_/items/projects/1,3,11
    ```

### Get Items

Get an array of items within a given collection.

```http
GET /[project]/items/[collection-name]
```

#### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `limit`       | [Read More](#limit)        |
| `meta`        | [Read More](#meta)         |
| `offset`      | [Read More](#offset)       |
| `single`      | [Read More](#single)       |
| `sort`        | [Read More](#sort)         |
| `status`      | [Read More](#status)       |
| `filter`      | [Read More](#filter)       |
| `lang`        | [Read More](#language)     |
| `q`           | [Read More](#search-query) |
| `groups`      | [Read More](#groups)       |

#### Examples

*   Search for all projects in the `design` category
    ```bash
    curl -u [token]: -g https://api.directus.io/_/items/projects?filter[category][eq]=design
    ```

### Get Item Revision

Get a specific revision of an item. This endpoint uses a zero-based offset to select a revision, where `0` is the creation revision. Negative offsets are allowed, and select as if `0` is the current revision.

```http
GET /[project]/items/[collection-name]/[id]/revisions/[offset]
```

#### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |
| `status`      | [Read More](#status)       |
| `lang`        | [Read More](#language)     |

#### Examples

*   Return the 2nd revision (from creation) for the project item with a primary key of 1
    ```bash
    curl -u <token>: https://api.directus.io/_/items/projects/1/revisions/2
    ```
*   Return the 2nd from current revision for the project item with a primary key of 1
    ```bash
    curl -u <token>: https://api.directus.io/_/items/projects/1/revisions/-2
    ```

### Get Item Revisions

Get an array of revisions from a given item.

```http
GET /[project]/items/[collection-name]/[id]/revisions
```

#### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `limit`       | [Read More](#limit)        |
| `meta`        | [Read More](#meta)         |
| `offset`      | [Read More](#offset)       |
| `single`      | [Read More](#single)       |
| `sort`        | [Read More](#sort)         |
| `status`      | [Read More](#status)       |
| `filter`      | [Read More](#filter)       |
| `lang`        | [Read More](#language)     |
| `q`           | [Read More](#search-query) |
| `groups`      | [Read More](#groups)       |

#### Examples

*   Get all revisions from the project item with a primary key of 1
    ```bash
    curl https://api.directus.io/_/items/projects/1/revisions
    ```

### Update Item

Update or replace a single item from a given collection.

```http
PATCH /[project]/items/[collection-name]/[pk]
```

::: warning

*   **PATCH** partially updates the item with the provided data, any missing data is ignored

:::

#### Body

A single item to be updated. Field keys must match the collection's column names.

#### Examples

*   Return the project item with an primary key of `1`
    ```bash
    curl -u <token>: -d "title=new title" https://api.directus.io/_/items/projects/1
    ```

### Update Items

Update multiple items in a given collection.

```http
PATCH /[project]/items/[collection-name]
PATCH /[project]/items/[collection-name]/[pk1],[pk2],[pk3],...
```

::: warning PATCH

*   **PATCH** partially updates the item with the provided data, any missing data is ignored

:::

::: danger WARNING
Batch updating can quickly overwrite large amounts of data. Please be careful when implementing this request.
:::

#### Body

Update multiple items with the same data: `PATCH /items/projects/1,2`


```json
{
  "title": "Unknown Title"
}
```

Update multiple items, each with its dataset: `PATCH /items/projects`. Each item requires a primary key fields to identify to which item the dataset belongs.


```json
[{
  "id": 1,
  "title": "Unknown Title 1"
}, {
  "id": 2,
  "title": "Unknown Title 2"
}]
```

### Revert Item

Reverts an item to a previous revision state.

```http
PATCH /[project]/items/[collection-name]/[item-pk]/revert/[revision-id]
```

#### Body

There is no need for a body with this request.

#### Examples

*   Revert the project item (PK:`1`) to its previous state in revision (PK:`2`)
    ```bash
    curl -u <token>: https://api.directus.io/_/items/projects/1/revert/2
    ```

### Delete Items

Deletes one or more items from a specific collection. This endpoint also accepts CSV of primary key values, and would then return an array of items.

```http
DELETE /[project]/items/[collection-name]/[pk]
DELETE /[project]/items/[collection-name]/[pk1],[pk2],[pk3],...
```

::: danger WARNING
Batch Delete can quickly destroy large amounts of data. Please be careful when implementing this request.
:::

## System

@TODO These endpoints need the same reference as listed above

All system tables (`directus_*`) are blocked from being used through the regular `/items` endpoint to prevent security leaks or because they require additional processing before sending to the end user. This means that any requests to `/items/directus_*` will always return `401 Unauthorized`.

These system endpoints still follow the same spec as a “regular” `/items/[collection-name]` endpoint but require the additional processing outlined below:

### Activity

#### Activity Actions

| Name           | Description                                                |
| -------------- | ---------------------------------------------------------- |
| `authenticate` | User authenticated using credentials                       |
| `comment`      | Comment was added to an item                               |
| `upload`       | File was created                                           |
| `create`       | Item was created                                           |
| `update`       | Item was updated                                           |
| `delete`       | Item was deleted                                           |
| `soft-delete`  | Item was soft-deleted. Updated to a soft-deleted status    |
| `revert`       | Item was updated using a revision's data                   |

#### Get Activity

Returns a list of activity.

```http
GET /[project]/activity
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `limit`       | [Read More](#limit)        |
| `meta`        | [Read More](#meta)         |
| `offset`      | [Read More](#offset)       |
| `single`      | [Read More](#single)       |
| `sort`        | [Read More](#sort)         |
| `filter`      | [Read More](#filter)       |
| `q`           | [Read More](#search-query) |
| `groups`      | [Read More](#groups)       |

##### Response

```json
{
  "data": [
    {
      "id": 1,
      "action": "authenticate",
      "action_by": 1,
      "action_on": "2018-12-19T14:05:41+00:00",
      "ip": "::1",
      "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15",
      "collection": "directus_users",
      "item": "1",
      "edited_on": null,
      "comment": null,
      "comment_deleted_on": null
    },
    {
      "id": 2,
      "action": "create",
      "action_by": 1,
      "action_on": "2018-12-19T14:06:42+00:00",
      "ip": "::1",
      "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15",
      "collection": "directus_fields",
      "item": "133",
      "edited_on": null,
      "comment": null,
      "comment_deleted_on": null
    }
  ]
}
```

#### Get Activity Event

Get one or more specific activity events.

```http
GET /[project]/activity/[id]
GET /[project]/activity/[id1],[id2],[id3],...
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |
| `status`      | [Read More](#status)       |
| `lang`        | [Read More](#language)     |

##### Response

```json
{
  "data": {
    "id": 1,
    "action": "authenticate",
    "action_by": 1,
    "action_on": "2018-12-19T14:05:41+00:00",
    "ip": "::1",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15",
    "collection": "directus_users",
    "item": "1",
    "edited_on": null,
    "comment": null,
    "comment_deleted_on": null
  }
}
```

#### Create Comment

Create a new comment on an item. Each comment must include the item primary key and its parent collection name.

```http
POST /[project]/activity/comment
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `meta`        | [Read More](#meta)         |

##### Body

A single object representing the new comment.

```json
{
    "collection": "projects",
    "item": 1,
    "comment": "A new comment"
}
```

##### Response

```json
{
  "data": {
    "id": 2,
    "action": "comment",
    "action_by": 1,
    "action_on": "2018-12-19T21:39:41+00:00",
    "ip": "127.0.0.1",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15",
    "collection": "projects",
    "item": "1",
    "edited_on": null,
    "comment": "A new comment",
    "comment_deleted_on": null
  }
}
```

#### Update Comment

Update a comment by its ID.

```http
PATCH /[project]/activity/comment/[id]
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `meta`        | [Read More](#meta)         |

##### Body

A single object representing the new comment. The collection and item fields are not required.

```json
{
    "comment": "An updated comment"
}
```

##### Response

```json
{
  "data": {
    "id": 2,
    "action": "comment",
    "action_by": 1,
    "action_on": "2018-12-19T21:39:41+00:00",
    "ip": "127.0.0.1",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15",
    "collection": "test",
    "item": "1",
    "edited_on": "2018-12-20T02:41:00+00:00",
    "comment": "An updated comment",
    "comment_deleted_on": null
  }
}
```

#### Delete Comment

Delete a comment by its ID.

```http
DELETE /[project]/activity/comment/[id]
```

##### Supported Query Parameters

None.

##### Response

Empty (HTTP 204)

### Collections

These endpoints are used for creating, reading, updating, and deleting collections. Similar to `/fields`, it alters the database schema directly as needed.

#### Create Collection

Creates a new collection.

```http
POST /[project]/collections
```

In the top-level object, the `collection` field is required.

In the `fields` list, `field`, `type`, and `interface` are required.

The `datatype` (database vendor specific) may also be required if the `type` supports different datatypes. For example, the `primary_key` type supports both _string_ and _number_, so it is also required to set the `datatype` to a numeric or string datatype.

When `type` requires a length, such as a string or integer, a `length` attribute is required.

```json
{
    "collection": "projects",
    "managed": true,
    "hidden": false,
    "single": false,
    "translation": null,
    "note": "This collection will store all of our projects",
    "icon": null,
    "fields": [
        {
            "field": "id",
            "type": "integer",
            "datatype": "int",
            "interface": "primary-key",
            "primary_key": true,
            "auto_increment": true,
            "signed": false
        },
        {
            "field": "title",
            "type": "string",
            "datatype": "varchar",
            "interface": "text-input",
            "length": 255,
            "readonly": false,
            "required": true,
            "note": "The project title"
        }
    ]
}
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `meta`        | [Read More](#meta)         |

##### Response

```json
{
  "data": {
    "collection": "projects",
    "managed": true,
    "hidden": false,
    "single": false,
    "icon": null,
    "note": "This collection will store all of our projects",
    "translation": null
  }
}
```

#### Get Collections

Returns a list of all collections in the database.

```http
GET /[project]/collections
```

#### Get Collection

Returns the details of a single collection.

```http
GET /[project]/collections/[name]
```

#### Update Collection

Adds new fields, updates existing fields, and manages the other details of a given collection.

```http
PATCH /[project]/collections/[name]
```

```json
{
    "note": "This collection stores all of our client projects",
    "fields": [
        {
            "field": "title",
            "length": 128
        }
    ]
}
```

::: danger WARNING
Updating field names, can break existing API endpoints and changing field length/type can result in a loss of data. Please be careful when implementing this request.
:::

#### Delete Collection

Permanently deletes a collection information, the table and all its contents.

```http
DELETE /[project]/collections/[name]
```

:::warning
Deleting a collection removes the actual table and any records therein from the database permanently. Please proceed with extreme caution.
:::

### Collection Presets

These endpoints are used for creating, reading, updating, and deleting collection presets.

#### Create Collection Preset

Creates a new collection preset.

```http
POST /[project]/collection_presets
```

#### Get Collection Presets

Returns a list of collection presets.

```http
GET /[project]/collection_presets
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `limit`       | [Read More](#limit)        |
| `meta`        | [Read More](#meta)         |
| `offset`      | [Read More](#offset)       |
| `single`      | [Read More](#single)       |
| `sort`        | [Read More](#sort)         |
| `filter`      | [Read More](#filter)       |
| `q`           | [Read More](#search-query) |
| `groups`      | [Read More](#groups)       |

#### Get Collection Preset

Returns the details of one or more collection presets.

```http
GET /[project]/collection_presets/[id]
GET /[project]/collection_presets/[id1],[id2],[id3],...
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |

#### Update Collection Preset

Updates the details of one or more collection presets.

```http
PATCH /[project]/collection_presets
PATCH /[project]/collection_presets/[id]
PATCH /[project]/collection_presets/[id1],[id2],[id3],...
```

#### Delete Collection Preset

Permanently deletes a collection_presets.

```http
DELETE /[project]/collection_presets/[id]
DELETE /[project]/collection_presets/[id1],[id2],[id3],...
```

::: danger WARNING
Batch Delete can quickly destroy large amounts of data. Please be careful when implementing this request.
:::

### Fields

These endpoints are used for creating, reading, updating, and deleting fields within a collection. It alters the database schema directly as needed.

#### Create Field

Creates a new field in a given collection. When creating a field you must submit the [Directus field type](/guides/field-types.md) (`type`) as well as a database datatype (`datatype`) specific to your SQL vendor.

```http
POST /[project]/fields/[collection]
```

```json
{
  "field": "description",
  "type": "string",
  "datatype": "varchar",
  "interface": "textarea",
  "unique": true,
  "primary_key": false,
  "auto_increment": false,
  "default_value": null,
  "note": null,
  "signed": true,
  "sort": 0,
  "hidden_detail": false,
  "hidden_browse": false,
  "required": false,
  "options": null,
  "locked": false,
  "translation": null,
  "readonly": false,
  "width": 4,
  "validation": null,
  "group": null,
  "length": "255"
}
```

::: warning
You must ensure that the Directus field type, database datatype, and interface all work together. This is easy when done through the App, since options are limited and defaults are provided. When working directly with the API you'll need to check compatibility.

For example, you wouldn't have a `wysiwyg` interface with a `boolean` type save to a `datetime` datatype... that's just crazy.
:::

#### Get Fields

Returns the list of all fields that belongs to a given collection.

```http
GET /[project]/fields/[collection]
```

#### Get Field

Returns the details of a single field.

```http
GET /[project]/fields/[collection]/[field]
```

#### Update Field

Updates the details of a given field.

```http
PATCH /[project]/fields/[collection]/[field]
```

```json
{
  "required": true
}
```

#### Delete Field

Permanently deletes a field and its content.

```http
DELETE /[project]/fields/[collection]
```

:::warning
Deleting a field removes the actual column and any data therein from the database permanently. Please proceed with extreme caution.
:::

### Files

These endpoints are used for uploading, updating, and deleting files and virtual folders.

#### Upload File

Uploads or creates a new file.

```http
POST /[project]/files
```

::: tip NOTE
All uploads except when using URLs requires the `filename` property.
:::

There are different ways to upload a file:

##### Using Base64 Content

Using passing the base64 file contents to the `data` field.

```json
{
  "filename": "image.jpg",
  "data": "<base64-content>"
}
```

##### Using `multipart/form-data` Content Type

Passing the file form-data to the `data` field when making the `multipart/form-data` `POST` request.

This allows for easier uploading of files when using an HTML form element with the `enctype` (encoding type) set to `multipart/form-data`.

##### Using Supported embedded URLs

Directus supports adding embed videos from YouTube and Vimeo to Directus Files using the video URL. Saving an image as its thumbnail.

```json
{
  "data": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

##### Using URLs

```json
{
  "data": "https://example.com/path/to/image.jpg"
}
```

#### Get Files

Returns a list of files.

```http
GET /[project]/files
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `limit`       | [Read More](#limit)        |
| `meta`        | [Read More](#meta)         |
| `offset`      | [Read More](#offset)       |
| `single`      | [Read More](#single)       |
| `sort`        | [Read More](#sort)         |
| `filter`      | [Read More](#filter)       |
| `q`           | [Read More](#search-query) |
| `groups`      | [Read More](#groups)       |

#### Get File

Returns the details of one or more files.

```http
GET /[project]/files/[id]
GET /[project]/files/[id1],[id2],[id3],...
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |

#### Update File

Replaces a file or updates its details.

```http
PATCH /[project]/files/[id]
```

```json
{
  "data": "<base64-content>",
  "description" : "new description"
}
```

#### Update Multiple Files

Replaces several files, or updates their details.

```http
PATCH /[project]/files
PATCH /[project]/files/[id1],[id2],[id3],...
```

##### Different Data

Each file object requires the `id` field to identify which record the new data will belongs to.

```
PATCH /_/files
```

```json
[{
  "id": 1,
  "data": "<base64-content>",
  "description" : "New Description"
}, {
  "id": 2,
  "title" : "New Title"
}]
```

##### Same Data

```
PATCH /_/files/1,2,3
```

```json
{
  "tags": ["marketing", "2017"]
}
```

#### Delete File

Permanently deletes one or more files from the filesystem and database.

```http
DELETE /[project]/files/[id]
DELETE /[project]/files/[id1],[id2],[id3],...
```

::: danger WARNING
Batch Delete can quickly destroy large amounts of data. Please be careful when implementing this request.
:::

#### Get File Revisions

Returns a list of file's revisions.

```http
GET /[project]/files/[id]/revisions
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `limit`       | [Read More](#limit)        |
| `meta`        | [Read More](#meta)         |
| `offset`      | [Read More](#offset)       |
| `single`      | [Read More](#single)       |
| `sort`        | [Read More](#sort)         |
| `q`           | [Read More](#search-query) |
| `groups`      | [Read More](#groups)       |

#### Get File Revision

```http
GET /[project]/files/[id]/revisions/[offset]
```

Returns the revisions of a file using a 0-index based offset.

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |

### Folders

These endpoints are used for creating, reading, updating, and deleting virtual folders.

#### Create Folder

Creates a new virtual folder.

```http
POST /[project]/files/folders
```

```json
{
  "name": "Christmas 2017",
  "parent_folder": null
}
```

#### Get Folders

Returns a list of virtual folders.

```http
GET /[project]/files/folders
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `limit`       | [Read More](#limit)        |
| `meta`        | [Read More](#meta)         |
| `offset`      | [Read More](#offset)       |
| `single`      | [Read More](#single)       |
| `sort`        | [Read More](#sort)         |
| `filter`      | [Read More](#filter)       |
| `q`           | [Read More](#search-query) |
| `groups`      | [Read More](#groups)       |

#### Get Folder

Returns the details of one or more virtual folders.

```http
GET /[project]/files/folders/[id]
GET /[project]/files/folders/[id1],[id2],[id3],...
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |

#### Update Folder

Updates the details of a given virtual folder.

```http
PATCH /[project]/files/folders/[id]
```

```json
{
  "name": "Christmas Photos 2017"
}
```

#### Delete Folder

Permanently deletes one or more virtual folders.

```http
DELETE /[project]/files/[id]
DELETE /[project]/files/[id1],[id2],[id3],...
```

:::warning
This is not a recurrsive delete. As of now, any sub-folders and files are left orphaned in the heirarchy. Be sure to empty a virtual folder before deleting it.
:::

### Permissions

These endpoints are used for creating, reading, updating, and deleting permissions.

#### Create Permission

Creates one or more permissions.

```http
POST /[project]/permissions
```

##### Body

```json
{
  "collection": "projects",
  "role": 3,
  "create": "full",
  "read": "full",
  "update": "mine",
  "delete": "none"
}
```

_Or, for multiple permissions:_

```json
[{
  "collection": "projects",
  "role": 3,
  "create": "full",
  "read": "full",
  "update": "mine",
  "delete": "none"
}, {
  "collection": "projects",
  "role": 4,
  "create": "none",
  "read": "full",
  "update": "none",
  "delete": "none"
}]
```

#### Get Permissions

Returns a list of permissions.

```http
GET /[project]/permissions
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `limit`       | [Read More](#limit)        |
| `meta`        | [Read More](#meta)         |
| `offset`      | [Read More](#offset)       |
| `single`      | [Read More](#single)       |
| `sort`        | [Read More](#sort)         |
| `filter`      | [Read More](#filter)       |
| `q`           | [Read More](#search-query) |
| `groups`      | [Read More](#groups)       |

#### Get Permission

Returns the details of one or more permissions.

```http
GET /[project]/permissions/[id]
GET /[project]/permissions/[id1],[id2],[id3],...
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |

#### Get My Permissions

Returns all permissions belonging to the currently authenticated user.

```http
GET /[project]/permissions/me
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `limit`       | [Read More](#limit)        |
| `meta`        | [Read More](#meta)         |
| `offset`      | [Read More](#offset)       |
| `single`      | [Read More](#single)       |
| `sort`        | [Read More](#sort)         |
| `filter`      | [Read More](#filter)       |
| `q`           | [Read More](#search-query) |
| `groups`      | [Read More](#groups)       |

#### Get My Collection Permissions

Returns a collection's permissions belonging to the currently authenticated user.

```http
GET /[project]/permissions/me/[collection-name]
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |

#### Update Permission

Updates the details of one or more permissions.

```http
PATCH /[project]/permissions
PATCH /[project]/permissions/[id]
PATCH /[project]/permissions/[id1],[id2],[id3],...
```

##### Examples

```http
PATCH /_/permissions/1
```

```json
{
  "create": "none"
}
```

_Or, for multiple permissions with the same data:_

```http
PATCH /_/permissions/1,2,3
```

```json
{
  "create": "none",
  "delete": "none"
}
```

_Or, for multiple permissions with different data:_

```http
PATCH /_/permissions
```

```json
[{
  "id": 1,
  "create": "none",
  "delete": "none"
}, {
  "id": 2,
  "create": "mine",
  "delte": "mine"
}]
```

#### Delete Permission

Permanently deletes one or more permissions.

```http
DELETE /[project]/permissions/[id]
DELETE /[project]/permissions/[id1],[id2],[id3],...
```

::: danger WARNING
Batch Delete can quickly destroy large amounts of data. Please be careful when implementing this request.
:::

### Relations

These endpoints are used for creating, reading, updating, and deleting collection relations.

#### Create Relation

Creates one or more relations.

```http
POST /[project]/relations
```

##### Examples

```json
{
  "collection_many": "projects",
  "field_many": "author",
  "collection_one": "directus_users",
  "field_one": null
}
```

_Or, for multiple relations:_

```json
[
  {
    "collection_many": "projects",
    "field_many": "author",
    "collection_one": "directus_users",
    "field_one": null
  },
  {
    "collection_many": "projects",
    "field_many": "category",
    "collection_one": "categories",
    "field_one": null
  }
]
```

#### Get Relations

```http
GET /[project]/relations
```

Returns the list of relations.

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `limit`       | [Read More](#limit)        |
| `meta`        | [Read More](#meta)         |
| `offset`      | [Read More](#offset)       |
| `single`      | [Read More](#single)       |
| `sort`        | [Read More](#sort)         |
| `filter`      | [Read More](#filter)       |
| `q`           | [Read More](#search-query) |
| `groups`      | [Read More](#groups)       |

#### Get Relation

Returns the details of one or more relations.

```http
GET /[project]/relations/[id]
GET /[project]/relations/[id1],[id2],[id3],...
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |

#### Update Relation

Updates the details of one or more relations.

```http
PATCH /[project]/relations
PATCH /[project]/relations/[id]
PATCH /[project]/relations/[id1],[id2],[id3],...
```

##### Examples

```http
PATCH /_/relations/1
```

```json
{
  "field_one": "projects"
}
```

_Or, for multiple relations with the same data:_

```http
PATCH /_/relations/1,2
```

```json
{
  "field_one": null
}
```

_Or, for multiple relations with different data:_

```http
PATCH /_/relations
```

```json
[{
  "id": 1,
  "field_one": "projects"
}, {
  "id": 2,
  "field_one": "categories"
}]
```

#### Delete Relations

Permanently deletes one or more relations.

```http
DELETE /[project]/relations/[id]
DELETE /[project]/relations/[id1],[id2],[id3],...
```

::: danger WARNING
Batch Delete can quickly destroy large amounts of data. Please be careful when implementing this request.
:::

### Revisions

These endpoints are used for fetching one or more revisions.

#### Get Revisions

Get a list of all revisions.

```http
GET /[project]/revisions
```

#### Get Revisions

Get the details of one or more revisions by their ID.

```http
GET /[project]/revisions/[id]
GET /[project]/revisions/[id1],[id2],[id3],...
```

### Roles

These endpoints are used for creating, reading, updating, and deleting roles.

#### Create Role

Creates one or more roles.

```http
POST /[project]/roles
```

::: warning NOTE
Directus is also compatible with _System for Cross-domain Identity Management_ (SCIM) protocol. All roles have an `external_id` to link each with the external system, these must be unique within Directus. Directus will automatically generate a UUID (v4) if this field is left blank when creating a role.
:::

```json
{
  "name": "Interns"
}
```

_Or, to create multiple at once:_

```json
[
  {
    "name": "Interns"
  },
  {
    "name": "Editors"
  }
]
```

#### Get Roles

Returns a list of roles.

```http
GET /[project]/roles
```

Returns a list of roles and their users

```http
GET /[project]/roles?fields=*,users.user.*
```

#### Get Role

Returns the details of one or more roles.

```http
GET /[project]/roles/[id]
GET /[project]/roles/[id1],[id2],[id3],...
```

#### Update Role

Updates the details of one or more roles.

```http
PATCH /[project]/roles
PATCH /[project]/roles/[id]
PATCH /[project]/roles/[id1],[id2],[id3],...
```

##### Examples

_To update a single role:_

```http
PATCH /_/roles/3
```

###### Body

```json
{
  "description": "new description"
}
```

_Or, to update multiple with the same data:_

```http
PATCH /_/roles/1,2,3
```

###### Body

```json
{
  "ip_whitelist": "10.0.0.1,127.0.0.1"
}
```

_Or, to update multiple with different data:_

```http
PATCH /_/roles
```

###### Body

```json
[{
  "id": 1,
  "ip_whitelist": "10.0.0.1"
}, {
  "id": 2,
  "ip_whitelist": "127.0.0.1"
}]
```

#### Delete Role

Permanently deletes one or more roles.

```http
DELETE /[project]/roles/[id]
DELETE /[project]/roles/[id1],[id2],[id3],...
```

::: danger WARNING
Batch Delete can quickly destroy large amounts of data. Please be careful when implementing this request.
:::

### Settings

These endpoints are used for creating, reading, updating, and deleting the general settings.

#### Create Setting

Creates one or more settings.

```http
POST /[project]/settings
```

#### Get Settings

Returns the list of settings.

```http
GET /[project]/settings
```

#### Get Setting

Returns the details of one or more settings.

```http
GET /[project]/settings/[id]
GET /[project]/settings/[id1],[id2],[id3],...
```

#### Update Setting

Updates the details of one or more settings.

```http
PATCH /[project]/settings
PATCH /[project]/settings/[id]
PATCH /[project]/settings/[id1],[id2],[id3],...
```

#### Delete Setting

Permanently deletes one or more settings.

```http
DELETE /[project]/settings/[id]
DELETE /[project]/settings/[id1],[id2],[id3],...
```

::: danger WARNING
Batch Delete can quickly destroy large amounts of data. Please be careful when implementing this request.
:::

### Users

#### Create User

Creates a new Directus user within this project.

```http
POST /[project]/users
```

##### Body

The email and password for the new user to be created. Any other submitted fields are optional, but field keys must match column names within `directus_users`.

```json
{
    "email": "rijk@directus.io",
    "password": "d1r3ctus"
}
```

#### Get Users

Returns a list of Directus users within this project.

```http
GET /[project]/users
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `limit`       | [Read More](#limit)        |
| `meta`        | [Read More](#meta)         |
| `offset`      | [Read More](#offset)       |
| `single`      | [Read More](#single)       |
| `sort`        | [Read More](#sort)         |
| `status`      | [Read More](#status)       |
| `filter`      | [Read More](#filter)       |
| `lang`        | [Read More](#language)     |
| `q`           | [Read More](#search-query) |
| `groups`      | [Read More](#groups)       |

##### Examples

Get a list of Directus users.

```bash
curl -u <token>: https://api.directus.io/_/users
```

#### Get User

Gets a single user from within this project.

```http
GET /[project]/users/[pk]
GET /[project]/users/[pk],[pk],[pk]
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |
| `status`      | [Read More](#status)       |

##### Examples

Returns the user with an ID of `1`.

```bash
curl -u <token>: https://api.directus.io/_/users/1
```

#### Get Currently Logged-In User

Gets a single user from within this project based on the token that's used to make the request.

```http
GET /[project]/users/me
```

##### Supported Query Parameters

| Name          | Documentation              |
| ------------- | -------------------------- |
| `fields`      | [Read More](#fields)       |
| `meta`        | [Read More](#meta)         |
| `status`      | [Read More](#status)       |

##### Examples

Returns the user based on the token provided.

```bash
curl -u <token>: https://api.directus.io/_/users/me
```

#### Update User

Updates a Directus User.

```http
PATCH /[project]/users/[id]
```

:::tip NOTE
**PATCH** will partially update the item with the provided data, any missing fields will be ignored.
:::

##### Body

An [User Object](#). Fields names must match column names within `directus_users` collection.

#### Delete User

Deletes one or more users from this project.

```http
DELETE /[project]/users/[id]
DELETE /[project]/users/[id1],[id2],[id3],...
```

::: tip NOTE
Instead of deleting a user, you should instead soft-delete them (update their `status` to "suspended" or "deleted") to maintain accountability relations with the `directus_users.id`. Only hard-delete if the user was created in error and never used.
:::

::: danger WARNING
Batch Delete can quickly destroy large amounts of data. Please be careful when implementing this request.
:::

#### Invite User

Invites one or more users to this project. It creates a user with an `invited` status, and then sends an email to the user with instructions on how to activate their account.

```http
POST /[project]/users/invite
```

The API will generate and send a JWT token inside the email for this specific request. The payload contains the following data:

- `type`: The token type, always set to `invitation`.
- `date`: The datetime when the token was generated.
- `exp`: The expiration datetime of the token.
- `email`: The email of the user that will receive the invitation.
- `sender`: The ID of the user that sends the invitation.

##### Body

A single email or list of emails to send invites to.

```json
{
    "email": "rijk@directus.io"
}
```

_Or, to invite multiple users:_

```json
{
  "email": [
    "rijk@directus.io",
    "welling@directus.io",
    "ben@directus.io"
  ]
}
```

#### Accept User Invitation

Accepts and enables an invited user using a JWT invitation token.

```http
POST /[project]/users/invite/[token]
```

#### Track User

Sets the last accessed page/datetime of the Directus App. This information is used to determine if the user is still logged into the Directus App and to warn when multiple users are editing the same item.

```http
PATCH /[project]/users/[id]/tracking/page
```

##### Body

The path to the last page the user was on in the Directus App.

```json
{
    "last_page": "/tables/projects"
}
```

#### Get User Revisions

Returns a list of revisions of a user.

```http
GET /[project]/users/[id]/revisions
```

#### Get User Revision

Returns a single revision of an user using a 0-index based offset.

```http
GET /[project]/users/[id]/revisions/[offset]
```

## Utilities

| Available Hashers |
| ----------------- |
| `core`            |
| `bcrypt`          |
| `sha1`            |
| `sha224`          |
| `sha256`          |
| `sha384`          |
| `sha512`          |

The default `hasher` is `core` which uses the `password_hash` function and the PHP default algorthim defined by `PASSWORD_DEFAULT`.

### Hash String

Hashes a submitted string using the chosen algorithm.

```http
POST /[project]/utils/hash
```

#### Body

The hashing algorithm and the string to hash.

```json
{
    "hasher": "sha1",
    "string": "Directus"
}
```

#### Response

```json
{
  "data": {
    "hash": "<hashed-string>"
  }
}
```

### Match Hashed String

Verifies that a string hashed with a given algorithm matches a hashed string.

```http
POST /[project]/utils/hash/match
```

#### Body

The hashing algorithm to use, the plain string, and the hashed string.

```json
{
    "hasher": "sha1",
    "string": "Directus",
    "hash": "c898896f3f70f61bc3fb19bef222aa860e5ea717"
}
```

#### Response

```json
{
  "data": {
    "valid": true
  }
}
```

### Generate Random String

Returns a randomly generated alphanumeric string.

```http
POST /[project]/utils/random/string
```

#### Body

| Name   | Default | Description                  |
| ------ | ------- | ---------------------------- |
| length | 32      | Length of string to generate |

## Mail

### Send Email

Send an email to one or more recipients.

```http
POST /[project]/mail
```

#### Body

```json
{
  "to": [
    1,
    "user@example.com",
    2,
    {"email": "intern@example.com", "name": "Jane Doe"}
  ],
  "subject": "New Password",
  "body": "Hello <b>{{name}}</b>, this is your new password: {{password}}.",
  "type": "html",
  "data": {
    "name": "John Doe",
    "password": "secret"
  }
}
```

## Extensions

Directus can easily be extended through the addition of several types of extensions. Extensions are and important part of the Directus App that live within the decoupled Directus API. These extensions include: Interfaces, Layouts, and Pages. These three different types of extensions live in their own directory and may have their own endpoints. All custom endpoints defined in extensions (`pages`, `interfaces`, etc) require authentication.

### Get Extensions

These endpoints search for different types of enabled extensions and include the content of each extension's `meta.json` file.

```http
GET /interfaces
GET /layouts
GET /pages
```

### Get Interface

All endpoints defined in an interface will be located within the `interfaces` group.

```http
GET /[project]/interfaces/[interface-id]
```

### Get Page

All endpoints defined in a page will be located within the `pages` group.

```http
GET /[project]/pages/[page-id]
```

### Get Custom Endpoint

All custom endpoints that are not related to an extension will be located under the `custom` group.

::: warning
These endpoints do not require authentication, and are therefore publically accessible.
:::

```http
GET /[project]/custom/[endpoint-id]
```

## Server

A server is comprised of the OS, HTTP server, PHP, and an instance of the Directus API.

### Information

Returns information about the server and API instance.

```http
GET /
```

#### Response

```json
{
  "data": {
    "api": {
      "version": "2.0.14",
      "database": "mysql",
      "project_name": "Directus",
      "project_logo": {
        "full_url": "http://localhost/uploads/_/originals/logo.jpg",
        "url": "/uploads/_/originals/logo.jpg"
      }
    },
    "server": {
      "general": {
        "php_version": "7.2.1",
        "php_api": "apache2handler"
      },
      "max_upload_size": 8388608
    }
  }
}
```

### Ping

If the server is setup correctly it will respond with `pong` as plain text.

```http
GET /server/ping
```

## Projects

Each instance of Directus can manage multiple projects. A project is comprised of a dedicated SQL database, a config file, and any storage directories.

### Information

Returns information about the server and API instance in relation to project.

```http
GET /[project]/
```

An example would be if `upload_max_size` has been increased only for a single project within this API instance.

#### Response

```json
{
  "data": {
    "api": {
      "version": "2.0.0-rc.2"
    },
    "server": {
      "general": {
        "php_version": "7.2.1",
        "php_api": "apache2handler"
      },
      "max_upload_size": 8388608
    }
  }
}
```

### Update

Updates the project database.

```http
POST /[project]/update
```

#### Response

Empty response when successful.

### Create Project

Create a new project (database and config file) to be managed by this API instance.

```http
POST /projects
```

#### Body

| Attribute       | Description                            | Required
| --------------- | -------------------------------------- | ---------
| `project`       | The project key. Default: `_`          | No
| `force`         | Force the installation                 | No
| `existing`      | Ignore existing installation           | No
| `db_type`       | Database type. Only `mysql` supported  | No
| `db_host`       | Database host. Default: `localhost`    | No
| `db_socket`     | Database unix socket                   | No
| `db_port`       | Database port. Default: `3306`         | No
| `db_name`       | Database name                          | Yes
| `db_user`       | Database user name                     | Yes
| `db_password`   | Database user password                 | No
| `user_email`    | Directus Admin email                   | Yes
| `user_password` | Directus Admin password                | Yes
| `user_token`    | Directus Admin token. Default: `null`  | No
| `mail_from`     | Default mailer `from` email            | No
| `project_name`  | The project name. Default: `Directus`  | No
| `app_url`       | The application's URL.                 | No
| `cors_enabled`  | Enable CORS. Default `true`            | No
| `auth_secret`   | Sets the authentication secret key     | No
| `auth`          | [Auth Object](#projects-auth-config)   | No
| `cors`          | [CORS Object](#projects-cors-config)   | No
| `cache`         | [Cache Object](#projects-cache-config) | No
| `storage`       | [Storage Object](#projects-storage-config) | No
| `mail`          | [Mail Object](#projects-mail-config) | No
| `rate_limit`    | [Rate Limit Object](#projects-mail-config) | No

::: warning
When `project` is not specified it will create the default configuration.
:::

::: tip
If there's a fille in the root named `.lock` this instance is locked from creating new projects.
:::

```json
{
    "db_name": "directus",
    "db_user": "root",
    "db_password": "pass",
    "user_email": "admin@example.com",
    "user_password": "password"
}
```

### Projects Auth Config

| Attribute       | Description
| --------------- | --------------------------------------
| `secret`        | Auth secret key
| `public`        | Auth public key
| `social_providers` | List of SSO Providers.

SSO Providers supported `okta`, `github`, `facebook`, `google`, and `twitter`.

Read more about the `auth` configuration [here](../advanced/api/configuration.md#auth).

### Projects CORS Config

| Attribute       | Description
| --------------- | --------------------------------------
| `enabled`       | Enable (`true`) or disable (`false`) CORS
| `origin`        | List of allowed origin hosts
| `methods`       | List of allowed HTTP methods
| `headers`       | List of allowed HTTP headers
| `exposed_header`| List of HTTP headers to expose in the response
| `max_age`       | How long (in seconds) to cache a preflight request
| `credentials`   | Include client credentials (cookies, auth headers, and TLS client certificates)

Read more about the `cors` configuration [here](../advanced/api/configuration.md#cors).

### Projects Cache Config

| Attribute       | Description
| --------------- | --------------------------------------
| `enabled`       | Enable (`true`) or disable (`false`) cache
| `response_ttl`  | How long (in seconds) the cache will be valid
| `adapter`       | Cache adapter identifier (`apc`, `apcu`, `filesystem`, `memcached`, `redis`)
| `path`          | When using `filesystem` adapter, path where the cache will be stored
| `host`          | The adapter host
| `port`          | The adapter port

Read more about the `cache` configuration [here](../advanced/api/configuration.md#cache).

### Projects Storage Config

| Attribute       | Description
| --------------- | --------------------------------------
| `adapter`       | Storage adapter identifier
| `root`          | Storage root path
| `root_url`      | Storage url to access files in `root`
| `thumb_root`    | Thumbnails root path
| `key`           | S3 Bucket key
| `secret`        | S3 Bucket secret
| `region`        | S3 Bucket region
| `version`       | S3 Bucket version
| `bucket`        | S3 Bucket name
| `options`       | S3 Bucket options
| `endpoint`      | S3 Bucket endpoint

Read more about the `storage` configuration [here](../advanced/api/configuration.md#storage).

### Projects Mail Config

| Attribute       | Description
| --------------- | --------------------------------------
| `transport`     | Mail transport
| `sendmail`      | Mail sendmail command (when `sendmail` is used)
| `host`          | SMTP host
| `port`          | SMTP port
| `username`      | SMTP username
| `password`      | SMTP password
| `encryption`    | SMTP encryption

Read more about the `storage` configuration [here](../advanced/api/configuration.md#mail).

### Projects Rate Limit Config

| Attribute       | Description
| --------------- | --------------------------------------
| `enabled`       | Enable (`true`) or Disable (`false`)
| `limit`         | Number of request within `interval`
| `interval`      | How long (in seconds) a interval will last
| `adapter`       | Rate limit adapter
| `host`          | Adapter host
| `port`          | Adapter port
| `timeout`       | Adapter request timeout

## Field Types

Returns the list of [Directus field types](/guides/field-types.md).

```http
GET /types
```

## Webhooks

Webhooks allow you to send an HTTP request when a specific event occurs. Creating a webhook in Directus is done by creating a custom hook that makes an HTTP request.

The example below sends a `POST` request to `http://example.com/alert` every time an article is created, using the following payload:

```json
{
  "type": "article",
  "data": {
    "title": "new article",
    "body": "this is a new article"
  }
}
```

```php
<?php

return [
    'actions' => [
        // Send an alert when a article is created
        'collection.insert.articles' => function (array $data) {
            $client = new \GuzzleHttp\Client([
                'base_uri' => 'http://example.com'
            ]);

            $data = [
                'type' => 'article',
                'data' => $data
            ];

            $response = $client->request('POST', '/alert', [
                'json' => $data
            ]);
        }
    ]
];
```

## Directus Objects

A list of all system objects expected or returned by Directus endpoints.

### Activity Object

| Key                   |  Type             | Description                               |
| --------------------- | ----------------- | ----------------------------------------- |
| `id`                  | `integer`         |                                           |
| `action`              | `string`          |                                           |
| `action_by`           | `integer`,`User`  | The ID of the User                        |
| `action_on`           | `timestamp`       |                                           |
| `ip`                  | `string`          |                                           |
| `user_agent`          | `string`          |                                           |
| `collection`          | `string`          |                                           |
| `item`                | `string`          |                                           |
| `edited_on`           | `timestamp`       |                                           |
| `comment`             | `string`          |                                           |
| `comment_deleted_on`  | `timestamp`       |                                           |

### Activity Seen Object

| Key                   |  Type                 | Description                               |
| --------------------- | --------------------- | ----------------------------------------- |
| `id`                  | `integer`             |                                           |
| `activity`            | `integer`, `Activity` | The ID of the Activity                    |
| `user`                | `integer`,`User`      | The ID of the User                        |
| `seen_on`             | `timestamp`           |                                           |
| `archived`            | `boolean`             |                                           |

### Collection Object

| Key                   |  Type                | Description                               |
| --------------------- | -------------------- | ----------------------------------------- |
| `collection`          | `string`             |                                           |
| `managed`             | `boolean`            |                                           |
| `hidden`              | `boolean`            |                                           |
| `single`              | `boolean`            |                                           |
| `icon`                | `string`             |                                           |
| `note`                | `string`             |                                           |
| `translation`         | `json`               |                                           |

### Collection Preset Object

| Key                   |  Type                | Description                               |
| --------------------- | -------------------- | ----------------------------------------- |
| `id`                  | `integer`            |                                           |
| `title`               | `string`             |                                           |
| `user`                | `integer`, `User`    |  The ID of the User                       |
| `role`                | `integer`, `Role`    |  The ID of the Role                       |
| `collection`          | `string`             |                                           |
| `search_query`        | `string`             |                                           |
| `filters`             | `json`               |                                           |
| `view_type`           | `string`             |                                           |
| `view_query`          | `json`               |                                           |
| `view_options`        | `json`               |                                           |
| `translation`         | `json`               |                                           |

### Field Object

| Key                   |  Type                  | Description                               |
| --------------------- | ---------------------- | ----------------------------------------- |
| `id`                  | `integer`              |                                           |
| `collection`          | `string`, `Collection` | The ID of the Collection                  |
| `field`               | `string`               |                                           |
| `type`                | `string`               |                                           |
| `interface`           | `string`               |                                           |
| `options`             | `json`                 |                                           |
| `locked`              | `boolean`              |                                           |
| `validation`          | `string`               |                                           |
| `required`            | `boolean`              |                                           |
| `readonly`            | `boolean`              |                                           |
| `hidden_detail`       | `boolean`              |                                           |
| `hidden_browse`       | `boolean`              |                                           |
| `sort`                | `integer`              |                                           |
| `width`               | `integer`              |                                           |
| `group`               | `integer`              |                                           |
| `note`                | `string`               |                                           |
| `translation`         | `json`                 |                                           |

### File Object

| Key           | Type               | Description          |
|---------------|--------------------|----------------------|
| `id`          | `integer`          |                      |
| `storage`     | `string`           |                      |
| `filename`    | `string`           |                      |
| `title`       | `string`           |                      |
| `type`        | `string`           |                      |
| `uploaded_by` | `integer`, `User`  | The ID of the User   |
| `uploaded_on` | `timestamp`        |                      |
| `charset`     | `string`           |                      |
| `filesize`    | `integer`          |                      |
| `width`       | `integer`          |                      |
| `height`      | `integer`          |                      |
| `duration`    | `integer`          |                      |
| `embed`       | `string`           |                      |
| `folder`      | `string`, `Folder` | The ID of the Folder |
| `description` | `string`           |                      |
| `location`    | `string`           |                      |
| `tags`        | `array`, `string`  |                      |
| `metadata`    | `json`             |                      |
| `data`        | `json`             |                      |

### Folder Object

| Key             | Type               | Description |
|-----------------|--------------------|-------------|
| `id`            | `integer`          |             |
| `name`          | `string`           |             |
| `parent_folder` | `string`, `Folder` |             |

### Permission Object

| Key                     | Type              | Description                                          |
|-------------------------|-------------------|------------------------------------------------------|
| `id`                    | `integer`         |                                                      |
| `collection`            | `string`          |                                                      |
| `role`                  | `integer`, `Role` | The ID of the Role                                   |
| `status`                | `string`          |                                                      |
| `create`                | `string`          | "none" (or NULL), "full"                             |
| `read`                  | `string`          | "none" (or NULL), "mine", "role", "full"             |
| `update`                | `string`          | "none" (or NULL), "mine", "full"                     |
| `delete`                | `string`          | "none" (or NULL), "mine", "role", "full"             |
| `comment`               | `string`          | "none", "read", "update" (or NULL), "create", "full" |
| `explain`               | `string`          | "none" (or NULL), "update", "create", "always"       |
| `read_field_blacklist`  | `array`           | List of fields that the role cannot read             |
| `write_field_blacklist` | `array`           | List of fields that the role cannot edit             |
| `status_blacklist`      | `array`           |                                                      |

### Relation Object

| Key               | Type                   | Description |
|-------------------|------------------------|-------------|
| `id`              | `integer`              |             |
| `collection_many` | `string`, `Collection` |             |
| `field_many`      | `string`, `Field`      |             |
| `collection_one`  | `string`, `Collection` |             |
| `field_one`       | `string`, `Field`      |             |
| `junction_field`  | `string`, `Field`      |             |

### Revision Object

| Key                 | Type                   | Description                                                                                       |
|---------------------|------------------------|---------------------------------------------------------------------------------------------------|
| `id`                | `integer`              |                                                                                                   |
| `activity`          | `integer`, `Activity`  | The ID of the Activity                                                                            |
| `collection`        | `string`, `Collection` | The ID of the Collection                                                                          |
| `item`              | `string`               | ID of the item in the collection, or the Collection name if the collection is directus_collection |
| `data`              | `json`                 | The item's JSON object                                                                            |
| `delta`             | `json`                 | Item keys that were changed and their updated values                                              |
| `parent_collection` | `string`,`Collection`  |                                                                                                   |
| `parent_item`       | `string`,`Item`        |                                                                                                   |
| `parent_changed`    | `boolean`              |                                                                                                   |

### Role Object

| Key             | Type            | Description             |
|-----------------|-----------------|-------------------------|
| `id`            | `integer`       |                         |
| `name`          | `string`        | Name of the role        |
| `description`   | `string`        | Description of the role |
| `ip_whitelist`  | `string`        |                         |
| `nav_blacklist` | `string`        |                         |
| `external_id`   | `string`        |                         |

### Setting Object

| Key     | Type      | Description |
|---------|-----------|-------------|
| `id`    | `integer` |             |
| `key`   | `string`  |             |
| `value` | `string`  |             |

### User Object

| Key                   | Type              | Description                   |
|-----------------------|-------------------|-------------------------------|
| `id`                  | `integer`         |                               |
| `status`              | `string`          |                               |
| `first_name`          | `string`          |                               |
| `last_name`           | `string`          |                               |
| `email`               | `string`          |                               |
| `password`            | `string`          |                               |
| `token`               | `string`          | Static token                  |
| `timezone`            | `string`          |                               |
| `locale`              | `string`          |                               |
| `locale_options`      | `string`          |                               |
| `avatar`              | `integer`, `File` | The ID of the File            |
| `company`             | `string`          |                               |
| `title`               | `string`          |                               |
| `email_notifications` | `boolean`         |                               |
| `last_access_on`      | `timestamp`       |                               |
| `last_page`           | `string`          | The relative path of the page |
| `external_id`         | `string`          | For SCIM authorization        |

### User Role Object

| Key    | Type              | Description        |
|--------|-------------------|--------------------|
| `id`   | `integer`         |                    |
| `user` | `integer`, `User` | The ID of the User |
| `role` | `integer`, `Role` | The ID of the Role |

## SCIM

Directus partially supports Version 2 of System for Cross-domain Identity Management (SCIM). It is an open standard that allows for the exchange of user information between systems, therefore allowing users to be externally managed using the endpoints described below.

### Overview

| Endpoint       | Methods                         |
| -------------- | ------------------------------- |
| `/Users`       | `GET`, `POST`                   |
| `/Users/[id]`  | `GET`, `PUT`, `PATCH`           |
| `/Groups`      | `GET`, `POST`                   |
| `/Groups/[id]` | `GET`, `PUT`, `PATCH`, `DELETE` |

Learn more within the "SCIM Endpoints and HTTP Methods" section of [RFC7644](https://tools.ietf.org/html/rfc7644#section-3.2).

If want to integrate Directus SCIM endpoints with Okta, follow these steps on [Publishing Your SCIM-Based Provisioning Integration](https://developer.okta.com/standards/SCIM/#publishing-your-scim-based-provisioning-integration) section.

### Create SCIM User

```http
POST /[project]/scim/v2/Users
```

#### Body

```json
{
  "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
  "userName":"johndoe@example.com",
  "externalId":"johndoe-id",
  "name":{
    "familyName":"Doe",
    "givenName":"John"
  }
}
```

#### Response

```json
{
  "schemas": [
    "urn:ietf:params:scim:schemas:core:2.0:User"
  ],
  "id": "johndoe-id",
  "externalId": 4,
  "meta": {
    "resourceType": "User",
    "location": "http://example.com/_/scim/v2/Users/johndoe-id",
    "version": "W/\"fb2c131ad3a58d1f32800c1379cdfe50\""
  },
  "name": {
    "familyName": "Doe",
    "givenName": "John"
  },
  "userName": "johndoe@example.com",
  "emails": [
    {
      "value": "johndoe@example.com",
      "type": "work",
      "primary": true
    }
  ],
  "locale": "en-US",
  "timezone": "America/New_York",
  "active": false
}
```

### Get SCIM Users

```http
GET /[project]/scim/v2/Users
```

#### Supported Query Parameters
| Name         | Type        | Description
| ------------ | ------------| ------------
| `startIndex` | `Integer`   | The 1-based index of the first result in the current set of list results.
| `count`      | `Integer`   | Specifies the desired maximum number of query results per page.
| `filter`     | `String`    | `id`, `userName`, `emails.value` and `externalId` attributes are supported. Only the `eq` operator is supported.

```http
GET /[project]/scim/v2/Users?filter=userName eq user@example.com
```

#### Response

```json
{
  "schemas": [
    "urn:ietf:params:scim:api:messages:2.0:ListResponse"
  ],
  "totalResults": 3,
  "Resources": [
    {
      "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:User"
      ],
      "id": "789",
      "externalId": 1,
      "meta": {
          "resourceType": "User",
          "location": "http://example.com/_/scim/v2/Users/789",
          "version": "W/\"fb2c131da3a58d1f32800c3179cdfe50\""
      },
      "name": {
          "familyName": "User",
          "givenName": "Admin"
      },
      "userName": "admin@example.com",
      "emails": [
          {
              "value": "admin@example.com",
              "type": "work",
              "primary": true
          }
      ],
      "locale": "en-US",
      "timezone": "Europe/Berlin",
      "active": true
    },
    {
      "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:User"
      ],
      "id": "345",
      "externalId": 2,
      "meta": {
        "resourceType": "User",
        "location": "http://example.com/_/scim/v2/Users/345",
        "version": "W/\"68c210ea2la8isj2ba11d8b3b2982d\""
      },
      "name": {
        "familyName": "User",
        "givenName": "Intern"
      },
      "userName": "intern@example.com",
      "emails": [
        {
          "value": "intern@example.com",
          "type": "work",
          "primary": true
        }
      ],
      "locale": "en-US",
      "timezone": "America/New_York",
      "active": true
    },
    {
      "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:User"
      ],
      "id": "123",
      "externalId": 3,
      "meta": {
        "resourceType": "User",
        "location": "http://example.com/_/scim/v2/Users/123",
        "version": "W/\"20e4fasdf0jkdf9aa497f55598c8c883\""
      },
      "name": {
        "familyName": "User",
        "givenName": "Disabled"
      },
      "userName": "disabled@example.com",
      "emails": [
        {
          "value": "disabled@example.com",
          "type": "work",
          "primary": true
        }
      ],
      "locale": "en-US",
      "timezone": "America/New_York",
      "active": false
    }
  ]
}
```

### Get SCIM User

```http
GET /[project]/scim/v2/Users/[id]
```

The `id` must be the `external_id` in the `directus_users` collection, which is the `id` in the SCIM Users results.

#### Response

```json
{
  "schemas": [
    "urn:ietf:params:scim:schemas:core:2.0:User"
  ],
  "id": "789",
  "externalId": 1,
  "meta": {
    "resourceType": "User",
    "location": "http://example.com/_/scim/v2/Users/789",
    "version": "W/\"fb2c131da3a58d1f32800c3179cdfe50\""
  },
  "name": {
    "familyName": "User",
    "givenName": "Admin"
  },
  "userName": "admin@example.com",
  "emails": [
    {
      "value": "admin@example.com",
      "type": "work",
      "primary": true
    }
  ],
  "locale": "en-US",
  "timezone": "Europe/Berlin",
  "active": true
}
```

### Update SCIM User

```http
PATCH /[project]/scim/v2/Users/[id]
```

#### Body

```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
  "name": {
    "familyName": "Doe",
    "givenName": "Johnathan"
  }
}
```

#### Response

```json
{
  "schemas": [
    "urn:ietf:params:scim:schemas:core:2.0:User"
  ],
  "id": "johndoe-id",
  "externalId": 4,
  "meta": {
    "resourceType": "User",
    "location": "http://example.com/_/scim/v2/Users/johndoe-id",
    "version": "W/\"fb2c131ad3a66d1f32800c1379cdfe50\""
  },
  "name": {
    "familyName": "Doe",
    "givenName": "Johnathan"
  },
  "userName": "johndoe@example.com",
  "emails": [
    {
      "value": "johndoe@example.com",
      "type": "work",
      "primary": true
    }
  ],
  "locale": "en-US",
  "timezone": "America/New_York",
  "active": false
}
```

### Create SCIM Group

```http
POST /[project]/scim/v2/Users
```

#### Body

```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
  "displayName": "Editors",
  "externalId": "editors-id"
}
```

#### Response

```json
{
  "schemas": [
    "urn:ietf:params:scim:schemas:core:2.0:Group"
  ],
  "id": "editors-id",
  "externalId": 4,
  "meta": {
    "resourceType": "Group",
    "location": "http://example.com/_/scim/v2/Groups/editors-id",
    "version": "W/\"7b7bc2512ee1fedcd76bdc68926d4f7b\""
  },
  "displayName": "Editors",
  "members": []
}
```

### Get SCIM Groups

```http
GET /[project]/scim/v2/Groups
```

#### Supported Query Parameters

| Name         | Type        | Description
| ------------ | ------------| ------------
| `startIndex` | `Integer`   | The 1-based index of the first result in the current set of list results.
| `count`      | `Integer`   | Specifies the desired maximum number of query results per page.
| `filter`     | `String`    | `displayName` attribute Supported. Only operator `eq` is supported.

```http
GET /[project]/scim/v2/Groups
```

#### Response

```json
{
  "schemas": [
    "urn:ietf:params:scim:api:messages:2.0:ListResponse"
  ],
  "totalResults": 3,
  "Resources": [
    {
      "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:Group"
      ],
      "id": "one",
      "externalId": 1,
      "meta": {
        "resourceType": "Group",
        "location": "http://example.com/_/scim/v2/Groups/one",
        "version": "W/\"7b7bc2512ee1fedcd76bdc68926d4f7b\""
      },
      "displayName": "Administrator",
      "members": [
        {
          "value": "admin@example.com",
          "$ref": "http://example.com/_/scim/v2/Users/789",
          "display": "Admin User"
        }
      ]
    },
    {
      "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:Group"
      ],
      "id": "two",
      "externalId": 2,
      "meta": {
        "resourceType": "Group",
        "location": "http://example.com/_/scim/v2/Groups/two",
        "version": "W/\"3d067bedfe2f4677470dd6ccf64d05ed\""
      },
      "displayName": "Public",
      "members": []
    },
    {
      "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:Group"
      ],
      "id": "three",
      "externalId": 3,
      "meta": {
        "resourceType": "Group",
        "location": "http://example.com/_/scim/v2/Groups/three",
        "version": "W/\"17ac93e56edd16cafa7b57979b959292\""
      },
      "displayName": "Intern",
      "members": [
        {
            "value": "intern@example.com",
            "$ref": "http://example.com/_/scim/v2/Users/345",
            "display": "Intern User"
        },
        {
            "value": "disabled@example.com",
            "$ref": "http://example.com/_/scim/v2/Users/123",
            "display": "Disabled User"
        }
      ]
    }
  ]
}
```

### Get SCIM Group

```http
GET /[project]/scim/v2/Groups/[id]
```

#### Response

```json
{
  "schemas": [
    "urn:ietf:params:scim:schemas:core:2.0:Group"
  ],
  "id": "one",
  "externalId": 1,
  "meta": {
    "resourceType": "Group",
    "location": "http://example.com/_/scim/v2/Groups/one",
    "version": "W/\"7b7bc2512ee1fedcd76bdc68926d4f7b\""
  },
  "displayName": "Administrator",
  "members": [
    {
      "value": "admin@example.com",
      "$ref": "http://example.com/_/scim/v2/Users/1",
      "display": "Admin User"
    }
  ]
}
```

### Update SCIM Group

```http
PATCH /[project]/scim/v2/Groups/[id]
```

#### Body

```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
  "displayName": "Writers"
}
```

#### Response

```json
{
  "schemas": [
    "urn:ietf:params:scim:schemas:core:2.0:Group"
  ],
  "id": "editors-id",
  "externalId": 4,
  "meta": {
    "resourceType": "Group",
    "location": "http://example.com/_/scim/v2/Groups/editors-id",
    "version": "W/\"7b7bc2512ee1fedcd76bdc68926d4f7b\""
  },
  "displayName": "Writers",
  "members": []
}
```

### Delete SCIM Group

```http
DELETE /[project]/scim/v2/Groups/[id]
```

#### Response

Response is empty when successful.
