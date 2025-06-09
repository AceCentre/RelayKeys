/*********************************************************************
 RelayKeys Raspberry Pi Pico W Implementation
 
 EXPERIMENTAL - UNTESTED
 
 Pico W implementation for RelayKeys using BTStack - BLE HID Keyboard and Mouse
 Compatible with the RelayKeys AT command protocol
 
 Copyright Ace Centre 2024 - MIT Licence
 
 This implementation uses BTStack (the official Bluetooth stack for Pico W)
 instead of Arduino BLE libraries for better performance and compatibility.
 
 Hardware Requirements:
 - Raspberry Pi Pico W
 - Optional: LED for status indication (built-in LED on GPIO 25)
 - Optional: Button for mode switching (GPIO 14)
 
 Based on BTStack hid_keyboard_demo.c and adapted for RelayKeys compatibility.
 
 WARNING: This is experimental code and has not been tested with hardware.
 Use at your own risk and expect bugs and compatibility issues.
*********************************************************************/

#include <stdio.h>
#include <string.h>
#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "btstack.h"
#include "btstack_run_loop.h"
#include "../common/relaykeys_common.h"
#include "board_config.h"

//#define DEBUG // uncomment this line to see additional prints in Serial monitor

// BTStack HID Service
static uint8_t hid_service_buffer[300];
static uint8_t device_id_sdp_service_buffer[100];
static const char hid_device_name[] = BLE_NAME;
static btstack_packet_callback_registration_t hci_event_callback_registration;
static uint16_t hid_cid;

// Device state
device_state_t deviceState = {0};
bool deviceConnected = false;
uint16_t target_ble_conn = 0;

// AT Command processing
static char receive_buffer[256];
static uint8_t receive_buffer_pos = 0;

// HID Report descriptors (from BTStack example)
#define REPORT_ID_KEYBOARD 0x01
#define REPORT_ID_MOUSE    0x02
#define REPORT_ID_CONSUMER 0x03

// Keyboard HID descriptor (from BTStack)
static const uint8_t hid_descriptor_keyboard[] = {
    0x05, 0x01,        // Usage Page (Generic Desktop)
    0x09, 0x06,        // Usage (Keyboard)
    0xa1, 0x01,        // Collection (Application)
    0x85, REPORT_ID_KEYBOARD, // Report ID
    
    // Modifier byte
    0x75, 0x01,        // Report Size (1)
    0x95, 0x08,        // Report Count (8)
    0x05, 0x07,        // Usage Page (Key codes)
    0x19, 0xe0,        // Usage Minimum (Keyboard LeftControl)
    0x29, 0xe7,        // Usage Maximum (Keyboard Right GUI)
    0x15, 0x00,        // Logical Minimum (0)
    0x25, 0x01,        // Logical Maximum (1)
    0x81, 0x02,        // Input (Data, Variable, Absolute)
    
    // Reserved byte
    0x75, 0x01,        // Report Size (1)
    0x95, 0x08,        // Report Count (8)
    0x81, 0x03,        // Input (Constant, Variable, Absolute)
    
    // LED report (output)
    0x95, 0x05,        // Report Count (5)
    0x75, 0x01,        // Report Size (1)
    0x05, 0x08,        // Usage Page (LEDs)
    0x19, 0x01,        // Usage Minimum (Num Lock)
    0x29, 0x05,        // Usage Maximum (Kana)
    0x91, 0x02,        // Output (Data, Variable, Absolute)
    0x95, 0x01,        // Report Count (1)
    0x75, 0x03,        // Report Size (3)
    0x91, 0x03,        // Output (Constant, Variable, Absolute)
    
    // Keycodes
    0x95, 0x06,        // Report Count (6)
    0x75, 0x08,        // Report Size (8)
    0x15, 0x00,        // Logical Minimum (0)
    0x25, 0xff,        // Logical Maximum (255)
    0x05, 0x07,        // Usage Page (Key codes)
    0x19, 0x00,        // Usage Minimum (Reserved)
    0x29, 0xff,        // Usage Maximum (Reserved)
    0x81, 0x00,        // Input (Data, Array)
    0xc0,              // End Collection
    
    // Mouse HID descriptor
    0x05, 0x01,        // Usage Page (Generic Desktop)
    0x09, 0x02,        // Usage (Mouse)
    0xa1, 0x01,        // Collection (Application)
    0x85, REPORT_ID_MOUSE, // Report ID
    0x09, 0x01,        // Usage (Pointer)
    0xa1, 0x00,        // Collection (Physical)
    
    // Buttons
    0x05, 0x09,        // Usage Page (Button)
    0x19, 0x01,        // Usage Minimum (Button 1)
    0x29, 0x05,        // Usage Maximum (Button 5)
    0x15, 0x00,        // Logical Minimum (0)
    0x25, 0x01,        // Logical Maximum (1)
    0x95, 0x05,        // Report Count (5)
    0x75, 0x01,        // Report Size (1)
    0x81, 0x02,        // Input (Data, Variable, Absolute)
    0x95, 0x01,        // Report Count (1)
    0x75, 0x03,        // Report Size (3)
    0x81, 0x03,        // Input (Constant, Variable, Absolute)
    
    // Position
    0x05, 0x01,        // Usage Page (Generic Desktop)
    0x09, 0x30,        // Usage (X)
    0x09, 0x31,        // Usage (Y)
    0x09, 0x38,        // Usage (Wheel)
    0x15, 0x81,        // Logical Minimum (-127)
    0x25, 0x7f,        // Logical Maximum (127)
    0x75, 0x08,        // Report Size (8)
    0x95, 0x03,        // Report Count (3)
    0x81, 0x06,        // Input (Data, Variable, Relative)
    0xc0,              // End Collection
    0xc0,              // End Collection
    
    // Consumer Control (Media Keys)
    0x05, 0x0c,        // Usage Page (Consumer)
    0x09, 0x01,        // Usage (Consumer Control)
    0xa1, 0x01,        // Collection (Application)
    0x85, REPORT_ID_CONSUMER, // Report ID
    0x05, 0x0c,        // Usage Page (Consumer)
    0x15, 0x00,        // Logical Minimum (0)
    0x25, 0x01,        // Logical Maximum (1)
    0x75, 0x01,        // Report Size (1)
    0x95, 0x10,        // Report Count (16)
    0x09, 0xe2,        // Usage (Mute)
    0x09, 0xe9,        // Usage (Volume Increment)
    0x09, 0xea,        // Usage (Volume Decrement)
    0x81, 0x02,        // Input (Data, Variable, Absolute)
    0xc0,              // End Collection
};

// Forward declarations
static void packet_handler(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size);
void setup_hid_service(void);
void process_uart_input(void);
void updateStatusLED(void);

// Mouse button mapping for Pico W
const mouse_button_map_t mouse_buttons_map[] = {
    {MOUSE_BUTTON_LEFT_CHAR, 0x01},
    {MOUSE_BUTTON_RIGHT_CHAR, 0x02},
    {MOUSE_BUTTON_MIDDLE_CHAR, 0x04},
    {MOUSE_BUTTON_BACKWARD_CHAR, 0x08},
    {MOUSE_BUTTON_FORWARD_CHAR, 0x10},
    {MOUSE_BUTTON_RELEASE_CHAR, 0},
};

void setup() {
    stdio_init_all();
    
    // Initialize CYW43 (WiFi/Bluetooth chip)
    if (cyw43_arch_init()) {
        printf("Failed to initialize CYW43\n");
        return;
    }
    
    // Initialize pins
    INIT_USER_BUTTON();
    INIT_STATUS_LED();
    
    printf("RelayKeys Pico W Starting...\n");
    PRINT_BOARD_INFO();
    
    // Initialize device state
    deviceState.maxBleDevListSize = MAX_BLE_DEV_LIST_SIZE_DEFAULT;
    deviceState.ble_mode = false; // Start in serial mode
    
    // Load configuration (placeholder - would need flash storage implementation)
    // load_mode_file();
    // load_devList_fromFile();
    
    // Initialize BTStack
    hci_event_callback_registration.callback = &packet_handler;
    hci_add_event_handler(&hci_event_callback_registration);
    
    // Setup HID service
    setup_hid_service();
    
    // Set device name
    gap_set_local_name(BLE_NAME);
    gap_discoverable_control(1);
    gap_set_class_of_device(0x2540); // Keyboard class
    
    // Start BTStack
    hci_power_control(HCI_POWER_ON);
    
    updateStatusLED();
    
    printf("RelayKeys Pico W Ready\n");
}

void loop() {
    // Process BTStack events
    btstack_run_loop_execute_once();
    
    // Handle serial input when not in BLE mode
    if (!deviceState.ble_mode) {
        process_uart_input();
    }
    
    // Handle button press
    if (BUTTON_PRESSED()) {
        uint8_t clicks = detect_click();
        if (clicks == 1) {
            addNewBleDevice("");
        } else if (clicks >= 2) {
            change_mode("");
        }
    }
    
    // Handle file saving (placeholder)
    if (deviceState.flag_saveListToFile) {
        deviceState.flag_saveListToFile = false;
        // save_devList_toFile();
    }
    
    // Handle add device timeout
    if (deviceState.flag_addDevProsStarted) {
        if (to_ms_since_boot(get_absolute_time()) - deviceState.addDevProsStartTicks >= ADD_NEW_DEV_PROCESS_TIMEOUT) {
            deviceState.flag_addDevProsStarted = false;
            updateStatusLED();
            DEBUG_PRINTLN("Add device timeout");
        }
    }
    
    updateStatusLED();
    sleep_ms(10);
}

void setup_hid_service(void) {
    // Initialize HID Device service
    hid_device_init();
    
    // Set HID parameters
    hid_device_register_packet_handler(packet_handler);
    
    // Set HID descriptor
    hid_device_init_with_descriptor(hid_descriptor_keyboard, sizeof(hid_descriptor_keyboard));
    
    // Register for HID events
    hci_event_callback_registration.callback = &packet_handler;
    hci_add_event_handler(&hci_event_callback_registration);
}

static void packet_handler(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size) {
    UNUSED(channel);
    UNUSED(size);
    
    if (packet_type != HCI_EVENT_PACKET) return;
    
    switch (hci_event_packet_get_type(packet)) {
        case HCI_EVENT_HID_META:
            switch (hci_event_hid_meta_get_subevent_code(packet)) {
                case HID_SUBEVENT_CONNECTION_OPENED:
                    hid_cid = hid_subevent_connection_opened_get_hid_cid(packet);
                    deviceConnected = true;
                    printf("HID Connected\n");
                    break;
                case HID_SUBEVENT_CONNECTION_CLOSED:
                    hid_cid = 0;
                    deviceConnected = false;
                    printf("HID Disconnected\n");
                    break;
                default:
                    break;
            }
            break;
        default:
            break;
    }
}

void process_uart_input(void) {
    int c = getchar_timeout_us(0); // Non-blocking read
    if (c != PICO_ERROR_TIMEOUT) {
        receive_char(0, (char)c);
    }
}

void updateStatusLED(void) {
    static uint32_t last_update = 0;
    static bool led_state = false;
    uint32_t now = to_ms_since_boot(get_absolute_time());

    if (deviceState.flag_addDevProsStarted) {
        // Fast blink for pairing mode
        if (now - last_update > 150) {
            led_state = !led_state;
            LED_SET(led_state);
            last_update = now;
        }
    } else if (deviceState.ble_mode) {
        // Slow blink for BLE mode
        if (now - last_update > 500) {
            led_state = !led_state;
            LED_SET(led_state);
            last_update = now;
        }
    } else {
        // Solid on for serial mode
        LED_ON();
    }
}

uint8_t detect_click(void) {
    uint32_t press_time = to_ms_since_boot(get_absolute_time());
    uint8_t click_counter = 0;

    while ((to_ms_since_boot(get_absolute_time()) - press_time) < BUTTON_CLICK_TIMEOUT) {
        if (BUTTON_PRESSED() && (to_ms_since_boot(get_absolute_time()) - press_time) < BUTTON_CLICK_TIMEOUT) {
            click_counter++;
            sleep_ms(BUTTON_DEBOUNCE_TIME);
            while (BUTTON_PRESSED()) {
                sleep_ms(BUTTON_DEBOUNCE_TIME);
            }
            press_time = to_ms_since_boot(get_absolute_time());
        }
    }

    return click_counter;
}

void toLower(char *s) {
    toLowerCommon(s);
}

void at_response(const char *msg) {
    printf("%s", msg);
}

// AT Command implementations
void sendBLEKeyboardCode(char *myLine) {
    if (!deviceConnected) {
        at_response("ERROR: Not connected\n");
        return;
    }

    uint8_t report[9]; // Report ID + 8 bytes
    memset(report, 0, sizeof(report));

    // Parse keyboard report: "XX-XX-XX-XX-XX-XX-XX-XX"
    char *p = strtok(myLine, "=");
    p = strtok(NULL, "-");

    report[0] = REPORT_ID_KEYBOARD; // Report ID
    for (size_t i = 1; p && (i < sizeof(report)); i++) {
        report[i] = strtoul(p, NULL, 16);
        p = strtok(NULL, "-");
    }

    // Handle special consumer keys
    switch (report[3]) { // keycode[0] position
        case KEYCODE_MUTE:
        case KEYCODE_VOLUME_UP:
        case KEYCODE_VOLUME_DOWN: {
            uint8_t consumer_report[3] = {REPORT_ID_CONSUMER, 0, 0};
            if (report[3] == KEYCODE_MUTE) consumer_report[1] = CONSUMER_KEY_MUTE;
            else if (report[3] == KEYCODE_VOLUME_UP) consumer_report[1] = CONSUMER_KEY_VOLUME_UP;
            else if (report[3] == KEYCODE_VOLUME_DOWN) consumer_report[1] = CONSUMER_KEY_VOLUME_DOWN;

            hid_device_send_input_report(hid_cid, consumer_report, sizeof(consumer_report));
            sleep_ms(10);
            consumer_report[1] = 0; // Release
            hid_device_send_input_report(hid_cid, consumer_report, sizeof(consumer_report));
            break;
        }
        default:
            // Regular keyboard report
            hid_device_send_input_report(hid_cid, report, sizeof(report));
            break;
    }

    at_response(AT_RESPONSE_OK);
}

void sendBLEMouseMove(char *line) {
    if (!deviceConnected) {
        at_response("ERROR: Not connected\n");
        return;
    }

    int32_t x = 0, y = 0, wy = 0, wx = 0;

    // Parse: X,Y,WY,WX
    char *p = strtok(line, "=");
    p = strtok(NULL, ",");

    for (size_t i = 0; p != NULL; i++) {
        if (i == 0) x = strtol(p, NULL, 10);
        else if (i == 1) y = strtol(p, NULL, 10);
        else if (i == 2) wy = strtol(p, NULL, 10);
        else if (i == 3) wx = strtol(p, NULL, 10);
        else {
            at_response(AT_RESPONSE_INVALID_INPUT);
            return;
        }
        p = strtok(NULL, ",");
    }

    uint8_t mouse_report[5] = {REPORT_ID_MOUSE, 0, 0, 0, 0};
    mouse_report[1] = 0; // buttons
    mouse_report[2] = (int8_t)((x > 127) ? 127 : (x < -127) ? -127 : x);
    mouse_report[3] = (int8_t)((y > 127) ? 127 : (y < -127) ? -127 : y);
    mouse_report[4] = (int8_t)((wy > 127) ? 127 : (wy < -127) ? -127 : wy);

    hid_device_send_input_report(hid_cid, mouse_report, sizeof(mouse_report));

    at_response(AT_RESPONSE_OK);
}

void sendBLEMouseButton(char *line) {
    if (!deviceConnected) {
        at_response("ERROR: Not connected\n");
        return;
    }

    uint8_t button = 0;
    int mode = 0; // 0=press/release, 1=click, 2=doubleclick

    // Parse: Button[,Action]
    char *p = strtok(line, "=");
    p = strtok(NULL, ",");

    for (size_t i = 0; p != NULL; i++) {
        if (i == 0) {
            // Find button
            for (int c = 0; c < sizeof(mouse_buttons_map) / sizeof(mouse_buttons_map[0]); c++) {
                if (mouse_buttons_map[c].thechar == p[0]) {
                    button = mouse_buttons_map[c].button;
                    break;
                }
            }
        } else if (i == 1) {
            toLower(p);
            if (strcmp(p, "click") == 0) mode = 1;
            else if (strcmp(p, "doubleclick") == 0) mode = 2;
        } else {
            at_response(AT_RESPONSE_INVALID_INPUT);
            return;
        }
        p = strtok(NULL, ",");
    }

    uint8_t mouse_report[5] = {REPORT_ID_MOUSE, 0, 0, 0, 0};

    if (mode == 1) { // Click
        mouse_report[1] = button;
        hid_device_send_input_report(hid_cid, mouse_report, sizeof(mouse_report));
        sleep_ms(40);
        mouse_report[1] = 0;
        hid_device_send_input_report(hid_cid, mouse_report, sizeof(mouse_report));
    } else if (mode == 2) { // Double click
        for (int i = 0; i < 2; i++) {
            mouse_report[1] = button;
            hid_device_send_input_report(hid_cid, mouse_report, sizeof(mouse_report));
            sleep_ms(40);
            mouse_report[1] = 0;
            hid_device_send_input_report(hid_cid, mouse_report, sizeof(mouse_report));
            if (i == 0) sleep_ms(40);
        }
    } else { // Press/Release toggle
        mouse_report[1] = button;
        hid_device_send_input_report(hid_cid, mouse_report, sizeof(mouse_report));
    }

    at_response(AT_RESPONSE_OK);
}

// Placeholder implementations for device management
void sendBleSendCurrentDeviceName(char *myLine) {
    at_response("at+blecurrentdevicename\n");
    if (!deviceConnected) {
        at_response("NONE\n");
    } else {
        at_response("PicoW_Device\n");
    }
}

void addNewBleDevice(char *myLine) {
    at_response("at+bleaddnewdevice\n");

    if (deviceState.bleDeviceNameListIndex >= deviceState.maxBleDevListSize) {
        at_response("ERROR: Device list is full\n");
        return;
    }

    deviceState.flag_addDevProsStarted = true;
    deviceState.addDevProsStartTicks = to_ms_since_boot(get_absolute_time());
    updateStatusLED();

    char buff[256];
    snprintf(buff, sizeof(buff), "Connect your device with %s\n", BLE_NAME);
    at_response(buff);
}

void removeBleDevice(char *myLine) {
    at_response("at+bleremovedevice\n");
    at_response("Device removal not implemented in experimental version\n");
}

void switchBleConnection(char *myLine) {
    at_response("at+switchconn\n");
    at_response("Connection switching not implemented in experimental version\n");
}

void printBleDevList(char *myLine) {
    at_response("at+printdevlist\n");
    at_response("Device list not implemented in experimental version\n");
}

void setBleMaxDevListSize(char *myLine) {
    at_response("at+blemaxdevlistsize\n");

    char *p = strtok(myLine, "=");
    p = strtok(NULL, "\0");

    if (p) {
        uint8_t newSize = atoi(p);
        if (newSize > 0 && newSize <= MAX_BLE_DEVICES) {
            deviceState.maxBleDevListSize = newSize;
            at_response(AT_RESPONSE_SUCCESS);
        } else {
            at_response("ERROR: Invalid Value\n");
        }
    } else {
        at_response("ERROR: Invalid Value\n");
    }
}

void deleteDevList(char *myLine) {
    at_response("at+deletedevlist\n");

    // Clear device list
    deviceState.bleDeviceNameListIndex = 0;
    memset(deviceState.bleDeviceNameList, 0, sizeof(deviceState.bleDeviceNameList));

    // Disconnect current device
    if (deviceConnected && hid_cid) {
        hid_device_disconnect(hid_cid);
    }

    at_response(AT_RESPONSE_SUCCESS);
}

void change_mode(char *myLine) {
    printf("Changing operating mode\n");

    at_response(AT_RESPONSE_OK);

    deviceState.ble_mode = !deviceState.ble_mode;

    // Save mode (placeholder - would need flash storage implementation)
    // save_mode_file();

    // Disconnect and restart advertising
    if (deviceConnected && hid_cid) {
        hid_device_disconnect(hid_cid);
    }

    printf("Mode changed to: %s\n", deviceState.ble_mode ? "BLE" : "Serial");
}

void get_mode(char *myLine) {
    if (deviceState.ble_mode) {
        at_response("BLE\n");
    } else {
        at_response("Serial\n");
    }
}

// Command parsing and execution
void execute(uint16_t conn_handle, char *myLine) {
    if (myLine == NULL || *myLine == '\0')
        return;

    char cmdTemp[100];
    memcpy(cmdTemp, myLine, 100);

    char *cmd = strtok(cmdTemp, "=");
    if (cmd == NULL || *cmd == '\0')
        return;

    toLower(cmd);

    // Find and execute command
    for (size_t i = 0; i < sizeof(commands) / sizeof(commands[0]); i++) {
        if (strcmp(cmd, commands[i].command) == 0) {
            commands[i].action(myLine);
            if (!deviceState.ble_mode) {
                sleep_ms(30);
            }
            return;
        }
    }

    // Command not found
    at_response(AT_RESPONSE_OK);
}

void receive_char(uint16_t conn_handle, char receive_char) {
    switch (receive_char) {
        case '\n':
            break;
        case '\r':
            receive_buffer[receive_buffer_pos] = '\0';
            execute(conn_handle, receive_buffer);
            receive_buffer_pos = 0;
            break;
        case '\b': // backspace
            if (receive_buffer_pos > 0) {
                receive_buffer_pos--;
            }
            break;
        default:
            receive_buffer[receive_buffer_pos++] = receive_char;
            if (receive_buffer_pos >= sizeof(receive_buffer) - 1) {
                receive_buffer[receive_buffer_pos] = '\0';
                execute(conn_handle, receive_buffer);
                receive_buffer_pos = 0;
            }
            break;
    }
}

// Placeholder file system functions (would need flash storage implementation)
void save_devList_toFile(void) {
    printf("Device list save not implemented\n");
}

void load_devList_fromFile(void) {
    printf("Device list load not implemented\n");
}

void load_mode_file(void) {
    deviceState.ble_mode = false; // Default to serial mode
    printf("Mode load not implemented, defaulting to serial mode\n");
}

void save_tmp_file(void) {
    printf("Temp file save not implemented\n");
}

void load_tmp_file(void) {
    printf("Temp file load not implemented\n");
}

// AT Command table
const command_action_t commands[] = {
    {"at+blekeyboardcode", sendBLEKeyboardCode},
    {"at+blehidmousemove", sendBLEMouseMove},
    {"at+blehidmousebutton", sendBLEMouseButton},
    {"at+blecurrentdevicename", sendBleSendCurrentDeviceName},
    {"at+bleaddnewdevice", addNewBleDevice},
    {"at+bleremovedevice", removeBleDevice},
    {"at+switchconn", switchBleConnection},
    {"at+printdevlist", printBleDevList},
    {"at+blemaxdevlistsize", setBleMaxDevListSize},
    {"at+resetdevlist", deleteDevList},
    {"at+switchmode", change_mode},
    {"at+getmode", get_mode},
};
