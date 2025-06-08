#!/usr/bin/env python3
"""
Quick script to check available COM ports and find RelayKeys dongle
"""

import serial.tools.list_ports


def check_ports():
    print("🔍 Scanning for available COM ports...")
    ports = serial.tools.list_ports.comports()

    if not ports:
        print("❌ No COM ports found")
        return

    print(f"📍 Found {len(ports)} COM port(s):")

    for port in ports:
        print(f"\n  Port: {port.device}")
        print(f"  Description: {port.description}")
        print(f"  Hardware ID: {port.hwid}")
        if hasattr(port, "vid") and port.vid:
            print(f"  VID: {hex(port.vid)}")
        if hasattr(port, "pid") and port.pid:
            print(f"  PID: {hex(port.pid)}")

        # Check if this looks like a RelayKeys device
        is_relaykeys = False
        if "CP2104" in port.description:
            is_relaykeys = True
            print("  🎯 MATCH: CP2104 detected")
        elif "nRF52" in port.description:
            is_relaykeys = True
            print("  🎯 MATCH: nRF52 detected")
        elif hasattr(port, "vid") and port.vid and hex(port.vid).upper() == "0X239A":
            is_relaykeys = True
            print("  🎯 MATCH: Adafruit VID detected")
        elif "239A" in port.hwid.upper():
            is_relaykeys = True
            print("  🎯 MATCH: Adafruit hardware ID detected")

        if is_relaykeys:
            print("  ✅ This looks like a RelayKeys device!")
            return port.device

    print("\n❌ No RelayKeys device found")
    return None


if __name__ == "__main__":
    device = check_ports()
    if device:
        print(f"\n🚀 Try running: uv run python relaykeysd.py --debug --dev={device}")
