# Setting up a board for RelayKeys

{% hint style="info" %}
If you have a pre-prepared Bliuetooth stick (for example from Ace Centre) you don't need to read this section. If you are buying your own electronics to use then read on.&#x20;
{% endhint %}

A wide range of Arduino boards supports HID (Human Interface Device). Often these are to emulate simple keypress' but to do more complex things like send one or modififer keys with a key - or to emulate holding a key down for a set period of time is either impossible or difficult to implement. Adafruit have developed the firmware on their Bluefruit nrf\* range of boards to emulate HID keyboards well using their AT Commands.

Currently RelayKeys is designed to work with the [Adafruit Feather nRF52840 Express](https://www.adafruit.com/product/4062) (Buy in the [UK from Pimoroni](https://shop.pimoroni.com/products/adafruit-feather-nrf52840-express)) or with the [Adafruit itsybitsy nrf52840 ](https://www.adafruit.com/product/4481)or with lesser support for the [The Adafruit - Bluefruit LE Friend - nRF51822 - v3.0](https://www.adafruit.com/product/2267) (Buy in the [UK from Pimoroni](https://shop.pimoroni.com/products/adafruit-bluefruit-le-friend-ble-4-0-nrf51822-v1-0#description)). _Although Note: We really arent supporting the LE Friend much - we do hear it works but dragons beware!_ See below for details on configuring these.

{% hint style="info" %}
If you are using a receiver dongle - follow the same guidance below but you will also need to copy over the firmware file for the dongle. Same procedure - different file name
{% endhint %}

##
