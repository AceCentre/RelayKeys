/*********************************************************************
 RelayKeys Basic Test Example
 
 This example demonstrates basic RelayKeys functionality by sending
 test keyboard and mouse commands. Useful for testing hardware setup
 and verifying AT command compatibility.
 
 Copyright Ace Centre 2024 - MIT Licence
 
 Hardware Requirements:
 - nRF52840 or ESP32 board with RelayKeys firmware
 - Serial connection for sending commands
 
 Usage:
 1. Upload RelayKeys firmware to your board
 2. Upload this test sketch to a second Arduino (or use serial monitor)
 3. Connect the boards via serial (or use USB serial)
 4. The test will send various AT commands to demonstrate functionality
*********************************************************************/

// Test configuration
#define TEST_DELAY 2000  // Delay between test commands (ms)
#define SERIAL_BAUD 115200

// Test commands
const char* testCommands[] = {
  // Basic connectivity test
  "AT",
  
  // Get current mode
  "AT+GETMODE",
  
  // Send "Hello" text (H-e-l-l-o)
  "AT+BLEKEYBOARDCODE=00-00-0B-08-0F-0F-12-00",
  "AT+BLEKEYBOARDCODE=00-00-00-00-00-00-00-00", // Release keys
  
  // Send space
  "AT+BLEKEYBOARDCODE=00-00-2C-00-00-00-00-00",
  "AT+BLEKEYBOARDCODE=00-00-00-00-00-00-00-00", // Release keys
  
  // Send "World" text (W-o-r-l-d)
  "AT+BLEKEYBOARDCODE=00-00-1A-12-15-0F-07-00",
  "AT+BLEKEYBOARDCODE=00-00-00-00-00-00-00-00", // Release keys
  
  // Mouse movement tests
  "AT+BLEHIDMOUSEMOVE=10,0,0,0",   // Move right
  "AT+BLEHIDMOUSEMOVE=-10,0,0,0",  // Move left
  "AT+BLEHIDMOUSEMOVE=0,10,0,0",   // Move down
  "AT+BLEHIDMOUSEMOVE=0,-10,0,0",  // Move up
  
  // Mouse click tests
  "AT+BLEHIDMOUSEBUTTON=l,click",      // Left click
  "AT+BLEHIDMOUSEBUTTON=r,click",      // Right click
  "AT+BLEHIDMOUSEBUTTON=m,click",      // Middle click
  
  // Mouse scroll tests
  "AT+BLEHIDMOUSEMOVE=0,0,1,0",    // Scroll down
  "AT+BLEHIDMOUSEMOVE=0,0,-1,0",   // Scroll up
  
  // Volume control tests
  "AT+BLEKEYBOARDCODE=00-00-80-00-00-00-00-00", // Volume up
  "AT+BLEKEYBOARDCODE=00-00-00-00-00-00-00-00", // Release
  "AT+BLEKEYBOARDCODE=00-00-81-00-00-00-00-00", // Volume down
  "AT+BLEKEYBOARDCODE=00-00-00-00-00-00-00-00", // Release
  
  // Device management tests
  "AT+PRINTDEVLIST",               // List paired devices
  "AT+BLECURRENTDEVICENAME",       // Get current device name
  
  // End marker
  NULL
};

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(2000);
  
  Serial.println("RelayKeys Basic Test Starting...");
  Serial.println("Make sure RelayKeys device is connected and paired with a target device.");
  Serial.println("Commands will be sent every 2 seconds.");
  Serial.println("----------------------------------------");
  
  delay(3000); // Give user time to read instructions
}

void loop() {
  static int commandIndex = 0;
  
  // Check if we've reached the end of commands
  if (testCommands[commandIndex] == NULL) {
    Serial.println("----------------------------------------");
    Serial.println("All test commands completed!");
    Serial.println("Restarting test sequence in 10 seconds...");
    delay(10000);
    commandIndex = 0;
    return;
  }
  
  // Send current command
  String command = String(testCommands[commandIndex]);
  Serial.print("Sending: ");
  Serial.println(command);
  
  // Send command with proper line ending
  Serial.print(command);
  Serial.print("\r\n");
  
  // Wait for response (simple timeout)
  unsigned long startTime = millis();
  String response = "";
  
  while (millis() - startTime < 1000) { // 1 second timeout
    if (Serial.available()) {
      char c = Serial.read();
      response += c;
      if (c == '\n') break; // End of response
    }
  }
  
  // Print response
  if (response.length() > 0) {
    Serial.print("Response: ");
    Serial.print(response);
  } else {
    Serial.println("No response received");
  }
  
  Serial.println();
  
  // Move to next command
  commandIndex++;
  
  // Wait before next command
  delay(TEST_DELAY);
}

// Helper function to send a single AT command (can be called from serial monitor)
void sendATCommand(String command) {
  Serial.print("Manual command: ");
  Serial.println(command);
  Serial.print(command);
  Serial.print("\r\n");
  
  // Wait for response
  unsigned long startTime = millis();
  while (millis() - startTime < 1000) {
    if (Serial.available()) {
      Serial.write(Serial.read());
    }
  }
  Serial.println();
}

// Additional test functions that can be called manually

void testKeyboardInput() {
  Serial.println("Testing keyboard input...");
  
  // Type "RelayKeys Test"
  const char* message[] = {
    "AT+BLEKEYBOARDCODE=00-00-15-08-0F-04-1C-0E", // "Relay"
    "AT+BLEKEYBOARDCODE=00-00-00-00-00-00-00-00", // Release
    "AT+BLEKEYBOARDCODE=00-00-0E-08-1C-16-00-00", // "Keys"
    "AT+BLEKEYBOARDCODE=00-00-00-00-00-00-00-00", // Release
    "AT+BLEKEYBOARDCODE=00-00-2C-00-00-00-00-00", // Space
    "AT+BLEKEYBOARDCODE=00-00-00-00-00-00-00-00", // Release
    "AT+BLEKEYBOARDCODE=00-00-17-08-16-17-00-00", // "Test"
    "AT+BLEKEYBOARDCODE=00-00-00-00-00-00-00-00", // Release
    NULL
  };
  
  for (int i = 0; message[i] != NULL; i++) {
    Serial.println(message[i]);
    delay(500);
  }
}

void testMouseMovement() {
  Serial.println("Testing mouse movement...");
  
  // Draw a square with mouse movement
  Serial.println("AT+BLEHIDMOUSEMOVE=50,0,0,0");   // Right
  delay(500);
  Serial.println("AT+BLEHIDMOUSEMOVE=0,50,0,0");   // Down
  delay(500);
  Serial.println("AT+BLEHIDMOUSEMOVE=-50,0,0,0");  // Left
  delay(500);
  Serial.println("AT+BLEHIDMOUSEMOVE=0,-50,0,0");  // Up
  delay(500);
}

void testDeviceManagement() {
  Serial.println("Testing device management...");
  
  Serial.println("AT+PRINTDEVLIST");
  delay(1000);
  Serial.println("AT+BLECURRENTDEVICENAME");
  delay(1000);
  Serial.println("AT+GETMODE");
  delay(1000);
}
