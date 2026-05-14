package simulator

import (
	"fmt"
	"log"
	"regexp"
	"strconv"
	"strings"
	"sync"
)

const (
	MaxDevices      = 15
	MaxNameLength   = 32
	InitialMode     = "KEYBOARD"
)

type Device struct {
	Name      string
	Connected bool
}

type DongleState struct {
	mu            sync.Mutex
	devices       []Device
	currentIndex  int
	mode          string
	hidEnabled    bool
	echoEnabled   bool
	bonded        bool
	addDevActive  bool
	switchActive  bool

	lastKeyboardReport [8]byte
	lastMouseX         int
	lastMouseY         int
}

func NewDongle() *DongleState {
	d := &DongleState{
		devices: []Device{
			{Name: "iPhone", Connected: false},
			{Name: "iPad", Connected: true},
			{Name: "MacBook", Connected: false},
		},
		currentIndex:     1,
		mode:             InitialMode,
		hidEnabled:       true,
		echoEnabled:      true,
		lastKeyboardReport: [8]byte{},
	}
	return d
}

func NewEmptyDongle() *DongleState {
	d := NewDongle()
	d.devices = nil
	d.currentIndex = -1
	return d
}

func (d *DongleState) CurrentDevice() string {
	d.mu.Lock()
	defer d.mu.Unlock()
	if d.currentIndex >= 0 && d.currentIndex < len(d.devices) {
		return d.devices[d.currentIndex].Name
	}
	return "NONE"
}

func (d *DongleState) Mode() string {
	d.mu.Lock()
	defer d.mu.Unlock()
	return d.mode
}

func (d *DongleState) Devices() []Device {
	d.mu.Lock()
	defer d.mu.Unlock()
	cp := make([]Device, len(d.devices))
	copy(cp, d.devices)
	return cp
}

func (d *DongleState) LastKeyboardReport() [8]byte {
	d.mu.Lock()
	defer d.mu.Unlock()
	return d.lastKeyboardReport
}

type CommandLog struct {
	Cmd      string
	Response string
}

func (d *DongleState) ProcessCommand(cmd string) string {
	d.mu.Lock()
	defer d.mu.Unlock()

	cmd = strings.TrimSpace(cmd)

	if cmd == "" {
		return "ERROR"
	}

	if !d.echoEnabled {
	} else {
	}

	switch {
	case cmd == "AT":
		return "OK"

	case cmd == "ATE=0":
		d.echoEnabled = false
		return "OK"

	case cmd == "ATE=1":
		d.echoEnabled = true
		return "OK"

	case cmd == "AT+BLEHIDEN=1":
		d.hidEnabled = true
		return "OK"

	case cmd == "AT+BLEKEYBOARDEN=1":
		d.hidEnabled = true
		return "OK"

	case cmd == "ATZ":
		return "OK"

	case cmd == "AT+GAPDISCONNECT":
		if d.currentIndex >= 0 && d.currentIndex < len(d.devices) {
			d.devices[d.currentIndex].Connected = false
		}
		d.bonded = false
		return "OK"

	case cmd == "AT+GAPDELBONDS":
		d.bonded = false
		return "OK"

	case cmd == "AT+SWITCHCONN":
		return d.handleSwitchConn("")

	case strings.HasPrefix(cmd, `AT+SWITCHCONN="`):
		re := regexp.MustCompile(`AT\+SWITCHCONN="([^"]*)"`)
		matches := re.FindStringSubmatch(cmd)
		if len(matches) > 1 {
			return d.handleSwitchConn(matches[1])
		}
		return "ERROR"

	case cmd == "AT+BLECURRENTDEVICENAME":
		if d.currentIndex >= 0 && d.currentIndex < len(d.devices) {
			return "OK\n" + d.devices[d.currentIndex].Name
		}
		return "OK\nNONE"

	case cmd == "AT+PRINTDEVLIST":
		var lines []string
		lines = append(lines, "OK")
		for _, dev := range d.devices {
			status := ""
			if dev.Connected {
				status = " [connected]"
			}
			lines = append(lines, fmt.Sprintf("%d: %s%s", len(lines)-1, dev.Name, status))
		}
		return strings.Join(lines, "\n")

	case cmd == "AT+BLEADDNEWDEVICE":
		d.addDevActive = true
		newName := fmt.Sprintf("NewDevice_%d", len(d.devices)+1)
		d.devices = append(d.devices, Device{Name: newName, Connected: false})
		d.addDevActive = false
		return "OK"

	case cmd == "AT+RESETDEVLIST":
		d.devices = nil
		d.currentIndex = -1
		return "OK"

	case strings.HasPrefix(cmd, "AT+BLEREMOVEDEVICE="):
		re := regexp.MustCompile(`AT\+BLEREMOVEDEVICE="([^"]*)"`)
		matches := re.FindStringSubmatch(cmd)
		if len(matches) > 1 {
			name := matches[1]
			for i, dev := range d.devices {
				if dev.Name == name {
					d.devices = append(d.devices[:i], d.devices[i+1:]...)
					if d.currentIndex >= len(d.devices) {
						d.currentIndex = len(d.devices) - 1
					}
					return "OK"
				}
			}
			return "ERROR"
		}
		return "ERROR"

	case strings.HasPrefix(cmd, "AT+BLEKEYBOARDCODE="):
		return d.handleKeyboardCode(cmd)

	case strings.HasPrefix(cmd, "AT+BLEHIDMOUSEMOVE="):
		return d.handleMouseMove(cmd)

	case strings.HasPrefix(cmd, "AT+BLEHIDMOUSEBUTTON="):
		return d.handleMouseButton(cmd)

	case cmd == "AT+GETMODE":
		return d.mode

	case cmd == "AT+SWITCHMODE":
		if d.mode == "KEYBOARD" {
			d.mode = "MOUSE"
		} else {
			d.mode = "KEYBOARD"
		}
		return d.mode

	default:
		log.Printf("[SIMULATOR] Unknown command: %s", cmd)
		return "ERROR"
	}
}

func (d *DongleState) handleSwitchConn(targetName string) string {
	if len(d.devices) == 0 {
		return "ERROR"
	}

	if d.currentIndex >= 0 && d.currentIndex < len(d.devices) {
		d.devices[d.currentIndex].Connected = false
	}

	if targetName == "" {
		d.currentIndex = (d.currentIndex + 1) % len(d.devices)
	} else {
		found := false
		for i, dev := range d.devices {
			if strings.Contains(strings.ToLower(dev.Name), strings.ToLower(targetName)) {
				d.currentIndex = i
				found = true
				break
			}
		}
		if !found {
			return "ERROR"
		}
	}

	if d.currentIndex >= 0 && d.currentIndex < len(d.devices) {
		d.devices[d.currentIndex].Connected = true
	}
	return "OK"
}

var keyboardCodeRe = regexp.MustCompile(`AT\+BLEKEYBOARDCODE=([0-9a-fA-F]{2})-([0-9a-fA-F]{2})-([0-9a-fA-F]{2})-([0-9a-fA-F]{2})-([0-9a-fA-F]{2})-([0-9a-fA-F]{2})-([0-9a-fA-F]{2})-([0-9a-fA-F]{2})`)

func (d *DongleState) handleKeyboardCode(cmd string) string {
	matches := keyboardCodeRe.FindStringSubmatch(cmd)
	if matches == nil {
		return "ERROR"
	}

	for i := 0; i < 8; i++ {
		b, err := parseHexByte(matches[i+1])
		if err != nil {
			return "ERROR"
		}
		d.lastKeyboardReport[i] = b
	}

	log.Printf("[SIMULATOR] Keyboard report: mod=%02x keys=%02x %02x %02x %02x %02x %02x",
		d.lastKeyboardReport[0],
		d.lastKeyboardReport[2],
		d.lastKeyboardReport[3],
		d.lastKeyboardReport[4],
		d.lastKeyboardReport[5],
		d.lastKeyboardReport[6],
		d.lastKeyboardReport[7],
	)

	return "OK"
}

var mouseMoveRe = regexp.MustCompile(`AT\+BLEHIDMOUSEMOVE=(-?\d+),(-?\d+),(-?\d+),(-?\d+)`)

func (d *DongleState) handleMouseMove(cmd string) string {
	matches := mouseMoveRe.FindStringSubmatch(cmd)
	if matches == nil {
		return "ERROR"
	}

	dx, _ := strconv.Atoi(matches[1])
	dy, _ := strconv.Atoi(matches[2])
	d.lastMouseX += dx
	d.lastMouseY += dy

	log.Printf("[SIMULATOR] Mouse move: dx=%d dy=%d (total: %d,%d)", dx, dy, d.lastMouseX, d.lastMouseY)
	return "OK"
}

var mouseBtnRe = regexp.MustCompile(`AT\+BLEHIDMOUSEBUTTON=(\w)(?:,(\w+))?`)

func (d *DongleState) handleMouseButton(cmd string) string {
	matches := mouseBtnRe.FindStringSubmatch(cmd)
	if matches == nil {
		return "ERROR"
	}

	btn := matches[1]
	behavior := "click"
	if matches[2] != "" {
		behavior = matches[2]
	}

	log.Printf("[SIMULATOR] Mouse button: %s (%s)", btn, behavior)
	return "OK"
}

func parseHexByte(s string) (byte, error) {
	v, err := strconv.ParseUint(s, 16, 8)
	if err != nil {
		return 0, err
	}
	return byte(v), nil
}
