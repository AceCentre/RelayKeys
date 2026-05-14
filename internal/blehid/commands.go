package blehid

import (
	"fmt"
	"log"
	"strings"
)

func clamp(val, min, max int) int {
	if val < min {
		return min
	}
	if val > max {
		return max
	}
	return val
}

func InitSerial(port Port) error {
	port.Flush()
	if _, err := port.WriteAT("AT"); err != nil {
		return fmt.Errorf("AT ping failed: %w", err)
	}
	if _, err := port.WriteAT("ATE=0"); err != nil {
		return fmt.Errorf("disable echo failed: %w", err)
	}
	resp, err := port.WriteAT("AT+BLEHIDEN=1")
	if err != nil {
		return fmt.Errorf("enable HID failed: %w", err)
	}
	if strings.ToUpper(strings.TrimSpace(resp)) == "ERROR" {
		if _, err := port.WriteAT("AT+BLEKEYBOARDEN=1"); err != nil {
			return fmt.Errorf("fallback keyboard enable failed: %w", err)
		}
	}
	if _, err := port.WriteAT("ATZ"); err != nil {
		return fmt.Errorf("ATZ reset failed: %w", err)
	}
	return nil
}

func SendMouseMove(port Port, right, down, wheely, wheelx int) error {
	right = clamp(right, -MaxMouseMove, MaxMouseMove)
	down = clamp(down, -MaxMouseMove, MaxMouseMove)
	wheely = clamp(wheely, -MaxMouseMove, MaxMouseMove)
	wheelx = clamp(wheelx, -MaxMouseMove, MaxMouseMove)

	for right != 0 || down != 0 || wheelx != 0 || wheely != 0 {
		rm := clamp(right, -128, 127)
		dm := clamp(down, -128, 127)
		wym := clamp(wheely, -128, 127)
		wxm := clamp(wheelx, -128, 127)
		cmd := fmt.Sprintf("AT+BLEHIDMOUSEMOVE=%d,%d,%d,%d", rm, dm, wym, wxm)
		if _, err := port.WriteAT(cmd); err != nil {
			return err
		}
		right -= rm
		down -= dm
		wheely -= wym
		wheelx -= wxm
	}
	return nil
}

func SendMouseButton(port Port, btn string, behavior string) error {
	cmd := fmt.Sprintf("AT+BLEHIDMOUSEBUTTON=%s", btn)
	if behavior != "" {
		cmd += "," + behavior
	}
	_, err := port.WriteAT(cmd)
	return err
}

func SendKeyboardCode(port Port, key string, modifiers []string, down bool, keys *[8]byte) error {
	modKeys := []string{"LCTRL", "LSHIFT", "LALT", "LMETA", "RCTRL", "RSHIFT", "RALT", "RMETA"}
	for _, mk := range modKeys {
		if key == mk {
			modifiers = append(modifiers, key)
			key = ""
			break
		}
	}

	log.Printf("keyevent: key=%s mods=%v down=%v", key, modifiers, down)

	var hidmod byte
	for _, m := range modifiers {
		if bit, ok := ModifierBits[m]; ok {
			hidmod |= bit
		}
	}

	if down {
		keys[0] |= hidmod
	} else {
		keys[0] &^= hidmod
	}

	keycode := Keymap[key]

	if key != "" && keycode != 0 {
		if down {
			for i := 2; i < 8; i++ {
				if keys[i] == 0 {
					keys[i] = keycode
					break
				}
			}
		} else {
			for i := 2; i < 8; i++ {
				if keys[i] == keycode {
					keys[i] = 0
					break
				}
			}
		}
	}

	cmd := fmt.Sprintf("AT+BLEKEYBOARDCODE=%02x-00", keys[0])
	for i := 2; i < 8; i++ {
		if keys[i] != 0 {
			cmd += fmt.Sprintf("-%02x", keys[i])
		} else {
			cmd += "-00"
		}
	}

	_, err := port.WriteAT(cmd)
	return err
}

func SendSwitchCommand(port Port, cmd string) error {
	var resp string
	var err error
	if cmd == "switch" {
		resp, err = port.WriteAT("AT+SWITCHCONN")
	} else if strings.HasPrefix(cmd, "switch=") {
		name := strings.TrimPrefix(cmd, "switch=")
		atcmd := fmt.Sprintf(`AT+SWITCHCONN="%s"`, name)
		resp, err = port.WriteAT(atcmd)
	} else {
		return nil
	}
	if err != nil {
		return err
	}
	if strings.Contains(resp, "ERROR") {
		return fmt.Errorf("switch failed: %s", resp)
	}
	return nil
}

func GetDeviceName(port Port) (string, error) {
	port.Flush()
	resp, err := port.WriteAT("AT+BLECURRENTDEVICENAME")
	if err != nil {
		return "NONE", err
	}
	lines := strings.Split(strings.TrimSpace(resp), "\n")
	if len(lines) >= 2 {
		return strings.TrimSpace(lines[1]), nil
	}
	if len(lines) == 1 && lines[0] != "" {
		return strings.TrimSpace(lines[0]), nil
	}
	return "NONE", nil
}

func GetDeviceList(port Port) ([]string, error) {
	port.Flush()
	resp, err := port.WriteAT("AT+PRINTDEVLIST")
	if err != nil {
		return nil, err
	}
	lines := strings.Split(strings.TrimSpace(resp), "\n")
	if len(lines) > 1 {
		return lines[1:], nil
	}
	return nil, nil
}

func DropBondedDevice(port Port) error {
	if _, err := port.WriteAT("AT+GAPDISCONNECT"); err != nil {
		return err
	}
	_, err := port.WriteAT("AT+GAPDELBONDS")
	return err
}

func AddNewDevice(port Port) error {
	_, err := port.WriteAT("AT+BLEADDNEWDEVICE")
	return err
}

func ClearDeviceList(port Port) error {
	_, err := port.WriteAT("AT+RESETDEVLIST")
	return err
}

func RemoveDevice(port Port, name string) error {
	_, err := port.WriteAT(fmt.Sprintf(`AT+BLEREMOVEDEVICE="%s"`, name))
	return err
}

func GetMode(port Port) (string, error) {
	return port.WriteAT("AT+GETMODE")
}

func SwitchMode(port Port) (string, error) {
	return port.WriteAT("AT+SWITCHMODE")
}

func CheckDongle(port Port) (string, error) {
	return port.WriteAT("AT")
}
