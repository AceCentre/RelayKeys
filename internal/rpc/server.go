package rpc

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"strings"
	"sync"

	"github.com/acecentre/relaykeys/internal/blehid"
)

type Server struct {
	port    blehid.Port
	cfg     serverConfig
	keys    [8]byte
	mu      sync.Mutex
	running bool
}

type serverConfig struct {
	Username string
	Password string
}

type jsonRPCRequest struct {
	Version string          `json:"jsonrpc"`
	Method  string          `json:"method"`
	Params  json.RawMessage `json:"params"`
	ID      json.RawMessage `json:"id"`
}

type jsonRPCResponse struct {
	Version string          `json:"jsonrpc"`
	Result  interface{}     `json:"result,omitempty"`
	Error   *jsonRPCError   `json:"error,omitempty"`
	ID      json.RawMessage `json:"id"`
}

type jsonRPCError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

func NewServerWithConfig(port blehid.Port, username, password string) *Server {
	return &Server{
		port: port,
		cfg: serverConfig{
			Username: username,
			Password: password,
		},
	}
}

func (s *Server) IsRunning() bool {
	return s.running
}

func (s *Server) Port() blehid.Port {
	return s.port
}

func (s *Server) SetPort(p blehid.Port) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.port = p
}

func (s *Server) ProcessBleCmd(cmd string) string {
	return s.processBleCmd(cmd)
}

func (s *Server) ListenAndServe(ctx context.Context, addr string) error {
	mux := http.NewServeMux()
	mux.HandleFunc("/", s.HandleRPC)

	srv := &http.Server{Handler: mux}

	ln, err := net.Listen("tcp", addr)
	if err != nil {
		return fmt.Errorf("failed to listen on %s: %w", addr, err)
	}

	log.Printf("JSON-RPC server listening on %s", addr)

	go func() {
		<-ctx.Done()
		s.running = false
		srv.Close()
	}()

	s.running = true
	return srv.Serve(ln)
}

func (s *Server) HandleRPC(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	if s.cfg.Username != "" || s.cfg.Password != "" {
		u, p, ok := r.BasicAuth()
		if !ok || u != s.cfg.Username {
			pHash := sha256.Sum256([]byte(p))
			cfgHash := sha256.Sum256([]byte(s.cfg.Password))
			if hex.EncodeToString(pHash[:]) != hex.EncodeToString(cfgHash[:]) {
				w.WriteHeader(http.StatusForbidden)
				json.NewEncoder(w).Encode(jsonRPCResponse{
					Version: "2.0",
					Error:   &jsonRPCError{Code: 403, Message: "Invalid username or password"},
				})
				return
			}
		}
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}

	var req jsonRPCRequest
	if err := json.Unmarshal(body, &req); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(jsonRPCResponse{
			Version: "2.0",
			Error:   &jsonRPCError{Code: -32700, Message: "Parse error"},
			ID:      json.RawMessage("null"),
		})
		return
	}

	s.mu.Lock()
	result := s.dispatch(req.Method, req.Params)
	s.mu.Unlock()

	resp := jsonRPCResponse{
		Version: "2.0",
		Result:  result,
		ID:      req.ID,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func (s *Server) dispatch(method string, rawParams json.RawMessage) interface{} {
	if s.port == nil {
		return "No connection with dongle"
	}

	switch method {
	case "actions":
		return s.handleActions(rawParams)
	case "keyevent":
		return s.handleKeyevent(rawParams)
	case "mousemove":
		return s.handleMousemove(rawParams)
	case "mousebutton":
		return s.handleMousebutton(rawParams)
	case "ble_cmd":
		return s.handleBleCmd(rawParams)
	case "daemon":
		return s.handleDaemon(rawParams)
	case "exit":
		return "OK"
	default:
		return fmt.Sprintf("Unknown method: %s", method)
	}
}

func (s *Server) handleActions(rawParams json.RawMessage) interface{} {
	var params [][][]interface{}
	if err := json.Unmarshal(rawParams, &params); err != nil {
		return "INVALID_INPUT"
	}
	if len(params) == 0 {
		return "INVALID_INPUT"
	}
	actionList := params[0]
	results := make([]string, 0, len(actionList))
	for _, actionArr := range actionList {
		if len(actionArr) == 0 {
			continue
		}
		cmd, _ := actionArr[0].(string)
		result := s.processAction(cmd, actionArr[1:])
		results = append(results, result)
	}
	return strings.Join(results, ", ")
}

func (s *Server) handleKeyevent(rawParams json.RawMessage) interface{} {
	var params [][]interface{}
	if err := json.Unmarshal(rawParams, &params); err != nil {
		return "INVALID_INPUT"
	}
	if len(params) == 0 || len(params[0]) < 3 {
		return "INVALID_INPUT"
	}
	args := params[0]
	key, _ := args[0].(string)
	var mods []string
	if arr, ok := args[1].([]interface{}); ok {
		for _, m := range arr {
			if ms, ok := m.(string); ok {
				mods = append(mods, ms)
			}
		}
	} else if ms, ok := args[1].(string); ok {
		if ms != "" {
			mods = []string{ms}
		}
	}
	down, _ := args[2].(bool)

	if err := blehid.SendKeyboardCode(s.port, key, mods, down, &s.keys); err != nil {
		return "FAIL"
	}
	return "SUCCESS"
}

func (s *Server) handleMousemove(rawParams json.RawMessage) interface{} {
	var params [][]interface{}
	if err := json.Unmarshal(rawParams, &params); err != nil {
		return "INVALID_INPUT"
	}
	if len(params) == 0 || len(params[0]) < 2 {
		return "INVALID_INPUT"
	}
	args := params[0]
	right := toInt(args[0])
	down := toInt(args[1])
	wheely := 0
	wheelx := 0
	if len(args) > 2 {
		wheely = toInt(args[2])
	}
	if len(args) > 3 {
		wheelx = toInt(args[3])
	}
	if err := blehid.SendMouseMove(s.port, right, down, wheely, wheelx); err != nil {
		return "FAIL"
	}
	return "SUCCESS"
}

func (s *Server) handleMousebutton(rawParams json.RawMessage) interface{} {
	var params [][]interface{}
	if err := json.Unmarshal(rawParams, &params); err != nil {
		return "INVALID_INPUT"
	}
	if len(params) == 0 || len(params[0]) < 1 {
		return "INVALID_INPUT"
	}
	args := params[0]
	btn, _ := args[0].(string)
	behavior := ""
	if len(args) > 1 {
		behavior, _ = args[1].(string)
	}
	if err := blehid.SendMouseButton(s.port, btn, behavior); err != nil {
		return "FAIL"
	}
	return "SUCCESS"
}

func (s *Server) handleBleCmd(rawParams json.RawMessage) interface{} {
	var params [][]interface{}
	if err := json.Unmarshal(rawParams, &params); err != nil {
		return "INVALID_INPUT"
	}
	if len(params) == 0 || len(params[0]) < 1 {
		return "INVALID_INPUT"
	}
	cmd, _ := params[0][0].(string)
	return s.processBleCmd(cmd)
}

func (s *Server) handleDaemon(rawParams json.RawMessage) interface{} {
	var params [][]interface{}
	if err := json.Unmarshal(rawParams, &params); err != nil {
		return "INVALID_INPUT"
	}
	if len(params) == 0 || len(params[0]) < 1 {
		return "INVALID_INPUT"
	}
	cmd, _ := params[0][0].(string)
	switch cmd {
	case "get_mode":
		return "Hardware serial"
	case "dongle_status":
		resp, err := blehid.CheckDongle(s.port)
		if err != nil {
			return "No connection"
		}
		if strings.Contains(resp, "OK") {
			return "Connected"
		}
		return "No connection"
	default:
		return fmt.Sprintf("Unknown daemon command: %s", cmd)
	}
}

func (s *Server) processAction(cmd string, args []interface{}) string {
	switch cmd {
	case "mousemove":
		right := 0
		down := 0
		wheely := 0
		wheelx := 0
		if len(args) > 0 {
			right = toInt(args[0])
		}
		if len(args) > 1 {
			down = toInt(args[1])
		}
		if len(args) > 2 {
			wheely = toInt(args[2])
		}
		if len(args) > 3 {
			wheelx = toInt(args[3])
		}
		if err := blehid.SendMouseMove(s.port, right, down, wheely, wheelx); err != nil {
			return "FAIL"
		}
		return "SUCCESS"

	case "mousebutton":
		btn := ""
		behavior := ""
		if len(args) > 0 {
			btn, _ = args[0].(string)
		}
		if len(args) > 1 {
			behavior, _ = args[1].(string)
		}
		if err := blehid.SendMouseButton(s.port, btn, behavior); err != nil {
			return "FAIL"
		}
		return "SUCCESS"

	case "keyevent":
		key := ""
		var mods []string
		down := false
		if len(args) > 0 {
			key, _ = args[0].(string)
		}
		if len(args) > 1 {
			if arr, ok := args[1].([]interface{}); ok {
				for _, m := range arr {
					if ms, ok := m.(string); ok {
						mods = append(mods, ms)
					}
				}
			}
		}
		if len(args) > 2 {
			down, _ = args[2].(bool)
		}
		if err := blehid.SendKeyboardCode(s.port, key, mods, down, &s.keys); err != nil {
			return "FAIL"
		}
		return "SUCCESS"

	case "ble_cmd":
		if len(args) > 0 {
			subcmd, _ := args[0].(string)
			return s.processBleCmd(subcmd)
		}
		return "FAIL"

	default:
		return fmt.Sprintf("Unknown action: %s", cmd)
	}
}

func (s *Server) processBleCmd(cmd string) string {
	var err error
	var result string

	switch {
	case cmd == "switch":
		err = blehid.SendSwitchCommand(s.port, cmd)
	case strings.HasPrefix(cmd, "switch="):
		err = blehid.SendSwitchCommand(s.port, cmd)
	case cmd == "devname":
		result, err = blehid.GetDeviceName(s.port)
		if err != nil {
			return "FAIL"
		}
		return result
	case cmd == "devlist":
		list, err := blehid.GetDeviceList(s.port)
		if err != nil {
			return "FAIL"
		}
		return strings.Join(list, "\n")
	case cmd == "devadd":
		err = blehid.AddNewDevice(s.port)
	case cmd == "devreset":
		err = blehid.ClearDeviceList(s.port)
	case strings.HasPrefix(cmd, "devremove="):
		name := strings.TrimPrefix(cmd, "devremove=")
		err = blehid.RemoveDevice(s.port, name)
	case cmd == "get_mode":
		result, err = blehid.GetMode(s.port)
		if err != nil {
			return "FAIL"
		}
		return result
	case cmd == "switch_mode":
		result, err = blehid.SwitchMode(s.port)
		if err != nil {
			return "FAIL"
		}
		return result
	case cmd == "keyboard_release":
		for i := 0; i < 8; i++ {
			s.keys[i] = 0
		}
		_ = blehid.SendKeyboardCode(s.port, "", nil, false, &s.keys)
		return "SUCCESS"
	default:
		return fmt.Sprintf("Unknown ble_cmd: %s", cmd)
	}

	if err != nil {
		return "FAIL"
	}
	if result != "" {
		return result
	}
	return "SUCCESS"
}

func toInt(v interface{}) int {
	switch val := v.(type) {
	case float64:
		return int(val)
	case int:
		return val
	case string:
		n := 0
		fmt.Sscanf(val, "%d", &n)
		return n
	case json.Number:
		n, _ := val.Int64()
		return int(n)
	default:
		return 0
	}
}
