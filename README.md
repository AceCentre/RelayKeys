# RelayKeys

Allow a Computer to mimic a Bluetooth Keyboard(& Mouse). Using some hardware (a couple of different options currently) and a piece of software running on the 'Server' machine - any devices which support Bluetooth LE HID can then recieve the keystrokes.

## Getting Started

There are two different boards to purchase currently (NB: [A range have been looked into](https://forums.adafruit.com/viewtopic.php?f=53&t=145081&start=15) - but its not as straightforward as you would think). Your options:

- [Adafruit Feather nRF52840 Express](https://www.adafruit.com/product/4062) (Buy in the [UK from Pimoroni](https://shop.pimoroni.com/products/adafruit-feather-nrf52840-express))
- [The Adafruit - Bluefruit LE Friend - nRF51822 - v3.0](https://www.adafruit.com/product/2267) (Buy in the [UK from Pimoroni](https://shop.pimoroni.com/products/adafruit-bluefruit-le-friend-ble-4-0-nrf51822-v1-0#description))

### Setup: Bluefruit LE Friend 

#### On the 'Server' (i.e. the machine you will send from)

- [Install the CP2104 Driver](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers)
- Plug it in
- Set the switch on the device to CMD mode
- Open up a serial terminal and connect to the device (See [here](https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/terminal-settings#terraterm-windows-5-2) for exact settings for your Operating System)
- Turn on HID Mode. More info [here](https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/ble-services#at-plus-blehiden-14-31). To be precise - enter this into your serial terminal

	AT+BLEHIDEN=1
	ATZ 

(You should see 'OK' after each entry)

- Next change the default speed. i.e. enter this in your serial terminal:

	AT+BAUDRATE=115200

- Next put the device into [DATA mode](https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/uart-test#blefriend-configuration-6-3) (slide the switch). 


### Setup: Connect the partner/client machine via Bluetooth

This is easy. On your other device connect to the unit as you would any bluetooth keyboard. E.g. Settings->Add Bluetooth Device->Search for device and add the device. 


### Setup: Run the software. 

- You will need Python3 running on your machine
- Install the libraries 

	pip install -r requirements.txt

- A window will appear. Type in it. 
- Done! 


## Authors

* **bbx10** - *Initial work* - [bbx10/haroldpimentel.wordpress.com](https://haroldpimentel.wordpress.com/2016/09/08/bluetooth-keyboard-switch-with-arduino/)

A massive thanks - this was the big breakthrough. You can read the full thread [here](https://forums.adafruit.com/viewtopic.php?f=53&t=145081&start=15)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
