# Tobii Communicator 5

[Communicator 5](https://www.tobiidynavox.com/pages/communicator-5-ap) is a AAC software for Tobii Dynavox communication aids . Follow the steps below to add commands to your pageset

{% hint style="info" %}
Pageset quick start.  Want a headstart? Download the Pageset here. It has all the commands you should need. Just import, add the pageset to your Home Page and adapt&#x20;

![](<../.gitbook/assets/communicator5_pageset.png>)

{% endhint %}

## Sending the message bar

This is the best way to enter longer texts and allows you to use the communication aid's prediction and phrase banks etc. Use the "Copy" command followed the Run Program command to run relaykeys-cli-win.exe with the **paste** argument

![](<../.gitbook/assets/communicator5_text_paste.png>)

## Simple keystrokes

This is useful for making a keyboard-like page with individual letters and other keys that send one keystroke at a time. Use the Run Program command to run relaykeys-cli-win.exe with the **keypress:LETTER** argument (where letter is the key you want to send)

![](<../.gitbook/assets/communicator5_keypress.png>)


## Sending keyboard shortcuts

For special commands and shortcuts such as control-C, alt-F4 etc use the Run Program command to run relaykeys-cli-win.exe with the **keypress:KEYNAME,MODIFIER** argument (where keyname is the key you want to send)

![](<../.gitbook/assets/communicator5_navigation_shortcut.png>)

## Sending mouse commands

Use the Run Program command to run relaykeys-cli-win.exe with the **mousemove:X,Y** argument (where X,Y is the distance you want to move the mouse), or the **mousebutton:BUTTON,ACTION** argument (where BUTTON is the button to use, and ACTION is click or doubleclick etc.)

![](<../.gitbook/assets/communicator5_navigation_mousemove.png>)

![](<../.gitbook/assets/communicator5_navigation_mousebutton.png>)

## Controlling RelayKeys

Use the Run Program command to run relaykeys-cli-win.exe with the ble-cmd:reconnect, ble-cmd:switch, or ble-cmd:devname --notify  commands

![](<../.gitbook/assets/communicator5_control_reconnect.png>)

![](<../.gitbook/assets/communicator5_control_switchnotify.png>)

