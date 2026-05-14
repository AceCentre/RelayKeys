"""
Core RelayKeys functionality

This module contains the core components:
- Daemon for BLE HID communication
- Client for sending commands to the daemon
- BLE HID protocol implementation
- Serial communication wrappers
"""

from .client import RelayKeysClient
from .daemon import main as daemon_main

__all__ = [
    "RelayKeysClient", 
    "daemon_main",
]
