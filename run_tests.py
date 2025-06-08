#!/usr/bin/env python3
"""
RelayKeys Test Runner
Automatically detects hardware and runs appropriate tests
"""

import subprocess
import sys
import argparse
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from tests.hardware_detection import HardwareDetector
except ImportError:
    print("❌ Error: Could not import hardware detection. Run from project root.")
    sys.exit(1)


def run_command(cmd, description="Running command"):
    """Run a command and return success status"""
    print(f"\n🔧 {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="RelayKeys Test Runner")
    parser.add_argument("--hardware-only", action="store_true", 
                       help="Only run hardware tests")
    parser.add_argument("--dummy-only", action="store_true", 
                       help="Only run dummy/software tests")
    parser.add_argument("--quick", action="store_true", 
                       help="Run quick tests only")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    
    args = parser.parse_args()
    
    print("🚀 RelayKeys Test Runner")
    print("=" * 50)
    
    # Detect hardware
    detector = HardwareDetector()
    hardware_info = detector.get_hardware_info()
    hardware_connected = hardware_info['hardware_connected']
    
    print(f"🔍 Hardware Status: {'✅ Connected' if hardware_connected else '❌ Not Connected'}")
    if hardware_connected:
        print(f"🎯 Primary Device: {hardware_info['primary_device']}")
        print(f"📱 Device Count: {hardware_info['device_count']}")
        for i, device in enumerate(hardware_info['devices'], 1):
            print(f"   {i}. {device['device']} ({device['relaykeys_type']})")
    
    # Determine what tests to run
    test_commands = []
    
    if args.hardware_only:
        if not hardware_connected:
            print("❌ Error: --hardware-only specified but no hardware detected")
            return 1
        test_commands = [
            ("uv run pytest tests/test_hardware_aware.py::TestHardwareMode -v", "Hardware Tests"),
            ("uv run pytest tests/test_hardware_aware.py::TestFullIntegration::test_full_workflow_hardware -v", "Hardware Integration"),
        ]
    elif args.dummy_only:
        test_commands = [
            ("uv run pytest tests/test_serial_wrappers.py::TestDummySerial -v", "Dummy Serial Tests"),
            ("uv run pytest tests/test_hardware_aware.py::TestDummyMode -v", "Dummy Mode Tests"),
        ]
    elif args.quick:
        test_commands = [
            ("uv run pytest tests/test_hardware_aware.py::TestHardwareDetection -v", "Hardware Detection"),
            ("uv run pytest tests/test_serial_wrappers.py::TestDummySerial -v", "Basic Tests"),
        ]
    else:
        # Full test suite
        test_commands = [
            ("uv run pytest tests/test_hardware_aware.py::TestHardwareDetection -v", "Hardware Detection Tests"),
            ("uv run pytest tests/test_serial_wrappers.py::TestDummySerial -v", "Basic Unit Tests"),
            ("uv run pytest tests/test_hardware_aware.py::TestDummyMode -v", "Dummy Mode Tests"),
            ("uv run pytest tests/test_hardware_aware.py::TestAdaptiveMode -v", "Adaptive Tests"),
        ]
        
        if hardware_connected:
            test_commands.extend([
                ("uv run pytest tests/test_hardware_aware.py::TestHardwareMode -v", "Hardware Tests"),
                ("uv run pytest tests/test_hardware_aware.py::TestFullIntegration::test_full_workflow_hardware -v", "Hardware Integration"),
            ])
        else:
            print("⏭️  Skipping hardware tests (no hardware detected)")
    
    # Run tests
    print(f"\n📋 Running {len(test_commands)} test suite(s)")
    print("=" * 50)
    
    results = []
    for cmd, description in test_commands:
        success = run_command(cmd, description)
        results.append((description, success))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {description}")
        if success:
            passed += 1
    
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Check output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
