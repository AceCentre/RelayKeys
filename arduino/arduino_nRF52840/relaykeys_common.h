/*********************************************************************
 RelayKeys Common Header
 
 Shared definitions and constants for RelayKeys Arduino implementations
 across different platforms (nRF52840, ESP32)
 
 Copyright Ace Centre 2024 - MIT Licence
 
 This file contains common AT command definitions, constants, and 
 utility functions that are shared between different hardware platforms.
*********************************************************************/

#ifndef RELAYKEYS_COMMON_H
#define RELAYKEYS_COMMON_H

// Version information
#define RELAYKEYS_VERSION "2.02"
#define FIRMWARE_NAME "RelayKeys"

// BLE Configuration
#define BLE_NAME "AceRK"
#define BLE_MANUFACTURER "Ace Centre"

// Timing constants
#define ADD_NEW_DEV_PROCESS_TIMEOUT 30000  // 30 seconds in milliseconds
#define SWAP_CONN_PROCESS_TIMEOUT 30000    // 30 seconds in milliseconds
#define BUTTON_DEBOUNCE_TIME 100           // 100ms debounce
#define BUTTON_CLICK_TIMEOUT 500           // 500ms for click detection

// Device list configuration
#define MAX_BLE_DEVICES 15
#define MAX_BLE_DEV_LIST_SIZE_DEFAULT 3
#define BLE_DEVICE_NAME_LENGTH 32

// AT Command responses
#define AT_RESPONSE_OK "OK\n"
#define AT_RESPONSE_ERROR "ERROR\n"
#define AT_RESPONSE_SUCCESS "SUCCESS\n"
#define AT_RESPONSE_INVALID_INPUT "INVALID_INPUT\n"
#define AT_RESPONSE_TIMEOUT "TIMEOUT\n"

// Mouse button definitions
typedef struct {
    char thechar;
    uint8_t button;
} mouse_button_map_t;

// Mouse button mappings (platform-specific values will be defined in each implementation)
extern const mouse_button_map_t mouse_buttons_map[];

// AT Command structure
typedef void (*action_func_t)(char *myLine);

typedef struct {
    char command[32 + 1]; // max 32 characters plus '\0' terminator
    action_func_t action;
} command_action_t;

// Common AT Commands (to be implemented by each platform)
extern const command_action_t commands[];

// Device state structure
typedef struct {
    bool ble_mode;
    bool flag_addDevProsStarted;
    bool flag_bleSwapConnProsStarted;
    bool flag_saveListToFile;
    uint8_t bleDeviceNameListIndex;
    uint8_t maxBleDevListSize;
    uint8_t switchBleConnStartIndex;
    uint8_t switchBleConnCurrIndex;
    uint32_t addDevProsStartTicks;
    uint32_t swapConnProsStartTicks;
    char bleDeviceNameList[MAX_BLE_DEVICES][BLE_DEVICE_NAME_LENGTH];
} device_state_t;

// Function prototypes (to be implemented by each platform)
void at_response(const char *msg);
void execute(uint16_t conn_handle, char *myLine);
void receive_char(uint16_t conn_handle, char receive_char);
void updateStatusLED();
uint8_t detect_click();
void toLower(char *s);

// AT Command handlers (to be implemented by each platform)
void sendBLEKeyboardCode(char *myLine);
void sendBLEMouseMove(char *line);
void sendBLEMouseButton(char *line);
void sendBleSendCurrentDeviceName(char *myLine);
void addNewBleDevice(char *myLine);
void removeBleDevice(char *myLine);
void switchBleConnection(char *myLine);
void printBleDevList(char *myLine);
void setBleMaxDevListSize(char *myLine);
void deleteDevList(char *myLine);
void change_mode(char *myLine);
void get_mode(char *myLine);

// File system functions (to be implemented by each platform)
void save_devList_toFile(void);
void load_devList_fromFile(void);
void load_mode_file(void);
void save_tmp_file(void);
void load_tmp_file(void);

// Utility functions
inline void toLowerCommon(char *s) {
    while (*s) {
        if (isupper(*s)) {
            *s += 0x20;
        }
        s++;
    }
}

// Common mouse button definitions (values may vary by platform)
#define MOUSE_BUTTON_LEFT_CHAR 'l'
#define MOUSE_BUTTON_RIGHT_CHAR 'r'
#define MOUSE_BUTTON_MIDDLE_CHAR 'm'
#define MOUSE_BUTTON_BACKWARD_CHAR 'b'
#define MOUSE_BUTTON_FORWARD_CHAR 'f'
#define MOUSE_BUTTON_RELEASE_CHAR '0'

// HID Report constants
#define HID_KEYBOARD_REPORT_SIZE 8
#define HID_MOUSE_REPORT_SIZE 4

// Special key codes for volume control
#define KEYCODE_MUTE 0x7F
#define KEYCODE_VOLUME_UP 0x80
#define KEYCODE_VOLUME_DOWN 0x81

// Consumer key codes
#define CONSUMER_KEY_MUTE 0xE2
#define CONSUMER_KEY_VOLUME_UP 0xE9
#define CONSUMER_KEY_VOLUME_DOWN 0xEA

// Modifier key bit masks
#define MODIFIER_LEFT_CTRL   0x01
#define MODIFIER_LEFT_SHIFT  0x02
#define MODIFIER_LEFT_ALT    0x04
#define MODIFIER_LEFT_META   0x08
#define MODIFIER_RIGHT_CTRL  0x10
#define MODIFIER_RIGHT_SHIFT 0x20
#define MODIFIER_RIGHT_ALT   0x40
#define MODIFIER_RIGHT_META  0x80

// Debug macro
#ifdef DEBUG
#define DEBUG_PRINT(x) Serial.print(x)
#define DEBUG_PRINTLN(x) Serial.println(x)
#else
#define DEBUG_PRINT(x)
#define DEBUG_PRINTLN(x)
#endif

#endif // RELAYKEYS_COMMON_H
