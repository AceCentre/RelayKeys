# RelayKeys ESP32 Receiver Dongle

This is the ESP32 version of the RelayKeys receiver dongle, which acts as a BLE Central device to connect to RelayKeys transmitters and forwards HID reports via USB to the host computer.

## Overview

The ESP32 receiver dongle replaces the nRF52840 version with ESP32-specific libraries and capabilities. It maintains the same functionality while leveraging ESP32's native USB HID support (on compatible boards).

## Hardware Requirements

### Recommended Boards (with Native USB HID)
- **ESP32-S2** development boards
- **ESP32-S3** development boards  
- **ESP32-C3** development boards

### Alternative Boards (Limited USB Support)
- ESP32-WROOM (requires external USB Host shield - not implemented)
- ESP32-DevKitC (requires external USB Host shield - not implemented)

## Features

- **BLE Central Mode**: Automatically scans for and connects to "AceRK" devices
- **USB HID Output**: Forwards keyboard, mouse, and consumer control reports to host
- **Status LED**: Visual indication of connection state
- **Manual Reconnection**: Button press to restart scanning/connection
- **Multiple Board Support**: Configurable for different ESP32 variants

## Pin Configuration

The pin configuration is handled in `board_config.h`. By default:

- **User Button**: GPIO 0 (Boot button)
- **Status LED**: GPIO 2 (Built-in LED)

To use a different board configuration, edit `board_config.h` and uncomment the appropriate section.

## Status LED Behavior

- **Solid ON**: Connected to a RelayKeys device
- **Blinking (500ms)**: Scanning for devices or disconnected

## Button Functions

- **Single Press**: Restart BLE scanning and attempt reconnection

## Installation

1. **Install ESP32 Board Package** in Arduino IDE:
   - Go to File → Preferences
   - Add `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json` to Additional Board Manager URLs
   - Go to Tools → Board → Boards Manager
   - Search for "ESP32" and install the package

2. **Select Your Board**:
   - Go to Tools → Board → ESP32 Arduino
   - Choose your specific ESP32 board (e.g., "ESP32S3 Dev Module")

3. **Configure Board Settings**:
   - **USB CDC On Boot**: Enabled (for ESP32-S2/S3/C3)
   - **USB DFU On Boot**: Disabled
   - **USB Firmware MSC On Boot**: Disabled

4. **Upload the Code**:
   - Open `receiver_dongle_ESP32.ino`
   - Configure your board in `board_config.h` if needed
   - Upload to your ESP32

## Usage

1. **Power On**: The receiver will start scanning for RelayKeys devices
2. **Pairing**: Put your RelayKeys transmitter in pairing mode
3. **Connection**: The receiver will automatically connect when it finds an "AceRK" device
4. **Operation**: HID reports from the transmitter will be forwarded to your computer

## Troubleshooting

### No USB HID Functionality
- Ensure you're using an ESP32-S2, ESP32-S3, or ESP32-C3 board
- Check that "USB CDC On Boot" is enabled in Arduino IDE board settings
- Verify the board is properly recognized by your computer

### Connection Issues
- Check that the RelayKeys transmitter is advertising as "AceRK"
- Press the button on the receiver to restart scanning
- Check serial output for debugging information

### Compilation Errors
- Ensure you have the latest ESP32 board package installed
- Check that your board configuration in `board_config.h` is correct
- Verify all required libraries are available

## Debug Mode

To enable debug output, uncomment the `#define DEBUG` line at the top of the main file. This will:
- Print received HID data to serial console
- Disable actual USB HID output
- Show detailed connection and scanning information

## Differences from nRF52840 Version

- **BLE Library**: Uses ESP32 BLE libraries instead of Bluefruit
- **USB HID**: Uses ESP32 native USB HID instead of TinyUSB
- **Board Support**: Configurable for multiple ESP32 variants
- **Memory**: Uses ESP32's larger memory capacity
- **Power**: Different power management characteristics

## Limitations

- ESP32-WROOM and similar boards without native USB require external hardware
- Some advanced HID features may need additional implementation
- Power consumption may differ from nRF52840 version

## Contributing

When contributing to this ESP32 receiver implementation:
1. Test on multiple ESP32 board variants when possible
2. Maintain compatibility with the existing RelayKeys protocol
3. Update documentation for any new features or requirements
4. Follow the existing code style and structure

## License

MIT License - Copyright Ace Centre 2024
