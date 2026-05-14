# Config File details

## Introduction

RelayKeys uses an INI-format configuration file called `relaykeys.cfg`. The daemon searches for it in this order:

1. Path specified by `--config` flag
2. `~/.relaykeys.cfg`
3. `<exe_dir>/relaykeys.cfg` (same directory as the executable)
4. `./relaykeys.cfg` (current working directory)
5. `%APPDATA%\RelayKeys\relaykeys.cfg` (Windows only)

## Example

```ini
[server]
host = 127.0.0.1
port = 5383
dev = COM5
baud = 115200
debug = false
noserial = false
logfile = relaykeys.log

[client]
host = 127.0.0.1
port = 5383
delay = 5

[cli]
keymap_file = us_keymap.json
```

## Sections

### [server]

| Setting  | Default      | Description                                      |
|----------|--------------|--------------------------------------------------|
| host     | 127.0.0.1    | RPC server bind address                          |
| port     | 5383         | RPC server port                                  |
| dev      | (auto)       | Serial port (e.g. `COM5`). Auto-detects if empty |
| baud     | 115200       | Serial baud rate                                 |
| debug    | false        | Enable verbose logging                           |
| noserial | false        | Run without serial hardware                      |
| logfile  | (empty)      | File for debug log output                        |

### [client]

| Setting | Default   | Description                               |
|---------|-----------|-------------------------------------------|
| host    | 127.0.0.1| RPC server address (for CLI)              |
| port    | 5383      | RPC server port (for CLI)                 |
| delay   | 5         | Delay (ms) between keystrokes when typing |

### [cli]

| Setting     | Default          | Description                     |
|-------------|------------------|---------------------------------|
| keymap_file | us_keymap.json   | Keyboard layout file to use     |

## Keyboard Layouts

Keymap files are stored in the `keymaps/` directory. Available layouts:

| File                    | Layout             |
|-------------------------|--------------------|
| `us_keymap.json`        | US QWERTY          |
| `uk_keymap.json`        | UK QWERTY          |
| `de_keymap.json`        | German QWERTZ      |
| `fr_azerty_keymap.json` | French AZERTY      |
| `es_qwerty_keymap.json` | Spanish QWERTY     |
| `it_qwerty_keymap.json` | Italian QWERTY     |

To switch layout, change the `keymap_file` setting:

```ini
[cli]
keymap_file = fr_azerty_keymap.json
```

Each keymap is a JSON file mapping characters to HID key codes and modifiers:

```json
{
    "a": ["A", []],
    "A": ["A", ["LSHIFT"]],
    " ": ["SPACE", []],
    "\r": [null, null]
}
```

## Serial Port Configuration

RelayKeys auto-detects the dongle by scanning for Adafruit nRF52840 boards (VID `239A`, PIDs `8029`, `810B`, `8051`). If auto-detection fails or you have multiple boards:

1. Open Windows Device Manager
2. Expand "Ports (COM & LPT)"
3. Find the Adafruit device and note the COM port number
4. Set `dev = COM3` (or your port) in the config file

You can also use `relaykeys-daemon.exe --list-ports` to see all detected serial ports.
