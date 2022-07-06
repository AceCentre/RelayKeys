# RelayKeys

Allow a Computer to mimic a Bluetooth Keyboard (& Mouse). 
Using some hardware (a couple of different options currently) and a piece of software running on the 'Server' machine - any devices which support Bluetooth LE HID can then receive the keystrokes. **For full documentation (and updated docs!) see https://docs.acecentre.org.uk/products/v/relaykeys/**

<!--ts-->
   * [RelayKeys](#relaykeys)
      * [Why?](#why)
      * [Getting Started](#getting-started)
         * [Don't have any hardware yet? Want to see what the software does?](#dont-have-any-hardware-yet-want-to-see-what-the-software-does)
         * [1. Setup: Adafruit Feather nRF52840 Express](#1-setup-adafruit-feather-nrf52840-express)
         * [2. Setup: Connect the partner/client machine via Bluetooth](#2-setup-connect-the-partnerclient-machine-via-bluetooth)
         * [3. Setup: Run the software.](#3-setup-run-the-software)
      * [How does this all work?](#how-does-this-all-work)
      * [Anatomy of the files](#anatomy-of-the-files)
      * [License](#license)
      * [Credits](#credits)

<!-- Added by: willwade, at:  -->

<!--te-->

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

	pip install -r requirements.txt
	python relaykeysd.py


then in another terminal run

	python relaykeys-cli.py --noserial type:Hello

(Yes 3 - terminals. One is pretending to be a serial port, the other is the RPC server - and the last is the relaykeys client) NB: Only tested on MacOS but should work on any posix system


### 1. Setup: Adafruit Feather nRF52840 Express

- Check the setup of your [Arduino IDE](https://learn.adafruit.com/bluefruit-nrf52-feather-learning-guide/arduino-bsp-setup) (remember we're using the nRF52840 board!)
- Upload the [sketch](arduino_nRF52840/arduino_nRF52840.ino) to your feather. 
- Run the server side code
- Done!  

### 2. Setup: Connect the partner/client machine via Bluetooth

This is easy. On your other device connect to the unit as you would any bluetooth keyboard. E.g. Settings->Add Bluetooth Device->Search for device and add the device. 


### 3. Setup: Run the software. 

You currently have two options for this - 1. Run the precompiled binaries or 2. Use the python code on its own

#### 3.1 Precompiled binaries

There is a number of exe's available

You can try running the installer package (see releases). Note that on Windows - finding your dongle isn't reliable yet. You will more than likely need to find which COM port the device is on (look in device manager) - and add it to the relaykeys.cfg under the server. e.g.

	dev = COM6

Once installed - you can test it by opening the C:\Program Files(x86)\AceCentre\RelayKeys\relaykeys-qt.exe  and type in the box. For working with the Grid etc you will want to call the relaykeys-cli-win.exe in this directory. 



## To build

You need [nsis](http://nsis.sourceforge.io) installed for this next part. 

	pip install -r requirements.txt
	python build.py 

You will then get a setup.exe


## How does this all work? 

Although there are two bits of hardware identified you can do this with other Bluetooth boards. The essential element is being able to transmit at a high enough speed, reliably, over the serial port of the computer (what we are defining as the 'server' in this context). 

## Anatomy of the files

* ``arduino/`` - firmware for the arduino board
* ``docs/``  - VuePress docs for http://acecentre.github.io/relayKeys/. Build Script is **docs-deploy.sh**
* ``resources/`` - Helper files for development (e.g. ``demoSerial.py`` which pretends to be an arduino board connected, viewComPorts which outputs the connected com ports), AAC software pagesets and all-keys.txt which is a output of all the keys supported by RelayKeys. Also note the development files - ``relaykeys-pygame`` and ``relaykeys.py`` - which are stripped down versions of the whole project. Useful for debugging and testing things without the daemon server. Just move ``relaykeys.py`` into the root directory to get it to work. 
* ``blehid.py`` - Library/Import file used by relaykeysd. Includes the function that writes the AT command to the serial port, init the serial port, and sends keyboard/mouse codes. 
* ``build.py``, ``buildinstaller.nsi`` - Build files to turn this project into a installer. Run ``python build.py`` to trigger the build. 
* ``docs-deploy.sh`` - deploys the documentation to the github pages site. 
* ``relaykeys-cli.py`` - This is the command line interface version of relaykeys. Conencts to the daemon server. 
* ``relaykeys-example.cfg`` - The default config file. Note this gets copied on install to the right location and is used as the standard config. Note commented out baud and dev lines. Dev fixes the ``COM`` port if the com port finding code doesn't work
* ``relaykeys-qt.py`` - The GUI version of our relakeys testing app. 
* ``relaykeys.spec.ini`` - Used for the NSIS build (i.e. ``buildinstaller.nsi``)
* ``relaykeysclient.py`` - The main library file used by -cli and -qt versions. Connects to the server. 
*  ``relaykeysd-service-restart.bat``, ``relaykeysd-service.py`` - The Windows service applcation
* ``relaykeysd.py`` - The daemon. This is what is run in the background - and controlled by the service. If you want to test RelayKeys - run this file first - and leave it running. e.g. ``python relakyeysd.py &&``. Note the command line flags in the header. 


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Credits

- [bbx10](https://forums.adafruit.com/viewtopic.php?f=53&t=145081&start=15) on the Adafruit forums who got this up and running. Awesome. 
- [Keyboard](https://thenounproject.com/search/?q=keyboard&i=1442359) by Atif Arshad from the Noun Project
- [Bluetooth](https://thenounproject.com/search/?q=bluetooth&i=1678456) by Adrien Coquet from the Noun Project
