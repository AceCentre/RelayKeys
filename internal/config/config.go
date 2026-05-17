package config

import (
	"os"
	"path/filepath"
	"runtime"
	"strconv"
)

type Config struct {
	Host       string
	Port       int
	Username   string
	Password   string
	Dev        string
	Baud       int
	Debug      bool
	NoSerial   bool
	BLEMode    bool
	LogFile    string
	ClientHost string
	ClientPort int
	KeymapFile string
	Delay      int
	FirmwareType string
}

func Load(path string) (*Config, error) {
	cfg := &Config{
		Host:       "127.0.0.1",
		Port:       5383,
		Baud:       115200,
		ClientHost: "127.0.0.1",
		ClientPort: 5383,
		FirmwareType: "legacy",
	}

	home, _ := os.UserHomeDir()
	paths := []string{}
	if path != "" {
		paths = append(paths, path)
	} else {
		if home != "" {
			paths = append(paths,
				filepath.Join(home, ".relaykeys.cfg"),
			)
		}
		exePath, _ := os.Executable()
		if exePath != "" {
			paths = append(paths,
				filepath.Join(filepath.Dir(exePath), "relaykeys.cfg"),
			)
		}
		paths = append(paths, "relaykeys.cfg")
		if runtime.GOOS == "windows" {
			appData := os.Getenv("APPDATA")
			if appData != "" {
				paths = append(paths,
					filepath.Join(appData, "RelayKeys", "relaykeys.cfg"),
				)
			}
		}
	}

	for _, p := range paths {
		data, err := os.ReadFile(p)
		if err != nil {
			continue
		}
		parseINI(data, cfg)
		break
	}

	return cfg, nil
}

func parseINI(data []byte, cfg *Config) {
	section := ""
	for _, line := range splitLines(string(data)) {
		line = trimSpace(line)
		if line == "" || line[0] == '#' || line[0] == ';' {
			continue
		}
		if line[0] == '[' && line[len(line)-1] == ']' {
			section = line[1 : len(line)-1]
			continue
		}
		key, val, ok := parseKeyValue(line)
		if !ok {
			continue
		}
		switch section {
		case "server":
			switch key {
			case "host":
				cfg.Host = val
			case "port":
				cfg.Port, _ = strconv.Atoi(val)
			case "dev":
				cfg.Dev = val
			case "baud":
				cfg.Baud, _ = strconv.Atoi(val)
			case "username":
				cfg.Username = val
			case "password":
				cfg.Password = val
			case "debug":
				cfg.Debug = val == "true" || val == "1"
			case "firmware_type":
				cfg.FirmwareType = val
			case "noserial":
				cfg.NoSerial = val == "true" || val == "1"
			case "logfile":
				cfg.LogFile = val
			}
		case "client":
			switch key {
			case "host":
				cfg.ClientHost = val
			case "port":
				cfg.ClientPort, _ = strconv.Atoi(val)
			case "username":
				cfg.Username = val
			case "password":
				cfg.Password = val
			case "delay":
				cfg.Delay, _ = strconv.Atoi(val)
			}
		case "cli":
			switch key {
			case "keymap_file":
				cfg.KeymapFile = val
			}
		}
	}
}

func splitLines(s string) []string {
	var lines []string
	start := 0
	for i := 0; i < len(s); i++ {
		if s[i] == '\n' {
			line := s[start:i]
			if len(line) > 0 && line[len(line)-1] == '\r' {
				line = line[:len(line)-1]
			}
			lines = append(lines, line)
			start = i + 1
		}
	}
	if start < len(s) {
		lines = append(lines, s[start:])
	}
	return lines
}

func trimSpace(s string) string {
	start, end := 0, len(s)
	for start < end && (s[start] == ' ' || s[start] == '\t') {
		start++
	}
	for end > start && (s[end-1] == ' ' || s[end-1] == '\t') {
		end--
	}
	return s[start:end]
}

func parseKeyValue(line string) (string, string, bool) {
	for i := 0; i < len(line); i++ {
		if line[i] == '=' {
			return trimSpace(line[:i]), trimSpace(line[i+1:]), true
		}
	}
	return "", "", false
}
