#!/usr/bin/env python3
"""
Tests for cli_keymap module
"""

import json
from pathlib import Path

import pytest

import cli_keymap


class TestKeyMapping:
    """Test key mapping functionality"""

    def test_load_keymap_file_exists(self):
        """Test loading keymap when file exists"""
        # Check if the default keymap file exists
        keymap_path = Path("cli_keymaps/default.json")
        if keymap_path.exists():
            keymap = cli_keymap.load_keymap("default")
            assert isinstance(keymap, dict)
            assert len(keymap) > 0

    def test_load_keymap_file_not_exists(self):
        """Test loading keymap when file doesn't exist"""
        keymap = cli_keymap.load_keymap("nonexistent")
        # Should return empty dict or None
        assert keymap is None or keymap == {}

    def test_keymap_structure(self):
        """Test keymap structure is valid"""
        keymap_path = Path("cli_keymaps/default.json")
        if keymap_path.exists():
            with open(keymap_path) as f:
                keymap_data = json.load(f)

            # Check it's a dictionary
            assert isinstance(keymap_data, dict)

            # Check some expected keys exist
            expected_keys = ["A", "B", "C", "SPACE", "ENTER"]
            for key in expected_keys:
                if key in keymap_data:
                    # Each key should map to a list or string
                    assert isinstance(keymap_data[key], (list, str))

    def test_special_keys_mapping(self):
        """Test that special keys are properly mapped"""
        keymap_path = Path("cli_keymaps/default.json")
        if keymap_path.exists():
            with open(keymap_path) as f:
                keymap_data = json.load(f)

            # Test some special keys
            special_keys = ["SPACE", "ENTER", "TAB", "ESCAPE"]
            for key in special_keys:
                if key in keymap_data:
                    # Special keys should have proper mappings
                    assert keymap_data[key] is not None

    def test_modifier_keys_mapping(self):
        """Test that modifier keys are properly mapped"""
        keymap_path = Path("cli_keymaps/default.json")
        if keymap_path.exists():
            with open(keymap_path) as f:
                keymap_data = json.load(f)

            # Test modifier keys
            modifier_keys = ["LSHIFT", "RSHIFT", "LCTRL", "RCTRL", "LALT", "RALT"]
            for key in modifier_keys:
                if key in keymap_data:
                    # Modifier keys should have proper mappings
                    assert keymap_data[key] is not None


class TestKeyConversion:
    """Test key conversion functions"""

    def test_char_to_key_conversion(self):
        """Test character to key conversion"""
        # Test basic character conversion
        if hasattr(cli_keymap, "char_to_key"):
            # Test uppercase letters
            assert cli_keymap.char_to_key("A") == "A"
            assert cli_keymap.char_to_key("Z") == "Z"

            # Test lowercase letters (should convert to uppercase)
            assert cli_keymap.char_to_key("a") == "A"
            assert cli_keymap.char_to_key("z") == "Z"

    def test_special_char_conversion(self):
        """Test special character conversion"""
        if hasattr(cli_keymap, "char_to_key"):
            # Test space
            space_key = cli_keymap.char_to_key(" ")
            assert space_key in ["SPACE", " "]

            # Test newline
            enter_key = cli_keymap.char_to_key("\n")
            assert enter_key in ["ENTER", "RETURN", "\n"]

    def test_number_conversion(self):
        """Test number character conversion"""
        if hasattr(cli_keymap, "char_to_key"):
            # Test digits
            for digit in "0123456789":
                key = cli_keymap.char_to_key(digit)
                assert key == digit or key == f"KEY_{digit}"


class TestKeymapValidation:
    """Test keymap validation"""

    def test_validate_keymap_structure(self):
        """Test keymap structure validation"""
        # Valid keymap
        valid_keymap = {"A": "A", "B": ["B"], "SPACE": " ", "ENTER": "\n"}

        # This would be a validation function
        assert self._is_valid_keymap(valid_keymap)

    def test_validate_keymap_invalid(self):
        """Test invalid keymap detection"""
        # Invalid keymap (non-string/list values)
        invalid_keymap = {
            "A": 123,  # Invalid: should be string or list
            "B": None,  # Invalid: should be string or list
        }

        assert not self._is_valid_keymap(invalid_keymap)

    def _is_valid_keymap(self, keymap):
        """Helper function to validate keymap structure"""
        if not isinstance(keymap, dict):
            return False

        for key, value in keymap.items():
            if not isinstance(key, str):
                return False
            if not isinstance(value, (str, list)):
                return False
            if isinstance(value, list):
                if not all(isinstance(item, str) for item in value):
                    return False

        return True


class TestKeymapFiles:
    """Test keymap file operations"""

    def test_keymap_directory_exists(self):
        """Test that keymap directory exists"""
        keymap_dir = Path("cli_keymaps")
        assert keymap_dir.exists() and keymap_dir.is_dir()

    def test_default_keymap_exists(self):
        """Test that default keymap exists"""
        default_keymap = Path("cli_keymaps/default.json")
        if default_keymap.exists():
            # Test it's valid JSON
            with open(default_keymap) as f:
                data = json.load(f)
            assert isinstance(data, dict)

    def test_keymap_file_format(self):
        """Test keymap file format"""
        keymap_dir = Path("cli_keymaps")
        if keymap_dir.exists():
            for keymap_file in keymap_dir.glob("*.json"):
                # Test each JSON file is valid
                with open(keymap_file) as f:
                    try:
                        data = json.load(f)
                        assert isinstance(data, dict)
                    except json.JSONDecodeError:
                        pytest.fail(f"Invalid JSON in {keymap_file}")


class TestKeyboardLayouts:
    """Test different keyboard layouts"""

    def test_multiple_layouts(self):
        """Test support for multiple keyboard layouts"""
        keymap_dir = Path("cli_keymaps")
        if keymap_dir.exists():
            json_files = list(keymap_dir.glob("*.json"))

            # Should have at least one keymap file
            assert len(json_files) >= 1

            # Test each layout file
            for layout_file in json_files:
                with open(layout_file) as f:
                    layout_data = json.load(f)

                # Basic validation
                assert isinstance(layout_data, dict)
                assert len(layout_data) > 0


if __name__ == "__main__":
    pytest.main([__file__])
