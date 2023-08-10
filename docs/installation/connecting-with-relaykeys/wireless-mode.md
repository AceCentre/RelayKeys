# Wireless Mode



{% hint style="warning" %}
Warning: This mode definitley is slightly more laggy and can be fiddly to setup.&#x20;
{% endhint %}

Note that this mode is useful on devices where you can't plug anything into your device. The setup can feel _strange -_ what we need to do is tell your relaykeys hardware the device to connect to.

1. Plug in device and follow instructions [as above](wireless-mode.md#plug-in-your-relaykeys-stick-and-pair-with-a-computer-wired-mode)
2. Pair the main AAC/Host device with it. So pair the computer you have attached it to with RelayKeys hardware. This can feel a bit strange - you are connecting the hardware to the same machine you are on. See [here](wireless-mode.md#undefined-1) for how to put it into pairing mode.
3. Disconnect the relaykeys hardware. In your bluetooth settings you actually need to click on the item and "Remove" device. (NB: If you cant do this it might be because you need to be an admin. The trick is open the Control Panel -> Devices & Printers -> Relaykeys -> Right click, Remove and you will be asked for an Admin password)
4. Plug relaykeys into a power source - away from the computer. Your RelayKeys may have a battery or you might need to plug into a wall USB power source.
5. Double press the User switch It should now shine a nice <mark style="color:blue;">blue</mark> colour!
6. Run RelayKeysd with `--ble_mode` See [here](../../developers/relaykeys-daemon.md) for more details
