package macro

import (
	"os"
	"path/filepath"
	"testing"
)

func TestManagerSaveLoadListDelete(t *testing.T) {
	dir := t.TempDir()
	m := NewManager(dir)

	names, err := m.List()
	if err != nil {
		t.Fatalf("List: %v", err)
	}
	if len(names) != 0 {
		t.Fatalf("expected empty, got %v", names)
	}

	cmds := []string{"keypress:A", "delay:100", "keypress:ENTER"}
	if err := m.Save("test_macro", cmds); err != nil {
		t.Fatalf("Save: %v", err)
	}

	loaded, err := m.Load("test_macro")
	if err != nil {
		t.Fatalf("Load: %v", err)
	}
	if len(loaded) != 3 {
		t.Fatalf("expected 3 commands, got %d", len(loaded))
	}
	if loaded[0] != "keypress:A" {
		t.Fatalf("expected 'keypress:A', got '%s'", loaded[0])
	}

	names, err = m.List()
	if err != nil {
		t.Fatalf("List: %v", err)
	}
	if len(names) != 1 || names[0] != "test_macro" {
		t.Fatalf("expected [test_macro], got %v", names)
	}

	if err := m.Delete("test_macro"); err != nil {
		t.Fatalf("Delete: %v", err)
	}

	names, err = m.List()
	if err != nil {
		t.Fatalf("List after delete: %v", err)
	}
	if len(names) != 0 {
		t.Fatalf("expected empty after delete, got %v", names)
	}
}

func TestManagerRecording(t *testing.T) {
	dir := t.TempDir()
	m := NewManager(dir)

	if m.IsRecording() {
		t.Fatal("should not be recording initially")
	}

	m.StartRecording()
	if !m.IsRecording() {
		t.Fatal("should be recording after start")
	}

	m.RecordCommand("keypress:A")
	m.RecordCommand("delay:50")
	m.RecordCommand("keypress:B")

	if err := m.SaveRecording("recording_test"); err != nil {
		t.Fatalf("SaveRecording: %v", err)
	}

	if m.IsRecording() {
		t.Fatal("should not be recording after save")
	}

	loaded, err := m.Load("recording_test")
	if err != nil {
		t.Fatalf("Load: %v", err)
	}
	if len(loaded) != 3 {
		t.Fatalf("expected 3 commands, got %d: %v", len(loaded), loaded)
	}
}

func TestManagerMacroPath(t *testing.T) {
	dir := t.TempDir()
	m := NewManager(dir)

	expected := filepath.Join(dir, "my_macro.txt")
	if p := m.macroPath("my_macro"); p != expected {
		t.Fatalf("expected %s, got %s", expected, p)
	}

	if p := m.macroPath("my_macro.txt"); p != expected {
		t.Fatalf("expected %s, got %s", expected, p)
	}

	expected = filepath.Join(dir, "sub_dir_safe_macro.txt")
	if p := m.macroPath("sub/dir/safe_macro"); p != expected {
		t.Fatalf("expected %s, got %s", expected, p)
	}
}

func TestManagerSaveCreatesDir(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "nested", "macros")
	m := NewManager(dir)

	if err := m.Save("test", []string{"keypress:A"}); err != nil {
		t.Fatalf("Save should create dirs: %v", err)
	}

	if _, err := os.Stat(dir); os.IsNotExist(err) {
		t.Fatal("directory was not created")
	}
}

func TestManagerLoadNotFound(t *testing.T) {
	dir := t.TempDir()
	m := NewManager(dir)

	_, err := m.Load("nonexistent")
	if err == nil {
		t.Fatal("expected error for nonexistent macro")
	}
}

func TestManagerSaveRecordingEmpty(t *testing.T) {
	dir := t.TempDir()
	m := NewManager(dir)

	m.StartRecording()
	if err := m.SaveRecording("empty"); err == nil {
		t.Fatal("expected error for empty recording")
	}
}
