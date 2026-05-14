#!/bin/bash
set -e

mkdir -p firmware

SKETCH_TX="arduino/arduino_nRF52840/arduino_nRF52840.ino"
SKETCH_RX="arduino/receiver_dongle/receiver_dongle.ino"

build_uf2() {
    local name=$1
    local fqbn=$2
    local sketch=$3

    echo "Building $name (FQBN: $fqbn)..."
    arduino-cli compile --fqbn "$fqbn" --build-path "./build-firmware/$name" "$sketch"

    local hex
    hex=$(find "./build-firmware/$name" -name "*.hex" -not -name "bootloader*.hex" | head -1)
    if [ -z "$hex" ]; then
        echo "ERROR: No hex file found for $name"
        exit 1
    fi

    echo "  Converting $(basename $hex) to UF2..."
    python3 uf2conv.py "$hex" -c -f 0xADA52840 -o "firmware/${name}.UF2"
    echo "  -> firmware/${name}.UF2"
}

rm -rf build-firmware
mkdir -p build-firmware

build_uf2 "Feather-nRF52840"              "adafruit:nrf52:feather52840"  "$SKETCH_TX"
build_uf2 "Feather-nRF52840-Reciever"     "adafruit:nrf52:feather52840"  "$SKETCH_RX"
build_uf2 "ItsyBitsy"                    "adafruit:nrf52:itsybitsy52840" "$SKETCH_TX"
build_uf2 "ItsyBitsy-Reciever"           "adafruit:nrf52:itsybitsy52840" "$SKETCH_RX"
build_uf2 "Raytac-MDBT50Q"                "adafruit:nrf52:mdbt50qrx"     "$SKETCH_TX"
build_uf2 "Raytac-MDBT50Q-Reciever"       "adafruit:nrf52:mdbt50qrx"     "$SKETCH_RX"

echo ""
echo "Firmware builds complete:"
ls -lh firmware/*.UF2
