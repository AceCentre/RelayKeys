//go:build windows

package main

import (
	_ "embed"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"runtime"
	"strings"
	"time"

	"github.com/getlantern/systray"
)

var rpcURL = "http://127.0.0.1:5383/"

//go:embed icon_connected.ico
var iconConnected []byte

//go:embed icon_disconnected.ico
var iconDisconnected []byte

func main() {
	systray.Run(onReady, onExit)
}

func onReady() {
	systray.SetTitle("RK")
	systray.SetTooltip("RelayKeys")
	systray.SetIcon(iconDisconnected)

	mStatus := systray.AddMenuItem("Dongle: Checking...", "")
	mStatus.Disable()

	systray.AddSeparator()

	mOpen := systray.AddMenuItem("Open Web UI", "")
	mSwitch := systray.AddMenuItem("Switch Device", "")
	mRestart := systray.AddMenuItem("Restart Service", "")

	systray.AddSeparator()

	mQuit := systray.AddMenuItem("Quit", "")

	go pollStatus(mStatus)

	go func() {
		for {
			select {
			case <-mOpen.ClickedCh:
				openBrowser()
			case <-mSwitch.ClickedCh:
				sendRPC("ble_cmd", `[["switch"]]`)
			case <-mRestart.ClickedCh:
				restartService()
			case <-mQuit.ClickedCh:
				systray.Quit()
			}
		}
	}()
}

func onExit() {}

func pollStatus(mStatus *systray.MenuItem) {
	for {
		dongleStatus, deviceName := getStatus()
		if dongleStatus == "Connected" {
			systray.SetIcon(iconConnected)
			systray.SetTooltip("RelayKeys — " + deviceName)
			if deviceName != "" && deviceName != "NONE" {
				mStatus.SetTitle("Device: " + deviceName)
			} else {
				mStatus.SetTitle("Dongle: Connected (no device)")
			}
		} else {
			systray.SetIcon(iconDisconnected)
			systray.SetTooltip("RelayKeys — Disconnected")
			mStatus.SetTitle("Dongle: Not connected")
		}
		time.Sleep(5 * time.Second)
	}
}

func getStatus() (string, string) {
	client := &http.Client{Timeout: 2 * time.Second}

	body := `{"jsonrpc":"2.0","method":"daemon","params":[["dongle_status"]],"id":1}`
	resp, err := client.Post(rpcURL, "application/json", strings.NewReader(body))
	if err != nil {
		return "Disconnected", ""
	}
	defer resp.Body.Close()

	var result struct {
		Result string `json:"result"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "Disconnected", ""
	}
	if result.Result != "Connected" {
		return result.Result, ""
	}

	body2 := `{"jsonrpc":"2.0","method":"ble_cmd","params":[["devname"]],"id":2}`
	resp2, err := client.Post(rpcURL, "application/json", strings.NewReader(body2))
	if err != nil {
		return "Connected", ""
	}
	defer resp2.Body.Close()

	var result2 struct {
		Result string `json:"result"`
	}
	if err := json.NewDecoder(resp2.Body).Decode(&result2); err != nil {
		return "Connected", ""
	}
	return "Connected", result2.Result
}

func sendRPC(method string, params string) {
	client := &http.Client{Timeout: 3 * time.Second}
	body := fmt.Sprintf(`{"jsonrpc":"2.0","method":"%s","params":%s,"id":1}`, method, params)
	resp, err := client.Post(rpcURL, "application/json", strings.NewReader(body))
	if err != nil {
		return
	}
	resp.Body.Close()
}

func openBrowser() {
	url := rpcURL + "ui/"
	switch runtime.GOOS {
	case "windows":
		exec.Command("rundll32.exe", "url.dll,FileProtocolHandler", url).Start()
	case "darwin":
		exec.Command("open", url).Start()
	case "linux":
		exec.Command("xdg-open", url).Start()
	}
}

func restartService() {
	switch runtime.GOOS {
	case "windows":
		exec.Command("net", "stop", "RelayKeys").Run()
		exec.Command("net", "start", "RelayKeys").Run()
	case "darwin":
		exec.Command("launchctl", "unload", "~/Library/LaunchAgents/com.acecentre.relaykeys.plist").Run()
		exec.Command("launchctl", "load", "~/Library/LaunchAgents/com.acecentre.relaykeys.plist").Run()
	}
}

func init() {
	if len(os.Args) > 1 {
		if os.Args[1] == "--url" && len(os.Args) > 2 {
			rpcURL = os.Args[2]
		}
	}
}
