package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	"github.com/acecentre/relaykeys/internal/config"
	"github.com/acecentre/relaykeys/internal/keymap"
	"github.com/acecentre/relaykeys/internal/rpc"
)

var version = "dev"

func main() {
	log.SetFlags(0)

	var cfgPath string
	var debug bool
	var macroFile string
	var delay int
	var showVersion bool
	var notify bool

	args := os.Args[1:]
	commands := []string{}

	i := 0
	for i < len(args) {
		switch args[i] {
		case "--config", "-c":
			if i+1 < len(args) {
				cfgPath = args[i+1]
				i += 2
			} else {
				log.Fatal("--config requires a path")
			}
		case "--debug":
			debug = true
			i++
		case "--notify":
			notify = true
			i++
		case "--delay":
			if i+1 < len(args) {
				delay, _ = strconv.Atoi(args[i+1])
				i += 2
			} else {
				log.Fatal("--delay requires a value")
			}
		case "-f":
			if i+1 < len(args) {
				macroFile = args[i+1]
				i += 2
			} else {
				log.Fatal("-f requires a filename")
			}
		case "--version":
			showVersion = true
			i++
		case "--help", "-h":
			printUsage()
			os.Exit(0)
		default:
			if !strings.HasPrefix(args[i], "-") {
				commands = append(commands, args[i])
			}
			i++
		}
	}

	if showVersion {
		fmt.Printf("relaykeys-cli %s\n", version)
		os.Exit(0)
	}

	if len(commands) == 0 && macroFile == "" {
		printUsage()
		os.Exit(1)
	}

	cfg, err := config.Load(cfgPath)
	if err != nil {
		log.Fatalf("Config error: %v", err)
	}

	if debug {
		cfg.Debug = true
	}

	host := cfg.ClientHost
	port := cfg.ClientPort
	url := fmt.Sprintf("http://%s:%d/", host, port)

	client := rpc.NewClient(url, cfg.Username, cfg.Password)

	if cfg.KeymapFile != "" {
		if err := keymap.Load(cfg.KeymapFile); err != nil {
			log.Printf("Warning: keymap load failed: %v", err)
		}
	} else {
		if err := keymap.Load("us_keymap.json"); err != nil {
			log.Printf("Warning: default keymap load failed: %v", err)
		}
	}

	if cfg.Delay > 0 && delay == 0 {
		delay = cfg.Delay
	}

	allCommands := []string{}
	if macroFile != "" {
		macroCommands, err := loadMacroFile(macroFile)
		if err != nil {
			log.Fatalf("Macro file error: %v", err)
		}
		allCommands = append(allCommands, macroCommands...)
	}
	allCommands = append(allCommands, commands...)

	for _, cmd := range allCommands {
		result, err := executeCommand(client, cmd, delay)
		if err != nil {
			if notify {
				sendNotification("RelayKeys", fmt.Sprintf("Error: %v", err))
			}
			log.Fatalf("Error: %v", err)
		}
		if result != "" {
			fmt.Println(result)
		}
		if notify {
			sendCommandNotification(cmd, result)
		}
	}
}

func printUsage() {
	fmt.Fprintf(os.Stderr, "RelayKeys CLI %s\n\n", version)
	fmt.Fprintf(os.Stderr, "Usage: relaykeys-cli [options] <command> [command...]\n\n")
	fmt.Fprintf(os.Stderr, "Options:\n")
	fmt.Fprintf(os.Stderr, "  --config, -c <path>   Path to config file\n")
	fmt.Fprintf(os.Stderr, "  --debug               Enable debug logging\n")
	fmt.Fprintf(os.Stderr, "  --delay <ms>          Delay between commands (milliseconds)\n")
	fmt.Fprintf(os.Stderr, "  -f <file>             Execute macro file\n")
	fmt.Fprintf(os.Stderr, "  --notify              Send result as OS notification\n")
	fmt.Fprintf(os.Stderr, "  --version             Show version\n")
	fmt.Fprintf(os.Stderr, "  --help, -h            Show this help\n\n")
	fmt.Fprintf(os.Stderr, "Commands:\n")
	fmt.Fprintf(os.Stderr, "  type:<text>           Type text on target device\n")
	fmt.Fprintf(os.Stderr, "  keypress:<key>[,<mod>...]\n")
	fmt.Fprintf(os.Stderr, "                        Press and release a key\n")
	fmt.Fprintf(os.Stderr, "  keyevent:<key>,<down>[,<mod>...]\n")
	fmt.Fprintf(os.Stderr, "                        Send key event (down=1 or 0)\n")
	fmt.Fprintf(os.Stderr, "  mousemove:<x>,<y>    Move mouse\n")
	fmt.Fprintf(os.Stderr, "  mousebutton:<btn>[,<behavior>]\n")
	fmt.Fprintf(os.Stderr, "                        Click/hold/release mouse button\n")
	fmt.Fprintf(os.Stderr, "  ble_cmd:<command>     BLE command (devname, devlist, switch, etc.)\n")
	fmt.Fprintf(os.Stderr, "  daemon:<command>      Daemon command (dongle_status, get_mode)\n")
	fmt.Fprintf(os.Stderr, "  delay:<ms>           Wait for specified milliseconds\n")
	fmt.Fprintf(os.Stderr, "  paste                 Paste clipboard contents\n")
}

func loadMacroFile(name string) ([]string, error) {
	if !strings.Contains(name, "/") && !strings.Contains(name, "\\") {
		exePath, _ := os.Executable()
		exeDir := filepath.Dir(exePath)

		candidates := []string{
			filepath.Join(exeDir, "macros", name),
			filepath.Join(exeDir, "macros", name+".txt"),
			filepath.Join(".", "macros", name),
			filepath.Join(".", "macros", name+".txt"),
		}

		for _, p := range candidates {
			if _, err := os.Stat(p); err == nil {
				name = p
				break
			}
		}
	}

	f, err := os.Open(name)
	if err != nil {
		return nil, fmt.Errorf("cannot open macro file: %w", err)
	}
	defer f.Close()

	var lines []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			lines = append(lines, line)
		}
	}
	return lines, scanner.Err()
}

func executeCommand(client *rpc.Client, cmd string, delay int) (string, error) {
	parts := strings.SplitN(cmd, ":", 2)
	name := parts[0]
	data := ""
	if len(parts) > 1 {
		data = parts[1]
	}

	switch name {
	case "type":
		return doType(client, data, delay)
	case "paste":
		return doPaste(client, delay)
	case "keypress":
		return doKeypress(client, data, delay)
	case "keyevent":
		return doKeyevent(client, data, delay)
	case "mousemove":
		return doMousemove(client, data, delay)
	case "mousebutton":
		return doMousebutton(client, data, delay)
	case "ble_cmd":
		return doBleCmd(client, data)
	case "daemon":
		return doDaemonCmd(client, data)
	case "delay":
		ms, _ := strconv.Atoi(data)
		if ms > 0 {
			time.Sleep(time.Duration(ms) * time.Millisecond)
		}
		return "", nil
	default:
		return "", fmt.Errorf("unknown command: %s", cmd)
	}
}

func doType(client *rpc.Client, text string, delay int) (string, error) {
	escaped := false
	escapeMap := map[rune]rune{'t': '\t', 'n': '\n', 'r': '\r'}

	for _, ch := range text {
		if ch == '\\' && !escaped {
			escaped = true
			continue
		}
		if escaped {
			escaped = false
			if replacement, ok := escapeMap[ch]; ok {
				ch = replacement
			} else {
				if err := typeChar(client, '\\', delay); err != nil {
					return "", err
				}
			}
		}
		if err := typeChar(client, ch, delay); err != nil {
			return "", err
		}
	}
	return "", nil
}

func typeChar(client *rpc.Client, ch rune, delay int) error {
	key, mods := keymap.CharToKeyevent(ch)
	if key == "" {
		return nil
	}

	_, err := client.Call("keyevent", key, mods, true)
	if err != nil {
		return err
	}
	if delay > 0 {
		time.Sleep(time.Duration(delay) * time.Millisecond)
	}

	_, err = client.Call("keyevent", key, mods, false)
	if delay > 0 {
		time.Sleep(time.Duration(delay) * time.Millisecond)
	}
	return err
}

func doPaste(client *rpc.Client, delay int) (string, error) {
	text, err := readClipboard()
	if err != nil {
		return "", fmt.Errorf("clipboard read failed: %w", err)
	}
	return doType(client, text, delay)
}

func doKeypress(client *rpc.Client, data string, delay int) (string, error) {
	parts := strings.Split(data, ",")
	key := parts[0]
	var mods []string
	if len(parts) > 1 {
		mods = parts[1:]
	}

	_, err := client.Call("keyevent", key, mods, true)
	if err != nil {
		return "", err
	}
	if delay > 0 {
		time.Sleep(time.Duration(delay) * time.Millisecond)
	}
	_, err = client.Call("keyevent", key, mods, false)
	if delay > 0 {
		time.Sleep(time.Duration(delay) * time.Millisecond)
	}
	return "", err
}

func doKeyevent(client *rpc.Client, data string, delay int) (string, error) {
	parts := strings.Split(data, ",")
	if len(parts) < 2 {
		return "", fmt.Errorf("keyevent requires at least key,isdown")
	}

	key := parts[0]
	var mods []string
	isDown := parts[len(parts)-1] == "1"

	if len(parts) > 2 {
		mods = parts[1 : len(parts)-1]
	}

	result, err := client.Call("keyevent", key, mods, isDown)
	if delay > 0 {
		time.Sleep(time.Duration(delay) * time.Millisecond)
	}
	return result, err
}

func doMousemove(client *rpc.Client, data string, delay int) (string, error) {
	parts := strings.Split(data, ",")
	if len(parts) < 2 {
		return "", fmt.Errorf("mousemove requires x,y")
	}

	x, _ := strconv.Atoi(parts[0])
	y, _ := strconv.Atoi(parts[1])
	wy := 0
	wx := 0
	if len(parts) > 2 {
		wy, _ = strconv.Atoi(parts[2])
	}
	if len(parts) > 3 {
		wx, _ = strconv.Atoi(parts[3])
	}

	result, err := client.Call("mousemove", x, y, wy, wx)
	if delay > 0 {
		time.Sleep(time.Duration(delay) * time.Millisecond)
	}
	return result, err
}

func doMousebutton(client *rpc.Client, data string, delay int) (string, error) {
	parts := strings.Split(data, ",")
	btn := strings.ToLower(parts[0])
	behavior := ""
	if len(parts) > 1 {
		behavior = strings.ToLower(parts[1])
	}

	result, err := client.Call("mousebutton", btn, behavior)
	if delay > 0 {
		time.Sleep(time.Duration(delay) * time.Millisecond)
	}
	return result, err
}

func doBleCmd(client *rpc.Client, data string) (string, error) {
	return client.Call("ble_cmd", data)
}

func doDaemonCmd(client *rpc.Client, data string) (string, error) {
	return client.Call("daemon", data)
}

func sendCommandNotification(cmd, result string) {
	parts := strings.SplitN(cmd, ":", 2)
	name := parts[0]
	data := ""
	if len(parts) > 1 {
		data = parts[1]
	}

	msg := ""

	switch name {
	case "ble_cmd":
		if result == "TIMEOUT" || result == "FAIL" || result == "No connection with dongle" {
			msg = "Command failed. Check dongle connection."
		} else {
			switch {
			case data == "devname":
				msg = "Connected to " + result
			case data == "devlist":
				msg = "Device list: " + result
			case data == "devadd":
				msg = "Adding new device. Pair your device with the RelayKeys dongle."
			case data == "devreset":
				msg = "Device list cleared."
			case data == "switch":
				msg = "Switching to next device."
			case strings.HasPrefix(data, "switch="):
				msg = "Switching to " + strings.TrimPrefix(data, "switch=")
			case strings.HasPrefix(data, "devremove="):
				msg = strings.TrimPrefix(data, "devremove=") + " removed."
			case data == "get_mode":
				msg = "Daemon mode: " + result
			case data == "switch_mode":
				msg = "Switching daemon mode."
			}
		}
	case "daemon":
		if data == "dongle_status" {
			msg = "Dongle: " + result
		} else if data == "get_mode" {
			msg = "Mode: " + result
		}
	case "type":
		msg = "Typed: " + data
	case "keypress":
		msg = "Key: " + data
	}

	if msg != "" {
		sendNotification("RelayKeys", msg)
	}
}
