package keymap

import (
	"os"
	"path/filepath"
	"testing"
)

func TestLoadUSKeymap(t *testing.T) {
	err := Load("us_keymap.json")
	if err != nil {
		t.Skipf("US keymap not found (expected in keymaps/): %v", err)
	}

	tests := []struct {
		char    rune
		wantKey string
		wantMod []string
	}{
		{'a', "A", nil},
		{'A', "A", []string{"LSHIFT"}},
		{'z', "Z", nil},
		{'0', "0", nil},
		{'9', "9", nil},
		{' ', "SPACE", nil},
		{'\n', "ENTER", []string{"LSHIFT"}},
		{'\t', "TAB", nil},
		{'!', "1", []string{"LSHIFT"}},
		{'@', "2", []string{"LSHIFT"}},
		{'#', "3", []string{"LSHIFT"}},
		{'$', "4", []string{"LSHIFT"}},
		{'%', "5", []string{"LSHIFT"}},
		{'^', "6", []string{"LSHIFT"}},
		{'&', "7", []string{"LSHIFT"}},
		{'*', "8", []string{"LSHIFT"}},
		{'(', "9", []string{"LSHIFT"}},
		{')', "0", []string{"LSHIFT"}},
		{'-', "MINUS", nil},
		{'=', "EQUALS", nil},
		{'[', "LEFTBRACKET", nil},
		{']', "RIGHTBRACKET", nil},
		{'\\', "BACKSLASH", nil},
		{';', "SEMICOLON", nil},
		{'\'', "QUOTE", nil},
		{'`', "BACKQUOTE", nil},
		{',', "COMMA", nil},
		{'.', "PERIOD", nil},
		{'/', "SLASH", nil},
		{'<', "COMMA", []string{"LSHIFT"}},
		{'>', "PERIOD", []string{"LSHIFT"}},
		{'?', "SLASH", []string{"LSHIFT"}},
		{':', "SEMICOLON", []string{"LSHIFT"}},
		{'"', "QUOTE", []string{"LSHIFT"}},
		{'{', "LEFTBRACKET", []string{"LSHIFT"}},
		{'}', "RIGHTBRACKET", []string{"LSHIFT"}},
		{'|', "BACKSLASH", []string{"LSHIFT"}},
		{'+', "EQUALS", []string{"LSHIFT"}},
		{'_', "MINUS", []string{"LSHIFT"}},
		{'~', "BACKQUOTE", []string{"LSHIFT"}},
	}

	for _, tt := range tests {
		key, mods := CharToKeyevent(tt.char)
		if key != tt.wantKey {
			t.Errorf("char %q: key expected %s, got %s", tt.char, tt.wantKey, key)
		}
		if !modsEqual(mods, tt.wantMod) {
			t.Errorf("char %q: mods expected %v, got %v", tt.char, tt.wantMod, mods)
		}
	}
}

func TestLoadUKKeymap(t *testing.T) {
	err := Load("uk_keymap.json")
	if err != nil {
		t.Skipf("UK keymap not found: %v", err)
	}

	key, mods := CharToKeyevent('@')
	if key != "QUOTE" || !modsEqual(mods, []string{"LSHIFT"}) {
		t.Errorf("UK @: expected QUOTE+[LSHIFT], got %s+%v", key, mods)
	}

	key, mods = CharToKeyevent('"')
	if key != "2" || !modsEqual(mods, []string{"LSHIFT"}) {
		t.Errorf("UK \": expected 2+[LSHIFT], got %s+%v", key, mods)
	}
}

func TestLoadDEKeymap(t *testing.T) {
	err := Load("de_keymap.json")
	if err != nil {
		t.Skipf("DE keymap not found: %v", err)
	}

	key, _ := CharToKeyevent('z')
	if key != "Y" {
		t.Errorf("DE z: expected Y, got %s", key)
	}

	key, _ = CharToKeyevent('y')
	if key != "Z" {
		t.Errorf("DE y: expected Z, got %s", key)
	}

	key, _ = CharToKeyevent('ü')
	if key != "LEFTBRACKET" {
		t.Errorf("DE ü: expected LEFTBRACKET, got %s", key)
	}

	key, _ = CharToKeyevent('ß')
	if key != "MINUS" {
		t.Errorf("DE ß: expected MINUS, got %s", key)
	}
}

func TestLoadNonexistent(t *testing.T) {
	err := Load("nonexistent_keymap.json")
	if err == nil {
		t.Error("expected error for nonexistent keymap")
	}
}

func TestCharToKeyeventFallback(t *testing.T) {
	active = nil

	key, mods := CharToKeyevent('h')
	if key != "H" {
		t.Errorf("fallback lowercase: expected H, got %s", key)
	}
	if len(mods) != 0 {
		t.Errorf("fallback lowercase: expected no mods, got %v", mods)
	}

	key, mods = CharToKeyevent('H')
	if key != "H" {
		t.Errorf("fallback uppercase: expected H, got %s", key)
	}
	if !modsEqual(mods, []string{"LSHIFT"}) {
		t.Errorf("fallback uppercase: expected LSHIFT, got %v", mods)
	}

	key, mods = CharToKeyevent('5')
	if key != "5" {
		t.Errorf("fallback digit: expected 5, got %s", key)
	}

	key, _ = CharToKeyevent('\r')
	if key != "" {
		t.Errorf("fallback CR: expected empty key, got %s", key)
	}
}

func TestAllKeymapFilesExist(t *testing.T) {
	keymaps := []string{
		"us_keymap.json",
		"uk_keymap.json",
		"de_keymap.json",
		"fr_azerty_keymap.json",
		"es_qwerty_keymap.json",
		"it_qwerty_keymap.json",
	}

	for _, km := range keymaps {
		t.Run(km, func(t *testing.T) {
			err := Load(km)
			if err != nil {
				t.Errorf("failed to load %s: %v", km, err)
			}
		})
	}
}

func TestKeymapParseJSON(t *testing.T) {
	jsonData := `{
		"a": ["A", []],
		"B": ["B", ["LSHIFT"]],
		"@": ["2", ["LSHIFT"]],
		" ": ["SPACE", []],
		"\n": ["ENTER", []]
	}`

	tmpDir := t.TempDir()
	tmpFile := filepath.Join(tmpDir, "test_keymap.json")
	os.WriteFile(tmpFile, []byte(jsonData), 0644)

	active = nil
	err := Load(tmpFile)
	if err != nil {
		t.Fatalf("Load: %v", err)
	}

	key, mods := CharToKeyevent('a')
	if key != "A" || len(mods) != 0 {
		t.Errorf("a: expected A/[], got %s/%v", key, mods)
	}

	key, mods = CharToKeyevent('B')
	if key != "B" || !modsEqual(mods, []string{"LSHIFT"}) {
		t.Errorf("B: expected B/[LSHIFT], got %s/%v", key, mods)
	}

	key, mods = CharToKeyevent('@')
	if key != "2" || !modsEqual(mods, []string{"LSHIFT"}) {
		t.Errorf("@: expected 2/[LSHIFT], got %s/%v", key, mods)
	}

	key, mods = CharToKeyevent(' ')
	if key != "SPACE" {
		t.Errorf("space: expected SPACE, got %s", key)
	}

	key, _ = CharToKeyevent('\n')
	if key != "ENTER" {
		t.Errorf("newline: expected ENTER, got %s", key)
	}
}

func modsEqual(a, b []string) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}
