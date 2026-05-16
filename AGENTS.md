# RelayKeys Agents Documentation

## Current State: ZMK Bridge Integration (Phase 1)

**Overview**
The codebase has been updated to support a pure software-driven nRF52840 BLE HID bridge using ZMK firmware, replacing the legacy hardware-mod approach. The host side is managed by the RelayKeys Go daemon.

**Completed Work**
1. **ZMK Firmware Structure**: A `firmware/zmk` directory was added containing `west.yml`, a dummy `relaykeys_dongle` shield (bypassing hardware matrix scanning), and `relaykeys_handler.c` which implements a ZMK Studio RPC subsystem to receive binary payloads and inject HID reports over the BLE endpoint.
2. **Protobuf Integration**: Defined `relaykeys.proto` under `internal/zmk/proto` and generated Go bindings for communication between the Go daemon and ZMK firmware.
3. **Go Transport Layer**: Added `internal/zmkbridge` which frames Protobuf payloads using ZMK's SLIP/COBS-like framing (0xAB, 0xAC, 0xAD) and writes raw bytes to the serial interface.
4. **Configuration**: Added `FirmwareType` to `config.go` and `rpc/server.go`, allowing backward compatibility with `legacy` AT commands or switching to the new `zmk` protocol.

## Next Steps (Phase 2 & Beyond)

* **Implement Mouse & Consumer Reports in Firmware**: Currently `relaykeys_handler.c` only constructs and injects Keyboard reports (`zmk_hid_keyboard_report_body`). It needs to be extended to support Mouse and Consumer (media) reports based on the type enum from the protobuf definition.
* **Implement Mouse/Media Send Functions in Go**: Implement `SendMouseMove`, `SendMouseButton` and other functionalities inside `internal/zmkbridge/bridge.go` to wrap and send correct Protobuf messages.
* **Native ZMK Administration**: Map BLE bonding and profile status from ZMK back to the Go daemon state. Add protobuf RPC definitions for getting connected devices, clearing slots, and switching devices (e.g. implementing `ProcessBleCmd` completely). Update the Web UI to show which of the 5 ZMK slots are occupied and which devices are connected.
* **Compile Firmware**: Test the standard ZMK build locally or via GitHub actions for the `relaykeys_dongle` shield.

*When modifying the ZMK handler code, make sure to consider `nanopb` struct generation if new fields are added.*
