#!/usr/bin/env python3
"""
RelayKeys code quality and testing script
Run this to check code quality and run tests
Automatically detects hardware and runs appropriate tests
"""

import subprocess
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from tests.hardware_detection import HardwareDetector
except ImportError:
    HardwareDetector = None


def run_command(cmd, description):
    """Run a command and report results"""
    print(f"\n🔧 {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False


def main():
    """Run all quality checks"""
    print("🚀 RelayKeys Code Quality & Testing Suite")
    print("=" * 60)

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Error: pyproject.toml not found. Run this from the project root.")
        sys.exit(1)

    # Detect hardware
    hardware_connected = False
    if HardwareDetector:
        detector = HardwareDetector()
        hardware_info = detector.get_hardware_info()
        hardware_connected = hardware_info['hardware_connected']

        print(f"🔍 Hardware Detection: {'✅ Connected' if hardware_connected else '❌ Not Connected'}")
        if hardware_connected:
            print(f"🎯 Primary Device: {hardware_info['primary_device']}")
            print(f"📱 Device Count: {hardware_info['device_count']}")
        print()

    results = []
    
    # 1. Ruff linting
    results.append(run_command(
        "uv run ruff check .",
        "Ruff Linting Check"
    ))
    
    # 2. Black formatting check
    results.append(run_command(
        "uv run black --check --diff .",
        "Black Code Formatting Check"
    ))
    
    # 3. Run basic tests (without integration tests that need daemon)
    results.append(run_command(
        "uv run pytest tests/test_serial_wrappers.py::TestDummySerial -v",
        "Basic Unit Tests"
    ))

    # 4. Hardware detection tests
    if HardwareDetector:
        results.append(run_command(
            "uv run pytest tests/test_hardware_aware.py::TestHardwareDetection -v",
            "Hardware Detection Tests"
        ))

    # 5. Import tests
    results.append(run_command(
        "uv run pytest tests/test_daemon_integration.py::TestModuleImports::test_import_serial_wrappers -v",
        "Module Import Tests"
    ))

    # 6. Configuration tests
    results.append(run_command(
        "uv run pytest tests/test_daemon_integration.py::TestConfigurationLoading -v",
        "Configuration Loading Tests"
    ))

    # 7. Hardware-aware tests (dummy mode)
    results.append(run_command(
        "uv run pytest tests/test_hardware_aware.py::TestDummyMode -v",
        "Dummy Mode Tests"
    ))

    # 8. Hardware tests (only if hardware is connected)
    if hardware_connected:
        results.append(run_command(
            "uv run pytest tests/test_hardware_aware.py::TestHardwareMode -v",
            "Hardware Mode Tests"
        ))
        results.append(run_command(
            "uv run pytest tests/test_hardware_aware.py::TestFullIntegration::test_full_workflow_hardware -v",
            "Hardware Integration Tests"
        ))
    else:
        print("⏭️  Skipping hardware tests (no hardware detected)")

    # 9. Adaptive tests (work with or without hardware)
    results.append(run_command(
        "uv run pytest tests/test_hardware_aware.py::TestAdaptiveMode -v",
        "Adaptive Mode Tests"
    ))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ALL CHECKS PASSED! ({passed}/{total})")
        print("✅ Code is ready for production!")
        return 0
    else:
        print(f"⚠️  Some checks failed: {passed}/{total} passed")
        print("❌ Please fix the issues above before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
