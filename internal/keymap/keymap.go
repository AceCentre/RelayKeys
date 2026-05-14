package keymap

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
)

type KeymapEntry struct {
	Key        string
	Modifiers  []string
}

type Keymap map[rune]KeymapEntry

var active Keymap

func Load(name string) error {
	if name == "" {
		name = "us_keymap.json"
	}

	paths := []string{}

	exePath, err := os.Executable()
	if err == nil {
		exeDir := filepath.Dir(exePath)
		paths = append(paths,
			filepath.Join(exeDir, "keymaps", name),
			filepath.Join(exeDir, "..", "keymaps", name),
		)
	}

	_, thisFile, _, _ := runtime.Caller(0)
	thisDir := filepath.Dir(thisFile)
	paths = append(paths,
		filepath.Join(thisDir, "..", "..", "keymaps", name),
		filepath.Join(thisDir, "keymaps", name),
	)

	if runtime.GOOS == "windows" {
		appData := os.Getenv("APPDATA")
		if appData != "" {
			paths = append(paths, filepath.Join(appData, "RelayKeys", "keymaps", name))
		}
	}

	home, _ := os.UserHomeDir()
	if home != "" {
		paths = append(paths,
			filepath.Join(home, ".relaykeys", "keymaps", name),
			filepath.Join(home, ".config", "relaykeys", "keymaps", name),
		)
	}

	paths = append(paths, name)

	for _, p := range paths {
		data, err := os.ReadFile(p)
		if err != nil {
			continue
		}
		km, err := parseKeymapJSON(data)
		if err != nil {
			return fmt.Errorf("failed to parse keymap %s: %w", p, err)
		}
		active = km
		return nil
	}

	return fmt.Errorf("keymap file not found: %s (searched: %v)", name, paths)
}

func parseKeymapJSON(data []byte) (Keymap, error) {
	var raw map[string]interface{}
	if err := json.Unmarshal(data, &raw); err != nil {
		return nil, err
	}

	km := make(Keymap, len(raw))
	for charStr, val := range raw {
		runes := []rune(charStr)
		if len(runes) != 1 {
			continue
		}
		ch := runes[0]

		arr, ok := val.([]interface{})
		if !ok || len(arr) < 2 {
			continue
		}

		var key string
		if arr[0] == nil {
			continue
		}
		key, ok = arr[0].(string)
		if !ok {
			continue
		}

		var mods []string
		modArr, ok := arr[1].([]interface{})
		if ok {
			for _, m := range modArr {
				if ms, ok := m.(string); ok {
					mods = append(mods, ms)
				}
			}
		}

		km[ch] = KeymapEntry{Key: key, Modifiers: mods}
	}

	return km, nil
}

func CharToKeyevent(ch rune) (string, []string) {
	if active == nil {
		_ = Load("us_keymap.json")
	}

	if entry, ok := active[ch]; ok {
		return entry.Key, entry.Modifiers
	}

	if ch >= 'a' && ch <= 'z' {
		return string(rune(ch - 32)), nil
	}
	if ch >= 'A' && ch <= 'Z' {
		return string(ch), []string{"LSHIFT"}
	}
	if ch >= '0' && ch <= '9' {
		return string(ch), nil
	}

	return "", nil
}

func Active() Keymap {
	return active
}
