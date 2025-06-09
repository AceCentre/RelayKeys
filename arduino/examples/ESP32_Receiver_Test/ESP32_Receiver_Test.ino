/*********************************************************************
 RelayKeys ESP32 Receiver Test Example
 
 This example demonstrates the ESP32 receiver dongle functionality by
 monitoring its operation and providing diagnostic information.
 
 This sketch should be uploaded to a separate Arduino board connected
 to the ESP32 receiver's serial output for monitoring purposes.
 
 Copyright Ace Centre 2024 - MIT Licence
 
 Hardware Requirements:
 - ESP32 receiver dongle running receiver_dongle_ESP32.ino
 - Second Arduino board for monitoring (or use serial monitor)
 - RelayKeys transmitter for testing
 
 Usage:
 1. Upload receiver firmware to ESP32 board
 2. Upload this test sketch to monitoring Arduino (optional)
 3. Connect ESP32 receiver to host computer via USB
 4. Power on RelayKeys transmitter
 5. Monitor serial output for connection status and HID data
*********************************************************************/

// Test configuration
#define SERIAL_BAUD 115200
#define MONITOR_INTERVAL 5000  // Status check interval (ms)

// Test state
unsigned long lastStatusCheck = 0;
bool receiverConnected = false;
int hidReportsReceived = 0;

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(2000);
  
  Serial.println("=== RelayKeys ESP32 Receiver Test Monitor ===");
  Serial.println("This monitor helps verify ESP32 receiver functionality");
  Serial.println();
  Serial.println("Expected sequence:");
  Serial.println("1. ESP32 receiver starts scanning for 'AceRK' devices");
  Serial.println("2. When RelayKeys transmitter is found, connection is established");
  Serial.println("3. HID reports from transmitter are forwarded to host computer");
  Serial.println("4. Status LED shows connection state");
  Serial.println();
  Serial.println("Monitoring ESP32 receiver serial output...");
  Serial.println("================================================");
  
  lastStatusCheck = millis();
}

void loop() {
  // Monitor serial input from ESP32 receiver
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();
    
    // Parse and categorize messages
    if (line.indexOf("RelayKeys ESP32 Receiver") >= 0) {
      Serial.println("[STARTUP] " + line);
    }
    else if (line.indexOf("Starting BLE scan") >= 0) {
      Serial.println("[SCAN] " + line);
      receiverConnected = false;
    }
    else if (line.indexOf("Found RelayKeys device") >= 0) {
      Serial.println("[DISCOVERY] " + line);
    }
    else if (line.indexOf("Connected to") >= 0) {
      Serial.println("[CONNECTION] " + line);
      receiverConnected = true;
    }
    else if (line.indexOf("Disconnected") >= 0) {
      Serial.println("[DISCONNECTION] " + line);
      receiverConnected = false;
    }
    else if (line.indexOf("Notify callback") >= 0) {
      Serial.println("[HID_DATA] " + line);
      hidReportsReceived++;
    }
    else if (line.indexOf("Processing") >= 0) {
      Serial.println("[HID_PROCESS] " + line);
    }
    else if (line.indexOf("Button pressed") >= 0) {
      Serial.println("[USER_INPUT] " + line);
    }
    else if (line.indexOf("ERROR") >= 0 || line.indexOf("Failed") >= 0) {
      Serial.println("[ERROR] " + line);
    }
    else if (line.length() > 0) {
      Serial.println("[INFO] " + line);
    }
  }
  
  // Periodic status report
  if (millis() - lastStatusCheck >= MONITOR_INTERVAL) {
    printStatusReport();
    lastStatusCheck = millis();
  }
  
  delay(10);
}

void printStatusReport() {
  Serial.println();
  Serial.println("=== STATUS REPORT ===");
  Serial.print("Receiver Connected: ");
  Serial.println(receiverConnected ? "YES" : "NO");
  Serial.print("HID Reports Received: ");
  Serial.println(hidReportsReceived);
  Serial.print("Uptime: ");
  Serial.print(millis() / 1000);
  Serial.println(" seconds");
  
  if (!receiverConnected) {
    Serial.println();
    Serial.println("TROUBLESHOOTING TIPS:");
    Serial.println("- Ensure RelayKeys transmitter is powered on");
    Serial.println("- Check that transmitter is advertising as 'AceRK'");
    Serial.println("- Press button on receiver to restart scanning");
    Serial.println("- Verify ESP32 receiver firmware is properly uploaded");
  } else {
    Serial.println();
    Serial.println("CONNECTION ACTIVE:");
    Serial.println("- HID reports should be forwarded to host computer");
    Serial.println("- Test keyboard/mouse input on transmitter");
    Serial.println("- Check host computer for HID device recognition");
  }
  
  Serial.println("=====================");
  Serial.println();
}

// Manual test functions (call from serial monitor)
void sendTestInstructions() {
  Serial.println();
  Serial.println("=== MANUAL TEST INSTRUCTIONS ===");
  Serial.println("1. Ensure ESP32 receiver is connected to host computer");
  Serial.println("2. Power on RelayKeys transmitter");
  Serial.println("3. Wait for connection (LED solid on receiver)");
  Serial.println("4. Test the following on transmitter:");
  Serial.println("   - Send keyboard commands via AT+BLEKEYBOARDCODE");
  Serial.println("   - Send mouse commands via AT+BLEHIDMOUSEMOVE");
  Serial.println("   - Send mouse clicks via AT+BLEHIDMOUSEBUTTON");
  Serial.println("5. Verify HID input is received on host computer");
  Serial.println("6. Check this monitor for HID data processing messages");
  Serial.println("================================");
  Serial.println();
}

void printHardwareInfo() {
  Serial.println();
  Serial.println("=== HARDWARE REQUIREMENTS ===");
  Serial.println("ESP32 Receiver Dongle:");
  Serial.println("- ESP32-S2, ESP32-S3, or ESP32-C3 (recommended)");
  Serial.println("- Native USB HID support required");
  Serial.println("- Status LED for connection indication");
  Serial.println("- Button for manual reconnection");
  Serial.println();
  Serial.println("RelayKeys Transmitter:");
  Serial.println("- nRF52840 or ESP32 with RelayKeys firmware");
  Serial.println("- Must advertise as 'AceRK' device name");
  Serial.println("- BLE HID service implementation");
  Serial.println("=============================");
  Serial.println();
}

void printExpectedBehavior() {
  Serial.println();
  Serial.println("=== EXPECTED BEHAVIOR ===");
  Serial.println("Receiver LED States:");
  Serial.println("- Blinking: Scanning for devices or disconnected");
  Serial.println("- Solid ON: Connected to RelayKeys transmitter");
  Serial.println();
  Serial.println("Serial Output:");
  Serial.println("- Startup messages with board configuration");
  Serial.println("- BLE scanning and discovery messages");
  Serial.println("- Connection/disconnection events");
  Serial.println("- HID data processing notifications");
  Serial.println();
  Serial.println("Host Computer:");
  Serial.println("- Should recognize ESP32 as USB HID device");
  Serial.println("- Keyboard/mouse input forwarded from transmitter");
  Serial.println("- No additional drivers required");
  Serial.println("=========================");
  Serial.println();
}

// Call these functions from serial monitor for additional information:
// sendTestInstructions();
// printHardwareInfo();
// printExpectedBehavior();
