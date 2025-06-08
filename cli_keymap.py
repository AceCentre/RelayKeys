import json
from pathlib import Path

nonchars_key_map = None


def load_keymap_file(config):
    global nonchars_key_map

    keymap_file = (
        Path(__file__).resolve().parent
        / "cli_keymaps"
        / config.get("keymap_file", "us_keymap.json")
    )
    if keymap_file.exists() and keymap_file.is_file():
        with open(keymap_file, encoding="utf-8") as f:
            try:
                nonchars_key_map = json.loads(f.read())
            except Exception as e:
                print("Invalid keymap json file:", e)
                return
    else:
        print("Invalid path to keymap file:", keymap_file)
        return False

    return True


def char_to_keyevent_params(char):
    global nonchars_key_map

    ret = nonchars_key_map.get(char, None)
    if ret is not None:
        return ret
    if char.isdigit():
        return (char, [])
    if char.upper() == char:
        return (char.upper(), ["LSHIFT"])
    return (char.upper(), [])
