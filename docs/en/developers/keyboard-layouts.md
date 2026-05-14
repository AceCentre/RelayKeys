# Keyboard Layouts

RelayKeys supports multiple keyboard layouts to accommodate users from different regions and language preferences. This document describes the available layouts and how to use them.

## Available Layouts

| File                    | Layout             | Special characters                        |
|-------------------------|--------------------|---------------------------------------------|
| `us_keymap.json`        | US QWERTY          | Standard US English                         |
| `uk_keymap.json`        | UK QWERTY          | £ symbol and UK-specific characters         |
| `de_keymap.json`        | German QWERTZ      | ä, ö, ü, ß and German characters            |
| `fr_azerty_keymap.json` | French AZERTY      | é, è, ç, à, ù, €, £, ², °                  |
| `es_qwerty_keymap.json` | Spanish QWERTY     | ñ, ¿, ¡, á, é, í, ó, ú, €                  |
| `it_qwerty_keymap.json` | Italian QWERTY     | à, è, ì, ò, ù, €, £, °, §                  |

## Using a Keyboard Layout

Set the layout in your `relaykeys.cfg`:

```ini
[cli]
keymap_file = fr_azerty_keymap.json
```

Restart the daemon for the change to take effect.

You can also switch layouts at runtime via the CLI:

```bash
relaykeys-cli.exe ble_cmd:keymap:fr_azerty_keymap.json
```

## Layout File Format

Each layout is a JSON file in the `keymaps/` directory mapping characters to HID key codes and modifiers:

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
- **character** — the Unicode character to be typed
- **HID_KEY** — the HID keyboard code (e.g., `A`, `1`, `SPACE`)
- **MODIFIER** — list of modifier keys (e.g., `LSHIFT`, `RALT`, `LCTRL`)

### HID Key Codes

RelayKeys uses standard USB HID key codes:

- **Letters**: A–Z
- **Numbers**: 0–9
- **Modifiers**: LSHIFT, RSHIFT, LCTRL, RCTRL, LALT, RALT, LMETA, RMETA
- **Special keys**: SPACE, ENTER, TAB, BACKSPACE, DELETE, ESCAPE
- **Function keys**: F1–F12
- **Arrow keys**: LEFTARROW, RIGHTARROW, UPARROW, DOWNARROW
- **Symbols**: COMMA, PERIOD, SLASH, SEMICOLON, QUOTE, etc.

## Testing Layouts

```bash
# Run all tests (includes keymap tests)
go test ./... -count=1

# Run just the keymap tests
go test ./internal/keymap/ -count=1 -v
```

### Manual Testing

1. **Basic characters**: Test a–z, A–Z, 0–9
2. **Special characters**: Test language-specific characters (é, ñ, ü, etc.)
3. **Symbols**: Test common symbols (@, #, $, %, etc.)
4. **Modifiers**: Test Shift, Alt, Ctrl combinations

## Troubleshooting

### Layout Not Working

1. Check that `keymap_file` in `relaykeys.cfg` points to the correct file
2. Verify the file exists in the `keymaps/` directory
3. Validate the JSON with a linter (e.g., https://jsonlint.com)
4. Ensure the file is saved with UTF-8 encoding

### Missing Characters

Characters not in the layout will produce an error when typed. Add custom mappings to the layout file as needed.

### Wrong Characters Typed

1. Ensure the RelayKeys keymap matches the keyboard layout of the target BLE device
2. Verify that modifier keys (Shift, Alt) are correctly mapped in the layout file

## Contributing New Layouts

To contribute a new keyboard layout:

1. Create a new JSON file in `keymaps/` following the naming pattern `{language}_{variant}_keymap.json`
2. Include all standard characters: letters, numbers, symbols, and language-specific characters
3. Uppercase letters must use the `LSHIFT` modifier
4. Save with UTF-8 encoding
5. Run `go test ./internal/keymap/` to verify
6. Submit a pull request

### Layout Requirements

- **Complete coverage**: Include all standard keyboard characters
- **Correct modifiers**: Uppercase letters must use LSHIFT modifier
- **Valid JSON**: Layout must be valid JSON with proper UTF-8 encoding
- **Consistent naming**: Use the pattern `{language}_{variant}_keymap.json`
