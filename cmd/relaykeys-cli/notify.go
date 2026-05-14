package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
)

func iconPath() string {
	exe, _ := os.Executable()
	candidates := []string{
		filepath.Join(filepath.Dir(exe), "assets", "icons", "logo.png"),
		filepath.Join(filepath.Dir(exe), "..", "assets", "icons", "logo.png"),
		"assets/icons/logo.png",
	}
	for _, p := range candidates {
		if _, err := os.Stat(p); err == nil {
			abs, _ := filepath.Abs(p)
			return abs
		}
	}
	return ""
}

func sendNotification(title, message string) error {
	switch runtime.GOOS {
	case "windows":
		escapedTitle := escapePS(title)
		escapedMsg := escapePS(message)
		iconXML := ""
		if icon := iconPath(); icon != "" {
			iconXML = fmt.Sprintf(`<image id="3" src="file:///%s" />`, escapePS(icon))
		}
		template := fmt.Sprintf(
			`<toast><visual><binding template="ToastText02"><text id="1">%s</text><text id="2">%s</text>%s</binding></visual></toast>`,
			escapedTitle, escapedMsg, iconXML,
		)
		script := fmt.Sprintf(
			`[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null; [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom, ContentType = WindowsRuntime] > $null; $xml = New-Object Windows.Data.Xml.Dom.XmlDocument; $xml.LoadXml('%s'); $toast = [Windows.UI.Notifications.ToastNotification]::new($xml); [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("RelayKeys").Show($toast)`,
			template,
		)
		return exec.Command("powershell.exe", "-NoProfile", "-Command", script).Run()
	case "darwin":
		return exec.Command("osascript", "-e",
			fmt.Sprintf(`display notification "%s" with title "%s"`, escapeApple(message), escapeApple(title)),
		).Run()
	case "linux":
		icon := iconPath()
		if icon != "" {
			return exec.Command("notify-send", "-i", icon, title, message).Run()
		}
		return exec.Command("notify-send", title, message).Run()
	default:
		return fmt.Errorf("notifications not supported on %s", runtime.GOOS)
	}
}

func escapePS(s string) string {
	r := make([]byte, 0, len(s)*2)
	for _, c := range s {
		switch c {
		case '\'':
			r = append(r, "''"...)
		case '"':
			r = append(r, "&quot;"...)
		case '<':
			r = append(r, "&lt;"...)
		case '>':
			r = append(r, "&gt;"...)
		case '&':
			r = append(r, "&amp;"...)
		case '\n':
			r = append(r, "&#10;"...)
		default:
			r = append(r, string(c)...)
		}
	}
	return string(r)
}

func escapeApple(s string) string {
	r := make([]byte, 0, len(s)*2)
	for _, c := range s {
		if c == '"' {
			r = append(r, `\"`...)
		} else if c == '\\' {
			r = append(r, `\\`...)
		} else {
			r = append(r, string(c)...)
		}
	}
	return string(r)
}
