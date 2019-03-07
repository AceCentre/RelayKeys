# Commands

## Introduction

We have created a command line interface which allows you to send mouse and keyboard commands to your RelayKeys hardware. 

To run it access 

``relaykeys-cli.exe command:data``

or if running it in pure python

``python relaykeys-cli.py command:data``

Where 'command' and 'data' are provided below

### Command: paste

This takes the pasteboard of the computer (i.e. when you copy some text) and pastes the resulting string to RelayKeys

i.e. 

``relaykeys-cli.exe paste``


### Command: type:text

Types the string following the :. Note you will need to escape spaces etc 

``relaykeys-cli.exe type:Hello\ World``


### Command: keypress:KEY,MODIFIER

Sends the KEY and any modifier, For example:


``relaykeys-cli.exe keypress:A``

Will emulate pressing and releasing the letter `A`. What about a shift?

``relaykeys-cli.exe keypress:A,LSHIFT``

Will emulate pressing the A with Left Shift. i.e. Upper casing the A. 


#### Modifiers

* Left Control/CTRL: ``LCTRL``
* Left Shift/🔼 : ``LSHIFT``
* Left Alt/Alt: ``LALT``
* (Left) Meta/Windows Key/Mac Key/Command Key: ``LMETA`` **Note: On Windows there is generally only one Windows key. So use LMETA to emulate pressing the Windows key**
* Right Control/CTRL:: ``LCTRL``
* Right Shift/🔼 : ``RSHIFT``
* (Right) Meta/Windows Key/Mac Key/Command Key: ``RMETA``` 



### Command: keyevent:KEY,MODIFIER,Up/Down


Emulates holding or releasing one key with a modifer. For example:

``relaykeys-cli.exe keyevent:A,LSHIFT,1``

Emulates pressing a `A` with `Shift` Down.
To release: 

``relaykeys-cli.exe keyevent:A,LSHIFT,0``

Bear in mind it can only send one at a time. So a classic example is to emulate pressing the Windows key and tab. Commonly used to switch applications. To do this you would need to send two commands

	relaykeys-cli.exe keyevent:LMETA,1
	relaykeys-cli.exe keyevent:TAB,1
	relaykeys-cli.exe keyvent:LMETA,0
	relaykeys-cli.exe keyevent:TAB,0


### Command: mousemove:PixelsLeft,PixelsDown

Sends the command to move the mouse x Pixels Left and x Pixels Down. To go in the other direction send negative numbers. Eg. To go Left by 10 and Down by 10

``relaykeys-cli.exe mousemove:10,10``

and Right by 10, Up by 10: 

``relaykeys-cli.exe keyevent:-10,-10``

Straight up:

``relaykeys-cli.exe keyevent:0,-10``

Straight down:

``relaykeys-cli.exe keyevent:0,10``

Straight left:

``relaykeys-cli.exe keyevent:10,0``

Straight right:

``relaykeys-cli.exe keyevent:-10,0``


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

``relaykeys-cli.exe mousebutton:L,doubleclick``

Send a right click:

``relaykeys-cli.exe mousebutton:R,click``

What about dragging? 

