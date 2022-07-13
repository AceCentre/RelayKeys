# Daemon reference

The daemon (or RPC server) is the component that opens up a connection to the COM port and sends the correct AT command to the board. You can control it with some arguments

When you use our installer it installs this as a service. If you run the code without installing (or you turn the service off for some reason) you can run it as `relaykeysd.py` or `relaykeysd.exe`&#x20;

## --noserial

Run the daemon and dont try and connect to hardware. If you are on linux/MacOS you can fake a serial port [following these tips](supported-boards.md#developing-without-a-board). If you are on Windows just fix a COM port in the config file or use the `--dev` option - just choose a non-existent COM port

## --dev

Force the daemon to use a COM port rather than auto detecting one.

e.g.

`python relaykeysd.py --noserial --dev=COM7`

For more info see [here](../../developers/relaykeys-cfg.html#dev-defining-your-port-of-the-relaykeys-hardware)

## --debug

Sets a more verbose debugging output on the console.

## --pidfile=file

Give a pidfile for the daemon to crate - or link to one.

**Default: pidfile**

## --logfile=logfile

File to use as a log file for the debugging messages.

**Default: logfile**

## --config=configfile

File to use as a config file. For more info see [here](relaykeys-cfg.md)

**Default: relaykeys.cfg**

## --**ble\_mode=True|False**

Use the daemon in wireless (ble\_mode) or wired mode.

**Default: false**
