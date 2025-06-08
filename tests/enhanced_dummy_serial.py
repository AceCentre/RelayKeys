#!/usr/bin/env python3
"""
Enhanced DummySerial for comprehensive synthetic testing
Simulates realistic RelayKeys hardware behavior
"""

import time
import threading
import queue
import random
from typing import Dict, List, Optional, Any


class EnhancedDummySerial:
    """Advanced dummy serial that simulates realistic RelayKeys hardware"""
    
    def __init__(self, devpath, baud, **kwargs):
        self.devpath = devpath
        self.baud = baud
        self.is_open = True
        self.timeout = kwargs.get('timeout', 1)
        
        # Command history and response queue
        self.command_history = []
        self.response_queue = queue.Queue()
        
        # Simulated device state
        self.device_state = {
            'connected': True,
            'device_name': 'RelayKeys-Synthetic-Test',
            'device_list': ['TestDevice1', 'TestDevice2', 'SyntheticDevice'],
            'current_device': 'TestDevice1',
            'mode': 'BLE_HID',
            'battery': 85,
            'version': '2.1.0',
            'firmware': 'SyntheticFW-v1.0',
            'pairing_mode': False,
            'last_keypress': None,
            'mouse_position': [0, 0],
            'connection_quality': 'Excellent',
            'error_count': 0,
            'uptime': 0
        }
        
        # Simulate realistic timing
        self.command_delay = kwargs.get('command_delay', 0.01)
        self.response_delay = kwargs.get('response_delay', 0.02)
        
        # Error simulation
        self.error_rate = kwargs.get('error_rate', 0.0)  # 0.0 = no errors, 1.0 = always error
        self.simulate_timeouts = kwargs.get('simulate_timeouts', False)
        
        # Start background processes
        self._start_background_tasks()
        
        print(f"EnhancedDummySerial initialized on {devpath} at {baud} baud")
    
    def _start_background_tasks(self):
        """Start background tasks to simulate device behavior"""
        self.background_thread = threading.Thread(target=self._background_worker, daemon=True)
        self.background_thread.start()
    
    def _background_worker(self):
        """Background worker to simulate device state changes"""
        while self.is_open:
            time.sleep(1)
            self.device_state['uptime'] += 1
            
            # Simulate battery drain
            if random.random() < 0.1:  # 10% chance per second
                self.device_state['battery'] = max(0, self.device_state['battery'] - 1)
            
            # Simulate connection quality changes
            if random.random() < 0.05:  # 5% chance per second
                qualities = ['Excellent', 'Good', 'Fair', 'Poor']
                self.device_state['connection_quality'] = random.choice(qualities)
    
    def __enter__(self):
        return self
    
    def __exit__(self, a, b, c):
        self.close()
    
    def close(self):
        """Close the serial connection"""
        self.is_open = False
        self.device_state['connected'] = False
    
    def flushInput(self):
        """Flush input buffer"""
        while not self.response_queue.empty():
            try:
                self.response_queue.get_nowait()
            except queue.Empty:
                break
    
    def flushOutput(self):
        """Flush output buffer"""
        pass
    
    def write(self, data):
        """Write data to the device"""
        if not self.is_open:
            raise Exception("Serial port not open")
        
        # Simulate command delay
        time.sleep(self.command_delay)
        
        # Process the command
        command = data.decode('utf-8').strip() if isinstance(data, bytes) else str(data).strip()
        self.command_history.append(command)
        print(f"EnhancedDummy TX: {command}")
        
        # Simulate errors
        if random.random() < self.error_rate:
            self._queue_response(b"ERROR: Simulated error\n")
            self.device_state['error_count'] += 1
            return
        
        # Generate response
        response = self._generate_response(command)
        if response:
            self._queue_response(response)
    
    def _queue_response(self, response):
        """Queue a response with realistic delay"""
        def delayed_response():
            time.sleep(self.response_delay)
            self.response_queue.put(response)
        
        threading.Thread(target=delayed_response, daemon=True).start()
    
    def _generate_response(self, command):
        """Generate realistic responses based on AT commands"""
        cmd = command.upper().replace('\r', '').replace('\n', '')
        
        # Basic AT commands
        if cmd == 'AT':
            return b"OK\n"
        elif cmd == 'ATE0':
            return b"OK\n"
        elif cmd == 'ATZ':
            return b"RelayKeys Reset\nOK\n"
        
        # BLE HID commands
        elif cmd.startswith('AT+BLEHIDEN'):
            value = cmd.split('=')[1] if '=' in cmd else '1'
            self.device_state['mode'] = 'BLE_HID' if value == '1' else 'UART'
            return b"OK\n"
        
        elif cmd.startswith('AT+BLEKEYBOARDCODE'):
            # Extract keycode
            if '=' in cmd:
                keycode = cmd.split('=')[1]
                self.device_state['last_keypress'] = keycode
                return b"OK\n"
            return b"ERROR: Invalid keycode\n"
        
        elif cmd.startswith('AT+BLEHIDMOUSEMOVE'):
            # Extract mouse movement
            if '=' in cmd:
                coords = cmd.split('=')[1].split(',')
                if len(coords) >= 2:
                    try:
                        dx, dy = int(coords[0]), int(coords[1])
                        self.device_state['mouse_position'][0] += dx
                        self.device_state['mouse_position'][1] += dy
                        return b"OK\n"
                    except ValueError:
                        return b"ERROR: Invalid coordinates\n"
            return b"ERROR: Invalid mouse command\n"
        
        elif cmd.startswith('AT+BLEHIDMOUSEBUTTON'):
            return b"OK\n"
        
        # Device management
        elif cmd == 'AT+PRINTDEVLIST':
            devices = '\n'.join(self.device_state['device_list'])
            return f"{devices}\nOK\n".encode()
        
        elif cmd.startswith('AT+ADDDEVICE'):
            new_device = f"NewDevice{len(self.device_state['device_list']) + 1}"
            self.device_state['device_list'].append(new_device)
            return f"Device added: {new_device}\nOK\n".encode()
        
        elif cmd.startswith('AT+REMOVEDEVICE'):
            if '=' in cmd:
                device_name = cmd.split('=')[1].strip('"')
                if device_name in self.device_state['device_list']:
                    self.device_state['device_list'].remove(device_name)
                    return f"Device removed: {device_name}\nOK\n".encode()
                else:
                    return f"ERROR: Device not found: {device_name}\n".encode()
            return b"ERROR: No device specified\n"
        
        elif cmd == 'AT+CLEARDEVLIST':
            self.device_state['device_list'] = []
            return b"Device list cleared\nOK\n"
        
        # Status and info commands
        elif cmd == 'AT+BLECURRENTDEVICENAME' or cmd == 'AT+DEVNAME':
            return f"{self.device_state['current_device']}\nOK\n".encode()
        
        elif cmd == 'AT+VERSION':
            return f"Version: {self.device_state['version']}\nOK\n".encode()
        
        elif cmd == 'AT+FIRMWARE':
            return f"Firmware: {self.device_state['firmware']}\nOK\n".encode()
        
        elif cmd == 'AT+BATTERY':
            return f"Battery: {self.device_state['battery']}%\nOK\n".encode()
        
        elif cmd == 'AT+STATUS':
            status = f"""Device Status:
Name: {self.device_state['device_name']}
Mode: {self.device_state['mode']}
Battery: {self.device_state['battery']}%
Connection: {self.device_state['connection_quality']}
Uptime: {self.device_state['uptime']}s
Errors: {self.device_state['error_count']}
OK"""
            return status.encode()
        
        elif cmd == 'AT+UPTIME':
            return f"Uptime: {self.device_state['uptime']} seconds\nOK\n".encode()
        
        # Mode and configuration
        elif cmd == 'AT+SWITCHMODE':
            old_mode = self.device_state['mode']
            new_mode = 'UART' if old_mode == 'BLE_HID' else 'BLE_HID'
            self.device_state['mode'] = new_mode
            return f"Mode switched from {old_mode} to {new_mode}\nOK\n".encode()
        
        elif cmd.startswith('AT+SETDEVICENAME'):
            if '=' in cmd:
                new_name = cmd.split('=')[1].strip('"')
                self.device_state['device_name'] = new_name
                return f"Device name set to: {new_name}\nOK\n".encode()
            return b"ERROR: No name specified\n"
        
        # Pairing commands
        elif cmd == 'AT+STARTPAIRING':
            self.device_state['pairing_mode'] = True
            return b"Pairing mode started\nOK\n"
        
        elif cmd == 'AT+STOPPAIRING':
            self.device_state['pairing_mode'] = False
            return b"Pairing mode stopped\nOK\n"
        
        # Test commands
        elif cmd == 'AT+TEST':
            return b"Test successful\nOK\n"
        
        elif cmd.startswith('AT+ECHO'):
            if '=' in cmd:
                echo_text = cmd.split('=')[1]
                return f"ECHO: {echo_text}\nOK\n".encode()
            return b"ECHO: \nOK\n"
        
        # Error simulation commands
        elif cmd == 'AT+SIMULATEERROR':
            return b"ERROR: Simulated error condition\n"
        
        elif cmd == 'AT+SIMULATEDISCONNECT':
            self.device_state['connected'] = False
            return b"Device disconnected\nERROR\n"
        
        # Unknown command
        else:
            return f"ERROR: Unknown command: {cmd}\n".encode()
    
    def readline(self):
        """Read a line from the device"""
        if not self.is_open:
            raise Exception("Serial port not open")
        
        try:
            # Wait for response with timeout
            response = self.response_queue.get(timeout=self.timeout)
            print(f"EnhancedDummy RX: {response}")
            return response
        except queue.Empty:
            if self.simulate_timeouts:
                raise Exception("Read timeout")
            return b"OK\n"  # Default response
    
    def read_all(self):
        """Read all available data"""
        if not self.is_open:
            raise Exception("Serial port not open")
        
        all_data = b""
        while not self.response_queue.empty():
            try:
                data = self.response_queue.get_nowait()
                all_data += data
            except queue.Empty:
                break
        
        if not all_data:
            # Default device info
            info = f"""RelayKeys Synthetic Test Device
Device: {self.device_state['device_name']}
Mode: {self.device_state['mode']}
Battery: {self.device_state['battery']}%
Version: {self.device_state['version']}
Connection: {self.device_state['connection_quality']}
Status: {'Connected' if self.device_state['connected'] else 'Disconnected'}
Uptime: {self.device_state['uptime']}s
""".encode()
            return info
        
        return all_data
    
    # Testing utilities
    def get_command_history(self):
        """Get history of commands sent (for testing)"""
        return self.command_history.copy()
    
    def get_device_state(self):
        """Get current device state (for testing)"""
        return self.device_state.copy()
    
    def set_device_state(self, **kwargs):
        """Update device state (for testing scenarios)"""
        self.device_state.update(kwargs)
    
    def simulate_disconnect(self):
        """Simulate device disconnection"""
        self.device_state['connected'] = False
        self.is_open = False
    
    def simulate_low_battery(self, level=10):
        """Simulate low battery condition"""
        self.device_state['battery'] = level
    
    def simulate_error_condition(self):
        """Simulate various error conditions"""
        self.error_rate = 0.5  # 50% error rate
        self.device_state['connection_quality'] = 'Poor'
    
    def reset_to_normal(self):
        """Reset to normal operation"""
        self.error_rate = 0.0
        self.device_state['connected'] = True
        self.device_state['connection_quality'] = 'Excellent'
        self.is_open = True
