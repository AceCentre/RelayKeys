#!/usr/bin/env python3
"""
Generate keyboard layout files for RelayKeys.

This script creates the actual JSON keymap files from the layout definitions.
"""

import sys
from pathlib import Path

# Add the tools directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from layout_converter import KeyboardLayoutConverter
from layout_definitions import LAYOUT_REGISTRY, get_layout


def generate_all_layouts():
    """Generate all predefined layouts."""
    converter = KeyboardLayoutConverter()
    
    print("Generating keyboard layouts for RelayKeys...")
    print(f"Target directory: {converter.keymaps_dir}")
    
    # Ensure the keymaps directory exists
    converter.keymaps_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_count = len(LAYOUT_REGISTRY)
    
    for layout_name, layout_func in LAYOUT_REGISTRY.items():
        print(f"\nGenerating {layout_name}...")
        
        try:
            # Get the layout
            layout = layout_func()
            
            # Validate the layout
            is_valid, errors = converter.validate_layout(layout)
            if not is_valid:
                print(f"  ❌ Layout {layout_name} has validation errors:")
                for error in errors:
                    print(f"    - {error}")
                continue
            
            # Test the layout
            test_text = "Hello World! 123 @#$%^&*()_+-=[]{}|\\:;\"'<>,.?/"
            if not converter.test_layout(layout, test_text):
                print(f"  ⚠️  Layout {layout_name} failed basic testing")
                # Continue anyway, as some characters might be missing but layout could still be useful
            
            # Save the layout
            filename = f"{layout_name}_keymap.json"
            if converter.save_layout(layout, filename):
                print(f"  ✅ Successfully generated {filename}")
                success_count += 1
            else:
                print(f"  ❌ Failed to save {filename}")
                
        except Exception as e:
            print(f"  ❌ Error generating {layout_name}: {e}")
    
    print(f"\n📊 Summary: {success_count}/{total_count} layouts generated successfully")
    
    if success_count > 0:
        print("\n🎉 New layouts are ready to use!")
        print("To use a layout, update your relaykeys.cfg file:")
        print("  [cli]")
        print("  keymap_file = fr_azerty_keymap.json")
        print("\nAvailable layouts:")
        for layout_name in LAYOUT_REGISTRY.keys():
            filename = f"{layout_name}_keymap.json"
            if (converter.keymaps_dir / filename).exists():
                print(f"  - {filename}")


def generate_specific_layout(layout_name: str):
    """Generate a specific layout."""
    if layout_name not in LAYOUT_REGISTRY:
        print(f"❌ Unknown layout: {layout_name}")
        print(f"Available layouts: {list(LAYOUT_REGISTRY.keys())}")
        return False
    
    converter = KeyboardLayoutConverter()
    converter.keymaps_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating {layout_name}...")
    
    try:
        layout = get_layout(layout_name)
        
        # Validate
        is_valid, errors = converter.validate_layout(layout)
        if not is_valid:
            print("❌ Layout has validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        # Save
        filename = f"{layout_name}_keymap.json"
        if converter.save_layout(layout, filename):
            print(f"✅ Successfully generated {filename}")
            
            # Show some sample mappings
            print("\nSample character mappings:")
            sample_chars = ["a", "é", "ñ", "ç", "@", "€", "1", "!", "?"]
            for char in sample_chars:
                if char in layout:
                    mapping = layout[char]
                    if mapping[0] is None:
                        print(f"  '{char}' -> [null mapping]")
                    else:
                        mods = f" + {mapping[1]}" if mapping[1] else ""
                        print(f"  '{char}' -> {mapping[0]}{mods}")
            
            return True
        else:
            print(f"❌ Failed to save {filename}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating {layout_name}: {e}")
        return False


def show_layout_info(layout_name: str):
    """Show detailed information about a layout."""
    if layout_name not in LAYOUT_REGISTRY:
        print(f"❌ Unknown layout: {layout_name}")
        print(f"Available layouts: {list(LAYOUT_REGISTRY.keys())}")
        return
    
    layout = get_layout(layout_name)
    
    print(f"📋 Layout Information: {layout_name}")
    print(f"Total characters mapped: {len(layout)}")
    
    # Categorize characters
    letters = []
    numbers = []
    symbols = []
    special = []
    
    for char in layout.keys():
        if len(char) == 1:
            if char.isalpha():
                letters.append(char)
            elif char.isdigit():
                numbers.append(char)
            elif char.isprintable() and not char.isspace():
                symbols.append(char)
            else:
                special.append(char)
        else:
            special.append(char)
    
    print(f"  Letters: {len(letters)}")
    print(f"  Numbers: {len(numbers)}")
    print(f"  Symbols: {len(symbols)}")
    print(f"  Special: {len(special)}")
    
    # Show some examples
    if letters:
        print(f"\nSample letters: {sorted(letters)[:10]}")
    if symbols:
        print(f"Sample symbols: {sorted(symbols)[:15]}")
    
    # Check for common special characters
    special_chars = ["€", "£", "¥", "©", "®", "™", "°", "±", "×", "÷"]
    found_special = [char for char in special_chars if char in layout]
    if found_special:
        print(f"Special characters: {found_special}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python generate_layouts.py all                    # Generate all layouts")
        print("  python generate_layouts.py <layout_name>          # Generate specific layout")
        print("  python generate_layouts.py info <layout_name>     # Show layout info")
        print("  python generate_layouts.py list                   # List available layouts")
        print()
        print(f"Available layouts: {list(LAYOUT_REGISTRY.keys())}")
        return
    
    command = sys.argv[1]
    
    if command == "all":
        generate_all_layouts()
    elif command == "list":
        print("Available predefined layouts:")
        for layout_name in LAYOUT_REGISTRY.keys():
            print(f"  - {layout_name}")
    elif command == "info":
        if len(sys.argv) < 3:
            print("Usage: python generate_layouts.py info <layout_name>")
            return
        show_layout_info(sys.argv[2])
    elif command in LAYOUT_REGISTRY:
        generate_specific_layout(command)
    else:
        print(f"❌ Unknown command or layout: {command}")
        print(f"Available layouts: {list(LAYOUT_REGISTRY.keys())}")
        print("Use 'all' to generate all layouts, 'list' to list available layouts")


if __name__ == "__main__":
    main()
