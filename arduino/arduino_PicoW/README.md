# RelayKeys Raspberry Pi Pico W Implementation

## ⚠️ EXPERIMENTAL - UNTESTED ⚠️

**WARNING: This is experimental code that has NOT been tested with actual hardware. Use at your own risk and expect bugs, compilation errors, and compatibility issues.**

## Overview

This is a Raspberry Pi Pico W implementation of RelayKeys using BTStack (the official Bluetooth stack for Pico W). It provides BLE HID keyboard and mouse functionality compatible with the RelayKeys AT command protocol.

## Why Pico W?

- **Cost Effective**: Significantly cheaper than nRF52840 or ESP32 boards (~$6 vs $25+)
- **Official Bluetooth Stack**: Uses BTStack, the professional-grade Bluetooth implementation
- **Good Performance**: Dual-core ARM Cortex-M0+ at 133MHz with 264KB RAM
- **Native USB**: Built-in USB HID support
- **Wide Availability**: Easy to source through official channels

## Hardware Requirements

### Recommended Hardware
- **Raspberry Pi Pico W** (required)
- **Micro USB cable** for programming and power
- **Optional**: External button on GPIO 14 for mode switching
- **Optional**: External LED if not using built-in LED

### Pin Configuration
- **Built-in LED**: Status indication (CYW43 chip LED)
- **GPIO 14**: User button (configurable in board_config.h)
- **USB**: Serial communication and power

## Features

### ✅ Planned Features
- **BLE HID Keyboard**: Send keyboard reports via Bluetooth
- **BLE HID Mouse**: Send mouse movement and clicks
- **Consumer Control**: Media keys (volume, mute)
- **AT Command Protocol**: Full RelayKeys command compatibility
- **Device Management**: Pairing and connection management
- **Mode Switching**: Serial/BLE mode toggle
- **Status LED**: Visual connection indication

### ⚠️ Experimental/Incomplete
- **Device List Storage**: Flash storage not implemented
- **Multiple Device Pairing**: Basic implementation only
- **Connection Switching**: Not implemented
- **Power Management**: Not optimized
- **Error Handling**: Basic implementation

### ❌ Not Implemented
- **Receiver Dongle Mode**: BLE Central functionality
- **File System**: Persistent storage for device lists
- **Advanced Pairing**: Complex pairing scenarios
- **WiFi Features**: WiFi capability not used

## Installation

### Prerequisites

1. **Pico SDK**: Install the Raspberry Pi Pico SDK
   ```bash
   git clone https://github.com/raspberrypi/pico-sdk.git
   export PICO_SDK_PATH=/path/to/pico-sdk
   ```

2. **BTStack**: Clone BTStack repository
   ```bash
   git clone https://github.com/bluekitchen/btstack.git
   ```

3. **Build Tools**: CMake, GCC ARM toolchain
   ```bash
   # Ubuntu/Debian
   sudo apt install cmake gcc-arm-none-eabi
   
   # macOS
   brew install cmake gcc-arm-embedded
   ```

### Building (Theoretical - Untested)

1. **Setup Build Environment**:
   ```bash
   mkdir build
   cd build
   cmake .. -DPICO_BOARD=pico_w
   ```

2. **Build Firmware**:
   ```bash
   make arduino_PicoW
   ```

3. **Flash to Pico W**:
   - Hold BOOTSEL button while connecting USB
   - Copy `arduino_PicoW.uf2` to RPI-RP2 drive

### Arduino IDE Alternative (Not Recommended)

This implementation is designed for native Pico SDK, not Arduino IDE. Arduino IDE support would require significant modifications.

## Usage (Theoretical)

### Initial Setup
1. Flash firmware to Pico W
2. Connect via USB serial (115200 baud)
3. Device starts in serial mode

### AT Commands
Same as other RelayKeys implementations:

```
AT+BLEKEYBOARDCODE=00-00-0B-08-0F-0F-12-00  // Type "Hello"
AT+BLEHIDMOUSEMOVE=10,5,0,0                 // Move mouse
AT+BLEHIDMOUSEBUTTON=l,click                // Left click
AT+BLEADDNEWDEVICE                          // Enter pairing mode
AT+SWITCHMODE                               // Toggle serial/BLE mode
```

### LED Status Indicators

| LED Pattern | Status |
|-------------|--------|
| Solid ON | Serial mode, ready |
| Slow Blink | BLE mode, ready |
| Fast Blink | Pairing mode |

## Development Status

### Completed (Theoretical)
- [x] Basic code structure
- [x] BTStack integration framework
- [x] HID descriptor definitions
- [x] AT command parsing
- [x] Board configuration system

### In Progress
- [ ] BTStack HID service implementation
- [ ] Connection management
- [ ] Error handling
- [ ] Testing framework

### Not Started
- [ ] Flash storage implementation
- [ ] Advanced device management
- [ ] Power optimization
- [ ] Receiver dongle mode
- [ ] Hardware testing

## Known Issues (Expected)

### Compilation Issues
- BTStack integration may need adjustment
- Missing include paths
- Library compatibility problems
- CMake configuration issues

### Runtime Issues (Expected)
- Bluetooth initialization failures
- HID service registration problems
- Memory management issues
- Timing and synchronization problems

### Compatibility Issues
- May not work with existing RelayKeys software
- HID report format differences
- Connection stability problems
- Pairing difficulties

## Technical Implementation

### BTStack Integration
```c
// Uses BTStack HID device API
#include "btstack.h"
hid_device_init();
hid_device_send_input_report(hid_cid, report, sizeof(report));
```

### HID Descriptors
Based on BTStack examples with RelayKeys-compatible report IDs:
- Report ID 1: Keyboard
- Report ID 2: Mouse  
- Report ID 3: Consumer Control

### Memory Usage
- **Flash**: ~200KB (estimated)
- **RAM**: ~50KB (estimated)
- **Stack**: ~8KB (estimated)

## Contributing

### Before Contributing
1. **Test with Hardware**: Verify code actually works
2. **Fix Compilation**: Ensure code compiles without errors
3. **Document Issues**: Report specific problems found
4. **Incremental Changes**: Small, testable improvements

### Development Priorities
1. **Get it Compiling**: Fix build system and dependencies
2. **Basic Functionality**: Get keyboard HID working
3. **Hardware Testing**: Test with actual Pico W
4. **Compatibility**: Ensure works with RelayKeys software
5. **Documentation**: Update based on actual testing

## Comparison with Other Platforms

| Feature | nRF52840 | ESP32 | Pico W |
|---------|----------|-------|--------|
| Cost | $25+ | $10+ | $6 |
| BLE Stack | Bluefruit | Arduino BLE | BTStack |
| Maturity | Stable | Stable | Experimental |
| Performance | High | High | Medium |
| Memory | 256KB RAM | 520KB RAM | 264KB RAM |
| USB HID | TinyUSB | Native (S2/S3) | Native |
| Community | Large | Large | Growing |

## Future Plans

### Short Term
- [ ] Get basic compilation working
- [ ] Test with actual hardware
- [ ] Fix critical bugs
- [ ] Basic HID functionality

### Medium Term
- [ ] Full AT command compatibility
- [ ] Device management features
- [ ] Flash storage implementation
- [ ] Performance optimization

### Long Term
- [ ] Receiver dongle implementation
- [ ] Advanced pairing features
- [ ] Power management
- [ ] Production readiness

## Support

### Getting Help
- **GitHub Issues**: Report bugs and ask questions
- **Documentation**: Check BTStack and Pico SDK docs
- **Community**: Raspberry Pi and BTStack forums

### Reporting Issues
When reporting issues, include:
- Exact error messages
- Build environment details
- Hardware configuration
- Steps to reproduce

## License

MIT License - Copyright Ace Centre 2024

## Disclaimer

This is experimental software provided "as is" without warranty. The authors are not responsible for any damage or issues caused by using this code. Use at your own risk and always test thoroughly before deploying.
