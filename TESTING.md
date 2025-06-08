# RelayKeys Testing Guide

This document explains the RelayKeys testing system, which automatically adapts based on whether hardware is connected.

## 🔍 Hardware-Aware Testing

RelayKeys uses an intelligent testing system that automatically detects if RelayKeys hardware is connected and runs appropriate tests:

- **With Hardware**: Runs full integration tests with real hardware
- **Without Hardware**: Runs dummy/simulation tests that don't require hardware
- **Adaptive Tests**: Tests that work in both modes

## 🚀 Quick Start

### Run All Tests (Recommended)
```bash
# Automatically detects hardware and runs appropriate tests
uv run python run_tests.py
```

### Quick Tests Only
```bash
# Fast tests for development
uv run python run_tests.py --quick
```

### Hardware-Specific Tests
```bash
# Only run tests that require hardware (fails if no hardware)
uv run python run_tests.py --hardware-only

# Only run software/dummy tests
uv run python run_tests.py --dummy-only
```

### Code Quality + Tests
```bash
# Run linting, formatting, and tests
uv run python lint_and_test.py
```

## 🔧 Hardware Detection

The system automatically detects RelayKeys hardware by looking for:

- **CP2104 USB to UART Bridge**: Common RelayKeys hardware
- **nRF52 Development Kit**: Nordic semiconductor boards
- **Adafruit Devices**: VID 0x239A or hardware ID containing "239A"

### Check Hardware Status
```bash
# See what hardware is detected
uv run python tests/hardware_detection.py
```

Example output:
```
🔍 RelayKeys Hardware Detection Report
==================================================
✅ Hardware Connected: 1 device(s) found
🎯 Primary Device: COM6

📋 Detected RelayKeys Devices:
  1. COM6
     Type: CP2104 USB to UART Bridge
     Description: CP2104 USB to UART Bridge Controller
     VID:PID: 0x10c4:0xea60
```

## 📋 Test Categories

### 1. Hardware Detection Tests
- Test the hardware detection system itself
- Always run regardless of hardware status
- Located in: `tests/test_hardware_aware.py::TestHardwareDetection`

### 2. Dummy Mode Tests (`@pytest.mark.no_hardware`)
- Tests that simulate hardware without requiring real devices
- Use dummy serial connections
- Located in: `tests/test_hardware_aware.py::TestDummyMode`

### 3. Hardware Mode Tests (`@pytest.mark.hardware_required`)
- Tests that require actual RelayKeys hardware
- Automatically skipped if no hardware detected
- Located in: `tests/test_hardware_aware.py::TestHardwareMode`

### 4. Adaptive Tests
- Tests that work with or without hardware
- Adapt behavior based on what's available
- Located in: `tests/test_hardware_aware.py::TestAdaptiveMode`

### 5. Integration Tests (`@pytest.mark.integration`)
- Full workflow tests
- Separate versions for hardware and dummy modes
- Located in: `tests/test_hardware_aware.py::TestFullIntegration`

## 🛠️ Development Workflow

### For Developers Without Hardware
```bash
# Run all software tests
uv run python run_tests.py --dummy-only

# Quick development tests
uv run python run_tests.py --quick

# Code quality checks
uv run ruff check .
uv run black --check .
```

### For Developers With Hardware
```bash
# Run full test suite (hardware + software)
uv run python run_tests.py

# Test only hardware functionality
uv run python run_tests.py --hardware-only

# Verify hardware detection
uv run python tests/hardware_detection.py
```

### Continuous Integration
```bash
# Complete quality + test suite
uv run python lint_and_test.py
```

## 📁 Test File Structure

```
tests/
├── conftest.py                 # Pytest configuration & fixtures
├── hardware_detection.py       # Hardware detection utilities
├── test_hardware_aware.py      # Main hardware-aware tests
├── test_serial_wrappers.py     # Serial communication tests
├── test_relaykeysclient.py     # RPC client tests
├── test_cli_keymap.py          # Keymap tests
└── test_daemon_integration.py  # Legacy integration tests
```

## 🎯 Test Markers

Use pytest markers to control test execution:

```python
@pytest.mark.hardware_required
def test_real_hardware():
    """This test needs actual hardware"""
    pass

@pytest.mark.no_hardware  
def test_dummy_mode():
    """This test works without hardware"""
    pass

@pytest.mark.integration
def test_full_workflow():
    """This is an integration test"""
    pass

@pytest.mark.slow
def test_long_running():
    """This test takes a long time"""
    pass
```

## 🔧 Fixtures Available

The testing system provides these fixtures:

- `hardware_detector`: Hardware detection instance
- `hardware_info`: Complete hardware information
- `hardware_connected`: Boolean - is hardware connected?
- `primary_device`: Primary RelayKeys device port
- `daemon_process`: Auto-configured daemon process
- `relaykeys_client`: RPC client instance
- `test_mode`: "hardware" or "dummy"

## 📊 Example Test Output

```
🚀 RelayKeys Test Runner
==================================================
🔍 Hardware Status: ✅ Connected
🎯 Primary Device: COM6
📱 Device Count: 1
   1. COM6 (cp2104)

📋 Running 6 test suite(s)
==================================================

🔧 Hardware Detection Tests
✅ PASSED - Hardware Detection Tests

🔧 Basic Unit Tests  
✅ PASSED - Basic Unit Tests

🔧 Dummy Mode Tests
✅ PASSED - Dummy Mode Tests

🔧 Adaptive Tests
✅ PASSED - Adaptive Tests

🔧 Hardware Tests
✅ PASSED - Hardware Tests

🔧 Hardware Integration
✅ PASSED - Hardware Integration

🎯 Overall: 6/6 test suites passed
🎉 All tests passed!
```

## 🐛 Troubleshooting

### No Hardware Detected But Hardware Is Connected
1. Check if device appears in Device Manager (Windows) or `lsusb` (Linux)
2. Verify driver installation
3. Try different USB ports/cables
4. Run: `uv run python tests/hardware_detection.py` to see all detected ports

### Tests Failing With Hardware
1. Ensure no other software is using the COM port
2. Check hardware is properly flashed with RelayKeys firmware
3. Try running daemon manually: `uv run python relaykeysd.py --debug --dev=COMX`

### Tests Timing Out
1. Increase timeout values in test configuration
2. Check if antivirus is interfering
3. Try running tests individually to isolate issues

## 🔄 Adding New Tests

### Hardware-Aware Test Template
```python
@pytest.mark.hardware_required
def test_new_hardware_feature(daemon_process, relaykeys_client, hardware_connected):
    """Test new feature with real hardware"""
    if not hardware_connected:
        pytest.skip("Hardware not connected")
    
    # Your test code here
    result = relaykeys_client.some_new_command()
    assert result == "SUCCESS"

def test_new_feature_dummy(daemon_process, relaykeys_client):
    """Test new feature in dummy mode"""
    # Your test code here - should work without hardware
    result = relaykeys_client.some_new_command()
    assert result is not None
```

This testing system ensures RelayKeys works reliably whether you're developing with or without hardware! 🎉
