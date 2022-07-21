# Command Line Usage

### Command Line flags

We have created a command line interface which allows you to send mouse and keyboard commands to your RelayKeys hardware.

To run it access

`relaykeys-cli.exe command:data`

or if running it in pure python

`python relaykeys-cli.py command:data`

and the non-verbose, non-windowed version

`python relaykeys-cli-win.py command:data`

Where 'command' and 'data' are provided below.

{% hint style="info" %}
Remember to change your application accordingly We regularly use the term for  command line application '_relaykeys-cli_'  in this documentation. Often though you will want to use the '**relaykeys-cli-win.exe**' application that will run a little quicker and has no printed output. Use this for your default call to relaykeys from other applications. If you want to see any errors use '_relaykeys-cli.exe_'
{% endhint %}

{% hint style="info" %}
If you are developing with the code You must make sure the server  is running when you call the cli files. The [server (aka Daemon)](relaykeys-daemon.md) is the code that turns these commands into the correct AT syntax and access the com port
{% endhint %}

### Defining a Keymap -c

Keymap files are located in [**cli\_keymap**](https://github.com/AceCentre/RelayKeys/tree/master/cli\_keymaps) folder. You can choose which keymap file the CLI is going to use in the cfg by assigning file name to keymap\_file variable (see [here](https://github.com/AceCentre/RelayKeys/blob/12d3eadca2cea53561a5a3979562aae8b4b6cd7c/relaykeys-example.cfg#L17))

By default the **us\_keymap.json** is loaded.\
\
To run relaykeys-cli with other keymap either change the cfg setting [or use the -c flag](relaykeys-cfg.md) on the cli application. E.g.

`relaykeys-cli.exe -c .\relaykeys-example.cfg type:@`

See more info on the format [here](relaykeys-cfg.md#introduction)

### Command: paste

This takes the pasteboard of the computer (i.e. when you copy some text) and pastes the resulting string to RelayKeys

i.e.

`relaykeys-cli.exe paste`

### Command: type:text

Types the string following the :. Note you will need to escape spaces etc

`relaykeys-cli.exe type:Hello\ World`

#### A special note about type/paste

You can send special characters, ones that are usually shifted, by sending the key and the shift modifier (see **keyevent** below). But for the type and paste commands we have some other characters that are hardcoded and it will do the conversion on the fly.

So for example, to send the @ symbol:

`relaykeys-cli.exe type:@`

All codes which are converted can be seen below. **NB: \t = Tab \r\n are line breaks\~**

### Command: keypress:KEY,MODIFIER

Sends the KEY and any modifier, For example:

`relaykeys-cli.exe keypress:A`

Will emulate pressing and releasing the letter `A`. What about a shift?

`relaykeys-cli.exe keypress:A,LSHIFT`

Will emulate pressing the A with Left Shift. i.e. Upper casing the A.

`relaykeys-cliexe keypress:RIGHTARROW,LSHIFT,LCTRL`

Will press the right arrow, left shit and left control (would select the next word in programs like word)

#### Modifiers

* Left Control/CTRL: `LCTRL`
* Left Shift : `LSHIFT`
* Left Alt/Alt: `LALT`
* (Left) Meta/Windows Key/Mac Key/Command Key: `LMETA` **Note: On Windows there is generally only one Windows key. So use LMETA to emulate pressing the Windows key**
* Right Control/CTRL:: `LCTRL`
* Right Shift : `RSHIFT`
* (Right) Meta/Windows Key/Mac Key/Command Key: `RMETA`

So all the other keys are defined below. We will try and explain what these are when its ambiguous

<details>

<summary>Keys</summary>

* 0
* 1
* 2
* 3
* 4
* 5
* 6
* 7
* 8
* 9
* A
* B
* C
* D
* E
* F
* G
* H
* I
* J
* K
* L
* M
* N
* O
* P
* Q
* R
* S
* T
* U
* V
* W
* X
* Y
* Z
* BACKSPACE - Back Delete key
* ENTER - Return
* DELETE - Forward delete key
* TAB
* PAUSE
* ESCAPE
* SPACE
* QUOTE
* COMMA
* MINUS
* PERIOD
* SLASH
* SEMICOLON
* EQUALS
* LEFTBRACKET
* BACKSLASH
* RIGHTBRACKET
* BACKQUOTE
* KP0
* KP1
* KP2
* KP3
* KP4
* KP5
* KP6
* KP7
* KP8
* KP9
* KP\_PERIOD
* KP\_DIVIDE
* KP\_MULTIPLY
* KP\_MINUS
* KP\_PLUS
* KP\_ENTER
* KP\_EQUAL - Keypad =
* KP\_COMMA
* KP\_EQSIGN
* UP
* DOWN
* RIGHT
* LEFT
* INSERT
* HOME
* END
* PAGEUP
* PAGEDOWN
* F1
* F2
* F3
* F4
* F5
* F6
* F7
* F8
* F9
* F10
* F11
* F12
* NUMLOCK
* CAPSLOCK
* SCROLLOCK
* RIGHTARROW
* LEFTARROW
* DOWNARROW
* UPARROW
* APP
* LGUI - Keyboard Left GUI
* RGUI - Keyboard Right GUI
* CUSTOM\~ - Keyboard Non-US # and \~
* PRINTSCREEN
* POWER
* EXECUTE
* HELP
* MENU
* SELECT
* STOP
* AGAIN
* UNDO
* CUT
* COPY
* PASTE
* FIND
* MUTE
* VOLUP
* VOLDOWN
* LOCKING\_CAPSLOCK
* LOCKING\_NUMLOCK
* LOCKING\_SCROLLOCK
* ALTERASE
* ATTENTION
* CANCEL
* CLEAR
* PRIOR
* RETURN
* SEPARATOR
* OUT 0xA0
* OPER 0xA1&#x20;

</details>

### Command: keyevent:KEY,MODIFIER,Up/Down

Emulates holding or releasing one key with a modifer. For example:

`relaykeys-cli.exe keyevent:A,LSHIFT,1`

Emulates pressing a `A` with `Shift` Down. To release:

`relaykeys-cli.exe keyevent:A,LSHIFT,0`

So a classic example is to emulate pressing the Alt key and Tab key. Commonly used to switch applications. To do this you would need to send two commands.

```
    relaykeys-cli-win.exe" keyevent:TAB,LALT,1
    relaykeys-cli-win.exe" keyevent:TAB,LALT,0
```

### Command: mousemove:PixelsRight,PixelsDown

Sends the command to move the mouse x Pixels Right and x Pixels Down. To go in the other direction send negative numbers. Eg. To go Right by 10 and Down by 10

`relaykeys-cli.exe mousemove:10,10`

and Left by 10, Up by 10:

`relaykeys-cli.exe mousemove:-10,-10`

Straight up:

`relaykeys-cli.exe mousemove:0,-10`

Straight down:

`relaykeys-cli.exe mousemove:0,10`

Straight right:

`relaykeys-cli.exe mousemove:10,0`

Straight left:

`relaykeys-cli.exe mousemove:-10,0`

### Command: mousebutton:Button,Behaviour

Sends the Mouse button press. Mouse buttons available:

* L: Left
* R: Right
* M: Middle
* F: Scroll Forward
* B: Scroll Backward

Behaviours:

* click
* doubleclick

Note: If you don't provide a behaviour it will hold and release the button for 0 Seconds.

Send a doubleclick:

`relaykeys-cli.exe mousebutton:L,doubleclick`

Send a right click:

`relaykeys-cli.exe mousebutton:R,click`

**What about dragging?**

Activate Drag Start button&#x20;

`relaykeys-cli mousebutton:L,press`&#x20;

User moves mouse&#x20;

`relaykeys-cli mousemove:x,y`&#x20;

User moves mouse some more&#x20;

`relaykeys-cli mousemove:x,y`&#x20;

user activates Drag Stop button&#x20;

`relaykeys-cli mousebutton:0`

### Command: delay: nms

Adds a delay. Particularly useful when writing a macro and you need to wait for something to happen on the client operating system.&#x20;

`relaykeys-cli delay:1000`

Puts in a a delay of 1 second.&#x20;

### Device Management Commands

#### Optional extra flag --notfiy

On the following commands you can provide a `--notify` flag. If so your Operating System will return a system notification. Useful if you dont have access to view the command line.&#x20;

`relaykeys-cli.exe ble_cmd:devlist`

Gets a list of devices that the device has in memory

`relaykeys-cli.exe ble_cmd:devadd`

Put the device into a pairing state

`relaykeys-cli.exe ble_cmd:devreset`

Reset the entire stored devices (its like wiping the volatile memory)

`relaykeys-cli.exe ble_cmd:switch`

Switch the current connected device to the next one in RelayKeys memory

`relaykeys-cli.exe ble_cmd:devremove=DEVNAME`

Remove just one named device from the memory.

`relaykeys-cli.exe ble_cmd:reconnect`

Tells the daemon/server to try and reconnect to the serial port.

`relaykeys-cli.exe daemon:switch_mode`

Tells the daemon/server to try and switch between wired

`relaykeys-cli.exe daemon:get_mode`

Returns current mode&#x20;

`relaykeys-cli.exe daemon:dongle_status`

Returns whether it is connected or not

### Command: -f file.txt (Macro)

Provide a macro file - where each line in a text file is a cli command.  For example **ios\_open\_notes.txt** found in the _macros_ directory of the installation folder (i.e at _C:\Program Files (x86)\Ace Centre\RelayKeys\maccros)_

`relaykeys-cli.exe -f ios_open_notes.txt`

or like this&#x20;

`relaykeys-cli.exe -f Documents/open_ios_notes.txt`

where it reads the file from a file path.. or..\
\
`relaykeys-cli.exe -f ./open_ios_notes.txt`&#x20;

where it reads the file in folder where current exe is run from\


where ios\_open\_notes.txt is:

```
keypress:H,LMETA
keypress:SPACE,LMETA
type:notes
delay:500
keypress:ENTER
```

{% hint style="info" %}
Warning: There is no syntax checking of this document.&#x20;
{% endhint %}

{% hint style="info" %}
Want to send a long string of mouse commands and want to record your movements for a script? Start by using [https://github.com/rmpr/atbswp](https://github.com/rmpr/atbswp) - You'll need to edit the file but its a handy starting point
{% endhint %}
