#!/usr/bin/env python3
"""
Comprehensive Synthetic Test Runner for RelayKeys
Runs extensive tests without requiring any hardware
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path


def run_command(cmd, description="Running command", timeout=300):
    """Run a command and return success status"""
    print(f"\n🔧 {description}")
    print("=" * 60)
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, shell=True, timeout=timeout)
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED ({duration:.1f}s)")
            return True
        else:
            print(f"❌ {description} - FAILED ({duration:.1f}s)")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT (>{timeout}s)")
        return False
    except Exception as e:
        print(f"💥 {description} - ERROR: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="RelayKeys Synthetic Test Suite")
    parser.add_argument("--quick", action="store_true", 
                       help="Run quick tests only (skip stress tests)")
    parser.add_argument("--stress-only", action="store_true", 
                       help="Run stress tests only")
    parser.add_argument("--cli-only", action="store_true", 
                       help="Run CLI tests only")
    parser.add_argument("--serial-only", action="store_true", 
                       help="Run serial tests only")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--timeout", type=int, default=300,
                       help="Timeout per test suite in seconds (default: 300)")
    
    args = parser.parse_args()
    
    print("🚀 RelayKeys Comprehensive Synthetic Test Suite")
    print("=" * 70)
    print("🎯 Testing ALL functionality without requiring hardware")
    print("⚡ This will push RelayKeys to its limits in synthetic mode")
    print()
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Error: pyproject.toml not found. Run this from the project root.")
        sys.exit(1)
    
    results = []
    verbose_flag = "-v" if args.verbose else ""
    
    # Define test suites
    test_suites = []
    
    if not args.stress_only and not args.cli_only:
        # Core synthetic tests
        test_suites.extend([
            (f"uv run pytest tests/test_synthetic_comprehensive.py::TestSyntheticSerialCommunication {verbose_flag}",
             "🔌 Synthetic Serial Communication Tests", 120),
            
            (f"uv run pytest tests/test_synthetic_comprehensive.py::TestSyntheticDaemonIntegration {verbose_flag}",
             "🤖 Synthetic Daemon Integration Tests", 180),
            
            (f"uv run pytest tests/test_synthetic_comprehensive.py::TestSyntheticErrorScenarios {verbose_flag}",
             "⚠️  Synthetic Error Scenario Tests", 90),
            
            (f"uv run pytest tests/test_synthetic_comprehensive.py::TestSyntheticPerformance {verbose_flag}",
             "⚡ Synthetic Performance Tests", 150),
        ])
    
    if not args.stress_only and not args.serial_only:
        # CLI tests
        test_suites.extend([
            (f"uv run pytest tests/test_synthetic_cli.py::TestSyntheticCLICommands {verbose_flag}",
             "💻 Synthetic CLI Command Tests", 240),
            
            (f"uv run pytest tests/test_synthetic_cli.py::TestSyntheticCLIMacros {verbose_flag}",
             "📝 Synthetic CLI Macro Tests", 180),
            
            (f"uv run pytest tests/test_synthetic_cli.py::TestSyntheticCLIErrorHandling {verbose_flag}",
             "🚨 Synthetic CLI Error Handling Tests", 120),
            
            (f"uv run pytest tests/test_synthetic_cli.py::TestSyntheticCLIConfiguration {verbose_flag}",
             "⚙️  Synthetic CLI Configuration Tests", 90),
        ])
        
        if not args.quick:
            test_suites.append(
                (f"uv run pytest tests/test_synthetic_cli.py::TestSyntheticCLIPerformance {verbose_flag}",
                 "🏃 Synthetic CLI Performance Tests", 300)
            )
    
    if args.stress_only or (not args.quick and not args.cli_only and not args.serial_only):
        # Stress tests
        test_suites.extend([
            (f"uv run pytest tests/test_synthetic_stress.py::TestSyntheticStressRPC {verbose_flag}",
             "🔥 Synthetic RPC Stress Tests", 600),
            
            (f"uv run pytest tests/test_synthetic_stress.py::TestSyntheticStressCLI {verbose_flag}",
             "💥 Synthetic CLI Stress Tests", 600),
            
            (f"uv run pytest tests/test_synthetic_stress.py::TestSyntheticStressSerial {verbose_flag}",
             "⚡ Synthetic Serial Stress Tests", 300),
            
            (f"uv run pytest tests/test_synthetic_stress.py::TestSyntheticStressMemory {verbose_flag}",
             "🧠 Synthetic Memory Stress Tests", 300),
        ])
    
    # Filter by specific test types
    if args.cli_only:
        test_suites = [suite for suite in test_suites if "CLI" in suite[1]]
    elif args.serial_only:
        test_suites = [suite for suite in test_suites if "Serial" in suite[1]]
    
    print(f"📋 Running {len(test_suites)} test suite(s)")
    if args.quick:
        print("⚡ Quick mode: Skipping stress tests")
    if args.stress_only:
        print("🔥 Stress mode: Running stress tests only")
    print()
    
    # Run all test suites
    start_time = time.time()
    
    for cmd, description, timeout in test_suites:
        success = run_command(cmd, description, min(timeout, args.timeout))
        results.append((description, success))
        
        # Brief pause between test suites
        time.sleep(1)
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SYNTHETIC TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = 0
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {description}")
        if success:
            passed += 1
    
    total = len(results)
    print(f"\n🎯 Overall Results:")
    print(f"   ✅ Passed: {passed}/{total} test suites")
    print(f"   ⏱️  Total Time: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
    
    if passed == total:
        print("\n🎉 ALL SYNTHETIC TESTS PASSED!")
        print("🚀 RelayKeys is ready for production!")
        print("💪 The system handled all synthetic scenarios successfully!")
        
        # Performance summary
        if total_duration > 0:
            tests_per_minute = (total * 60) / total_duration
            print(f"📈 Performance: {tests_per_minute:.1f} test suites per minute")
        
        return 0
    else:
        failed = total - passed
        print(f"\n⚠️  {failed} test suite(s) failed")
        print("🔍 Check the output above for details")
        print("🛠️  Some synthetic scenarios need attention")
        return 1


if __name__ == "__main__":
    sys.exit(main())
