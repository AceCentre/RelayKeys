package simulator_test

import (
	"strings"
	"testing"

	"github.com/acecentre/relaykeys/internal/blehid"
	"github.com/acecentre/relaykeys/internal/simulator"
)

func TestSimPortImplementsPort(t *testing.T) {
	d := simulator.NewDongle()
	var _ blehid.Port = simulator.NewSimPort(d)
}

func TestInitSerialViaBlehid(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	err := blehid.InitSerial(port)
	if err != nil {
		t.Fatalf("InitSerial: %v", err)
	}

	log := port.CommandLog()
	expectedTX := []string{"AT", "ATE=0", "AT+BLEHIDEN=1", "ATZ"}
	txIdx := 0
	for _, entry := range log {
		if txIdx >= len(expectedTX) {
			break
		}
		if strings.HasPrefix(entry, "TX: ") {
			cmd := strings.TrimPrefix(entry, "TX: ")
			if cmd != expectedTX[txIdx] {
				t.Errorf("TX[%d]: expected %s, got %s", txIdx, expectedTX[txIdx], cmd)
			}
			txIdx++
		}
	}
	if txIdx != len(expectedTX) {
		t.Errorf("expected %d TX commands, found %d", len(expectedTX), txIdx)
	}
}

func TestSendKeyboardCode(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	var keys [8]byte
	err := blehid.SendKeyboardCode(port, "A", nil, true, &keys)
	if err != nil {
		t.Fatalf("SendKeyboardCode: %v", err)
	}

	if keys[0] != 0x00 {
		t.Errorf("modifier: expected 0x00, got 0x%02x", keys[0])
	}
	if keys[2] != 0x04 {
		t.Errorf("key slot: expected 0x04 (A), got 0x%02x", keys[2])
	}

	report := d.LastKeyboardReport()
	if report[2] != 0x04 {
		t.Errorf("dongle report key: expected 0x04, got 0x%02x", report[2])
	}

	// Release
	err = blehid.SendKeyboardCode(port, "A", nil, false, &keys)
	if err != nil {
		t.Fatalf("SendKeyboardCode release: %v", err)
	}
	if keys[2] != 0x00 {
		t.Errorf("key slot after release: expected 0x00, got 0x%02x", keys[2])
	}
}

func TestSendKeyboardCodeWithModifiers(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	var keys [8]byte

	err := blehid.SendKeyboardCode(port, "LSHIFT", nil, true, &keys)
	if err != nil {
		t.Fatalf("SendKeyboardCode LSHIFT: %v", err)
	}
	if keys[0] != 0x02 {
		t.Errorf("modifier after LSHIFT down: expected 0x02, got 0x%02x", keys[0])
	}

	err = blehid.SendKeyboardCode(port, "A", []string{"LSHIFT"}, true, &keys)
	if err != nil {
		t.Fatalf("SendKeyboardCode A+LSHIFT: %v", err)
	}
	if keys[0] != 0x02 {
		t.Errorf("modifier: expected 0x02, got 0x%02x", keys[0])
	}
	if keys[2] != 0x04 {
		t.Errorf("key: expected 0x04, got 0x%02x", keys[2])
	}

	report := d.LastKeyboardReport()
	if report[0] != 0x02 {
		t.Errorf("dongle report mod: expected 0x02, got 0x%02x", report[0])
	}
}

func TestSendMouseMove(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	err := blehid.SendMouseMove(port, 100, -50, 0, 0)
	if err != nil {
		t.Fatalf("SendMouseMove: %v", err)
	}

	cmd := port.LastCommand()
	if !contains(cmd, "AT+BLEHIDMOUSEMOVE=100,-50,0,0") {
		t.Errorf("expected mouse move AT cmd, got: %s", cmd)
	}
}

func TestSendMouseMoveLargeDelta(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	err := blehid.SendMouseMove(port, 300, 0, 0, 0)
	if err != nil {
		t.Fatalf("SendMouseMove large: %v", err)
	}

	log := port.CommandLog()
	moveCount := 0
	for _, l := range log {
		if contains(l, "AT+BLEHIDMOUSEMOVE") {
			moveCount++
		}
	}
	if moveCount != 3 {
		t.Errorf("large move: expected 3 mouse move commands, got %d", moveCount)
	}
}

func TestSendMouseButton(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	err := blehid.SendMouseButton(port, "l", "click")
	if err != nil {
		t.Fatalf("SendMouseButton: %v", err)
	}

	cmd := port.LastCommand()
	if !contains(cmd, "AT+BLEHIDMOUSEBUTTON=l,click") {
		t.Errorf("expected mouse button AT cmd, got: %s", cmd)
	}
}

func TestGetDeviceName(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	name, err := blehid.GetDeviceName(port)
	if err != nil {
		t.Fatalf("GetDeviceName: %v", err)
	}
	if name == "" || name == "NONE" {
		t.Errorf("expected device name, got: %s", name)
	}
}

func TestGetDeviceList(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	list, err := blehid.GetDeviceList(port)
	if err != nil {
		t.Fatalf("GetDeviceList: %v", err)
	}
	if len(list) == 0 {
		t.Error("expected devices in list")
	}
}

func TestSwitchDevice(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	err := blehid.SendSwitchCommand(port, "switch")
	if err != nil {
		t.Fatalf("SwitchCommand: %v", err)
	}

	current := d.CurrentDevice()
	if current == "" || current == "NONE" {
		t.Error("expected device after switch")
	}
}

func TestSwitchDeviceByName(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	err := blehid.SendSwitchCommand(port, "switch=iPhone")
	if err != nil {
		t.Fatalf("SwitchCommand by name: %v", err)
	}

	current := d.CurrentDevice()
	if current != "iPhone" {
		t.Errorf("expected iPhone, got: %s", current)
	}
}

func TestAddRemoveDevice(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	initial := len(d.Devices())

	if err := blehid.AddNewDevice(port); err != nil {
		t.Fatalf("AddNewDevice: %v", err)
	}
	if len(d.Devices()) != initial+1 {
		t.Errorf("expected %d devices after add, got %d", initial+1, len(d.Devices()))
	}

	if err := blehid.RemoveDevice(port, "iPhone"); err != nil {
		t.Fatalf("RemoveDevice: %v", err)
	}

	for _, dev := range d.Devices() {
		if dev.Name == "iPhone" {
			t.Error("iPhone should have been removed")
		}
	}
}

func TestClearDeviceList(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	if err := blehid.ClearDeviceList(port); err != nil {
		t.Fatalf("ClearDeviceList: %v", err)
	}

	if len(d.Devices()) != 0 {
		t.Errorf("expected 0 devices, got %d", len(d.Devices()))
	}
}

func TestDropBondedDevice(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	if err := blehid.DropBondedDevice(port); err != nil {
		t.Fatalf("DropBondedDevice: %v", err)
	}

	cmds := port.CommandLog()
	foundDisconnect := false
	foundDelbonds := false
	for _, l := range cmds {
		if contains(l, "AT+GAPDISCONNECT") {
			foundDisconnect = true
		}
		if contains(l, "AT+GAPDELBONDS") {
			foundDelbonds = true
		}
	}
	if !foundDisconnect || !foundDelbonds {
		t.Errorf("expected disconnect+delbonds, got log: %v", cmds)
	}
}

func TestGetMode(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	mode, err := blehid.GetMode(port)
	if err != nil {
		t.Fatalf("GetMode: %v", err)
	}
	if mode != "KEYBOARD" {
		t.Errorf("expected KEYBOARD mode, got: %s", mode)
	}
}

func TestSwitchMode(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	resp, err := blehid.SwitchMode(port)
	if err != nil {
		t.Fatalf("SwitchMode: %v", err)
	}
	if resp != "MOUSE" {
		t.Errorf("expected MOUSE after switch, got: %s", resp)
	}

	mode, err := blehid.GetMode(port)
	if err != nil {
		t.Fatalf("GetMode: %v", err)
	}
	if mode != "MOUSE" {
		t.Errorf("GetMode after switch: expected MOUSE, got %s", mode)
	}
}

func TestCheckDongle(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	resp, err := blehid.CheckDongle(port)
	if err != nil {
		t.Fatalf("CheckDongle: %v", err)
	}
	if resp != "OK" {
		t.Errorf("expected OK, got: %s", resp)
	}
}
