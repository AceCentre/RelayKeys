//go:build darwin

package main

/*
#cgo LDFLAGS: -framework Cocoa
#include <stdlib.h>

extern void runMenuBarApp();
extern void cocoaUpdateStatus(const char* device, int connected);
*/
import "C"
import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"runtime"
	"strings"
	"time"
	"unsafe"
)

var menuBarApp *menuBar

type menuBar struct {
	rpcURL string
}

func newMenuBar(rpcURL string) *menuBar {
	return &menuBar{rpcURL: rpcURL}
}

func (m *menuBar) run() {
	menuBarApp = m
	go m.pollStatus()
	C.runMenuBarApp()
}

func (m *menuBar) updateStatus(device string, connected bool) {
	cDev := C.CString(device)
	defer C.free(unsafe.Pointer(cDev))
	conn := 0
	if connected {
		conn = 1
	}
	C.cocoaUpdateStatus(cDev, C.int(conn))
}

func (m *menuBar) pollStatus() {
	for {
		name, connected := m.getStatus()
		m.updateStatus(name, connected)
		time.Sleep(5 * time.Second)
	}
}

func (m *menuBar) getStatus() (string, bool) {
	client := &http.Client{Timeout: 2 * time.Second}
	body := fmt.Sprintf(`{"jsonrpc":"2.0","method":"daemon","params":[["dongle_status"]],"id":1}`)
	resp, err := client.Post(m.rpcURL, "application/json", strings.NewReader(body))
	if err != nil {
		return "", false
	}
	defer resp.Body.Close()

	var result struct {
		Result string `json:"result"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", false
	}
	if result.Result != "Connected" {
		return "", false
	}

	body2 := fmt.Sprintf(`{"jsonrpc":"2.0","method":"ble_cmd","params":[["devname"]],"id":2}`)
	resp2, err := client.Post(m.rpcURL, "application/json", strings.NewReader(body2))
	if err != nil {
		return "Connected", true
	}
	defer resp2.Body.Close()

	var result2 struct {
		Result string `json:"result"`
	}
	if err := json.NewDecoder(resp2.Body).Decode(&result2); err != nil {
		return "Connected", true
	}
	return result2.Result, true
}

func (m *menuBar) sendRPC(method string, params string) {
	client := &http.Client{Timeout: 3 * time.Second}
	body := fmt.Sprintf(`{"jsonrpc":"2.0","method":"%s","params":%s,"id":1}`, method, params)
	resp, err := client.Post(m.rpcURL, "application/json", strings.NewReader(body))
	if err != nil {
		return
	}
	resp.Body.Close()
}

//export goClickOpen
func goClickOpen() {
	exec.Command("open", menuBarApp.rpcURL+"/ui/").Start()
}

//export goClickCapture
func goClickCapture() {
	menuBarApp.sendRPC("ble_cmd", `[["keyboard_release"]]`)
}

//export goClickSwitch
func goClickSwitch() {
	menuBarApp.sendRPC("ble_cmd", `[["switch"]]`)
}

//export goClickQuit
func goClickQuit() {
	os.Exit(0)
}

func main() {
	runtime.LockOSThread()
	app := newMenuBar("http://127.0.0.1:5383")
	app.run()
}
