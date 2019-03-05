# Store

Directus heavily uses [Vuex](https://vuex.vuejs.org/guide/) for global application state management. You can inspect the Vuex Store using the [Vue DevTools](https://github.com/vuejs/vue-devtools).

Please refer to the official [Vuex documentation](https://vuex.vuejs.org/guide/) for more information on how to use the store.

## About mutation types

We chose to put all the different mutation types as constants in `/store/mutation-types.js`. That way, we have a single source of all the available mutations that can happen in the store. If you're adding new mutations, please put your mutation type definition in that file.

If you're wondering why there's emoji's in the mutation types: it's just to make the devtools [a little more friendly](https://medium.com/@rijk/make-your-vuex-mutation-names-friendly-7e4b53597cd0) ☺️

![Store Mutations](/img/store/emoji.png)


## Action and Mutation Naming

In the Vuex store, actions that are going to retrieve data are always called `get<data>`, f.e. `getItems` or `getUserInfo`. These actions will always fire two out of three possible mutations:

_Using `getUserInfo` action as example_:

* `USER_PENDING` — Start fetching the data
* `USER_SUCCESS` — Got the user info
* `USER_FAILED` — Fetching user error failed


## Promises
Every store action that fetches data should return a promise so the caller can know when the request is done. The promise will resolve _without_ any data, since that data will be in the store. This limitation forces the implementation to rely on the store as single source of truth. The promise will also resolve on a "failed" request, since a response with an api error is also a "successful" request response.

## State

When in `development` mode, you can view all of these state variables in [Vue DevTools](https://github.com/vuejs/vue-devtools), but we've included an abridged example here for reference. All of these values can be accessed within the App using: `this.$store.state`. For example, `this.$store.state.currentUser.first_name` would be `Admin` in the example below.

```json
{
  "hydrated":"[native Date Thu Nov 01 2018 12:50:03 GMT-0400 (Eastern Daylight Time)]",
  "hydratingError":null,
  "latency":[
    {
      "date":1541091002627,
      "latency":476.09999997075647
    }
  ],
  "settings":{
    "auto_sign_out":"60",
    "project_name":"Directus",
    "default_limit":"200",
    "logo":"",
    "youtube_api_key":""
  },
  "currentUser":{
    "id":1,
    "first_name":"Admin",
    "last_name":"User",
    "email":"admin@example.com",
    "locale":"en-US",
    "avatar":null,
    "roles":[1],
    "admin":true
  },
  "collections":{
    "work":{
      "collection":"work",
      "note":null,
      "hidden":false,
      "single":false,
      "managed":true,
      "fields":{
        "id":{
          "collection":"work",
          "field":"id",
          "datatype":"INT",
          "unique":false,
          "primary_key":true,
          "auto_increment":true,
          "default_value":null,
          "note":"",
          "signed":false,
          "id":1,
          "type":"integer",
          "sort":0,
          "interface":"primary-key",
          "hidden_detail":true,
          "hidden_browse":false,
          "required":true,
          "options":{},
          "locked":0,
          "translation":null,
          "readonly":false,
          "width":4,
          "validation":null,
          "group":null,
          "length":"10"
        }
      },
      "icon":null,
      "translation":null,
      "status_mapping":"__vue_devtool_undefined__"
    }
  },
  "bookmarks":[],
  "sidebars":{
    "nav":false,
    "info":false
  },
  "queue":[],
  "auth":{
    "token":"xxxxxxxxx",
    "url":"https://example.com",
    "project":"_",
    "error":null,
    "loading":false,
    "projectName":"Directus Example"
  },
  "extensions":{
    "layouts":{
      "tabular":{
        "id":"tabular",
        "path":"extensions/core/layouts/tabular/meta.json",
        "name":"Table",
        "version":"1.0.0",
        "translation":{
          "en-US":{
            "tabular":"Table",
            "fields":"Fields"
          }
        }
      }
    },
    "interfaces":{
      "text-input":{
        "id":"text-input",
        "path":"extensions/core/interfaces/text-input/meta.json",
        "name":"Text Input",
        "version":"1.0.1",
        "icon":"text_fields",
        "types":[
          "string",
          "lang"
        ],
        "recommended":{
          "length":200
        },
        "options":{},
        "translation":{
          "en-US":{
            "input":"Text Input"
          }
        }
      }
    },
    "pages":{}
  },
  "edits":{
    "collection":"work",
    "primaryKey":"+",
    "values":{},
    "savedValues":{}
  },
  "permissions":{
    "work":{
      "create":"full",
      "read":"full",
      "update":"full",
      "delete":"full",
      "comment":"full",
      "explain":"full",
      "status_blacklist":[],
      "read_field_blacklist":[],
      "write_field_blacklist":[],
      "$create":{
        "create":"full",
        "read":"full",
        "update":"full",
        "delete":"full",
        "comment":"full",
        "explain":"full",
        "status_blacklist":[],
        "read_field_blacklist":[],
        "write_field_blacklist":[]
      }
    }
  },
  "users":{
    "1":{
      "id":1,
      "status":"active",
      "first_name":"Admin",
      "last_name":"User",
      "timezone":"America/New_York",
      "avatar":null,
      "company":null,
      "title":null,
      "roles":[1]
    }
  },
  "relations":[
    {
      "id":1,
      "collection_many":"directus_activity",
      "field_many":"action_by",
      "collection_one":"directus_users",
      "field_one":null,
      "junction_field":null
    }
  ],
  "serverInfo":{
    "apiVersion":"2.0.4",
    "phpVersion":"7.2.7",
    "maxUploadSize":8388608,
    "databaseVendor":"mysql"
  }
}
```
