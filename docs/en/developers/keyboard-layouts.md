# Keyboard Layouts

RelayKeys supports multiple keyboard layouts to accommodate users from different regions and language preferences. This document describes the available layouts and how to use them.

## Available Layouts

### Current Layouts

- **US QWERTY** (`us_keymap.json`) - Standard US English keyboard layout
- **UK QWERTY** (`uk_keymap.json`) - UK English keyboard layout with £ symbol and other UK-specific characters
- **German QWERTZ** (`de_keymap.json`) - German keyboard layout with ä, ö, ü, ß and other German characters

### New Layouts (Added in this update)

- **French AZERTY** (`fr_azerty_keymap.json`) - Standard French keyboard layout with é, è, ç, à and other French characters
- **Spanish QWERTY** (`es_qwerty_keymap.json`) - Spanish keyboard layout with ñ, ¿, ¡ and other Spanish characters  
- **Italian QWERTY** (`it_qwerty_keymap.json`) - Italian keyboard layout with à, è, ì, ò, ù and other Italian characters

## Using a Keyboard Layout

To use a specific keyboard layout:

1. **Edit your configuration file** (`relaykeys.cfg`):
   ```ini
   [cli]
   keymap_file = fr_azerty_keymap.json
   ```

2. **Restart RelayKeys** for the changes to take effect.

3. **Test the layout** by typing some text to ensure special characters work correctly.

## Layout Structure

Each keyboard layout is stored as a JSON file with the following structure:

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

Where:
- `character` is the Unicode character to be typed
- `HID_KEY` is the HID keyboard code (e.g., "A", "1", "SPACE")
- `MODIFIER` is a list of modifier keys (e.g., "LSHIFT", "RALT", "LCTRL")

## Special Characters by Layout

### French AZERTY
- **Accented vowels**: é, è, à, ç, ù
- **Special symbols**: €, £, ², ³, °
- **Punctuation**: « » (French quotes)

### Spanish QWERTY  
- **Special characters**: ñ, Ñ
- **Inverted punctuation**: ¿, ¡
- **Accented vowels**: á, é, í, ó, ú
- **Special symbols**: €, £

### Italian QWERTY
- **Accented vowels**: à, è, ì, ò, ù
- **Special symbols**: €, £, °, §
- **Punctuation**: « »

## Creating Custom Layouts

You can create custom keyboard layouts using the provided tools:

### Using the Layout Generator

```bash
# Generate a new layout based on a template
python tools/generate_layouts.py fr_azerty

# Generate all predefined layouts
python tools/generate_layouts.py all

# Show information about a layout
python tools/generate_layouts.py info fr_azerty

# List available layouts
python tools/generate_layouts.py list
```

### Using the Layout Converter

```bash
# Create a new layout from scratch
python tools/layout_converter.py --create-layout my_custom_layout --template qwerty

# Validate an existing layout
python tools/layout_converter.py --validate-layout my_layout.json

# Test a layout with sample text
python tools/layout_converter.py --test-layout my_layout.json --test-text "Hello World!"

# List all available layouts
python tools/layout_converter.py --list-layouts
```

## Testing Layouts

### Automated Testing

Run the test suite to verify all layouts:

```bash
# Test all keyboard layouts
python -m pytest tests/test_cli_keymap.py::TestKeyboardLayouts -v

# Test specific layout functionality
python -m pytest tests/test_cli_keymap.py::TestKeyboardLayouts::test_layout_validation -v
```

### Manual Testing

1. **Basic characters**: Test a-z, A-Z, 0-9
2. **Special characters**: Test language-specific characters (é, ñ, ü, etc.)
3. **Symbols**: Test common symbols (@, #, $, %, etc.)
4. **Modifiers**: Test Shift, Alt, Ctrl combinations
5. **Function keys**: Test F1-F12, arrow keys, etc.

## Troubleshooting

### Layout Not Working

1. **Check configuration**: Ensure the `keymap_file` setting in `relaykeys.cfg` points to the correct file
2. **Verify file exists**: Check that the layout file exists in the `src/relaykeys/cli/keymaps/` directory
3. **Validate JSON**: Use a JSON validator to ensure the layout file is valid JSON
4. **Check encoding**: Ensure the file is saved with UTF-8 encoding

### Missing Characters

1. **Check layout coverage**: Some layouts may not include all characters
2. **Use fallback**: Characters not in the layout will use the default US mapping
3. **Add custom mappings**: Edit the layout file to add missing characters

### Wrong Characters Typed

1. **Check system layout**: Ensure your system keyboard layout matches the RelayKeys layout
2. **Verify modifiers**: Check that modifier keys (Shift, Alt) are correctly mapped
3. **Test with simple characters**: Start with basic a-z characters before testing special characters

## Contributing New Layouts

To contribute a new keyboard layout:

1. **Create the layout definition** in `tools/layout_definitions.py`
2. **Add comprehensive character mappings** including:
   - All letters (lowercase and uppercase)
   - Numbers and symbols
   - Language-specific characters
   - Common punctuation
3. **Test thoroughly** with the provided test suite
4. **Document the layout** including special characters and usage notes
5. **Submit a pull request** with your changes

### Layout Requirements

- **Complete coverage**: Include all standard keyboard characters
- **Correct modifiers**: Uppercase letters must use LSHIFT modifier
- **Valid JSON**: Layout must be valid JSON with proper encoding
- **Consistent naming**: Use the pattern `{language}_{variant}_keymap.json`
- **Documentation**: Include usage examples and special character notes

## Technical Details

### HID Key Codes

RelayKeys uses standard USB HID key codes. Supported keys include:

- **Letters**: A-Z
- **Numbers**: 0-9  
- **Modifiers**: LSHIFT, RSHIFT, LCTRL, RCTRL, LALT, RALT, LMETA, RMETA
- **Special keys**: SPACE, ENTER, TAB, BACKSPACE, DELETE, ESCAPE
- **Function keys**: F1-F12
- **Arrow keys**: LEFTARROW, RIGHTARROW, UPARROW, DOWNARROW
- **Symbols**: COMMA, PERIOD, SLASH, SEMICOLON, QUOTE, etc.

### Modifier Combinations

- **LSHIFT/RSHIFT**: Shift key (for uppercase, symbols)
- **LALT/RALT**: Alt key (RALT often used for AltGr on international layouts)
- **LCTRL/RCTRL**: Control key
- **LMETA/RMETA**: Windows/Cmd key

### Character Encoding

- Layout files must be saved with **UTF-8 encoding**
- Unicode characters are supported in the JSON keys
- Special characters like newline use escape sequences (`\n`, `\r`, `\t`)

## Future Enhancements

Planned improvements for keyboard layout support:

- **More layouts**: Nordic languages (Swedish, Norwegian, Danish, Finnish)
- **Layout auto-detection**: Automatically detect system keyboard layout
- **GUI layout switcher**: Easy layout switching in the Qt application
- **Layout preview**: Visual representation of keyboard layouts
- **Custom layout editor**: GUI tool for creating and editing layouts
- **Layout validation**: Real-time validation and error checking
- **Import/export**: Support for importing layouts from other sources
