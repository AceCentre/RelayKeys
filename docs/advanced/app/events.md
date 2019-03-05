# Events

::: danger
Global events should be used only as a last resort when working with [the store](./store.md) or regular Vue events between child and parent components doesn't work for your usecase.
:::

The Directus app has a global event-bus you can use to send messages across the system. Right now, the only global event that's being used in this fashion is `error`.

## Usage

The EventBus can be imported directly from the `./events/index.js` file, or can be used in `this.$events`.

```js
import EventBus from "./events/";

EventBus.on("event", handlerFunction);

EventBus.off("event", handlerFunction);

EventBus.once("event", handlerFunction);

EventBus.emit("event", "value");
```

## Creating a new global event

You should put all event handlers in the `/events` folder and put all `EventBus.on` statements in `./events/index.js`. It's near impossible to keep track of all global events if you don't.

If for whatever reason you need to listen to a global event from within a component, please add a note to the `./events/index.js` file so we can keep track of when and why an event is used.

## Used Events

The following events are globally in use:

### Error

#### When

Something went wrong somewhere in the system

#### What

The global parent app will console.error the error and optionally show a notification to the user

#### Options

| name    | type     | default                    | description                                            |
|---------|----------|----------------------------|--------------------------------------------------------|
| notify  | Boolean  | false                      | Show a notification to the user                        |
| message | [String] | $t('something_went_wrong') | Message to show in the console / notification          |
| error   | Object   | null                       | The error stacktrace or whatever error you want logged |
