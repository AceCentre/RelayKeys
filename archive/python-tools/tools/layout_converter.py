#!/usr/bin/env python3
"""
RelayKeys Keyboard Layout Converter

This tool helps convert keyboard layouts from various sources to RelayKeys JSON format.
It supports manual layout definition, validation, and testing.

Usage:
    python layout_converter.py --create-layout fr_azerty
    python layout_converter.py --validate-layout us_keymap.json
    python layout_converter.py --list-layouts
    python layout_converter.py --test-layout fr_keymap.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class KeyboardLayoutConverter:
    """Converts and manages keyboard layouts for RelayKeys."""
    
    def __init__(self):
        self.relaykeys_root = Path(__file__).parent.parent
        self.keymaps_dir = self.relaykeys_root / "src" / "relaykeys" / "cli" / "keymaps"
        
        # Standard HID key codes that RelayKeys supports
        self.hid_keys = {
            "BACKSPACE", "ENTER", "TAB", "PAUSE", "ESCAPE", "SPACE",
            "QUOTE", "COMMA", "MINUS", "PERIOD", "SLASH",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "SEMICOLON", "EQUALS", "LEFTBRACKET", "BACKSLASH", 
            "RIGHTBRACKET", "BACKQUOTE", "A", "B", "C", "D", "E", "F",
            "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
            "S", "T", "U", "V", "W", "X", "Y", "Z", "DELETE", "END",
            "PAGEDOWN", "PAGEUP", "HOME", "LEFTARROW", "UPARROW",
            "RIGHTARROW", "DOWNARROW", "INSERT", "F1", "F2", "F3", "F4",
            "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
            "NUMLOCK", "SCROLLLOCK", "CAPSLOCK", "PRINTSCREEN",
            "NON-US-BACKSLASH", "NONUSHASH"
        }
        
        # Standard modifiers
        self.modifiers = {"LSHIFT", "RSHIFT", "LCTRL", "RCTRL", "LALT", "RALT", "LMETA", "RMETA"}
        
        # Common layout templates
        self.layout_templates = {
            "qwerty": self._get_qwerty_template(),
            "azerty": self._get_azerty_template(),
            "qwertz": self._get_qwertz_template()
        }

    def _get_qwerty_template(self) -> Dict[str, List]:
        """Get QWERTY base template."""
        return {
            # Control characters
            "\r": [None, None],
            "\t": ["TAB", []],
            " ": ["SPACE", []],
            "\n": ["ENTER", []],
            
            # Numbers row
            "`": ["BACKQUOTE", []],
            "1": ["1", []],
            "2": ["2", []],
            "3": ["3", []],
            "4": ["4", []],
            "5": ["5", []],
            "6": ["6", []],
            "7": ["7", []],
            "8": ["8", []],
            "9": ["9", []],
            "0": ["0", []],
            "-": ["MINUS", []],
            "=": ["EQUALS", []],
            
            # Top row
            "q": ["Q", []],
            "w": ["W", []],
            "e": ["E", []],
            "r": ["R", []],
            "t": ["T", []],
            "y": ["Y", []],
            "u": ["U", []],
            "i": ["I", []],
            "o": ["O", []],
            "p": ["P", []],
            "[": ["LEFTBRACKET", []],
            "]": ["RIGHTBRACKET", []],
            "\\": ["BACKSLASH", []],
            
            # Home row
            "a": ["A", []],
            "s": ["S", []],
            "d": ["D", []],
            "f": ["F", []],
            "g": ["G", []],
            "h": ["H", []],
            "j": ["J", []],
            "k": ["K", []],
            "l": ["L", []],
            ";": ["SEMICOLON", []],
            "'": ["QUOTE", []],
            
            # Bottom row
            "z": ["Z", []],
            "x": ["X", []],
            "c": ["C", []],
            "v": ["V", []],
            "b": ["B", []],
            "n": ["N", []],
            "m": ["M", []],
            ",": ["COMMA", []],
            ".": ["PERIOD", []],
            "/": ["SLASH", []]
        }

    def _get_azerty_template(self) -> Dict[str, List]:
        """Get AZERTY base template (French layout)."""
        template = self._get_qwerty_template()
        
        # Modify for AZERTY layout
        azerty_changes = {
            # Top row changes
            "a": ["Q", []],  # A is where Q was
            "z": ["W", []],  # Z is where W was
            "q": ["A", []],  # Q is where A was
            "w": ["Z", []],  # W is where Z was
            
            # Numbers row (French specific)
            "&": ["1", []],
            "é": ["2", []],
            "\"": ["3", []],
            "'": ["4", []],
            "(": ["5", []],
            "-": ["6", []],
            "è": ["7", []],
            "_": ["8", []],
            "ç": ["9", []],
            "à": ["0", []],
            ")": ["MINUS", []],
            "=": ["EQUALS", []],
            
            # Special French characters
            "ù": ["QUOTE", []],
            "^": ["LEFTBRACKET", []],
            "$": ["RIGHTBRACKET", []],
            "*": ["BACKSLASH", []],
            "m": ["SEMICOLON", []],
            "%": ["COMMA", []],
            "µ": ["NONUSHASH", []],
            "<": ["NON-US-BACKSLASH", []]
        }
        
        template.update(azerty_changes)
        return template

    def _get_qwertz_template(self) -> Dict[str, List]:
        """Get QWERTZ base template (German layout)."""
        template = self._get_qwerty_template()
        
        # Modify for QWERTZ layout
        qwertz_changes = {
            # Y and Z swapped
            "z": ["Y", []],
            "y": ["Z", []],
            
            # German specific characters
            "ü": ["LEFTBRACKET", []],
            "+": ["RIGHTBRACKET", []],
            "ö": ["SEMICOLON", []],
            "ä": ["QUOTE", []],
            "#": ["BACKSLASH", []],
            "<": ["NON-US-BACKSLASH", []],
            "ß": ["MINUS", []],
            "´": ["EQUALS", []]
        }
        
        template.update(qwertz_changes)
        return template

    def create_layout(self, layout_name: str, base_template: str = "qwerty", 
                     custom_mappings: Optional[Dict[str, List]] = None) -> Dict[str, List]:
        """Create a new keyboard layout."""
        if base_template not in self.layout_templates:
            raise ValueError(f"Unknown template: {base_template}. Available: {list(self.layout_templates.keys())}")
        
        layout = self.layout_templates[base_template].copy()
        
        if custom_mappings:
            layout.update(custom_mappings)
        
        # Add shifted versions for letters
        shifted_layout = {}
        for char, mapping in layout.items():
            if len(char) == 1 and char.isalpha() and char.islower():
                shifted_layout[char.upper()] = [mapping[0], ["LSHIFT"]]
        
        layout.update(shifted_layout)
        
        return layout

    def validate_layout(self, layout: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate a keyboard layout."""
        errors = []
        
        if not isinstance(layout, dict):
            errors.append("Layout must be a dictionary")
            return False, errors
        
        for char, mapping in layout.items():
            if not isinstance(char, str):
                errors.append(f"Character key must be string, got {type(char)}")
                continue
                
            if mapping is None or (isinstance(mapping, list) and len(mapping) == 2 and mapping[0] is None):
                continue  # Special null mapping
                
            if not isinstance(mapping, list) or len(mapping) != 2:
                errors.append(f"Mapping for '{char}' must be [key, modifiers] list")
                continue
                
            key, modifiers = mapping
            
            if key is not None and key not in self.hid_keys:
                errors.append(f"Unknown HID key '{key}' for character '{char}'")
                
            if not isinstance(modifiers, list):
                errors.append(f"Modifiers for '{char}' must be a list")
                continue
                
            for mod in modifiers:
                if mod not in self.modifiers:
                    errors.append(f"Unknown modifier '{mod}' for character '{char}'")
        
        return len(errors) == 0, errors

    def save_layout(self, layout: Dict[str, List], filename: str) -> bool:
        """Save layout to JSON file."""
        try:
            filepath = self.keymaps_dir / filename
            self.keymaps_dir.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(layout, f, indent=4, ensure_ascii=False, sort_keys=True)
            
            print(f"Layout saved to {filepath}")
            return True
        except Exception as e:
            print(f"Error saving layout: {e}")
            return False

    def load_layout(self, filename: str) -> Optional[Dict[str, List]]:
        """Load layout from JSON file."""
        try:
            filepath = self.keymaps_dir / filename
            with open(filepath, encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading layout: {e}")
            return None

    def list_layouts(self) -> List[str]:
        """List all available layouts."""
        if not self.keymaps_dir.exists():
            return []
        
        return [f.name for f in self.keymaps_dir.glob("*.json")]

    def test_layout(self, layout: Dict[str, List], test_text: str = None) -> bool:
        """Test a layout with sample text."""
        if test_text is None:
            test_text = "Hello World! 123 @#$%"
        
        print(f"Testing layout with text: '{test_text}'")
        
        missing_chars = []
        for char in test_text:
            if char not in layout:
                missing_chars.append(char)
        
        if missing_chars:
            print(f"Missing character mappings: {missing_chars}")
            return False
        
        print("Layout test passed!")
        return True


def main():
    parser = argparse.ArgumentParser(description="RelayKeys Keyboard Layout Converter")
    parser.add_argument("--create-layout", help="Create a new layout with given name")
    parser.add_argument("--template", default="qwerty", choices=["qwerty", "azerty", "qwertz"],
                       help="Base template for new layout")
    parser.add_argument("--validate-layout", help="Validate an existing layout file")
    parser.add_argument("--list-layouts", action="store_true", help="List all available layouts")
    parser.add_argument("--test-layout", help="Test a layout file")
    parser.add_argument("--test-text", help="Custom text for layout testing")
    
    args = parser.parse_args()
    
    converter = KeyboardLayoutConverter()
    
    if args.list_layouts:
        layouts = converter.list_layouts()
        print("Available layouts:")
        for layout in layouts:
            print(f"  - {layout}")
        return
    
    if args.validate_layout:
        layout = converter.load_layout(args.validate_layout)
        if layout is None:
            sys.exit(1)
        
        is_valid, errors = converter.validate_layout(layout)
        if is_valid:
            print(f"Layout {args.validate_layout} is valid!")
        else:
            print(f"Layout {args.validate_layout} has errors:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        return
    
    if args.test_layout:
        layout = converter.load_layout(args.test_layout)
        if layout is None:
            sys.exit(1)
        
        success = converter.test_layout(layout, args.test_text)
        if not success:
            sys.exit(1)
        return
    
    if args.create_layout:
        print(f"Creating layout '{args.create_layout}' based on '{args.template}' template...")
        
        # This is a basic implementation - in practice, you'd want to add
        # specific character mappings for each language
        layout = converter.create_layout(args.create_layout, args.template)
        
        is_valid, errors = converter.validate_layout(layout)
        if not is_valid:
            print("Generated layout has errors:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        
        filename = f"{args.create_layout}_keymap.json"
        if converter.save_layout(layout, filename):
            print(f"Layout created successfully: {filename}")
        else:
            sys.exit(1)
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
