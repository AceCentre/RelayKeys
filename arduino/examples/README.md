# RelayKeys Arduino Examples

This directory contains example sketches and test programs for RelayKeys Arduino implementations.

## Available Examples

### RelayKeys_Basic_Test
**Purpose**: Demonstrates basic RelayKeys transmitter functionality by sending test AT commands.

**Hardware Required**:
- RelayKeys transmitter (nRF52840 or ESP32 with RelayKeys firmware)
- Target device paired with the transmitter (computer, phone, tablet)

**Usage**:
1. Upload RelayKeys firmware to your transmitter board
2. Pair the transmitter with a target device
3. Upload this test sketch to a second Arduino (or use serial monitor)
4. Connect the boards via serial or use USB serial
5. The test will automatically send various AT commands

**Test Commands Included**:
- Basic connectivity (`AT`)
- Mode checking (`AT+GETMODE`)
- Keyboard input (typing "Hello World")
- Mouse movement and clicking
- Volume control
- Device management commands

### ESP32_Receiver_Test
**Purpose**: Monitors and tests ESP32 receiver dongle functionality.

**Hardware Required**:
- ESP32 receiver dongle with receiver firmware
- RelayKeys transmitter for testing
- Host computer connected via USB
- Optional: Second Arduino for monitoring (or use serial monitor)

**Usage**:
1. Upload receiver firmware to ESP32 board
2. Upload this test sketch to monitoring Arduino (optional)
3. Connect ESP32 receiver to host computer via USB
4. Power on RelayKeys transmitter
5. Monitor serial output for connection status and HID data

**Monitoring Features**:
- Connection status tracking
- HID report counting
- Diagnostic messages
- Troubleshooting tips
- Manual test instructions

## Running the Examples

### Using Arduino IDE Serial Monitor
1. Upload the example sketch to your Arduino
2. Open Tools → Serial Monitor
3. Set baud rate to 115200
4. Follow the on-screen instructions

### Using a Second Arduino
1. Upload the example to a second Arduino board
2. Connect the boards via serial (TX/RX pins)
3. Power both boards
4. Monitor the output on the second board's serial connection

## Test Scenarios

### Transmitter Testing (RelayKeys_Basic_Test)
- **Keyboard Functionality**: Types test messages
- **Mouse Functionality**: Moves cursor and clicks buttons
- **Volume Control**: Tests media keys
- **Device Management**: Lists and manages paired devices
- **Mode Switching**: Tests serial/BLE mode changes

### Receiver Testing (ESP32_Receiver_Test)
- **BLE Scanning**: Monitors device discovery
- **Connection Management**: Tracks connection state
- **HID Forwarding**: Verifies data forwarding to host
- **Error Detection**: Identifies connection issues
- **Status Monitoring**: Provides real-time diagnostics

## Troubleshooting

### Common Issues

#### Transmitter Tests Fail
- Ensure transmitter is properly paired with target device
- Check that target device is in range and connected
- Verify AT command syntax is correct
- Check serial connection between test board and transmitter

#### Receiver Tests Show No Connection
- Verify transmitter is advertising as "AceRK"
- Check that ESP32 receiver has native USB HID support
- Ensure receiver firmware is properly uploaded
- Try pressing the button on receiver to restart scanning

#### No HID Output on Host
- Verify ESP32 board supports native USB HID (S2/S3/C3)
- Check USB cable and connection to host
- Ensure "USB CDC On Boot" is enabled in Arduino IDE
- Try different USB port or host computer

### Debug Mode
Enable debug mode in the firmware by uncommenting `#define DEBUG`:
- Shows detailed BLE communication
- Displays HID report data
- Provides connection diagnostics
- Helps identify protocol issues

## Creating Custom Tests

### For Transmitters
1. Copy `RelayKeys_Basic_Test` as a template
2. Modify the `testCommands[]` array with your AT commands
3. Adjust timing and test sequence as needed
4. Add custom test functions for specific scenarios

### For Receivers
1. Copy `ESP32_Receiver_Test` as a template
2. Modify the message parsing logic for your needs
3. Add custom monitoring functions
4. Implement specific test scenarios

## Example AT Commands

### Keyboard Commands
```
AT+BLEKEYBOARDCODE=00-00-0B-08-0F-0F-12-00  // Type "Hello"
AT+BLEKEYBOARDCODE=00-00-00-00-00-00-00-00  // Release all keys
AT+BLEKEYBOARDCODE=00-00-80-00-00-00-00-00  // Volume up
```

### Mouse Commands
```
AT+BLEHIDMOUSEMOVE=10,5,0,0     // Move right 10px, down 5px
AT+BLEHIDMOUSEBUTTON=l,click    // Left click
AT+BLEHIDMOUSEBUTTON=r,click    // Right click
```

### Device Management
```
AT+PRINTDEVLIST                 // List paired devices
AT+BLEADDNEWDEVICE             // Enter pairing mode
AT+SWITCHCONN                  // Switch to next device
```

## Contributing

When adding new examples:
1. Follow the existing code structure and commenting style
2. Include comprehensive documentation
3. Test with actual hardware before submitting
4. Add troubleshooting information for common issues
5. Update this README with the new example information

## License

MIT License - Copyright Ace Centre 2024
