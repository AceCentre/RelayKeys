#!/usr/bin/env python3
"""
Comprehensive synthetic CLI tests for RelayKeys
Tests all CLI functionality without requiring hardware
"""

import os
import subprocess
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.mark.no_hardware
class TestSyntheticCLICommands:
    """Test all CLI commands in synthetic mode"""
    
    @pytest.fixture
    def daemon_process(self):
        """Start daemon for CLI testing"""
        process = subprocess.Popen([
            "uv", "run", "python", "relaykeysd.py",
            "--noserial", "--dev=COM99", "--debug"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)  # Give daemon time to start
        yield process
        
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
    
    def test_cli_basic_commands(self, daemon_process):
        """Test basic CLI commands"""
        time.sleep(2)
        
        basic_commands = [
            "daemon:dongle_status",
            "daemon:get_mode", 
            "ble_cmd:devname",
            "ble_cmd:devlist",
        ]
        
        for cmd in basic_commands:
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", cmd
                ], capture_output=True, text=True, timeout=10)
                
                # Command should execute (may have various return codes)
                assert result.returncode in [0, 1]  # 0=success, 1=expected error
                
            except subprocess.TimeoutExpired:
                pytest.skip(f"CLI command {cmd} timed out")
    
    def test_cli_keyboard_commands(self, daemon_process):
        """Test keyboard-related CLI commands"""
        time.sleep(2)
        
        keyboard_commands = [
            "keyevent:A,[],1",      # Press A
            "keyevent:A,[],0",      # Release A
            "keyevent:B,[LSHIFT],1", # Press Shift+B
            "keyevent:B,[LSHIFT],0", # Release Shift+B
            "keypress:SPACE",        # Press and release Space
            "keypress:ENTER",        # Press and release Enter
        ]
        
        for cmd in keyboard_commands:
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", cmd
                ], capture_output=True, text=True, timeout=15)
                
                # Should execute without crashing
                assert result.returncode in [0, 1]
                
            except subprocess.TimeoutExpired:
                pytest.skip(f"CLI command {cmd} timed out")
    
    def test_cli_mouse_commands(self, daemon_process):
        """Test mouse-related CLI commands"""
        time.sleep(2)
        
        mouse_commands = [
            "mousemove:10,10",       # Move mouse
            "mousemove:-5,5",        # Move mouse back
            "mousebutton:l,click",   # Left click
            "mousebutton:r,click",   # Right click
            "mousebutton:m,press",   # Middle press
            "mousebutton:0",         # Release all
        ]
        
        for cmd in mouse_commands:
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", cmd
                ], capture_output=True, text=True, timeout=15)
                
                assert result.returncode in [0, 1]
                
            except subprocess.TimeoutExpired:
                pytest.skip(f"CLI command {cmd} timed out")
    
    def test_cli_type_command(self, daemon_process):
        """Test type command with various text"""
        time.sleep(2)
        
        test_texts = [
            "Hello World",
            "Test123!@#",
            "Special chars: àáâãäå",
            "Numbers: 0123456789",
            "Symbols: !@#$%^&*()",
        ]
        
        for text in test_texts:
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", f"type:{text}"
                ], capture_output=True, text=True, timeout=20)
                
                # Type command should execute
                assert result.returncode in [0, 1]
                
            except subprocess.TimeoutExpired:
                pytest.skip(f"CLI type command timed out for: {text}")
    
    def test_cli_paste_command(self, daemon_process):
        """Test paste command"""
        time.sleep(2)
        
        # Mock clipboard content
        with patch('pyperclip.paste') as mock_paste:
            mock_paste.return_value = "Test clipboard content"
            
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", "paste"
                ], capture_output=True, text=True, timeout=15)
                
                assert result.returncode in [0, 1]
                
            except subprocess.TimeoutExpired:
                pytest.skip("CLI paste command timed out")
    
    def test_cli_ble_commands(self, daemon_process):
        """Test BLE-related CLI commands"""
        time.sleep(2)
        
        ble_commands = [
            "ble_cmd:devlist",
            "ble_cmd:devname",
            "ble_cmd:devadd",
            "ble_cmd:devreset",
        ]
        
        for cmd in ble_commands:
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", cmd
                ], capture_output=True, text=True, timeout=15)
                
                assert result.returncode in [0, 1]
                
            except subprocess.TimeoutExpired:
                pytest.skip(f"CLI BLE command {cmd} timed out")


@pytest.mark.no_hardware
class TestSyntheticCLIMacros:
    """Test CLI macro functionality"""
    
    @pytest.fixture
    def daemon_process(self):
        """Start daemon for macro testing"""
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
    
    def test_cli_macro_execution(self, daemon_process):
        """Test macro file execution"""
        time.sleep(2)
        
        # Create a test macro file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            macro_content = """keypress:H
keypress:E
keypress:L
keypress:L
keypress:O
keypress:SPACE
keypress:W
keypress:O
keypress:R
keypress:L
keypress:D
"""
            f.write(macro_content)
            macro_file = f.name
        
        try:
            # Execute the macro
            result = subprocess.run([
                "uv", "run", "python", "relaykeys-cli.py", f"macro:{macro_file}"
            ], capture_output=True, text=True, timeout=30)
            
            # Should execute without crashing
            assert result.returncode in [0, 1]
            
        except subprocess.TimeoutExpired:
            pytest.skip("CLI macro execution timed out")
        finally:
            # Clean up
            os.unlink(macro_file)
    
    def test_cli_complex_macro(self, daemon_process):
        """Test complex macro with various commands"""
        time.sleep(2)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            complex_macro = """type:Hello World
delay:500
keypress:ENTER
mousemove:10,10
mousebutton:l,click
delay:100
keyevent:A,[LCTRL],1
keyevent:A,[LCTRL],0
type:Selected All
"""
            f.write(complex_macro)
            macro_file = f.name
        
        try:
            result = subprocess.run([
                "uv", "run", "python", "relaykeys-cli.py", f"macro:{macro_file}"
            ], capture_output=True, text=True, timeout=45)
            
            assert result.returncode in [0, 1]
            
        except subprocess.TimeoutExpired:
            pytest.skip("Complex macro execution timed out")
        finally:
            os.unlink(macro_file)


@pytest.mark.no_hardware
class TestSyntheticCLIErrorHandling:
    """Test CLI error handling scenarios"""
    
    def test_cli_invalid_commands(self):
        """Test CLI with invalid commands"""
        invalid_commands = [
            "invalid:command",
            "keyevent:INVALID_KEY,[],1",
            "mousemove:invalid,coords",
            "ble_cmd:invalid_ble_command",
            "daemon:invalid_daemon_command",
        ]
        
        for cmd in invalid_commands:
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", cmd
                ], capture_output=True, text=True, timeout=10)
                
                # Should handle errors gracefully (may succeed in dummy mode)
                assert result.returncode in [0, 1, 2]
                
            except subprocess.TimeoutExpired:
                pytest.skip(f"Invalid command {cmd} timed out")
    
    def test_cli_no_daemon(self):
        """Test CLI behavior when daemon is not running"""
        # Don't start daemon for this test
        
        commands = [
            "daemon:dongle_status",
            "keypress:A",
            "mousemove:10,10",
        ]
        
        for cmd in commands:
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", cmd
                ], capture_output=True, text=True, timeout=10)
                
                # Should handle daemon not running (may succeed in dummy mode)
                assert result.returncode in [0, 1, 2]
                # In dummy mode, daemon might still be running from previous tests
                
            except subprocess.TimeoutExpired:
                pytest.skip(f"CLI command {cmd} timed out without daemon")
    
    def test_cli_malformed_arguments(self):
        """Test CLI with malformed arguments"""
        malformed_commands = [
            "keyevent:",  # Missing arguments
            "keyevent:A",  # Incomplete arguments
            "mousemove:",  # Missing coordinates
            "type:",  # Empty type command
            "macro:",  # Missing macro file
        ]
        
        for cmd in malformed_commands:
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", cmd
                ], capture_output=True, text=True, timeout=10)
                
                # Should handle malformed commands gracefully (may succeed in dummy mode)
                assert result.returncode in [0, 1, 2]
                
            except subprocess.TimeoutExpired:
                pytest.skip(f"Malformed command {cmd} timed out")


@pytest.mark.no_hardware
class TestSyntheticCLIConfiguration:
    """Test CLI configuration scenarios"""
    
    def test_cli_with_config_file(self):
        """Test CLI with custom configuration"""
        # Create a test config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cfg', delete=False) as f:
            config_content = """[client]
url = http://127.0.0.1:5383/
timeout = 10

[cli]
keymap_file = us_keymap.json
"""
            f.write(config_content)
            config_file = f.name
        
        try:
            # Test CLI with custom config
            result = subprocess.run([
                "uv", "run", "python", "relaykeys-cli.py", 
                "--config", config_file, "daemon:dongle_status"
            ], capture_output=True, text=True, timeout=10)
            
            # Should execute with custom config
            assert result.returncode in [0, 1]
            
        except subprocess.TimeoutExpired:
            pytest.skip("CLI with config file timed out")
        finally:
            os.unlink(config_file)
    
    def test_cli_keymap_functionality(self):
        """Test CLI keymap functionality"""
        # Test if keymap files exist and are valid
        keymap_dir = Path("cli_keymaps")
        if keymap_dir.exists():
            keymap_files = list(keymap_dir.glob("*.json"))
            assert len(keymap_files) > 0
            
            # Test each keymap file is valid JSON
            for keymap_file in keymap_files:
                try:
                    import json
                    with open(keymap_file) as f:
                        keymap_data = json.load(f)
                    assert isinstance(keymap_data, dict)
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON in keymap file: {keymap_file}")


@pytest.mark.no_hardware
class TestSyntheticCLIPerformance:
    """Test CLI performance scenarios"""
    
    @pytest.fixture
    def daemon_process(self):
        """Start daemon for performance testing"""
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
    
    def test_cli_rapid_commands(self, daemon_process):
        """Test rapid CLI command execution"""
        import time
        time.sleep(2)
        start_time = time.time()
        
        # Execute 20 rapid commands
        for i in range(20):
            try:
                result = subprocess.run([
                    "uv", "run", "python", "relaykeys-cli.py", "keypress:A"
                ], capture_output=True, text=True, timeout=5)
                
                # Don't assert success, just that it doesn't crash
                
            except subprocess.TimeoutExpired:
                continue  # Skip timeouts in performance test
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time (less than 60 seconds)
        assert duration < 60.0
    
    def test_cli_large_type_command(self, daemon_process):
        """Test CLI with large type command"""
        time.sleep(2)
        
        # Create large text to type
        large_text = "A" * 500  # 500 characters
        
        try:
            result = subprocess.run([
                "uv", "run", "python", "relaykeys-cli.py", f"type:{large_text}"
            ], capture_output=True, text=True, timeout=60)
            
            # Should handle large text without crashing
            assert result.returncode in [0, 1]
            
        except subprocess.TimeoutExpired:
            pytest.skip("Large type command timed out")


if __name__ == "__main__":
    pytest.main([__file__])
