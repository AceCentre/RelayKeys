#!/bin/bash

# RelayKeys Pico W Build Script
# EXPERIMENTAL - UNTESTED

set -e

echo "RelayKeys Pico W Build Script"
echo "============================="
echo "WARNING: This is experimental code and may not work!"
echo ""

# Check for required environment variables
if [ -z "$PICO_SDK_PATH" ]; then
    echo "ERROR: PICO_SDK_PATH environment variable not set"
    echo "Please install Pico SDK and set PICO_SDK_PATH"
    echo "Example: export PICO_SDK_PATH=/path/to/pico-sdk"
    exit 1
fi

if [ ! -d "$PICO_SDK_PATH" ]; then
    echo "ERROR: PICO_SDK_PATH directory does not exist: $PICO_SDK_PATH"
    exit 1
fi

# Check for BTStack
BTSTACK_ROOT="../../../btstack"
if [ ! -d "$BTSTACK_ROOT" ]; then
    echo "ERROR: BTStack not found at $BTSTACK_ROOT"
    echo "Please clone BTStack:"
    echo "  git clone https://github.com/bluekitchen/btstack.git"
    exit 1
fi

echo "Environment Check:"
echo "  PICO_SDK_PATH: $PICO_SDK_PATH"
echo "  BTSTACK_ROOT: $BTSTACK_ROOT"
echo ""

# Create build directory
BUILD_DIR="build"
if [ -d "$BUILD_DIR" ]; then
    echo "Cleaning existing build directory..."
    rm -rf "$BUILD_DIR"
fi

mkdir "$BUILD_DIR"
cd "$BUILD_DIR"

echo "Configuring CMake..."
cmake .. -DPICO_BOARD=pico_w

echo "Building RelayKeys for Pico W..."
make arduino_PicoW

if [ $? -eq 0 ]; then
    echo ""
    echo "Build completed successfully!"
    echo "Output file: $BUILD_DIR/arduino_PicoW.uf2"
    echo ""
    echo "To flash to Pico W:"
    echo "1. Hold BOOTSEL button while connecting USB"
    echo "2. Copy arduino_PicoW.uf2 to RPI-RP2 drive"
    echo "3. Pico W will reboot and run RelayKeys firmware"
    echo ""
    echo "WARNING: This firmware is experimental and untested!"
else
    echo ""
    echo "Build failed! This is expected for experimental code."
    echo "Check the error messages above and:"
    echo "1. Ensure all dependencies are installed"
    echo "2. Check BTStack integration"
    echo "3. Verify Pico SDK version compatibility"
    echo "4. Report issues on GitHub"
fi
