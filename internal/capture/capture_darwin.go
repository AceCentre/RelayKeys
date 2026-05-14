//go:build darwin

package capture

/*
#cgo CFLAGS: -x objective-c
#cgo LDFLAGS: -framework CoreGraphics -framework Carbon

#include <Carbon/Carbon.h>
#include <CoreGraphics/CoreGraphics.h>

extern void goKeyboardCallback(CGKeyCode code, int down);
extern void goMouseCallback(int dx, int dy, int button, int down, int scrollY);

static CGEventRef eventCallback(CGEventTapProxy proxy, CGEventType type, CGEventRef event, void *userInfo) {
    if (type == kCGEventKeyDown || type == kCGEventKeyUp) {
        CGKeyCode code = (CGKeyCode)CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode);
        int down = (type == kCGEventKeyDown) ? 1 : 0;
        goKeyboardCallback(code, down);
    } else if (type == kCGEventMouseMoved || type == kCGEventLeftMouseDragged || type == kCGEventRightMouseDragged || type == kCGEventOtherMouseDragged) {
        CGPoint loc = CGEventGetLocation(event);
        static double lastX = 0, lastY = 0;
        int dx = (int)(loc.x - lastX);
        int dy = (int)(loc.y - lastY);
        lastX = loc.x;
        lastY = loc.y;
        if (dx != 0 || dy != 0) {
            goMouseCallback(dx, dy, 0, 0, 0);
        }
    } else if (type == kCGEventLeftMouseDown || type == kCGEventLeftMouseUp ||
               type == kCGEventRightMouseDown || type == kCGEventRightMouseUp ||
               type == kCGEventOtherMouseDown || type == kCGEventOtherMouseUp) {
        int64_t btn = CGEventGetIntegerValueField(event, kCGMouseEventButtonNumber);
        int down = (type == kCGEventLeftMouseDown || type == kCGEventRightMouseDown || type == kCGEventOtherMouseDown) ? 1 : 0;
        goMouseCallback(0, 0, (int)btn, down, 0);
    } else if (type == kCGEventScrollWheel) {
        int64_t dy = CGEventGetIntegerValueField(event, kCGScrollWheelEventDeltaAxis1);
        goMouseCallback(0, 0, 0, 0, (int)dy);
    }
    return event;
}

static void *createEventTap() {
    CGEventMask mask = CGEventMaskBit(kCGEventKeyDown) | CGEventMaskBit(kCGEventKeyUp) |
                       CGEventMaskBit(kCGEventMouseMoved) | CGEventMaskBit(kCGEventLeftMouseDragged) |
                       CGEventMaskBit(kCGEventRightMouseDragged) | CGEventMaskBit(kCGEventOtherMouseDragged) |
                       CGEventMaskBit(kCGEventLeftMouseDown) | CGEventMaskBit(kCGEventLeftMouseUp) |
                       CGEventMaskBit(kCGEventRightMouseDown) | CGEventMaskBit(kCGEventRightMouseUp) |
                       CGEventMaskBit(kCGEventOtherMouseDown) | CGEventMaskBit(kCGEventOtherMouseUp) |
                       CGEventMaskBit(kCGEventScrollWheel);
    CFMachPortRef tap = CGEventTapCreate(kCGSessionEventTap, kCGHeadInsertEventTap, kCGEventTapOptionListenOnly, mask, eventCallback, NULL);
    return (void *)tap;
}

static void runTap(void *tap) {
    CFRunLoopSourceRef src = CFMachPortCreateRunLoopSource(kCFAllocatorDefault, (CFMachPortRef)tap, 0);
    CFRunLoopAddSource(CFRunLoopGetCurrent(), src, kCFRunLoopCommonModes);
    CFRelease(src);
    CGEventTapEnable((CFMachPortRef)tap, true);
    CFRunLoopRun();
}

static void stopTap(void *tap) {
    CFRunLoopStop(CFRunLoopGetCurrent());
    CGEventTapEnable((CFMachPortRef)tap, false);
}
*/
import "C"
import (
	"log"
	"runtime"
)

var globalCapture *Capture

func init() {
	runtime.LockOSThread()
}

func (c *Capture) startPlatform() error {
	globalCapture = c

	tap := C.createEventTap()
	if tap == nil {
		log.Println("[Capture] macOS: CGEventTap creation failed — check Accessibility permissions")
		c.mu.Lock()
		c.active = false
		c.mu.Unlock()
		return nil
	}

	go func() {
		runtime.LockOSThread()
		C.runTap(tap)
	}()

	go func() {
		<-c.stop
		C.stopTap(tap)
	}()

	return nil
}

//export goKeyboardCallback
func goKeyboardCallback(code C.CGKeyCode, down C.int) {
	if globalCapture == nil {
		return
	}
	key := macKeyCodeToHID(int(code))
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
			Type:   "mousemove",
			DX:     int(dx),
			DY:     int(dy),
		})
	}
	if int(button) != 0 && (int(down) == 1 || int(down) == 0) {
		btn := "l"
		if int(button) == 1 {
			btn = "r"
		} else if int(button) == 2 {
			btn = "m"
		}
		globalCapture.emit(Event{
			Type:   "mousebutton",
			Button: btn,
			Down:   int(down) == 1,
		})
	}
	if int(scrollY) != 0 {
		globalCapture.emit(Event{
			Type:   "mousescroll",
			WheelY: int(scrollY),
		})
	}
}

func macKeyCodeToHID(code int) string {
	m := map[int]string{
		0: "A", 1: "S", 2: "D", 3: "F", 4: "H", 5: "G", 6: "Z", 7: "X",
		8: "C", 9: "V", 11: "B", 12: "Q", 13: "W", 14: "E", 15: "R",
		16: "Y", 17: "T", 18: "1", 19: "2", 20: "3", 21: "4", 22: "6",
		23: "5", 24: "=", 25: "9", 26: "7", 27: "-", 28: "8", 29: "0",
		30: "]", 31: "O", 32: "U", 33: "[", 34: "I", 35: "P",
		36: "ENTER", 37: "L", 38: "J", 39: "'", 40: "K", 41: ";",
		42: "\\", 43: ",", 44: "/", 45: "N", 46: "M", 47: ".",
		48: "TAB", 49: "SPACE", 50: "`", 51: "BACKSPACE",
		96: "F5", 97: "F6", 98: "F7", 99: "F3", 100: "F8",
		101: "F9", 103: "F11", 105: "F13", 107: "F14", 109: "F10",
		111: "F12", 113: "F15", 118: "F4", 119: "END", 120: "F2",
		121: "PAGEDOWN", 122: "F1", 123: "LEFT", 124: "RIGHT",
		125: "DOWN", 126: "UP",
	}
	if name, ok := m[code]; ok {
		return name
	}
	return ""
}
