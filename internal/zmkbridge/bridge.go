package zmkbridge

import (
	"fmt"
	"log"
	"strings"

	"github.com/acecentre/relaykeys/internal/blehid"
	pb "github.com/acecentre/relaykeys/internal/zmk/proto"
	"google.golang.org/protobuf/proto"
)

const (
	sofByte = 0xAB
	escByte = 0xAC
	eofByte = 0xAD
)

func framePayload(payload []byte) []byte {
	var framed []byte
	framed = append(framed, sofByte)
	for _, b := range payload {
		if b == sofByte || b == escByte || b == eofByte {
			framed = append(framed, escByte)
			framed = append(framed, b)
		} else {
			framed = append(framed, b)
		}
	}
	framed = append(framed, eofByte)
	return framed
}

func sendReport(port blehid.Port, repType pb.InjectReportRequest_ReportType, data []byte) error {
	req := &pb.InjectReportRequest{
		Type: repType,
		Data: data,
	}

	payload, err := proto.Marshal(req)
	if err != nil {
		return fmt.Errorf("failed to marshal protobuf: %w", err)
	}

	framed := framePayload(payload)

	log.Printf("ZMK Bridge sending report type %v, len %d, framed len %d", repType, len(data), len(framed))

	return port.WriteRaw(framed)
}

func SendKeyboardCode(port blehid.Port, key string, modifiers []string, down bool, keys *[8]byte) error {
	// Re-use logic from blehid to compute modifiers and keys
	var hidmod byte
	for _, m := range modifiers {
		if bit, ok := blehid.ModifierBits[m]; ok {
			hidmod |= bit
		}
	}

	if down {
		keys[0] |= hidmod
	} else {
		keys[0] &^= hidmod
	}

	keycode := blehid.Keymap[key]
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

	// 8-byte standard HID report
	data := keys[:]
	return sendReport(port, pb.InjectReportRequest_KEYBOARD, data)
}

func SendMouseMove(port blehid.Port, right, down, wheely, wheelx int) error {
	// 5-byte Mouse report: buttons, x, y, scroll_y, scroll_x
	data := []byte{0, byte(int8(right)), byte(int8(down)), byte(int8(wheely)), byte(int8(wheelx))}
	return sendReport(port, pb.InjectReportRequest_MOUSE, data)
}

func SendMouseButton(port blehid.Port, btn string, behavior string) error {
	var buttons byte
	switch btn {
	case "l": buttons = 1
	case "r": buttons = 2
	case "m": buttons = 4
	}

	data := []byte{buttons, 0, 0, 0, 0}

	if behavior == "click" || behavior == "" {
	    // Down then up
		sendReport(port, pb.InjectReportRequest_MOUSE, data)
		data[0] = 0
		return sendReport(port, pb.InjectReportRequest_MOUSE, data)
	}

	if behavior == "up" {
	    data[0] = 0
	}

	return sendReport(port, pb.InjectReportRequest_MOUSE, data)
}

func sendAdminCommand(port blehid.Port, command pb.AdminCommandRequest_CommandType, slot int32) (*pb.AdminCommandResponse, error) {
	req := &pb.AdminCommandRequest{
		Command: command,
		Slot:    slot,
	}

	payload, err := proto.Marshal(req)
	if err != nil {
		return nil, err
	}

	framed := framePayload(payload)
	// We should actually read the response here if we need it
	// But port.WriteRaw doesn't read currently. For phase 2 we can return success
	// assuming write succeeds. We would need a custom Read if ZMK responds.
	err = port.WriteRaw(framed)
	if err != nil {
	    return nil, err
	}

	respBuf, err := port.ReadRaw(1024)
	if err == nil && len(respBuf) > 3 {
	    // Deframing
	    var deframed []byte
	    for i := 1; i < len(respBuf) - 1; i++ {
	        if respBuf[i] == escByte && i+1 < len(respBuf)-1 {
	            deframed = append(deframed, respBuf[i+1])
	            i++
	        } else {
	            deframed = append(deframed, respBuf[i])
	        }
	    }
	    var resp pb.AdminCommandResponse
	    if err := proto.Unmarshal(deframed, &resp); err == nil {
	        return &resp, nil
	    }
	}

	return &pb.AdminCommandResponse{Success: true}, nil
}

// ZMK admin commands
func ProcessBleCmd(port blehid.Port, cmd string) string {
	switch {
	case cmd == "devlist":
	    // Return a structured JSON or ZMK specific string that the web UI parses
		return "ZMK_NATIVE_MODE"
	case cmd == "devadd":
	    _, err := sendAdminCommand(port, pb.AdminCommandRequest_PAIR, 0)
	    if err != nil { return "FAIL" }
	case cmd == "devreset":
	    _, err := sendAdminCommand(port, pb.AdminCommandRequest_RESET, 0)
	    if err != nil { return "FAIL" }
	case strings.HasPrefix(cmd, "switch="):
	    var slot int32
	    fmt.Sscanf(strings.TrimPrefix(cmd, "switch="), "%d", &slot)
	    _, err := sendAdminCommand(port, pb.AdminCommandRequest_SWITCH_SLOT, slot)
	    if err != nil { return "FAIL" }
	}
	return "SUCCESS"
}
