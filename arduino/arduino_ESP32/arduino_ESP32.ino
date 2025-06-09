/*********************************************************************
 RelayKeys ESP32 Implementation
 
 ESP32 implementation for RelayKeys - BLE HID Keyboard and Mouse
 Compatible with the RelayKeys AT command protocol
 
 Copyright Ace Centre 2024 - MIT Licence
 
 This implementation provides the same AT command interface as the 
 nRF52840 version but uses ESP32 BLE libraries and capabilities.
 
 Hardware Requirements:
 - ESP32 development board (ESP32-WROOM, ESP32-S3, etc.)
 - Optional: LED for status indication
 - Optional: Button for mode switching
 
 Based on the asterics/esp32_mouse_keyboard project and adapted
 for RelayKeys compatibility.
*********************************************************************/

#include "BLEDevice.h"
#include "BLEHIDDevice.h"
#include "HIDTypes.h"
#include "HIDKeyboardTypes.h"
#include "BLE2902.h"
#include "BLECharacteristic.h"
#include "SPIFFS.h"
#include "Preferences.h"
#include "../common/relaykeys_common.h"
#include "board_config.h"

//#define DEBUG // uncomment this line to see additional prints in Serial monitor

// BLE objects
BLEHIDDevice* pHID = nullptr;
BLECharacteristic* pInputKeyboard = nullptr;
BLECharacteristic* pInputMouse = nullptr;
BLECharacteristic* pInputConsumer = nullptr;
BLECharacteristic* pOutputKeyboard = nullptr;
BLEServer* pServer = nullptr;
BLEService* pService = nullptr;
BLEAdvertising* pAdvertising = nullptr;

// UART Service for AT commands
BLEService* pUartService = nullptr;
BLECharacteristic* pTxCharacteristic = nullptr;
BLECharacteristic* pRxCharacteristic = nullptr;

// Device state
device_state_t deviceState = {0};
uint8_t keys[HID_KEYBOARD_REPORT_SIZE] = {0}; // Current keyboard state
bool deviceConnected = false;
bool oldDeviceConnected = false;
uint16_t target_ble_conn = 0;
uint16_t response_ble_conn = 0;

// Preferences for persistent storage
Preferences preferences;

// Mouse button mapping for ESP32
const mouse_button_map_t mouse_buttons_map[] = {
    {MOUSE_BUTTON_LEFT_CHAR, MOUSE_LEFT},
    {MOUSE_BUTTON_RIGHT_CHAR, MOUSE_RIGHT},
    {MOUSE_BUTTON_MIDDLE_CHAR, MOUSE_MIDDLE},
    {MOUSE_BUTTON_BACKWARD_CHAR, 0x08}, // Back button
    {MOUSE_BUTTON_FORWARD_CHAR, 0x10},  // Forward button
    {MOUSE_BUTTON_RELEASE_CHAR, 0},
};

// Forward declarations
void startBLE();
void updateStatusLED();
void setupHID();
void setupUART();

// BLE Server callbacks
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
        deviceConnected = true;
        DEBUG_PRINTLN("Device connected");
    }

    void onDisconnect(BLEServer* pServer) {
        deviceConnected = false;
        DEBUG_PRINTLN("Device disconnected");
    }
};

// UART RX callback for AT commands
class UartCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
        std::string rxValue = pCharacteristic->getValue();
        
        if (rxValue.length() > 0) {
            for (int i = 0; i < rxValue.length(); i++) {
                receive_char(0, rxValue[i]);
            }
        }
    }
};

void setup() {
    Serial.begin(115200);
    delay(1000);

    DEBUG_PRINTLN("RelayKeys ESP32 Starting...");
    PRINT_BOARD_INFO();

    // Initialize pins using board configuration
    INIT_USER_BUTTON();
    INIT_STATUS_LED();
    
    // Initialize SPIFFS for file storage
    if (!SPIFFS.begin(true)) {
        DEBUG_PRINTLN("SPIFFS Mount Failed");
    }
    
    // Initialize preferences
    preferences.begin("relaykeys", false);
    
    // Load configuration
    load_mode_file();
    load_devList_fromFile();
    load_tmp_file();
    
    // Initialize device state
    deviceState.maxBleDevListSize = MAX_BLE_DEV_LIST_SIZE_DEFAULT;
    
    // Start BLE
    startBLE();
    
    updateStatusLED();
    
    DEBUG_PRINTLN("RelayKeys ESP32 Ready");
}

void startBLE() {
    BLEDevice::init(BLE_NAME);
    pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());
    
    setupHID();
    setupUART();
    
    // Start advertising
    pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->setAppearance(HID_KEYBOARD);
    pAdvertising->addServiceUUID(pService->getUUID());
    pAdvertising->addServiceUUID(pUartService->getUUID());
    pAdvertising->setScanResponse(true);
    pAdvertising->setMinPreferred(0x06);
    pAdvertising->setMinPreferred(0x12);
    
    BLEDevice::startAdvertising();
    DEBUG_PRINTLN("BLE advertising started");
}

void setupHID() {
    pHID = new BLEHIDDevice(pServer);
    
    // Set HID device info
    pHID->manufacturer()->setValue(BLE_MANUFACTURER);
    pHID->pnp(0x02, 0xe502, 0xa111, 0x0210);
    pHID->hidInfo(0x00, 0x02);
    
    // Keyboard
    pInputKeyboard = pHID->inputReport(1); // Report ID 1
    pOutputKeyboard = pHID->outputReport(1);
    
    // Mouse  
    pInputMouse = pHID->inputReport(2); // Report ID 2
    
    // Consumer (media keys)
    pInputConsumer = pHID->inputReport(3); // Report ID 3
    
    // Set HID report maps
    pHID->reportMap((uint8_t*)_hidReportDescriptor, sizeof(_hidReportDescriptor));
    pHID->startServices();
    
    pService = pHID->hidService();
}

void setupUART() {
    // Create UART service for AT commands
    pUartService = pServer->createService("6E400001-B5A3-F393-E0A9-E50E24DCCA9E");
    
    // TX characteristic (ESP32 -> Client)
    pTxCharacteristic = pUartService->createCharacteristic(
        "6E400003-B5A3-F393-E0A9-E50E24DCCA9E",
        BLECharacteristic::PROPERTY_NOTIFY
    );
    pTxCharacteristic->addDescriptor(new BLE2902());
    
    // RX characteristic (Client -> ESP32)
    pRxCharacteristic = pUartService->createCharacteristic(
        "6E400002-B5A3-F393-E0A9-E50E24DCCA9E",
        BLECharacteristic::PROPERTY_WRITE
    );
    pRxCharacteristic->setCallbacks(new UartCallbacks());
    
    pUartService->start();
}

void loop() {
    // Handle serial input when not in BLE mode
    if (!deviceState.ble_mode && Serial.available() > 0) {
        receive_char(0, Serial.read());
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
    
    // Handle file saving
    if (deviceState.flag_saveListToFile) {
        deviceState.flag_saveListToFile = false;
        save_devList_toFile();
    }
    
    // Handle add device timeout
    if (deviceState.flag_addDevProsStarted) {
        if (millis() - deviceState.addDevProsStartTicks >= ADD_NEW_DEV_PROCESS_TIMEOUT) {
            deviceState.flag_addDevProsStarted = false;
            updateStatusLED();
            DEBUG_PRINTLN("Add device timeout");
        }
    }
    
    // Handle connection switching timeout
    if (deviceState.flag_bleSwapConnProsStarted) {
        if (millis() - deviceState.swapConnProsStartTicks >= SWAP_CONN_PROCESS_TIMEOUT) {
            deviceState.flag_bleSwapConnProsStarted = false;
            DEBUG_PRINTLN("Connection switch timeout");
        }
    }
    
    // Handle BLE connection state changes
    if (!deviceConnected && oldDeviceConnected) {
        delay(500);
        pServer->startAdvertising();
        DEBUG_PRINTLN("Start advertising");
        oldDeviceConnected = deviceConnected;
    }
    
    if (deviceConnected && !oldDeviceConnected) {
        oldDeviceConnected = deviceConnected;
    }
    
    delay(10);
}

// HID Report Descriptor (simplified version)
static const uint8_t _hidReportDescriptor[] = {
    // Keyboard
    0x05, 0x01,        // Usage Page (Generic Desktop Ctrls)
    0x09, 0x06,        // Usage (Keyboard)
    0xA1, 0x01,        // Collection (Application)
    0x85, 0x01,        //   Report ID (1)
    0x05, 0x07,        //   Usage Page (Kbrd/Keypad)
    0x19, 0xE0,        //   Usage Minimum (0xE0)
    0x29, 0xE7,        //   Usage Maximum (0xE7)
    0x15, 0x00,        //   Logical Minimum (0)
    0x25, 0x01,        //   Logical Maximum (1)
    0x75, 0x01,        //   Report Size (1)
    0x95, 0x08,        //   Report Count (8)
    0x81, 0x02,        //   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x95, 0x01,        //   Report Count (1)
    0x75, 0x08,        //   Report Size (8)
    0x81, 0x03,        //   Input (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x95, 0x06,        //   Report Count (6)
    0x75, 0x08,        //   Report Size (8)
    0x15, 0x00,        //   Logical Minimum (0)
    0x25, 0x65,        //   Logical Maximum (101)
    0x05, 0x07,        //   Usage Page (Kbrd/Keypad)
    0x19, 0x00,        //   Usage Minimum (0x00)
    0x29, 0x65,        //   Usage Maximum (0x65)
    0x81, 0x00,        //   Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,              // End Collection

    // Mouse
    0x05, 0x01,        // Usage Page (Generic Desktop Ctrls)
    0x09, 0x02,        // Usage (Mouse)
    0xA1, 0x01,        // Collection (Application)
    0x85, 0x02,        //   Report ID (2)
    0x09, 0x01,        //   Usage (Pointer)
    0xA1, 0x00,        //   Collection (Physical)
    0x05, 0x09,        //     Usage Page (Button)
    0x19, 0x01,        //     Usage Minimum (0x01)
    0x29, 0x05,        //     Usage Maximum (0x05)
    0x15, 0x00,        //     Logical Minimum (0)
    0x25, 0x01,        //     Logical Maximum (1)
    0x95, 0x05,        //     Report Count (5)
    0x75, 0x01,        //     Report Size (1)
    0x81, 0x02,        //     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x95, 0x01,        //     Report Count (1)
    0x75, 0x03,        //     Report Size (3)
    0x81, 0x03,        //     Input (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x01,        //     Usage Page (Generic Desktop Ctrls)
    0x09, 0x30,        //     Usage (X)
    0x09, 0x31,        //     Usage (Y)
    0x09, 0x38,        //     Usage (Wheel)
    0x15, 0x81,        //     Logical Minimum (-127)
    0x25, 0x7F,        //     Logical Maximum (127)
    0x75, 0x08,        //     Report Size (8)
    0x95, 0x03,        //     Report Count (3)
    0x81, 0x06,        //     Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,              //   End Collection
    0xC0,              // End Collection

    // Consumer (Media Keys)
    0x05, 0x0C,        // Usage Page (Consumer)
    0x09, 0x01,        // Usage (Consumer Control)
    0xA1, 0x01,        // Collection (Application)
    0x85, 0x03,        //   Report ID (3)
    0x05, 0x0C,        //   Usage Page (Consumer)
    0x15, 0x00,        //   Logical Minimum (0)
    0x25, 0x01,        //   Logical Maximum (1)
    0x75, 0x01,        //   Report Size (1)
    0x95, 0x10,        //   Report Count (16)
    0x09, 0xE2,        //   Usage (Mute)
    0x09, 0xE9,        //   Usage (Volume Increment)
    0x09, 0xEA,        //   Usage (Volume Decrement)
    0x81, 0x02,        //   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,              // End Collection
};

// Utility functions
void updateStatusLED() {
    if (deviceState.flag_addDevProsStarted) {
        // Blink fast for pairing mode
        digitalWrite(STATUS_LED, (millis() / 150) % 2);
    } else if (deviceState.ble_mode) {
        // Slow blink for BLE mode
        digitalWrite(STATUS_LED, (millis() / 500) % 2);
    } else {
        // Solid on for serial mode
        LED_ON();
    }
}

uint8_t detect_click() {
    uint32_t press_time = millis();
    uint8_t click_counter = 0;

    while ((millis() - press_time) < BUTTON_CLICK_TIMEOUT) {
        if (BUTTON_PRESSED() && (millis() - press_time) < BUTTON_CLICK_TIMEOUT) {
            click_counter++;
            delay(BUTTON_DEBOUNCE_TIME);
            while (BUTTON_PRESSED()) {
                delay(BUTTON_DEBOUNCE_TIME);
            }
            press_time = millis();
        }
    }

    return click_counter;
}

void toLower(char *s) {
    toLowerCommon(s);
}

void at_response(const char *msg) {
    if (deviceState.ble_mode && deviceConnected && pTxCharacteristic) {
        pTxCharacteristic->setValue((uint8_t*)msg, strlen(msg));
        pTxCharacteristic->notify();
    } else {
        Serial.print(msg);
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
                delay(30);
            }
            return;
        }
    }

    // Command not found
    at_response(AT_RESPONSE_OK);
}

void receive_char(uint16_t conn_handle, char receive_char) {
    static uint8_t bytesIn = 0;
    static char receive_buffer[256];

    switch (receive_char) {
        case '\n':
            break;
        case '\r':
            receive_buffer[bytesIn] = '\0';
            execute(conn_handle, receive_buffer);
            bytesIn = 0;
            break;
        case '\b': // backspace
            if (bytesIn > 0) {
                bytesIn--;
            }
            break;
        default:
            receive_buffer[bytesIn++] = receive_char;
            if (bytesIn >= sizeof(receive_buffer) - 1) {
                receive_buffer[bytesIn] = '\0';
                execute(conn_handle, receive_buffer);
                bytesIn = 0;
            }
            break;
    }
}

// AT Command implementations
void sendBLEKeyboardCode(char *myLine) {
    uint8_t report[HID_KEYBOARD_REPORT_SIZE];
    memset(report, 0, sizeof(report));

    // Parse keyboard report: "XX-XX-XX-XX-XX-XX-XX-XX"
    char *p = strtok(myLine, "=");
    p = strtok(NULL, "-");

    for (size_t i = 0; p && (i < sizeof(report)); i++) {
        report[i] = strtoul(p, NULL, 16);
        p = strtok(NULL, "-");
    }

    // Handle special consumer keys
    switch (report[2]) {
        case KEYCODE_MUTE:
            if (pInputConsumer && deviceConnected) {
                uint8_t consumerReport[2] = {CONSUMER_KEY_MUTE, 0};
                pInputConsumer->setValue(consumerReport, 2);
                pInputConsumer->notify();
                delay(10);
                memset(consumerReport, 0, 2);
                pInputConsumer->setValue(consumerReport, 2);
                pInputConsumer->notify();
            }
            break;
        case KEYCODE_VOLUME_UP:
            if (pInputConsumer && deviceConnected) {
                uint8_t consumerReport[2] = {CONSUMER_KEY_VOLUME_UP, 0};
                pInputConsumer->setValue(consumerReport, 2);
                pInputConsumer->notify();
                delay(10);
                memset(consumerReport, 0, 2);
                pInputConsumer->setValue(consumerReport, 2);
                pInputConsumer->notify();
            }
            break;
        case KEYCODE_VOLUME_DOWN:
            if (pInputConsumer && deviceConnected) {
                uint8_t consumerReport[2] = {CONSUMER_KEY_VOLUME_DOWN, 0};
                pInputConsumer->setValue(consumerReport, 2);
                pInputConsumer->notify();
                delay(10);
                memset(consumerReport, 0, 2);
                pInputConsumer->setValue(consumerReport, 2);
                pInputConsumer->notify();
            }
            break;
        default:
            // Regular keyboard report
            if (pInputKeyboard && deviceConnected) {
                pInputKeyboard->setValue(report, sizeof(report));
                pInputKeyboard->notify();
            }
            break;
    }

    at_response(AT_RESPONSE_OK);
}

void sendBLEMouseMove(char *line) {
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

    if (pInputMouse && deviceConnected) {
        uint8_t mouseReport[4] = {0};
        mouseReport[0] = 0; // buttons
        mouseReport[1] = (int8_t)constrain(x, -127, 127);
        mouseReport[2] = (int8_t)constrain(y, -127, 127);
        mouseReport[3] = (int8_t)constrain(wy, -127, 127);

        pInputMouse->setValue(mouseReport, sizeof(mouseReport));
        pInputMouse->notify();

        // Handle horizontal scroll if needed (wx)
        if (wx != 0) {
            // ESP32 BLE HID doesn't directly support horizontal scroll in this simple implementation
            // Could be added with extended HID descriptor
        }
    }

    at_response(AT_RESPONSE_OK);
}

void sendBLEMouseButton(char *line) {
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

    if (pInputMouse && deviceConnected) {
        uint8_t mouseReport[4] = {0, 0, 0, 0};

        if (mode == 1) { // Click
            mouseReport[0] = button;
            pInputMouse->setValue(mouseReport, sizeof(mouseReport));
            pInputMouse->notify();
            delay(40);
            mouseReport[0] = 0;
            pInputMouse->setValue(mouseReport, sizeof(mouseReport));
            pInputMouse->notify();
        } else if (mode == 2) { // Double click
            for (int i = 0; i < 2; i++) {
                mouseReport[0] = button;
                pInputMouse->setValue(mouseReport, sizeof(mouseReport));
                pInputMouse->notify();
                delay(40);
                mouseReport[0] = 0;
                pInputMouse->setValue(mouseReport, sizeof(mouseReport));
                pInputMouse->notify();
                if (i == 0) delay(40);
            }
        } else { // Press/Release toggle
            mouseReport[0] = button;
            pInputMouse->setValue(mouseReport, sizeof(mouseReport));
            pInputMouse->notify();
        }
    }

    at_response(AT_RESPONSE_OK);
}

void sendBleSendCurrentDeviceName(char *myLine) {
    at_response("at+blecurrentdevicename\n");

    if (!deviceConnected) {
        at_response("NONE\n");
    } else {
        // For ESP32, we'll use a simplified approach
        // In a full implementation, you'd track connected device names
        at_response("ESP32_Device\n");
    }
}

void addNewBleDevice(char *myLine) {
    at_response("at+bleaddnewdevice\n");

    if (deviceState.bleDeviceNameListIndex >= deviceState.maxBleDevListSize) {
        at_response("ERROR: Device list is full\n");
        return;
    }

    deviceState.flag_addDevProsStarted = true;
    deviceState.addDevProsStartTicks = millis();
    updateStatusLED();

    char buff[256];
    snprintf(buff, sizeof(buff), "Connect your device with %s\n", BLE_NAME);
    at_response(buff);
}

void removeBleDevice(char *myLine) {
    at_response("at+bleremovedevice\n");

    // Parse device name from quotes
    char tempName[BLE_DEVICE_NAME_LENGTH] = {0};
    char *start = strchr(myLine, '"');
    if (start) {
        start++; // Skip opening quote
        char *end = strchr(start, '"');
        if (end) {
            size_t len = min((size_t)(end - start), sizeof(tempName) - 1);
            strncpy(tempName, start, len);
            tempName[len] = '\0';
        }
    }

    if (strlen(tempName) == 0) {
        at_response("ERROR: Syntax\n");
        return;
    }

    // Find and remove device from list
    bool found = false;
    for (uint8_t i = 0; i < deviceState.bleDeviceNameListIndex; i++) {
        if (strcmp(tempName, deviceState.bleDeviceNameList[i]) == 0) {
            found = true;
            // Shift remaining devices down
            for (uint8_t j = i; j < deviceState.bleDeviceNameListIndex - 1; j++) {
                strcpy(deviceState.bleDeviceNameList[j], deviceState.bleDeviceNameList[j + 1]);
            }
            deviceState.bleDeviceNameListIndex--;
            deviceState.flag_saveListToFile = true;
            break;
        }
    }

    if (found) {
        at_response(AT_RESPONSE_SUCCESS);
    } else {
        at_response("ERROR: Name not found in the list\n");
    }
}

void switchBleConnection(char *myLine) {
    at_response("at+switchconn\n");

    if (!deviceConnected) {
        at_response("ERROR: No device connected now\n");
        return;
    }

    if (deviceState.bleDeviceNameListIndex < 2) {
        at_response("ERROR: No other device present in list\n");
        return;
    }

    // For ESP32 implementation, this is simplified
    // In a full implementation, you'd handle multiple connections
    at_response("Switching connections not fully implemented in ESP32 version\n");
}

void printBleDevList(char *myLine) {
    at_response("at+printdevlist\n");

    char buff[256];
    for (uint8_t i = 0; i < deviceState.bleDeviceNameListIndex; i++) {
        snprintf(buff, sizeof(buff), "%d:%s\n", i + 1, deviceState.bleDeviceNameList[i]);
        at_response(buff);
    }
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

    // Clear from persistent storage
    preferences.clear();

    // Disconnect current device
    if (deviceConnected && pServer) {
        pServer->disconnect(pServer->getConnId());
    }

    at_response(AT_RESPONSE_SUCCESS);
}

void change_mode(char *myLine) {
    DEBUG_PRINTLN("Changing operating mode");

    at_response(AT_RESPONSE_OK);

    deviceState.ble_mode = !deviceState.ble_mode;

    // Save mode to preferences
    preferences.putBool("ble_mode", deviceState.ble_mode);

    // Disconnect and restart
    if (deviceConnected && pServer) {
        pServer->disconnect(pServer->getConnId());
    }

    delay(1000);
    ESP.restart();
}

void get_mode(char *myLine) {
    if (deviceState.ble_mode) {
        at_response("BLE\n");
    } else {
        at_response("Serial\n");
    }
}

// File system functions using Preferences (NVRAM)
void save_devList_toFile(void) {
    preferences.putBytes("devList", deviceState.bleDeviceNameList, sizeof(deviceState.bleDeviceNameList));
    preferences.putUChar("devListIdx", deviceState.bleDeviceNameListIndex);

    DEBUG_PRINT("Saved device list with ");
    DEBUG_PRINT(deviceState.bleDeviceNameListIndex);
    DEBUG_PRINTLN(" devices");
}

void load_devList_fromFile(void) {
    size_t len = preferences.getBytesLength("devList");
    if (len > 0) {
        preferences.getBytes("devList", deviceState.bleDeviceNameList, sizeof(deviceState.bleDeviceNameList));
        deviceState.bleDeviceNameListIndex = preferences.getUChar("devListIdx", 0);

        // Validate index
        if (deviceState.bleDeviceNameListIndex > MAX_BLE_DEVICES) {
            deviceState.bleDeviceNameListIndex = 0;
        }

        DEBUG_PRINT("Loaded device list with ");
        DEBUG_PRINT(deviceState.bleDeviceNameListIndex);
        DEBUG_PRINTLN(" devices");
    }
}

void load_mode_file(void) {
    deviceState.ble_mode = preferences.getBool("ble_mode", false);
    DEBUG_PRINT("Loaded mode: ");
    DEBUG_PRINTLN(deviceState.ble_mode ? "BLE" : "Serial");
}

void save_tmp_file(void) {
    preferences.putBool("swapStarted", deviceState.flag_bleSwapConnProsStarted);
    preferences.putUChar("swapStartIdx", deviceState.switchBleConnStartIndex);
    preferences.putUChar("swapCurrIdx", deviceState.switchBleConnCurrIndex);
    DEBUG_PRINTLN("Temp parameters saved");
}

void load_tmp_file(void) {
    deviceState.flag_bleSwapConnProsStarted = preferences.getBool("swapStarted", false);
    deviceState.switchBleConnStartIndex = preferences.getUChar("swapStartIdx", 0);
    deviceState.switchBleConnCurrIndex = preferences.getUChar("swapCurrIdx", 0);

    if (deviceState.flag_bleSwapConnProsStarted) {
        DEBUG_PRINTLN("Temp parameters loaded");
        // Clear temp file after loading
        preferences.remove("swapStarted");
        preferences.remove("swapStartIdx");
        preferences.remove("swapCurrIdx");
    }
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
