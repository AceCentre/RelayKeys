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

::: tip Remember to change your application accordingly We regularly use the verbose command line application 'relaykeys-cli' in this documentation. Often though you will want to use the 'relaykeys-cli-win' application that will run a little quicker and has no printed output. :::

::: tip If you are developing with the code You must make sure the daemon code is running when you call the cli files. The daemon is the code that turns these commands into the correct AT syntax and access the com port :::

### Defining a Keymap -c

Keymap files are located in [**cli\_keymap**](https://github.com/AceCentre/RelayKeys/tree/master/cli\_keymaps) folder. You can choose which keymap file the CLI is going to use in the cfg by assigning file name to keymap\_file variable (see [here](https://github.com/AceCentre/RelayKeys/blob/12d3eadca2cea53561a5a3979562aae8b4b6cd7c/relaykeys-example.cfg#L17))

By default the **us\_keymap.json** is loaded.\
\
To run relaykeys-cli with other keymap either change the cfg setting or use the -c flag on the cli application. E.g.

`relaykeys-cli.exe -c .\relaykeys-example.cfg type:@`

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

All codes which are converted can be seen below. **NB: \t = Tab \r\n are line breaks**

| \r | &  | {  |
| -- | -- | -- |
|    | \* | ]  |
|    | (  | }  |
| \` | )  | \\ |
| \~ | \_ | \| |
| !  | +  |    |
| @  | -  |    |
| #  | =  | .  |
| $  | ;  | <  |
| %  | :  | >  |
| ^  | \[ | /  |

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
* Left Shift/🔼 : `LSHIFT`
* Left Alt/Alt: `LALT`
* (Left) Meta/Windows Key/Mac Key/Command Key: `LMETA` **Note: On Windows there is generally only one Windows key. So use LMETA to emulate pressing the Windows key**
* Right Control/CTRL:: `LCTRL`
* Right Shift/🔼 : `RSHIFT`
* (Right) Meta/Windows Key/Mac Key/Command Key: \`\`RMETA\`\`\`

#### Keys

So the keys are defined below.

| Defined Key | Detail | Defined Key          | Detail             | Defined Key | Detail                   | Defined Key        | Detail |
| ----------- | ------ | -------------------- | ------------------ | ----------- | ------------------------ | ------------------ | ------ |
| 0           |        | BACKSPACE            | Back Delete key    | KP\_EQSIGN  |                          | HELP               |        |
| 1           |        | ENTER                | Return             | UP          |                          | MENU               |        |
| 2           |        | DELETE               | Forward delete key | DOWN        |                          | SELECT             |        |
| 3           |        | TAB                  |                    | RIGHT       |                          | STOP               |        |
| 4           |        | PAUSE                |                    | LEFT        |                          | AGAIN              |        |
| 5           |        | ESCAPE               |                    | INSERT      |                          | UNDO               |        |
| 6           |        | SPACE                |                    | HOME        |                          | CUT                |        |
| 7           |        | QUOTE                |                    | END         |                          | COPY               |        |
| 8           |        | COMMA                |                    | PAGEUP      |                          | PASTE              |        |
| 9           |        | MINUS                |                    | PAGEDOWN    |                          | FIND               |        |
| A           |        | PERIOD               |                    | F1          |                          | MUTE               |        |
| B           |        | SLASH                |                    | F2          |                          | VOLUP              |        |
| C           |        | SEMICOLON            |                    | F3          |                          | VOLDOWN            |        |
| D           |        | EQUALS               |                    | F4          |                          | LOCKING\_CAPSLOCK  |        |
| E           |        | LEFTBRACKET          |                    | F5          |                          | LOCKING\_NUMLOCK   |        |
| F           |        | BACKSLASH            |                    | F6          |                          | LOCKING\_SCROLLOCK |        |
| G           |        | RIGHTBRACKET         |                    | F7          |                          | ALTERASE           |        |
| H           |        | BACKQUOTE            |                    | F8          |                          | ATTENTION          |        |
| I           |        | KP0                  |                    | F9          |                          | CANCEL             |        |
| J           |        | KP1                  |                    | F10         |                          | CLEAR              |        |
| K           |        | KP2                  |                    | F11         |                          | PRIOR              |        |
| L           |        | KP3                  |                    | F12         |                          | RETURN             |        |
| M           |        | KP4                  |                    | NUMLOCK     |                          | SEPARATOR          |        |
| N           |        | KP5                  |                    | CAPSLOCK    |                          | OUT 0xA0           |        |
| O           |        | KP6                  |                    | SCROLLOCK   |                          | OPER 0xA1          |        |
| P           |        | KP7                  |                    | RIGHTARROW  |                          |                    |        |
| Q           |        | KP8                  |                    | LEFTARROW   |                          |                    |        |
| R           |        | KP9                  |                    | DOWNARROW   |                          |                    |        |
| S           |        | KP\_PERIOD           |                    | UPARROW     |                          |                    |        |
| T           |        | KP\_DIVIDE           |                    | APP         |                          |                    |        |
| U           |        | KP\_MULTIPLY         |                    | LGUI        | Keyboard Left GUI        |                    |        |
| V           |        | KP\_MINUS            |                    | RGUI        | Keyboard Right GUI       |                    |        |
| W           |        | KP\_PLUS             |                    | CUSTOM\~    | Keyboard Non-US # and \~ |                    |        |
| X           |        | KP\_ENTER            |                    | PRINTSCREEN |                          |                    |        |
| Y           |        | KP\_EQUAL # Keypad = |                    | POWER       |                          |                    |        |
| Z           |        | KP\_COMMA            |                    | EXECUTE     |                          |                    |        |

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

### BLE Commands

`relaykeys-cli.exe ble_cmd:devlist`

`relaykeys-cli.exe ble_cmd:devadd`

`relaykeys-cli.exe ble_cmd:devreset`

`relaykeys-cli.exe ble_cmd:switch`

`relaykeys-cli.exe ble_cmd:devremove=DEVNAME`
