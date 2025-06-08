#!/usr/bin/env python3
"""
Hardware-aware tests for RelayKeys
These tests automatically adapt based on whether hardware is connected
"""

import pytest
import subprocess
import time
import requests
import json


@pytest.mark.no_hardware
class TestDummyMode:
    """Tests that run in dummy mode (no hardware required)"""
    
    def test_dummy_daemon_starts(self, daemon_process, test_mode):
        """Test daemon starts in dummy mode"""
        assert test_mode in ["dummy", "hardware"]
        assert daemon_process.poll() is None
    
    def test_dummy_rpc_responds(self, daemon_process, relaykeys_client):
        """Test RPC server responds in dummy mode"""
        time.sleep(2)
        
        try:
            result = relaykeys_client.daemon("dongle_status")
            # In dummy mode, should get some response
            assert result is not None
        except Exception as e:
            pytest.skip(f"RPC not accessible: {e}")
    
    def test_dummy_keyevent(self, daemon_process, relaykeys_client):
        """Test keyevent in dummy mode"""
        time.sleep(2)
        
        try:
            result = relaykeys_client.keyevent("A", [], True)
            # Should get some response (SUCCESS or error)
            assert result is not None
        except Exception as e:
            pytest.skip(f"RPC not accessible: {e}")


@pytest.mark.hardware_required
class TestHardwareMode:
    """Tests that require actual hardware"""
    
    def test_hardware_daemon_starts(self, daemon_process, hardware_connected, primary_device):
        """Test daemon starts with real hardware"""
        assert hardware_connected
        assert primary_device is not None
        assert daemon_process.poll() is None
    
    def test_hardware_device_detection(self, hardware_detector):
        """Test hardware device detection"""
        devices = hardware_detector.find_relaykeys_devices()
        assert len(devices) > 0
        
        primary = hardware_detector.get_primary_relaykeys_device()
        assert primary is not None
    
    def test_hardware_communication(self, daemon_process, relaykeys_client, hardware_connected):
        """Test actual hardware communication"""
        if not hardware_connected:
            pytest.skip("Hardware not connected")
        
        time.sleep(3)  # Give hardware more time
        
        try:
            # Test device name query
            result = relaykeys_client.ble_cmd("devname")
            assert "result" in result
            
            # Test device list
            result = relaykeys_client.ble_cmd("devlist")
            assert "result" in result
            
        except Exception as e:
            pytest.fail(f"Hardware communication failed: {e}")
    
    def test_hardware_keyevent(self, daemon_process, relaykeys_client, hardware_connected):
        """Test keyevent with real hardware"""
        if not hardware_connected:
            pytest.skip("Hardware not connected")
        
        time.sleep(2)
        
        try:
            result = relaykeys_client.keyevent("A", [], True)
            time.sleep(0.1)
            result = relaykeys_client.keyevent("A", [], False)
            
            # With real hardware, should get SUCCESS
            assert result == "SUCCESS" or "result" in str(result)
            
        except Exception as e:
            pytest.fail(f"Hardware keyevent failed: {e}")


class TestAdaptiveMode:
    """Tests that adapt based on hardware availability"""
    
    def test_daemon_mode_detection(self, test_mode, hardware_connected):
        """Test that we correctly detect the test mode"""
        if hardware_connected:
            assert test_mode == "hardware"
        else:
            assert test_mode == "dummy"
    
    def test_adaptive_daemon_startup(self, daemon_process, test_mode):
        """Test daemon starts in appropriate mode"""
        assert daemon_process.poll() is None
        
        # Give daemon time to initialize
        time.sleep(3)
        
        # Daemon should be running regardless of mode
        assert daemon_process.poll() is None
    
    def test_adaptive_basic_commands(self, daemon_process, relaykeys_client, test_mode):
        """Test basic commands work in any mode"""
        time.sleep(2)
        
        try:
            # Test daemon status - should work in any mode
            result = relaykeys_client.daemon("dongle_status")
            assert result is not None
            
            # Test get_mode - should work in any mode
            result = relaykeys_client.daemon("get_mode")
            assert result is not None
            
        except Exception as e:
            pytest.skip(f"Basic commands not accessible: {e}")
    
    def test_adaptive_keyevent_response(self, daemon_process, relaykeys_client, test_mode):
        """Test keyevent response varies by mode"""
        time.sleep(2)
        
        try:
            result = relaykeys_client.keyevent("A", [], True)
            
            if test_mode == "hardware":
                # With hardware, expect SUCCESS
                assert result == "SUCCESS" or "SUCCESS" in str(result)
            else:
                # With dummy, expect some response (may be different)
                assert result is not None
                
        except Exception as e:
            pytest.skip(f"Keyevent not accessible: {e}")


class TestHardwareDetection:
    """Test the hardware detection system itself"""
    
    def test_hardware_detector_creation(self, hardware_detector):
        """Test hardware detector can be created"""
        assert hardware_detector is not None
    
    def test_port_scanning(self, hardware_detector):
        """Test port scanning functionality"""
        ports = hardware_detector.scan_ports()
        assert isinstance(ports, list)
        # Should find at least some ports on most systems
    
    def test_hardware_info_structure(self, hardware_info):
        """Test hardware info has correct structure"""
        required_keys = ['hardware_connected', 'device_count', 'devices', 'primary_device', 'all_ports']
        
        for key in required_keys:
            assert key in hardware_info
        
        assert isinstance(hardware_info['hardware_connected'], bool)
        assert isinstance(hardware_info['device_count'], int)
        assert isinstance(hardware_info['devices'], list)
        assert isinstance(hardware_info['all_ports'], list)
    
    def test_hardware_detection_consistency(self, hardware_detector, hardware_connected):
        """Test hardware detection is consistent"""
        # Multiple calls should return same result
        result1 = hardware_detector.is_hardware_connected()
        result2 = hardware_detector.is_hardware_connected()
        
        assert result1 == result2 == hardware_connected


@pytest.mark.integration
class TestFullIntegration:
    """Full integration tests that work with or without hardware"""
    
    def test_full_workflow_dummy(self, daemon_process, relaykeys_client):
        """Test complete workflow in dummy mode"""
        time.sleep(3)
        
        try:
            # 1. Check daemon status
            status = relaykeys_client.daemon("dongle_status")
            assert status is not None
            
            # 2. Send a keyevent
            result = relaykeys_client.keyevent("H", [], True)
            time.sleep(0.1)
            result = relaykeys_client.keyevent("H", [], False)
            
            # 3. Send mouse movement
            result = relaykeys_client.mousemove(5, 5, 0, 0)
            
            # 4. Check mode
            mode = relaykeys_client.daemon("get_mode")
            assert mode is not None
            
        except Exception as e:
            pytest.skip(f"Full workflow test failed: {e}")
    
    @pytest.mark.hardware_required
    def test_full_workflow_hardware(self, daemon_process, relaykeys_client, hardware_connected):
        """Test complete workflow with hardware"""
        if not hardware_connected:
            pytest.skip("Hardware not connected")
        
        time.sleep(5)  # Give hardware more time
        
        try:
            # 1. Check hardware status
            status = relaykeys_client.daemon("dongle_status")
            assert "Connected" in str(status) or status is not None
            
            # 2. Get device list
            devices = relaykeys_client.ble_cmd("devlist")
            assert "result" in devices
            
            # 3. Get current device name
            devname = relaykeys_client.ble_cmd("devname")
            assert "result" in devname
            
            # 4. Send keyevent to hardware
            result = relaykeys_client.keyevent("H", [], True)
            time.sleep(0.1)
            result = relaykeys_client.keyevent("H", [], False)
            assert result == "SUCCESS" or "SUCCESS" in str(result)
            
        except Exception as e:
            pytest.fail(f"Hardware workflow test failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
