#!/usr/bin/env python3
"""
RelayKeys Layout Switcher

A utility to easily switch between different keyboard layouts by updating the configuration file.
"""

import argparse
import configparser
import sys
from pathlib import Path
from typing import List, Optional


class LayoutSwitcher:
    """Manages switching between keyboard layouts in RelayKeys."""
    
    def __init__(self):
        self.relaykeys_root = Path(__file__).parent.parent
        self.config_file = self.relaykeys_root / "relaykeys.cfg"
        self.keymaps_dir = self.relaykeys_root / "src" / "relaykeys" / "cli" / "keymaps"
        
        # Available layouts with descriptions
        self.layouts = {
            "us_keymap.json": "US English QWERTY",
            "uk_keymap.json": "UK English QWERTY", 
            "de_keymap.json": "German QWERTZ",
            "fr_azerty_keymap.json": "French AZERTY",
            "es_qwerty_keymap.json": "Spanish QWERTY",
            "it_qwerty_keymap.json": "Italian QWERTY"
        }

    def get_available_layouts(self) -> List[str]:
        """Get list of available layout files."""
        if not self.keymaps_dir.exists():
            return []
        
        available = []
        for layout_file in self.layouts.keys():
            if (self.keymaps_dir / layout_file).exists():
                available.append(layout_file)
        
        return available

    def get_current_layout(self) -> Optional[str]:
        """Get the currently configured layout."""
        if not self.config_file.exists():
            return None
        
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file)
            
            if 'cli' in config and 'keymap_file' in config['cli']:
                return config['cli']['keymap_file']
        except Exception as e:
            print(f"Error reading config file: {e}")
        
        return None

    def set_layout(self, layout_file: str) -> bool:
        """Set the keyboard layout in the configuration file."""
        if not self.config_file.exists():
            print(f"Configuration file not found: {self.config_file}")
            return False
        
        if layout_file not in self.get_available_layouts():
            print(f"Layout file not found: {layout_file}")
            return False
        
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file)
            
            # Ensure [cli] section exists
            if 'cli' not in config:
                config.add_section('cli')
            
            # Set the keymap file
            config['cli']['keymap_file'] = layout_file
            
            # Write back to file
            with open(self.config_file, 'w') as f:
                config.write(f)
            
            print(f"✅ Layout switched to: {layout_file}")
            print(f"   Description: {self.layouts.get(layout_file, 'Unknown')}")
            print("\n⚠️  Please restart RelayKeys for the change to take effect.")
            return True
            
        except Exception as e:
            print(f"Error updating config file: {e}")
            return False

    def list_layouts(self):
        """List all available layouts."""
        available = self.get_available_layouts()
        current = self.get_current_layout()
        
        print("Available keyboard layouts:")
        print("=" * 50)
        
        for layout_file in available:
            description = self.layouts.get(layout_file, "Unknown")
            status = " (CURRENT)" if layout_file == current else ""
            print(f"  {layout_file:<25} - {description}{status}")
        
        if not available:
            print("  No layouts found!")
        
        print(f"\nLayouts directory: {self.keymaps_dir}")
        if current:
            print(f"Current layout: {current}")
        else:
            print("Current layout: Not configured")

    def show_layout_info(self, layout_file: str):
        """Show detailed information about a specific layout."""
        if layout_file not in self.get_available_layouts():
            print(f"Layout not found: {layout_file}")
            return
        
        description = self.layouts.get(layout_file, "Unknown")
        layout_path = self.keymaps_dir / layout_file
        
        print(f"Layout Information: {layout_file}")
        print("=" * 50)
        print(f"Description: {description}")
        print(f"File path: {layout_path}")
        print(f"File size: {layout_path.stat().st_size} bytes")
        
        # Try to load and show some stats
        try:
            import json
            with open(layout_path, 'r', encoding='utf-8') as f:
                layout_data = json.load(f)
            
            total_chars = len(layout_data)
            letters = sum(1 for char in layout_data.keys() if len(char) == 1 and char.isalpha())
            digits = sum(1 for char in layout_data.keys() if len(char) == 1 and char.isdigit())
            symbols = total_chars - letters - digits
            
            print(f"Total characters: {total_chars}")
            print(f"  Letters: {letters}")
            print(f"  Digits: {digits}")
            print(f"  Symbols/Special: {symbols}")
            
            # Show some sample characters
            sample_chars = []
            for char in sorted(layout_data.keys()):
                if len(char) == 1 and not char.isascii():
                    sample_chars.append(char)
                if len(sample_chars) >= 10:
                    break
            
            if sample_chars:
                print(f"Special characters: {' '.join(sample_chars)}")
                
        except Exception as e:
            print(f"Could not analyze layout file: {e}")

    def test_layout(self, layout_file: str, test_text: str = None):
        """Test a layout with sample text."""
        if layout_file not in self.get_available_layouts():
            print(f"Layout not found: {layout_file}")
            return
        
        # Import the layout converter
        sys.path.insert(0, str(Path(__file__).parent))
        try:
            from layout_converter import KeyboardLayoutConverter
            
            converter = KeyboardLayoutConverter()
            layout_path = self.keymaps_dir / layout_file
            
            # Load the layout
            layout_data = converter.load_layout(layout_file)
            if layout_data is None:
                print(f"Failed to load layout: {layout_file}")
                return
            
            # Use default test text if none provided
            if test_text is None:
                # Choose appropriate test text based on layout
                if "fr_" in layout_file:
                    test_text = "Bonjour! Comment ça va? 123 €àéèù"
                elif "es_" in layout_file:
                    test_text = "¡Hola! ¿Cómo estás? 123 €ñáéíóú"
                elif "it_" in layout_file:
                    test_text = "Ciao! Come stai? 123 €àèìòù"
                elif "de_" in layout_file:
                    test_text = "Hallo! Wie geht's? 123 €äöüß"
                else:
                    test_text = "Hello World! 123 @#$%^&*()"
            
            print(f"Testing layout: {layout_file}")
            print(f"Test text: '{test_text}'")
            print("-" * 50)
            
            success = converter.test_layout(layout_data, test_text)
            if success:
                print("✅ Layout test passed!")
            else:
                print("❌ Layout test failed!")
                
        except ImportError:
            print("Layout testing tools not available")


def main():
    parser = argparse.ArgumentParser(description="RelayKeys Layout Switcher")
    parser.add_argument("--list", action="store_true", help="List available layouts")
    parser.add_argument("--current", action="store_true", help="Show current layout")
    parser.add_argument("--set", help="Set keyboard layout")
    parser.add_argument("--info", help="Show information about a layout")
    parser.add_argument("--test", help="Test a layout with sample text")
    parser.add_argument("--test-text", help="Custom text for layout testing")
    
    args = parser.parse_args()
    
    switcher = LayoutSwitcher()
    
    if args.list:
        switcher.list_layouts()
        return
    
    if args.current:
        current = switcher.get_current_layout()
        if current:
            print(f"Current layout: {current}")
            description = switcher.layouts.get(current, "Unknown")
            print(f"Description: {description}")
        else:
            print("No layout currently configured")
        return
    
    if args.set:
        success = switcher.set_layout(args.set)
        if not success:
            sys.exit(1)
        return
    
    if args.info:
        switcher.show_layout_info(args.info)
        return
    
    if args.test:
        switcher.test_layout(args.test, args.test_text)
        return
    
    # No arguments provided, show help
    parser.print_help()


if __name__ == "__main__":
    main()
