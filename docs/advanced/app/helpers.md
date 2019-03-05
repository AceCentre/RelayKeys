# Helpers

> Utility functions and microlibraries that are being used across the App are being stored and managed in the `/helpers` folder. Every function is in a separate file, and is being bundled into `this.$helpers` in the `/helpers/index.js` file.

## Functions

### Title Formatter

Most (raw) values in Directus are being displayed in title case. We try to prevent showing users raw (db) names like `image_gallery`, instead we want to show "Image Gallery". This formatter function is available to all Vue components. The function is available in the `$helper` directive with the method name `formatTitle`:

> This package converts any string into title case. This means only using capital letters for the principal words. Articles, conjunctions, and prepositions do not get capital letters unless they start the title.

```js
this.$helpers.formatTitle("hello_world"); // Hello World
this.$helpers.formatTitle("iphone_storageSolution"); // iPhone Storage Solution
this.$helpers.formatTitle('snowWhiteAndTheSevenDwarfs'); // Snow White and the Seven Dwarfs
```

This function is alternatively available as a stand-alone npm package: [@directus/format-title](https://npmjs.com/@directus/format-title).

### Date

Convert SQL datetime string to JavaScript Date object, or vise versa:

```js
this.$helpers.date.sqlToDate("2018-07-19 15:36:00");
// => Date

this.$helpers.date.dateToSql(new Date());
// => "2018-07-19 15:36:00"
```

### componentExists

Check if a component is registered in the global Vue instance

```js
this.$helpers.componentExists("v-checkbox"); // true
```

### formatFilters

The API uses filters in the URL in a URL-safe syntax: `filters[field][operator]=value`. While this works great in the URL, it's not the most useful to process and use in JavaScript, for example when rendering the filter on the listing view. In order work with filters more efficiently, the app uses a proprietary JSON format for filters:

```json
[
  {
    "field": "age",
    "operator": "eq",
    "value": "22"
  }
]
```

The `formatFilters` helper function converts that format to the API readable format:

```js
const filters = [
  {
    field: "age",
    operator: "eq",
    value: "22"
  }
];

this.$helpers.formatFilters(filters);
// => filters[age][eq]=22
```

## Micro Libraries

### [`micromustache`](https://www.npmjs.com/package/micromustache)

String interpolation using an object.

```js
const person = {
  first: 'Michael',
  last: 'Jackson'
};

this.$helpers.micromustache.render('Search for {{first}} {{ last }} songs!', person);
// => Search for Michael Jackson songs!
```

or

```
this.$helpers.micromustache.render(
  "Hello {{text}}!",
  { text: "World" }
);
```

### [`shortid`](https://www.npmjs.com/package/shortid)

> ShortId creates amazingly short non-sequential url-friendly unique ids. Perfect for url shorteners, MongoDB and Redis ids, and any other id users might see.

```js
this.$helpers.shortid.generate();
// => PPBqWA9
```

### [`date-fns`](https://www.npmjs.com/package/date-fns)

> date-fns provides the most comprehensive, yet simple and consistent toolset for manipulating JavaScript dates in a browser & Node.js.

```js
this.$helpers.dateFns;
```
