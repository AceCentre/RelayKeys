# Bluefruit LE Friend

{% hint style="info" %}
Although it _should_ work - and we promise you it _did_ work - something has broken functionality working with the LE friend. So we aren't **officially** supporting this right now
{% endhint %}

* [Install the CP2104 Driver](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers)
* Update it to 0.8.1. Easiest way to do this is to connect to using the Bluefruit app - it will auto-update it if required.
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
