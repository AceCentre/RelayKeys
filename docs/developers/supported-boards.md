# Supported Electronics Boards

HID (Human Interface Device) is supported by a wide range of Arduino boards. Often these are to emulate simple keypress' but to do more complex things like send one or modififer keys with a key - or to emulate holding a key down for a set period of time is either impossible or difficult to implement. Adafruit have developed the firmware on their Bluefruit nrf\* range of boards to emulate HID keyboards well using their AT Commands.

Currently RelayKeys is designed to work with the [Adafruit Feather nRF52840 Express](https://www.adafruit.com/product/4062) (Buy in the [UK from Pimoroni](https://shop.pimoroni.com/products/adafruit-feather-nrf52840-express)) or with the [Adafruit itsybitsy nrf52840 ](https://www.adafruit.com/product/4481)or with lesser support for the [The Adafruit - Bluefruit LE Friend - nRF51822 - v3.0](https://www.adafruit.com/product/2267) (Buy in the [UK from Pimoroni](https://shop.pimoroni.com/products/adafruit-bluefruit-le-friend-ble-4-0-nrf51822-v1-0#description)). _Although Note: We really arent supporting the LE Friend much - we do hear it works but dragons beware!_ See below for details on configuring these:

## Setup for Adafruit Feather nRF52840 Express

* Check the setup of your [Arduino IDE](https://learn.adafruit.com/bluefruit-nrf52-feather-learning-guide/arduino-bsp-setup) (remember we're using the nRF52840 board!)
* Upload the [sketch](../../arduino/arduino\_nRF52840/arduino\_nRF52840.ino) to your feather.
* Run the server side code
* Done!

## Setup for Adafruit itsybitsy nRF52840&#x20;

* Check the setup of your [Arduino IDE](https://learn.adafruit.com/bluefruit-nrf52-feather-learning-guide/arduino-bsp-setup) (remember we're using the nRF52840 board!)
* Upload the [sketch](../../arduino/arduino\_nRF52840/arduino\_nRF52840.ino) to your feather.
* Run the server side code
* Done!

## Setup for Bluefruit LE Friend

{% hint style="info" %}
Although it _should_ work - and we promise you it _did_ work - something has broken functionality working with the LE friend. So we aren't **officially** supporting this right now&#x20;
{% endhint %}

* [Install the CP2104 Driver](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers)
* Update it to 0.8.1. Easiest way to do this is to connect to using the Bluefruit app - it will auto update it if required.
* Plug it in
* Set the switch on the device to CMD mode
* Open up a serial terminal and connect to the device (See [here](https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/terminal-settings#terraterm-windows-5-2) for exact settings for your Operating System)
*   Turn on HID Mode. More info [here](https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/ble-services#at-plus-blehiden-14-31). To be precise - enter this into your serial terminal

    ```
      AT+BLEHIDEN=1

      ATZ 
    ```

(You should see 'OK' after each entry)

*   Next change the default speed. i.e. enter this in your serial terminal:

    ```
      AT+BAUDRATE=115200
    ```
* Next put the device into [DATA mode](https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/uart-test#blefriend-configuration-6-3) (slide the switch).
*   Finally - update the relaykeys.cfg file with

    ```
      baud = 115200
      
    ```

(Or whatever speed you so wish)

## Developing without a board?

If you are developing the 'server' side of things and want to try out the code you can run this without any hardware by having a null serial terminal. To do this, in a terminal run:

```
python resources/demoSerial.py
```

then in another terminal run

```
python relayekeysd.py --noserial
```

NB: Only tested on MacOS but should work on any posix system. For Windows simply give a COM port that doesn't exist.
