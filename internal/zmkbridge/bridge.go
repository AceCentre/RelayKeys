package zmkbridge

import (
	"fmt"
	"log"

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
	// Just stubbed out for now - would send MOUSE report type.
	// Mouse report depends on ZMK config, normally 4 to 5 bytes.
	return nil
}

func SendMouseButton(port blehid.Port, btn string, behavior string) error {
	return nil
}

// ZMK admin commands
func ProcessBleCmd(port blehid.Port, cmd string) string {
    // Process advanced ZMK ble commands here.
	return "SUCCESS"
}
