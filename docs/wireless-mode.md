# Wireless Mode

By default RelayKeys is designed to be plugged into one computer (the sending machine) and then connects to devices over bluetooth. \
\
It also can be used in a wireless mode - where it just requires power and both sides are connected wirelessly.

Here are instructions for setting device in BLE mode.

1. Add host device which will be running relaykeys into device list of nrf52840.(Needed only once for host device)

1.a nrf52840 should be in serial mode.\
1.b Trigger adding device from cli, qt-app, or by pressing button.\
1.c Connect to nrf52840 with your host device.\
1.d After connection was established and device name was added you need to disconnect your host device from nrf52840.\
Later relaykeysd will be making connecting automatically.\
2\. Reupload Arduino sketch of nrf52840 with ble\_mode flag set to true.\
3\. Start relaykeysd with '--ble\_mode' option
