# Config File details

## Introduction

In the same directory as relaykeys there is a file `relaykeys.cfg`

It looks like this:

```
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

[cli]
keymap_file = us_keymap.json
```

Feel free to change any of the settings but **Be careful that you make the username/password the same** - otherwise the CLI programme can't talk to the service.

Note the keymap file. This is found in the sub directory **cli\_keymaps**. You can have multiple keymaps in here if you wish and switch between them using the[ cli using -c](../using-relaykeys/relaykeys-cli.md#defining-a-keymap-c)

## Available Keyboard Layouts

RelayKeys now supports multiple keyboard layouts for different languages and regions:

- **us_keymap.json** - US English QWERTY layout
- **uk_keymap.json** - UK English QWERTY layout
- **de_keymap.json** - German QWERTZ layout
- **fr_azerty_keymap.json** - French AZERTY layout (NEW!)
- **es_qwerty_keymap.json** - Spanish QWERTY layout (NEW!)
- **it_qwerty_keymap.json** - Italian QWERTY layout (NEW!)

To use a different layout, simply change the `keymap_file` setting:

```ini
[cli]
keymap_file = fr_azerty_keymap.json
```

### Language-Specific Features

**French AZERTY:**
- Accented characters: é, è, à, ç, ù
- Special symbols: €, £, ², ³, °
- Proper AZERTY key positioning

**Spanish QWERTY:**
- Special characters: ñ, Ñ
- Inverted punctuation: ¿, ¡
- Accented vowels: á, é, í, ó, ú
- Euro symbol: €

**Italian QWERTY:**
- Accented vowels: à, è, ì, ò, ù
- Special symbols: €, £, °, §

Each file is a json file (tip - using [jsonlint](https://jsonlint.com) to check its formatted ok) looks something like the below where the string is sent dependent on the characters sent. eg. on a UK keyboard **! is sent by presing shift and 1.**

```
{
    "\r": [null, null],
    "\t": ["TAB", []],
    " ":  ["SPACE", []],
    "`":  ["BACKQUOTE", []],
    "~":  ["BACKQUOTE", ["LSHIFT"]],
    "!":  ["1", ["LSHIFT"]]
}
```

## Dev - Defining your port of the RelayKeys hardware

RelayKeys software tries to find the RelayKeys board automagically. If you have a device with a number of COM ports attached - or ones that have similar functionality you may have some difficulties. If so try _fixing_ the COM port.

1. Access Device Manager. Search for "Device Manager" in Windows.

[![Image from Gyazo](https://i.gyazo.com/0b327be4a6ad9ea569da378e1f1d7a1a.gif)](https://gyazo.com/0b327be4a6ad9ea569da378e1f1d7a1a)

1. Click on Ports. If you only have RelayKeys connected you should see one device. If you see many - try unplugging it and replugging it in to find which COM port it is.

[![Image from Gyazo](https://i.gyazo.com/0b327be4a6ad9ea569da378e1f1d7a1a.gif)](https://gyazo.com/0b327be4a6ad9ea569da378e1f1d7a1a)

1. Note the number and edit your RelayKeys cfg file. Search for "RelayKeys config" in Windows - and open with Notepad.

[![Image from Gyazo](https://i.gyazo.com/427603ca7c287942ad92ccd823c0f64d.gif)](https://gyazo.com/427603ca7c287942ad92ccd823c0f64d)

1. Type `dev = COM3` where **COM3** is your port number you found in step 2-3.
