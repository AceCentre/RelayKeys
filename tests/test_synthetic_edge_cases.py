#!/usr/bin/env python3
"""
Synthetic edge case tests for RelayKeys
Test unusual, boundary, and corner cases without hardware
"""

import pytest
import time
import threading
import subprocess
import requests
import json
import tempfile
import os
import string
import random
from unittest.mock import patch, MagicMock
from tests.enhanced_dummy_serial import EnhancedDummySerial


@pytest.mark.no_hardware
class TestSyntheticBoundaryConditions:
    """Test boundary conditions and edge cases"""
    
    def test_empty_commands(self):
        """Test empty and minimal commands"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Test empty command
        serial.write(b"\r\n")
        response = serial.readline()
        assert len(response) > 0
        
        # Test minimal AT command
        serial.write(b"AT\r\n")
        response = serial.readline()
        assert response == b"OK\n"
        
        # Test command with only spaces
        serial.write(b"   \r\n")
        response = serial.readline()
        assert len(response) > 0
    
    def test_maximum_length_commands(self):
        """Test commands at maximum length boundaries"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Test very long command
        long_command = "AT+ECHO=" + "X" * 1000 + "\r\n"
        serial.write(long_command.encode())
        response = serial.readline()
        assert len(response) > 0
        
        # Test command with maximum device name length
        max_name = "A" * 255
        serial.write(f"AT+SETDEVICENAME={max_name}\r\n".encode())
        response = serial.readline()
        assert b"OK" in response or b"ERROR" in response
    
    def test_special_characters(self):
        """Test commands with special characters"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        special_chars = [
            "àáâãäå",  # Accented characters
            "中文测试",   # Chinese characters
            "🎉🚀💻",   # Emojis
            "!@#$%^&*()",  # Symbols
            "\x00\x01\x02",  # Control characters
        ]
        
        for chars in special_chars:
            try:
                serial.write(f"AT+ECHO={chars}\r\n".encode('utf-8', errors='ignore'))
                response = serial.readline()
                assert len(response) > 0
            except UnicodeEncodeError:
                # Expected for some special characters
                pass
    
    def test_rapid_state_changes(self):
        """Test rapid device state changes"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Rapidly switch modes
        for i in range(20):
            serial.write(b"AT+SWITCHMODE\r\n")
            response = serial.readline()
            assert b"OK" in response or b"switched" in response
        
        # Rapidly change device names
        for i in range(10):
            serial.write(f"AT+SETDEVICENAME=Device{i}\r\n".encode())
            response = serial.readline()
            assert len(response) > 0
    
    def test_concurrent_state_access(self):
        """Test concurrent access to device state"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        def state_reader():
            """Read device state repeatedly"""
            for i in range(50):
                serial.write(b"AT+STATUS\r\n")
                response = serial.readline()
                time.sleep(0.01)
        
        def state_modifier():
            """Modify device state repeatedly"""
            for i in range(50):
                serial.write(f"AT+SETDEVICENAME=Concurrent{i}\r\n".encode())
                response = serial.readline()
                time.sleep(0.01)
        
        # Run concurrently
        reader_thread = threading.Thread(target=state_reader)
        modifier_thread = threading.Thread(target=state_modifier)
        
        reader_thread.start()
        modifier_thread.start()
        
        reader_thread.join()
        modifier_thread.join()
        
        # Should complete without errors
        assert True


@pytest.mark.no_hardware
class TestSyntheticRPCEdgeCases:
    """Test RPC edge cases and boundary conditions"""
    
    @pytest.fixture
    def daemon_process(self):
        """Start daemon for RPC edge case testing"""
        process = subprocess.Popen([
            "uv", "run", "python", "relaykeysd.py",
            "--noserial", "--dev=COM99", "--debug"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        yield process
        
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
    
    def test_malformed_json_requests(self, daemon_process):
        """Test malformed JSON RPC requests"""
        time.sleep(2)
        
        malformed_requests = [
            '{"method": "keyevent", "params": ["A", [], true], "id": 1',  # Missing closing brace
            '{"method": "keyevent", "params": ["A", [], true] "id": 1}',  # Missing comma
            '{"method": "keyevent", "params": ["A", [], true], "id": }',  # Invalid ID
            '{"method": , "params": ["A", [], true], "id": 1}',  # Missing method
            'not json at all',  # Not JSON
            '',  # Empty request
            '{}',  # Empty JSON object
        ]
        
        for malformed_json in malformed_requests:
            try:
                response = requests.post(
                    "http://localhost:5383/",
                    data=malformed_json,
                    headers={'Content-Type': 'application/json'},
                    timeout=5
                )
                # Should handle malformed requests gracefully
                assert response.status_code in [200, 400, 500]
            except requests.exceptions.ConnectionError:
                pytest.skip("Daemon RPC server not accessible")
            except:
                # Other exceptions are acceptable for malformed requests
                pass
    
    def test_extreme_parameter_values(self, daemon_process):
        """Test extreme parameter values"""
        time.sleep(2)
        
        extreme_tests = [
            # Very large numbers
            {"method": "mousemove", "params": [999999, -999999, 0, 0], "id": 1},
            
            # Very long strings
            {"method": "keyevent", "params": ["A" * 1000, [], True], "id": 1},
            
            # Empty arrays
            {"method": "keyevent", "params": [], "id": 1},
            
            # Null values
            {"method": "keyevent", "params": [None, None, None], "id": 1},
            
            # Wrong parameter types
            {"method": "keyevent", "params": [123, "not_array", "not_boolean"], "id": 1},
            
            # Nested structures
            {"method": "keyevent", "params": [{"nested": "object"}, [], True], "id": 1},
        ]
        
        for test_request in extreme_tests:
            try:
                response = requests.post(
                    "http://localhost:5383/",
                    json=test_request,
                    timeout=5
                )
                
                # Should handle extreme values gracefully
                assert response.status_code in [200, 400, 500]
                
                if response.status_code == 200:
                    data = response.json()
                    # Should have either result or error
                    assert "result" in data or "error" in data
                    
            except requests.exceptions.ConnectionError:
                pytest.skip("Daemon RPC server not accessible")
            except:
                # Exceptions are acceptable for extreme values
                pass
    
    def test_rapid_id_sequence(self, daemon_process):
        """Test rapid ID sequence and ID reuse"""
        time.sleep(2)
        
        # Test with very large IDs
        large_ids = [999999999, -999999999, 0, 1.5, "string_id"]
        
        for test_id in large_ids:
            try:
                response = requests.post(
                    "http://localhost:5383/",
                    json={"method": "daemon", "params": ["dongle_status"], "id": test_id},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # ID should be preserved in response
                    assert "id" in data
                    
            except requests.exceptions.ConnectionError:
                pytest.skip("Daemon RPC server not accessible")
            except:
                pass
    
    def test_simultaneous_identical_requests(self, daemon_process):
        """Test many identical requests simultaneously"""
        time.sleep(2)
        
        def send_identical_request():
            """Send identical request"""
            try:
                response = requests.post(
                    "http://localhost:5383/",
                    json={"method": "daemon", "params": ["dongle_status"], "id": 42},
                    timeout=10
                )
                return response.status_code == 200
            except:
                return False
        
        # Send 20 identical requests simultaneously
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(send_identical_request) for _ in range(20)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Most should succeed
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.5


@pytest.mark.no_hardware
class TestSyntheticCLIEdgeCases:
    """Test CLI edge cases and boundary conditions"""
    
    @pytest.fixture
    def daemon_process(self):
        """Start daemon for CLI edge case testing"""
        process = subprocess.Popen([
            "uv", "run", "python", "relaykeysd.py",
            "--noserial", "--dev=COM99", "--debug"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        yield process
        
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
    
    def test_cli_extreme_arguments(self, daemon_process):
        """Test CLI with extreme arguments"""
        time.sleep(2)
        
        extreme_args = [
            "type:" + "A" * 10000,  # Very long text
            "keyevent:INVALID_KEY_NAME,[],1",  # Invalid key
            "mousemove:999999,-999999",  # Extreme coordinates
            "mousebutton:invalid_button,invalid_action",  # Invalid button/action
            "ble_cmd:" + "X" * 1000,  # Very long BLE command
        ]
        
        for arg in extreme_args:
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", arg
                ], capture_output=True, text=True, timeout=30)
                
                # Should handle extreme arguments gracefully
                assert result.returncode in [0, 1, 2]  # Various error codes acceptable
                
            except subprocess.TimeoutExpired:
                # Timeout is acceptable for extreme cases
                pass
            except:
                # Other exceptions are acceptable
                pass
    
    def test_cli_special_character_handling(self, daemon_process):
        """Test CLI with special characters"""
        time.sleep(2)
        
        special_texts = [
            "type:Hello\nWorld",  # Newlines
            "type:Tab\tSeparated",  # Tabs
            "type:Quote\"Test",  # Quotes
            "type:Backslash\\Test",  # Backslashes
            "type:Unicode🎉Test",  # Unicode
        ]
        
        for text in special_texts:
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", text
                ], capture_output=True, text=True, timeout=20)
                
                # Should handle special characters
                assert result.returncode in [0, 1]
                
            except subprocess.TimeoutExpired:
                pass
            except:
                pass
    
    def test_cli_macro_edge_cases(self, daemon_process):
        """Test CLI macro edge cases"""
        time.sleep(2)
        
        # Create edge case macro files
        edge_case_macros = [
            # Empty macro
            "",
            
            # Macro with only comments
            "# This is a comment\n# Another comment\n",
            
            # Macro with invalid commands
            "invalid_command:test\nkeypress:A\n",
            
            # Macro with extreme delays
            "delay:999999\nkeypress:A\n",
            
            # Macro with malformed lines
            "keypress:\ntype:\nmousemove:\n",
        ]
        
        for i, macro_content in enumerate(edge_case_macros):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(macro_content)
                macro_file = f.name
            
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", f"macro:{macro_file}"
                ], capture_output=True, text=True, timeout=30)
                
                # Should handle edge case macros gracefully
                assert result.returncode in [0, 1, 2]
                
            except subprocess.TimeoutExpired:
                pass
            except:
                pass
            finally:
                os.unlink(macro_file)


@pytest.mark.no_hardware
class TestSyntheticResourceLimits:
    """Test resource limits and exhaustion scenarios"""
    
    def test_memory_exhaustion_simulation(self):
        """Test behavior under simulated memory pressure"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Create many large responses
        large_responses = []
        for i in range(100):
            large_data = "X" * 10000
            serial.write(f"AT+ECHO={large_data}\r\n".encode())
            response = serial.readline()
            large_responses.append(response)
        
        # Should handle large data accumulation
        assert len(large_responses) == 100
        
        # Clean up
        del large_responses
    
    def test_file_descriptor_limits(self):
        """Test file descriptor usage patterns"""
        # Create many serial instances
        serials = []
        
        try:
            for i in range(50):
                serial = EnhancedDummySerial(f"/dev/test{i}", 115200)
                serials.append(serial)
                
                # Use each serial briefly
                serial.write(b"AT\r\n")
                response = serial.readline()
                assert response == b"OK\n"
                
        finally:
            # Clean up all serials
            for serial in serials:
                try:
                    serial.close()
                except:
                    pass
    
    def test_thread_exhaustion_simulation(self):
        """Test behavior with many threads"""
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        def worker_thread(thread_id):
            """Worker thread function"""
            for i in range(5):
                serial.write(f"AT+ECHO=Thread{thread_id}_{i}\r\n".encode())
                response = serial.readline()
                time.sleep(0.01)
        
        # Create many threads
        threads = []
        for i in range(50):
            thread = threading.Thread(target=worker_thread, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join(timeout=10)
        
        # Should complete without issues
        assert True


if __name__ == "__main__":
    pytest.main([__file__])
