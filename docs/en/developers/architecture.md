# Architecture of RelayKeys

![RelayKeys Sketch](../.gitbook/assets/untitled\_page.png)

RelayKeys is a mixture of a Open Hardware board that communicates in Bluetooth LE and acts as a BLE HID device (i.e. a keyboard/mouse) which can emulate **all** keyboard keys and their modifiers as well as mouse movements. (4). This is controlled by a serial connection from a device - either wired (i.e. as a USB dongle) or wireless (i.e. as a BLE Serial device).\
\
We have developed RPC server (2) for a desktop computer which simplifies software connecting to the serial bus and allows us to create a simpler way of sending commands to the device than AT commands. This is done either directly via the RPC Server (_Daemon_) or via a **Command Line Interface** (_CLI_). The daemon also serves a web-based user interface for device management and testing.

If you make software and want to benefit from the features of RelayKeys you can either write commands to the RPC server (2), or via our CLI (1) or if you wish direct to the serial interface (6). This can be wired serial or wireless if you put the device into wireless mode (5). Even if you wish to ignore our hardware we do ask Assistive Technology developers to consider copying the command structure at either one of these levels to allow for open development.

The Arduino based board is currently a **Adafruit nrf52840 express or Adafruit nrf52840 itsybitsy**.

## Anatomy of the files

* `arduino/` - firmware for the arduino board
* `cmd/relaykeys-daemon/` - The daemon entry point. Runs as a background process or Windows service. Handles serial communication, RPC server, and web UI.
* `cmd/relaykeys-cli/` - The command line interface. Used by AAC software (Grid 3, Communicator 5, etc.) to send keystrokes and control BLE devices.
* `cmd/relaykeys-tray/` - System tray application (Windows) / menu bar app (macOS). Shows dongle connection status and provides quick access to common actions.
* `internal/blehid/` - AT command protocol over serial + HID keycode map
* `internal/config/` - INI config file loading
* `internal/keymap/` - JSON keymap loading (US, UK, DE, FR, ES, IT layouts)
* `internal/macro/` - Macro save/load/record/replay
* `internal/rpc/` - JSON-RPC server (port 5383) + client
* `internal/serial/` - Hardware serial via `go.bug.st/serial`, auto-detect by VID/PID
* `internal/simulator/` - Full firmware simulator for testing without hardware
* `internal/webui/` - Embedded web UI (HTML/JS/CSS) + WebSocket hub
* `keymaps/` - Keymap JSON files shipped alongside the binary
* `macros/` - User macro files
* `assets/` - Icons and other resources
* `build-go.ps1` - Windows build script (PowerShell)
* `build-go.sh` - macOS/Linux build script (bash)
* `build-installer.nsi` - NSIS installer script for Windows

## Steps to run RelayKeys (non-installer method)

_Prerequisites_

* [Install Go 1.23+](https://go.dev/dl/)
* Have access to a nrf52840 arduino board. e.g. the Adafruit nrf52840 express

1. Grab a nrf52840 board and load the arduino code onto it. Plug it in a usb slot on your computer
2. Clone the repo: `git clone https://github.com/AceCentre/RelayKeys.git && cd RelayKeys`
3. Build the daemon and CLI:
   ```
   go build -o relaykeys-daemon.exe ./cmd/relaykeys-daemon
   go build -o relaykeys-cli.exe ./cmd/relaykeys-cli
   ```
4. Run the daemon: `relaykeys-daemon.exe --debug`
5. Pair your relaykeys arduino with a PC/Mac/iOS/Android device and open a text file
6. Test it out with the CLI: `relaykeys-cli.exe type:Hello`

You should see "Hello" typed on the paired device. If not, check the daemon console output for errors.

If the daemon cannot find the COM port automatically, you can fix it in the config file: `dev = COM3`. See [config details](relaykeys-cfg.md) for more information.
