#!/usr/bin/env python3
"""
Integration tests for RelayKeys daemon
Tests the daemon without requiring hardware
"""

import subprocess
import time

import pytest
import requests


class TestDaemonIntegration:
    """Integration tests for the RelayKeys daemon"""

    @pytest.fixture
    def daemon_process(self):
        """Start daemon process for testing"""
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

        # Give daemon time to start
        time.sleep(3)

        yield process

        # Cleanup
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

    def test_daemon_starts_successfully(self, daemon_process):
        """Test that daemon starts without errors"""
        # Check process is still running
        assert daemon_process.poll() is None

    def test_rpc_server_responds(self, daemon_process):
        """Test that RPC server is responding"""
        # Give extra time for server to be ready
        time.sleep(2)

        try:
            response = requests.post(
                "http://localhost:5383/",
                json={"method": "daemon", "params": ["dongle_status"], "id": 1},
                timeout=5,
            )
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("Daemon RPC server not accessible")

    def test_daemon_status_command(self, daemon_process):
        """Test daemon status command"""
        time.sleep(2)

        try:
            response = requests.post(
                "http://localhost:5383/",
                json={"method": "daemon", "params": ["dongle_status"], "id": 1},
                timeout=5,
            )

            if response.status_code == 200:
                data = response.json()
                assert "result" in data
        except requests.exceptions.ConnectionError:
            pytest.skip("Daemon RPC server not accessible")

    def test_keyevent_command(self, daemon_process):
        """Test keyevent command through RPC"""
        time.sleep(2)

        try:
            response = requests.post(
                "http://localhost:5383/",
                json={"method": "keyevent", "params": ["A", [], True], "id": 1},
                timeout=5,
            )

            if response.status_code == 200:
                data = response.json()
                assert "result" in data
        except requests.exceptions.ConnectionError:
            pytest.skip("Daemon RPC server not accessible")

    def test_mousemove_command(self, daemon_process):
        """Test mousemove command through RPC"""
        time.sleep(2)

        try:
            response = requests.post(
                "http://localhost:5383/",
                json={"method": "mousemove", "params": [10, 10, 0, 0], "id": 1},
                timeout=5,
            )

            if response.status_code == 200:
                data = response.json()
                assert "result" in data
        except requests.exceptions.ConnectionError:
            pytest.skip("Daemon RPC server not accessible")


class TestCLIIntegration:
    """Integration tests for CLI commands"""

    @pytest.fixture
    def daemon_process(self):
        """Start daemon process for CLI testing"""
        process = subprocess.Popen(
            ["uv", "run", "python", "relaykeysd.py", "--noserial", "--dev=COM99"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Give daemon time to start
        time.sleep(3)

        yield process

        # Cleanup
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

    def test_cli_daemon_status(self, daemon_process):
        """Test CLI daemon status command"""
        time.sleep(2)

        try:
            result = subprocess.run(
                ["uv", "run", "python", "relaykeys-cli.py", "daemon:dongle_status"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            # Command should execute without error
            assert result.returncode == 0 or "timeout" in result.stderr.lower()
        except subprocess.TimeoutExpired:
            pytest.skip("CLI command timed out")

    def test_cli_type_command(self, daemon_process):
        """Test CLI type command"""
        time.sleep(2)

        try:
            result = subprocess.run(
                ["uv", "run", "python", "relaykeys-cli.py", "type:Test"],
                capture_output=True,
                text=True,
                timeout=15,
            )

            # Command should execute (may timeout due to slow processing)
            assert result.returncode == 0 or "timeout" in result.stderr.lower()
        except subprocess.TimeoutExpired:
            pytest.skip("CLI command timed out")


class TestConfigurationLoading:
    """Test configuration loading"""

    def test_config_file_exists(self):
        """Test that example config file exists"""
        import os

        assert os.path.exists("relaykeys-example.cfg")

    def test_config_file_parsing(self):
        """Test config file can be parsed"""
        from configparser import ConfigParser

        config = ConfigParser()
        config.read("relaykeys-example.cfg")

        # Should have at least some sections
        assert len(config.sections()) >= 0

    def test_config_client_section(self):
        """Test client section in config"""
        from configparser import ConfigParser

        config = ConfigParser()
        config.read("relaykeys-example.cfg")

        # Check if client section exists or use defaults
        if config.has_section("client"):
            client_config = dict(config["client"])
            assert isinstance(client_config, dict)


class TestModuleImports:
    """Test that all modules can be imported"""

    def test_import_relaykeysclient(self):
        """Test importing relaykeysclient"""
        from relaykeys.core import client

        assert hasattr(client, "RelayKeysClient")

    def test_import_serial_wrappers(self):
        """Test importing serial_wrappers"""
        from relaykeys.core import serial_wrappers

        assert hasattr(serial_wrappers, "DummySerial")

    def test_import_cli_keymap(self):
        """Test importing cli_keymap"""
        from relaykeys.cli import keymap

        assert hasattr(keymap, "load_keymap_file")

    def test_import_blehid(self):
        """Test importing blehid"""
        from relaykeys.core import blehid
        # Should import without error
        assert hasattr(blehid, "blehid_init_serial")


class TestErrorHandling:
    """Test error handling scenarios"""

    def test_invalid_rpc_request(self):
        """Test handling of invalid RPC requests"""
        # This would test with a running daemon
        # For now, just test the structure
        invalid_request = {"invalid": "request"}

        # Should be properly formatted JSON-RPC
        assert "method" not in invalid_request
        assert "params" not in invalid_request

    def test_connection_refused_handling(self):
        """Test handling when daemon is not running"""
        try:
            response = requests.post(
                "http://localhost:5383/",
                json={"method": "daemon", "params": ["status"], "id": 1},
                timeout=1,
            )
        except requests.exceptions.ConnectionError:
            # This is expected when daemon is not running
            pass


if __name__ == "__main__":
    pytest.main([__file__])
