# RelayKeys

Allow a Computer to mimic a Bluetooth Keyboard (& Mouse). 
Using some hardware (a couple of different options currently) and a piece of software running on the 'Server' machine - any devices which support Bluetooth LE HID can then receive the keystrokes. **For full documentation (and updated docs!) see https://docs.acecentre.org.uk/products/v/relaykeys/**

<p align="center">
  <img src="https://github.com/acecentre/relaykeys/actions/workflows/build.yml/badge.svg?branch=master" alt="Github Action Build workflow status" />
  <img alt="GitHub" src="https://img.shields.io/github/license/acecentre/relaykeys">
  <img alt="GitHub issues" src="https://img.shields.io/github/issues-raw/acecentre/relaykeys">
  <img alt="Lines of code" src="https://img.shields.io/tokei/lines/github/acecentre/relaykeys">
  <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/acecentre/relaykeys/total">
  <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/relaykeys/eyecommander">
</p>

<!--ts-->
   * [RelayKeys](#relaykeys)
      * [Why?](#why)
      * [Getting Started](#getting-started)
      * [License](#license)
      * [Credits](#credits)

<!-- Added by: willwade, at:  -->

<!--te-->

## Why?

Well a range of purposes. For some - its just a convenient way of saving some money on a [KVM switch](https://en.wikipedia.org/wiki/KVM_switch) - or replacing now hard to find [commercial solutions](https://docs.acecentre.org.uk/products/v/relaykeys/developers/other-projects). 

For the [AceCentre](http://acecentre.org.uk) we want people with disabilities who are forced to use one system (e.g. a dedicated Eyegaze system) to be able to access other computers and systems they may need to use for work or leisure. This has only been available on a couple of commercial AAC systems - and often need to be on the same network which is sadly often impossible in schools or government workplaces - Or they do work over bluetooth but for only one system in the field exists like this (see [here for more details on these](https://docs.acecentre.org.uk/products/v/relaykeys/developers/other-projects#aac-projects)). Some people may also want to jyst control their tablet or phone using this technique rather than rely on computer control functions - for example to control music software or photo editing software which usually demands the full screen. Or others want to make custom full screen custom keyboards using their specialist software. 

**Why not just rely on other solutions?** Some commercial solutions are great. We advocate using them over our solution when you can. When you can't (e.g. no alternative or restrictions to what devices you can control) then this may be a solution. 

**We are a commercial developer.. I like it but I think I could do it differently**. Thats great! But please consider the end user. If you as a commercial supplier dont want to continue making this hardware/software solution in the future consider a route to how a user could use a open solution. Please consider either replicating our command set at a serial or CLI level. Are we missing something that your solution provides? Please let us know so we can improve it. 

**Why not just do this in software alone?** Sure. If you can. On windows - its not possible.. Yet. Maybe in Windows 11. In MacOS it *should* be - and iOS & Android its definitely possible. But our solution kind of offloads the problem. If you work in one of the mobile environments and want to replicate the functionality go for it - just please consider following some similarity in command structure (take a look at the macros for example)

![Image of Person Using AAC](https://acecentre.org.uk/wp-content/uploads/2017/05/Helping-children-with-AAC-needs-1280x492.jpg)


## Getting Started

If you are a developer start [here](https://docs.acecentre.org.uk/products/v/relaykeys/developers/architecture). If you are an end user who just wants to get going start [here](https://docs.acecentre.org.uk/products/v/relaykeys/installation).

### Development Setup

RelayKeys is written in Go. The host software consists of a daemon (background service) and a CLI client.

```bash
# Clone the repository
git clone https://github.com/AceCentre/RelayKeys.git
cd RelayKeys

# Build (Windows)
powershell -ExecutionPolicy Bypass -File build-go.ps1

# Or build manually
go build -o relaykeys-daemon.exe ./cmd/relaykeys-daemon
go build -o relaykeys-cli.exe ./cmd/relaykeys-cli

# Run tests
go test ./... -count=1

# Cross-compile (macOS/Linux from any platform)
bash build-go.sh
```

### Architecture

| Component | Description |
|-----------|-------------|
| `cmd/relaykeys-daemon/` | Background service — serial, RPC, web UI, Windows service support |
| `cmd/relaykeys-cli/` | CLI client — used by AAC software (Grid 3, Communicator 5, etc.) |
| `internal/blehid/` | AT command protocol over serial + HID keycode map |
| `internal/config/` | INI config loading |
| `internal/keymap/` | JSON keymap loading (US, UK, DE, FR, ES, IT) |
| `internal/macro/` | Macro save/load/record/replay |
| `internal/rpc/` | JSON-RPC server (port 5383) + client |
| `internal/serial/` | Hardware serial via `go.bug.st/serial`, auto-detect by VID/PID |
| `internal/simulator/` | Full firmware simulator for testing |
| `internal/webui/` | Embedded web UI + WebSocket hub |

The daemon listens on `127.0.0.1:5383` for JSON-RPC over HTTP, serves a web UI at `/ui/`, and communicates with the nRF52840 dongle via AT commands over serial at 115200 baud.

### CLI Commands

```bash
relaykeys-cli "type:Hello World"          # Type text on target BLE device
relaykeys-cli "keypress:ENTER"            # Press a key
relaykeys-cli "keypress:H,LMETA"          # Win+H (modifier)
relaykeys-cli "mousemove:100,100"         # Move mouse
relaykeys-cli "mousebutton:l,click"       # Left click
relaykeys-cli "ble_cmd:devlist"           # List paired BLE devices
relaykeys-cli "ble_cmd:devadd"            # Enter pairing mode
relaykeys-cli -f macrofile.txt            # Run macro file
```


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Credits

- [bbx10](https://forums.adafruit.com/viewtopic.php?f=53&t=145081&start=15) on the Adafruit forums who got this up and running. Awesome. 
- [Keyboard](https://thenounproject.com/search/?q=keyboard&i=1442359) by Atif Arshad from the Noun Project
- [Bluetooth](https://thenounproject.com/search/?q=bluetooth&i=1678456) by Adrien Coquet from the Noun Project

<a href = "https://github.com/AceCentre/RelayKeys/graphs/contributors">
<img src = "https://contrib.rocks/image?repo=AceCentre/RelayKeys"/>
</a>
