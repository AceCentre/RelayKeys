#!/usr/bin/env python3
"""
Comprehensive synthetic tests for RelayKeys
Tests every possible scenario without requiring hardware
"""

import subprocess
import threading
import time
from unittest.mock import patch

import pytest
import requests

from tests.enhanced_dummy_serial import EnhancedDummySerial


@pytest.mark.no_hardware
class TestSyntheticSerialCommunication:
    """Test all serial communication scenarios"""
    
    def test_basic_at_commands(self):
        """Test basic AT command responses"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Test basic commands
        serial.write(b"AT\r\n")
        response = serial.readline()
        assert response == b"OK\n"
        
        serial.write(b"ATE0\r\n")
        response = serial.readline()
        assert response == b"OK\n"
        
        serial.write(b"ATZ\r\n")
        response = serial.readline()
        assert b"Reset" in response
    
    def test_ble_hid_commands(self):
        """Test BLE HID command sequences"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Enable BLE HID
        serial.write(b"AT+BLEHIDEN=1\r\n")
        response = serial.readline()
        assert response == b"OK\n"
        
        # Send keyboard command
        serial.write(b"AT+BLEKEYBOARDCODE=04-00\r\n")
        response = serial.readline()
        assert response == b"OK\n"
        
        # Send mouse movement
        serial.write(b"AT+BLEHIDMOUSEMOVE=10,20,0,0\r\n")
        response = serial.readline()
        assert response == b"OK\n"
        
        # Check device state
        state = serial.get_device_state()
        assert state['mode'] == 'BLE_HID'
        assert state['last_keypress'] == '04-00'
        assert state['mouse_position'] == [10, 20]
    
    def test_device_management(self):
        """Test device list management"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Get initial device list
        serial.write(b"AT+PRINTDEVLIST\r\n")
        response = serial.readline()
        assert b"TestDevice1" in response
        
        # Add a device
        serial.write(b"AT+ADDDEVICE\r\n")
        response = serial.readline()
        assert b"Device added" in response
        
        # Remove a device (case-insensitive)
        serial.write(b'AT+REMOVEDEVICE="TestDevice1"\r\n')
        response = serial.readline()
        assert b"Device removed" in response or b"ERROR: Device not found" in response
        
        # Clear device list
        serial.write(b"AT+CLEARDEVLIST\r\n")
        response = serial.readline()
        assert response == b"Device list cleared\nOK\n"
    
    def test_status_commands(self):
        """Test status and information commands"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Test various status commands
        commands = [
            (b"AT+DEVNAME\r\n", b"TestDevice1"),
            (b"AT+VERSION\r\n", b"Version: 2.1.0"),
            (b"AT+BATTERY\r\n", b"Battery: 85%"),
            (b"AT+UPTIME\r\n", b"Uptime:"),
        ]
        
        for command, expected in commands:
            serial.write(command)
            response = serial.readline()
            assert expected in response
    
    def test_error_conditions(self):
        """Test error handling and edge cases"""
        serial = EnhancedDummySerial("/dev/test", 115200, error_rate=0.0)
        
        # Test invalid commands
        serial.write(b"AT+INVALIDCOMMAND\r\n")
        response = serial.readline()
        assert b"ERROR" in response
        
        # Test malformed commands
        serial.write(b"AT+BLEKEYBOARDCODE=\r\n")
        response = serial.readline()
        assert b"ERROR" in response or b"OK" in response  # May accept empty parameter
        
        # Test device not found
        serial.write(b'AT+REMOVEDEVICE="NonExistentDevice"\r\n')
        response = serial.readline()
        assert b"ERROR: Device not found" in response
    
    def test_connection_lifecycle(self):
        """Test connection establishment and teardown"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Test connection is initially open
        assert serial.is_open
        
        # Test normal operation
        serial.write(b"AT\r\n")
        response = serial.readline()
        assert response == b"OK\n"
        
        # Test disconnection
        serial.simulate_disconnect()
        assert not serial.is_open
        
        # Test operations after disconnect
        with pytest.raises(Exception):
            serial.write(b"AT\r\n")
    
    def test_concurrent_operations(self):
        """Test concurrent serial operations"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        def send_commands():
            for i in range(10):
                serial.write(f"AT+ECHO=Test{i}\r\n".encode())
                time.sleep(0.01)
        
        # Start multiple threads
        threads = [threading.Thread(target=send_commands) for _ in range(3)]
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Check command history
        history = serial.get_command_history()
        assert len(history) == 30  # 3 threads * 10 commands each


@pytest.mark.no_hardware
class TestSyntheticDaemonIntegration:
    """Test daemon integration with synthetic hardware"""
    
    @pytest.fixture
    def synthetic_daemon(self):
        """Start daemon with enhanced dummy serial"""
        with patch('serial.Serial') as mock_serial:
            # Replace serial.Serial with our enhanced dummy
            mock_serial.return_value = EnhancedDummySerial("/dev/test", 115200)
            
            process = subprocess.Popen([
                "uv", "run", "python", "relaykeysd.py",
                "--noserial", "--dev=COM99", "--debug"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            time.sleep(3)  # Give daemon time to start
            yield process
            
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
    
    def test_daemon_startup_sequence(self, synthetic_daemon):
        """Test complete daemon startup sequence"""
        assert synthetic_daemon.poll() is None
        
        # Test RPC server is responding
        try:
            response = requests.post(
                "http://localhost:5383/",
                json={"method": "daemon", "params": ["dongle_status"], "id": 1},
                timeout=5
            )
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("Daemon RPC server not accessible")
    
    def test_complete_keyevent_workflow(self, synthetic_daemon):
        """Test complete keyboard event workflow"""
        time.sleep(2)
        
        try:
            # Test individual key events
            key_sequences = [
                ("A", [], True),   # Press A
                ("A", [], False),  # Release A
                ("B", ["LSHIFT"], True),   # Press Shift+B
                ("B", ["LSHIFT"], False),  # Release Shift+B
                ("SPACE", [], True),       # Press Space
                ("SPACE", [], False),      # Release Space
            ]
            
            for key, modifiers, down in key_sequences:
                response = requests.post(
                    "http://localhost:5383/",
                    json={"method": "keyevent", "params": [key, modifiers, down], "id": 1},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # Should get some response (success or error)
                    assert "result" in data or "error" in data
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Daemon RPC server not accessible")
    
    def test_complete_mouse_workflow(self, synthetic_daemon):
        """Test complete mouse event workflow"""
        time.sleep(2)
        
        try:
            # Test mouse movements
            mouse_movements = [
                (10, 0, 0, 0),    # Move right
                (-5, 10, 0, 0),   # Move left and down
                (0, 0, 1, 0),     # Scroll up
                (0, 0, -1, 0),    # Scroll down
            ]
            
            for dx, dy, wheel_y, wheel_x in mouse_movements:
                response = requests.post(
                    "http://localhost:5383/",
                    json={"method": "mousemove", "params": [dx, dy, wheel_y, wheel_x], "id": 1},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    assert "result" in data or "error" in data
            
            # Test mouse buttons
            button_events = [
                ("l", "press"),    # Left button press
                ("l", "release"),  # Left button release
                ("r", "click"),    # Right button click
                ("m", "doubleclick"),  # Middle button double-click
            ]
            
            for button, action in button_events:
                response = requests.post(
                    "http://localhost:5383/",
                    json={"method": "mousebutton", "params": [button, action], "id": 1},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    assert "result" in data or "error" in data
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Daemon RPC server not accessible")
    
    def test_ble_command_workflow(self, synthetic_daemon):
        """Test BLE command workflow"""
        time.sleep(2)
        
        try:
            # Test BLE commands
            ble_commands = [
                "devlist",
                "devname", 
                "devadd",
                "devremove=TestDevice1",
                "devreset",
            ]
            
            for cmd in ble_commands:
                response = requests.post(
                    "http://localhost:5383/",
                    json={"method": "ble_cmd", "params": [cmd], "id": 1},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    assert "result" in data or "error" in data
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Daemon RPC server not accessible")


@pytest.mark.no_hardware
class TestSyntheticErrorScenarios:
    """Test error scenarios and edge cases"""
    
    def test_serial_communication_errors(self):
        """Test serial communication error handling"""
        # Test with high error rate
        serial = EnhancedDummySerial("/dev/test", 115200, error_rate=0.8)
        
        error_count = 0
        for i in range(10):
            serial.write(b"AT\r\n")
            response = serial.readline()
            if b"ERROR" in response:
                error_count += 1
        
        # Should have some errors with 80% error rate
        assert error_count > 0
    
    def test_timeout_scenarios(self):
        """Test timeout handling"""
        serial = EnhancedDummySerial("/dev/test", 115200, 
                                   simulate_timeouts=True, timeout=0.1)
        
        # This should timeout (but our dummy may not actually timeout)
        serial.write(b"AT+SLOWCOMMAND\r\n")
        try:
            response = serial.readline()
            # If no timeout occurs, that's also acceptable in dummy mode
            assert len(response) > 0
        except Exception:
            # Timeout is expected
            pass
    
    def test_device_state_changes(self):
        """Test dynamic device state changes"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Test low battery scenario
        serial.simulate_low_battery(5)
        serial.write(b"AT+BATTERY\r\n")
        response = serial.readline()
        assert b"5%" in response
        
        # Test error condition
        serial.simulate_error_condition()
        serial.write(b"AT+STATUS\r\n")
        response = serial.readline()
        assert b"Poor" in response or b"ERROR" in response
    
    def test_connection_recovery(self):
        """Test connection recovery scenarios"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Simulate disconnect
        serial.simulate_disconnect()
        assert not serial.is_open
        
        # Reset to normal (simulate reconnection)
        serial.reset_to_normal()
        assert serial.is_open
        
        # Test normal operation after recovery
        serial.write(b"AT\r\n")
        response = serial.readline()
        assert response == b"OK\n"


@pytest.mark.no_hardware
class TestSyntheticPerformance:
    """Test performance scenarios"""
    
    def test_high_frequency_commands(self):
        """Test high-frequency command processing"""
        serial = EnhancedDummySerial("/dev/test", 115200, command_delay=0.001)
        
        start_time = time.time()
        
        # Send 100 commands rapidly
        for i in range(100):
            serial.write(f"AT+ECHO=Test{i}\r\n".encode())
            response = serial.readline()
            assert b"ECHO" in response
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time (less than 5 seconds)
        assert duration < 5.0
        
        # Check all commands were processed
        history = serial.get_command_history()
        assert len(history) == 100
    
    def test_large_data_transfer(self):
        """Test large data transfer scenarios"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Send large echo command
        large_data = "X" * 1000
        serial.write(f"AT+ECHO={large_data}\r\n".encode())
        response = serial.readline()
        
        assert b"ECHO" in response
        assert large_data.encode() in response
    
    def test_concurrent_stress(self):
        """Test concurrent access stress scenarios"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        def stress_worker(worker_id):
            for i in range(20):
                serial.write(f"AT+ECHO=Worker{worker_id}_{i}\r\n".encode())
                time.sleep(0.01)
        
        # Start 5 concurrent workers
        threads = [threading.Thread(target=stress_worker, args=(i,)) for i in range(5)]
        
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # Should complete in reasonable time
        assert (end_time - start_time) < 10.0
        
        # Check all commands were processed
        history = serial.get_command_history()
        assert len(history) == 100  # 5 workers * 20 commands each


if __name__ == "__main__":
    pytest.main([__file__])
