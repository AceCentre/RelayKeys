"""
RelayKeys - A simple app/hardware solution to send keystrokes from one computer to another over Bluetooth LE

This package provides:
- Core daemon functionality for BLE HID communication
- CLI tools for sending commands
- GUI application for user interaction
- Utilities for hardware detection and management
"""

__version__ = "2.02"
__author__ = "AceCentre"
__email__ = "info@acecentre.org.uk"

# Public API exports
from .core.client import RelayKeysClient
from .core.daemon import main as daemon_main

__all__ = [
    "RelayKeysClient",
    "daemon_main",
]
