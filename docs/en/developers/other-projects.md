# Prior Art/Related Projects

### Other projects / Similar work / Inspiration

* [The original RelayKeys from Harold Pimental](https://haroldpimentel.wordpress.com/2016/09/08/bluetooth-keyboard-switch-with-arduino/).
* **bbx10** on the adafruit forums. **bbx10** developed the Ascii to HID translation function. A massive thanks - the code is currently mostly his. He also worked out some of the early problems on speed issues we were having. You can read the full thread [here](https://forums.adafruit.com/viewtopic.php?f=53\&t=145081\&start=15).
* [HID-Relay](https://github.com/juancgarcia/HID-Relay) from [juancgarcia](https://github.com/juancgarcia). Not really spent much time looking at this - but looks neat. Converts hardware keyboards to Bluetooth.
* [232Key](https://www.232key.com/index.html) - Converts Serial devices to Keyboard. Kind of the other way round to what we want.
* [BL\_keyboard\_RPI](https://github.com/quangthanh010290/BL\_keyboard\_RPI). Turns a Pi into keyboard emulator
* [ESP32\_mouse\_keyboard](https://github.com/RoganDawes/esp32\_mouse\_keyboard). Uses a ESP32 as a mouse/keyboard over serial. Very similar idea. (See [issue 39](https://github.com/AceCentre/RelayKeys/issues/29)for details about this in relation to using VNC (TY [@RoganDawes](https://github.com/RoganDawes))

### AAC projects

* [MacroServerMac](http://github.com/willwade/MacroServerMac) was an attempt to create a Mac Port of "MacroServer" developed by [JabblaSoft](http://jabblasoft.com) for MindExpress . This is a protocol for communication over a TCP/IP stack. Its pretty nice - but if you are in a school or business allowing others machines to access the network in this way is often restricted. It can also be pretty flaky
* [Liberator](http://liberator.co.uk) / [PRC](http://prentrom.com) - have the neatest commercial solution out there for AAC. You can either plug in a USB cable - or use a bluetooth dongle to connect with another computer. Its awesome - but sadly only available to you if use one of their devices.
* [Dynavox](http://tobiidynavox.com) used to make the [AccessIT](http://www.spectronics.com.au/product/accessit). A similar idea but using infrared rather than radio/bluetooth. It was pretty expensive but a lot of people loved its simplicity. More recently they have brought this back to life with [AccessIT 3](https://www.tobiidynavox.com/products/accessit-3). Note it only works in Snap software - and not for any device. Just another windows device. You also need a USB port on the device you connect to.&#x20;
* The AAC world has been trying to create standards for this for years.. and some have succeeded. Check out [AACKeys](https://aacinstitute.org/aac-keys/) and the "GIDEI" protocol - which now feels a little outdated but a great attempt at standardising communication between AAC devices and other systems over serial.

### Non-disability related products

* the [Buffalo BSHSBT04BK](http://buffalo.jp/product/peripheral/wireless-adapter/bshsbt04bk/) was pretty neat. You can still get this in Japan and does a very similar job
* The [IOGEAR KeyShair](https://www.iogear.com/product/GKMB02) (now discontinued) looked like exactly the same dongle - but with different software.

Both of these products though failed to respond to software (on-screen) keyboards reliably.
