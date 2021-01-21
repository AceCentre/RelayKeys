## Serial Commands

So if you want to communicate directly with the serial device - instead of via the RPC daemon you can. 

## Connection - Baud rate, nr/vid settings

* Baud rate should be 115200 
* Hardware flow control CTS/RTS on
* nrfVID = '239A'
* nrfPID = '8029'

Then you send and receive commands over Serial. The following is a list of the commands and what you should expect to receive back 


## Mouse and Keyboard commands 

### AT+BLEKEYBOARDCODE=KeyboardCode

The good thing about RelayKeys is that we dont try and send actual characters - we send actual keys. This is good - as it means we dont deal with the multilingual problems and different keyboard maps. However - it does mean the the command to send and press a keyboard key can look a little daunting. Here is what it looks like. 

``AT+BLEKEYBOARDCODE=02-00-00-00-00-00-00-00``

This is pretty standard stuff when it comes to a keyboard HID code. E.g. [look at this](https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf) to see what its all about. In short though: 

        Byte 0: Keyboard modifier bits (SHIFT, ALT, CTRL etc)
        Byte 1: reserved
        Byte 2-7: Up to six keyboard usage indexes representing the keys that are 
                  currently "pressed". 
                  Order is not important, a key is either pressed (present in the 
                  buffer) or not pressed.

The letter "a" is usage code 0x04 for example. If you want an uppercase "A", then you would also need to set the Byte 0 modifier bits to select "Left Shift" (or "Right Shift").

Hint: [Look at this file for a way to format this nicely](https://github.com/AceCentre/RelayKeys/blob/69fffd89cf5ace9ee74ed6bc4fe958bff4fb3db2/blehid.py#L222)


### AT+BLEHIDMOUSEMOVE=MouseMoveX,MouseMoveY,0,0

MouseMoveX = Pixels RIGHT and MouseMoveY = Pixels DOWN. So to go RIGHT/UP = use negative numbers. 

e.g. This moves it Right by 10 and Down by 10

``AT+BLEHIDMOUSEMOVE=10,10,0,0``


### AT+BLEHIDMOUSEBUTTON=MouseButton

``	
AT+BLEHIDMOUSEBUTTON=Button[,Action]
``

Button is one of l = Left, r= Right, m=Middle, b=Scroll backward, f=Scroll forward
Action is Click or Doubleclick 

e.g.

*Single click:*

	AT+BLEHIDMOUSEBUTTON=l,click

*Double click:*

	AT+BLEHIDMOUSEBUTTON=l,doubleclick

	

## Connection commands

### AT+BLEADDNEWDEVICE


Adds a new device to the cached list of devices.  After giving this AT command the user should connect with the board via BLE. If connection is successful then the device's name will be added into the list and the board will connect with the device.

Note: A user can only add a new device if the cached list is not full. If the list is full then the board will return with an `Error`. If no new device connects with the board till the timeout (set to 30 seconds), a `Timeout Error` will be returned.

### AT+BLEREMOVEDEVICE="DEVICE_NAME"

This AT command will remove said device's name from the cached list. Device's name should be written between double quotes. You have to be exact with this!  If `device_name` is not found in the list, then the board will return with an `Error`.

If `device_name` is currently connected to a BLE device, then the board will disconnect from this device and then remove device's name from the list.

### AT+BLECURRENTDEVICENAME

This AT command will return the currently connected BLE device's name. If the board is not connected with any BLE device then it will return `NONE`.

### AT+SWITCHCONN

This AT command will switch the  BLE connection to the next device in the cached list.
The board will try to connect with the next listed device till the timeout, then `Timeout Error` will be returned and the board will try to connect with the next  device listed in the cache.. and so on.. 

### AT+PRINTDEVLIST

This AT command will return a list of device names.

### AT+BLEMAXDEVLISTSIZE=NUMBER

This AT command will change the maximum number of BLE devices possible in the cached list.
The number should be greater than 0 and less then 15
