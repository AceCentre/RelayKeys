# RelayKeys

Allow a Computer to mimic a Bluetooth Keyboard(& Mouse). Using some hardware (a couple of different options currently) and a piece of software running on the 'Server' machine - any devices which support Bluetooth LE HID can then recieve the keystrokes.

## Why?

Well a range of purposes. For some - its just a convient way of saving some money on a [KVM switch](https://en.wikipedia.org/wiki/KVM_switch) - or replacing now hard to find commerical solutions (e.g. the [Buffalo BSHSBT04BK](http://buffalo.jp/product/peripheral/wireless-adapter/bshsbt04bk/) or the [IOGEAR KeyShair](https://www.iogear.com/product/GKMB02)). (Also [read this blopost on The Farrago for a different set of reasons](https://haroldpimentel.wordpress.com/2016/09/08/bluetooth-keyboard-switch-with-arduino/)). 

For the AceCentre we want people with disabilities who are forced to use one system (e.g. a dedicated Eyegaze system) to be able to access other computers and systems they may need to use for work or leisure. This has only been available on a few systems - and either rely on a piece of software running on the 'client' (i.e. receiving ) machine - and often on the same network (a great idea (thanks to [Jabbla doing this](http://jabblasoft.com) but sadly often impossible in schools or government workplaces) - Or over bluetooth but for only one system (Congrats [Prente Romiche](http://prentrom.com) who have been doing this for years). 

Back story.. The AAC world has been trying to create standards for this for years.. and some have succeeded. Check out [AACKeys](https://aacinstitute.org/aac-keys/) - which now feels a little outdated but a great attempt at standardising communication between AAC devices and other systems. 

![Image of Person Using AAC](https://acecentre.org.uk/wp-content/uploads/2017/05/Helping-children-with-AAC-needs-1280x492.jpg)


## Getting Started

There are two different boards to purchase currently (NB: [A range have been looked into](https://forums.adafruit.com/viewtopic.php?f=53&t=145081&start=15) - but its not as straightforward as you would think). Your options:

- [Adafruit Feather nRF52840 Express](https://www.adafruit.com/product/4062) (Buy in the [UK from Pimoroni](https://shop.pimoroni.com/products/adafruit-feather-nrf52840-express)). Carry on reading to know how set this up (to-do)
- [The Adafruit - Bluefruit LE Friend - nRF51822 - v3.0](https://www.adafruit.com/product/2267) (Buy in the [UK from Pimoroni](https://shop.pimoroni.com/products/adafruit-bluefruit-le-friend-ble-4-0-nrf51822-v1-0#description)). Carry on reading [here to see how to set this up](#setup-bluefruit-le-friend). 


### Don't have any hardware yet? 

Alternatively you can try out the code without any hardware. To do this, in a terminal run:

	python resources/demoSerial.py

then in another terminal run

	python relayeKeys.py no-serial


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


## Thanks

- [Keyboard](https://thenounproject.com/search/?q=keyboard&i=1442359) by Atif Arshad from the Noun Project
- [Bluetooth](https://thenounproject.com/search/?q=bluetooth&i=1678456) by Adrien Coquet from the Noun Project