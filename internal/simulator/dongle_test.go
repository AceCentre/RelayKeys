package simulator_test

import (
	"testing"

	"github.com/acecentre/relaykeys/internal/simulator"
)

func TestDongleBasicAT(t *testing.T) {
	d := simulator.NewDongle()

	resp := d.ProcessCommand("AT")
	if resp != "OK" {
		t.Errorf("AT: expected OK, got %s", resp)
	}
}

func TestDongleInitSequence(t *testing.T) {
	d := simulator.NewDongle()

	steps := []struct {
		cmd  string
		want string
	}{
		{"AT", "OK"},
		{"ATE=0", "OK"},
		{"AT+BLEHIDEN=1", "OK"},
		{"ATZ", "OK"},
	}

	for _, s := range steps {
		resp := d.ProcessCommand(s.cmd)
		if resp != s.want {
			t.Errorf("%s: expected %s, got %s", s.cmd, s.want, resp)
		}
	}
}

func TestDongleKeyboardCode(t *testing.T) {
	d := simulator.NewDongle()

	resp := d.ProcessCommand("AT+BLEKEYBOARDCODE=02-00-04-00-00-00-00-00")
	if resp != "OK" {
		t.Errorf("keyboard code: expected OK, got %s", resp)
	}

	report := d.LastKeyboardReport()
	if report[0] != 0x02 {
		t.Errorf("modifier: expected 0x02, got 0x%02x", report[0])
	}
	if report[2] != 0x04 {
		t.Errorf("key: expected 0x04 (A), got 0x%02x", report[2])
	}

	// Release all
	resp = d.ProcessCommand("AT+BLEKEYBOARDCODE=00-00-00-00-00-00-00-00")
	if resp != "OK" {
		t.Errorf("release: expected OK, got %s", resp)
	}
	report = d.LastKeyboardReport()
	if report[0] != 0x00 || report[2] != 0x00 {
		t.Errorf("release: expected all zeros, got mod=0x%02x key=0x%02x", report[0], report[2])
	}
}

func TestDongleMouseMove(t *testing.T) {
	d := simulator.NewDongle()

	resp := d.ProcessCommand("AT+BLEHIDMOUSEMOVE=10,20,0,0")
	if resp != "OK" {
		t.Errorf("mouse move: expected OK, got %s", resp)
	}

	resp = d.ProcessCommand("AT+BLEHIDMOUSEMOVE=-5,-10,0,0")
	if resp != "OK" {
		t.Errorf("mouse move negative: expected OK, got %s", resp)
	}
}

func TestDongleMouseButton(t *testing.T) {
	d := simulator.NewDongle()

	resp := d.ProcessCommand("AT+BLEHIDMOUSEBUTTON=l,click")
	if resp != "OK" {
		t.Errorf("mouse button: expected OK, got %s", resp)
	}

	resp = d.ProcessCommand("AT+BLEHIDMOUSEBUTTON=r")
	if resp != "OK" {
		t.Errorf("mouse button (no behavior): expected OK, got %s", resp)
	}
}

func TestDongleDeviceList(t *testing.T) {
	d := simulator.NewDongle()

	resp := d.ProcessCommand("AT+PRINTDEVLIST")
	if resp == "" {
		t.Error("devlist: expected non-empty response")
	}
	if !contains(resp, "iPhone") || !contains(resp, "iPad") || !contains(resp, "MacBook") {
		t.Errorf("devlist: expected device names in response, got: %s", resp)
	}
}

func TestDongleSwitchConn(t *testing.T) {
	d := simulator.NewDongle()

	devices := d.Devices()
	if len(devices) == 0 {
		t.Fatal("expected devices")
	}

	resp := d.ProcessCommand("AT+SWITCHCONN")
	if resp != "OK" {
		t.Errorf("switch: expected OK, got %s", resp)
	}

	current := d.CurrentDevice()
	if current == "" || current == "NONE" {
		t.Error("switch: expected a device name after switch")
	}
}

func TestDongleSwitchConnByName(t *testing.T) {
	d := simulator.NewDongle()

	resp := d.ProcessCommand(`AT+SWITCHCONN="iPhone"`)
	if resp != "OK" {
		t.Errorf("switch by name: expected OK, got %s", resp)
	}

	current := d.CurrentDevice()
	if current != "iPhone" {
		t.Errorf("switch by name: expected iPhone, got %s", current)
	}
}

func TestDongleDeviceName(t *testing.T) {
	d := simulator.NewDongle()

	_ = d.ProcessCommand("AT+SWITCHCONN")
	resp := d.ProcessCommand("AT+BLECURRENTDEVICENAME")

	lines := splitLines(resp)
	if len(lines) < 2 {
		t.Fatalf("devname: expected at least 2 lines, got: %s", resp)
	}
	name := lines[1]
	if name == "" || name == "NONE" {
		t.Errorf("devname: expected a device name, got: %s", name)
	}
}

func TestDongleAddDevice(t *testing.T) {
	d := simulator.NewDongle()
	initial := len(d.Devices())

	resp := d.ProcessCommand("AT+BLEADDNEWDEVICE")
	if resp != "OK" {
		t.Errorf("add device: expected OK, got %s", resp)
	}

	if len(d.Devices()) != initial+1 {
		t.Errorf("add device: expected %d devices, got %d", initial+1, len(d.Devices()))
	}
}

func TestDongleRemoveDevice(t *testing.T) {
	d := simulator.NewDongle()
	initial := len(d.Devices())

	resp := d.ProcessCommand(`AT+BLEREMOVEDEVICE="iPhone"`)
	if resp != "OK" {
		t.Errorf("remove device: expected OK, got %s", resp)
	}

	if len(d.Devices()) != initial-1 {
		t.Errorf("remove device: expected %d devices, got %d", initial-1, len(d.Devices()))
	}

	for _, dev := range d.Devices() {
		if dev.Name == "iPhone" {
			t.Error("remove device: iPhone should be gone")
		}
	}
}

func TestDongleResetDevList(t *testing.T) {
	d := simulator.NewDongle()

	resp := d.ProcessCommand("AT+RESETDEVLIST")
	if resp != "OK" {
		t.Errorf("reset devlist: expected OK, got %s", resp)
	}

	if len(d.Devices()) != 0 {
		t.Errorf("reset devlist: expected 0 devices, got %d", len(d.Devices()))
	}

	if d.CurrentDevice() != "NONE" {
		t.Errorf("reset devlist: expected NONE, got %s", d.CurrentDevice())
	}
}

func TestDongleGetSetMode(t *testing.T) {
	d := simulator.NewDongle()

	mode := d.ProcessCommand("AT+GETMODE")
	if mode != "KEYBOARD" {
		t.Errorf("get mode: expected KEYBOARD, got %s", mode)
	}

	resp := d.ProcessCommand("AT+SWITCHMODE")
	if resp != "MOUSE" {
		t.Errorf("switch mode: expected MOUSE, got %s", resp)
	}

	mode = d.ProcessCommand("AT+GETMODE")
	if mode != "MOUSE" {
		t.Errorf("get mode after switch: expected MOUSE, got %s", mode)
	}

	_ = d.ProcessCommand("AT+SWITCHMODE")
	mode = d.ProcessCommand("AT+GETMODE")
	if mode != "KEYBOARD" {
		t.Errorf("get mode after second switch: expected KEYBOARD, got %s", mode)
	}
}

func TestDongleUnknownCommand(t *testing.T) {
	d := simulator.NewDongle()

	resp := d.ProcessCommand("AT+UNKNOWNCMD")
	if resp != "ERROR" {
		t.Errorf("unknown cmd: expected ERROR, got %s", resp)
	}
}

func TestDongleDisconnect(t *testing.T) {
	d := simulator.NewDongle()

	resp := d.ProcessCommand("AT+GAPDISCONNECT")
	if resp != "OK" {
		t.Errorf("disconnect: expected OK, got %s", resp)
	}

	resp = d.ProcessCommand("AT+GAPDELBONDS")
	if resp != "OK" {
		t.Errorf("delbonds: expected OK, got %s", resp)
	}
}

func TestDongleEmptyDongle(t *testing.T) {
	d := simulator.NewEmptyDongle()

	if d.CurrentDevice() != "NONE" {
		t.Errorf("empty dongle: expected NONE, got %s", d.CurrentDevice())
	}

	resp := d.ProcessCommand("AT+SWITCHCONN")
	if resp != "ERROR" {
		t.Errorf("switch on empty: expected ERROR, got %s", resp)
	}

	resp = d.ProcessCommand("AT+PRINTDEVLIST")
	if !contains(resp, "OK") {
		t.Errorf("devlist empty: expected OK, got %s", resp)
	}
}

func contains(s, sub string) bool {
	return len(s) >= len(sub) && (s == sub || len(sub) == 0 ||
		(len(s) > 0 && len(sub) > 0 && findSubstr(s, sub)))
}

func findSubstr(s, sub string) bool {
	for i := 0; i <= len(s)-len(sub); i++ {
		if s[i:i+len(sub)] == sub {
			return true
		}
	}
	return false
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
