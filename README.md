# RelayKeys

Allow a Computer to mimic a Bluetooth Keyboard (& Mouse). Using some hardware (a couple of different options currently) and a piece of software running on the 'Server' machine - any devices which support Bluetooth LE HID can then receive the keystrokes.

<!--ts-->
<!--te-->

   * [RelayKeys](#relaykeys)
      * [Why?](#why)
      * [Getting Started](#getting-started)
         * [Don't have any hardware yet? Want to see what the software does?](#dont-have-any-hardware-yet-want-to-see-what-the-software-does)
         * [Setup: Adafruit Feather nRF52840 Express](#setup-adafruit-feather-nrf52840-express)
         * [Setup: Bluefruit LE Friend](#setup-bluefruit-le-friend)
         * [Setup: Connect the partner/client machine via Bluetooth](#setup-connect-the-partnerclient-machine-via-bluetooth)
         * [Setup: Run the software.](#setup-run-the-software)
      * [How does this all work?](#how-does-this-all-work)
      * [Other projects / Similar work / Inspiration](#other-projects--similar-work--inspiration)
         * [And on the AAC side of things:](#and-on-the-aac-side-of-things)
         * [Non-disability related products:](#non-disability-related-products)
      * [License](#license)
      * [Credits](#credits)

## Why?

Well a range of purposes. For some - its just a convenient way of saving some money on a [KVM switch](https://en.wikipedia.org/wiki/KVM_switch) - or replacing now hard to find [commercial solutions](https://github.com/AceCentre/RelayKeys#non-disability-related-products). 

For the [AceCentre](http://acecentre.org.uk) we want people with disabilities who are forced to use one system (e.g. a dedicated Eyegaze system) to be able to access other computers and systems they may need to use for work or leisure. This has only been available on a couple of commercial AAC systems - and often need to be on the same network which is sadly often impossible in schools or government workplaces - Or they do work over bluetooth but for only one system in the field exists like this (see [here for more details on these](#and-on-the-aac-side-of-things)). 

![Image of Person Using AAC](https://acecentre.org.uk/wp-content/uploads/2017/05/Helping-children-with-AAC-needs-1280x492.jpg)


## Getting Started

There are two different boards to purchase currently (NB: [A range have been looked into](https://forums.adafruit.com/viewtopic.php?f=53&t=145081&start=15) - but its not as straightforward as you would think). Your options:

- [Adafruit Feather nRF52840 Express](https://www.adafruit.com/product/4062) (Buy in the [UK from Pimoroni](https://shop.pimoroni.com/products/adafruit-feather-nrf52840-express)). Carry on reading to know how set this up (to-do)
- [The Adafruit - Bluefruit LE Friend - nRF51822 - v3.0](https://www.adafruit.com/product/2267) (Buy in the [UK from Pimoroni](https://shop.pimoroni.com/products/adafruit-bluefruit-le-friend-ble-4-0-nrf51822-v1-0#description)). Carry on reading [here to see how to set this up](#setup-bluefruit-le-friend). 


### Don't have any hardware yet? Want to see what the software does?

If you are developing the 'server' side of things and want to try out the code you can run this without any hardware by having a null serial terminal. To do this, in a terminal run:

	python resources/demoSerial.py

then in another terminal run

	python relayeKeys.py no-serial

NB: Only tested on MacOS but should work on any posix system


### Setup: Adafruit Feather nRF52840 Express

- Upload the [sketch](arduino_nRF52840.ino) to your feather. 
- Run the server side code
- Done!  

### Setup: Bluefruit LE Friend 

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

## How does this all work? 

Although there are two bits of hardware identified you can do this with other Bluetooth boards. The essential element is being able to transmit at a high enough speed, reliably, over the serial port of the computer (what we are defining as the 'server' in this context). 

## Other projects / Similar work / Inspiration

- [The original RelayKeys from Harold Pimental](https://haroldpimentel.wordpress.com/2016/09/08/bluetooth-keyboard-switch-with-arduino/). 
- **bbx10** on the adafruit forums. **bbx10** developed the Ascii to HID translation function. A massive thanks - the code is currently mostly his. He also worked out some of the early problems on speed issues we were having. You can read the full thread [here](https://forums.adafruit.com/viewtopic.php?f=53&t=145081&start=15).
- [HID-Relay](https://github.com/juancgarcia/HID-Relay) from [juancgarcia](https://github.com/juancgarcia). Not really spent much time looking at this - but looks neat. Converts hardware keyboards to Bluetooth. 

### And on the AAC side of things:

- [MacroServerMac](http://github.com/willwade/MacroServerMac) was an attempt to create a Mac Port of "MacroServer" developed by [JabblaSoft](http://jabblasoft.com) for MindExpress . This is a protocol for communication over a TCP/IP stack. Its pretty nice - but if you are in a school or business allowing others machines to access the network in this way is often restricted. It can also be pretty flaky
- [Liberator](http://liberator.co.uk) / [PRC](http://prentrom.com) - have the neatest commercial solution out there for AAC. You can either plug in a USB cable - or use a bluetooth dongle to connect with another computer. Its awesome. 
- [Dynavox](http://tobiidynavox.com) used to make the [AccessIT](http://www.spectronics.com.au/product/accessit). A similar idea but using infrared rather than radio/bluetooth. 
- The AAC world has been trying to create standards for this for years.. and some have succeeded. Check out [AACKeys](https://aacinstitute.org/aac-keys/) and the "GIDEI" protocol - which now feels a little outdated but a great attempt at standardising communication between AAC devices and other systems over serial. 

### Non-disability related products:

- the [Buffalo BSHSBT04BK](http://buffalo.jp/product/peripheral/wireless-adapter/bshsbt04bk/) was pretty neat. You can still get this in Japan and does a very similar job
- The [IOGEAR KeyShair](https://www.iogear.com/product/GKMB02) (now discontinued) looked like exactly the same dongle - but with different software.

Both of these products though failed to respond to software (on-screen) keyboards reliably. 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Credits

- [bbx10](https://forums.adafruit.com/viewtopic.php?f=53&t=145081&start=15) on the Adafruit forums who got this up and running. Awesome. 
- [Keyboard](https://thenounproject.com/search/?q=keyboard&i=1442359) by Atif Arshad from the Noun Project
- [Bluetooth](https://thenounproject.com/search/?q=bluetooth&i=1678456) by Adrien Coquet from the Noun Project