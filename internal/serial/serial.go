package serial

import (
	"fmt"
	"log"
	"strings"
	"sync"
	"time"

	"github.com/acecentre/relaykeys/internal/config"
	goSerial "go.bug.st/serial"
	"go.bug.st/serial/enumerator"
)

const nrfVID = "239A"

var nrfPIDs = map[string]bool{
	"8029": true,
	"810B": true,
	"8051": true,
}

type HardwarePort struct {
	port goSerial.Port
	mu   sync.Mutex
	cfg  *config.Config
}

func Open(cfg *config.Config) (*HardwarePort, error) {
	if cfg.NoSerial {
		log.Println("Running in no-serial (dummy) mode")
		return &HardwarePort{cfg: cfg}, nil
	}

	devPath := cfg.Dev
	if devPath == "" {
		found, err := FindDevice()
		if err != nil {
			return nil, fmt.Errorf("auto-detect failed: %w", err)
		}
		if found == "" {
			return nil, fmt.Errorf("no RelayKeys dongle found — is it plugged in?")
		}
		devPath = found
		log.Printf("Auto-detected device: %s", devPath)
	}

	mode := &goSerial.Mode{
		BaudRate: cfg.Baud,
	}
	
	p, err := goSerial.Open(devPath, mode)
	if err != nil {
		return nil, fmt.Errorf("failed to open %s: %w", devPath, err)
	}
	
	p.SetReadTimeout(1000)

	time.Sleep(100 * time.Millisecond)

	log.Printf("Serial device opened: %s @ %d baud", devPath, cfg.Baud)
	return &HardwarePort{port: p, cfg: cfg}, nil
}

func FindDevice() (string, error) {
	ports, err := enumerator.GetDetailedPortsList()
	if err != nil {
		return "", err
	}

	for _, p := range ports {
		if strings.Contains(p.Product, "CP2104") ||
			strings.Contains(p.Product, "nRF52") {
			log.Printf("Found dongle: %s (%s)", p.Name, p.Product)
			return p.Name, nil
		}
		if p.VID == nrfVID {
			if p.PID != "" && nrfPIDs[strings.ToUpper(p.PID)] {
				log.Printf("Found dongle by VID/PID: %s (%s:%s)", p.Name, p.VID, p.PID)
				return p.Name, nil
			}
		}
	}

	return "", nil
}

func ListPorts() ([]string, error) {
	ports, err := enumerator.GetDetailedPortsList()
	if err != nil {
		return nil, err
	}
	var names []string
	for _, p := range ports {
		names = append(names, fmt.Sprintf("%s  VID=%s PID=%s  %s", p.Name, p.VID, p.PID, p.Product))
	}
	return names, nil
}

func (h *HardwarePort) Init() error {
	if h.port == nil {
		return nil
	}
	h.port.ResetInputBuffer()
	h.port.ResetOutputBuffer()
	time.Sleep(100 * time.Millisecond)
	h.port.ResetInputBuffer()

	resp, err := h.WriteAT("AT")
	if err != nil {
		return fmt.Errorf("dongle not responding: %w", err)
	}
	if !strings.Contains(resp, "OK") {
		return fmt.Errorf("unexpected AT response: %s", resp)
	}

	return nil
}

func (h *HardwarePort) WriteAT(cmd string) (string, error) {
	if h.port == nil {
		log.Printf("[DUMMY] TX: %s", cmd)
		return "OK", nil
	}

	h.mu.Lock()
	defer h.mu.Unlock()

	h.port.ResetInputBuffer()

	cmdBytes := []byte(cmd + "\r\n")
	if _, err := h.port.Write(cmdBytes); err != nil {
		return "", fmt.Errorf("write failed: %w", err)
	}

	log.Printf("TX: %s", cmd)

	buf := make([]byte, 4096)
	var response []byte

	deadline := time.Now().Add(3 * time.Second)
	for time.Now().Before(deadline) {
		n, err := h.port.Read(buf)
		if err != nil {
			if len(response) > 0 {
				break
			}
			return "", fmt.Errorf("read failed: %w", err)
		}
		if n > 0 {
			response = append(response, buf[:n]...)
			respStr := string(response)
			if strings.HasSuffix(strings.TrimSpace(respStr), "OK") ||
				strings.HasSuffix(strings.TrimSpace(respStr), "ERROR") ||
				strings.HasSuffix(strings.TrimSpace(respStr), "SUCCESS") {
				time.Sleep(50 * time.Millisecond)
				if n2, _ := h.port.Read(buf); n2 > 0 {
					response = append(response, buf[:n2]...)
				}
				break
			}
			continue
		}

		if len(response) > 0 {
			time.Sleep(100 * time.Millisecond)
			if n2, _ := h.port.Read(buf); n2 > 0 {
				response = append(response, buf[:n2]...)
				continue
			}
			break
		}
	}

	if len(response) == 0 {
		return "", fmt.Errorf("read timeout waiting for response to: %s", cmd)
	}

	resp := strings.TrimSpace(string(response))
	log.Printf("RX: %s", resp)
	return resp, nil
}

func (h *HardwarePort) WriteATNoResponse(cmd string) error {
	_, err := h.WriteAT(cmd)
	return err
}

func (h *HardwarePort) Flush() {
	if h.port != nil {
		_ = h.port.ResetInputBuffer()
		_ = h.port.ResetOutputBuffer()
	}
}

func (h *HardwarePort) Close() error {
	if h.port != nil {
		return h.port.Close()
	}
	return nil
}
