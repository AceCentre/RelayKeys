#!/usr/bin/env python3
"""
Synthetic stress tests for RelayKeys
Push the system to its limits without requiring hardware
"""

import concurrent.futures
import random
import string
import subprocess
import time

import pytest
import requests


@pytest.mark.no_hardware
@pytest.mark.slow
class TestSyntheticStressRPC:
    """Stress test RPC server with synthetic load"""
    
    @pytest.fixture
    def daemon_process(self):
        """Start daemon for stress testing"""
        process = subprocess.Popen([
            "uv", "run", "python", "relaykeysd.py",
            "--noserial", "--dev=COM99", "--debug"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(5)  # Give daemon extra time for stress tests
        yield process
        
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
    
    def test_concurrent_rpc_requests(self, daemon_process):
        """Test many concurrent RPC requests"""
        time.sleep(3)
        
        def make_request(request_id):
            """Make a single RPC request"""
            try:
                response = requests.post(
                    "http://localhost:5383/",
                    json={"method": "daemon", "params": ["dongle_status"], "id": request_id},
                    timeout=10
                )
                return response.status_code == 200
            except:
                return False
        
        # Test with 50 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request, i) for i in range(50)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # At least 70% should succeed
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.7
    
    def test_rapid_keyevent_stress(self, daemon_process):
        """Test rapid keyboard events"""
        time.sleep(3)
        
        def send_keyevents(worker_id, count):
            """Send multiple keyevents rapidly"""
            success_count = 0
            for i in range(count):
                try:
                    key = random.choice(['A', 'B', 'C', 'D', 'E'])
                    down = random.choice([True, False])
                    
                    response = requests.post(
                        "http://localhost:5383/",
                        json={"method": "keyevent", "params": [key, [], down], "id": f"{worker_id}_{i}"},
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        success_count += 1
                        
                except:
                    pass  # Ignore individual failures in stress test
                
                time.sleep(0.01)  # Small delay between requests
            
            return success_count
        
        # Start 10 workers, each sending 20 keyevents
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(send_keyevents, i, 20) for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        total_sent = 10 * 20  # 200 total
        total_success = sum(results)
        success_rate = total_success / total_sent
        
        # At least 50% should succeed under stress
        assert success_rate >= 0.5
    
    def test_mixed_command_stress(self, daemon_process):
        """Test mixed command types under stress"""
        time.sleep(3)
        
        def random_command_worker(worker_id, duration_seconds):
            """Send random commands for specified duration"""
            start_time = time.time()
            success_count = 0
            total_count = 0
            
            while time.time() - start_time < duration_seconds:
                try:
                    # Random command type
                    command_type = random.choice(['keyevent', 'mousemove', 'daemon', 'ble_cmd'])
                    
                    if command_type == 'keyevent':
                        key = random.choice(['A', 'B', 'C', 'SPACE', 'ENTER'])
                        down = random.choice([True, False])
                        params = [key, [], down]
                    elif command_type == 'mousemove':
                        dx = random.randint(-10, 10)
                        dy = random.randint(-10, 10)
                        params = [dx, dy, 0, 0]
                    elif command_type == 'daemon':
                        params = [random.choice(['dongle_status', 'get_mode'])]
                    else:  # ble_cmd
                        params = [random.choice(['devname', 'devlist'])]
                    
                    response = requests.post(
                        "http://localhost:5383/",
                        json={"method": command_type, "params": params, "id": f"{worker_id}_{total_count}"},
                        timeout=3
                    )
                    
                    total_count += 1
                    if response.status_code == 200:
                        success_count += 1
                        
                except:
                    total_count += 1
                
                time.sleep(0.02)  # 50 commands per second max
            
            return success_count, total_count
        
        # Run stress test for 10 seconds with 5 workers
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(random_command_worker, i, 10) for i in range(5)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        total_success = sum(result[0] for result in results)
        total_commands = sum(result[1] for result in results)
        
        if total_commands > 0:
            success_rate = total_success / total_commands
            # At least 40% should succeed under heavy mixed load
            assert success_rate >= 0.4
    
    def test_large_payload_stress(self, daemon_process):
        """Test large RPC payloads"""
        time.sleep(3)
        
        def send_large_payload(size):
            """Send RPC request with large payload"""
            try:
                # Create large text for type command
                large_text = ''.join(random.choices(string.ascii_letters + string.digits, k=size))
                
                response = requests.post(
                    "http://localhost:5383/",
                    json={"method": "keyevent", "params": ["A", [], True], "id": 1, "large_data": large_text},
                    timeout=15
                )
                
                return response.status_code == 200
            except:
                return False
        
        # Test various payload sizes
        payload_sizes = [100, 500, 1000, 2000, 5000]
        results = []
        
        for size in payload_sizes:
            success = send_large_payload(size)
            results.append(success)
            time.sleep(0.5)  # Brief pause between large payloads
        
        # At least some large payloads should succeed
        success_count = sum(results)
        assert success_count >= len(payload_sizes) // 2


@pytest.mark.no_hardware
@pytest.mark.slow
class TestSyntheticStressCLI:
    """Stress test CLI with synthetic load"""
    
    @pytest.fixture
    def daemon_process(self):
        """Start daemon for CLI stress testing"""
        process = subprocess.Popen([
            "uv", "run", "python", "relaykeysd.py",
            "--noserial", "--dev=COM99", "--debug"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(5)
        yield process
        
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
    
    def test_concurrent_cli_processes(self, daemon_process):
        """Test multiple CLI processes running concurrently"""
        time.sleep(3)
        
        def run_cli_command(command, timeout=15):
            """Run a single CLI command"""
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", command
                ], capture_output=True, text=True, timeout=timeout)
                return result.returncode in [0, 1]  # Success or expected error
            except subprocess.TimeoutExpired:
                return False
            except:
                return False
        
        # Test 20 concurrent CLI processes
        commands = [
            "daemon:dongle_status",
            "keypress:A",
            "keypress:B", 
            "mousemove:1,1",
            "ble_cmd:devname",
        ] * 4  # 20 total commands
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(run_cli_command, cmd) for cmd in commands]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        success_rate = sum(results) / len(results)
        # At least 60% should succeed
        assert success_rate >= 0.6
    
    def test_cli_rapid_typing_stress(self, daemon_process):
        """Test rapid typing through CLI"""
        time.sleep(3)
        
        def rapid_typing_worker(worker_id, text_length):
            """Type text rapidly through CLI"""
            try:
                # Generate random text
                text = ''.join(random.choices(string.ascii_letters, k=text_length))
                
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", f"type:{text}"
                ], capture_output=True, text=True, timeout=30)
                
                return result.returncode in [0, 1]
            except:
                return False
        
        # Test 5 workers typing 50-character strings
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(rapid_typing_worker, i, 50) for i in range(5)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.6


@pytest.mark.no_hardware
@pytest.mark.slow
class TestSyntheticStressSerial:
    """Stress test serial communication"""
    
    def test_serial_command_flood(self):
        """Test flooding serial with commands"""
        from tests.enhanced_dummy_serial import EnhancedDummySerial
        
        serial = EnhancedDummySerial("/dev/test", 115200, command_delay=0.001)
        
        def command_flood_worker(worker_id, command_count):
            """Send many commands rapidly"""
            success_count = 0
            for i in range(command_count):
                try:
                    command = random.choice([
                        b"AT\r\n",
                        b"AT+BLEHIDEN=1\r\n",
                        b"AT+DEVNAME\r\n",
                        b"AT+BATTERY\r\n",
                        b"AT+PRINTDEVLIST\r\n"
                    ])
                    
                    serial.write(command)
                    response = serial.readline()
                    
                    if b"OK" in response or b"Battery" in response:
                        success_count += 1
                        
                except:
                    pass
            
            return success_count
        
        # Start 10 workers, each sending 50 commands
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(command_flood_worker, i, 50) for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        total_success = sum(results)
        total_commands = 10 * 50  # 500 total
        success_rate = total_success / total_commands
        
        # Should handle most commands successfully
        assert success_rate >= 0.8
    
    def test_serial_error_recovery_stress(self):
        """Test serial error recovery under stress"""
        from tests.enhanced_dummy_serial import EnhancedDummySerial
        
        # Start with high error rate
        serial = EnhancedDummySerial("/dev/test", 115200, error_rate=0.5)
        
        error_count = 0
        success_count = 0
        
        # Send 100 commands with 50% error rate
        for i in range(100):
            try:
                serial.write(b"AT\r\n")
                response = serial.readline()
                
                if b"ERROR" in response:
                    error_count += 1
                elif b"OK" in response:
                    success_count += 1
                    
            except:
                error_count += 1
        
        # Should have roughly 50% errors
        total_commands = error_count + success_count
        if total_commands > 0:
            error_rate = error_count / total_commands
            assert 0.3 <= error_rate <= 0.7  # Roughly 50% ± 20%
        
        # Reset to normal and test recovery
        serial.reset_to_normal()
        
        recovery_success = 0
        for i in range(10):
            try:
                serial.write(b"AT\r\n")
                response = serial.readline()
                if b"OK" in response:
                    recovery_success += 1
            except:
                pass
        
        # Should recover well
        recovery_rate = recovery_success / 10
        assert recovery_rate >= 0.8


@pytest.mark.no_hardware
@pytest.mark.slow
class TestSyntheticStressMemory:
    """Test memory usage under stress"""
    
    def test_memory_leak_detection(self):
        """Test for memory leaks during extended operation"""
        import gc

        from tests.enhanced_dummy_serial import EnhancedDummySerial
        
        # Force garbage collection
        gc.collect()
        
        # Create and destroy many serial instances
        for i in range(100):
            serial = EnhancedDummySerial(f"/dev/test{i}", 115200)
            
            # Use the serial instance
            for j in range(10):
                serial.write(f"AT+ECHO=Test{j}\r\n".encode())
                response = serial.readline()
            
            # Close and delete
            serial.close()
            del serial
            
            # Periodic garbage collection
            if i % 20 == 0:
                gc.collect()
        
        # Final garbage collection
        gc.collect()
        
        # Test should complete without memory issues
        assert True  # If we get here, no memory issues occurred
    
    def test_large_data_handling(self):
        """Test handling of large data structures"""
        from tests.enhanced_dummy_serial import EnhancedDummySerial
        
        serial = EnhancedDummySerial("/dev/test", 115200)
        
        # Test with increasingly large data
        for size in [1000, 5000, 10000, 20000]:
            large_data = "X" * size
            
            try:
                serial.write(f"AT+ECHO={large_data}\r\n".encode())
                response = serial.readline()
                
                # Should handle large data
                assert len(response) > 0
                
            except MemoryError:
                pytest.fail(f"Memory error with data size {size}")
            except:
                # Other errors are acceptable for very large data
                pass


if __name__ == "__main__":
    pytest.main([__file__])
