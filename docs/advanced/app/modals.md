# Using Modals

Modals can be used for a variety of reasons, from showing alerts to allowing users to pick and upload images in an advanced file explorer.

There are 4 types of modal available in the system:

* Alert
* Prompt
* Confirm
* Modal

The first three mimic the default browser modals (`alert()`, `prompt()`, and `confirm()`), the last one can be used for basically everything else.

We recommend using the first three when applicable, and only using the generic modal for more elaborate interactions, like an image picker.

## General Usage

All 4 modal types are available as global Vue components: `v-alert`, `v-prompt`, `v-confirm`, and `v-modal`. These components can be included in any Vue single file component and will immediately render a blocker over the whole app and disable user interaction outside of the modal. Because of this, you should always use a modal in combination with a `v-if` statement based on the local state of your component. You'll also have to toggle this state based on the cancel prop of this component, to allow the user to cancel out of the modal by clicking outside of it.

```vue
<template>
  <div class="my-component">

    <button @click="alertActive = true">Show Alert</button>

    <v-prompt
      v-if="promptActive"
      v-model="value"
      @confirm="saveValue"
      @cancel="promptActive = false"
      message="Hello World!">
    </v-prompt>

  </div>
</template>

<script>
export default {
  name: "my-component",
  data() {
    return {
      promptActive: true,
      value: ""
    };
  },
  methods: {
    saveValue() {}
  }
}
</script>
```

### Portals

The overlay and modal are rendered using a combination of `position: absolute` and `position: fixed`. When using modals in a component that itself has position styling rules associated with it, or has other style rules that conflict with the modal styles, you'll run into a bunch of style issues. To work around this, you can use a `portal-vue` to render the modal itself at then end of the DOM.

> PortalVue is a set of two components that allow you to render a component's template (or a part of it) anywhere in the document - even outside the part controlled by your Vue App!

To render the modal at the end of the DOM, and thus prevent style conflicts, render the modal in a `<portal>` element to the `modal` target:

```vue
<template>
  <div class="my-component">

    <button @click="alertActive = true">Show Alert</button>

    <portal v-if="alertActive" to="modal">
      <v-alert
        @confirm="alertActive = false"
        message="Hello World!">
      </v-alert>
    </portal>

  </div>
</template>

<script>
export default {
  name: "my-component",
  data() {
    return {
      alertActive: true
    };
  }
}
</script>
```

::: warning
There can only be one portal rendered at a time. Make sure to put the v-if statement on the portal itself so you don't end up with conflicts.
:::

## Alert

![Alert](/img/modals/alert.png)

The alert can be used to show the user a message that needs the user's full attention. Try to refrain from using alerts for basic messages. For small confirmations / warnings, use [notifications]() instead.

### Props

`message`
The message that is displayed to the user.

`confirm-text`
The text in the confirm button. Defaults to (the translation of) `ok`.

### Events

`confirm`
The user dismisses the alert.

::: warning NOTE
An alert is basically a read-only message. There is no difference between confirming and canceling. To render a choice, use a `v-confirm` instead.
:::

### Example

```vue
<template>
  <div class="my-component">

    <button @click="alertActive = true">Show Alert</button>

    <portal v-if="alertActive" to="modal">
      <v-alert
        @confirm="alertActive = false"
        message="Hello World!">
      </v-alert>
    </portal>

  </div>
</template>

<script>
export default {
  name: "my-component",
  data() {
    return {
      alertActive: true
    };
  }
}
</script>
```

## Prompt

![Prompt](/img/modals/prompt.png)

The prompt component can be used to ask the user a question. This is for example used in creating new collections.

### Props

`message`
The message that is displayed to the user.

`confirm-text`
The text in the confirm button. Defaults to (the translation of) `ok`.

`cancel-text`
The text that cancels out of the modal. Defaults to (the translation of) `cancel`.

`value`
The value to render in the input of the prompt

`multiline`
Render a textarea instead of a text-input

`required`
Require an user input before he/she can confirm/close out of the modal

`placeholder`
The placeholder to render in the input

`loading`
Shows a loading indicator on the submit button. Useful when you need to perform an API request on confirm of the modal.

`safe`
Only allow database-safe values. (eg `Hello World` => `hello_world`)

### Events

`confirm`
The user submits the value

`cancel`
The user cancels out of the modal

`input`
User inputs a value into the input

::: tip
This component allows the use of `v-model`
:::

::: warning
Since the input's value is managed by the local state of your file, make sure to empty the value on submit's if that's appropriate for your usecase.
:::

### Example

```vue
<template>
  <div class="my-component">

    <button @click="promptActive = true">Show Prompt</button>

    <portal v-if="promptActive" to="modal">
      <v-prompt
        v-model="value"
        message="Hello World!"
        :loading="loading"
        @cancel="promptActive = false"
        @confirm="saveValue">
      </v-prompt>
    </portal>

  </div>
</template>

<script>
export default {
  name: "my-component",
  data() {
    return {
      loading: false,
      promptActive: true,
      value: ""
    };
  },
  methods: {
    saveValue() {
      this.loading = true;

      this.$fakeAPICall(this.value)
        .then(() => {
          this.loading = false;
          this.promptActive = false;
          this.value = "";
        });
    }
  }
}
</script>
```

## Confirm

![Confirm](/img/modals/confirm.png)

Confirms are basic yes or no questions for the user. For example "Are you sure to log out?". For these types of questions, a confirm can be used.

### Props

`message`
The message that is displayed to the user.

`confirm-text`
The text in the confirm button. Defaults to (the translation of) `ok`.

`cancel-text`
The text that cancels out of the modal. Defaults to (the translation of) `cancel`.

`loading`
Shows a loading indicator on the submit button. Useful when you need to perform an API request on confirm of the modal.

`color`
The color variable name to use in the primary button. Uses the global color variable names (eg `red`, `green-50`, `accent`).

### Events

`confirm`
The user submits the value

`cancel`
The user cancels out of the modal

### Example

```vue
<template>
  <div class="my-component">

    <button @click="confirmActive = true">Show Confirm</button>

    <portal v-if="confirmActive" to="modal">
      <v-confirm
        message="Are you sure you want to log out?"
        :loading="loading"
        @cancel="confirmActive = false"
        @confirm="logout">
      </v-confirm>
    </portal>

  </div>
</template>

<script>
export default {
  name: "my-component",
  data() {
    return {
      loading: false,
      confirmActive: true
    };
  },
  methods: {
    logout() {
      this.loading = true;

      this.$fakeAPICall()
        .then(() => {
          this.loading = false;
          this.confirmActive = false;
        });
    }
  }
}
</script>
```

## Modal

![Modal](/img/modals/modal.png)

The `v-modal` component is a "general use" modal component. You can use it to render any other markup in a system standard looking modal.

### Props

`action-required`
Prevent the user from canceling the modal by clicking outside of the modal or hitting ESC

`title`
Title of the modal, rendered in the top header

`buttons`
Object that controls what buttons to render inside the modal's footer. Defaults to nothing. The object's key is used as the event name

_Example buttons object:_
```js
{
  save: {
    text: "me gusta",
    loading: false,
    disabled: false,
    color: "green"
  },
  remove: {
    text: "no me gusta",
    loading: false,
    disabled: true,
    color: "red"
  }
}
```

### Events

`cancel`
The user cancels out of the modal. Can be disabled by using the `action-required` prop.

_Other events are based on the button config passed in. See the `button` prop above._

### Example

```vue
<template>
  <div class="my-component">

    <button @click="modalActive = true">Show modal</button>

    <portal v-if="modalActive" to="modal">
      <v-modal
        title="My Modal"
        :buttons="buttons"
        @save="save"
        @remove="remove">
        <h1>Hello!</h1>
      </v-modal>
    </portal>

  </div>
</template>

<script>
export default {
  name: "my-component",
  data() {
    return {
      modalActive: true
    };
  },
  computed: {
    buttons() {
      return {
        save: {
          text: "me gusta",
          loading: false,
          disabled: false,
          color: "green"
        },
        remove: {
          text: "no me gusta",
          loading: false,
          disabled: true,
          color: red
        }
      }
    }
  },
  methods: {
    save() {},
    remove() {}
  }
}
</script>
```
