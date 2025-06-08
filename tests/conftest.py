#!/usr/bin/env python3
"""
Pytest configuration for RelayKeys
Automatically configures tests based on hardware availability
"""

import pytest
import subprocess
import time
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.hardware_detection import HardwareDetector


def pytest_configure(config):
    """Configure pytest based on hardware availability"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "hardware_required: mark test as requiring actual hardware"
    )
    config.addinivalue_line(
        "markers", "no_hardware: mark test as working without hardware"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on hardware availability"""
    detector = HardwareDetector()
    hardware_connected = detector.is_hardware_connected()
    
    # Print hardware status
    print(f"\n🔍 Hardware Detection: {'✅ Connected' if hardware_connected else '❌ Not Connected'}")
    if hardware_connected:
        primary_device = detector.get_primary_relaykeys_device()
        print(f"🎯 Primary Device: {primary_device}")
    
    skip_hardware = pytest.mark.skip(reason="Hardware not connected")
    skip_no_hardware = pytest.mark.skip(reason="Hardware is connected, skipping dummy tests")
    
    for item in items:
        # Skip hardware tests if no hardware
        if "hardware_required" in item.keywords and not hardware_connected:
            item.add_marker(skip_hardware)
        
        # Optionally skip no-hardware tests if hardware is connected
        # (uncomment if you want this behavior)
        # if "no_hardware" in item.keywords and hardware_connected:
        #     item.add_marker(skip_no_hardware)


@pytest.fixture(scope="session")
def hardware_detector():
    """Provide hardware detector for tests"""
    return HardwareDetector()


@pytest.fixture(scope="session")
def hardware_info(hardware_detector):
    """Provide hardware information for tests"""
    return hardware_detector.get_hardware_info()


@pytest.fixture(scope="session")
def hardware_connected(hardware_info):
    """Boolean fixture indicating if hardware is connected"""
    return hardware_info['hardware_connected']


@pytest.fixture(scope="session")
def primary_device(hardware_info):
    """Primary RelayKeys device port"""
    return hardware_info['primary_device']


@pytest.fixture(scope="session")
def daemon_process(hardware_connected, primary_device):
    """Start daemon process for testing (hardware-aware)"""
    if hardware_connected and primary_device:
        # Start with real hardware
        cmd = [
            "uv", "run", "python", "relaykeysd.py",
            "--debug", f"--dev={primary_device}"
        ]
        print(f"🔧 Starting daemon with hardware: {primary_device}")
    else:
        # Start with dummy hardware
        cmd = [
            "uv", "run", "python", "relaykeysd.py",
            "--noserial", "--dev=COM99", "--debug"
        ]
        print("🔧 Starting daemon in dummy mode")
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Give daemon time to start
    time.sleep(5 if hardware_connected else 3)
    
    yield process
    
    # Cleanup
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
            print("✅ Daemon terminated cleanly")
        except subprocess.TimeoutExpired:
            process.kill()
            print("⚠️ Daemon force killed")


@pytest.fixture
def relaykeys_client():
    """Provide a RelayKeys client for testing"""
    from relaykeysclient import RelayKeysClient
    return RelayKeysClient(url="http://127.0.0.1:5383/")


@pytest.fixture(scope="session")
def test_mode(hardware_connected):
    """Determine test mode based on hardware"""
    return "hardware" if hardware_connected else "dummy"


class TestConfig:
    """Test configuration based on hardware availability"""
    
    def __init__(self):
        self.detector = HardwareDetector()
        self.hardware_info = self.detector.get_hardware_info()
    
    @property
    def hardware_connected(self):
        return self.hardware_info['hardware_connected']
    
    @property
    def primary_device(self):
        return self.hardware_info['primary_device']
    
    @property
    def test_mode(self):
        return "hardware" if self.hardware_connected else "dummy"
    
    def get_daemon_args(self):
        """Get appropriate daemon arguments"""
        if self.hardware_connected:
            return ["--debug", f"--dev={self.primary_device}"]
        else:
            return ["--noserial", "--dev=COM99", "--debug"]
    
    def should_skip_hardware_test(self):
        """Check if hardware tests should be skipped"""
        return not self.hardware_connected
    
    def should_skip_dummy_test(self):
        """Check if dummy tests should be skipped"""
        # Usually we don't skip dummy tests even with hardware
        return False


# Global test config instance
test_config = TestConfig()


def pytest_runtest_setup(item):
    """Setup for individual test runs"""
    # You can add per-test setup logic here
    pass


def pytest_report_header(config):
    """Add custom header to pytest report"""
    detector = HardwareDetector()
    hardware_info = detector.get_hardware_info()
    
    header = [
        f"RelayKeys Test Suite",
        f"Hardware Status: {'✅ Connected' if hardware_info['hardware_connected'] else '❌ Not Connected'}",
    ]
    
    if hardware_info['hardware_connected']:
        header.append(f"Primary Device: {hardware_info['primary_device']}")
        header.append(f"Device Count: {hardware_info['device_count']}")
    
    return header
