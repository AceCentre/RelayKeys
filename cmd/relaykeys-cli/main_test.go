package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestLoadMacroFromFile(t *testing.T) {
	dir := t.TempDir()
	macroPath := filepath.Join(dir, "test_macro.txt")
	content := "keypress:H,LMETA\nkeypress:SPACE,LMETA\ntype:notes\ndelay:500\nkeypress:ENTER\n"
	os.WriteFile(macroPath, []byte(content), 0644)

	cmds, err := loadMacroFile(macroPath)
	if err != nil {
		t.Fatalf("loadMacroFile: %v", err)
	}

	expected := []string{
		"keypress:H,LMETA",
		"keypress:SPACE,LMETA",
		"type:notes",
		"delay:500",
		"keypress:ENTER",
	}
	if len(cmds) != len(expected) {
		t.Fatalf("expected %d commands, got %d", len(expected), len(cmds))
	}
	for i, cmd := range cmds {
		if cmd != expected[i] {
			t.Errorf("cmd[%d]: expected %s, got %s", i, expected[i], cmd)
		}
	}
}

func TestLoadMacroSkipsBlankLines(t *testing.T) {
	dir := t.TempDir()
	macroPath := filepath.Join(dir, "blanks.txt")
	content := "type:hello\n\n\ntype:world\n\n"
	os.WriteFile(macroPath, []byte(content), 0644)

	cmds, err := loadMacroFile(macroPath)
	if err != nil {
		t.Fatalf("loadMacroFile: %v", err)
	}
	if len(cmds) != 2 {
		t.Errorf("expected 2 commands, got %d: %v", len(cmds), cmds)
	}
}

func TestLoadMacroNotFound(t *testing.T) {
	_, err := loadMacroFile("nonexistent_macro_12345.txt")
	if err == nil {
		t.Error("expected error for nonexistent macro")
	}
}

func TestParseCommand(t *testing.T) {
	tests := []struct {
		input  string
		name   string
		data   string
	}{
		{"type:hello", "type", "hello"},
		{"ble_cmd:switch", "ble_cmd", "switch"},
		{"keyevent:A,LSHIFT,1", "keyevent", "A,LSHIFT,1"},
		{"paste", "paste", ""},
		{"delay:500", "delay", "500"},
		{"ble_cmd:switch=iPhone", "ble_cmd", "switch=iPhone"},
	}

	for _, tt := range tests {
		parts := strings.SplitN(tt.input, ":", 2)
		if parts[0] != tt.name {
			t.Errorf("name: expected %s, got %s", tt.name, parts[0])
		}
		data := ""
		if len(parts) > 1 {
			data = parts[1]
		}
		if data != tt.data {
			t.Errorf("data: expected %s, got %s", tt.data, data)
		}
	}
}
