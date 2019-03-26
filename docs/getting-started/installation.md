# ⚙️ Installation

> The easiest way to get up-and-running is with the [Windows Installer](https://github.com/AceCentre/RelayKeys/releases/latest), which includes the RelayKeys-CLI, and the RelayKeys-QT software. Read on to see how to install and setup.  

## A quick reminder of how this works

So RelayKeys consists of a hardware solution that talks Bluetooth HID to secondary devices - anything that can pair with bluetooth and understand a keyboard works, and some software on the 'server' device; i.e. the device sending the key/mouse movements. So for our installation we really focus on the 'server' since the client needs no additional hardware or software.  

![RelayKeys Overview](../img/overview.png)

## Requirements

RelayKeys is designed to work on Windows, Linux, Mac Operating Systems. We have built a Windows installer that makes the process a lot easier on that platform. For Mac & Linux you will need to build the app from source. 

* **Windows 7-10**
* **A USB Port**
* **Ability to Install software as Administrator**
* **A second device to connect to** Could be a Windows computer, a Mac, an iPad etc

and most importantly:

* **A supported piece of RelayKeys ready hardware**
    * Right now:  this is designed to work with the Adafruit nrf52840 express. Others will be added to the list as this is developed. 

::: tip If you have a RelayKeys stick provided by the AceCentre 
Carry on reading below. If you wish to by your own hardware [read this guide](/technical/supported-boards.html). 
:::

## Setup

Download the installer from [here](https://github.com/AceCentre/RelayKeys/releases/latest). When downloaded 'Run' the program 

::: warning The programme is not 'signed' 
This means that you may need to allow it access to your computer to run. Hit 'more' to allow this
:::

Step-through the install procedure. Select 'Normal install' and let the RelayKeys setup software do its thing to install the software in the correct place (By default: C:\Program Files (x86)\AceCentre). 

::: warning If you use 'Portable' or change the location of the software:
Make a note of where you have stored the programme as you will need this when linking it with your software. 
:::


## Plug-in Your RelayKeys stick & pair with a computer

1. Make sure the Micro-USB connector is attached to the stick and then attach the female end of the USB lead into your computer 
2. You should see your stick light a solid blue ("Paired") or flashing blue ("Un-paired")

If "Flashing". This means you have yet to pair the RelayKeys device with another computer. 

### Pair with a Windows Computer 

So to connect to Another Windows computer, go to Settings, Bluetooth, "Add a device", and connect to "RelayKeys"
![Pairing Windows](../img/screenshots/windows-pairing.gif)

### Pair with an iOS device

To connect to an iPad/iPhone, go to Settings, Bluetooth and add "Bluefruit52" or "RelayKeys"
![Pairing iPad](../img/screenshots/ipad-pairing.gif)

### Pair with a Mac

To connect to a mac, Open up "System Preferences", Bluetooth and add "RelayKeys"

![Pairing Mac](../img/screenshots/mac-pairing.gif)

## Checking it works

1. Open up something on the second computer that you can enter text into. E.g. Notes on the iPad, Notepad on Windows or Notes on a mac
2. On your server computer (the one with RelayKeys attached) run "RelayKeys" (search for it in your Windows search bar). Alternatively find it in ``C:\Program Files(x86)\AceCentre\RelayKeys\relaykeys-qt.exe``
3. With the window having focus - type into it. You should see the keystrokes appear on the second computer 

## Using it with your AAC software

You can get going by using one of these example files that work with your AAC Software:

* [The Grid 3](https://www.dropbox.com/s/3mcvnpnyi36lpdh/RelayKeysDemo.gridset?dl=1)
* [MindExpress](https://www.dropbox.com/s/4z194iwf90kzfwj/RelayKeys%20sample%20demo.jmm?dl=1)
* Tobii Communicator
* Dynavox Series 5

When you are ready, [have a read of how to integrate the features you need](/guides/basic-principles.html). 

---

👍 You've successfully installed and setup RelayKeys! Now you may want to use the CLI or QT program. Read on to find out how these work. 

😞 Got a problem? Dang! See our [troubleshooting](/getting-started/contributing.md) guide. 
