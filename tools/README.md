# RelayKeys Layout Tools

This directory contains tools for creating, managing, and converting keyboard layouts for RelayKeys.

## Tools Overview

### 1. Layout Generator (`generate_layouts.py`)

Generates keyboard layout JSON files from predefined layout definitions.

**Usage:**
```bash
# Generate all predefined layouts
uv run python generate_layouts.py all

# Generate a specific layout
uv run python generate_layouts.py fr_azerty

# Show layout information
uv run python generate_layouts.py info fr_azerty

# List available layouts
uv run python generate_layouts.py list
```

**Available Layouts:**
- `fr_azerty` - French AZERTY keyboard layout
- `es_qwerty` - Spanish QWERTY keyboard layout  
- `it_qwerty` - Italian QWERTY keyboard layout

### 2. Layout Converter (`layout_converter.py`)

A comprehensive tool for creating, validating, and testing keyboard layouts.

**Usage:**
```bash
# Create a new layout from a template
uv run python layout_converter.py --create-layout my_layout --template qwerty

# Validate an existing layout
uv run python layout_converter.py --validate-layout us_keymap.json

# Test a layout with sample text
uv run python layout_converter.py --test-layout fr_azerty_keymap.json

# List all available layouts
uv run python layout_converter.py --list-layouts
```

**Templates:**
- `qwerty` - Standard QWERTY layout (US/UK style)
- `azerty` - French AZERTY layout
- `qwertz` - German QWERTZ layout

### 3. Layout Definitions (`layout_definitions.py`)

Contains detailed character mappings for specific keyboard layouts. This is where new layouts are defined.

**Adding a New Layout:**
1. Add a function like `get_mylang_layout()` that returns a dictionary of character mappings
2. Add the layout to the `LAYOUT_REGISTRY` dictionary
3. Test the layout using the converter tools

## Layout File Format

Keyboard layouts are stored as JSON files with the following structure:

```json
{
    "character": ["HID_KEY", ["MODIFIER1", "MODIFIER2"]],
    "a": ["A", []],
    "A": ["A", ["LSHIFT"]],
    "é": ["2", ["RALT"]],
    " ": ["SPACE", []],
    "\r": [null, null]
}
```

**Key Components:**
- **Character**: The Unicode character to be typed
- **HID_KEY**: The HID keyboard code (e.g., "A", "1", "SPACE")
- **Modifiers**: List of modifier keys (e.g., "LSHIFT", "RALT", "LCTRL")

## Supported HID Keys

The tools support all standard HID keyboard codes:

**Letters**: A-Z  
**Numbers**: 0-9  
**Modifiers**: LSHIFT, RSHIFT, LCTRL, RCTRL, LALT, RALT, LMETA, RMETA  
**Special Keys**: SPACE, ENTER, TAB, BACKSPACE, DELETE, ESCAPE  
**Function Keys**: F1-F12  
**Arrow Keys**: LEFTARROW, RIGHTARROW, UPARROW, DOWNARROW  
**Symbols**: COMMA, PERIOD, SLASH, SEMICOLON, QUOTE, etc.

## Examples

### Generate French Layout
```bash
uv run python generate_layouts.py fr_azerty
```

This creates `fr_azerty_keymap.json` with French AZERTY mappings including:
- é, è, à, ç, ù (accented characters)
- €, £, ², ³ (special symbols)
- Proper AZERTY key positioning (a/q, z/w swapped)

### Validate a Layout
```bash
uv run python layout_converter.py --validate-layout fr_azerty_keymap.json
```

Checks for:
- Valid JSON structure
- Correct HID key codes
- Valid modifier combinations
- Proper character encoding

### Test a Layout
```bash
uv run python layout_converter.py --test-layout fr_azerty_keymap.json --test-text "Bonjour! Comment ça va?"
```

Tests that all characters in the text can be properly mapped.

## Creating Custom Layouts

### Method 1: Using Templates
```bash
# Create a new layout based on QWERTY
uv run python layout_converter.py --create-layout my_custom --template qwerty
```

### Method 2: Define in Code
1. Edit `layout_definitions.py`
2. Add your layout function:
```python
def get_my_language_layout() -> Dict[str, List]:
    return {
        "a": ["A", []],
        "á": ["A", ["RALT"]],
        # ... more mappings
    }
```
3. Add to registry:
```python
LAYOUT_REGISTRY = {
    # ... existing layouts
    "my_language": get_my_language_layout,
}
```
4. Generate the layout:
```bash
uv run python generate_layouts.py my_language
```

## Testing

Run the test suite to verify all layouts:

```bash
# Test all keyboard layout functionality
uv run python -m pytest tests/test_cli_keymap.py::TestKeyboardLayouts -v

# Test specific layout validation
uv run python -m pytest tests/test_cli_keymap.py::TestKeyboardLayouts::test_layout_validation -v
```

## Troubleshooting

### Layout Not Generated
- Check that the layout function is properly defined
- Verify the layout is added to `LAYOUT_REGISTRY`
- Run validation to check for errors

### Invalid Characters
- Ensure all HID keys are supported (check `hid_keys` set in converter)
- Verify modifier combinations are valid
- Check Unicode character encoding

### Test Failures
- Run individual tests to isolate issues
- Check layout structure matches expected format
- Verify character coverage meets requirements

## Contributing

When adding new layouts:

1. **Research the layout** - Use official keyboard specifications
2. **Include all characters** - Letters, numbers, symbols, special characters
3. **Test thoroughly** - Validate and test with sample text
4. **Document usage** - Add examples and special character notes
5. **Follow naming conventions** - Use `{language}_{variant}_keymap.json`

## Future Enhancements

Planned improvements:
- GUI layout editor
- Import from other keyboard layout formats
- Layout auto-detection based on system locale
- Visual layout preview
- More comprehensive testing tools
