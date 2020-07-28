# Config File details

## Introduction

In the same directory as relaykeys there is a file ``relaykeys.cfg`` 

It looks like this:

	[server]
	host = 127.0.0.1
	port = 5383
	username = relaykeys
	password = QTSEOvmXInmmp1XHVi5Dk9Mj
	logfile = logfile.txt

	[client]
	host = 127.0.0.1
	port = 5383
	username = relaykeys
	password = QTSEOvmXInmmp1XHVi5Dk9Mj
	toggle = 1
	togglekey = A
	togglemods = RALT


Feel free to change any of the settings but **Be careful that you make the username/password the same** - otherwise the CLI programme can't talk to the service. 


## Dev - Defining your port of the RelayKeys hardware


RelayKeys software tries to find the RelayKeys board automagically. If you have a device with a number of COM ports attached - or ones that have similar functionality you may have some difficulties. If so try *fixing* the COM port.

1. Access Device Manager. Search for "Device Manager" in Windows. 

[![Image from Gyazo](https://i.gyazo.com/0b327be4a6ad9ea569da378e1f1d7a1a.gif)](https://gyazo.com/0b327be4a6ad9ea569da378e1f1d7a1a)

2. Click on Ports. If you only have RelayKeys connected you should see one device. If you see many - try unplugging it and replugging it in to find which COM port it is. 

[![Image from Gyazo](https://i.gyazo.com/0b327be4a6ad9ea569da378e1f1d7a1a.gif)](https://gyazo.com/0b327be4a6ad9ea569da378e1f1d7a1a)

3. Note the number and edit your RelayKeys cfg file. Search for "RelayKeys config" in Windows - and open with Notepad. 

[![Image from Gyazo](https://i.gyazo.com/427603ca7c287942ad92ccd823c0f64d.gif)](https://gyazo.com/427603ca7c287942ad92ccd823c0f64d)

4. Type ``dev = COM3`` where **COM3** is your port number you found in step 2-3. 

