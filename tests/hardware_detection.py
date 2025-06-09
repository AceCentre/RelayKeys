#!/usr/bin/env python3
"""
Hardware detection utilities for RelayKeys testing
Automatically detects if RelayKeys hardware is connected
"""

import logging
from typing import Any, Dict, List, Optional

import serial.tools.list_ports


class HardwareDetector:
    """Detect RelayKeys hardware automatically"""
    
    # Known RelayKeys hardware identifiers
    RELAYKEYS_IDENTIFIERS = {
        'cp2104': {
            'description_contains': ['CP2104'],
            'name': 'CP2104 USB to UART Bridge'
        },
        'nrf52': {
            'description_contains': ['nRF52'],
            'name': 'nRF52 Development Kit'
        },
        'adafruit_vid': {
            'vid': 0x239A,
            'name': 'Adafruit Device'
        },
        'adafruit_hwid': {
            'hwid_contains': ['239A'],
            'name': 'Adafruit Hardware ID'
        }
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def scan_ports(self) -> List[Dict[str, Any]]:
        """Scan all available COM ports and return detailed info"""
        ports_info = []
        
        try:
            ports = serial.tools.list_ports.comports()
            
            for port in ports:
                port_info = {
                    'device': port.device,
                    'description': port.description,
                    'hwid': port.hwid,
                    'vid': getattr(port, 'vid', None),
                    'pid': getattr(port, 'pid', None),
                    'serial_number': getattr(port, 'serial_number', None),
                    'is_relaykeys': False,
                    'relaykeys_type': None
                }
                
                # Check if this port matches RelayKeys hardware
                relaykeys_type = self._identify_relaykeys_device(port)
                if relaykeys_type:
                    port_info['is_relaykeys'] = True
                    port_info['relaykeys_type'] = relaykeys_type
                
                ports_info.append(port_info)
                
        except Exception as e:
            self.logger.error(f"Error scanning ports: {e}")
        
        return ports_info
    
    def _identify_relaykeys_device(self, port) -> Optional[str]:
        """Identify if a port is a RelayKeys device and return its type"""
        
        # Check CP2104
        if any(id_str in port.description for id_str in self.RELAYKEYS_IDENTIFIERS['cp2104']['description_contains']):
            return 'cp2104'
        
        # Check nRF52
        if any(id_str in port.description for id_str in self.RELAYKEYS_IDENTIFIERS['nrf52']['description_contains']):
            return 'nrf52'
        
        # Check Adafruit VID
        if hasattr(port, 'vid') and port.vid == self.RELAYKEYS_IDENTIFIERS['adafruit_vid']['vid']:
            return 'adafruit_vid'
        
        # Check Adafruit HWID
        if any(id_str in port.hwid.upper() for id_str in self.RELAYKEYS_IDENTIFIERS['adafruit_hwid']['hwid_contains']):
            return 'adafruit_hwid'
        
        return None
    
    def find_relaykeys_devices(self) -> List[Dict[str, Any]]:
        """Find all RelayKeys devices"""
        all_ports = self.scan_ports()
        return [port for port in all_ports if port['is_relaykeys']]
    
    def get_primary_relaykeys_device(self) -> Optional[str]:
        """Get the primary RelayKeys device port"""
        devices = self.find_relaykeys_devices()
        
        if not devices:
            return None
        
        # Prefer CP2104 devices first, then others
        for device in devices:
            if device['relaykeys_type'] == 'cp2104':
                return device['device']
        
        # Return first available device
        return devices[0]['device']
    
    def is_hardware_connected(self) -> bool:
        """Check if any RelayKeys hardware is connected"""
        return len(self.find_relaykeys_devices()) > 0
    
    def get_hardware_info(self) -> Dict[str, Any]:
        """Get comprehensive hardware information"""
        devices = self.find_relaykeys_devices()
        
        return {
            'hardware_connected': len(devices) > 0,
            'device_count': len(devices),
            'devices': devices,
            'primary_device': self.get_primary_relaykeys_device(),
            'all_ports': self.scan_ports()
        }
    
    def print_hardware_status(self):
        """Print a nice hardware status report"""
        info = self.get_hardware_info()
        
        print("🔍 RelayKeys Hardware Detection Report")
        print("=" * 50)
        
        if info['hardware_connected']:
            print(f"✅ Hardware Connected: {info['device_count']} device(s) found")
            print(f"🎯 Primary Device: {info['primary_device']}")
            
            print("\n📋 Detected RelayKeys Devices:")
            for i, device in enumerate(info['devices'], 1):
                print(f"  {i}. {device['device']}")
                print(f"     Type: {self.RELAYKEYS_IDENTIFIERS.get(device['relaykeys_type'], {}).get('name', 'Unknown')}")
                print(f"     Description: {device['description']}")
                if device['vid']:
                    print(f"     VID:PID: {hex(device['vid'])}:{hex(device['pid']) if device['pid'] else 'None'}")
        else:
            print("❌ No RelayKeys Hardware Detected")
            
        print(f"\n📊 Total COM Ports: {len(info['all_ports'])}")
        
        if not info['hardware_connected'] and info['all_ports']:
            print("\n💡 Available COM Ports:")
            for port in info['all_ports'][:5]:  # Show first 5
                print(f"  - {port['device']}: {port['description']}")
            if len(info['all_ports']) > 5:
                print(f"  ... and {len(info['all_ports']) - 5} more")


def detect_hardware() -> bool:
    """Simple function to detect if hardware is connected"""
    detector = HardwareDetector()
    return detector.is_hardware_connected()


def get_hardware_device() -> Optional[str]:
    """Get the primary hardware device port"""
    detector = HardwareDetector()
    return detector.get_primary_relaykeys_device()


if __name__ == "__main__":
    # Run hardware detection when called directly
    detector = HardwareDetector()
    detector.print_hardware_status()
    
    # Exit with appropriate code
    import sys
    sys.exit(0 if detector.is_hardware_connected() else 1)
