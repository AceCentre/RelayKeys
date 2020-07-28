Daemon reference
===========================

The daemon (or RPC server) is the component that opens up a connection to the COM port and sends the correct AT command to the board. You can control it with some arguments

## --noserial

Run the daemon and dont try and connect to hardware. If you are on linux/MacOS you can fake a serial port [following these tips](/developers/supported-boards.html#developing-without-a-board). If you are on Windows just fix a COM port in the config file or use the ``--dev`` option - just choose a non-existent COM port

## --dev 

Force the daemon to use a COM port rather than auto detecting one. 

e.g. 

``python relaykeysd.py --noserial --dev=COM7``

## --debug

Sets a more verbose debugging output on the console. 

## --pidfile=file

Give a pidfile for the daemon to crate - or link to one.

**Default: pidfile**

## --logfile=logfile

File to use as a log file for the debugging messages. 

**Default: logfile**

## --config=configfile

File to use as a config file

**Default: relaykeys.cfg**
