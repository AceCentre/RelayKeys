/*********************************************************************
 RelayKeys ESP32 Receiver Dongle Board Configuration
 
 This file contains board-specific pin definitions and configurations
 for different ESP32 development boards used as receiver dongles.
 Uncomment the section that matches your hardware.
 
 Copyright Ace Centre 2024 - MIT Licence
*********************************************************************/

#ifndef BOARD_CONFIG_H
#define BOARD_CONFIG_H

// Uncomment ONE of the following board configurations

// ===================================================================
// ESP32-S2/S3 Development Board (with native USB support)
// ===================================================================
#define BOARD_ESP32_S2_S3
#ifdef BOARD_ESP32_S2_S3
  #define USER_SW 0          // Boot button
  #define STATUS_LED 2       // Built-in LED
  #define BOARD_NAME "ESP32-S2/S3"
  #define HAS_NATIVE_USB 1   // Native USB HID support
#endif

// ===================================================================
// ESP32-WROOM Development Board (requires USB Host shield)
// ===================================================================
// #define BOARD_ESP32_WROOM
#ifdef BOARD_ESP32_WROOM
  #define USER_SW 0          // Boot button
  #define STATUS_LED 2       // Built-in LED
  #define BOARD_NAME "ESP32-WROOM"
  #define HAS_NATIVE_USB 0   // No native USB, needs USB Host
#endif

// ===================================================================
// ESP32-C3 Development Board
// ===================================================================
// #define BOARD_ESP32_C3
#ifdef BOARD_ESP32_C3
  #define USER_SW 9          // Boot button
  #define STATUS_LED 8       // RGB LED
  #define BOARD_NAME "ESP32-C3"
  #define HAS_NATIVE_USB 1   // Native USB HID support
#endif

// ===================================================================
// TTGO T-Display ESP32
// ===================================================================
// #define BOARD_TTGO_T_DISPLAY
#ifdef BOARD_TTGO_T_DISPLAY
  #define USER_SW 35         // Button 1
  #define STATUS_LED 4       // Backlight control (no built-in LED)
  #define BOARD_NAME "TTGO T-Display"
  #define HAS_NATIVE_USB 0   // No native USB
#endif

// ===================================================================
// Adafruit ESP32 Feather
// ===================================================================
// #define BOARD_ADAFRUIT_ESP32_FEATHER
#ifdef BOARD_ADAFRUIT_ESP32_FEATHER
  #define USER_SW 0          // Boot button
  #define STATUS_LED 13      // Red LED
  #define BOARD_NAME "Adafruit ESP32 Feather"
  #define HAS_NATIVE_USB 0   // No native USB
#endif

// ===================================================================
// Custom Board Configuration
// ===================================================================
// #define BOARD_CUSTOM
#ifdef BOARD_CUSTOM
  #define USER_SW 0          // Define your button pin
  #define STATUS_LED 2       // Define your LED pin
  #define BOARD_NAME "Custom ESP32"
  #define HAS_NATIVE_USB 1   // Set to 1 if your board has native USB
  
  // Add any additional pin definitions here
  // #define EXTRA_LED 4
  // #define EXTRA_BUTTON 5
#endif

// ===================================================================
// Validation and Defaults
// ===================================================================

// Ensure a board is selected
#if !defined(BOARD_ESP32_S2_S3) && !defined(BOARD_ESP32_WROOM) && !defined(BOARD_ESP32_C3) && \
    !defined(BOARD_TTGO_T_DISPLAY) && !defined(BOARD_ADAFRUIT_ESP32_FEATHER) && \
    !defined(BOARD_CUSTOM)
  #warning "No board configuration selected! Using ESP32-S2/S3 defaults."
  #define BOARD_ESP32_S2_S3
  #define USER_SW 0
  #define STATUS_LED 2
  #define BOARD_NAME "ESP32-S2/S3 (Default)"
  #define HAS_NATIVE_USB 1
#endif

// Validate pin definitions
#ifndef USER_SW
  #error "USER_SW pin not defined! Check your board configuration."
#endif

#ifndef STATUS_LED
  #error "STATUS_LED pin not defined! Check your board configuration."
#endif

#ifndef BOARD_NAME
  #define BOARD_NAME "Unknown ESP32"
#endif

#ifndef HAS_NATIVE_USB
  #define HAS_NATIVE_USB 0
#endif

// Board-specific initialization macros
#define INIT_STATUS_LED() pinMode(STATUS_LED, OUTPUT)
#define INIT_USER_BUTTON() pinMode(USER_SW, INPUT_PULLUP)

// LED control macros
#define LED_ON() digitalWrite(STATUS_LED, HIGH)
#define LED_OFF() digitalWrite(STATUS_LED, LOW)
#define LED_TOGGLE() digitalWrite(STATUS_LED, !digitalRead(STATUS_LED))

// Button reading macro
#define BUTTON_PRESSED() (digitalRead(USER_SW) == LOW)

// Debug information
#ifdef DEBUG
  #define PRINT_BOARD_INFO() do { \
    Serial.println("=== Receiver Board Configuration ==="); \
    Serial.print("Board: "); Serial.println(BOARD_NAME); \
    Serial.print("User Button Pin: "); Serial.println(USER_SW); \
    Serial.print("Status LED Pin: "); Serial.println(STATUS_LED); \
    Serial.print("Native USB Support: "); Serial.println(HAS_NATIVE_USB ? "Yes" : "No"); \
    Serial.println("===================================="); \
  } while(0)
#else
  #define PRINT_BOARD_INFO()
#endif

#endif // BOARD_CONFIG_H
