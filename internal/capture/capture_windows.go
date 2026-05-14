//go:build windows

package capture

/*
#cgo LDFLAGS: -luser32

#include <windows.h>

extern void goKeyboardCallback(DWORD vkCode, int down);
extern void goMouseCallback(int dx, int dy, int button, int down, int scrollY);

static POINT lastMousePos = {0, 0};

LRESULT CALLBACK keyboardHook(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode >= 0) {
        KBDLLHOOKSTRUCT *kb = (KBDLLHOOKSTRUCT *)lParam;
        int down = (wParam == WM_KEYDOWN || wParam == WM_SYSKEYDOWN) ? 1 : 0;
        goKeyboardCallback(kb->vkCode, down);
    }
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

LRESULT CALLBACK mouseHook(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode >= 0) {
        MSLLHOOKSTRUCT *ms = (MSLLHOOKSTRUCT *)lParam;

        switch (wParam) {
        case WM_MOUSEMOVE: {
            int dx = (int)(ms->pt.x - lastMousePos.x);
            int dy = (int)(ms->pt.y - lastMousePos.y);
            lastMousePos = ms->pt;
            if (dx != 0 || dy != 0) {
                goMouseCallback(dx, dy, 0, 0, 0);
            }
            break;
        }
        case WM_LBUTTONDOWN: goMouseCallback(0, 0, 0, 1, 0); break;
        case WM_LBUTTONUP:   goMouseCallback(0, 0, 0, 0, 0); break;
        case WM_RBUTTONDOWN: goMouseCallback(0, 0, 1, 1, 0); break;
        case WM_RBUTTONUP:   goMouseCallback(0, 0, 1, 0, 0); break;
        case WM_MBUTTONDOWN: goMouseCallback(0, 0, 2, 1, 0); break;
        case WM_MBUTTONUP:   goMouseCallback(0, 0, 2, 0, 0); break;
        case WM_XBUTTONDOWN: goMouseCallback(0, 0, (int)(ms->mouseData >> 16), 1, 0); break;
        case WM_XBUTTONUP:   goMouseCallback(0, 0, (int)(ms->mouseData >> 16), 0, 0); break;
        case WM_MOUSEWHEEL: {
            int scrollY = (short)HIWORD(ms->mouseData) / WHEEL_DELTA;
            goMouseCallback(0, 0, 0, 0, scrollY);
            break;
        }
        case WM_MOUSEHWHEEL: {
            int scrollX = (short)HIWORD(ms->mouseData) / WHEEL_DELTA;
            goMouseCallback(scrollX, 0, 0, 0, 0);
            break;
        }
        }
    }
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

static HHOOK kbHook = NULL;
static HHOOK msHook = NULL;

static void installHooks() {
    kbHook = SetWindowsHookExA(WH_KEYBOARD_LL, keyboardHook, GetModuleHandle(NULL), 0);
    msHook = SetWindowsHookExA(WH_MOUSE_LL, mouseHook, GetModuleHandle(NULL), 0);
}

static void runMessageLoop() {
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0) > 0) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
}

static void removeHooks() {
    if (kbHook) { UnhookWindowsHookEx(kbHook); kbHook = NULL; }
    if (msHook) { UnhookWindowsHookEx(msHook); msHook = NULL; }
}
*/
import "C"
import (
	"log"
	"strings"
)

var globalCapture *Capture

func (c *Capture) startPlatform() error {
	globalCapture = c

	C.installHooks()
	if C.kbHook == nil && C.msHook == nil {
		log.Println("[Capture] Windows: SetWindowsHookEx failed")
		c.mu.Lock()
		c.active = false
		c.mu.Unlock()
		return nil
	}

	go func() {
		C.runMessageLoop()
	}()

	go func() {
		<-c.stop
		C.removeHooks()
	}()

	log.Println("[Capture] Windows: hooks installed")
	return nil
}

//export goKeyboardCallback
func goKeyboardCallback(vkCode C.DWORD, down C.int) {
	if globalCapture == nil {
		return
	}
	key := winVKToHID(int(vkCode))
	if key == "" {
		return
	}
	if IsModifier(key) {
		globalCapture.emit(Event{
			Type: "keyevent",
			Key:  key,
			Down: int(down) == 1,
		})
		return
	}
	globalCapture.emit(Event{
		Type: "keyevent",
		Key:  key,
		Down: int(down) == 1,
	})
}

//export goMouseCallback
func goMouseCallback(dx, dy, button, down, scrollY C.int) {
	if globalCapture == nil {
		return
	}
	if int(dx) != 0 || int(dy) != 0 {
		globalCapture.emit(Event{
			Type: "mousemove",
			DX:   int(dx),
			DY:   int(dy),
		})
	}
	if int(button) != 0 || int(down) != 0 || int(scrollY) == 0 {
		if int(down) == 1 || int(down) == 0 {
			btn := ""
			switch int(button) {
			case 0:
				btn = "l"
			case 1:
				btn = "r"
			case 2:
				btn = "m"
			default:
				return
			}
			globalCapture.emit(Event{
				Type:   "mousebutton",
				Button: btn,
				Down:   int(down) == 1,
			})
		}
	}
	if int(scrollY) != 0 {
		globalCapture.emit(Event{
			Type:   "mousescroll",
			WheelY: int(scrollY),
		})
	}
}

func winVKToHID(vk int) string {
	m := map[int]string{
		0x08: "BACKSPACE", 0x09: "TAB", 0x0D: "ENTER", 0x1B: "ESCAPE",
		0x20: "SPACE", 0x21: "PAGEUP", 0x22: "PAGEDOWN", 0x23: "END",
		0x24: "HOME", 0x25: "LEFT", 0x26: "UP", 0x27: "RIGHT", 0x28: "DOWN",
		0x2C: "PRINTSCREEN", 0x2D: "INSERT", 0x2E: "DELETE",
		0x30: "0", 0x31: "1", 0x32: "2", 0x33: "3", 0x34: "4",
		0x35: "5", 0x36: "6", 0x37: "7", 0x38: "8", 0x39: "9",
		0x41: "A", 0x42: "B", 0x43: "C", 0x44: "D", 0x45: "E",
		0x46: "F", 0x47: "G", 0x48: "H", 0x49: "I", 0x4A: "J",
		0x4B: "K", 0x4C: "L", 0x4D: "M", 0x4E: "N", 0x4F: "O",
		0x50: "P", 0x51: "Q", 0x52: "R", 0x53: "S", 0x54: "T",
		0x55: "U", 0x56: "V", 0x57: "W", 0x58: "X", 0x59: "Y",
		0x5A: "Z",
		0x5B: "LMETA", 0x5C: "RMETA",
		0x60: "KP0", 0x61: "KP1", 0x62: "KP2", 0x63: "KP3",
		0x64: "KP4", 0x65: "KP5", 0x66: "KP6", 0x67: "KP7",
		0x68: "KP8", 0x69: "KP9",
		0x6A: "KP_MULTIPLY", 0x6B: "KP_PLUS", 0x6D: "KP_MINUS",
		0x6E: "KP_PERIOD", 0x6F: "KP_DIVIDE",
		0x70: "F1", 0x71: "F2", 0x72: "F3", 0x73: "F4",
		0x74: "F5", 0x75: "F6", 0x76: "F7", 0x77: "F8",
		0x78: "F9", 0x79: "F10", 0x7A: "F11", 0x7B: "F12",
		0x90: "NUMLOCK", 0x91: "SCROLLOCK", 0x14: "CAPSLOCK",
		0xA0: "LSHIFT", 0xA1: "RSHIFT", 0xA2: "LCTRL", 0xA3: "RCTRL",
		0xA4: "LALT", 0xA5: "RALT",
		0xAD: "MUTE", 0xAE: "VOLDOWN", 0xAF: "VOLUP",
		0xBA: "SEMICOLON", 0xBB: "EQUALS", 0xBC: "COMMA",
		0xBD: "MINUS", 0xBE: "PERIOD", 0xBF: "SLASH",
		0xC0: "BACKQUOTE",
		0xDB: "LEFTBRACKET", 0xDC: "BACKSLASH", 0xDD: "RIGHTBRACKET",
		0xDE: "QUOTE",
	}
	if name, ok := m[vk]; ok {
		return name
	}
	return ""
}

func init() {
	_ = strings.TrimSpace
}
