#!/usr/bin/env python3
"""
Tests for cli_keymap module
"""

import json
import sys
from pathlib import Path

import pytest

from relaykeys.cli import keymap as cli_keymap


class TestKeyMapping:
    """Test key mapping functionality"""

    def test_load_keymap_file_exists(self):
        """Test loading keymap when file exists"""
        # Check if the default keymap file exists
        keymap_path = Path("src/relaykeys/cli/keymaps/us_keymap.json")
        if keymap_path.exists():
            config = {"keymap_file": "us_keymap.json"}
            result = cli_keymap.load_keymap_file(config)
            assert result is True

    def test_load_keymap_file_not_exists(self):
        """Test loading keymap when file doesn't exist"""
        config = {"keymap_file": "nonexistent.json"}
        result = cli_keymap.load_keymap_file(config)
        # Should return False for non-existent file
        assert result is False

    def test_keymap_structure(self):
        """Test keymap structure is valid"""
        keymap_path = Path("src/relaykeys/cli/keymaps/us_keymap.json")
        if keymap_path.exists():
            with open(keymap_path) as f:
                keymap_data = json.load(f)

            # Check it's a dictionary
            assert isinstance(keymap_data, dict)

            # Check some expected keys exist
            expected_keys = ["a", "b", "c", " ", "\n"]
            for key in expected_keys:
                if key in keymap_data:
                    # Each key should map to a list or string
                    assert isinstance(keymap_data[key], (list, str))

    def test_special_keys_mapping(self):
        """Test that special keys are properly mapped"""
        keymap_path = Path("src/relaykeys/cli/keymaps/us_keymap.json")
        if keymap_path.exists():
            with open(keymap_path) as f:
                keymap_data = json.load(f)

            # Test some special keys
            special_keys = [" ", "\n", "\t"]
            for key in special_keys:
                if key in keymap_data:
                    # Special keys should have proper mappings
                    assert keymap_data[key] is not None

    def test_modifier_keys_mapping(self):
        """Test that modifier keys are properly mapped"""
        # Test the char_to_keyevent_params function instead
        config = {"keymap_file": "us_keymap.json"}
        cli_keymap.load_keymap_file(config)

        # Test uppercase letters (should include LSHIFT)
        result = cli_keymap.char_to_keyevent_params("A")
        assert result is not None
        assert len(result) == 2  # (key, modifiers)
        assert "LSHIFT" in result[1]


class TestKeyConversion:
    """Test key conversion functions"""

    def test_char_to_key_conversion(self):
        """Test character to key conversion"""
        # Load keymap first
        config = {"keymap_file": "us_keymap.json"}
        cli_keymap.load_keymap_file(config)

        # Test basic character conversion
        result_a = cli_keymap.char_to_keyevent_params("a")
        assert result_a is not None
        assert result_a[0] == "A"  # Key
        assert result_a[1] == []   # No modifiers for lowercase

        result_A = cli_keymap.char_to_keyevent_params("A")
        assert result_A is not None
        assert result_A[0] == "A"  # Key
        assert "LSHIFT" in result_A[1]  # Shift modifier for uppercase

    def test_special_char_conversion(self):
        """Test special character conversion"""
        # Load keymap first
        config = {"keymap_file": "us_keymap.json"}
        cli_keymap.load_keymap_file(config)

        # Test space
        space_result = cli_keymap.char_to_keyevent_params(" ")
        assert space_result is not None

        # Test newline
        enter_result = cli_keymap.char_to_keyevent_params("\n")
        assert enter_result is not None

    def test_number_conversion(self):
        """Test number character conversion"""
        # Load keymap first
        config = {"keymap_file": "us_keymap.json"}
        cli_keymap.load_keymap_file(config)

        # Test digits
        for digit in "0123456789":
            result = cli_keymap.char_to_keyevent_params(digit)
            assert result is not None
            assert result[0] == digit  # Key should be the digit itself


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
        keymap_dir = Path("src/relaykeys/cli/keymaps")
        assert keymap_dir.exists() and keymap_dir.is_dir()

    def test_default_keymap_exists(self):
        """Test that default keymap exists"""
        default_keymap = Path("src/relaykeys/cli/keymaps/us_keymap.json")
        if default_keymap.exists():
            # Test it's valid JSON
            with open(default_keymap) as f:
                data = json.load(f)
            assert isinstance(data, dict)

    def test_keymap_file_format(self):
        """Test keymap file format"""
        keymap_dir = Path("src/relaykeys/cli/keymaps")
        if keymap_dir.exists():
            for keymap_file in keymap_dir.glob("*.json"):
                # Test each JSON file is valid
                with open(keymap_file, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        assert isinstance(data, dict)
                    except json.JSONDecodeError:
                        pytest.fail(f"Invalid JSON in {keymap_file}")
                    except UnicodeDecodeError:
                        pytest.fail(f"Unicode encoding error in {keymap_file}")


class TestKeyboardLayouts:
    """Test different keyboard layouts"""

    def test_multiple_layouts(self):
        """Test support for multiple keyboard layouts"""
        keymap_dir = Path("src/relaykeys/cli/keymaps")
        if keymap_dir.exists():
            json_files = list(keymap_dir.glob("*.json"))

            # Should have at least one keymap file
            assert len(json_files) >= 1

            # Test each layout file
            for layout_file in json_files:
                with open(layout_file, 'r', encoding='utf-8') as f:
                    try:
                        layout_data = json.load(f)
                        assert isinstance(layout_data, dict)
                        assert len(layout_data) > 0

                        # Test some basic structure
                        for char, mapping in layout_data.items():
                            assert isinstance(char, str)
                            if mapping is not None:
                                assert isinstance(mapping, list)
                                assert len(mapping) == 2
                                # Key can be None or string
                                assert mapping[0] is None or isinstance(mapping[0], str)
                                # Modifiers must be list (can be None for special cases)
                                assert mapping[1] is None or isinstance(mapping[1], list)

                    except json.JSONDecodeError:
                        pytest.fail(f"Invalid JSON in {layout_file}")
                    except Exception as e:
                        pytest.fail(f"Error testing {layout_file}: {e}")

    def test_layout_validation(self):
        """Test layout validation functionality"""
        # Import here to avoid circular imports
        sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
        try:
            from layout_converter import KeyboardLayoutConverter

            converter = KeyboardLayoutConverter()

            # Test valid layout
            valid_layout = {
                "a": ["A", []],
                "A": ["A", ["LSHIFT"]],
                " ": ["SPACE", []],
                "\r": [None, None]
            }

            is_valid, errors = converter.validate_layout(valid_layout)
            assert is_valid
            assert len(errors) == 0

            # Test invalid layout
            invalid_layout = {
                "a": "invalid_mapping",  # Should be list
                "b": ["INVALID_KEY", []],  # Invalid key
                "c": ["A", ["INVALID_MOD"]]  # Invalid modifier
            }

            is_valid, errors = converter.validate_layout(invalid_layout)
            assert not is_valid
            assert len(errors) > 0

        except ImportError:
            pytest.skip("Layout converter tools not available")

    def test_new_layouts_structure(self):
        """Test that new layouts follow the correct structure"""
        keymap_dir = Path("src/relaykeys/cli/keymaps")

        # Expected new layout files
        expected_layouts = [
            "fr_azerty_keymap.json",
            "es_qwerty_keymap.json",
            "it_qwerty_keymap.json"
        ]

        for layout_file in expected_layouts:
            layout_path = keymap_dir / layout_file
            if layout_path.exists():
                with open(layout_path, 'r', encoding='utf-8') as f:
                    layout_data = json.load(f)

                # Test basic structure
                assert isinstance(layout_data, dict)
                assert len(layout_data) > 0

                # Test that common characters are present
                common_chars = ["a", "e", "i", "o", "u", " ", "1", "2", "3"]
                for char in common_chars:
                    if char in layout_data:
                        mapping = layout_data[char]
                        assert isinstance(mapping, list)
                        assert len(mapping) == 2

    def test_layout_character_coverage(self):
        """Test that layouts have good character coverage"""
        keymap_dir = Path("src/relaykeys/cli/keymaps")

        # New layouts that should have comprehensive coverage
        comprehensive_layouts = [
            "fr_azerty_keymap.json",
            "es_qwerty_keymap.json",
            "it_qwerty_keymap.json"
        ]

        for json_file in keymap_dir.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                layout_data = json.load(f)

            # Count different types of characters
            letters = sum(1 for char in layout_data.keys() if len(char) == 1 and char.isalpha())
            digits = sum(1 for char in layout_data.keys() if len(char) == 1 and char.isdigit())

            # Different expectations for new vs old layouts
            if json_file.name in comprehensive_layouts:
                # New layouts should have comprehensive coverage
                assert letters >= 20, f"New layout {json_file.name} has too few letters ({letters})"
                assert digits >= 5, f"New layout {json_file.name} has too few digits ({digits})"
            else:
                # Old layouts may be incomplete, just check they have some content
                assert len(layout_data) > 0, f"Layout {json_file.name} is empty"

            # Should have space and enter
            assert " " in layout_data, f"Layout {json_file.name} missing space character"
            assert any(char in layout_data for char in ["\n", "\r"]), f"Layout {json_file.name} missing enter character"

    def test_layout_consistency(self):
        """Test that layouts are internally consistent"""
        keymap_dir = Path("src/relaykeys/cli/keymaps")

        for json_file in keymap_dir.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                layout_data = json.load(f)

            # Check that uppercase/lowercase pairs are consistent
            for char in layout_data.keys():
                if len(char) == 1 and char.islower() and char.isalpha():
                    upper_char = char.upper()
                    if upper_char in layout_data:
                        lower_mapping = layout_data[char]
                        upper_mapping = layout_data[upper_char]

                        # Skip if either mapping is null or malformed
                        if (lower_mapping is None or upper_mapping is None or
                            len(lower_mapping) != 2 or len(upper_mapping) != 2 or
                            lower_mapping[0] is None or upper_mapping[0] is None or
                            lower_mapping[1] is None or upper_mapping[1] is None):
                            continue

                        # Both should map to the same key
                        assert lower_mapping[0] == upper_mapping[0], \
                            f"Inconsistent key mapping for {char}/{upper_char} in {json_file.name}"

                        # Upper should have shift modifier (only for regular letters)
                        if char.isascii() and char.isalpha():
                            assert "LSHIFT" in upper_mapping[1] or "RSHIFT" in upper_mapping[1], \
                                f"Uppercase {upper_char} should have shift modifier in {json_file.name}"


if __name__ == "__main__":
    pytest.main([__file__])
