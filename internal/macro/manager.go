package macro

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"sync"
	"time"
)

type Entry struct {
	Command   string
	Timestamp time.Time
}

type Macro struct {
	Name    string
	Entries []Entry
}

type Manager struct {
	mu       sync.Mutex
	dir      string
	recording bool
	current  []Entry
}

func NewManager(dir string) *Manager {
	return &Manager{dir: dir}
}

func (m *Manager) MacroDir() string {
	return m.dir
}

func (m *Manager) List() ([]string, error) {
	m.mu.Lock()
	defer m.mu.Unlock()

	entries, err := os.ReadDir(m.dir)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, nil
		}
		return nil, err
	}

	var names []string
	for _, e := range entries {
		if e.IsDir() {
			continue
		}
		name := e.Name()
		if strings.HasSuffix(name, ".txt") {
			names = append(names, strings.TrimSuffix(name, ".txt"))
		}
	}
	sort.Strings(names)
	return names, nil
}

func (m *Manager) Load(name string) ([]string, error) {
	m.mu.Lock()
	defer m.mu.Unlock()

	path := m.macroPath(name)
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("macro not found: %s", name)
	}

	var lines []string
	scanner := bufio.NewScanner(strings.NewReader(string(data)))
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			lines = append(lines, line)
		}
	}
	return lines, scanner.Err()
}

func (m *Manager) Save(name string, commands []string) error {
	m.mu.Lock()
	defer m.mu.Unlock()

	if err := os.MkdirAll(m.dir, 0755); err != nil {
		return err
	}

	var sb strings.Builder
	for _, cmd := range commands {
		sb.WriteString(cmd)
		sb.WriteString("\n")
	}
	return os.WriteFile(m.macroPath(name), []byte(sb.String()), 0644)
}

func (m *Manager) Delete(name string) error {
	m.mu.Lock()
	defer m.mu.Unlock()

	return os.Remove(m.macroPath(name))
}

func (m *Manager) StartRecording() {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.recording = true
	m.current = nil
}

func (m *Manager) StopRecording() []Entry {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.recording = false
	entries := m.current
	m.current = nil
	return entries
}

func (m *Manager) IsRecording() bool {
	m.mu.Lock()
	defer m.mu.Unlock()
	return m.recording
}

func (m *Manager) RecordCommand(cmd string) {
	m.mu.Lock()
	defer m.mu.Unlock()
	if !m.recording {
		return
	}
	m.current = append(m.current, Entry{
		Command:   cmd,
		Timestamp: time.Now(),
	})
}

func (m *Manager) SaveRecording(name string) error {
	m.mu.Lock()
	entries := m.current
	m.recording = false
	m.current = nil
	m.mu.Unlock()

	if len(entries) == 0 {
		return fmt.Errorf("no recorded commands")
	}

	var commands []string
	for _, e := range entries {
		commands = append(commands, e.Command)
	}
	return m.Save(name, commands)
}

func (m *Manager) macroPath(name string) string {
	safe := strings.ReplaceAll(name, "/", "_")
	safe = strings.ReplaceAll(safe, "\\", "_")
	if !strings.HasSuffix(safe, ".txt") {
		safe += ".txt"
	}
	return filepath.Join(m.dir, safe)
}
