/*********************************************************************
 RelayKeys nRF52840 Implementation v2
 
 Updated nRF52840 implementation for RelayKeys using common header
 This is a refactored version of the original nRF52840 code that uses
 the shared common header for consistency across platforms.
 
 Copyright Ace Centre 2024 - MIT Licence
 
 Hardware Requirements:
 - Adafruit nRF52840 Express, ItsyBitsy, or compatible board
 - Built-in NeoPixel or DotStar LED for status
 - User button for mode switching
 
 This implementation maintains full compatibility with the original
 RelayKeys AT command protocol while using the new common header
 structure for better code organization.
*********************************************************************/

#include <bluefruit.h>
#include <Adafruit_LittleFS.h>
#include <InternalFileSystem.h>
#include "../common/relaykeys_common.h"

//#define DEBUG // uncomment this line to see additional prints in Serial monitor

// Hardware-specific pin definitions
#if defined(_VARIANT_ITSY52840_)
  // Adafruit ItsyBitsy nRF52840
  #define USER_SW 4
  #include <Adafruit_DotStar.h>
  Adafruit_DotStar statusLED(1, 8, 6, DOTSTAR_BGR);
#elif defined(_VARIANT_FEATHER52840_)
  // Adafruit Feather nRF52840
  #define USER_SW 7
  #include <Adafruit_NeoPixel.h>
  Adafruit_NeoPixel statusLED = Adafruit_NeoPixel(1, PIN_NEOPIXEL, NEO_GRB + NEO_KHZ800);
#elif defined(_VARIANT_MDBT50Q_RX_)
  // Raytac MDBT50Q-RX Dongle
  #define USER_SW PIN_BUTTON1
  #include <TimedBlink.h>
  TimedBlink monitor(LED_BLUE);
#else
  // Unknown board - default to ItsyBitsy-like configuration
  #define UNKNOWN_BOARD
  #define USER_SW 4
  #include <Adafruit_NeoPixel.h>
  Adafruit_NeoPixel statusLED = Adafruit_NeoPixel(1, 8, NEO_GRB + NEO_KHZ800);
#endif

// BLE objects
BLEDis bledis;
BLEHidAdafruit blehid;
BLEUart bleuart;

// Device state
device_state_t deviceState = {0};
uint8_t keys[HID_KEYBOARD_REPORT_SIZE] = {0}; // Current keyboard state
uint8_t max_prph_connection = 1;
uint8_t connection_count = 0;
uint16_t target_ble_conn = 0;
uint16_t response_ble_conn = 0;

// File system
using namespace Adafruit_LittleFS_Namespace;
#define FILENAME "/devNameList.txt"
#define MODE_FILENAME "/config.txt"
#define TMP_FILENAME "/tmp.txt"
File file(InternalFS);

// Mouse button mapping for nRF52840
const mouse_button_map_t mouse_buttons_map[] = {
    {MOUSE_BUTTON_LEFT_CHAR, MOUSE_BUTTON_LEFT},
    {MOUSE_BUTTON_RIGHT_CHAR, MOUSE_BUTTON_RIGHT},
    {MOUSE_BUTTON_MIDDLE_CHAR, MOUSE_BUTTON_MIDDLE},
    {MOUSE_BUTTON_BACKWARD_CHAR, MOUSE_BUTTON_BACKWARD},
    {MOUSE_BUTTON_FORWARD_CHAR, MOUSE_BUTTON_FORWARD},
    {MOUSE_BUTTON_RELEASE_CHAR, 0},
};

// Forward declarations
void startAdv(void);
void bleConnectCallback(uint16_t conn_handle);
void disconnect_callback(uint16_t conn_handle, uint8_t reason);
void prph_bleuart_rx_callback(uint16_t conn_handle);
void set_keyboard_led(uint16_t conn_handle, uint8_t led_bitmap);

void setup() {
    Serial.begin(115200);
    #if defined(UNKNOWN_BOARD) && defined(DEBUG)
    Serial.println("Unsupported hardware. Possibly not critical unless you want to initiate BLE mode with a button");
    #endif
    
    // Initialize Internal File System
    InternalFS.begin();
    
    // Load configuration
    load_mode_file();
    load_tmp_file();
    load_devList_fromFile();
    
    // Initialize pins
    pinMode(USER_SW, INPUT_PULLUP);
    
    // Initialize status LED
    #ifdef _VARIANT_MDBT50Q_RX_
    monitor.blink(800, 10);
    #else
    statusLED.begin();
    updateStatusLED();
    #endif
    
    // Initialize device state
    deviceState.maxBleDevListSize = MAX_BLE_DEV_LIST_SIZE_DEFAULT;
    
    // Set connection limits based on mode
    if (deviceState.ble_mode) {
        max_prph_connection = 2;
    } else {
        max_prph_connection = 1;
    }
    
    // Initialize Bluefruit
    Bluefruit.configPrphBandwidth(BANDWIDTH_MAX);
    Bluefruit.begin(max_prph_connection, 0);
    Bluefruit.setTxPower(4);
    Bluefruit.setName(BLE_NAME);
    Bluefruit.Periph.setConnectCallback(bleConnectCallback);
    Bluefruit.Periph.setDisconnectCallback(disconnect_callback);
    
    // Configure Device Information Service
    bledis.setManufacturer(BLE_MANUFACTURER);
    bledis.setModel(BLE_NAME);
    bledis.begin();
    
    // Configure BLE UART Service
    bleuart.begin();
    bleuart.setRxCallback(prph_bleuart_rx_callback);
    
    // Start BLE HID
    blehid.begin();
    blehid.setKeyboardLedCallback(set_keyboard_led);
    
    // Start advertising
    startAdv();
    
    DEBUG_PRINTLN("RelayKeys nRF52840 v2 Ready");
}

void startAdv(void) {
    // Advertising packet
    Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
    Bluefruit.Advertising.addTxPower();
    Bluefruit.Advertising.addAppearance(BLE_APPEARANCE_HID_KEYBOARD);
    
    // Include BLE HID service
    Bluefruit.Advertising.addService(blehid);
    
    // Add device name
    Bluefruit.Advertising.addName();
    
    // Start advertising
    Bluefruit.Advertising.restartOnDisconnect(true);
    Bluefruit.Advertising.setInterval(32, 244); // in unit of 0.625 ms
    Bluefruit.Advertising.setFastTimeout(30);   // number of seconds in fast mode
    Bluefruit.Advertising.start(0);             // 0 = Don't stop advertising after n seconds
    
    DEBUG_PRINTLN("RelayKeys UP & Running");
}

void loop() {
    // Handle serial input when not in BLE mode
    if (!deviceState.ble_mode && Serial.available() > 0) {
        receive_char(0, Serial.read());
    }
    
    // Handle button press
    if (digitalRead(USER_SW) == false) {
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
    
    // Handle connection switching
    if (deviceState.flag_bleSwapConnProsStarted == 1) {
        if (millis() - deviceState.swapConnProsStartTicks >= SWAP_CONN_PROCESS_TIMEOUT) {
            DEBUG_PRINTLN("Connection switch timeout");
            deviceState.switchBleConnCurrIndex++;
            if (deviceState.switchBleConnCurrIndex > deviceState.bleDeviceNameListIndex) {
                deviceState.switchBleConnCurrIndex = 1;
            }
            if (deviceState.switchBleConnCurrIndex == deviceState.switchBleConnStartIndex) {
                deviceState.flag_bleSwapConnProsStarted = 2;
            }
            deviceState.swapConnProsStartTicks = millis();
        }
    } else if (deviceState.flag_bleSwapConnProsStarted == 2) {
        if (millis() - deviceState.swapConnProsStartTicks >= SWAP_CONN_PROCESS_TIMEOUT) {
            deviceState.flag_bleSwapConnProsStarted = 0;
            DEBUG_PRINTLN("Connection switch final timeout");
        }
    }
    
    // Request CPU to enter low-power mode until an event/interrupt occurs
    waitForEvent();
}

// Utility functions
void updateStatusLED() {
    #if defined(_VARIANT_MDBT50Q_RX_)
    if (deviceState.flag_addDevProsStarted) {
        monitor.blink(150, 50); // Fast blink for pairing
    } else if (deviceState.ble_mode) {
        monitor.blink(300, 50); // Slow blink for BLE mode
    } else {
        digitalWrite(LED_BLUE, HIGH); // Solid on for serial mode
    }
    #else
    if (deviceState.flag_addDevProsStarted) {
        statusLED.setPixelColor(0, 16, 16, 0);  // Yellow for pairing
    } else if (deviceState.ble_mode) {
        statusLED.setPixelColor(0, 0, 0, 16);   // Blue for BLE mode
    } else {
        statusLED.setPixelColor(0, 0, 16, 0);   // Green for serial mode
    }
    statusLED.show();
    #endif
}

uint8_t detect_click() {
    uint32_t press_time = millis();
    uint8_t click_counter = 0;

    while ((millis() - press_time) < BUTTON_CLICK_TIMEOUT) {
        if (digitalRead(USER_SW) == false && (millis() - press_time) < BUTTON_CLICK_TIMEOUT) {
            click_counter++;
            delay(BUTTON_DEBOUNCE_TIME);
            while (digitalRead(USER_SW) == false) {
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
    int len = strlen(msg);

    if (deviceState.ble_mode) {
        bleuart.write(response_ble_conn, (const uint8_t*)msg, len);
    } else {
        Serial.write(msg, len);
    }
}

void update_connections(uint16_t conn_handle) {
    target_ble_conn = 1;
    response_ble_conn = 0;
    if (conn_handle == 1) {
        target_ble_conn = 0;
        response_ble_conn = 1;
    }
}

void execute(uint16_t conn_handle, char *myLine) {
    if (myLine == NULL || *myLine == '\0')
        return;

    char cmdTemp[100];
    memcpy(cmdTemp, myLine, 100);

    char *cmd = strtok(cmdTemp, "=");
    if (cmd == NULL || *cmd == '\0')
        return;

    toLower(cmd);

    if (deviceState.ble_mode) {
        update_connections(conn_handle);
    }

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

// BLE callbacks
void prph_bleuart_rx_callback(uint16_t conn_handle) {
    if (deviceState.ble_mode) {
        while (bleuart.available()) {
            receive_char(conn_handle, bleuart.read());
        }
    }
}

// AT Command implementations
void sendBLEKeyboardCode(char *myLine) {
    char buff[256];
    err_t ret;
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
            ret = blehid.consumerKeyPress(target_ble_conn, CONSUMER_KEY_MUTE);
            blehid.consumerKeyRelease(target_ble_conn);
            break;
        case KEYCODE_VOLUME_UP:
            ret = blehid.consumerKeyPress(target_ble_conn, CONSUMER_KEY_VOLUME_UP);
            blehid.consumerKeyRelease(target_ble_conn);
            break;
        case KEYCODE_VOLUME_DOWN:
            ret = blehid.consumerKeyPress(target_ble_conn, CONSUMER_KEY_VOLUME_DOWN);
            blehid.consumerKeyRelease(target_ble_conn);
            break;
        default:
            // Regular keyboard report
            ret = blehid.keyboardReport(target_ble_conn, report[0], &report[2]);
            break;
    }

    if ((int)ret != 1) {
        snprintf(buff, sizeof(buff), "ERROR %d\n", (int)ret);
        at_response(buff);
    } else {
        at_response(AT_RESPONSE_OK);
    }
}

void sendBLEMouseMove(char *line) {
    char buff[256];
    err_t ret = 1;
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

    if (x != 0 || y != 0) {
        ret = blehid.mouseMove(target_ble_conn, x, y);
    }

    if ((int)ret != 1) {
        snprintf(buff, sizeof(buff), "ERROR %d\n", (int)ret);
        at_response(buff);
        return;
    }

    if (wy != 0) {
        ret = blehid.mouseScroll(target_ble_conn, wy);
    }

    if ((int)ret != 1) {
        snprintf(buff, sizeof(buff), "ERROR %d\n", (int)ret);
        at_response(buff);
        return;
    }

    if (wx != 0) {
        ret = blehid.mousePan(target_ble_conn, wx);
    }

    if ((int)ret != 1) {
        snprintf(buff, sizeof(buff), "ERROR %d\n", (int)ret);
        at_response(buff);
        return;
    }

    at_response(AT_RESPONSE_OK);
}

void sendBLEMouseButton(char *line) {
    char buff[256];
    err_t ret;
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

    if (button != 0 && mode == 1) { // Click
        ret = blehid.mouseButtonPress(target_ble_conn, button);
        if (ret == 1) {
            delay(40);
            ret = blehid.mouseButtonRelease(target_ble_conn);
        }
    } else if (button != 0 && mode == 2) { // Double click
        ret = blehid.mouseButtonPress(target_ble_conn, button);
        if (ret == 1) {
            delay(40);
            ret = blehid.mouseButtonRelease(target_ble_conn);
        }
        if (ret == 1) {
            ret = blehid.mouseButtonPress(target_ble_conn, button);
        }
        if (ret == 1) {
            delay(40);
            ret = blehid.mouseButtonRelease(target_ble_conn);
        }
    } else { // Press/Release
        if (button == 0) {
            ret = blehid.mouseButtonRelease(target_ble_conn);
        } else {
            ret = blehid.mouseButtonPress(target_ble_conn, button);
        }
    }

    if ((int)ret != 1) {
        snprintf(buff, sizeof(buff), "ERROR %d\n", (int)ret);
        at_response(buff);
    } else {
        at_response(AT_RESPONSE_OK);
    }
}

void sendBleSendCurrentDeviceName(char *myLine) {
    char buff[256];
    at_response("at+blecurrentdevicename\n");

    if (!Bluefruit.connected()) {
        at_response("NONE\n");
    } else {
        BLEConnection *connection = Bluefruit.Connection(target_ble_conn);
        char bleDeviceName[BLE_DEVICE_NAME_LENGTH] = {0};

        connection->getPeerName(bleDeviceName, sizeof(bleDeviceName));
        if (strlen(bleDeviceName) == 0) {
            at_response("NONE\n");
        } else {
            snprintf(buff, sizeof(buff), "%s\n", bleDeviceName);
            at_response(buff);
        }
    }
}

void addNewBleDevice(char *myLine) {
    char buff[256];
    at_response("at+bleaddnewdevice\n");

    if (deviceState.bleDeviceNameListIndex >= deviceState.maxBleDevListSize) {
        at_response("ERROR: Device list is full\n");
    } else {
        BLEConnection *connection = Bluefruit.Connection(target_ble_conn);
        char bleDeviceName[BLE_DEVICE_NAME_LENGTH] = {0};

        connection->getPeerName(bleDeviceName, sizeof(bleDeviceName));

        delay(500);
        connection->disconnect();

        deviceState.flag_addDevProsStarted = true;
        updateStatusLED();
        deviceState.addDevProsStartTicks = millis();

        snprintf(buff, sizeof(buff), "Connect your device with %s\n", BLE_NAME);
        at_response(buff);
    }
}

void removeBleDevice(char *myLine) {
    at_response("at+bleremovedevice\n");

    char tempName[BLE_DEVICE_NAME_LENGTH] = {0};
    char tempNameIndex = 0;
    char flag_start = 0;

    if (strlen(myLine) == 0) {
        at_response("ERROR: Syntax\n");
        return;
    }

    // Parse device name from quotes
    for (char i = 0; i < strlen(myLine); i++) {
        if (myLine[i] == '"') {
            flag_start = 1;
        } else {
            if (flag_start) {
                if (myLine[i] == '"') {
                    flag_start = 0;
                    break;
                } else {
                    tempName[tempNameIndex++] = myLine[i];
                }
            }
        }
    }

    if (strlen(tempName) == 0) {
        at_response("ERROR: Syntax\n");
        return;
    }

    // Check if trying to remove current device
    BLEConnection *connection = Bluefruit.Connection(target_ble_conn);
    char bleDeviceName[BLE_DEVICE_NAME_LENGTH] = {0};
    connection->getPeerName(bleDeviceName, sizeof(bleDeviceName));

    if (!strcmp((char *)tempName, (char *)bleDeviceName)) {
        connection->disconnect();
    }

    // Check if trying to remove central device in BLE mode
    if (deviceState.ble_mode) {
        connection = Bluefruit.Connection(response_ble_conn);
        char centralBleDeviceName[BLE_DEVICE_NAME_LENGTH] = {0};
        connection->getPeerName(centralBleDeviceName, sizeof(centralBleDeviceName));
        if (!strcmp((char *)tempName, (char *)centralBleDeviceName)) {
            at_response("ERROR: Can't remove central device\n");
            return;
        }
    }

    // Find and remove device from list
    bool found = false;
    for (uint8_t i = 0; i < deviceState.maxBleDevListSize; i++) {
        if (!strcmp((char *)tempName, (char *)deviceState.bleDeviceNameList[i])) {
            found = true;
            deviceState.bleDeviceNameListIndex--;
            deviceState.flag_saveListToFile = true;

            // Shift remaining devices down
            for (uint8_t j = i; j < deviceState.maxBleDevListSize - 1; j++) {
                if (j < (deviceState.maxBleDevListSize - 1)) {
                    memset(deviceState.bleDeviceNameList[j], 0, sizeof(deviceState.bleDeviceNameList[j]));
                    strcpy(deviceState.bleDeviceNameList[j], deviceState.bleDeviceNameList[j + 1]);
                } else {
                    memset(deviceState.bleDeviceNameList[deviceState.maxBleDevListSize - 1], 0,
                           sizeof(deviceState.bleDeviceNameList[deviceState.maxBleDevListSize - 1]));
                }
            }
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
    char buff[256];
    char tempBleDevName[BLE_DEVICE_NAME_LENGTH] = {0};

    BLEConnection *connection = Bluefruit.Connection(target_ble_conn);
    at_response("at+switchconn\n");

    if (!Bluefruit.connected()) {
        at_response("ERROR: No device connected now\n");
        return;
    }

    if (deviceState.bleDeviceNameListIndex < 2) {
        at_response("ERROR: No other device present in list\n");
        return;
    }

    // Parse device argument if present
    char *start_dev_p = strstr(myLine, "=\"");
    if (start_dev_p != NULL) {
        char *end_dev_p = strrchr(myLine, '"');
        if (end_dev_p != NULL && end_dev_p != (start_dev_p + 1)) {
            start_dev_p += 2; // Move pointer to start of device name

            if ((end_dev_p - start_dev_p) <= 31) {
                strncpy(tempBleDevName, start_dev_p, (end_dev_p - start_dev_p));
            }
        }

        if (strlen(tempBleDevName) != 0) {
            for (int i = 0; i < deviceState.bleDeviceNameListIndex; i++) {
                if (!strcmp((char *)tempBleDevName, (char *)deviceState.bleDeviceNameList[i])) {
                    deviceState.switchBleConnCurrIndex = i + 1;
                    deviceState.flag_bleSwapConnProsStarted = 1;
                    deviceState.swapConnProsStartTicks = millis();

                    snprintf(buff, sizeof(buff), "Trying to connect with - %s\n",
                             deviceState.bleDeviceNameList[deviceState.switchBleConnCurrIndex - 1]);
                    at_response(buff);

                    connection->disconnect();
                    return;
                }
            }
            at_response("ERROR: Device not found in list\n");
            return;
        } else {
            at_response("ERROR: Syntax\n");
            return;
        }
    } else {
        // Switch to next device
        connection->getPeerName(tempBleDevName, sizeof(tempBleDevName));

        for (char i = 0; i < deviceState.maxBleDevListSize; i++) {
            if (!strcmp((char *)tempBleDevName, (char *)deviceState.bleDeviceNameList[i])) {
                deviceState.switchBleConnStartIndex = i + 1;

                if (deviceState.switchBleConnStartIndex >= deviceState.bleDeviceNameListIndex) {
                    deviceState.switchBleConnCurrIndex = 1;
                } else {
                    deviceState.switchBleConnCurrIndex = deviceState.switchBleConnStartIndex + 1;
                }

                deviceState.flag_bleSwapConnProsStarted = 1;
                deviceState.swapConnProsStartTicks = millis();

                snprintf(buff, sizeof(buff), "Trying to connect with - %s\n",
                         deviceState.bleDeviceNameList[deviceState.switchBleConnCurrIndex - 1]);
                at_response(buff);

                connection->disconnect();
                break;
            }
        }
    }
}

void printBleDevList(char *myLine) {
    char buff[256];
    at_response("at+printdevlist\n");

    for (char j = 0; j < deviceState.bleDeviceNameListIndex; j++) {
        snprintf(buff, sizeof(buff), "%d:%s\n", (j + 1), deviceState.bleDeviceNameList[j]);
        at_response(buff);
    }
}

void setBleMaxDevListSize(char *myLine) {
    at_response("at+blemaxdevlistsize\n");

    char *p = strtok(myLine, "=");
    p = strtok(NULL, "\0");
    uint8_t tempNum = atoi(p);

    if (tempNum > MAX_BLE_DEVICES || tempNum < 1) {
        deviceState.maxBleDevListSize = MAX_BLE_DEV_LIST_SIZE_DEFAULT;
        at_response("ERROR: Invalid Value\n");
    } else {
        deviceState.maxBleDevListSize = tempNum;
        at_response(AT_RESPONSE_SUCCESS);
    }
}

void deleteDevList(char *myLine) {
    at_response("at+deletedevlist\n");

    InternalFS.remove(FILENAME);
    deviceState.bleDeviceNameListIndex = 0;
    memset(deviceState.bleDeviceNameList, 0, sizeof(deviceState.bleDeviceNameList));

    BLEConnection *connection = NULL;
    for (int i = 0; i < max_prph_connection; i++) {
        connection = Bluefruit.Connection(i);
        connection->disconnect();
    }

    at_response(AT_RESPONSE_SUCCESS);
}

void change_mode(char *myLine) {
    DEBUG_PRINTLN("Changing operating mode");

    at_response(AT_RESPONSE_OK);

    deviceState.ble_mode = !deviceState.ble_mode;

    file.open(MODE_FILENAME, FILE_O_WRITE);
    if (file) {
        file.seek(0);
        file.write((const uint8_t *)&deviceState.ble_mode, 1);
        file.close();
    } else {
        DEBUG_PRINTLN("Mode file write failed");
    }

    BLEConnection *connection = NULL;
    for (int i = 0; i < max_prph_connection; i++) {
        connection = Bluefruit.Connection(i);
        connection->disconnect();
    }

    delay(1000);
    NVIC_SystemReset();
}

void get_mode(char *myLine) {
    if (deviceState.ble_mode) {
        at_response("BLE\n");
    } else {
        at_response("Serial\n");
    }
}

// File system functions
void save_devList_toFile(void) {
    file.open(FILENAME, FILE_O_WRITE);

    if (file) {
        DEBUG_PRINT("List has ");
        DEBUG_PRINT(deviceState.bleDeviceNameListIndex);
        DEBUG_PRINTLN(" devices");

        file.seek(0);
        file.write((const uint8_t *)deviceState.bleDeviceNameList, sizeof(deviceState.bleDeviceNameList));
        file.write((const uint8_t *)&deviceState.bleDeviceNameListIndex, 1);

        DEBUG_PRINT("Saving Device List to file ");
        DEBUG_PRINT(file.size());
        DEBUG_PRINTLN();
        file.close();
    } else {
        DEBUG_PRINTLN("Device list write failed");
    }
}

void load_devList_fromFile(void) {
    file.open(FILENAME, FILE_O_READ);

    if (file) {
        DEBUG_PRINT("Loading Device List from file ");
        DEBUG_PRINT(file.size());
        DEBUG_PRINTLN();

        deviceState.bleDeviceNameListIndex = 0;
        memset(deviceState.bleDeviceNameList, 0, sizeof(deviceState.bleDeviceNameList));

        file.read((void *)deviceState.bleDeviceNameList, sizeof(deviceState.bleDeviceNameList));
        file.read((void *)&deviceState.bleDeviceNameListIndex, 1);

        if (deviceState.bleDeviceNameListIndex > MAX_BLE_DEVICES) {
            deviceState.bleDeviceNameListIndex = 0;
        }

        DEBUG_PRINT("List has ");
        DEBUG_PRINT(deviceState.bleDeviceNameListIndex);
        DEBUG_PRINTLN(" devices");

        file.close();
    } else {
        DEBUG_PRINTLN("Device list read failed");
    }
}

void load_mode_file(void) {
    file.open(MODE_FILENAME, FILE_O_READ);

    if (file) {
        file.read((void *)&deviceState.ble_mode, 1);
        file.close();
    } else {
        DEBUG_PRINTLN("Mode file read failed");
    }
}

void save_tmp_file(void) {
    file.open(TMP_FILENAME, FILE_O_WRITE);

    if (file) {
        file.seek(0);
        file.write((const uint8_t *)&deviceState.flag_bleSwapConnProsStarted, 1);
        file.write((const uint8_t *)&deviceState.switchBleConnStartIndex, 1);
        file.write((const uint8_t *)&deviceState.switchBleConnCurrIndex, 1);
        file.close();

        DEBUG_PRINTLN("Temp parameters saved");
    } else {
        DEBUG_PRINTLN("Temp file write failed");
    }
}

void load_tmp_file(void) {
    file.open(TMP_FILENAME, FILE_O_READ);

    if (file) {
        file.read((void *)&deviceState.flag_bleSwapConnProsStarted, 1);
        file.read((void *)&deviceState.switchBleConnStartIndex, 1);
        file.read((void *)&deviceState.switchBleConnCurrIndex, 1);
        file.close();

        DEBUG_PRINTLN("Temp parameters loaded");
        InternalFS.remove(TMP_FILENAME);
    } else {
        DEBUG_PRINTLN("Temp file read failed");
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

// BLE connection callbacks
void bleConnectCallback(uint16_t conn_handle) {
    static int i;
    BLEConnection *connection = Bluefruit.Connection(conn_handle);
    char central_name[BLE_DEVICE_NAME_LENGTH] = {0};
    uint8_t timeout_counter = 10;

    connection->getPeerName(central_name, sizeof(central_name));

    // Wait for unpaired iPhone/iPad to provide full device name
    while (!strcmp((char *)central_name, "iPhone") || !strcmp((char *)central_name, "iPad")) {
        if (connection->connected() && timeout_counter > 0) {
            delay(1000);
            connection->getPeerName(central_name, sizeof(central_name));
            timeout_counter--;
        } else {
            connection->disconnect();
            return;
        }
    }

    connection_count++;

    // Handle connection switching
    if (deviceState.flag_bleSwapConnProsStarted == 1) {
        if (!strcmp((char *)central_name, (char *)deviceState.bleDeviceNameList[deviceState.switchBleConnCurrIndex - 1])) {
            deviceState.flag_bleSwapConnProsStarted = 0;
            DEBUG_PRINTLN("Connection switch success");
        } else {
            connection->disconnect();
            DEBUG_PRINT("Disconnected - Other device: ");
            DEBUG_PRINTLN(central_name);
        }
    } else if (deviceState.flag_bleSwapConnProsStarted == 2) {
        if (!strcmp((char *)central_name, (char *)deviceState.bleDeviceNameList[deviceState.switchBleConnStartIndex - 1])) {
            deviceState.flag_bleSwapConnProsStarted = 0;
            DEBUG_PRINT("Reconnected to last device: ");
            DEBUG_PRINTLN(central_name);
        } else {
            connection->disconnect();
            DEBUG_PRINTLN("Disconnected - Other device");
        }
    } else {
        // Handle new device addition
        if (deviceState.bleDeviceNameListIndex == 0 && !strcmp((char *)central_name, "AceRK receiver")) {
            // Auto-add receiver dongle
            strcpy(deviceState.bleDeviceNameList[deviceState.bleDeviceNameListIndex++], central_name);
            deviceState.flag_saveListToFile = true;
        } else {
            // Check if device is in list
            for (i = 0; i < deviceState.maxBleDevListSize; i++) {
                if (!strcmp((char *)central_name, (char *)deviceState.bleDeviceNameList[i])) {
                    DEBUG_PRINTLN("Device found in list");
                    if (deviceState.flag_addDevProsStarted) {
                        connection->disconnect();
                        DEBUG_PRINTLN("Disconnected - Device already in list");
                    }
                    break;
                }
            }

            if (i >= deviceState.maxBleDevListSize) {
                if (deviceState.flag_addDevProsStarted) {
                    deviceState.flag_addDevProsStarted = false;
                    updateStatusLED();

                    if (deviceState.bleDeviceNameListIndex >= deviceState.maxBleDevListSize) {
                        connection->disconnect();
                        DEBUG_PRINTLN("ERROR: Device list is full");
                    } else {
                        DEBUG_PRINTLN("SUCCESS - Device added to list");
                        strcpy(deviceState.bleDeviceNameList[deviceState.bleDeviceNameListIndex++], central_name);
                        deviceState.flag_saveListToFile = true;
                    }
                } else {
                    connection->disconnect();
                    DEBUG_PRINTLN("Disconnected - Not in list");
                }
            }
        }
    }

    // Keep advertising if not at max connections
    if (connection_count < max_prph_connection) {
        Bluefruit.Advertising.start(0);
    }
}

void disconnect_callback(uint16_t conn_handle, uint8_t reason) {
    (void) conn_handle;
    (void) reason;

    if (blehid.isBootMode()) {
        save_tmp_file();
        DEBUG_PRINTLN("Resetting HID mode");
        delay(1000);
        NVIC_SystemReset();
    }

    connection_count--;

    // Keep advertising if not at max connections
    if (connection_count < max_prph_connection) {
        Bluefruit.Advertising.start(0);
    }
}

void set_keyboard_led(uint16_t conn_handle, uint8_t led_bitmap) {
    // Light up red LED if any bits are set
    if (led_bitmap) {
        ledOn(LED_RED);
    } else {
        ledOff(LED_RED);
    }
}
