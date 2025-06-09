# RelayKeys Raspberry Pi Pico W CMake Configuration
# EXPERIMENTAL - UNTESTED

cmake_minimum_required(VERSION 3.13)

# Include the Pico SDK
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

# Include BTStack (adjust path as needed)
set(BTSTACK_ROOT ${CMAKE_CURRENT_LIST_DIR}/../../../btstack)
include(${BTSTACK_ROOT}/port/pico/pico_btstack_config.cmake)

project(relaykeys_picow C CXX ASM)

# Set C/C++ standards
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize the Pico SDK
pico_sdk_init()

# Add executable
add_executable(arduino_PicoW
    arduino_PicoW.ino  # Note: This is actually C code, not Arduino
)

# Rename .ino to .c for proper compilation
set_source_files_properties(arduino_PicoW.ino PROPERTIES LANGUAGE C)

# Include directories
target_include_directories(arduino_PicoW PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/../common
    ${BTSTACK_ROOT}/src
    ${BTSTACK_ROOT}/port/pico
)

# Link libraries
target_link_libraries(arduino_PicoW
    pico_stdlib
    pico_cyw43_arch_lwip_threadsafe_background
    pico_btstack_ble
    pico_btstack_classic
    pico_btstack_hid
)

# Enable USB output, disable UART output
pico_enable_stdio_usb(arduino_PicoW 1)
pico_enable_stdio_uart(arduino_PicoW 0)

# Create map/bin/hex/uf2 files
pico_add_extra_outputs(arduino_PicoW)

# Compiler definitions
target_compile_definitions(arduino_PicoW PRIVATE
    PICO_DEFAULT_UART=0
    PICO_DEFAULT_UART_TX_PIN=0
    PICO_DEFAULT_UART_RX_PIN=1
    CYW43_ENABLE_BLUETOOTH=1
    BTSTACK_FILE__="arduino_PicoW.c"
)

# Compiler flags
target_compile_options(arduino_PicoW PRIVATE
    -Wall
    -Wextra
    -Wno-unused-parameter
    -Wno-unused-variable
    -O2
)

# Print build information
message(STATUS "Building RelayKeys for Raspberry Pi Pico W")
message(STATUS "PICO_SDK_PATH: $ENV{PICO_SDK_PATH}")
message(STATUS "BTSTACK_ROOT: ${BTSTACK_ROOT}")

# Optional: Add custom target for flashing
add_custom_target(flash
    COMMAND ${CMAKE_COMMAND} -E echo "Hold BOOTSEL button and connect Pico W via USB"
    COMMAND ${CMAKE_COMMAND} -E echo "Then copy arduino_PicoW.uf2 to RPI-RP2 drive"
    DEPENDS arduino_PicoW
)
