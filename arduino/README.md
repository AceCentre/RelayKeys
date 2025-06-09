# RelayKeys Arduino Firmware

This directory contains Arduino firmware implementations for RelayKeys compatible hardware platforms. The firmware provides BLE HID (Bluetooth Low Energy Human Interface Device) functionality, allowing devices to act as wireless keyboards and mice.

## Supported Platforms

### nRF52840 (arduino_nRF52840_v2/)
- **Boards**: Adafruit nRF52840 Express, ItsyBitsy nRF52840, Raytac MDBT50Q-RX
- **Features**: Full RelayKeys compatibility, multiple device pairing, file system storage
- **Status**: ✅ Complete implementation

### ESP32 (arduino_ESP32/)
- **Boards**: ESP32-WROOM, ESP32-S3, and other ESP32 variants
- **Features**: RelayKeys AT command compatibility, BLE HID, NVRAM storage
- **Status**: ✅ Complete implementation

### Legacy nRF52840 (arduino_nRF52840/)
- **Status**: 🔄 Original implementation (maintained for compatibility)

## Receiver Dongles

### nRF52840 Receiver (receiver_dongle/)
- **Boards**: Adafruit nRF52840 Express, ItsyBitsy nRF52840, Raytac MDBT50Q-RX
- **Features**: BLE Central mode, USB HID output, connects to RelayKeys transmitters
- **Status**: ✅ Complete implementation

### ESP32 Receiver (receiver_dongle_ESP32/)
- **Boards**: ESP32-S2, ESP32-S3, ESP32-C3 (with native USB HID support)
- **Features**: BLE Central mode, USB HID output, connects to RelayKeys transmitters
- **Status**: ✅ Complete implementation

## Experimental Platforms

### Raspberry Pi Pico W (arduino_PicoW/)
- **Boards**: Raspberry Pi Pico W
- **Features**: BTStack-based BLE HID, RelayKeys AT command compatibility
- **Status**: ⚠️ Experimental - Untested code, expect compilation and runtime issues

## Common Features

All implementations support the same AT command protocol:

### Keyboard Commands
- `AT+BLEKEYBOARDCODE=XX-XX-XX-XX-XX-XX-XX-XX` - Send keyboard HID report
- Special keys: Volume up/down, mute

### Mouse Commands
- `AT+BLEHIDMOUSEMOVE=X,Y,WY,WX` - Mouse movement and scrolling
- `AT+BLEHIDMOUSEBUTTON=Button[,Action]` - Mouse button actions
  - Buttons: `l` (left), `r` (right), `m` (middle), `b` (back), `f` (forward)
  - Actions: `click`, `doubleclick`, or press/release toggle

### Device Management
- `AT+BLEADDNEWDEVICE` - Add new device to pairing list
- `AT+BLEREMOVEDEVICE="DeviceName"` - Remove device from list
- `AT+SWITCHCONN[="DeviceName"]` - Switch between connected devices
- `AT+PRINTDEVLIST` - List paired devices
- `AT+BLECURRENTDEVICENAME` - Get current connected device name
- `AT+RESETDEVLIST` - Clear all paired devices

### System Commands
- `AT+SWITCHMODE` - Toggle between serial/BLE modes
- `AT+GETMODE` - Get current mode
- `AT+BLEMAXDEVLISTSIZE=N` - Set maximum device list size

## Hardware Requirements

### Transmitter Boards

#### nRF52840 Boards
- **Adafruit nRF52840 Express**: Built-in NeoPixel, user button on pin 7
- **Adafruit ItsyBitsy nRF52840**: DotStar LED, user button on pin 4
- **Raytac MDBT50Q-RX**: Blue LED, user button on PIN_BUTTON1

#### ESP32 Boards
- **ESP32-WROOM**: Built-in LED on pin 2, boot button on pin 0
- **ESP32-S3**: Varies by board manufacturer
- **Other ESP32 variants**: Adjust pin definitions in code

### Receiver Dongle Boards

#### nRF52840 Receiver Dongles
- Same hardware as transmitters but running receiver firmware
- Acts as BLE Central to connect to RelayKeys transmitters
- Forwards HID reports via USB to host computer

#### ESP32 Receiver Dongles
- **ESP32-S2/S3/C3**: Recommended for native USB HID support
- **ESP32-WROOM**: Requires external USB Host shield (not implemented)
- Acts as BLE Central with USB HID output capability

### Experimental Boards

#### Raspberry Pi Pico W (Experimental)
- **Cost**: ~$6 (most affordable option)
- **Bluetooth**: CYW43439 chip with BTStack support
- **USB**: Native USB HID capability
- **Status**: Experimental code - compilation and runtime issues expected
- **Use Case**: Budget-friendly option for testing and development

## Installation

### Prerequisites
1. **Arduino IDE** with appropriate board support packages
2. **nRF52840**: Adafruit nRF52 board package
3. **ESP32**: Espressif ESP32 board package

### nRF52840 Setup
1. Install [Adafruit nRF52 Arduino Core](https://learn.adafruit.com/bluefruit-nrf52-feather-learning-guide/arduino-bsp-setup)
2. Select your board in Arduino IDE
3. Upload `arduino_nRF52840_v2.ino`

### ESP32 Setup
1. Install [ESP32 Arduino Core](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html)
2. Select your ESP32 board in Arduino IDE
3. Upload `arduino_ESP32.ino`

### Receiver Dongle Setup

#### nRF52840 Receiver
1. Follow nRF52840 setup steps above
2. Upload `receiver_dongle/receiver_dongle.ino`
3. Connect to host computer via USB

#### ESP32 Receiver
1. Follow ESP32 setup steps above
2. For ESP32-S2/S3/C3: Enable "USB CDC On Boot" in Arduino IDE
3. Upload `receiver_dongle_ESP32/receiver_dongle_ESP32.ino`
4. Connect to host computer via USB

### Experimental Setup

#### Pico W Setup (Experimental - Not Recommended)
1. Install [Pico SDK](https://github.com/raspberrypi/pico-sdk)
2. Install [BTStack](https://github.com/bluekitchen/btstack)
3. Build using CMake (see arduino_PicoW/README.md)
4. Flash .uf2 file to Pico W
5. **Warning**: Expect compilation errors and runtime issues

## Usage

### Transmitter Usage

#### Initial Setup
1. Upload firmware to your board
2. Power on the device
3. The device will start in serial mode (green/solid LED)

#### Pairing Devices
1. Single-click the user button to enter pairing mode (yellow/fast blink LED)
2. Connect your target device (phone, tablet, computer) via Bluetooth
3. Look for device named "AceRK"
4. Device will be added to the pairing list automatically

#### Mode Switching
- **Double-click** user button to switch between serial and BLE modes
- **Serial mode**: Commands via USB serial connection
- **BLE mode**: Commands via BLE UART service (blue/slow blink LED)

#### LED Status Indicators

| LED Color/Pattern | Status |
|-------------------|--------|
| Green/Solid | Serial mode, ready |
| Blue/Slow blink | BLE mode, ready |
| Yellow/Fast blink | Pairing mode |

### Receiver Dongle Usage

#### Setup
1. Upload receiver firmware to your board
2. Connect the receiver dongle to your host computer via USB
3. Power on the receiver - it will start scanning for RelayKeys devices

#### Operation
1. The receiver automatically scans for devices named "AceRK"
2. When found, it connects and pairs automatically
3. HID reports from the transmitter are forwarded to the host computer
4. Press the button to restart scanning if connection is lost

#### LED Status Indicators (Receiver)

| LED Pattern | Status |
|-------------|--------|
| Solid ON | Connected to RelayKeys device |
| Blinking | Scanning for devices or disconnected |

## AT Command Examples

### Send text "Hello"
```
AT+BLEKEYBOARDCODE=00-00-0B-08-0F-0F-12-00
```

### Move mouse right 10px, down 5px
```
AT+BLEHIDMOUSEMOVE=10,5,0,0
```

### Left mouse click
```
AT+BLEHIDMOUSEBUTTON=l,click
```

### List paired devices
```
AT+PRINTDEVLIST
```

## Development

### Code Structure
- `common/relaykeys_common.h` - Shared definitions and constants
- Platform-specific `.ino` files implement the AT command handlers
- Each platform uses its native BLE and storage libraries

### Adding New Platforms
1. Create new directory under `arduino/`
2. Include `../common/relaykeys_common.h`
3. Implement all functions declared in the common header
4. Follow the existing AT command structure

### Debugging
Uncomment `#define DEBUG` in the firmware to enable serial debug output.

## Receiver Dongle vs Transmitter

### Transmitters
- Act as BLE Peripheral devices
- Accept AT commands via serial or BLE UART
- Send HID reports to connected devices
- Support multiple device pairing and switching

### Receiver Dongles
- Act as BLE Central devices
- Automatically scan for and connect to "AceRK" transmitters
- Forward received HID reports via USB to host computer
- Useful for connecting RelayKeys to devices that don't support BLE
- Enable use with older computers or systems requiring USB HID

## Compatibility

This firmware is designed to be compatible with:
- RelayKeys Python daemon
- RelayKeys CLI tools
- RelayKeys Qt desktop application
- Any software using the RelayKeys AT command protocol

### Receiver Dongle Compatibility
- Works with any RelayKeys transmitter (nRF52840 or ESP32)
- Compatible with any USB HID-capable host system
- Supports Windows, macOS, Linux, and embedded systems

## License

MIT License - Copyright Ace Centre 2024

## Contributing

1. Test with actual RelayKeys software
2. Ensure AT command compatibility
3. Follow existing code style
4. Update documentation

## Support

For issues and questions:
- GitHub Issues: [RelayKeys Repository](https://github.com/AceCentre/RelayKeys)
- Documentation: [RelayKeys Docs](https://docs.acecentre.org.uk/products/v/relaykeys/)
