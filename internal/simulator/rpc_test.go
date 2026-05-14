package simulator_test

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/acecentre/relaykeys/internal/rpc"
	"github.com/acecentre/relaykeys/internal/simulator"
)

func TestRPCEndToEndKeyevent(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "", "")

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		srv.HandleRPC(w, r)
	}))
	defer ts.Close()

	client := rpc.NewClient(ts.URL, "", "")

	result, err := client.Call("keyevent", "A", nil, true)
	if err != nil {
		t.Fatalf("keyevent down: %v", err)
	}
	if result != "SUCCESS" {
		t.Errorf("keyevent down: expected SUCCESS, got %s", result)
	}

	result, err = client.Call("keyevent", "A", nil, false)
	if err != nil {
		t.Fatalf("keyevent up: %v", err)
	}
	if result != "SUCCESS" {
		t.Errorf("keyevent up: expected SUCCESS, got %s", result)
	}

	report := d.LastKeyboardReport()
	// After release, everything should be 0
	if report[2] != 0x00 {
		t.Errorf("report after release: expected key=0x00, got 0x%02x", report[2])
	}
}

func TestRPCEndToEndMousemove(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "", "")

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		srv.HandleRPC(w, r)
	}))
	defer ts.Close()

	client := rpc.NewClient(ts.URL, "", "")

	result, err := client.Call("mousemove", 100, -50, 0, 0)
	if err != nil {
		t.Fatalf("mousemove: %v", err)
	}
	if result != "SUCCESS" {
		t.Errorf("mousemove: expected SUCCESS, got %s", result)
	}

	cmd := port.LastCommand()
	if !contains(cmd, "AT+BLEHIDMOUSEMOVE") {
		t.Errorf("expected mouse move AT cmd, got: %s", cmd)
	}
}

func TestRPCEndToEndMousebutton(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "", "")

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		srv.HandleRPC(w, r)
	}))
	defer ts.Close()

	client := rpc.NewClient(ts.URL, "", "")

	result, err := client.Call("mousebutton", "l", "click")
	if err != nil {
		t.Fatalf("mousebutton: %v", err)
	}
	if result != "SUCCESS" {
		t.Errorf("mousebutton: expected SUCCESS, got %s", result)
	}
}

func TestRPCEndToEndBleCmd(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "", "")

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		srv.HandleRPC(w, r)
	}))
	defer ts.Close()

	client := rpc.NewClient(ts.URL, "", "")

	result, err := client.Call("ble_cmd", "devname")
	if err != nil {
		t.Fatalf("ble_cmd devname: %v", err)
	}
	if result == "" || result == "NONE" {
		t.Errorf("devname: expected a name, got %s", result)
	}

	result, err = client.Call("ble_cmd", "switch")
	if err != nil {
		t.Fatalf("ble_cmd switch: %v", err)
	}
	if result != "SUCCESS" {
		t.Errorf("switch: expected SUCCESS, got %s", result)
	}

	result, err = client.Call("ble_cmd", "get_mode")
	if err != nil {
		t.Fatalf("ble_cmd get_mode: %v", err)
	}
	if result != "KEYBOARD" {
		t.Errorf("get_mode: expected KEYBOARD, got %s", result)
	}
}

func TestRPCEndToEndActions(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "", "")

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		srv.HandleRPC(w, r)
	}))
	defer ts.Close()

	body := map[string]interface{}{
		"jsonrpc": "2.0",
		"method":  "actions",
		"params": []interface{}{
			[]interface{}{
				[]interface{}{"keyevent", "A", nil, true},
				[]interface{}{"keyevent", "A", nil, false},
			},
		},
		"id": 1,
	}
	data, _ := json.Marshal(body)

	resp, err := http.Post(ts.URL, "application/json", strings.NewReader(string(data)))
	if err != nil {
		t.Fatalf("actions request: %v", err)
	}
	defer resp.Body.Close()

	var result struct {
		Result string `json:"result"`
	}
	json.NewDecoder(resp.Body).Decode(&result)

	if !contains(result.Result, "SUCCESS") {
		t.Errorf("actions: expected SUCCESS in result, got %s", result.Result)
	}
}

func TestRPCEndToEndDaemon(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "", "")

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		srv.HandleRPC(w, r)
	}))
	defer ts.Close()

	client := rpc.NewClient(ts.URL, "", "")

	result, err := client.Call("daemon", "get_mode")
	if err != nil {
		t.Fatalf("daemon get_mode: %v", err)
	}
	if result != "Hardware serial" {
		t.Errorf("daemon get_mode: expected 'Hardware serial', got %s", result)
	}

	result, err = client.Call("daemon", "dongle_status")
	if err != nil {
		t.Fatalf("daemon dongle_status: %v", err)
	}
	if result != "Connected" {
		t.Errorf("daemon dongle_status: expected 'Connected', got %s", result)
	}
}

func TestRPCServerWithAuth(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "admin", "secret123")

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		srv.HandleRPC(w, r)
	}))
	defer ts.Close()

	clientNoAuth := rpc.NewClient(ts.URL, "", "")
	_, err := clientNoAuth.Call("daemon", "get_mode")
	if err == nil {
		t.Error("expected auth error for no-auth client")
	}

	clientWithAuth := rpc.NewClient(ts.URL, "admin", "secret123")
	result, err := clientWithAuth.Call("daemon", "get_mode")
	if err != nil {
		t.Fatalf("auth client: %v", err)
	}
	if result != "Hardware serial" {
		t.Errorf("auth client: expected 'Hardware serial', got %s", result)
	}
}

func TestRPCDeviceManagement(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "", "")

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		srv.HandleRPC(w, r)
	}))
	defer ts.Close()

	client := rpc.NewClient(ts.URL, "", "")

	result, err := client.Call("ble_cmd", "devlist")
	if err != nil {
		t.Fatalf("devlist: %v", err)
	}
	if !contains(result, "iPhone") {
		t.Errorf("devlist: expected iPhone in %s", result)
	}

	result, err = client.Call("ble_cmd", "devadd")
	if err != nil {
		t.Fatalf("devadd: %v", err)
	}
	if result != "SUCCESS" {
		t.Errorf("devadd: expected SUCCESS, got %s", result)
	}

	result, err = client.Call("ble_cmd", "devreset")
	if err != nil {
		t.Fatalf("devreset: %v", err)
	}
	if result != "SUCCESS" {
		t.Errorf("devreset: expected SUCCESS, got %s", result)
	}

	if len(d.Devices()) != 0 {
		t.Errorf("expected 0 devices after reset, got %d", len(d.Devices()))
	}
}

func TestRPCKeyboardRelease(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "", "")

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		srv.HandleRPC(w, r)
	}))
	defer ts.Close()

	client := rpc.NewClient(ts.URL, "", "")

	result, err := client.Call("keyevent", "A", []string{"LSHIFT"}, true)
	if err != nil {
		t.Fatalf("keyevent: %v", err)
	}
	if result != "SUCCESS" {
		t.Errorf("keyevent: expected SUCCESS, got %s", result)
	}

	result, err = client.Call("ble_cmd", "keyboard_release")
	if err != nil {
		t.Fatalf("keyboard_release: %v", err)
	}
	if result != "SUCCESS" {
		t.Errorf("keyboard_release: expected SUCCESS, got %s", result)
	}

	report := d.LastKeyboardReport()
	for i := 0; i < 8; i++ {
		if report[i] != 0 {
			t.Errorf("report[%d] after release: expected 0, got 0x%02x", i, report[i])
		}
	}
}

func TestRPCSwitchAndName(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "", "")

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		srv.HandleRPC(w, r)
	}))
	defer ts.Close()

	client := rpc.NewClient(ts.URL, "", "")

	result, err := client.Call("ble_cmd", "switch=iPhone")
	if err != nil {
		t.Fatalf("switch to iPhone: %v", err)
	}
	if result != "SUCCESS" {
		t.Errorf("switch: expected SUCCESS, got %s", result)
	}

	if d.CurrentDevice() != "iPhone" {
		t.Errorf("current device: expected iPhone, got %s", d.CurrentDevice())
	}

	result, err = client.Call("ble_cmd", "devname")
	if err != nil {
		t.Fatalf("devname: %v", err)
	}
	if !contains(result, "iPhone") {
		t.Errorf("devname: expected iPhone, got %s", result)
	}
}

func TestFullServerLifecycle(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "", "")

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	addr := "127.0.0.1:0"

	go srv.ListenAndServe(ctx, addr)

	time.Sleep(100 * time.Millisecond)

	cancel()
	time.Sleep(100 * time.Millisecond)

	if !srv.IsRunning() {
		t.Log("Server shut down cleanly")
	}
}

func TestRPCUnknownMethod(t *testing.T) {
	d := simulator.NewDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "", "")

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		srv.HandleRPC(w, r)
	}))
	defer ts.Close()

	client := rpc.NewClient(ts.URL, "", "")

	result, err := client.Call("nonexistent_method")
	if err != nil {
		t.Fatalf("unknown method: %v", err)
	}
	if !contains(result, "Unknown") {
		t.Errorf("unknown method: expected 'Unknown' in result, got %s", result)
	}
}

func TestRPCEmptyDongle(t *testing.T) {
	d := simulator.NewEmptyDongle()
	port := simulator.NewSimPort(d)

	srv := rpc.NewServerWithConfig(port, "", "")

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		srv.HandleRPC(w, r)
	}))
	defer ts.Close()

	client := rpc.NewClient(ts.URL, "", "")

	result, err := client.Call("ble_cmd", "switch")
	if err != nil {
		t.Fatalf("switch on empty: %v", err)
	}
	if result != "FAIL" {
		t.Errorf("switch on empty: expected FAIL, got %s", result)
	}

	result, err = client.Call("ble_cmd", "devname")
	if err != nil {
		t.Fatalf("devname on empty: %v", err)
	}
	if result != "NONE" {
		t.Errorf("devname on empty: expected NONE, got %s", result)
	}
}

// Helper to make the HandleRPC method accessible for httptest
func init() {
	_ = fmt.Sprintf // ensure fmt is imported
}
