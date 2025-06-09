/*********************************************************************
 RelayKeys ESP32 Receiver Dongle
 
 ESP32 implementation of the RelayKeys receiver dongle that acts as a
 BLE Central device to connect to RelayKeys transmitters and forwards
 HID reports via USB to the host computer.
 
 This replaces the nRF52840 receiver dongle with ESP32 functionality.
 
 Hardware Requirements:
 - ESP32-S2, ESP32-S3, or ESP32-C3 (for native USB HID support)
 - OR ESP32-WROOM with USB Host shield (not implemented in this version)
 
 Features:
 - BLE Central mode to connect to "AceRK" devices
 - USB HID Keyboard, Mouse, and Consumer Control output
 - Status LED indication for connection state
 - Button for manual connection/pairing
 
 Copyright Ace Centre 2024 - MIT Licence
*********************************************************************/

#include "BLEDevice.h"
#include "BLEClient.h"
#include "BLEUtils.h"
#include "BLEScan.h"
#include "BLEAdvertisedDevice.h"
#include "board_config.h"

#if HAS_NATIVE_USB
  #include "USB.h"
  #include "USBHIDKeyboard.h"
  #include "USBHIDMouse.h"
  #include "USBHIDConsumerControl.h"
#endif

//#define DEBUG // enables serial prints of received data, disables usb hid actions

#define BLE_NAME "AceRK receiver"
#define TARGET_DEVICE_NAME "AceRK"

// BLE UUIDs for HID service
static BLEUUID serviceUUID("1812"); // HID Service
static BLEUUID charUUID_keyboard("2A4D"); // HID Report (Keyboard)
static BLEUUID charUUID_mouse("2A4D"); // HID Report (Mouse) 
static BLEUUID charUUID_consumer("2A4D"); // HID Report (Consumer)

// BLE objects
BLEClient* pClient = nullptr;
BLERemoteService* pRemoteService = nullptr;
BLERemoteCharacteristic* pRemoteCharKeyboard = nullptr;
BLERemoteCharacteristic* pRemoteCharMouse = nullptr;
BLERemoteCharacteristic* pRemoteCharConsumer = nullptr;
BLEScan* pBLEScan = nullptr;

#if HAS_NATIVE_USB
// USB HID objects
USBHIDKeyboard keyboard;
USBHIDMouse mouse;
USBHIDConsumerControl consumerControl;
#endif

// Connection state
bool deviceConnected = false;
bool doConnect = false;
bool doScan = false;
BLEAdvertisedDevice* myDevice = nullptr;

// Status LED timing
unsigned long lastLedUpdate = 0;
bool ledState = false;

// HID Report IDs (matching the transmitter)
enum {
  RID_KEYBOARD = 1,
  RID_MOUSE = 2,
  RID_CONSUMER_CONTROL = 3,
};

// Forward declarations
void updateStatusLED();
void startScanning();
bool connectToServer();
void notifyCallback(BLERemoteCharacteristic* pBLERemoteCharacteristic, uint8_t* pData, size_t length, bool isNotify);

// BLE Advertised Device Callbacks
class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
  void onResult(BLEAdvertisedDevice advertisedDevice) {
    Serial.print("BLE Advertised Device found: ");
    Serial.println(advertisedDevice.toString().c_str());

    // Check if this is our target device
    if (advertisedDevice.haveName() && advertisedDevice.getName() == TARGET_DEVICE_NAME) {
      Serial.println("Found RelayKeys device!");
      
      BLEDevice::getScan()->stop();
      myDevice = new BLEAdvertisedDevice(advertisedDevice);
      doConnect = true;
      doScan = true;
    }
  }
};

// BLE Client Callbacks
class MyClientCallback : public BLEClientCallbacks {
  void onConnect(BLEClient* pclient) {
    Serial.println("Connected to RelayKeys device");
    deviceConnected = true;
  }

  void onDisconnect(BLEClient* pclient) {
    Serial.println("Disconnected from RelayKeys device");
    deviceConnected = false;
    doScan = true; // Start scanning again
  }
};

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("RelayKeys ESP32 Receiver Dongle Starting...");
  PRINT_BOARD_INFO();
  
  // Initialize pins
  INIT_USER_BUTTON();
  INIT_STATUS_LED();
  
  // Initialize USB HID if supported
  #if HAS_NATIVE_USB
    USB.begin();
    keyboard.begin();
    mouse.begin();
    consumerControl.begin();
    Serial.println("USB HID initialized");
  #else
    Serial.println("Warning: No native USB HID support on this board");
  #endif
  
  // Initialize BLE
  BLEDevice::init(BLE_NAME);
  
  // Create BLE Client
  pClient = BLEDevice::createClient();
  pClient->setClientCallbacks(new MyClientCallback());
  
  // Setup BLE scanning
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setInterval(1349);
  pBLEScan->setWindow(449);
  pBLEScan->setActiveScan(true);
  
  updateStatusLED();
  startScanning();
  
  Serial.println("RelayKeys ESP32 Receiver Ready");
}

void loop() {
  // Handle connection process
  if (doConnect == true) {
    if (connectToServer()) {
      Serial.println("Connected to the BLE Server.");
    } else {
      Serial.println("Failed to connect to the server; there is nothing more we will do.");
    }
    doConnect = false;
  }
  
  // Handle scanning restart
  if (doScan) {
    startScanning();
    doScan = false;
  }
  
  // Handle button press for manual reconnection
  if (BUTTON_PRESSED()) {
    delay(50); // Debounce
    if (BUTTON_PRESSED()) {
      Serial.println("Button pressed - restarting scan");
      if (deviceConnected && pClient) {
        pClient->disconnect();
      }
      doScan = true;
      while (BUTTON_PRESSED()) {
        delay(10); // Wait for button release
      }
    }
  }
  
  // Update status LED
  updateStatusLED();
  
  delay(10);
}

void startScanning() {
  Serial.println("Starting BLE scan for RelayKeys devices...");
  pBLEScan->start(5, false); // Scan for 5 seconds
}

bool connectToServer() {
  Serial.print("Forming a connection to ");
  Serial.println(myDevice->getAddress().toString().c_str());
  
  if (!pClient->connect(myDevice)) {
    Serial.println("Failed to connect");
    return false;
  }
  
  Serial.println("Connected to server");
  
  // Obtain a reference to the service we are after in the remote BLE server
  pRemoteService = pClient->getService(serviceUUID);
  if (pRemoteService == nullptr) {
    Serial.print("Failed to find our service UUID: ");
    Serial.println(serviceUUID.toString().c_str());
    pClient->disconnect();
    return false;
  }
  Serial.println("Found our service");
  
  // Get characteristics and setup notifications
  // Note: In a real implementation, you'd need to handle multiple characteristics
  // with different report IDs. This is a simplified version.
  std::map<std::string, BLERemoteCharacteristic*>* pMap = pRemoteService->getCharacteristics();
  
  for (auto &myPair : *pMap) {
    BLERemoteCharacteristic* pChar = myPair.second;
    
    if (pChar->canNotify()) {
      pChar->registerForNotify(notifyCallback);
      Serial.println("Registered for notifications on characteristic");
    }
  }
  
  return true;
}

// Callback for BLE notifications (HID reports)
void notifyCallback(BLERemoteCharacteristic* pBLERemoteCharacteristic, uint8_t* pData, size_t length, bool isNotify) {
  #ifdef DEBUG
    Serial.print("Notify callback for characteristic ");
    Serial.print(pBLERemoteCharacteristic->getUUID().toString().c_str());
    Serial.print(" of data length ");
    Serial.println(length);
    Serial.print("Data: ");
    for (int i = 0; i < length; i++) {
      Serial.printf("%02X ", pData[i]);
    }
    Serial.println();
  #endif

  #if HAS_NATIVE_USB
    // Process HID reports based on length and content
    if (length >= 8) {
      // Likely a keyboard report (8 bytes)
      processKeyboardReport(pData, length);
    } else if (length >= 4) {
      // Likely a mouse report (4+ bytes)
      processMouseReport(pData, length);
    } else if (length >= 2) {
      // Likely a consumer control report (2 bytes)
      processConsumerReport(pData, length);
    }
  #endif
}

#if HAS_NATIVE_USB
void processKeyboardReport(uint8_t* data, size_t length) {
  if (length < 8) return;

  #ifdef DEBUG
    Serial.println("Processing keyboard report");
  #else
    // Standard HID keyboard report format:
    // Byte 0: Modifier keys
    // Byte 1: Reserved
    // Bytes 2-7: Key codes

    uint8_t modifiers = data[0];
    uint8_t keycodes[6];

    for (int i = 0; i < 6; i++) {
      keycodes[i] = (i + 2 < length) ? data[i + 2] : 0;
    }

    // Send keyboard report
    keyboard.sendReport(modifiers, keycodes, 6);
  #endif
}

void processMouseReport(uint8_t* data, size_t length) {
  if (length < 4) return;

  #ifdef DEBUG
    Serial.println("Processing mouse report");
  #else
    // Standard HID mouse report format:
    // Byte 0: Button state
    // Byte 1: X movement
    // Byte 2: Y movement
    // Byte 3: Wheel movement

    uint8_t buttons = data[0];
    int8_t deltaX = (int8_t)data[1];
    int8_t deltaY = (int8_t)data[2];
    int8_t wheel = (length > 3) ? (int8_t)data[3] : 0;

    // Send mouse report
    if (buttons != 0) {
      mouse.click(buttons);
    }
    if (deltaX != 0 || deltaY != 0) {
      mouse.move(deltaX, deltaY);
    }
    if (wheel != 0) {
      mouse.move(0, 0, wheel);
    }
  #endif
}

void processConsumerReport(uint8_t* data, size_t length) {
  if (length < 2) return;

  #ifdef DEBUG
    Serial.println("Processing consumer control report");
  #else
    // Consumer control report format:
    // 2 bytes for media key codes
    uint16_t consumerKey = data[0] | (data[1] << 8);

    if (consumerKey != 0) {
      consumerControl.press(consumerKey);
      delay(10);
      consumerControl.release();
    }
  #endif
}
#endif

void updateStatusLED() {
  unsigned long currentTime = millis();

  if (deviceConnected) {
    // Solid on when connected
    LED_ON();
  } else {
    // Blink when scanning/disconnected
    if (currentTime - lastLedUpdate > 500) {
      ledState = !ledState;
      if (ledState) {
        LED_ON();
      } else {
        LED_OFF();
      }
      lastLedUpdate = currentTime;
    }
  }
}
