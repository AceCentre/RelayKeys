package webui

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/acecentre/relaykeys/internal/blehid"
	"github.com/acecentre/relaykeys/internal/capture"
	"github.com/acecentre/relaykeys/internal/macro"
	"github.com/gorilla/websocket"
)

type DeviceInfo struct {
	Name      string `json:"name"`
	Connected bool   `json:"connected"`
}

type Status struct {
	DongleConnected  bool         `json:"dongleConnected"`
	CurrentDevice    string       `json:"currentDevice"`
	DeviceList       []DeviceInfo `json:"deviceList"`
	DaemonMode       string       `json:"daemonMode"`
	RecordingMacro   bool         `json:"recordingMacro"`
	MacroList        []string     `json:"macroList"`
}

type commandFunc func(string) string

type Server struct {
	port       blehid.Port
	processBle commandFunc
	macros     *macro.Manager
	keys       [8]byte
	hub        *wsHub
	status     Status
	statusMu   sync.Mutex
	upgrader   websocket.Upgrader
}

type wsHub struct {
	mu      sync.Mutex
	clients map[*websocket.Conn]struct{}
}

func newHub() *wsHub {
	return &wsHub{clients: make(map[*websocket.Conn]struct{})}
}

func (h *wsHub) add(conn *websocket.Conn) {
	h.mu.Lock()
	h.clients[conn] = struct{}{}
	h.mu.Unlock()
}

func (h *wsHub) remove(conn *websocket.Conn) {
	h.mu.Lock()
	delete(h.clients, conn)
	h.mu.Unlock()
}

func (h *wsHub) broadcast(msg []byte) {
	h.mu.Lock()
	defer h.mu.Unlock()
	for conn := range h.clients {
		err := conn.WriteMessage(websocket.TextMessage, msg)
		if err != nil {
			go conn.Close()
			delete(h.clients, conn)
		}
	}
}

func New(port blehid.Port, processBle func(string) string) *Server {
	return &Server{
		port:       port,
		processBle: processBle,
		hub:        newHub(),
		status: Status{
			DaemonMode: "Hardware serial",
		},
		upgrader: websocket.Upgrader{CheckOrigin: func(r *http.Request) bool { return true }},
	}
}

func (s *Server) SetPort(p blehid.Port, processBle func(string) string) {
	s.port = p
	s.processBle = processBle
	s.UpdateStatus(func(st *Status) {
		st.DongleConnected = p != nil
	})
}

func (s *Server) SetMacros(m *macro.Manager) {
	s.macros = m
}

func (s *Server) UpdateStatus(fn func(*Status)) {
	s.statusMu.Lock()
	fn(&s.status)
	st := s.status
	s.statusMu.Unlock()

	data, _ := json.Marshal(map[string]interface{}{
		"type":   "status",
		"status": st,
	})
	s.hub.broadcast(data)
}

func (s *Server) GetStatus() Status {
	s.statusMu.Lock()
	defer s.statusMu.Unlock()
	return s.status
}

func (s *Server) HandleUI(w http.ResponseWriter, r *http.Request) {
	path := strings.TrimPrefix(r.URL.Path, "/ui")
	path = strings.TrimPrefix(path, "/")
	if path == "" {
		path = "index.html"
	}

	data, err := uiFS.ReadFile("ui/" + path)
	if err != nil {
		http.NotFound(w, r)
		return
	}

	ct := "text/plain"
	switch {
	case strings.HasSuffix(path, ".html"):
		ct = "text/html; charset=utf-8"
	case strings.HasSuffix(path, ".js"):
		ct = "application/javascript"
	case strings.HasSuffix(path, ".css"):
		ct = "text/css"
	case strings.HasSuffix(path, ".svg"):
		ct = "image/svg+xml"
	}
	w.Header().Set("Content-Type", ct)
	w.Write(data)
}

func (s *Server) HandleWS(w http.ResponseWriter, r *http.Request) {
	conn, err := s.upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("WS upgrade: %v", err)
		return
	}

	s.hub.add(conn)
	defer func() {
		s.hub.remove(conn)
		conn.Close()
	}()

	st := s.GetStatus()
	data, _ := json.Marshal(map[string]interface{}{
		"type":   "status",
		"status": st,
	})
	conn.WriteMessage(websocket.TextMessage, data)

	for {
		_, msg, err := conn.ReadMessage()
		if err != nil {
			break
		}

		var req map[string]interface{}
		if err := json.Unmarshal(msg, &req); err != nil {
			continue
		}

		cmd, _ := req["command"].(string)
		log.Printf("[WS] %s", cmd)

		switch cmd {
		case "switch":
			s.processBle("switch")
			s.refreshDevices()
		case "switch_to":
			name, _ := req["name"].(string)
			s.processBle("switch=" + name)
			s.refreshDevices()
		case "devadd":
			s.processBle("devadd")
			s.refreshDevices()
		case "devremove":
			name, _ := req["name"].(string)
			s.processBle("devremove=" + name)
			s.refreshDevices()
		case "devreset":
			s.processBle("devreset")
			s.refreshDevices()
		case "refresh":
			s.refreshDevices()
		case "keyevent":
			key, _ := req["key"].(string)
			down, _ := req["down"].(bool)
			var mods []string
			if raw, ok := req["modifiers"].([]interface{}); ok {
				for _, m := range raw {
					if s, ok := m.(string); ok {
						mods = append(mods, s)
					}
				}
			}
			if key != "" {
				if down {
					blehid.SendKeyboardCode(s.port, key, mods, true, &s.keys)
				} else {
					blehid.SendKeyboardCode(s.port, key, mods, false, &s.keys)
				}
				if s.macros != nil && s.macros.IsRecording() {
					if down && !capture.IsModifier(key) {
						modsStr := ""
						if len(mods) > 0 {
							modsStr = "," + strings.Join(mods, ",")
						}
						s.macros.RecordCommand(fmt.Sprintf("keypress:%s%s", key, modsStr))
					}
				}
			}
		case "mousemove":
			dx, _ := req["dx"].(float64)
			dy, _ := req["dy"].(float64)
			wy, _ := req["wy"].(float64)
			wx, _ := req["wx"].(float64)
			if s.port != nil {
				blehid.SendMouseMove(s.port, int(dx), int(dy), int(wy), int(wx))
			}
			if s.macros != nil && s.macros.IsRecording() {
				parts := []string{strconv.Itoa(int(dx)), strconv.Itoa(int(dy))}
				if int(wy) != 0 || int(wx) != 0 {
					parts = append(parts, strconv.Itoa(int(wy)), strconv.Itoa(int(wx)))
				}
				s.macros.RecordCommand("mousemove:" + strings.Join(parts, ","))
			}
		case "mousebutton":
			btn, _ := req["button"].(string)
			beh, _ := req["behavior"].(string)
			if s.port != nil {
				blehid.SendMouseButton(s.port, btn, beh)
			}
			if s.macros != nil && s.macros.IsRecording() {
				cmd := "mousebutton:" + btn
				if beh != "" {
					cmd += "," + beh
				}
				s.macros.RecordCommand(cmd)
			}
		case "macro_list":
			s.sendMacroList(conn)
		case "macro_run":
			name, _ := req["name"].(string)
			go s.runMacro(name, conn)
		case "macro_record_start":
			s.startRecording()
		case "macro_record_stop":
			name, _ := req["name"].(string)
			s.stopRecording(name)
		case "macro_delete":
			name, _ := req["name"].(string)
			if s.macros != nil {
				s.macros.Delete(name)
				s.sendMacroList(conn)
			}
		}
	}
}

func (s *Server) startRecording() {
	if s.macros == nil {
		return
	}
	s.macros.StartRecording()
	s.UpdateStatus(func(st *Status) {
		st.RecordingMacro = true
	})
}

func (s *Server) stopRecording(name string) {
	if s.macros == nil {
		return
	}
	if name == "" {
		name = fmt.Sprintf("macro_%s", time.Now().Format("20060102_150405"))
	}
	if err := s.macros.SaveRecording(name); err != nil {
		log.Printf("[Macro] Save failed: %v", err)
	}
	s.UpdateStatus(func(st *Status) {
		st.RecordingMacro = false
	})
}

func (s *Server) sendMacroList(conn *websocket.Conn) {
	if s.macros == nil {
		return
	}
	list, _ := s.macros.List()
	data, _ := json.Marshal(map[string]interface{}{
		"type":  "macro_list",
		"macros": list,
	})
	conn.WriteMessage(websocket.TextMessage, data)
}

func (s *Server) runMacro(name string, conn *websocket.Conn) {
	if s.macros == nil || s.port == nil {
		return
	}
	commands, err := s.macros.Load(name)
	if err != nil {
		log.Printf("[Macro] Load failed: %v", err)
		return
	}

	data, _ := json.Marshal(map[string]interface{}{
		"type": "macro_status",
		"running": true,
		"name": name,
	})
	conn.WriteMessage(websocket.TextMessage, data)

	for _, cmd := range commands {
		if err := s.executeMacroCommand(cmd); err != nil {
			log.Printf("[Macro] Command failed: %s: %v", cmd, err)
		}
	}

	data, _ = json.Marshal(map[string]interface{}{
		"type": "macro_status",
		"running": false,
		"name": name,
	})
	conn.WriteMessage(websocket.TextMessage, data)
}

func (s *Server) executeMacroCommand(cmd string) error {
	parts := strings.SplitN(cmd, ":", 2)
	name := parts[0]
	data := ""
	if len(parts) > 1 {
		data = parts[1]
	}

	switch name {
	case "keypress":
		p := strings.Split(data, ",")
		key := p[0]
		mods := p[1:]
		if err := blehid.SendKeyboardCode(s.port, key, mods, true, &s.keys); err != nil {
			return err
		}
		time.Sleep(20 * time.Millisecond)
		return blehid.SendKeyboardCode(s.port, key, mods, false, &s.keys)
	case "keyevent":
		p := strings.Split(data, ",")
		if len(p) < 2 {
			return fmt.Errorf("invalid keyevent: %s", data)
		}
		key := p[0]
		var mods []string
		down := false
		if len(p) > 2 {
			mods = p[1 : len(p)-1]
			down = p[len(p)-1] == "1"
		} else {
			down = p[1] == "1"
		}
		return blehid.SendKeyboardCode(s.port, key, mods, down, &s.keys)
	case "mousemove":
		p := strings.Split(data, ",")
		if len(p) < 2 {
			return fmt.Errorf("invalid mousemove: %s", data)
		}
		x, _ := strconv.Atoi(p[0])
		y, _ := strconv.Atoi(p[1])
		wy := 0
		wx := 0
		if len(p) > 2 {
			wy, _ = strconv.Atoi(p[2])
		}
		if len(p) > 3 {
			wx, _ = strconv.Atoi(p[3])
		}
		return blehid.SendMouseMove(s.port, x, y, wy, wx)
	case "mousebutton":
		p := strings.Split(data, ",")
		btn := p[0]
		beh := ""
		if len(p) > 1 {
			beh = p[1]
		}
		return blehid.SendMouseButton(s.port, btn, beh)
	case "ble_cmd":
		s.processBle(data)
		return nil
	case "delay":
		ms, _ := strconv.Atoi(data)
		if ms > 0 {
			time.Sleep(time.Duration(ms) * time.Millisecond)
		}
		return nil
	case "type":
		for _, ch := range data {
			key, mods := charToKey(ch)
			if key == "" {
				continue
			}
			if err := blehid.SendKeyboardCode(s.port, key, mods, true, &s.keys); err != nil {
				return err
			}
			time.Sleep(10 * time.Millisecond)
			if err := blehid.SendKeyboardCode(s.port, key, mods, false, &s.keys); err != nil {
				return err
			}
			time.Sleep(10 * time.Millisecond)
		}
		return nil
	default:
		return fmt.Errorf("unknown macro command: %s", name)
	}
}

func charToKey(ch rune) (string, []string) {
	if ch >= 'a' && ch <= 'z' {
		return string(rune(ch - 32)), nil
	}
	if ch >= 'A' && ch <= 'Z' {
		return string(ch), []string{"LSHIFT"}
	}
	if ch >= '0' && ch <= '9' {
		return string(ch), nil
	}
	switch ch {
	case ' ':
		return "SPACE", nil
	case '\n', '\r':
		return "ENTER", nil
	case '\t':
		return "TAB", nil
	case '.':
		return "PERIOD", nil
	case ',':
		return "COMMA", nil
	case ';':
		return "SEMICOLON", nil
	case '/':
		return "SLASH", nil
	case '\\':
		return "BACKSLASH", nil
	case '\'':
		return "QUOTE", nil
	case '-':
		return "MINUS", nil
	case '=':
		return "EQUALS", nil
	case '[':
		return "LEFTBRACKET", nil
	case ']':
		return "RIGHTBRACKET", nil
	case '`':
		return "BACKQUOTE", nil
	}
	return "", nil
}

func (s *Server) RefreshDevices() {
	s.refreshDevices()
}

func (s *Server) refreshDevices() {
	if s.port == nil {
		return
	}

	name, _ := blehid.GetDeviceName(s.port)
	list, _ := blehid.GetDeviceList(s.port)

	currentDevice := strings.TrimSpace(name)
	if currentDevice == "NONE" || currentDevice == "" {
		currentDevice = ""
	}

	devices := make([]DeviceInfo, 0)
	for _, d := range list {
		d = strings.TrimSpace(d)
		if d == "" || d == "OK" || d == "SUCCESS" {
			continue
		}
		cleanName := d
		if idx := strings.Index(d, ":"); idx >= 0 {
			cleanName = strings.TrimSpace(d[idx+1:])
		}
		if cleanName == "" {
			continue
		}
		connected := strings.Contains(d, "[connected]")
		devices = append(devices, DeviceInfo{
			Name:      cleanName,
			Connected: connected || cleanName == currentDevice,
		})
	}

	if currentDevice != "" {
		found := false
		for i := range devices {
			if devices[i].Name == currentDevice {
				devices[i].Connected = true
				found = true
				break
			}
		}
		if !found {
			devices = append(devices, DeviceInfo{
				Name:      currentDevice,
				Connected: true,
			})
		}
	}

	s.UpdateStatus(func(st *Status) {
		st.CurrentDevice = currentDevice
		st.DeviceList = devices
	})
}
