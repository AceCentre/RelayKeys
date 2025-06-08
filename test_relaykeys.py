#!/usr/bin/env python3
"""
Comprehensive test suite for RelayKeys without hardware
Tests all major components in no-serial mode
"""

import subprocess
import time
from pathlib import Path

import requests


def test_daemon_startup():
    """Test that the daemon starts up correctly in no-serial mode"""
    print("🔧 Testing daemon startup...")

    # Start daemon in background with no-serial mode
    try:
        process = subprocess.Popen(
            [
                "uv",
                "run",
                "python",
                "relaykeysd.py",
                "--noserial",
                "--dev=COM99",
                "--debug",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Give it time to start
        time.sleep(5)

        # Check if process is still running
        if process.poll() is None:
            print("✅ Daemon started successfully")

            # Try to connect to RPC server with a simple daemon command
            try:
                response = requests.post(
                    "http://localhost:5383/",
                    json={"method": "daemon", "params": ["dongle_status"], "id": 1},
                    timeout=5,
                )
                if response.status_code == 200:
                    print("✅ RPC server responding")
                    result = response.json()
                    if "result" in result:
                        print(f"  📋 Daemon status: {result['result']}")
                    return True, process
                else:
                    print("❌ RPC server not responding")
                    return False, process
            except Exception as e:
                print(f"❌ Could not connect to RPC server: {e}")
                return False, process
        else:
            stdout, stderr = process.communicate()
            print("❌ Daemon failed to start")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return False, None

    except Exception as e:
        print(f"❌ Error starting daemon: {e}")
        return False, None


def test_cli_commands(daemon_process):
    """Test CLI commands work correctly"""
    print("\n🔧 Testing CLI commands...")

    # Give daemon more time to fully initialize
    time.sleep(2)

    test_commands = [
        "type:Hello_World_Test",
        "keypress:A,LSHIFT",
        "mousebutton:l,click",
        "mousemove:10,10",
        "daemon:dongle_status",
        "daemon:get_mode",
        "ble_cmd:devlist",
        "ble_cmd:devname",
    ]

    for cmd in test_commands:
        try:
            print(f"  Testing: {cmd}")
            result = subprocess.run(
                ["uv", "run", "python", "relaykeys-cli.py", cmd],
                capture_output=True,
                text=True,
                timeout=15,
            )

            if result.returncode == 0:
                print(f"  ✅ {cmd} - Success")
                if "response:" in result.stdout:
                    # Extract the response for verification
                    lines = result.stdout.strip().split("\n")
                    last_line = lines[-1] if lines else ""
                    if "response:" in last_line:
                        response = last_line.split("response:")[-1].strip()
                        print(f"    📋 Response: {response}")
            else:
                print(f"  ❌ {cmd} - Failed")
                if result.stderr:
                    print(f"    Error: {result.stderr.strip()}")

        except subprocess.TimeoutExpired:
            print(f"  ⏰ {cmd} - Timeout")
        except Exception as e:
            print(f"  ❌ {cmd} - Error: {e}")


def test_imports():
    """Test that all required modules can be imported"""
    print("\n🔧 Testing imports...")

    modules_to_test = ["relaykeysclient", "blehid", "serial_wrappers", "cli_keymap"]

    for module in modules_to_test:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module} - {e}")


def test_config_loading():
    """Test configuration file loading"""
    print("\n🔧 Testing configuration...")

    # Check if example config exists
    if Path("relaykeys-example.cfg").exists():
        print("  ✅ Example config file exists")
    else:
        print("  ❌ Example config file missing")

    # Test config parsing
    try:
        from configparser import ConfigParser

        config = ConfigParser()
        config.read("relaykeys-example.cfg")
        print("  ✅ Config file parses correctly")

        # Check for required sections
        if config.has_section("DEFAULT"):
            print("  ✅ DEFAULT section found")
        else:
            print("  ❌ DEFAULT section missing")

    except Exception as e:
        print(f"  ❌ Config parsing failed: {e}")


def cleanup_daemon(daemon_process):
    """Clean up daemon process"""
    if daemon_process and daemon_process.poll() is None:
        print("\n🧹 Cleaning up daemon...")
        daemon_process.terminate()
        try:
            daemon_process.wait(timeout=5)
            print("  ✅ Daemon terminated cleanly")
        except subprocess.TimeoutExpired:
            daemon_process.kill()
            print("  ⚠️ Daemon force killed")


def main():
    """Run all tests"""
    print("🚀 Starting RelayKeys comprehensive test suite")
    print("=" * 50)

    # Test imports first
    test_imports()

    # Test config
    test_config_loading()

    # Test daemon startup
    daemon_success, daemon_process = test_daemon_startup()

    if daemon_success:
        # Test CLI commands
        test_cli_commands(daemon_process)

        # Cleanup
        cleanup_daemon(daemon_process)
    else:
        print("❌ Cannot proceed with CLI tests - daemon failed to start")

    print("\n" + "=" * 50)
    print("🏁 Test suite completed")


if __name__ == "__main__":
    main()
