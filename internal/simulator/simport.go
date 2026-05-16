package simulator

import (
	"strings"
	"sync"
)

type SimPort struct {
	dongle  *DongleState
	log     []string
	logMu   sync.Mutex
}

func NewSimPort(d *DongleState) *SimPort {
	return &SimPort{dongle: d}
}

func (s *SimPort) WriteAT(cmd string) (string, error) {
	s.logMu.Lock()
	s.log = append(s.log, "TX: "+cmd)
	s.logMu.Unlock()

	resp := s.dongle.ProcessCommand(cmd)

	s.logMu.Lock()
	s.log = append(s.log, "RX: "+resp)
	s.logMu.Unlock()

	return resp, nil
}

func (s *SimPort) WriteATNoResponse(cmd string) error {
	_, err := s.WriteAT(cmd)
	return err
}

func (s *SimPort) WriteRaw(data []byte) error { return nil }

func (s *SimPort) Flush() {}

func (s *SimPort) CommandLog() []string {
	s.logMu.Lock()
	defer s.logMu.Unlock()
	cp := make([]string, len(s.log))
	copy(cp, s.log)
	return cp
}

func (s *SimPort) ResetLog() {
	s.logMu.Lock()
	s.log = nil
	s.logMu.Unlock()
}

func (s *SimPort) LastCommand() string {
	s.logMu.Lock()
	defer s.logMu.Unlock()
	for i := len(s.log) - 1; i >= 0; i-- {
		if strings.HasPrefix(s.log[i], "TX: ") {
			return strings.TrimPrefix(s.log[i], "TX: ")
		}
	}
	return ""
}

func (s *SimPort) LastResponse() string {
	s.logMu.Lock()
	defer s.logMu.Unlock()
	for i := len(s.log) - 1; i >= 0; i-- {
		if strings.HasPrefix(s.log[i], "RX: ") {
			return strings.TrimPrefix(s.log[i], "RX: ")
		}
	}
	return ""
}
