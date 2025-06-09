/*********************************************************************
 RelayKeys Raspberry Pi Pico W Board Configuration
 
 EXPERIMENTAL - UNTESTED
 
 This file contains board-specific pin definitions and configurations
 for Raspberry Pi Pico W boards used with RelayKeys.
 
 Copyright Ace Centre 2024 - MIT Licence
*********************************************************************/

#ifndef BOARD_CONFIG_H
#define BOARD_CONFIG_H

#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"

// ===================================================================
// Raspberry Pi Pico W Standard Configuration
// ===================================================================
#define BOARD_PICO_W

#ifdef BOARD_PICO_W
  #define USER_SW 14         // GPIO 14 for user button (configurable)
  #define STATUS_LED_BUILTIN // Use built-in LED on CYW43 chip
  #define BOARD_NAME "Raspberry Pi Pico W"
#endif

// ===================================================================
// Custom Pico W Configuration
// ===================================================================
// Uncomment and modify if you want different pin assignments
// #define BOARD_PICO_W_CUSTOM
#ifdef BOARD_PICO_W_CUSTOM
  #define USER_SW 15         // Custom button pin
  #define STATUS_LED 25      // External LED pin (if not using built-in)
  #define BOARD_NAME "Custom Pico W"
  // #undef STATUS_LED_BUILTIN  // Uncomment to use external LED
#endif

// ===================================================================
// Validation and Defaults
// ===================================================================

// Ensure a board is selected
#if !defined(BOARD_PICO_W) && !defined(BOARD_PICO_W_CUSTOM)
  #warning "No board configuration selected! Using Pico W defaults."
  #define BOARD_PICO_W
  #define USER_SW 14
  #define STATUS_LED_BUILTIN
  #define BOARD_NAME "Raspberry Pi Pico W (Default)"
#endif

// Validate pin definitions
#ifndef USER_SW
  #error "USER_SW pin not defined! Check your board configuration."
#endif

#if !defined(STATUS_LED) && !defined(STATUS_LED_BUILTIN)
  #error "STATUS_LED not defined! Check your board configuration."
#endif

#ifndef BOARD_NAME
  #define BOARD_NAME "Unknown Pico W"
#endif

// ===================================================================
// Board-specific initialization macros
// ===================================================================

#define INIT_USER_BUTTON() do { \
    gpio_init(USER_SW); \
    gpio_set_dir(USER_SW, GPIO_IN); \
    gpio_pull_up(USER_SW); \
} while(0)

#ifdef STATUS_LED_BUILTIN
  #define INIT_STATUS_LED() do { \
    /* Built-in LED is initialized with cyw43_arch_init() */ \
  } while(0)
  
  #define LED_ON() cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1)
  #define LED_OFF() cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0)
  #define LED_TOGGLE() do { \
    static bool led_state = false; \
    led_state = !led_state; \
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, led_state); \
  } while(0)
  #define LED_SET(state) cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, state)
#else
  #define INIT_STATUS_LED() do { \
    gpio_init(STATUS_LED); \
    gpio_set_dir(STATUS_LED, GPIO_OUT); \
  } while(0)
  
  #define LED_ON() gpio_put(STATUS_LED, 1)
  #define LED_OFF() gpio_put(STATUS_LED, 0)
  #define LED_TOGGLE() gpio_put(STATUS_LED, !gpio_get(STATUS_LED))
  #define LED_SET(state) gpio_put(STATUS_LED, state)
#endif

// Button reading macro (active low with pull-up)
#define BUTTON_PRESSED() (!gpio_get(USER_SW))

// ===================================================================
// Debug information
// ===================================================================

#ifdef DEBUG
  #define PRINT_BOARD_INFO() do { \
    printf("=== Pico W Board Configuration ===\n"); \
    printf("Board: %s\n", BOARD_NAME); \
    printf("User Button Pin: GPIO %d\n", USER_SW); \
    printf("Status LED: %s\n", \
           defined(STATUS_LED_BUILTIN) ? "Built-in (CYW43)" : "External GPIO"); \
    if (!defined(STATUS_LED_BUILTIN)) { \
      printf("Status LED Pin: GPIO %d\n", STATUS_LED); \
    } \
    printf("Bluetooth: CYW43439 (BTStack)\n"); \
    printf("==================================\n"); \
  } while(0)
#else
  #define PRINT_BOARD_INFO() do { \
    printf("Board: %s\n", BOARD_NAME); \
  } while(0)
#endif

// ===================================================================
// Platform-specific definitions
// ===================================================================

// Timing constants for Pico W
#define BUTTON_DEBOUNCE_TIME 100    // 100ms debounce
#define BUTTON_CLICK_TIMEOUT 500    // 500ms for click detection

// Memory and performance settings
#define MAX_BLE_DEVICES 10          // Reduced for Pico W memory constraints
#define MAX_BLE_DEV_LIST_SIZE_DEFAULT 3

// BTStack specific settings
#define ENABLE_CLASSIC_PAIRING      // Enable classic Bluetooth pairing
#define ENABLE_BLE_PAIRING          // Enable BLE pairing

// ===================================================================
// Hardware capabilities
// ===================================================================

#define HAS_BLUETOOTH_LE 1          // Pico W has BLE support
#define HAS_BLUETOOTH_CLASSIC 1     // Pico W has classic Bluetooth
#define HAS_WIFI 1                  // Pico W has WiFi (not used in RelayKeys)
#define HAS_FLASH_STORAGE 1         // Pico W has flash storage
#define HAS_NATIVE_USB 1            // Pico W has native USB support

// Flash storage settings (for future implementation)
#define FLASH_STORAGE_SIZE (256 * 1024)  // 256KB for user data
#define FLASH_STORAGE_OFFSET (1024 * 1024)  // Start at 1MB offset

// ===================================================================
// Compatibility definitions
// ===================================================================

// Make compatible with RelayKeys common header
#ifndef BLE_NAME
  #define BLE_NAME "AceRK"
#endif

#ifndef BLE_MANUFACTURER
  #define BLE_MANUFACTURER "Ace Centre"
#endif

// Debug macros compatible with Arduino style
#ifdef DEBUG
  #define DEBUG_PRINT(x) printf("%s", x)
  #define DEBUG_PRINTLN(x) printf("%s\n", x)
#else
  #define DEBUG_PRINT(x)
  #define DEBUG_PRINTLN(x)
#endif

#endif // BOARD_CONFIG_H
